# HCT-PLAN-0001-R08 — HIGH Security & Commercialization Hardening

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R08`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

## Purpose
Close the 20 HIGH-severity gaps remaining after the R08 critical tenant-security architecture.

## 1. Tenant-Safe Observability
Telemetry is classified by sensitivity. Tenant/account/user IDs are represented by stable internal pseudonymous identifiers where human-readable data is unnecessary. Logs/traces/metrics exclude raw secrets and minimize PII/trading-sensitive payloads.

Cross-tenant dashboards authorize at query time, not merely ingestion time. High-cardinality tenant labels are bounded. Support/admin observability can summarize system impact without exposing another tenant's confidential strategy, positions or identifiers unnecessarily.

## 2. Append-Only Audit Boundary
Security/trading/admin audit events carry:
- actor/workload principal;
- tenant/account scope;
- real actor plus assumed identity for support sessions;
- action/resource;
- old/new state references;
- reason/incident/ticket where applicable;
- authentication assurance;
- timestamp/correlation;
- outcome/denial reason;
- integrity/version information.

Audit storage is access-controlled separately from ordinary application data and secret access. Retention/tamper-evidence requirements are explicit and provider-neutral.

## 3. Layered Abuse & Rate-Limit Controls
Abuse controls can operate by endpoint, IP/network, device/session, user, tenant, API credential and workload identity. They include credential-stuffing/login abuse, password/MFA/recovery abuse, enumeration, expensive-query/replay abuse and export attempts.

Limits fail locally whenever possible. An attack against one user/tenant must not consume another tenant's safety reserve. Security challenges/blocks are observable and appeal/recovery paths avoid permanent lockout from false positives.

## 4. Public API / Webhook Security Contract
Any future public API credential is tenant-bound, scoped, revocable, rotatable and separately identifiable from human sessions. High-risk endpoints require stronger scopes/assurance.

Outbound/inbound webhook design includes:
- signed messages with version/key ID;
- freshness/replay window and unique delivery ID;
- idempotent consumption;
- destination validation and SSRF/private-network protections;
- retry/backoff/dead-letter behavior;
- secret rotation;
- tenant-safe payload minimization.

## 5. Browser Security Boundary
Frontend remains an untrusted client. Planning requires:
- secure cookie/session attributes where cookie auth is used;
- CSRF defense for credentialed browser requests where applicable;
- restrictive, explicit CORS;
- clickjacking/frame protections;
- CSP and output-encoding/XSS controls;
- no exchange secret in browser storage;
- no client-only authorization/entitlement gate;
- sensitive action reauthentication performed/verified server-side.

## 6. Data Classification & Encryption Policy
Canonical classes:
`PUBLIC`, `INTERNAL`, `TENANT_CONFIDENTIAL`, `PII`, `TRADING_SENSITIVE`, `SECRET`, `AUDIT_SECURITY`.

Each class defines allowed stores, encryption, logging/telemetry treatment, retention, exportability and roles. TLS is mandatory across external and service boundaries. Encryption at rest is required for confidential classes; field/envelope encryption is used where database/storage compromise would otherwise expose high-value secrets.

## 7. Backup / Restore Isolation
Backup manifests identify environment, data classes, encryption/key dependencies, tenant range and schema/version. Restore procedures are tested for:
- whole environment recovery;
- selective tenant recovery where supported;
- no overwrite/mix with other tenants;
- revoked-secret/session state reconciliation;
- OMS/Risk/open-position consistency;
- audit continuity.

Backups containing encrypted secrets never include unprotected decryption keys in the same trust boundary.

## 8. Tenant Offboarding / Export / Deletion State Machine
Lifecycle:
`ACTIVE -> OFFBOARDING_REQUESTED -> TRADING_RESTRICTED -> EXPORT_READY? -> CREDENTIAL_REVOKE_SAFE -> RETENTION_WINDOW -> DELETION_EXECUTING -> CLOSED` with legal/audit hold variants.

Before credential deletion, HCT confirms open positions/orders/protection/reconciliation state and refuses to strand money-at-risk silently. User-exportable data and legally/operationally immutable evidence are classified separately. Completion evidence lists what was deleted, retained and why without leaking secret material.

## 9. Retention & Privacy Minimization
Each data family has documented purpose, owner, retention clock and deletion/aggregation policy. High-volume market telemetry and model/RAG memory are not retained indefinitely by default. Security/audit/trading evidence may have longer retention than user preferences/configuration.

RAG/index/vector deletion semantics are explicit so deleted tenant content does not remain retrievable from an orphaned embedding/index/cache.

## 10. Environment Isolation
Development, test, staging and production use separate environment identities, secrets and data boundaries. Production exchange credentials and customer PII are not copied into lower environments by default.

Fixtures/synthetic data are preferred. Any exceptional production-derived dataset is minimized/redacted, authorized, time-bounded, audited and stored under equivalent protection.

## 11. CI/CD & Software Supply-Chain Boundary
Build/release identity is separate from runtime/SecretStore access. Controls include:
- least-privileged short-lived CI credentials where supported;
- protected production deployment environments;
- secret scanning in commits/build output/artifacts;
- dependency/license/vulnerability checks;
- lockfile/provenance/SBOM expectations;
- signed/attested release identity where practical;
- reviewed workflow changes;
- fork/PR jobs cannot inherit production secrets;
- release actor and artifact provenance are auditable.

CI administrators do not automatically require raw tenant/exchange secret visibility.

## 12. Tenant-Safe Strategy / Artifact Sandbox
User-created strategy graphs/configuration/uploads are tenant-bound immutable versions. Inputs are treated as untrusted.

V1 arbitrary executable backend code remains prohibited. Parsers/compiler paths enforce size/depth/complexity limits, type/schema validation and resource quotas. File uploads receive type/size/content scanning and safe storage semantics. No artifact obtains arbitrary filesystem/network/process/SecretStore access.

## 13. Tenant-Scoped Incident Response
Security incidents create an `IncidentScope` with affected tenant/account/principal/capability/secret/release and confidence.

Response sequence:
`detect -> scope -> contain -> preserve safety -> revoke/quarantine -> reconcile -> eradicate -> recover -> verify -> postmortem`.

Containment is as narrow as safely possible. Credential compromise can trigger no-new-exposure for affected accounts while preserving safe reduce/protection/reconciliation paths if valid authority remains. Notifications reveal only relevant tenant information.

## 14. Security Anomaly Detection
Detect/report at minimum:
- tenant-context mismatch;
- repeated cross-tenant authorization denials;
- impossible ownership transitions;
- secret access outside expected workload;
- admin/support assumption anomalies;
- MFA/recovery/session anomalies;
- mass export/query behavior;
- sudden API credential invalidation/failures;
- privilege/role/entitlement escalation;
- unusual Harness/global control actions;
- audit/telemetry tampering symptoms.

Detection may tighten authority but must avoid automatically taking irreversible trading actions without approved Safety/Incident policy.

## 15. Tenant-Aware Disaster Recovery
DR proof includes Identity/Auth, SecretStore/KMS, DB, queues, cache/hot state where relevant, OMS/Risk/reconciliation state and audit evidence.

Recovery starts restrictive (`NO_NEW_EXPOSURE` / reconciliation modes as appropriate) until tenant/account exchange truth and credential availability are verified. No global resume merely because application health checks are green.

## 16. Commercial Account / Plan State Machine
Commercial state is explicit:
`TRIAL`, `ACTIVE_PAID`, `GRACE`, `PAST_DUE`, `CANCEL_PENDING`, `CANCELLED`, `SUSPENDED`, `OFFBOARDING`.

Entitlement changes define new optional actions/features but cannot orphan existing protected exposure. Past-due/cancelled state can block new trades/features according to policy while still allowing required close/protection/reconciliation/export/offboarding actions. Billing provider callbacks are untrusted until signature/idempotency/state-transition validation succeeds.

## 17. Regional / Exchange Eligibility Boundary
A tenant/account eligibility record stores current supported region/jurisdiction metadata, exchange availability, required KYC/API capability state and product restrictions where applicable.

Eligibility is a server-side policy input independent from locale, UI language, marketing page or successful payment. Unknown/incompatible eligibility blocks live activation rather than defaulting to allowed. Exact legal regional rules require current reviewed sources during commercialization/preflight.

## 18. Terms / Consent / Risk Disclosure Evidence
Required legal/commercial agreements are versioned documents with acceptance time, tenant/user identity, document version/hash and renewal/reacceptance policy for material changes.

Trading/security code consumes only acceptance/eligibility state, not free-form legal text. Legal wording and jurisdiction-specific obligations remain subject to professional/legal review before commercialization; the software architecture preserves evidence and gating.

## 19. Adversarial Multi-Tenant Security Test Matrix
Required future tests include:
- resource-ID mutation/BOLA across all tenant-owned APIs;
- DB/RLS bypass attempts;
- pooled-connection tenant bleed;
- cache-key collisions;
- queue/event forged tenant metadata;
- worker/exchange-account misbinding;
- websocket subscription cross-tenant leakage;
- export/report cross-tenant leakage;
- support/admin assumption boundaries;
- entitlement downgrade while positions are open;
- backup/restore/offboarding cross-tenant contamination;
- concurrent role/revocation races;
- property/fuzz tests asserting `tenant A action cannot mutate/read tenant B state`;
- secret-log/trace/artifact scanning.

## 20. Vulnerability & Security-Baseline Lifecycle
Security baseline includes dependency/container/code/IaC scanning as applicable, vulnerability inventory, severity/exploitability triage, remediation/mitigation SLA by risk, emergency-patch path with audit, regression testing and rollback/roll-forward.

Penetration-test readiness and SBOM/provenance evidence are planned before broad commercialization. A critical security defect can quarantine affected capability/tenant/release and trigger promotion validity re-evaluation under R07.

## HIGH gap closure map
- GAP-21: section 1
- GAP-22: section 2
- GAP-23: section 3
- GAP-24: section 4
- GAP-25: section 5
- GAP-26: section 6
- GAP-27: section 7
- GAP-28: section 8
- GAP-29: section 9
- GAP-30: section 10
- GAP-31: section 11
- GAP-32: section 12
- GAP-33: section 13
- GAP-34: section 14
- GAP-35: section 15
- GAP-36: section 16
- GAP-37: section 17
- GAP-38: section 18
- GAP-39: section 19
- GAP-40: section 20

## Result
All 40 initial R08 CRITICAL/HIGH gaps now have explicit planning-resolution contracts across docs 70–71. Requirements/decisions consolidation, objective acceptance gates and final audit remain required before R08 approval.