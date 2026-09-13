"""Provider-neutral S1E market truth contracts and restrictive predicates.

The module contains immutable, deterministic contracts only.  It deliberately
does not open transports, parse venue DTOs, retain durable state, or grant
execution authority.  Data quality and market-state trust are separate axes; lifecycle
and resource evidence can restrict a consumer without upgrading truth.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from enum import StrEnum
from typing import Final

from hct_backend.contracts import Environment, EnvironmentScopedId, IdentityKind, StableId
from hct_backend.market_universe import UniverseEligibilityState, UniverseEntry, UniverseSnapshot
from hct_backend.quota_governor import AdmissionDecision, AdmissionOutcome, AdmissionReason

_HASH_PATTERN: Final = re.compile(r"^[0-9a-f]{64}$")
_TOKEN_PATTERN: Final = re.compile(r"^[A-Za-z0-9._:/-]{1,128}$")


class MarketTruthError(ValueError):
    """Base fail-closed market truth error."""


class MarketTruthInputError(MarketTruthError):
    """Raised for malformed or unknown typed evidence."""


class MarketTruthConsistencyError(MarketTruthError):
    """Raised for contradictory, stale, or cross-generation evidence."""


class SequenceMode(StrEnum):
    STRICT_SEQUENCE = "STRICT_SEQUENCE"
    MONOTONIC_UPDATE_ID = "MONOTONIC_UPDATE_ID"
    TIMESTAMP_ORDERED_WITH_LIMITS = "TIMESTAMP_ORDERED_WITH_LIMITS"
    SNAPSHOT_ONLY = "SNAPSHOT_ONLY"
    NO_PROVABLE_SEQUENCE = "NO_PROVABLE_SEQUENCE"


class ChannelVisibility(StrEnum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"


class UpdateSemantics(StrEnum):
    SNAPSHOT = "SNAPSHOT"
    DELTA = "DELTA"
    SNAPSHOT_AND_DELTA = "SNAPSHOT_AND_DELTA"
    UNKNOWN = "UNKNOWN"


class SequenceResultKind(StrEnum):
    ACCEPT = "ACCEPT"
    DUPLICATE = "DUPLICATE"
    OUT_OF_ORDER = "OUT_OF_ORDER"
    GAP = "GAP"
    RESYNC_REQUIRED = "RESYNC_REQUIRED"
    SEQUENCE_UNPROVABLE = "SEQUENCE_UNPROVABLE"


class ClockHealth(StrEnum):
    HEALTHY = "HEALTHY"
    DRIFT = "DRIFT"
    JUMP = "JUMP"
    UNTRUSTED = "UNTRUSTED"


class QualityReason(StrEnum):
    FRESH_VALID = "FRESH_VALID"
    STALE = "STALE"
    EXPIRED = "EXPIRED"
    GAP = "GAP"
    DUPLICATE = "DUPLICATE"
    OUT_OF_ORDER = "OUT_OF_ORDER"
    SEQUENCE_UNPROVABLE = "SEQUENCE_UNPROVABLE"
    CLOCK_DRIFT = "CLOCK_DRIFT"
    CLOCK_JUMP = "CLOCK_JUMP"
    CLOCK_UNTRUSTED = "CLOCK_UNTRUSTED"
    SCHEMA_QUARANTINED = "SCHEMA_QUARANTINED"
    MISSING_PROVENANCE = "MISSING_PROVENANCE"
    MISSING_GENERATION = "MISSING_GENERATION"
    CROSS_CHANNEL_CONTRADICTION = "CROSS_CHANNEL_CONTRADICTION"
    RESOURCE_STARVATION = "RESOURCE_STARVATION"
    RESOURCE_DEGRADED = "RESOURCE_DEGRADED"
    RESOURCE_UNKNOWN = "RESOURCE_UNKNOWN"
    UNSYNCHRONIZED = "UNSYNCHRONIZED"
    RETIRED_GENERATION = "RETIRED_GENERATION"


class DataAuthorityState(StrEnum):
    ALLOW_NEW_EXPOSURE = "ALLOW_NEW_EXPOSURE"
    DEGRADED_NEW_EXPOSURE = "DEGRADED_NEW_EXPOSURE"
    NO_NEW_EXPOSURE = "NO_NEW_EXPOSURE"
    REDUCE_ONLY = "REDUCE_ONLY"
    RECONCILIATION_ONLY = "RECONCILIATION_ONLY"
    EMERGENCY = "EMERGENCY"


class MarketStateTrust(StrEnum):
    UNKNOWN = "UNKNOWN"
    UNTRUSTED = "UNTRUSTED"
    RESYNC_REQUIRED = "RESYNC_REQUIRED"
    DEGRADED = "DEGRADED"
    TRUSTED = "TRUSTED"


class LifecycleRestriction(StrEnum):
    NONE = "NONE"
    NEW_EXPOSURE_DISABLED = "NEW_EXPOSURE_DISABLED"
    ELIGIBILITY_UNKNOWN = "ELIGIBILITY_UNKNOWN"


class ActionClass(StrEnum):
    NEW_EXPOSURE = "NEW_EXPOSURE"
    ADD_EXPOSURE = "ADD_EXPOSURE"
    REDUCE_EXPOSURE = "REDUCE_EXPOSURE"
    CLOSE_EXPOSURE = "CLOSE_EXPOSURE"
    ESTABLISH_OR_REPAIR_PROTECTION = "ESTABLISH_OR_REPAIR_PROTECTION"
    CANCELLATION = "CANCELLATION"
    RECONCILIATION_RECOVERY = "RECONCILIATION_RECOVERY"


class ResourceDisposition(StrEnum):
    AVAILABLE = "AVAILABLE"
    DEGRADED = "DEGRADED"
    DENIED = "DENIED"
    UNKNOWN = "UNKNOWN"


_CONTINUITY_ATTESTATION: Final = object()


def _positive(value: int, label: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise MarketTruthInputError(f"{label} must be positive")


def _non_negative(value: int, label: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise MarketTruthInputError(f"{label} must be non-negative")


def _token(value: str, label: str) -> None:
    if not isinstance(value, str) or not _TOKEN_PATTERN.fullmatch(value):
        raise MarketTruthInputError(f"{label} is not a bounded token")


def _hash(value: object) -> str:
    encoded = json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _fingerprint(value: str, label: str) -> None:
    if not isinstance(value, str) or not _HASH_PATTERN.fullmatch(value):
        raise MarketTruthInputError(f"{label} must be a lowercase SHA-256 fingerprint")


def _utc(value: datetime, label: str) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise MarketTruthInputError(f"{label} must be timezone-aware")
    return value.astimezone(UTC)


def _stable(value: StableId, kind: IdentityKind, label: str) -> None:
    if not isinstance(value, StableId) or value.kind is not kind:
        raise MarketTruthInputError(f"{label} has the wrong identity kind")


def _generation(value: GenerationRef, label: str = "generation") -> None:
    if not isinstance(value, GenerationRef):
        raise MarketTruthInputError(f"{label} is required")


@dataclass(frozen=True, slots=True)
class GenerationRef:
    """Environment-scoped local generation identity with retirement fencing."""

    source_id: StableId
    environment: Environment
    number: int
    retired: bool = False

    def __post_init__(self) -> None:
        _stable(self.source_id, IdentityKind.EXCHANGE, "generation source")
        if not isinstance(self.environment, Environment):
            raise MarketTruthInputError("generation environment is invalid")
        _positive(self.number, "generation number")
        if not isinstance(self.retired, bool):
            raise MarketTruthInputError("generation retired flag is invalid")

    @property
    def fingerprint(self) -> str:
        return _hash(
            {
                "source": self.source_id.as_text(),
                "environment": self.environment.value,
                "number": self.number,
                "retired": self.retired,
            }
        )

    def rollover(self, number: int) -> GenerationRef:
        _positive(number, "next generation number")
        if self.retired or number <= self.number:
            raise MarketTruthConsistencyError("generation rollover is not permitted")
        return GenerationRef(self.source_id, self.environment, number)

    def retire(self) -> GenerationRef:
        return replace(self, retired=True)

    def accepts(self, incoming: GenerationRef) -> bool:
        return (
            isinstance(incoming, GenerationRef)
            and not self.retired
            and not incoming.retired
            and self.source_id == incoming.source_id
            and self.environment is incoming.environment
            and self.number == incoming.number
        )


@dataclass(frozen=True, slots=True)
class ChannelCapability:
    """Immutable provider-neutral capability and sequence policy material."""

    source_id: StableId
    visibility: ChannelVisibility
    channel: str
    contract_scope: StableId | None
    schema_version: int
    snapshot_available: bool
    update_semantics: UpdateSemantics
    ordering_evidence: str
    sequence_field: str | None
    cadence_ms: int | None
    heartbeat_ms: int | None
    mode: SequenceMode
    contiguous_proof: bool
    timestamp_limit_ms: int | None = None
    policy_version: int = 1

    def __post_init__(self) -> None:
        _stable(self.source_id, IdentityKind.EXCHANGE, "capability source")
        if not isinstance(self.visibility, ChannelVisibility):
            raise MarketTruthInputError("invalid channel visibility")
        _token(self.channel, "channel")
        if self.contract_scope is not None:
            _stable(self.contract_scope, IdentityKind.INSTRUMENT, "contract scope")
        _positive(self.schema_version, "schema version")
        if not isinstance(self.snapshot_available, bool):
            raise MarketTruthInputError("snapshot availability must be boolean")
        if not isinstance(self.update_semantics, UpdateSemantics):
            raise MarketTruthInputError("invalid update semantics")
        _token(self.ordering_evidence, "ordering evidence")
        if self.sequence_field is not None:
            _token(self.sequence_field, "sequence field")
        if self.cadence_ms is not None:
            _positive(self.cadence_ms, "cadence")
        if self.heartbeat_ms is not None:
            _positive(self.heartbeat_ms, "heartbeat")
        if not isinstance(self.mode, SequenceMode):
            raise MarketTruthInputError("invalid sequence mode")
        if not isinstance(self.contiguous_proof, bool):
            raise MarketTruthInputError("contiguous proof must be boolean")
        if self.timestamp_limit_ms is not None:
            _non_negative(self.timestamp_limit_ms, "timestamp limit")
        _positive(self.policy_version, "policy version")
        if self.mode in (SequenceMode.STRICT_SEQUENCE, SequenceMode.MONOTONIC_UPDATE_ID):
            if self.sequence_field is None:
                raise MarketTruthConsistencyError("sequence mode requires an update field")
        if self.mode is SequenceMode.SNAPSHOT_ONLY and not self.snapshot_available:
            raise MarketTruthConsistencyError("snapshot-only mode requires snapshots")
        if (
            self.mode is SequenceMode.TIMESTAMP_ORDERED_WITH_LIMITS
            and self.timestamp_limit_ms is None
        ):
            raise MarketTruthConsistencyError("timestamp mode requires a bound")

    @property
    def fingerprint(self) -> str:
        return _hash(
            {
                "source": self.source_id.as_text(),
                "visibility": self.visibility.value,
                "channel": self.channel,
                "contract": self.contract_scope.as_text() if self.contract_scope else None,
                "schema_version": self.schema_version,
                "snapshot_available": self.snapshot_available,
                "update_semantics": self.update_semantics.value,
                "ordering_evidence": self.ordering_evidence,
                "sequence_field": self.sequence_field,
                "cadence_ms": self.cadence_ms,
                "heartbeat_ms": self.heartbeat_ms,
                "mode": self.mode.value,
                "contiguous_proof": self.contiguous_proof,
                "timestamp_limit_ms": self.timestamp_limit_ms,
                "policy_version": self.policy_version,
            }
        )


@dataclass(frozen=True, slots=True)
class SequenceObservation:
    """Normalized sequence evidence, never a venue DTO."""

    generation: GenerationRef
    observed_at: datetime
    event_fingerprint: str
    update_id: int | None = None
    is_snapshot: bool = False
    source_id: StableId | None = None
    channel: str | None = None
    contract_id: StableId | None = None
    schema_version: int | None = None
    capability_fingerprint: str | None = None
    capability_policy_version: int | None = None
    visibility: ChannelVisibility = ChannelVisibility.PUBLIC

    def __post_init__(self) -> None:
        _generation(self.generation)
        object.__setattr__(self, "observed_at", _utc(self.observed_at, "observed time"))
        _fingerprint(self.event_fingerprint, "event fingerprint")
        if self.update_id is not None:
            _non_negative(self.update_id, "update id")
        if not isinstance(self.is_snapshot, bool):
            raise MarketTruthInputError("snapshot flag must be boolean")
        if self.source_id is None:
            raise MarketTruthInputError("observation source is required")
        _stable(self.source_id, IdentityKind.EXCHANGE, "observation source")
        if self.source_id != self.generation.source_id:
            raise MarketTruthConsistencyError("observation source and generation differ")
        if self.channel is None:
            raise MarketTruthInputError("observation channel is required")
        _token(self.channel, "observation channel")
        if self.contract_id is None:
            raise MarketTruthInputError("observation contract is required")
        _stable(self.contract_id, IdentityKind.INSTRUMENT, "observation contract")
        if self.schema_version is None:
            raise MarketTruthInputError("observation schema version is required")
        _positive(self.schema_version, "observation schema version")
        if self.capability_fingerprint is None:
            raise MarketTruthInputError("observation capability fingerprint is required")
        _fingerprint(self.capability_fingerprint, "observation capability")
        if self.capability_policy_version is None:
            raise MarketTruthInputError("observation capability policy version is required")
        _positive(self.capability_policy_version, "observation capability policy version")
        if not isinstance(self.visibility, ChannelVisibility):
            raise MarketTruthInputError("observation visibility is invalid")


@dataclass(frozen=True, slots=True, init=False)
class SequenceContinuityState:
    """Evaluator-issued continuity state carried across accepted observations."""

    source_id: StableId
    generation: GenerationRef
    capability_fingerprint: str
    capability_policy_version: int
    last_event_fingerprint: str
    last_update_id: int | None
    synchronized: bool
    valid: bool
    _attestation: object

    def __init__(self, *args: object, **kwargs: object) -> None:
        raise MarketTruthInputError("SequenceContinuityState must be issued by evaluate_sequence")

    @classmethod
    def _from_evaluator(
        cls,
        *,
        capability: ChannelCapability,
        observation: SequenceObservation,
        synchronized: bool,
        valid: bool,
    ) -> SequenceContinuityState:
        instance = object.__new__(cls)
        object.__setattr__(instance, "source_id", capability.source_id)
        object.__setattr__(instance, "generation", observation.generation)
        object.__setattr__(instance, "capability_fingerprint", capability.fingerprint)
        object.__setattr__(instance, "capability_policy_version", capability.policy_version)
        object.__setattr__(instance, "last_event_fingerprint", observation.event_fingerprint)
        object.__setattr__(instance, "last_update_id", observation.update_id)
        object.__setattr__(instance, "synchronized", synchronized)
        object.__setattr__(instance, "valid", valid)
        object.__setattr__(instance, "_attestation", _CONTINUITY_ATTESTATION)
        return instance

    def _is_attested(self) -> bool:
        return self._attestation is _CONTINUITY_ATTESTATION

    def matches(self, capability: ChannelCapability, previous: SequenceObservation | None) -> bool:
        return (
            self._is_attested()
            and self.source_id == capability.source_id
            and self.capability_fingerprint == capability.fingerprint
            and self.capability_policy_version == capability.policy_version
            and previous is not None
            and self.generation == previous.generation
            and self.last_event_fingerprint == previous.event_fingerprint
            and self.last_update_id == previous.update_id
        )


@dataclass(frozen=True, slots=True)
class SequenceEvaluation:
    result: SequenceResultKind
    synchronized: bool
    reason: QualityReason | None = None
    continuity: SequenceContinuityState | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.result, SequenceResultKind):
            raise MarketTruthInputError("invalid sequence result")
        if not isinstance(self.synchronized, bool):
            raise MarketTruthInputError("synchronization flag must be boolean")
        if self.reason is not None and not isinstance(self.reason, QualityReason):
            raise MarketTruthInputError("invalid sequence reason")
        if self.continuity is not None:
            if not isinstance(self.continuity, SequenceContinuityState):
                raise MarketTruthInputError("invalid sequence continuity")
            if not self.continuity._is_attested():
                raise MarketTruthConsistencyError("sequence continuity is not evaluator-issued")
            if self.continuity.synchronized != self.synchronized:
                raise MarketTruthConsistencyError("sequence continuity does not match evaluation")
        expected_reason: QualityReason | None
        if self.result is SequenceResultKind.ACCEPT:
            expected_reason = QualityReason.UNSYNCHRONIZED if not self.synchronized else None
            if self.reason not in {expected_reason, None}:
                raise MarketTruthConsistencyError("accepted sequence has an invalid reason")
            if self.synchronized and self.reason is not None:
                raise MarketTruthConsistencyError(
                    "synchronized accepted sequence cannot carry a restriction reason"
                )
        elif self.result is SequenceResultKind.DUPLICATE:
            expected_reason = QualityReason.DUPLICATE
            if self.reason is not expected_reason:
                raise MarketTruthConsistencyError("duplicate sequence has an invalid reason")
        elif self.result is SequenceResultKind.OUT_OF_ORDER:
            expected_reason = QualityReason.OUT_OF_ORDER
            if self.synchronized or self.reason is not expected_reason:
                raise MarketTruthConsistencyError("out-of-order sequence must be unsynchronized")
        elif self.result is SequenceResultKind.GAP:
            expected_reason = QualityReason.GAP
            if self.synchronized or self.reason is not expected_reason:
                raise MarketTruthConsistencyError("gap sequence must be unsynchronized")
        elif self.result is SequenceResultKind.SEQUENCE_UNPROVABLE:
            expected_reason = QualityReason.SEQUENCE_UNPROVABLE
            if self.synchronized or self.reason is not expected_reason:
                raise MarketTruthConsistencyError("unprovable sequence must be unsynchronized")
        else:
            if self.synchronized or self.reason not in {
                QualityReason.RETIRED_GENERATION,
                QualityReason.SEQUENCE_UNPROVABLE,
                QualityReason.UNSYNCHRONIZED,
            }:
                raise MarketTruthConsistencyError(
                    "resynchronization-required sequence must be unsynchronized"
                )

    @property
    def requires_resynchronization(self) -> bool:
        return self.result in {
            SequenceResultKind.GAP,
            SequenceResultKind.RESYNC_REQUIRED,
            SequenceResultKind.SEQUENCE_UNPROVABLE,
        }


def evaluate_sequence(
    capability: ChannelCapability,
    previous: SequenceObservation | None,
    current: SequenceObservation,
    continuity: SequenceContinuityState | None = None,
) -> SequenceEvaluation:
    """Evaluate one observation while carrying evaluator-issued continuity state."""

    _validate_observation_capability(capability, current)
    if previous is not None:
        _validate_observation_capability(capability, previous)
        if (
            previous.source_id != current.source_id
            or previous.channel != current.channel
            or previous.contract_id != current.contract_id
            or previous.schema_version != current.schema_version
            or previous.capability_fingerprint != current.capability_fingerprint
            or previous.capability_policy_version != current.capability_policy_version
            or previous.visibility is not current.visibility
        ):
            raise MarketTruthConsistencyError("sequence observations have mixed identity")
    if continuity is not None and not continuity.matches(capability, previous):
        raise MarketTruthConsistencyError("sequence continuity does not match prior observation")

    def evaluated(
        result: SequenceResultKind,
        synchronized: bool,
        reason: QualityReason | None,
        *,
        valid: bool,
        preserve_continuity: bool = False,
    ) -> SequenceEvaluation:
        if preserve_continuity and continuity is not None:
            next_continuity = continuity
        else:
            source_observation = current if valid or previous is None else previous
            next_continuity = SequenceContinuityState._from_evaluator(
                capability=capability,
                observation=source_observation,
                synchronized=synchronized,
                valid=valid,
            )
        return SequenceEvaluation(result, synchronized, reason, next_continuity)

    if current.generation.retired:
        return evaluated(
            SequenceResultKind.RESYNC_REQUIRED,
            False,
            QualityReason.RETIRED_GENERATION,
            valid=False,
        )
    if current.generation.source_id != capability.source_id:
        raise MarketTruthConsistencyError("observation and capability source differ")
    if previous is not None and not previous.generation.accepts(current.generation):
        return evaluated(
            SequenceResultKind.RESYNC_REQUIRED,
            False,
            QualityReason.RETIRED_GENERATION,
            valid=False,
        )
    if capability.mode is SequenceMode.NO_PROVABLE_SEQUENCE:
        return evaluated(
            SequenceResultKind.SEQUENCE_UNPROVABLE,
            False,
            QualityReason.SEQUENCE_UNPROVABLE,
            valid=False,
        )
    if previous is not None and previous.event_fingerprint == current.event_fingerprint:
        synchronized = continuity.synchronized if continuity is not None else False
        return evaluated(
            SequenceResultKind.DUPLICATE,
            synchronized,
            QualityReason.DUPLICATE,
            valid=True,
            preserve_continuity=True,
        )
    if capability.mode is SequenceMode.SNAPSHOT_ONLY:
        if not current.is_snapshot:
            return evaluated(
                SequenceResultKind.SEQUENCE_UNPROVABLE,
                False,
                QualityReason.SEQUENCE_UNPROVABLE,
                valid=False,
            )
        if previous is not None and current.observed_at < previous.observed_at:
            return evaluated(
                SequenceResultKind.OUT_OF_ORDER,
                False,
                QualityReason.OUT_OF_ORDER,
                valid=False,
            )
        return evaluated(SequenceResultKind.ACCEPT, True, None, valid=True)
    if capability.mode is SequenceMode.TIMESTAMP_ORDERED_WITH_LIMITS:
        if previous is not None:
            assert capability.timestamp_limit_ms is not None
            age_ms = int((previous.observed_at - current.observed_at).total_seconds() * 1000)
            if age_ms > capability.timestamp_limit_ms:
                return evaluated(
                    SequenceResultKind.OUT_OF_ORDER,
                    False,
                    QualityReason.OUT_OF_ORDER,
                    valid=False,
                )
        if not current.is_snapshot:
            return evaluated(
                SequenceResultKind.SEQUENCE_UNPROVABLE,
                False,
                QualityReason.SEQUENCE_UNPROVABLE,
                valid=False,
            )
        return evaluated(SequenceResultKind.ACCEPT, True, None, valid=True)
    if current.update_id is None:
        return evaluated(
            SequenceResultKind.SEQUENCE_UNPROVABLE,
            False,
            QualityReason.SEQUENCE_UNPROVABLE,
            valid=False,
        )
    if previous is None:
        synchronized = current.is_snapshot
        return evaluated(
            SequenceResultKind.ACCEPT,
            synchronized,
            None if synchronized else QualityReason.UNSYNCHRONIZED,
            valid=True,
        )
    if previous.update_id is None:
        return evaluated(
            SequenceResultKind.SEQUENCE_UNPROVABLE,
            False,
            QualityReason.SEQUENCE_UNPROVABLE,
            valid=False,
        )
    if current.update_id < previous.update_id:
        return evaluated(
            SequenceResultKind.OUT_OF_ORDER,
            False,
            QualityReason.OUT_OF_ORDER,
            valid=False,
        )
    if current.update_id == previous.update_id:
        synchronized = continuity.synchronized if continuity is not None else False
        return evaluated(
            SequenceResultKind.DUPLICATE,
            synchronized,
            QualityReason.DUPLICATE,
            valid=True,
            preserve_continuity=True,
        )
    if current.is_snapshot:
        return evaluated(SequenceResultKind.ACCEPT, True, None, valid=True)
    if (
        capability.mode is SequenceMode.STRICT_SEQUENCE
        and current.update_id > previous.update_id + 1
    ):
        return evaluated(SequenceResultKind.GAP, False, QualityReason.GAP, valid=False)
    if (
        capability.mode is SequenceMode.MONOTONIC_UPDATE_ID
        and current.update_id > previous.update_id + 1
    ):
        if capability.contiguous_proof:
            return evaluated(SequenceResultKind.GAP, False, QualityReason.GAP, valid=False)
        return evaluated(
            SequenceResultKind.SEQUENCE_UNPROVABLE,
            False,
            QualityReason.SEQUENCE_UNPROVABLE,
            valid=False,
        )
    synchronized = continuity.synchronized if continuity is not None and continuity.valid else False
    return evaluated(
        SequenceResultKind.ACCEPT,
        synchronized,
        None if synchronized else QualityReason.UNSYNCHRONIZED,
        valid=True,
    )


def _validate_observation_capability(
    capability: ChannelCapability, observation: SequenceObservation
) -> None:
    if not isinstance(capability, ChannelCapability):
        raise MarketTruthInputError("channel capability is required")
    if observation.source_id != capability.source_id:
        raise MarketTruthConsistencyError("observation and capability source differ")
    if observation.channel != capability.channel:
        raise MarketTruthConsistencyError("observation and capability channel differ")
    if (
        capability.contract_scope is not None
        and observation.contract_id != capability.contract_scope
    ):
        raise MarketTruthConsistencyError("observation and capability contract differ")
    if observation.schema_version != capability.schema_version:
        raise MarketTruthConsistencyError("observation and capability schema differ")
    if observation.capability_fingerprint != capability.fingerprint:
        raise MarketTruthConsistencyError("observation capability fingerprint differs")
    if observation.capability_policy_version != capability.policy_version:
        raise MarketTruthConsistencyError("observation capability policy differs")
    if observation.visibility is not capability.visibility:
        raise MarketTruthConsistencyError("observation and capability visibility differ")


@dataclass(frozen=True, slots=True)
class NormalizedMarketEvent:
    """Immutable normalized public event envelope."""

    event_id: EnvironmentScopedId
    environment: Environment
    source_id: StableId
    channel: str
    contract_id: StableId
    schema_version: int
    generation: GenerationRef
    provenance_fingerprint: str
    payload_fingerprint: str
    event_time: datetime
    wall_receive_time: datetime
    monotonic_elapsed_ms: int
    capability_fingerprint: str
    capability_policy_version: int
    update_id: int | None = None
    is_snapshot: bool = False

    def __post_init__(self) -> None:
        if self.event_id.kind is not IdentityKind.EVIDENCE:
            raise MarketTruthInputError("event identity must use a typed evidence identity")
        if (
            not isinstance(self.environment, Environment)
            or self.event_id.environment is not self.environment
        ):
            raise MarketTruthConsistencyError("event environment identity mismatch")
        _stable(self.source_id, IdentityKind.EXCHANGE, "event source")
        _stable(self.contract_id, IdentityKind.INSTRUMENT, "event contract")
        _positive(self.schema_version, "event schema version")
        _generation(self.generation)
        if self.source_id != self.generation.source_id:
            raise MarketTruthConsistencyError("event source and generation differ")
        _token(self.channel, "event channel")
        if self.generation.environment is not self.environment:
            raise MarketTruthConsistencyError("event generation environment mismatch")
        _fingerprint(self.provenance_fingerprint, "event provenance")
        _fingerprint(self.payload_fingerprint, "event payload")
        _fingerprint(self.capability_fingerprint, "event capability")
        _positive(self.capability_policy_version, "event capability policy version")
        object.__setattr__(self, "event_time", _utc(self.event_time, "event time"))
        object.__setattr__(
            self, "wall_receive_time", _utc(self.wall_receive_time, "wall receive time")
        )
        _non_negative(self.monotonic_elapsed_ms, "monotonic elapsed time")
        if self.update_id is not None:
            _non_negative(self.update_id, "event update id")
        if not isinstance(self.is_snapshot, bool):
            raise MarketTruthInputError("event snapshot flag must be boolean")

    @property
    def fingerprint(self) -> str:
        return _hash(
            {
                "event_id": self.event_id.as_text(),
                "environment": self.environment.value,
                "source": self.source_id.as_text(),
                "channel": self.channel,
                "contract": self.contract_id.as_text(),
                "schema_version": self.schema_version,
                "generation": self.generation.fingerprint,
                "provenance": self.provenance_fingerprint,
                "payload": self.payload_fingerprint,
                "capability": self.capability_fingerprint,
                "capability_policy_version": self.capability_policy_version,
                "event_time": self.event_time.isoformat(),
                "wall_receive_time": self.wall_receive_time.isoformat(),
                "monotonic_elapsed_ms": self.monotonic_elapsed_ms,
                "update_id": self.update_id,
                "is_snapshot": self.is_snapshot,
            }
        )

    def sequence_observation(self) -> SequenceObservation:
        return SequenceObservation(
            generation=self.generation,
            observed_at=self.event_time,
            event_fingerprint=self.fingerprint,
            update_id=self.update_id,
            is_snapshot=self.is_snapshot,
            source_id=self.source_id,
            channel=self.channel,
            contract_id=self.contract_id,
            schema_version=self.schema_version,
            capability_fingerprint=self.capability_fingerprint,
            capability_policy_version=self.capability_policy_version,
            visibility=ChannelVisibility.PUBLIC,
        )


@dataclass(frozen=True, slots=True, init=False)
class ResourceAdmissionEvidence:
    """Read-only Module 29 seam bound to one canonical admission decision."""

    disposition: ResourceDisposition
    admission_fingerprint: str
    admission_outcome: AdmissionOutcome
    admission_reason: AdmissionReason

    def __init__(self, *args: object, **kwargs: object) -> None:
        raise MarketTruthInputError(
            "ResourceAdmissionEvidence must be derived from AdmissionDecision"
        )

    @classmethod
    def from_admission(cls, decision: AdmissionDecision) -> ResourceAdmissionEvidence:
        if not isinstance(decision, AdmissionDecision):
            raise MarketTruthInputError("canonical Module 29 admission decision is required")
        disposition = {
            AdmissionOutcome.ADMIT: ResourceDisposition.AVAILABLE,
            AdmissionOutcome.DEFER: ResourceDisposition.DEGRADED,
            AdmissionOutcome.SHED: ResourceDisposition.DENIED,
            AdmissionOutcome.CIRCUIT_OPEN: ResourceDisposition.DENIED,
            AdmissionOutcome.UNKNOWN: ResourceDisposition.UNKNOWN,
        }[decision.outcome]
        instance = object.__new__(cls)
        object.__setattr__(instance, "disposition", disposition)
        object.__setattr__(instance, "admission_fingerprint", decision.fingerprint)
        object.__setattr__(instance, "admission_outcome", decision.outcome)
        object.__setattr__(instance, "admission_reason", decision.reason)
        return instance

    @property
    def decision_fingerprint(self) -> str:
        return self.admission_fingerprint

    @property
    def outcome(self) -> AdmissionOutcome:
        return self.admission_outcome

    @property
    def reason(self) -> AdmissionReason:
        return self.admission_reason

    @property
    def snapshot_fingerprint(self) -> str:
        """Compatibility alias exposing only canonical decision provenance."""

        return self.admission_fingerprint


@dataclass(frozen=True, slots=True)
class QualityAssessment:
    """Independent quality predicates; a score cannot override any failure."""

    age_ms: int | None
    freshness_limit_ms: int | None
    sequence: SequenceEvaluation
    clock: ClockHealth
    schema_valid: bool | None
    provenance_valid: bool | None
    generation_valid: bool | None
    coherent: bool | None
    resource: ResourceAdmissionEvidence
    contradiction: bool = False
    explanatory_score: int | None = None

    def __post_init__(self) -> None:
        if self.age_ms is not None:
            _non_negative(self.age_ms, "quality age")
        if self.freshness_limit_ms is not None:
            _positive(self.freshness_limit_ms, "freshness limit")
        if not isinstance(self.sequence, SequenceEvaluation):
            raise MarketTruthInputError("sequence evidence is required")
        if not isinstance(self.clock, ClockHealth):
            raise MarketTruthInputError("clock evidence is required")
        for value, label in (
            (self.schema_valid, "schema validity"),
            (self.provenance_valid, "provenance validity"),
            (self.generation_valid, "generation validity"),
            (self.coherent, "coherency"),
        ):
            if value is not None and not isinstance(value, bool):
                raise MarketTruthInputError(f"{label} must be boolean or unknown")
        if not isinstance(self.resource, ResourceAdmissionEvidence):
            raise MarketTruthInputError("resource evidence is required")
        if not isinstance(self.contradiction, bool):
            raise MarketTruthInputError("contradiction flag must be boolean")
        if self.explanatory_score is not None and (
            isinstance(self.explanatory_score, bool)
            or not isinstance(self.explanatory_score, int)
            or not 0 <= self.explanatory_score <= 100
        ):
            raise MarketTruthInputError("explanatory score must be between zero and one hundred")


_ACTION_ALL: tuple[ActionClass, ...] = tuple(ActionClass)
_ACTION_NEW_RESTRICTED: tuple[ActionClass, ...] = (
    ActionClass.NEW_EXPOSURE,
    ActionClass.ADD_EXPOSURE,
)


@dataclass(frozen=True, slots=True, init=False)
class DataAuthorityDecision:
    """Validated restrictive evidence; affected actions are not permissions."""

    state: DataAuthorityState
    reasons: tuple[QualityReason, ...]
    affected_actions: tuple[ActionClass, ...]
    explanatory_score: int | None

    def __init__(
        self,
        state: DataAuthorityState,
        reasons: tuple[QualityReason, ...],
        affected_actions: tuple[ActionClass, ...],
        explanatory_score: int | None,
    ) -> None:
        raise MarketTruthInputError(
            "DataAuthorityDecision must be derived by derive_data_authority"
        )

    @classmethod
    def _from_derived(
        cls,
        state: DataAuthorityState,
        reasons: tuple[QualityReason, ...],
        affected_actions: tuple[ActionClass, ...],
        explanatory_score: int | None,
    ) -> DataAuthorityDecision:
        instance = object.__new__(cls)
        cls._validate_material(state, reasons, affected_actions, explanatory_score)
        object.__setattr__(instance, "state", state)
        object.__setattr__(instance, "reasons", reasons)
        object.__setattr__(instance, "affected_actions", affected_actions)
        object.__setattr__(instance, "explanatory_score", explanatory_score)
        return instance

    @staticmethod
    def _validate_material(
        state: DataAuthorityState,
        reasons: tuple[QualityReason, ...],
        affected_actions: tuple[ActionClass, ...],
        explanatory_score: int | None,
    ) -> None:
        if not isinstance(state, DataAuthorityState):
            raise MarketTruthInputError("invalid authority state")
        if not reasons or any(not isinstance(item, QualityReason) for item in reasons):
            raise MarketTruthInputError("authority reasons are required")
        if tuple(sorted(set(reasons), key=lambda item: item.value)) != reasons:
            raise MarketTruthInputError("authority reasons must be unique and ordered")
        if any(not isinstance(item, ActionClass) for item in affected_actions):
            raise MarketTruthInputError("invalid affected action")
        if tuple(item for item in _ACTION_ALL if item in affected_actions) != affected_actions:
            raise MarketTruthInputError("affected actions must be unique and canonical")
        if explanatory_score is not None and (
            isinstance(explanatory_score, bool)
            or not isinstance(explanatory_score, int)
            or not 0 <= explanatory_score <= 100
        ):
            raise MarketTruthInputError("invalid authority explanatory score")
        if state is DataAuthorityState.ALLOW_NEW_EXPOSURE:
            if reasons != (QualityReason.FRESH_VALID,) or affected_actions:
                raise MarketTruthConsistencyError(
                    "allowing authority requires fresh evidence and no affected actions"
                )
        elif not affected_actions:
            raise MarketTruthConsistencyError(
                "restrictive authority must identify affected actions"
            )

    @property
    def restrictive_only(self) -> bool:
        return self.state is not DataAuthorityState.ALLOW_NEW_EXPOSURE

    @property
    def allowed_actions(self) -> tuple[ActionClass, ...]:
        """S1E never grants action permission; downstream owners decide."""

        return ()


def derive_data_authority(assessment: QualityAssessment) -> DataAuthorityDecision:
    """Reduce hard predicates in restrictive order; score is explanatory only."""

    reasons: set[QualityReason] = set()
    if assessment.age_ms is None or assessment.freshness_limit_ms is None:
        reasons.add(QualityReason.EXPIRED)
    elif assessment.age_ms > assessment.freshness_limit_ms * 2:
        reasons.add(QualityReason.EXPIRED)
    elif assessment.age_ms > assessment.freshness_limit_ms:
        reasons.add(QualityReason.STALE)
    if assessment.sequence.reason is not None:
        reasons.add(assessment.sequence.reason)
    if not assessment.sequence.synchronized:
        reasons.add(QualityReason.UNSYNCHRONIZED)
    if assessment.clock is ClockHealth.DRIFT:
        reasons.add(QualityReason.CLOCK_DRIFT)
    elif assessment.clock is ClockHealth.JUMP:
        reasons.add(QualityReason.CLOCK_JUMP)
    elif assessment.clock is ClockHealth.UNTRUSTED:
        reasons.add(QualityReason.CLOCK_UNTRUSTED)
    if assessment.schema_valid is False:
        reasons.add(QualityReason.SCHEMA_QUARANTINED)
    elif assessment.schema_valid is None:
        reasons.add(QualityReason.SCHEMA_QUARANTINED)
    if assessment.provenance_valid is not True:
        reasons.add(QualityReason.MISSING_PROVENANCE)
    if assessment.generation_valid is not True:
        reasons.add(QualityReason.MISSING_GENERATION)
    if assessment.coherent is not True:
        reasons.add(QualityReason.CROSS_CHANNEL_CONTRADICTION)
    if assessment.contradiction:
        reasons.add(QualityReason.CROSS_CHANNEL_CONTRADICTION)
    if assessment.resource.disposition is ResourceDisposition.DENIED:
        reasons.add(QualityReason.RESOURCE_STARVATION)
    elif assessment.resource.disposition is ResourceDisposition.UNKNOWN:
        reasons.add(QualityReason.RESOURCE_UNKNOWN)
    elif assessment.resource.disposition is ResourceDisposition.DEGRADED:
        reasons.add(QualityReason.RESOURCE_DEGRADED)
    if not reasons:
        reasons.add(QualityReason.FRESH_VALID)
    ordered = tuple(sorted(reasons, key=lambda item: item.value))
    if (
        QualityReason.CROSS_CHANNEL_CONTRADICTION in reasons
        or QualityReason.SCHEMA_QUARANTINED in reasons
    ):
        state = DataAuthorityState.EMERGENCY
        actions = _ACTION_ALL
    elif assessment.resource.disposition is ResourceDisposition.UNKNOWN:
        state = DataAuthorityState.RECONCILIATION_ONLY
        actions = _ACTION_ALL
    elif assessment.resource.disposition is ResourceDisposition.DENIED:
        state = DataAuthorityState.REDUCE_ONLY
        actions = _ACTION_ALL
    elif any(
        reason
        in {
            QualityReason.EXPIRED,
            QualityReason.GAP,
            QualityReason.SEQUENCE_UNPROVABLE,
            QualityReason.RETIRED_GENERATION,
            QualityReason.CLOCK_JUMP,
            QualityReason.CLOCK_UNTRUSTED,
            QualityReason.MISSING_PROVENANCE,
            QualityReason.MISSING_GENERATION,
            QualityReason.OUT_OF_ORDER,
            QualityReason.UNSYNCHRONIZED,
        }
        for reason in reasons
    ):
        state = DataAuthorityState.NO_NEW_EXPOSURE
        actions = _ACTION_NEW_RESTRICTED
    elif any(
        reason
        in {
            QualityReason.STALE,
            QualityReason.CLOCK_DRIFT,
            QualityReason.DUPLICATE,
            QualityReason.RESOURCE_DEGRADED,
        }
        for reason in reasons
    ):
        state = DataAuthorityState.DEGRADED_NEW_EXPOSURE
        actions = _ACTION_NEW_RESTRICTED
    else:
        state = DataAuthorityState.ALLOW_NEW_EXPOSURE
        actions = ()
    return DataAuthorityDecision._from_derived(
        state, ordered, actions, assessment.explanatory_score
    )


@dataclass(frozen=True, slots=True, init=False)
class SynchronizationProof:
    """Evaluator-issued synchronization proof; caller-selected verification is forbidden."""

    source_id: StableId
    generation: GenerationRef
    mode: SequenceMode
    snapshot_fingerprint: str
    capability_fingerprint: str
    capability_policy_version: int
    verified: bool

    def __init__(self, *args: object, **kwargs: object) -> None:
        raise MarketTruthInputError(
            "SynchronizationProof must be derived from successful sequence evidence"
        )

    @classmethod
    def from_sequence_evaluation(
        cls,
        *,
        capability: ChannelCapability,
        generation: GenerationRef,
        snapshot_fingerprint: str,
        evaluation: SequenceEvaluation,
    ) -> SynchronizationProof:
        if not isinstance(capability, ChannelCapability):
            raise MarketTruthInputError("channel capability is required")
        _generation(generation)
        _fingerprint(snapshot_fingerprint, "proof snapshot")
        if not isinstance(evaluation, SequenceEvaluation):
            raise MarketTruthInputError("sequence evaluation is required")
        continuity = evaluation.continuity
        if (
            evaluation.result is not SequenceResultKind.ACCEPT
            or not evaluation.synchronized
            or continuity is None
            or not continuity.valid
            or not continuity.synchronized
            or not continuity._is_attested()
            or continuity.source_id != capability.source_id
            or continuity.generation != generation
            or continuity.capability_fingerprint != capability.fingerprint
            or continuity.capability_policy_version != capability.policy_version
            or continuity.last_event_fingerprint != snapshot_fingerprint
        ):
            raise MarketTruthConsistencyError(
                "synchronization proof requires evaluator-issued matching evidence"
            )
        instance = object.__new__(cls)
        object.__setattr__(instance, "source_id", capability.source_id)
        object.__setattr__(instance, "generation", generation)
        object.__setattr__(instance, "mode", capability.mode)
        object.__setattr__(instance, "snapshot_fingerprint", snapshot_fingerprint)
        object.__setattr__(instance, "capability_fingerprint", capability.fingerprint)
        object.__setattr__(instance, "capability_policy_version", capability.policy_version)
        object.__setattr__(instance, "verified", True)
        instance._validate_material()
        return instance

    def _validate_material(self) -> None:
        _stable(self.source_id, IdentityKind.EXCHANGE, "proof source")
        _generation(self.generation)
        if self.source_id != self.generation.source_id:
            raise MarketTruthConsistencyError("proof source and generation differ")
        if not isinstance(self.mode, SequenceMode):
            raise MarketTruthInputError("proof mode is invalid")
        _fingerprint(self.snapshot_fingerprint, "proof snapshot")
        _fingerprint(self.capability_fingerprint, "proof capability")
        _positive(self.capability_policy_version, "proof capability policy version")
        if not isinstance(self.verified, bool):
            raise MarketTruthInputError("proof verification must be boolean")
        if not self.verified:
            raise MarketTruthConsistencyError("synchronization proof must be verified")


_MARKET_TRUTH_DEGRADATION_REASONS: Final = frozenset(
    {
        QualityReason.STALE,
        QualityReason.DUPLICATE,
        QualityReason.CLOCK_DRIFT,
        QualityReason.CLOCK_JUMP,
        QualityReason.CLOCK_UNTRUSTED,
        QualityReason.GAP,
        QualityReason.OUT_OF_ORDER,
        QualityReason.SEQUENCE_UNPROVABLE,
        QualityReason.UNSYNCHRONIZED,
        QualityReason.EXPIRED,
        QualityReason.SCHEMA_QUARANTINED,
        QualityReason.MISSING_PROVENANCE,
        QualityReason.MISSING_GENERATION,
        QualityReason.CROSS_CHANNEL_CONTRADICTION,
        QualityReason.RETIRED_GENERATION,
    }
)


@dataclass(frozen=True, slots=True, init=False)
class UniverseLifecycleEvidence:
    """Typed read-only view of the S1C universe owner."""

    snapshot_id: StableId
    contract_id: StableId
    universe_generation: int
    state: UniverseEligibilityState
    reason_codes: tuple[str, ...]
    source_version: int
    snapshot_fingerprint: str
    entry_fingerprint: str

    def __init__(self, *args: object, **kwargs: object) -> None:
        raise MarketTruthInputError(
            "UniverseLifecycleEvidence must be resolved from a canonical UniverseSnapshot"
        )

    @classmethod
    def _from_canonical(
        cls, snapshot: UniverseSnapshot, entry: UniverseEntry
    ) -> UniverseLifecycleEvidence:
        instance = object.__new__(cls)
        cls._validate_material(
            snapshot.snapshot_id,
            entry.contract_id,
            snapshot.capability_version,
            entry.state,
            tuple(item.value for item in entry.reason_codes),
            snapshot.exchange_reference_version,
            snapshot.fingerprint,
            entry.fingerprint,
        )
        object.__setattr__(instance, "snapshot_id", snapshot.snapshot_id)
        object.__setattr__(instance, "contract_id", entry.contract_id)
        object.__setattr__(instance, "universe_generation", snapshot.capability_version)
        object.__setattr__(instance, "state", entry.state)
        object.__setattr__(
            instance, "reason_codes", tuple(item.value for item in entry.reason_codes)
        )
        object.__setattr__(instance, "source_version", snapshot.exchange_reference_version)
        object.__setattr__(instance, "snapshot_fingerprint", snapshot.fingerprint)
        object.__setattr__(instance, "entry_fingerprint", entry.fingerprint)
        return instance

    @staticmethod
    def _validate_material(
        snapshot_id: StableId,
        contract_id: StableId,
        universe_generation: int,
        state: UniverseEligibilityState,
        reason_codes: tuple[str, ...],
        source_version: int,
        snapshot_fingerprint: str,
        entry_fingerprint: str,
    ) -> None:
        _stable(snapshot_id, IdentityKind.UNIVERSE_SNAPSHOT, "universe snapshot")
        _stable(contract_id, IdentityKind.INSTRUMENT, "universe contract")
        _positive(universe_generation, "universe generation")
        if not isinstance(state, UniverseEligibilityState):
            raise MarketTruthInputError("invalid universe eligibility state")
        if not reason_codes or any(not isinstance(item, str) for item in reason_codes):
            raise MarketTruthInputError("universe reasons are required")
        _positive(source_version, "universe source version")
        _fingerprint(snapshot_fingerprint, "universe snapshot fingerprint")
        _fingerprint(entry_fingerprint, "universe entry fingerprint")

    @staticmethod
    def _canonical_entry(snapshot: UniverseSnapshot, contract_id: StableId) -> UniverseEntry:
        _stable(contract_id, IdentityKind.INSTRUMENT, "universe contract")
        for entry in snapshot.entries:
            if entry.contract_id == contract_id:
                return entry
        raise MarketTruthConsistencyError("universe contract is missing from its snapshot")

    @classmethod
    def from_snapshot(
        cls, snapshot: UniverseSnapshot, contract_id: StableId
    ) -> UniverseLifecycleEvidence:
        if not isinstance(snapshot, UniverseSnapshot):
            raise MarketTruthInputError("typed universe snapshot is required")
        return cls._from_canonical(snapshot, cls._canonical_entry(snapshot, contract_id))

    @classmethod
    def from_entry(
        cls, snapshot: UniverseSnapshot, entry: UniverseEntry
    ) -> UniverseLifecycleEvidence:
        if not isinstance(snapshot, UniverseSnapshot) or not isinstance(entry, UniverseEntry):
            raise MarketTruthInputError("typed universe evidence is required")
        canonical = cls._canonical_entry(snapshot, entry.contract_id)
        if entry != canonical or entry.fingerprint != canonical.fingerprint:
            raise MarketTruthConsistencyError("universe entry is not canonical snapshot material")
        return cls._from_canonical(snapshot, canonical)

    @property
    def restriction(self) -> LifecycleRestriction:
        if self.state is UniverseEligibilityState.INELIGIBLE:
            return LifecycleRestriction.NEW_EXPOSURE_DISABLED
        if self.state is UniverseEligibilityState.UNKNOWN:
            return LifecycleRestriction.ELIGIBILITY_UNKNOWN
        return LifecycleRestriction.NONE


@dataclass(frozen=True, slots=True)
class MarketStateSnapshot:
    """Generation-scoped coherent state; Module 5 remains its sole owner."""

    contract_id: StableId
    environment: Environment
    generation: GenerationRef
    source_id: StableId
    source_version: int
    provenance_fingerprint: str
    event_fingerprints: tuple[str, ...]
    trust: MarketStateTrust
    data_authority: DataAuthorityDecision
    synchronized: bool
    synchronization_proof: SynchronizationProof | None
    capability_fingerprint: str
    capability_policy_version: int
    lifecycle_restriction: LifecycleRestriction = LifecycleRestriction.NONE

    def __post_init__(self) -> None:
        _stable(self.contract_id, IdentityKind.INSTRUMENT, "state contract")
        if not isinstance(self.environment, Environment):
            raise MarketTruthInputError("state environment is invalid")
        _generation(self.generation)
        if self.generation.environment is not self.environment:
            raise MarketTruthConsistencyError("state generation environment differs")
        _stable(self.source_id, IdentityKind.EXCHANGE, "state source")
        if self.source_id != self.generation.source_id:
            raise MarketTruthConsistencyError("state source and generation differ")
        _positive(self.source_version, "state source version")
        _fingerprint(self.provenance_fingerprint, "state provenance")
        _fingerprint(self.capability_fingerprint, "state capability")
        _positive(self.capability_policy_version, "state capability policy version")
        if not self.event_fingerprints or any(
            not _HASH_PATTERN.fullmatch(item) for item in self.event_fingerprints
        ):
            raise MarketTruthInputError("state event fingerprints are required")
        if not isinstance(self.trust, MarketStateTrust):
            raise MarketTruthInputError("invalid market state trust")
        if not isinstance(self.data_authority, DataAuthorityDecision):
            raise MarketTruthInputError("data authority is required")
        if not isinstance(self.synchronized, bool):
            raise MarketTruthInputError("state synchronization must be boolean")
        if self.synchronized:
            if self.synchronization_proof is None or not self.synchronization_proof.verified:
                raise MarketTruthConsistencyError("synchronized state requires verified proof")
        if self.synchronization_proof is not None:
            if self.synchronization_proof.generation != self.generation:
                raise MarketTruthConsistencyError("state proof generation differs")
            if self.synchronization_proof.source_id != self.source_id:
                raise MarketTruthConsistencyError("state proof source differs")
            if self.synchronization_proof.capability_fingerprint != self.capability_fingerprint:
                raise MarketTruthConsistencyError("state proof capability differs")
            if (
                self.synchronization_proof.capability_policy_version
                != self.capability_policy_version
            ):
                raise MarketTruthConsistencyError("state proof capability policy differs")
        if self.trust is MarketStateTrust.TRUSTED and (
            not self.synchronized
            or self.synchronization_proof is None
            or not self.synchronization_proof.verified
            or any(
                reason in _MARKET_TRUTH_DEGRADATION_REASONS
                for reason in self.data_authority.reasons
            )
        ):
            raise MarketTruthConsistencyError(
                "trusted state lacks independent synchronization or quality proof"
            )
        if not isinstance(self.lifecycle_restriction, LifecycleRestriction):
            raise MarketTruthInputError("invalid lifecycle restriction")

    @property
    def fingerprint(self) -> str:
        return _hash(
            {
                "contract": self.contract_id.as_text(),
                "environment": self.environment.value,
                "generation": self.generation.fingerprint,
                "source": self.source_id.as_text(),
                "source_version": self.source_version,
                "provenance": self.provenance_fingerprint,
                "events": self.event_fingerprints,
                "trust": self.trust.value,
                "authority": self.data_authority.state.value,
                "synchronized": self.synchronized,
                "capability": self.capability_fingerprint,
                "capability_policy_version": self.capability_policy_version,
                "proof": self.synchronization_proof.snapshot_fingerprint
                if self.synchronization_proof
                else None,
                "lifecycle": self.lifecycle_restriction.value,
            }
        )


def apply_universe_lifecycle(
    state: MarketStateSnapshot, evidence: UniverseLifecycleEvidence
) -> MarketStateSnapshot:
    """Add lifecycle restriction without changing Market-State trust."""

    if state.contract_id != evidence.contract_id:
        raise MarketTruthConsistencyError("lifecycle and market-state contracts differ")
    return replace(state, lifecycle_restriction=evidence.restriction)


def accept_market_state(
    current: MarketStateSnapshot | None, candidate: MarketStateSnapshot
) -> MarketStateSnapshot:
    """Apply the generation firewall; old or retired evidence cannot mutate truth."""

    if candidate.generation.retired:
        raise MarketTruthConsistencyError("retired generation cannot be accepted")
    if current is None:
        return candidate
    if (
        current.contract_id != candidate.contract_id
        or current.environment is not candidate.environment
    ):
        raise MarketTruthConsistencyError("state identity boundary mismatch")
    if current.generation.retired:
        raise MarketTruthConsistencyError("current state is fenced by retired generation")
    if candidate.generation.source_id != current.generation.source_id:
        raise MarketTruthConsistencyError("state source generation mismatch")
    if candidate.generation.number < current.generation.number:
        raise MarketTruthConsistencyError("late prior generation cannot mutate current state")
    if candidate.generation.number > current.generation.number and not candidate.synchronized:
        raise MarketTruthConsistencyError("new generation requires synchronization proof")
    return candidate


@dataclass(frozen=True, slots=True)
class ProjectionLease:
    issued_elapsed_ms: int
    ttl_ms: int
    invalidated: bool = False
    invalidation_reason: str | None = None

    def __post_init__(self) -> None:
        _non_negative(self.issued_elapsed_ms, "lease issue time")
        _positive(self.ttl_ms, "lease ttl")
        if not isinstance(self.invalidated, bool):
            raise MarketTruthInputError("lease invalidation must be boolean")
        if self.invalidated and not self.invalidation_reason:
            raise MarketTruthConsistencyError("invalidated lease requires a reason")
        if self.invalidation_reason is not None:
            _token(self.invalidation_reason, "invalidation reason")

    def fresh_at(self, elapsed_ms: int) -> bool:
        _non_negative(elapsed_ms, "lease check time")
        return (
            not self.invalidated
            and self.issued_elapsed_ms <= elapsed_ms < self.issued_elapsed_ms + self.ttl_ms
        )


@dataclass(frozen=True, slots=True, init=False)
class ProjectionEnvelope:
    """Cache projection metadata; it cannot originate or upgrade authority."""

    source_id: StableId
    generation: GenerationRef
    state_fingerprint: str
    provenance_fingerprint: str
    trust: MarketStateTrust
    data_authority: DataAuthorityState
    lease: ProjectionLease
    lifecycle_restriction: LifecycleRestriction

    def __init__(self, *args: object, **kwargs: object) -> None:
        raise MarketTruthInputError("ProjectionEnvelope must be created by project_state")

    @classmethod
    def _from_material(
        cls,
        *,
        source_id: StableId,
        generation: GenerationRef,
        state_fingerprint: str,
        provenance_fingerprint: str,
        trust: MarketStateTrust,
        data_authority: DataAuthorityState,
        lease: ProjectionLease,
        lifecycle_restriction: LifecycleRestriction,
    ) -> ProjectionEnvelope:
        instance = object.__new__(cls)
        object.__setattr__(instance, "source_id", source_id)
        object.__setattr__(instance, "generation", generation)
        object.__setattr__(instance, "state_fingerprint", state_fingerprint)
        object.__setattr__(instance, "provenance_fingerprint", provenance_fingerprint)
        object.__setattr__(instance, "trust", trust)
        object.__setattr__(instance, "data_authority", data_authority)
        object.__setattr__(instance, "lease", lease)
        object.__setattr__(instance, "lifecycle_restriction", lifecycle_restriction)
        instance._validate_material()
        return instance

    def _validate_material(self) -> None:
        _stable(self.source_id, IdentityKind.EXCHANGE, "projection source")
        if self.source_id != self.generation.source_id:
            raise MarketTruthConsistencyError("projection source differs from generation")
        _fingerprint(self.state_fingerprint, "projection state")
        _fingerprint(self.provenance_fingerprint, "projection provenance")
        if not isinstance(self.trust, MarketStateTrust):
            raise MarketTruthInputError("projection trust is invalid")
        if not isinstance(self.data_authority, DataAuthorityState):
            raise MarketTruthInputError("projection authority is invalid")
        if not isinstance(self.lease, ProjectionLease):
            raise MarketTruthInputError("projection lease is required")
        if not isinstance(self.lifecycle_restriction, LifecycleRestriction):
            raise MarketTruthInputError("projection lifecycle is invalid")

    def fresh_at(self, elapsed_ms: int) -> bool:
        return self.lease.fresh_at(elapsed_ms)


def project_state(
    state: MarketStateSnapshot, *, issued_elapsed_ms: int, ttl_ms: int
) -> ProjectionEnvelope:
    """Create a projection from authoritative state; no reverse constructor exists."""

    return ProjectionEnvelope._from_material(
        source_id=state.source_id,
        generation=state.generation,
        state_fingerprint=state.fingerprint,
        provenance_fingerprint=state.provenance_fingerprint,
        trust=state.trust,
        data_authority=state.data_authority.state,
        lease=ProjectionLease(issued_elapsed_ms, ttl_ms),
        lifecycle_restriction=state.lifecycle_restriction,
    )


def invalidate_projection(projection: ProjectionEnvelope, reason: str) -> ProjectionEnvelope:
    if not isinstance(projection, ProjectionEnvelope):
        raise MarketTruthInputError("projection is required")
    _token(reason, "projection invalidation reason")
    return ProjectionEnvelope._from_material(
        source_id=projection.source_id,
        generation=projection.generation,
        state_fingerprint=projection.state_fingerprint,
        provenance_fingerprint=projection.provenance_fingerprint,
        trust=projection.trust,
        data_authority=projection.data_authority,
        lease=ProjectionLease(
            projection.lease.issued_elapsed_ms,
            projection.lease.ttl_ms,
            invalidated=True,
            invalidation_reason=reason,
        ),
        lifecycle_restriction=projection.lifecycle_restriction,
    )


def replay_sequence(
    capability: ChannelCapability, events: tuple[NormalizedMarketEvent, ...]
) -> tuple[SequenceEvaluation, ...]:
    """Deterministic fixture/replay seam with no clock, sleep, or external I/O."""

    observations = tuple(event.sequence_observation() for event in events)
    if not observations:
        return ()
    for observation in observations:
        _validate_observation_capability(capability, observation)
    identity = (
        observations[0].source_id,
        observations[0].channel,
        observations[0].contract_id,
        observations[0].schema_version,
        observations[0].capability_fingerprint,
        observations[0].capability_policy_version,
        observations[0].visibility,
        observations[0].generation.environment,
        observations[0].generation.number,
    )
    if any(
        (
            observation.source_id,
            observation.channel,
            observation.contract_id,
            observation.schema_version,
            observation.capability_fingerprint,
            observation.capability_policy_version,
            observation.visibility,
            observation.generation.environment,
            observation.generation.number,
        )
        != identity
        for observation in observations[1:]
    ):
        raise MarketTruthConsistencyError("replay inputs have mixed identity")

    previous: SequenceObservation | None = None
    continuity: SequenceContinuityState | None = None
    results: list[SequenceEvaluation] = []
    for current in observations:
        result = evaluate_sequence(capability, previous, current, continuity)
        results.append(result)
        if result.result is SequenceResultKind.ACCEPT:
            previous = current
            continuity = result.continuity
        elif previous is not None and result.continuity is not None:
            continuity = (
                result.continuity if result.continuity.matches(capability, previous) else None
            )
        else:
            continuity = None
    return tuple(results)
