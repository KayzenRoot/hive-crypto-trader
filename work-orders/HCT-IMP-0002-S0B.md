# HCT-IMP-0002-S0B - SecurityContext, Tenant/Account Binding & Opaque SecretStore Foundation

Status: `PENDING_AUTHORIZATION`
Risk class: `HIGH_ASSURANCE`
Parent authorization increment: `HCT-IMPL-AUTH-0002`
Required checkpoint before execution: future explicit promotion from `HCT-CP-0016`
Required authorization ceiling: `NON_TRADING_STAGE_0_SECURITY_FOUNDATION_ONLY`

## OBJECTIVE
Implement the second bounded Stage-0 foundation slice after explicit authorization: canonical SecurityContext, exact tenant/account binding, fail-closed scope guards and an opaque provider-neutral SecretStore boundary, with no real secret material, exchange connectivity, persistence, deployment or trading capability.

## CONTEXT
S0A established the repository/runtime/contract foundation. R11 Stage 0 and R08 security requirements require server-derived authority, exact tenant/account binding and a SecretStore boundary before later exchange, realtime, risk, execution or live-capable work.

This Work Order is executable only after a new checkpoint explicitly sets:
- `implementation_authorized=true`
- `implementation_authorization_scope=["HCT-IMP-0002-S0B"]`
- `implementation_authorization_ceiling="NON_TRADING_STAGE_0_SECURITY_FOUNDATION_ONLY"`.

Until then, this document is specification only.

## SCOPE
### S0B-1 - Typed security identity primitives
Extend the canonical contract foundation with typed identities required by this slice, including as applicable:
- `PrincipalID`
- `TenantID`
- `MembershipID`
- `ExchangeAccountID`
- `SessionID`
- `CorrelationID` / `TraceID`
- `PolicyVersion` / role-scope reference
- `CredentialRef` / `SecretRef` as opaque identifiers only.

All stateful identity remains environment-aware where required by frozen architecture.

### S0B-2 - Immutable SecurityContext
Implement an immutable/frozen versioned SecurityContext containing the minimum server-authority evidence needed by protected backend operations:
- principal;
- tenant;
- membership;
- account scope where applicable;
- roles/scopes/policy version;
- assurance state;
- session identity/security version;
- correlation/trace identity;
- environment namespace;
- issued/effective/expiry/version metadata where required by the chosen bounded design.

The context SHALL be created through a trusted/server-side construction boundary. Raw client tenant/account fields SHALL NOT construct authority directly.

### S0B-3 - Tenant/account binding
Implement a canonical immutable `TenantExchangeAccountBinding`-equivalent primitive containing only non-secret identity/reference metadata required by later domains:
- tenant identity;
- exchange account identity;
- environment;
- opaque `CredentialRef`;
- policy/risk namespace identity where required;
- binding version/identity.

Binding validation SHALL fail closed on tenant/account/environment mismatch.

### S0B-4 - Authorization guard primitives
Implement deterministic backend/internal guards sufficient to prove:
- object scope belongs to the SecurityContext tenant/account/environment;
- required role/scope/policy evidence is present;
- identifier knowledge alone grants no access;
- malformed/missing/stale/incompatible context fails closed;
- cross-tenant/cross-account/cross-environment attempts fail closed.

Do not implement a complete future IAM product or commercial entitlement engine.

### S0B-5 - Opaque SecretStore boundary
Implement only a provider-neutral interface/port and safe metadata types for future secret providers.

Allowed:
- opaque `SecretRef`/`CredentialRef`;
- secret purpose/classification metadata;
- capability/request metadata without secret value;
- safe redacted/reference representation;
- deterministic fake/null implementation for tests that stores only references/metadata and cannot expose real secret material.

The S0B SecretStore API SHALL NOT return raw secret strings/bytes or connect to external providers.

### S0B-6 - Security-safe audit/evidence hooks
Where audit/evidence is needed by this slice, record only safe identity/reference metadata. Raw secrets are `NEVER_LOG`, `NEVER_TRACE`, `NEVER_PROMPT`, `NEVER_EXPORT`.

