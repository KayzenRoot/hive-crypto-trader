# Execution Intelligence, OMS, Reconciliation & Recovery

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R02`
Risk class: `HIGH_ASSURANCE`

## Objective
Once a candidate trade passes Strategy, Copilot, Safety, Risk, Session Policy, Position Sizing and Leverage constraints, HCT must convert the approved intent into exchange actions without corrupting the thesis through avoidable slippage, duplicate orders, stale assumptions, partial-fill confusion or uncertain exchange state.

Execution is not a transport detail. It is a first-class decision and safety domain.

## Core rule
`Approved trade intent != successful exchange execution`.

HCT must distinguish:
- intended action;
- submitted action;
- exchange-accepted action;
- partially filled action;
- fully filled action;
- cancelled/rejected action;
- uncertain action;
- reconciled final state.

No component may infer a fill merely because a request returned without a local error.

## Execution decision chain
Conceptual flow:

`Approved Order Intent -> Execution Feasibility -> Order Plan -> Preflight -> Submit -> Exchange Ack -> Fill/Order Events -> OMS -> Reconciliation -> Position State -> Protective Order Verification`

Any uncertain state can interrupt the chain and trigger recovery/no-new-exposure behavior.

## Canonical Order Intent
Before exchange translation, create an immutable canonical Order Intent containing at least:
- tenant/account;
- exchange/market/instrument;
- strategy/version;
- signal/candidate id;
- session-policy snapshot id;
- side/direction;
- intent type: OPEN/ADD/REDUCE/CLOSE/PROTECT/CANCEL/REPLACE;
- target quantity/notional;
- maximum approved risk;
- leverage/margin constraints;
- desired price behavior;
- allowed order types/time-in-force;
- stop/TP/trailing requirements;
- slippage budget;
- expiration/deadline;
- execution priority;
- idempotency/correlation id;
- source authority/provenance.

Exchange-specific payloads are derived from this object and never replace its audit identity.

## Execution Feasibility Engine
Before submission, evaluate whether the approved intent remains executable under current conditions.

Candidate checks:
- market still within entry thesis/time window;
- spread within limit;
- order-book depth/liquidity sufficient;
- estimated slippage within budget;
- exchange/API/WS health acceptable;
- symbol/contract status unchanged;
- quantity/price increments valid;
- min/max order constraints satisfied;
- margin remains sufficient;
- portfolio/risk still valid after latency since approval;
- protective-order capability available;
- no conflicting/duplicate order already active;
- data freshness acceptable.

If conditions have materially changed, the result is re-price/re-plan/re-approve or abort, not blind submission.

## HCT Execution Quality Score (EQS)
Research/operational metric describing how suitable current conditions are for executing a specific approved intent.

Candidate dimensions:
- spread quality;
- visible depth;
- short-horizon volatility;
- book imbalance/stability;
- expected market impact;
- API/WS health;
- quote freshness;
- latency budget;
- historical fill quality for similar conditions;
- urgency versus signal half-life.

EQS is not a market-direction signal. It may delay/reject an entry if execution quality is inadequate.

## HCT Slippage Budget
Every Order Intent should have a governed slippage budget derived from strategy horizon, expected edge, liquidity, volatility and user/platform policy.

Slippage budget may be represented in price, bps, ticks or risk currency, but the canonical value must be unambiguous.

Hard rule: Execution logic cannot consume unlimited slippage to force a fill. If the budget is exhausted, it must stop, re-evaluate or escalate according to policy.

## HCT Fill Probability & Impact Model
Research model estimating likely fill quality for candidate order types/price levels.

Potential outputs:
- fill probability over a time window;
- expected fill latency;
- expected partial-fill probability;
- expected slippage;
- expected market impact;
- cancellation/reprice likelihood.

This model may choose among policy-approved execution tactics but cannot increase position risk.

## Order Mutation Planner
Execution may adapt an order while preserving the approved trade intent.

Examples:
- limit price adjustment inside allowed bounds;
- cancel/replace;
- split parent order into children;
- switch from passive to more aggressive approved tactic as signal expiry approaches;
- stop attempting when edge/slippage budget deteriorates.

Every mutation must preserve:
- same parent intent/correlation id;
- versioned reason;
- before/after parameters;
- consumed slippage/latency budget;
- no increase beyond approved quantity/risk.

The planner may not silently convert a conservative intent into an unrestricted market order.

## Child Orders / Execution Slicing
For appropriate size/liquidity conditions, HCT may split one parent intent into child orders.

Potential tactics:
- passive limit slicing;
- time-sliced execution;
- liquidity-aware slices;
- bounded urgency escalation.

V1 does not require institutional algorithm names or complex smart-order routing across exchanges because live scope is MEXC-only. The architecture should nevertheless support future venue-aware routing without changing the canonical parent-intent model.

## Partial Fill State Machine
Partial fills are normal and must be modeled explicitly.

Candidate states:
`CREATED -> PREFLIGHTED -> SUBMITTING -> ACKNOWLEDGED -> PARTIALLY_FILLED -> FILLED`

Alternative terminal/intermediate states:
`REJECTED`, `CANCEL_PENDING`, `CANCELLED`, `EXPIRED`, `REPLACE_PENDING`, `UNCERTAIN`, `RECONCILING`.

Partial fill handling must re-evaluate:
- remaining quantity;
- remaining risk budget;
- current market conditions;
- minimum viable position;
- protective order coverage for already-filled quantity;
- whether continuing still matches signal validity.

## Protective Order Integrity Monitor
Opening exposure is not complete until required protective behavior is verified.

Monitor:
- stop order exists/accepted where strategy/policy requires;
- TP orders exist where required;
- protective quantity matches actual filled exposure;
- reduce-only semantics where applicable;
- trigger price/type is correct;
- trailing parameters are correct;
- protection survives partial fills/order amendments;
- exchange-side cancellation/rejection is detected;
- protection remains valid after leverage/margin/position changes.

If required protection cannot be established, policy may forbid further exposure and initiate reduction/closure depending on risk state.

## HCT Protective Coverage Ratio (PCR)
Operational metric:
`verified protected exposure / total exposure requiring protection`.

Example states:
- `FULLY_PROTECTED`
- `PARTIALLY_PROTECTED`
- `UNPROTECTED`
- `UNKNOWN`

For strategies/policies requiring exchange-side protection, `UNKNOWN` is unsafe and must trigger escalation.

## OMS source of lifecycle truth
The OMS maintains the internal event-sourced lifecycle of order intents and exchange orders while acknowledging that the exchange remains authoritative about actual orders/fills/positions.

The OMS must support:
- parent/child relationships;
- idempotency;
- duplicate detection;
- client/exchange order identifiers;
- partial fills;
- amendments/cancel-replace;
- rejected/expired orders;
- late/out-of-order events;
- uncertain submission outcomes;
- protective-order relationships;
- immutable event history.

## Idempotency & duplicate prevention
Every state-changing execution request requires a stable internal correlation/idempotency identity wherever the exchange capability allows.

Before retrying an uncertain submission, HCT must first determine whether the exchange already accepted it whenever possible. Retrying blindly can create duplicate exposure.

## Unknown Outcome Protocol
Example: network timeout after submitting an order.

The system must not classify this as failed.

Required behavior:
1. mark intent/order as `UNCERTAIN`;
2. block unsafe duplicate retry;
3. query/reconcile using client/exchange identifiers, orders, fills and position delta;
4. infer only from corroborated exchange evidence;
5. resolve to ACKNOWLEDGED/PARTIAL/FILLED/REJECTED/CANCELLED or remain uncertain;
6. if unresolved beyond governed threshold, restrict new exposure and escalate.

## Reconciliation Engine
Reconciliation compares local projections with exchange-authoritative state.

Domains:
- open orders;
- recent/late fills;
- positions;
- position size/side;
- average entry where available;
- leverage/margin mode;
- balance/equity/margin;
- protective orders;
- liquidation-related state where available.

Reconciliation must run both event-driven and periodically as an independent safety mechanism.

## HCT State Confidence Index (SCI)
Operational metric estimating confidence that local order/position/account state matches the exchange.

Inputs may include:
- freshness of private streams;
- last successful REST reconciliation;
- unresolved order states;
- sequence/event gaps;
- timestamp drift;
- inconsistent position/order evidence;
- API health.

Candidate states:
`CONFIRMED`, `HIGH_CONFIDENCE`, `DEGRADED`, `UNCERTAIN`, `UNSAFE`.

New exposure can require a minimum state-confidence threshold.

## Execution Shadow Simulator
Before or alongside production, simulate alternative approved execution tactics against captured/replay order-book/trade data.

Purpose:
- compare limit versus market-like tactics;
- estimate execution cost;
- validate mutation policies;
- test partial-fill handling;
- evaluate slippage budgets;
- improve execution models without experimenting recklessly with production money.

Simulation assumptions must be explicit; queue position and fill realism are non-trivial and cannot be treated as exact.

## HCT Execution Drift Monitor
Detect whether actual execution quality has deteriorated relative to validated baselines.

Candidate evidence:
- slippage distribution shift;
- fill latency shift;
- rejection/cancel rates;
- partial-fill frequency;
- API latency;
- spread/depth regime changes;
- discrepancy between predicted and actual fill quality.

Drift can lower aggression, reduce size via downstream re-approval, disable tactics or trigger review. It cannot increase approved risk.

## Recovery modes
Candidate operational states:
- `NORMAL`
- `EXECUTION_DEGRADED`
- `NO_NEW_ORDERS`
- `REDUCE_ONLY`
- `RECONCILIATION_ONLY`
- `PROTECTION_RECOVERY`
- `EXCHANGE_UNCERTAIN`
- `EMERGENCY`

Recovery prioritizes knowing actual exchange state and preserving/reducing exposure over opening new trades.

## Crash/restart recovery
After process restart/deployment/failover:
1. do not trust cached local execution state;
2. reload durable intent/OMS event history;
3. query/rebuild exchange-authoritative open orders/positions/account state;
4. match unresolved intents/orders;
5. verify protective coverage;
6. compute State Confidence Index;
7. only resume new exposure after recovery gates pass.

## Observability
Execution cockpit/telemetry should expose:
- parent intent and child orders;
- expected vs actual fill;
- slippage budget and consumed slippage;
- execution quality;
- partial fill progress;
- order latency;
- protective coverage;
- reconciliation age;
- state confidence;
- unresolved/uncertain orders;
- duplicate-prevention events;
- exchange/API health;
- recovery mode.

## Safety boundaries
Execution intelligence may optimize how an already-approved action is performed, but cannot:
- create a new directional thesis;
- exceed approved quantity/risk;
- raise leverage;
- bypass Safety/Risk/Session Policy;
- continue past hard slippage limits without re-approval;
- infer fills without exchange evidence;
- hide partial/uncertain states;
- retry uncertain orders blindly;
- remove required protective behavior.
