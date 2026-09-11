# HCT-PLAN-0001-R06 — Acceptance Criteria & Review Gates

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R06`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

## Purpose
Define objective gates required before R06 may receive `APPROVED`.

## Gate A — Evidence contract
All Brain inputs use a canonical versioned Evidence Envelope with provenance, temporal validity, generation, producer/version, uncertainty and lineage.

## Gate B — Admissibility
Unsupported, stale, contaminated, expired or critically untrusted evidence is deterministically rejected/quarantined before fusion.

## Gate C — Confidence semantics
Directional probability, opportunity quality, data confidence, calibration reliability, execution feasibility and risk compatibility remain distinct.

## Gate D — Calibration
Calibration has context hierarchy, sample sufficiency, drift/validity rules and conservative fallback including `CALIBRATION_UNTRUSTED`.

## Gate E — Selective decision
Abstention and no-trade states are first-class and near-tie/uncertain/expired decisions cannot be forced directional.

## Gate F — Evidence independence
Shared lineage/redundancy is measurable and consensus cannot double-count materially dependent evidence.

## Gate G — Uncertainty decomposition
Critical uncertainty dimensions remain visible and cannot disappear inside one average score.

## Gate H — Agent authority
Agents emit structured evidence under explicit authority ceilings; no agent has direct order/risk-limit authority.

## Gate I — Bounded deliberation
Agent reasoning has round/time/cost/tool/signal-life limits and deterministic termination.

## Gate J — Adversarial/stability controls
Governed adversarial triggers and bounded decision-stability testing exist for fragile/high-impact cases.

## Gate K — Point-in-time memory
Memory preserves event/knowledge/ingestion/correction/maturity times and market-state generation.

## Gate L — Leakage firewall
Historical replay/training cannot access future knowledge, later corrections or immature outcomes.

## Gate M — Temporal retrieval & analog sufficiency
Retrieval is regime/time/context aware and sparse/duplicate analog sets are explicitly insufficient.

## Gate N — Label maturity/no-trade learning
Outcome horizons mature explicitly and counterfactual no-trade learning never masquerades as actual execution.

## Gate O — Drift localization
Drift is localized before adaptation; retrain-everything behavior is prohibited.

## Gate P — Learning authority
Only bounded approved online statistics may adapt directly; material behavior requires governed promotion and no self-promotion.

## Gate Q — Forgetting/recurring regime control
Historical competence and recurring regimes are explicitly evaluated during adaptation.

## Gate R — Version pinning
Material model/prompt/agent/tool/skill/retriever/calibration/policy behavior is versioned and attributable per decision.

## Gate S — External-source contamination
Web/news evidence has provenance/reliability/timestamps/corroboration/expiry and cannot silently become canonical training truth.

## Gate T — Compute/freshness routing
Expensive intelligence is shortlist/value driven, bounded, cancellable and subordinate to signal lifetime.

## Gate U — Attribution/replay
Decision-to-outcome attribution and reproducible replay contracts distinguish deterministic and stochastic reproduction classes.

## Gate V — R05 coupling
Critical R05 data authority states deterministically constrain evidence admission and Brain outputs.

## Gate W — Brain/Risk separation
Brain confidence cannot raise hard risk/leverage or bypass Safety/Risk/Policy.

## Gate X — Fail-safe modes
Brain degradation states have explicit allowed outputs, fallbacks and recovery proof.

## Gate Y — Observability
Audit exposes structured evidence/provenance/calibration/uncertainty/disagreement/retrieval/version/reason codes without requiring private chain-of-thought.

## Gate Z — Promotion proof
Intelligence changes require incremental-value evidence through applicable point-in-time replay/OOS/paper/shadow/champion-challenger stages.

## Gate AA — Canonical consistency
Before approval, R06 decisions and requirements are consolidated, all 30 gaps map to accepted planning resolutions, Scope still forbids implementation/live authority, PR matches branch content and an objective final R06 audit exists.

## Verdict rule
- unresolved CRITICAL/HIGH planning defect => `CORRECTION REQUIRED`;
- missing authoritative dependency necessary for planning => `BLOCKED`;
- all gates pass => `APPROVED`.

R06 planning approval never authorizes implementation, production credentials or live trading.
