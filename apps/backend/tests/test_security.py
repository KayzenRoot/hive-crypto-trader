from dataclasses import FrozenInstanceError, replace
from datetime import UTC, datetime, timedelta

import pytest

from hct_backend.contracts import Environment
from hct_backend.security import (
    CURRENT_CONTEXT_VERSION,
    AssuranceLevel,
    AuthorizationDenied,
    BindingID,
    ContextConstructionError,
    CorrelationID,
    CredentialRef,
    ExchangeAccountID,
    MembershipID,
    NullSecretStore,
    PolicyNamespaceID,
    PolicyVersion,
    PrincipalID,
    ReferenceOnlySecretStore,
    ResourceID,
    ScopedResource,
    SecretRef,
    SecretReferenceMetadata,
    SecurityBoundaryError,
    SecurityContext,
    SessionID,
    TenantExchangeAccountBinding,
    TenantID,
    TraceID,
    TrustedAuthorityEvidence,
    authorize_scope,
    build_trusted_authority_evidence,
)

NOW = datetime(2026, 9, 12, 12, 0, tzinfo=UTC)


def make_context(
    *,
    tenant: str = "tenant-a",
    account: str | None = "account-a",
    environment: Environment = Environment.PAPER,
    expires_at: datetime = NOW + timedelta(hours=1),
    context_version: int = CURRENT_CONTEXT_VERSION,
) -> SecurityContext:
    evidence = build_trusted_authority_evidence(
        principal_id=PrincipalID("principal-a"),
        tenant_id=TenantID(tenant),
        membership_id=MembershipID("membership-a"),
        account_id=ExchangeAccountID(account) if account is not None else None,
        roles=("operator",),
        scopes=("security.read", "resource.read"),
        policy_version=PolicyVersion("policy-v1"),
        assurance=AssuranceLevel.HIGH,
        session_id=SessionID("session-a"),
        security_version=1,
        correlation_id=CorrelationID("correlation-a"),
        trace_id=TraceID("trace-a"),
        environment=environment,
        issued_at=NOW - timedelta(minutes=1),
        effective_at=NOW,
        expires_at=expires_at,
        context_version=context_version,
    )
    return SecurityContext.from_trusted_evidence(evidence, now=NOW)


def make_resource(
    *,
    tenant: str = "tenant-a",
    account: str | None = "account-a",
    environment: Environment = Environment.PAPER,
) -> ScopedResource:
    return ScopedResource(
        resource_id=ResourceID("resource-a"),
        tenant_id=TenantID(tenant),
        membership_id=MembershipID("membership-a"),
        account_id=ExchangeAccountID(account) if account is not None else None,
        environment=environment,
    )


def make_binding(
    *,
    tenant: str = "tenant-a",
    account: str = "account-a",
    environment: Environment = Environment.PAPER,
) -> TenantExchangeAccountBinding:
    return TenantExchangeAccountBinding(
        binding_id=BindingID("binding-a"),
        tenant_id=TenantID(tenant),
        account_id=ExchangeAccountID(account),
        environment=environment,
        credential_ref=CredentialRef("cred-ref-account-a"),
        policy_namespace=PolicyNamespaceID("policy-namespace-a"),
    )


def test_trusted_server_evidence_constructs_active_context() -> None:
    context = make_context()
    assert context.tenant_id == TenantID("tenant-a")
    assert context.account_id == ExchangeAccountID("account-a")
    assert context.environment is Environment.PAPER
    assert context.context_version == CURRENT_CONTEXT_VERSION
    assert context.safe_metadata()["tenant_id"] == "tenant-a"


def test_client_fields_cannot_construct_authority() -> None:
    with pytest.raises(ContextConstructionError, match="trusted server evidence"):
        SecurityContext()
    with pytest.raises(ContextConstructionError, match="trusted server evidence"):
        SecurityContext.from_trusted_evidence({"tenant_id": "tenant-a"}, now=NOW)  # type: ignore[arg-type]
    with pytest.raises(ContextConstructionError, match="trusted server evidence"):
        TrustedAuthorityEvidence(tenant_id=TenantID("tenant-a"))


def test_context_and_binding_are_immutable() -> None:
    context = make_context()
    binding = make_binding()
    with pytest.raises(FrozenInstanceError):
        context.tenant_id = TenantID("tenant-b")  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        binding.environment = Environment.REPLAY  # type: ignore[misc]
    with pytest.raises(TypeError):
        context.tenant_id.value = "tenant-b"  # type: ignore[misc]


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("tenant", "tenant-b"),
        ("account", "account-b"),
        ("environment", Environment.REPLAY),
    ],
)
def test_scope_mismatch_matrix_fails_closed(field: str, value: object) -> None:
    context = make_context()
    kwargs: dict[str, object] = {
        "tenant": "tenant-a",
        "account": "account-a",
        "environment": Environment.PAPER,
    }
    kwargs[field] = value
    resource = make_resource(**kwargs)  # type: ignore[arg-type]
    with pytest.raises(AuthorizationDenied, match="mismatch"):
        authorize_scope(context, resource, now=NOW)


