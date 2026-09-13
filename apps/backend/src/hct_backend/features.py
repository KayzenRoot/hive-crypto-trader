"""Deterministic, provider-neutral Module 8 feature contracts and evaluation.

This module consumes immutable S1E/S1F evidence and fixture values only.  It
does not open transports, persist state, create orders or grant authority.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from decimal import ROUND_HALF_EVEN, Decimal, InvalidOperation, localcontext
from enum import StrEnum
from typing import Any, Final, Self

from hct_backend.contracts import Environment, IdentityKind, StableId
from hct_backend.s1f_numeric import (
    DecimalValue,
    NumericFailureReason,
    NumericPolicyError,
)
from hct_backend.s1f_values import (
    CandleBar,
    Finality,
    Quantity,
    QuantityUnit,
    Timeframe,
)

FEATURE_ALGORITHM_VERSION: Final = "S2A_STANDARD_FEATURES_V1"
FEATURE_DECIMAL_POLICY_VERSION: Final = "FEATURE_DECIMAL_V1"
RECURSIVE_STATE_VERSION: Final = "S2A_ACCUMULATOR_STATE_V1"
DERIVED_MTF_PROVENANCE: Final = "DERIVED_ANALYTICAL_V1"
_SCALE_18 = Decimal("1e-18")
_HASH = re.compile(r"^[0-9a-f]{64}$")
_FEATURE_IDS = frozenset(
    {
        "F-RET-001",
        "F-SMA-001",
        "F-EMA-001",
        "F-ROC-001",
        "F-RSI-001",
        "F-TR-001",
        "F-ATR-001",
        "F-VSMA-001",
    }
)
_N_FEATURES = frozenset(
    {"F-SMA-001", "F-EMA-001", "F-ROC-001", "F-RSI-001", "F-ATR-001", "F-VSMA-001"}
)
_CLOSE_FEATURES = frozenset({"F-RET-001", "F-SMA-001", "F-EMA-001", "F-ROC-001", "F-RSI-001"})
_RECURSIVE_FEATURES = frozenset({"F-EMA-001", "F-ATR-001", "F-RSI-001"})


class FeatureError(ValueError):
    """Base failure for an invalid or contradictory feature contract."""


class FeatureRegistryError(FeatureError):
    """Raised when a registry operation would silently redefine behavior."""


class FeatureEvaluationError(FeatureError):
    """Raised only for malformed evaluator inputs, never for restrictive output states."""


class FeatureValidity(StrEnum):
    VALID = "VALID"
    UNKNOWN = "UNKNOWN"
    INVALID = "INVALID"
    WARMUP = "WARMUP"
    DEGRADED = "DEGRADED"


def _hash(material: object) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _require_hash(value: str, label: str) -> None:
    if not isinstance(value, str) or _HASH.fullmatch(value) is None:
        raise FeatureError(f"{label} must be a lowercase SHA-256 fingerprint")


def _utc(value: datetime, label: str) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise FeatureError(f"{label} must be timezone-aware")
    return value.astimezone(UTC)


def _enum_text(value: object) -> str:
    return str(getattr(value, "value", value))


def _canonical(value: Decimal) -> DecimalValue:
    if not value.is_finite():
        raise NumericPolicyError(NumericFailureReason.NON_FINITE, "finite Decimal required")
    with localcontext() as context:
        context.prec = 76
        context.rounding = ROUND_HALF_EVEN
        rounded = value.quantize(_SCALE_18, rounding=ROUND_HALF_EVEN)
    return DecimalValue.parse(rounded)


def _safe_canonical(value: Decimal) -> DecimalValue | None:
    try:
        return _canonical(value)
    except (InvalidOperation, NumericPolicyError, ValueError):
        return None


def _mean(values: Sequence[Decimal]) -> Decimal:
    if not values:
        raise FeatureEvaluationError("mean requires values")
    with localcontext() as context:
        context.prec = 76
        context.rounding = ROUND_HALF_EVEN
        return sum(values, Decimal(0)) / Decimal(len(values))


@dataclass(frozen=True, slots=True)
class FeatureDefinition:
    """Immutable behaviorally material feature definition."""

    canonical_id: str
    version: int
    semantic_family: str
    input_contract: str
    timeframe: Timeframe
    window: int | None
    output_type: str = "DecimalValue"
    validity_policy: str = "FAIL_CLOSED_V1"
    parameter_n: int | None = None
    source_field: str = "close"
    seed_rule: str = "NONE"
    algorithm_version: str = FEATURE_ALGORITHM_VERSION
    decimal_policy_version: str = FEATURE_DECIMAL_POLICY_VERSION
    rounding_mode: str = "ROUND_HALF_EVEN"

    def __post_init__(self) -> None:
        if self.canonical_id not in _FEATURE_IDS:
            raise FeatureError("feature ID is outside the exact S2A allowlist")
        if isinstance(self.version, bool) or not isinstance(self.version, int) or self.version < 1:
            raise FeatureError("feature version must be positive")
        if not isinstance(self.timeframe, Timeframe):
            raise FeatureError("feature timeframe is required")
        if not self.semantic_family or not self.input_contract:
            raise FeatureError("feature semantic and input contracts are required")
        if self.canonical_id in _N_FEATURES:
            if (
                isinstance(self.parameter_n, bool)
                or not isinstance(self.parameter_n, int)
                or self.parameter_n < 2
                or self.window != self.parameter_n
            ):
                raise FeatureError("N-based features require integer N >= 2 and matching window")
        elif self.parameter_n is not None or self.window is not None:
            raise FeatureError("non-N feature cannot carry a window parameter")
        if self.algorithm_version != FEATURE_ALGORITHM_VERSION:
            raise FeatureError("unsupported feature algorithm version")
        if self.decimal_policy_version != FEATURE_DECIMAL_POLICY_VERSION:
            raise FeatureError("unsupported Decimal policy")
        if self.rounding_mode != "ROUND_HALF_EVEN":
            raise FeatureError("unsupported rounding mode")

    @classmethod
    def standard(
        cls,
        canonical_id: str,
        *,
        parameter_n: int | None = None,
        timeframe: Timeframe | None = None,
        version: int = 1,
    ) -> Self:
        families = {
            "F-RET-001": ("return", "CLOSED_CLOSE", "NONE", "close"),
            "F-SMA-001": ("simple_moving_average", "CLOSED_CLOSE", "NONE", "close"),
            "F-EMA-001": ("exponential_moving_average", "CLOSED_CLOSE", "SMA_N", "close"),
            "F-ROC-001": ("rate_of_change", "CLOSED_CLOSE", "NONE", "close"),
            "F-RSI-001": (
                "relative_strength_index_wilder",
                "CLOSED_CLOSE",
                "MEAN_FIRST_N_DELTAS",
                "close",
            ),
            "F-TR-001": ("true_range", "CLOSED_OHLC", "HIGH_MINUS_LOW", "ohlc"),
            "F-ATR-001": ("average_true_range_wilder", "CLOSED_OHLC", "MEAN_FIRST_N_TR", "ohlc"),
            "F-VSMA-001": ("volume_sma", "CLOSED_NATIVE_QUANTITY", "NONE", "quantity"),
        }
        if canonical_id not in families:
            raise FeatureError("feature ID is outside the exact S2A allowlist")
        family, contract, seed, source = families[canonical_id]
        frame = timeframe or Timeframe("Min1", 60)
        n = parameter_n if canonical_id in _N_FEATURES else None
        return cls(
            canonical_id=canonical_id,
            version=version,
            semantic_family=family,
            input_contract=contract,
            timeframe=frame,
            window=n,
            parameter_n=n,
            source_field=source,
            seed_rule=seed,
        )

    @property
    def material(self) -> dict[str, object]:
        return {
            "canonical_id": self.canonical_id,
            "version": self.version,
            "semantic_family": self.semantic_family,
            "input_contract": self.input_contract,
            "timeframe": self.timeframe.fingerprint,
            "window": self.window,
            "output_type": self.output_type,
            "validity_policy": self.validity_policy,
            "parameter_n": self.parameter_n,
            "source_field": self.source_field,
            "seed_rule": self.seed_rule,
            "algorithm_version": self.algorithm_version,
            "decimal_policy_version": self.decimal_policy_version,
            "rounding_mode": self.rounding_mode,
        }

    @property
    def fingerprint(self) -> str:
        return _hash(self.material)


@dataclass(frozen=True, slots=True)
class FeatureVersion:
    """Versioned material contract; the fingerprint includes every behavior input."""

    definition: FeatureDefinition

    def __post_init__(self) -> None:
        if not isinstance(self.definition, FeatureDefinition):
            raise FeatureError("FeatureVersion requires a FeatureDefinition")

    @classmethod
    def standard(
        cls,
        canonical_id: str,
        *,
        parameter_n: int | None = None,
        timeframe: Timeframe | None = None,
        version: int = 1,
    ) -> Self:
        return cls(
            FeatureDefinition.standard(
                canonical_id,
                parameter_n=parameter_n,
                timeframe=timeframe,
                version=version,
            )
        )

    @property
    def canonical_id(self) -> str:
        return self.definition.canonical_id

    @property
    def version(self) -> int:
        return self.definition.version

    @property
    def parameter_n(self) -> int | None:
        return self.definition.parameter_n

    @property
    def timeframe(self) -> Timeframe:
        return self.definition.timeframe

    @property
    def fingerprint(self) -> str:
        return _hash({"feature_definition": self.definition.material})


@dataclass(frozen=True, slots=True)
class FeatureRegistry:
    """Persistent registry: every register operation returns a new registry."""

    versions: tuple[FeatureVersion, ...] = ()

    def register(self, feature: FeatureVersion) -> Self:
        if not isinstance(feature, FeatureVersion):
            raise FeatureRegistryError("FeatureVersion is required")
        for existing in self.versions:
            if existing.canonical_id != feature.canonical_id:
                continue
            if existing.version == feature.version:
                if existing.fingerprint != feature.fingerprint:
                    raise FeatureRegistryError("material version collision")
                return self
        return type(self)(
            tuple(
                sorted(
                    (*self.versions, feature), key=lambda item: (item.canonical_id, item.version)
                )
            )
        )

    def resolve(self, canonical_id: str, version: int | None = None) -> FeatureVersion:
        matches = [item for item in self.versions if item.canonical_id == canonical_id]
        if version is not None:
            matches = [item for item in matches if item.version == version]
        if len(matches) != 1:
            raise FeatureRegistryError("feature version is missing or ambiguous")
        return matches[0]


@dataclass(frozen=True, slots=True)
class FeatureSample:
    """A point-in-time, environment-scoped input evidence item."""

    value: DecimalValue | None
    fingerprint: str
    event_time: datetime
    knowledge_time: datetime
    wall_receive_time: datetime
    closed: bool
    source_id: StableId
    contract_id: StableId
    environment: Environment
    generation_fingerprint: str
    market_state_fingerprint: str
    provenance_fingerprint: str
    timeframe: Timeframe
    interval_start: datetime | None = None
    interval_end: datetime | None = None
    high: DecimalValue | None = None
    low: DecimalValue | None = None
    close: DecimalValue | None = None
    quantity: Quantity | None = None
    market_state_trust: str = "TRUSTED"
    upstream_fidelity: str = "TRUSTED"

    def __post_init__(self) -> None:
        _require_hash(self.fingerprint, "sample fingerprint")
        _require_hash(self.generation_fingerprint, "generation fingerprint")
        _require_hash(self.market_state_fingerprint, "market-state fingerprint")
        _require_hash(self.provenance_fingerprint, "provenance fingerprint")
        if self.value is not None and not isinstance(self.value, DecimalValue):
            raise FeatureError("sample value must be DecimalValue or absent")
        if (
            not isinstance(self.source_id, StableId)
            or self.source_id.kind is not IdentityKind.EXCHANGE
        ):
            raise FeatureError("sample source identity is invalid")
        if (
            not isinstance(self.contract_id, StableId)
            or self.contract_id.kind is not IdentityKind.INSTRUMENT
        ):
            raise FeatureError("sample contract identity is invalid")
        if not isinstance(self.environment, Environment) or not isinstance(
            self.timeframe, Timeframe
        ):
            raise FeatureError("sample identity metadata is invalid")
        if not isinstance(self.closed, bool):
            raise FeatureError("sample closed state is invalid")
        event = _utc(self.event_time, "sample event time")
        knowledge = _utc(self.knowledge_time, "sample knowledge time")
        wall = _utc(self.wall_receive_time, "sample wall receive time")
        if knowledge > wall:
            raise FeatureError("sample knowledge time cannot exceed wall receive time")
        object.__setattr__(self, "event_time", event)
        object.__setattr__(self, "knowledge_time", knowledge)
        object.__setattr__(self, "wall_receive_time", wall)
        for label, interval_value in (
            ("interval start", self.interval_start),
            ("interval end", self.interval_end),
        ):
            if interval_value is not None:
                object.__setattr__(self, label.replace(" ", "_"), _utc(interval_value, label))
        if self.interval_start is not None and self.interval_end is not None:
            if self.interval_end <= self.interval_start:
                raise FeatureError("sample interval must be positive")
        for label, numeric_value in (("high", self.high), ("low", self.low), ("close", self.close)):
            if numeric_value is not None and not isinstance(numeric_value, DecimalValue):
                raise FeatureError(f"sample {label} must be DecimalValue")
        if self.quantity is not None and (
            not isinstance(self.quantity, Quantity)
            or self.quantity.unit is not QuantityUnit.CONTRACTS_PROVIDER_NATIVE_V1
        ):
            raise FeatureError("sample quantity must use provider-native contracts")
        trust = _enum_text(self.market_state_trust)
        fidelity = _enum_text(self.upstream_fidelity)
        if trust not in {"TRUSTED", "DEGRADED", "UNKNOWN", "UNTRUSTED", "RESYNC_REQUIRED"}:
            raise FeatureError("unknown market-state trust")
        if fidelity not in {"TRUSTED", "RESOURCE_DEGRADED", "INELIGIBLE"}:
            raise FeatureError("unknown upstream fidelity")
        object.__setattr__(self, "market_state_trust", trust)
        object.__setattr__(self, "upstream_fidelity", fidelity)

    @classmethod
    def from_decimal(
        cls,
        value: DecimalValue | str | int | Decimal,
        *,
        index: int = 0,
        source_id: StableId | None = None,
        contract_id: StableId | None = None,
        environment: Environment = Environment.REPLAY,
        generation_fingerprint: str | None = None,
        market_state_fingerprint: str | None = None,
        provenance_fingerprint: str | None = None,
        event_time: datetime | None = None,
        knowledge_time: datetime | None = None,
        wall_receive_time: datetime | None = None,
        closed: bool = True,
        timeframe: Timeframe | None = None,
        upstream_fidelity: str = "TRUSTED",
    ) -> Self:
        parsed = value if isinstance(value, DecimalValue) else DecimalValue.parse(value)
        source = source_id or StableId(kind=IdentityKind.EXCHANGE, value="fixture")
        contract = contract_id or StableId(kind=IdentityKind.INSTRUMENT, value="fixture")
        frame = timeframe or Timeframe("Min1", 60)
        base = datetime(2020, 1, 1, tzinfo=UTC) + timedelta(seconds=index * frame.duration_seconds)
        event = event_time or base
        knowledge = knowledge_time or event
        wall = wall_receive_time or knowledge
        generation = generation_fingerprint or _hash(
            {"source": source.as_text(), "environment": environment.value, "generation": 1}
        )
        state = market_state_fingerprint or _hash(
            {
                "fixture": True,
                "source": source.as_text(),
                "contract": contract.as_text(),
                "index": index,
            }
        )
        provenance = provenance_fingerprint or _hash(
            {"fixture": True, "value": parsed.fingerprint, "index": index}
        )
        fingerprint = _hash(
            {
                "fixture": True,
                "value": parsed.fingerprint,
                "index": index,
                "event": event.isoformat(),
            }
        )
        return cls(
            value=parsed,
            fingerprint=fingerprint,
            event_time=event,
            knowledge_time=knowledge,
            wall_receive_time=wall,
            closed=closed,
            source_id=source,
            contract_id=contract,
            environment=environment,
            generation_fingerprint=generation,
            market_state_fingerprint=state,
            provenance_fingerprint=provenance,
            timeframe=frame,
            interval_start=event,
            interval_end=event + timedelta(seconds=frame.duration_seconds),
            close=parsed,
            upstream_fidelity=upstream_fidelity,
        )

    @classmethod
    def from_candle(cls, candle: CandleBar, *, upstream_fidelity: str = "TRUSTED") -> Self:
        if not isinstance(candle, CandleBar):
            raise FeatureError("CandleBar is required")
        return cls(
            value=candle.close,
            fingerprint=candle.fingerprint,
            event_time=candle.context.event_time,
            knowledge_time=candle.context.knowledge_time,
            wall_receive_time=candle.context.wall_receive_time,
            closed=candle.finality is Finality.CLOSED,
            source_id=candle.context.source_id,
            contract_id=candle.context.contract_id,
            environment=candle.context.environment,
            generation_fingerprint=candle.context.generation.fingerprint,
            market_state_fingerprint=candle.context.provenance_fingerprint,
            provenance_fingerprint=candle.context.provenance_fingerprint,
            timeframe=candle.timeframe,
            interval_start=candle.start,
            interval_end=candle.end,
            high=candle.high,
            low=candle.low,
            close=candle.close,
            quantity=candle.volume,
            upstream_fidelity=upstream_fidelity,
        )

    @property
    def content_fingerprint(self) -> str:
        return _hash(
            {
                "source_fingerprint": self.fingerprint,
                "value": self.value.fingerprint if self.value else None,
                "event_time": self.event_time.isoformat(),
                "knowledge_time": self.knowledge_time.isoformat(),
                "wall_receive_time": self.wall_receive_time.isoformat(),
                "closed": self.closed,
                "source": self.source_id.as_text(),
                "contract": self.contract_id.as_text(),
                "environment": self.environment.value,
                "generation": self.generation_fingerprint,
                "market_state": self.market_state_fingerprint,
                "provenance": self.provenance_fingerprint,
                "timeframe": self.timeframe.fingerprint,
                "interval_start": self.interval_start.isoformat() if self.interval_start else None,
                "interval_end": self.interval_end.isoformat() if self.interval_end else None,
                "high": self.high.fingerprint if self.high else None,
                "low": self.low.fingerprint if self.low else None,
                "close": self.close.fingerprint if self.close else None,
                "quantity": self.quantity.fingerprint if self.quantity else None,
                "trust": self.market_state_trust,
                "fidelity": self.upstream_fidelity,
            }
        )


@dataclass(frozen=True, slots=True)
class RecursiveAccumulatorState:
    """Serialized, canonical state for deterministic recursive replay."""

    feature_fingerprint: str
    algorithm_version: str
    parameter_n: int
    components: tuple[DecimalValue, ...]
    previous_input: DecimalValue | None
    previous_close: DecimalValue | None
    processed_samples: int
    lineage: tuple[str, ...]
    market_state_lineage: tuple[str, ...]
    source_generation_fingerprint: str
    environment: Environment
    event_time: datetime
    knowledge_time: datetime
    wall_receive_time: datetime
    window_start: datetime
    window_end: datetime

    def __post_init__(self) -> None:
        _require_hash(self.feature_fingerprint, "state feature fingerprint")
        if self.algorithm_version != RECURSIVE_STATE_VERSION:
            raise FeatureError("unsupported recursive state version")
        if isinstance(self.parameter_n, bool) or self.parameter_n < 2:
            raise FeatureError("state N is invalid")
        if not all(
            isinstance(value, DecimalValue) and value.material_scale == 18
            for value in self.components
        ):
            raise FeatureError("recursive components must be canonical scale 18")
        if self.previous_input is not None and self.previous_input.material_scale != 18:
            raise FeatureError("previous input must be canonical scale 18")
        if self.previous_close is not None and self.previous_close.material_scale != 18:
            raise FeatureError("previous close must be canonical scale 18")
        if isinstance(self.processed_samples, bool) or self.processed_samples < 1:
            raise FeatureError("state sample count is invalid")
        if not self.lineage or any(_HASH.fullmatch(item) is None for item in self.lineage):
            raise FeatureError("state lineage is invalid")
        if len(set(self.lineage)) != len(self.lineage):
            raise FeatureError("state lineage must be ordered and unique")
        if not self.market_state_lineage or any(
            _HASH.fullmatch(item) is None for item in self.market_state_lineage
        ):
            raise FeatureError("state market-state lineage is invalid")
        if len(self.market_state_lineage) != len(self.lineage):
            raise FeatureError("state lineage and market-state lineage lengths differ")
        _require_hash(self.source_generation_fingerprint, "state generation")
        if not isinstance(self.environment, Environment):
            raise FeatureError("state environment is invalid")
        event = _utc(self.event_time, "state event time")
        knowledge = _utc(self.knowledge_time, "state knowledge time")
        wall = _utc(self.wall_receive_time, "state wall time")
        start = _utc(self.window_start, "state window start")
        end = _utc(self.window_end, "state window end")
        if knowledge > wall or end < start:
            raise FeatureError("state temporal bounds are invalid")
        object.__setattr__(self, "event_time", event)
        object.__setattr__(self, "knowledge_time", knowledge)
        object.__setattr__(self, "wall_receive_time", wall)
        object.__setattr__(self, "window_start", start)
        object.__setattr__(self, "window_end", end)

    @property
    def fingerprint(self) -> str:
        return _hash(self.to_dict(include_fingerprint=False))

    def to_dict(self, *, include_fingerprint: bool = True) -> dict[str, Any]:
        material: dict[str, Any] = {
            "feature_fingerprint": self.feature_fingerprint,
            "algorithm_version": self.algorithm_version,
            "parameter_n": self.parameter_n,
            "components": [value.canonical_text for value in self.components],
            "component_scales": [value.material_scale for value in self.components],
            "previous_input": self.previous_input.canonical_text if self.previous_input else None,
            "previous_close": self.previous_close.canonical_text if self.previous_close else None,
            "processed_samples": self.processed_samples,
            "lineage": self.lineage,
            "market_state_lineage": self.market_state_lineage,
            "source_generation_fingerprint": self.source_generation_fingerprint,
            "environment": self.environment.value,
            "event_time": self.event_time.isoformat(),
            "knowledge_time": self.knowledge_time.isoformat(),
            "wall_receive_time": self.wall_receive_time.isoformat(),
            "window_start": self.window_start.isoformat(),
            "window_end": self.window_end.isoformat(),
        }
        if include_fingerprint:
            material["state_fingerprint"] = self.fingerprint
        return material

    def serialize(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))

    @classmethod
    def deserialize(cls, raw: str | Mapping[str, Any]) -> Self:
        payload = json.loads(raw) if isinstance(raw, str) else dict(raw)
        with localcontext() as context:
            context.prec = 76
            context.rounding = ROUND_HALF_EVEN
            components = tuple(
                DecimalValue.parse(Decimal(text).quantize(_SCALE_18, rounding=ROUND_HALF_EVEN))
                for text in payload["components"]
            )
            previous_input = (
                DecimalValue.parse(
                    Decimal(payload["previous_input"]).quantize(_SCALE_18, rounding=ROUND_HALF_EVEN)
                )
                if payload.get("previous_input") is not None
                else None
            )
            previous_close = (
                DecimalValue.parse(
                    Decimal(payload["previous_close"]).quantize(_SCALE_18, rounding=ROUND_HALF_EVEN)
                )
                if payload.get("previous_close") is not None
                else None
            )
        state = cls(
            feature_fingerprint=payload["feature_fingerprint"],
            algorithm_version=payload["algorithm_version"],
            parameter_n=payload["parameter_n"],
            components=components,
            previous_input=previous_input,
            previous_close=previous_close,
            processed_samples=payload["processed_samples"],
            lineage=tuple(payload["lineage"]),
            market_state_lineage=tuple(payload["market_state_lineage"]),
            source_generation_fingerprint=payload["source_generation_fingerprint"],
            environment=Environment(payload["environment"]),
            event_time=datetime.fromisoformat(payload["event_time"]),
            knowledge_time=datetime.fromisoformat(payload["knowledge_time"]),
            wall_receive_time=datetime.fromisoformat(payload["wall_receive_time"]),
            window_start=datetime.fromisoformat(payload["window_start"]),
            window_end=datetime.fromisoformat(payload["window_end"]),
        )
        if payload.get("state_fingerprint") != state.fingerprint:
            raise FeatureError("recursive state fingerprint mismatch")
        return state


@dataclass(frozen=True, slots=True)
class FeatureValue:
    """Immutable output bound to definition, point-in-time context and ordered lineage."""

    feature: FeatureVersion
    value: DecimalValue | None
    validity: FeatureValidity
    reason: str
    source_market_state_fingerprint: str
    source_generation_fingerprint: str
    source_id: StableId
    contract_id: StableId
    environment: Environment
    timeframe: Timeframe
    event_time: datetime
    knowledge_time: datetime
    wall_receive_time: datetime
    window_start: datetime
    window_end: datetime
    sample_count: int
    required_sample_count: int
    lineage: tuple[str, ...]
    upstream_fidelity: str
    recursive_state: RecursiveAccumulatorState | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.feature, FeatureVersion) or not isinstance(
            self.validity, FeatureValidity
        ):
            raise FeatureError("feature output identity is invalid")
        if not self.reason or self.sample_count < 0 or self.required_sample_count < 1:
            raise FeatureError("feature output metadata is invalid")
        if self.validity in {FeatureValidity.VALID, FeatureValidity.DEGRADED}:
            if not isinstance(self.value, DecimalValue):
                raise FeatureError("valid feature output requires a value")
        elif self.value is not None:
            raise FeatureError("restrictive feature output cannot carry a value")
        _require_hash(self.source_market_state_fingerprint, "feature market-state fingerprint")
        _require_hash(self.source_generation_fingerprint, "feature generation fingerprint")
        if (
            not isinstance(self.source_id, StableId)
            or self.source_id.kind is not IdentityKind.EXCHANGE
            or not isinstance(self.contract_id, StableId)
            or self.contract_id.kind is not IdentityKind.INSTRUMENT
        ):
            raise FeatureError("feature source identities are required")
        if not isinstance(self.environment, Environment) or not isinstance(
            self.timeframe, Timeframe
        ):
            raise FeatureError("feature environment/timeframe is invalid")
        object.__setattr__(self, "event_time", _utc(self.event_time, "feature event time"))
        object.__setattr__(
            self, "knowledge_time", _utc(self.knowledge_time, "feature knowledge time")
        )
        object.__setattr__(
            self, "wall_receive_time", _utc(self.wall_receive_time, "feature wall time")
        )
        object.__setattr__(self, "window_start", _utc(self.window_start, "feature window start"))
        object.__setattr__(self, "window_end", _utc(self.window_end, "feature window end"))
        if self.window_end < self.window_start or self.knowledge_time > self.wall_receive_time:
            raise FeatureError("feature temporal bounds are invalid")
        if not self.lineage or len(set(self.lineage)) != len(self.lineage):
            raise FeatureError("feature lineage is missing or duplicated")
        for item in self.lineage:
            _require_hash(item, "feature lineage entry")
        fidelity = _enum_text(self.upstream_fidelity)
        if fidelity not in {"TRUSTED", "RESOURCE_DEGRADED", "INELIGIBLE"}:
            raise FeatureError("feature fidelity is invalid")
        object.__setattr__(self, "upstream_fidelity", fidelity)
        if (
            isinstance(self.sample_count, bool)
            or not isinstance(self.sample_count, int)
            or self.sample_count < 0
            or isinstance(self.required_sample_count, bool)
            or not isinstance(self.required_sample_count, int)
            or self.required_sample_count < 1
        ):
            raise FeatureError("feature sample cardinality is invalid")

    @property
    def lineage_manifest_fingerprint(self) -> str:
        return _hash({"ordered": self.lineage})

    @property
    def fingerprint(self) -> str:
        return _hash(
            {
                "feature": self.feature.fingerprint,
                "value": self.value.fingerprint if self.value else None,
                "validity": self.validity.value,
                "reason": self.reason,
                "market_state": self.source_market_state_fingerprint,
                "generation": self.source_generation_fingerprint,
                "source": self.source_id.as_text(),
                "contract": self.contract_id.as_text(),
                "environment": self.environment.value,
                "timeframe": self.timeframe.fingerprint,
                "event_time": self.event_time.isoformat(),
                "knowledge_time": self.knowledge_time.isoformat(),
                "wall_receive_time": self.wall_receive_time.isoformat(),
                "window_start": self.window_start.isoformat(),
                "window_end": self.window_end.isoformat(),
                "sample_count": self.sample_count,
                "required_sample_count": self.required_sample_count,
                "lineage": self.lineage_manifest_fingerprint,
                "fidelity": self.upstream_fidelity,
                "recursive_state": self.recursive_state.fingerprint
                if self.recursive_state
                else None,
            }
        )


@dataclass(frozen=True, slots=True)
class FeatureSnapshot:
    """Immutable collection of feature outputs for one source point-in-time."""

    values: tuple[FeatureValue, ...]
    source_market_state_fingerprint: str
    source_generation_fingerprint: str
    environment: Environment
    evaluation_time: datetime

    def __post_init__(self) -> None:
        if not self.values or len({value.feature.canonical_id for value in self.values}) != len(
            self.values
        ):
            raise FeatureError("snapshot feature IDs must be unique and non-empty")
        _require_hash(self.source_market_state_fingerprint, "snapshot market state")
        _require_hash(self.source_generation_fingerprint, "snapshot generation")
        if any(
            value.source_market_state_fingerprint != self.source_market_state_fingerprint
            or value.source_generation_fingerprint != self.source_generation_fingerprint
            or value.environment is not self.environment
            for value in self.values
        ):
            raise FeatureError("snapshot values do not share one source identity")
        object.__setattr__(
            self, "evaluation_time", _utc(self.evaluation_time, "snapshot evaluation time")
        )

    @property
    def fingerprint(self) -> str:
        return _hash(
            {
                "values": tuple(value.fingerprint for value in self.values),
                "market_state": self.source_market_state_fingerprint,
                "generation": self.source_generation_fingerprint,
                "environment": self.environment.value,
                "evaluation_time": self.evaluation_time.isoformat(),
            }
        )


def _required_count(feature: FeatureVersion) -> int:
    if feature.canonical_id == "F-RET-001" or feature.canonical_id == "F-TR-001":
        return 2 if feature.canonical_id == "F-RET-001" else 1
    assert feature.parameter_n is not None
    if feature.canonical_id in {"F-ROC-001", "F-RSI-001"}:
        return feature.parameter_n + 1
    return feature.parameter_n


def _coerce_samples(
    samples: Iterable[FeatureSample | CandleBar | DecimalValue | str | int | Decimal],
) -> tuple[FeatureSample, ...]:
    result: list[FeatureSample] = []
    for index, sample in enumerate(samples):
        if isinstance(sample, FeatureSample):
            result.append(sample)
        elif isinstance(sample, CandleBar):
            result.append(FeatureSample.from_candle(sample))
        else:
            result.append(FeatureSample.from_decimal(sample, index=index))
    return tuple(result)


def _context_status(
    samples: Sequence[FeatureSample], evaluation_time: datetime | None
) -> tuple[FeatureValidity | None, str, str]:
    if not samples:
        return FeatureValidity.WARMUP, "NO_INPUT_SAMPLES", "TRUSTED"
    first = samples[0]
    for sample in samples:
        if (
            sample.source_id != first.source_id
            or sample.contract_id != first.contract_id
            or sample.environment is not first.environment
            or sample.generation_fingerprint != first.generation_fingerprint
            or sample.timeframe.fingerprint != first.timeframe.fingerprint
        ):
            return (
                FeatureValidity.INVALID,
                "MIXED_SOURCE_CONTRACT_ENVIRONMENT_GENERATION_OR_TIMEFRAME",
                first.upstream_fidelity,
            )
    for previous, current in zip(samples[:-1], samples[1:], strict=False):
        previous_start = previous.interval_start or previous.event_time
        current_start = current.interval_start or current.event_time
        if current_start <= previous_start or current.event_time <= previous.event_time:
            return (
                FeatureValidity.INVALID,
                "NON_MONOTONIC_OR_DUPLICATE_SAMPLE_ORDER",
                first.upstream_fidelity,
            )
    if evaluation_time is not None:
        boundary = _utc(evaluation_time, "evaluation time")
        if any(
            sample.event_time > boundary or sample.knowledge_time > boundary for sample in samples
        ):
            return (
                FeatureValidity.INVALID,
                "FUTURE_EVENT_OR_KNOWLEDGE_EVIDENCE",
                first.upstream_fidelity,
            )
    if any(
        sample.market_state_trust in {"UNKNOWN", "UNTRUSTED", "RESYNC_REQUIRED"}
        for sample in samples
    ):
        return FeatureValidity.UNKNOWN, "UPSTREAM_MARKET_STATE_UNTRUSTED", first.upstream_fidelity
    if any(not sample.closed for sample in samples):
        return FeatureValidity.WARMUP, "CLOSED_INPUT_REQUIRED", first.upstream_fidelity
    if any(
        sample.market_state_trust == "DEGRADED" or sample.upstream_fidelity == "RESOURCE_DEGRADED"
        for sample in samples
    ):
        return FeatureValidity.DEGRADED, "UPSTREAM_FIDELITY_DEGRADED", "RESOURCE_DEGRADED"
    return None, "", first.upstream_fidelity


def _feature_values(samples: Sequence[FeatureSample], feature: FeatureVersion) -> list[Decimal]:
    if feature.canonical_id in _CLOSE_FEATURES:
        values = [sample.value for sample in samples]
    elif feature.canonical_id in {"F-TR-001", "F-ATR-001"}:
        values = [sample.high for sample in samples]
    elif feature.canonical_id == "F-VSMA-001":
        quantities = [sample.quantity for sample in samples]
        if any(not isinstance(quantity, Quantity) for quantity in quantities):
            raise FeatureEvaluationError("volume SMA requires native quantity inputs")
        first = quantities[0]
        assert first is not None
        if any(
            quantity is None
            or quantity.unit is not first.unit
            or quantity.source_contract_identity_version != first.source_contract_identity_version
            for quantity in quantities
        ):
            raise FeatureEvaluationError("volume SMA quantity contract is inconsistent")
        return [quantity.value.value for quantity in quantities if quantity is not None]
    else:
        values = [sample.value for sample in samples]
    if any(not isinstance(value, DecimalValue) for value in values):
        raise FeatureEvaluationError("feature input field is missing")
    return [value.value for value in values if isinstance(value, DecimalValue)]


def _true_range(samples: Sequence[FeatureSample], index: int) -> Decimal:
    sample = samples[index]
    if not all(
        isinstance(value, DecimalValue) for value in (sample.high, sample.low, sample.close)
    ):
        raise FeatureEvaluationError("true range requires OHLC inputs")
    assert sample.high is not None and sample.low is not None and sample.close is not None
    if index == 0:
        return sample.high.value - sample.low.value
    previous = samples[index - 1].close
    if not isinstance(previous, DecimalValue):
        raise FeatureEvaluationError("true range requires previous close")
    return max(
        sample.high.value - sample.low.value,
        abs(sample.high.value - previous.value),
        abs(sample.low.value - previous.value),
    )


def _state_for(
    feature: FeatureVersion,
    components: tuple[DecimalValue, ...],
    sample: FeatureSample,
    samples: Sequence[FeatureSample],
    lineage: tuple[str, ...],
    previous_state: RecursiveAccumulatorState | None = None,
) -> RecursiveAccumulatorState:
    new_samples = samples[-1:] if previous_state is not None else samples
    previous = sample.value
    previous_close = sample.close
    if previous is not None:
        previous = _canonical(previous.value)
    if previous_close is not None:
        previous_close = _canonical(previous_close.value)
    canonical_components = tuple(_canonical(item.value) for item in components)
    prior_market_states = previous_state.market_state_lineage if previous_state else ()
    prior_event = previous_state.event_time if previous_state else sample.event_time
    prior_knowledge = previous_state.knowledge_time if previous_state else sample.knowledge_time
    prior_wall = previous_state.wall_receive_time if previous_state else sample.wall_receive_time
    prior_start = (
        previous_state.window_start
        if previous_state
        else (sample.interval_start or sample.event_time)
    )
    prior_end = (
        previous_state.window_end if previous_state else (sample.interval_end or sample.event_time)
    )
    return RecursiveAccumulatorState(
        feature_fingerprint=feature.fingerprint,
        algorithm_version=RECURSIVE_STATE_VERSION,
        parameter_n=feature.parameter_n or 2,
        components=canonical_components,
        previous_input=previous,
        previous_close=previous_close,
        processed_samples=(previous_state.processed_samples if previous_state else 0)
        + len(new_samples),
        lineage=lineage,
        market_state_lineage=prior_market_states
        + tuple(item.market_state_fingerprint for item in new_samples),
        source_generation_fingerprint=sample.generation_fingerprint,
        environment=sample.environment,
        event_time=max(prior_event, *(item.event_time for item in new_samples)),
        knowledge_time=max(prior_knowledge, *(item.knowledge_time for item in new_samples)),
        wall_receive_time=max(prior_wall, *(item.wall_receive_time for item in new_samples)),
        window_start=min(
            prior_start, *(item.interval_start or item.event_time for item in new_samples)
        ),
        window_end=max(prior_end, *(item.interval_end or item.event_time for item in new_samples)),
    )


def _build_output(
    feature: FeatureVersion,
    samples: Sequence[FeatureSample],
    value: DecimalValue | None,
    validity: FeatureValidity,
    reason: str,
    lineage: tuple[str, ...],
    recursive_state: RecursiveAccumulatorState | None = None,
    upstream_fidelity: str | None = None,
    previous_state: RecursiveAccumulatorState | None = None,
) -> FeatureValue:
    first = samples[0]
    if recursive_state is not None:
        source_market_state = _hash({"ordered": recursive_state.market_state_lineage})
        event_time = recursive_state.event_time
        knowledge_time = recursive_state.knowledge_time
        wall_receive_time = recursive_state.wall_receive_time
        window_start = recursive_state.window_start
        window_end = recursive_state.window_end
        sample_count = recursive_state.processed_samples
    elif previous_state is not None:
        source_market_state = _hash(
            {
                "ordered": previous_state.market_state_lineage
                + tuple(item.market_state_fingerprint for item in samples)
            }
        )
        event_time = max(previous_state.event_time, *(item.event_time for item in samples))
        knowledge_time = max(
            previous_state.knowledge_time, *(item.knowledge_time for item in samples)
        )
        wall_receive_time = max(
            previous_state.wall_receive_time, *(item.wall_receive_time for item in samples)
        )
        window_start = min(
            previous_state.window_start,
            *(item.interval_start or item.event_time for item in samples),
        )
        window_end = max(
            previous_state.window_end, *(item.interval_end or item.event_time for item in samples)
        )
        sample_count = previous_state.processed_samples + len(samples)
    else:
        source_market_state = _hash(
            {"ordered": tuple(item.market_state_fingerprint for item in samples)}
        )
        event_time = max(item.event_time for item in samples)
        knowledge_time = max(item.knowledge_time for item in samples)
        wall_receive_time = max(item.wall_receive_time for item in samples)
        window_start = min(item.interval_start or item.event_time for item in samples)
        window_end = max(item.interval_end or item.event_time for item in samples)
        sample_count = len(lineage)
    return FeatureValue(
        feature=feature,
        value=value if validity in {FeatureValidity.VALID, FeatureValidity.DEGRADED} else None,
        validity=validity,
        reason=reason,
        source_market_state_fingerprint=source_market_state,
        source_generation_fingerprint=first.generation_fingerprint,
        source_id=first.source_id,
        contract_id=first.contract_id,
        environment=first.environment,
        timeframe=first.timeframe,
        event_time=event_time,
        knowledge_time=knowledge_time,
        wall_receive_time=wall_receive_time,
        window_start=window_start,
        window_end=window_end,
        sample_count=sample_count,
        required_sample_count=_required_count(feature),
        lineage=lineage,
        upstream_fidelity=upstream_fidelity or first.upstream_fidelity,
        recursive_state=recursive_state,
    )


def _compute_numeric(
    feature: FeatureVersion,
    samples: Sequence[FeatureSample],
    previous_state: RecursiveAccumulatorState | None,
) -> tuple[Decimal | None, str, tuple[DecimalValue, ...]]:
    identifier = feature.canonical_id
    n = feature.parameter_n
    values = (
        _feature_values(samples, feature) if identifier not in {"F-TR-001", "F-ATR-001"} else []
    )
    if identifier == "F-RET-001":
        denominator = values[-2]
        if denominator == 0:
            return None, "ZERO_DENOMINATOR", ()
        return values[-1] / denominator - 1, "COMPUTED", ()
    if identifier == "F-SMA-001":
        assert n is not None
        return _mean(values[-n:]), "COMPUTED", ()
    if identifier == "F-ROC-001":
        assert n is not None
        denominator = values[-n - 1]
        if denominator == 0:
            return None, "ZERO_DENOMINATOR", ()
        return (values[-1] - denominator) / denominator, "COMPUTED", ()
    if identifier == "F-RSI-001":
        assert n is not None
        if previous_state is not None and previous_state.components:
            previous_gain, previous_loss = (item.value for item in previous_state.components)
            if previous_state.previous_input is None:
                raise FeatureEvaluationError("RSI resume state lacks previous input")
            delta = values[-1] - previous_state.previous_input.value
            gain = max(delta, Decimal(0))
            loss = max(-delta, Decimal(0))
            with localcontext() as context:
                context.prec = 76
                avg_gain = ((previous_gain * (n - 1)) + gain) / n
                avg_loss = ((previous_loss * (n - 1)) + loss) / n
        else:
            deltas = [right - left for left, right in zip(values[:-1], values[1:], strict=False)]
            avg_gain = _mean([max(delta, Decimal(0)) for delta in deltas[-n:]])
            avg_loss = _mean([max(-delta, Decimal(0)) for delta in deltas[-n:]])
        if avg_gain == 0 and avg_loss == 0:
            return Decimal(50), "COMPUTED", (_canonical(avg_gain), _canonical(avg_loss))
        if avg_loss == 0:
            return Decimal(100), "COMPUTED", (_canonical(avg_gain), _canonical(avg_loss))
        if avg_gain == 0:
            return Decimal(0), "COMPUTED", (_canonical(avg_gain), _canonical(avg_loss))
        with localcontext() as context:
            context.prec = 76
            rs = avg_gain / avg_loss
            return (
                Decimal(100) - (Decimal(100) / (Decimal(1) + rs)),
                "COMPUTED",
                (
                    _canonical(avg_gain),
                    _canonical(avg_loss),
                ),
            )
    if identifier == "F-VSMA-001":
        assert n is not None
        return _mean(values[-n:]), "COMPUTED", ()
    if identifier == "F-TR-001":
        return _true_range(samples, len(samples) - 1), "COMPUTED", ()
    if identifier == "F-ATR-001":
        assert n is not None
        if previous_state is not None and previous_state.components:
            previous_atr = previous_state.components[0].value
            current_sample = samples[-1]
            if not all(
                isinstance(value, DecimalValue)
                for value in (current_sample.high, current_sample.low)
            ):
                raise FeatureEvaluationError("ATR resume input lacks OHLC")
            assert current_sample.high is not None and current_sample.low is not None
            previous_close = previous_state.previous_close
            if previous_close is None:
                raise FeatureEvaluationError("ATR resume state lacks previous close")
            current_tr = max(
                current_sample.high.value - current_sample.low.value,
                abs(current_sample.high.value - previous_close.value),
                abs(current_sample.low.value - previous_close.value),
            )
            with localcontext() as context:
                context.prec = 76
                current = ((previous_atr * (n - 1)) + current_tr) / n
            return current, "COMPUTED", (_canonical(current),)
        tr_values = [_true_range(samples, index) for index in range(len(samples))]
        return _mean(tr_values[-n:]), "COMPUTED", ()
    if identifier == "F-EMA-001":
        assert n is not None
        if previous_state is not None and previous_state.components:
            previous_ema = previous_state.components[0].value
            with localcontext() as context:
                context.prec = 76
                alpha = Decimal(2) / Decimal(n + 1)
                current = alpha * values[-1] + (Decimal(1) - alpha) * previous_ema
            return current, "COMPUTED", (_canonical(current),)
        current = _mean(values[-n:])
        return current, "COMPUTED", (_canonical(current),)
    raise FeatureEvaluationError("unsupported feature ID")


def evaluate_feature_series(
    feature: FeatureVersion,
    samples: Iterable[FeatureSample | CandleBar | DecimalValue | str | int | Decimal],
    *,
    evaluation_time: datetime | None = None,
    initial_state: RecursiveAccumulatorState | None = None,
) -> tuple[FeatureValue, ...]:
    """Evaluate one feature at every observed sample, preserving deterministic state."""

    if not isinstance(feature, FeatureVersion):
        raise FeatureEvaluationError("FeatureVersion is required")
    values = _coerce_samples(samples)
    if not values:
        return ()
    if initial_state is not None and initial_state.feature_fingerprint != feature.fingerprint:
        raise FeatureEvaluationError("resume state belongs to another feature version")
    outputs: list[FeatureValue] = []
    state = initial_state
    prior_lineage = initial_state.lineage if initial_state is not None else ()
    prior_count = initial_state.processed_samples if initial_state is not None else 0
    for index in range(len(values)):
        prefix = values[: index + 1]
        context_status, context_reason, fidelity = _context_status(prefix, evaluation_time)
        lineage = prior_lineage + tuple(item.content_fingerprint for item in prefix)
        total_count = prior_count + index + 1
        required = _required_count(feature)
        if context_status is not None and context_status is not FeatureValidity.DEGRADED:
            outputs.append(
                _build_output(
                    feature,
                    prefix,
                    None,
                    context_status,
                    context_reason,
                    lineage,
                    upstream_fidelity=fidelity,
                )
            )
            continue
        if total_count < required:
            outputs.append(
                _build_output(
                    feature,
                    prefix,
                    None,
                    FeatureValidity.WARMUP,
                    "INSUFFICIENT_REQUIRED_SAMPLES",
                    lineage,
                    upstream_fidelity=fidelity,
                )
            )
            continue
        try:
            numeric, reason, components = _compute_numeric(feature, prefix, state)
        except (FeatureEvaluationError, NumericPolicyError, InvalidOperation, ValueError) as exc:
            outputs.append(
                _build_output(
                    feature,
                    prefix,
                    None,
                    FeatureValidity.INVALID,
                    str(exc),
                    lineage,
                    upstream_fidelity=fidelity,
                )
            )
            continue
        if numeric is None:
            outputs.append(
                _build_output(
                    feature,
                    prefix,
                    None,
                    FeatureValidity.INVALID,
                    reason,
                    lineage,
                    upstream_fidelity=fidelity,
                )
            )
            continue
        output = _safe_canonical(numeric)
        if output is None:
            outputs.append(
                _build_output(
                    feature,
                    prefix,
                    None,
                    FeatureValidity.INVALID,
                    "CANONICAL_DECIMAL_OVERFLOW",
                    lineage,
                    upstream_fidelity=fidelity,
                )
            )
            continue
        previous_state = state
        state = None
        if feature.canonical_id in _RECURSIVE_FEATURES:
            state_components = components
            if not state_components:
                state_components = (_canonical(numeric),)
            state = _state_for(
                feature, state_components, prefix[-1], prefix, lineage, previous_state
            )
        validity = (
            FeatureValidity.DEGRADED if fidelity == "RESOURCE_DEGRADED" else FeatureValidity.VALID
        )
        outputs.append(
            _build_output(feature, prefix, output, validity, reason, lineage, state, fidelity)
        )
    return tuple(outputs)


def _recursive_latest(
    feature: FeatureVersion,
    inputs: Sequence[FeatureSample],
    initial_state: RecursiveAccumulatorState | None,
    lineage: tuple[str, ...],
) -> tuple[DecimalValue, RecursiveAccumulatorState]:
    """Replay recursive values without materializing one output per prefix."""

    n = feature.parameter_n
    assert n is not None
    has_state = initial_state is not None and bool(initial_state.components)
    prior_count = initial_state.processed_samples if initial_state is not None else 0
    prior_market = initial_state.market_state_lineage if initial_state is not None else ()
    source_generation = inputs[0].generation_fingerprint
    environment = inputs[0].environment
    input_market_states = tuple(item.market_state_fingerprint for item in inputs)
    previous_close_value = (
        initial_state.previous_close.value
        if initial_state is not None
        and initial_state.components
        and initial_state.previous_close is not None
        else None
    )
    previous_input_value = (
        initial_state.previous_input.value
        if initial_state is not None
        and initial_state.components
        and initial_state.previous_input is not None
        else None
    )
    previous_input: DecimalValue | None = None
    previous_close: DecimalValue | None = None
    components: tuple[DecimalValue, ...]

    def true_range(sample: FeatureSample, prior: Decimal | None) -> Decimal:
        if not all(
            isinstance(value, DecimalValue) for value in (sample.high, sample.low, sample.close)
        ):
            raise FeatureEvaluationError("true range requires OHLC inputs")
        assert sample.high is not None and sample.low is not None and sample.close is not None
        if prior is None:
            return sample.high.value - sample.low.value
        return max(
            sample.high.value - sample.low.value,
            abs(sample.high.value - prior),
            abs(sample.low.value - prior),
        )

    if feature.canonical_id == "F-EMA-001":
        values = _feature_values(inputs, feature)
        if has_state and initial_state is not None:
            current = initial_state.components[0].value
            start = 0
        else:
            current = _mean(values[:n])
            start = n
        with localcontext() as context:
            context.prec = 76
            context.rounding = ROUND_HALF_EVEN
            alpha = Decimal(2) / Decimal(n + 1)
            for value in values[start:]:
                current = alpha * value + (Decimal(1) - alpha) * current
        components = (_canonical(current),)
        previous_input = _canonical(values[-1])
        output = components[0]
    elif feature.canonical_id == "F-RSI-001":
        values = _feature_values(inputs, feature)
        if has_state and initial_state is not None:
            avg_gain = initial_state.components[0].value
            avg_loss = initial_state.components[1].value
            previous = previous_input_value
            start = 0
        else:
            deltas = [right - left for left, right in zip(values[:-1], values[1:], strict=False)]
            avg_gain = _mean([max(delta, Decimal(0)) for delta in deltas[:n]])
            avg_loss = _mean([max(-delta, Decimal(0)) for delta in deltas[:n]])
            previous = values[n]
            start = n + 1
        with localcontext() as context:
            context.prec = 76
            context.rounding = ROUND_HALF_EVEN
            for value in values[start:]:
                assert previous is not None
                delta = value - previous
                gain = max(delta, Decimal(0))
                loss = max(-delta, Decimal(0))
                avg_gain = _canonical(((avg_gain * (n - 1)) + gain) / n).value
                avg_loss = _canonical(((avg_loss * (n - 1)) + loss) / n).value
                previous = value
        if avg_gain == 0 and avg_loss == 0:
            output = _canonical(Decimal(50))
        elif avg_loss == 0:
            output = _canonical(Decimal(100))
        elif avg_gain == 0:
            output = _canonical(Decimal(0))
        else:
            with localcontext() as context:
                context.prec = 76
                output = _canonical(
                    Decimal(100) - (Decimal(100) / (Decimal(1) + avg_gain / avg_loss))
                )
        components = (_canonical(avg_gain), _canonical(avg_loss))
        previous_input = _canonical(values[-1])
    else:
        tr_values: list[Decimal] = []
        prior = previous_close_value
        for sample in inputs:
            current_tr = true_range(sample, prior)
            tr_values.append(current_tr)
            prior = sample.close.value if sample.close is not None else None
        if has_state and initial_state is not None:
            current = initial_state.components[0].value
            start = 0
        else:
            current = _mean(tr_values[:n])
            start = n
        with localcontext() as context:
            context.prec = 76
            context.rounding = ROUND_HALF_EVEN
            for current_tr in tr_values[start:]:
                current = ((current * (n - 1)) + current_tr) / n
        components = (_canonical(current),)
        previous_close = _canonical(inputs[-1].close.value) if inputs[-1].close else None
        if previous_close is None:
            raise FeatureEvaluationError("ATR resume input lacks previous close")
        output = components[0]

    first = inputs[0]
    prior_event = initial_state.event_time if initial_state is not None else first.event_time
    prior_knowledge = (
        initial_state.knowledge_time if initial_state is not None else first.knowledge_time
    )
    prior_wall = (
        initial_state.wall_receive_time if initial_state is not None else first.wall_receive_time
    )
    prior_start = (
        initial_state.window_start
        if initial_state is not None
        else (first.interval_start or first.event_time)
    )
    prior_end = (
        initial_state.window_end
        if initial_state is not None
        else (first.interval_end or first.event_time)
    )
    state = RecursiveAccumulatorState(
        feature_fingerprint=feature.fingerprint,
        algorithm_version=RECURSIVE_STATE_VERSION,
        parameter_n=n,
        components=components,
        previous_input=previous_input,
        previous_close=previous_close,
        processed_samples=prior_count + len(inputs),
        lineage=lineage,
        market_state_lineage=prior_market + input_market_states,
        source_generation_fingerprint=source_generation,
        environment=environment,
        event_time=max(prior_event, *(item.event_time for item in inputs)),
        knowledge_time=max(prior_knowledge, *(item.knowledge_time for item in inputs)),
        wall_receive_time=max(prior_wall, *(item.wall_receive_time for item in inputs)),
        window_start=min(prior_start, *(item.interval_start or item.event_time for item in inputs)),
        window_end=max(prior_end, *(item.interval_end or item.event_time for item in inputs)),
    )
    return output, state


def evaluate_feature(
    feature: FeatureVersion,
    samples: Iterable[FeatureSample | CandleBar | DecimalValue | str | int | Decimal],
    *,
    evaluation_time: datetime | None = None,
    initial_state: RecursiveAccumulatorState | None = None,
) -> FeatureValue:
    """Evaluate one feature and return the latest point-in-time result."""

    if not isinstance(feature, FeatureVersion):
        raise FeatureEvaluationError("FeatureVersion is required")
    inputs = _coerce_samples(samples)
    if not inputs:
        raise FeatureEvaluationError("at least one sample is required")
    if initial_state is not None and initial_state.feature_fingerprint != feature.fingerprint:
        raise FeatureEvaluationError("resume state belongs to another feature version")
    context_status, context_reason, fidelity = _context_status(inputs, evaluation_time)
    prior_lineage = initial_state.lineage if initial_state is not None else ()
    lineage = prior_lineage + tuple(item.content_fingerprint for item in inputs)
    prior_count = initial_state.processed_samples if initial_state is not None else 0
    required = _required_count(feature)
    if context_status is not None and context_status is not FeatureValidity.DEGRADED:
        return _build_output(
            feature,
            inputs,
            None,
            context_status,
            context_reason,
            lineage,
            upstream_fidelity=fidelity,
            previous_state=initial_state,
        )
    if prior_count + len(inputs) < required:
        return _build_output(
            feature,
            inputs,
            None,
            FeatureValidity.WARMUP,
            "INSUFFICIENT_REQUIRED_SAMPLES",
            lineage,
            upstream_fidelity=fidelity,
            previous_state=initial_state,
        )
    state = initial_state
    numeric: Decimal | None = None
    reason = "COMPUTED"
    components: tuple[DecimalValue, ...] = ()
    if feature.canonical_id in _RECURSIVE_FEATURES:
        try:
            output, state = _recursive_latest(feature, inputs, initial_state, lineage)
            numeric = output.value
        except (FeatureEvaluationError, NumericPolicyError, InvalidOperation, ValueError) as exc:
            numeric = None
            reason = str(exc)
    else:
        try:
            numeric, reason, components = _compute_numeric(feature, inputs, initial_state)
        except (FeatureEvaluationError, NumericPolicyError, InvalidOperation, ValueError) as exc:
            numeric = None
            reason = str(exc)
    if numeric is None:
        return _build_output(
            feature,
            inputs,
            None,
            FeatureValidity.INVALID,
            reason,
            lineage,
            upstream_fidelity=fidelity,
            previous_state=initial_state,
        )
    canonical_output = _safe_canonical(numeric)
    if canonical_output is None:
        return _build_output(
            feature,
            inputs,
            None,
            FeatureValidity.INVALID,
            "CANONICAL_DECIMAL_OVERFLOW",
            lineage,
            upstream_fidelity=fidelity,
            previous_state=initial_state,
        )
    validity = (
        FeatureValidity.DEGRADED if fidelity == "RESOURCE_DEGRADED" else FeatureValidity.VALID
    )
    return _build_output(
        feature,
        inputs,
        canonical_output,
        validity,
        reason,
        lineage,
        state,
        fidelity,
        initial_state if state is None else None,
    )


def evaluate_snapshot(
    features: Iterable[FeatureVersion],
    samples: Iterable[FeatureSample | CandleBar | DecimalValue | str | int | Decimal],
    *,
    evaluation_time: datetime | None = None,
) -> FeatureSnapshot:
    feature_list = tuple(features)
    if not feature_list:
        raise FeatureEvaluationError("snapshot requires features")
    sample_list = _coerce_samples(samples)
    values = tuple(
        evaluate_feature(feature, sample_list, evaluation_time=evaluation_time)
        for feature in feature_list
    )
    first = values[0]
    return FeatureSnapshot(
        values=values,
        source_market_state_fingerprint=first.source_market_state_fingerprint,
        source_generation_fingerprint=first.source_generation_fingerprint,
        environment=first.environment,
        evaluation_time=evaluation_time or first.knowledge_time,
    )


@dataclass(frozen=True, slots=True)
class AlignedWindowEvidence:
    """Derived analytical OHLCV evidence; never a Market-State truth owner."""

    target_minutes: int
    start: datetime
    end: datetime
    constituents: tuple[CandleBar, ...]
    validity: FeatureValidity
    reason: str
    source_id: StableId | None
    contract_id: StableId | None
    environment: Environment | None
    generation_fingerprint: str | None
    open: DecimalValue | None
    high: DecimalValue | None
    low: DecimalValue | None
    close: DecimalValue | None
    volume: Quantity | None
    event_time: datetime | None
    knowledge_time: datetime | None
    wall_receive_time: datetime | None
    lineage: tuple[str, ...]
    provenance: str = DERIVED_MTF_PROVENANCE

    def __post_init__(self) -> None:
        if self.target_minutes not in {5, 15}:
            raise FeatureError("only deterministic 5m and 15m alignment is authorized")
        object.__setattr__(self, "start", _utc(self.start, "aligned start"))
        object.__setattr__(self, "end", _utc(self.end, "aligned end"))
        if (
            self.end <= self.start
            or (self.end - self.start).total_seconds() != self.target_minutes * 60
        ):
            raise FeatureError("aligned window geometry is invalid")
        if self.validity in {FeatureValidity.VALID, FeatureValidity.DEGRADED}:
            if any(
                value is None for value in (self.open, self.high, self.low, self.close, self.volume)
            ):
                raise FeatureError("valid aligned evidence requires OHLCV")
        if (not self.lineage and self.validity is not FeatureValidity.WARMUP) or len(
            set(self.lineage)
        ) != len(self.lineage):
            raise FeatureError("aligned lineage is missing or duplicated")
        for item in self.lineage:
            _require_hash(item, "aligned lineage entry")
        if self.provenance != DERIVED_MTF_PROVENANCE:
            raise FeatureError("unsupported derived provenance")

    @property
    def fingerprint(self) -> str:
        return _hash(
            {
                "target_minutes": self.target_minutes,
                "start": self.start.isoformat(),
                "end": self.end.isoformat(),
                "validity": self.validity.value,
                "reason": self.reason,
                "source": self.source_id.as_text() if self.source_id else None,
                "contract": self.contract_id.as_text() if self.contract_id else None,
                "environment": self.environment.value if self.environment else None,
                "generation": self.generation_fingerprint,
                "open": self.open.fingerprint if self.open else None,
                "high": self.high.fingerprint if self.high else None,
                "low": self.low.fingerprint if self.low else None,
                "close": self.close.fingerprint if self.close else None,
                "volume": self.volume.fingerprint if self.volume else None,
                "event_time": self.event_time.isoformat() if self.event_time else None,
                "knowledge_time": self.knowledge_time.isoformat() if self.knowledge_time else None,
                "wall_receive_time": self.wall_receive_time.isoformat()
                if self.wall_receive_time
                else None,
                "lineage": self.lineage,
                "provenance": self.provenance,
            }
        )


def _aligned_bounds(start: datetime, target_minutes: int) -> tuple[datetime, datetime]:
    seconds = target_minutes * 60
    epoch = int(start.timestamp())
    aligned = epoch - (epoch % seconds)
    begin = datetime.fromtimestamp(aligned, tz=UTC)
    return begin, begin + timedelta(seconds=seconds)


def align_closed_1m_candles(
    candles: Iterable[CandleBar],
    target_minutes: int,
    *,
    evaluation_time: datetime | None = None,
    upstream_fidelity: str = "TRUSTED",
) -> AlignedWindowEvidence:
    """Derive one exact 5m/15m window from complete CLOSED 1m constituents."""

    if target_minutes not in {5, 15}:
        raise FeatureEvaluationError("target timeframe must be 5 or 15 minutes")
    if upstream_fidelity not in {"TRUSTED", "RESOURCE_DEGRADED"}:
        raise FeatureEvaluationError("unsupported upstream fidelity")
    items = tuple(candles)
    if not items:
        now = _utc(evaluation_time or datetime(1970, 1, 1, tzinfo=UTC), "evaluation time")
        start, end = _aligned_bounds(now, target_minutes)
        return AlignedWindowEvidence(
            target_minutes,
            start,
            end,
            (),
            FeatureValidity.WARMUP,
            "NO_CONSTITUENTS",
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            (),
        )
    first = items[0]
    start, end = _aligned_bounds(first.start, target_minutes)
    lineage = tuple(item.fingerprint for item in items)
    base_kwargs: dict[str, Any] = dict(
        target_minutes=target_minutes,
        start=start,
        end=end,
        constituents=items,
        source_id=first.context.source_id,
        contract_id=first.context.contract_id,
        environment=first.context.environment,
        generation_fingerprint=first.context.generation.fingerprint,
        open=None,
        high=None,
        low=None,
        close=None,
        volume=None,
        event_time=max(item.context.event_time for item in items),
        knowledge_time=max(item.context.knowledge_time for item in items),
        wall_receive_time=max(item.context.wall_receive_time for item in items),
        lineage=lineage,
    )
    expected = target_minutes
    boundary = _utc(evaluation_time, "evaluation time") if evaluation_time is not None else None
    if any(
        item.timeframe.duration_seconds != 60 or item.finality is not Finality.CLOSED
        for item in items
    ):
        return AlignedWindowEvidence(
            **base_kwargs,
            validity=FeatureValidity.INVALID,
            reason="CLOSED_1M_CONSTITUENTS_REQUIRED",
        )
    if (
        any(
            item.context.knowledge_time > boundary or item.context.event_time > boundary
            for item in items
        )
        if boundary
        else False
    ):
        return AlignedWindowEvidence(
            **base_kwargs, validity=FeatureValidity.INVALID, reason="FUTURE_CONSTITUENT_EVIDENCE"
        )
    if any(item.start < start or item.end > end for item in items):
        return AlignedWindowEvidence(
            **base_kwargs,
            validity=FeatureValidity.INVALID,
            reason="CONSTITUENT_OUTSIDE_ALIGNED_WINDOW",
        )
    if items != tuple(sorted(items, key=lambda item: item.start)):
        return AlignedWindowEvidence(
            **base_kwargs, validity=FeatureValidity.INVALID, reason="OUT_OF_ORDER_CONSTITUENTS"
        )
    if len(items) != expected:
        validity = (
            FeatureValidity.WARMUP
            if boundary is None or boundary < end
            else FeatureValidity.UNKNOWN
        )
        return AlignedWindowEvidence(
            **base_kwargs, validity=validity, reason="INCOMPLETE_ALIGNED_WINDOW"
        )
    for left, right in zip(items[:-1], items[1:], strict=False):
        if left.end != right.start:
            return AlignedWindowEvidence(
                **base_kwargs,
                validity=FeatureValidity.INVALID,
                reason="NON_CONTIGUOUS_ALIGNED_WINDOW",
            )
    for item in items:
        if (
            item.context.source_id != first.context.source_id
            or item.context.contract_id != first.context.contract_id
            or item.context.environment is not first.context.environment
            or item.context.generation != first.context.generation
            or item.timeframe.version != first.timeframe.version
            or item.context.provenance_fingerprint != first.context.provenance_fingerprint
            or item.volume.unit is not first.volume.unit
            or item.volume.source_contract_identity_version
            != first.volume.source_contract_identity_version
        ):
            return AlignedWindowEvidence(
                **base_kwargs,
                validity=FeatureValidity.INVALID,
                reason="MIXED_IDENTITY_OR_QUANTITY_CONTRACT",
            )
    if items[0].start != start or items[-1].end != end:
        return AlignedWindowEvidence(
            **base_kwargs, validity=FeatureValidity.INVALID, reason="WINDOW_GEOMETRY_MISMATCH"
        )
    try:
        open_value = items[0].open
        high_value = max(item.high.value for item in items)
        low_value = min(item.low.value for item in items)
        close_value = items[-1].close
        with localcontext() as context:
            context.prec = 76
            volume_value = sum((item.volume.value.value for item in items), Decimal(0))
        volume = Quantity(
            _canonical(volume_value),
            first.volume.unit,
            first.volume.source_contract_identity_version,
        )
        fidelity = "RESOURCE_DEGRADED" if upstream_fidelity == "RESOURCE_DEGRADED" else "TRUSTED"
        valid_kwargs = {
            **base_kwargs,
            "open": open_value,
            "high": _canonical(high_value),
            "low": _canonical(low_value),
            "close": close_value,
            "volume": volume,
        }
        return AlignedWindowEvidence(
            **valid_kwargs,
            validity=FeatureValidity.DEGRADED
            if fidelity == "RESOURCE_DEGRADED"
            else FeatureValidity.VALID,
            reason="COMPLETE_COHERENT_ALIGNED_WINDOW",
        )
    except (NumericPolicyError, InvalidOperation, ValueError) as exc:
        return AlignedWindowEvidence(
            **base_kwargs, validity=FeatureValidity.INVALID, reason=str(exc)
        )


def align_candles(
    candles: Iterable[CandleBar],
    target_minutes: int,
    *,
    evaluation_time: datetime | None = None,
    upstream_fidelity: str = "TRUSTED",
) -> AlignedWindowEvidence:
    """Short alias for the public deterministic MTF alignment operation."""

    return align_closed_1m_candles(
        candles,
        target_minutes,
        evaluation_time=evaluation_time,
        upstream_fidelity=upstream_fidelity,
    )


__all__ = [
    "AlignedWindowEvidence",
    "DERIVED_MTF_PROVENANCE",
    "FEATURE_ALGORITHM_VERSION",
    "FEATURE_DECIMAL_POLICY_VERSION",
    "FeatureDefinition",
    "FeatureError",
    "FeatureEvaluationError",
    "FeatureRegistry",
    "FeatureRegistryError",
    "FeatureSample",
    "FeatureSnapshot",
    "FeatureValidity",
    "FeatureValue",
    "FeatureVersion",
    "RecursiveAccumulatorState",
    "RECURSIVE_STATE_VERSION",
    "align_candles",
    "align_closed_1m_candles",
    "evaluate_feature",
    "evaluate_feature_series",
    "evaluate_snapshot",
]
