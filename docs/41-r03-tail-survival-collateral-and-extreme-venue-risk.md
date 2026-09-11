# HCT-PLAN-0001-R03 — Tail, Survival, Collateral & Extreme Venue Risk

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R03`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

## Objective
Close the remaining HIGH institutional gaps in R03 by defining deterministic controls for tail loss, multi-horizon survival, operational margin reserves, protective-order failure, pyramiding/add-to-position behavior, collateral concentration and exchange extreme-state mechanics such as partial liquidation and ADL.

## 1. Multi-horizon survival budget
Risk must not be managed only per trade or per day. HCT should maintain nested budgets for:
- trade;
- rolling intraday window;
- session/day;
- rolling week;
- rolling month;
- account lifetime survival reserve.

Lower-horizon budgets cannot consume capital reserved to satisfy higher-horizon survival constraints.

Candidate states:
- `SURVIVAL_HEALTHY`
- `SURVIVAL_CAUTION`
- `SURVIVAL_REDUCED_RISK`
- `SURVIVAL_NO_NEW_EXPOSURE`
- `SURVIVAL_RECOVERY_ONLY`
- `SURVIVAL_EMERGENCY`

## 2. Tail Risk / Expected Shortfall layer
HCT should estimate loss beyond ordinary stop-based risk using stress-conditioned measures rather than one Gaussian VaR number.

Research constructs:
- `HCT Tail Loss Envelope (TLE)`;
- `HCT Expected Shortfall Surface (ESS)`;
- `HCT Survival Probability Floor (SPF)`.

Inputs may include:
- realized/forecast volatility;
- jump/gap history;
- liquidity collapse scenarios;
- correlated crypto beta;
- spread/slippage expansion;
- stop execution uncertainty;
- funding/fee stress;
- cross-margin contagion;
- exchange degradation;
- stablecoin/collateral stress.

Tail metrics may only tighten risk. They cannot expand hard ceilings.

## 3. Operational Margin Reserve
Introduce a deterministic `OperationalMarginReserve` that is unavailable for normal position sizing.

It covers plausible needs for:
- slippage beyond median assumptions;
- funding/fees;
- protection delays;
- partial-fill transitions;
- tier/MMR changes;
- cross-margin deterioration;
- emergency reduction/close;
- reconciliation uncertainty.

The reserve is separate from strategy opportunity budget. A strategy cannot consume it to increase size.

Research metric: `HCT Margin Survival Reserve Ratio (MSRR)`.

## 4. Protection Failure Exposure
A stop order is not equivalent to guaranteed realized loss.

Risk must model:
- trigger failure;
- rejected/expired protection;
- stale quantity after partial fill;
- adverse fill beyond stop;
- gap through stop;
- API/private-stream uncertainty;
- unsupported guaranteed-stop capability;
- exchange-side cancellation or rule changes.

Introduce `Protection Failure Exposure (PFE)` and `Protection Confidence State`:
- `PROTECTION_VERIFIED`
- `PROTECTION_DEGRADED`
- `PROTECTION_PARTIAL`
- `PROTECTION_UNKNOWN`
- `PROTECTION_FAILED`

New exposure can be denied when required protection confidence is below policy.

## 5. Pyramiding and add-to-position policy
Every ADD is a new risk decision. Existing unrealized profit does not create free risk automatically.

Rules:
1. re-run full RiskSnapshot for each add;
2. reserve incremental risk before submit;
3. recompute average entry, stop/invalidation, tier/MMR, liquidation corridor and portfolio concentration;
4. cap cumulative risk across all adds;
5. prohibit martingale/loss-recovery escalation by default;
6. prohibit adding solely because price moved against the position unless an explicitly approved strategy defines it and global risk policy permits it;
7. profitable adds must still respect risk-budget and liquidation constraints;
8. stale/uncertain protection blocks additional exposure.

Research metric: `HCT Incremental Risk Efficiency (IRE)` measuring incremental expected opportunity value versus incremental tail/margin/concentration risk.

## 6. Collateral concentration and stablecoin risk
HCT must distinguish trading PnL risk from collateral/counterparty risk.

Track:
- collateral asset composition;
- stablecoin concentration;
- depeg/price-dislocation risk;
- venue custody concentration;
- haircut/valuation uncertainty where applicable;
- multi-asset collateral correlations;
- withdrawal/operational incidents when relevant.

Research constructs:
- `Collateral Concentration Index (CCI)`;
- `Collateral Stress Haircut (CSH)`;
- `Effective Risk Capital (ERC)` = nominal equity adjusted by governed collateral stress haircuts.

Position sizing should use effective risk capital when collateral quality is degraded rather than blindly using nominal wallet equity.

## 7. Extreme venue mechanics: liquidation ladder and ADL
MEXC currently documents tiered/partial liquidation behavior and ADL as an extreme backstop when the insurance fund is insufficient. These are venue mechanics and must be treated as dynamic external dependencies rather than fixed constants.

HCT should maintain `ExtremeVenueRiskState` including:
- current risk tier;
- proximity to maintenance margin;
- partial-liquidation exposure;
- insurance-fund / venue-risk telemetry where observable;
- ADL indicator/ranking where observable;
- leverage/profit conditions associated with elevated ADL risk;
- current exchange announcements/rule observations;
- confidence/freshness.

Research metric: `HCT ADL Exposure Score (AES)`.

A high or unknown extreme-venue risk state may:
- reduce leverage;
- reduce position size;
- restrict new exposure;
- prefer isolated over cross margin where policy/strategy allows;
- trigger `REDUCE_ONLY` or `NO_NEW_EXPOSURE` under severe uncertainty.

## 8. User risk presets
The UI may offer presets such as:
- `CONSERVATIVE`
- `BALANCED`
- `AGGRESSIVE`
- `CUSTOM`

Presets are bundles of user-level ceilings, not authority to exceed platform limits. They may configure:
- max risk/trade;
- max daily loss;
- max drawdown;
- max portfolio exposure;
- leverage ceiling;
- concurrent positions;
- correlation concentration;
- survival reserve target;
- tail-risk tolerance;
- cross-margin policy;
- pyramiding allowance;
- news/event tolerance.

`AGGRESSIVE` still remains under global HCT hard safety ceilings.

## 9. Risk explainability contract
Every pre-trade decision should be able to explain at least:
- monetary risk;
- reserved risk;
- notional and leverage;
- initial/maintenance margin;
- current/projected risk tier;
- stop and liquidation corridor;
- tail-risk estimate;
- operational margin reserve remaining;
- cross-margin contagion;
- correlated portfolio exposure;
- collateral quality/concentration;
- protection confidence;
- survival-state impact;
- ADL/extreme-venue risk where observable;
- exact reason for size reduction, leverage reduction, WAIT or VETO.

No single composite score may hide a critical failed subcondition.

## 10. Validation and invariants
Required scenario tests include:
- correlated market crash;
- gap through stop;
- stop reject after fill;
- stablecoin depeg;
- large unrealized profit with high ADL exposure;
- partial liquidation path;
- cross-margin contagion cascade;
- three simultaneous pending orders;
- pyramiding across tier boundary;
- weekly loss budget exhausted while daily budget remains;
- operational reserve consumed by adverse execution;
- exchange risk-rule update during open position.

Invariants:
- tail-risk models cannot increase hard risk ceilings;
- operational margin reserve cannot be spent as normal opportunity risk;
- adding to a position always creates a new risk decision;
- uncertain protection cannot be treated as guaranteed protection;
- nominal equity cannot automatically equal effective risk capital under collateral stress;
- ADL/partial-liquidation mechanics are modeled as external venue risk, not ignored;
- higher-horizon survival guard may block trades even when trade-level risk appears acceptable.

## Current R03 status after this hardening
The previously identified CRITICAL gaps are architected in `docs/40-r03-institutional-risk-control-architecture.md`.
This document closes the principal HIGH architecture gaps around survival/tail/collateral/extreme venue mechanics. Remaining work before R03 approval should focus on consistency audit, acceptance criteria, requirements/decision-ledger alignment and objective round review.
