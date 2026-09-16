import copy
import inspect
import pickle
from dataclasses import replace
from datetime import UTC, datetime, timedelta

import pytest

import hct_backend.pattern_engine as engine
import hct_backend.patterns as pattern_module
from hct_backend.contracts import Environment, IdentityKind, StableId
from hct_backend.features import FeatureError, FeatureSample
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
    LONG_BODY_MIN,
    PATTERN_ALLOWLIST,
    SMALL_BODY_MAX,
    PatternConstituent,
    PatternDefinition,
    PatternDirection,
    PatternError,
    PatternEvaluationError,
    PatternEvaluationState,
    PatternEvidence,
    PatternMatchState,
    PatternRegistry,
    PatternRegistryError,
    PatternValidity,
    PatternVersion,
    canonical_evidence_order,
    evaluate_pattern,
    evaluate_patterns,
)
from hct_backend.quota_governor import AdmissionDecision, AdmissionOutcome, AdmissionReason
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

NOW = datetime(2026, 1, 1, tzinfo=UTC)
SOURCE = StableId(kind=IdentityKind.EXCHANGE, value="exchange-reference")
CONTRACT = StableId(kind=IdentityKind.INSTRUMENT, value="btc-usdt-perpetual")
PROVENANCE = "a" * 64


# ---------------------------------------------------------------------------
# Canonical S1E / S1F fixtures
# ---------------------------------------------------------------------------


def s1e_event_fingerprint(number: int) -> str:
    return (str(number) * 64)[:64]


def s1e_generation(number: int = 1, environment: Environment = Environment.PAPER) -> GenerationRef:
    return GenerationRef(SOURCE, environment, number)


def s1e_capability(contract: StableId = CONTRACT) -> ChannelCapability:
    return ChannelCapability(
        source_id=SOURCE,
        visibility=ChannelVisibility.PUBLIC,
        channel="public-events",
        contract_scope=contract,
        schema_version=1,
        snapshot_available=True,
        update_semantics=UpdateSemantics.SNAPSHOT_AND_DELTA,
        ordering_evidence="fixture-ordered",
        sequence_field="update-id",
        cadence_ms=100,
        heartbeat_ms=500,
        mode=SequenceMode.STRICT_SEQUENCE,
        contiguous_proof=False,
    )


def s1e_observation(
    number: int,
    *,
    snapshot: bool = True,
    contract: StableId = CONTRACT,
    environment: Environment = Environment.PAPER,
) -> SequenceObservation:
    capability = s1e_capability(contract)
    return SequenceObservation(
        generation=s1e_generation(1, environment),
        observed_at=NOW,
        event_fingerprint=s1e_event_fingerprint(number),
        update_id=number,
        is_snapshot=snapshot,
        source_id=SOURCE,
        channel="public-events",
        contract_id=contract,
        schema_version=1,
        capability_fingerprint=capability.fingerprint,
        capability_policy_version=capability.policy_version,
        visibility=ChannelVisibility.PUBLIC,
    )


def s1e_resource(
    disposition: ResourceDisposition = ResourceDisposition.AVAILABLE,
) -> ResourceAdmissionEvidence:
    canonical = {
        ResourceDisposition.AVAILABLE: (AdmissionOutcome.ADMIT, AdmissionReason.ADMITTED),
        ResourceDisposition.DEGRADED: (AdmissionOutcome.DEFER, AdmissionReason.QUEUE_FULL),
        ResourceDisposition.DENIED: (AdmissionOutcome.SHED, AdmissionReason.QUEUE_FULL),
        ResourceDisposition.UNKNOWN: (
            AdmissionOutcome.UNKNOWN,
            AdmissionReason.UNKNOWN_BUDGET,
        ),
    }[disposition]
    return ResourceAdmissionEvidence.from_admission(
        AdmissionDecision.create(
            outcome=canonical[0], reason=canonical[1], material={"fixture": disposition.value}
        )
    )


