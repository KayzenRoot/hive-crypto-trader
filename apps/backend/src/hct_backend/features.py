"""Deterministic, provider-neutral Module 8 feature contracts and evaluation.

This module consumes immutable S1E/S1F evidence and fixture values only.  It
does not open transports, persist state, create orders or grant authority.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from decimal import ROUND_HALF_EVEN, Decimal, InvalidOperation, localcontext
from enum import StrEnum
from typing import Any, Final, Self

from hct_backend.contracts import Environment, IdentityKind, StableId
from hct_backend.market_truth import (
    DataAuthorityState,
    LifecycleRestriction,
    MarketStateSnapshot,
    MarketStateTrust,
    QualityReason,
    ResourceAdmissionEvidence,
    ResourceDisposition,
)
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
FEATURE_AUTHORITY_VERSION: Final = "S2A_AUTHORITY_EVIDENCE_V1"
DERIVED_MTF_PROVENANCE: Final = "DERIVED_ANALYTICAL_V1"
_SCALE_18 = Decimal("1e-18")
_HASH = re.compile(r"^[0-9a-f]{64}$")
_STATE_ATTESTATION: Final = object()
_ALIGNED_ATTESTATION: Final = object()
_AUTHORITY_ATTESTATION: Final = object()
_TRUST_SEVERITY: Final = (
    MarketStateTrust.UNTRUSTED,
    MarketStateTrust.RESYNC_REQUIRED,
    MarketStateTrust.UNKNOWN,
    MarketStateTrust.DEGRADED,
    MarketStateTrust.TRUSTED,
)
_AUTHORITY_SEVERITY: Final = (
    DataAuthorityState.EMERGENCY,
    DataAuthorityState.RECONCILIATION_ONLY,
    DataAuthorityState.REDUCE_ONLY,
    DataAuthorityState.NO_NEW_EXPOSURE,
    DataAuthorityState.DEGRADED_NEW_EXPOSURE,
    DataAuthorityState.ALLOW_NEW_EXPOSURE,
)
_RESOURCE_SEVERITY: Final = (
    ResourceDisposition.DENIED,
    ResourceDisposition.UNKNOWN,
    ResourceDisposition.DEGRADED,
    ResourceDisposition.AVAILABLE,
)
_LIFECYCLE_SEVERITY: Final = (
    LifecycleRestriction.NEW_EXPOSURE_DISABLED,
    LifecycleRestriction.ELIGIBILITY_UNKNOWN,
    LifecycleRestriction.NONE,
)
_UNKNOWN_QUALITY_REASONS: Final = frozenset(
    {
        QualityReason.STALE,
        QualityReason.EXPIRED,
        QualityReason.GAP,
        QualityReason.DUPLICATE,
        QualityReason.OUT_OF_ORDER,
        QualityReason.SEQUENCE_UNPROVABLE,
        QualityReason.CLOCK_DRIFT,
        QualityReason.CLOCK_JUMP,
        QualityReason.CLOCK_UNTRUSTED,
        QualityReason.SCHEMA_QUARANTINED,
        QualityReason.MISSING_PROVENANCE,
        QualityReason.MISSING_GENERATION,
        QualityReason.UNSYNCHRONIZED,
    }
)
_INVALID_QUALITY_REASONS: Final = frozenset(
    {
        QualityReason.RETIRED_GENERATION,
        QualityReason.CROSS_CHANNEL_CONTRADICTION,
    }
)
_RESTRICTIVE_QUALITY_REASONS: Final = _UNKNOWN_QUALITY_REASONS | _INVALID_QUALITY_REASONS
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


class FeatureAxisRestriction(StrEnum):
    """Restriction axis kept separate from analytical FeatureValidity."""

    NONE = "NONE"
    RESTRICTIVE = "RESTRICTIVE"


def _hash(material: object) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _is_hash(value: object) -> bool:
    """Exact lowercase SHA-256 fingerprint test."""

    return isinstance(value, str) and _HASH.fullmatch(value) is not None


def _require_hash(value: str, label: str) -> None:
    if not _is_hash(value):
        raise FeatureError(f"{label} must be a lowercase SHA-256 fingerprint")


def _utc(value: datetime, label: str) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise FeatureError(f"{label} must be timezone-aware")
    return value.astimezone(UTC)


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


def _rsi_output(avg_gain: Decimal, avg_loss: Decimal) -> DecimalValue:
    """Canonical Wilder RSI output for the given average gain and loss."""

    if avg_gain == 0 and avg_loss == 0:
        return _canonical(Decimal(50))
    if avg_loss == 0:
        return _canonical(Decimal(100))
    if avg_gain == 0:
        return _canonical(Decimal(0))
    with localcontext() as context:
        context.prec = 76
        context.rounding = ROUND_HALF_EVEN
        return _canonical(Decimal(100) - (Decimal(100) / (Decimal(1) + avg_gain / avg_loss)))


def _value_evidence_material(
    *,
    fingerprint: str,
    provenance_fingerprint: str,
    source_id: StableId,
    contract_id: StableId,
    environment: Environment,
    generation_fingerprint: str,
    timeframe: Timeframe,
    closed: bool,
    event_time: datetime,
    knowledge_time: datetime,
    wall_receive_time: datetime,
    interval_start: datetime | None,
    interval_end: datetime | None,
    value: DecimalValue | None,
    high: DecimalValue | None,
    low: DecimalValue | None,
    close: DecimalValue | None,
    quantity: Quantity | None,
) -> dict[str, object]:
    """Canonical S1F value-evidence material bound by non-fixture authority."""

    return {
        "value_evidence_version": FEATURE_AUTHORITY_VERSION,
        "fingerprint": fingerprint,
        "provenance": provenance_fingerprint,
        "source": source_id.as_text(),
        "contract": contract_id.as_text(),
        "environment": environment.value,
        "generation": generation_fingerprint,
        "timeframe": timeframe.fingerprint,
        "timeframe_version": timeframe.version,
        "closed": closed,
        "event_time": event_time.isoformat(),
        "knowledge_time": knowledge_time.isoformat(),
        "wall_receive_time": wall_receive_time.isoformat(),
        "interval_start": interval_start.isoformat() if interval_start else None,
        "interval_end": interval_end.isoformat() if interval_end else None,
        "value": value.fingerprint if value else None,
        "high": high.fingerprint if high else None,
        "low": low.fingerprint if low else None,
        "close": close.fingerprint if close else None,
        "quantity": quantity.fingerprint if quantity else None,
    }


def _candle_value_evidence_material(candle: CandleBar) -> dict[str, object]:
    context = candle.context
    return _value_evidence_material(
        fingerprint=candle.fingerprint,
        provenance_fingerprint=context.provenance_fingerprint,
        source_id=context.source_id,
        contract_id=context.contract_id,
        environment=context.environment,
        generation_fingerprint=context.generation.fingerprint,
        timeframe=candle.timeframe,
        closed=candle.finality is Finality.CLOSED,
        event_time=context.event_time,
        knowledge_time=context.knowledge_time,
        wall_receive_time=context.wall_receive_time,
        interval_start=candle.start,
        interval_end=candle.end,
        value=candle.close,
        high=candle.high,
        low=candle.low,
        close=candle.close,
        quantity=candle.volume,
    )


@dataclass(frozen=True, slots=True, init=False)
class FeatureAuthorityEvidence:
    """Read-only typed S1E authority evidence consumed by Module 8.

    Analytical truth, market-state trust, data authority, resource admission and
    universe lifecycle are separate axes.  This evidence carries all of them
    without granting any downstream action authority.

    Non-fixture authority is evaluator-issued and content-bound: it can only be
    derived from a canonical S1E ``MarketStateSnapshot`` (plus the governed
    Module 29 admission seam where resource state is required), and it binds the
    exact source, contract, environment, generation and S1F value evidence it
    attests.  Synthetic authority is REPLAY-only and unmistakably marked.
    """

    market_state_fingerprint: str
    market_state_trust: MarketStateTrust
    data_authority_state: DataAuthorityState
    data_authority_fingerprint: str
    data_authority_reasons: tuple[QualityReason, ...]
    resource_disposition: ResourceDisposition
    resource_evidence_fingerprint: str
    lifecycle_restriction: LifecycleRestriction
    source_id: StableId
    contract_id: StableId
    environment: Environment
    generation_fingerprint: str
    bound_evidence_fingerprint: str | None
    is_fixture: bool
    _attestation: object = field(default=None, repr=False, compare=False)

    def __init__(self, *args: object, **kwargs: object) -> None:
        raise FeatureError(
            "FeatureAuthorityEvidence must be issued by from_market_state, from_candle or fixture"
        )

    def _is_attested(self) -> bool:
        return self._attestation is _AUTHORITY_ATTESTATION

    @classmethod
    def _issue(
        cls,
        *,
        market_state_fingerprint: str,
        market_state_trust: MarketStateTrust,
        data_authority_state: DataAuthorityState,
        data_authority_fingerprint: str,
        data_authority_reasons: tuple[QualityReason, ...],
        resource_disposition: ResourceDisposition,
        resource_evidence_fingerprint: str,
        lifecycle_restriction: LifecycleRestriction,
        source_id: StableId,
        contract_id: StableId,
        environment: Environment,
        generation_fingerprint: str,
        bound_evidence_fingerprint: str | None,
        is_fixture: bool,
    ) -> FeatureAuthorityEvidence:
        instance = object.__new__(cls)
        for name, value in (
            ("market_state_fingerprint", market_state_fingerprint),
            ("market_state_trust", market_state_trust),
            ("data_authority_state", data_authority_state),
            ("data_authority_fingerprint", data_authority_fingerprint),
            ("data_authority_reasons", data_authority_reasons),
            ("resource_disposition", resource_disposition),
            ("resource_evidence_fingerprint", resource_evidence_fingerprint),
            ("lifecycle_restriction", lifecycle_restriction),
            ("source_id", source_id),
            ("contract_id", contract_id),
            ("environment", environment),
            ("generation_fingerprint", generation_fingerprint),
            ("bound_evidence_fingerprint", bound_evidence_fingerprint),
            ("is_fixture", is_fixture),
        ):
            object.__setattr__(instance, name, value)
        object.__setattr__(instance, "_attestation", _AUTHORITY_ATTESTATION)
        instance.__post_init__()
        return instance

    def __post_init__(self) -> None:
        if not self._is_attested():
            raise FeatureError("authority evidence is not evaluator-issued")
        _require_hash(self.market_state_fingerprint, "authority market-state fingerprint")
        if not isinstance(self.market_state_trust, MarketStateTrust):
            raise FeatureError("authority market-state trust is invalid")
        if not isinstance(self.data_authority_state, DataAuthorityState):
            raise FeatureError("authority data-authority state is invalid")
        _require_hash(self.data_authority_fingerprint, "authority decision fingerprint")
        if not isinstance(self.data_authority_reasons, tuple) or not self.data_authority_reasons:
            raise FeatureError("authority reasons are required")
        if any(not isinstance(item, QualityReason) for item in self.data_authority_reasons):
            raise FeatureError("authority reasons must be governed quality reasons")
        if (
            tuple(sorted(set(self.data_authority_reasons), key=lambda item: item.value))
            != self.data_authority_reasons
        ):
            raise FeatureError("authority reasons must be unique and ordered")
        if not isinstance(self.resource_disposition, ResourceDisposition):
            raise FeatureError("authority resource disposition is invalid")
        _require_hash(self.resource_evidence_fingerprint, "authority resource fingerprint")
        if not isinstance(self.lifecycle_restriction, LifecycleRestriction):
            raise FeatureError("authority lifecycle restriction is invalid")
        if (
            not isinstance(self.source_id, StableId)
            or self.source_id.kind is not IdentityKind.EXCHANGE
            or not isinstance(self.contract_id, StableId)
            or self.contract_id.kind is not IdentityKind.INSTRUMENT
        ):
            raise FeatureError("authority source identities are invalid")
        if not isinstance(self.environment, Environment):
            raise FeatureError("authority environment is invalid")
        _require_hash(self.generation_fingerprint, "authority generation fingerprint")
        if not isinstance(self.is_fixture, bool):
            raise FeatureError("authority fixture flag must be boolean")
        if self.is_fixture:
            if self.environment is not Environment.REPLAY:
                raise FeatureError("synthetic authority is REPLAY-only")
            if self.bound_evidence_fingerprint is not None:
                _require_hash(self.bound_evidence_fingerprint, "authority bound value evidence")
        else:
            if self.bound_evidence_fingerprint is not None:
                _require_hash(self.bound_evidence_fingerprint, "authority bound value evidence")

    @property
    def resource_restriction(self) -> FeatureAxisRestriction:
        if self.resource_disposition is ResourceDisposition.AVAILABLE:
            return FeatureAxisRestriction.NONE
        return FeatureAxisRestriction.RESTRICTIVE

    @property
    def lifecycle_axis(self) -> FeatureAxisRestriction:
        if self.lifecycle_restriction is LifecycleRestriction.NONE:
            return FeatureAxisRestriction.NONE
        return FeatureAxisRestriction.RESTRICTIVE

    @property
    def restrictive_reasons(self) -> tuple[QualityReason, ...]:
        return tuple(
            reason
            for reason in self.data_authority_reasons
            if reason in _RESTRICTIVE_QUALITY_REASONS
        )

    @property
    def market_truth_restrictive(self) -> bool:
        return self.market_state_trust is not MarketStateTrust.TRUSTED or bool(
            self.restrictive_reasons
        )

    @property
    def material(self) -> dict[str, object]:
        return {
            "authority_version": FEATURE_AUTHORITY_VERSION,
            "market_state_fingerprint": self.market_state_fingerprint,
            "market_state_trust": self.market_state_trust.value,
            "data_authority_state": self.data_authority_state.value,
            "data_authority_fingerprint": self.data_authority_fingerprint,
            "data_authority_reasons": [item.value for item in self.data_authority_reasons],
            "resource_disposition": self.resource_disposition.value,
            "resource_evidence_fingerprint": self.resource_evidence_fingerprint,
            "lifecycle_restriction": self.lifecycle_restriction.value,
            "source": self.source_id.as_text(),
            "contract": self.contract_id.as_text(),
            "environment": self.environment.value,
            "generation": self.generation_fingerprint,
            "bound_evidence_fingerprint": self.bound_evidence_fingerprint,
            "is_fixture": self.is_fixture,
        }

    @property
    def fingerprint(self) -> str:
        return _hash(self.material)

    def matches_identity(
        self,
        *,
        source_id: StableId,
        contract_id: StableId,
        environment: Environment,
        generation_fingerprint: str,
    ) -> bool:
        return (
            self.source_id == source_id
            and self.contract_id == contract_id
            and self.environment is environment
            and self.generation_fingerprint == generation_fingerprint
        )

    @classmethod
    def from_market_state(
        cls,
        state: MarketStateSnapshot,
        *,
        resource: ResourceAdmissionEvidence | None = None,
    ) -> FeatureAuthorityEvidence:
        """Derive read-only authority evidence from canonical S1E state."""

        if not isinstance(state, MarketStateSnapshot):
            raise FeatureError("canonical S1E market-state snapshot is required")
        if resource is not None and not isinstance(resource, ResourceAdmissionEvidence):
            raise FeatureError("canonical module 29 admission evidence is required")
        decision = state.data_authority
        return cls._issue(
            market_state_fingerprint=state.fingerprint,
            market_state_trust=state.trust,
            data_authority_state=decision.state,
            data_authority_fingerprint=_hash(
                {
                    "state": decision.state.value,
                    "reasons": [item.value for item in decision.reasons],
                    "affected_actions": [item.value for item in decision.affected_actions],
                    "explanatory_score": decision.explanatory_score,
                }
            ),
            data_authority_reasons=tuple(
                sorted(set(decision.reasons), key=lambda item: item.value)
            ),
            resource_disposition=(
                resource.disposition if resource is not None else ResourceDisposition.UNKNOWN
            ),
            resource_evidence_fingerprint=(
                resource.decision_fingerprint
                if resource is not None
                else _hash({"resource": "ABSENT", "state": state.fingerprint})
            ),
            lifecycle_restriction=state.lifecycle_restriction,
            source_id=state.source_id,
            contract_id=state.contract_id,
            environment=state.environment,
            generation_fingerprint=state.generation.fingerprint,
            bound_evidence_fingerprint=None,
            is_fixture=False,
        )

    @classmethod
    def from_candle(
        cls,
        candle: CandleBar,
        state: MarketStateSnapshot,
        *,
        resource: ResourceAdmissionEvidence | None = None,
    ) -> FeatureAuthorityEvidence:
        """Bind canonical S1E authority to one exact S1F candle evidence."""

        if not isinstance(candle, CandleBar):
            raise FeatureError("CandleBar is required")
        if not isinstance(state, MarketStateSnapshot):
            raise FeatureError("canonical S1E market-state snapshot is required")
        if (
            state.source_id != candle.context.source_id
            or state.contract_id != candle.context.contract_id
            or state.environment is not candle.context.environment
            or state.generation != candle.context.generation
        ):
            raise FeatureError("candle and market-state identity disagree")
        base = cls.from_market_state(state, resource=resource)
        return cls._issue(
            market_state_fingerprint=base.market_state_fingerprint,
            market_state_trust=base.market_state_trust,
            data_authority_state=base.data_authority_state,
            data_authority_fingerprint=base.data_authority_fingerprint,
            data_authority_reasons=base.data_authority_reasons,
            resource_disposition=base.resource_disposition,
            resource_evidence_fingerprint=base.resource_evidence_fingerprint,
            lifecycle_restriction=base.lifecycle_restriction,
            source_id=base.source_id,
            contract_id=base.contract_id,
            environment=base.environment,
            generation_fingerprint=base.generation_fingerprint,
            bound_evidence_fingerprint=_hash(_candle_value_evidence_material(candle)),
            is_fixture=False,
        )

    @classmethod
    def fixture_for_candle(
        cls,
        candle: CandleBar,
        *,
        market_state_trust: MarketStateTrust = MarketStateTrust.TRUSTED,
        data_authority_state: DataAuthorityState = DataAuthorityState.ALLOW_NEW_EXPOSURE,
        data_authority_reasons: tuple[QualityReason, ...] = (QualityReason.FRESH_VALID,),
        resource_disposition: ResourceDisposition = ResourceDisposition.AVAILABLE,
        lifecycle_restriction: LifecycleRestriction = LifecycleRestriction.NONE,
    ) -> FeatureAuthorityEvidence:
        """Issue REPLAY-only authority bound to one exact 1m constituent."""

        if not isinstance(candle, CandleBar):
            raise FeatureError("CandleBar is required")
        context = candle.context
        if context.environment is not Environment.REPLAY:
            raise FeatureError("per-constituent synthetic authority is REPLAY-only")
        return cls.fixture(
            market_state_fingerprint=_hash(
                {
                    "fixture": True,
                    "candle": candle.fingerprint,
                    "generation": context.generation.fingerprint,
                }
            ),
            source_id=context.source_id,
            contract_id=context.contract_id,
            environment=context.environment,
            generation_fingerprint=context.generation.fingerprint,
            market_state_trust=market_state_trust,
            data_authority_state=data_authority_state,
            data_authority_reasons=data_authority_reasons,
            resource_disposition=resource_disposition,
            lifecycle_restriction=lifecycle_restriction,
            bound_evidence_fingerprint=_hash(_candle_value_evidence_material(candle)),
        )

    @classmethod
    def fixture(
        cls,
        *,
        market_state_fingerprint: str,
        source_id: StableId | None = None,
        contract_id: StableId | None = None,
        environment: Environment = Environment.REPLAY,
        generation_fingerprint: str | None = None,
        market_state_trust: MarketStateTrust = MarketStateTrust.TRUSTED,
        data_authority_state: DataAuthorityState = DataAuthorityState.ALLOW_NEW_EXPOSURE,
        data_authority_reasons: tuple[QualityReason, ...] = (QualityReason.FRESH_VALID,),
        resource_disposition: ResourceDisposition = ResourceDisposition.AVAILABLE,
        lifecycle_restriction: LifecycleRestriction = LifecycleRestriction.NONE,
        bound_evidence_fingerprint: str | None = None,
    ) -> FeatureAuthorityEvidence:
        """Replay-scoped synthetic authority; it can never claim live authority."""

        if environment is not Environment.REPLAY:
            raise FeatureError("synthetic fixture authority is REPLAY-only")
        source = source_id or StableId(kind=IdentityKind.EXCHANGE, value="fixture")
        contract = contract_id or StableId(kind=IdentityKind.INSTRUMENT, value="fixture")
        return cls._issue(
            market_state_fingerprint=market_state_fingerprint,
            market_state_trust=market_state_trust,
            data_authority_state=data_authority_state,
            data_authority_fingerprint=_hash(
                {
                    "fixture": True,
                    "state": data_authority_state.value,
                    "reasons": [item.value for item in data_authority_reasons],
                }
            ),
            data_authority_reasons=tuple(
                sorted(set(data_authority_reasons), key=lambda item: item.value)
            ),
            resource_disposition=resource_disposition,
            resource_evidence_fingerprint=_hash(
                {
                    "fixture": True,
                    "resource": resource_disposition.value,
                    "state": market_state_fingerprint,
                }
            ),
            lifecycle_restriction=lifecycle_restriction,
            source_id=source,
            contract_id=contract,
            environment=environment,
            generation_fingerprint=(
                generation_fingerprint
                or _hash({"fixture": True, "source": source.as_text(), "generation": 1})
            ),
            bound_evidence_fingerprint=bound_evidence_fingerprint,
            is_fixture=True,
        )


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
    authority: FeatureAuthorityEvidence
    interval_start: datetime | None = None
    interval_end: datetime | None = None
    high: DecimalValue | None = None
    low: DecimalValue | None = None
    close: DecimalValue | None = None
    quantity: Quantity | None = None

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
        if not isinstance(self.authority, FeatureAuthorityEvidence):
            raise FeatureError("sample authority evidence is required")
        if self.market_state_fingerprint != self.authority.market_state_fingerprint:
            raise FeatureError("sample market state is not bound to its authority evidence")
        if self.authority.is_fixture:
            if self.environment is not Environment.REPLAY:
                raise FeatureError("synthetic fixture authority is REPLAY-only")
            if (
                self.authority.bound_evidence_fingerprint is not None
                and self.authority.bound_evidence_fingerprint != self.value_evidence_fingerprint
            ):
                raise FeatureError("sample material disagrees with its bound value evidence")
        else:
            if not self.authority.matches_identity(
                source_id=self.source_id,
                contract_id=self.contract_id,
                environment=self.environment,
                generation_fingerprint=self.generation_fingerprint,
            ):
                raise FeatureError("sample identity disagrees with its authority evidence")
            if self.authority.bound_evidence_fingerprint != self.value_evidence_fingerprint:
                raise FeatureError(
                    "sample material disagrees with its bound canonical value evidence"
                )

    @property
    def value_evidence_fingerprint(self) -> str:
        """Content binding between a non-fixture sample and its authority."""

        return _hash(
            _value_evidence_material(
                fingerprint=self.fingerprint,
                provenance_fingerprint=self.provenance_fingerprint,
                source_id=self.source_id,
                contract_id=self.contract_id,
                environment=self.environment,
                generation_fingerprint=self.generation_fingerprint,
                timeframe=self.timeframe,
                closed=self.closed,
                event_time=self.event_time,
                knowledge_time=self.knowledge_time,
                wall_receive_time=self.wall_receive_time,
                interval_start=self.interval_start,
                interval_end=self.interval_end,
                value=self.value,
                high=self.high,
                low=self.low,
                close=self.close,
                quantity=self.quantity,
            )
        )

    @property
    def market_state_trust(self) -> MarketStateTrust:
        return self.authority.market_state_trust

    @property
    def resource_disposition(self) -> ResourceDisposition:
        return self.authority.resource_disposition

    @property
    def resource_restriction(self) -> FeatureAxisRestriction:
        return self.authority.resource_restriction

    @property
    def lifecycle_axis(self) -> FeatureAxisRestriction:
        return self.authority.lifecycle_axis

    @property
    def data_authority_state(self) -> DataAuthorityState:
        return self.authority.data_authority_state

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
        market_state_trust: MarketStateTrust = MarketStateTrust.TRUSTED,
        data_authority_state: DataAuthorityState = DataAuthorityState.ALLOW_NEW_EXPOSURE,
        data_authority_reasons: tuple[QualityReason, ...] = (QualityReason.FRESH_VALID,),
        resource_disposition: ResourceDisposition = ResourceDisposition.AVAILABLE,
        lifecycle_restriction: LifecycleRestriction = LifecycleRestriction.NONE,
    ) -> Self:
        """Build a synthetic scalar fixture; fixtures are REPLAY-only."""

        if environment is not Environment.REPLAY:
            raise FeatureError("synthetic fixture samples are REPLAY-only")
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
            authority=FeatureAuthorityEvidence.fixture(
                market_state_fingerprint=state,
                source_id=source,
                contract_id=contract,
                environment=environment,
                generation_fingerprint=generation,
                market_state_trust=market_state_trust,
                data_authority_state=data_authority_state,
                data_authority_reasons=data_authority_reasons,
                resource_disposition=resource_disposition,
                lifecycle_restriction=lifecycle_restriction,
            ),
            interval_start=event,
            interval_end=event + timedelta(seconds=frame.duration_seconds),
            close=parsed,
        )

    @classmethod
    def from_candle(
        cls,
        candle: CandleBar,
        *,
        market_state: MarketStateSnapshot | None = None,
        resource: ResourceAdmissionEvidence | None = None,
    ) -> Self:
        """Bind an S1F candle to canonical S1E authority evidence.

        A non-REPLAY candle can never be admitted without the matching canonical
        market-state snapshot; the S1F provenance fingerprint is never reused as
        market-state identity.
        """

        if not isinstance(candle, CandleBar):
            raise FeatureError("CandleBar is required")
        context = candle.context
        if market_state is None:
            if context.environment is not Environment.REPLAY:
                raise FeatureError(
                    "authoritative candle samples require canonical S1E market-state evidence"
                )
            authority = FeatureAuthorityEvidence.fixture(
                market_state_fingerprint=_hash(
                    {
                        "fixture": True,
                        "provenance": context.provenance_fingerprint,
                        "event": context.originating_event_fingerprint,
                    }
                ),
                source_id=context.source_id,
                contract_id=context.contract_id,
                environment=context.environment,
                generation_fingerprint=context.generation.fingerprint,
            )
        else:
            if not isinstance(market_state, MarketStateSnapshot):
                raise FeatureError("canonical S1E market-state snapshot is required")
            authority = FeatureAuthorityEvidence.from_candle(
                candle, market_state, resource=resource
            )
        return cls(
            value=candle.close,
            fingerprint=candle.fingerprint,
            event_time=context.event_time,
            knowledge_time=context.knowledge_time,
            wall_receive_time=context.wall_receive_time,
            closed=candle.finality is Finality.CLOSED,
            source_id=context.source_id,
            contract_id=context.contract_id,
            environment=context.environment,
            generation_fingerprint=context.generation.fingerprint,
            market_state_fingerprint=authority.market_state_fingerprint,
            provenance_fingerprint=context.provenance_fingerprint,
            timeframe=candle.timeframe,
            authority=authority,
            interval_start=candle.start,
            interval_end=candle.end,
            high=candle.high,
            low=candle.low,
            close=candle.close,
            quantity=candle.volume,
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
                "authority": self.authority.fingerprint,
                "market_state_trust": self.authority.market_state_trust.value,
                "data_authority": self.authority.data_authority_state.value,
                "resource_restriction": self.authority.resource_restriction.value,
                "lifecycle_restriction": self.authority.lifecycle_axis.value,
            }
        )


@dataclass(frozen=True, slots=True, init=False)
class RecursiveAccumulatorState:
    """Evaluator-issued canonical state for deterministic recursive replay.

    The state binds the exact feature/algorithm/Decimal-policy, source,
    contract, environment, generation and timeframe context, the predecessor
    state fingerprint and the ordered input, market-state and authority lineage
    it consumed.  Only the evaluator can issue a resumable state; direct
    construction and unaudited deserialization stay inert and fail closed.
    """

    feature_id: str
    feature_version: int
    feature_fingerprint: str
    source_field: str
    parameter_n: int
    timeframe_fingerprint: str
    timeframe_version: int
    algorithm_version: str
    decimal_policy_version: str
    source_id: StableId
    contract_id: StableId
    environment: Environment
    source_generation_fingerprint: str
    components: tuple[DecimalValue, ...]
    previous_input: DecimalValue | None
    previous_close: DecimalValue | None
    processed_samples: int
    lineage: tuple[str, ...]
    market_state_lineage: tuple[str, ...]
    authority_lineage: tuple[str, ...]
    carried_market_state_trust: MarketStateTrust
    carried_data_authority_state: DataAuthorityState
    carried_resource_restriction: FeatureAxisRestriction
    carried_lifecycle_restriction: FeatureAxisRestriction
    carried_evidence_fingerprint: str
    previous_state_fingerprint: str | None
    event_time: datetime
    knowledge_time: datetime
    wall_receive_time: datetime
    window_start: datetime
    window_end: datetime
    _attestation: object = field(default=None, repr=False, compare=False)

    def __init__(self, *args: object, **kwargs: object) -> None:
        raise FeatureError("RecursiveAccumulatorState must be issued by the feature evaluator")

    def _is_attested(self) -> bool:
        return self._attestation is _STATE_ATTESTATION

    @classmethod
    def _from_evaluator(
        cls,
        *,
        feature: FeatureVersion,
        sample: FeatureSample,
        components: tuple[DecimalValue, ...],
        previous_input: DecimalValue | None,
        previous_close: DecimalValue | None,
        processed_samples: int,
        lineage: tuple[str, ...],
        market_state_lineage: tuple[str, ...],
        authority_lineage: tuple[str, ...],
        carried_market_state_trust: MarketStateTrust,
        carried_data_authority_state: DataAuthorityState,
        carried_resource_restriction: FeatureAxisRestriction,
        carried_lifecycle_restriction: FeatureAxisRestriction,
        carried_evidence_fingerprint: str,
        previous_state_fingerprint: str | None,
        validated_lineage_prefix: int,
        event_time: datetime,
        knowledge_time: datetime,
        wall_receive_time: datetime,
        window_start: datetime,
        window_end: datetime,
    ) -> RecursiveAccumulatorState:
        instance = object.__new__(cls)
        for name, value in (
            ("feature_id", feature.canonical_id),
            ("feature_version", feature.version),
            ("feature_fingerprint", feature.fingerprint),
            ("source_field", feature.definition.source_field),
            ("parameter_n", feature.parameter_n or 2),
            ("timeframe_fingerprint", sample.timeframe.fingerprint),
            ("timeframe_version", sample.timeframe.version),
            ("algorithm_version", RECURSIVE_STATE_VERSION),
            ("decimal_policy_version", FEATURE_DECIMAL_POLICY_VERSION),
            ("source_id", sample.source_id),
            ("contract_id", sample.contract_id),
            ("environment", sample.environment),
            ("source_generation_fingerprint", sample.generation_fingerprint),
            ("components", components),
            ("previous_input", previous_input),
            ("previous_close", previous_close),
            ("processed_samples", processed_samples),
            ("lineage", lineage),
            ("market_state_lineage", market_state_lineage),
            ("authority_lineage", authority_lineage),
            ("carried_market_state_trust", carried_market_state_trust),
            ("carried_data_authority_state", carried_data_authority_state),
            ("carried_resource_restriction", carried_resource_restriction),
            ("carried_lifecycle_restriction", carried_lifecycle_restriction),
            ("carried_evidence_fingerprint", carried_evidence_fingerprint),
            ("previous_state_fingerprint", previous_state_fingerprint),
            ("event_time", event_time),
            ("knowledge_time", knowledge_time),
            ("wall_receive_time", wall_receive_time),
            ("window_start", window_start),
            ("window_end", window_end),
        ):
            object.__setattr__(instance, name, value)
        object.__setattr__(instance, "_attestation", _STATE_ATTESTATION)
        instance.__post_init__(validated_lineage_prefix=validated_lineage_prefix)
        return instance

    def __post_init__(self, *, validated_lineage_prefix: int = 0) -> None:
        if (
            isinstance(validated_lineage_prefix, bool)
            or not isinstance(validated_lineage_prefix, int)
            or validated_lineage_prefix < 0
            or validated_lineage_prefix >= len(self.lineage)
        ):
            raise FeatureError("state validated lineage prefix is invalid")
        if self.feature_id not in _FEATURE_IDS:
            raise FeatureError("state feature ID is outside the exact S2A allowlist")
        if isinstance(self.feature_version, bool) or self.feature_version < 1:
            raise FeatureError("state feature version is invalid")
        _require_hash(self.feature_fingerprint, "state feature fingerprint")
        if not isinstance(self.source_field, str) or not self.source_field:
            raise FeatureError("state source field is required")
        if self.algorithm_version != RECURSIVE_STATE_VERSION:
            raise FeatureError("unsupported recursive state version")
        if self.decimal_policy_version != FEATURE_DECIMAL_POLICY_VERSION:
            raise FeatureError("unsupported recursive state Decimal policy")
        if isinstance(self.parameter_n, bool) or not isinstance(self.parameter_n, int):
            raise FeatureError("state N is invalid")
        if self.parameter_n < 2:
            raise FeatureError("state N is invalid")
        _require_hash(self.timeframe_fingerprint, "state timeframe fingerprint")
        if isinstance(self.timeframe_version, bool) or self.timeframe_version < 1:
            raise FeatureError("state timeframe version is invalid")
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
        if not self.lineage or any(
            not _is_hash(item) for item in self.lineage[validated_lineage_prefix:]
        ):
            raise FeatureError("state lineage is invalid")
        if len(set(self.lineage)) != len(self.lineage):
            raise FeatureError("state lineage must be ordered and unique")
        if not self.market_state_lineage or any(
            not _is_hash(item) for item in self.market_state_lineage[validated_lineage_prefix:]
        ):
            raise FeatureError("state market-state lineage is invalid")
        if len(self.market_state_lineage) != len(self.lineage):
            raise FeatureError("state lineage and market-state lineage lengths differ")
        if not self.authority_lineage or any(
            not _is_hash(item) for item in self.authority_lineage[validated_lineage_prefix:]
        ):
            raise FeatureError("state authority lineage is invalid")
        if len(self.authority_lineage) != len(self.lineage):
            raise FeatureError("state lineage and authority lineage lengths differ")
        if not isinstance(self.carried_market_state_trust, MarketStateTrust):
            raise FeatureError("state carried market-state trust is invalid")
        if not isinstance(self.carried_data_authority_state, DataAuthorityState):
            raise FeatureError("state carried data-authority state is invalid")
        if not isinstance(
            self.carried_resource_restriction, FeatureAxisRestriction
        ) or not isinstance(self.carried_lifecycle_restriction, FeatureAxisRestriction):
            raise FeatureError("state carried restriction axes are invalid")
        _require_hash(self.carried_evidence_fingerprint, "state carried authority evidence")
        if self.processed_samples != len(self.lineage):
            raise FeatureError("state sample count does not match its consumed lineage")
        if self.previous_state_fingerprint is not None:
            _require_hash(self.previous_state_fingerprint, "state predecessor fingerprint")
        _require_hash(self.source_generation_fingerprint, "state generation")
        if (
            not isinstance(self.source_id, StableId)
            or self.source_id.kind is not IdentityKind.EXCHANGE
            or not isinstance(self.contract_id, StableId)
            or self.contract_id.kind is not IdentityKind.INSTRUMENT
        ):
            raise FeatureError("state source identities are invalid")
        if not isinstance(self.environment, Environment):
            raise FeatureError("state environment is invalid")
        event = _utc(self.event_time, "state event time")
        knowledge = _utc(self.knowledge_time, "state knowledge time")
        wall = _utc(self.wall_receive_time, "state wall receive time")
        start = _utc(self.window_start, "state window start")
        end = _utc(self.window_end, "state window end")
        if knowledge > wall or end < start:
            raise FeatureError("state temporal bounds are invalid")
        object.__setattr__(self, "event_time", event)
        object.__setattr__(self, "knowledge_time", knowledge)
        object.__setattr__(self, "wall_receive_time", wall)
        object.__setattr__(self, "window_start", start)
        object.__setattr__(self, "window_end", end)

    def matches(self, feature: FeatureVersion, first: FeatureSample) -> bool:
        """Require the current first input to match the state context exactly."""

        return (
            self._is_attested()
            and self.feature_fingerprint == feature.fingerprint
            and self.feature_id == feature.canonical_id
            and self.feature_version == feature.version
            and self.parameter_n == (feature.parameter_n or 2)
            and self.source_id == first.source_id
            and self.contract_id == first.contract_id
            and self.environment is first.environment
            and self.source_generation_fingerprint == first.generation_fingerprint
            and self.timeframe_fingerprint == first.timeframe.fingerprint
        )

    @property
    def fingerprint(self) -> str:
        return _hash(self.to_dict(include_fingerprint=False))

    def to_dict(self, *, include_fingerprint: bool = True) -> dict[str, Any]:
        material: dict[str, Any] = {
            "feature_id": self.feature_id,
            "feature_version": self.feature_version,
            "feature_fingerprint": self.feature_fingerprint,
            "source_field": self.source_field,
            "parameter_n": self.parameter_n,
            "timeframe_fingerprint": self.timeframe_fingerprint,
            "timeframe_version": self.timeframe_version,
            "algorithm_version": self.algorithm_version,
            "decimal_policy_version": self.decimal_policy_version,
            "source": self.source_id.as_text(),
            "contract": self.contract_id.as_text(),
            "components": [value.canonical_text for value in self.components],
            "component_scales": [value.material_scale for value in self.components],
            "previous_input": self.previous_input.canonical_text if self.previous_input else None,
            "previous_close": self.previous_close.canonical_text if self.previous_close else None,
            "processed_samples": self.processed_samples,
            "lineage": self.lineage,
            "market_state_lineage": self.market_state_lineage,
            "authority_lineage": self.authority_lineage,
            "carried_market_state_trust": self.carried_market_state_trust.value,
            "carried_data_authority_state": self.carried_data_authority_state.value,
            "carried_resource_restriction": self.carried_resource_restriction.value,
            "carried_lifecycle_restriction": self.carried_lifecycle_restriction.value,
            "carried_evidence_fingerprint": self.carried_evidence_fingerprint,
            "previous_state_fingerprint": self.previous_state_fingerprint,
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
        """Rebuild an inert, unattested state from serialized material.

        The reconstructed material is revalidated and its self-fingerprint is
        recomputed, so tampering is detected.  The result is not evaluator-issued
        and cannot be resumed from until it is revalidated against recomputation.
        """

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
        source_id = StableId.parse(payload["source"])
        contract_id = StableId.parse(payload["contract"])
        if (
            source_id.kind is not IdentityKind.EXCHANGE
            or contract_id.kind is not IdentityKind.INSTRUMENT
        ):
            raise FeatureError("serialized state identities have the wrong kind")
        instance = object.__new__(cls)
        for name, value in (
            ("feature_id", payload["feature_id"]),
            ("feature_version", payload["feature_version"]),
            ("feature_fingerprint", payload["feature_fingerprint"]),
            ("source_field", payload["source_field"]),
            ("parameter_n", payload["parameter_n"]),
            ("timeframe_fingerprint", payload["timeframe_fingerprint"]),
            ("timeframe_version", payload["timeframe_version"]),
            ("algorithm_version", payload["algorithm_version"]),
            ("decimal_policy_version", payload["decimal_policy_version"]),
            ("source_id", source_id),
            ("contract_id", contract_id),
            ("environment", Environment(payload["environment"])),
            ("source_generation_fingerprint", payload["source_generation_fingerprint"]),
            ("components", components),
            ("previous_input", previous_input),
            ("previous_close", previous_close),
            ("processed_samples", payload["processed_samples"]),
            ("lineage", tuple(payload["lineage"])),
            ("market_state_lineage", tuple(payload["market_state_lineage"])),
            ("authority_lineage", tuple(payload["authority_lineage"])),
            (
                "carried_market_state_trust",
                MarketStateTrust(payload["carried_market_state_trust"]),
            ),
            (
                "carried_data_authority_state",
                DataAuthorityState(payload["carried_data_authority_state"]),
            ),
            (
                "carried_resource_restriction",
                FeatureAxisRestriction(payload["carried_resource_restriction"]),
            ),
            (
                "carried_lifecycle_restriction",
                FeatureAxisRestriction(payload["carried_lifecycle_restriction"]),
            ),
            ("carried_evidence_fingerprint", payload["carried_evidence_fingerprint"]),
            ("previous_state_fingerprint", payload.get("previous_state_fingerprint")),
            ("event_time", datetime.fromisoformat(payload["event_time"])),
            ("knowledge_time", datetime.fromisoformat(payload["knowledge_time"])),
            ("wall_receive_time", datetime.fromisoformat(payload["wall_receive_time"])),
            ("window_start", datetime.fromisoformat(payload["window_start"])),
            ("window_end", datetime.fromisoformat(payload["window_end"])),
        ):
            object.__setattr__(instance, name, value)
        object.__setattr__(instance, "_attestation", None)
        instance.__post_init__()
        if payload.get("state_fingerprint") != instance.fingerprint:
            raise FeatureError("recursive state fingerprint mismatch")
        return instance


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
    market_state_trust: MarketStateTrust
    data_authority_state: DataAuthorityState
    authority_evidence_fingerprint: str
    resource_restriction: FeatureAxisRestriction
    lifecycle_restriction: FeatureAxisRestriction
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
        if not isinstance(self.market_state_trust, MarketStateTrust):
            raise FeatureError("feature market-state trust is invalid")
        if not isinstance(self.data_authority_state, DataAuthorityState):
            raise FeatureError("feature data-authority state is invalid")
        if not isinstance(self.authority_evidence_fingerprint, str):
            raise FeatureError("feature authority evidence fingerprint is invalid")
        _require_hash(self.authority_evidence_fingerprint, "feature authority evidence")
        if not isinstance(self.resource_restriction, FeatureAxisRestriction) or not isinstance(
            self.lifecycle_restriction, FeatureAxisRestriction
        ):
            raise FeatureError("feature restriction axes are invalid")
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
                "market_state_trust": self.market_state_trust.value,
                "data_authority_state": self.data_authority_state.value,
                "authority_evidence": self.authority_evidence_fingerprint,
                "resource_restriction": self.resource_restriction.value,
                "lifecycle_restriction": self.lifecycle_restriction.value,
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
        axes = {
            (
                value.market_state_trust,
                value.data_authority_state,
                value.authority_evidence_fingerprint,
                value.resource_restriction,
                value.lifecycle_restriction,
            )
            for value in self.values
        }
        if len(axes) != 1:
            raise FeatureError("snapshot values do not share one authority axis identity")
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
                "axes": tuple(
                    sorted(
                        {
                            (
                                value.market_state_trust.value,
                                value.data_authority_state.value,
                                value.authority_evidence_fingerprint,
                                value.resource_restriction.value,
                                value.lifecycle_restriction.value,
                            )
                            for value in self.values
                        }
                    )
                ),
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


def _authority_summary(
    samples: Sequence[FeatureSample],
    prior: RecursiveAccumulatorState | None = None,
) -> tuple[
    MarketStateTrust,
    DataAuthorityState,
    FeatureAxisRestriction,
    FeatureAxisRestriction,
    str,
]:
    """Take the most restrictive axis value across inputs; never upgrade.

    When a predecessor state is present its carried axes are folded in, so a
    resume cannot widen market-state trust, data authority, resource admission
    or universe lifecycle eligibility.
    """

    trust = min(
        (sample.authority.market_state_trust for sample in samples),
        key=_TRUST_SEVERITY.index,
    )
    authority = min(
        (sample.authority.data_authority_state for sample in samples),
        key=_AUTHORITY_SEVERITY.index,
    )
    resource = (
        FeatureAxisRestriction.RESTRICTIVE
        if any(
            sample.authority.resource_restriction is FeatureAxisRestriction.RESTRICTIVE
            for sample in samples
        )
        else FeatureAxisRestriction.NONE
    )
    lifecycle = (
        FeatureAxisRestriction.RESTRICTIVE
        if any(
            sample.authority.lifecycle_axis is FeatureAxisRestriction.RESTRICTIVE
            for sample in samples
        )
        else FeatureAxisRestriction.NONE
    )
    evidence: dict[str, object] = {"ordered": [sample.authority.fingerprint for sample in samples]}
    if prior is not None:
        trust = min((trust, prior.carried_market_state_trust), key=_TRUST_SEVERITY.index)
        authority = min(
            (authority, prior.carried_data_authority_state), key=_AUTHORITY_SEVERITY.index
        )
        if prior.carried_resource_restriction is FeatureAxisRestriction.RESTRICTIVE:
            resource = FeatureAxisRestriction.RESTRICTIVE
        if prior.carried_lifecycle_restriction is FeatureAxisRestriction.RESTRICTIVE:
            lifecycle = FeatureAxisRestriction.RESTRICTIVE
        evidence["prior"] = prior.carried_evidence_fingerprint
    return trust, authority, resource, lifecycle, _hash(evidence)


def _context_status(
    samples: Sequence[FeatureSample], evaluation_time: datetime | None
) -> tuple[FeatureValidity | None, str, MarketStateTrust]:
    """Map market-truth evidence to analytical validity only.

    Resource admission and universe lifecycle never falsify otherwise valid
    analytical truth; they travel as separate restrictive axes.
    """

    if not samples:
        return FeatureValidity.WARMUP, "NO_INPUT_SAMPLES", MarketStateTrust.TRUSTED
    first = samples[0]
    trust = min(
        (sample.authority.market_state_trust for sample in samples),
        key=_TRUST_SEVERITY.index,
    )
    first_source = (first.source_id.kind, first.source_id.value)
    first_contract = (first.contract_id.kind, first.contract_id.value)
    first_timeframe = first.timeframe
    for sample in samples:
        if (
            (sample.source_id.kind, sample.source_id.value) != first_source
            or (sample.contract_id.kind, sample.contract_id.value) != first_contract
            or sample.environment is not first.environment
            or sample.generation_fingerprint != first.generation_fingerprint
            or sample.timeframe != first_timeframe
        ):
            return (
                FeatureValidity.INVALID,
                "MIXED_SOURCE_CONTRACT_ENVIRONMENT_GENERATION_OR_TIMEFRAME",
                trust,
            )
    for previous, current in zip(samples[:-1], samples[1:], strict=False):
        previous_start = previous.interval_start or previous.event_time
        current_start = current.interval_start or current.event_time
        if current_start <= previous_start or current.event_time <= previous.event_time:
            return (
                FeatureValidity.INVALID,
                "NON_MONOTONIC_OR_DUPLICATE_SAMPLE_ORDER",
                trust,
            )
    if evaluation_time is not None:
        boundary = _utc(evaluation_time, "evaluation time")
        if any(
            sample.event_time > boundary or sample.knowledge_time > boundary for sample in samples
        ):
            return (
                FeatureValidity.INVALID,
                "FUTURE_EVENT_OR_KNOWLEDGE_EVIDENCE",
                trust,
            )
    if any(
        _INVALID_QUALITY_REASONS.intersection(sample.authority.data_authority_reasons)
        for sample in samples
    ):
        return FeatureValidity.INVALID, "CONTRADICTORY_OR_RETIRED_MARKET_TRUTH", trust
    if trust in {
        MarketStateTrust.UNKNOWN,
        MarketStateTrust.UNTRUSTED,
        MarketStateTrust.RESYNC_REQUIRED,
    } or any(
        _UNKNOWN_QUALITY_REASONS.intersection(sample.authority.data_authority_reasons)
        for sample in samples
    ):
        return FeatureValidity.UNKNOWN, "UPSTREAM_MARKET_STATE_UNTRUSTED", trust
    if any(not sample.closed for sample in samples):
        return FeatureValidity.WARMUP, "CLOSED_INPUT_REQUIRED", trust
    if trust is MarketStateTrust.DEGRADED:
        return FeatureValidity.DEGRADED, "UPSTREAM_MARKET_STATE_DEGRADED", trust
    return None, "", trust


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
    prior_authority = previous_state.authority_lineage if previous_state else ()
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
    carried = _authority_summary(new_samples, previous_state)
    return RecursiveAccumulatorState._from_evaluator(
        feature=feature,
        sample=sample,
        components=canonical_components,
        previous_input=previous,
        previous_close=previous_close,
        processed_samples=(previous_state.processed_samples if previous_state else 0)
        + len(new_samples),
        lineage=lineage,
        market_state_lineage=prior_market_states
        + tuple(item.market_state_fingerprint for item in new_samples),
        authority_lineage=prior_authority
        + tuple(item.authority.fingerprint for item in new_samples),
        carried_market_state_trust=carried[0],
        carried_data_authority_state=carried[1],
        carried_resource_restriction=carried[2],
        carried_lifecycle_restriction=carried[3],
        carried_evidence_fingerprint=carried[4],
        previous_state_fingerprint=(
            previous_state.fingerprint if previous_state is not None else None
        ),
        validated_lineage_prefix=(len(previous_state.lineage) if previous_state is not None else 0),
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
    previous_state: RecursiveAccumulatorState | None = None,
) -> FeatureValue:
    first = samples[0]
    carried = recursive_state if recursive_state is not None else previous_state
    if carried is not None:
        # The carried summary already folds every consumed sample, so a resume
        # cannot widen any axis and the output fingerprint is path independent.
        trust = carried.carried_market_state_trust
        authority = carried.carried_data_authority_state
        resource = carried.carried_resource_restriction
        lifecycle = carried.carried_lifecycle_restriction
        evidence = carried.carried_evidence_fingerprint
    else:
        trust, authority, resource, lifecycle, evidence = _authority_summary(samples)
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
        market_state_trust=trust,
        data_authority_state=authority,
        authority_evidence_fingerprint=evidence,
        resource_restriction=resource,
        lifecycle_restriction=lifecycle,
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
        return (
            _rsi_output(avg_gain, avg_loss).value,
            "COMPUTED",
            (_canonical(avg_gain), _canonical(avg_loss)),
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


def _validate_resume_state(
    feature: FeatureVersion,
    state: RecursiveAccumulatorState | None,
    values: Sequence[FeatureSample],
) -> None:
    """Require an evaluator-issued state bound to the resumed context."""

    if state is None:
        return
    if not state._is_attested():
        raise FeatureEvaluationError("resume state is not evaluator-issued")
    if state.feature_fingerprint != feature.fingerprint:
        raise FeatureEvaluationError("resume state belongs to another feature version")
    if state.feature_id != feature.canonical_id or state.feature_version != feature.version:
        raise FeatureEvaluationError("resume state feature identity disagrees")
    if state.parameter_n != (feature.parameter_n or 2):
        raise FeatureEvaluationError("resume state N disagrees with the feature definition")
    if state.algorithm_version != RECURSIVE_STATE_VERSION:
        raise FeatureEvaluationError("resume state algorithm version is unsupported")
    if state.decimal_policy_version != FEATURE_DECIMAL_POLICY_VERSION:
        raise FeatureEvaluationError("resume state Decimal policy is unsupported")
    if values and not state.matches(feature, values[0]):
        raise FeatureEvaluationError(
            "resume state source, contract, environment, generation or timeframe disagrees"
        )


def _evaluate_steps(
    feature: FeatureVersion,
    values: tuple[FeatureSample, ...],
    evaluation_time: datetime | None,
    initial_state: RecursiveAccumulatorState | None,
    *,
    emit_series: bool,
) -> list[FeatureValue]:
    """Run the single incremental evaluation loop for one feature.

    ``emit_series`` materializes one output per observed sample; the batch entry
    point reuses the identical loop and materializes only the final step.  Both
    paths therefore share values, canonical components and state fingerprints by
    construction instead of by coincidence.
    """

    outputs: list[FeatureValue] = []
    state = initial_state
    prior_lineage = initial_state.lineage if initial_state is not None else ()
    prior_count = initial_state.processed_samples if initial_state is not None else 0
    required = _required_count(feature)
    last_index = len(values) - 1
    content_fingerprints = tuple(item.content_fingerprint for item in values)
    for index in range(len(values)):
        prefix = values[: index + 1]
        context_status, context_reason, trust = _context_status(prefix, evaluation_time)
        lineage = prior_lineage + content_fingerprints[: index + 1]
        total_count = prior_count + index + 1
        emit = emit_series or index == last_index
        if context_status is not None and context_status is not FeatureValidity.DEGRADED:
            if emit:
                outputs.append(
                    _build_output(feature, prefix, None, context_status, context_reason, lineage)
                )
            continue
        if total_count < required:
            if emit:
                outputs.append(
                    _build_output(
                        feature,
                        prefix,
                        None,
                        FeatureValidity.WARMUP,
                        "INSUFFICIENT_REQUIRED_SAMPLES",
                        lineage,
                    )
                )
            continue
        try:
            numeric, reason, components = _compute_numeric(feature, prefix, state)
        except (FeatureEvaluationError, NumericPolicyError, InvalidOperation, ValueError) as exc:
            if emit:
                outputs.append(
                    _build_output(feature, prefix, None, FeatureValidity.INVALID, str(exc), lineage)
                )
            continue
        if numeric is None:
            if emit:
                outputs.append(
                    _build_output(feature, prefix, None, FeatureValidity.INVALID, reason, lineage)
                )
            continue
        output = _safe_canonical(numeric)
        if output is None:
            if emit:
                outputs.append(
                    _build_output(
                        feature,
                        prefix,
                        None,
                        FeatureValidity.INVALID,
                        "CANONICAL_DECIMAL_OVERFLOW",
                        lineage,
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
            FeatureValidity.DEGRADED
            if trust is MarketStateTrust.DEGRADED
            else FeatureValidity.VALID
        )
        if emit:
            outputs.append(_build_output(feature, prefix, output, validity, reason, lineage, state))
    return outputs


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
    _validate_resume_state(feature, initial_state, values)
    return tuple(_evaluate_steps(feature, values, evaluation_time, initial_state, emit_series=True))


def evaluate_feature(
    feature: FeatureVersion,
    samples: Iterable[FeatureSample | CandleBar | DecimalValue | str | int | Decimal],
    *,
    evaluation_time: datetime | None = None,
    initial_state: RecursiveAccumulatorState | None = None,
) -> FeatureValue:
    """Evaluate one feature and return the latest point-in-time result.

    This is the final step of the same incremental evaluation used by
    :func:`evaluate_feature_series`, so batch, series and resumed replay can
    never disagree on values, canonical components or state fingerprints.
    """

    if not isinstance(feature, FeatureVersion):
        raise FeatureEvaluationError("FeatureVersion is required")
    inputs = _coerce_samples(samples)
    if not inputs:
        raise FeatureEvaluationError("at least one sample is required")
    _validate_resume_state(feature, initial_state, inputs)
    return _evaluate_steps(feature, inputs, evaluation_time, initial_state, emit_series=False)[-1]


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


@dataclass(frozen=True, slots=True, init=False)
class AlignedWindowEvidence:
    """Evaluator-issued derived 5m/15m analytical evidence.

    Every material field is recomputed by the evaluator from the exact ordered
    constituents, so a caller cannot mint VALID/DEGRADED evidence or disagree
    with constituent identity, values, times, provenance or authority axes.
    """

    target_minutes: int
    target_timeframe_fingerprint: str
    start: datetime
    end: datetime
    constituents: tuple[CandleBar, ...]
    constituent_fingerprints: tuple[str, ...]
    constituent_provenance_fingerprints: tuple[str, ...]
    authority_evidence_fingerprints: tuple[str, ...]
    authority_fold_fingerprint: str
    data_authority_state: DataAuthorityState
    constituent_market_state_trust: MarketStateTrust
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
    resource_restriction: FeatureAxisRestriction
    lifecycle_restriction: FeatureAxisRestriction
    provenance: str
    _attestation: object = field(default=None, repr=False, compare=False)

    def __init__(self, *args: object, **kwargs: object) -> None:
        raise FeatureError("AlignedWindowEvidence must be issued by align_closed_1m_candles")

    def _is_attested(self) -> bool:
        return self._attestation is _ALIGNED_ATTESTATION

    @classmethod
    def _from_evaluator(cls, **material: Any) -> AlignedWindowEvidence:
        instance = object.__new__(cls)
        for name, value in material.items():
            object.__setattr__(instance, name, value)
        object.__setattr__(instance, "_attestation", _ALIGNED_ATTESTATION)
        instance.__post_init__()
        return instance

    def __post_init__(self) -> None:
        if self.target_minutes not in {5, 15}:
            raise FeatureError("only deterministic 5m and 15m alignment is authorized")
        _require_hash(self.target_timeframe_fingerprint, "aligned target timeframe fingerprint")
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
        if self.lineage != self.constituent_fingerprints:
            raise FeatureError("aligned lineage is not bound to the exact ordered constituents")
        if not (
            len(self.constituent_provenance_fingerprints)
            == len(self.authority_evidence_fingerprints)
            == len(self.constituent_fingerprints)
        ):
            raise FeatureError("aligned constituent evidence lengths disagree")
        for item in self.constituent_provenance_fingerprints:
            _require_hash(item, "aligned constituent provenance")
        for item in self.authority_evidence_fingerprints:
            _require_hash(item, "aligned authority evidence")
        _require_hash(self.authority_fold_fingerprint, "aligned authority fold")
        if not isinstance(self.data_authority_state, DataAuthorityState):
            raise FeatureError("aligned data-authority state is invalid")
        if not isinstance(self.constituent_market_state_trust, MarketStateTrust):
            raise FeatureError("aligned constituent market-state trust is invalid")
        if not isinstance(self.resource_restriction, FeatureAxisRestriction) or not isinstance(
            self.lifecycle_restriction, FeatureAxisRestriction
        ):
            raise FeatureError("aligned restriction axes are invalid")
        if self.provenance != DERIVED_MTF_PROVENANCE:
            raise FeatureError("unsupported derived provenance")
        for attr, label in (
            ("event_time", "aligned event time"),
            ("knowledge_time", "aligned knowledge time"),
            ("wall_receive_time", "aligned wall receive time"),
        ):
            value = getattr(self, attr)
            if value is not None:
                object.__setattr__(self, attr, _utc(value, label))

    @property
    def fingerprint(self) -> str:
        return _hash(
            {
                "target_minutes": self.target_minutes,
                "target_timeframe": self.target_timeframe_fingerprint,
                "start": self.start.isoformat(),
                "end": self.end.isoformat(),
                "constituents": self.constituent_fingerprints,
                "constituent_provenance": self.constituent_provenance_fingerprints,
                "authority_evidence": self.authority_evidence_fingerprints,
                "authority_fold": self.authority_fold_fingerprint,
                "data_authority_state": self.data_authority_state.value,
                "constituent_market_state_trust": self.constituent_market_state_trust.value,
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
                "resource_restriction": self.resource_restriction.value,
                "lifecycle_restriction": self.lifecycle_restriction.value,
                "provenance": self.provenance,
            }
        )


def _aligned_bounds(start: datetime, target_minutes: int) -> tuple[datetime, datetime]:
    seconds = target_minutes * 60
    epoch = int(start.timestamp())
    aligned = epoch - (epoch % seconds)
    begin = datetime.fromtimestamp(aligned, tz=UTC)
    return begin, begin + timedelta(seconds=seconds)


def _fold_constituent_authority(
    authorities: Sequence[FeatureAuthorityEvidence],
) -> tuple[
    MarketStateTrust,
    DataAuthorityState,
    FeatureAxisRestriction,
    FeatureAxisRestriction,
    str,
]:
    """Fold every exact constituent authority without upgrading any axis."""

    if not authorities:
        raise FeatureEvaluationError("per-constituent authority evidence is required")
    trust = min((item.market_state_trust for item in authorities), key=_TRUST_SEVERITY.index)
    data_authority = min(
        (item.data_authority_state for item in authorities), key=_AUTHORITY_SEVERITY.index
    )
    resource = (
        FeatureAxisRestriction.RESTRICTIVE
        if any(
            item.resource_restriction is FeatureAxisRestriction.RESTRICTIVE for item in authorities
        )
        else FeatureAxisRestriction.NONE
    )
    lifecycle = (
        FeatureAxisRestriction.RESTRICTIVE
        if any(item.lifecycle_axis is FeatureAxisRestriction.RESTRICTIVE for item in authorities)
        else FeatureAxisRestriction.NONE
    )
    fingerprint = _hash({"ordered_authority": [item.fingerprint for item in authorities]})
    return trust, data_authority, resource, lifecycle, fingerprint


def _constituent_market_truth_status(
    authorities: Sequence[FeatureAuthorityEvidence],
) -> tuple[FeatureValidity | None, str]:
    """Governed H012 restriction from the folded constituent market truth."""

    trust = min((item.market_state_trust for item in authorities), key=_TRUST_SEVERITY.index)
    reasons = {reason for item in authorities for reason in item.data_authority_reasons}
    if reasons & _INVALID_QUALITY_REASONS:
        return FeatureValidity.INVALID, "CONTRADICTORY_OR_RETIRED_CONSTITUENT_MARKET_TRUTH"
    if trust in {
        MarketStateTrust.UNKNOWN,
        MarketStateTrust.UNTRUSTED,
        MarketStateTrust.RESYNC_REQUIRED,
    } or (reasons & _UNKNOWN_QUALITY_REASONS):
        return FeatureValidity.UNKNOWN, "CONSTITUENT_MARKET_STATE_UNTRUSTED"
    if trust is MarketStateTrust.DEGRADED:
        return FeatureValidity.DEGRADED, "CONSTITUENT_MARKET_STATE_DEGRADED"
    return None, ""


def _bound_constituent_authorities(
    items: tuple[CandleBar, ...],
    authorities: Sequence[FeatureAuthorityEvidence] | None,
) -> tuple[FeatureAuthorityEvidence, ...]:
    """Require one exact canonical authority binding per 1m constituent."""

    if authorities is None:
        if any(item.context.environment is not Environment.REPLAY for item in items):
            raise FeatureEvaluationError(
                "authoritative aligned windows require per-constituent authority evidence"
            )
        return tuple(FeatureAuthorityEvidence.fixture_for_candle(item) for item in items)
    if isinstance(authorities, (str, bytes)) or not isinstance(authorities, Sequence):
        raise FeatureEvaluationError("per-constituent authority evidence must be a sequence")
    resolved = tuple(authorities)
    if len(resolved) != len(items):
        raise FeatureEvaluationError(
            "per-constituent authority evidence must match the constituent count"
        )
    for candle, item in zip(items, resolved, strict=True):
        if not isinstance(item, FeatureAuthorityEvidence):
            raise FeatureEvaluationError("per-constituent authority evidence is not typed")
        if not item._is_attested():
            raise FeatureEvaluationError("per-constituent authority is not evaluator-issued")
        context = candle.context
        if not item.matches_identity(
            source_id=context.source_id,
            contract_id=context.contract_id,
            environment=context.environment,
            generation_fingerprint=context.generation.fingerprint,
        ):
            raise FeatureEvaluationError(
                "per-constituent authority identity disagrees with its candle"
            )
        if item.is_fixture and context.environment is not Environment.REPLAY:
            raise FeatureEvaluationError("synthetic per-constituent authority is REPLAY-only")
        if item.bound_evidence_fingerprint != _hash(_candle_value_evidence_material(candle)):
            raise FeatureEvaluationError(
                "per-constituent authority is not bound to its exact candle evidence"
            )
    return resolved


def align_closed_1m_candles(
    candles: Iterable[CandleBar],
    target_minutes: int,
    *,
    evaluation_time: datetime | None = None,
    authorities: Sequence[FeatureAuthorityEvidence] | None = None,
) -> AlignedWindowEvidence:
    """Derive one exact 5m/15m window from complete CLOSED 1m constituents.

    Authority is bound per constituent: a single state can never blanket an
    entire window, so an earlier degraded, unknown or restrictive constituent
    cannot be hidden by a later trusted one.
    """

    if target_minutes not in {5, 15}:
        raise FeatureEvaluationError("target timeframe must be 5 or 15 minutes")
    target_frame = Timeframe(f"Min{target_minutes}", target_minutes * 60)
    items = tuple(candles)
    if not items:
        now = _utc(evaluation_time or datetime(1970, 1, 1, tzinfo=UTC), "evaluation time")
        start, end = _aligned_bounds(now, target_minutes)
        return AlignedWindowEvidence._from_evaluator(
            target_minutes=target_minutes,
            target_timeframe_fingerprint=target_frame.fingerprint,
            start=start,
            end=end,
            constituents=(),
            constituent_fingerprints=(),
            constituent_provenance_fingerprints=(),
            authority_evidence_fingerprints=(),
            authority_fold_fingerprint=_hash({"ordered_authority": []}),
            data_authority_state=DataAuthorityState.ALLOW_NEW_EXPOSURE,
            constituent_market_state_trust=MarketStateTrust.TRUSTED,
            validity=FeatureValidity.WARMUP,
            reason="NO_CONSTITUENTS",
            source_id=None,
            contract_id=None,
            environment=None,
            generation_fingerprint=None,
            open=None,
            high=None,
            low=None,
            close=None,
            volume=None,
            event_time=None,
            knowledge_time=None,
            wall_receive_time=None,
            lineage=(),
            resource_restriction=FeatureAxisRestriction.NONE,
            lifecycle_restriction=FeatureAxisRestriction.NONE,
            provenance=DERIVED_MTF_PROVENANCE,
        )
    first = items[0]
    start, end = _aligned_bounds(first.start, target_minutes)
    constituent_fingerprints = tuple(item.fingerprint for item in items)
    provenance_fingerprints = tuple(item.context.provenance_fingerprint for item in items)
    resolved_authorities = _bound_constituent_authorities(items, authorities)
    trust, data_authority, resource, lifecycle, authority_fold = _fold_constituent_authority(
        resolved_authorities
    )
    base_kwargs: dict[str, Any] = dict(
        target_minutes=target_minutes,
        target_timeframe_fingerprint=target_frame.fingerprint,
        start=start,
        end=end,
        constituents=items,
        constituent_fingerprints=constituent_fingerprints,
        constituent_provenance_fingerprints=provenance_fingerprints,
        authority_evidence_fingerprints=tuple(item.fingerprint for item in resolved_authorities),
        authority_fold_fingerprint=authority_fold,
        data_authority_state=data_authority,
        constituent_market_state_trust=trust,
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
        lineage=constituent_fingerprints,
        resource_restriction=resource,
        lifecycle_restriction=lifecycle,
        provenance=DERIVED_MTF_PROVENANCE,
    )
    expected = target_minutes
    boundary = _utc(evaluation_time, "evaluation time") if evaluation_time is not None else None
    if any(
        item.timeframe.duration_seconds != 60 or item.finality is not Finality.CLOSED
        for item in items
    ):
        return AlignedWindowEvidence._from_evaluator(
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
        return AlignedWindowEvidence._from_evaluator(
            **base_kwargs, validity=FeatureValidity.INVALID, reason="FUTURE_CONSTITUENT_EVIDENCE"
        )
    if any(item.start < start or item.end > end for item in items):
        return AlignedWindowEvidence._from_evaluator(
            **base_kwargs,
            validity=FeatureValidity.INVALID,
            reason="CONSTITUENT_OUTSIDE_ALIGNED_WINDOW",
        )
    if items != tuple(sorted(items, key=lambda item: item.start)):
        return AlignedWindowEvidence._from_evaluator(
            **base_kwargs, validity=FeatureValidity.INVALID, reason="OUT_OF_ORDER_CONSTITUENTS"
        )
    market_truth_status, market_truth_reason = _constituent_market_truth_status(
        resolved_authorities
    )
    if market_truth_status in {FeatureValidity.INVALID, FeatureValidity.UNKNOWN}:
        return AlignedWindowEvidence._from_evaluator(
            **base_kwargs, validity=market_truth_status, reason=market_truth_reason
        )
    if len(items) != expected:
        validity = (
            FeatureValidity.WARMUP
            if boundary is None or boundary < end
            else FeatureValidity.UNKNOWN
        )
        return AlignedWindowEvidence._from_evaluator(
            **base_kwargs, validity=validity, reason="INCOMPLETE_ALIGNED_WINDOW"
        )
    for left, right in zip(items[:-1], items[1:], strict=False):
        if left.end != right.start:
            return AlignedWindowEvidence._from_evaluator(
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
            return AlignedWindowEvidence._from_evaluator(
                **base_kwargs,
                validity=FeatureValidity.INVALID,
                reason="MIXED_IDENTITY_OR_QUANTITY_CONTRACT",
            )
    if items[0].start != start or items[-1].end != end:
        return AlignedWindowEvidence._from_evaluator(
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
    except (NumericPolicyError, InvalidOperation, ValueError) as exc:
        return AlignedWindowEvidence._from_evaluator(
            **base_kwargs, validity=FeatureValidity.INVALID, reason=str(exc)
        )
    return AlignedWindowEvidence._from_evaluator(
        **{
            **base_kwargs,
            "open": open_value,
            "high": _canonical(high_value),
            "low": _canonical(low_value),
            "close": close_value,
            "volume": volume,
            "validity": (
                FeatureValidity.DEGRADED
                if market_truth_status is FeatureValidity.DEGRADED
                else FeatureValidity.VALID
            ),
            "reason": "COMPLETE_COHERENT_ALIGNED_WINDOW",
        }
    )


def align_candles(
    candles: Iterable[CandleBar],
    target_minutes: int,
    *,
    evaluation_time: datetime | None = None,
    authorities: Sequence[FeatureAuthorityEvidence] | None = None,
) -> AlignedWindowEvidence:
    """Short alias for the public deterministic MTF alignment operation."""

    return align_closed_1m_candles(
        candles,
        target_minutes,
        evaluation_time=evaluation_time,
        authorities=authorities,
    )


def restore_recursive_state(
    feature: FeatureVersion,
    payload: str | Mapping[str, Any],
    *,
    consumed_inputs: Iterable[FeatureSample | CandleBar | DecimalValue | str | int | Decimal],
) -> RecursiveAccumulatorState:
    """Re-issue an evaluator-attested state from serialized material.

    The canonical state is recomputed from the exact ordered inputs the
    serialized state claims to have consumed; the payload is accepted only when
    every material field, the ordered input and authority lineage and the
    predecessor-chain link agree with that recomputation.  Anything else fails
    closed instead of resuming from caller-controlled material.
    """

    if not isinstance(feature, FeatureVersion):
        raise FeatureEvaluationError("FeatureVersion is required")
    if feature.canonical_id not in _RECURSIVE_FEATURES:
        raise FeatureEvaluationError("serialized resume requires a recursive feature")
    inputs = _coerce_samples(consumed_inputs)
    if not inputs:
        raise FeatureEvaluationError("serialized resume requires the consumed inputs")
    context_status, context_reason, _ = _context_status(inputs, None)
    if context_status is not None and context_status is not FeatureValidity.DEGRADED:
        raise FeatureEvaluationError(
            f"serialized resume inputs are not admissible: {context_reason}"
        )
    if len(inputs) < _required_count(feature):
        raise FeatureEvaluationError("serialized resume inputs are below the required cardinality")
    submitted = RecursiveAccumulatorState.deserialize(payload)
    if submitted.feature_fingerprint != feature.fingerprint:
        raise FeatureEvaluationError("serialized state belongs to another feature version")
    canonical = evaluate_feature_series(feature, inputs)[-1].recursive_state
    if canonical is None:
        raise FeatureError("serialized recursive state could not be recomputed")
    if submitted.to_dict(include_fingerprint=False) != canonical.to_dict(include_fingerprint=False):
        raise FeatureError("serialized recursive state disagrees with recomputation")
    return canonical


__all__ = [
    "AlignedWindowEvidence",
    "DERIVED_MTF_PROVENANCE",
    "FEATURE_ALGORITHM_VERSION",
    "FEATURE_AUTHORITY_VERSION",
    "FEATURE_DECIMAL_POLICY_VERSION",
    "FeatureAuthorityEvidence",
    "FeatureAxisRestriction",
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
    "restore_recursive_state",
]
