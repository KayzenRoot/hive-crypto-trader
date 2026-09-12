# HCT-IMPL-AUTH-0002 - S0B Implementation Authorization Candidate

Status: `INDEPENDENT_REVIEW_REQUIRED`
Risk class: `HIGH_ASSURANCE`
Authorization increment: `HCT-IMPL-AUTH-0002`
Candidate implementation slice: `HCT-IMP-0002-S0B`
Canonical base: `main@9353cd691d73a4b769d1ccd13823142b2ebf8168`
Canonical checkpoint: `HCT-CP-0016 / S0A_IMPLEMENTATION_APPROVED_MERGED`

## Purpose
Evaluate whether one bounded continuation of R11 Stage 0 may be authorized after approved S0A completion. This candidate grants no implementation authority until independent review, merge, and a new checkpoint promotion explicitly authorize only `HCT-IMP-0002-S0B`.

## Current authoritative state
At `HCT-CP-0016`:
- `implementation_authorized=false`
- `implementation_authorization_scope=[]`
- `implementation_authorization_ceiling="NONE_PENDING_NEXT_GOVERNED_AUTHORIZATION"`
- `production_credentials_authorized=false`
- `production_deployment_authorized=false`
- `limited_live_authorized=false`
- `live_trading_authorized=false`

S0A is approved and merged. Planning remains frozen under `HCT-CP-0014`.

## Why S0B is next
R11 Stage 0 requires shared contracts/governance/security foundations before exchange truth, realtime, risk, execution, intelligence or live-capable behavior. S0A completed the runtime/repository/canonical-contract foundation. The next necessary bounded dependency is the security identity boundary required by R08 and R11:
- canonical server-derived `SecurityContext`;
- exact tenant/account binding;
- opaque secret-reference boundary.

## Proposed authorization
After independent approval, merge, and checkpoint promotion, authorize exactly:

`HCT-IMP-0002-S0B - SecurityContext, Tenant/Account Binding & Opaque SecretStore Foundation`

Proposed ceiling:

`NON_TRADING_STAGE_0_SECURITY_FOUNDATION_ONLY`

## Proposed S0B scope
### 1. Canonical SecurityContext
Implement an immutable/versioned server-authority context containing typed identity for, where applicable:
- authenticated principal;
- tenant;
- membership;
- account scope;
- role/permission or policy version reference;
- assurance state;
- session identity/version;
- correlation/trace identity;
- environment namespace.

Client-supplied tenant/account identifiers are routing/input data only and SHALL NOT create authority.

### 2. Tenant/account binding
Implement canonical immutable binding primitives sufficient to express and validate:

`tenant -> exchange account identity -> opaque CredentialRef -> policy/risk namespace -> environment`

S0B SHALL NOT connect to an exchange and SHALL NOT resolve `CredentialRef` into secret material.

### 3. Fail-closed authorization guards
Implement deterministic pure/internal guard primitives that reject:
- missing or malformed SecurityContext;
- tenant mismatch;
- membership/account mismatch;
- environment mismatch;
- absent required scope/role/policy evidence;
- stale/incompatible context version where defined;
- object identifiers whose ownership/scope does not match the context.

No browser-side or frontend-only decision grants backend authority.

### 4. Opaque SecretStore abstraction
Implement only a provider-neutral abstraction and opaque metadata/reference contracts needed by later authorized slices.

Allowed concepts:
- `CredentialRef` / `SecretRef` typed opaque identifier;
- secret purpose/classification metadata;
- provider-neutral store capability interface/port;
- non-secret metadata needed for policy checks;
- safe/redacted representation rules;
- deterministic fake/null adapter for tests only, containing no real secret values.

The abstraction SHALL NOT expose or persist real API keys, secret keys, private keys, tokens, seed phrases or other secret material in this slice.

### 5. Security evidence/tests
Implement tests proving exact tenant/account/environment separation, fail-closed context validation, redacted/opaque secret references and absence of secret/exchange capabilities.

## Explicitly out of scope
S0B SHALL NOT implement:
- real API keys, secret keys, private keys, tokens or secret values;
- credential import, verification, activation, rotation, invalidation, compromise, revocation or deletion workflows;
- AWS Secrets Manager, GCP Secret Manager, Azure Key Vault, HashiCorp Vault, KMS/HSM or any production secret provider;
- secret encryption/decryption implementation;
- OAuth/OIDC, login, MFA, passkeys/WebAuthn, recovery or browser session flows;
- database persistence, RLS or cache/queue tenant isolation;
- exchange connectivity, MEXC adapters, REST/WebSocket clients or private streams;
- market-data ingest;
- Safety, Session Policy, Risk, sizing, leverage, reservations;
- OMS, orders, cancel/replace, fills, positions, balances;
- reconciliation or protection;
- strategies, signals, models, agents, Brain, RAG or Copilot;
- production deployment;
- limited-live or real-money trading;
- later Stage-0 or Stage-1+ capability.

## Proof obligations
An implementation candidate under this authorization SHALL prove at minimum:
1. `SecurityContext` is immutable and typed.
2. Authority can only be derived through a trusted/server-side construction boundary, not from raw client tenant/account fields.
3. Cross-tenant and cross-account access attempts fail closed.
4. Environment mismatch fails closed across `LIVE`, `PAPER`, `SHADOW`, `REPLAY`.
5. Object/scope authorization is server-side and identifier knowledge alone grants no access.
6. Tenant-account binding rejects mismatched tenant/account/environment combinations.
7. `CredentialRef` is opaque, non-secret and safe to log only in its governed redacted/reference form.
8. No secret material appears in source, fixtures, logs, traces, snapshots, generated contracts or test output.
9. SecretStore remains a provider-neutral interface/test double only and cannot reach external secret providers.
10. No exchange/network/trading capability is introduced.
11. Frontend remains non-authoritative.
12. Exact-head CI/evidence and independent HIGH_ASSURANCE review are required before merge.

## Proposed post-approval flags
Only after a later checkpoint promotion:
- `implementation_authorized=true`
- `implementation_authorization_scope=["HCT-IMP-0002-S0B"]`
- `implementation_authorization_ceiling="NON_TRADING_STAGE_0_SECURITY_FOUNDATION_ONLY"`
- `production_credentials_authorized=false`
- `production_deployment_authorized=false`
- `limited_live_authorized=false`
- `live_trading_authorized=false`

## Independent review requirements
The reviewer SHALL verify:
- exact PR base/head identity;
- S0A/CP0016 provenance;
- R08 `TEN-001`, `TEN-002`, `TEN-007`, `SEC-001`, `SEC-004` alignment;
- R11 Stage-0 ordering;
- no semantic expansion beyond the proposed bounded security foundation;
- no real secret material/provider implementation;
- no exchange, trading, deployment or live authority;
- implementation Work Order completeness;
- exact-head authorization-governance CI success;
- zero unresolved CRITICAL/HIGH findings.

Verdict exactly one of:
- `APPROVED`
- `CORRECTION REQUIRED`
- `BLOCKED`

## STOP CONDITION
Do not begin product implementation from this document. Keep the authorization PR open and unmerged until exact-head governance CI succeeds and a separate HIGH_ASSURANCE execution stream publishes its verdict. Merge/promotion may authorize only `HCT-IMP-0002-S0B`. No credentials, production deployment, limited-live or live trading are authorized by this candidate.