"""Backend-only S0B authority, scope and opaque-reference primitives."""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from types import MappingProxyType
from typing import Protocol, Self

from hct_backend.contracts import Environment
from hct_backend.generated_contracts import ID_VALUE_PATTERN

CURRENT_CONTEXT_VERSION = 1
_TRUSTED_CONSTRUCTION_TOKEN = object()
_ID_PATTERN = re.compile(ID_VALUE_PATTERN)
_EVIDENCE_PATTERN = re.compile(r"^[a-z][a-z0-9._:-]{0,63}$")
_REFERENCE_PREFIXES = ("cred-ref-", "secret-ref-")


class SecurityBoundaryError(ValueError):
    """Base error for deterministic fail-closed S0B validation."""


class ContextConstructionError(SecurityBoundaryError):
    """Raised when authority is not created through the trusted boundary."""


class AuthorizationDenied(SecurityBoundaryError):
    """Raised for any missing, stale or mismatched authorization evidence."""


class AssuranceLevel(StrEnum):
    STANDARD = "STANDARD"
    HIGH = "HIGH"


class ReferenceKind(StrEnum):
    CREDENTIAL = "credential"
    SECRET = "secret"


class SecretPurpose(StrEnum):
    ACCOUNT_ACCESS = "account-access"
    AUDIT_REFERENCE = "audit-reference"


class SecretClassification(StrEnum):
    SECRET_REFERENCE = "secret-reference"


def _validate_identity(value: str, label: str) -> str:
    if not isinstance(value, str) or not _ID_PATTERN.fullmatch(value):
        raise SecurityBoundaryError(f"invalid {label}")
    return value


def _validate_evidence(value: str, label: str) -> str:
    if not isinstance(value, str) or not _EVIDENCE_PATTERN.fullmatch(value) or value == "*":
        raise SecurityBoundaryError(f"invalid {label} evidence")
    return value


class _TypedIdentity:
    """Small immutable identity value with a distinct Python type per scope."""

    __slots__ = ("_value",)
    _value: str

    def __init__(self, value: str) -> None:
        object.__setattr__(self, "_value", _validate_identity(value, type(self).__name__))

    @property
    def value(self) -> str:
        return self._value

    def __setattr__(self, name: str, value: object) -> None:
        if hasattr(self, "_value"):
            raise TypeError(f"{type(self).__name__} is immutable")
        object.__setattr__(self, name, value)

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, _TypedIdentity)
            and type(self) is type(other)
            and self._value == other._value
        )

    def __hash__(self) -> int:
        return hash((type(self), self._value))

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self._value!r})"


class PrincipalID(_TypedIdentity):
    __slots__ = ()


class TenantID(_TypedIdentity):
    __slots__ = ()


class MembershipID(_TypedIdentity):
    __slots__ = ()


class ExchangeAccountID(_TypedIdentity):
    __slots__ = ()


class SessionID(_TypedIdentity):
    __slots__ = ()


class CorrelationID(_TypedIdentity):
    __slots__ = ()


class TraceID(_TypedIdentity):
    __slots__ = ()


class PolicyVersion(_TypedIdentity):
    __slots__ = ()

    def __init__(self, value: str) -> None:
        super().__init__(value)
        if not value.startswith("policy-"):
            raise SecurityBoundaryError("invalid policy version")


class PolicyNamespaceID(_TypedIdentity):
    __slots__ = ()


class BindingID(_TypedIdentity):
    __slots__ = ()


class ResourceID(_TypedIdentity):
    __slots__ = ()


class _OpaqueReference(_TypedIdentity):
    __slots__ = ()

    def __init__(self, value: str) -> None:
        super().__init__(value)
        if not value.startswith(_REFERENCE_PREFIXES):
            raise SecurityBoundaryError("invalid opaque reference")

    def __repr__(self) -> str:
        return f"{type(self).__name__}(<opaque>)"

    def __str__(self) -> str:
        return f"<{type(self).__name__}:opaque>"

    def safe_metadata(self) -> dict[str, str]:
        return {"reference_type": type(self).__name__, "reference_state": "opaque"}


