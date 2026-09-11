# HCT-PLAN-0001-R07 — Simulation / Replay / Backtest / Paper / Shadow / Promotion Laboratory Gap Audit

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R07`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`
Initial verdict: `CORRECTION REQUIRED`

## Objective
Formally reconcile the pre-discovery laboratory in `docs/36-simulation-replay-paper-shadow-and-promotion-laboratory.md` against approved R03 Risk, R04 Execution/OMS/Reconciliation, R05 realtime/data-quality and R06 Intelligence/Temporal Memory contracts.

The laboratory is a proof system, not a PnL screenshot generator. Promotion evidence must remain point-in-time correct, reproducible, realistic, statistically defensible and operationally equivalent enough to the eventual live system that passing the laboratory has real meaning.

## Existing strengths
- staged lifecycle from research through replay/paper/shadow/champion-challenger;
- Temporal Non-Interference Checker concept;
- Deterministic Replay Fingerprint and Market Replay Fidelity Score;
- realistic fees/funding/slippage/latency/partial fills;
- Fill Realism Envelope and signal-half-life stress;
- walk-forward/OOS and parameter-plateau concepts;
- Reality Gap Score and live-parity contract;
- stress/failure simulation, synthetic crises and Monte Carlo;
- Decision Twin/ablation and counterfactual separation;
- explicit promotion gates, rollback concept and limited-live stage.

## R07 gaps

### GAP-R07-01 — Dataset eligibility and capture-completeness authority
Severity: `CRITICAL`
Promotion experiments need a deterministic Dataset Eligibility Gate consuming R05 capture-completeness/fidelity manifests. Missing critical channels, unproven continuity, schema quarantine or materially degraded intervals cannot silently count as full-fidelity evidence.

### GAP-R07-02 — Point-in-time universe / survivorship-bias firewall
Severity: `CRITICAL`
Historical tests must reconstruct which contracts actually existed, were API/trading eligible, paused/delisted/listed and had which rules at each decision epoch. Current symbol lists cannot be projected backward.

### GAP-R07-03 — End-to-end temporal leakage proof
Severity: `CRITICAL`
TNIC must become a formal proof contract covering joins, resampling, feature windows, labels, news/RAG, model/retriever training, universe membership, exchange-rule versions, corrections/vintages and downstream execution outcomes.

### GAP-R07-04 — Holdout / OOS access firewall
Severity: `CRITICAL`
Repeatedly viewing and tuning against the final OOS set turns it into training data. Need immutable evaluation splits, access/audit controls, purging/embargo where temporal dependence requires it, and nested validation for parameter/model selection.

### GAP-R07-05 — Full experiment environment identity
Severity: `CRITICAL`
Code/data hashes alone are insufficient. Promotion-grade experiments need pinned dependency lockfiles, runtime/container/build identity, configuration, simulator version, model/provider behavior class, hardware-relevant settings and deterministic/random stream identity.

### GAP-R07-06 — Causal event scheduler and race semantics
Severity: `CRITICAL`
Replay must define causal ordering when market data, signals, risk decisions, order submits, fills, cancels, private events and reconciliation overlap. Impossible event orderings or zero-time races may not create synthetic edge.

### GAP-R07-07 — Venue capability/rule parity by historical version
Severity: `CRITICAL`
Simulation must resolve point-in-time order types, position modes, reduce-only/STP semantics, quantity/price precision, leverage/risk tiers, MMR, symbol limits, request/rate behavior and other venue capabilities rather than applying today's rules to all history.

### GAP-R07-08 — Fill realism authority
Severity: `CRITICAL`
Need explicit fill-model confidence classes, queue/priority uncertainty, liquidity participation limits, no-fill/partial-fill behavior and prohibition of impossible same-bar/same-tick fills. Optimistic fill assumptions may not be the sole promotion basis.

### GAP-R07-09 — Accounting/margin/liquidation/funding parity
Severity: `CRITICAL`
Simulator accounting must match R03 risk semantics and venue precision for fees, funding, realized/unrealized PnL, initial/maintenance margin, cross/isolated margin, tier transitions, liquidation references, partial liquidation and collateral effects where modeled.

