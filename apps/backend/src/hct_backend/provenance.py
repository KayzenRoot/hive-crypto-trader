"""S0C backend-only integrity and configuration provenance primitives.

This module deliberately has no transport, persistence, provider, or runtime
mutation boundary.  It composes the frozen S0A envelopes and the typed S0B
scope/reference values.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Sequence
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from enum import StrEnum
from typing import Final

from hct_backend.contracts import (
    AuditEnvelope,
    Environment,
    EnvironmentScopedId,
    EvidenceEnvelope,
    IdentityKind,
    StableId,
)
from hct_backend.security import (
    CredentialRef,
    ExchangeAccountID,
    PolicyVersion,
    SecretRef,
    SecurityContext,
    TenantID,
)

_HASH_PATTERN: Final = re.compile(r"^[0-9a-f]{64}$")
_FIELD_PATTERN: Final = re.compile(r"^[a-z][a-z0-9_.-]{0,63}$")
_TEXT_PATTERN: Final = re.compile(r"^[^\x00-\x1f\x7f]{1,256}$")
_SECRET_TEXT_PATTERN: Final = re.compile(
    r"(?i)(?:-----begin|api[_-]?key|private[_-]?key|access[_-]?token|password|"
    r"gh[pousr]_|github_pat_|(?:AKIA|ASIA)[0-9A-Z]{16}|sk[_-][A-Za-z0-9_]{20,})"
)


class ProvenanceBoundaryError(ValueError):
    """Raised when a value leaves the S0C fail-closed boundary."""


class IntegrityError(ProvenanceBoundaryError):
    """Raised when a hash, link, scope, or correction proof is invalid."""


class TruthClass(StrEnum):
    AUTHORITATIVE = "AUTHORITATIVE"
    OBSERVED = "OBSERVED"
    DERIVED = "DERIVED"
    TELEMETRY = "TELEMETRY"


class SourceClass(StrEnum):
    SERVER_AUTHORITY = "SERVER_AUTHORITY"
    CONFIG_DECLARED = "CONFIG_DECLARED"
    RELEASE_DECLARED = "RELEASE_DECLARED"
    POLICY_DECLARED = "POLICY_DECLARED"
    OBSERVATION = "OBSERVATION"
    DERIVATION = "DERIVATION"
    TELEMETRY = "TELEMETRY"


class AuthorityClass(StrEnum):
    AUDIT_EVIDENCE = "AUDIT_EVIDENCE"
    CONFIG_PROVENANCE = "CONFIG_PROVENANCE"
    RELEASE_PROVENANCE = "RELEASE_PROVENANCE"
    POLICY_PROVENANCE = "POLICY_PROVENANCE"
    NO_TRADING_AUTHORITY = "NO_TRADING_AUTHORITY"


class AttributeKey(StrEnum):
    COMPONENT = "component"
    CONFIG_REF = "config_ref"
    CORRECTION_REASON = "correction_reason"
    POLICY_REF = "policy_ref"
    REASON_CODE = "reason_code"
    REFERENCE = "reference"
    RELEASE_REF = "release_ref"
    RESULT = "result"
    SUMMARY = "summary"


class ConfigField(StrEnum):
    COMPONENT = "component"
    DESCRIPTION = "description"
    MODE = "mode"
    POLICY_REF = "policy_ref"
    RELEASE_REF = "release_ref"
    SCHEMA_VERSION = "schema_version"
    VALUE_REF = "value_ref"


class ConfigKind(StrEnum):
    RELEASE = "RELEASE"
    CONFIGURATION = "CONFIGURATION"
    POLICY = "POLICY"


_CANONICAL_BASE_FIELDS: Final = frozenset(
    {
        "authority",
        "config_fingerprint",
        "config_kind",
        "correction_of",
        "environment",
        "event_type",
        "identity",
        "payload_hash",
        "policy_version",
        "predecessor",
        "provenance_id",
        "record_type",
        "recorded_at",
        "release_id",
        "sequence",
        "snapshot_id",
        "source",
        "truth",
        "version",
    }
)


type CanonicalAtom = str | int | bool | None
type SafeValue = (
    str
    | int
    | bool
    | None
    | CredentialRef
    | SecretRef
    | PolicyVersion
    | StableId
)


def _utc(value: datetime, label: str) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise ProvenanceBoundaryError(f"{label} must be timezone-aware")
    return value.astimezone(UTC)


def _timestamp(value: datetime) -> str:
    return _utc(value, "timestamp").isoformat(timespec="microseconds").replace("+00:00", "Z")


def _safe_text(value: str, label: str) -> str:
    if not isinstance(value, str) or not _TEXT_PATTERN.fullmatch(value):
        raise ProvenanceBoundaryError(f"invalid {label}")
    if _SECRET_TEXT_PATTERN.search(value):
        raise ProvenanceBoundaryError(f"secret-shaped {label} is not permitted")
    return value


def _canonical_atom(value: SafeValue | Environment | object) -> CanonicalAtom:
    if value is None or isinstance(value, (bool, int)):
        return value
    if isinstance(value, str):
        return _safe_text(value, "canonical text")
    if isinstance(value, Environment):
        return value.value
    if isinstance(value, PolicyVersion):
        return f"POLICY:{value.value}"
    if isinstance(value, StableId):
        return value.as_text()
    if isinstance(value, (CredentialRef, SecretRef)):
        return f"OPAQUE:{type(value).__name__}"
    raise ProvenanceBoundaryError("unsupported canonical value")


def canonicalize(fields: tuple[tuple[str, SafeValue], ...]) -> bytes:
    """Canonicalize only a tuple of allowlisted scalar field pairs.

    Mapping, sequence, arbitrary object, and nested payload inputs are not
    accepted.  The tuple may be supplied in any order; duplicate keys are
    rejected and the canonical output is sorted by key.
    """

    if not isinstance(fields, tuple):
        raise ProvenanceBoundaryError("canonical fields must be a tuple")
    values: dict[str, CanonicalAtom] = {}
    for field in fields:
        if not isinstance(field, tuple) or len(field) != 2:
            raise ProvenanceBoundaryError("canonical field pairs are required")
        key, value = field
        if (
            not isinstance(key, str)
            or not _FIELD_PATTERN.fullmatch(key)
            or key in values
            or not (
                key in _CANONICAL_BASE_FIELDS
                or (
                    key.startswith("attribute.")
                    and key[10:] in {item.value for item in AttributeKey}
                )
                or (
                    key.startswith("metadata.")
                    and key[9:] in {item.value for item in ConfigField}
                )
                or (key.startswith("scope.") and key[6:] in {"account", "environment", "tenant"})
            )
        ):
            raise ProvenanceBoundaryError("invalid or duplicate canonical field")
        values[key] = _canonical_atom(value)
    return json.dumps(
        {key: values[key] for key in sorted(values)},
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def fingerprint(fields: tuple[tuple[str, SafeValue], ...]) -> str:
    """Return the SHA-256 fingerprint of the bounded canonical field set."""

    return hashlib.sha256(canonicalize(fields)).hexdigest()


def _validate_hash(value: str, label: str) -> str:
    if not isinstance(value, str) or not _HASH_PATTERN.fullmatch(value):
        raise IntegrityError(f"invalid {label}")
    return value


def _id_text(identity: EnvironmentScopedId) -> str:
    return identity.as_text()


def _scope_fields(
    scope: ProvenanceScope, prefix: str = "scope"
) -> tuple[tuple[str, SafeValue], ...]:
    return (
        (f"{prefix}.account", scope.account_id.value if scope.account_id is not None else "none"),
        (f"{prefix}.environment", scope.environment.value),
        (f"{prefix}.tenant", scope.tenant_id.value),
    )


@dataclass(frozen=True, slots=True)
class ProvenanceScope:
    """Exact environment/tenant/account namespace for a provenance value."""

    environment: Environment
    tenant_id: TenantID
    account_id: ExchangeAccountID | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.environment, Environment):
            raise ProvenanceBoundaryError("invalid provenance environment")
        if not isinstance(self.tenant_id, TenantID):
            raise ProvenanceBoundaryError("invalid provenance tenant")
        if self.account_id is not None and not isinstance(self.account_id, ExchangeAccountID):
            raise ProvenanceBoundaryError("invalid provenance account")


def _attribute_value(value: object, label: str) -> SafeValue:
    if isinstance(value, str):
        return _safe_text(value, label)
    if isinstance(value, (bool, int)) or value is None:
        return value
    if isinstance(value, (CredentialRef, SecretRef, PolicyVersion, StableId)):
        return value
    raise ProvenanceBoundaryError(f"unsupported {label} type")


@dataclass(frozen=True, slots=True)
class RecordAttribute:
    key: AttributeKey
    value: SafeValue

    def __post_init__(self) -> None:
        if not isinstance(self.key, AttributeKey):
            raise ProvenanceBoundaryError("record attributes require controlled keys")
        _attribute_value(self.value, "record attribute")


@dataclass(frozen=True, slots=True)
class ConfigAttribute:
    key: ConfigField
    value: SafeValue

    def __post_init__(self) -> None:
        if not isinstance(self.key, ConfigField):
            raise ProvenanceBoundaryError("configuration metadata requires controlled keys")
        _attribute_value(self.value, "configuration metadata")


def _record_attributes(
    attributes: tuple[RecordAttribute, ...]
) -> tuple[tuple[str, SafeValue], ...]:
    if not isinstance(attributes, tuple):
        raise ProvenanceBoundaryError("record attributes must be an immutable tuple")
    if any(not isinstance(attribute, RecordAttribute) for attribute in attributes):
        raise ProvenanceBoundaryError("record attributes must be typed and unique")
    keys = [attribute.key.value for attribute in attributes]
    if len(keys) != len(set(keys)):
        raise ProvenanceBoundaryError("record attributes must be typed and unique")
    ordered = sorted(
        ((attribute.key.value, attribute) for attribute in attributes), key=lambda item: item[0]
    )
    return tuple(
        (f"attribute.{key}", _attribute_value(value.value, "record attribute"))
        for key, value in ordered
    )


def _config_attributes(
    attributes: tuple[ConfigAttribute, ...]
) -> tuple[tuple[str, SafeValue], ...]:
    if not isinstance(attributes, tuple):
        raise ProvenanceBoundaryError("configuration metadata must be an immutable tuple")
    if any(not isinstance(attribute, ConfigAttribute) for attribute in attributes):
        raise ProvenanceBoundaryError("configuration metadata must be typed and unique")
    keys = [attribute.key.value for attribute in attributes]
    if len(keys) != len(set(keys)):
        raise ProvenanceBoundaryError("configuration metadata must be typed and unique")
    ordered = sorted(
        ((attribute.key.value, attribute) for attribute in attributes), key=lambda item: item[0]
    )
    return tuple(
        (f"metadata.{key}", _attribute_value(value.value, "configuration metadata"))
        for key, value in ordered
    )


def _validate_truth_source_authority(
    truth: TruthClass, source: SourceClass, authority: AuthorityClass
) -> None:
    expected_sources = {
        TruthClass.AUTHORITATIVE: {
            SourceClass.SERVER_AUTHORITY,
            SourceClass.CONFIG_DECLARED,
            SourceClass.RELEASE_DECLARED,
            SourceClass.POLICY_DECLARED,
        },
        TruthClass.OBSERVED: {SourceClass.OBSERVATION},
        TruthClass.DERIVED: {SourceClass.DERIVATION},
        TruthClass.TELEMETRY: {SourceClass.TELEMETRY},
    }
    if source not in expected_sources[truth]:
        raise ProvenanceBoundaryError("truth and source classes are incompatible")
    expected_authority = {
        SourceClass.SERVER_AUTHORITY: AuthorityClass.AUDIT_EVIDENCE,
        SourceClass.CONFIG_DECLARED: AuthorityClass.CONFIG_PROVENANCE,
        SourceClass.RELEASE_DECLARED: AuthorityClass.RELEASE_PROVENANCE,
        SourceClass.POLICY_DECLARED: AuthorityClass.POLICY_PROVENANCE,
        SourceClass.OBSERVATION: AuthorityClass.AUDIT_EVIDENCE,
        SourceClass.DERIVATION: AuthorityClass.NO_TRADING_AUTHORITY,
        SourceClass.TELEMETRY: AuthorityClass.NO_TRADING_AUTHORITY,
    }
    if authority is not expected_authority[source]:
        raise ProvenanceBoundaryError("source cannot grant the requested authority")


def _payload_fields(
    *,
    record_type: str,
    identity: EnvironmentScopedId,
    environment: Environment,
    event_type: str,
    recorded_at: datetime,
    scope: ProvenanceScope,
    truth: TruthClass,
    source: SourceClass,
    authority: AuthorityClass,
    record_version: int,
    attributes: tuple[RecordAttribute, ...],
    correction_of: EnvironmentScopedId | None,
) -> tuple[tuple[str, SafeValue], ...]:
    fields: list[tuple[str, SafeValue]] = [
        ("authority", authority.value),
        ("environment", environment.value),
        ("event_type", event_type),
        ("identity", _id_text(identity)),
        ("record_type", record_type),
        ("recorded_at", _timestamp(recorded_at)),
        ("version", record_version),
        ("source", source.value),
        ("truth", truth.value),
        *_scope_fields(scope),
        *_record_attributes(attributes),
    ]
    if correction_of is not None:
        fields.append(("correction_of", _id_text(correction_of)))
    return tuple(fields)


def _domain_fields(record: AuditRecord | EvidenceRecord) -> tuple[tuple[str, SafeValue], ...]:
    if isinstance(record, AuditRecord):
        record_type = "audit"
        fields = list(
            _payload_fields(
                record_type=record_type,
                identity=record.record_id,
                environment=record.environment,
                event_type=record.envelope.event_type,
                recorded_at=record.envelope.occurred_at,
                scope=record.scope,
                truth=record.truth,
                source=record.source,
                authority=record.authority,
                record_version=record.record_version,
                attributes=record.attributes,
                correction_of=record.correction_of,
            )
        )
        payload_hash = record.envelope.payload_hash
    else:
        record_type = "evidence"
        fields = list(
            _payload_fields(
                record_type=record_type,
                identity=record.record_id,
                environment=record.environment,
                event_type=record.envelope.evidence_type,
                recorded_at=record.recorded_at,
                scope=record.scope,
                truth=record.truth,
                source=record.source,
                authority=record.authority,
                record_version=record.record_version,
                attributes=record.attributes,
                correction_of=record.correction_of,
            )
        )
        payload_hash = record.envelope.payload_hash
    fields.extend(
        (
            ("payload_hash", payload_hash),
            ("predecessor", record.predecessor_fingerprint or "none"),
            ("sequence", record.sequence),
        )
    )
    return tuple(fields)


@dataclass(frozen=True, slots=True)
class AuditRecord:
    """Immutable domain record composed around the public S0A audit envelope."""

    envelope: AuditEnvelope
    scope: ProvenanceScope
    truth: TruthClass
    source: SourceClass
    authority: AuthorityClass
    record_version: int = 1
    attributes: tuple[RecordAttribute, ...] = ()
    correction_of: EnvironmentScopedId | None = None
    sequence: int = 0
    predecessor_fingerprint: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.envelope, AuditEnvelope) or not isinstance(
            self.scope, ProvenanceScope
        ):
            raise ProvenanceBoundaryError("invalid audit record envelope or scope")
        if self.envelope.event_id.kind.value != "AUDIT":
            raise ProvenanceBoundaryError("audit record requires an audit identity")
        if self.envelope.environment is not self.scope.environment:
            raise IntegrityError("audit environment and scope mismatch")
        if not all(isinstance(item, value) for item, value in (
            (self.truth, TruthClass),
            (self.source, SourceClass),
            (self.authority, AuthorityClass),
        )):
            raise ProvenanceBoundaryError("invalid audit truth/source/authority")
        _validate_truth_source_authority(self.truth, self.source, self.authority)
        if (
            not isinstance(self.record_version, int)
            or isinstance(self.record_version, bool)
            or self.record_version < 1
        ):
            raise ProvenanceBoundaryError("invalid audit record version")
        _record_attributes(self.attributes)
        if self.correction_of is not None:
            if self.correction_of.environment is not self.environment:
                raise IntegrityError("correction crosses environment")
            if self.correction_of == self.record_id:
                raise IntegrityError("correction must have a new identity")
        self._validate_link_fields()
        self.verify()

    @classmethod
    def create(
        cls,
        *,
        event_id: EnvironmentScopedId,
        environment: Environment,
        event_type: str,
        occurred_at: datetime,
        scope: ProvenanceScope,
        truth: TruthClass,
        source: SourceClass,
        authority: AuthorityClass,
        record_version: int = 1,
        attributes: tuple[RecordAttribute, ...] = (),
        correction_of: EnvironmentScopedId | None = None,
    ) -> AuditRecord:
        _utc(occurred_at, "occurred_at")
        payload_hash = fingerprint(
            _payload_fields(
                record_type="audit",
                identity=event_id,
                environment=environment,
                event_type=event_type,
                recorded_at=occurred_at,
                scope=scope,
                truth=truth,
                source=source,
                authority=authority,
                record_version=record_version,
                attributes=attributes,
                correction_of=correction_of,
            )
        )
        return cls(
            envelope=AuditEnvelope(
                event_id=event_id,
                environment=environment,
                event_type=event_type,
                payload_hash=payload_hash,
                occurred_at=occurred_at,
            ),
            scope=scope,
            truth=truth,
            source=source,
            authority=authority,
            record_version=record_version,
            attributes=attributes,
            correction_of=correction_of,
        )

    @property
    def record_id(self) -> EnvironmentScopedId:
        return self.envelope.event_id

    @property
    def environment(self) -> Environment:
        return self.envelope.environment

    @property
    def fingerprint(self) -> str:
        return fingerprint(_domain_fields(self))

    def _validate_link_fields(self) -> None:
        if (
            not isinstance(self.sequence, int)
            or isinstance(self.sequence, bool)
            or self.sequence < 0
        ):
            raise IntegrityError("invalid record sequence")
        if self.sequence == 0 and self.predecessor_fingerprint is not None:
            raise IntegrityError("unlinked record cannot carry a predecessor")
        if self.sequence > 0 and self.predecessor_fingerprint is not None:
            _validate_hash(self.predecessor_fingerprint, "predecessor fingerprint")

    def verify(self) -> None:
        expected = fingerprint(
            _payload_fields(
                record_type="audit",
                identity=self.record_id,
                environment=self.environment,
                event_type=self.envelope.event_type,
                recorded_at=self.envelope.occurred_at,
                scope=self.scope,
                truth=self.truth,
                source=self.source,
                authority=self.authority,
                record_version=self.record_version,
                attributes=self.attributes,
                correction_of=self.correction_of,
            )
        )
        if self.envelope.payload_hash != expected:
            raise IntegrityError("audit payload hash mismatch")


@dataclass(frozen=True, slots=True)
class EvidenceRecord:
    """Immutable domain record composed around the public S0A evidence envelope."""

    envelope: EvidenceEnvelope
    recorded_at: datetime
    scope: ProvenanceScope
    truth: TruthClass
    source: SourceClass
    authority: AuthorityClass
    record_version: int = 1
    attributes: tuple[RecordAttribute, ...] = ()
    correction_of: EnvironmentScopedId | None = None
    sequence: int = 0
    predecessor_fingerprint: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.envelope, EvidenceEnvelope) or not isinstance(
            self.scope, ProvenanceScope
        ):
            raise ProvenanceBoundaryError("invalid evidence record envelope or scope")
        if self.envelope.evidence_id.kind.value != "EVIDENCE":
            raise ProvenanceBoundaryError("evidence record requires an evidence identity")
        if self.envelope.environment is not self.scope.environment:
            raise IntegrityError("evidence environment and scope mismatch")
        if not all(isinstance(item, value) for item, value in (
            (self.truth, TruthClass),
            (self.source, SourceClass),
            (self.authority, AuthorityClass),
        )):
            raise ProvenanceBoundaryError("invalid evidence truth/source/authority")
        _validate_truth_source_authority(self.truth, self.source, self.authority)
        if (
            not isinstance(self.record_version, int)
            or isinstance(self.record_version, bool)
            or self.record_version < 1
        ):
            raise ProvenanceBoundaryError("invalid evidence record version")
        _record_attributes(self.attributes)
        _utc(self.recorded_at, "recorded_at")
        if self.correction_of is not None:
            if self.correction_of.environment is not self.environment:
                raise IntegrityError("correction crosses environment")
            if self.correction_of == self.record_id:
                raise IntegrityError("correction must have a new identity")
        self._validate_link_fields()
        self.verify()

    @classmethod
    def create(
        cls,
        *,
        evidence_id: EnvironmentScopedId,
        environment: Environment,
        evidence_type: str,
        recorded_at: datetime,
        scope: ProvenanceScope,
        truth: TruthClass,
        source: SourceClass,
        authority: AuthorityClass,
        record_version: int = 1,
        attributes: tuple[RecordAttribute, ...] = (),
        correction_of: EnvironmentScopedId | None = None,
    ) -> EvidenceRecord:
        _utc(recorded_at, "recorded_at")
        payload_hash = fingerprint(
            _payload_fields(
                record_type="evidence",
                identity=evidence_id,
                environment=environment,
                event_type=evidence_type,
                recorded_at=recorded_at,
                scope=scope,
                truth=truth,
                source=source,
                authority=authority,
                record_version=record_version,
                attributes=attributes,
                correction_of=correction_of,
            )
        )
        return cls(
            envelope=EvidenceEnvelope(
                evidence_id=evidence_id,
                environment=environment,
                evidence_type=evidence_type,
                payload_hash=payload_hash,
            ),
            recorded_at=recorded_at,
            scope=scope,
            truth=truth,
            source=source,
            authority=authority,
            record_version=record_version,
            attributes=attributes,
            correction_of=correction_of,
        )

    @property
    def record_id(self) -> EnvironmentScopedId:
        return self.envelope.evidence_id

    @property
    def environment(self) -> Environment:
        return self.envelope.environment

    @property
    def fingerprint(self) -> str:
        return fingerprint(_domain_fields(self))

    def _validate_link_fields(self) -> None:
        if (
            not isinstance(self.sequence, int)
            or isinstance(self.sequence, bool)
            or self.sequence < 0
        ):
            raise IntegrityError("invalid record sequence")
        if self.sequence == 0 and self.predecessor_fingerprint is not None:
            raise IntegrityError("unlinked record cannot carry a predecessor")
        if self.sequence > 0 and self.predecessor_fingerprint is not None:
            _validate_hash(self.predecessor_fingerprint, "predecessor fingerprint")

    def verify(self) -> None:
        expected = fingerprint(
            _payload_fields(
                record_type="evidence",
                identity=self.record_id,
                environment=self.environment,
                event_type=self.envelope.evidence_type,
                recorded_at=self.recorded_at,
                scope=self.scope,
                truth=self.truth,
                source=self.source,
                authority=self.authority,
                record_version=self.record_version,
                attributes=self.attributes,
                correction_of=self.correction_of,
            )
        )
        if self.envelope.payload_hash != expected:
            raise IntegrityError("evidence payload hash mismatch")


type Record = AuditRecord | EvidenceRecord


def link_record(record: Record, *, sequence: int, predecessor_fingerprint: str | None) -> Record:
    """Create a linked immutable copy; the source record is never changed."""

    if not isinstance(record, (AuditRecord, EvidenceRecord)):
        raise IntegrityError("invalid record to link")
    if sequence < 1 or (sequence == 1 and predecessor_fingerprint is not None):
        raise IntegrityError("invalid first link")
    if sequence > 1:
        _validate_hash(predecessor_fingerprint or "", "predecessor fingerprint")
    if record.sequence != 0 or record.predecessor_fingerprint is not None:
        raise IntegrityError("record is already linked")
    return replace(record, sequence=sequence, predecessor_fingerprint=predecessor_fingerprint)


def verify_chain(records: Sequence[Record]) -> None:
    """Verify ordered, linked, same-scope records and fail on gaps/reorder."""

    if not isinstance(records, (tuple, list)):
        raise IntegrityError("chain must be an ordered immutable/list sequence")
    previous: Record | None = None
    for expected_sequence, record in enumerate(records, start=1):
        if not isinstance(record, (AuditRecord, EvidenceRecord)):
            raise IntegrityError("chain contains an unsupported record")
        record.verify()
        if record.sequence != expected_sequence:
            raise IntegrityError("chain sequence mismatch")
        if previous is None:
            if record.predecessor_fingerprint is not None:
                raise IntegrityError("chain first predecessor mismatch")
        elif record.predecessor_fingerprint != previous.fingerprint:
            raise IntegrityError("chain predecessor mismatch")
        if previous is not None and (
            record.environment is not previous.environment or record.scope != previous.scope
        ):
            raise IntegrityError("chain scope mismatch")
        previous = record


@dataclass(frozen=True, slots=True)
class AppendOnlyChain:
    """Immutable in-memory append-only chain; no persistence operation exists."""

    records: tuple[Record, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.records, tuple):
            raise IntegrityError("chain records must be an immutable tuple")
        verify_chain(self.records)

    def append(self, record: Record) -> AppendOnlyChain:
        if record.sequence != 0 or record.predecessor_fingerprint is not None:
            raise IntegrityError("append requires an unlinked record")
        predecessor = self.records[-1].fingerprint if self.records else None
        linked = link_record(
            record, sequence=len(self.records) + 1, predecessor_fingerprint=predecessor
        )
        assert isinstance(linked, (AuditRecord, EvidenceRecord))
        return AppendOnlyChain(records=(*self.records, linked))


def _validate_correction(original: Record, correction: Record) -> None:
    if correction.correction_of != original.record_id:
        raise IntegrityError("correction predecessor mismatch")
    if correction.record_id == original.record_id:
        raise IntegrityError("correction identity must be new")
    if correction.environment is not original.environment or correction.scope != original.scope:
        raise IntegrityError("correction scope mismatch")
    if correction.fingerprint == original.fingerprint:
        raise IntegrityError("correction fingerprint must be new")


def correct_audit_record(
    original: AuditRecord,
    *,
    event_id: EnvironmentScopedId,
    occurred_at: datetime,
    attributes: tuple[RecordAttribute, ...],
) -> AuditRecord:
    if event_id.environment is not original.environment:
        raise IntegrityError("correction crosses environment")
    corrected = AuditRecord.create(
        event_id=event_id,
        environment=original.environment,
        event_type=original.envelope.event_type,
        occurred_at=occurred_at,
        scope=original.scope,
        truth=original.truth,
        source=original.source,
        authority=original.authority,
        record_version=original.record_version,
        attributes=attributes,
        correction_of=original.record_id,
    )
    _validate_correction(original, corrected)
    return corrected


def correct_evidence_record(
    original: EvidenceRecord,
    *,
    evidence_id: EnvironmentScopedId,
    recorded_at: datetime,
    attributes: tuple[RecordAttribute, ...],
) -> EvidenceRecord:
    if evidence_id.environment is not original.environment:
        raise IntegrityError("correction crosses environment")
    corrected = EvidenceRecord.create(
        evidence_id=evidence_id,
        environment=original.environment,
        evidence_type=original.envelope.evidence_type,
        recorded_at=recorded_at,
        scope=original.scope,
        truth=original.truth,
        source=original.source,
        authority=original.authority,
        record_version=original.record_version,
        attributes=attributes,
        correction_of=original.record_id,
    )
    _validate_correction(original, corrected)
    return corrected


@dataclass(frozen=True, slots=True)
class ConfigSnapshot:
    """Immutable safe configuration metadata; no raw configuration mapping."""

    snapshot_id: EnvironmentScopedId
    environment: Environment
    config_kind: ConfigKind
    version: int
    attributes: tuple[ConfigAttribute, ...] = ()

    def __post_init__(self) -> None:
        if self.snapshot_id.kind.value != "CONFIG":
            raise ProvenanceBoundaryError("configuration snapshot requires a config identity")
        if self.snapshot_id.environment is not self.environment:
            raise IntegrityError("configuration snapshot environment mismatch")
        if not isinstance(self.config_kind, ConfigKind):
            raise ProvenanceBoundaryError("invalid configuration kind")
        if not isinstance(self.version, int) or isinstance(self.version, bool) or self.version < 1:
            raise ProvenanceBoundaryError("invalid configuration version")
        _config_attributes(self.attributes)

    @property
    def fingerprint(self) -> str:
        fields: list[tuple[str, SafeValue]] = [
            ("config_kind", self.config_kind.value),
            ("environment", self.environment.value),
            ("snapshot_id", self.snapshot_id.as_text()),
            ("version", self.version),
            *_config_attributes(self.attributes),
        ]
        return fingerprint(tuple(fields))


@dataclass(frozen=True, slots=True)
class ConfigProvenance:
    """Exact release/config/policy provenance with a safe metadata fingerprint."""

    provenance_id: EnvironmentScopedId
    scope: ProvenanceScope
    release_id: StableId
    snapshot: ConfigSnapshot
    policy_version: PolicyVersion
    version: int = 1

    def __post_init__(self) -> None:
        if self.provenance_id.kind.value != "CONFIG":
            raise ProvenanceBoundaryError("provenance requires a config identity")
        if self.provenance_id.environment is not self.scope.environment:
            raise IntegrityError("provenance identity and scope mismatch")
        if self.snapshot.environment is not self.scope.environment:
            raise IntegrityError("provenance snapshot scope mismatch")
        if not isinstance(self.release_id, StableId) or (
            self.release_id.kind is not IdentityKind.RELEASE
        ):
            raise ProvenanceBoundaryError("release provenance must be a typed release reference")
        if not isinstance(self.policy_version, PolicyVersion):
            raise ProvenanceBoundaryError("policy provenance must be a typed policy version")
        if not isinstance(self.version, int) or isinstance(self.version, bool) or self.version < 1:
            raise ProvenanceBoundaryError("invalid provenance version")

    @property
    def config_fingerprint(self) -> str:
        return self.snapshot.fingerprint

    @property
    def fingerprint(self) -> str:
        return fingerprint(
            (
                ("config_fingerprint", self.snapshot.fingerprint),
                ("policy_version", self.policy_version.value),
                ("provenance_id", self.provenance_id.as_text()),
                ("release_id", self.release_id),
                ("version", self.version),
                *_scope_fields(self.scope),
            )
        )

    def assert_matches(
        self,
        *,
        release_id: StableId,
        config_fingerprint: str,
        policy_version: PolicyVersion,
    ) -> None:
        if self.release_id != release_id:
            raise IntegrityError("release provenance mismatch")
        if self.config_fingerprint != _validate_hash(config_fingerprint, "config fingerprint"):
            raise IntegrityError("configuration fingerprint mismatch")
        if self.policy_version != policy_version:
            raise IntegrityError("policy version mismatch")


def scope_from_security_context(context: object) -> ProvenanceScope:
    """Project only exact namespace fields from a trusted S0B context."""

    if not isinstance(context, SecurityContext):
        raise ProvenanceBoundaryError("trusted security context is required")
    return ProvenanceScope(
        environment=context.environment,
        tenant_id=context.tenant_id,
        account_id=context.account_id,
    )
