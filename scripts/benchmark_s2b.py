"""Deterministic S2B pattern baseline; it consumes only local replay fixtures."""

from __future__ import annotations

import argparse
import gc
import hashlib
import json
import platform
import statistics
import sys
import time
import tracemalloc
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "apps" / "backend" / "src"))

from hct_backend.contracts import Environment, IdentityKind, StableId
from hct_backend.features import FeatureSample
from hct_backend.market_truth import (
    ChannelCapability,
    ChannelVisibility,
    ClockHealth,
    GenerationRef,
    LifecycleRestriction,
    MarketStateSnapshot,
    MarketStateTrust,
    QualityAssessment,
    ResourceAdmissionEvidence,
    ResourceDisposition,
    SequenceMode,
    SequenceObservation,
    SynchronizationProof,
    UpdateSemantics,
    derive_data_authority,
    evaluate_sequence,
)
from hct_backend.patterns import (
    PATTERN_ALLOWLIST,
    PatternConstituent,
    PatternEvaluationState,
    PatternMatchState,
    PatternRegistry,
    PatternValidity,
    PatternVersion,
)
from hct_backend.patterns import evaluate_patterns as evaluate_all_patterns
from hct_backend.quota_governor import (
    AdmissionDecision,
    AdmissionOutcome,
    AdmissionReason,
)
from hct_backend.s1f_numeric import DecimalValue
from hct_backend.s1f_values import (
    CandleBar,
    CandleCloseProof,
    Finality,
    OrderedLineage,
    ProviderTransactionAmount,
    Quantity,
    QuantityUnit,
    Timeframe,
    ValueContext,
)

MODE = "S2B_BASELINE_ESTABLISHMENT_V1"
FIXTURE_VERSION = "S2B_PATTERN_FIXTURE_V1"
BENCHMARK_SEED = 0
PROFILE_CARDINALITY = {
    "MICRO": (1, 2048),
    "NOMINAL": (8, 4096),
    "STRESS": (16, 8192),
}
TIMEFRAMES = (Timeframe("Min1", 60), Timeframe("Min5", 300), Timeframe("Min15", 900))
# The frozen profile cardinality fixes the corpus. Pattern evaluation runs over a
# deterministic bounded sample of that corpus so the baseline completes in bounded
# time; the stride and the evaluated-window count are recorded in the profile result.
WINDOW_EVALUATION_BUDGET = 512
SOURCE = StableId(kind=IdentityKind.EXCHANGE, value="fixture")
PROVENANCE = "b" * 64
NOW = datetime(2026, 1, 1, tzinfo=UTC)


class BenchmarkValidationError(RuntimeError):
    """Raised when a benchmark document fails a mandatory correctness gate."""


def _generation() -> GenerationRef:
    return GenerationRef(SOURCE, Environment.REPLAY, 1)


def _capability(contract: StableId) -> ChannelCapability:
    return ChannelCapability(
        source_id=SOURCE,
        visibility=ChannelVisibility.PUBLIC,
        channel="replay.events",
        contract_scope=contract,
        schema_version=1,
        snapshot_available=True,
        update_semantics=UpdateSemantics.SNAPSHOT_AND_DELTA,
        ordering_evidence="fixture-sequenced",
        sequence_field="update-id",
        cadence_ms=100,
        heartbeat_ms=500,
        mode=SequenceMode.STRICT_SEQUENCE,
        contiguous_proof=False,
    )


def _resource(disposition: ResourceDisposition) -> ResourceAdmissionEvidence:
    canonical = {
        ResourceDisposition.AVAILABLE: (
            AdmissionOutcome.ADMIT,
            AdmissionReason.ADMITTED,
        ),
        ResourceDisposition.DEGRADED: (
            AdmissionOutcome.DEFER,
            AdmissionReason.QUEUE_FULL,
        ),
        ResourceDisposition.DENIED: (AdmissionOutcome.SHED, AdmissionReason.QUEUE_FULL),
        ResourceDisposition.UNKNOWN: (
            AdmissionOutcome.UNKNOWN,
            AdmissionReason.UNKNOWN_BUDGET,
        ),
    }[disposition]
    return ResourceAdmissionEvidence.from_admission(
        AdmissionDecision.create(
            outcome=canonical[0],
            reason=canonical[1],
            material={"fixture": disposition.value},
        )
    )


