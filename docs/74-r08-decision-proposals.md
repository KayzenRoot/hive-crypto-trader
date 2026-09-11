# HCT-PLAN-0001-R08 — Decision Proposals for Ledger Consolidation

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R08`
Date: `2026-09-11`

These decisions are accepted within R08 planning but must be consolidated into `docs/10-decisions-ledger.md` before final R08 approval.

## HCT-DEC-0090 — Protected operations require canonical server-derived tenant security context
Status: APPROVED_FOR_DISCOVERY

Decision: every protected request, job, event, worker action and authoritative state transition derives an authenticated immutable SecurityContext containing principal, tenant/membership/account scope, policy/role/assurance/session state and correlation identity. Client-supplied tenant IDs or resource IDs never prove authority by themselves; every tenant-owned object/action requires server-side ownership/operation authorization.

## HCT-DEC-0091 — Tenant isolation spans database, connection pools, cache and asynchronous messaging
Status: APPROVED_FOR_DISCOVERY

Decision: HCT uses enforceable tenant ownership for persistence plus database defense-in-depth where appropriate; ordinary tenant paths do not use bypass authority. Pooled connection/async context cannot leak tenant state. Tenant-sensitive caches are namespaced/authorized, and queued/events are authenticated producer envelopes whose tenant metadata is routing context rather than authorization proof.

## HCT-DEC-0092 — Trading authority is bound to one canonical tenant–exchange-account identity
Status: APPROVED_FOR_DISCOVERY

Decision: private streams, RiskSnapshots/Reservations, execution commands, OMS, positions, protection and reconciliation bind to a canonical tenant–exchange-account–credential identity. Cross-tenant/account binding mismatch is rejected before exchange transmission. Shared cross-tenant exchange credentials/accounts are not an implicit V1 capability.

## HCT-DEC-0093 — Exchange credentials live behind a cryptographically separated SecretStore lifecycle
Status: APPROVED_FOR_DISCOVERY

Decision: raw exchange credentials are backend-only SecretStore objects protected by provider-neutral envelope/key-management semantics with environment and tenant/account blast-radius separation. Import/verify/activate/rotate/revoke/compromise/delete is an audited lifecycle; ordinary database/admin/frontend paths retain opaque references only.

## HCT-DEC-0094 — Raw secrets are never normal telemetry, prompt or support data
Status: APPROVED_FOR_DISCOVERY

Decision: raw secrets are `NEVER_LOG`, `NEVER_TRACE`, `NEVER_PROMPT`, `NEVER_EXPORT`. HCT uses secret-aware DTO/redaction, CI/artifact scanning and opaque capabilities for agents/tools. Invalid/compromised tenant exchange credentials block new exposure and trigger account-specific reconciliation/protection assessment.

## HCT-DEC-0095 — Human identity security includes strong authentication, step-up, recovery and revocable sessions
Status: APPROVED_FOR_DISCOVERY

Decision: HCT supports strong MFA and phishing-resistant authenticators such as passkeys/WebAuthn where supported, with higher assurance for admin/live-sensitive actions. Recovery is a governed security-critical flow, and sessions/tokens are scoped, bounded, revocable and revalidated after material identity/role/recovery changes.

## HCT-DEC-0096 — Workload, admin and support authorities are distinct, least-privileged identities
Status: APPROVED_FOR_DISCOVERY

Decision: services/workers use authenticated least-privileged workload principals distinct from human/CI identities. Admin authority uses a separate high-assurance, reason/scope/time-bounded privilege plane plus protected break-glass. Future support assumption preserves real actor plus assumed tenant identity, is read-only by default and may never silently impersonate or reveal secrets.

## HCT-DEC-0097 — Harness scope is tenant-aware and commercial entitlement never equals trading authorization
Status: APPROVED_FOR_DISCOVERY

Decision: Harness controls use exact typed tenant/account/capability scope and dependency/blast-radius analysis; global wildcard actions require stronger privilege. Commercial entitlement only states purchased feature availability and cannot grant admin, Safety/Risk bypass or trading authority. Billing changes preserve required close/protection/reconciliation of existing exposure.

## HCT-DEC-0098 — Multi-tenant resource scheduling preserves safety reserves before tenant workloads
Status: APPROVED_FOR_DISCOVERY

Decision: HCT enforces hierarchical platform/safety/tenant/account/workload quotas across exchange/API/WS, scanner, agents/models, replay, queues, storage/cache and compute. A noisy tenant is throttled/degraded locally before unrelated tenants lose protection/reconciliation capacity.

## HCT-DEC-0099 — Tenant-sensitive data, telemetry, audit, backup and offboarding have explicit lifecycle boundaries
Status: APPROVED_FOR_DISCOVERY

Decision: HCT classifies data sensitivity and defines encryption, observability, audit, retention/export and access rules. Backups preserve tenant/key isolation; offboarding safely handles open exposure, credential revocation, export, legal/audit retention and deletion from ordinary stores, caches and RAG/vector indexes without cross-tenant contamination.

## HCT-DEC-0100 — Production environments and software supply chain are isolated from development and tenant artifacts
Status: APPROVED_FOR_DISCOVERY

Decision: production/non-production identities, secrets and data are separated. CI/CD uses least-privileged protected deployment identities and secret/provenance/dependency controls; forks/untrusted jobs cannot inherit production secrets. User strategies/uploads remain tenant-scoped untrusted declarative artifacts and receive no arbitrary filesystem/network/process/SecretStore capability.

## HCT-DEC-0101 — Security incidents and disaster recovery are tenant-scoped and trading-aware
Status: APPROVED_FOR_DISCOVERY

Decision: incident/anomaly handling identifies exact tenant/account/principal/capability/secret/release blast radius, contains narrowly while preserving safe protection/reconciliation, and audits recovery. DR restores Identity, SecretStore, tenant data, Risk/OMS/reconciliation and audit integrity without tenant mixing, resuming new exposure only after restrictive recovery proof.

## HCT-DEC-0102 — Commercial account state cannot strand money-at-risk
Status: APPROVED_FOR_DISCOVERY

Decision: trial/paid/grace/past-due/cancelled/suspended/offboarding states have deterministic feature/entitlement behavior while preserving mandatory risk-reducing close, protection, reconciliation, export and safe offboarding actions for existing exposure.

## HCT-DEC-0103 — Commercial eligibility, external APIs and security assurance require explicit governed evidence
Status: APPROVED_FOR_DISCOVERY

Decision: region/exchange/KYC/API capability eligibility is server-side policy independent from locale/payment; required terms/privacy/risk agreements are versioned acceptance evidence subject to legal review. Future public APIs/webhooks/browser sessions require scoped tenant-bound security controls. Broad commercialization requires an adversarial multi-tenant security test matrix plus an auditable vulnerability/supply-chain lifecycle and penetration-test readiness.
