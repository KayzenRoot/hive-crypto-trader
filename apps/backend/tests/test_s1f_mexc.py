import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from hct_backend.contracts import Environment, IdentityKind, StableId
from hct_backend.market_truth import GenerationRef
from hct_backend.s1f_mexc import (
    MexcDecodeContext,
    MexcPublicDecoder,
    MexcQuarantineError,
    funding_from_ticker,
    reference_and_funding_from_ticker,
)
from hct_backend.s1f_values import (
    CandleBar,
    OrderBookDelta,
    OrderBookSnapshot,
    TickerState,
    TradeTick,
)

FIXTURES = json.loads(
    Path("apps/backend/tests/fixtures/s1f/mexc-public-fixtures.json").read_text()
)["fixtures"]
SOURCE = StableId(kind=IdentityKind.EXCHANGE, value="mexc")
CONTRACT = StableId(kind=IdentityKind.INSTRUMENT, value="btc-usdt")


def context(**overrides: object) -> MexcDecodeContext:
    values = dict(
        source_id=SOURCE,
        environment=Environment.REPLAY,
        generation=GenerationRef(SOURCE, Environment.REPLAY, 1),
        contract_id=CONTRACT,
        symbol="BTC_USDT",
        knowledge_time=datetime(2026, 1, 1, tzinfo=UTC),
        wall_receive_time=datetime(2026, 1, 1, tzinfo=UTC),
        monotonic_elapsed_ms=0,
        provenance_fingerprint="a" * 64,
        subscription_context="fixture",
        previous_depth_version=1,
    )
    values.update(overrides)
    return MexcDecodeContext(**values)


def test_decoder_constructs_all_primary_public_value_families() -> None:
    decoder = MexcPublicDecoder()
    assert isinstance(decoder.decode(json.dumps(FIXTURES["ticker"]), context()).value, TickerState)
    assert isinstance(decoder.decode(json.dumps(FIXTURES["deal"]), context()).value, TradeTick)
    assert isinstance(decoder.decode(json.dumps(FIXTURES["kline"]), context()).value, CandleBar)
    assert isinstance(
        decoder.decode(json.dumps(FIXTURES["depth_delta"]), context()).value, OrderBookDelta
    )


@pytest.mark.parametrize(
    "fixture", ["malformed_numeric", "wrong_timestamp_unit", "unknown_channel", "missing_required"]
)
def test_decoder_quarantines_negative_provider_cases(fixture: str) -> None:
    with pytest.raises(MexcQuarantineError):
        MexcPublicDecoder().decode(json.dumps(FIXTURES[fixture]), context())


def test_depth_snapshot_and_exact_kline_close_proof_are_bounded() -> None:
    decoder = MexcPublicDecoder()
    snapshot = decoder.decode_rest_depth(json.dumps(FIXTURES["depth_snapshot"]), context())
    assert snapshot.version == 1
    proof = decoder.decode_rest_kline_close_proof(
        json.dumps({"symbol": "BTC_USDT", "interval": "Min1", "time": ["1700000040"]}),
        context(),
        expected_interval="Min1",
        expected_start=datetime.fromtimestamp(1700000040, UTC),
        expected_end=datetime.fromtimestamp(1700000100, UTC),
    )
    assert len(proof) == 64


def test_bulk_ticker_full_depth_reference_and_funding_paths() -> None:
    decoder = MexcPublicDecoder()
    ticker = FIXTURES["ticker"]
    bulk = {
        "channel": "push.tickers",
        "symbol": "BTC_USDT",
        "ts": "1700000000000",
        "data": {"data": [ticker["data"]]},
    }
    values = decoder.decode(json.dumps(bulk), context()).values
    assert len(values) == 1
    assert isinstance(values[0], TickerState)
    references = reference_and_funding_from_ticker(values[0])
    assert {item.kind.value for item in references} == {"MARK", "FAIR", "INDEX"}
    assert funding_from_ticker(values[0]) is not None
    full = decoder.decode(json.dumps(FIXTURES["depth_delta"]), context(full_depth=True)).value
    assert isinstance(full, OrderBookSnapshot)
    assert full.version == 2


@pytest.mark.parametrize(
    "payload",
    [
        "not-json",
        json.dumps({"channel": "push.ticker", "ts": "1700000000000", "data": []}),
        json.dumps({"channel": "push.tickers", "ts": "1700000000000", "data": {}}),
        json.dumps(
            {
                "channel": "push.deal",
                "ts": "1700000000000",
                "data": {"p": "411.8", "v": "1", "t": "1700000000000"},
            }
        ),
    ],
)
def test_decoder_rejects_malformed_shapes_or_accepts_single_deal(payload: str) -> None:
    if '"channel": "push.deal"' in payload:
        assert isinstance(MexcPublicDecoder().decode(payload, context()).value, TradeTick)
    elif '"channel": "push.tickers"' in payload:
        assert MexcPublicDecoder().decode(payload, context()).values == ()
    else:
        with pytest.raises(MexcQuarantineError):
            MexcPublicDecoder().decode(payload, context())


def test_decoder_rejects_identity_depth_and_close_proof_contradictions() -> None:
    decoder = MexcPublicDecoder()
    with pytest.raises(MexcQuarantineError):
        decoder.decode(json.dumps(FIXTURES["depth_delta"]), context(previous_depth_version=None))
    with pytest.raises(MexcQuarantineError):
        decoder.decode(
            json.dumps({**FIXTURES["ticker"], "symbol": "ETH_USDT"}),
            context(),
        )
    with pytest.raises(MexcQuarantineError):
        decoder.decode_rest_depth("[]", context())
    with pytest.raises(MexcQuarantineError):
        decoder.decode_rest_kline_close_proof(
            json.dumps({"symbol": "ETH_USDT", "interval": "Min1", "time": ["1700000040"]}),
            context(),
            expected_interval="Min1",
            expected_start=datetime.fromtimestamp(1700000040, UTC),
            expected_end=datetime.fromtimestamp(1700000100, UTC),
        )
    with pytest.raises(MexcQuarantineError):
        decoder.decode_rest_kline_close_proof(
            json.dumps({"symbol": "BTC_USDT", "interval": "Min5", "time": ["1700000040"]}),
            context(),
            expected_interval="Min1",
            expected_start=datetime.fromtimestamp(1700000040, UTC),
            expected_end=datetime.fromtimestamp(1700000100, UTC),
        )
