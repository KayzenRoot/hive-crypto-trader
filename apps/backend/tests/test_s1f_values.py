from dataclasses import replace
from datetime import UTC, datetime, timedelta

import pytest

from hct_backend.contracts import Environment, IdentityKind, StableId
from hct_backend.market_truth import GenerationRef
from hct_backend.s1f_numeric import DecimalValue
from hct_backend.s1f_values import (
    BookLevel,
    CandleBar,
    CapabilityState,
    CapabilityValue,
    Finality,
    FundingEvidence,
    OrderBookDelta,
    OrderBookSnapshot,
    OrderedLineage,
    ProviderTransactionAmount,
    Quantity,
    QuantityUnit,
    ReferencePriceEvidence,
    ReferencePriceKind,
    TickerState,
    Timeframe,
    TradeTick,
    ValueCapability,
    ValueContext,
    ValuePlaneConsistencyError,
    ValuePlaneError,
    validate_series_units,
)

NOW = datetime(2026, 1, 1, tzinfo=UTC)
SOURCE = StableId(kind=IdentityKind.EXCHANGE, value="mexc")
CONTRACT = StableId(kind=IdentityKind.INSTRUMENT, value="btc-usdt")


def context(channel: str = "sub.kline") -> ValueContext:
    return ValueContext(
        SOURCE,
        channel,
        CONTRACT,
        Environment.REPLAY,
        GenerationRef(SOURCE, Environment.REPLAY, 1),
        1,
        "a" * 64,
        "b" * 64,
        NOW,
        NOW,
        NOW,
        0,
    )


def quantity(value: str) -> Quantity:
    return Quantity(
        DecimalValue.parse(value),
        QuantityUnit.CONTRACTS_PROVIDER_NATIVE_V1,
        "S1F_MEXC_SOURCE_CONTRACT_V1",
    )


def level(price: str, value: str, count: int = 1) -> BookLevel:
    return BookLevel(DecimalValue.parse(price), quantity(value), count)


def test_capability_state_never_synthesizes_missing_value() -> None:
    assert CapabilityValue.unavailable(CapabilityState.UNKNOWN, "missing").value is None
    with pytest.raises(ValuePlaneConsistencyError):
        CapabilityValue(CapabilityState.UNKNOWN, DecimalValue.parse("1"), "missing")


def test_book_delta_requires_contiguous_version_and_removes_zero_quantity() -> None:
    snapshot = OrderBookSnapshot(
        context("sub.depth"), (level("411.8", "10"),), (level("412.0", "5"),), 1, "depth"
    )
    delta = OrderBookDelta(
        context("sub.depth"), (level("411.8", "0"),), (level("412.1", "3"),), 1, 2, "depth"
    )
    updated = delta.apply(snapshot)
    assert updated.version == 2
    assert updated.bids == ()
    assert updated.asks[0].price.canonical_text == "412"
    assert updated.asks[1].price.canonical_text == "412.1"
    with pytest.raises(ValuePlaneConsistencyError):
        OrderBookDelta(context("sub.depth"), (), (), 1, 3, "depth")


def test_candle_interval_lineage_and_closed_proof_are_explicit() -> None:
    frame = Timeframe("Min1", 60)
    line = OrderedLineage.from_event("b" * 64, NOW)
    kwargs = dict(
        context=context(),
        timeframe=frame,
        start=datetime(2026, 1, 1, 0, 0, tzinfo=UTC),
        end=datetime(2026, 1, 1, 0, 1, tzinfo=UTC),
        open=DecimalValue.parse("10"),
        high=DecimalValue.parse("12"),
        low=DecimalValue.parse("9"),
        close=DecimalValue.parse("11"),
        volume=quantity("2"),
        amount=ProviderTransactionAmount(DecimalValue.parse("22"), "S1F_MEXC_SOURCE_CONTRACT_V1"),
        lineage=line,
    )
    with pytest.raises(ValuePlaneConsistencyError):
        CandleBar(**kwargs, finality=Finality.CLOSED)
    bar = CandleBar(**kwargs, finality=Finality.OPEN)
    corrected = CandleBar(
        **{**kwargs, "close": DecimalValue.parse("11.1"), "lineage": line.append("c" * 64, NOW)},
        finality=Finality.OPEN,
        revision=1,
        predecessor_fingerprint=bar.fingerprint,
    )
    assert corrected.fingerprint != bar.fingerprint


def test_mixed_units_fail_closed() -> None:
    values = (quantity("1"), quantity("2"))
    assert validate_series_units(values) is QuantityUnit.CONTRACTS_PROVIDER_NATIVE_V1


