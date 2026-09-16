import json
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path

import pytest

import hct_backend.features as feature_module
from hct_backend.contracts import Environment, IdentityKind, StableId
from hct_backend.features import (
    AlignedWindowEvidence,
    FeatureAuthorityEvidence,
    FeatureAxisRestriction,
    FeatureDefinition,
    FeatureError,
    FeatureEvaluationError,
    FeatureRegistry,
    FeatureRegistryError,
    FeatureSample,
    FeatureSnapshot,
    FeatureValidity,
    FeatureVersion,
    RecursiveAccumulatorState,
    align_closed_1m_candles,
    evaluate_feature,
    evaluate_feature_series,
    evaluate_snapshot,
    restore_recursive_state,
)
from hct_backend.market_truth import (
    ChannelCapability,
    ChannelVisibility,
    ClockHealth,
    DataAuthorityState,
    GenerationRef,
    LifecycleRestriction,
    MarketStateSnapshot,
    MarketStateTrust,
    QualityAssessment,
    QualityReason,
    ResourceAdmissionEvidence,
    ResourceDisposition,
    SequenceMode,
    SequenceObservation,
    SynchronizationProof,
    UpdateSemantics,
    derive_data_authority,
    evaluate_sequence,
)
from hct_backend.quota_governor import AdmissionDecision, AdmissionOutcome, AdmissionReason
from hct_backend.s1f_numeric import DecimalValue, NumericPolicyError
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
SOURCE = StableId(kind=IdentityKind.EXCHANGE, value="fixture")
CONTRACT = StableId(kind=IdentityKind.INSTRUMENT, value="btc-usdt")
S1E_SOURCE = StableId(kind=IdentityKind.EXCHANGE, value="exchange-reference")
S1E_CONTRACT = StableId(kind=IdentityKind.INSTRUMENT, value="btc-usdt-perpetual")
S1E_PROVENANCE = "a" * 64

# The adversarial sequences below carry non-terminating recurrence state: a
# higher-precision accumulator leaks a 1e-18 difference into the published
# value if any recursive update is not canonicalized before the next update.
RECURRENCE_VALUES = ["1", "2", "3", "5", "8", "13", "21", "34", "55", "89", "144", "233"]
RECURRENCE_N = 6


def samples(values: list[str]) -> tuple[FeatureSample, ...]:
    return tuple(
        FeatureSample.from_decimal(value, index=index) for index, value in enumerate(values)
    )


def ohlc_samples(values: list[tuple[str, str, str]]) -> tuple[FeatureSample, ...]:
    result = []
    for index, (high, low, close) in enumerate(values):
        sample = FeatureSample.from_decimal(close, index=index)
        result.append(
            replace(
                sample,
                high=DecimalValue.parse(high),
                low=DecimalValue.parse(low),
                close=DecimalValue.parse(close),
            )
        )
    return tuple(result)


def volume_samples(values: list[str]) -> tuple[FeatureSample, ...]:
    result = []
    for index, value in enumerate(values):
        sample = FeatureSample.from_decimal(value, index=index)
        result.append(
            replace(
                sample,
                quantity=Quantity(
                    DecimalValue.parse(value),
                    QuantityUnit.CONTRACTS_PROVIDER_NATIVE_V1,
                    "S1F",
                ),
            )
        )
    return tuple(result)


def derived_ohlc(values: list[str], *, parameter_n: int) -> tuple[FeatureSample, ...]:
    """OHLC fixtures whose closes exercise the same recurrence sequence."""

    del parameter_n
    rows = []
    for value in values:
        number = Decimal(value)
        rows.append((str(number + 2), str(number - 1), value))
    return ohlc_samples(rows)


def inputs_for(identifier: str, values: list[str]) -> tuple[FeatureSample, ...]:
    if identifier == "F-ATR-001":
        return derived_ohlc(values, parameter_n=RECURRENCE_N)
    return samples(values)


def authority(
    sample: FeatureSample,
    *,
    trust: MarketStateTrust = MarketStateTrust.TRUSTED,
    resource: ResourceDisposition = ResourceDisposition.AVAILABLE,
    lifecycle: LifecycleRestriction = LifecycleRestriction.NONE,
    data_authority: DataAuthorityState = DataAuthorityState.ALLOW_NEW_EXPOSURE,
    reasons: tuple[QualityReason, ...] = (QualityReason.FRESH_VALID,),
) -> FeatureAuthorityEvidence:
    return FeatureAuthorityEvidence.fixture(
        market_state_fingerprint=sample.market_state_fingerprint,
        market_state_trust=trust,
        data_authority_state=data_authority,
        data_authority_reasons=reasons,
        resource_disposition=resource,
        lifecycle_restriction=lifecycle,
    )


def constituent_authority(
    candle: CandleBar,
    *,
    trust: MarketStateTrust = MarketStateTrust.TRUSTED,
    resource: ResourceDisposition = ResourceDisposition.AVAILABLE,
    lifecycle: LifecycleRestriction = LifecycleRestriction.NONE,
    reasons: tuple[QualityReason, ...] = (QualityReason.FRESH_VALID,),
) -> FeatureAuthorityEvidence:
    return FeatureAuthorityEvidence.fixture_for_candle(
        candle,
        market_state_trust=trust,
        resource_disposition=resource,
        lifecycle_restriction=lifecycle,
        data_authority_reasons=reasons,
    )


def with_authority(sample: FeatureSample, **kwargs: object) -> FeatureSample:
    return replace(sample, authority=authority(sample, **kwargs))  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Canonical S1E evidence fixtures
# ---------------------------------------------------------------------------


def s1e_generation(number: int = 1) -> GenerationRef:
    return GenerationRef(S1E_SOURCE, Environment.PAPER, number)


def s1e_capability() -> ChannelCapability:
    return ChannelCapability(
        source_id=S1E_SOURCE,
        visibility=ChannelVisibility.PUBLIC,
        channel="public-events",
        contract_scope=S1E_CONTRACT,
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
        event_fingerprint=(str(number) * 64)[:64],
        update_id=number,
        is_snapshot=snapshot,
        source_id=S1E_SOURCE,
        channel="public-events",
        contract_id=S1E_CONTRACT,
        schema_version=1,
        capability_fingerprint=capability.fingerprint,
        capability_policy_version=capability.policy_version,
        visibility=ChannelVisibility.PUBLIC,
    )