### GAP-R07-10 — R03/R04 state-machine parity
Severity: `CRITICAL`
Replay/paper/shadow must preserve RiskSnapshot expiry/revalidation, Risk Reservation Ledger, Command Authorization Lease, OMS fill conservation, cancel/replace races, unknown outcomes, protection dependency/coverage, reconciliation conflicts and restart recovery semantics rather than bypassing them for convenience.

### GAP-R07-11 — Live-Parity conformance test
Severity: `CRITICAL`
Need executable contract tests proving research/replay/paper/shadow use the same strategy/Brain/Safety/Risk/policy/OMS semantics as live, with only environment adapters differing. Semantic forks must be explicit and disqualify false parity claims.

### GAP-R07-12 — Paper/shadow hard isolation
Severity: `CRITICAL`
Paper/shadow candidates must be incapable of mutating real exchange state, production Risk Reservations, authoritative positions, protection, account balances or production configuration. Credential/tool boundaries must enforce this, not merely naming conventions.

### GAP-R07-13 — Promotion evidence immutability/provenance
Severity: `CRITICAL`
Promotion artifacts require immutable experiment IDs, data/code/config fingerprints, evidence hashes, evaluator versions, reviewer identity, timestamps and append-only decisions so favorable results cannot be silently replaced after review.

### GAP-R07-14 — Multiple-testing / selection-bias control
Severity: `CRITICAL`
Large strategy/model/parameter searches can manufacture winners. Need experiment-family identity, search-budget accounting, false-discovery/selection-bias controls, preregistered primary metrics where appropriate and explicit penalty for repeated selection on the same evidence.

### GAP-R07-15 — Stochastic reproducibility contract
Severity: `CRITICAL`
Monte Carlo, stochastic fills and LLM/model behavior need separated named RNG streams/seeds where possible and explicit reproduction classes where providers/hardware are nondeterministic. “Reproducible” may not be claimed when only approximate reproduction is possible.

### GAP-R07-16 — Promotion evidence expiry and revalidation triggers
Severity: `CRITICAL`
A once-approved candidate cannot remain valid forever. Need revalidation triggers for material venue-rule changes, data/schema changes, model/provider changes, regime drift, execution reality-gap growth, prolonged inactivity and safety defects.

### GAP-R07-17 — Limited-live canary authority and rollback
Severity: `CRITICAL`
`LIMITED_LIVE` needs a deterministic operating envelope, maximum loss/exposure, symbol/account/time scope, health gates, rollback target, automatic kill criteria and rule that canary scope may tighten but never silently broaden.

### GAP-R07-18 — Statistical and economic significance contract
Severity: `HIGH`
Promotion metrics need uncertainty intervals and economic materiality, not only point estimates. Thresholds should be component-specific and distinguish statistically detectable from commercially meaningful improvement.

### GAP-R07-19 — Effective sample independence
Severity: `HIGH`
Need effective sample size/episode independence across trades, correlated symbols, regimes and event clusters so thousands of highly related observations are not counted as thousands of independent proofs.

### GAP-R07-20 — Regime/OOD coverage requirements
Severity: `HIGH`
Candidates need explicit coverage of relevant trend/range, volatility, liquidity, event and execution-quality regimes plus OOD/novel-condition behavior. Lack of representative regimes must reduce promotion confidence or scope.

### GAP-R07-21 — Search budget, nested tuning and parameter robustness
Severity: `HIGH`
Parameter/model search budgets, nested validation and plateau/fragility tests need one contract. Hyperparameter optimization may not see the final promotion holdout.

### GAP-R07-22 — Empirical calibration of fee/fill/latency models
Severity: `HIGH`
Simulation assumptions must be calibrated against observed paper/shadow/live-capture distributions where available. Static guessed latency/slippage/fill assumptions need confidence class and conservative fallback.

### GAP-R07-23 — Missing/degraded-data interval policy
Severity: `HIGH`
Experiments must classify intervals as full-fidelity, degraded, research-only or invalid-for-promotion. Imputation/coalescing/synthetic repair must be explicit and cannot silently become historical truth.

