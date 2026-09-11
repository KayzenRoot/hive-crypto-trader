# HCT-PLAN-0001-R03 — Risk Gap Audit & Institutional Hardening

Status: `RESOLVED_IN_PLANNING`
Increment: `HCT-PLAN-0001-R03`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

## Objective
Formally reconcile the R03 scope — Safety, Risk, leverage and position sizing — against the pre-discovery work captured in `docs/28-risk-intelligence-position-sizing-leverage-and-equity-guard.md`, identify missing institutional-grade controls, and define the R03 hardening required before round approval.

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

## Accepted pre-discovery strengths
The pre-discovery risk architecture already covered:
- deterministic Risk Engine authority;
- hierarchical risk budgets;
- Daily Equity Guard;
- position sizing from monetary risk/invalidation rather than leverage-first sizing;
- leverage as collateral/survivability parameter rather than alpha;
- liquidation buffer concepts;
- portfolio correlation/common-factor concentration;
- stress lattice;
- stop/invalidation separation;
- drawdown state machine;
- profit-protection modes;
- risk explainability;
- prohibition on martingale-style recovery and target chasing;
- AI inability to relax hard risk ceilings.

## Current MEXC risk-model facts affecting architecture
The following exchange behavior is treated as dynamic external state, not frozen constants:
1. Fair Price is the liquidation trigger reference.
2. Liquidation depends on maintenance-margin conditions.
3. Isolated and cross margin have materially different semantics.
4. Maintenance margin is tiered by position/risk level.
5. Maximum leverage depends on position size/risk tier.
6. Venue rules such as leverage/position limits/MMR may change under market stress.
7. Cross-margin liquidation state can change because other positions and wallet equity share collateral.
8. Extreme conditions may involve partial/tiered liquidation and ADL mechanics.

Architectural consequence: venue risk parameters and margin state must be resolved/reconciled dynamically wherever available. Unknown critical risk state blocks new exposure.

## Final gap resolution matrix

### GAP-R03-01 — Canonical margin-mode policy
Severity: `HIGH`
Status: `RESOLVED_IN_PLANNING`

Margin mode is explicit in RiskSnapshot/order policy. Mismatch or unverifiable state blocks or degrades new exposure. Cross and isolated semantics are handled distinctly, with future modes behind capability contracts.

### GAP-R03-02 — Dynamic Risk Tier & Maintenance Margin Resolver
Severity: `CRITICAL`
Status: `RESOLVED_IN_PLANNING`

Covered by `ExchangeRiskRuleResolver`, tier-transition analysis and dynamic venue-rule provenance in `docs/40` and Decisions Ledger.

### GAP-R03-03 — Post-trade liquidation preview
Severity: `CRITICAL`
Status: `RESOLVED_IN_PLANNING`

Risk approval evaluates projected post-fill notional, tier/MMR, margin, liquidation corridor, fees/funding/slippage, portfolio effects and uncertainty before exposure increases.

### GAP-R03-04 — Cross-margin contagion guard
Severity: `CRITICAL`
Status: `RESOLVED_IN_PLANNING`

Covered by deterministic CrossMarginContagionGuard and shared-collateral stress evaluation.

### GAP-R03-05 — Margin reserve / operational failure reserve
Severity: `HIGH`
Status: `RESOLVED_IN_PLANNING`

Covered by protected Operational Margin Reserve, excluded from normal opportunity sizing.

### GAP-R03-06 — Tail-risk measurement beyond correlation
Severity: `HIGH`
Status: `RESOLVED_IN_PLANNING`

Covered by tail-loss/Expected Shortfall-style research, stress surfaces and common-tail/correlation-collapse analysis. Tail models may only tighten hard limits.

### GAP-R03-07 — Risk-of-ruin / survival budget
Severity: `HIGH`
Status: `RESOLVED_IN_PLANNING`

Covered by account-survival budget and survival-state concepts across cumulative loss horizons.

### GAP-R03-08 — Multi-horizon risk budgets
Severity: `HIGH`
Status: `RESOLVED_IN_PLANNING`

Trade, intraday/session, daily, weekly, monthly and account-survival budgets are explicitly hierarchical.

### GAP-R03-09 — Risk budget consumption accounting
Severity: `HIGH`
Status: `RESOLVED_IN_PLANNING`

Canonical risk categories and Risk Reservation Ledger define open, pending, uncertain, contingent, correlated, tail and collateral risk without naïve double-counting.

### GAP-R03-10 — Pending-order and partial-fill risk reservation
Severity: `CRITICAL`
Status: `RESOLVED_IN_PLANNING`

Risk reserves before submit; partial fills conserve reserved/open risk; timeout/cancel requests never free budget before authoritative resolution.

### GAP-R03-11 — Add-to-position / pyramiding policy
Severity: `HIGH`
Status: `RESOLVED_IN_PLANNING`