## OUT OF SCOPE
Do not implement:
- API keys, secret keys, private keys, access/refresh tokens, seed phrases or any real/test-looking secret value;
- secret import/verification/activation/rotation/revocation/deletion lifecycle;
- encryption/decryption, envelope encryption, KMS/HSM;
- AWS/GCP/Azure/Vault secret provider adapters;
- OAuth/OIDC, login endpoints, MFA, passkeys/WebAuthn, recovery, browser session/token transport;
- database persistence/RLS;
- cache/queue/worker tenant isolation beyond pure contracts needed by this slice;
- MEXC or any exchange SDK/client/adapter/REST/WebSocket connection;
- private streams or exchange auth/signing;
- market data;
- Safety/Session/Risk/sizing/leverage/reservations;
- OMS/orders/fills/positions/balances;
- reconciliation/protection;
- strategy/signal/intelligence/RAG/agent/Brain/Copilot behavior;
- production deployment;
- limited-live or real-money trading;
- later Stage-0 or Stage-1+ functionality.

## FILES / SOURCES TO READ
Before mutation, at minimum:
- `checkpoints/workstreams/planning/latest.json`
- promoted checkpoint that explicitly authorizes S0B;
- `docs/11-checkpoint.md`
- `docs/00-source-hierarchy.md`
- `docs/09-definition-of-done.md`
- `docs/10-decisions-ledger.md`
- `docs/70-r08-critical-tenant-security-architecture.md`
- `docs/73-r08-multitenant-security-requirements-addendum.md`
- `docs/91-r11-integrated-authority-state-dependency-architecture.md`
- `docs/100-r12-requirements-traceability-and-no-loss-proof.md`
- `docs/108-s0a-implementation-approval-and-checkpoint-promotion.md`
- `docs/109-implementation-authorization-s0b-candidate.md`
- `work-orders/HCT-IMPL-AUTH-0002.md`
- S0A ADR/contracts/tests/evidence;
- Issue #35 and the future S0B implementation issue.

## REQUIREMENTS
### REQ-S0B-001 - Server-derived authority
SecurityContext authority SHALL be constructed only from trusted/server-side evidence and canonical bindings. Client-provided tenant/account IDs alone SHALL never prove authority.

### REQ-S0B-002 - Immutability
SecurityContext and binding objects SHALL be immutable/frozen after construction.

### REQ-S0B-003 - Typed scope
Principal/tenant/membership/account/session/correlation and secret-reference identities SHALL be typed and validated.

### REQ-S0B-004 - Exact tenant/account/environment isolation
Mismatch at any required boundary SHALL reject before a protected action could continue.

### REQ-S0B-005 - Object authorization
Server-side guards SHALL validate object/resource scope. Identifier possession alone is insufficient.

### REQ-S0B-006 - Fail closed
Missing, malformed, expired/stale where applicable, unsupported-version, scope-mismatched or environment-mismatched contexts SHALL reject deterministically.

### REQ-S0B-007 - Opaque secrets
CredentialRef/SecretRef SHALL contain no secret value and SHALL have safe/redacted representations.

### REQ-S0B-008 - No secret resolution
The S0B SecretStore interface SHALL not return raw secret material and SHALL not connect to external providers.

### REQ-S0B-009 - No external authority
S0B SHALL introduce no exchange, network, persistence, deployment or trading authority.

### REQ-S0B-010 - Frontend non-authority
No frontend state or browser-supplied field becomes authoritative SecurityContext evidence.

### REQ-S0B-011 - Evidence
Exact-head tests/CI/evidence SHALL prove all required negative cases and absence of prohibited capability.

## ARCHITECTURE RULES
- Reuse S0A canonical contract/generation foundations. Do not create a shadow contract system.
- SecurityContext is backend/domain authority.
- Keep environment namespace exact and fail closed.
- Keep opaque secret references distinct from secret material.
- No secret value appears in serializable public contracts.
- No network/provider implementation in SecretStore.
- No persistence in this slice unless a future governed correction explicitly authorizes it.
- Keep APIs minimal and deterministic.
- Any material architecture deviation requires STOP + governed change control.