def s1e_resource(disposition: ResourceDisposition = ResourceDisposition.AVAILABLE):
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
) -> MarketStateSnapshot:
    capability = s1e_capability()
    evaluation = evaluate_sequence(capability, None, s1e_observation(99, snapshot=True))
    proof = SynchronizationProof.from_sequence_evaluation(
        capability=capability,
        generation=s1e_generation(),
        evaluation=evaluation,
    )
    return MarketStateSnapshot(
        contract_id=S1E_CONTRACT,
        environment=Environment.PAPER,
        generation=s1e_generation(),
        source_id=S1E_SOURCE,
        source_version=1,
        provenance_fingerprint=S1E_PROVENANCE,
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
                resource=s1e_resource(),
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


def paper_candle(index: int, close: str) -> CandleBar:
    frame = Timeframe("Min1", 60)
    start = NOW + timedelta(minutes=index)
    context = ValueContext(
        S1E_SOURCE,
        "sub.kline",
        S1E_CONTRACT,
        Environment.PAPER,
        s1e_generation(),
        1,
        S1E_PROVENANCE,
        ("%064x" % (index + 1)),
        start,
        start,
        start,
        index,
    )
    return CandleBar(
        context,
        frame,
        start,
        start + timedelta(minutes=1),
        DecimalValue.parse("10"),
        DecimalValue.parse(str(12 + index)),
        DecimalValue.parse("9"),
        DecimalValue.parse(close),
        Quantity(DecimalValue.parse("2"), QuantityUnit.CONTRACTS_PROVIDER_NATIVE_V1, "S1F"),
        ProviderTransactionAmount(DecimalValue.parse("20"), "S1F"),
        Finality.OPEN,
        OrderedLineage.from_fingerprints(("%064x" % (index + 100),), start),
    )


# ---------------------------------------------------------------------------
# Proof obligations PO-F01 .. PO-F10
# ---------------------------------------------------------------------------


def test_po_f08_exact_feature_allowlist_and_registry_are_immutable() -> None:
    feature = FeatureVersion.standard("F-SMA-001", parameter_n=3)
    registry = FeatureRegistry().register(feature)
    assert registry.resolve("F-SMA-001", 1) is feature
    assert registry.register(feature) is registry
    changed = FeatureVersion(replace(feature.definition, source_field="different-material-input"))
    with pytest.raises(FeatureRegistryError):
        registry.register(changed)
    with pytest.raises(ValueError):
        FeatureDefinition.standard("F-UNKNOWN-001")


@pytest.mark.parametrize(
    ("feature", "values", "expected"),
    [
        (FeatureVersion.standard("F-RET-001"), ["10", "12"], "0.2"),
        (FeatureVersion.standard("F-SMA-001", parameter_n=3), ["1", "2", "3"], "2"),
        (FeatureVersion.standard("F-EMA-001", parameter_n=3), ["1", "2", "3", "4"], "3"),
        (FeatureVersion.standard("F-ROC-001", parameter_n=2), ["2", "4", "6"], "2"),
        (FeatureVersion.standard("F-VSMA-001", parameter_n=3), ["1", "2", "3"], "2"),
    ],
)
def test_po_f01_standard_feature_vectors_are_deterministic(
    feature: FeatureVersion, values: list[str], expected: str
) -> None:
    inputs = volume_samples(values) if feature.canonical_id == "F-VSMA-001" else samples(values)
    result = evaluate_feature(feature, inputs)
    assert result.validity is FeatureValidity.VALID
    assert result.value is not None
    assert result.value.canonical_text == expected
    assert len(result.fingerprint) == 64


def test_po_f04_warmup_boundaries_and_rsi_edge_cases_are_exact() -> None:
    feature = FeatureVersion.standard("F-RSI-001", parameter_n=3)
    results = evaluate_feature_series(feature, samples(["10", "11", "12", "13"]))
    assert [result.validity for result in results] == [
        FeatureValidity.WARMUP,
        FeatureValidity.WARMUP,
        FeatureValidity.WARMUP,
        FeatureValidity.VALID,
    ]
    assert results[-1].value is not None and results[-1].value.canonical_text == "100"
    flat = evaluate_feature(feature, samples(["10", "10", "10", "10"]))
    down = evaluate_feature(feature, samples(["10", "9", "8", "7"]))
    assert flat.value is not None and flat.value.canonical_text == "50"
    assert down.value is not None and down.value.canonical_text == "0"


def test_po_f01_true_range_atr_and_canonical_recursive_state() -> None:
    feature = FeatureVersion.standard("F-ATR-001", parameter_n=3)
    values = ohlc_samples(
        [("12", "9", "10"), ("13", "10", "12"), ("15", "11", "14"), ("16", "13", "15")]
    )
    results = evaluate_feature_series(feature, values)
    assert results[1].validity is FeatureValidity.WARMUP
    assert (
        results[2].value is not None and results[2].value.canonical_text == "3.333333333333333333"
    )
    assert results[2].recursive_state is not None
    assert all(
        component.material_scale == 18 for component in results[2].recursive_state.components
    )
    assert (
        results[2].recursive_state.serialize()
        == type(results[2].recursive_state)
        .deserialize(results[2].recursive_state.serialize())
        .serialize()
    )


def test_po_f10_serialized_resume_is_bit_for_bit_equal() -> None:
    all_samples = samples(["1", "2", "3", "4", "5"])
    for identifier in ("F-EMA-001", "F-RSI-001"):
        feature = FeatureVersion.standard(identifier, parameter_n=3)
        full = evaluate_feature_series(feature, all_samples)
        resume_state = full[3].recursive_state
        assert resume_state is not None
        resumed = evaluate_feature_series(feature, all_samples[4:], initial_state=resume_state)
        assert resumed[-1].fingerprint == full[-1].fingerprint
        assert resumed[-1].recursive_state is not None
        assert resumed[-1].recursive_state.serialize() == full[-1].recursive_state.serialize()


def test_po_f03_point_in_time_and_no_lookahead_fail_closed() -> None:
    future = FeatureSample.from_decimal(
        "1",
        event_time=NOW + timedelta(minutes=1),
        knowledge_time=NOW + timedelta(minutes=1),
        wall_receive_time=NOW + timedelta(minutes=1),
    )
    result = evaluate_feature(
        FeatureVersion.standard("F-RET-001"), [samples(["1"])[0], future], evaluation_time=NOW
    )
    assert result.validity is FeatureValidity.INVALID
    assert result.reason == "FUTURE_EVENT_OR_KNOWLEDGE_EVIDENCE"


def test_po_f02_input_mutation_is_visible_in_output_fingerprint() -> None:
    original = samples(["1", "2", "3"])
    changed = replace(original[-1], fingerprint="f" * 64)
    left = evaluate_feature(FeatureVersion.standard("F-SMA-001", parameter_n=3), original)
    right = evaluate_feature(
        FeatureVersion.standard("F-SMA-001", parameter_n=3), [*original[:-1], changed]
    )
    assert left.value == right.value
    assert left.fingerprint != right.fingerprint


def _candle(index: int, close: str) -> CandleBar:
    frame = Timeframe("Min1", 60)
    start = NOW + timedelta(minutes=index)
    context = ValueContext(
        SOURCE,
        "sub.kline",
        CONTRACT,
        Environment.REPLAY,
        GenerationRef(SOURCE, Environment.REPLAY, 1),
        1,
        "a" * 64,
        ("%064x" % (index + 1)),
        start,
        start,
        start,
        index,
    )
    lineage = OrderedLineage.from_fingerprints(("%064x" % (index + 100),), start)
    return CandleBar(
        context,
        frame,
        start,
        start + timedelta(minutes=1),
        DecimalValue.parse("10"),
        DecimalValue.parse(str(12 + index)),
        DecimalValue.parse("9"),
        DecimalValue.parse(close),
        Quantity(DecimalValue.parse("2"), QuantityUnit.CONTRACTS_PROVIDER_NATIVE_V1, "S1F"),
        ProviderTransactionAmount(DecimalValue.parse("20"), "S1F"),
        Finality.OPEN,
        lineage,
    )


def _closed_candles(count: int = 5) -> tuple[CandleBar, ...]:
    opened = tuple(_candle(index, str(10 + index)) for index in range(count + 1))
    return tuple(
        CandleBar(
            current.context,
            current.timeframe,
            current.start,
            current.end,
            current.open,
            current.high,
            current.low,
            current.close,
            current.volume,
            current.amount,
            Finality.CLOSED,
            current.lineage,
            close_proof=CandleCloseProof._from_next_window_evidence(
                current_candle=current,
                next_window=opened[index + 1],
            ),
        )
        for index, current in enumerate(opened[:-1])
    )


def test_po_f07_deterministic_mtf_alignment_and_status_mapping() -> None:
    candles = _closed_candles()
    aligned = align_closed_1m_candles(candles[:5], 5, evaluation_time=NOW + timedelta(minutes=5))
    assert aligned.validity is FeatureValidity.VALID
    assert aligned.open is not None and aligned.open.canonical_text == "10"
    assert aligned.high is not None and aligned.high.canonical_text == "16"
    assert aligned.low is not None and aligned.low.canonical_text == "9"
    assert aligned.close is not None and aligned.close.canonical_text == "14"
    assert aligned.volume is not None and aligned.volume.value.canonical_text == "10"
    assert aligned.provenance == "DERIVED_ANALYTICAL_V1"
    assert aligned.event_time == candles[4].context.event_time
    assert aligned.knowledge_time == candles[4].context.knowledge_time
    assert aligned.wall_receive_time == candles[4].context.wall_receive_time
    assert (
        align_closed_1m_candles(candles[:4], 5, evaluation_time=NOW + timedelta(minutes=4)).validity
        is FeatureValidity.WARMUP
    )
    assert (
        align_closed_1m_candles(candles[:4], 5, evaluation_time=NOW + timedelta(minutes=5)).validity
        is FeatureValidity.UNKNOWN
    )
    assert (
        align_closed_1m_candles(tuple(reversed(candles[:5])), 5).validity is FeatureValidity.INVALID
    )


def test_po_f07_fifteen_minute_alignment_and_post_close_unknown() -> None:
    candles = _closed_candles(15)
    boundary = NOW + timedelta(minutes=15)
    aligned = align_closed_1m_candles(candles, 15, evaluation_time=boundary)
    assert aligned.validity is FeatureValidity.VALID
    assert aligned.end == boundary
    assert aligned.knowledge_time == candles[-1].context.knowledge_time
    assert (
        align_closed_1m_candles(candles[:-1], 15, evaluation_time=boundary).validity
        is FeatureValidity.UNKNOWN
    )


def test_po_f09_snapshot_keeps_one_source_identity() -> None:
    result = evaluate_snapshot(
        [
            FeatureVersion.standard("F-RET-001"),
            FeatureVersion.standard("F-SMA-001", parameter_n=2),
        ],
        samples(["1", "2"]),
    )
    assert len(result.values) == 2
    assert len(result.fingerprint) == 64


def test_po_f09_derived_alignment_is_non_authoritative_and_not_an_action_surface() -> None:
    aligned = align_closed_1m_candles(_closed_candles(), 5)
    assert aligned.provenance == "DERIVED_ANALYTICAL_V1"
    assert not hasattr(aligned, "order")
    assert not hasattr(aligned, "position")


def test_po_f01_all_eight_feature_ids_have_golden_vectors() -> None:
    close_inputs = samples(["10", "11", "12", "13"])
    ohlc_inputs = ohlc_samples([("12", "9", "10"), ("13", "10", "12"), ("15", "11", "14")])
    vectors = {
        "F-RET-001": evaluate_feature(FeatureVersion.standard("F-RET-001"), close_inputs),
        "F-SMA-001": evaluate_feature(
            FeatureVersion.standard("F-SMA-001", parameter_n=3), close_inputs
        ),
        "F-EMA-001": evaluate_feature(
            FeatureVersion.standard("F-EMA-001", parameter_n=3), close_inputs
        ),
        "F-ROC-001": evaluate_feature(
            FeatureVersion.standard("F-ROC-001", parameter_n=2), close_inputs
        ),
        "F-RSI-001": evaluate_feature(
            FeatureVersion.standard("F-RSI-001", parameter_n=3), close_inputs
        ),
        "F-TR-001": evaluate_feature(FeatureVersion.standard("F-TR-001"), ohlc_inputs[:1]),
        "F-ATR-001": evaluate_feature(
            FeatureVersion.standard("F-ATR-001", parameter_n=2), ohlc_inputs[:2]
        ),
        "F-VSMA-001": evaluate_feature(
            FeatureVersion.standard("F-VSMA-001", parameter_n=3), volume_samples(["1", "2", "3"])
        ),
    }
    assert set(vectors) == {
        "F-RET-001",
        "F-SMA-001",
        "F-EMA-001",
        "F-ROC-001",
        "F-RSI-001",
        "F-TR-001",
        "F-ATR-001",
        "F-VSMA-001",
    }
    assert all(item.validity is FeatureValidity.VALID for item in vectors.values())


def test_po_f04_first_valid_cardinality_for_every_feature() -> None:
    expected = {
        "F-RET-001": 2,
        "F-SMA-001": 4,
        "F-EMA-001": 4,
        "F-ROC-001": 5,
        "F-RSI-001": 5,
        "F-TR-001": 1,
        "F-ATR-001": 4,
        "F-VSMA-001": 4,
    }
    values = ["1", "2", "3", "5", "8", "13", "21"]
    for identifier, first_valid in expected.items():
        feature = FeatureVersion.standard(
            identifier,
            parameter_n=4 if identifier not in {"F-RET-001", "F-TR-001"} else None,
        )
        if identifier in {"F-TR-001", "F-ATR-001"}:
            inputs = derived_ohlc(values, parameter_n=4)
        elif identifier == "F-VSMA-001":
            inputs = volume_samples(values)
        else:
            inputs = samples(values)
        results = evaluate_feature_series(feature, inputs)
        if first_valid == 1:
            assert results[0].validity is FeatureValidity.VALID, identifier
            continue
        assert results[first_valid - 2].validity is FeatureValidity.WARMUP, identifier
        assert results[first_valid - 1].validity is FeatureValidity.VALID, identifier


def test_po_f05_unknown_and_contradictory_market_truth_remain_restrictive() -> None:
    base = samples(["1", "2"])
    unknown = with_authority(
        base[-1], trust=MarketStateTrust.UNKNOWN, reasons=(QualityReason.STALE,)
    )
    assert (
        evaluate_feature(FeatureVersion.standard("F-RET-001"), [base[0], unknown]).validity
        is FeatureValidity.UNKNOWN
    )
    degraded_truth = with_authority(
        base[-1], trust=MarketStateTrust.DEGRADED, reasons=(QualityReason.RESOURCE_DEGRADED,)
    )
    degraded_result = evaluate_feature(
        FeatureVersion.standard("F-RET-001"), [base[0], degraded_truth]
    )
    assert degraded_result.validity is FeatureValidity.DEGRADED
    assert degraded_result.value is not None
    retired = with_authority(base[-1], reasons=(QualityReason.RETIRED_GENERATION,))
    assert (
        evaluate_feature(FeatureVersion.standard("F-RET-001"), [base[0], retired]).validity
        is FeatureValidity.INVALID
    )
    mixed = replace(base[-1], generation_fingerprint="b" * 64)
    assert (
        evaluate_feature(FeatureVersion.standard("F-RET-001"), [base[0], mixed]).validity
        is FeatureValidity.INVALID
    )


def test_po_f06_generation_and_environment_namespaces_do_not_alias() -> None:
    replay = evaluate_feature(FeatureVersion.standard("F-RET-001"), samples(["1", "2"]))
    state = s1e_state()
    paper_samples = tuple(
        FeatureSample.from_candle(paper_candle(index, close), market_state=state)
        for index, close in enumerate(["10", "11"])
    )
    paper = evaluate_feature(FeatureVersion.standard("F-RET-001"), paper_samples)
    assert replay.fingerprint != paper.fingerprint
    assert replay.environment is Environment.REPLAY
    assert paper.environment is Environment.PAPER


def test_po_f02_definition_and_numeric_contract_guards_are_fail_closed() -> None:
    definition = FeatureDefinition.standard("F-SMA-001", parameter_n=3)
    invalid_definition_factories = (
        lambda: replace(definition, version=0),
        lambda: replace(definition, parameter_n=1, window=1),
        lambda: replace(definition, algorithm_version="UNKNOWN"),
        lambda: replace(definition, decimal_policy_version="UNKNOWN"),
        lambda: replace(definition, rounding_mode="ROUND_DOWN"),
        lambda: replace(FeatureDefinition.standard("F-RET-001"), window=2),
    )
    for factory in invalid_definition_factories:
        with pytest.raises(FeatureError):
            factory()
    with pytest.raises(FeatureError):
        FeatureVersion("not-a-definition")  # type: ignore[arg-type]
    with pytest.raises(FeatureRegistryError):
        FeatureRegistry().register("not-a-feature")  # type: ignore[arg-type]
    with pytest.raises(FeatureRegistryError):
        FeatureRegistry().resolve("F-SMA-001")
    with pytest.raises(NumericPolicyError):
        feature_module._canonical(Decimal("NaN"))
    assert feature_module._safe_canonical(Decimal("NaN")) is None
    with pytest.raises(FeatureEvaluationError):
        feature_module._mean([])


def test_po_f03_sample_identity_and_temporal_guards_are_fail_closed() -> None:
    base = samples(["1", "2"])[0]
    invalid_sample_factories = (
        lambda: replace(base, fingerprint="bad"),
        lambda: replace(
            base,
            source_id=StableId(kind=IdentityKind.INSTRUMENT, value="wrong-source"),
        ),
        lambda: replace(
            base,
            contract_id=StableId(kind=IdentityKind.EXCHANGE, value="wrong-contract"),
        ),
        lambda: replace(base, environment="REPLAY"),  # type: ignore[arg-type]
        lambda: replace(base, timeframe="Min1"),  # type: ignore[arg-type]
        lambda: replace(base, closed=1),  # type: ignore[arg-type]
        lambda: replace(base, knowledge_time=NOW + timedelta(minutes=2)),
        lambda: replace(base, interval_start=NOW + timedelta(minutes=2), interval_end=NOW),
        lambda: replace(base, high="1"),  # type: ignore[arg-type]
        lambda: replace(base, quantity="1"),  # type: ignore[arg-type]
        lambda: replace(base, authority="TRUSTED"),  # type: ignore[arg-type]
        lambda: replace(base, market_state_fingerprint="c" * 64),
    )
    for factory in invalid_sample_factories:
        with pytest.raises((FeatureError, NumericPolicyError)):
            factory()


def test_po_f08_state_output_and_snapshot_integrity_guards() -> None:
    feature = FeatureVersion.standard("F-EMA-001", parameter_n=3)
    result = evaluate_feature(feature, samples(["1", "2", "3", "4"]))
    state = result.recursive_state
    assert state is not None
    invalid_state_factories = (
        lambda: RecursiveAccumulatorState(),
        lambda: replace(state, algorithm_version="UNKNOWN"),
        lambda: replace(state, parameter_n=1),
        lambda: replace(state, components=(DecimalValue.parse("1"),)),
        lambda: replace(state, previous_input=DecimalValue.parse("1")),
        lambda: replace(state, processed_samples=0),
        lambda: replace(state, lineage=("bad",)),
        lambda: replace(state, lineage=(state.lineage[0], state.lineage[0])),
        lambda: replace(state, market_state_lineage=("bad",)),
        lambda: replace(state, authority_lineage=("bad",)),
        lambda: replace(state, environment="REPLAY"),  # type: ignore[arg-type]
        lambda: replace(state, knowledge_time=NOW + timedelta(days=1)),
        lambda: replace(state, previous_state_fingerprint="bad"),
        lambda: replace(state, decimal_policy_version="UNKNOWN"),
        lambda: replace(state, timeframe_fingerprint="bad"),
        lambda: replace(state, feature_version=0),
    )
    for factory in invalid_state_factories:
        with pytest.raises((FeatureError, TypeError)):
            factory()
    payload = json.loads(state.serialize())
    payload["state_fingerprint"] = "0" * 64
    with pytest.raises(FeatureError):
        RecursiveAccumulatorState.deserialize(payload)
    with pytest.raises(FeatureError):
        replace(result, value=None)
    with pytest.raises(FeatureError):
        replace(result, source_id=CONTRACT)
    with pytest.raises(FeatureError):
        replace(result, sample_count=True)
    with pytest.raises(FeatureError):
        FeatureSnapshot(
            values=(result, result),
            source_market_state_fingerprint=result.source_market_state_fingerprint,
            source_generation_fingerprint=result.source_generation_fingerprint,
            environment=result.environment,
            evaluation_time=NOW,
        )


def test_po_f07_mtf_structural_provenance_and_boundary_guards() -> None:
    opened = tuple(_candle(index, str(10 + index)) for index in range(6))
    candles = _closed_candles()
    with pytest.raises(FeatureEvaluationError):
        align_closed_1m_candles(candles, 10)
    with pytest.raises(FeatureEvaluationError):
        align_closed_1m_candles(candles, 5, authorities="TRUSTED")  # type: ignore[arg-type]
    assert align_closed_1m_candles((opened[0],), 5).validity is FeatureValidity.INVALID
    future_context = replace(
        candles[0].context,
        knowledge_time=NOW + timedelta(days=1),
        wall_receive_time=NOW + timedelta(days=1),
    )
    future = replace(candles[0], context=future_context)
    assert (
        align_closed_1m_candles((future, *candles[1:]), 5, evaluation_time=NOW).validity
        is FeatureValidity.INVALID
    )
    outside = align_closed_1m_candles((candles[0], _closed_candles(6)[5]), 5)
    assert outside.validity is FeatureValidity.INVALID
    mixed_provenance = replace(
        candles[0], context=replace(candles[0].context, provenance_fingerprint="b" * 64)
    )
    assert (
        align_closed_1m_candles((mixed_provenance, *candles[1:]), 5).validity
        is FeatureValidity.INVALID
    )
    mixed_quantity = replace(
        candles[0],
        volume=replace(candles[0].volume, source_contract_identity_version="OTHER"),
    )
    assert (
        align_closed_1m_candles((mixed_quantity, *candles[1:]), 5).validity
        is FeatureValidity.INVALID
    )


def test_po_f02_remaining_contract_branches_and_candle_coercion() -> None:
    definition = FeatureDefinition.standard("F-SMA-001", parameter_n=3)
    for change in (
        {"canonical_id": "UNKNOWN"},
        {"timeframe": "Min1"},
        {"semantic_family": ""},
    ):
        with pytest.raises(FeatureError):
            replace(definition, **change)
    assert len(FeatureVersion.standard("F-RET-001").fingerprint) == 64
    registry = FeatureRegistry().register(FeatureVersion.standard("F-RET-001"))
    registry = registry.register(FeatureVersion.standard("F-SMA-001", parameter_n=3))
    with pytest.raises(FeatureRegistryError):
        registry.resolve("F-RET-001", version=2)
    with pytest.raises(FeatureError):
        replace(samples(["1"])[0], value="1")
    with pytest.raises(FeatureError):
        replace(samples(["1"])[0], event_time=datetime(2026, 1, 1))
    with pytest.raises(FeatureError):
        replace(samples(["1"])[0], interval_start=NOW + timedelta(minutes=2), interval_end=NOW)
    opened = _candle(0, "10")
    candle_sample = FeatureSample.from_candle(opened)
    assert (
        evaluate_feature(FeatureVersion.standard("F-TR-001"), [candle_sample]).validity
        is FeatureValidity.WARMUP
    )
    assert feature_module._context_status((), None)[0] is FeatureValidity.WARMUP
    assert (
        evaluate_feature(
            FeatureVersion.standard("F-TR-001"),
            [replace(samples(["1"])[0], high=None, low=None, close=None)],
        ).validity
        is FeatureValidity.INVALID
    )
    assert (
        evaluate_feature(
            FeatureVersion.standard("F-TR-001"),
            [replace(samples(["1"])[0], high=DecimalValue.parse("2"), low=None)],
        ).validity
        is FeatureValidity.INVALID
    )
    assert (
        evaluate_feature(
            FeatureVersion.standard("F-VSMA-001", parameter_n=2), samples(["1", "2"])
        ).validity
        is FeatureValidity.INVALID
    )
    quantities = volume_samples(["1", "2"])
    mismatched_quantity = replace(
        quantities[-1],
        quantity=replace(quantities[-1].quantity, source_contract_identity_version="OTHER"),
    )
    assert (
        evaluate_feature(
            FeatureVersion.standard("F-VSMA-001", parameter_n=2),
            [quantities[0], mismatched_quantity],
        ).validity
        is FeatureValidity.INVALID
    )
    reversed_result = evaluate_feature(
        FeatureVersion.standard("F-RET-001"), list(reversed(samples(["1", "2"])))
    )
    assert reversed_result.validity is FeatureValidity.INVALID


def test_po_f08_feature_output_restrictive_metadata_guards() -> None:
    result = evaluate_feature(FeatureVersion.standard("F-RET-001"), samples(["1", "2"]))
    invalid_factories = (
        lambda: replace(result, reason=""),
        lambda: replace(result, sample_count=-1),
        lambda: replace(result, validity=FeatureValidity.UNKNOWN),
        lambda: replace(result, timeframe="Min1"),  # type: ignore[arg-type]
        lambda: replace(result, window_start=NOW + timedelta(days=1)),
        lambda: replace(result, lineage=()),
        lambda: replace(result, market_state_trust="TRUSTED"),  # type: ignore[arg-type]
        lambda: replace(result, resource_restriction="NONE"),  # type: ignore[arg-type]
        lambda: replace(result, authority_evidence_fingerprint="bad"),
    )
    for factory in invalid_factories:
        with pytest.raises((FeatureError, TypeError)):
            factory()
    other = evaluate_feature(
        FeatureVersion.standard("F-RET-001"),
        tuple(replace(item, generation_fingerprint="b" * 64) for item in samples(["1", "2"])),
    )
    with pytest.raises(FeatureError):
        FeatureSnapshot(
            values=(result, other),
            source_market_state_fingerprint=result.source_market_state_fingerprint,
            source_generation_fingerprint=result.source_generation_fingerprint,
            environment=result.environment,
            evaluation_time=NOW,
        )


# ---------------------------------------------------------------------------
# IMP-H001 canonical recursive state on every update
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("identifier", ["F-EMA-001", "F-ATR-001", "F-RSI-001"])
def test_imp_h001_batch_series_and_state_fingerprint_parity(identifier: str) -> None:
    feature = FeatureVersion.standard(identifier, parameter_n=RECURRENCE_N)
    inputs = inputs_for(identifier, RECURRENCE_VALUES)
    batch = evaluate_feature(feature, inputs)
    series = evaluate_feature_series(feature, inputs)
    last = series[-1]
    assert batch.validity is FeatureValidity.VALID
    assert batch.value is not None and last.value is not None
    assert batch.value.canonical_text == last.value.canonical_text
    assert batch.value.material_scale == 18
    assert batch.recursive_state is not None and last.recursive_state is not None
    assert [item.canonical_text for item in batch.recursive_state.components] == [
        item.canonical_text for item in last.recursive_state.components
    ]
    assert batch.recursive_state.fingerprint == last.recursive_state.fingerprint
    assert batch.recursive_state.serialize() == last.recursive_state.serialize()
    assert batch.fingerprint == last.fingerprint


def test_imp_h001_hidden_precision_cannot_change_the_published_value() -> None:
    feature = FeatureVersion.standard("F-EMA-001", parameter_n=RECURRENCE_N)
    inputs = samples(RECURRENCE_VALUES)
    full = evaluate_feature_series(feature, inputs)
    result = evaluate_feature(feature, inputs)
    assert result.recursive_state is not None
    assert all(value.material_scale == 18 for value in result.recursive_state.components)
    material = json.loads(result.recursive_state.serialize())
    assert all(scale == 18 for scale in material["component_scales"])
    assert material["previous_state_fingerprint"] is not None
    # A resumed recurrence consumes only the canonical state, so it must
    # reproduce the uninterrupted replay bit for bit.
    extended = [*RECURRENCE_VALUES, "377", "610", "987"]
    extended_series = evaluate_feature_series(feature, samples(extended))
    boundary = extended_series[9].recursive_state
    assert boundary is not None
    resumed = evaluate_feature_series(feature, samples(extended)[10:], initial_state=boundary)
    assert [item.fingerprint for item in resumed] == [
        item.fingerprint for item in extended_series[10:]
    ]
    assert full[-1].fingerprint == extended_series[len(RECURRENCE_VALUES) - 1].fingerprint


@pytest.mark.parametrize("identifier", ["F-EMA-001", "F-ATR-001", "F-RSI-001"])
@pytest.mark.parametrize("split", [7, 8, 10])
def test_imp_h001_serialized_resume_matches_uninterrupted_replay(
    identifier: str, split: int
) -> None:
    feature = FeatureVersion.standard(identifier, parameter_n=RECURRENCE_N)
    inputs = inputs_for(identifier, RECURRENCE_VALUES)
    full = evaluate_feature_series(feature, inputs)
    boundary = full[split - 1].recursive_state
    assert boundary is not None
    restored = restore_recursive_state(
        feature, boundary.serialize(), consumed_inputs=inputs[:split]
    )
    resumed = evaluate_feature_series(feature, inputs[split:], initial_state=restored)
    assert resumed[-1].fingerprint == full[-1].fingerprint
    assert resumed[-1].recursive_state is not None
    assert resumed[-1].recursive_state.serialize() == full[-1].recursive_state.serialize()


# ---------------------------------------------------------------------------
# IMP-H002 state identity, attestation and predecessor chain
# ---------------------------------------------------------------------------


def _attested_state(identifier: str = "F-EMA-001", parameter_n: int = RECURRENCE_N):
    feature = FeatureVersion.standard(identifier, parameter_n=parameter_n)
    inputs = inputs_for(identifier, RECURRENCE_VALUES)
    state = evaluate_feature(feature, inputs).recursive_state
    assert state is not None
    return feature, inputs, state


def test_imp_h002_state_is_evaluator_issued_only() -> None:
    _, _, state = _attested_state()
    assert state._is_attested()
    with pytest.raises(FeatureError):
        RecursiveAccumulatorState()
    with pytest.raises(FeatureError):
        replace(state, previous_state_fingerprint="a" * 64)
    inert = RecursiveAccumulatorState.deserialize(state.serialize())
    assert not inert._is_attested()
    feature = FeatureVersion.standard("F-EMA-001", parameter_n=RECURRENCE_N)
    with pytest.raises(FeatureEvaluationError):
        evaluate_feature(feature, samples(RECURRENCE_VALUES), initial_state=inert)


def test_imp_h002_state_binds_context_and_predecessor_chain() -> None:
    feature, _, state = _attested_state()
    material = json.loads(state.serialize())
    assert material["source"] == "EXCHANGE:fixture"
    assert material["algorithm_version"] == "S2A_ACCUMULATOR_STATE_V1"
    assert material["decimal_policy_version"] == "FEATURE_DECIMAL_V1"
    assert material["parameter_n"] == RECURRENCE_N
    assert material["previous_state_fingerprint"] is not None
    assert len(material["lineage"]) == len(material["authority_lineage"])
    assert len(material["lineage"]) == len(material["market_state_lineage"])
    assert material["processed_samples"] == len(material["lineage"])
    seed = evaluate_feature(
        feature, inputs_for("F-EMA-001", RECURRENCE_VALUES)[:RECURRENCE_N]
    ).recursive_state
    assert seed is not None and seed.previous_state_fingerprint is None
    lineage = evaluate_feature_series(feature, inputs_for("F-EMA-001", RECURRENCE_VALUES))
    for earlier, later in zip(lineage[RECURRENCE_N:], lineage[RECURRENCE_N + 1 :], strict=False):
        assert earlier.recursive_state is not None and later.recursive_state is not None
        assert later.recursive_state.previous_state_fingerprint == (
            earlier.recursive_state.fingerprint
        )


def test_imp_h002_forged_chain_and_cross_context_injection_fail() -> None:
    feature, inputs, state = _attested_state()
    next_sample = FeatureSample.from_decimal("987", index=len(inputs))
    for label, mutated in (
        (
            "cross-source",
            replace(next_sample, source_id=StableId(kind=IdentityKind.EXCHANGE, value="other")),
        ),
        (
            "cross-contract",
            replace(next_sample, contract_id=StableId(kind=IdentityKind.INSTRUMENT, value="other")),
        ),
        ("cross-generation", replace(next_sample, generation_fingerprint="b" * 64)),
        (
            "cross-environment",
            FeatureSample.from_candle(paper_candle(12, "9"), market_state=s1e_state()),
        ),
        ("cross-timeframe", replace(next_sample, timeframe=Timeframe("Min5", 300))),
    ):
        try:
            result = evaluate_feature(feature, [mutated], initial_state=state)
        except FeatureEvaluationError:
            continue
        assert result.validity is not FeatureValidity.VALID, label
    with pytest.raises(FeatureEvaluationError):
        evaluate_feature(
            FeatureVersion.standard("F-EMA-001", parameter_n=RECURRENCE_N + 1),
            inputs,
            initial_state=state,
        )
    forged = state.serialize().replace("EXCHANGE:fixture", "EXCHANGE:forged")
    with pytest.raises(FeatureError):
        restore_recursive_state(feature, forged, consumed_inputs=inputs)
    tampered = state.serialize().replace(state.components[0].canonical_text, "1.000000000000000001")
    with pytest.raises((FeatureError, FeatureEvaluationError)):
        restore_recursive_state(feature, tampered, consumed_inputs=inputs)
    restored = restore_recursive_state(feature, state.serialize(), consumed_inputs=inputs)
    assert restored._is_attested()
    assert restored.fingerprint == state.fingerprint


# ---------------------------------------------------------------------------
# IMP-H003 axis separation
# ---------------------------------------------------------------------------


def test_imp_h003_resource_and_lifecycle_are_separate_restrictive_axes() -> None:
    base = samples(["1", "2"])
    feature = FeatureVersion.standard("F-RET-001")
    degraded = with_authority(base[-1], resource=ResourceDisposition.DEGRADED)
    result = evaluate_feature(feature, [base[0], degraded])
    assert result.validity is FeatureValidity.VALID
    assert result.value is not None
    assert result.resource_restriction is FeatureAxisRestriction.RESTRICTIVE
    denied = with_authority(base[-1], resource=ResourceDisposition.DENIED)
    denied_result = evaluate_feature(feature, [base[0], denied])
    assert denied_result.validity is FeatureValidity.VALID
    assert denied_result.resource_restriction is FeatureAxisRestriction.RESTRICTIVE
    unknown = with_authority(base[-1], resource=ResourceDisposition.UNKNOWN)
    unknown_result = evaluate_feature(feature, [base[0], unknown])
    assert unknown_result.validity is FeatureValidity.VALID
    assert unknown_result.resource_restriction is FeatureAxisRestriction.RESTRICTIVE
    ineligible = with_authority(base[-1], lifecycle=LifecycleRestriction.NEW_EXPOSURE_DISABLED)
    lifecycle_result = evaluate_feature(feature, [base[0], ineligible])
    assert lifecycle_result.validity is FeatureValidity.VALID
    assert lifecycle_result.lifecycle_restriction is FeatureAxisRestriction.RESTRICTIVE
    assert lifecycle_result.resource_restriction is FeatureAxisRestriction.NONE


def test_imp_h003_market_truth_conditions_stay_restrictive() -> None:
    feature = FeatureVersion.standard("F-RET-001")
    base = samples(["1", "2"])
    for trust, expected in (
        (MarketStateTrust.UNKNOWN, FeatureValidity.UNKNOWN),
        (MarketStateTrust.UNTRUSTED, FeatureValidity.UNKNOWN),
        (MarketStateTrust.RESYNC_REQUIRED, FeatureValidity.UNKNOWN),
        (MarketStateTrust.DEGRADED, FeatureValidity.DEGRADED),
    ):
        restricted = with_authority(base[-1], trust=trust)
        assert evaluate_feature(feature, [base[0], restricted]).validity is expected
    for reason in (
        QualityReason.STALE,
        QualityReason.GAP,
        QualityReason.SEQUENCE_UNPROVABLE,
        QualityReason.CLOCK_UNTRUSTED,
        QualityReason.SCHEMA_QUARANTINED,
    ):
        restricted = with_authority(base[-1], reasons=(reason,))
        assert (
            evaluate_feature(feature, [base[0], restricted]).validity is FeatureValidity.UNKNOWN
        ), reason
    contradiction = with_authority(base[-1], reasons=(QualityReason.CROSS_CHANNEL_CONTRADICTION,))
    assert evaluate_feature(feature, [base[0], contradiction]).validity is FeatureValidity.INVALID


def test_imp_h003_feature_path_cannot_upgrade_any_axis() -> None:
    feature = FeatureVersion.standard("F-EMA-001", parameter_n=3)
    restricted = tuple(
        with_authority(item, trust=MarketStateTrust.DEGRADED, resource=ResourceDisposition.DEGRADED)
        for item in samples(["1", "2", "3", "4"])
    )
    series = evaluate_feature_series(feature, restricted)
    for output in series:
        assert output.market_state_trust is not MarketStateTrust.TRUSTED
        assert output.resource_restriction is FeatureAxisRestriction.RESTRICTIVE
    state = series[2].recursive_state
    assert state is not None
    trusted_continuation = tuple(
        with_authority(FeatureSample.from_decimal(value, index=4 + offset))
        for offset, value in enumerate(["5", "6"])
    )
    resumed = evaluate_feature_series(feature, trusted_continuation, initial_state=state)
    for output in resumed:
        assert output.market_state_trust is MarketStateTrust.DEGRADED
        assert output.resource_restriction is FeatureAxisRestriction.RESTRICTIVE
        assert output.data_authority_state is DataAuthorityState.ALLOW_NEW_EXPOSURE


def test_imp_h003_authoritative_candle_requires_canonical_s1e_evidence() -> None:
    candle = paper_candle(0, "10")
    with pytest.raises(FeatureError):
        FeatureSample.from_candle(candle)
    state = s1e_state()
    bound = FeatureSample.from_candle(candle, market_state=state)
    assert bound.market_state_fingerprint == state.fingerprint
    assert bound.market_state_fingerprint != candle.context.provenance_fingerprint
    assert bound.market_state_trust is MarketStateTrust.TRUSTED
    assert bound.resource_disposition is ResourceDisposition.UNKNOWN
    restricted = FeatureSample.from_candle(
        candle, market_state=state, resource=s1e_resource(ResourceDisposition.DEGRADED)
    )
    assert restricted.resource_restriction is FeatureAxisRestriction.RESTRICTIVE
    mismatched = paper_candle(0, "10")
    with pytest.raises(FeatureError):
        FeatureSample.from_candle(
            replace(mismatched, context=replace(mismatched.context, contract_id=CONTRACT)),
            market_state=state,
        )


def test_imp_h003_fixture_namespace_firewall_is_replay_only() -> None:
    for environment in (Environment.LIVE, Environment.PAPER, Environment.SHADOW):
        with pytest.raises(FeatureError):
            FeatureSample.from_decimal("1", environment=environment)
    fixture = FeatureSample.from_decimal("1")
    assert fixture.authority.is_fixture
    assert fixture.environment is Environment.REPLAY
    with pytest.raises(FeatureError):
        replace(fixture, environment=Environment.LIVE)
    live_authority = FeatureAuthorityEvidence.from_market_state(s1e_state())
    assert not live_authority.is_fixture
    assert live_authority.market_state_fingerprint == s1e_state().fingerprint
    with pytest.raises(FeatureError):
        replace(fixture, environment=Environment.PAPER)
    with pytest.raises(FeatureError):
        FeatureAuthorityEvidence.fixture(market_state_fingerprint="bad")


# ---------------------------------------------------------------------------
# IMP-H004 derived window evidence is content bound
# ---------------------------------------------------------------------------


def test_imp_h004_direct_and_tampered_evidence_cannot_mint_validity() -> None:
    with pytest.raises(FeatureError):
        AlignedWindowEvidence()
    aligned = align_closed_1m_candles(
        _closed_candles(), 5, evaluation_time=NOW + timedelta(minutes=5)
    )
    assert aligned._is_attested()
    with pytest.raises(FeatureError):
        replace(aligned, validity=FeatureValidity.VALID, reason="FORGED")
    with pytest.raises(FeatureError):
        replace(aligned, high=DecimalValue.parse("999"))
    with pytest.raises(FeatureError):
        replace(aligned, lineage=("a" * 64,))
    with pytest.raises((FeatureError, TypeError)):
        replace(aligned, open=DecimalValue.parse("999"))


def test_imp_h004_material_is_recomputed_from_constituents() -> None:
    for target, count in ((5, 5), (15, 15)):
        candles = _closed_candles(count)
        boundary = NOW + timedelta(minutes=target)
        aligned = align_closed_1m_candles(candles, target, evaluation_time=boundary)
        assert aligned.validity is FeatureValidity.VALID
        assert aligned.open == candles[0].open
        assert aligned.close == candles[-1].close
        assert aligned.high.canonical_text == max(item.high.canonical_text for item in candles)
        assert aligned.low.canonical_text == min(item.low.canonical_text for item in candles)
        assert aligned.lineage == tuple(item.fingerprint for item in candles)
        assert aligned.constituent_fingerprints == aligned.lineage
        assert aligned.authority_evidence_fingerprints
        material = aligned.fingerprint
        corrected = replace(candles[0], close=DecimalValue.parse("11"))
        revised = align_closed_1m_candles(
            (corrected, *candles[1:]), target, evaluation_time=boundary
        )
        assert revised.fingerprint != material
        reordered = align_closed_1m_candles(
            tuple(reversed(candles)), target, evaluation_time=boundary
        )
        assert reordered.fingerprint != material
        assert reordered.validity is FeatureValidity.INVALID
        drifted = replace(candles[0], revision=1, predecessor_fingerprint=candles[0].fingerprint)
        assert (
            align_closed_1m_candles(
                (drifted, *candles[1:]), target, evaluation_time=boundary
            ).fingerprint
            != material
        )


def test_imp_h004_incomplete_and_degraded_paths_bind_evidence() -> None:
    candles = _closed_candles()
    boundary = NOW + timedelta(minutes=5)
    warmup = align_closed_1m_candles(candles[:4], 5, evaluation_time=NOW + timedelta(minutes=4))
    unknown = align_closed_1m_candles(candles[:4], 5, evaluation_time=boundary)
    assert warmup.validity is FeatureValidity.WARMUP
    assert unknown.validity is FeatureValidity.UNKNOWN
    for item in (warmup, unknown):
        assert item.lineage == tuple(candle.fingerprint for candle in candles[:4])
        assert (
            item.fingerprint
            != align_closed_1m_candles(candles[1:5], 5, evaluation_time=boundary).fingerprint
        )
    degraded = align_closed_1m_candles(
        candles[:5],
        5,
        evaluation_time=boundary,
        authorities=tuple(
            constituent_authority(candle, resource=ResourceDisposition.DEGRADED)
            for candle in candles[:5]
        ),
    )
    assert degraded.validity is FeatureValidity.VALID
    assert degraded.high is not None and degraded.close is not None
    assert degraded.resource_restriction is FeatureAxisRestriction.RESTRICTIVE


def test_imp_h004_public_alias_matches_canonical_entry_point() -> None:
    candles = _closed_candles()
    boundary = NOW + timedelta(minutes=5)
    assert (
        feature_module.align_candles(candles[:5], 5, evaluation_time=boundary).fingerprint
        == align_closed_1m_candles(candles[:5], 5, evaluation_time=boundary).fingerprint
    )


# ---------------------------------------------------------------------------
# Authority evidence construction and governed seams
# ---------------------------------------------------------------------------


def test_authority_evidence_validation_is_fail_closed() -> None:
    good = FeatureAuthorityEvidence.fixture(market_state_fingerprint="a" * 64)
    invalid_factories = (
        lambda: replace(good, market_state_fingerprint="bad"),
        lambda: replace(good, market_state_trust="TRUSTED"),  # type: ignore[arg-type]
        lambda: replace(good, data_authority_state="ALLOW_NEW_EXPOSURE"),  # type: ignore[arg-type]
        lambda: replace(good, data_authority_fingerprint="bad"),
        lambda: replace(good, data_authority_reasons=()),
        lambda: replace(good, data_authority_reasons=("FRESH_VALID",)),  # type: ignore[arg-type]
        lambda: replace(
            good,
            data_authority_reasons=(QualityReason.STALE, QualityReason.FRESH_VALID),
        ),
        lambda: replace(good, resource_disposition="AVAILABLE"),  # type: ignore[arg-type]
        lambda: replace(good, resource_evidence_fingerprint="bad"),
        lambda: replace(good, lifecycle_restriction="NONE"),  # type: ignore[arg-type]
        lambda: replace(good, is_fixture="yes"),  # type: ignore[arg-type]
    )
    for factory in invalid_factories:
        with pytest.raises(FeatureError):
            factory()
    assert len(good.fingerprint) == 64
    assert good.material["authority_version"] == "S2A_AUTHORITY_EVIDENCE_V1"


def test_authority_evidence_axes_are_derived_not_synthesized() -> None:
    available = FeatureAuthorityEvidence.fixture(market_state_fingerprint="a" * 64)
    assert available.resource_restriction is FeatureAxisRestriction.NONE
    assert available.lifecycle_axis is FeatureAxisRestriction.NONE
    assert available.restrictive_reasons == ()
    assert available.market_truth_restrictive is False
    stale = FeatureAuthorityEvidence.fixture(
        market_state_fingerprint="a" * 64,
        data_authority_reasons=(QualityReason.STALE,),
    )
    assert stale.restrictive_reasons == (QualityReason.STALE,)
    assert stale.market_truth_restrictive is True
    degraded_trust = FeatureAuthorityEvidence.fixture(
        market_state_fingerprint="a" * 64, market_state_trust=MarketStateTrust.DEGRADED
    )
    assert degraded_trust.market_truth_restrictive is True


def test_authority_evidence_from_market_state_requires_canonical_evidence() -> None:
    state = s1e_state()
    derived = FeatureAuthorityEvidence.from_market_state(state)
    assert derived.market_state_fingerprint == state.fingerprint
    assert derived.market_state_trust is MarketStateTrust.TRUSTED
    assert derived.resource_disposition is ResourceDisposition.UNKNOWN
    assert derived.is_fixture is False
    with_resource = FeatureAuthorityEvidence.from_market_state(
        state, resource=s1e_resource(ResourceDisposition.AVAILABLE)
    )
    assert with_resource.resource_disposition is ResourceDisposition.AVAILABLE
    assert with_resource.resource_evidence_fingerprint != derived.resource_evidence_fingerprint
    with pytest.raises(FeatureError):
        FeatureAuthorityEvidence.from_market_state("not-a-state")  # type: ignore[arg-type]
    with pytest.raises(FeatureError):
        FeatureAuthorityEvidence.from_market_state(
            state,
            resource="not-an-admission",  # type: ignore[arg-type]
        )


def test_feature_engine_compatibility_surface_matches_features() -> None:
    import hct_backend.feature_engine as engine

    for name in engine.__all__:
        assert getattr(engine, name) is getattr(feature_module, name), name
    assert "restore_recursive_state" in engine.__all__
    assert "FeatureAuthorityEvidence" in engine.__all__


def test_restore_recursive_state_rejects_inadmissible_material() -> None:
    feature = FeatureVersion.standard("F-EMA-001", parameter_n=RECURRENCE_N)
    inputs = samples(RECURRENCE_VALUES)
    state = evaluate_feature(feature, inputs).recursive_state
    assert state is not None
    payload = state.serialize()
    with pytest.raises((FeatureError, FeatureEvaluationError)):
        restore_recursive_state(
            FeatureVersion.standard("F-SMA-001", parameter_n=RECURRENCE_N),
            payload,
            consumed_inputs=inputs,
        )
    with pytest.raises((FeatureError, FeatureEvaluationError)):
        restore_recursive_state(feature, payload, consumed_inputs=[])
    with pytest.raises((FeatureError, FeatureEvaluationError)):
        restore_recursive_state(feature, payload, consumed_inputs=inputs[:2])
    with pytest.raises((FeatureError, FeatureEvaluationError)):
        restore_recursive_state(
            feature,
            payload,
            consumed_inputs=tuple(
                replace(item, generation_fingerprint="b" * 64) for item in inputs
            ),
        )
    with pytest.raises((FeatureError, FeatureEvaluationError)):
        restore_recursive_state(
            FeatureVersion.standard("F-EMA-001", parameter_n=RECURRENCE_N + 1),
            payload,
            consumed_inputs=inputs,
        )


def test_recursive_state_matches_requires_exact_context() -> None:
    feature = FeatureVersion.standard("F-EMA-001", parameter_n=RECURRENCE_N)
    inputs = samples(RECURRENCE_VALUES)
    state = evaluate_feature(feature, inputs).recursive_state
    assert state is not None
    assert state.matches(feature, inputs[0])
    assert not state.matches(feature, replace(inputs[0], generation_fingerprint="b" * 64))
    assert not state.matches(feature, replace(inputs[0], timeframe=Timeframe("Min5", 300)))
    assert not state.matches(
        FeatureVersion.standard("F-EMA-001", parameter_n=RECURRENCE_N + 1), inputs[0]
    )


def test_evaluation_entry_points_require_samples() -> None:
    feature = FeatureVersion.standard("F-RET-001")
    with pytest.raises(FeatureEvaluationError):
        evaluate_feature(feature, [])
    assert evaluate_feature_series(feature, []) == ()
    with pytest.raises(FeatureEvaluationError):
        evaluate_feature("F-RET-001", samples(["1", "2"]))  # type: ignore[arg-type]
    with pytest.raises(FeatureEvaluationError):
        restore_recursive_state(
            "F-EMA-001",  # type: ignore[arg-type]
            "{}",
            consumed_inputs=samples(["1"]),
        )


def test_from_candle_requires_a_candle_and_rejects_non_snapshot_state() -> None:
    with pytest.raises(FeatureError):
        FeatureSample.from_candle("not-a-candle")  # type: ignore[arg-type]
    with pytest.raises(FeatureError):
        FeatureSample.from_candle(
            paper_candle(0, "10"),
            market_state="not-a-state",  # type: ignore[arg-type]
        )


def test_aligned_evidence_without_constituents_is_deterministic_warmup() -> None:
    first = align_closed_1m_candles((), 5, evaluation_time=NOW + timedelta(minutes=5))
    second = align_closed_1m_candles((), 5, evaluation_time=NOW + timedelta(minutes=5))
    assert first.validity is FeatureValidity.WARMUP
    assert first.reason == "NO_CONSTITUENTS"
    assert first.fingerprint == second.fingerprint
    assert first.constituent_fingerprints == ()
    assert len(first.fingerprint) == 64


def test_aligned_evidence_material_cannot_disagree_with_constituents() -> None:
    candles = _closed_candles()
    valid = align_closed_1m_candles(candles[:5], 5, evaluation_time=NOW + timedelta(minutes=5))
    material: dict[str, object] = {
        "target_minutes": valid.target_minutes,
        "target_timeframe_fingerprint": valid.target_timeframe_fingerprint,
        "start": valid.start,
        "end": valid.end,
        "constituents": valid.constituents,
        "constituent_fingerprints": valid.constituent_fingerprints,
        "constituent_provenance_fingerprints": valid.constituent_provenance_fingerprints,
        "authority_evidence_fingerprints": valid.authority_evidence_fingerprints,
        "authority_fold_fingerprint": valid.authority_fold_fingerprint,
        "data_authority_state": valid.data_authority_state,
        "constituent_market_state_trust": valid.constituent_market_state_trust,
        "validity": FeatureValidity.VALID,
        "reason": "FORGED",
        "source_id": valid.source_id,
        "contract_id": valid.contract_id,
        "environment": valid.environment,
        "generation_fingerprint": valid.generation_fingerprint,
        "open": valid.open,
        "high": valid.high,
        "low": valid.low,
        "close": valid.close,
        "volume": valid.volume,
        "event_time": valid.event_time,
        "knowledge_time": valid.knowledge_time,
        "wall_receive_time": valid.wall_receive_time,
        "lineage": ("a" * 64,),
        "resource_restriction": valid.resource_restriction,
        "lifecycle_restriction": valid.lifecycle_restriction,
        "provenance": valid.provenance,
    }
    with pytest.raises(FeatureError):
        AlignedWindowEvidence._from_evaluator(**material)
    material["lineage"] = valid.constituent_fingerprints
    material["resource_restriction"] = "NONE"
    with pytest.raises(FeatureError):
        AlignedWindowEvidence._from_evaluator(**material)
    material["resource_restriction"] = valid.resource_restriction
    material["provenance"] = "UNSUPPORTED_V1"
    with pytest.raises(FeatureError):
        AlignedWindowEvidence._from_evaluator(**material)
    material["provenance"] = valid.provenance
    material["target_minutes"] = 7
    with pytest.raises(FeatureError):
        AlignedWindowEvidence._from_evaluator(**material)
    material["target_minutes"] = valid.target_minutes
    material["constituent_provenance_fingerprints"] = ()
    with pytest.raises(FeatureError):
        AlignedWindowEvidence._from_evaluator(**material)


# ---------------------------------------------------------------------------
# IMP-H005 non-fixture authority and value evidence are not caller-mintable
# ---------------------------------------------------------------------------


def test_imp_h005_non_fixture_authority_is_evaluator_issued() -> None:
    with pytest.raises(FeatureError):
        FeatureAuthorityEvidence()
    state = s1e_state()
    derived = FeatureAuthorityEvidence.from_market_state(state, resource=s1e_resource())
    assert derived._is_attested()
    assert derived.is_fixture is False
    assert derived.environment is Environment.PAPER
    assert derived.source_id == S1E_SOURCE
    assert derived.bound_evidence_fingerprint is None
    for change in (
        {"market_state_trust": MarketStateTrust.UNTRUSTED},
        {"data_authority_state": DataAuthorityState.EMERGENCY},
        {"resource_disposition": ResourceDisposition.AVAILABLE},
        {"lifecycle_restriction": LifecycleRestriction.NONE},
        {"is_fixture": True},
        {"bound_evidence_fingerprint": "a" * 64},
        {"environment": Environment.LIVE},
    ):
        with pytest.raises(FeatureError):
            replace(derived, **change)


def test_imp_h005_forged_non_replay_sample_fails() -> None:
    state = s1e_state()
    unbound = FeatureAuthorityEvidence.from_market_state(state, resource=s1e_resource())
    forged = {
        "value": DecimalValue.parse("10"),
        "fingerprint": "a" * 64,
        "event_time": NOW,
        "knowledge_time": NOW,
        "wall_receive_time": NOW,
        "closed": True,
        "source_id": S1E_SOURCE,
        "contract_id": S1E_CONTRACT,
        "environment": Environment.PAPER,
        "generation_fingerprint": s1e_generation().fingerprint,
        "market_state_fingerprint": unbound.market_state_fingerprint,
        "provenance_fingerprint": S1E_PROVENANCE,
        "timeframe": Timeframe("Min1", 60),
        "authority": unbound,
        "close": DecimalValue.parse("10"),
    }
    with pytest.raises(FeatureError):
        FeatureSample(**forged)  # type: ignore[arg-type]
    other = FeatureAuthorityEvidence.fixture_for_candle(_candle(0, "10"))
    forged["authority"] = other
    forged["market_state_fingerprint"] = other.market_state_fingerprint
    with pytest.raises(FeatureError):
        FeatureSample(**forged)  # type: ignore[arg-type]
    forged["environment"] = Environment.REPLAY
    with pytest.raises(FeatureError):
        FeatureSample(**forged)  # type: ignore[arg-type]


def test_imp_h005_non_replay_mutation_is_rejected() -> None:
    state = s1e_state()
    bound = FeatureSample.from_candle(paper_candle(0, "10"), market_state=state)
    assert bound.authority.is_fixture is False
    assert bound.market_state_fingerprint == state.fingerprint
    mutations = (
        {"close": DecimalValue.parse("11")},
        {"high": DecimalValue.parse("13")},
        {"low": DecimalValue.parse("8")},
        {"value": DecimalValue.parse("9")},
        {
            "quantity": Quantity(
                DecimalValue.parse("5"), QuantityUnit.CONTRACTS_PROVIDER_NATIVE_V1, "S1F"
            )
        },
        {"fingerprint": "b" * 64},
        {"provenance_fingerprint": "c" * 64},
        {"event_time": NOW + timedelta(minutes=1)},
        {"knowledge_time": NOW + timedelta(minutes=1)},
        {"wall_receive_time": NOW + timedelta(minutes=2)},
        {"interval_start": NOW + timedelta(minutes=1)},
        {"interval_end": NOW + timedelta(minutes=2)},
        {"timeframe": Timeframe("Min5", 300)},
        {"generation_fingerprint": "d" * 64},
        {
            "source_id": StableId(kind=IdentityKind.EXCHANGE, value="other-venue"),
        },
        {
            "contract_id": StableId(kind=IdentityKind.INSTRUMENT, value="other-contract"),
        },
        {"market_state_fingerprint": "e" * 64},
        {"authority": FeatureAuthorityEvidence.from_market_state(state)},
    )
    for change in mutations:
        with pytest.raises(FeatureError):
            replace(bound, **change)


def test_imp_h005_canonical_candle_binding_succeeds_and_mismatch_fails() -> None:
    state = s1e_state()
    candle = paper_candle(0, "10")
    sample = FeatureSample.from_candle(candle, market_state=state)
    assert sample.value_evidence_fingerprint == sample.authority.bound_evidence_fingerprint
    assert sample.fingerprint == candle.fingerprint
    assert sample.market_state_fingerprint != candle.context.provenance_fingerprint
    mismatched = (
        lambda: replace(candle, context=replace(candle.context, source_id=SOURCE)),
        lambda: replace(candle, context=replace(candle.context, contract_id=CONTRACT)),
        lambda: replace(
            candle,
            context=replace(
                candle.context, generation=GenerationRef(S1E_SOURCE, Environment.PAPER, 2)
            ),
        ),
        lambda: replace(candle, context=replace(candle.context, environment=Environment.REPLAY)),
    )
    for factory in mismatched:
        with pytest.raises((FeatureError, ValueError)):
            FeatureSample.from_candle(factory(), market_state=state)


def test_imp_h005_fixture_replay_only_remains_supported() -> None:
    candle = _candle(0, "10")
    fixture = FeatureSample.from_candle(candle)
    assert fixture.authority.is_fixture
    assert fixture.environment is Environment.REPLAY
    mutating = replace(fixture, high=DecimalValue.parse("99"))
    assert mutating.high is not None
    for environment in (Environment.LIVE, Environment.PAPER, Environment.SHADOW):
        with pytest.raises(FeatureError):
            FeatureAuthorityEvidence.fixture(
                market_state_fingerprint="a" * 64, environment=environment
            )
        with pytest.raises(FeatureError):
            FeatureSample.from_decimal("1", environment=environment)


# ---------------------------------------------------------------------------
# IMP-H006 per-constituent MTF authority binding
# ---------------------------------------------------------------------------


def _aligned_with(
    candles: tuple[CandleBar, ...],
    *,
    authorities: tuple[FeatureAuthorityEvidence, ...] | None = None,
    target_minutes: int = 5,
    evaluation_time: datetime | None = None,
) -> AlignedWindowEvidence:
    return align_closed_1m_candles(
        candles,
        target_minutes,
        evaluation_time=evaluation_time or NOW + timedelta(minutes=target_minutes),
        authorities=authorities,
    )


def test_imp_h006_five_trusted_constituents_are_valid() -> None:
    candles = _closed_candles()
    aligned = _aligned_with(candles[:5])
    assert aligned.validity is FeatureValidity.VALID
    assert aligned.authority_evidence_fingerprints == tuple(
        constituent_authority(candle).fingerprint for candle in candles[:5]
    )
    assert len(set(aligned.authority_evidence_fingerprints)) == 5


def test_imp_h006_resource_degraded_constituent_restricts_without_invalidating() -> None:
    candles = _closed_candles()
    authorities = tuple(
        constituent_authority(
            candle,
            resource=(
                ResourceDisposition.DEGRADED if index == 3 else ResourceDisposition.AVAILABLE
            ),
        )
        for index, candle in enumerate(candles[:5])
    )
    aligned = _aligned_with(candles[:5], authorities=authorities)
    assert aligned.validity is FeatureValidity.VALID
    assert aligned.high is not None
    assert aligned.resource_restriction is FeatureAxisRestriction.RESTRICTIVE
    assert aligned.lifecycle_restriction is FeatureAxisRestriction.NONE


def test_imp_h006_lifecycle_ineligible_constituent_restricts_without_invalidating() -> None:
    candles = _closed_candles()
    authorities = tuple(
        constituent_authority(
            candle,
            lifecycle=(
                LifecycleRestriction.NEW_EXPOSURE_DISABLED
                if index == 0
                else LifecycleRestriction.NONE
            ),
        )
        for index, candle in enumerate(candles[:5])
    )
    aligned = _aligned_with(candles[:5], authorities=authorities)
    assert aligned.validity is FeatureValidity.VALID
    assert aligned.lifecycle_restriction is FeatureAxisRestriction.RESTRICTIVE
    assert aligned.resource_restriction is FeatureAxisRestriction.NONE


@pytest.mark.parametrize(
    ("trust", "expected"),
    [
        (MarketStateTrust.UNKNOWN, FeatureValidity.UNKNOWN),
        (MarketStateTrust.RESYNC_REQUIRED, FeatureValidity.UNKNOWN),
        (MarketStateTrust.UNTRUSTED, FeatureValidity.UNKNOWN),
    ],
)
def test_imp_h006_unknown_constituent_is_not_washed_by_trusted(
    trust: MarketStateTrust, expected: FeatureValidity
) -> None:
    candles = _closed_candles()
    trusted = tuple(constituent_authority(candle) for candle in candles[:5])
    assert _aligned_with(candles[:5], authorities=trusted).validity is FeatureValidity.VALID
    mixed = tuple(
        constituent_authority(candle, trust=trust) if index == 4 else item
        for index, (candle, item) in enumerate(zip(candles[:5], trusted, strict=True))
    )
    restricted = _aligned_with(candles[:5], authorities=mixed)
    assert restricted.validity is expected
    assert restricted.fingerprint != _aligned_with(candles[:5], authorities=trusted).fingerprint


def test_imp_h006_degraded_constituent_market_truth_stays_degraded() -> None:
    candles = _closed_candles()
    authorities = tuple(
        constituent_authority(
            candle,
            trust=MarketStateTrust.DEGRADED if index == 2 else MarketStateTrust.TRUSTED,
            reasons=(
                (QualityReason.RESOURCE_DEGRADED,) if index == 2 else (QualityReason.FRESH_VALID,)
            ),
        )
        for index, candle in enumerate(candles[:5])
    )
    aligned = _aligned_with(candles[:5], authorities=authorities)
    assert aligned.validity is FeatureValidity.DEGRADED
    assert aligned.constituent_market_state_trust is MarketStateTrust.DEGRADED


def test_imp_h006_authority_sequence_mismatches_fail_closed() -> None:
    candles = _closed_candles()
    trusted = tuple(constituent_authority(candle) for candle in candles[:5])
    with pytest.raises(FeatureEvaluationError):
        _aligned_with(candles[:5], authorities=trusted[:4])
    with pytest.raises(FeatureEvaluationError):
        _aligned_with(candles[:5], authorities=trusted + (trusted[0],))
    permuted = (trusted[1], trusted[0], *trusted[2:])
    with pytest.raises(FeatureEvaluationError):
        _aligned_with(candles[:5], authorities=permuted)
    for change in (
        {"source_id": StableId(kind=IdentityKind.EXCHANGE, value="other-venue")},
        {"contract_id": StableId(kind=IdentityKind.INSTRUMENT, value="other-contract")},
        {"environment": Environment.PAPER},
        {"generation_fingerprint": "f" * 64},
    ):
        with pytest.raises((FeatureError, FeatureEvaluationError)):
            broken = (replace(trusted[0], **change), *trusted[1:])
            _aligned_with(candles[:5], authorities=broken)
    non_authority = ("not-authority", *trusted[1:])
    with pytest.raises(FeatureEvaluationError):
        _aligned_with(candles[:5], authorities=non_authority)  # type: ignore[arg-type]


def test_imp_h006_blanket_authority_is_removed_from_the_contract() -> None:
    candles = _closed_candles()
    with pytest.raises(TypeError):
        align_closed_1m_candles(candles[:5], 5, authority=constituent_authority(candles[0]))  # type: ignore[call-arg]
    with pytest.raises(FeatureEvaluationError):
        align_closed_1m_candles(
            candles[:5],
            5,
            authorities=constituent_authority(candles[0]),  # type: ignore[arg-type]
        )


def test_imp_h006_binding_mutation_changes_the_aligned_fingerprint() -> None:
    candles = _closed_candles()
    trusted = tuple(constituent_authority(candle) for candle in candles[:5])
    baseline = _aligned_with(candles[:5], authorities=trusted)
    corrected = (
        *candles[:1],
        replace(candles[1], close=DecimalValue.parse("12")),
        *candles[2:5],
    )
    with pytest.raises(FeatureEvaluationError):
        _aligned_with(corrected, authorities=trusted)
    rebound = (
        trusted[0],
        constituent_authority(corrected[1]),
        *trusted[2:],
    )
    assert _aligned_with(corrected, authorities=rebound).fingerprint != baseline.fingerprint
    with pytest.raises(FeatureError):
        replace(
            trusted[2],
            bound_evidence_fingerprint=trusted[3].bound_evidence_fingerprint,
        )
    swapped = (trusted[0], trusted[3], trusted[2], trusted[1], trusted[4])
    with pytest.raises(FeatureEvaluationError):
        _aligned_with(candles[:5], authorities=swapped)
    reordered_candles = (candles[1], candles[0], *candles[2:5])
    reordered = _aligned_with(reordered_candles, authorities=(trusted[1], trusted[0], *trusted[2:]))
    assert reordered.fingerprint != baseline.fingerprint
    assert reordered.validity is FeatureValidity.INVALID
    revised_candles = (
        *candles[:2],
        replace(
            candles[2],
            revision=1,
            predecessor_fingerprint=candles[2].fingerprint,
        ),
        *candles[3:5],
    )
    revised_authorities = (*trusted[:2], constituent_authority(revised_candles[2]), *trusted[3:])
    assert (
        _aligned_with(revised_candles, authorities=revised_authorities).fingerprint
        != baseline.fingerprint
    )


# ---------------------------------------------------------------------------
# IMP-H007 the benchmark and CI gate fail closed on every profile
# ---------------------------------------------------------------------------

_BENCHMARK_PROFILE_SHAPE = {
    "MICRO": (1, 4096, 64),
    "NOMINAL": (16, 8192, 256),
    "STRESS": (32, 16384, 512),
}


def _benchmark_module():
    import importlib.util

    root = Path(__file__).resolve().parents[3]
    spec = importlib.util.spec_from_file_location(
        "s2a_benchmark_under_test", root / "scripts" / "benchmark_s2a.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _synthetic_benchmark_document(parity: dict[str, str]) -> dict[str, object]:
    module = _benchmark_module()
    profiles = []
    for name, (contracts, candles, window) in _BENCHMARK_PROFILE_SHAPE.items():
        passed = parity[name] == "PASS"
        profiles.append(
            {
                "profile": name,
                "contracts": contracts,
                "closed_1m_candles_per_contract": candles,
                "max_window": window,
                "feature_ids": list(module.FEATURE_IDS),
                "feature_evaluations": 8 * contracts,
                "memory_probe_contracts": 1,
                "window_buffer_depth": window,
                "warmup_count": 1,
                "restrictive_state_count": 0,
                "no_lookahead_rejection_count": contracts,
                "input_manifest_hash": "a" * 64,
                "output_manifest_hash": "b" * 64,
                "recursive_parity": parity[name],
                "recursive_parity_fingerprint": "c" * 64,
                "recursive_parity_mismatches": 0 if passed else 1,
                "correctness": "PASS" if passed else "FAIL",
                "bounded_completion": True,
                "feature_evaluations_per_second": 1.0,
                "replay_throughput_candles_per_second": 1.0,
                "peak_memory_bytes": 1,
                "per_feature_compute_latency_ns": {
                    identifier: {"p50": 1.0, "p95": 1.0, "p99": 1.0, "max": 1.0}
                    for identifier in module.FEATURE_IDS
                },
            }
        )
    return {"mode": "S2A_BASELINE_ESTABLISHMENT_V1", "profiles": profiles}


def test_imp_h007_validator_accepts_a_fully_green_pair() -> None:
    module = _benchmark_module()
    good = _synthetic_benchmark_document({"MICRO": "PASS", "NOMINAL": "PASS", "STRESS": "PASS"})
    module.validate_benchmark_documents(good, good)


@pytest.mark.parametrize("profile", ["MICRO", "NOMINAL", "STRESS"])
def test_imp_h007_validator_fails_closed_per_profile(profile: str) -> None:
    module = _benchmark_module()
    good = _synthetic_benchmark_document({"MICRO": "PASS", "NOMINAL": "PASS", "STRESS": "PASS"})
    broken = _synthetic_benchmark_document(
        {
            "MICRO": "FAIL" if profile == "MICRO" else "PASS",
            "NOMINAL": "FAIL" if profile == "NOMINAL" else "PASS",
            "STRESS": "FAIL" if profile == "STRESS" else "PASS",
        }
    )
    with pytest.raises(module.BenchmarkValidationError):
        module.validate_benchmark_documents(broken, broken)
    with pytest.raises(module.BenchmarkValidationError):
        module.validate_benchmark_documents(broken, good)
    with pytest.raises(module.BenchmarkValidationError):
        module.validate_benchmark_documents(good, broken)


def test_imp_h007_validator_rejects_missing_profiles_and_drift() -> None:
    module = _benchmark_module()
    good = _synthetic_benchmark_document({"MICRO": "PASS", "NOMINAL": "PASS", "STRESS": "PASS"})
    duplicated = _synthetic_benchmark_document(
        {"MICRO": "PASS", "NOMINAL": "PASS", "STRESS": "PASS"}
    )
    duplicated["profiles"] = duplicated["profiles"][:2] + duplicated["profiles"][1:2]
    with pytest.raises(module.BenchmarkValidationError):
        module.validate_benchmark_documents(duplicated, duplicated)
    omitted = _synthetic_benchmark_document({"MICRO": "PASS", "NOMINAL": "PASS", "STRESS": "PASS"})
    omitted["profiles"] = omitted["profiles"][:2]
    with pytest.raises(module.BenchmarkValidationError):
        module.validate_benchmark_documents(omitted, omitted)
    drift = _synthetic_benchmark_document({"MICRO": "PASS", "NOMINAL": "PASS", "STRESS": "PASS"})
    drift["profiles"][1]["output_manifest_hash"] = "d" * 64
    with pytest.raises(module.BenchmarkValidationError):
        module.validate_benchmark_documents(good, drift)
