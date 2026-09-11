# HCT-PLAN-0001-R07 — Validation Laboratory HIGH Hardening

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R07`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

## Purpose
Close the 17 HIGH-severity gaps remaining after the R07 critical architecture.

## 1. Statistical + economic significance
Promotion evidence SHALL report uncertainty intervals appropriate to the metric and data-generating process, not only point estimates. Component-specific gates distinguish statistical detectability from economically meaningful improvement after costs, risk, latency and operational complexity.

A tiny statistically detectable benefit may fail promotion if it is operationally irrelevant; a large but highly uncertain benefit may remain research-only.

## 2. Effective Sample Independence
Each Promotion Evidence Bundle reports both raw observations and an effective independent evidence estimate considering:
- same-event clusters;
- highly correlated symbols;
- duplicated/overlapping windows;
- regime concentration;
- repeated parameter variants;
- common upstream features/data.

Promotion thresholds use effective evidence rather than raw trade count where dependence is material.

## 3. Regime and OOD Coverage Matrix
Each candidate declares which regimes/conditions are validated, weakly covered, absent or explicitly out of scope across trend/range, volatility, liquidity, event/news, breadth, symbol cluster and execution quality.

Promotion may be scoped to validated conditions. OOD/unknown regime behavior must have a conservative fallback rather than extrapolated confidence.

## 4. Search Budget + Nested Validation + Parameter Robustness
Parameter/model search receives an explicit budget and search-space manifest. Selection happens inside training/validation folds while final holdouts remain untouched.

Robustness evidence includes plateau/neighborhood behavior, parameter sensitivity, cost sensitivity and regime sensitivity. A needle-like optimum receives a fragility penalty or fails promotion.

## 5. Empirical Execution-Model Calibration
Fee, funding, latency, spread, slippage, fill/no-fill and cancellation models are periodically compared against paper/shadow and later limited-live observations where available.

Each model stores:
- calibration dataset/window;
- empirical distribution/error;
- confidence class;
- age/validity;
- conservative fallback when evidence is weak.

## 6. Degraded/Missing Data Policy
Every experiment interval has fidelity classification:
`FULL_FIDELITY`, `DEGRADED_BUT_USABLE`, `RESEARCH_ONLY`, `INVALID_FOR_PROMOTION`.

Imputation, coalescing, interpolation or synthetic repair must be tagged with method/version and cannot silently become historical truth. Promotion metrics disclose exposure to degraded intervals.

## 7. Synthetic Crisis Governance
Synthetic scenarios preserve generator/version/seed, assumptions, targeted failure mode, severity and expected invariants. Historical and synthetic evidence are reported separately.

Synthetic crisis success proves safety/resilience behavior only. It does not prove historical profitability or market-frequency estimates.

## 8. Monte Carlo / Resampling Validity
Resampling methods must document assumptions and preserve material temporal dependence, clustering, regime/path dependence and portfolio interactions where relevant.

Naive IID permutation is prohibited when it destroys the mechanism being measured. Monte Carlo output is sensitivity/tail evidence, never a confidence-manufacturing substitute for real OOS data.

## 9. Portfolio / Multi-Strategy Replay
Portfolio promotion tests simultaneous strategies and signals under shared constraints:
- capital/equity;
- Risk Reservation Ledger;
- common-factor/correlation exposure;
- cross margin/collateral;
- concurrent API/execution quota;
- conflicting orders;
- shared liquidity/market impact;
- compute/backpressure contention.

A strategy may pass stand-alone tests yet fail portfolio eligibility.

## 10. Decision Twin / Ablation Control
Paired experiments use the same admissible point-in-time evidence and change only the declared component under study where feasible.

Reports identify confounders, stochasticity and reproduction class. Results are described as causal only when experiment design supports causal interpretation; otherwise they are comparative evidence.

## 11. Shadow Divergence Monitor
Candidate and Champion are aligned over shared live input windows and compared across:
- decision distribution;
- abstention rate;
- calibration;
- latency;
- proposed/executed simulated tactics;
- expected fill quality;
- Safety/Risk outcomes;
- protection/reconciliation behavior;
- resource/API/model cost.

Component-specific divergence thresholds trigger review, extension of shadow duration or quarantine.

## 12. Component-Level Reality Gap
Reality-gap evidence is decomposed by dimensions such as decision, calibration, execution, latency, cost, fill rate, drawdown, turnover, risk and protection.

Critical dimension failure cannot be masked by one favorable aggregate RGS. Trend/worsening rate matters in addition to absolute gap.

## 13. Typed Promotion Evidence Matrix
Promotion profiles are component-specific, including at least:
- strategy/indicator;
- Intelligence Brain/model/retriever/agent;
- Risk/policy component;
- execution tactic/model;
- market-data/feature component.

Each profile declares mandatory metrics, optional metrics, minimum validation stages, failure gates and allowed promotion scope. Mandatory safety dimensions cannot be averaged away.

## 14. Rollback State Compatibility
Rollback evidence covers more than executable availability. It verifies compatibility of:
- open positions/orders/protection;
- Risk Reservations and OMS state;
- strategy/model internal state;
- memory/index versions;
- feature/data schemas;
- database/state migrations;
- policy/config versions.

If immediate rollback is unsafe, a documented roll-forward/recovery path is required.

## 15. Independent Promotion Review
HIGH_ASSURANCE promotion uses a distinct review role/process from candidate production where practical. The reviewer receives the immutable evidence bundle, failed-gate history and experiment-family/search history.

Approval identity, conflicts, rationale and conditions are append-only audit evidence. Models/agents may recommend but cannot approve themselves.

## 16. Experiment Resource Governor
Experiments have explicit CPU/GPU/memory/storage/API/model/token/cost budgets plus queue priority, cancellation, checkpoint/resume and partial-result semantics.

Resource shortage may delay or cancel experiments; it cannot silently reduce data fidelity, skip required gates or switch to optimistic assumptions.

## 17. Laboratory Observability + Holdout Integrity
Observability includes experiment queue/runtime, CPU/memory/storage, evaluator errors, data-fidelity state, leakage checks, failed/passed gates, reproduction class and cost.

Holdout raw outcomes and detailed diagnostics are access-controlled enough to prevent repeated manual tuning. Dashboards may expose pass/fail/summary evidence without turning final holdouts into an interactive tuning playground.

## HIGH gap closure map
- GAP-18: section 1
- GAP-19: section 2
- GAP-20: section 3
- GAP-21: section 4
- GAP-22: section 5
- GAP-23: section 6
- GAP-24: section 7
- GAP-25: section 8
- GAP-26: section 9
- GAP-27: section 10
- GAP-28: section 11
- GAP-29: section 12
- GAP-30: section 13
- GAP-31: section 14
- GAP-32: section 15
- GAP-33: section 16
- GAP-34: section 17

## Result
All 34 initial R07 CRITICAL/HIGH gaps now have explicit planning-resolution contracts across docs 64–65. Acceptance gates, decisions/requirements consolidation and final audit remain required before approval.