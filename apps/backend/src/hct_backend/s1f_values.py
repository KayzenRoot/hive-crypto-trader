"""Immutable, provider-neutral typed public market values for S1F."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from typing import Any, TypeVar

from hct_backend.contracts import Environment, IdentityKind, StableId
from hct_backend.market_truth import GenerationRef, NormalizedMarketEvent
from hct_backend.s1f_numeric import (
    DecimalValue,
    NumericFailureReason,
    NumericPolicyError,
    require_price,
    require_quantity,
    validate_ohlc,
)


class ValuePlaneError(ValueError):
    """Base error for fail-closed typed value contracts."""


class ValuePlaneConsistencyError(ValuePlaneError):
    """Raised when identity, lineage, units or proof contradict."""


class CapabilityState(StrEnum):
    SUPPORTED = "SUPPORTED"
    UNSUPPORTED = "UNSUPPORTED"
    UNKNOWN = "UNKNOWN"


class QuantityUnit(StrEnum):
    CONTRACTS_PROVIDER_NATIVE_V1 = "CONTRACTS_PROVIDER_NATIVE_V1"


class Finality(StrEnum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    UNKNOWN = "UNKNOWN"


class CandleProofKind(StrEnum):
    NEXT_WINDOW = "NEXT_WINDOW"
    REST_CONFIRMATION = "REST_CONFIRMATION"


class ReferencePriceKind(StrEnum):
    MARK = "MARK"
    INDEX = "INDEX"
    FAIR = "FAIR"


T = TypeVar("T")
_CANDLE_PROOF_ATTESTATION: object = object()


def _hash(material: object) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _utc(value: datetime, label: str) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise ValuePlaneError(f"{label} must be timezone-aware UTC")
    return value.astimezone(UTC)


def _fingerprint(value: str, label: str) -> None:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(c not in "0123456789abcdef" for c in value)
    ):
        raise ValuePlaneError(f"{label} must be a lowercase SHA-256 fingerprint")


def _stable(value: StableId, kind: IdentityKind, label: str) -> None:
    if not isinstance(value, StableId) or value.kind is not kind:
        raise ValuePlaneError(f"{label} has the wrong identity kind")


@dataclass(frozen=True, slots=True)
class ValueContext:
    source_id: StableId
    channel: str
    contract_id: StableId
    environment: Environment
    generation: GenerationRef
    schema_version: int
    provenance_fingerprint: str
    originating_event_fingerprint: str
    event_time: datetime
    knowledge_time: datetime
    wall_receive_time: datetime
    monotonic_elapsed_ms: int

    def __post_init__(self) -> None:
        _stable(self.source_id, IdentityKind.EXCHANGE, "value source")
        _stable(self.contract_id, IdentityKind.INSTRUMENT, "value contract")
        if not isinstance(self.environment, Environment):
            raise ValuePlaneError("value environment is invalid")
        if (
            self.generation.source_id != self.source_id
            or self.generation.environment is not self.environment
        ):
            raise ValuePlaneConsistencyError("value generation identity differs")
        if not isinstance(self.channel, str) or not self.channel:
            raise ValuePlaneError("value channel is required")
        if (
            isinstance(self.schema_version, bool)
            or not isinstance(self.schema_version, int)
            or self.schema_version < 1
        ):
            raise ValuePlaneError("value schema version is invalid")
        _fingerprint(self.provenance_fingerprint, "value provenance")
        _fingerprint(self.originating_event_fingerprint, "originating event")
        object.__setattr__(self, "event_time", _utc(self.event_time, "event time"))
        object.__setattr__(self, "knowledge_time", _utc(self.knowledge_time, "knowledge time"))
        object.__setattr__(
            self, "wall_receive_time", _utc(self.wall_receive_time, "wall receive time")
        )
        if self.knowledge_time > self.wall_receive_time:
            raise ValuePlaneConsistencyError("knowledge_time cannot be after wall_receive_time")
        if (
            isinstance(self.monotonic_elapsed_ms, bool)
            or not isinstance(self.monotonic_elapsed_ms, int)
            or self.monotonic_elapsed_ms < 0
        ):
            raise ValuePlaneError("monotonic elapsed time is invalid")

    @classmethod
    def from_event(
        cls,
        event: NormalizedMarketEvent,
        *,
        knowledge_time: datetime,
        wall_receive_time: datetime | None = None,
        monotonic_elapsed_ms: int | None = None,
    ) -> ValueContext:
        if not isinstance(event, NormalizedMarketEvent):
            raise ValuePlaneError("normalized event is required")
        receive = wall_receive_time or event.wall_receive_time
        elapsed = (
            event.monotonic_elapsed_ms if monotonic_elapsed_ms is None else monotonic_elapsed_ms
        )
        return cls(
            source_id=event.source_id,
            channel=event.channel,
            contract_id=event.contract_id,
            environment=event.environment,
            generation=event.generation,
            schema_version=event.schema_version,
            provenance_fingerprint=event.provenance_fingerprint,
            originating_event_fingerprint=event.fingerprint,
            event_time=event.event_time,
            knowledge_time=knowledge_time,
            wall_receive_time=receive,
            monotonic_elapsed_ms=elapsed,
        )

    @property
    def identity_fingerprint(self) -> str:
        return _hash(
            {
                "source": self.source_id.as_text(),
                "channel": self.channel,
                "contract": self.contract_id.as_text(),
                "environment": self.environment.value,
                "generation": self.generation.fingerprint,
                "schema": self.schema_version,
                "provenance": self.provenance_fingerprint,
                "event": self.originating_event_fingerprint,
            }
        )


@dataclass(frozen=True, slots=True)
class Quantity:
    value: DecimalValue
    unit: QuantityUnit
    source_contract_identity_version: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, DecimalValue) or not isinstance(self.unit, QuantityUnit):
            raise ValuePlaneError("typed quantity value and unit are required")
        if (
            not isinstance(self.source_contract_identity_version, str)
            or not self.source_contract_identity_version
        ):
            raise ValuePlaneError("quantity source contract identity is required")
        if self.value.value < 0:
            raise NumericPolicyError(
                NumericFailureReason.NEGATIVE_QUANTITY, "quantity cannot be negative"
            )

    @property
    def fingerprint(self) -> str:
        return _hash(
            {
                "value": self.value.canonical_text,
                "material_scale": self.value.material_scale,
                "unit_kind": self.unit.value,
                "source_contract_identity_version": self.source_contract_identity_version,
            }
        )


@dataclass(frozen=True, slots=True)
class ProviderTransactionAmount:
    value: DecimalValue
    source_contract_identity_version: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, DecimalValue) or self.value.value < 0:
            raise ValuePlaneError("transaction amount must be a nonnegative Decimal")
        if (
            not isinstance(self.source_contract_identity_version, str)
            or not self.source_contract_identity_version
        ):
            raise ValuePlaneError("amount source contract identity is required")

    @property
    def fingerprint(self) -> str:
        return _hash(
            {
                "value": self.value.canonical_text,
                "material_scale": self.value.material_scale,
                "type": "ProviderTransactionAmount",
                "source_contract_identity_version": self.source_contract_identity_version,
            }
        )


@dataclass(frozen=True, slots=True)
class CapabilityValue[T]:
    state: CapabilityState
    value: T | None
    source_field: str

    def __post_init__(self) -> None:
        if not isinstance(self.state, CapabilityState) or not self.source_field:
            raise ValuePlaneError("capability value metadata is invalid")
        if self.state is CapabilityState.SUPPORTED and self.value is None:
            raise ValuePlaneConsistencyError("SUPPORTED value cannot be absent")
        if self.state is not CapabilityState.SUPPORTED and self.value is not None:
            raise ValuePlaneConsistencyError("unsupported or unknown value cannot be synthesized")

    @classmethod
    def supported(cls, value: T, source_field: str) -> CapabilityValue[T]:
        return cls(CapabilityState.SUPPORTED, value, source_field)

    @classmethod
    def unavailable(cls, state: CapabilityState, source_field: str) -> CapabilityValue[T]:
        if state is CapabilityState.SUPPORTED:
            raise ValuePlaneError("unavailable state must not be SUPPORTED")
        return cls(state, None, source_field)


@dataclass(frozen=True, slots=True)
class ValueCapability:
    family: str
    channel: str
    state: CapabilityState
    policy_version: int = 1

    def __post_init__(self) -> None:
        if not self.family or not self.channel or not isinstance(self.state, CapabilityState):
            raise ValuePlaneError("value capability is invalid")
        if (
            isinstance(self.policy_version, bool)
            or not isinstance(self.policy_version, int)
            or self.policy_version < 1
        ):
            raise ValuePlaneError("capability policy version is invalid")

    @property
    def fingerprint(self) -> str:
        return _hash(
            {
                "family": self.family,
                "channel": self.channel,
                "state": self.state.value,
                "policy": self.policy_version,
            }
        )


@dataclass(frozen=True, slots=True)
class OrderedLineage:
    fingerprints: tuple[str, ...]
    manifest_fingerprint: str
    knowledge_time: datetime

    def __post_init__(self) -> None:
        if not isinstance(self.fingerprints, tuple) or not self.fingerprints:
            raise ValuePlaneError("ordered lineage requires fingerprints")
        for item in self.fingerprints:
            _fingerprint(item, "lineage entry")
        if len(set(self.fingerprints)) != len(self.fingerprints):
            raise ValuePlaneConsistencyError(
                "ordered lineage cannot contain duplicate fingerprints"
            )
        _fingerprint(self.manifest_fingerprint, "lineage manifest")
        expected_manifest = _hash({"ordered": self.fingerprints})
        if self.manifest_fingerprint != expected_manifest:
            raise ValuePlaneConsistencyError("lineage manifest does not match ordered entries")
        object.__setattr__(
            self, "knowledge_time", _utc(self.knowledge_time, "lineage knowledge time")
        )

    @classmethod
    def from_fingerprints(
        cls, fingerprints: tuple[str, ...], knowledge_time: datetime
    ) -> OrderedLineage:
        return cls(
            fingerprints=fingerprints,
            manifest_fingerprint=_hash({"ordered": fingerprints}),
            knowledge_time=knowledge_time,
        )

    @classmethod
    def from_event(cls, event_fingerprint: str, knowledge_time: datetime) -> OrderedLineage:
        return cls.from_fingerprints((event_fingerprint,), knowledge_time)

    def append(self, fingerprint: str, knowledge_time: datetime) -> OrderedLineage:
        _fingerprint(fingerprint, "lineage entry")
        return self.from_fingerprints(self.fingerprints + (fingerprint,), knowledge_time)


@dataclass(frozen=True, slots=True)
class TradeTick:
    context: ValueContext
    price: DecimalValue
    quantity: Quantity
    aggressor: str | None = None
    value_version: int = 1

    def __post_init__(self) -> None:
        if not isinstance(self.price, DecimalValue) or self.price.value <= 0:
            raise NumericPolicyError(
                NumericFailureReason.NON_POSITIVE_PRICE, "trade price must be positive"
            )
        if (
            not isinstance(self.quantity, Quantity)
            or self.quantity.unit is not QuantityUnit.CONTRACTS_PROVIDER_NATIVE_V1
        ):
            raise ValuePlaneConsistencyError(
                "trade quantity must use provider-native contract units"
            )
        require_quantity(self.quantity.value.value)
        if self.aggressor is not None and self.aggressor not in {"BUY", "SELL", "UNKNOWN"}:
            raise ValuePlaneError("aggressor is not a canonical value")
        if (
            isinstance(self.value_version, bool)
            or not isinstance(self.value_version, int)
            or self.value_version < 1
        ):
            raise ValuePlaneError("value version is invalid")

    @property
    def fingerprint(self) -> str:
        return _hash(
            {
                "family": "TradeTick",
                "context": self.context.identity_fingerprint,
                "price": self.price.fingerprint,
                "quantity": self.quantity.fingerprint,
                "aggressor": self.aggressor,
                "version": self.value_version,
            }
        )


@dataclass(frozen=True, slots=True)
class TickerState:
    context: ValueContext
    last_price: CapabilityValue[DecimalValue]
    bid_price: CapabilityValue[DecimalValue]
    ask_price: CapabilityValue[DecimalValue]
    volume24: CapabilityValue[Quantity]
    hold_vol: CapabilityValue[Quantity]
    index_price: CapabilityValue[DecimalValue]
    fair_price: CapabilityValue[DecimalValue]
    funding_rate: CapabilityValue[DecimalValue]
    value_version: int = 1

    def __post_init__(self) -> None:
        values = (
            self.last_price,
            self.bid_price,
            self.ask_price,
            self.index_price,
            self.fair_price,
            self.funding_rate,
        )
        if (
            any(not isinstance(value, CapabilityValue) for value in values)
            or not isinstance(self.volume24, CapabilityValue)
            or not isinstance(self.hold_vol, CapabilityValue)
        ):
            raise ValuePlaneError("ticker capability values are required")
        for value in (
            self.last_price,
            self.bid_price,
            self.ask_price,
            self.index_price,
            self.fair_price,
        ):
            if value.value is not None and value.value.value <= 0:
                raise NumericPolicyError(
                    NumericFailureReason.NON_POSITIVE_PRICE, "ticker price must be positive"
                )
        for quantity_capability in (self.volume24, self.hold_vol):
            if (
                quantity_capability.value is not None
                and quantity_capability.value.unit is not QuantityUnit.CONTRACTS_PROVIDER_NATIVE_V1
            ):
                raise ValuePlaneConsistencyError("ticker quantity must use provider-native units")

    @property
    def fingerprint(self) -> str:
        def material(value: CapabilityValue[Any]) -> object:
            return {
                "state": value.state.value,
                "value": getattr(value.value, "fingerprint", None),
                "source": value.source_field,
            }

        return _hash(
            {
                "family": "TickerState",
                "context": self.context.identity_fingerprint,
                "fields": [
                    material(item)
                    for item in (
                        self.last_price,
                        self.bid_price,
                        self.ask_price,
                        self.volume24,
                        self.hold_vol,
                        self.index_price,
                        self.fair_price,
                        self.funding_rate,
                    )
                ],
                "version": self.value_version,
            }
        )


@dataclass(frozen=True, slots=True)
class Timeframe:
    name: str
    duration_seconds: int
    version: int = 1
    alignment: str = "UNIX_EPOCH_MULTIPLES"

    def __post_init__(self) -> None:
        if (
            not self.name
            or isinstance(self.duration_seconds, bool)
            or not isinstance(self.duration_seconds, int)
            or self.duration_seconds <= 0
        ):
            raise ValuePlaneError("timeframe is invalid")
        if isinstance(self.version, bool) or not isinstance(self.version, int) or self.version < 1:
            raise ValuePlaneError("timeframe version is invalid")
        if self.alignment != "UNIX_EPOCH_MULTIPLES":
            raise ValuePlaneConsistencyError("unsupported timeframe alignment")

    @property
    def fingerprint(self) -> str:
        return _hash(
            {
                "name": self.name,
                "duration_seconds": self.duration_seconds,
                "version": self.version,
                "alignment": self.alignment,
            }
        )


@dataclass(frozen=True, slots=True, init=False)
class CandleCloseProof:
    kind: CandleProofKind
    source_id: StableId
    contract_id: StableId
    environment: Environment
    generation: GenerationRef
    timeframe_fingerprint: str
    expected_start: datetime
    expected_end: datetime
    evidence_fingerprint: str
    knowledge_time: datetime
    admissibility_time: datetime
    next_window_start: datetime | None = None
    origin: str = ""
    _attestation: object = field(default=None, repr=False, compare=False)

    def __init__(self, *args: object, **kwargs: object) -> None:
        raise ValuePlaneConsistencyError("CandleCloseProof must be issued by an evaluator")

    @classmethod
    def _from_evaluator(
        cls,
        *,
        kind: CandleProofKind,
        source_id: StableId,
        contract_id: StableId,
        environment: Environment,
        generation: GenerationRef,
        timeframe_fingerprint: str,
        expected_start: datetime,
        expected_end: datetime,
        evidence_fingerprint: str,
        knowledge_time: datetime,
        admissibility_time: datetime,
        next_window_start: datetime | None,
        origin: str,
    ) -> CandleCloseProof:
        instance = object.__new__(cls)
        object.__setattr__(instance, "kind", kind)
        object.__setattr__(instance, "source_id", source_id)
        object.__setattr__(instance, "contract_id", contract_id)
        object.__setattr__(instance, "environment", environment)
        object.__setattr__(instance, "generation", generation)
        object.__setattr__(instance, "timeframe_fingerprint", timeframe_fingerprint)
        object.__setattr__(instance, "expected_start", expected_start)
        object.__setattr__(instance, "expected_end", expected_end)
        object.__setattr__(instance, "evidence_fingerprint", evidence_fingerprint)
        object.__setattr__(instance, "knowledge_time", knowledge_time)
        object.__setattr__(instance, "admissibility_time", admissibility_time)
        object.__setattr__(instance, "next_window_start", next_window_start)
        object.__setattr__(instance, "origin", origin)
        object.__setattr__(instance, "_attestation", _CANDLE_PROOF_ATTESTATION)
        instance.__post_init__()
        return instance

    @classmethod
    def _from_next_window_evidence(
        cls,
        *,
        current_candle: CandleBar,
        next_window: CandleBar,
    ) -> CandleCloseProof:
        if not isinstance(current_candle, CandleBar) or not isinstance(next_window, CandleBar):
            raise ValuePlaneError("typed current and next-window candles are required")
        if current_candle.finality is not Finality.OPEN:
            raise ValuePlaneConsistencyError("next-window proof requires an open current candle")
        current_context = current_candle.context
        next_context = next_window.context
        if current_context.generation.retired or next_context.generation.retired:
            raise ValuePlaneConsistencyError("retired generation cannot attest candle close")
        if (
            next_context.source_id != current_context.source_id
            or next_context.contract_id != current_context.contract_id
            or next_context.environment is not current_context.environment
            or next_context.generation != current_context.generation
            or next_window.timeframe.fingerprint != current_candle.timeframe.fingerprint
        ):
            raise ValuePlaneConsistencyError("next-window evidence identity does not match")
        if next_window.start != current_candle.end:
            raise ValuePlaneConsistencyError(
                "next-window evidence must start at current candle end"
            )
        if next_context.knowledge_time < current_context.knowledge_time:
            raise ValuePlaneConsistencyError(
                "next-window evidence knowledge time predates current candle evidence"
            )
        if next_context.wall_receive_time < next_context.knowledge_time:
            raise ValuePlaneConsistencyError(
                "next-window evidence admissibility time predates its knowledge time"
            )
        return cls._from_evaluator(
            kind=CandleProofKind.NEXT_WINDOW,
            source_id=current_context.source_id,
            contract_id=current_context.contract_id,
            environment=current_context.environment,
            generation=current_context.generation,
            timeframe_fingerprint=current_candle.timeframe.fingerprint,
            expected_start=current_candle.start,
            expected_end=current_candle.end,
            evidence_fingerprint=next_window.fingerprint,
            knowledge_time=next_context.knowledge_time,
            admissibility_time=next_context.wall_receive_time,
            next_window_start=next_window.start,
            origin="NEXT_WINDOW_CONTINUITY_V1",
        )

    @classmethod
    def _from_decoder(
        cls,
        *,
        source_id: StableId,
        contract_id: StableId,
        environment: Environment,
        generation: GenerationRef,
        timeframe: Timeframe,
        start: datetime,
        end: datetime,
        evidence_fingerprint: str,
        knowledge_time: datetime,
        admissibility_time: datetime,
    ) -> CandleCloseProof:
        return cls._from_evaluator(
            kind=CandleProofKind.REST_CONFIRMATION,
            source_id=source_id,
            contract_id=contract_id,
            environment=environment,
            generation=generation,
            timeframe_fingerprint=timeframe.fingerprint,
            expected_start=start,
            expected_end=end,
            evidence_fingerprint=evidence_fingerprint,
            knowledge_time=knowledge_time,
            admissibility_time=admissibility_time,
            next_window_start=None,
            origin="MEXC_REST_KLINE_V1",
        )

    def __post_init__(self) -> None:
        if self._attestation is not _CANDLE_PROOF_ATTESTATION:
            raise ValuePlaneConsistencyError("candle close proof is not evaluator-issued")
        _stable(self.source_id, IdentityKind.EXCHANGE, "proof source")
        _stable(self.contract_id, IdentityKind.INSTRUMENT, "proof contract")
        if not isinstance(self.environment, Environment):
            raise ValuePlaneError("proof environment is invalid")
        if (
            self.generation.source_id != self.source_id
            or self.generation.environment is not self.environment
            or self.generation.retired
        ):
            raise ValuePlaneConsistencyError("proof generation identity differs")
        _fingerprint(self.timeframe_fingerprint, "proof timeframe")
        _fingerprint(self.evidence_fingerprint, "proof evidence")
        start = _utc(self.expected_start, "proof expected start")
        end = _utc(self.expected_end, "proof expected end")
        if end <= start:
            raise ValuePlaneConsistencyError("proof window must be half-open and positive")
        object.__setattr__(self, "expected_start", start)
        object.__setattr__(self, "expected_end", end)
        object.__setattr__(
            self, "knowledge_time", _utc(self.knowledge_time, "proof knowledge time")
        )
        object.__setattr__(
            self, "admissibility_time", _utc(self.admissibility_time, "proof admissibility time")
        )
        if self.knowledge_time > self.admissibility_time:
            raise ValuePlaneConsistencyError("proof knowledge time cannot be after admissibility")
        if self.kind is CandleProofKind.NEXT_WINDOW:
            if self.origin != "NEXT_WINDOW_CONTINUITY_V1" or self.next_window_start is None:
                raise ValuePlaneConsistencyError("next-window proof material is incomplete")
            if _utc(self.next_window_start, "proof next window") != end:
                raise ValuePlaneConsistencyError("next-window proof does not start at candle end")
            object.__setattr__(
                self, "next_window_start", _utc(self.next_window_start, "proof next window")
            )
        elif self.kind is CandleProofKind.REST_CONFIRMATION:
            if self.origin != "MEXC_REST_KLINE_V1" or self.next_window_start is not None:
                raise ValuePlaneConsistencyError("REST proof material is invalid")
        else:
            raise ValuePlaneError("unknown candle proof kind")

    @property
    def fingerprint(self) -> str:
        return _hash(
            {
                "kind": self.kind.value,
                "source": self.source_id.as_text(),
                "contract": self.contract_id.as_text(),
                "environment": self.environment.value,
                "generation": self.generation.fingerprint,
                "timeframe": self.timeframe_fingerprint,
                "start": self.expected_start.isoformat(),
                "end": self.expected_end.isoformat(),
                "evidence": self.evidence_fingerprint,
                "knowledge": self.knowledge_time.isoformat(),
                "admissibility": self.admissibility_time.isoformat(),
                "next_window_start": self.next_window_start.isoformat()
                if self.next_window_start
                else None,
                "origin": self.origin,
            }
        )

    def matches_candle(self, candle: CandleBar) -> bool:
        return (
            self._attestation is _CANDLE_PROOF_ATTESTATION
            and not self.generation.retired
            and candle.context.source_id == self.source_id
            and candle.context.contract_id == self.contract_id
            and candle.context.environment is self.environment
            and candle.context.generation == self.generation
            and candle.timeframe.fingerprint == self.timeframe_fingerprint
            and candle.start == self.expected_start
            and candle.end == self.expected_end
            and (
                self.kind is CandleProofKind.REST_CONFIRMATION
                or self.next_window_start == candle.end
            )
        )


@dataclass(frozen=True, slots=True)
class CandleBar:
    context: ValueContext
    timeframe: Timeframe
    start: datetime
    end: datetime
    open: DecimalValue
    high: DecimalValue
    low: DecimalValue
    close: DecimalValue
    volume: Quantity
    amount: ProviderTransactionAmount
    finality: Finality
    lineage: OrderedLineage
    revision: int = 0
    predecessor_fingerprint: str | None = None
    close_proof: CandleCloseProof | None = None

    def __post_init__(self) -> None:
        start = _utc(self.start, "candle start")
        end = _utc(self.end, "candle end")
        object.__setattr__(self, "start", start)
        object.__setattr__(self, "end", end)
        if end - start != timedelta(seconds=self.timeframe.duration_seconds):
            raise ValuePlaneConsistencyError("candle interval does not match timeframe")
        if start.timestamp() % self.timeframe.duration_seconds != 0:
            raise ValuePlaneConsistencyError("candle start is not Unix-epoch aligned")
        validate_ohlc(self.open, self.high, self.low, self.close)
        if self.volume.unit is not QuantityUnit.CONTRACTS_PROVIDER_NATIVE_V1:
            raise ValuePlaneConsistencyError("candle volume must use provider-native units")
        if not isinstance(self.amount, ProviderTransactionAmount):
            raise ValuePlaneError("candle amount must remain distinct from Quantity")
        if not isinstance(self.finality, Finality) or not isinstance(self.lineage, OrderedLineage):
            raise ValuePlaneError("candle finality and lineage are required")
        if (
            isinstance(self.revision, bool)
            or not isinstance(self.revision, int)
            or self.revision < 0
        ):
            raise ValuePlaneError("candle revision is invalid")
        if self.revision > 0 and not self.predecessor_fingerprint:
            raise ValuePlaneConsistencyError("correction requires predecessor lineage")
        if self.close_proof is not None and not isinstance(self.close_proof, CandleCloseProof):
            raise ValuePlaneConsistencyError("candle close proof must be typed")
        if self.finality is Finality.CLOSED and (
            self.close_proof is None or not self.close_proof.matches_candle(self)
        ):
            raise ValuePlaneConsistencyError("closed candle requires matching typed finality proof")

    @property
    def fingerprint(self) -> str:
        return _hash(
            {
                "family": "CandleBar",
                "context": self.context.identity_fingerprint,
                "timeframe": self.timeframe.fingerprint,
                "start": self.start.isoformat(),
                "end": self.end.isoformat(),
                "open": self.open.fingerprint,
                "high": self.high.fingerprint,
                "low": self.low.fingerprint,
                "close": self.close.fingerprint,
                "volume": self.volume.fingerprint,
                "amount": self.amount.fingerprint,
                "finality": self.finality.value,
                "lineage": self.lineage.manifest_fingerprint,
                "revision": self.revision,
                "predecessor": self.predecessor_fingerprint,
                "close_proof": self.close_proof.fingerprint if self.close_proof else None,
            }
        )


@dataclass(frozen=True, slots=True)
class BookLevel:
    price: DecimalValue
    quantity: Quantity
    order_count: int

    def __post_init__(self) -> None:
        if self.price.value <= 0:
            raise NumericPolicyError(
                NumericFailureReason.NON_POSITIVE_PRICE, "book price must be positive"
            )
        if self.quantity.unit is not QuantityUnit.CONTRACTS_PROVIDER_NATIVE_V1:
            raise ValuePlaneConsistencyError("book quantity must use provider-native units")
        if (
            isinstance(self.order_count, bool)
            or not isinstance(self.order_count, int)
            or self.order_count < 0
        ):
            raise ValuePlaneError("order count must be non-negative")

    @property
    def fingerprint(self) -> str:
        return _hash(
            {
                "price": self.price.fingerprint,
                "quantity": self.quantity.fingerprint,
                "order_count": self.order_count,
            }
        )


def _validate_levels(
    levels: tuple[BookLevel, ...], *, bids: bool, allow_zero: bool = False
) -> None:
    previous = None
    for level in levels:
        if not allow_zero and level.quantity.value.value == 0:
            raise ValuePlaneConsistencyError("zero quantity is only a delta removal instruction")
        current = level.price.value
        if previous is not None and (
            (bids and current >= previous) or (not bids and current <= previous)
        ):
            raise ValuePlaneConsistencyError("book levels are not canonically sorted")
        previous = current


@dataclass(frozen=True, slots=True)
class OrderBookSnapshot:
    context: ValueContext
    bids: tuple[BookLevel, ...]
    asks: tuple[BookLevel, ...]
    version: int
    subscription_context: str

    def __post_init__(self) -> None:
        _validate_levels(self.bids, bids=True)
        _validate_levels(self.asks, bids=False)
        if isinstance(self.version, bool) or not isinstance(self.version, int) or self.version < 0:
            raise ValuePlaneError("book version is invalid")
        if not self.subscription_context:
            raise ValuePlaneConsistencyError("full-depth identity requires subscription context")

    @property
    def fingerprint(self) -> str:
        return _hash(
            {
                "family": "OrderBookSnapshot",
                "context": self.context.identity_fingerprint,
                "bids": [level.fingerprint for level in self.bids],
                "asks": [level.fingerprint for level in self.asks],
                "version": self.version,
                "subscription_context": self.subscription_context,
            }
        )


@dataclass(frozen=True, slots=True)
class DepthRecoverySnapshot:
    source_id: StableId
    contract_id: StableId
    environment: Environment
    generation: GenerationRef
    subscription_context: str
    bids: tuple[BookLevel, ...]
    asks: tuple[BookLevel, ...]
    version: int
    provider_event_time: datetime | None
    knowledge_time: datetime
    wall_receive_time: datetime

    def __post_init__(self) -> None:
        _stable(self.source_id, IdentityKind.EXCHANGE, "recovery source")
        _stable(self.contract_id, IdentityKind.INSTRUMENT, "recovery contract")
        if not isinstance(self.environment, Environment):
            raise ValuePlaneError("recovery environment is invalid")
        if (
            self.generation.source_id != self.source_id
            or self.generation.environment is not self.environment
            or self.generation.retired
        ):
            raise ValuePlaneConsistencyError("recovery generation identity differs")
        if not self.subscription_context:
            raise ValuePlaneConsistencyError("recovery subscription context is required")
        if any(not isinstance(level, BookLevel) for level in (*self.bids, *self.asks)):
            raise ValuePlaneError("recovery levels must be typed")
        _validate_levels(self.bids, bids=True)
        _validate_levels(self.asks, bids=False)
        if isinstance(self.version, bool) or not isinstance(self.version, int) or self.version < 0:
            raise ValuePlaneError("recovery version is invalid")
        if self.provider_event_time is not None:
            object.__setattr__(
                self, "provider_event_time", _utc(self.provider_event_time, "provider event time")
            )
        object.__setattr__(
            self, "knowledge_time", _utc(self.knowledge_time, "recovery knowledge time")
        )
        object.__setattr__(
            self, "wall_receive_time", _utc(self.wall_receive_time, "recovery receive time")
        )
        if self.knowledge_time > self.wall_receive_time:
            raise ValuePlaneConsistencyError("recovery knowledge time cannot be after receive time")

    @property
    def fingerprint(self) -> str:
        return _hash(
            {
                "source": self.source_id.as_text(),
                "contract": self.contract_id.as_text(),
                "environment": self.environment.value,
                "generation": self.generation.fingerprint,
                "subscription": self.subscription_context,
                "bids": [level.fingerprint for level in self.bids],
                "asks": [level.fingerprint for level in self.asks],
                "version": self.version,
                "provider_event_time": self.provider_event_time.isoformat()
                if self.provider_event_time
                else None,
                "knowledge": self.knowledge_time.isoformat(),
                "receive": self.wall_receive_time.isoformat(),
            }
        )


@dataclass(frozen=True, slots=True)
class DepthRecoveryEvidence:
    snapshots: tuple[DepthRecoverySnapshot, ...]
    previous_version: int | None

    def __post_init__(self) -> None:
        if not self.snapshots:
            raise ValuePlaneConsistencyError("depth recovery evidence requires snapshots")
        if any(not isinstance(item, DepthRecoverySnapshot) for item in self.snapshots):
            raise ValuePlaneError("depth recovery snapshots must be typed")
        versions = tuple(item.version for item in self.snapshots)
        if versions != tuple(sorted(set(versions))):
            raise ValuePlaneConsistencyError("depth recovery versions must be strictly increasing")
        if self.previous_version is not None and (
            isinstance(self.previous_version, bool)
            or not isinstance(self.previous_version, int)
            or self.previous_version < 0
            or self.snapshots[-1].version <= self.previous_version
        ):
            raise ValuePlaneConsistencyError("depth recovery does not advance the current book")
        first = self.snapshots[0]
        if any(
            item.source_id != first.source_id
            or item.contract_id != first.contract_id
            or item.environment is not first.environment
            or item.generation != first.generation
            or item.subscription_context != first.subscription_context
            for item in self.snapshots[1:]
        ):
            raise ValuePlaneConsistencyError("depth recovery identity is inconsistent")

    @property
    def anchor(self) -> DepthRecoverySnapshot:
        return self.snapshots[-1]

    @property
    def fingerprint(self) -> str:
        return _hash(
            {
                "previous_version": self.previous_version,
                "snapshots": [snapshot.fingerprint for snapshot in self.snapshots],
            }
        )

    def resume_with_contiguous_delta(self, delta: OrderBookDelta) -> OrderBookSnapshot:
        anchor = self.anchor
        if (
            delta.context.source_id != anchor.source_id
            or delta.context.contract_id != anchor.contract_id
            or delta.context.environment is not anchor.environment
            or delta.context.generation != anchor.generation
            or delta.subscription_context != anchor.subscription_context
            or delta.previous_version != anchor.version
        ):
            raise ValuePlaneConsistencyError("delta does not continue the recovery anchor")
        snapshot = OrderBookSnapshot(
            delta.context,
            anchor.bids,
            anchor.asks,
            anchor.version,
            anchor.subscription_context,
        )
        return delta.apply(snapshot)


@dataclass(frozen=True, slots=True)
class OrderBookDelta:
    context: ValueContext
    bids: tuple[BookLevel, ...]
    asks: tuple[BookLevel, ...]
    previous_version: int
    version: int
    subscription_context: str

    def __post_init__(self) -> None:
        _validate_levels(self.bids, bids=True, allow_zero=True)
        _validate_levels(self.asks, bids=False, allow_zero=True)
        if self.version != self.previous_version + 1:
            raise ValuePlaneConsistencyError("depth version is not previous+1; resync is required")
        if not self.subscription_context:
            raise ValuePlaneConsistencyError("delta subscription context is required")

    @property
    def fingerprint(self) -> str:
        return _hash(
            {
                "family": "OrderBookDelta",
                "context": self.context.identity_fingerprint,
                "bids": [level.fingerprint for level in self.bids],
                "asks": [level.fingerprint for level in self.asks],
                "previous": self.previous_version,
                "version": self.version,
                "subscription_context": self.subscription_context,
            }
        )

    def apply(self, snapshot: OrderBookSnapshot) -> OrderBookSnapshot:
        if (
            snapshot.context.identity_fingerprint != self.context.identity_fingerprint
            or snapshot.version != self.previous_version
            or snapshot.subscription_context != self.subscription_context
        ):
            raise ValuePlaneConsistencyError("delta cannot mutate a different book context")

        def update(
            existing: tuple[BookLevel, ...], changes: tuple[BookLevel, ...], descending: bool
        ) -> tuple[BookLevel, ...]:
            levels = {level.price.canonical_text: level for level in existing}
            for level in changes:
                key = level.price.canonical_text
                if level.quantity.value.value == 0:
                    levels.pop(key, None)
                else:
                    levels[key] = level
            result = tuple(levels.values())
            return tuple(sorted(result, key=lambda item: item.price.value, reverse=descending))

        return OrderBookSnapshot(
            self.context,
            update(snapshot.bids, self.bids, True),
            update(snapshot.asks, self.asks, False),
            self.version,
            self.subscription_context,
        )


@dataclass(frozen=True, slots=True)
class ReferencePriceEvidence:
    context: ValueContext
    kind: ReferencePriceKind
    value: DecimalValue
    source_field: str

    def __post_init__(self) -> None:
        if not isinstance(self.kind, ReferencePriceKind) or not self.source_field:
            raise ValuePlaneError("reference price evidence metadata is invalid")
        require_price(self.value.value)

    @property
    def fingerprint(self) -> str:
        return _hash(
            {
                "family": "ReferencePriceEvidence",
                "context": self.context.identity_fingerprint,
                "kind": self.kind.value,
                "value": self.value.fingerprint,
                "source": self.source_field,
            }
        )


@dataclass(frozen=True, slots=True)
class FundingEvidence:
    context: ValueContext
    rate: DecimalValue
    applicable_time: datetime
    source_field: str = "fundingRate"

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "applicable_time", _utc(self.applicable_time, "funding applicable time")
        )
        if not isinstance(self.rate, DecimalValue):
            raise ValuePlaneError("funding rate must be Decimal")
        if not self.source_field:
            raise ValuePlaneError("funding source field is required")

    @property
    def fingerprint(self) -> str:
        return _hash(
            {
                "family": "FundingEvidence",
                "context": self.context.identity_fingerprint,
                "rate": self.rate.fingerprint,
                "applicable_time": self.applicable_time.isoformat(),
                "source": self.source_field,
            }
        )


def validate_series_units(values: tuple[Quantity, ...]) -> QuantityUnit:
    if not values:
        raise ValuePlaneConsistencyError("quantity series cannot be empty")
    units = {value.unit for value in values}
    if len(units) != 1:
        raise ValuePlaneConsistencyError("mixed quantity units fail closed")
    return next(iter(units))


def value_context_from_event(
    event: NormalizedMarketEvent, knowledge_time: datetime
) -> ValueContext:
    return ValueContext.from_event(event, knowledge_time=knowledge_time)