## CONSTRAINTS
- Work only after exact checkpoint authorization.
- Use a governed implementation branch and PR.
- No force push/history rewrite.
- Do not modify frozen planning semantics.
- No known CRITICAL/HIGH finding may be carried to merge.
- Same-account independent review is valid only as a separate execution stream that reconstructs the verdict.

## ACCEPTANCE CRITERIA
A. Exact authorized checkpoint/context lock passes before mutation.
B. SecurityContext is immutable, typed and versioned.
C. Trusted/server-side construction path is explicit and testable.
D. Client tenant/account fields cannot directly create authority.
E. Tenant/account/environment binding is immutable and fails closed on mismatch.
F. Object/scope authorization guard rejects cross-tenant/account cases.
G. Missing/malformed/unsupported/stale context cases defined by the implementation reject deterministically.
H. CredentialRef/SecretRef is opaque and non-secret.
I. Secret references are safely represented/redacted in logs/repr/serialization as designed.
J. SecretStore is provider-neutral and cannot return raw secret material.
K. No external secret provider integration exists.
L. No exchange/network/trading capability exists.
M. No DB/RLS/auth-provider/browser-login implementation exists.
N. Frontend remains non-authoritative.
O. Canonical contract generation/parity remains reproducible.
P. Backend strict type/lint/build/tests pass.
Q. Frontend regression build/tests remain green if shared contracts change.
R. Static secret scan covers changed text and fixtures.
S. Unauthorized-capability scan proves no exchange/provider/trading implementation.
T. Exact raw-head CI passes.
U. Independent HIGH_ASSURANCE review returns APPROVED with CRITICAL=0 and HIGH=0.

## TESTS
At minimum, if authorized:
- SecurityContext happy-path construction from trusted evidence;
- immutability/frozen behavior;
- client-only tenant/account input cannot create authoritative context;
- missing tenant/membership/account when required rejects;
- wrong tenant rejects;
- wrong account rejects;
- wrong environment rejects;
- wrong membership/policy/role/scope rejects;
- malformed typed IDs reject;
- unsupported context version rejects;
- expired/stale context rejects if expiry is modeled;
- object/resource ownership mismatch rejects;
- binding mismatch matrix across tenants/accounts/environments;
- CredentialRef/SecretRef cannot accept or serialize secret-value fields;
- safe repr/log output contains no raw secret material;
- fake/null SecretStore cannot resolve external providers or expose raw secret data;
- generated/shared contract parity/reproducibility;
- secret scan over all changed text/fixtures;
- prohibited capability scan for exchange/provider/trading code;
- existing S0A regression suite;
- strict type/lint/build/dependency audit;
- `git diff --check` against exact PR base.

Property/fuzz tests SHOULD be used where effective for cross-tenant/account/environment mismatch matrices and malformed identity inputs.

## DELIVERABLES
If authorized, expected implementation deliverables include:
- one security-boundary ADR before substantive code;
- canonical/shared contract updates;
- backend SecurityContext/binding/guard implementation;
- opaque SecretStore interface and test-only null/fake boundary;
- tests including negative isolation matrix;
- CI updates if required;
- `evidence/HCT-IMP-0002-S0B.md`;
- one implementation PR;
- exact-head author-side evidence;
- independent review verdict.

## REVIEW FORMAT
Independent reviewer returns exactly one:
- `APPROVED`
- `CORRECTION REQUIRED`
- `BLOCKED`

Review SHALL report exact head, tests/build/audits, cross-tenant/account/environment isolation, opaque secret boundary, prohibited capability audit, CRITICAL count and HIGH count.

## STOP CONDITION
After implementation, stop with the S0B PR OPEN and UNMERGED after exact-head CI/evidence and author-side preflight. Do not merge, promote checkpoint, add real credentials, integrate a production secret provider, connect to an exchange, deploy production, activate limited-live or enable real-money trading. A separate independent HIGH_ASSURANCE review is mandatory.