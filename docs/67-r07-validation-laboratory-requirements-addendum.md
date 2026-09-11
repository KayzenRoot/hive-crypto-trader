# HCT-PLAN-0001-R07 — Validation Laboratory Requirements Addendum

Status: `ACCEPTED_FOR_R07_PLANNING`
Increment: `HCT-PLAN-0001-R07`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

## Purpose
This addendum is the canonical R07 requirements source together with `docs/02-requirements.md` until planning-freeze consolidation. It converts docs 63–66 into explicit requirements for Simulation, Replay, Backtest, Paper, Shadow and Promotion.

## VAL-001 — Dataset Eligibility Gate
Every promotion-grade experiment SHALL use an immutable dataset manifest carrying source/provenance, R05 capture completeness/fidelity, temporal coverage, schema/gap/correction state, universe/rule references and allowed-use class. Critically untrusted data SHALL NOT be treated as promotion evidence.

## VAL-002 — Point-in-time universe
Historical tests SHALL reconstruct the actual symbol/contract universe, listing/delisting/paused/API eligibility and relevant venue-rule state at each decision epoch. Current survivors SHALL NOT be projected backward.

## VAL-003 — Temporal Non-Interference proof
Promotion-grade historical experiments SHALL prove that every consumed market/news/RAG/feature/label/universe/rule/model input was available at the simulated decision time. Material leakage invalidates affected evidence.

## VAL-004 — Holdout/OOS firewall
Final promotion holdouts SHALL be isolated from model/parameter tuning and repeated manual inspection. Access SHALL be logged; temporal purge/embargo and nested validation SHALL be used where dependency structure requires them. A repeatedly inspected holdout may be declared consumed and replaced before confirmatory promotion use.

## VAL-005 — Reproduction Manifest
Promotion experiments SHALL pin code, data, configuration, dependencies, runtime/container/build, simulator/accounting/fill/latency versions, model/prompt/tool/skill/retriever/calibration/policy versions, venue semantics, evaluator versions and RNG/reproduction identity sufficient to classify reproducibility honestly.

## VAL-006 — Causal event scheduling
Replay SHALL use explicit causal ordering and tie/race semantics for market events, decisions, risk approval, order commands, fills, cancel/replace, private events, protection and reconciliation. Consequences SHALL NOT be observable by their own causes.

## VAL-007 — Historical venue semantics
Simulation SHALL use point-in-time exchange capabilities/rules where material, including order/TIF/STP/reduce-only/position mode, precision/minimums, risk tiers/MMR/leverage/position limits, fees/funding, symbol status and other execution-critical semantics. Unknown critical semantics SHALL reduce dataset/experiment eligibility.

## VAL-008 — Fill realism
Fill simulation SHALL declare realism/confidence class and model relevant spread, liquidity, participation, queue uncertainty, latency, no-fill, partial-fill and cancellation behavior. Impossible same-bar/same-tick perfect fills are prohibited. Promotion SHALL NOT rely solely on an optimistic fill envelope.

## VAL-009 — Canonical accounting/margin kernel
Replay/paper/shadow SHALL share canonical definitions for position state, PnL, fees, funding, margin, tier transitions, liquidation-related state, collateral effects and precision consistent with approved R03/R04 contracts and point-in-time venue semantics.

## VAL-010 — R03/R04 state-machine parity
Validation environments SHALL preserve RiskSnapshot/revalidation, Risk Reservation Ledger, Command Authorization Lease, execution identity, fill conservation, unknown outcome, cancel/replace race, protection dependency, reconciliation conflict and recovery semantics rather than bypass them for backtest convenience.

## VAL-011 — Live-Parity conformance
Research/replay/paper/shadow SHALL use the same domain contracts/semantics as production where feasible. Semantic forks SHALL be explicit `PARITY_EXCEPTION`s and SHALL block blanket live-parity claims until resolved or deliberately scoped.

## VAL-012 — Paper/shadow capability isolation
Paper/shadow SHALL be technically unable to mutate production exchange orders, positions, Risk Reservations, protection, balances or authoritative configuration. Hypothetical fills/actions SHALL be namespace-isolated and SHALL NOT become real trading truth.

## VAL-013 — Immutable promotion evidence
Every promotion decision SHALL reference an immutable/versioned Promotion Evidence Bundle containing manifests, datasets, metrics, gate results, evaluator/reviewer identities, evidence hashes and relevant failed/search history. Reviewed results SHALL NOT be silently overwritten.

## VAL-014 — Multiple-testing and selection-bias governance
Related experiments SHALL use an ExperimentFamilyID and track attempted variants, search space, metrics, datasets/folds and holdout accesses. Promotion SHALL account for repeated search/selection and SHALL NOT present a mined winner as if it were a single preregistered test.

## VAL-015 — Stochastic reproduction classes
Stochastic fills, latency, resampling and model behavior SHALL use separated RNG streams/seeds where possible and SHALL declare an explicit reproduction class. Provider/hardware nondeterminism SHALL be disclosed instead of falsely labeled deterministic.