def _state(
    contract: StableId,
    *,
    trust: MarketStateTrust = MarketStateTrust.TRUSTED,
    lifecycle: LifecycleRestriction = LifecycleRestriction.NONE,
    resource: ResourceDisposition = ResourceDisposition.AVAILABLE,
    event_number: int = 99,
) -> MarketStateSnapshot:
    capability = _capability(contract)
    observation = SequenceObservation(
        generation=_generation(),
        observed_at=NOW,
        event_fingerprint=(str(event_number) * 64)[:64],
        update_id=event_number,
        is_snapshot=True,
        source_id=SOURCE,
        channel="replay.events",
        contract_id=contract,
        schema_version=1,
        capability_fingerprint=capability.fingerprint,
        capability_policy_version=capability.policy_version,
        visibility=ChannelVisibility.PUBLIC,
    )
    evaluation = evaluate_sequence(capability, None, observation)
    proof = SynchronizationProof.from_sequence_evaluation(
        capability=capability,
        generation=_generation(),
        evaluation=evaluation,
    )
    return MarketStateSnapshot(
        contract_id=contract,
        environment=Environment.REPLAY,
        generation=_generation(),
        source_id=SOURCE,
        source_version=1,
        provenance_fingerprint=PROVENANCE,
        event_fingerprints=(
            proof.synchronization_anchor_fingerprint,
            proof.latest_event_fingerprint,
        ),
        trust=trust,
        data_authority=derive_data_authority(
            QualityAssessment(
                age_ms=10,
                freshness_limit_ms=100,
                sequence=evaluation,
                clock=ClockHealth.HEALTHY,
                schema_valid=True,
                provenance_valid=True,
                generation_valid=True,
                coherent=True,
                resource=_resource(resource),
                contradiction=False,
                explanatory_score=99,
            )
        ),
        synchronized=True,
        synchronization_proof=proof,
        capability_fingerprint=capability.fingerprint,
        capability_policy_version=capability.policy_version,
        channel=capability.channel,
        schema_version=capability.schema_version,
        visibility=capability.visibility,
        lifecycle_restriction=lifecycle,
    )


def _body_shape(index: int) -> tuple[str, str, str, str]:
    """Deterministic OHLC corpus covering matches, non-matches and boundaries."""

    base = Decimal(100 + (index % 97))
    half = Decimal("0.5")
    small = Decimal("0.05")
    tiny = Decimal("0.1")
    selector = index % 12
    if selector == 0:
        return (str(base), str(base + 1), str(base - 1), str(base))
    if selector == 1:
        return (str(base), str(base + 6), str(base), str(base + 6))
    if selector == 2:
        return (str(base + 5), str(base + 5), str(base - 5), str(base - 5))
    if selector == 3:
        return (str(base + 4), str(base + 4), str(base - 4), str(base - 4))
    if selector == 4:
        return (str(base - 3), str(base + 5), str(base - 3), str(base + 4))
    if selector == 5:
        return (str(base + 3), str(base + 5), str(base - 5), str(base - 4))
    if selector == 6:
        return (str(base + 10), str(base + 10), str(base - 1), str(base - half))
    if selector == 7:
        return (
            str(base - tiny),
            str(base + tiny + tiny),
            str(base - tiny - tiny),
            str(base - small),
        )
    if selector == 8:
        return (
            str(base - half),
            str(base + 12),
            str(base - half),
            str(base + 12 - half),
        )
    if selector == 9:
        return (
            str(base + half),
            str(base + half),
            str(base - 12),
            str(base - 12 + half),
        )
    if selector == 10:
        return (str(base), str(base), str(base), str(base))
    return (str(base), str(base + 2), str(base - 2), str(base + 1))


