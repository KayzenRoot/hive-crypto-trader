# Agentic Copilot Architecture

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R02`
Risk class: `HIGH_ASSURANCE`

## Product intent
Hive Crypto Trader will include a Copilot operating mode in which the system may autonomously analyze markets and manage the trading lifecycle within user-approved and platform-enforced constraints.

Copilot autonomy may include, once implementation is separately authorized and promotion gates are passed:
- market scanning and opportunity selection;
- long/short candidate generation;
- entry execution;
- take-profit and stop-loss placement/adjustment;
- trailing-stop management;
- partial profit taking and position reduction;
- order cancellation/replacement;
- position close;
- pausing new exposure;
- intraday mode changes based on approved policies;
- no-trade decisions.

Copilot must never be equivalent to unrestricted model access to exchange credentials. It operates through deterministic policy, risk, safety and execution boundaries.

## User-defined operating envelope
Before enabling Copilot, the user/tenant configures a governed operating envelope. Candidate controls include:
- maximum daily loss in absolute and/or percentage terms;
- optional daily profit target or open-ended profit mode;
- maximum risk per trade;
- maximum simultaneous positions;
- maximum portfolio exposure;
- leverage ceiling and policy;
- allowed/blocked symbols or market classes;
- allowed strategy profiles;
- allowed operating hours/session windows;
- news/event sensitivity profile;
- volatility tolerance;
- liquidity/spread thresholds;
- maximum drawdown from intraday high-water mark;
- cooldown after consecutive losses;
- maximum order frequency;
- manual emergency stop and immediate no-new-trades control.

User settings can only reduce or constrain risk beyond platform hard limits. Tenant settings may not exceed platform/global safety ceilings.

## Agent topology
The Copilot should be designed as a supervised multi-agent system rather than one unrestricted agent.

Candidate agents:
1. **Market Scout Agent** — ranks symbols and market conditions.
2. **Technical Analyst Agent** — interprets indicators, patterns and multi-timeframe context.
3. **Regime & Cycle Agent** — assesses volatility, trend/range, liquidity and broader cycle context.
4. **Memory/RAG Agent** — retrieves relevant historical analogues, prior failures and symbol-specific context.
5. **Strategy Agent** — evaluates strategy-specific setup quality.
6. **Risk Agent** — computes risk proposal but cannot override deterministic Risk Engine hard limits.
7. **Execution Planner Agent** — proposes order type, entry, TP/SL, trailing and scale-in/out actions.
8. **Position Manager Agent** — monitors open positions and proposes management actions.
9. **News/Event Context Agent** — provides event-risk context when an approved source is available.
10. **Adversarial/Devil's Advocate Agent** — attempts to disprove the proposed trade before execution.
11. **Supervisor/Decision Agent** — synthesizes agent evidence into a candidate action and confidence score.
12. **Post-Trade Review Agent** — analyzes outcome and writes structured learning episodes.

## Decision contract
Agents do not directly call exchange order endpoints.

`Agents -> Supervisor -> Candidate Action -> Safety Governor -> Risk Engine -> Policy Engine -> Execution Engine -> Exchange -> Reconciliation`

A candidate action must include proposed action, symbol/timeframe, strategy/model versions, supporting and conflicting evidence, calibrated confidence, size/leverage request, TP/SL/trailing proposal, invalidation conditions, relevant memory references, market regime, execution/liquidity concerns and policy/risk assumptions.

## Authority hierarchy
1. Exchange constraints.
2. Platform Safety Governor.
3. Platform Risk Engine hard limits.
4. Tenant/user operating envelope.
5. Strategy hard rules.
6. Copilot supervisor recommendation.
7. Individual agent recommendations.

Lower layers cannot override higher layers.

## Autonomy modes
- `OFF`: manual trading/analysis only.
- `ADVISORY`: Copilot analyzes and proposes, user confirms execution.
- `GUARDED_AUTOPILOT`: Copilot executes within a narrow approved envelope.
- `FULL_COPILOT`: autonomous lifecycle management within all configured hard limits.

Each mode must be visibly distinct and auditable.

## Daily session contract
When Copilot starts a trading session, create an immutable session policy snapshot containing user limits, platform limits, strategies, model versions, enabled agents, symbol universe, news/volatility policy and account state. Live behavior must be attributable to that snapshot.

## Fail-safe behavior
If exchange state becomes uncertain, data freshness is insufficient, reconciliation fails, limits cannot be evaluated, an agent/model is unavailable, or safety checks disagree, the default is no new exposure and controlled degraded-state handling.

## No guarantee rule
Autonomy does not imply profitability. Copilot quality is measured using risk-adjusted return, drawdown, calibration, execution quality, reliability and safety metrics, not raw profit alone.
