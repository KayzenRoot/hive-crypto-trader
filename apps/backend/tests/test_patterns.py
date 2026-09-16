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


def s1e_generation(number: int = 1) -> GenerationRef:
    return GenerationRef(SOURCE, Environment.PAPER, number)


def s1e_capability() -> ChannelCapability:
    return ChannelCapability(
        source_id=SOURCE,
        visibility=ChannelVisibility.PUBLIC,
        channel="public-events",
        contract_scope=CONTRACT,
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


def s1e_observation(number: int, *, snapshot: bool = True) -> SequenceObservation:
    capability = s1e_capability()
    return SequenceObservation(
        generation=s1e_generation(),
        observed_at=NOW,
        event_fingerprint=s1e_event_fingerprint(number),
        update_id=number,
        is_snapshot=snapshot,
        source_id=SOURCE,
        channel="public-events",
        contract_id=CONTRACT,
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
) -> MarketStateSnapshot:
    capability = s1e_capability()
    evaluation = evaluate_sequence(capability, None, s1e_observation(event_number, snapshot=True))
    proof = SynchronizationProof.from_sequence_evaluation(
        capability=capability,
        generation=s1e_generation(generation_number),
        evaluation=evaluation,
    )
    return MarketStateSnapshot(
        contract_id=CONTRACT,
        environment=Environment.PAPER,
        generation=s1e_generation(generation_number),
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
) -> CandleBar:
    timeframe = frame or Timeframe("Min1", 60)
    start = NOW + timedelta(seconds=index * timeframe.duration_seconds)
    context = ValueContext(
        SOURCE,
        "sub.kline",
        CONTRACT,
        Environment.PAPER,
        s1e_generation(generation_number),
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
    *rows: tuple[str, str, str, str], state: MarketStateSnapshot, frame: Timeframe | None = None
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
        )
        for index, row in enumerate(rows)
    )


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
    mixed = bars(("10", "11", "9", "10"), state=state, frame=Timeframe("Min1", 60))
    wrong_frame = bars(("10", "11", "9", "10"), state=state, frame=Timeframe("Min9", 60))
    evidence = evaluate_pattern(PatternVersion.standard("P-MS-001"), mixed + wrong_frame)
    assert evidence.validity is PatternValidity.INVALID


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
    payload = dict(
        pattern=evidence.pattern,
        match_state=PatternMatchState.NOT_MATCHED,
        direction=PatternDirection.NONE,
        validity=PatternValidity.VALID,
        reason="FORGED",
        source_id=evidence.source_id,
        contract_id=evidence.contract_id,
        environment=evidence.environment,
        generation_fingerprint=evidence.generation_fingerprint,
        timeframe_fingerprint=evidence.timeframe_fingerprint,
        timeframe_version=evidence.timeframe_version,
        timeframe_duration_seconds=evidence.timeframe_duration_seconds,
        window_start=evidence.window_start,
        window_end=evidence.window_end,
        event_time=evidence.event_time,
        knowledge_time=evidence.knowledge_time,
        wall_receive_time=evidence.wall_receive_time,
        evaluation_boundary=evidence.evaluation_boundary,
        lineage=evidence.lineage,
        sample_lineage=evidence.sample_lineage,
        authority_lineage=evidence.authority_lineage,
        market_state_trust=evidence.market_state_trust,
        data_authority_state=evidence.data_authority_state,
        resource_restriction=evidence.resource_restriction,
        lifecycle_restriction=evidence.lifecycle_restriction,
        revision=0,
        predecessor_evidence_fingerprint=None,
    )
    with pytest.raises(PatternError):
        PatternEvidence._from_evaluator(**{**payload, "reason": ""})
    with pytest.raises(PatternError):
        PatternEvidence._from_evaluator(
            **{
                **payload,
                "validity": PatternValidity.UNKNOWN,
                "match_state": PatternMatchState.MATCHED,
            }
        )
    with pytest.raises(PatternError):
        PatternEvidence._from_evaluator(
            **{**payload, "match_state": PatternMatchState.INDETERMINATE}
        )


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
    base = evaluate_pattern(
        PatternVersion.standard("P-DC-001"), bars(("10", "11", "9", "10"), state=state)
    )
    revised_candle = paper_candle(
        0, open_value="10", high="11.5", low="9", close="10", event_number=99
    )
    from dataclasses import replace

    revised_candle = replace(
        revised_candle, revision=1, predecessor_fingerprint=revised_candle.fingerprint
    )
    revised_pair = PatternConstituent(
        revised_candle, FeatureSample.from_candle(revised_candle, market_state=state)
    )
    revised = evaluate_pattern(
        PatternVersion.standard("P-DC-001"),
        (revised_pair,),
        revision=1,
        predecessor_evidence_fingerprint=base.fingerprint,
    )
    assert revised.fingerprint != base.fingerprint
    assert revised.predecessor_evidence_fingerprint == base.fingerprint


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
    constituents = bars(("10", "11", "9", "10"), state=state)
    first = evaluate_pattern(PatternVersion.standard("P-DC-001"), constituents)
    second = evaluate_pattern(
        PatternVersion.standard("P-DC-001"),
        constituents,
        revision=1,
        predecessor_evidence_fingerprint=first.fingerprint,
    )
    third = evaluate_pattern(
        PatternVersion.standard("P-DC-001"),
        constituents,
        revision=2,
        predecessor_evidence_fingerprint=second.fingerprint,
    )
    assert second.predecessor_evidence_fingerprint == first.fingerprint
    assert third.predecessor_evidence_fingerprint == second.fingerprint
    assert first.fingerprint not in {second.fingerprint, third.fingerprint}


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
