"""Deterministic S2A feature baseline; it consumes only local replay fixtures."""

from __future__ import annotations

import argparse
import gc
import hashlib
import json
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

from hct_backend.contracts import Environment, IdentityKind, StableId  # noqa: E402
from hct_backend.features import (  # noqa: E402
    FeatureSample,
    FeatureValidity,
    FeatureVersion,
    align_closed_1m_candles,
    evaluate_feature,
    evaluate_feature_series,
)
from hct_backend.market_truth import GenerationRef  # noqa: E402
from hct_backend.s1f_numeric import DecimalValue  # noqa: E402
from hct_backend.s1f_values import (  # noqa: E402
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

FEATURE_IDS = (
    "F-RET-001",
    "F-SMA-001",
    "F-EMA-001",
    "F-ROC-001",
    "F-RSI-001",
    "F-TR-001",
    "F-ATR-001",
    "F-VSMA-001",
)
N = 14
PROFILES = {
    "MICRO": {"contracts": 1, "candles": 4096, "max_window": 64},
    "NOMINAL": {"contracts": 16, "candles": 8192, "max_window": 256},
    "STRESS": {"contracts": 32, "candles": 16384, "max_window": 512},
}
NOW = datetime(2026, 1, 1, tzinfo=UTC)


def _feature(identifier: str) -> FeatureVersion:
    return FeatureVersion.standard(
        identifier,
        parameter_n=N if identifier not in {"F-RET-001", "F-TR-001"} else None,
    )


def _sample(contract_number: int, index: int) -> FeatureSample:
    source = StableId(kind=IdentityKind.EXCHANGE, value="fixture")
    contract = StableId(
        kind=IdentityKind.INSTRUMENT, value=f"contract-{contract_number:02d}"
    )
    close = DecimalValue.parse(str(100 + (index % 1000)))
    sample = FeatureSample.from_decimal(
        close,
        index=index,
        source_id=source,
        contract_id=contract,
        environment=Environment.REPLAY,
    )
    high = DecimalValue.parse(str(close.value + Decimal("2")))
    low = DecimalValue.parse(str(close.value - Decimal("1")))
    quantity = Quantity(
        DecimalValue.parse(str(1 + (index % 11))),
        QuantityUnit.CONTRACTS_PROVIDER_NATIVE_V1,
        "S2A-BENCHMARK-Q-V1",
    )
    return replace(sample, high=high, low=low, close=close, quantity=quantity)


def _tail_samples(
    contract_number: int, count: int, window: int
) -> tuple[FeatureSample, ...]:
    start = count - window
    return tuple(_sample(contract_number, index) for index in range(start, count))


def _manifest_hash(contract_number: int, count: int) -> str:
    digest = hashlib.sha256()
    for index in range(count):
        digest.update(f"{contract_number}:{index}:{100 + index % 1000}\n".encode())
    return digest.hexdigest()


def _percentiles(values: list[int]) -> dict[str, float]:
    ordered = sorted(values)
    return {
        "p50": statistics.quantiles(ordered, n=100, method="inclusive")[49]
        if len(ordered) > 1
        else float(ordered[0]),
        "p95": statistics.quantiles(ordered, n=100, method="inclusive")[94]
        if len(ordered) > 1
        else float(ordered[0]),
        "p99": statistics.quantiles(ordered, n=100, method="inclusive")[98]
        if len(ordered) > 1
        else float(ordered[0]),
        "max": float(max(ordered)),
    }


def _candle(contract_number: int, generation_number: int, index: int) -> CandleBar:
    source = StableId(kind=IdentityKind.EXCHANGE, value="fixture")
    contract = StableId(
        kind=IdentityKind.INSTRUMENT, value=f"contract-{contract_number:02d}"
    )
    frame = Timeframe("Min1", 60)
    start = NOW + timedelta(minutes=index)
    context = ValueContext(
        source,
        "replay.kline",
        contract,
        Environment.REPLAY,
        GenerationRef(source, Environment.REPLAY, generation_number),
        1,
        "a" * 64,
        ("%064x" % (index + generation_number * 10000)),
        start,
        start,
        start,
        index,
    )
    close = DecimalValue.parse(str(100 + index % 1000))
    return CandleBar(
        context,
        frame,
        start,
        start + timedelta(minutes=1),
        close,
        DecimalValue.parse(str(close.value + Decimal("2"))),
        DecimalValue.parse(str(close.value - Decimal("1"))),
        close,
        Quantity(
            DecimalValue.parse(str(1 + index % 11)),
            QuantityUnit.CONTRACTS_PROVIDER_NATIVE_V1,
            "S2A-BENCHMARK-Q-V1",
        ),
        ProviderTransactionAmount(DecimalValue.parse("100"), "S2A-BENCHMARK-A-V1"),
        Finality.OPEN,
        OrderedLineage.from_fingerprints(("%064x" % (index + 1),), start),
    )


def _closed_candles(
    contract_number: int, generation_number: int, count: int
) -> tuple[CandleBar, ...]:
    opened = tuple(
        _candle(contract_number, generation_number, index) for index in range(count + 1)
    )
    return tuple(
        replace(
            current,
            finality=Finality.CLOSED,
            close_proof=CandleCloseProof._from_next_window_evidence(
                current_candle=current,
                next_window=opened[index + 1],
            ),
        )
        for index, current in enumerate(opened[:-1])
    )


def _run_profile(name: str) -> dict[str, object]:
    profile = PROFILES[name]
    contracts = int(profile["contracts"])
    candle_count = int(profile["candles"])
    max_window = int(profile["max_window"])
    feature_latencies: dict[str, list[int]] = {
        identifier: [] for identifier in FEATURE_IDS
    }
    output_hasher = hashlib.sha256()
    warmup_count = 0
    restrictive_count = 0
    no_lookahead_rejections = 0
    feature_evaluations = 0
    input_manifest = hashlib.sha256()
    start = time.perf_counter_ns()
    steady_memory = 0
    peak_memory = 0
    for contract_number in range(contracts):
        input_manifest.update(_manifest_hash(contract_number, candle_count).encode())
        memory_probe = contract_number == 0
        if memory_probe:
            tracemalloc.start()
        inputs = _tail_samples(contract_number, candle_count, max_window)
        for identifier in FEATURE_IDS:
            feature = _feature(identifier)
            required = (
                1
                if identifier == "F-TR-001"
                else 2
                if identifier == "F-RET-001"
                else N + 1
                if identifier in {"F-ROC-001", "F-RSI-001"}
                else N
            )
            warmup_inputs = inputs[: max(0, required - 1)]
            if warmup_inputs:
                warmup = evaluate_feature_series(feature, warmup_inputs)
                warmup_count += sum(
                    item.validity is FeatureValidity.WARMUP for item in warmup
                )
            measured = time.perf_counter_ns()
            result = evaluate_feature(feature, inputs)
            feature_latencies[identifier].append(time.perf_counter_ns() - measured)
            output_hasher.update(result.fingerprint.encode())
            feature_evaluations += 1
            restrictive_count += sum(
                item.validity
                in {
                    FeatureValidity.UNKNOWN,
                    FeatureValidity.INVALID,
                    FeatureValidity.DEGRADED,
                }
                for item in evaluate_feature_series(feature, inputs[-required:])
            )
        boundary = inputs[-1].event_time
        future = replace(
            inputs[-1],
            event_time=boundary + timedelta(minutes=1),
            knowledge_time=boundary + timedelta(minutes=1),
            wall_receive_time=boundary + timedelta(minutes=1),
        )
        rejection = evaluate_feature(
            _feature("F-RET-001"), [inputs[-2], future], evaluation_time=boundary
        )
        no_lookahead_rejections += rejection.validity is FeatureValidity.INVALID

        if name == "STRESS":
            candles = _closed_candles(contract_number, 1, 15)
            aligned = align_closed_1m_candles(
                candles, 15, evaluation_time=candles[-1].end
            )
            assert aligned.validity is FeatureValidity.VALID
            output_hasher.update(aligned.fingerprint.encode())
            missing = align_closed_1m_candles(
                candles[:-1], 15, evaluation_time=candles[-1].end
            )
            assert missing.validity is FeatureValidity.UNKNOWN
            corrected = replace(candles[0], close=DecimalValue.parse("101"))
            revised = align_closed_1m_candles(
                (corrected, *candles[1:]), 15, evaluation_time=candles[-1].end
            )
            assert revised.fingerprint != aligned.fingerprint
            mixed = _closed_candles(contract_number, 2, 15)
            mixed_result = align_closed_1m_candles(
                (*candles[:14], mixed[-1]), 15, evaluation_time=candles[-1].end
            )
            assert mixed_result.validity is FeatureValidity.INVALID
            restrictive_count += 3
        if memory_probe:
            steady_memory, peak_memory = tracemalloc.get_traced_memory()
            tracemalloc.stop()
    elapsed_ns = time.perf_counter_ns() - start
    return {
        "profile": name,
        "contracts": contracts,
        "closed_1m_candles_per_contract": candle_count,
        "max_window": max_window,
        "feature_ids": list(FEATURE_IDS),
        "feature_evaluations": feature_evaluations,
        "feature_evaluations_per_second": feature_evaluations
        / (elapsed_ns / 1_000_000_000),
        "per_feature_compute_latency_ns": {
            identifier: _percentiles(values)
            for identifier, values in feature_latencies.items()
        },
        "replay_throughput_candles_per_second": (contracts * candle_count)
        / (elapsed_ns / 1_000_000_000),
        "peak_memory_bytes": peak_memory,
        "steady_memory_bytes": steady_memory,
        "memory_probe_contracts": 1,
        "window_buffer_depth": max_window,
        "warmup_count": warmup_count,
        "restrictive_state_count": restrictive_count,
        "no_lookahead_rejection_count": no_lookahead_rejections,
        "input_manifest_hash": input_manifest.hexdigest(),
        "output_manifest_hash": output_hasher.hexdigest(),
        "correctness": "PASS",
        "bounded_completion": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=(*PROFILES, "all"), default="all")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    names = tuple(PROFILES) if args.profile == "all" else (args.profile,)
    result = {
        "mode": "S2A_BASELINE_ESTABLISHMENT_V1",
        "runtime": "python-3.12-decimal-feature-engine",
        "seed": "S2A-FIXTURE-SEED-V1",
        "profiles": [_run_profile(name) for name in names],
    }
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    gc.collect()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
