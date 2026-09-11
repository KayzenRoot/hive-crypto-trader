# HCT-PLAN-0001-R10 — Observability, Audit, Incident & FinOps Requirements Addendum

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R10`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

This addendum is canonical together with `docs/02-requirements.md` until planning-freeze consolidation.

## R10-REQ-001 — Observability non-authority
Telemetry SHALL NOT replace exchange, OMS, reconciliation, Security, Safety or Risk truth. Derived/estimated data SHALL be identified as such.

## R10-REQ-002 — Observability context envelope
High-assurance logs/metrics/traces/events SHALL carry applicable versioned service/environment/release, tenant/account scope, correlation, generation, time, authority and classification context.

## R10-REQ-003 — Causal trading lineage
HCT SHALL support traceable lineage from market evidence/candidate decision through Safety/Risk, Risk Reservation, execution, exchange evidence, OMS, protection, reconciliation and outcome/audit.

## R10-REQ-004 — Time integrity
Observability SHALL distinguish event/exchange, receive/knowledge, processing and persisted time and use monotonic elapsed timing where appropriate. Clock health SHALL be explicit.

## R10-REQ-005 — Telemetry data firewall
Raw secrets, signing material, session/recovery tokens and prohibited sensitive data SHALL be excluded/redacted before telemetry emission/export using structured field policies.

## R10-REQ-006 — Tenant-safe observability
Telemetry query/search/export and privileged access SHALL enforce R08 tenant/account/environment isolation, purpose limitation and least privilege.

## R10-REQ-007 — Append-only audit
Security/trading/admin audit SHALL be logically append-only, attributable and correction-safe; material audit evidence SHALL support tamper-evidence appropriate to deployment capability.

## R10-REQ-008 — Audit event taxonomy
Audit SHALL cover authentication/session/recovery, privilege, secrets, Safety/Harness, Risk, execution/OMS/reconciliation/protection, promotion/model lifecycle, release/config, entitlement/commercial and incident events.

## R10-REQ-009 — Trading-aware SLOs
HCT SHALL define SLO/SLI families for data freshness/coherency, account-state freshness, protection, reconciliation, uncertain outcomes, decision/execution latency, audit durability and general service availability.

## R10-REQ-010 — Correctness over availability
Safe refusal/restriction of new exposure SHALL be considered valid operation where required. Availability objectives SHALL NOT incentivize bypassing hard safety/risk/data gates.

## R10-REQ-011 — Error-budget policy
Critical SLO violations/burn MAY tighten authority only through governed deterministic policy. Telemetry SHALL NOT relax authority, and restoring stronger authority SHALL require underlying domain recovery proof.

## R10-REQ-012 — Protection/reconciliation SLIs
HCT SHALL measure protection establishment/verification, protected quantity, private-state age, reconciliation watermark/conflict age, uncertain-order duration and recovery convergence.

## R10-REQ-013 — Incident severity
Incident severity SHALL account for money-at-risk, state certainty, protection/reduction capability, tenant/security blast radius and recoverability/time sensitivity.

## R10-REQ-014 — Incident response state machine
Material incident response SHALL support Detect, Triage, Classify, Contain, Safe Operating Mode, Preserve Evidence, Reconcile, Remediate, Verify, Progressive Restore, Review and Close semantics.

## R10-REQ-015 — Bounded automated containment
Observability/detection automation SHALL NOT receive generic exchange-order authority. Only pre-approved bounded Harness/Safety/security containment may be automated.

## R10-REQ-016 — Incident evidence bundle
Material incidents SHALL preserve immutable timelines, affected identities/versions/state generations, actions, exchange/OMS/reconciliation references, telemetry gaps and recovery proof.

## R10-REQ-017 — Security incident integration
Credential/session/cross-tenant/privilege/SecretStore/supply-chain security incidents SHALL integrate with tenant/account-scoped trading-safe containment and recovery.

## R10-REQ-018 — Recovery proof
After material incidents/restart/failover/control-plane outage, stronger trading authority SHALL not resume until required identity, market/account state, reservations, protection, exchange capability and evidence conditions are proven.

## R10-REQ-019 — Compliance evidence map
HCT SHALL maintain a versioned Control Evidence Map for internal requirements, owners, artifacts, retention, applicability and mapped external references where useful. It SHALL NOT claim legal compliance/certification without required external/legal process.

## R10-REQ-020 — FinOps safety boundary
Cost controls SHALL NOT disable required Safety/Risk/protection/reconciliation/security/audit/incident evidence below the approved minimum.

## R10-REQ-021 — Trading golden signals
Operational dashboards SHALL include authority state, freshness, reconciliation lag, protection coverage, uncertain-order/risk-reservation age, decision freshness, quota pressure, exchange health and evidence-pipeline health where applicable.

## R10-REQ-022 — Explicit SLI math
Each production SLI SHALL define eligible population, numerator/denominator, windows, exclusions, aggregation, source quality and missing-data semantics.

## R10-REQ-023 — Cardinality budget
Telemetry dimensions SHALL have bounded cardinality policies. Unbounded identifiers SHALL use secure trace/log/audit lookup rather than uncontrolled global metric labels.

## R10-REQ-024 — Sampling policy
Sampling SHALL preserve mandatory security/trading/incident/tail evidence according to policy; sampled absence SHALL never prove an event did not occur.

## R10-REQ-025 — Retention classes
Telemetry/evidence SHALL have explicit retention classes prioritizing trading/security/audit evidence over high-volume low-value diagnostics. Exact durations require later legal/business/storage review.

## R10-REQ-026 — Telemetry degradation states
Collector/export/storage degradation SHALL be explicit. Hot safety paths SHALL remain isolated from remote observability dependencies, while mandatory-evidence durability failure may restrict new exposure.

## R10-REQ-027 — Observe the observability plane
HCT SHALL observe dropped signals, buffers, exporter failures, ingest lag, schema rejection, clock skew, sampling policy, storage capacity and mandatory-evidence durability.

## R10-REQ-028 — Alert lifecycle
Actionable alerts SHALL have rule/version, owner, severity, scope, evidence, dedup/grouping, runbook, escalation, inhibit/suppress and resolution/expiry semantics.

## R10-REQ-029 — Runbook lifecycle
Runbooks SHALL be versioned, authority-bounded, safety-aware and include diagnosis, allowed/forbidden actions, evidence, rollback/roll-forward and restore verification.

## R10-REQ-030 — On-call/escalation
HCT SHALL define a bootstrap-compatible responder/paging/escalation model and preserve SEV0/SEV1 notification regardless of normal quiet-hour preferences.

## R10-REQ-031 — Post-incident review
Material incidents SHALL produce evidence-driven reviews and tracked corrective actions/regression obligations.

## R10-REQ-032 — Release/config observability
Runtime evidence SHALL correlate to build/release, config/policy, feature/capability, schema/migration and rollback events.

## R10-REQ-033 — Model/agent observability
Model/agent/tool/retrieval observability SHALL capture allowed version, latency, cost, failure, calibration/abstention and drift signals without exposing prohibited prompts/secrets/private reasoning.

## R10-REQ-034 — Retention/deletion/legal-hold governance
Retention and tenant deletion/offboarding SHALL be reconciled by explicit data classes and jurisdiction-specific legal review; legal hold SHALL be explicit/scoped/audited if applicable.

## R10-REQ-035 — Evidence export
Audit/incident/assurance exports SHALL be scoped, integrity-manifested, redacted/classified, authorized and tenant-safe.

## R10-REQ-036 — Cost allocation
Costs SHOULD be attributable, where feasible, by provider/service/environment/platform/tenant/account/capability/model/research workload with documented shared-cost allocation.

## R10-REQ-037 — Budget/anomaly guardrails
HCT SHALL monitor actual/forecast spend and quotas and MAY automatically suppress nonessential workloads before exhaustion, preserving safety/security/evidence priorities.

## R10-REQ-038 — AI/agent/research budgets
Inference, agent/tool, retrieval, replay/research and storage/egress workloads SHALL have explicit budgets/telemetry appropriate to bootstrap and commercial phases.

## R10-REQ-039 — Provider-neutral billing normalization
HCT SHALL maintain an internal provider-neutral cost model and SHOULD use FOCUS-compatible normalization where source provider data makes it appropriate.

## R10-REQ-040 — Unit economics and migration triggers
HCT SHALL measure relevant cost/headroom/latency unit economics and use measured reliability/security/capacity economics, not customer count alone, to trigger infrastructure migration.

## R10-REQ-041 — Cost truth classes
Estimated cost, provider usage, billing statement, invoiced cost and corrections SHALL remain semantically distinct and reconcilable.

## R10-REQ-042 — Compliance applicability drift
Jurisdiction/product/customer/exchange/framework applicability assumptions SHALL be versioned, owned, reviewed and never inferred solely from locale/payment.

## R10-REQ-043 — Audit access governance
Sensitive audit/incident telemetry access/export SHALL be least-privilege, purpose-limited, scoped and attributable to the real actor/workload.

## R10-REQ-044 — Dashboard truth hierarchy
Operational dashboards SHALL distinguish authoritative facts, reconciled projections, telemetry observations, derived SLO/metrics, forecasts/scores and unavailable/unknown data.

## R10-REQ-045 — External reference posture
OpenTelemetry, NIST CSF 2.0 / SP 800-61r3 and FOCUS may guide interoperability/process/cost normalization. HCT SHALL version external dependencies and SHALL NOT treat framework alignment as certification/compliance by itself.

## Scope invariant
These requirements are planning contracts. They do not authorize implementation, production deployment/topology, credentials, limited-live activation or real-money trading.
