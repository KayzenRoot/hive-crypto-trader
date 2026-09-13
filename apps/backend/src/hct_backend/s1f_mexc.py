"""Deterministic, fixture-driven decoder for the locked public MEXC V1 contract."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import Any, cast

from hct_backend.contracts import Environment, IdentityKind, StableId
from hct_backend.market_truth import GenerationRef
from hct_backend.s1f_numeric import (
    DecimalValue,
    NumericFailureReason,
    NumericPolicyError,
    require_price,
    require_quantity,
)
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
)

MEXC_SOURCE_CONTRACT_VERSION = "S1F_MEXC_SOURCE_CONTRACT_V1"
MEXC_WS_URL = "wss://contract.mexc.com/edge"
MEXC_PUBLIC_CHANNELS = (
    "sub.tickers",
    "sub.ticker",
    "sub.deal",
    "sub.depth",
    "sub.depth.full",
    "sub.kline",
)
MEXC_REST_DEPTH = "/api/v1/contract/depth/"
MEXC_REST_DEPTH_COMMITS = "/api/v1/contract/depth_commits/"
MEXC_REST_KLINE = "/api/v1/contract/kline/"


class MexcQuarantineError(ValueError):
    """Provider data is rejected before it can become canonical value truth."""

    def __init__(self, reason: str, payload_fingerprint: str) -> None:
        self.reason = reason
        self.payload_fingerprint = payload_fingerprint
        super().__init__(f"{reason}: {payload_fingerprint}")


@dataclass(frozen=True, slots=True)
class QuarantinedPayload:
    reason: str
    payload_fingerprint: str
    channel: str | None


@dataclass(frozen=True, slots=True)
class MexcDecodeContext:
    source_id: StableId
    environment: Environment
    generation: GenerationRef
    contract_id: StableId
    symbol: str
    knowledge_time: datetime
    wall_receive_time: datetime
    monotonic_elapsed_ms: int
    provenance_fingerprint: str
    schema_version: int = 1
    subscription_context: str = ""
    previous_depth_version: int | None = None
    full_depth: bool = False

    def __post_init__(self) -> None:
        if (
            self.source_id.kind is not IdentityKind.EXCHANGE
            or self.contract_id.kind is not IdentityKind.INSTRUMENT
        ):
            raise ValueError("MEXC source and contract identities are required")
        if (
            self.generation.source_id != self.source_id
            or self.generation.environment is not self.environment
        ):
            raise ValueError("MEXC generation context differs")
        if not self.symbol or not self.subscription_context:
            raise ValueError("symbol and subscription context are required")


@dataclass(frozen=True, slots=True)
class DecodedMexcMessage:
    channel: str
    values: tuple[object, ...]
    payload_fingerprint: str
    capability: ValueCapability

    @property
    def value(self) -> object:
        if len(self.values) != 1:
            raise ValueError("message contains more than one canonical value")
        return self.values[0]


def _hash(material: object) -> str:
    raw = json.dumps(material, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("MEXC time must be timezone-aware")
    return value.astimezone(UTC)


def _payload_fingerprint(payload: object) -> str:
    return _hash(payload)


def _strict_epoch_milliseconds(raw: object) -> datetime:
    text = str(raw)
    if not text.isdigit() or len(text) != 13:
        raise MexcQuarantineError(
            "EPOCH_MILLISECONDS_STRICT_13_DIGIT_VALIDATOR", _payload_fingerprint(raw)
        )
    return datetime.fromtimestamp(int(text) / 1000, UTC)


def _epoch_seconds(raw: object) -> datetime:
    text = str(raw)
    if not text.isdigit() or len(text) not in {10, 11}:
        raise MexcQuarantineError("KLINE_EPOCH_SECONDS_REQUIRED", _payload_fingerprint(raw))
    return datetime.fromtimestamp(int(text), UTC)


def _field(data: dict[str, Any], key: str, payload: object) -> Any:
    if key not in data:
        raise MexcQuarantineError(f"MISSING_REQUIRED_FIELD:{key}", _payload_fingerprint(payload))
    return data[key]


def _decimal(
    raw: object, payload: object, *, price: bool = False, quantity: bool = False
) -> DecimalValue:
    try:
        value = DecimalValue.parse(raw if isinstance(raw, (str, int, Decimal)) else raw)  # type: ignore[arg-type]
        if price:
            return require_price(value.value)
        if quantity:
            return require_quantity(value.value)
        return value
    except (NumericPolicyError, TypeError, ValueError) as exc:
        reason = getattr(exc, "reason", NumericFailureReason.MALFORMED)
        raise MexcQuarantineError(f"DECIMAL:{reason}", _payload_fingerprint(payload)) from exc


def _quantity(raw: object, payload: object, contract_version: str) -> Quantity:
    return Quantity(
        _decimal(raw, payload, quantity=True),
        QuantityUnit.CONTRACTS_PROVIDER_NATIVE_V1,
        contract_version,
    )


def _context(
    ctx: MexcDecodeContext, channel: str, event_time: datetime, payload_fp: str
) -> ValueContext:
    return ValueContext(
        source_id=ctx.source_id,
        channel=channel,
        contract_id=ctx.contract_id,
        environment=ctx.environment,
        generation=ctx.generation,
        schema_version=ctx.schema_version,
        provenance_fingerprint=ctx.provenance_fingerprint,
        originating_event_fingerprint=_hash(
            {"payload": payload_fp, "channel": channel, "symbol": ctx.symbol}
        ),
        event_time=event_time,
        knowledge_time=_utc(ctx.knowledge_time),
        wall_receive_time=_utc(ctx.wall_receive_time),
        monotonic_elapsed_ms=ctx.monotonic_elapsed_ms,
    )


def _capability_value(
    data: dict[str, Any], field: str, parser: Any, payload: object, *, required: bool = False
) -> CapabilityValue[Any]:
    if field not in data or data[field] is None:
        if required:
            raise MexcQuarantineError(
                f"MISSING_REQUIRED_FIELD:{field}", _payload_fingerprint(payload)
            )
        return CapabilityValue.unavailable(CapabilityState.UNKNOWN, field)
    try:
        return CapabilityValue.supported(parser(data[field]), field)
    except (NumericPolicyError, ValueError, TypeError) as exc:
        raise MexcQuarantineError(f"FIELD_INVALID:{field}", _payload_fingerprint(payload)) from exc


def _timeframe(name: str, payload: object) -> Timeframe:
    durations = {
        "Min1": 60,
        "Min5": 300,
        "Min15": 900,
        "Min30": 1800,
        "Min60": 3600,
        "Hour4": 14400,
        "Hour8": 28800,
        "Day1": 86400,
        "Week1": 604800,
        "Month1": 2592000,
    }
    try:
        return Timeframe(name, durations[name])
    except (KeyError, ValueError) as exc:
        raise MexcQuarantineError(
            "UNKNOWN_PROVIDER_INTERVAL", _payload_fingerprint(payload)
        ) from exc


def _book_level(raw: object, payload: object, contract_version: str) -> BookLevel:
    if not isinstance(raw, list) or len(raw) != 3:
        raise MexcQuarantineError(
            "DEPTH_TUPLE_MUST_BE_PRICE_CONTRACT_VOLUME_ORDER_COUNT", _payload_fingerprint(payload)
        )
    try:
        price = _decimal(raw[0], payload, price=True)
        quantity = _quantity(raw[1], payload, contract_version)
        order_count = int(raw[2])
    except (ValueError, TypeError) as exc:
        raise MexcQuarantineError("DEPTH_TUPLE_INVALID", _payload_fingerprint(payload)) from exc
    return BookLevel(price, quantity, order_count)


class MexcPublicDecoder:
    """Decode only the normalized public source contract; unknown payloads quarantine."""

    def decode(self, raw: str | bytes, context: MexcDecodeContext) -> DecodedMexcMessage:
        try:
            payload = json.loads(raw, parse_float=str, parse_int=str)
        except (TypeError, ValueError, json.JSONDecodeError) as exc:
            raise MexcQuarantineError("MALFORMED_JSON", _payload_fingerprint(str(raw))) from exc
        payload_fp = _payload_fingerprint(payload)
        if not isinstance(payload, dict):
            raise MexcQuarantineError("ROOT_OBJECT_REQUIRED", payload_fp)
        channel = payload.get("channel")
        if channel not in {"push.ticker", "push.tickers", "push.deal", "push.kline", "push.depth"}:
            raise MexcQuarantineError("UNKNOWN_OR_UNAUTHORIZED_CHANNEL", payload_fp)
        outer_ts = _field(payload, "ts", payload)
        event_time = _strict_epoch_milliseconds(outer_ts)
        data = _field(payload, "data", payload)
        if not isinstance(data, (dict, list)):
            raise MexcQuarantineError("DATA_OBJECT_OR_LIST_REQUIRED", payload_fp)
        values: tuple[object, ...]
        if channel == "push.ticker":
            if not isinstance(data, dict):
                raise MexcQuarantineError("TICKER_OBJECT_REQUIRED", payload_fp)
            values = (
                self._ticker(cast(dict[str, Any], data), payload, context, event_time, payload_fp),
            )
        elif channel == "push.tickers":
            values = self._bulk_ticker(data, payload, context, event_time, payload_fp)
        elif channel == "push.deal":
            if not isinstance(data, dict):
                raise MexcQuarantineError("DEALS_OBJECT_REQUIRED", payload_fp)
            values = self._deals(
                cast(dict[str, Any], data), payload, context, event_time, payload_fp
            )
        elif channel == "push.kline":
            if not isinstance(data, dict):
                raise MexcQuarantineError("KLINE_OBJECT_REQUIRED", payload_fp)
            values = (
                self._candle(cast(dict[str, Any], data), payload, context, event_time, payload_fp),
            )
        else:
            if not isinstance(data, dict):
                raise MexcQuarantineError("DEPTH_OBJECT_REQUIRED", payload_fp)
            values = (
                self._depth(cast(dict[str, Any], data), payload, context, event_time, payload_fp),
            )
        family = type(values[0]).__name__ if values else "Unknown"
        return DecodedMexcMessage(
            channel, values, payload_fp, ValueCapability(family, channel, CapabilityState.SUPPORTED)
        )

    def decode_rest_depth(self, raw: str | bytes, context: MexcDecodeContext) -> OrderBookSnapshot:
        payload = self._json_object(raw)
        payload_fp = _payload_fingerprint(payload)
        timestamp = _strict_epoch_milliseconds(_field(payload, "timestamp", payload))
        version = int(_field(payload, "version", payload))
        return OrderBookSnapshot(
            _context(context, "rest.depth", timestamp, payload_fp),
            tuple(
                _book_level(item, payload, MEXC_SOURCE_CONTRACT_VERSION)
                for item in _field(payload, "bids", payload)
            ),
            tuple(
                _book_level(item, payload, MEXC_SOURCE_CONTRACT_VERSION)
                for item in _field(payload, "asks", payload)
            ),
            version,
            context.subscription_context,
        )

    def decode_rest_kline_close_proof(
        self,
        raw: str | bytes,
        context: MexcDecodeContext,
        *,
        expected_interval: str,
        expected_start: datetime,
        expected_end: datetime,
    ) -> str:
        payload = self._json_object(raw)
        payload_fp = _payload_fingerprint(payload)
        if payload.get("interval") != expected_interval or payload.get("symbol") not in {
            None,
            context.symbol,
        }:
            raise MexcQuarantineError("KLINE_CLOSE_IDENTITY_MISMATCH", payload_fp)
        times = _field(payload, "time", payload)
        if not isinstance(times, list) or not any(
            _epoch_seconds(item) == expected_start for item in times
        ):
            raise MexcQuarantineError("KLINE_CLOSE_TIME_PROOF_MISMATCH", payload_fp)
        if expected_end <= expected_start:
            raise MexcQuarantineError("KLINE_INTERVAL_INVALID", payload_fp)
        return _hash(
            {
                "source": MEXC_SOURCE_CONTRACT_VERSION,
                "symbol": context.symbol,
                "interval": expected_interval,
                "start": expected_start.isoformat(),
                "end": expected_end.isoformat(),
                "time": times,
            }
        )

    def _json_object(self, raw: str | bytes) -> dict[str, Any]:
        try:
            payload = json.loads(raw, parse_float=str, parse_int=str)
        except (TypeError, ValueError, json.JSONDecodeError) as exc:
            raise MexcQuarantineError("MALFORMED_JSON", _payload_fingerprint(str(raw))) from exc
        if not isinstance(payload, dict):
            raise MexcQuarantineError("ROOT_OBJECT_REQUIRED", _payload_fingerprint(payload))
        return payload

    def _ticker(
        self,
        data: dict[str, Any],
        payload: object,
        ctx: MexcDecodeContext,
        event_time: datetime,
        payload_fp: str,
    ) -> TickerState:
        symbol = payload.get("symbol") if isinstance(payload, dict) else None
        if symbol not in {None, ctx.symbol}:
            raise MexcQuarantineError("SYMBOL_CONTEXT_MISMATCH", payload_fp)
        context = _context(ctx, "sub.ticker", event_time, payload_fp)

        def parse_price(raw: object) -> DecimalValue:
            return _decimal(raw, payload, price=True)

        def parse_quantity(raw: object) -> Quantity:
            return _quantity(raw, payload, MEXC_SOURCE_CONTRACT_VERSION)

        return TickerState(
            context,
            _capability_value(data, "lastPrice", parse_price, payload, required=True),
            _capability_value(data, "bid1", parse_price, payload),
            _capability_value(data, "ask1", parse_price, payload),
            _capability_value(data, "volume24", parse_quantity, payload),
            _capability_value(data, "holdVol", parse_quantity, payload),
            _capability_value(data, "indexPrice", parse_price, payload),
            _capability_value(data, "fairPrice", parse_price, payload),
            _capability_value(data, "fundingRate", lambda raw: _decimal(raw, payload), payload),
        )

    def _bulk_ticker(
        self,
        data: list[Any] | dict[str, Any],
        payload: object,
        ctx: MexcDecodeContext,
        event_time: datetime,
        payload_fp: str,
    ) -> tuple[object, ...]:
        rows = data if isinstance(data, list) else data.get("data", [])
        if not isinstance(rows, list):
            raise MexcQuarantineError("BULK_TICKER_LIST_REQUIRED", payload_fp)
        values: list[TickerState] = []
        for row in rows:
            if not isinstance(row, dict) or row.get("symbol") not in {None, ctx.symbol}:
                raise MexcQuarantineError("BULK_TICKER_SYMBOL_MISMATCH", payload_fp)
            values.append(self._ticker(row, {"symbol": ctx.symbol}, ctx, event_time, payload_fp))
        return tuple(values)

    def _deals(
        self,
        data: dict[str, Any],
        payload: object,
        ctx: MexcDecodeContext,
        event_time: datetime,
        payload_fp: str,
    ) -> tuple[TradeTick, ...]:
        rows = data.get("deals")
        if rows is None and all(key in data for key in ("p", "v", "t")):
            rows = [data]
        if not isinstance(rows, list) or not rows:
            raise MexcQuarantineError("DEALS_LIST_REQUIRED", payload_fp)
        values: list[TradeTick] = []
        for row in rows:
            if not isinstance(row, dict):
                raise MexcQuarantineError("DEAL_OBJECT_REQUIRED", payload_fp)
            deal_time = _strict_epoch_milliseconds(_field(row, "t", payload))
            context = _context(ctx, "sub.deal", deal_time, payload_fp)
            aggressor = {1: "BUY", 2: "SELL"}.get(int(row["T"])) if "T" in row else None
            values.append(
                TradeTick(
                    context,
                    _decimal(_field(row, "p", payload), payload, price=True),
                    _quantity(_field(row, "v", payload), payload, MEXC_SOURCE_CONTRACT_VERSION),
                    aggressor,
                )
            )
        return tuple(values)

    def _candle(
        self,
        data: dict[str, Any],
        payload: object,
        ctx: MexcDecodeContext,
        event_time: datetime,
        payload_fp: str,
    ) -> CandleBar:
        interval = _field(data, "interval", payload)
        timeframe = _timeframe(interval, payload)
        start = _epoch_seconds(_field(data, "t", payload))
        end = start + timedelta(seconds=timeframe.duration_seconds)
        context = _context(ctx, "sub.kline", event_time, payload_fp)
        open_value = _decimal(_field(data, "o", payload), payload, price=True)
        high = _decimal(_field(data, "h", payload), payload, price=True)
        low = _decimal(_field(data, "l", payload), payload, price=True)
        close = _decimal(_field(data, "c", payload), payload, price=True)
        lineage = OrderedLineage.from_event(
            context.originating_event_fingerprint, context.knowledge_time
        )
        return CandleBar(
            context,
            timeframe,
            start,
            end,
            open_value,
            high,
            low,
            close,
            _quantity(_field(data, "q", payload), payload, MEXC_SOURCE_CONTRACT_VERSION),
            ProviderTransactionAmount(
                _decimal(_field(data, "a", payload), payload, quantity=True),
                MEXC_SOURCE_CONTRACT_VERSION,
            ),
            Finality.OPEN,
            lineage,
        )

    def _depth(
        self,
        data: dict[str, Any],
        payload: object,
        ctx: MexcDecodeContext,
        event_time: datetime,
        payload_fp: str,
    ) -> OrderBookSnapshot | OrderBookDelta:
        version = int(_field(data, "version", payload))
        context = _context(ctx, "sub.depth", event_time, payload_fp)
        bids = tuple(
            _book_level(item, payload, MEXC_SOURCE_CONTRACT_VERSION)
            for item in _field(data, "bids", payload)
        )
        asks = tuple(
            _book_level(item, payload, MEXC_SOURCE_CONTRACT_VERSION)
            for item in _field(data, "asks", payload)
        )
        if ctx.full_depth:
            return OrderBookSnapshot(context, bids, asks, version, ctx.subscription_context)
        if ctx.previous_depth_version is None:
            raise MexcQuarantineError("PREVIOUS_DEPTH_VERSION_REQUIRED", payload_fp)
        return OrderBookDelta(
            context, bids, asks, ctx.previous_depth_version, version, ctx.subscription_context
        )


def reference_and_funding_from_ticker(
    ticker: TickerState,
) -> tuple[ReferencePriceEvidence, ...] | tuple[()]:
    values: list[ReferencePriceEvidence] = []
    if ticker.fair_price.value is not None:
        values.extend(
            (
                ReferencePriceEvidence(
                    ticker.context, ReferencePriceKind.MARK, ticker.fair_price.value, "fairPrice"
                ),
                ReferencePriceEvidence(
                    ticker.context, ReferencePriceKind.FAIR, ticker.fair_price.value, "fairPrice"
                ),
            )
        )
    if ticker.index_price.value is not None:
        values.append(
            ReferencePriceEvidence(
                ticker.context, ReferencePriceKind.INDEX, ticker.index_price.value, "indexPrice"
            )
        )
    return tuple(values)


def funding_from_ticker(ticker: TickerState) -> FundingEvidence | None:
    if ticker.funding_rate.value is None:
        return None
    return FundingEvidence(ticker.context, ticker.funding_rate.value, ticker.context.event_time)
