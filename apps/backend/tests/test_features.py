from dataclasses import replace
from datetime import UTC, datetime, timedelta

import pytest

from hct_backend.contracts import Environment, IdentityKind, StableId
from hct_backend.features import (
    FeatureDefinition,
    FeatureRegistry,
    FeatureRegistryError,
    FeatureSample,
    FeatureValidity,
    FeatureVersion,
    align_closed_1m_candles,
    evaluate_feature,
    evaluate_feature_series,
    evaluate_snapshot,
)
from hct_backend.market_truth import GenerationRef
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
SOURCE = StableId(kind=IdentityKind.EXCHANGE, value="fixture")
CONTRACT = StableId(kind=IdentityKind.INSTRUMENT, value="btc-usdt")


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


def test_po_f10_serialized_resume_is_bit_for_bit_equal_for_ema_and_rsi() -> None:
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


def test_po_f03_point_in_time_and_axis_separation_fail_closed() -> None:
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
    degraded = replace(samples(["1", "2"])[-1], upstream_fidelity="RESOURCE_DEGRADED")
    degraded_result = evaluate_feature(
        FeatureVersion.standard("F-RET-001"), [samples(["1"])[0], degraded]
    )
    assert degraded_result.validity is FeatureValidity.DEGRADED
    assert degraded_result.value is not None
    ineligible = replace(samples(["1", "2"])[-1], upstream_fidelity="INELIGIBLE")
    ineligible_result = evaluate_feature(
        FeatureVersion.standard("F-RET-001"), [samples(["1"])[0], ineligible]
    )
    assert ineligible_result.validity is FeatureValidity.VALID


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


def test_po_f05_unknown_degraded_and_contradictory_inputs_remain_restrictive() -> None:
    base = samples(["1", "2"])
    unknown = replace(base[-1], market_state_trust="UNKNOWN")
    assert (
        evaluate_feature(FeatureVersion.standard("F-RET-001"), [base[0], unknown]).validity
        is FeatureValidity.UNKNOWN
    )
    degraded = replace(base[-1], upstream_fidelity="RESOURCE_DEGRADED")
    degraded_result = evaluate_feature(FeatureVersion.standard("F-RET-001"), [base[0], degraded])
    assert degraded_result.validity is FeatureValidity.DEGRADED
    assert degraded_result.value is not None
    mixed = replace(base[-1], generation_fingerprint="b" * 64)
    assert (
        evaluate_feature(FeatureVersion.standard("F-RET-001"), [base[0], mixed]).validity
        is FeatureValidity.INVALID
    )


def test_po_f06_generation_and_environment_namespaces_do_not_alias() -> None:
    replay = evaluate_feature(FeatureVersion.standard("F-RET-001"), samples(["1", "2"]))
    live_samples = tuple(
        replace(item, environment=Environment.LIVE, generation_fingerprint="b" * 64)
        for item in samples(["1", "2"])
    )
    live = evaluate_feature(FeatureVersion.standard("F-RET-001"), live_samples)
    assert replay.fingerprint != live.fingerprint
    assert replay.environment is Environment.REPLAY
    assert live.environment is Environment.LIVE


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


def test_po_f09_derived_alignment_is_non_authoritative_and_not_an_action_surface() -> None:
    aligned = align_closed_1m_candles(_closed_candles(), 5)
    assert aligned.provenance == "DERIVED_ANALYTICAL_V1"
    assert not hasattr(aligned, "order")
    assert not hasattr(aligned, "position")
