# HCT-PLAN-0001-R10 — Observability, Audit, Incident Response, Compliance-Readiness & FinOps Gap Audit

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R10`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`
Initial verdict: `CORRECTION REQUIRED`

## Objective
Audit whether HCT can detect, explain, contain, recover from and economically understand failures across a multi-tenant automated trading platform without leaking secrets or mistaking telemetry for authoritative exchange truth.

R10 treats observability as an evidence system, not merely logs and dashboards.

Primary pre-discovery inputs:
- R03 Risk/Survival/Protection contracts;
- R04 Execution/OMS/Reconciliation contracts;
- R05 realtime/data authority and freshness contracts;
- R06 Brain/evidence/version attribution contracts;
- R07 promotion/replay evidence contracts;
- R08 SecurityContext/tenant/secrets/incident boundaries;
- R09 UI-state/client observability contracts;
- `docs/06-test-benchmark-plan.md`;
- `docs/07-deployment.md`;
- `docs/20-admin-control-plane-and-harness.md`;
- `docs/32-bootstrap-free-infrastructure-and-scale-migration.md`.

Current external reference baseline includes OpenTelemetry semantic conventions for traces/metrics/logs/resources, NIST CSF 2.0, NIST SP 800-61r3 incident-response guidance and FOCUS 1.4 for vendor-neutral cost/billing normalization. HCT-specific HIGH_ASSURANCE contracts remain authoritative.

## CRITICAL gaps

### GAP-R10-01 — Canonical Observability Envelope
No formal cross-signal envelope yet binds tenant/account/environment/service/version/generation/correlation/authority/time semantics across logs, metrics, traces and events.

### GAP-R10-02 — Telemetry is not trading truth
Need a hard boundary preventing metrics/logs/traces from becoming authoritative order/position/balance/protection state when exchange/OMS/reconciliation evidence disagrees.

### GAP-R10-03 — End-to-end transaction correlation
Need one causally traceable lineage from market event/opportunity through Brain, Safety/Risk, Risk Reservation, Execution Command, exchange evidence, OMS, protection and reconciliation.

### GAP-R10-04 — Time integrity across telemetry
Need explicit event time, receive time, processing time, monotonic duration and clock-health handling so traces do not fabricate order causality.

### GAP-R10-05 — Secret/PII/tenant data telemetry firewall
Need field-level classification/redaction preventing credentials, signing material, session tokens, sensitive tenant payloads and prohibited model/support data from entering telemetry.

### GAP-R10-06 — Tenant-safe observability isolation
Need tenant/account scoping for metrics/logs/traces/search/export and admin/support access so observability itself cannot become a cross-tenant leak.

### GAP-R10-07 — Audit-log immutability/tamper evidence
Need append-only audit semantics, cryptographic/hash-chain or equivalent tamper evidence where warranted, actor/source attribution and controlled corrections rather than editable history.

### GAP-R10-08 — Audit event taxonomy
Need canonical event families for auth, admin, Safety/Risk, execution, OMS, reconciliation, secret lifecycle, strategy/model promotion, Harness, billing and support assumption.

### GAP-R10-09 — Trading-aware SLO hierarchy
Need SLOs for safety/correctness/freshness/reconciliation/protection/execution, not only generic API uptime.

### GAP-R10-10 — Availability must not outrank correctness
Need explicit rule that a system may intentionally refuse new exposure while still meeting safety goals; “always available” is not the objective.

### GAP-R10-11 — Error-budget policy tied to trading authority
Need deterministic mapping from SLO burn/critical violations to degraded/no-new-exposure/reduce/reconciliation-only/emergency behavior where appropriate.

### GAP-R10-12 — Protection/Reconciliation SLOs
Need measurable deadlines and confidence for protective coverage establishment, private-state convergence, restart/failover recovery and unresolved exchange uncertainty.

### GAP-R10-13 — Incident severity model
Need severity based on money-at-risk, tenant blast radius, state certainty, secret compromise, trading authority and recoverability rather than generic HTTP error counts.

### GAP-R10-14 — Trading-aware incident response state machine
Need detection → containment → safe-operation mode → reconciliation → remediation → proof → progressive restore, preserving risk reduction/protection.

### GAP-R10-15 — Automated incident controls authority
Need clear distinction between telemetry-triggered recommendation and deterministic Harness/Safety action, with bounded auto-containment and no observability service gaining arbitrary trade authority.

### GAP-R10-16 — Incident evidence preservation
Need immutable incident timeline, affected versions/configs/state generations, commands, exchange evidence and forensic artifacts before cleanup destroys proof.

### GAP-R10-17 — Security incident integration
Need security incidents (credential compromise, auth anomaly, cross-tenant access, supply-chain event) integrated with trading-aware containment and secret/session revocation.

### GAP-R10-18 — Recovery proof / restore gates
Need objective gates before restoring new exposure after incidents, deploy rollback, dependency recovery or observability/control-plane outage.

### GAP-R10-19 — Compliance evidence map
Need a framework mapping requirements/controls/evidence/owners/retention without falsely claiming regulatory certification or legal compliance.

