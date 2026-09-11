# Risk Intelligence, Position Sizing, Leverage & Daily Equity Guard

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R02`
Risk class: `HIGH_ASSURANCE`

## Objective
HCT must treat risk construction as a primary decision domain rather than a final percentage check. After an opportunity exists, the system must determine whether new exposure is acceptable, how much risk can be allocated, how leverage affects liquidation/survivability, where the thesis is invalidated, and how the trade interacts with existing portfolio risk.

## Authority model
The deterministic Risk Engine remains authoritative. Agents and learned models may propose tighter constraints or improved estimates but cannot relax platform/user hard ceilings.

Conceptual chain:
`Candidate Opportunity -> Risk Intelligence -> Portfolio Exposure -> Position Sizing -> Leverage Constraints -> Daily Equity Guard -> Safety/Policy -> Execution`

## Risk budget hierarchy
Candidate hierarchy:
1. platform hard limits;
2. tenant/account limits;
3. daily/session risk budget;
4. portfolio risk budget;
5. strategy budget;
6. symbol/correlation-cluster budget;
7. individual trade risk;
8. execution/liquidity adjustment.

Lower layers cannot exceed higher-layer budgets.

## Daily Equity Guard
The Daily Equity Guard protects the session/account from loss escalation and profit giveback.

Candidate controls:
- hard daily maximum loss;
- soft warning threshold;
- max intraday drawdown from session high-water mark;
- consecutive-loss cooldown;
- optional profit target;
- optional stop-at-target;
- reduce-risk-after-target mode;
- trailing daily profit lock;
- no-target/open-target mode;
- max realized + unrealized loss envelope;
- emergency no-new-exposure state.

A profit target must never cause the system to increase leverage or trade frequency merely to reach the target.

## HCT Adaptive Risk Budget Surface
Research concept: instead of one fixed risk-per-trade number, calculate an explainable permissible-risk surface conditioned on:
- data quality;
- market regime;
- volatility;
- liquidity;
- strategy calibration;
- signal independence;
- execution conditions;
- portfolio correlation;
- current drawdown;
- event/news risk;
- opportunity persistence;
- liquidation distance.

The adaptive surface can only reduce or allocate inside approved hard ceilings unless an explicit future policy says otherwise.

## Position sizing
Position size should derive from approved monetary risk and invalidation distance rather than leverage-first thinking.

Conceptually:
`position risk budget / effective stop risk -> base size -> liquidity/execution adjustment -> portfolio/correlation adjustment -> leverage/collateral validation`

Required inputs may include:
- equity/balance state;
- approved risk amount;
- stop/invalidation distance;
- contract precision/minimums;
- fee/funding assumptions;
- expected slippage;
- volatility;
- liquidity/depth;
- current exposure;
- correlation cluster exposure;
- strategy/symbol limits.

## Leverage Engine
Leverage is an implementation/collateral parameter subordinate to survivability and risk.

The engine must distinguish:
- notional exposure;
- margin/collateral committed;
- monetary risk to stop;
- liquidation distance;
- maintenance margin constraints;
- mark/fair-price behavior as exchange-defined;
- exchange leverage tiers/caps.

High leverage is not automatically high monetary risk if sizing is small, but it can reduce liquidation tolerance and amplify operational failure consequences. Therefore leverage is constrained by both monetary risk and liquidation-defense rules.

## HCT Liquidation Defense Distance (LDD)
Research/operational metric measuring buffer between planned invalidation/protective exits and exchange liquidation mechanics under adverse movement, slippage, fees/funding and uncertainty.

Possible states:
- `SAFE_BUFFER`
- `THIN_BUFFER`
- `UNACCEPTABLE`
- `UNKNOWN_EXCHANGE_STATE`

No new position should be authorized when liquidation safety cannot be evaluated reliably.

## HCT Margin Fragility Score (MFS)
Research metric estimating how vulnerable a proposed/open position is to collateral stress or operational failure.

Candidate factors:
- liquidation distance;
- leverage;
- volatility;
- gap/jump risk;
- order-book depth;
- protective-order reliability;
- correlated losses;
- margin-mode constraints;
- exchange/reconciliation health.

## Portfolio correlation and hidden concentration
The portfolio must not treat different tickers as independent simply because their names differ.

Risk analysis should estimate:
- rolling/conditional correlations;
- common BTC/ETH beta;
- sector/theme clusters;
- stablecoin/counterparty dependencies;
- strategy correlation;
- direction concentration;
- liquidity concentration;
- shared-event risk.

## HCT Correlated Exposure Equivalent (CEE)
Research representation that converts nominal positions into an estimated effective common-factor exposure.

Example concept:
`5 separate altcoin longs` may behave like `one large crypto-beta long` under stress.

CEE helps prevent accidental leverage stacking across correlated symbols.

## HCT Portfolio Stress Lattice
Instead of one stress case, test a lattice of plausible shocks, for example:
- BTC -2/-5/-10%;
- volatility doubles;
- liquidity/depth falls;
- spread widens;
- correlated altcoins move more than BTC;
- exchange API degrades;
- protective fills slip;
- news shock occurs.

The goal is not perfect prediction but identification of fragile combinations before entry.

## Stop/invalidation architecture
Separate:
- thesis invalidation level;
- protective hard stop;
- execution buffer;
- volatility stop;
- structural stop;
- time stop;
- trailing logic;
- emergency/safety close.

A strategy may propose semantics, but Risk/Safety can require stricter protection.

## HCT Stop Quality Score (SQS)
Research metric evaluating whether a stop is structurally meaningful and operationally executable rather than arbitrarily close/far.

Candidate inputs:
- market structure;
- volatility;
- expected noise;
- spread/slippage;
- liquidity vacuum risk;
- historical excursion distribution;
- liquidation distance;
- strategy thesis.

## Drawdown-state machine
Candidate account/session states:
- `NORMAL`
- `CAUTION`
- `RISK_REDUCED`
- `NO_NEW_EXPOSURE`
- `RECOVERY_ONLY`
- `EMERGENCY`

Transitions use deterministic policy and audited inputs. Agents can recommend transitions but cannot secretly weaken them.

## Profit protection modes
User-selectable modes may include:
- `NO_DAILY_TARGET`
- `STOP_AT_TARGET`
- `REDUCE_RISK_AFTER_TARGET`
- `TRAIL_SESSION_HIGH_WATER_MARK`
- `LOCK_MINIMUM_PROFIT_AFTER_TARGET`

All modes preserve the daily max-loss hard floor.

## Risk explainability
Before a trade, the UI should be able to explain:
- proposed monetary risk;
- notional size;
- leverage;
- stop/invalidation;
- liquidation buffer;
- expected slippage/fees;
- portfolio correlation impact;
- risk budget consumed/remaining;
- daily loss/profit guard state;
- main stress scenarios;
- reason for any risk reduction or veto.

## Safety rules
No component may:
- increase total risk because multiple strategies agree;
- increase risk to recover losses;
- increase risk to hit a profit target;
- assume diversification from highly correlated crypto assets without evidence;
- treat leverage as a substitute for position sizing;
- authorize a trade when exchange margin/liquidation state is unknown;
- let an AI agent override deterministic risk limits.
