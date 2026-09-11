# HCT-PLAN-0001-R10 — Acceptance Criteria & Review Gates

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R10`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

## Gate A — Observability non-authority
Telemetry can explain authoritative state but cannot replace exchange/OMS/reconciliation/Risk/Security truth.

## Gate B — Canonical observability context
Logs/metrics/traces/events have a versioned context envelope for service/environment/release, tenant/account scope where permitted, correlations, generations, time semantics, authority and classification.

## Gate C — End-to-end causal trace
Market-to-decision-to-Risk-to-Execution-to-exchange-to-OMS/protection/reconciliation lineage is traceable without collapsing immutable domain IDs.

## Gate D — Time integrity
Event/receive/processing/wall/monotonic semantics and clock health prevent false causal/latency claims.

## Gate E — Telemetry data firewall
Secrets/tokens/signing material/prohibited sensitive data are structurally excluded/redacted before logging/export.

## Gate F — Tenant-safe observability
Query/search/export/admin/support telemetry paths preserve tenant/account/environment isolation and least privilege.

## Gate G — Tamper-evident audit
Audit is append-only with actor/scope/reason/evidence/version identity and correction-by-superseding-event; high-value evidence supports tamper-evidence mechanisms.

## Gate H — Audit taxonomy
Authentication, privilege, secret lifecycle, Safety/Risk, execution, OMS/reconciliation, promotion, release, entitlement and incident event families are covered.

## Gate I — Trading-aware SLO hierarchy
Safety/correctness/freshness/protection/reconciliation SLOs are separate from generic API/UI availability.

## Gate J — Correctness over availability
Safe refusal/degradation can count as correct operation and uptime incentives cannot bypass hard gates.

## Gate K — Error-budget authority coupling
Critical SLO burn may tighten authority through governed policy, but telemetry cannot relax authority and recovery requires domain proof.

## Gate L — Protection/reconciliation SLIs
Coverage, verification latency, watermarks/conflict age, uncertain-order age and restart/failover convergence are measurable.

## Gate M — Trading-aware incident severity
Severity is based on money-at-risk, state certainty, tenant/security blast radius, protection/reduction ability and recoverability.

## Gate N — Incident state machine
Detection through progressive restore/review preserves capital protection, truth establishment and evidence.

## Gate O — Automated containment boundary
Automation may execute only pre-approved bounded containment and never gains generic arbitrary trading authority.

## Gate P — Incident evidence preservation
Material incidents produce immutable evidence bundles before cleanup destroys required proof.

## Gate Q — Security incident coupling
Credential/session/cross-tenant/supply-chain/security events integrate secret/session revocation, containment and trading-safe recovery.

## Gate R — Recovery proof
New exposure does not resume after material incidents/failover until defined identity/data/account/protection/risk/evidence conditions pass.

## Gate S — Compliance evidence map
Controls/evidence/owners/retention/applicability are mapped without claiming certification or legal compliance unsupported by independent/legal review.

## Gate T — FinOps safety boundary
Cost controls cannot disable mandatory Safety/Risk/protection/reconciliation/security/audit/evidence below required minimum.

## Gate U — Trading golden signals
Operational views include domain signals beyond generic RED/USE metrics.

## Gate V — SLI mathematical definition
Each SLI has population, numerator/denominator, windows, exclusions, aggregation, source quality and missing-data semantics.

## Gate W — Cardinality and sampling
Telemetry attribute cardinality is budgeted; sampling preserves mandatory/security/trading/tail evidence and sampled absence is not proof of nonoccurrence.

## Gate X — Retention/evidence classes
Telemetry retention prioritizes money/security/audit evidence over high-volume low-value diagnostics with explicit classes.

## Gate Y — Telemetry-pipeline degradation
Collector/export/storage failure has explicit states; hot safety survives but mandatory-evidence risk can restrict authority.

## Gate Z — Observability-of-observability
Dropped signals, buffers, exporter lag, schema rejection, sampling, storage capacity and mandatory-evidence durability are themselves monitored.

## Gate AA — Alert/runbook/on-call lifecycle
Alerts have owner/severity/dedup/runbook/escalation and runbooks are versioned, authority-bounded and restoration-aware; bootstrap on-call is explicit.

## Gate AB — Post-incident/release/model observability
Postmortems, release/config markers and model/agent latency/cost/failure/calibration observability are governed without leaking prohibited data.

## Gate AC — Retention/deletion/export governance
Offboarding/deletion, audit/security retention, legal hold concepts and evidence export use classified/scoped/authorized rules subject to legal review.

## Gate AD — FinOps allocation/budgets
Cost allocation, anomaly/forecast guardrails and AI/agent/research budgets preserve P0/P1 safety capacity.

## Gate AE — Cost data truth and normalization
Realtime estimate, provider usage, billing statement, invoice and correction are distinct; provider-neutral/FOCUS-aligned normalization is used where applicable.

## Gate AF — Unit economics/capacity triggers
Costs/headroom/latency per relevant tenant/account/capability/experiment drive migration decisions more than customer count alone.

## Gate AG — Compliance applicability drift
Jurisdiction/product/framework assumptions are versioned, owned and periodically reviewed; locale/payment never silently grants eligibility.

## Gate AH — Audit access governance
Sensitive audit/telemetry access and exports are least-privilege, purpose-limited and attributable to the real actor.

## Gate AI — Dashboard truth hierarchy
Authoritative facts, reconciled projections, telemetry, derived metrics, forecasts/scores and unknown data remain visually/semantically distinct.

## Gate AJ — Canonical consistency
R10 decisions/requirements, test/benchmark direction, Scope and branch/PR state agree; no implementation/deployment/live authorization is introduced and an objective final audit exists.

## Verdict rule
- unresolved CRITICAL/HIGH R10 planning defect => `CORRECTION REQUIRED`;
- missing authoritative dependency necessary for safe planning => `BLOCKED`;
- all gates pass => `APPROVED`.

R10 approval never authorizes implementation, production credentials, production deployment, limited-live activation or real-money trading.