def _event_fingerprint(event_number: int) -> str:
    return (str(event_number) * 64)[:64]


def _candle(
    contract: StableId,
    frame: Timeframe,
    index: int,
    shape: tuple[str, str, str, str],
    event_number: int = 99,
) -> CandleBar:
    start = NOW + timedelta(seconds=index * frame.duration_seconds)
    context = ValueContext(
        SOURCE,
        "replay.kline",
        contract,
        Environment.REPLAY,
        _generation(),
        1,
        PROVENANCE,
        _event_fingerprint(event_number),
        start,
        start,
        start,
        index,
    )
    return CandleBar(
        context,
        frame,
        start,
        start + timedelta(seconds=frame.duration_seconds),
        DecimalValue.parse(shape[0]),
        DecimalValue.parse(shape[1]),
        DecimalValue.parse(shape[2]),
        DecimalValue.parse(shape[3]),
        Quantity(
            DecimalValue.parse(str(1 + (index % 11))),
            QuantityUnit.CONTRACTS_PROVIDER_NATIVE_V1,
            FIXTURE_VERSION,
        ),
        ProviderTransactionAmount(DecimalValue.parse("100"), FIXTURE_VERSION),
        Finality.OPEN,
        OrderedLineage.from_fingerprints(("%064x" % (index + 3),), start),
    )


def _corpus(
    contract: StableId,
    frame: Timeframe,
    count: int,
    state: MarketStateSnapshot,
    *,
    event_number: int = 99,
) -> tuple[PatternConstituent, ...]:
    """Build ``count`` CLOSED paired constituents with typed close proofs."""

    opened = tuple(
        _candle(contract, frame, index, _body_shape(index), event_number)
        for index in range(count + 1)
    )
    closed = tuple(
        replace(
            current,
            finality=Finality.CLOSED,
            close_proof=CandleCloseProof._from_next_window_evidence(
                current_candle=current, next_window=opened[index + 1]
            ),
        )
        for index, current in enumerate(opened[:-1])
    )
    pairs = []
    for index, candle in enumerate(closed):
        pairs.append(
            PatternConstituent(
                candle, FeatureSample.from_candle(candle, market_state=state)
            )
        )
    return tuple(pairs)


def _percentiles(values: list[int]) -> dict[str, float]:
    ordered = sorted(values)
    if len(ordered) == 1:
        only = float(ordered[0])
        return {"p50": only, "p95": only, "p99": only, "max": only}
    quantiles = statistics.quantiles(ordered, n=100, method="inclusive")
    return {
        "p50": quantiles[49],
        "p95": quantiles[94],
        "p99": quantiles[98],
        "max": float(max(ordered)),
    }