class CredentialRef(_OpaqueReference):
    __slots__ = ()

    def __init__(self, value: str) -> None:
        super().__init__(value)
        if not value.startswith("cred-ref-"):
            raise SecurityBoundaryError("invalid credential reference")


class SecretRef(_OpaqueReference):
    __slots__ = ()

    def __init__(self, value: str) -> None:
        super().__init__(value)
        if not value.startswith("secret-ref-"):
            raise SecurityBoundaryError("invalid secret reference")


def _normalize_evidence(values: Iterable[str], label: str) -> frozenset[str]:
    normalized = frozenset(_validate_evidence(value, label) for value in values)
    if not normalized:
        raise SecurityBoundaryError(f"missing {label} evidence")
    return normalized


def _normalize_optional_evidence(values: Iterable[str], label: str) -> frozenset[str]:
    values_tuple = tuple(values)
    if not values_tuple:
        return frozenset()
    return _normalize_evidence(values_tuple, label)


def _require_utc(value: datetime, label: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise SecurityBoundaryError(f"{label} must be timezone-aware")
    return value.astimezone(UTC)


@dataclass(frozen=True, slots=True, init=False)
class TrustedAuthorityEvidence:
    """Validated server evidence consumed by the SecurityContext factory."""

    principal_id: PrincipalID
    tenant_id: TenantID
    membership_id: MembershipID
    account_id: ExchangeAccountID | None
    roles: frozenset[str]
    scopes: frozenset[str]
    policy_version: PolicyVersion
    assurance: AssuranceLevel
    session_id: SessionID
    security_version: int
    correlation_id: CorrelationID
    trace_id: TraceID
    environment: Environment
    context_version: int
    issued_at: datetime
    effective_at: datetime
    expires_at: datetime

    def __init__(
        self,
        *,
        principal_id: PrincipalID | None = None,
        tenant_id: TenantID | None = None,
        membership_id: MembershipID | None = None,
        account_id: ExchangeAccountID | None = None,
        roles: Iterable[str] = (),
        scopes: Iterable[str] = (),
        policy_version: PolicyVersion | None = None,
        assurance: AssuranceLevel | None = None,
        session_id: SessionID | None = None,
        security_version: int = 0,
        correlation_id: CorrelationID | None = None,
        trace_id: TraceID | None = None,
        environment: Environment | None = None,
        context_version: int = 0,
        issued_at: datetime | None = None,
        effective_at: datetime | None = None,
        expires_at: datetime | None = None,
        _construction_token: object | None = None,
    ) -> None:
        if _construction_token is not _TRUSTED_CONSTRUCTION_TOKEN:
            raise ContextConstructionError("trusted server evidence is required")
        required = (
            principal_id,
            tenant_id,
            membership_id,
            policy_version,
            assurance,
            session_id,
            correlation_id,
            trace_id,
            environment,
            issued_at,
            effective_at,
            expires_at,
        )
        if any(value is None for value in required):
            raise ContextConstructionError("trusted evidence is incomplete")
        if not all(
            isinstance(value, expected)
            for value, expected in (
                (principal_id, PrincipalID),
                (tenant_id, TenantID),
                (membership_id, MembershipID),
                (policy_version, PolicyVersion),
                (assurance, AssuranceLevel),
                (session_id, SessionID),
                (correlation_id, CorrelationID),
                (trace_id, TraceID),
                (environment, Environment),
            )
        ) or (account_id is not None and not isinstance(account_id, ExchangeAccountID)):
            raise ContextConstructionError("trusted evidence types are invalid")
        assert issued_at is not None
        assert effective_at is not None
        assert expires_at is not None
        if context_version != CURRENT_CONTEXT_VERSION:
            raise ContextConstructionError("unsupported context version")
        if security_version < 1:
            raise ContextConstructionError("invalid security version")
        issued = _require_utc(issued_at, "issued_at")
        effective = _require_utc(effective_at, "effective_at")
        expires = _require_utc(expires_at, "expires_at")
        if not issued <= effective < expires:
            raise ContextConstructionError("invalid context time bounds")
        object.__setattr__(self, "principal_id", principal_id)
        object.__setattr__(self, "tenant_id", tenant_id)
        object.__setattr__(self, "membership_id", membership_id)
        object.__setattr__(self, "account_id", account_id)
        object.__setattr__(self, "roles", _normalize_evidence(roles, "role"))
        object.__setattr__(self, "scopes", _normalize_evidence(scopes, "scope"))
        object.__setattr__(self, "policy_version", policy_version)
        object.__setattr__(self, "assurance", assurance)
        object.__setattr__(self, "session_id", session_id)
        object.__setattr__(self, "security_version", security_version)
        object.__setattr__(self, "correlation_id", correlation_id)
        object.__setattr__(self, "trace_id", trace_id)
        object.__setattr__(self, "environment", environment)
        object.__setattr__(self, "context_version", context_version)
        object.__setattr__(self, "issued_at", issued)
        object.__setattr__(self, "effective_at", effective)
        object.__setattr__(self, "expires_at", expires)


def build_trusted_authority_evidence(
    *,
    principal_id: PrincipalID,
    tenant_id: TenantID,
    membership_id: MembershipID,
    account_id: ExchangeAccountID | None,
    roles: Iterable[str],
    scopes: Iterable[str],
    policy_version: PolicyVersion,
    assurance: AssuranceLevel,
    session_id: SessionID,
    security_version: int,
    correlation_id: CorrelationID,
    trace_id: TraceID,
    environment: Environment,
    issued_at: datetime,
    effective_at: datetime,
    expires_at: datetime,
    context_version: int = CURRENT_CONTEXT_VERSION,
) -> TrustedAuthorityEvidence:
    """Trusted server-side boundary for already-authenticated evidence."""

    return TrustedAuthorityEvidence(
        principal_id=principal_id,
        tenant_id=tenant_id,
        membership_id=membership_id,
        account_id=account_id,
        roles=roles,
        scopes=scopes,
        policy_version=policy_version,
        assurance=assurance,
        session_id=session_id,
        security_version=security_version,
        correlation_id=correlation_id,
        trace_id=trace_id,
        environment=environment,
        context_version=context_version,
        issued_at=issued_at,
        effective_at=effective_at,
        expires_at=expires_at,
        _construction_token=_TRUSTED_CONSTRUCTION_TOKEN,
    )


@dataclass(frozen=True, slots=True, init=False)
class SecurityContext:
    """Immutable backend authority context; never a client-authoritative DTO."""

    principal_id: PrincipalID
    tenant_id: TenantID
    membership_id: MembershipID
    account_id: ExchangeAccountID | None
    roles: frozenset[str]
    scopes: frozenset[str]
    policy_version: PolicyVersion
    assurance: AssuranceLevel
    session_id: SessionID
    security_version: int
    correlation_id: CorrelationID
    trace_id: TraceID
    environment: Environment
    context_version: int
    issued_at: datetime
    effective_at: datetime
    expires_at: datetime

    def __init__(
        self,
        *,
        _evidence: TrustedAuthorityEvidence | None = None,
        _now: datetime | None = None,
        _construction_token: object | None = None,
    ) -> None:
        if (
            _construction_token is not _TRUSTED_CONSTRUCTION_TOKEN
            or _evidence is None
            or _now is None
        ):
            raise ContextConstructionError("SecurityContext requires trusted server evidence")
        if _evidence.context_version != CURRENT_CONTEXT_VERSION:
            raise ContextConstructionError("unsupported context version")
        now = _require_utc(_now, "now")
        if now < _evidence.effective_at or now >= _evidence.expires_at:
            raise ContextConstructionError("context is not active")
        for field in (
            "principal_id",
            "tenant_id",
            "membership_id",
            "account_id",
            "roles",
            "scopes",
            "policy_version",
            "assurance",
            "session_id",
            "security_version",
            "correlation_id",
            "trace_id",
            "environment",
            "context_version",
            "issued_at",
            "effective_at",
            "expires_at",
        ):
            object.__setattr__(self, field, getattr(_evidence, field))

    @classmethod
    def from_trusted_evidence(
        cls, evidence: TrustedAuthorityEvidence, *, now: datetime
    ) -> Self:
        if not isinstance(evidence, TrustedAuthorityEvidence):
            raise ContextConstructionError("trusted server evidence is required")
        return cls(
            _evidence=evidence,
            _now=now,
            _construction_token=_TRUSTED_CONSTRUCTION_TOKEN,
        )

    def assert_active(self, *, now: datetime) -> None:
        current = _require_utc(now, "now")
        if self.context_version != CURRENT_CONTEXT_VERSION:
            raise AuthorizationDenied("unsupported context version")
        if current < self.effective_at or current >= self.expires_at:
            raise AuthorizationDenied("context is stale or expired")

    def safe_metadata(self) -> dict[str, str | int]:
        return {
            "principal_id": self.principal_id.value,
            "tenant_id": self.tenant_id.value,
            "membership_id": self.membership_id.value,
            "account_id": self.account_id.value if self.account_id is not None else "none",
            "environment": self.environment.value,
            "context_version": self.context_version,
            "security_version": self.security_version,
        }


@dataclass(frozen=True, slots=True)
class TenantExchangeAccountBinding:
    binding_id: BindingID
    tenant_id: TenantID
    account_id: ExchangeAccountID
    environment: Environment
    credential_ref: CredentialRef
    policy_namespace: PolicyNamespaceID
    version: int = 1

    def __post_init__(self) -> None:
        if not all(
            isinstance(value, expected)
            for value, expected in (
                (self.binding_id, BindingID),
                (self.tenant_id, TenantID),
                (self.account_id, ExchangeAccountID),
                (self.environment, Environment),
                (self.credential_ref, CredentialRef),
                (self.policy_namespace, PolicyNamespaceID),
            )
        ):
            raise SecurityBoundaryError("invalid tenant-account binding types")
        if self.version < 1:
            raise SecurityBoundaryError("invalid binding version")

    def safe_metadata(self) -> dict[str, str | int]:
        return {
            "binding_id": self.binding_id.value,
            "tenant_id": self.tenant_id.value,
            "account_id": self.account_id.value,
            "environment": self.environment.value,
            "policy_namespace": self.policy_namespace.value,
            "version": self.version,
            **self.credential_ref.safe_metadata(),
        }


@dataclass(frozen=True, slots=True)
class ScopedResource:
    resource_id: ResourceID
    tenant_id: TenantID
    membership_id: MembershipID
    account_id: ExchangeAccountID | None
    environment: Environment

    def __post_init__(self) -> None:
        if not all(
            isinstance(value, expected)
            for value, expected in (
                (self.resource_id, ResourceID),
                (self.tenant_id, TenantID),
                (self.membership_id, MembershipID),
                (self.environment, Environment),
            )
        ) or (self.account_id is not None and not isinstance(self.account_id, ExchangeAccountID)):
            raise SecurityBoundaryError("invalid scoped resource types")


def _require_exact(actual: object, expected: object, label: str) -> None:
    if actual != expected:
        raise AuthorizationDenied(f"{label} mismatch")


def authorize_scope(
    context: SecurityContext,
    resource: ScopedResource,
    *,
    required_roles: Iterable[str] = (),
    required_scopes: Iterable[str] = (),
    required_policy: PolicyVersion | None = None,
    binding: TenantExchangeAccountBinding | None = None,
    now: datetime,
) -> None:
    """Authorize one exact object scope without external resolution."""

    if not isinstance(context, SecurityContext) or not isinstance(resource, ScopedResource):
        raise AuthorizationDenied("invalid authorization inputs")
    context.assert_active(now=now)
    _require_exact(context.tenant_id, resource.tenant_id, "tenant")
    _require_exact(context.membership_id, resource.membership_id, "membership")
    _require_exact(context.environment, resource.environment, "environment")
    if resource.account_id is not None:
        _require_exact(context.account_id, resource.account_id, "account")
    for role in _normalize_optional_evidence(required_roles, "required role"):
        if role not in context.roles:
            raise AuthorizationDenied("required role evidence missing")
    for scope in _normalize_optional_evidence(required_scopes, "required scope"):
        if scope not in context.scopes:
            raise AuthorizationDenied("required scope evidence missing")
    if required_policy is not None:
        _require_exact(context.policy_version, required_policy, "policy")
    if binding is not None:
        _require_exact(context.tenant_id, binding.tenant_id, "binding tenant")
        _require_exact(context.account_id, binding.account_id, "binding account")
        _require_exact(context.environment, binding.environment, "binding environment")


@dataclass(frozen=True, slots=True)
class SecretReferenceMetadata:
    reference_kind: ReferenceKind
    purpose: SecretPurpose
    classification: SecretClassification
    environment: Environment

    def __post_init__(self) -> None:
        if not all(
            isinstance(value, expected)
            for value, expected in (
                (self.reference_kind, ReferenceKind),
                (self.purpose, SecretPurpose),
                (self.classification, SecretClassification),
                (self.environment, Environment),
            )
        ):
            raise SecurityBoundaryError("invalid reference metadata types")

    def safe_metadata(self) -> dict[str, str]:
        return {
            "reference_kind": self.reference_kind.value,
            "purpose": self.purpose.value,
            "classification": self.classification.value,
            "environment": self.environment.value,
        }


class SecretStore(Protocol):
    """Provider-neutral reference metadata port with no raw-value operation."""

    def supports(self, reference: CredentialRef | SecretRef) -> bool:
        ...

    def describe(self, reference: CredentialRef | SecretRef) -> SecretReferenceMetadata | None:
        ...


class NullSecretStore:
    """Deterministic test boundary that stores and resolves nothing."""

    def supports(self, reference: CredentialRef | SecretRef) -> bool:
        if not isinstance(reference, (CredentialRef, SecretRef)):
            raise SecurityBoundaryError("invalid opaque reference")
        return False

    def describe(self, reference: CredentialRef | SecretRef) -> None:
        if not isinstance(reference, (CredentialRef, SecretRef)):
            raise SecurityBoundaryError("invalid opaque reference")
        return None


class ReferenceOnlySecretStore:
    """Test double containing reference metadata only and no secret values."""

    __slots__ = ("_metadata",)

    def __init__(
        self,
        metadata: Mapping[CredentialRef | SecretRef, SecretReferenceMetadata],
    ) -> None:
        if any(
            not isinstance(key, (CredentialRef, SecretRef))
            or not isinstance(value, SecretReferenceMetadata)
            for key, value in metadata.items()
        ):
            raise SecurityBoundaryError("invalid opaque reference")
        self._metadata = MappingProxyType(dict(metadata))

    def supports(self, reference: CredentialRef | SecretRef) -> bool:
        if not isinstance(reference, (CredentialRef, SecretRef)):
            raise SecurityBoundaryError("invalid opaque reference")
        return reference in self._metadata

    def describe(self, reference: CredentialRef | SecretRef) -> SecretReferenceMetadata | None:
        if not isinstance(reference, (CredentialRef, SecretRef)):
            raise SecurityBoundaryError("invalid opaque reference")
        return self._metadata.get(reference)
