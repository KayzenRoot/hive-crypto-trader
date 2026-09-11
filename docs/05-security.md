# Security

Status: `DISCOVERY_IN_PROGRESS`
Active increment: `HCT-PLAN-0001-R08`
Risk class: `HIGH_ASSURANCE`

## Security objective
HCT is a multi-tenant trading platform that may hold exchange API credentials and initiate money-affecting actions. Security therefore requires explicit identity, tenant, account, secret and authority boundaries throughout the backend, not only authentication at the UI edge.

No secret, exchange credential, wallet seed, private key or production token may be committed to the repository or exposed to the browser, ordinary telemetry, support tooling or model/agent prompts.

## Canonical R08 security source set
- `docs/69-r08-multitenant-security-commercialization-gap-audit.md`
- `docs/70-r08-critical-tenant-security-architecture.md`
- `docs/71-r08-high-security-commercialization-hardening.md`
- `docs/72-r08-acceptance-criteria-and-review-gates.md`
- `docs/73-r08-multitenant-security-requirements-addendum.md`
- `docs/74-r08-decision-proposals.md` until R08 decision consolidation/final closure
- `docs/20-admin-control-plane-and-harness.md`
- approved R03–R07 authority/recovery/promotion contracts.

## Core security invariants
1. Every protected operation derives a server-authenticated `SecurityContext`; client tenant/resource IDs never prove authority.
2. Every tenant-owned resource/action receives server-side ownership/operation authorization.
3. Database, connection-pool, cache, queue/event, worker and private-stream boundaries are tenant-aware and adversarially tested.
4. Risk, Execution, OMS, protection and reconciliation bind to a canonical tenant–exchange-account–credential identity.
5. Raw exchange credentials exist only behind a backend SecretStore/Vault boundary with cryptographic key separation, least privilege, rotation/revocation and audit.
6. Raw secrets are `NEVER_LOG`, `NEVER_TRACE`, `NEVER_PROMPT`, `NEVER_EXPORT` through ordinary paths.
7. Human auth uses strong assurance with MFA/phishing-resistant methods where supported; dangerous actions require step-up.
8. Recovery/session revocation cannot be weaker than normal authentication.
9. Services/workers, humans, CI/CD, admin and support use distinct least-privileged identities.
10. Admin/support access is purpose/time/scope limited, strongly authenticated and permanently attributable to the real actor; silent impersonation is prohibited.
11. Harness controls are tenant/account/capability scoped and cannot spill across tenants unintentionally.
12. Commercial entitlement never equals trading/security authorization.
13. Per-tenant resource quotas preserve platform safety reserves and prevent noisy-neighbor starvation.
14. Tenant-sensitive observability, audit, backups, retention, offboarding and RAG/index deletion preserve isolation and confidentiality.
15. Production/non-production and CI/runtime trust boundaries are separated.
16. Incident response and DR are tenant-scoped and trading-aware, with restrictive recovery before new exposure resumes.
17. Commercial billing/eligibility changes cannot strand existing money-at-risk.
18. Broad commercialization requires adversarial multi-tenant testing, vulnerability/supply-chain lifecycle and external legal/compliance review where applicable.

## External guidance anchors
R08 planning is informed by current public guidance such as NIST SP 800-63-4 and OWASP multi-tenant/secrets-management guidance, but HCT-specific threat models and HIGH_ASSURANCE contracts remain authoritative for this product.

## Current authorization state
- implementation: `NOT_GRANTED`
- production secrets/credentials: `NOT_GRANTED`
- production deployment: `NOT_GRANTED`
- limited-live / real-money trading: `NOT_GRANTED`

R08 security planning cannot itself grant any of those authorities.