# HCT-PLAN-0001-R08 — Acceptance Criteria & Review Gates

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R08`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

## Purpose
Define objective planning gates required before R08 may receive `APPROVED`.

## Gate A — Canonical Security Context
Every protected request/job/event/state transition derives authenticated tenant/principal/account scope server-side; client tenant metadata alone never proves authority.

## Gate B — Object authorization
Every tenant-owned resource and operation has server-side ownership/authorization enforcement and non-enumerating cross-tenant denial behavior where practical.

## Gate C — Database & pool isolation
Tenant persistence has enforceable ownership/RLS-or-equivalent defense, no ordinary bypass role, transaction/reset-safe pool context and adversarial cross-tenant tests.

## Gate D — Cache / queue / event isolation
Tenant-sensitive cache namespaces and async work envelopes bind tenant/principal/policy while consumer authorization remains mandatory; forged tenant metadata cannot cross boundaries.

## Gate E — Trading account binding
Risk, reservations, execution, OMS, private streams, protection and reconciliation use canonical tenant–exchange-account–credential binding and reject inconsistent cross-tenant commands.

## Gate F — Credential vault
Raw exchange credentials live behind an encrypted backend SecretStore boundary with least-privileged workload access, no browser/admin ordinary reveal and no shared tenant master key.

## Gate G — Cryptographic/key separation
Environment and tenant/account secret blast radius is bounded by provider-neutral envelope/key hierarchy, key versioning/rotation and separation between encrypted database backups and decryption authority.

## Gate H — Secret lifecycle & exfiltration
Credential import/verify/activate/rotate/revoke/compromise/delete is an audited state machine; raw secrets are never logged/traced/prompted/exported through ordinary paths.

## Gate I — Human authentication assurance
Tenant/admin authentication supports strong MFA/phishing-resistant methods, assurance-aware SecurityContext and step-up/re-authentication for dangerous actions.

## Gate J — Recovery & session lifecycle
Account recovery cannot bypass authentication policy; sessions/tokens have bounded scope/lifetime, revocation/security-version semantics and sensitive-change invalidation.

## Gate K — Workload identity
Services/workers have distinct least-privileged authenticated workload principals; shared static platform root credentials are not the default service trust model.

## Gate L — Admin / break-glass
Privileged authority uses a distinct policy/session plane with high assurance, reason/scope/blast-radius evidence, time-bounded elevation and audited break-glass behavior.

## Gate M — Support assumption
Any future support impersonation preserves real actor + assumed identity, is time/purpose limited, read-only by default, cannot reveal secrets and is fully audited.

## Gate N — Tenant-scoped Harness
Harness capability controls resolve exact tenant/account/capability scope and cannot spill tenant-specific freezes/quarantines into unrelated tenants unintentionally.

## Gate O — Entitlement vs authorization
Plan/feature entitlement is independent of execution/security authorization. Billing state changes cannot bypass Safety/Risk or strand existing protected exposure.

## Gate P — Noisy-neighbor governor
Per-tenant/account workload quotas and fair scheduling preserve platform/safety reserves so one tenant cannot starve unrelated tenants’ protection/reconciliation.

## Gate Q — Observability & audit isolation
Logs/traces/metrics and audit evidence preserve tenant/privacy boundaries, actor attribution and tamper-resistant history without leaking secrets or unrelated tenant data.

## Gate R — Abuse/rate-limit controls
Authentication/API/export/replay abuse is rate-limited at appropriate identity/network/tenant layers and containment is as local as safely possible.

## Gate S — Public API/webhook/browser boundary
Future APIs/webhooks have tenant-bound scopes/signatures/replay/idempotency/SSRF controls; browser sessions use appropriate CSRF/CORS/CSP/frame/token protections with no client-only authorization.

## Gate T — Data classification & encryption
All data families have sensitivity class, allowed stores/logging/retention/export rules and encryption requirements; SECRET material receives stronger field/envelope protection.

## Gate U — Backup / restore isolation
Backups preserve encryption and tenant boundaries; restore procedures prevent tenant mixing and reconcile revoked sessions/secrets plus OMS/Risk/open-position state.

## Gate V — Offboarding / retention / RAG deletion
Tenant closure safely handles open exposure, credential revocation, export, legal/audit retention, deletion evidence and removal from caches/vector/RAG indexes.

## Gate W — Environment / CI supply-chain isolation
Prod/non-prod secrets and identities are separate; CI/CD uses least privilege, protected deployment boundaries, secret/provenance/dependency controls and cannot leak production secrets into forks/build output.

## Gate X — Tenant artifact sandbox
Custom strategies/uploads/configuration are tenant-scoped/versioned/untrusted, bounded in resource complexity and cannot gain arbitrary filesystem/network/process/SecretStore capabilities.

## Gate Y — Incident & anomaly containment
Security events identify tenant/account/capability/secret blast radius, detect suspicious cross-tenant/privileged/secret/session behavior and preserve safe containment/reconciliation.

## Gate Z — Tenant-aware disaster recovery
DR restores identity, SecretStore, data, queues, Risk/OMS/reconciliation and audit state without cross-tenant mixing and resumes new exposure only after restrictive recovery proof.

## Gate AA — Commercial state transitions
Trial/paid/grace/past-due/cancel/suspend/offboard states have deterministic entitlement behavior that always preserves required protection/close/reconciliation/offboarding paths.

## Gate AB — Regional eligibility & agreement evidence
Region/exchange/KYC/API eligibility is a server-side policy input independent of locale/payment; required terms/privacy/risk-disclosure acceptance is versioned evidence and legal wording remains externally reviewed.

## Gate AC — Adversarial tenant testing
Future implementation requires a systematic cross-tenant security matrix covering IDs, DB/RLS, pools, cache, queues, workers, websockets, export, admin/support, backups, billing races and secret leakage.

## Gate AD — Vulnerability lifecycle
Security baseline includes code/dependency/container/IaC scanning where applicable, vulnerability triage/remediation, provenance/SBOM expectations, emergency security patch audit and penetration-test readiness.

## Gate AE — Canonical consistency
Before approval:
- accepted R08 decisions are consolidated in Decisions Ledger;
- accepted R08 requirements are canonical;
- all 40 gaps map to planning resolutions;
- Scope still prohibits implementation/production secrets/deployment/live trading;
- PR represents branch content;
- objective final R08 audit exists.

## Verdict rule
- unresolved CRITICAL/HIGH planning defect => `CORRECTION REQUIRED`;
- missing authoritative dependency required for planning => `BLOCKED`;
- all gates pass => `APPROVED`.

R08 planning approval never authorizes implementation, production secrets/credentials, deployment, limited-live or real-money trading.