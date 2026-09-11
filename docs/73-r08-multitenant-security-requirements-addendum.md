# HCT-PLAN-0001-R08 — Multi-Tenant Security & Commercialization Requirements Addendum

Status: `ACCEPTED_FOR_R08_PLANNING`
Increment: `HCT-PLAN-0001-R08`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

## Purpose
This addendum is the canonical R08 requirements source together with `docs/02-requirements.md` until planning-freeze consolidation.

## TEN-001 — Canonical Security Context
Every protected request, job, event, worker action and authoritative state mutation SHALL consume a server-derived immutable SecurityContext containing authenticated principal, tenant/membership/account scope, current policy/role/assurance/session state and correlation identity. Client tenant IDs alone SHALL NOT prove authority.

## TEN-002 — Object-level authorization
Every tenant-owned resource/action SHALL enforce server-side ownership and operation authorization, including internal APIs and background jobs. Knowledge of identifiers SHALL NOT grant access.

## TEN-003 — Database isolation
Tenant persistence SHALL enforce tenant ownership using application authorization plus database-level defense such as RLS/equivalent where appropriate. Ordinary tenant request paths SHALL NOT use superuser/BYPASSRLS-style authority. Cross-tenant negative tests are mandatory.

## TEN-004 — Pooled context isolation
DB connections, async workers, threads/coroutines and job runners SHALL not carry tenant authority across reuse. Tenant context SHALL be transaction/reset-safe and concurrency-tested.

## TEN-005 — Cache isolation
Tenant/user/policy-sensitive cache values SHALL use tenant-aware namespaces and authorization before protected reads. Intentionally global entries SHALL use an explicit global-safe classification.

## TEN-006 — Queue/event isolation
Tenant-bound messages SHALL use an authenticated TenantWorkEnvelope with producer, tenant/account/resource, operation, policy/version, expiry and idempotency identity. Consumers SHALL authenticate producer and re-authorize operation/resource.

## TEN-007 — Tenant–exchange-account binding
Every private market stream, RiskSnapshot, Risk Reservation, Execution Command, OMS event, position, protection and reconciliation state SHALL resolve one canonical tenant–exchange-account–credential binding. Cross-tenant/account binding mismatch SHALL reject before exchange transmission.

## SEC-001 — Exchange credential vault
Raw exchange credentials SHALL be stored only behind the backend SecretStore/Vault boundary, never in the frontend or ordinary tenant configuration. Workload access SHALL be least-privileged and scoped to credential purpose.

## SEC-002 — Secret cryptographic hierarchy
Secret encryption SHALL use provider-neutral envelope/key-management semantics with production/non-production separation, versioned rotation and bounded tenant/account compromise blast radius. Encrypted DB backup alone SHALL NOT contain sufficient trust to decrypt exchange credentials.

## SEC-003 — Credential lifecycle
Credential import, verification, activation, rotation, invalidation, compromise, revocation and deletion SHALL be an explicit audited state machine. Invalid/compromised credentials SHALL block new exposure for affected account and trigger reconciliation/protection assessment.

## SEC-004 — Secret exfiltration prevention
Raw secrets SHALL be classified `NEVER_LOG`, `NEVER_TRACE`, `NEVER_PROMPT`, `NEVER_EXPORT`. Errors, logs, traces, audit payloads, support tools, CI/artifacts and AI/agent paths SHALL receive opaque references/redacted metadata rather than secret values.

## IAM-001 — Authentication assurance
HCT SHALL support strong MFA and phishing-resistant authenticators such as passkeys/WebAuthn where supported. Privileged administration requires strong authentication; dangerous tenant/admin actions SHALL require current step-up/re-authentication according to risk.

## IAM-002 — Secure account recovery
Recovery SHALL be a governed high-assurance flow with protected recovery factors, anti-social-engineering controls, session/security revalidation and stronger owner/super-admin break-glass recovery. Support personnel SHALL NOT bypass recovery by direct database mutation.

## IAM-003 — Session/token lifecycle
Sessions/tokens SHALL be scoped, audience-bound, bounded in lifetime, revocable and security-version aware. Sensitive identity/role/recovery changes SHALL revoke/revalidate affected sessions and private realtime channels within bounded time.

## IAM-004 — Workload identity
Backend services/workers SHALL use distinct authenticated least-privileged workload principals and short-lived credentials where practical. Runtime, CI/CD, market data, admin and SecretStore authorities SHALL be separated.

## ADM-001 — Privileged admin boundary
Admin authority SHALL use a distinct privileged session/policy plane with strong authentication, step-up, reason/context, scope/blast-radius preview, time-bounded elevation, before/after evidence and immutable audit.

## ADM-002 — Break-glass
Break-glass recovery/authority SHALL be separate from routine administration, strongly protected, tested and high-severity audited/alerted. Initial single-owner policy SHALL NOT be misrepresented as dual-control security.

## ADM-003 — Support assumption
Future support/impersonation SHALL preserve real actor plus assumed tenant/user identity, be purpose/time limited and read-only by default, never reveal raw secrets and remain visibly/auditably active. Silent impersonation is prohibited.

## ADM-004 — Tenant-scoped Harness
Harness controls SHALL use exact typed scope and dependency/blast-radius evaluation. Tenant/account quarantine SHALL NOT unintentionally affect unrelated tenants; wildcard/global controls require stronger privilege.

## COM-001 — Entitlement is not authorization
Commercial plan/feature entitlement SHALL be separate from identity/authorization/trading authority. Final operation authority remains the intersection of membership/policy/entitlement/Safety/Risk/exchange capability/state. Billing changes SHALL preserve required reduction/protection/reconciliation for existing exposure.