## VAL-016 — Promotion validity lease
Production eligibility SHALL have a validity horizon and revalidation triggers for material venue, data/schema, model/prompt/retriever/skill, runtime, regime, reality-gap or safety/reconciliation changes.

## VAL-017 — Limited-live canary envelope
Future `LIMITED_LIVE`, if separately authorized later, SHALL use an immutable account/symbol/time/risk/loss/exposure/health/expiry envelope, exact rollback target and automatic kill criteria. Canary scope may tighten automatically and SHALL NOT silently broaden. R07 itself grants no live authority.

## VAL-018 — Statistical and economic significance
Promotion evidence SHALL report uncertainty and component-appropriate economic materiality after costs/risk/latency/complexity, not only favorable point estimates.

## VAL-019 — Effective evidence independence
Promotion evidence SHALL distinguish raw observations from effective independent episodes, accounting for correlated symbols, overlapping windows, common events/regimes and repeated searches where material.

## VAL-020 — Regime/OOD coverage
Candidates SHALL declare validated, weakly covered, absent and out-of-distribution market/execution conditions. Promotion scope SHALL NOT claim unsupported regimes, and OOD behavior SHALL have conservative fallback.

## VAL-021 — Search budget and parameter robustness
Hyperparameter/model search SHALL have an explicit search-space/budget and occur inside nested validation. Final holdouts SHALL remain untouched. Promotion SHALL evaluate parameter plateau, neighboring sensitivity, regime stability and cost sensitivity rather than only the best point.

## VAL-022 — Empirical simulator calibration
Fee/funding/latency/spread/slippage/fill/cancel models SHALL be versioned and calibrated against observed paper/shadow/capture or later authorized live data when available, with error/confidence/age and conservative fallback.

## VAL-023 — Degraded/missing data integrity
Experiment intervals SHALL be classified by fidelity. Imputation/coalescing/interpolation/synthetic repair SHALL be explicit and versioned and SHALL NOT silently become historical truth or full-fidelity promotion evidence.

## VAL-024 — Synthetic and Monte Carlo governance
Synthetic crises SHALL remain separately identified from historical evidence and may prove survivability/failure handling but not historical profitability. Monte Carlo/resampling SHALL document assumptions and preserve material dependence/path structure when required.

## VAL-025 — Portfolio interaction replay
Where behavior can interact, promotion SHALL test shared capital, Risk Reservations, correlations/common factors, cross margin/collateral, simultaneous signals, conflicting orders, API/resource contention and shared liquidity rather than only isolated components.

## VAL-026 — Paired comparison and shadow divergence
Decision Twin/ablation SHALL use matched point-in-time evidence and disclose confounders. Shadow Divergence SHALL compare candidate and Champion decision/calibration/latency/execution/risk/resource behavior under aligned windows and component-specific thresholds.

## VAL-027 — Component-level Reality Gap
Backtest→replay→paper→shadow→limited-live gaps SHALL be decomposed by decision, calibration, execution, fill, latency, cost, risk and protection dimensions. A critical failing dimension SHALL NOT be averaged away by a favorable composite.

## VAL-028 — Typed Promotion Evidence Matrix
Strategies/features, Intelligence/agents/retrievers, Risk/policy components, execution tactics/models and market-data components SHALL have typed mandatory metrics/stages/failure gates and allowed scope. Safety-critical mandatory gates cannot be averaged away.

## VAL-029 — Rollback state compatibility
Rollback proof SHALL cover persisted model/strategy/memory/schema/config/OMS/open-position/order/protection/Risk Reservation compatibility, not just availability of an older binary. If rollback is unsafe, a governed roll-forward/recovery plan is required.

## VAL-030 — Independent promotion review
HIGH_ASSURANCE promotion SHALL use auditable independent review from candidate creation where practical. Models/agents cannot self-approve. Reviewer identity, conflicts, rationale and conditions SHALL be immutable evidence.

## VAL-031 — Experiment Resource Governor
Replay/Monte Carlo/model evaluation SHALL have CPU/GPU/memory/storage/API/token/cost budgets, queue priority, cancellation/checkpoint/resume and partial-result semantics. Resource pressure SHALL NOT silently weaken required validation rigor.

## VAL-032 — Laboratory observability and holdout integrity
The lab SHALL expose experiment runtime/resource cost, data fidelity, evaluator errors, leakage status, gate outcomes and reproduction class while restricting raw holdout feedback enough to prevent interactive manual overfitting.

## Validation principle
Historical PnL alone is insufficient. A candidate is promotion-eligible only when applicable data, temporal, execution, risk, reproducibility, robustness, parity and governance gates pass.

## Safety
This document grants planning acceptance only. `implementation_authorized=false`; production credentials/deployment, limited-live activation and real-money trading remain unauthorized.