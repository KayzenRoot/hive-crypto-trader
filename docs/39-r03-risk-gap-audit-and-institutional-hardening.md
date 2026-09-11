# HCT-PLAN-0001-R03 — Risk Gap Audit & Institutional Hardening

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R03`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

## Objective
Formally reconcile the R03 scope — Safety, Risk, leverage and position sizing — against the pre-discovery work captured in `docs/28-risk-intelligence-position-sizing-leverage-and-equity-guard.md`, identify missing institutional-grade controls, and define the next R03 hardening tasks before round approval.

This document does not authorize implementation or live trading.

## Source inputs
Primary repository inputs:
- `docs/28-risk-intelligence-position-sizing-leverage-and-equity-guard.md`;
- `docs/02-requirements.md`;
- `docs/03-scope.md`;
- `docs/10-decisions-ledger.md`;
- `docs/14-product-module-map.md`;
- `docs/29-execution-intelligence-oms-reconciliation-and-recovery.md`;
- `docs/30-realtime-market-data-intelligence-and-streaming-rd.md`;
- `docs/35-intelligence-brain-evidence-fusion-calibration-and-selective-decision.md`;
- `docs/36-simulation-replay-paper-shadow-and-promotion-laboratory.md`.

Current external exchange facts were rechecked against MEXC documentation/support material on 2026-09-11.

## Current pre-discovery strengths
The pre-discovery risk architecture is already strong in the following areas:
- deterministic Risk Engine authority;
- hierarchical risk budgets;
- Daily Equity Guard;
- position sizing from monetary risk/invalidation rather than leverage-first sizing;
- leverage treated as collateral/survivability parameter rather than alpha;
- liquidation buffer concepts;
- portfolio correlation/common-factor concentration;
- stress lattice;
- stop/invalidation separation;
- drawdown state machine;
- profit-protection modes;
- risk explainability;
- explicit prohibition on martingale-style recovery and target chasing;
- AI cannot relax hard risk ceilings.

These are accepted as R03 foundation inputs, subject to the gaps below.

## Current MEXC risk-model facts that affect architecture
The following current exchange behavior is material to R03 and must be treated as dynamic external state rather than frozen constants:

1. MEXC uses **Fair Price** as the liquidation trigger reference.
2. Liquidation occurs when maintenance-margin conditions are breached; MEXC describes MMR reaching 100% as the liquidation threshold.
3. Isolated and cross margin use materially different liquidation/equity semantics.
4. Maintenance margin is tiered by position/risk level and is not simply a constant function of selected leverage.
5. Maximum leverage depends on position size/risk tier.
6. MEXC may change maximum leverage, position limits and maintenance-margin ratios in abnormal/volatile conditions.
7. Cross-margin liquidation state can change because other cross positions and wallet equity affect the shared margin pool.

Architectural consequence: HCT must query/reconcile venue risk parameters and margin state at runtime wherever the API exposes them. No strategy or UI may assume a static leverage ceiling, static maintenance-margin rate or static liquidation distance.

## R03 gap audit

### GAP-R03-01 — Canonical margin-mode policy
Severity: `HIGH`

Current pre-discovery distinguishes liquidation/margin concepts but does not yet define a canonical HCT policy for:
- isolated margin;
- cross margin;
- future multi-asset/cross-collateral modes;
- per-strategy/per-tenant allowed margin modes;
- fallback/degradation when margin mode cannot be verified.

Required direction:
- make margin mode explicit in every risk snapshot/order intent;
- default new V1 autonomous strategies to the safest policy proven by validation rather than exchange UI defaults;
- block new exposure when actual exchange margin mode differs from the approved session/order policy and cannot be reconciled safely.

### GAP-R03-02 — Dynamic Risk Tier & Maintenance Margin Resolver
Severity: `CRITICAL`

Need a canonical resolver that determines, for the proposed post-trade position:
- current risk tier;
- current maximum allowed leverage;
- maintenance-margin rate;
- position limit;
- tier transition caused by the new order;
- effect of partial fills/adds/reductions;
- whether exchange rules changed since strategy/risk evaluation.

A trade may be valid before sizing but become invalid after size pushes the position into a higher maintenance-margin tier.

### GAP-R03-03 — Post-trade liquidation preview
Severity: `CRITICAL`

Risk approval must evaluate the **projected post-fill state**, not only current account state.

Required preview should estimate under relevant margin mode:
- post-trade notional;
- initial margin;
- maintenance margin;
- liquidation reference/price where derivable;
- liquidation buffer versus thesis invalidation/stop;
- fee/funding/slippage reserve;
- portfolio/cross-margin effects;
- uncertainty bounds.

Unknown/low-confidence projected liquidation state => no new exposure.

### GAP-R03-04 — Cross-margin contagion guard
Severity: `CRITICAL`

Cross margin can couple otherwise separate positions through shared equity.

Need explicit controls for:
- one losing position consuming collateral needed by others;
- simultaneous correlated stress;
- open-order margin consumption;
- wallet/equity changes;
- cross-position unrealized PnL dependence;
- protection degradation during multi-position drawdown.

Research construct: **HCT Cross-Margin Contagion Index (CMCI)**.

### GAP-R03-05 — Margin reserve / operational failure reserve
Severity: `HIGH`

A stop is not guaranteed to fill exactly at its trigger. Risk sizing needs a reserve for:
- slippage;
- spread expansion;
- gap/jump risk;
- delayed cancel/replace;
- API/WS degradation;
- protective-order failure;
- funding/fees where material.

Research construct: **HCT Operational Margin Reserve (OMR)**.

### GAP-R03-06 — Tail-risk measurement beyond correlation
Severity: `HIGH`

Correlation alone is insufficient during crypto stress because correlations can converge toward one and tails are nonlinear.

R03 should include governed portfolio tail-risk measures such as:
- Expected Shortfall / CVaR style views where statistically appropriate;
- scenario loss distribution;
- common-factor shocks;
- jump/gap stress;
- liquidity-adjusted loss;
- concentrated stablecoin/counterparty/exchange risk.

These measures support tighter risk decisions but cannot relax hard limits.

### GAP-R03-07 — Risk-of-ruin / survival budget
Severity: `HIGH`

Need an explicit account-survival layer that prevents individually valid trades from creating unacceptable cumulative ruin probability or drawdown trajectory.

Research construct: **HCT Survival Budget Index (SBI)**.

Inputs may include:
- current drawdown;
- historical strategy loss distribution;
- tail losses;
- consecutive-loss behavior;
- portfolio correlation;
- leverage/margin fragility;
- remaining daily/session/monthly risk budget;
- model/regime uncertainty.

### GAP-R03-08 — Multi-horizon risk budgets
Severity: `HIGH`

Current design is strong on trade/session/day. Institutional hardening should explicitly define budgets for:
- trade;
- rolling intraday window;
- daily;
- weekly;
- monthly;
- strategy lifecycle;
- tenant/account lifetime drawdown.

Longer-horizon limits may only tighten shorter-horizon authority.

### GAP-R03-09 — Risk budget consumption accounting
Severity: `HIGH`

Need deterministic definitions for what consumes risk budget:
- open-position potential loss to approved stop;
- realized loss;
- unrealized loss;
- pending-order projected risk;
- correlated exposure;
- conditional/add-on orders;
- multiple strategies targeting the same position;
- protective-order uncertainty.

Without this, several individually valid intents can overbook the same risk budget.

Research construct: **HCT Risk Reservation Ledger (RRL)**.

### GAP-R03-10 — Pending-order and partial-fill risk reservation
Severity: `CRITICAL`

Risk cannot wait until a fill occurs.

Required behavior:
- reserve risk before submit;
- convert reserved risk to realized/open-position risk as fills arrive;
- release only after cancel/rejection is exchange-confirmed/reconciled;
- preserve reservation in `UNCERTAIN` order state;
- prevent duplicate intents from reserving or consuming risk inconsistently.

This must integrate with OMS/idempotency.

### GAP-R03-11 — Add-to-position / pyramiding policy
Severity: `HIGH`

Need explicit rules for adding to existing positions:
- maximum total thesis risk;
- whether adding is allowed when current position is losing;
- add-on price/stop semantics;
- weighted entry effects;
- changed liquidation distance;
- tier transitions;
- correlation/portfolio changes;
- anti-martingale/martingale protections.

Default safety rule: no loss-recovery averaging unless a separately validated strategy explicitly defines bounded add logic and total thesis risk remains within original/approved ceilings.

### GAP-R03-12 — Stop-gap and stop-failure risk
Severity: `HIGH`

A configured stop does not equal a guaranteed exit.

Need explicit modeling for:
- trigger-to-fill slippage;
- no-liquidity scenarios;
- stop rejection/cancellation;
- exchange outage;
- price gaps;
- fair/mark/last trigger differences;
- guaranteed-stop capability if/where venue-specific and available.

Research construct: **HCT Protective Failure Exposure (PFE)**.

### GAP-R03-13 — ADL / forced-deleveraging awareness
Severity: `MEDIUM/HIGH`

Futures venues can use auto-deleveraging/insurance mechanisms during extreme conditions. R03 should model venue-specific forced-deleveraging/insurance-fund risk as an operational/tail-risk factor where API/data access permits.

It must not be assumed that a profitable open position is immune from venue-level extreme-event mechanics.

### GAP-R03-14 — Stablecoin/collateral concentration
Severity: `HIGH`

USDT-margined futures create collateral dependence beyond symbol price risk.

Need portfolio risk categories for:
- collateral asset concentration;
- stablecoin depeg/stress;
- exchange/custodial concentration;
- settlement asset risk;
- future multi-collateral interactions.

### GAP-R03-15 — Risk parameter provenance and snapshot hash
Severity: `CRITICAL`

Every approved trade needs an immutable/versioned risk snapshot containing at minimum:
- account/equity state;
- margin mode;
- contract/risk tier;
- maintenance margin rate;
- leverage ceiling/current leverage;
- selected leverage;
- position size/notional;
- risk amount/percentage;
- stop/invalidation;
- projected liquidation buffer;
- portfolio/correlation state;
- daily/session state;
- policy version;
- exchange-rule version/timestamp where available;
- data freshness/confidence;
- risk decision result/reasons;
- snapshot hash/correlation ID.

Execution must prove it is consuming a still-valid risk snapshot or request reapproval.

### GAP-R03-16 — Risk snapshot expiry / revalidation
Severity: `CRITICAL`

Risk approvals have a finite lifetime. Revalidate when:
- price moves materially;
- volatility/liquidity changes;
- risk tier changes;
- account equity changes;
- another order/position changes exposure;
- exchange rules change;
- signal lifetime is consumed;
- data/reconciliation confidence degrades.

Research construct: **HCT Risk Approval Half-Life (RAHL)**.

### GAP-R03-17 — Tenant/user risk profile presets
Severity: `MEDIUM`

For commercialization, define safe user-facing presets such as:
- CONSERVATIVE;
- BALANCED;
- AGGRESSIVE_WITHIN_PLATFORM_CEILINGS;
- CUSTOM_RESTRICTED.

Presets configure bounded policy, never bypass platform hard ceilings. Avoid marketing language implying expected returns.

### GAP-R03-18 — Risk explainability and pre-trade preview completeness
Severity: `MEDIUM/HIGH`

The cockpit should show not only risk/trade and leverage, but also:
- amount reserved by pending orders;
- remaining deployable risk;
- risk tier before/after;
- projected liquidation buffer;
- correlated exposure equivalent;
- cross-margin contagion warning;
- stress-loss estimates;
- data/exchange-state confidence;
- reason for each reduction/veto.

## Proprietary R03 research technologies
The following are approved as research hypotheses, not production claims:

1. **Cross-Margin Contagion Index (CMCI)** — shared-collateral fragility across cross positions.
2. **Operational Margin Reserve (OMR)** — extra margin/risk reserve for execution/protection uncertainty.
3. **Survival Budget Index (SBI)** — account-level survivability under cumulative/tail loss.
4. **Risk Reservation Ledger (RRL)** — deterministic risk reservation across pending/partial/uncertain intents.
5. **Protective Failure Exposure (PFE)** — loss exposure beyond nominal stop assumptions.
6. **Risk Approval Half-Life (RAHL)** — validity horizon of a risk approval under changing market/account state.
7. **Tier Transition Risk (TTR)** — incremental risk created by moving into a new exchange maintenance-margin/risk tier.
8. **Liquidation Buffer Confidence Interval (LBCI)** — uncertainty-aware liquidation buffer rather than a single point estimate.
9. **Portfolio Tail Coupling Score (PTCS)** — nonlinear/common-tail concentration beyond ordinary correlation.
10. **Risk Budget Utilization Surface (RBUS)** — multidimensional view of reserved, open, realized and contingent risk across hierarchy/time horizons.
11. **Collateral Fragility Score (CFS-Risk)** — collateral/stablecoin/exchange concentration risk; distinct namespace from continual-learning catastrophic-forgetting metrics.
12. **Stop-to-Liquidation Safety Corridor (SLSC)** — distance and uncertainty corridor between thesis stop/protection and liquidation mechanics.

Every research construct requires explicit validation and must only tighten or inform risk inside deterministic hard ceilings until separately promoted.

## Proposed canonical R03 authority chain

`Candidate Action`
`-> Risk Snapshot Builder`
`-> Risk Reservation Ledger`
`-> Portfolio/Tail/Correlation Analysis`
`-> Position Sizing`
`-> Dynamic Risk-Tier/Margin Resolver`
`-> Leverage & Liquidation Defense`
`-> Daily/Multi-Horizon Equity Guard`
`-> Safety Governor / Session Policy`
`-> APPROVE / REDUCE / WAIT / VETO`
`-> Execution Intelligence`

For open positions, risk continues continuously:

`Exchange/Reconciliation -> Position Risk Monitor -> Margin/Tier/Liquidation Monitor -> Portfolio Risk -> Equity Guard -> Reduce/Protect/Close recommendations -> deterministic Safety/Execution path`

## Canonical decision outputs
R03 should standardize risk outcomes such as:
- `RISK_APPROVED`;
- `RISK_APPROVED_REDUCED_SIZE`;
- `RISK_WAIT_REVALIDATION`;
- `RISK_VETO_BUDGET`;
- `RISK_VETO_MARGIN`;
- `RISK_VETO_LIQUIDATION_BUFFER`;
- `RISK_VETO_PORTFOLIO_CONCENTRATION`;
- `RISK_VETO_DATA_UNCERTAIN`;
- `RISK_VETO_EXCHANGE_STATE_UNCERTAIN`;
- `RISK_NO_NEW_EXPOSURE`;
- `RISK_REDUCE_ONLY`;
- `RISK_EMERGENCY`.

## Bootstrap/free-first compatibility
R03 hardening does not require expensive infrastructure.

Bootstrap implementation can use:
- deterministic in-process risk calculations in the persistent trading worker/backend;
- Supabase/PostgreSQL for policy/risk snapshots/audit metadata;
- compact historical aggregates for calibration/stress research;
- local/offline Monte Carlo/stress experiments where useful;
- provider-neutral contracts for later scale.

No paid risk analytics service is required for V1.

## External references checked during R03 start
Planning inputs verified on 2026-09-11:
- MEXC `FAQ on Liquidation for Futures Trading` — Fair Price liquidation trigger, MMR/liquidation semantics, isolated vs cross liquidation calculations.
- MEXC `A Complete Guide to Futures Information Terminology` — initial margin, maintenance margin, position-size-dependent risk tiers and leverage.
- MEXC Futures Risk Limit pages — per-contract tiered maximum leverage and maintenance-margin rates; venue may adjust leverage/position limits/MMR during abnormal market conditions.

Provider rules are external dependencies and must be revalidated during implementation/preflight.

## R03 initial verdict
`CORRECTION REQUIRED`

Reason: the pre-discovery architecture is strong but the CRITICAL gaps above must be incorporated into the canonical R03 risk design before the round can be promoted.

## Next necessary R03 action
Create the formal institutional risk-control architecture that closes at least GAP-R03-02, 03, 04, 09, 10, 15 and 16 first, because those gaps affect deterministic authority and can invalidate otherwise correct position sizing.

## STOP CONDITION
Do not approve R03 until all CRITICAL gaps have canonical designs, authority boundaries, state transitions, validation requirements and explicit exchange-state/reconciliation dependencies. No implementation Work Order or live trading authorization before R03 promotion.
