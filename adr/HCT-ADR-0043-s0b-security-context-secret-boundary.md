# HCT-ADR-0043 - S0B Security Context and Opaque Secret Boundary

Status: `IMPLEMENTED_FOR_REVIEW`
Date: `2026-09-12`
Work Order: `HCT-IMP-0002-S0B`
Authorization: `HCT-CP-0017 / IMPLEMENTATION_AUTHORIZED_S0B`

## Decision

S0B adds backend-domain authority primitives only. `SecurityContext` is an
immutable, versioned value that is constructed from an explicit trusted
server-evidence boundary. It is not a browser payload, public API schema or
authentication/session transport. A protected operation must receive a
context whose tenant, membership, account and environment scope exactly
matches the operation and whose policy evidence is sufficient for that
operation.

The public OpenAPI contract remains unchanged because no S0B authority type
crosses a runtime/API boundary in this slice. The backend reuses the S0A
`Environment` namespace and typed identity validation rather than creating a
second public contract system.

## Authority and construction boundary

`TrustedAuthorityEvidence` is the only input accepted by the
`SecurityContext.from_trusted_evidence` factory. It contains already-validated
typed identities and server-derived role/scope/policy/assurance evidence. A
raw mapping, client tenant ID, client account ID or frontend state has no
factory path and cannot establish authority. Direct construction of
`SecurityContext` is rejected unless the module-private construction capability
is supplied by the trusted factory.

The context contains:

- principal, tenant, membership and optional exchange-account identities;
- role/scope evidence and a policy-version reference;
- assurance state, session/security version and correlation/trace identity;
- exact environment namespace;
- context version and deterministic issued/effective/expiry timestamps.

The context and all binding/reference values are frozen after construction.
Expiry is evaluated against an injected deterministic `now` value. Unknown
environment values, unsupported context versions, malformed identities and
expired contexts fail closed.

## Binding and guard model

`TenantExchangeAccountBinding` is an immutable identity/reference primitive
containing tenant, exchange-account, environment, an opaque credential
reference, a policy namespace and a binding version. It contains no credential
material, endpoint, client or signing object. Construction rejects a binding
whose identity/environment evidence is inconsistent.

The pure `authorize_scope` guard requires exact context and resource scope,
required role/scope/policy evidence and a matching binding. Identifier
possession alone is insufficient. Tenant, membership, account, environment,
object and binding mismatches all raise the same fail-closed authorization
error without attempting external resolution.

No wildcard or implicit superuser authority is defined. A caller must name
the exact required evidence for the operation.

## Opaque reference and SecretStore boundary

`CredentialRef` and `SecretRef` are validated opaque identifiers. Their safe
representation exposes only reference metadata and never includes their
identifier value in `repr`, `str` or safe serialization. They do not represent
or contain credential material.

The provider-neutral `SecretStore` protocol exposes only reference support and
non-secret metadata description. The deterministic `NullSecretStore` test
double stores no values, performs no network/provider operation and has no
method that returns a secret, token, key, decrypted payload or generic secret
lookup result. Provider integration, lifecycle, encryption, KMS/HSM and
exchange authentication remain future separately authorized work.

Raw secrets are `NEVER_LOG`, `NEVER_TRACE`, `NEVER_PROMPT` and `NEVER_EXPORT`.
The S0B code has no raw-secret field, fixture or serialization path.

## Contract, tests and time

S0B authority types remain backend-internal. Only the existing S0A public
health/readiness/version and safe identity contracts remain cross-runtime.
Tests use fixed UTC timestamps and direct table-driven mismatch cases for
tenant, membership, account, environment, role/scope/policy, object ownership,
binding, malformed IDs, unsupported version and expiry. Safe reference tests
assert that representations contain no reference value and that the null
store cannot resolve or contact an external provider.

## Platform, rollback and operational boundary

Windows development uses system Python 3.12 and the existing uv/pytest/Ruff/
mypy toolchain. Linux CI uses the existing locked installs. No new dependency,
database, network, exchange, browser-auth or deployment path is introduced.
The slice has no persistence or external side effects, so rollback is a normal
commit revert before merge.

This ADR does not authorize authentication, credential provisioning, exchange
connectivity, trading, production deployment, limited-live or real-money
operation. Those remain separate governed gates.