Every ADD is a fresh exposure-increasing decision requiring a new RiskSnapshot, reservation and projected portfolio/tier/liquidation review. Martingale/loss-recovery escalation is prohibited by default.

### GAP-R03-12 — Stop-gap and stop-failure risk
Severity: `HIGH`
Status: `RESOLVED_IN_PLANNING`

Protection Failure Exposure covers gap-through-stop, trigger-to-fill slippage, rejection/cancellation, partial coverage, stale quantity, outage and uncertain protection.

### GAP-R03-13 — ADL / forced-deleveraging awareness
Severity: `MEDIUM/HIGH`
Status: `RESOLVED_IN_PLANNING`

Extreme venue mechanics, partial/tiered liquidation and ADL exposure are explicit risk inputs where observable, with conservative UNKNOWN degradation otherwise.

### GAP-R03-14 — Stablecoin/collateral concentration
Severity: `HIGH`
Status: `RESOLVED_IN_PLANNING`

Collateral concentration, stablecoin/depeg risk, stress haircuts and Effective Risk Capital are explicit inputs.

### GAP-R03-15 — Risk parameter provenance and snapshot hash
Severity: `CRITICAL`
Status: `RESOLVED_IN_PLANNING`

Immutable/versioned RiskSnapshot captures account, margin, tier/MMR, leverage, size, stop/invalidation, liquidation, portfolio, policy, venue-rule provenance, freshness/confidence and hash/correlation identity.

### GAP-R03-16 — Risk snapshot expiry / revalidation
Severity: `CRITICAL`
Status: `RESOLVED_IN_PLANNING`

Risk approvals have finite validity plus event-driven invalidation/revalidation triggers across market, portfolio, exchange and policy changes.

### GAP-R03-17 — Tenant/user risk profile presets
Severity: `MEDIUM`
Status: `RESOLVED_IN_PLANNING`

CONSERVATIVE, BALANCED, AGGRESSIVE and CUSTOM are bounded configuration bundles beneath platform hard ceilings and carry no return promise.

### GAP-R03-18 — Risk explainability and pre-trade preview completeness
Severity: `MEDIUM/HIGH`
Status: `RESOLVED_IN_PLANNING`

Risk explainability includes requested/approved risk, reservations, deployable risk, tier before/after, liquidation corridor, tail/survival state, correlated/cross-margin exposure, collateral quality, protection confidence and exact veto/reduction reasons.

## Proprietary R03 research technologies
Approved only as research hypotheses, never as production profit claims:
1. Cross-Margin Contagion Index (CMCI)
2. Operational Margin Reserve (OMR)
3. Survival Budget Index (SBI)
4. Risk Reservation Ledger (RRL)
5. Protective Failure Exposure (PFE)
6. Risk Approval Half-Life (RAHL)
7. Tier Transition Risk (TTR)
8. Liquidation Buffer Confidence Interval (LBCI)
9. Portfolio Tail Coupling Score (PTCS)
10. Risk Budget Utilization Surface (RBUS)
11. Collateral Fragility Score (CFS-Risk)
12. Stop-to-Liquidation Safety Corridor (SLSC)
13. Tail Loss Envelope
14. Expected Shortfall Surface
15. Survival Probability Floor
16. Collateral Stress Haircut / Effective Risk Capital
17. ADL Exposure Score

Each construct must demonstrate incremental decision/safety value before future implementation promotion.

## Canonical R03 authority chain
`Candidate Action -> Risk Snapshot Builder -> Risk Reservation Ledger -> Portfolio/Tail/Correlation Analysis -> Position Sizing -> Dynamic Risk-Tier/Margin Resolver -> Leverage & Liquidation Defense -> Multi-Horizon Equity/Survival Guard -> Safety Governor / Session Policy -> APPROVE / REDUCE / WAIT / VETO -> Execution Intelligence`

For open positions:
`Exchange/Reconciliation -> Position Risk Monitor -> Margin/Tier/Liquidation Monitor -> Portfolio Risk -> Equity/Survival Guard -> Reduce/Protect/Close recommendation -> deterministic Safety/Execution path`

## Final R03 status
Initial verdict was `CORRECTION REQUIRED` because CRITICAL/HIGH institutional controls were missing from the pre-discovery material.

After `docs/40`, `docs/41`, `docs/42`, Requirements alignment and Decisions `HCT-DEC-0042` through `HCT-DEC-0049`, all identified CRITICAL/HIGH R03 planning gaps are resolved.

Final objective review is recorded in `docs/43-r03-final-audit.md` with verdict `APPROVED`.

Implementation and live trading remain unauthorized.

## STOP CONDITION
Satisfied for R03 planning: no unresolved CRITICAL/HIGH gap remains, final audit is `APPROVED`, and the round may proceed to merge/checkpoint promotion. Future implementation still requires separate HIGH_ASSURANCE Work Orders and evidence.