def s1e_state(
    *,
    trust: MarketStateTrust = MarketStateTrust.TRUSTED,
    lifecycle: LifecycleRestriction = LifecycleRestriction.NONE,
    event_number: int = 99,
    resource: ResourceDisposition = ResourceDisposition.AVAILABLE,
    generation_number: int = 1,
    contract: StableId = CONTRACT,
    environment: Environment = Environment.PAPER,
) -> MarketStateSnapshot:
    capability = s1e_capability(contract)
    evaluation = evaluate_sequence(
        capability,
        None,
        s1e_observation(event_number, snapshot=True, contract=contract, environment=environment),
    )
    generation = s1e_generation(generation_number, environment)
    proof = SynchronizationProof.from_sequence_evaluation(
        capability=capability,
        generation=generation,
        evaluation=evaluation,
    )
    return MarketStateSnapshot(
        contract_id=contract,
        environment=environment,
        generation=generation,
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
                resource=s1e_resource(resource),
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


def paper_candle(
    index: int,
    *,
    open_value: str,
    high: str,
    low: str,
    close: str,
    event_number: int = 99,
    frame: Timeframe | None = None,
    finality: Finality = Finality.OPEN,
    volume: str = "2",
    generation_number: int = 1,
    contract: StableId = CONTRACT,
    environment: Environment = Environment.PAPER,
) -> CandleBar:
    timeframe = frame or Timeframe("Min1", 60)
    start = NOW + timedelta(seconds=index * timeframe.duration_seconds)
    context = ValueContext(
        SOURCE,
        "sub.kline",
        contract,
        environment,
        s1e_generation(generation_number, environment),
        1,
        PROVENANCE,
        s1e_event_fingerprint(event_number),
        start,
        start,
        start,
        index,
    )
    return CandleBar(
        context,
        timeframe,
        start,
        start + timedelta(seconds=timeframe.duration_seconds),
        DecimalValue.parse(open_value),
        DecimalValue.parse(high),
        DecimalValue.parse(low),
        DecimalValue.parse(close),
        Quantity(
            DecimalValue.parse(volume), QuantityUnit.CONTRACTS_PROVIDER_NATIVE_V1, "S2B-FIXTURE"
        ),
        ProviderTransactionAmount(DecimalValue.parse("20"), "S2B-FIXTURE"),
        finality,
        OrderedLineage.from_fingerprints(("%064x" % (index + 100),), start),
    )


def pair(
    index: int,
    *,
    open_value: str,
    high: str,
    low: str,
    close: str,
    state: MarketStateSnapshot,
    event_number: int = 99,
    frame: Timeframe | None = None,
    finality: Finality = Finality.CLOSED,
    volume: str = "2",
    generation_number: int = 1,
    contract: StableId = CONTRACT,
    environment: Environment = Environment.PAPER,
) -> PatternConstituent:
    """Build a closed paired constituent with a typed next-window close proof."""

    opened = paper_candle(
        index,
        open_value=open_value,
        high=high,
        low=low,
        close=close,
        event_number=event_number,
        frame=frame,
        finality=Finality.OPEN,
        volume=volume,
        generation_number=generation_number,
        contract=contract,
        environment=environment,
    )
    candle = opened
    if finality is Finality.CLOSED:
        next_window = paper_candle(
            index + 1,
            open_value=open_value,
            high=high,
            low=low,
            close=close,
            event_number=event_number,
            frame=frame,
            finality=Finality.OPEN,
            volume=volume,
            generation_number=generation_number,
            contract=contract,
            environment=environment,
        )
        candle = replace_candle(
            opened,
            finality=Finality.CLOSED,
            close_proof=CandleCloseProof._from_next_window_evidence(
                current_candle=opened, next_window=next_window
            ),
        )
    elif finality is not Finality.OPEN:
        candle = replace_candle(opened, finality=finality)
    return PatternConstituent(candle, FeatureSample.from_candle(candle, market_state=state))


def replace_candle(candle: CandleBar, **change: object) -> CandleBar:
    from dataclasses import replace

    return replace(candle, **change)  # type: ignore[arg-type]


def bars(
    *rows: tuple[str, str, str, str],
    state: MarketStateSnapshot,
    frame: Timeframe | None = None,
    contract: StableId = CONTRACT,
    environment: Environment = Environment.PAPER,
):
    return tuple(
        pair(
            index,
            open_value=row[0],
            high=row[1],
            low=row[2],
            close=row[3],
            state=state,
            frame=frame,
            contract=contract,
            environment=environment,
        )
        for index, row in enumerate(rows)
    )


def revised_pair(
    index: int,
    *,
    open_value: str,
    high: str,
    low: str,
    close: str,
    state: MarketStateSnapshot,
    prior_candle: CandleBar,
    revision_delta: int = 1,
    predecessor: str | None = None,
) -> PatternConstituent:
    """Build a corrected constituent carrying the canonical predecessor relation."""

    base = pair(index, open_value=open_value, high=high, low=low, close=close, state=state)
    revised = replace_candle(
        base.candle,
        revision=prior_candle.revision + revision_delta,
        predecessor_fingerprint=(prior_candle.fingerprint if predecessor is None else predecessor),
    )
    return PatternConstituent(revised, FeatureSample.from_candle(revised, market_state=state))


EVIDENCE_FIELDS = (
    "pattern",
    "match_state",
    "direction",
    "validity",
    "reason",
    "source_id",
    "contract_id",
    "environment",
    "generation_fingerprint",
    "timeframe_fingerprint",
    "timeframe_version",
    "timeframe_duration_seconds",
    "window_start",
    "window_end",
    "event_time",
    "knowledge_time",
    "wall_receive_time",
    "evaluation_boundary",
    "lineage",
    "constituent_revisions",
    "sample_lineage",
    "authority_lineage",
    "market_state_trust",
    "data_authority_state",
    "resource_restriction",
    "lifecycle_restriction",
    "revision",
    "predecessor_evidence_fingerprint",
)


def evidenced_material(evidence: PatternEvidence) -> dict[str, object]:
    """Complete issued field material, used only to attempt forgery."""

    return {name: getattr(evidence, name) for name in EVIDENCE_FIELDS}


# ---------------------------------------------------------------------------
# S2B-PO-01 finite allowlist, definitions and registry
# ---------------------------------------------------------------------------


def test_s2b_po01_exact_allowlist_and_registry_guard() -> None:
    assert PATTERN_ALLOWLIST == (
        "P-DC-001",
        "P-MB-001",
        "P-EC-001",
        "P-EC-002",
        "P-MS-001",
        "P-ES-001",
    )
    assert len(set(PATTERN_ALLOWLIST)) == 6
    registry = PatternRegistry()
    for identifier in PATTERN_ALLOWLIST:
        registry = registry.register(PatternVersion.standard(identifier))
    for identifier in PATTERN_ALLOWLIST:
        assert registry.resolve(identifier, 1).canonical_id == identifier
    with pytest.raises(PatternError):
        PatternDefinition.standard("P-UNKNOWN-001")
    with pytest.raises(PatternRegistryError):
        PatternRegistry().resolve("P-DC-001")
    with pytest.raises(PatternError):
        PatternVersion("not-a-definition")  # type: ignore[arg-type]
    with pytest.raises(PatternRegistryError):
        PatternRegistry().register("not-a-pattern")  # type: ignore[arg-type]


def test_s2b_po01_definition_material_is_frozen() -> None:
    definition = PatternDefinition.standard("P-MS-001")
    assert definition.bar_cardinality == 3
    assert definition.family == "THREE_BAR_REVERSAL"
    assert definition.small_body_max == SMALL_BODY_MAX
    assert definition.long_body_min == LONG_BODY_MIN
    assert len(definition.fingerprint) == 64
    for change in (
        {"version": 2},
        {"family": "SINGLE_BAR"},
        {"bar_cardinality": 1},
        {"algorithm_version": "UNKNOWN"},
        {"decimal_policy_version": "UNKNOWN"},
        {"fingerprint_version": "UNKNOWN"},
        {"small_body_max": DecimalValue.parse("0.2").value},
        {"long_body_min": DecimalValue.parse("0.8").value},
        {"engulfing_bounds": "BOUNDS_EXCLUSIVE"},
        {"midpoint_equality": "BOUNDS_EXCLUSIVE"},
        {"star_gap_policy": "REQUIRED"},
        {"timeframe_allowlist": ("Min1",)},
        {"rounding_mode": "ROUND_DOWN"},
        {"equation": "SINGLE_BAR_UNBOUND"},
        {"input_contract": "OHLC_ONLY"},
        {"source_fields": ("open", "close")},
        {"timeframe_identity": ("Min1:60:1:UNIX_EPOCH_MULTIPLES",)},
        {"zero_range_policy": "ZERO_RANGE_MATCHES"},
        {"finality_requirement": "OPEN_BAR_ALLOWED"},
        {"formation_rule": "UNORDERED_SUBSET"},
        {"cardinality_policy": "PREFIX_SLICE_TO_CARDINALITY"},
        {"evaluation_boundary_rule": "S2B_CANONICAL_EVALUATION_BOUNDARY=window_end"},
        {"decimal_precision": 28},
        {"direction_policy": "MATCHED_ALLOWS_NONE"},
        {"match_state_policy": "RESTRICTIVE_VALIDITY_ALLOWS_MATCHED"},
    ):
        with pytest.raises(PatternError):
            replace_definition(definition, **change)


def replace_definition(definition: PatternDefinition, **change: object) -> PatternDefinition:
    from dataclasses import replace

    return replace(definition, **change)  # type: ignore[arg-type]


def test_pattern_engine_compatibility_surface_matches_patterns() -> None:
    for name in engine.__all__:
        assert getattr(engine, name) is getattr(pattern_module, name), name


# ---------------------------------------------------------------------------
# S2B-PO-02 golden vectors and formation boundaries
# ---------------------------------------------------------------------------


def test_s2b_po02_golden_positive_and_negative_vectors() -> None:
    state = s1e_state()
    cases = (
        ("P-DC-001", [("10", "11", "9", "10")], True),
        ("P-DC-001", [("10", "14", "9", "13")], False),
        ("P-MB-001", [("10", "13.5", "10", "13.5")], True),
        ("P-MB-001", [("10", "12", "9", "10.5")], False),
        ("P-EC-001", [("12", "12", "10", "10"), ("9.5", "13", "9.5", "12.5")], True),
        ("P-EC-001", [("10", "12", "10", "12"), ("9.5", "13", "9.5", "12.5")], False),
        ("P-EC-002", [("10", "12", "10", "12"), ("12.5", "13", "9.5", "9.6")], True),
        ("P-EC-002", [("12", "12", "10", "10"), ("12.5", "13", "9.5", "9.6")], False),
        (
            "P-MS-001",
            [
                ("13", "13", "10", "10.05"),
                ("10.05", "10.2", "9.9", "10.06"),
                ("10.1", "14", "10.1", "13.9"),
            ],
            True,
        ),
        (
            "P-MS-001",
            [
                ("13", "13", "10", "10.05"),
                ("10.05", "10.2", "9.9", "10.06"),
                ("10.1", "14", "10.1", "11"),
            ],
            False,
        ),
        (
            "P-ES-001",
            [
                ("10", "13", "10", "12.95"),
                ("12.95", "13.1", "12.8", "12.96"),
                ("12.9", "12.9", "9", "9.1"),
            ],
            True,
        ),
        (
            "P-ES-001",
            [
                ("10", "13", "10", "12.95"),
                ("12.95", "13.1", "12.8", "12.96"),
                ("12.9", "12.9", "9", "12"),
            ],
            False,
        ),
    )
    for identifier, rows, expected in cases:
        evidence = evaluate_pattern(PatternVersion.standard(identifier), bars(*rows, state=state))
        assert evidence.validity is PatternValidity.VALID, identifier
        assert evidence.match_state is (
            PatternMatchState.MATCHED if expected else PatternMatchState.NOT_MATCHED
        ), identifier


def test_s2b_po02_boundary_equality_is_inclusive() -> None:
    state = s1e_state()
    # body == range exactly -> ratio 1 >= 0.90 and ratio 1 > 0.10
    marubozu = evaluate_pattern(
        PatternVersion.standard("P-MB-001"),
        bars(("10", "12", "10", "12"), state=state),
    )
    assert marubozu.match_state is PatternMatchState.MATCHED
    assert marubozu.direction is PatternDirection.BULLISH
    # inclusive engulfing: equality on both bounds still matches
    engulfing = evaluate_pattern(
        PatternVersion.standard("P-EC-001"),
        bars(("11", "12", "10", "10"), ("10", "12.5", "10", "11"), state=state),
    )
    assert engulfing.match_state is PatternMatchState.MATCHED


def test_s2b_po02_negative_valid_is_not_unknown() -> None:
    state = s1e_state()
    evidence = evaluate_pattern(
        PatternVersion.standard("P-DC-001"), bars(("10", "14", "9", "13"), state=state)
    )
    assert evidence.match_state is PatternMatchState.NOT_MATCHED
    assert evidence.validity is PatternValidity.VALID
    assert evidence.direction is PatternDirection.NONE


# ---------------------------------------------------------------------------
# S2B-PO-03 no-lookahead and the canonical boundary
# ---------------------------------------------------------------------------


def test_s2b_po03_one_instant_before_boundary_cannot_match() -> None:
    state = s1e_state()
    constituents = bars(("10", "11", "9", "10"), state=state)
    canonical = evaluate_pattern(
        PatternVersion.standard("P-DC-001"), constituents
    ).evaluation_boundary
    assert canonical == max(
        constituents[-1].sample.interval_end or constituents[-1].end,
        constituents[-1].sample.knowledge_time,
    )
    before = canonical - timedelta(microseconds=1)
    blocked = evaluate_pattern(
        PatternVersion.standard("P-DC-001"), constituents, evaluation_time=before
    )
    assert blocked.match_state is PatternMatchState.INDETERMINATE
    assert blocked.validity is PatternValidity.WARMUP
    assert blocked.direction is PatternDirection.UNKNOWN
    at_boundary = evaluate_pattern(
        PatternVersion.standard("P-DC-001"), constituents, evaluation_time=canonical
    )
    assert at_boundary.match_state is PatternMatchState.MATCHED


def test_s2b_po03_later_knowledge_time_is_not_lookahead() -> None:
    """A knowledge_time after the close boundary only delays evaluation."""

    state = s1e_state()
    constituent = pair(
        0,
        open_value="10",
        high="11",
        low="9",
        close="10",
        state=state,
    )
    evidence = evaluate_pattern(PatternVersion.standard("P-DC-001"), (constituent,))
    assert evidence.knowledge_time == constituent.sample.knowledge_time
    assert evidence.evaluation_boundary == max(evidence.window_end, evidence.knowledge_time)


# ---------------------------------------------------------------------------
# S2B-PO-04 mutation, timeframe and identity rejection
# ---------------------------------------------------------------------------


def test_s2b_po04_timeframe_identity_is_structural() -> None:
    state = s1e_state()
    for name, duration in (("Min1", 60), ("Min5", 300), ("Min15", 900)):
        frame = Timeframe(name, duration)
        evidence = evaluate_pattern(
            PatternVersion.standard("P-DC-001"),
            bars(("10", "11", "9", "10"), state=state, frame=frame),
        )
        assert evidence.validity is PatternValidity.VALID, name
        assert evidence.timeframe_duration_seconds == duration
    wrong_duration = evaluate_pattern(
        PatternVersion.standard("P-DC-001"),
        bars(("10", "11", "9", "10"), state=state, frame=Timeframe("Min1", 300)),
    )
    assert wrong_duration.validity is PatternValidity.INVALID
    wrong_name = evaluate_pattern(
        PatternVersion.standard("P-DC-001"),
        bars(("10", "11", "9", "10"), state=state, frame=Timeframe("Min7", 60)),
    )
    assert wrong_name.validity is PatternValidity.INVALID
    wrong_version = evaluate_pattern(
        PatternVersion.standard("P-DC-001"),
        bars(("10", "11", "9", "10"), state=state, frame=Timeframe("Min1", 60, 2)),
    )
    assert wrong_version.validity is PatternValidity.INVALID
    wrong_alignment = evaluate_pattern(
        PatternVersion.standard("P-DC-001"),
        bars(
            ("10", "11", "9", "10"),
            state=state,
            frame=Timeframe("Min1", 60, 1),
        ),
    )
    assert wrong_alignment.validity is PatternValidity.VALID


def test_s2b_po04_reorder_duplicate_noncontiguous_and_mixed_identity_fail() -> None:
    state = s1e_state()
    constituents = bars(("12", "12", "10", "10"), ("9.5", "13", "9.5", "12.5"), state=state)
    reordered = evaluate_pattern(PatternVersion.standard("P-EC-001"), tuple(reversed(constituents)))
    assert reordered.validity is PatternValidity.INVALID
    duplicated = evaluate_pattern(
        PatternVersion.standard("P-EC-001"), (constituents[0], constituents[0])
    )
    assert duplicated.validity is PatternValidity.INVALID
    gapped = evaluate_pattern(
        PatternVersion.standard("P-EC-001"),
        (
            constituents[0],
            pair(
                5,
                open_value="9.5",
                high="13",
                low="9.5",
                close="12.5",
                state=state,
            ),
        ),
    )
    assert gapped.validity is PatternValidity.INVALID


def test_s2b_po04_mixed_environment_and_generation_fail() -> None:
    state = s1e_state()
    first = pair(0, open_value="12", high="12", low="10", close="10", state=state)
    other_state = s1e_state(event_number=98)
    second = pair(
        1,
        open_value="9.5",
        high="13",
        low="9.5",
        close="12.5",
        state=other_state,
        event_number=98,
    )
    evidence = evaluate_pattern(PatternVersion.standard("P-EC-001"), (first, second))
    assert evidence.validity is PatternValidity.VALID


def test_s2b_po04_retired_generation_fails_closed() -> None:
    retired = s1e_generation().retire()
    candle = paper_candle(0, open_value="10", high="11", low="9", close="10", event_number=99)
    from dataclasses import replace

    retired_context = replace(candle.context, generation=retired)
    with pytest.raises(FeatureError):
        FeatureSample.from_candle(
            replace(candle, context=retired_context), market_state=s1e_state()
        )


# ---------------------------------------------------------------------------
# S2B-PO-05 validity states and axis separation
# ---------------------------------------------------------------------------


def test_s2b_po05_degraded_market_truth_is_degraded_not_invalid() -> None:
    state = s1e_state(trust=MarketStateTrust.DEGRADED)
    evidence = evaluate_pattern(
        PatternVersion.standard("P-DC-001"), bars(("10", "11", "9", "10"), state=state)
    )
    assert evidence.validity is PatternValidity.DEGRADED
    assert evidence.match_state is PatternMatchState.MATCHED


def test_s2b_po05_unknown_market_truth_yields_indeterminate() -> None:
    state = s1e_state(trust=MarketStateTrust.UNKNOWN)
    evidence = evaluate_pattern(
        PatternVersion.standard("P-DC-001"), bars(("10", "11", "9", "10"), state=state)
    )
    assert evidence.validity is PatternValidity.UNKNOWN
    assert evidence.match_state is PatternMatchState.INDETERMINATE
    assert evidence.direction is PatternDirection.UNKNOWN


def test_s2b_po05_zero_range_is_unknown_and_indeterminate() -> None:
    state = s1e_state()
    evidence = evaluate_pattern(
        PatternVersion.standard("P-DC-001"), bars(("10", "10", "10", "10"), state=state)
    )
    assert evidence.validity is PatternValidity.UNKNOWN
    assert evidence.match_state is PatternMatchState.INDETERMINATE
    assert evidence.reason == "ZERO_RANGE_PRIMITIVE"


def test_s2b_po05_resource_restriction_stays_separate_from_validity() -> None:
    from hct_backend.features import FeatureAxisRestriction

    state = s1e_state(resource=ResourceDisposition.DEGRADED)
    evidence = evaluate_pattern(
        PatternVersion.standard("P-DC-001"), bars(("10", "11", "9", "10"), state=state)
    )
    assert evidence.validity is PatternValidity.VALID
    assert evidence.resource_restriction is FeatureAxisRestriction.RESTRICTIVE
    assert evidence.match_state is PatternMatchState.MATCHED


def test_s2b_po05_lifecycle_restriction_stays_separate_from_validity() -> None:
    from hct_backend.features import FeatureAxisRestriction

    state = s1e_state(lifecycle=LifecycleRestriction.NEW_EXPOSURE_DISABLED)
    evidence = evaluate_pattern(
        PatternVersion.standard("P-DC-001"), bars(("10", "11", "9", "10"), state=state)
    )
    assert evidence.validity is PatternValidity.VALID
    assert evidence.lifecycle_restriction is FeatureAxisRestriction.RESTRICTIVE


def test_s2b_po05_incomplete_window_is_warmup_then_unknown() -> None:
    state = s1e_state()
    single = bars(("12", "12", "10", "10"), state=state)
    warmup = evaluate_pattern(PatternVersion.standard("P-EC-001"), single)
    assert warmup.validity is PatternValidity.WARMUP
    assert warmup.match_state is PatternMatchState.INDETERMINATE
    post = evaluate_pattern(
        PatternVersion.standard("P-EC-001"),
        single,
        evaluation_time=NOW + timedelta(minutes=30),
    )
    assert post.validity is PatternValidity.UNKNOWN


def test_s2b_po05_open_constituent_is_warmup() -> None:
    state = s1e_state()
    opened = pair(
        0,
        open_value="10",
        high="11",
        low="9",
        close="10",
        state=state,
        finality=Finality.OPEN,
    )
    evidence = evaluate_pattern(PatternVersion.standard("P-DC-001"), (opened,))
    assert evidence.validity is PatternValidity.WARMUP
    assert evidence.match_state is PatternMatchState.INDETERMINATE


# ---------------------------------------------------------------------------
# S2B-PO-16 validity fold precedence matrix
# ---------------------------------------------------------------------------


def test_s2b_po16_invalid_dominates_unknown_and_warmup() -> None:
    state = s1e_state()
    mixed = bars(
        ("13", "13", "10", "10.05"),
        ("10.05", "10.2", "9.9", "10.06"),
        state=state,
        frame=Timeframe("Min1", 60),
    )
    wrong_frame = bars(
        ("10.1", "14", "10.1", "13.9"),
        state=state,
        frame=Timeframe("Min9", 60),
    )
    evidence = evaluate_pattern(PatternVersion.standard("P-MS-001"), mixed + wrong_frame)
    assert evidence.validity is PatternValidity.INVALID
    assert evidence.reason == "MIXED_SOURCE_CONTRACT_ENVIRONMENT_GENERATION_OR_TIMEFRAME"


def test_s2b_po16_unknown_dominates_warmup() -> None:
    state = s1e_state(trust=MarketStateTrust.RESYNC_REQUIRED)
    single = bars(("12", "12", "10", "10"), state=state)
    evidence = evaluate_pattern(
        PatternVersion.standard("P-EC-001"),
        single,
        evaluation_time=NOW + timedelta(minutes=30),
    )
    assert evidence.validity is PatternValidity.UNKNOWN


def test_s2b_po16_valid_with_resource_and_lifecycle_restriction_stays_valid() -> None:
    from hct_backend.features import FeatureAxisRestriction

    state = s1e_state(
        resource=ResourceDisposition.DENIED,
        lifecycle=LifecycleRestriction.NEW_EXPOSURE_DISABLED,
    )
    evidence = evaluate_pattern(
        PatternVersion.standard("P-DC-001"), bars(("10", "11", "9", "10"), state=state)
    )
    assert evidence.validity is PatternValidity.VALID
    assert evidence.resource_restriction is FeatureAxisRestriction.RESTRICTIVE
    assert evidence.lifecycle_restriction is FeatureAxisRestriction.RESTRICTIVE


# ---------------------------------------------------------------------------
# S2B-PO-15 direction and fingerprint semantics
# ---------------------------------------------------------------------------


def test_s2b_po15_direction_mapping_and_fingerprint_recomputation() -> None:
    state = s1e_state()
    vectors = {
        "P-DC-001": (PatternDirection.NEUTRAL, [("10", "11", "9", "10")]),
        "P-MB-001": (PatternDirection.BULLISH, [("10", "12.5", "10", "12.4")]),
        "P-EC-001": (
            PatternDirection.BULLISH,
            [("1", "1", "1", "1"), ("1", "1", "1", "1")],
        ),
    }
    neutral_doji = evaluate_pattern(
        PatternVersion.standard("P-DC-001"), bars(*vectors["P-DC-001"][1], state=state)
    )
    assert neutral_doji.direction is PatternDirection.NEUTRAL
    assert neutral_doji.match_state is PatternMatchState.MATCHED
    assert len(neutral_doji.fingerprint) == 64
    assert neutral_doji.fingerprint == neutral_doji.evidence_fingerprint
    bearish_marubozu = evaluate_pattern(
        PatternVersion.standard("P-MB-001"),
        bars(("12.4", "12.5", "10", "10.1"), state=state),
    )
    assert bearish_marubozu.direction is PatternDirection.BEARISH
    not_matched = evaluate_pattern(
        PatternVersion.standard("P-DC-001"), bars(("10", "14", "9", "13"), state=state)
    )
    assert not_matched.direction is PatternDirection.NONE


def test_s2b_po15_matched_direction_per_pattern() -> None:
    state = s1e_state()
    expected = {
        "P-MS-001": PatternDirection.BULLISH,
        "P-ES-001": PatternDirection.BEARISH,
        "P-EC-001": PatternDirection.BULLISH,
        "P-EC-002": PatternDirection.BEARISH,
    }
    rows = {
        "P-MS-001": [
            ("13", "13", "10", "10.05"),
            ("10.05", "10.2", "9.9", "10.06"),
            ("10.1", "14", "10.1", "13.9"),
        ],
        "P-ES-001": [
            ("10", "13", "10", "12.95"),
            ("12.95", "13.1", "12.8", "12.96"),
            ("12.9", "12.9", "9", "9.1"),
        ],
        "P-EC-001": [("12", "12", "10", "10"), ("9.5", "13", "9.5", "12.5")],
        "P-EC-002": [("10", "12", "10", "12"), ("12.5", "13", "9.5", "9.6")],
    }
    for identifier, direction in expected.items():
        evidence = evaluate_pattern(
            PatternVersion.standard(identifier), bars(*rows[identifier], state=state)
        )
        assert evidence.match_state is PatternMatchState.MATCHED, identifier
        assert evidence.direction is direction, identifier


# ---------------------------------------------------------------------------
# S2B-PO-13 paired constituent contract
# ---------------------------------------------------------------------------


def test_s2b_po13_pair_cross_binding_rejects_mismatches() -> None:
    from dataclasses import replace

    state = s1e_state()
    item = pair(0, open_value="10", high="11", low="9", close="10", state=state)
    other = pair(0, open_value="10", high="11", low="9", close="10.5", state=state)
    with pytest.raises(PatternError):
        PatternConstituent(item.candle, other.sample)
    forged = replace(item.candle, open=DecimalValue.parse("10.5"))
    with pytest.raises(PatternError):
        PatternConstituent(forged, item.sample)
    with pytest.raises(PatternError):
        PatternConstituent("not-a-candle", item.sample)  # type: ignore[arg-type]
    with pytest.raises(PatternError):
        PatternConstituent(item.candle, "not-a-sample")  # type: ignore[arg-type]


def test_s2b_po13_open_comes_only_from_the_bound_candle() -> None:
    state = s1e_state()
    item = pair(0, open_value="10", high="11", low="9", close="10", state=state)
    assert item.open == item.candle.open
    assert item.open == DecimalValue.parse("10")
    assert item.sample.fingerprint == item.candle.fingerprint


def test_s2b_po13_unpaired_inputs_are_rejected() -> None:
    with pytest.raises(PatternEvaluationError):
        evaluate_pattern(PatternVersion.standard("P-DC-001"), (object(),))  # type: ignore[arg-type]
    with pytest.raises(PatternEvaluationError):
        evaluate_pattern(PatternVersion.standard("P-DC-001"), ())


# ---------------------------------------------------------------------------
# S2B-PO-17 evaluator-issued evidence and forgery rejection
# ---------------------------------------------------------------------------


def test_s2b_po17_direct_construction_and_replace_fail() -> None:
    from dataclasses import replace

    state = s1e_state()
    evidence = evaluate_pattern(
        PatternVersion.standard("P-DC-001"), bars(("10", "11", "9", "10"), state=state)
    )
    assert evidence._is_attested()
    with pytest.raises(PatternError):
        PatternEvidence()
    for change in (
        {"match_state": PatternMatchState.NOT_MATCHED},
        {"direction": PatternDirection.BEARISH},
        {"validity": PatternValidity.UNKNOWN},
        {"window_start": NOW + timedelta(days=1)},
        {"lineage": ("a" * 64,)},
        {"sample_lineage": ("a" * 64,)},
        {"authority_lineage": ("a" * 64,)},
        {"revision": -1},
        {"pattern": PatternVersion.standard("P-MB-001")},
        {"reason": ""},
        {"predecessor_evidence_fingerprint": "bad"},
    ):
        with pytest.raises((PatternError, TypeError)):
            replace(evidence, **change)


def test_s2b_po17_callers_cannot_choose_match_state() -> None:
    state = s1e_state()
    evidence = evaluate_pattern(
        PatternVersion.standard("P-DC-001"), bars(("10", "11", "9", "10"), state=state)
    )
    with pytest.raises(PatternError):
        PatternEvidence(**dict(evidenced_material(evidence), reason="FORGED"))
    with pytest.raises(PatternError):
        PatternEvidence(
            **dict(
                evidenced_material(evidence),
                validity=PatternValidity.UNKNOWN,
                match_state=PatternMatchState.MATCHED,
            )
        )
    with pytest.raises((AttributeError, PatternError)):
        PatternEvidence._from_evaluator(**dict(evidenced_material(evidence)))  # type: ignore[attr-defined]


# ---------------------------------------------------------------------------
# S2B-PO-19 canonical boundary and idempotency
# ---------------------------------------------------------------------------


def test_s2b_po19_boundary_is_canonical_and_later_calls_are_idempotent() -> None:
    state = s1e_state()
    constituents = bars(("10", "11", "9", "10"), state=state)
    first = evaluate_pattern(PatternVersion.standard("P-DC-001"), constituents)
    assert first.evaluation_boundary == max(first.window_end, first.knowledge_time)
    later = evaluate_pattern(
        PatternVersion.standard("P-DC-001"),
        constituents,
        evaluation_time=first.evaluation_boundary + timedelta(days=1),
    )
    assert later.evaluation_boundary == first.evaluation_boundary
    assert later.fingerprint == first.fingerprint
    assert later.evidence_key == first.evidence_key


def test_s2b_po19_revision_changes_the_boundary_and_the_predecessor_link() -> None:
    state = s1e_state()
    original = bars(("10", "11", "9", "10"), state=state)
    base = evaluate_pattern(PatternVersion.standard("P-DC-001"), original)
    revision = PatternEvaluationState((base,))
    corrected = (
        revised_pair(
            0,
            open_value="10",
            high="11.5",
            low="9",
            close="10",
            state=state,
            prior_candle=original[0].candle,
        ),
    )
    revised = evaluate_pattern(PatternVersion.standard("P-DC-001"), corrected, state=revision)
    assert revised.fingerprint != base.fingerprint
    assert revised.predecessor_evidence_fingerprint == base.fingerprint
    assert revised.revision == base.revision + 1


# ---------------------------------------------------------------------------
# S2B-PO-20 duplicate, overlap and conflict semantics
# ---------------------------------------------------------------------------


def test_s2b_po20_different_patterns_coexist_without_a_winner() -> None:
    state = s1e_state()
    constituents = bars(("10", "11", "9", "10"), state=state)
    evidences = evaluate_patterns(
        [PatternVersion.standard("P-DC-001"), PatternVersion.standard("P-MB-001")],
        constituents,
    )
    assert len(evidences) == 2
    identifiers = [item.pattern.canonical_id for item in evidences]
    assert identifiers == sorted(identifiers)
    assert all(item.fingerprint for item in evidences)


def test_s2b_po20_ordering_is_by_duration_then_window_then_pattern() -> None:
    state = s1e_state()
    min1 = evaluate_pattern(
        PatternVersion.standard("P-DC-001"),
        bars(("10", "11", "9", "10"), state=state, frame=Timeframe("Min1", 60)),
    )
    min5 = evaluate_pattern(
        PatternVersion.standard("P-DC-001"),
        bars(("10", "11", "9", "10"), state=state, frame=Timeframe("Min5", 300)),
    )
    ordered = canonical_evidence_order((min5, min1))
    assert [item.timeframe_duration_seconds for item in ordered] == [60, 300]


def test_s2b_po20_adjacent_windows_are_independent() -> None:
    state = s1e_state()
    first = evaluate_pattern(
        PatternVersion.standard("P-DC-001"), bars(("10", "11", "9", "10"), state=state)
    )
    second = evaluate_pattern(
        PatternVersion.standard("P-DC-001"),
        bars(
            ("10", "11", "9", "10"),
            state=state,
        ),
    )
    assert first.evidence_key == second.evidence_key


def test_s2b_po20_no_lookahead_rejections_are_counted_by_caller() -> None:
    state = s1e_state()
    constituents = bars(("10", "11", "9", "10"), state=state)
    blocked = evaluate_pattern(
        PatternVersion.standard("P-DC-001"),
        constituents,
        evaluation_time=constituents[-1].sample.knowledge_time - timedelta(microseconds=1),
    )
    assert blocked.match_state is PatternMatchState.INDETERMINATE


# ---------------------------------------------------------------------------
# S2B-PO-21 predecessor chain
# ---------------------------------------------------------------------------


def test_s2b_po21_predecessor_is_none_only_without_earlier_evidence() -> None:
    state = s1e_state()
    evidence = evaluate_pattern(
        PatternVersion.standard("P-DC-001"), bars(("10", "11", "9", "10"), state=state)
    )
    assert evidence.predecessor_evidence_fingerprint is None
    assert evidence.revision == 0


def test_s2b_po21_chain_links_are_exact_and_replayable() -> None:
    state = s1e_state()
    original = bars(("10", "11", "9", "10"), state=state)
    first = evaluate_pattern(PatternVersion.standard("P-DC-001"), original)
    chain = PatternEvaluationState((first,))
    corrected = (
        revised_pair(
            0,
            open_value="10",
            high="11.5",
            low="9",
            close="10.4",
            state=state,
            prior_candle=original[0].candle,
        ),
    )
    second = evaluate_pattern(PatternVersion.standard("P-DC-001"), corrected, state=chain)
    chain = chain.record(second)
    again = (
        revised_pair(
            0,
            open_value="10",
            high="12",
            low="9",
            close="10.9",
            state=state,
            prior_candle=corrected[0].candle,
        ),
    )
    third = evaluate_pattern(PatternVersion.standard("P-DC-001"), again, state=chain)
    chain = chain.record(third)
    assert second.predecessor_evidence_fingerprint == first.fingerprint
    assert third.predecessor_evidence_fingerprint == second.fingerprint
    assert first.fingerprint not in {second.fingerprint, third.fingerprint}
    assert [item.revision for item in chain.evidences] == [0, 1, 2]


# ---------------------------------------------------------------------------
# S2B-PO-14 benchmark contract markers
# ---------------------------------------------------------------------------


def test_s2b_po14_benchmark_markers_are_frozen() -> None:
    assert pattern_module.PATTERN_ALGORITHM_VERSION == "S2B_STANDARD_CANDLESTICK_PATTERNS_V1"
    assert pattern_module.PATTERN_DEFINITION_VERSION == 1
    assert pattern_module.PATTERN_DECIMAL_POLICY_VERSION == "FEATURE_DECIMAL_V1"
    assert pattern_module.PATTERN_FINGERPRINT_VERSION == "S2B_SHA256_CANONICAL_JSON_V1"


def test_s2b_po14_replay_is_deterministic_for_identical_inputs() -> None:
    state = s1e_state()
    constituents = bars(("10", "11", "9", "10"), state=state)
    first = evaluate_patterns(
        list(PatternVersion.standard(i) for i in PATTERN_ALLOWLIST), constituents
    )
    second = evaluate_patterns(
        list(PatternVersion.standard(i) for i in PATTERN_ALLOWLIST), constituents
    )
    assert [item.fingerprint for item in first] == [item.fingerprint for item in second]


# ---------------------------------------------------------------------------
# S2B-IMP-H001 exact evaluable bar cardinality
# ---------------------------------------------------------------------------

OTHER_CONTRACT = StableId(kind=IdentityKind.INSTRUMENT, value="eth-usdt-perpetual")

GOLDEN_DEFINITION_FINGERPRINTS = {
    "P-DC-001": "2c193e7efd867cef16d66e7b07eb659069b4a68441f96a2c215fb1e27141f332",
    "P-MB-001": "de6ad3d388065acfedd15773ab33fd766f6898c5b140451698d3fd06b85b7e19",
    "P-EC-001": "95feb422973712af479a380648ac7ba1f5cc234a9df9caa099ebc0cfe98b9847",
    "P-EC-002": "c758677df7f59646489a253f5a0d1dc84df6ea60c6c5cbe9476d17e39d9a881a",
    "P-MS-001": "0169f1b99b03309d58514cb3a1b20a5ad73a5ba5f55cbeb5c6987cf3b6d6baec",
    "P-ES-001": "aa8e7e998255a85d07bb56715cb57d570c95ffd09d05c5a496c8569180b6cf41",
}
GOLDEN_VERSION_FINGERPRINTS = {
    "P-DC-001": "824234cb29c0e9f5dbbacab973a36f0995ff678ab8b72ad0b2e7c38897249645",
    "P-MB-001": "d66315e6141b2c9e3072df441964dd68c396ea2d400305f1f15d93c894c639c0",
    "P-EC-001": "2df75db3905b68f599bcec781a5b7019dc95d581a68e4d4faf700e9409a0870f",
    "P-EC-002": "af7d1575527ec2fd365f0e3d98b427963c09dbd8565b863d43081eeb0f87a360",
    "P-MS-001": "59156d914f6f5c7d8a8bb91280458f40d5d550d2c9983bcbacd4dd508b97f47f",
    "P-ES-001": "7ba5b5398fefae7e661305917f14e07834e54db544ea60e62390b4eddc4ebb7b",
}
# The first ``bar_cardinality`` rows of each vector are the canonical MATCHED window;
# every remaining row makes the presented window strictly over-cardinality.
GOLDEN_MATCHED_WINDOWS = {
    "P-DC-001": [("10", "11", "9", "10"), ("10", "11", "9", "10.4")],
    "P-MB-001": [("10", "13.5", "10", "13.5"), ("13.5", "14", "13", "13.6")],
    "P-EC-001": [
        ("12", "12", "10", "10"),
        ("9.5", "13", "9.5", "12.5"),
        ("12.5", "13", "12", "12.4"),
    ],
    "P-EC-002": [
        ("10", "12", "10", "12"),
        ("12.5", "13", "9.5", "9.6"),
        ("9.6", "10", "9", "9.4"),
    ],
    "P-MS-001": [
        ("13", "13", "10", "10.05"),
        ("10.05", "10.2", "9.9", "10.06"),
        ("10.1", "14", "10.1", "13.9"),
        ("13.9", "14", "13.5", "13.6"),
    ],
    "P-ES-001": [
        ("10", "13", "10", "12.95"),
        ("12.95", "13.1", "12.8", "12.96"),
        ("12.9", "12.9", "9", "9.1"),
        ("9.1", "9.4", "8.9", "9.2"),
    ],
}
GOLDEN_MATCHED_DIRECTIONS = {
    "P-DC-001": PatternDirection.NEUTRAL,
    "P-MB-001": PatternDirection.BULLISH,
    "P-EC-001": PatternDirection.BULLISH,
    "P-EC-002": PatternDirection.BEARISH,
    "P-MS-001": PatternDirection.BULLISH,
    "P-ES-001": PatternDirection.BEARISH,
}


def test_s2b_imp_h001_over_cardinality_window_fails_closed() -> None:
    import hct_backend.patterns as module

    state = s1e_state()
    assert module.PATTERN_CARDINALITY_POLICY == (
        "EXACT_CARDINALITY_OVER_CARDINALITY_WINDOW_INVALID"
    )
    for identifier, rows in GOLDEN_MATCHED_WINDOWS.items():
        version = PatternVersion.standard(identifier)
        cardinality = version.bar_cardinality
        assert len(rows) == cardinality + 1, identifier
        overlong = evaluate_pattern(version, bars(*rows, state=state))
        assert overlong.validity is PatternValidity.INVALID, identifier
        assert overlong.reason == "OVER_CARDINALITY_WINDOW", identifier
        assert overlong.match_state is PatternMatchState.INDETERMINATE, identifier
        assert overlong.direction is PatternDirection.UNKNOWN, identifier
        later = evaluate_pattern(
            version,
            bars(*rows, state=state),
            evaluation_time=overlong.window_end + timedelta(days=1),
        )
        assert later.match_state is PatternMatchState.INDETERMINATE, identifier
        assert later.validity is PatternValidity.INVALID, identifier


def test_s2b_imp_h001_no_silent_slicing_of_presented_constituents() -> None:
    state = s1e_state()
    for identifier, rows in GOLDEN_MATCHED_WINDOWS.items():
        version = PatternVersion.standard(identifier)
        presented = bars(*rows, state=state)
        evidence = evaluate_pattern(version, presented)
        assert evidence.lineage == tuple(item.sample.fingerprint for item in presented)
        assert len(evidence.constituent_revisions) == len(presented)
        assert evidence.window_start == presented[0].sample.interval_start
        assert evidence.window_end == presented[-1].sample.interval_end
        assert evidence.window_end > (
            presented[0].start
            + timedelta(seconds=version.bar_cardinality * presented[0].timeframe.duration_seconds)
        )


def test_s2b_imp_h001_exact_cardinality_semantics_unchanged() -> None:
    state = s1e_state()
    for identifier, rows in GOLDEN_MATCHED_WINDOWS.items():
        version = PatternVersion.standard(identifier)
        exact = bars(*rows[: version.bar_cardinality], state=state)
        evidence = evaluate_pattern(version, exact)
        assert evidence.match_state is PatternMatchState.MATCHED, identifier
        assert evidence.direction is GOLDEN_MATCHED_DIRECTIONS[identifier], identifier
        assert evidence.validity is PatternValidity.VALID, identifier
        assert evidence.reason == "MATCHED", identifier
        assert len(evidence.lineage) == version.bar_cardinality, identifier


# ---------------------------------------------------------------------------
# S2B-IMP-H002 non-forgeable authoritative evidence
# ---------------------------------------------------------------------------


def test_s2b_imp_h002_no_arbitrary_material_issuance_api() -> None:
    for name in (
        "_from_evaluator",
        "_from_material",
        "_mint",
        "_attach_attestation",
        "_issue",
    ):
        assert not hasattr(PatternEvidence, name), name
    signature = inspect.signature(pattern_module._issue_pattern_evidence)
    assert tuple(signature.parameters) == ("pattern", "items", "supplied_time", "prior")
    forbidden = {
        "match_state",
        "direction",
        "validity",
        "reason",
        "lineage",
        "sample_lineage",
        "authority_lineage",
        "constituent_revisions",
        "revision",
        "predecessor_evidence_fingerprint",
        "window_start",
        "window_end",
        "event_time",
        "knowledge_time",
        "evaluation_boundary",
        "fingerprint",
        "material",
    }
    assert forbidden.isdisjoint(signature.parameters)
    for parameter in signature.parameters.values():
        assert parameter.kind is not inspect.Parameter.VAR_KEYWORD
    with pytest.raises(TypeError):
        pattern_module._issue_pattern_evidence(match_state=PatternMatchState.MATCHED)


def test_s2b_imp_h002_coherent_forgery_is_impossible() -> None:
    state = s1e_state()
    version = PatternVersion.standard("P-DC-001")
    constituents = bars(("10", "14", "9", "13"), state=state)
    legitimate = evaluate_pattern(version, constituents)
    assert legitimate.match_state is PatternMatchState.NOT_MATCHED
    coherent = dict(
        evidenced_material(legitimate),
        match_state=PatternMatchState.MATCHED,
        direction=PatternDirection.NEUTRAL,
        validity=PatternValidity.VALID,
        reason="MATCHED",
    )
    with pytest.raises(PatternError):
        PatternEvidence(**coherent)
    with pytest.raises((AttributeError, PatternError)):
        PatternEvidence._from_evaluator(**coherent)  # type: ignore[attr-defined]
    with pytest.raises(PatternError):
        replace(
            legitimate,
            match_state=PatternMatchState.MATCHED,
            direction=PatternDirection.NEUTRAL,
        )
    manual = object.__new__(PatternEvidence)
    for name, value in coherent.items():
        object.__setattr__(manual, name, value)
    object.__setattr__(manual, "_attestation", None)
    with pytest.raises(PatternError):
        manual.__post_init__()
    refused = evaluate_pattern(version, constituents)
    assert refused.match_state is PatternMatchState.NOT_MATCHED
    assert refused.fingerprint == legitimate.fingerprint


def test_s2b_imp_h002_caller_selected_fields_are_rejected() -> None:
    state = s1e_state()
    evidence = evaluate_pattern(
        PatternVersion.standard("P-MS-001"),
        bars(*GOLDEN_MATCHED_WINDOWS["P-MS-001"][:3], state=state),
    )
    for field, value in (
        ("validity", PatternValidity.DEGRADED),
        ("window_start", evidence.window_start + timedelta(seconds=60)),
        ("knowledge_time", evidence.knowledge_time + timedelta(seconds=1)),
        ("evaluation_boundary", evidence.evaluation_boundary + timedelta(seconds=1)),
        ("lineage", tuple(reversed(evidence.lineage))),
        ("sample_lineage", tuple(reversed(evidence.sample_lineage))),
        ("authority_lineage", tuple(reversed(evidence.authority_lineage))),
        ("pattern", PatternVersion.standard("P-DC-001")),
        ("constituent_revisions", (9, 9, 9)),
    ):
        with pytest.raises((PatternError, TypeError)):
            replace(evidence, **{field: value})
        manual = object.__new__(PatternEvidence)
        for name in EVIDENCE_FIELDS:
            object.__setattr__(manual, name, getattr(evidence, name))
        object.__setattr__(manual, field, value)
        object.__setattr__(manual, "_attestation", None)
        with pytest.raises(PatternError):
            manual.__post_init__()


def test_s2b_imp_h002_tampered_or_copied_evidence_is_rejected() -> None:
    state = s1e_state()
    evidence = evaluate_pattern(
        PatternVersion.standard("P-DC-001"), bars(("10", "11", "9", "10"), state=state)
    )
    assert evidence._is_attested()
    with pytest.raises(PatternError):
        copy.copy(evidence)
    with pytest.raises(PatternError):
        copy.deepcopy(evidence)
    with pytest.raises(PatternError):
        pickle.dumps(evidence)
    object.__setattr__(evidence, "match_state", PatternMatchState.NOT_MATCHED)
    assert not evidence._is_attested()
    with pytest.raises(PatternEvaluationError):
        canonical_evidence_order((evidence,))


# ---------------------------------------------------------------------------
# S2B-IMP-H003 evaluator-derived revision and predecessor chain
# ---------------------------------------------------------------------------


def chain_evidence_fingerprints(
    evidences: tuple[PatternEvidence, ...],
) -> tuple[str, ...]:
    return tuple(item.fingerprint for item in evidences)


def test_s2b_imp_h003_raw_revision_and_predecessor_inputs_are_removed() -> None:
    state = s1e_state()
    version = PatternVersion.standard("P-DC-001")
    constituents = bars(("10", "11", "9", "10"), state=state)
    for function in (evaluate_pattern, evaluate_patterns):
        parameters = inspect.signature(function).parameters
        assert "revision" not in parameters
        assert "revisions" not in parameters
        assert "predecessor_evidence_fingerprint" not in parameters
        assert "predecessor_evidence_fingerprints" not in parameters
    with pytest.raises(TypeError):
        evaluate_pattern(version, constituents, revision=1)  # type: ignore[call-arg]
    with pytest.raises(TypeError):
        evaluate_pattern(  # type: ignore[call-arg]
            version, constituents, predecessor_evidence_fingerprint="a" * 64
        )
    with pytest.raises(TypeError):
        evaluate_patterns(  # type: ignore[call-arg]
            [version], constituents, revisions={"P-DC-001": 1}
        )
    with pytest.raises(TypeError):
        evaluate_patterns(  # type: ignore[call-arg]
            [version], constituents, predecessor_evidence_fingerprints={"P-DC-001": "a" * 64}
        )
    with pytest.raises(PatternEvaluationError):
        evaluate_pattern(version, constituents, state="a" * 64)  # type: ignore[arg-type]
    with pytest.raises(PatternEvaluationError):
        evaluate_patterns([version], constituents, states={"P-MB-001": PatternEvaluationState()})


def test_s2b_imp_h003_scope_covers_pattern_identity_source_contract_environment() -> None:
    state = s1e_state()
    head = evaluate_pattern(
        PatternVersion.standard("P-DC-001"), bars(("10", "11", "9", "10"), state=state)
    )
    scope = PatternEvaluationState((head,)).scope_key
    assert scope is not None
    assert scope[:5] == (
        "P-DC-001",
        1,
        head.source_id.as_text(),
        head.contract_id.as_text(),
        head.environment.value,
    )
    assert scope[5:8] == (
        head.timeframe_fingerprint,
        head.timeframe_version,
        head.timeframe_duration_seconds,
    )
    assert scope[8:] == (head.window_start.isoformat(), head.window_end.isoformat())


def test_s2b_imp_h003_wrong_scope_is_rejected() -> None:
    state = s1e_state()
    version = PatternVersion.standard("P-DC-001")
    original = bars(("10", "11", "9", "10"), state=state)
    head = evaluate_pattern(version, original)
    chain = PatternEvaluationState((head,))
    correction = (
        revised_pair(
            0,
            open_value="10",
            high="12",
            low="9",
            close="10.5",
            state=state,
            prior_candle=original[0].candle,
        ),
    )
    with pytest.raises(PatternEvaluationError):
        evaluate_pattern(PatternVersion.standard("P-MB-001"), correction, state=chain)
    other_state = s1e_state(contract=OTHER_CONTRACT)
    other_contract = bars(("10", "11", "9", "10"), state=other_state, contract=OTHER_CONTRACT)
    other_head = evaluate_pattern(version, other_contract)
    with pytest.raises(PatternEvaluationError):
        evaluate_pattern(version, correction, state=PatternEvaluationState((other_head,)))
    other_window = bars(
        ("10", "11", "9", "10"),
        ("10", "11", "9", "10"),
        state=state,
        frame=Timeframe("Min5", 300),
    )
    window_head = evaluate_pattern(version, other_window[:1])
    shifted = (
        revised_pair(
            5,
            open_value="10",
            high="12",
            low="9",
            close="10.5",
            state=state,
            prior_candle=other_window[0].candle,
        ),
    )
    with pytest.raises(PatternEvaluationError):
        evaluate_pattern(version, shifted, state=PatternEvaluationState((window_head,)))


def test_s2b_imp_h003_skip_fork_and_overwrite_are_rejected() -> None:
    state = s1e_state()
    version = PatternVersion.standard("P-DC-001")
    original = bars(("10", "11", "9", "10"), state=state)
    head = evaluate_pattern(version, original)
    first_chain = PatternEvaluationState((head,))
    correction = (
        revised_pair(
            0,
            open_value="10",
            high="12",
            low="9",
            close="10.5",
            state=state,
            prior_candle=original[0].candle,
        ),
    )
    second = evaluate_pattern(version, correction, state=first_chain)
    chain = first_chain.record(second)
    with pytest.raises(PatternEvaluationError):
        PatternEvaluationState((second,))
    again = (
        revised_pair(
            0,
            open_value="10",
            high="13",
            low="9",
            close="10.9",
            state=state,
            prior_candle=correction[0].candle,
        ),
    )
    third = evaluate_pattern(version, again, state=chain)
    with pytest.raises(PatternEvaluationError):
        PatternEvaluationState((head,)).record(third)
    fork = (
        revised_pair(
            0,
            open_value="10",
            high="11.9",
            low="9",
            close="10.1",
            state=state,
            prior_candle=original[0].candle,
        ),
    )
    sibling = evaluate_pattern(version, fork, state=first_chain)
    with pytest.raises(PatternEvaluationError):
        chain.record(sibling)
    with pytest.raises(PatternEvaluationError):
        chain.record(second)
    assert [item.revision for item in chain.record(third).evidences] == [0, 1, 2]


def test_s2b_imp_h003_constituent_continuity_is_required() -> None:
    state = s1e_state()
    version = PatternVersion.standard("P-DC-001")
    original = bars(("10", "11", "9", "10"), state=state)
    head = evaluate_pattern(version, original)
    chain = PatternEvaluationState((head,))
    skipped_revision = (
        revised_pair(
            0,
            open_value="10",
            high="12",
            low="9",
            close="10.5",
            state=state,
            prior_candle=original[0].candle,
            revision_delta=2,
        ),
    )
    with pytest.raises(PatternEvaluationError):
        evaluate_pattern(version, skipped_revision, state=chain)
    wrong_predecessor = (
        revised_pair(
            0,
            open_value="10",
            high="12",
            low="9",
            close="10.5",
            state=state,
            prior_candle=original[0].candle,
            predecessor="f" * 64,
        ),
    )
    with pytest.raises(PatternEvaluationError):
        evaluate_pattern(version, wrong_predecessor, state=chain)


def test_s2b_imp_h003_valid_correction_derives_the_immediate_link() -> None:
    state = s1e_state()
    version = PatternVersion.standard("P-EC-001")
    rows = GOLDEN_MATCHED_WINDOWS["P-EC-001"][:2]
    original = bars(*rows, state=state)
    head = evaluate_pattern(version, original)
    assert head.revision == 0
    assert head.predecessor_evidence_fingerprint is None
    unchanged_first, revised_second = (
        original[0],
        revised_pair(
            1,
            open_value="9.5",
            high="13",
            low="9.5",
            close="12.6",
            state=state,
            prior_candle=original[1].candle,
        ),
    )
    successor = evaluate_pattern(
        version,
        (unchanged_first, revised_second),
        state=PatternEvaluationState((head,)),
    )
    assert successor.revision == head.revision + 1
    assert successor.predecessor_evidence_fingerprint == head.fingerprint
    assert successor.lineage[0] == head.lineage[0]
    assert successor.lineage[1] != head.lineage[1]
    assert chain_evidence_fingerprints((head, successor)) == (
        head.fingerprint,
        successor.fingerprint,
    )


def test_s2b_imp_h003_no_change_revision_is_rejected() -> None:
    state = s1e_state()
    version = PatternVersion.standard("P-DC-001")
    original = bars(("10", "11", "9", "10"), state=state)
    head = evaluate_pattern(version, original)
    chain = PatternEvaluationState((head,))
    with pytest.raises(PatternEvaluationError):
        evaluate_pattern(version, original, state=chain)
    with pytest.raises(PatternEvaluationError):
        evaluate_patterns([version], original, states={"P-DC-001": chain})


def test_s2b_imp_h003_replay_reproduces_the_chain() -> None:
    state = s1e_state()
    version = PatternVersion.standard("P-DC-001")
    original = bars(("10", "11", "9", "10"), state=state)
    head = evaluate_pattern(version, original)

    def replay() -> tuple[str, ...]:
        chain = PatternEvaluationState((head,))
        first_candle = revised_pair(
            0,
            open_value="10",
            high="12",
            low="9",
            close="10.5",
            state=state,
            prior_candle=original[0].candle,
        )
        first = evaluate_pattern(version, (first_candle,), state=chain)
        chain = chain.record(first)
        second_candle = revised_pair(
            0,
            open_value="10",
            high="12.5",
            low="9",
            close="10.8",
            state=state,
            prior_candle=first_candle.candle,
        )
        second = evaluate_pattern(version, (second_candle,), state=chain)
        chain = chain.record(second)
        return chain_evidence_fingerprints(chain.evidences)

    assert replay() == replay()
    assert len(replay()) == 3


# ---------------------------------------------------------------------------
# S2B-IMP-H004 fully content-bound definition identity
# ---------------------------------------------------------------------------


def test_s2b_imp_h004_definition_golden_fingerprints() -> None:
    for identifier in PATTERN_ALLOWLIST:
        definition = PatternDefinition.standard(identifier)
        assert definition.version == 1, identifier
        assert definition.fingerprint == GOLDEN_DEFINITION_FINGERPRINTS[identifier], identifier
        assert (
            PatternVersion.standard(identifier).fingerprint
            == GOLDEN_VERSION_FINGERPRINTS[identifier]
        ), identifier


def test_s2b_imp_h004_definition_material_binds_every_frozen_semantic() -> None:
    import hct_backend.patterns as module

    definition = PatternDefinition.standard("P-MS-001")
    assert definition.input_contract == "CANDLEBAR_OHLC_PLUS_EVALUATOR_ISSUED_FEATURE_SAMPLE"
    assert definition.source_fields == ("open", "high", "low", "close")
    assert definition.timeframe_identity == (
        "Min1:60:1:UNIX_EPOCH_MULTIPLES",
        "Min5:300:1:UNIX_EPOCH_MULTIPLES",
        "Min15:900:1:UNIX_EPOCH_MULTIPLES",
    )
    assert definition.decimal_policy_version == "FEATURE_DECIMAL_V1"
    assert definition.decimal_precision == 76
    assert definition.rounding_mode == "ROUND_HALF_EVEN"
    assert definition.small_body_max == SMALL_BODY_MAX
    assert definition.long_body_min == LONG_BODY_MIN
    assert definition.engulfing_bounds == "BOUNDS_INCLUSIVE"
    assert definition.midpoint_equality == "BOUNDS_INCLUSIVE"
    assert definition.star_gap_policy == "NONE_IN_V1"
    assert definition.zero_range_policy == "ZERO_RANGE_PRIMITIVE_UNKNOWN"
    assert definition.finality_requirement == "CLOSED_BAR_REQUIRED"
    assert definition.formation_rule == "EXACT_ORDERED_CONTIGUOUS_CLOSED_PAIRS_K"
    assert definition.cardinality_policy == ("EXACT_CARDINALITY_OVER_CARDINALITY_WINDOW_INVALID")
    assert definition.evaluation_boundary_rule == (
        "S2B_CANONICAL_EVALUATION_BOUNDARY=max(window_end,knowledge_time)"
    )
    assert definition.direction_policy == (
        "MATCHED_REQUIRES_CONCRETE_DIRECTION_NOT_MATCHED_REQUIRES_NONE"
    )
    assert definition.match_state_policy == "RESTRICTIVE_VALIDITY_REQUIRES_INDETERMINATE"
    assert definition.equation == module.PATTERN_EQUATIONS["P-MS-001"]
    assert "close[2]>=midpoint(open[0],close[0])" in definition.equation
    assert "r[1]<=SMALL_BODY_MAX" in definition.equation
    assert "gap=NONE_IN_V1" in definition.equation
    assert len(module.PATTERN_EQUATIONS) == 6


def test_s2b_imp_h004_definition_mutation_is_rejected() -> None:
    for identifier in PATTERN_ALLOWLIST:
        definition = PatternDefinition.standard(identifier)
        with pytest.raises(PatternError):
            replace_definition(definition, equation=f"MUTATED_EQUATION:{identifier}")
        with pytest.raises(PatternError):
            replace_definition(definition, bar_cardinality=definition.bar_cardinality + 1)
        with pytest.raises(PatternError):
            replace_definition(
                definition,
                timeframe_identity=("Min1:60:2:UNIX_EPOCH_MULTIPLES",),
            )


def test_s2b_imp_h004_every_material_key_is_fingerprint_visible() -> None:
    import hct_backend.patterns as module

    for identifier in PATTERN_ALLOWLIST:
        definition = PatternDefinition.standard(identifier)
        material = dict(definition.material)
        baseline = module._hash(material)
        assert baseline == definition.fingerprint, identifier
        for key, value in material.items():
            mutated = dict(material)
            if isinstance(value, list):
                mutated[key] = ["S2B_MUTATED"]
            elif isinstance(value, bool):
                mutated[key] = not value
            elif isinstance(value, int):
                mutated[key] = value + 1
            else:
                mutated[key] = "S2B_MUTATED"
            assert module._hash(mutated) != baseline, (identifier, key)