### GAP-R07-24 — Synthetic crisis governance
Severity: `HIGH`
Synthetic scenarios require generator/version/seed/assumption provenance, separate reporting from historical evidence and explicit rule that they test survivability/failure handling rather than prove historical profitability.

### GAP-R07-25 — Monte Carlo/resampling validity
Severity: `HIGH`
Resampling methods must preserve relevant serial dependence, clustering, regime structure and path-dependent risk where needed. Naive IID shuffling cannot be used to manufacture reassuring tails.

### GAP-R07-26 — Portfolio and multi-strategy interaction replay
Severity: `HIGH`
Promotion must evaluate shared capital, common-factor exposure, simultaneous signals, quota/resource contention, correlation and cross-margin effects rather than validating every strategy only in isolation.

### GAP-R07-27 — Decision Twin / ablation causal limits
Severity: `HIGH`
Paired experiments need identical admissible evidence and controlled differences. Decision Twin/ablation results must state confounders and cannot claim causality when environment/model stochasticity prevents it.

### GAP-R07-28 — Shadow divergence monitoring
Severity: `HIGH`
Need explicit Shadow Divergence Monitor comparing candidate vs champion decisions, latency, fills, risk actions, abstention, calibration and resource cost over aligned windows, with alert/quarantine thresholds.

### GAP-R07-29 — Reality-gap thresholds by component
Severity: `HIGH`
Backtest→replay→paper→shadow→limited-live gaps need component-specific tolerances and trend detection. One aggregate RGS may not hide a critical execution, calibration or risk divergence.

### GAP-R07-30 — Component-specific Promotion Evidence Matrix
Severity: `HIGH`
Strategies, risk models, Brain changes, retrievers, agents and execution tactics require different required metrics/gates. A one-size promotion score is insufficient; critical mandatory dimensions cannot be averaged away.

### GAP-R07-31 — Rollback state compatibility
Severity: `HIGH`
Rollback must include compatibility of persisted strategy/model state, memory/index versions, open positions/orders, feature schemas and migrations. “Previous binary exists” is not enough rollback proof.

### GAP-R07-32 — Independent review / segregation of promotion authority
Severity: `HIGH`
HIGH_ASSURANCE promotion requires reviewer independence from the producing candidate where practical, explicit evidence review, conflict/audit identity and no model/agent self-approval.

### GAP-R07-33 — Experiment compute/cost budget and cancellation
Severity: `HIGH`
Heavy replays, Monte Carlo and model evaluations need bounded compute/storage/API cost, priority queues, cancellation and resumability. Resource pressure may delay experiments but cannot silently lower validation rigor.

### GAP-R07-34 — Laboratory observability and benchmark integrity
Severity: `HIGH`
Need experiment runtime/resource/queue metrics, evaluator errors, data-fidelity state, failed gates and reproducibility class without exposing final holdout data broadly enough to encourage manual overfitting.

## Priority closure order
### CRITICAL first
1. dataset eligibility/completeness;
2. point-in-time universe;
3. temporal leakage proof;
4. holdout/OOS firewall;
5. experiment environment identity;
6. causal event ordering;
7. historical venue semantics;
8. fill realism authority;
9. accounting/margin parity;
10. R03/R04 state-machine parity;
11. live-parity conformance;
12. paper/shadow hard isolation;
13. immutable promotion evidence;
14. multiple-testing/selection-bias control;
15. stochastic reproducibility;
16. promotion expiry/revalidation;
17. limited-live canary/rollback.

### HIGH next
Statistical/economic significance, effective independence, regime coverage, nested tuning/plateau, empirical cost/latency/fill calibration, degraded-data policy, synthetic/Monte-Carlo governance, portfolio interactions, paired-ablation limits, shadow divergence, component-level reality gap/promotion matrices, rollback compatibility, independent review, compute budgets and lab observability.

## Initial verdict
`CORRECTION REQUIRED`

The pre-discovery is strong, but the laboratory cannot become a promotion authority until the CRITICAL/HIGH contracts above are canonical and objectively auditable.

## STOP CONDITION
Do not approve R07 while any CRITICAL/HIGH gap remains unresolved. R07 planning approval, if later achieved, does not authorize implementation, production credentials, production deployment, limited live or real-money trading.