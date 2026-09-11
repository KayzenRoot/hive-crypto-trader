# HCT-PLAN-0001-R10 — Decision Proposals for Ledger Consolidation

Status: `CONSOLIDATED`
Increment: `HCT-PLAN-0001-R10`
Date: `2026-09-11`

`HCT-DEC-0118` through `HCT-DEC-0131` were accepted during R10 planning and are now consolidated into `docs/10-decisions-ledger.md`. This file remains as round-local provenance and must not compete with the canonical Decisions Ledger.

## HCT-DEC-0118 — Observability is a governed evidence plane, never authoritative trading truth
Status: APPROVED_FOR_DISCOVERY

Decision: HCT telemetry uses a versioned observability context envelope and explicitly classifies authoritative facts, reconciled projections, observations, derived metrics and estimates. Logs/metrics/traces can explain exchange/OMS/Risk state but cannot replace it or relax authority.

## HCT-DEC-0119 — Trading decisions and outcomes require end-to-end causal/time lineage
Status: APPROVED_FOR_DISCOVERY

Decision: HCT maintains causal correlation from market state through Brain, Safety/Risk, Risk Reservation, execution, exchange evidence, OMS, protection and reconciliation while preserving immutable domain IDs. Event/receive/processing/monotonic time and clock health remain explicit to prevent false latency or causality claims.

## HCT-DEC-0120 — Telemetry is secret-safe and tenant-safe by construction
Status: APPROVED_FOR_DISCOVERY

Decision: observability uses structured allowlisted/redacted fields; raw credentials, signing material, tokens and prohibited sensitive context are never normal telemetry. Query/search/export/admin/support access inherits R08 tenant/account/environment isolation and least privilege.

## HCT-DEC-0121 — High-value audit is append-only, attributable and tamper-evident
Status: APPROVED_FOR_DISCOVERY

Decision: HCT maintains append-only audit events covering auth/privilege/secrets/Safety/Risk/execution/OMS/reconciliation/promotion/release/commercial/incident actions. Corrections append superseding evidence; high-value evidence supports appropriate hash-chain/signature/WORM-style tamper-evidence according to deployment capability.

## HCT-DEC-0122 — SLOs prioritize safety, correctness, freshness and reconciliation over raw uptime
Status: APPROVED_FOR_DISCOVERY

Decision: HCT defines trading-aware SLO/SLI families and accepts safe restriction/refusal of new exposure as correct behavior. Critical SLO burn may tighten authority only through governed deterministic policy; stronger authority resumes only after underlying domain recovery proof.

## HCT-DEC-0123 — Protection and reconciliation are measurable operational contracts
Status: APPROVED_FOR_DISCOVERY

Decision: protection establishment/verification, protected quantity, private-state freshness, reconciliation coverage/conflict age, uncertain-order age and recovery convergence are first-class SLIs with policy/versioned targets finalized through implementation benchmarks.

## HCT-DEC-0124 — Incident severity and response are trading-aware
Status: APPROVED_FOR_DISCOVERY

Decision: incident severity considers money-at-risk, state certainty, tenant/security blast radius, protection/reduction capability and recoverability. Canonical response progresses through detection, containment, safe operating mode, evidence preservation, reconciliation, remediation, verification and progressive restore.

## HCT-DEC-0125 — Incident automation is bounded and recovery requires objective proof
Status: APPROVED_FOR_DISCOVERY

Decision: detection automation may page/enrich and execute only pre-approved bounded containment through Harness/Safety/security controls; it never gains arbitrary trading authority. Material incidents preserve evidence bundles, and stronger trading authority returns only after explicit recovery gates pass.

## HCT-DEC-0126 — Compliance readiness is evidence mapping, not an unsupported compliance claim
Status: APPROVED_FOR_DISCOVERY

Decision: HCT maintains a versioned Control Evidence Map with internal controls, owners, evidence, retention and applicability plus external-framework mappings where useful. Jurisdiction/product applicability is versioned and legally reviewed as needed; framework alignment alone does not constitute certification or legal compliance.

## HCT-DEC-0127 — FinOps is subordinate to capital safety, security and evidence durability
Status: APPROVED_FOR_DISCOVERY

Decision: cost controls may suppress research/optional workloads first but may not silently disable minimum Safety/Risk/protection/reconciliation/security/audit/incident evidence. P0/P1 safety capacity is protected from budget optimization.

## HCT-DEC-0128 — Telemetry cardinality, sampling, retention and pipeline degradation are governed resources
Status: APPROVED_FOR_DISCOVERY

Decision: HCT budgets telemetry cardinality, preserves mandatory/tail/security/trading evidence under sampling, uses evidence-class retention and exposes observability-pipeline degradation. If mandatory evidence durability is at risk beyond policy, new exposure may be restricted without making remote observability a synchronous hot-path dependency.

## HCT-DEC-0129 — Alerting, runbooks, on-call and postmortems are lifecycle-managed operational artifacts
Status: APPROVED_FOR_DISCOVERY

Decision: actionable alerts have owners/severity/dedup/runbooks/escalation; runbooks are versioned and authority-bounded; bootstrap owner-only response still has explicit paging/escalation; material incidents produce evidence-driven reviews and tracked corrective/regression actions.

## HCT-DEC-0130 — FinOps uses provider-neutral cost truth, allocation and bounded AI/research budgets
Status: APPROVED_FOR_DISCOVERY

Decision: HCT distinguishes realtime estimates, provider-reported usage, statements, invoices and corrections; allocates costs by relevant provider/environment/tenant/capability/model/experiment dimensions where feasible; budgets AI/agent/retrieval/replay workloads; and uses FOCUS-compatible normalization where source billing data supports it.

## HCT-DEC-0131 — Infrastructure migration is driven by measured reliability, capacity and unit economics
Status: APPROVED_FOR_DISCOVERY

Decision: HCT tracks cost/headroom/latency per relevant tenant/account/capability/workload and uses observed reliability/security/capacity economics rather than customer count alone to trigger infrastructure upgrades. Operational dashboards preserve a truth hierarchy so forecasts/cost scores never masquerade as authoritative facts.
