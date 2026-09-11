# HCT-PLAN-0001-R08 — Multi-Tenant / Security / Secrets / Commercialization Gap Audit

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R08`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`
Initial verdict: `CORRECTION REQUIRED`

## Objective
Reconcile the existing Multi-Tenant Platform Foundation, security placeholder, Administrative Control Plane/Harness and free-first infrastructure planning against the requirements of a commercial automated futures platform holding exchange credentials and operating on behalf of multiple independent tenants.

The core security objective is stronger than “users cannot see each other’s dashboard.” One tenant must not be able to read, influence, exhaust, impersonate, route orders through, inherit credentials from or corrupt the authoritative state of another tenant. Administrative/support access must be explicit, purpose-limited and auditable.

## Canonical pre-discovery inputs
- `docs/05-security.md`
- `docs/20-admin-control-plane-and-harness.md`
- `docs/32-bootstrap-free-infrastructure-and-scale-migration.md`
- `docs/14-product-module-map.md`
- `docs/04-architecture.md`
- approved R03–R07 authority, execution, realtime, intelligence and promotion contracts.

## External security anchors reviewed
Planning should align where applicable with current public guidance such as:
- NIST SP 800-63-4 Digital Identity Guidelines (final July 2025) for authentication/federation assurance concepts;
- OWASP Multi-Tenant Security Cheat Sheet for tenant-context propagation, cache/session/data isolation and noisy-neighbor controls;
- OWASP Secrets Management Cheat Sheet for least privilege, secret lifecycle, rotation, auditing and separation of secret-management authority.

These are guidance inputs, not substitutes for HCT-specific threat modeling.

## Existing strengths
- backend is authoritative and frontend is an untrusted client;
- no exchange secret belongs in the repository/client;
- owner-only Administrative Control Plane with step-up authentication concepts;
- Harness supports scoped capability isolation and blast-radius awareness;
- multi-tenant foundation already requires isolation, quotas, policy and audit boundaries;
- free-first infrastructure explicitly refuses unsafe service choices;
- R03–R07 already define strong tenant-sensitive Risk, Execution, Realtime, Intelligence and Promotion state that can be bound to tenancy.

## R08 gaps

### GAP-R08-01 — Canonical Tenant Security Context
Severity: `CRITICAL`
Every request, job, event, cache access, model/tool call and state transition needs one authenticated/authorized canonical tenant/account/security context. User-supplied tenant IDs cannot be treated as authorization proof.

### GAP-R08-02 — Object-level authorization / ownership invariant
Severity: `CRITICAL`
Every tenant-owned resource must be authorized server-side by ownership and operation, preventing BOLA/IDOR-style cross-tenant access even when identifiers are guessed or leaked.

### GAP-R08-03 — Database tenant-isolation contract
Severity: `CRITICAL`
Need deterministic DB isolation strategy, including tenant ownership columns/keys where appropriate, RLS or equivalent defense-in-depth, migration/test rules and prohibition of ordinary tenant paths using superuser/BYPASSRLS-style authority.

### GAP-R08-04 — Connection-pool / session-context isolation
Severity: `CRITICAL`
Tenant/session context must not leak across reused DB connections, worker pools or async task contexts. Transaction-local or equivalent reset-safe semantics and isolation tests are required.

### GAP-R08-05 — Cache tenant isolation
Severity: `CRITICAL`
Every tenant/user/policy-sensitive cache key requires canonical tenant/user/permission/version namespace, authorization before protected reads and explicit global-shared namespace for intentionally common data.

### GAP-R08-06 — Queue/event/message tenant isolation
Severity: `CRITICAL`
Queued work and events require authenticated producer identity, tenant/account scope, authorization at consumer, idempotent ownership checks and no assumption that a tenant_id field alone proves authority.

### GAP-R08-07 — Trading worker ownership isolation
Severity: `CRITICAL`
Realtime workers, subscriptions, OMS commands, Risk Reservations and account reconciliation must bind to tenant+exchange-account identity so one tenant’s worker/state cannot route through another tenant’s credentials or account.

### GAP-R08-08 — Exchange credential vault boundary
Severity: `CRITICAL`
Exchange API credentials need per-tenant/account secret identities, encrypted storage, runtime-only retrieval, least-privilege permissions, no frontend exposure, no broad shared “master exchange key” and explicit metadata without exposing secret material.

### GAP-R08-09 — Secret encryption/key hierarchy
Severity: `CRITICAL`
Need envelope/key hierarchy separating application data from secret-encryption keys, environment separation, provider-neutral SecretStore/KMS contract, key rotation/versioning and explicit blast radius if one wrapping/data key is compromised.