## TEN-008 — Noisy-neighbor resource governance
HCT SHALL enforce hierarchical platform/safety/tenant/account/workload quotas for API, WS, scan, AI, replay, queue, storage, cache and compute. One tenant SHALL be throttled/degraded locally before unrelated tenants lose safety-critical protection/reconciliation capacity.

## SEC-005 — Tenant-safe observability
Telemetry SHALL minimize tenant-sensitive/PII data, never expose raw secrets and enforce authorization on tenant/admin queries. Cross-tenant system health views SHALL reveal only necessary impact metadata.

## SEC-006 — Audit integrity/isolation
Security/admin/trading audit evidence SHALL preserve actor, tenant/account, operation, assurance, reason, time, outcome and integrity/version data in an access-controlled append-only/tamper-evident logical boundary.

## SEC-007 — Abuse and rate-limit controls
Authentication, recovery, APIs, exports and expensive workloads SHALL have layered user/session/network/tenant/workload abuse controls with local containment and observable recovery/escalation.

## SEC-008 — Public API/webhook security
Future APIs/webhooks SHALL use tenant-bound scoped credentials, rotation/revocation, signature/freshness/replay/idempotency controls and SSRF/private-network destination protections.

## SEC-009 — Browser security
Frontend SHALL remain untrusted and use appropriate secure session/cookie/token, CSRF, CORS, CSP/XSS and clickjacking protections. No sensitive authorization or exchange secret may depend on browser-only state.

## DATA-001 — Data classification/encryption
All data SHALL be classified at least as PUBLIC, INTERNAL, TENANT_CONFIDENTIAL, PII, TRADING_SENSITIVE, SECRET or AUDIT_SECURITY, with defined store/encryption/logging/retention/export/access policy per class.

## DATA-002 — Backup/restore isolation
Backups SHALL preserve tenant boundaries and encryption/key separation. Restores SHALL reconcile revoked secrets/sessions, OMS/Risk/open-position state and SHALL NOT mix or overwrite unrelated tenant state.

## DATA-003 — Offboarding/export/deletion
Tenant closure SHALL safely handle open exposure, export, credential revoke/delete, retention/legal/audit holds, cache/index/RAG deletion and proof of completed deletion/retention reasons.

## DATA-004 — Privacy/retention minimization
Each data family SHALL have documented purpose and retention lifecycle. Sensitive PII, support data, raw telemetry and RAG/vector data SHALL NOT be retained indefinitely without explicit purpose.

## OPS-001 — Environment isolation
Production and non-production SHALL use separate identities, secrets and data boundaries. Production customer data/credentials SHALL NOT be copied into lower environments by default.

## OPS-002 — CI/CD supply-chain boundary
CI/CD SHALL use least-privileged identities, protected production deployment gates, secret-leak controls, reviewed workflows and dependency/provenance/SBOM expectations. Fork/PR jobs SHALL NOT inherit production secrets.

## TEN-009 — Tenant-safe strategy/artifact sandbox
User strategies/configs/uploads SHALL be tenant-scoped, immutable/versioned and treated as untrusted input. Arbitrary backend code/filesystem/network/process/SecretStore access remains prohibited unless separately designed and sandboxed in a future decision.

## SEC-010 — Tenant-scoped incident response
Security incidents SHALL track exact tenant/account/principal/capability/secret/release scope and follow contain→reconcile→recover→verify semantics with the narrowest safe freeze and no unrelated tenant disclosure.

## SEC-011 — Security anomaly detection
HCT SHALL detect cross-tenant context mismatches, authorization denials, secret-access anomalies, privilege/support/admin anomalies, takeover/recovery patterns, export abuse and suspicious global Harness actions.

## OPS-003 — Tenant-aware disaster recovery
DR SHALL restore identity, SecretStore/KMS, tenant data, queues, Risk/OMS/reconciliation and audit integrity without cross-tenant mixing. New exposure resumes only after restrictive recovery/reconciliation proof.

## COM-002 — Commercial state safety
Trial/paid/grace/past-due/cancelled/suspended/offboarding states SHALL have deterministic entitlements while preserving mandatory close/protection/reconciliation/export/offboarding actions.

## COM-003 — Regional/exchange eligibility
Region/jurisdiction, exchange availability, KYC/API permission and product restrictions SHALL be server-side eligibility policy inputs independent from locale or payment success. Unknown/incompatible live eligibility fails closed.

## COM-004 — Agreement/version evidence
Required Terms/Privacy/Risk agreements SHALL be versioned with user/tenant acceptance identity/time/hash and material-change handling. Legal wording remains subject to external professional review before commercialization.

## SEC-012 — Adversarial multi-tenant test matrix
Implementation validation SHALL systematically test cross-tenant object IDs, DB/RLS, pooled connections, cache, queues/events, workers/private streams, exports, support/admin, backups, billing transitions, auth revocation races and secret leakage, including property/fuzz tests where effective.

## SEC-013 — Vulnerability lifecycle
HCT SHALL maintain an auditable code/dependency/container/IaC vulnerability lifecycle as applicable, including detection, severity/exploitability triage, remediation/mitigation, regression, emergency patch/rollback, SBOM/provenance expectations and penetration-test readiness before broad commercialization.

## Safety
This addendum grants planning acceptance only. `implementation_authorized=false`; production credentials/secrets, deployment, limited-live and real-money trading remain unauthorized.