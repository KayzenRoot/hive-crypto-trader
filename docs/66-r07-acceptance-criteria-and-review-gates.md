# HCT-PLAN-0001-R07 — Acceptance Criteria & Review Gates

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R07`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

## Purpose
Define objective gates required before R07 may receive `APPROVED`.

## Gate A — Dataset eligibility
Promotion experiments use immutable dataset manifests and R05 completeness/fidelity authority; critically degraded evidence cannot masquerade as full fidelity.

## Gate B — Point-in-time universe
Historical universe, symbol eligibility, listing/delisting/pauses and venue rules are reconstructed at each decision epoch; current survivors are never projected backward.

## Gate C — Temporal non-interference
TNIC covers market data, joins/resampling, features, labels, news/RAG, universe/rules, model context and outcomes. Any unresolved leakage invalidates affected promotion evidence.

## Gate D — Holdout/OOS firewall
Final promotion holdouts are isolated from tuning/manual search; access is audited, temporal purge/embargo is used where needed and nested selection prevents holdout-driven optimization.

## Gate E — Experiment identity
Promotion-grade experiments pin code/data/config/dependencies/runtime/container/simulator/models/policies/RNG/evaluator identity with an immutable manifest hash.

## Gate F — Causal event scheduler
Replay event ordering/races are explicit and causal; impossible zero-time observation/execution loops cannot create synthetic edge.

## Gate G — Historical venue semantics
Order/margin/position/risk-tier/precision/fee/funding/capability rules are point-in-time versioned or explicitly UNKNOWN with conservative eligibility consequences.

## Gate H — Fill realism
Fill models expose realism/confidence class and model no-fill/partial/slippage/latency/liquidity constraints. Promotion cannot depend solely on impossible/optimistic fills.

## Gate I — Accounting/margin parity
Replay/paper/shadow use a canonical accounting/margin kernel consistent with approved risk/venue semantics for PnL, fees, funding, margin, liquidation and precision.

## Gate J — R03/R04 state-machine parity
Validation preserves RiskSnapshot/Reservation, authorization leases, OMS/fill conservation, cancel/replace, unknown outcome, protection and reconciliation semantics.

## Gate K — Live-Parity conformance
Strategy/Brain/Safety/Risk/policy/OMS behavior is shared or conformance-tested across replay/paper/shadow/live; semantic forks are explicit parity exceptions.

## Gate L — Paper/shadow isolation
Hypothetical candidates cannot mutate live exchange state, production positions/orders/reservations/protection/configuration and cannot silently access state-changing production capabilities.

## Gate M — Immutable promotion evidence
Promotion decisions reference append-only evidence bundles with exact manifests, hashes, evaluator/reviewer identities and failed/search-history context.

## Gate N — Multiple-testing governor
Experiment families track attempted variants/search space/metrics/holdout accesses and apply selection-bias/multiple-testing controls appropriate to the research process.

## Gate O — Stochastic reproduction
Named RNG streams/seeds and explicit reproduction classes exist; provider/hardware nondeterminism is disclosed rather than labeled deterministic.

## Gate P — Promotion validity lease
Production eligibility expires or requires revalidation after material venue/data/model/runtime/regime/reality-gap/safety changes.

## Gate Q — Limited-live canary contract
Future canary promotion has immutable scope/risk/loss/health/expiry/rollback limits, can automatically tighten and cannot silently broaden; R07 itself grants no real-money authority.

## Gate R — Statistical/economic significance
Promotion evidence reports uncertainty and economic materiality appropriate to the component, not only favorable point estimates.

## Gate S — Effective independence
Effective independent evidence is distinguished from raw sample/trade counts across correlated symbols/events/windows/regimes/searches.

## Gate T — Regime/OOD coverage
Validated/weak/absent regimes and OOD behavior are explicit; promotion scope cannot claim unsupported conditions.

## Gate U — Search/parameter robustness
Search budgets, nested validation, untouched promotion holdout and parameter plateau/fragility evidence are explicit.

## Gate V — Empirical simulator calibration
Fee/funding/latency/fill/slippage models are calibrated against observable paper/shadow/capture evidence when available with version/age/error/confidence and conservative fallback.

## Gate W — Degraded/synthetic/resampling integrity
Missing/degraded/imputed intervals, synthetic crises and Monte Carlo/resampling are explicitly classified and cannot be presented as clean historical profitability proof.

## Gate X — Portfolio interaction
Promotion evaluates shared capital/risk reservations/correlation/cross-margin/quota/liquidity/resource contention where component behavior can interact at portfolio level.

## Gate Y — Paired comparison / shadow / reality gap
Decision Twin/ablation limitations, Shadow Divergence and component-level Reality Gap are explicit; critical divergences cannot be hidden by aggregate metrics.

## Gate Z — Typed Promotion Evidence Matrix
Each component class has mandatory metrics/stages/failure gates and allowed scope. Safety-critical dimensions cannot be averaged away.

## Gate AA — Rollback compatibility
Rollback includes persisted state/schema/memory/OMS/open-position compatibility or an explicit safe roll-forward/recovery path.

## Gate AB — Independent review and resource governance
HIGH_ASSURANCE promotion has auditable independent review where practical; experiment compute/cost pressure cannot silently lower validation rigor.

## Gate AC — Canonical consistency
Before approval:
- R07 decisions are consolidated in Decisions Ledger;
- accepted R07 requirements are canonical;
- all 34 gaps map to accepted planning resolutions;
- Scope still forbids implementation/live authority;
- PR matches branch content;
- objective final R07 audit exists.

## Verdict rule
- unresolved CRITICAL/HIGH planning defect => `CORRECTION REQUIRED`;
- missing authoritative dependency necessary for planning => `BLOCKED`;
- all gates pass => `APPROVED`.

R07 planning approval never authorizes implementation, production credentials/deployment, limited-live activation or real-money trading.