### GAP-R08-10 — Secret lifecycle / rotation / revocation
Severity: `CRITICAL`
Create/import/verify/activate/rotate/revoke/delete/recover workflows require states, audit, grace/overlap strategy where supported and immediate no-new-exposure behavior if a credential becomes invalid/compromised.

### GAP-R08-11 — Secret exfiltration prevention
Severity: `CRITICAL`
Logs, traces, metrics, exception payloads, support tools, CI output, prompts/agents, browser responses and crash dumps must have explicit redaction/non-export rules. Agents/models never receive raw exchange secrets unless an impossible-to-avoid future capability is separately approved.

### GAP-R08-12 — Human authentication assurance
Severity: `CRITICAL`
Need user/admin authentication baseline covering phishing-resistant options/passkeys where supported, MFA/step-up for dangerous actions, session assurance, reauthentication, risk-based challenges and password fallback rules where retained.

### GAP-R08-13 — Account recovery security
Severity: `CRITICAL`
Recovery cannot become the weakest path. Need recovery-factor lifecycle, anti-social-engineering controls, cooldown/notification for sensitive recovery, session/key revocation and special handling for owner/super-admin recovery.

### GAP-R08-14 — Session/token lifecycle and revocation
Severity: `CRITICAL`
Access/refresh/session tokens need audience/scope, rotation/reuse detection where applicable, expiration, device/session visibility, global/tenant/user revocation and forced reauthentication after password/MFA/security-critical changes.

### GAP-R08-15 — Service-to-service workload identity
Severity: `CRITICAL`
Backend workers/services require distinct least-privileged workload identities and short-lived credentials where practical; shared static service secrets cannot become an invisible platform-wide root credential.

### GAP-R08-16 — Privileged admin authorization / break-glass
Severity: `CRITICAL`
Owner/admin control requires separate privileged policy, step-up authentication, reason/context, short-lived elevation, immutable audit and break-glass recovery. Normal tenant credentials cannot be upgraded into admin by client-side state.

### GAP-R08-17 — Support impersonation / tenant data access
Severity: `CRITICAL`
Future support/admin access to tenant views/data requires purpose-limited scoped access, explicit actor identity, visible impersonation state, reason/ticket, time limit and audit. Silent impersonation is prohibited.

### GAP-R08-18 — Tenant-scoped Harness authority
Severity: `CRITICAL`
Harness changes must bind to tenant/account/capability scope and dependency graph. A tenant-specific freeze/quarantine must not accidentally apply to other tenants; global emergency controls remain separately privileged.

### GAP-R08-19 — Entitlement vs authorization separation
Severity: `CRITICAL`
Commercial plan/feature entitlements cannot grant trading/security authority by themselves. Billing says what feature is purchased; authorization/policy says what operation is allowed. Downgrade/expiry must fail safely without breaking protection/reconciliation of existing positions.

### GAP-R08-20 — Tenant resource quota / noisy-neighbor governor
Severity: `CRITICAL`
Per-tenant quotas are required for API calls, WS subscriptions, scanner breadth, agent/model/token spend, replay jobs, storage, event queues and worker compute so one tenant cannot starve protection/reconciliation resources of another.

### GAP-R08-21 — Cross-tenant observability leakage
Severity: `HIGH`
Logs/metrics/traces/dashboard labels must prevent tenant-sensitive data leakage while preserving supportability. High-cardinality tenant labels and trace payloads need privacy/security rules.

### GAP-R08-22 — Audit-log isolation and integrity
Severity: `HIGH`
Audit evidence needs append-only integrity, actor/tenant/account context, retention, access control and cross-tenant query boundaries. Admin audit access should not imply secret/data access.

### GAP-R08-23 — Tenant-scoped rate limiting / abuse controls
Severity: `HIGH`
Need layered user/session/IP/device/tenant/API-key limits, credential-stuffing protection, enumeration resistance, abuse thresholds and safe escalation without allowing one attacker to deny service to unrelated tenants.

### GAP-R08-24 — API/webhook authorization and signing
Severity: `HIGH`
Future public APIs/webhooks require tenant-bound credentials/scopes, signature/replay protection, idempotency, rotation/revocation and webhook destination abuse/SSRF controls.

### GAP-R08-25 — CSRF/CORS/clickjacking/frontend session boundary
Severity: `HIGH`
Browser security controls must be explicit even though frontend is untrusted: secure cookie/token handling, CSRF defense where applicable, restrictive CORS, frame protections and no sensitive authorization logic in client code.

### GAP-R08-26 — Encryption/data-classification policy
Severity: `HIGH`
Need data classification for public, tenant-confidential, PII, trading-sensitive, secret and audit data plus encryption in transit/at rest, field-level protection where justified and key-access policy by class.