def ticker() -> TickerState:
    price = CapabilityValue.supported(DecimalValue.parse("10"), "price")
    volume = CapabilityValue.supported(quantity("2"), "volume")
    funding = CapabilityValue.supported(DecimalValue.parse("0.01"), "fundingRate")
    return TickerState(
        context("sub.ticker"), price, price, price, volume, volume, price, price, funding
    )


def test_typed_values_fingerprint_and_reject_invalid_metadata() -> None:
    value = ticker()
    assert len(value.fingerprint) == 64
    assert ReferencePriceEvidence(
        value.context, ReferencePriceKind.MARK, DecimalValue.parse("10"), "fairPrice"
    ).fingerprint
    assert FundingEvidence(
        value.context, DecimalValue.parse("0.01"), value.context.event_time
    ).fingerprint
    assert ValueCapability("TickerState", "sub.ticker", CapabilityState.SUPPORTED).fingerprint
    with pytest.raises(ValuePlaneError):
        ValueCapability("", "sub.ticker", CapabilityState.SUPPORTED)
    with pytest.raises(ValuePlaneError):
        ValueCapability("TickerState", "sub.ticker", CapabilityState.SUPPORTED, 0)
    with pytest.raises(ValuePlaneError):
        CapabilityValue.unavailable(CapabilityState.SUPPORTED, "missing")
    with pytest.raises(ValuePlaneError):
        Quantity(DecimalValue.parse("1"), "BASE", "contract")  # type: ignore[arg-type]
    with pytest.raises(ValuePlaneError):
        ProviderTransactionAmount(DecimalValue.parse("1"), "")


def test_context_lineage_trade_and_timeframe_guards() -> None:
    line = OrderedLineage.from_fingerprints(("a" * 64,), NOW)
    appended = line.append("b" * 64, NOW + timedelta(seconds=1))
    assert appended.fingerprints == ("a" * 64, "b" * 64)
    with pytest.raises(ValuePlaneError):
        OrderedLineage.from_fingerprints(("a" * 64, "a" * 64), NOW)
    with pytest.raises(ValuePlaneError):
        OrderedLineage.from_fingerprints(("bad",), NOW)
    trade = TradeTick(context("sub.deal"), DecimalValue.parse("10"), quantity("1"), "BUY")
    assert len(trade.fingerprint) == 64
    with pytest.raises(ValuePlaneError):
        TradeTick(context("sub.deal"), DecimalValue.parse("10"), quantity("1"), "MAYBE")
    with pytest.raises(ValuePlaneError):
        Timeframe("", 60)
    with pytest.raises(ValuePlaneError):
        Timeframe("Min1", 60, alignment="WALL_CLOCK")
    with pytest.raises(ValuePlaneConsistencyError):
        ValueContext(
            SOURCE,
            "sub.ticker",
            CONTRACT,
            Environment.REPLAY,
            GenerationRef(SOURCE, Environment.REPLAY, 1),
            1,
            "a" * 64,
            "b" * 64,
            NOW,
            NOW + timedelta(seconds=1),
            NOW,
            0,
        )


def test_order_book_and_candle_reject_inconsistent_revisions() -> None:
    snapshot = OrderBookSnapshot(
        context("sub.depth"), (level("412", "1"),), (level("413", "1"),), 1, "depth"
    )
    assert len(snapshot.fingerprint) == 64
    with pytest.raises(ValuePlaneConsistencyError):
        OrderBookSnapshot(
            context("sub.depth"), (level("411", "1"), level("412", "1")), (), 1, "depth"
        )
    with pytest.raises(ValuePlaneError):
        BookLevel(DecimalValue.parse("1"), quantity("1"), -1)
    delta = OrderBookDelta(context("sub.depth"), (level("412", "2"),), (), 1, 2, "depth")
    assert len(delta.fingerprint) == 64
    with pytest.raises(ValuePlaneConsistencyError):
        delta.apply(replace(snapshot, version=3))
    frame = Timeframe("Min1", 60)
    line = OrderedLineage.from_event("b" * 64, NOW)
    candle_args = dict(
        context=context(),
        timeframe=frame,
        start=NOW,
        end=NOW + timedelta(seconds=60),
        open=DecimalValue.parse("10"),
        high=DecimalValue.parse("12"),
        low=DecimalValue.parse("9"),
        close=DecimalValue.parse("11"),
        volume=quantity("2"),
        amount=ProviderTransactionAmount(DecimalValue.parse("22"), "contract"),
        lineage=line,
    )
    with pytest.raises(ValuePlaneConsistencyError):
        CandleBar(**candle_args, finality=Finality.CLOSED)
    with pytest.raises(ValuePlaneConsistencyError):
        CandleBar(**candle_args, finality=Finality.OPEN, revision=1)
    assert CandleBar(**candle_args, finality=Finality.UNKNOWN).fingerprint
    with pytest.raises(ValuePlaneConsistencyError):
        validate_series_units(())