def test_membership_and_object_scope_mismatch_fail_closed() -> None:
    context = make_context()
    resource = replace(make_resource(), membership_id=MembershipID("membership-b"))
    with pytest.raises(AuthorizationDenied, match="membership mismatch"):
        authorize_scope(context, resource, now=NOW)

    other_tenant = replace(
        make_resource(),
        resource_id=ResourceID("resource-b"),
        tenant_id=TenantID("tenant-b"),
    )
    with pytest.raises(AuthorizationDenied, match="tenant mismatch"):
        authorize_scope(context, other_tenant, now=NOW)


def test_required_role_scope_policy_and_binding_are_exact() -> None:
    context = make_context()
    resource = make_resource()
    authorize_scope(
        context,
        resource,
        required_roles=("operator",),
        required_scopes=("resource.read",),
        required_policy=PolicyVersion("policy-v1"),
        binding=make_binding(),
        now=NOW,
    )
    with pytest.raises(AuthorizationDenied, match="role evidence"):
        authorize_scope(context, resource, required_roles=("admin",), now=NOW)
    with pytest.raises(AuthorizationDenied, match="scope evidence"):
        authorize_scope(context, resource, required_scopes=("resource.write",), now=NOW)
    with pytest.raises(AuthorizationDenied, match="policy mismatch"):
        authorize_scope(context, resource, required_policy=PolicyVersion("policy-v2"), now=NOW)
    with pytest.raises(AuthorizationDenied, match="binding account"):
        authorize_scope(context, resource, binding=make_binding(account="account-b"), now=NOW)


def test_missing_or_wildcard_evidence_fails_closed() -> None:
    with pytest.raises(SecurityBoundaryError, match="missing role"):
        build_trusted_authority_evidence(
            principal_id=PrincipalID("principal-a"),
            tenant_id=TenantID("tenant-a"),
            membership_id=MembershipID("membership-a"),
            account_id=ExchangeAccountID("account-a"),
            roles=(),
            scopes=("resource.read",),
            policy_version=PolicyVersion("policy-v1"),
            assurance=AssuranceLevel.HIGH,
            session_id=SessionID("session-a"),
            security_version=1,
            correlation_id=CorrelationID("correlation-a"),
            trace_id=TraceID("trace-a"),
            environment=Environment.PAPER,
            issued_at=NOW - timedelta(minutes=1),
            effective_at=NOW,
            expires_at=NOW + timedelta(hours=1),
        )
    with pytest.raises(SecurityBoundaryError, match="invalid scope"):
        build_trusted_authority_evidence(
            principal_id=PrincipalID("principal-a"),
            tenant_id=TenantID("tenant-a"),
            membership_id=MembershipID("membership-a"),
            account_id=ExchangeAccountID("account-a"),
            roles=("operator",),
            scopes=("*",),
            policy_version=PolicyVersion("policy-v1"),
            assurance=AssuranceLevel.HIGH,
            session_id=SessionID("session-a"),
            security_version=1,
            correlation_id=CorrelationID("correlation-a"),
            trace_id=TraceID("trace-a"),
            environment=Environment.PAPER,
            issued_at=NOW - timedelta(minutes=1),
            effective_at=NOW,
            expires_at=NOW + timedelta(hours=1),
        )


def test_unsupported_stale_and_expired_contexts_fail_closed() -> None:
    with pytest.raises(ContextConstructionError, match="unsupported"):
        make_context(context_version=2)
    context = make_context(expires_at=NOW + timedelta(minutes=1))
    with pytest.raises(AuthorizationDenied, match="stale or expired"):
        context.assert_active(now=NOW + timedelta(minutes=1))


def test_malformed_typed_ids_and_environment_are_rejected() -> None:
    with pytest.raises(SecurityBoundaryError):
        TenantID("Tenant A")
    with pytest.raises(SecurityBoundaryError):
        CredentialRef("raw-secret-material")
    with pytest.raises(SecurityBoundaryError):
        PolicyVersion("v1")


def test_opaque_references_have_safe_representation_and_metadata_only_store() -> None:
    credential = CredentialRef("cred-ref-account-a")
    secret = SecretRef("secret-ref-audit-a")
    assert "account-a" not in repr(credential)
    assert "account-a" not in str(credential)
    assert credential.safe_metadata() == {
        "reference_type": "CredentialRef",
        "reference_state": "opaque",
    }
    metadata = SecretReferenceMetadata(
        reference_kind="credential",
        purpose="account-access",
        classification="secret",
        environment=Environment.PAPER,
    )
    store = ReferenceOnlySecretStore({credential: metadata})
    assert store.supports(credential)
    assert store.describe(credential) == metadata
    assert not store.supports(secret)
    assert NullSecretStore().describe(secret) is None
    assert not NullSecretStore().supports(credential)