### GAP-R08-27 — Backup/restore tenant isolation
Severity: `HIGH`
Backups and restores must preserve tenant boundaries, encryption and audit; restoring one tenant must not overwrite another or resurrect revoked secrets/session state without explicit reconciliation.

### GAP-R08-28 — Tenant offboarding / deletion / export
Severity: `HIGH`
Commercial platform needs deterministic account closure, exchange-credential revoke/delete, data export, retention/legal hold, delayed deletion and proof of completion while retaining legally/operationally required immutable trading/audit evidence.

### GAP-R08-29 — Data retention and privacy minimization
Severity: `HIGH`
Define purpose/retention for PII, trading history, raw market data, support evidence, model/RAG memory and security telemetry. Do not retain sensitive data merely because storage is available.

### GAP-R08-30 — Environment isolation
Severity: `HIGH`
Development/test/staging/production require separate secrets, identities, databases/tenants or equivalent boundaries. Production credentials/data must not be casually copied into lower environments.

### GAP-R08-31 — CI/CD and supply-chain secret boundary
Severity: `HIGH`
Build/release systems need least-privileged workload identities, protected environments, no secret leakage in logs/artifacts/forks, dependency/provenance controls and separation between deployment authority and raw secret visibility.

### GAP-R08-32 — Tenant-safe custom strategy/model artifacts
Severity: `HIGH`
User strategies, configs, uploaded artifacts and future models must be tenant-scoped, immutable/versioned and sandboxed. Arbitrary code/files/network access cannot bypass tenancy or secrets boundaries.

### GAP-R08-33 — Security event / incident tenant blast radius
Severity: `HIGH`
Incident state must identify affected tenant/account/capability/key, freeze narrowly where safe, revoke compromised credentials/sessions and communicate recovery without exposing unrelated tenant data.

### GAP-R08-34 — Security telemetry / anomaly detection
Severity: `HIGH`
Need detection for impossible tenant transitions, secret access anomalies, privilege escalation, unusual admin/support access, session takeover, API-key failures, mass export and cross-tenant authorization denials.

### GAP-R08-35 — Tenant-aware disaster recovery
Severity: `HIGH`
DR runbooks must restore identity, secret-store availability, tenant data, queues, trading/reconciliation state and audit integrity without cross-tenant mixing or blindly resuming exposure.

### GAP-R08-36 — Commercial plan state transitions
Severity: `HIGH`
Trial/paid/past-due/cancelled/suspended/downgraded states need deterministic feature behavior that preserves safety-critical position management/reconciliation and cannot strand open exposure because billing changed.

### GAP-R08-37 — Regional/commercial eligibility boundary
Severity: `HIGH`
Future commercialization needs tenant/account eligibility metadata for supported region, exchange availability/KYC/API permission and product restrictions. UI language or payment success cannot imply trading eligibility.

### GAP-R08-38 — Terms/consent/risk disclosure versioning
Severity: `HIGH`
Required product terms, privacy consent and risk disclosures need version/acceptance evidence and material-change handling, while legal/compliance wording remains a future reviewed artifact rather than invented by trading logic.

### GAP-R08-39 — Security testing / adversarial tenant test matrix
Severity: `HIGH`
Need systematic tests for cross-tenant IDs, caches, queues, DB/RLS, workers, websockets, exports, admin/support, backups, billing transitions and race conditions, plus secret-leak scanning and authz fuzz/property tests.

### GAP-R08-40 — Security baseline / vulnerability lifecycle
Severity: `HIGH`
Need dependency/container/code scanning, vulnerability triage severity/SLA, coordinated patch/rollback, penetration-test readiness, SBOM/provenance expectations and policy for security-critical emergency changes without bypassing audit.

## Priority closure order
### CRITICAL first
1. Tenant Security Context
2. object-level authorization
3. DB + connection-pool isolation
4. cache + queue/event isolation
5. trading worker/account ownership
6. credential vault + key hierarchy
7. secret lifecycle/exfiltration prevention
8. human auth + recovery + sessions
9. workload identities
10. admin/break-glass/support access
11. tenant Harness scoping
12. entitlement/authorization separation
13. noisy-neighbor resource quotas

### HIGH next
Observability/audit privacy, rate limits, APIs/webhooks/browser controls, encryption/classification, backup/offboarding/retention, environment/CI supply chain, strategy artifact sandboxing, incident/DR, commercial state/eligibility/consent, security testing and vulnerability lifecycle.

## Initial verdict
`CORRECTION REQUIRED`

The pre-discovery establishes intent but does not yet define enough machine-enforceable tenant, identity, secret, authorization and commercialization safety contracts for R08 approval.

## STOP CONDITION
Do not approve R08 while any CRITICAL/HIGH gap remains unresolved. Planning approval does not authorize implementation, production secrets/credentials, deployment or live trading.