def _run_profile(name: str) -> dict[str, object]:
    contracts, pairs_per_contract = PROFILE_CARDINALITY[name]
    registry = PatternRegistry()
    for identifier in PATTERN_ALLOWLIST:
        registry = registry.register(PatternVersion.standard(identifier))
    versions = tuple(
        registry.resolve(identifier, 1) for identifier in PATTERN_ALLOWLIST
    )
    # Each pattern is evaluated only over its own exact evaluable bar cardinality: an
    # overlong window is structurally contradictory and must never be sliced.
    groups = tuple(
        (
            cardinality,
            tuple(item for item in versions if item.bar_cardinality == cardinality),
        )
        for cardinality in sorted({item.bar_cardinality for item in versions})
    )
    latency: dict[str, list[int]] = {
        f"{identifier}|{frame.name}": []
        for identifier in PATTERN_ALLOWLIST
        for frame in TIMEFRAMES
    }
    output_hasher = hashlib.sha256()
    input_manifest = hashlib.sha256()
    counts_validity = {item.value: 0 for item in PatternValidity}
    counts_match = {item.value: 0 for item in PatternMatchState}
    evaluations = 0
    no_lookahead_rejections = 0
    restrictive_count = 0
    boundary_rejections = 0
    over_cardinality_rejections = 0
    chain_evaluations = 0
    chain_links_valid = 0
    correctness_failures = 0
    peak_memory = 0
    steady_memory = 0
    window_depth = 0
    evaluated_windows = 0
    record_stride = 1
    start = time.perf_counter_ns()
    for contract_number in range(contracts):
        contract = StableId(
            kind=IdentityKind.INSTRUMENT, value=f"contract-{contract_number:02d}"
        )
        for frame in TIMEFRAMES:
            input_manifest.update(
                f"{contract_number}:{frame.name}:{pairs_per_contract}\n".encode()
            )
            state = _state(contract)
            memory_probe = contract_number == 0 and frame.name == "Min1"
            if memory_probe:
                tracemalloc.start()
            corpus = _corpus(contract, frame, pairs_per_contract, state)
            required = max(item.bar_cardinality for item in versions)
            window_depth = max(window_depth, required)
            horizon = pairs_per_contract - required + 1
            stride = max(1, -(-horizon // WINDOW_EVALUATION_BUDGET))
            record_stride = stride
            offsets = list(range(0, horizon, stride))[:WINDOW_EVALUATION_BUDGET]
            evaluated_windows += len(offsets)
            for offset in offsets:
                for cardinality, group in groups:
                    window = corpus[offset : offset + cardinality]
                    measured = time.perf_counter_ns()
                    evidences = evaluate_all_patterns(group, window)
                    elapsed = time.perf_counter_ns() - measured
                    share = max(1, len(evidences))
                    for evidence in evidences:
                        latency[f"{evidence.pattern.canonical_id}|{frame.name}"].append(
                            elapsed // share
                        )
                        output_hasher.update(evidence.fingerprint.encode())
                        counts_validity[evidence.validity.value] += 1
                        counts_match[evidence.match_state.value] += 1
                        evaluations += 1
                        if evidence.match_state is PatternMatchState.INDETERMINATE:
                            restrictive_count += 1
                            if evidence.reason in {
                                "PRE_CANONICAL_BOUNDARY",
                                "INSUFFICIENT_REQUIRED_CONSTITUENTS",
                            }:
                                no_lookahead_rejections += 1
            # Deterministic pre-boundary proof: one instant before the canonical
            # boundary the pattern must not be reported as matched.
            for cardinality, group in groups:
                final_window = corpus[-cardinality:]
                boundary = final_window[-1].end
                before = boundary - timedelta(microseconds=1)
                blocked = evaluate_all_patterns(
                    group, final_window, evaluation_time=before
                )
                for item in blocked:
                    evaluations += 1
                    output_hasher.update(item.fingerprint.encode())
                    counts_validity[item.validity.value] += 1
                    counts_match[item.match_state.value] += 1
                    if item.match_state is PatternMatchState.INDETERMINATE:
                        boundary_rejections += 1
                        restrictive_count += 1
                    else:
                        correctness_failures += 1
            # Over-cardinality proof: a presented overlong window must fail closed and
            # must never be sliced to the canonical first k constituents.
            for cardinality, group in groups:
                overlong = corpus[-(cardinality + 1) :]
                if len(overlong) != cardinality + 1:
                    continue
                for item in evaluate_all_patterns(group, overlong):
                    evaluations += 1
                    output_hasher.update(item.fingerprint.encode())
                    counts_validity[item.validity.value] += 1
                    counts_match[item.match_state.value] += 1
                    restrictive_count += 1
                    if (
                        item.validity is PatternValidity.INVALID
                        and item.reason == "OVER_CARDINALITY_WINDOW"
                        and item.match_state is PatternMatchState.INDETERMINATE
                    ):
                        over_cardinality_rejections += 1
                    else:
                        correctness_failures += 1
            # Revision-chain proof: one corrected constituent must derive revision n+1
            # and the exact immediate predecessor fingerprint from the typed chain.
            for cardinality, group in groups:
                chain_window = corpus[-cardinality:]
                heads = {
                    item.pattern.canonical_id: item
                    for item in evaluate_all_patterns(group, chain_window)
                }
                last = chain_window[-1]
                revised_candle = replace(
                    last.candle,
                    revision=last.candle.revision + 1,
                    predecessor_fingerprint=last.candle.fingerprint,
                )
                revised = chain_window[:-1] + (
                    PatternConstituent(
                        revised_candle,
                        FeatureSample.from_candle(revised_candle, market_state=state),
                    ),
                )
                states = {
                    identifier: PatternEvaluationState((item,))
                    for identifier, item in heads.items()
                }
                for successor in evaluate_all_patterns(group, revised, states=states):
                    evaluations += 1
                    chain_evaluations += 1
                    output_hasher.update(successor.fingerprint.encode())
                    counts_validity[successor.validity.value] += 1
                    counts_match[successor.match_state.value] += 1
                    head = heads[successor.pattern.canonical_id]
                    if (
                        successor.revision == head.revision + 1
                        and successor.predecessor_evidence_fingerprint
                        == head.fingerprint
                    ):
                        chain_links_valid += 1
                    else:
                        correctness_failures += 1
            if name == "STRESS":
                # Deterministic adversarial corpus: resource and lifecycle restrictions
                # plus degraded market truth, evaluated over exact cardinality windows.
                restrictive_state = _state(
                    contract,
                    resource=ResourceDisposition.DEGRADED,
                    lifecycle=LifecycleRestriction.NEW_EXPOSURE_DISABLED,
                )
                restricted = _corpus(contract, frame, required, restrictive_state)
                degraded_state = _state(
                    contract, trust=MarketStateTrust.DEGRADED, event_number=97
                )
                degraded = _corpus(
                    contract, frame, required, degraded_state, event_number=97
                )
                for source in (restricted, degraded):
                    for cardinality, group in groups:
                        adversarial = evaluate_all_patterns(
                            group, source[-cardinality:]
                        )
                        for item in adversarial:
                            evaluations += 1
                            output_hasher.update(item.fingerprint.encode())
                            counts_validity[item.validity.value] += 1
                            counts_match[item.match_state.value] += 1
                            if item.match_state is PatternMatchState.INDETERMINATE:
                                restrictive_count += 1
            if memory_probe:
                steady_memory, peak_memory = tracemalloc.get_traced_memory()
                tracemalloc.stop()
            del corpus
    elapsed_ns = time.perf_counter_ns() - start
    return {
        "profile": name,
        "contracts": contracts,
        "closed_pairs_per_contract_per_timeframe": pairs_per_contract,
        "timeframes": [frame.name for frame in TIMEFRAMES],
        "pattern_ids": list(PATTERN_ALLOWLIST),
        "exact_cardinality_groups": [cardinality for cardinality, _ in groups],
        "pattern_evaluations": evaluations,
        "pattern_evaluations_per_second": evaluations / (elapsed_ns / 1_000_000_000),
        "per_pattern_timeframe_latency_ns": {
            key: _percentiles(values) for key, values in latency.items() if values
        },
        "replay_throughput_pairs_per_second": (
            contracts * pairs_per_contract * len(TIMEFRAMES)
        )
        / (elapsed_ns / 1_000_000_000),
        "peak_memory_bytes": peak_memory,
        "steady_memory_bytes": steady_memory,
        "window_buffer_depth": window_depth,
        "window_evaluation_budget": WINDOW_EVALUATION_BUDGET,
        "evaluated_windows": evaluated_windows,
        "window_stride": record_stride,
        "counts_by_pattern_validity": counts_validity,
        "counts_by_pattern_match_state": counts_match,
        "no_lookahead_rejections": no_lookahead_rejections + boundary_rejections,
        "boundary_rejections": boundary_rejections,
        "over_cardinality_rejections": over_cardinality_rejections,
        "revision_chain_probe": {
            "evaluations": chain_evaluations,
            "valid_links": chain_links_valid,
        },
        "restrictive_state_count": restrictive_count,
        "input_manifest_hash": input_manifest.hexdigest(),
        "output_manifest_hash": output_hasher.hexdigest(),
        "correctness": "PASS" if correctness_failures == 0 else "FAIL",
    }


REQUIRED_PROFILES: tuple[str, ...] = ("MICRO", "NOMINAL", "STRESS")

DETERMINISTIC_FIELDS: tuple[str, ...] = (
    "profile",
    "contracts",
    "closed_pairs_per_contract_per_timeframe",
    "timeframes",
    "pattern_ids",
    "pattern_evaluations",
    "exact_cardinality_groups",
    "window_buffer_depth",
    "window_evaluation_budget",
    "evaluated_windows",
    "window_stride",
    "counts_by_pattern_validity",
    "counts_by_pattern_match_state",
    "no_lookahead_rejections",
    "boundary_rejections",
    "over_cardinality_rejections",
    "revision_chain_probe",
    "restrictive_state_count",
    "input_manifest_hash",
    "output_manifest_hash",
    "correctness",
)


def _validate_profile_document(document: dict[str, object], label: str) -> None:
    if document.get("mode") != MODE:
        raise BenchmarkValidationError(f"{label}: unexpected benchmark mode")
    if document.get("fixture_version") != FIXTURE_VERSION:
        raise BenchmarkValidationError(f"{label}: unexpected fixture version")
    if document.get("seed") != BENCHMARK_SEED:
        raise BenchmarkValidationError(f"{label}: unexpected seed")
    profiles = document.get("profiles")
    if not isinstance(profiles, list) or not profiles:
        raise BenchmarkValidationError(f"{label}: benchmark profiles are missing")
    names = [item["profile"] for item in profiles]
    if names != list(REQUIRED_PROFILES):
        raise BenchmarkValidationError(
            f"{label}: expected exactly {list(REQUIRED_PROFILES)}, observed {names}"
        )
    for item in profiles:
        profile = item["profile"]
        contracts, pairs = PROFILE_CARDINALITY[profile]
        if (
            item["contracts"] != contracts
            or item["closed_pairs_per_contract_per_timeframe"] != pairs
        ):
            raise BenchmarkValidationError(
                f"{label}/{profile}: frozen cardinality changed"
            )
        if item["pattern_ids"] != list(PATTERN_ALLOWLIST):
            raise BenchmarkValidationError(
                f"{label}/{profile}: pattern allowlist changed"
            )
        if item["timeframes"] != [frame.name for frame in TIMEFRAMES]:
            raise BenchmarkValidationError(f"{label}/{profile}: timeframe set changed")
        if item["correctness"] != "PASS":
            raise BenchmarkValidationError(
                f"{label}/{profile}: correctness did not pass"
            )
        if item["pattern_evaluations"] <= 0:
            raise BenchmarkValidationError(
                f"{label}/{profile}: no evaluations recorded"
            )
        if item["pattern_evaluations_per_second"] <= 0:
            raise BenchmarkValidationError(
                f"{label}/{profile}: throughput is not positive"
            )
        if item["replay_throughput_pairs_per_second"] <= 0:
            raise BenchmarkValidationError(
                f"{label}/{profile}: replay throughput is not positive"
            )
        if item["peak_memory_bytes"] <= 0:
            raise BenchmarkValidationError(
                f"{label}/{profile}: peak memory is not positive"
            )
        if item["no_lookahead_rejections"] <= 0:
            raise BenchmarkValidationError(
                f"{label}/{profile}: no-lookahead rejections missing"
            )
        if item["counts_by_pattern_match_state"]["INDETERMINATE"] <= 0:
            raise BenchmarkValidationError(
                f"{label}/{profile}: no indeterminate outcomes"
            )
        if item["exact_cardinality_groups"] != sorted(
            {
                PatternVersion.standard(identifier).bar_cardinality
                for identifier in PATTERN_ALLOWLIST
            }
        ):
            raise BenchmarkValidationError(
                f"{label}/{profile}: exact cardinality groups changed"
            )
        if (
            item["counts_by_pattern_validity"]["INVALID"]
            != item["over_cardinality_rejections"]
        ):
            raise BenchmarkValidationError(
                f"{label}/{profile}: INVALID evidence is not exactly the over-cardinality probe"
            )
        if item["counts_by_pattern_validity"]["WARMUP"] != item["boundary_rejections"]:
            raise BenchmarkValidationError(
                f"{label}/{profile}: WARMUP evidence is not exactly the pre-boundary probe"
            )
        if item["boundary_rejections"] <= 0:
            raise BenchmarkValidationError(
                f"{label}/{profile}: pre-boundary rejections were not exercised"
            )
        if item["over_cardinality_rejections"] <= 0:
            raise BenchmarkValidationError(
                f"{label}/{profile}: over-cardinality windows were not rejected"
            )
        chain = item["revision_chain_probe"]
        if chain["evaluations"] <= 0 or chain["valid_links"] != chain["evaluations"]:
            raise BenchmarkValidationError(
                f"{label}/{profile}: revision chain links are not the immediate predecessors"
            )
        if not item["per_pattern_timeframe_latency_ns"]:
            raise BenchmarkValidationError(
                f"{label}/{profile}: latency material is missing"
            )
        for value in item["per_pattern_timeframe_latency_ns"].values():
            if set(value) != {"p50", "p95", "p99", "max"}:
                raise BenchmarkValidationError(
                    f"{label}/{profile}: latency shape is invalid"
                )


def validate_benchmark_documents(
    first: dict[str, object], second: dict[str, object]
) -> None:
    _validate_profile_document(first, "run-a")
    _validate_profile_document(second, "run-b")
    projected = [
        [
            {field: item[field] for field in DETERMINISTIC_FIELDS}
            for item in document["profiles"]
        ]
        for document in (first, second)
    ]
    if projected[0] != projected[1]:
        raise BenchmarkValidationError(
            "deterministic profile projection differs across consecutive runs"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--profile", choices=(*PROFILE_CARDINALITY, "all"), default="all"
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--validate",
        nargs=2,
        type=Path,
        metavar=("FIRST", "SECOND"),
        help="validate two consecutive benchmark documents and fail closed",
    )
    args = parser.parse_args()
    if args.validate is not None:
        first = json.loads(args.validate[0].read_text(encoding="utf-8"))
        second = json.loads(args.validate[1].read_text(encoding="utf-8"))
        validate_benchmark_documents(first, second)
        print(
            "S2B exact profiles, cardinalities, no-lookahead rejections and replay hash "
            "parity across both runs: PASS"
        )
        return 0
    if args.output is None:
        parser.error("--output is required unless --validate is used")
    names = tuple(PROFILE_CARDINALITY) if args.profile == "all" else (args.profile,)
    result: dict[str, object] = {
        "mode": MODE,
        "fixture_version": FIXTURE_VERSION,
        "seed": BENCHMARK_SEED,
        "runtime": f"python-{platform.python_version()}-decimal-pattern-engine",
        "build_identity": {
            "implementation": platform.python_implementation(),
            "release": platform.python_version(),
            "machine": platform.machine(),
            "system": platform.system(),
        },
        "profiles": [_run_profile(name) for name in names],
    }
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    gc.collect()
    if any(item["correctness"] != "PASS" for item in result["profiles"]):
        print("S2B benchmark correctness: FAIL", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