### GAP-R10-20 — FinOps safety boundary
Need hard rule that cost-saving automation cannot disable required audit, protection, reconciliation, security or minimum evidence retention.

## HIGH gaps

### GAP-R10-21 — RED metrics alone are insufficient
Need domain-specific trading golden signals: authority state, data age, reconciliation lag, protection coverage, uncertain orders, risk-reservation backlog, decision age, quota pressure and exchange health.

### GAP-R10-22 — SLI definitions and aggregation
Need precise numerator/denominator/window/scope rules so SLOs cannot be gamed by averaging tenants, symbols or quiet periods.

### GAP-R10-23 — Cardinality control
Need bounded labels/attributes for symbols, tenant IDs, order IDs, traces and agent/model metadata to avoid cost/resource explosions.

### GAP-R10-24 — Sampling policy
Need tail/error/security/trading-event-aware sampling so rare critical events are not sampled away while high-volume low-value telemetry is bounded.

### GAP-R10-25 — Log/trace/metric retention tiers
Need retention by evidence class, incident/legal/security/trading importance and bootstrap storage constraints.

### GAP-R10-26 — Telemetry pipeline degradation
Need explicit state when collectors/exporters/storage fail; local safety path must survive, but inability to preserve mandatory evidence can restrict new exposure.

### GAP-R10-27 — Observability of observability
Need health for collectors, dropped spans/logs/metrics, queue depth, exporter lag, schema/version mismatch and retention failures.

### GAP-R10-28 — Alert quality and ownership
Need alert owner, severity, dedup/grouping, actionable runbook, inhibition/suppression and stale-alert cleanup to prevent alarm fatigue.

### GAP-R10-29 — Runbook lifecycle
Need versioned runbooks tied to capability/incident types, preconditions, safe commands, rollback and verification.

### GAP-R10-30 — On-call/escalation model
Need a bootstrap-compatible escalation policy even for owner-only operation, plus future multi-role readiness.

### GAP-R10-31 — Post-incident review
Need blameless but evidence-driven postmortem, root/contributing factors, control gaps, regression tests and tracked corrective actions.

### GAP-R10-32 — Release/deploy observability
Need release/version markers, feature/capability changes, deployment health and rollback correlation in telemetry.

### GAP-R10-33 — Model/agent observability
Need latency/cost/failure/model-version/tool/skill/calibration/drift/abstention metrics without logging prompts/secrets prohibited by R08.

### GAP-R10-34 — Compliance data retention/deletion conflict
Need retention policy reconciling audit/security requirements with tenant offboarding/deletion and legal-hold concepts, subject to jurisdiction-specific legal review.

### GAP-R10-35 — Evidence export / audit package
Need reproducible evidence bundles for internal audit, incident review and future external assurance without exporting secrets/cross-tenant data.

### GAP-R10-36 — Cost allocation model
Need per-platform/tenant/account/capability/workload/model/replay cost attribution where technically feasible.

### GAP-R10-37 — Cost anomaly/budget guardrails
Need forecast/burn alerts and automated suppression of nonessential workloads before spend/quota exhaustion, preserving P0/P1 safety workloads.

### GAP-R10-38 — AI/agent/research cost budgets
Need explicit inference/tool/retrieval/replay cost budgets and value/cost telemetry so agents/research cannot consume unlimited spend.

### GAP-R10-39 — Provider billing normalization
Need provider-neutral cost schema; FOCUS-compatible normalization may be used where source billing data supports it.

### GAP-R10-40 — Unit economics and capacity trigger
Need cost per active tenant, cost per protected/live account, cost per decision/trade/replay and infrastructure migration triggers tied to measured capacity/reliability rather than customer count alone.

### GAP-R10-41 — Cost data trust and reconciliation
Need distinguish estimated realtime cost, provider-reported usage and invoiced/billed cost with correction/reconciliation semantics.

### GAP-R10-42 — Compliance scope/version drift
Need versioned jurisdiction/product-feature applicability and periodic review so an old legal/compliance assumption does not silently remain current.

### GAP-R10-43 — Audit access governance
Need least-privilege access to sensitive audit/incident telemetry, purpose limitation, support/admin logging and export approval where appropriate.

### GAP-R10-44 — Dashboard truth hierarchy
Operational dashboards must distinguish authoritative operational facts from telemetry-derived estimates, forecasts, scores and missing data.

## Initial assessment
HCT has strong domain evidence contracts in R03–R09, but the cross-cutting observability/audit/incident/FinOps layer is not yet formalized. `docs/06-test-benchmark-plan.md` remains bootstrap-level and `docs/07-deployment.md` is intentionally undeclared. R10 must therefore define operational evidence contracts without prematurely choosing production deployment topology.

## Verdict rule
Any unresolved CRITICAL/HIGH R10 planning defect keeps `CORRECTION REQUIRED`. Missing authoritative dependency necessary to plan safely yields `BLOCKED`. R10 approval never authorizes implementation, production credentials/deployment or live trading.
