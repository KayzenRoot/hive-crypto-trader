"""Deterministic, provider-neutral Module 9 candlestick pattern evidence.

This module consumes immutable S1E/S1F/S2A evidence only.  It derives
point-in-time analytical pattern evidence for exactly six frozen public/standard
candlestick patterns.  It does not open transports, persist state, create orders,
produce downstream decisions or grant authority.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from decimal import ROUND_HALF_EVEN, Decimal, localcontext
from enum import StrEnum
from typing import Any, Final, Self

from hct_backend.contracts import Environment, IdentityKind, StableId
from hct_backend.features import (
    FeatureAuthorityEvidence,
    FeatureAxisRestriction,
    FeatureSample,
)
from hct_backend.market_truth import (
    DataAuthorityState,
    LifecycleRestriction,
    MarketStateTrust,
    ResourceDisposition,
)
from hct_backend.s1f_numeric import DecimalValue
from hct_backend.s1f_values import CandleBar, Finality, Timeframe

PATTERN_ALGORITHM_VERSION: Final = "S2B_STANDARD_CANDLESTICK_PATTERNS_V1"
PATTERN_DEFINITION_VERSION: Final = 1
PATTERN_DECIMAL_POLICY_VERSION: Final = "FEATURE_DECIMAL_V1"
PATTERN_FINGERPRINT_VERSION: Final = "S2B_SHA256_CANONICAL_JSON_V1"
PATTERN_EVIDENCE_VERSION: Final = "S2B_PATTERN_EVIDENCE_V1"
SMALL_BODY_MAX: Final = Decimal("0.10")
LONG_BODY_MIN: Final = Decimal("0.90")
_ALIGNMENT: Final = "UNIX_EPOCH_MULTIPLES"

PATTERN_ALLOWLIST: Final = (
    "P-DC-001",
    "P-MB-001",
    "P-EC-001",
    "P-EC-002",
    "P-MS-001",
    "P-ES-001",
)
_PATTERN_IDS: Final = frozenset(PATTERN_ALLOWLIST)
_PATTERN_BAR_CARDINALITY: Final = {
    "P-DC-001": 1,
    "P-MB-001": 1,
    "P-EC-001": 2,
    "P-EC-002": 2,
    "P-MS-001": 3,
    "P-ES-001": 3,
}
_PATTERN_FAMILIES: Final = {
    "P-DC-001": "SINGLE_BAR",
    "P-MB-001": "SINGLE_BAR",
    "P-EC-001": "TWO_BAR_REVERSAL",
    "P-EC-002": "TWO_BAR_REVERSAL",
    "P-MS-001": "THREE_BAR_REVERSAL",
    "P-ES-001": "THREE_BAR_REVERSAL",
}
_TIMEFRAME_ALLOWLIST: Final = ("Min1", "Min5", "Min15")
# Structural timeframe identity: name -> (duration_seconds, version, alignment).
_TIMEFRAME_IDENTITY: Final = {
    "Min1": (60, 1, _ALIGNMENT),
    "Min5": (300, 1, _ALIGNMENT),
    "Min15": (900, 1, _ALIGNMENT),
}
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
_EVIDENCE_ATTESTATION: Final = object()


class PatternError(ValueError):
    """Base failure for an invalid or contradictory pattern contract."""


class PatternRegistryError(PatternError):
    """Raised when a registry operation would silently redefine behavior."""


class PatternEvaluationError(PatternError):
    """Raised only for malformed evaluator inputs, never for restrictive output states."""


class PatternValidity(StrEnum):
    """Local analytical validity axis for Module 9 pattern evidence."""

    VALID = "VALID"
    DEGRADED = "DEGRADED"
    WARMUP = "WARMUP"
    UNKNOWN = "UNKNOWN"
    INVALID = "INVALID"


class PatternMatchState(StrEnum):
    """Whether the named pattern actually occurred, kept separate from validity."""

    MATCHED = "MATCHED"
    NOT_MATCHED = "NOT_MATCHED"
    INDETERMINATE = "INDETERMINATE"


class PatternDirection(StrEnum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"
    NONE = "NONE"
    UNKNOWN = "UNKNOWN"


def _hash(material: object) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _require_hash(value: str, label: str) -> None:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(character not in "0123456789abcdef" for character in value)
    ):
        raise PatternError(f"{label} must be a lowercase SHA-256 fingerprint")


def _utc(value: datetime, label: str) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise PatternError(f"{label} must be timezone-aware")
    return value.astimezone(UTC)


def _authorized_frame(frame: Timeframe) -> bool:
    expected = _TIMEFRAME_IDENTITY.get(frame.name)
    if expected is None:
        return False
    duration, version, alignment = expected
    return (
        frame.duration_seconds == duration
        and frame.version == version
        and frame.alignment == alignment
    )


def _evaluation_context():
    """Fixed Decimal evaluation context: precision 76, ROUND_HALF_EVEN."""

    context = localcontext()
    entered = context.__enter__()
    entered.prec = 76
    entered.rounding = ROUND_HALF_EVEN
    return context


def _body_ratio(open_value: Decimal, high: Decimal, low: Decimal, close: Decimal) -> Decimal | None:
    """Canonical body/range ratio; ``None`` when the bar range is degenerate."""

    rng = high - low
    if rng == 0:
        return None
    body = abs(close - open_value)
    with _evaluation_context():
        return body / rng


def _midpoint(left: Decimal, right: Decimal) -> Decimal:
    with _evaluation_context():
        return (left + right) / Decimal(2)


@dataclass(frozen=True, slots=True)
class PatternDefinition:
    """Immutable behaviorally material pattern definition."""

    canonical_id: str
    version: int
    family: str
    bar_cardinality: int
    algorithm_version: str = PATTERN_ALGORITHM_VERSION
    decimal_policy_version: str = PATTERN_DECIMAL_POLICY_VERSION
    fingerprint_version: str = PATTERN_FINGERPRINT_VERSION
    small_body_max: Decimal = SMALL_BODY_MAX
    long_body_min: Decimal = LONG_BODY_MIN
    engulfing_bounds: str = "BOUNDS_INCLUSIVE"
    midpoint_equality: str = "BOUNDS_INCLUSIVE"
    star_gap_policy: str = "NONE_IN_V1"
    timeframe_allowlist: tuple[str, ...] = _TIMEFRAME_ALLOWLIST
    rounding_mode: str = "ROUND_HALF_EVEN"

    def __post_init__(self) -> None:
        if self.canonical_id not in _PATTERN_IDS:
            raise PatternError("pattern ID is outside the exact S2B allowlist")
        if isinstance(self.version, bool) or not isinstance(self.version, int) or self.version < 1:
            raise PatternError("pattern version must be positive")
        if self.version != PATTERN_DEFINITION_VERSION:
            raise PatternError("unsupported pattern definition version")
        if self.family != _PATTERN_FAMILIES[self.canonical_id]:
            raise PatternError("pattern family disagrees with its canonical ID")
        if self.bar_cardinality != _PATTERN_BAR_CARDINALITY[self.canonical_id]:
            raise PatternError("pattern bar cardinality disagrees with its canonical ID")
        if self.algorithm_version != PATTERN_ALGORITHM_VERSION:
            raise PatternError("unsupported pattern algorithm version")
        if self.decimal_policy_version != PATTERN_DECIMAL_POLICY_VERSION:
            raise PatternError("unsupported Decimal policy")
        if self.fingerprint_version != PATTERN_FINGERPRINT_VERSION:
            raise PatternError("unsupported fingerprint version")
        if not isinstance(self.small_body_max, Decimal) or not isinstance(
            self.long_body_min, Decimal
        ):
            raise PatternError("pattern body thresholds must be Decimal")
        if self.small_body_max != SMALL_BODY_MAX or self.long_body_min != LONG_BODY_MIN:
            raise PatternError("pattern body thresholds are frozen for V1")
        if self.engulfing_bounds != "BOUNDS_INCLUSIVE":
            raise PatternError("engulfing bounds must be inclusive")
        if self.midpoint_equality != "BOUNDS_INCLUSIVE":
            raise PatternError("star midpoint equality must be inclusive")
        if self.star_gap_policy != "NONE_IN_V1":
            raise PatternError("V1 imposes no star gap requirement")
        if self.timeframe_allowlist != _TIMEFRAME_ALLOWLIST:
            raise PatternError("unsupported structural timeframe allowlist")
        if self.rounding_mode != "ROUND_HALF_EVEN":
            raise PatternError("unsupported rounding mode")

    @classmethod
    def standard(cls, canonical_id: str) -> Self:
        if canonical_id not in _PATTERN_IDS:
            raise PatternError("pattern ID is outside the exact S2B allowlist")
        return cls(
            canonical_id=canonical_id,
            version=PATTERN_DEFINITION_VERSION,
            family=_PATTERN_FAMILIES[canonical_id],
            bar_cardinality=_PATTERN_BAR_CARDINALITY[canonical_id],
        )

    @property
    def material(self) -> dict[str, object]:
        return {
            "canonical_id": self.canonical_id,
            "version": self.version,
            "family": self.family,
            "bar_cardinality": self.bar_cardinality,
            "algorithm_version": self.algorithm_version,
            "decimal_policy_version": self.decimal_policy_version,
            "fingerprint_version": self.fingerprint_version,
            "small_body_max": str(self.small_body_max),
            "long_body_min": str(self.long_body_min),
            "engulfing_bounds": self.engulfing_bounds,
            "midpoint_equality": self.midpoint_equality,
            "star_gap_policy": self.star_gap_policy,
            "timeframe_allowlist": list(self.timeframe_allowlist),
            "rounding_mode": self.rounding_mode,
        }

    @property
    def fingerprint(self) -> str:
        return _hash(self.material)


@dataclass(frozen=True, slots=True)
class PatternVersion:
    """Versioned material contract; the fingerprint includes every behavior input."""

    definition: PatternDefinition

    def __post_init__(self) -> None:
        if not isinstance(self.definition, PatternDefinition):
            raise PatternError("PatternVersion requires a PatternDefinition")

    @classmethod
    def standard(cls, canonical_id: str) -> Self:
        return cls(PatternDefinition.standard(canonical_id))

    @property
    def canonical_id(self) -> str:
        return self.definition.canonical_id

    @property
    def version(self) -> int:
        return self.definition.version

    @property
    def bar_cardinality(self) -> int:
        return self.definition.bar_cardinality

    @property
    def fingerprint(self) -> str:
        return _hash({"pattern_definition": self.definition.material})


@dataclass(frozen=True, slots=True)
class PatternRegistry:
    """Persistent registry: every register operation returns a new registry."""

    versions: tuple[PatternVersion, ...] = ()

    def register(self, pattern: PatternVersion) -> Self:
        if not isinstance(pattern, PatternVersion):
            raise PatternRegistryError("PatternVersion is required")
        for existing in self.versions:
            if existing.canonical_id != pattern.canonical_id:
                continue
            if existing.version == pattern.version:
                if existing.fingerprint != pattern.fingerprint:
                    raise PatternRegistryError("material version collision")
                return self
        return type(self)(
            tuple(
                sorted(
                    (*self.versions, pattern),
                    key=lambda item: (item.canonical_id, item.version),
                )
            )
        )

    def resolve(self, canonical_id: str, version: int | None = None) -> PatternVersion:
        matches = [item for item in self.versions if item.canonical_id == canonical_id]
        if version is not None:
            matches = [item for item in matches if item.version == version]
        if len(matches) != 1:
            raise PatternRegistryError("pattern version is missing or ambiguous")
        return matches[0]


@dataclass(frozen=True, slots=True)
class PatternConstituent:
    """One exact paired constituent: S1F candle plus its evaluator-issued S2A sample.

    The ``CandleBar`` supplies the authoritative OHLC including ``open``; the
    ``FeatureSample`` and its ``FeatureAuthorityEvidence`` supply the canonical
    point-in-time authority proof.  The pair is bound by
    ``sample.fingerprint == candle.fingerprint``, and because
    ``CandleBar.fingerprint`` commits ``open`` a forged or mutated ``open``
    necessarily breaks the pair.
    """

    candle: CandleBar
    sample: FeatureSample

    def __post_init__(self) -> None:
        if not isinstance(self.candle, CandleBar):
            raise PatternError("constituent candle is required")
        if not isinstance(self.sample, FeatureSample):
            raise PatternError("constituent sample is required")
        candle = self.candle
        sample = self.sample
        context = candle.context
        if sample.fingerprint != candle.fingerprint:
            raise PatternError("constituent pair fingerprint does not match its candle")
        if sample.source_id != context.source_id:
            raise PatternError("constituent pair source disagrees with its candle")
        if sample.contract_id != context.contract_id:
            raise PatternError("constituent pair contract disagrees with its candle")
        if sample.environment is not context.environment:
            raise PatternError("constituent pair environment disagrees with its candle")
        if sample.generation_fingerprint != context.generation.fingerprint:
            raise PatternError("constituent pair generation disagrees with its candle")
        if sample.timeframe.fingerprint != candle.timeframe.fingerprint:
            raise PatternError("constituent pair timeframe disagrees with its candle")
        if sample.interval_start != candle.start or sample.interval_end != candle.end:
            raise PatternError("constituent pair interval disagrees with its candle")
        if sample.closed != (candle.finality is Finality.CLOSED):
            raise PatternError("constituent pair finality disagrees with its candle")
        if sample.high != candle.high or sample.low != candle.low:
            raise PatternError("constituent pair range disagrees with its candle")
        if sample.close != candle.close:
            raise PatternError("constituent pair close disagrees with its candle")
        if sample.quantity != candle.volume:
            raise PatternError("constituent pair quantity disagrees with its candle")

    @property
    def open(self) -> DecimalValue:
        """Authoritative open, taken only from the bound candle."""

        return self.candle.open

    @property
    def authority(self) -> FeatureAuthorityEvidence:
        return self.sample.authority

    @property
    def start(self) -> datetime:
        return self.candle.start

    @property
    def end(self) -> datetime:
        return self.candle.end

    @property
    def timeframe(self) -> Timeframe:
        return self.candle.timeframe


def _pair_fold(
    constituents: Sequence[PatternConstituent],
) -> tuple[
    MarketStateTrust,
    DataAuthorityState,
    FeatureAxisRestriction,
    FeatureAxisRestriction,
]:
    """Most-restrictive fold across constituent authorities; never upgrades."""

    trust = min(
        (item.authority.market_state_trust for item in constituents),
        key=_TRUST_SEVERITY.index,
    )
    authority = min(
        (item.authority.data_authority_state for item in constituents),
        key=_AUTHORITY_SEVERITY.index,
    )
    disposition = min(
        (item.authority.resource_disposition for item in constituents),
        key=_RESOURCE_SEVERITY.index,
    )
    lifecycle = min(
        (item.authority.lifecycle_restriction for item in constituents),
        key=_LIFECYCLE_SEVERITY.index,
    )
    resource = (
        FeatureAxisRestriction.RESTRICTIVE
        if disposition is not ResourceDisposition.AVAILABLE
        else FeatureAxisRestriction.NONE
    )
    lifecycle_axis = (
        FeatureAxisRestriction.RESTRICTIVE
        if lifecycle is not LifecycleRestriction.NONE
        else FeatureAxisRestriction.NONE
    )
    return trust, authority, resource, lifecycle_axis


@dataclass(frozen=True, slots=True)
class _Span:
    """Derived span material for one evaluation."""

    validity: PatternValidity | None
    reason: str
    window_start: datetime
    window_end: datetime
    event_time: datetime
    knowledge_time: datetime
    wall_receive_time: datetime
    boundary: datetime
    expected_end: datetime


def _span(constituents: Sequence[PatternConstituent], cardinality: int) -> _Span:
    """Validate ordering, uniqueness, contiguity, identity and timeframe."""

    if not constituents:
        raise PatternEvaluationError("at least one constituent is required")
    first = constituents[0]
    frame = first.timeframe
    window_start = first.sample.interval_start or first.start
    window_end = constituents[-1].sample.interval_end or constituents[-1].end
    event_time = max(item.sample.event_time for item in constituents)
    knowledge_time = max(item.sample.knowledge_time for item in constituents)
    wall_receive_time = max(item.sample.wall_receive_time for item in constituents)
    expected_end = first.start + timedelta(seconds=cardinality * frame.duration_seconds)

    def span(
        validity: PatternValidity | None, reason: str, *, end: datetime | None = None
    ) -> _Span:
        return _Span(
            validity=validity,
            reason=reason,
            window_start=window_start,
            window_end=end or window_end,
            event_time=event_time,
            knowledge_time=knowledge_time,
            wall_receive_time=wall_receive_time,
            boundary=max(end or window_end, knowledge_time),
            expected_end=expected_end,
        )

    if not _authorized_frame(frame):
        return span(PatternValidity.INVALID, "UNAUTHORIZED_TIMEFRAME_IDENTITY")
    for item in constituents:
        if (
            item.sample.source_id != first.sample.source_id
            or item.sample.contract_id != first.sample.contract_id
            or item.sample.environment is not first.sample.environment
            or item.sample.generation_fingerprint != first.sample.generation_fingerprint
            or item.timeframe.fingerprint != frame.fingerprint
        ):
            return span(
                PatternValidity.INVALID,
                "MIXED_SOURCE_CONTRACT_ENVIRONMENT_GENERATION_OR_TIMEFRAME",
            )
        if item.candle.context.generation.retired:
            return span(PatternValidity.INVALID, "RETIRED_GENERATION")
    if len(constituents) > 1:
        for previous, current in zip(constituents[:-1], constituents[1:], strict=False):
            if previous.end != current.start:
                return span(PatternValidity.INVALID, "NON_CONTIGUOUS_OR_REORDERED_CONSTITUENTS")
    if len({item.sample.fingerprint for item in constituents}) != len(constituents):
        return span(PatternValidity.INVALID, "DUPLICATE_CONSTITUENTS")
    for item in constituents:
        if item.candle.finality is not Finality.CLOSED:
            return span(PatternValidity.WARMUP, "CLOSED_CONSTITUENT_REQUIRED")
    if len(constituents) < cardinality:
        return span(
            PatternValidity.WARMUP,
            "INSUFFICIENT_REQUIRED_CONSTITUENTS",
            end=expected_end,
        )
    return span(None, "", end=window_end)


@dataclass(frozen=True, slots=True, init=False)
class PatternEvidence:
    """Evaluator-issued, content-bound analytical pattern evidence."""

    pattern: PatternVersion
    match_state: PatternMatchState
    direction: PatternDirection
    validity: PatternValidity
    reason: str
    source_id: StableId
    contract_id: StableId
    environment: Environment
    generation_fingerprint: str
    timeframe_fingerprint: str
    timeframe_version: int
    timeframe_duration_seconds: int
    window_start: datetime
    window_end: datetime
    event_time: datetime
    knowledge_time: datetime
    wall_receive_time: datetime
    evaluation_boundary: datetime
    lineage: tuple[str, ...]
    sample_lineage: tuple[str, ...]
    authority_lineage: tuple[str, ...]
    market_state_trust: MarketStateTrust
    data_authority_state: DataAuthorityState
    resource_restriction: FeatureAxisRestriction
    lifecycle_restriction: FeatureAxisRestriction
    revision: int
    predecessor_evidence_fingerprint: str | None
    _attestation: object = field(default=None, repr=False, compare=False)

    def __init__(self, *args: object, **kwargs: object) -> None:
        raise PatternError("PatternEvidence must be issued by the pattern evaluator")

    def _is_attested(self) -> bool:
        return self._attestation is _EVIDENCE_ATTESTATION

    @classmethod
    def _from_evaluator(cls, **material: Any) -> PatternEvidence:
        instance = object.__new__(cls)
        for name, value in material.items():
            object.__setattr__(instance, name, value)
        object.__setattr__(instance, "_attestation", _EVIDENCE_ATTESTATION)
        instance.__post_init__()
        return instance

    def __post_init__(self) -> None:
        if not self._is_attested():
            raise PatternError("pattern evidence is not evaluator-issued")
        if not isinstance(self.pattern, PatternVersion):
            raise PatternError("pattern evidence requires a PatternVersion")
        if not isinstance(self.match_state, PatternMatchState):
            raise PatternError("pattern match state is invalid")
        if not isinstance(self.direction, PatternDirection):
            raise PatternError("pattern direction is invalid")
        if not isinstance(self.validity, PatternValidity):
            raise PatternError("pattern validity is invalid")
        if not self.reason:
            raise PatternError("pattern evidence reason is required")
        if (
            not isinstance(self.source_id, StableId)
            or self.source_id.kind is not IdentityKind.EXCHANGE
            or not isinstance(self.contract_id, StableId)
            or self.contract_id.kind is not IdentityKind.INSTRUMENT
        ):
            raise PatternError("pattern evidence source identities are invalid")
        if not isinstance(self.environment, Environment):
            raise PatternError("pattern evidence environment is invalid")
        _require_hash(self.generation_fingerprint, "pattern evidence generation")
        _require_hash(self.timeframe_fingerprint, "pattern evidence timeframe")
        if isinstance(self.timeframe_version, bool) or self.timeframe_version < 1:
            raise PatternError("pattern evidence timeframe version is invalid")
        if isinstance(self.timeframe_duration_seconds, bool) or self.timeframe_duration_seconds < 1:
            raise PatternError("pattern evidence timeframe duration is invalid")
        for label in (
            "window_start",
            "window_end",
            "event_time",
            "knowledge_time",
            "wall_receive_time",
            "evaluation_boundary",
        ):
            object.__setattr__(self, label, _utc(getattr(self, label), f"pattern {label}"))
        if self.window_end < self.window_start or self.knowledge_time > self.wall_receive_time:
            raise PatternError("pattern evidence temporal bounds are invalid")
        if not self.lineage:
            raise PatternError("pattern lineage is required")
        for item in self.lineage:
            _require_hash(item, "pattern lineage entry")
        if len(self.sample_lineage) != len(self.lineage):
            raise PatternError("pattern sample lineage length disagrees")
        if len(self.authority_lineage) != len(self.lineage):
            raise PatternError("pattern authority lineage length disagrees")
        for item in (*self.sample_lineage, *self.authority_lineage):
            _require_hash(item, "pattern authority lineage entry")
        if not isinstance(self.market_state_trust, MarketStateTrust):
            raise PatternError("pattern market-state trust is invalid")
        if not isinstance(self.data_authority_state, DataAuthorityState):
            raise PatternError("pattern data-authority state is invalid")
        if not isinstance(self.resource_restriction, FeatureAxisRestriction) or not isinstance(
            self.lifecycle_restriction, FeatureAxisRestriction
        ):
            raise PatternError("pattern restriction axes are invalid")
        if isinstance(self.revision, bool) or self.revision < 0:
            raise PatternError("pattern revision is invalid")
        if self.predecessor_evidence_fingerprint is not None:
            _require_hash(
                self.predecessor_evidence_fingerprint,
                "pattern predecessor evidence fingerprint",
            )
        if self.validity in {PatternValidity.VALID, PatternValidity.DEGRADED}:
            if self.match_state is PatternMatchState.INDETERMINATE:
                raise PatternError("valid or degraded evidence cannot be INDETERMINATE")
            if self.match_state is PatternMatchState.NOT_MATCHED:
                if self.direction is not PatternDirection.NONE:
                    raise PatternError("NOT_MATCHED direction must be NONE")
            elif self.direction in {PatternDirection.NONE, PatternDirection.UNKNOWN}:
                raise PatternError("MATCHED direction must be concrete")
        else:
            if self.match_state is not PatternMatchState.INDETERMINATE:
                raise PatternError("restrictive validity requires an INDETERMINATE match state")
            if self.direction is not PatternDirection.UNKNOWN:
                raise PatternError("INDETERMINATE direction must be UNKNOWN")

    @property
    def evidence_key(self) -> str:
        """Canonical evidence identity per the frozen H014 contract."""

        return _hash(
            {
                "pattern_id": self.pattern.canonical_id,
                "definition_version": self.pattern.version,
                "source": self.source_id.as_text(),
                "contract": self.contract_id.as_text(),
                "environment": self.environment.value,
                "generation": self.generation_fingerprint,
                "timeframe_fingerprint": self.timeframe_fingerprint,
                "window_start": self.window_start.isoformat(),
                "window_end": self.window_end.isoformat(),
                "constituents": self.lineage,
            }
        )

    @property
    def fingerprint(self) -> str:
        """Canonical fingerprint v1 over the complete evidence material."""

        return _hash(
            {
                "evidence_version": PATTERN_EVIDENCE_VERSION,
                "fingerprint_version": PATTERN_FINGERPRINT_VERSION,
                "pattern": self.pattern.fingerprint,
                "match_state": self.match_state.value,
                "direction": self.direction.value,
                "validity": self.validity.value,
                "reason": self.reason,
                "source": self.source_id.as_text(),
                "contract": self.contract_id.as_text(),
                "environment": self.environment.value,
                "generation": self.generation_fingerprint,
                "timeframe_fingerprint": self.timeframe_fingerprint,
                "timeframe_version": self.timeframe_version,
                "timeframe_duration_seconds": self.timeframe_duration_seconds,
                "window_start": self.window_start.isoformat(),
                "window_end": self.window_end.isoformat(),
                "event_time": self.event_time.isoformat(),
                "knowledge_time": self.knowledge_time.isoformat(),
                "wall_receive_time": self.wall_receive_time.isoformat(),
                "evaluation_boundary": self.evaluation_boundary.isoformat(),
                "lineage": self.lineage,
                "sample_lineage": self.sample_lineage,
                "authority_lineage": self.authority_lineage,
                "market_state_trust": self.market_state_trust.value,
                "data_authority_state": self.data_authority_state.value,
                "resource_restriction": self.resource_restriction.value,
                "lifecycle_restriction": self.lifecycle_restriction.value,
                "revision": self.revision,
                "predecessor_evidence_fingerprint": self.predecessor_evidence_fingerprint,
            }
        )

    @property
    def evidence_fingerprint(self) -> str:
        return self.fingerprint


def _match_pattern(
    identifier: str,
    bars: Sequence[tuple[Decimal, Decimal, Decimal, Decimal]],
) -> tuple[PatternMatchState, PatternDirection, PatternValidity, str]:
    """Evaluate the frozen equation and return match, direction, validity, reason."""

    ratios: list[Decimal] = []
    for open_value, high, low, close in bars:
        ratio = _body_ratio(open_value, high, low, close)
        if ratio is None:
            return (
                PatternMatchState.INDETERMINATE,
                PatternDirection.UNKNOWN,
                PatternValidity.UNKNOWN,
                "ZERO_RANGE_PRIMITIVE",
            )
        ratios.append(ratio)
    matched: bool
    direction: PatternDirection
    if identifier == "P-DC-001":
        matched = ratios[0] <= SMALL_BODY_MAX
        direction = PatternDirection.NEUTRAL
    elif identifier == "P-MB-001":
        open_value, _high, _low, close = bars[0]
        matched = ratios[0] >= LONG_BODY_MIN
        direction = (
            PatternDirection.BULLISH
            if close > open_value
            else PatternDirection.BEARISH
            if close < open_value
            else PatternDirection.NEUTRAL
        )
    elif identifier == "P-EC-001":
        previous_open, _ph, _pl, previous_close = bars[0]
        current_open, _ch, _cl, current_close = bars[1]
        matched = (
            previous_close < previous_open
            and current_close > current_open
            and current_open <= previous_close
            and current_close >= previous_open
        )
        direction = PatternDirection.BULLISH
    elif identifier == "P-EC-002":
        previous_open, _ph, _pl, previous_close = bars[0]
        current_open, _ch, _cl, current_close = bars[1]
        matched = (
            previous_close > previous_open
            and current_close < current_open
            and current_open >= previous_close
            and current_close <= previous_open
        )
        direction = PatternDirection.BEARISH
    elif identifier in {"P-MS-001", "P-ES-001"}:
        first_open, _fh, _fl, first_close = bars[0]
        third_open, _th, _tl, third_close = bars[2]
        midpoint = _midpoint(first_open, first_close)
        if identifier == "P-MS-001":
            matched = (
                first_close < first_open
                and ratios[0] >= LONG_BODY_MIN
                and ratios[1] <= SMALL_BODY_MAX
                and third_close > third_open
                and ratios[2] >= LONG_BODY_MIN
                and third_close >= midpoint
            )
            direction = PatternDirection.BULLISH
        else:
            matched = (
                first_close > first_open
                and ratios[0] >= LONG_BODY_MIN
                and ratios[1] <= SMALL_BODY_MAX
                and third_close < third_open
                and ratios[2] >= LONG_BODY_MIN
                and third_close <= midpoint
            )
            direction = PatternDirection.BEARISH
    else:
        raise PatternEvaluationError("unsupported pattern ID")
    if matched:
        return PatternMatchState.MATCHED, direction, PatternValidity.VALID, "MATCHED"
    return (
        PatternMatchState.NOT_MATCHED,
        PatternDirection.NONE,
        PatternValidity.VALID,
        "NOT_MATCHED",
    )


def evaluate_pattern(
    pattern: PatternVersion,
    constituents: Iterable[PatternConstituent],
    *,
    evaluation_time: datetime | None = None,
    revision: int = 0,
    predecessor_evidence_fingerprint: str | None = None,
) -> PatternEvidence:
    """Evaluate one frozen pattern over its exact ordered paired constituents."""

    if not isinstance(pattern, PatternVersion):
        raise PatternEvaluationError("PatternVersion is required")
    items = tuple(constituents)
    if not items:
        raise PatternEvaluationError("at least one constituent is required")
    for item in items:
        if not isinstance(item, PatternConstituent):
            raise PatternEvaluationError("evaluator input must be paired constituents")
    span = _span(items, pattern.bar_cardinality)
    first = items[0]
    trust, authority, resource, lifecycle = _pair_fold(items)
    # ``sample.fingerprint`` is the bound candle fingerprint under the frozen pair
    # contract, and it is stored rather than recomputed.
    lineage = tuple(item.sample.fingerprint for item in items)
    sample_lineage = lineage
    authority_lineage = tuple(item.authority.fingerprint for item in items)

    def build(
        match_state: PatternMatchState,
        direction: PatternDirection,
        validity: PatternValidity,
        reason: str,
    ) -> PatternEvidence:
        return PatternEvidence._from_evaluator(
            pattern=pattern,
            match_state=match_state,
            direction=direction,
            validity=validity,
            reason=reason,
            source_id=first.sample.source_id,
            contract_id=first.sample.contract_id,
            environment=first.sample.environment,
            generation_fingerprint=first.sample.generation_fingerprint,
            timeframe_fingerprint=first.timeframe.fingerprint,
            timeframe_version=first.timeframe.version,
            timeframe_duration_seconds=first.timeframe.duration_seconds,
            window_start=span.window_start,
            window_end=span.window_end,
            event_time=span.event_time,
            knowledge_time=span.knowledge_time,
            wall_receive_time=span.wall_receive_time,
            evaluation_boundary=span.boundary,
            lineage=lineage,
            sample_lineage=sample_lineage,
            authority_lineage=authority_lineage,
            market_state_trust=trust,
            data_authority_state=authority,
            resource_restriction=resource,
            lifecycle_restriction=lifecycle,
            revision=revision,
            predecessor_evidence_fingerprint=predecessor_evidence_fingerprint,
        )

    def indeterminate(validity: PatternValidity, reason: str) -> PatternEvidence:
        return build(PatternMatchState.INDETERMINATE, PatternDirection.UNKNOWN, validity, reason)

    supplied = _utc(evaluation_time, "evaluation time") if evaluation_time is not None else None
    if span.validity is not None:
        validity = span.validity
        if validity is PatternValidity.WARMUP:
            boundary_for_maturity = span.expected_end
            if supplied is not None and supplied >= boundary_for_maturity:
                validity = PatternValidity.UNKNOWN
                reason = "REQUIRED_CLOSED_CONSTITUENT_UNAVAILABLE"
            else:
                reason = span.reason
        else:
            reason = span.reason
        return indeterminate(validity, reason)
    if supplied is not None and supplied < span.boundary:
        # Before the canonical boundary MATCHED and NOT_MATCHED are forbidden.
        return indeterminate(PatternValidity.WARMUP, "PRE_CANONICAL_BOUNDARY")
    if trust in {
        MarketStateTrust.UNKNOWN,
        MarketStateTrust.UNTRUSTED,
        MarketStateTrust.RESYNC_REQUIRED,
    }:
        return indeterminate(PatternValidity.UNKNOWN, "CONSTITUENT_MARKET_STATE_UNTRUSTED")
    bars = tuple(
        (
            item.candle.open.value,
            item.candle.high.value,
            item.candle.low.value,
            item.candle.close.value,
        )
        for item in items
    )
    match_state, direction, validity, reason = _match_pattern(pattern.canonical_id, bars)
    if validity is PatternValidity.UNKNOWN:
        return build(match_state, direction, validity, reason)
    if trust is MarketStateTrust.DEGRADED:
        return build(match_state, direction, PatternValidity.DEGRADED, "DEGRADED_ANALYTICAL_INPUT")
    return build(match_state, direction, validity, reason)


def canonical_evidence_order(
    evidences: Iterable[PatternEvidence],
) -> tuple[PatternEvidence, ...]:
    """Deterministic sequence ordering; it grants no rank or authority.

    Sequence is by timeframe ``duration_seconds`` ascending, then ``window_end``,
    ``pattern_id``, ``definition_version`` and evidence fingerprint ascending.
    """

    def key(item: PatternEvidence) -> tuple[int, str, str, int, str]:
        return (
            item.timeframe_duration_seconds,
            item.window_end.isoformat(),
            item.pattern.canonical_id,
            item.pattern.version,
            item.fingerprint,
        )

    return tuple(sorted(evidences, key=key))


def evaluate_patterns(
    patterns: Iterable[PatternVersion],
    constituents: Iterable[PatternConstituent],
    *,
    evaluation_time: datetime | None = None,
    predecessor_evidence_fingerprints: Mapping[str, str] | None = None,
    revisions: Mapping[str, int] | None = None,
) -> tuple[PatternEvidence, ...]:
    """Evaluate several patterns over the same paired constituents.

    Different pattern IDs are retained independently: no winner, suppression,
    score, ranking or trade preference is applied.
    """

    items = tuple(constituents)
    predecessors: dict[str, str] = dict(predecessor_evidence_fingerprints or {})
    revision_map: dict[str, int] = dict(revisions or {})
    evidences = [
        evaluate_pattern(
            pattern,
            items,
            evaluation_time=evaluation_time,
            revision=revision_map.get(pattern.canonical_id, 0),
            predecessor_evidence_fingerprint=predecessors.get(pattern.canonical_id),
        )
        for pattern in patterns
    ]
    return canonical_evidence_order(evidences)


__all__ = [
    "LONG_BODY_MIN",
    "PATTERN_ALGORITHM_VERSION",
    "PATTERN_ALLOWLIST",
    "PATTERN_DEFINITION_VERSION",
    "PATTERN_DECIMAL_POLICY_VERSION",
    "PATTERN_EVIDENCE_VERSION",
    "PATTERN_FINGERPRINT_VERSION",
    "SMALL_BODY_MAX",
    "PatternConstituent",
    "PatternDefinition",
    "PatternDirection",
    "PatternError",
    "PatternEvaluationError",
    "PatternEvidence",
    "PatternMatchState",
    "PatternRegistry",
    "PatternRegistryError",
    "PatternValidity",
    "PatternVersion",
    "canonical_evidence_order",
    "evaluate_pattern",
    "evaluate_patterns",
]
