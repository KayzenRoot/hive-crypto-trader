"""Deterministic, provider-neutral Module 9 candlestick pattern evidence.

This module consumes immutable S1E/S1F/S2A evidence only.  It derives
point-in-time analytical pattern evidence for exactly six frozen public/standard
candlestick patterns.  It does not open transports, persist state, create orders,
produce downstream decisions or grant authority.
"""

from __future__ import annotations

import hashlib
import hmac
import json
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from decimal import ROUND_HALF_EVEN, Decimal, localcontext
from enum import StrEnum
from typing import Final, Self, SupportsIndex

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
# Full structural timeframe identity tokens: duration, version and alignment are each
# behaviorally material, so each is fingerprint-visible in the definition.
PATTERN_TIMEFRAME_IDENTITY: Final = tuple(
    f"{name}:{duration}:{version}:{alignment}"
    for name, (duration, version, alignment) in _TIMEFRAME_IDENTITY.items()
)
PATTERN_INPUT_CONTRACT: Final = "CANDLEBAR_OHLC_PLUS_EVALUATOR_ISSUED_FEATURE_SAMPLE"
PATTERN_SOURCE_FIELDS: Final = ("open", "high", "low", "close")
PATTERN_DECIMAL_PRECISION: Final = 76
PATTERN_ZERO_RANGE_POLICY: Final = "ZERO_RANGE_PRIMITIVE_UNKNOWN"
PATTERN_FINALITY_REQUIREMENT: Final = "CLOSED_BAR_REQUIRED"
PATTERN_FORMATION_RULE: Final = "EXACT_ORDERED_CONTIGUOUS_CLOSED_PAIRS_K"
PATTERN_CARDINALITY_POLICY: Final = "EXACT_CARDINALITY_OVER_CARDINALITY_WINDOW_INVALID"
PATTERN_EVALUATION_BOUNDARY_RULE: Final = (
    "S2B_CANONICAL_EVALUATION_BOUNDARY=max(window_end,knowledge_time)"
)
PATTERN_DIRECTION_POLICY: Final = "MATCHED_REQUIRES_CONCRETE_DIRECTION_NOT_MATCHED_REQUIRES_NONE"
PATTERN_MATCH_STATE_POLICY: Final = "RESTRICTIVE_VALIDITY_REQUIRES_INDETERMINATE"
# Canonical per-pattern equation specification.  ``r`` is the canonical body ratio
# ``abs(close-open)/(high-low)`` computed under the frozen Decimal policy.
PATTERN_EQUATIONS: Final = {
    "P-DC-001": "DOJI:r[0]<=SMALL_BODY_MAX;r=abs(close-open)/(high-low);direction=NEUTRAL",
    "P-MB-001": (
        "LONG_BODY:r[0]>=LONG_BODY_MIN;r=abs(close-open)/(high-low);direction=SIGN(close-open)"
    ),
    "P-EC-001": (
        "BULLISH_ENGULFING:close[0]<open[0]&close[1]>open[1]&open[1]<=close[0]"
        "&close[1]>=open[0];engulfing_bounds=INCLUSIVE;direction=BULLISH"
    ),
    "P-EC-002": (
        "BEARISH_ENGULFING:close[0]>open[0]&close[1]<open[1]&open[1]>=close[0]"
        "&close[1]<=open[0];engulfing_bounds=INCLUSIVE;direction=BEARISH"
    ),
    "P-MS-001": (
        "MORNING_STAR:close[0]<open[0]&r[0]>=LONG_BODY_MIN&r[1]<=SMALL_BODY_MAX"
        "&close[2]>open[2]&r[2]>=LONG_BODY_MIN&close[2]>=midpoint(open[0],close[0])"
        ";midpoint_equality=INCLUSIVE;gap=NONE_IN_V1;direction=BULLISH"
    ),
    "P-ES-001": (
        "EVENING_STAR:close[0]>open[0]&r[0]>=LONG_BODY_MIN&r[1]<=SMALL_BODY_MAX"
        "&close[2]<open[2]&r[2]>=LONG_BODY_MIN&close[2]<=midpoint(open[0],close[0])"
        ";midpoint_equality=INCLUSIVE;gap=NONE_IN_V1;direction=BEARISH"
    ),
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


def _hash(payload: object) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


# Attestation is content-bound: the seal is a keyed digest over the complete evidence
# fingerprint, so any later field mutation invalidates the seal and is detected.
_SEAL_KEY: Final = _hash(
    {
        "attestation": "S2B_PATTERN_EVIDENCE_ATTESTATION_V1",
        "evidence_version": PATTERN_EVIDENCE_VERSION,
        "fingerprint_version": PATTERN_FINGERPRINT_VERSION,
        "algorithm_version": PATTERN_ALGORITHM_VERSION,
    }
)


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
    """Immutable behaviorally material pattern definition.

    Every frozen behaviorally material semantic is a field and is part of ``material``,
    so the definition/version fingerprint is a deterministic function of the complete
    contract: exact equation and source fields, full structural timeframe identity,
    formation/completion boundary rule, finality, thresholds, equality, zero-range
    policy, Decimal policy and the direction/match-state policy.
    """

    canonical_id: str
    version: int
    family: str
    bar_cardinality: int
    equation: str = ""
    input_contract: str = PATTERN_INPUT_CONTRACT
    source_fields: tuple[str, ...] = PATTERN_SOURCE_FIELDS
    algorithm_version: str = PATTERN_ALGORITHM_VERSION
    decimal_policy_version: str = PATTERN_DECIMAL_POLICY_VERSION
    decimal_precision: int = PATTERN_DECIMAL_PRECISION
    fingerprint_version: str = PATTERN_FINGERPRINT_VERSION
    small_body_max: Decimal = SMALL_BODY_MAX
    long_body_min: Decimal = LONG_BODY_MIN
    engulfing_bounds: str = "BOUNDS_INCLUSIVE"
    midpoint_equality: str = "BOUNDS_INCLUSIVE"
    star_gap_policy: str = "NONE_IN_V1"
    timeframe_allowlist: tuple[str, ...] = _TIMEFRAME_ALLOWLIST
    timeframe_identity: tuple[str, ...] = PATTERN_TIMEFRAME_IDENTITY
    rounding_mode: str = "ROUND_HALF_EVEN"
    zero_range_policy: str = PATTERN_ZERO_RANGE_POLICY
    finality_requirement: str = PATTERN_FINALITY_REQUIREMENT
    formation_rule: str = PATTERN_FORMATION_RULE
    cardinality_policy: str = PATTERN_CARDINALITY_POLICY
    evaluation_boundary_rule: str = PATTERN_EVALUATION_BOUNDARY_RULE
    direction_policy: str = PATTERN_DIRECTION_POLICY
    match_state_policy: str = PATTERN_MATCH_STATE_POLICY

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
        if self.equation != PATTERN_EQUATIONS[self.canonical_id]:
            raise PatternError("pattern equation token is frozen for V1")
        if self.input_contract != PATTERN_INPUT_CONTRACT:
            raise PatternError("unsupported pattern input contract")
        if self.source_fields != PATTERN_SOURCE_FIELDS:
            raise PatternError("unsupported pattern source fields")
        if self.algorithm_version != PATTERN_ALGORITHM_VERSION:
            raise PatternError("unsupported pattern algorithm version")
        if self.decimal_policy_version != PATTERN_DECIMAL_POLICY_VERSION:
            raise PatternError("unsupported Decimal policy")
        if (
            isinstance(self.decimal_precision, bool)
            or self.decimal_precision != PATTERN_DECIMAL_PRECISION
        ):
            raise PatternError("unsupported Decimal precision")
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
        if self.timeframe_identity != PATTERN_TIMEFRAME_IDENTITY:
            raise PatternError("unsupported structural timeframe identity")
        if self.rounding_mode != "ROUND_HALF_EVEN":
            raise PatternError("unsupported rounding mode")
        if self.zero_range_policy != PATTERN_ZERO_RANGE_POLICY:
            raise PatternError("unsupported zero-range policy")
        if self.finality_requirement != PATTERN_FINALITY_REQUIREMENT:
            raise PatternError("unsupported finality requirement")
        if self.formation_rule != PATTERN_FORMATION_RULE:
            raise PatternError("unsupported canonical formation rule")
        if self.cardinality_policy != PATTERN_CARDINALITY_POLICY:
            raise PatternError("unsupported bar cardinality policy")
        if self.evaluation_boundary_rule != PATTERN_EVALUATION_BOUNDARY_RULE:
            raise PatternError("unsupported canonical evaluation boundary rule")
        if self.direction_policy != PATTERN_DIRECTION_POLICY:
            raise PatternError("unsupported direction policy")
        if self.match_state_policy != PATTERN_MATCH_STATE_POLICY:
            raise PatternError("unsupported match-state policy")

    @classmethod
    def standard(cls, canonical_id: str) -> Self:
        if canonical_id not in _PATTERN_IDS:
            raise PatternError("pattern ID is outside the exact S2B allowlist")
        return cls(
            canonical_id=canonical_id,
            version=PATTERN_DEFINITION_VERSION,
            family=_PATTERN_FAMILIES[canonical_id],
            bar_cardinality=_PATTERN_BAR_CARDINALITY[canonical_id],
            equation=PATTERN_EQUATIONS[canonical_id],
        )

    @property
    def material(self) -> dict[str, object]:
        return {
            "canonical_id": self.canonical_id,
            "version": self.version,
            "family": self.family,
            "bar_cardinality": self.bar_cardinality,
            "equation": self.equation,
            "input_contract": self.input_contract,
            "source_fields": list(self.source_fields),
            "algorithm_version": self.algorithm_version,
            "decimal_policy_version": self.decimal_policy_version,
            "decimal_precision": self.decimal_precision,
            "fingerprint_version": self.fingerprint_version,
            "small_body_max": str(self.small_body_max),
            "long_body_min": str(self.long_body_min),
            "engulfing_bounds": self.engulfing_bounds,
            "midpoint_equality": self.midpoint_equality,
            "star_gap_policy": self.star_gap_policy,
            "timeframe_allowlist": list(self.timeframe_allowlist),
            "timeframe_identity": list(self.timeframe_identity),
            "rounding_mode": self.rounding_mode,
            "zero_range_policy": self.zero_range_policy,
            "finality_requirement": self.finality_requirement,
            "formation_rule": self.formation_rule,
            "cardinality_policy": self.cardinality_policy,
            "evaluation_boundary_rule": self.evaluation_boundary_rule,
            "direction_policy": self.direction_policy,
            "match_state_policy": self.match_state_policy,
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
    if len(constituents) > cardinality:
        # Every presented constituent is part of the claimed evidence window, so an
        # overlong window is structurally contradictory and never silently sliced.
        return span(PatternValidity.INVALID, "OVER_CARDINALITY_WINDOW")
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
    """Evaluator-issued, content-bound analytical pattern evidence.

    There is no caller-servable issuance API.  The only path that creates an
    attested instance is the module-private evaluator issuance function, which
    receives the frozen ``PatternVersion``, the exact validated paired constituents,
    the evaluation boundary time and the typed prior evidence state, and recomputes
    span, axis fold, equation, direction, validity, timestamps, lineage and
    fingerprint material itself.  The attestation seal is a keyed digest over the
    complete evidence fingerprint, so object-level tampering or copy-style mutation
    invalidates the seal instead of yielding attested material.
    """

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
    constituent_revisions: tuple[int, ...]
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

    def __copy__(self) -> PatternEvidence:
        raise PatternError("pattern evidence cannot be copied into unattested material")

    def __deepcopy__(self, memo: object) -> PatternEvidence:
        raise PatternError("pattern evidence cannot be deep-copied")

    def __reduce_ex__(self, protocol: SupportsIndex) -> str:
        raise PatternError("pattern evidence cannot be serialized or reconstructed")

    def _is_attested(self) -> bool:
        seal = self._attestation
        if not isinstance(seal, str):
            return False
        return hmac.compare_digest(seal, _evidence_seal(self))

    def __post_init__(self) -> None:
        self._validate_material()
        if not self._is_attested():
            raise PatternError("pattern evidence is not evaluator-issued")

    def _validate_material(self) -> None:
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
        if len(self.constituent_revisions) != len(self.lineage):
            raise PatternError("pattern constituent revision lineage length disagrees")
        for revision in self.constituent_revisions:
            if isinstance(revision, bool) or not isinstance(revision, int) or revision < 0:
                raise PatternError("pattern constituent revision is invalid")
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

        return _hash(_evidence_material(self))

    @property
    def evidence_fingerprint(self) -> str:
        return self.fingerprint

    @property
    def material(self) -> dict[str, object]:
        return _evidence_material(self)


def _evidence_material(evidence: PatternEvidence) -> dict[str, object]:
    """Complete canonical evidence material; every field is fingerprint-visible."""

    return {
        "evidence_version": PATTERN_EVIDENCE_VERSION,
        "fingerprint_version": PATTERN_FINGERPRINT_VERSION,
        "pattern": evidence.pattern.fingerprint,
        "match_state": evidence.match_state.value,
        "direction": evidence.direction.value,
        "validity": evidence.validity.value,
        "reason": evidence.reason,
        "source": evidence.source_id.as_text(),
        "contract": evidence.contract_id.as_text(),
        "environment": evidence.environment.value,
        "generation": evidence.generation_fingerprint,
        "timeframe_fingerprint": evidence.timeframe_fingerprint,
        "timeframe_version": evidence.timeframe_version,
        "timeframe_duration_seconds": evidence.timeframe_duration_seconds,
        "window_start": evidence.window_start.isoformat(),
        "window_end": evidence.window_end.isoformat(),
        "event_time": evidence.event_time.isoformat(),
        "knowledge_time": evidence.knowledge_time.isoformat(),
        "wall_receive_time": evidence.wall_receive_time.isoformat(),
        "evaluation_boundary": evidence.evaluation_boundary.isoformat(),
        "lineage": evidence.lineage,
        "constituent_revisions": evidence.constituent_revisions,
        "sample_lineage": evidence.sample_lineage,
        "authority_lineage": evidence.authority_lineage,
        "market_state_trust": evidence.market_state_trust.value,
        "data_authority_state": evidence.data_authority_state.value,
        "resource_restriction": evidence.resource_restriction.value,
        "lifecycle_restriction": evidence.lifecycle_restriction.value,
        "revision": evidence.revision,
        "predecessor_evidence_fingerprint": evidence.predecessor_evidence_fingerprint,
    }


def _evidence_seal(evidence: PatternEvidence) -> str:
    """Keyed digest over the complete evidence fingerprint."""

    return _hash({"seal": _SEAL_KEY, "evidence": evidence.fingerprint})


def _transition_material(evidence: PatternEvidence) -> dict[str, object]:
    """Evidence material without the revision link; used to reject no-change revisions."""

    material = _evidence_material(evidence)
    material.pop("revision")
    material.pop("predecessor_evidence_fingerprint")
    return material


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


@dataclass(frozen=True, slots=True)
class PatternEvaluationState:
    """Evaluator-owned immutable revision chain for one logical pattern/window key.

    This is the only accepted predecessor input to the public evaluation API: the
    revision and the predecessor fingerprint are derived from its head instead of being
    supplied by the caller.  Recording rejects a revision skip, a fork, a non-immediate
    predecessor, a scope change and an overwrite of an already recorded chain node, so
    the chain stays exact and replayable.
    """

    evidences: tuple[PatternEvidence, ...] = ()

    def __post_init__(self) -> None:
        previous: PatternEvidence | None = None
        for index, evidence in enumerate(self.evidences):
            if not isinstance(evidence, PatternEvidence) or not evidence._is_attested():
                raise PatternEvaluationError("chain entries must be evaluator-issued evidence")
            if evidence.revision != index:
                raise PatternEvaluationError("chain revision sequence has a skip")
            if previous is None:
                if evidence.predecessor_evidence_fingerprint is not None:
                    raise PatternEvaluationError("chain head cannot carry a predecessor")
            elif evidence.predecessor_evidence_fingerprint != previous.fingerprint or _scope_key(
                evidence
            ) != _scope_key(previous):
                raise PatternEvaluationError("chain link is not the immediate predecessor")
            previous = evidence

    @property
    def head(self) -> PatternEvidence | None:
        """The exact immediate predecessor for the next revision, when one exists."""

        return self.evidences[-1] if self.evidences else None

    @property
    def scope_key(self) -> tuple[object, ...] | None:
        return _scope_key(self.evidences[0]) if self.evidences else None

    def record(self, evidence: PatternEvidence) -> Self:
        """Append the exact immediate successor; reject skip, fork and overwrite."""

        if not isinstance(evidence, PatternEvidence) or not evidence._is_attested():
            raise PatternEvaluationError("chain entries must be evaluator-issued evidence")
        if any(item.fingerprint == evidence.fingerprint for item in self.evidences):
            raise PatternEvaluationError("chain node was already recorded")
        head = self.head
        if head is None:
            if evidence.revision != 0 or evidence.predecessor_evidence_fingerprint is not None:
                raise PatternEvaluationError("chain cannot start from a revision link")
        else:
            if _scope_key(evidence) != _scope_key(head):
                raise PatternEvaluationError("chain evidence scope disagrees with the chain")
            if evidence.revision != head.revision + 1:
                raise PatternEvaluationError("chain revision is not the immediate successor")
            if evidence.predecessor_evidence_fingerprint != head.fingerprint:
                raise PatternEvaluationError("chain link is not the immediate predecessor")
        return type(self)((*self.evidences, evidence))


def _scope_key(evidence: PatternEvidence) -> tuple[object, ...]:
    """The exact logical pattern/window scope of one evidence item."""

    return (
        evidence.pattern.canonical_id,
        evidence.pattern.version,
        evidence.source_id.as_text(),
        evidence.contract_id.as_text(),
        evidence.environment.value,
        evidence.timeframe_fingerprint,
        evidence.timeframe_version,
        evidence.timeframe_duration_seconds,
        evidence.window_start.isoformat(),
        evidence.window_end.isoformat(),
    )


def _require_immediate_predecessor(
    pattern: PatternVersion,
    items: Sequence[PatternConstituent],
    span: _Span,
    prior: PatternEvidence,
) -> None:
    """Reject any predecessor that is not the exact immediate typed predecessor."""

    if not isinstance(prior, PatternEvidence) or not prior._is_attested():
        raise PatternEvaluationError("typed prior pattern evidence is required")
    if (
        prior.pattern.canonical_id != pattern.canonical_id
        or prior.pattern.version != pattern.version
    ):
        raise PatternEvaluationError("predecessor pattern identity disagrees")
    first = items[0]
    if (
        prior.source_id != first.sample.source_id
        or prior.contract_id != first.sample.contract_id
        or prior.environment is not first.sample.environment
    ):
        raise PatternEvaluationError("predecessor source, contract or environment disagrees")
    if (
        prior.timeframe_fingerprint != first.timeframe.fingerprint
        or prior.timeframe_version != first.timeframe.version
        or prior.timeframe_duration_seconds != first.timeframe.duration_seconds
    ):
        raise PatternEvaluationError("predecessor timeframe identity disagrees")
    if prior.window_start != span.window_start or prior.window_end != span.window_end:
        raise PatternEvaluationError("predecessor window identity disagrees")
    if len(prior.lineage) != len(items):
        raise PatternEvaluationError("predecessor constituent cardinality disagrees")
    for index, item in enumerate(items):
        if item.candle.fingerprint == prior.lineage[index]:
            continue
        if (
            item.candle.revision != prior.constituent_revisions[index] + 1
            or item.candle.predecessor_fingerprint != prior.lineage[index]
        ):
            raise PatternEvaluationError(
                "changed constituent lacks the canonical immediate predecessor relation"
            )


def _issue_pattern_evidence(
    pattern: PatternVersion,
    items: Sequence[PatternConstituent],
    *,
    supplied_time: datetime | None,
    prior: PatternEvidence | None,
) -> PatternEvidence:
    """Evaluator-owned issuance: the only path that creates attested evidence.

    The inputs are the frozen definition, the exact validated paired constituents, the
    evaluation boundary time and the typed prior evidence state.  The span, axis fold,
    equation, direction, validity, timestamps, lineage, revision link and fingerprint
    material are all recomputed here; no caller-selected output material is accepted.
    """

    span = _span(items, pattern.bar_cardinality)
    first = items[0]
    trust, authority, resource, lifecycle = _pair_fold(items)
    # ``sample.fingerprint`` is the bound candle fingerprint under the frozen pair
    # contract, and it is stored rather than recomputed.
    lineage = tuple(item.sample.fingerprint for item in items)
    sample_lineage = lineage
    authority_lineage = tuple(item.authority.fingerprint for item in items)
    constituent_revisions = tuple(item.candle.revision for item in items)
    if prior is not None:
        _require_immediate_predecessor(pattern, items, span, prior)
        revision = prior.revision + 1
        predecessor = prior.fingerprint
    else:
        revision = 0
        predecessor = None

    def build(
        match_state: PatternMatchState,
        direction: PatternDirection,
        validity: PatternValidity,
        reason: str,
    ) -> PatternEvidence:
        instance = object.__new__(PatternEvidence)
        for name, value in (
            ("pattern", pattern),
            ("match_state", match_state),
            ("direction", direction),
            ("validity", validity),
            ("reason", reason),
            ("source_id", first.sample.source_id),
            ("contract_id", first.sample.contract_id),
            ("environment", first.sample.environment),
            ("generation_fingerprint", first.sample.generation_fingerprint),
            ("timeframe_fingerprint", first.timeframe.fingerprint),
            ("timeframe_version", first.timeframe.version),
            ("timeframe_duration_seconds", first.timeframe.duration_seconds),
            ("window_start", span.window_start),
            ("window_end", span.window_end),
            ("event_time", span.event_time),
            ("knowledge_time", span.knowledge_time),
            ("wall_receive_time", span.wall_receive_time),
            ("evaluation_boundary", span.boundary),
            ("lineage", lineage),
            ("constituent_revisions", constituent_revisions),
            ("sample_lineage", sample_lineage),
            ("authority_lineage", authority_lineage),
            ("market_state_trust", trust),
            ("data_authority_state", authority),
            ("resource_restriction", resource),
            ("lifecycle_restriction", lifecycle),
            ("revision", revision),
            ("predecessor_evidence_fingerprint", predecessor),
            ("_attestation", None),
        ):
            object.__setattr__(instance, name, value)
        instance._validate_material()
        object.__setattr__(instance, "_attestation", _evidence_seal(instance))
        if prior is not None and _transition_material(instance) == _transition_material(prior):
            raise PatternEvaluationError("revision request carries no behavior or evidence change")
        return instance

    def indeterminate(validity: PatternValidity, reason: str) -> PatternEvidence:
        return build(PatternMatchState.INDETERMINATE, PatternDirection.UNKNOWN, validity, reason)

    if span.validity is not None:
        validity = span.validity
        if validity is PatternValidity.WARMUP:
            boundary_for_maturity = span.expected_end
            if supplied_time is not None and supplied_time >= boundary_for_maturity:
                validity = PatternValidity.UNKNOWN
                reason = "REQUIRED_CLOSED_CONSTITUENT_UNAVAILABLE"
            else:
                reason = span.reason
        else:
            reason = span.reason
        return indeterminate(validity, reason)
    if supplied_time is not None and supplied_time < span.boundary:
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


def evaluate_pattern(
    pattern: PatternVersion,
    constituents: Iterable[PatternConstituent],
    *,
    evaluation_time: datetime | None = None,
    state: PatternEvaluationState | None = None,
) -> PatternEvidence:
    """Evaluate one frozen pattern over its exact ordered paired constituents.

    The revision and the predecessor fingerprint are never caller-selected.  When a
    typed ``state`` is supplied the revision is derived as ``head.revision + 1`` and the
    predecessor as ``head.fingerprint``; otherwise the result is the initial revision
    ``0`` with no predecessor.
    """

    if not isinstance(pattern, PatternVersion):
        raise PatternEvaluationError("PatternVersion is required")
    if state is not None and not isinstance(state, PatternEvaluationState):
        raise PatternEvaluationError("typed PatternEvaluationState is required")
    items = tuple(constituents)
    if not items:
        raise PatternEvaluationError("at least one constituent is required")
    for item in items:
        if not isinstance(item, PatternConstituent):
            raise PatternEvaluationError("evaluator input must be paired constituents")
    return _issue_pattern_evidence(
        pattern,
        items,
        supplied_time=_utc(evaluation_time, "evaluation time")
        if evaluation_time is not None
        else None,
        prior=state.head if state is not None else None,
    )


def canonical_evidence_order(evidences: Iterable[PatternEvidence]) -> tuple[PatternEvidence, ...]:
    """Deterministic sequence ordering; it grants no rank or authority.

    Sequence is by timeframe ``duration_seconds`` ascending, then ``window_end``,
    ``pattern_id``, ``definition_version`` and evidence fingerprint ascending.  Only
    evaluator-issued evidence is accepted, so tampered or copy-reconstructed material is
    rejected at the ordering boundary.
    """

    def key(item: PatternEvidence) -> tuple[int, str, str, int, str]:
        return (
            item.timeframe_duration_seconds,
            item.window_end.isoformat(),
            item.pattern.canonical_id,
            item.pattern.version,
            item.fingerprint,
        )

    ordered = tuple(sorted(evidences, key=key))
    for item in ordered:
        if not isinstance(item, PatternEvidence) or not item._is_attested():
            raise PatternEvaluationError("canonical sequence requires evaluator-issued evidence")
    return ordered


def evaluate_patterns(
    patterns: Iterable[PatternVersion],
    constituents: Iterable[PatternConstituent],
    *,
    evaluation_time: datetime | None = None,
    states: Mapping[str, PatternEvaluationState] | None = None,
) -> tuple[PatternEvidence, ...]:
    """Evaluate several patterns over the same paired constituents.

    Different pattern IDs are retained independently: no winner, suppression,
    score, ranking or trade preference is applied.  Revisions use the same typed
    ``PatternEvaluationState`` chain mechanism as ``evaluate_pattern``; raw predecessor
    hashes or revision numbers are not accepted.
    """

    items = tuple(constituents)
    versions = tuple(patterns)
    chain: dict[str, PatternEvaluationState] = dict(states or {})
    unknown = sorted(set(chain) - {item.canonical_id for item in versions})
    if unknown:
        raise PatternEvaluationError("chain state is outside the evaluated patterns")
    evidences = [
        evaluate_pattern(
            pattern,
            items,
            evaluation_time=evaluation_time,
            state=chain.get(pattern.canonical_id),
        )
        for pattern in versions
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
    "PatternEvaluationState",
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
