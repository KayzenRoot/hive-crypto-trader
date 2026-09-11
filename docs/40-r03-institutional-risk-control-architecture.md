# HCT-PLAN-0001-R03 — Institutional Risk Control Architecture

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R03`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

## Objective
Close the highest-severity R03 gaps by defining the deterministic risk-control architecture for:
- dynamic venue risk tiers / maintenance margin;
- post-trade liquidation preview;
- cross-margin contagion;
- risk reservation across pending/partial/uncertain orders;
- immutable risk snapshots;
- risk approval expiry and revalidation.

This architecture is planning-only and does not authorize implementation or live trading.

---

# 1. Risk authority model

Canonical authority order:

1. platform hard safety/risk ceilings;
2. exchange/contract constraints;
3. tenant/account policy ceilings;
4. session/day/multi-horizon equity guards;
5. portfolio/common-factor/tail-risk limits;
6. strategy/symbol/correlation-cluster limits;
7. trade-level monetary risk;
8. execution/liquidity adjustments.

No lower layer can expand authority granted by a higher layer.

AI, agents, RAG, strategies and learned models may:
- propose risk estimates;
- recommend tighter limits;
- identify hidden risks;
- request revalidation;
- recommend WAIT/VETO/REDUCE.

They may not:
- raise hard ceilings;
- alter exchange constraints;
- release risk reservations;
- declare an uncertain order cancelled;
- change margin mode silently;
- bypass deterministic risk state.

---

# 2. Canonical Risk Snapshot

Every candidate action that can change exposure must be evaluated against an immutable `RiskSnapshot`.

Minimum conceptual fields:

## Identity
- `risk_snapshot_id`;
- `tenant_id`;
- `account_id`;
- `exchange_id`;
- `instrument_id`;
- `candidate_action_id`;
- `strategy_version_id`;
- `session_policy_snapshot_id`;
- `market_state_generation_id`;
- `portfolio_state_generation_id`;
- `exchange_state_generation_id`;
- `created_at`;
- `expires_at`;
- `snapshot_hash`.

## Account/equity state
- wallet balance;
- equity;
- available margin;
- used margin;
- maintenance margin;
- unrealized PnL;
- realized session/day PnL;
- reserved risk;
- current drawdown;
- high-water mark;
- reconciliation confidence.

## Position state
- current position side/size/notional;
- average entry;
- margin mode;
- current leverage;
- current risk tier;
- current maintenance-margin rate;
- current liquidation reference/price if available/derivable;
- current protection state;
- current stop/invalidation state.

## Proposed post-trade state
- intent type: OPEN / ADD / REDUCE / CLOSE / PROTECT;
- requested size;
- approved size;
- projected position size/notional;
- projected risk tier;
- projected maximum leverage;
- projected maintenance-margin rate;
- projected initial margin;
- projected maintenance margin;
- projected liquidation reference/price;
- projected liquidation buffer;
- projected monetary risk to approved invalidation/protection;
- projected fees/funding reserve;
- projected execution/slippage reserve;
- projected portfolio/common-factor exposure.

## Policy state
- hard platform limits version;
- tenant/account policy version;
- session policy version;
- strategy risk policy version;
- exchange risk-rule observation timestamp/version where available;
- data freshness/confidence;
- risk decision;
- veto/reduction reasons.

Execution must consume the exact snapshot ID/hash or trigger risk revalidation.

---

# 3. Dynamic Exchange Risk Rule Resolver

Introduce a deterministic `ExchangeRiskRuleResolver` behind the exchange adapter contract.

Responsibilities:
- retrieve/normalize current contract risk tiers;
- determine position-size tier boundaries;
- determine maximum leverage by tier;
- determine maintenance-margin rate by tier;
- determine relevant position limits;
- determine supported margin modes;
- expose liquidation trigger reference semantics;
- expose fees/charges relevant to margin/liquidation where available;
- timestamp all observations;
- report unavailable/unknown fields explicitly.

Canonical normalized conceptual output:

```text
ExchangeRiskRules {
  exchange
  instrument
  observed_at
  margin_modes[]
  liquidation_trigger_reference
  tiers[] {
    min_position
    max_position
    max_leverage
    maintenance_margin_rate
    other_constraints
  }
  rule_confidence
  source_provenance
}
```

No strategy may hard-code a leverage ceiling as exchange truth.

---

# 4. Tier Transition Risk Engine

A candidate order can alter its own risk tier.

The `TierTransitionRiskEngine` evaluates:
- current tier;
- projected tier after full fill;
- projected tiers after plausible partial fills;
- new maintenance-margin requirement;
- reduced maximum leverage;
- position-limit proximity;
- whether requested leverage remains legal after transition;
- whether liquidation buffer deteriorates materially.

Canonical outcomes:
- `NO_TIER_CHANGE`;
- `TIER_CHANGE_SAFE`;
- `TIER_CHANGE_REDUCE_SIZE`;
- `TIER_CHANGE_REDUCE_LEVERAGE`;
- `TIER_CHANGE_VETO`;
- `TIER_STATE_UNKNOWN`.

Research metric: **HCT Tier Transition Risk (TTR)**.

---

# 5. Post-Trade Liquidation Preview Engine

Risk approval operates on projected post-trade state, not current state alone.

`PostTradeLiquidationPreview` should evaluate at minimum:

### Isolated margin
- projected initial margin;
- projected maintenance margin;
- projected liquidation point/reference;
- stop/invalidation versus liquidation distance;
- slippage/gap/protection reserve;
- margin additions only if explicitly allowed by policy, never assumed.

### Cross margin
- shared wallet/equity;
- all current cross positions;
- all current cross-position unrealized PnL;
- open-order margin usage;
- projected new order/position impact;
- correlated stress effects;
- other cross positions' effect on liquidation state.

Preview result is not a promise of the future. It is a risk estimate with confidence/uncertainty.

Canonical states:
- `LIQUIDATION_BUFFER_STRONG`;
- `LIQUIDATION_BUFFER_ACCEPTABLE`;
- `LIQUIDATION_BUFFER_THIN`;
- `LIQUIDATION_BUFFER_UNACCEPTABLE`;
- `LIQUIDATION_STATE_UNKNOWN`.

Unknown => no new exposure.

---

# 6. Liquidation Buffer Confidence Interval

A single liquidation price can create false precision.

Research construct: **HCT Liquidation Buffer Confidence Interval (LBCI)**.

Instead of only:
`liquidation price = X`

estimate a corridor considering:
- exchange-rule uncertainty;
- maintenance-margin tier changes;
- fees/funding;
- slippage;
- cross-margin equity changes;
- market gaps;
- reconciliation delay;
- other open positions.

The lower-confidence bound must still satisfy platform safety policy.

---

# 7. Stop-to-Liquidation Safety Corridor

Research construct: **HCT Stop-to-Liquidation Safety Corridor (SLSC)**.

Measure the protected corridor between:
- strategy thesis invalidation;
- hard protective stop;
- expected adverse fill region;
- liquidation boundary.

A safe corridor must remain positive after conservative execution and stress assumptions.

Possible states:
- `WIDE_SAFE`;
- `SAFE`;
- `THIN`;
- `OVERLAP_RISK`;
- `INVALID`;
- `UNKNOWN`.

If stop/protection and liquidation regions overlap under plausible stress, new exposure is vetoed or resized/releveraged.

---

# 8. Cross-Margin Contagion Guard

Introduce deterministic `CrossMarginContagionGuard`.

It evaluates how one proposed/open position can consume shared collateral and increase liquidation risk of others.

Inputs:
- wallet/equity;
- all cross positions;
- unrealized PnL;
- maintenance margin by position/tier;
- open-order margin;
- correlation/common-factor exposure;
- stress scenarios;
- collateral asset risk;
- data/reconciliation confidence.

Research metric: **HCT Cross-Margin Contagion Index (CMCI)**.

Conceptual behavior:
- one isolated low-risk-looking trade may be vetoed if it materially destabilizes shared cross collateral;
- correlated positions must be stressed together;
- unknown cross position/equity state blocks new exposure.

States:
- `CONTAGION_LOW`;
- `CONTAGION_MODERATE`;
- `CONTAGION_HIGH`;
- `CONTAGION_CRITICAL`;
- `CONTAGION_UNKNOWN`.

---

# 9. Risk Reservation Ledger

Introduce a deterministic, auditable **Risk Reservation Ledger (RRL)**.

Purpose: prevent risk overbooking before exchange fills are known.

A candidate that may increase exposure reserves risk **before submission**.

Conceptual reservation lifecycle:

`REQUESTED -> RESERVED -> SUBMITTED -> PARTIALLY_CONSUMED -> CONSUMED | RELEASE_PENDING -> RELEASED`

Exceptional states:
- `UNCERTAIN`;
- `RECONCILING`;
- `QUARANTINED`.

## Reservation rules
1. reserve before order submit;
2. reservation includes full plausible approved exposure unless policy explicitly supports staged reservation;
3. partial fills convert only the filled portion from reserved to open-position risk;
4. remaining unfilled portion stays reserved while order remains active/uncertain;
5. cancel request does not release reservation;
6. reservation releases only after exchange-confirmed cancellation/rejection/expiry or authoritative reconciliation;
7. network timeout after submit retains reservation;
8. duplicate/idempotent intents reference the same reservation where appropriate;
9. reservation itself has immutable audit history;
10. reservation cannot be manually removed by an agent/strategy.

---

# 10. Risk budget accounting model

Canonical risk categories:

- `REALIZED_LOSS_USED`;
- `OPEN_POSITION_RISK`;
- `PENDING_RESERVED_RISK`;
- `UNCERTAIN_ORDER_RISK`;
- `CONTINGENT_PROTECTIVE_GAP_RISK`;
- `CORRELATED_PORTFOLIO_RISK`;
- `TAIL_STRESS_RISK`;
- `COLLATERAL_RISK`.

The system should expose both:
- direct additive budget usage where mathematically appropriate; and
- non-additive portfolio/tail-risk measures where simple summation would mislead.

Never sum correlated-model estimates blindly as independent risks.

---

# 11. Risk Approval Half-Life

Introduce **HCT Risk Approval Half-Life (RAHL)**.

Every risk approval has an expiry based on:
- strategy horizon;
- signal half-life;
- volatility;
- liquidity;
- data freshness;
- portfolio change rate;
- exchange-rule freshness;
- account/reconciliation confidence;
- event/news risk.

Risk snapshot becomes stale immediately if certain invalidating events occur, regardless of clock TTL.

---

# 12. Risk revalidation triggers

Mandatory revalidation before execution/new exposure when any configured material trigger occurs:

## Market triggers
- price moves beyond tolerance;
- volatility regime changes;
- spread/depth deteriorates;
- liquidity vacuum appears;
- market-data integrity degrades;
- signal freshness/half-life threshold crossed.

## Account/portfolio triggers
- equity/wallet changes materially;
- another fill occurs;
- another order reserves/releases risk;
- correlated exposure changes;
- drawdown/equity-guard state changes;
- collateral state changes.

## Exchange triggers
- risk tier/rules change;
- maximum leverage changes;
- maintenance margin changes;
- margin mode changes;
- reconciliation confidence degrades;
- private stream gap/uncertainty appears.

## Policy triggers
- session policy changes;
- kill switch/harness state changes;
- strategy/model version changes;
- risk policy version changes.

---

# 13. Risk Snapshot State Machine

Candidate state machine:

`BUILDING`
`-> VALIDATING_EXCHANGE_STATE`
`-> VALIDATING_PORTFOLIO`
`-> VALIDATING_MARGIN`
`-> VALIDATING_BUDGET`
`-> APPROVED | APPROVED_REDUCED | WAIT_REVALIDATION | VETO`

After approval:

`APPROVED -> RESERVED -> EXECUTION_PENDING -> ACTIVE_POSITION_RISK`

Invalidation branches:
- `STALE`;
- `EXCHANGE_RULE_CHANGED`;
- `PORTFOLIO_CHANGED`;
- `ACCOUNT_CHANGED`;
- `DATA_UNCERTAIN`;
- `RECONCILIATION_UNCERTAIN`;
- `POLICY_CHANGED`.

An invalidated snapshot cannot be used to open new exposure.

---

# 14. Risk decisions and reasons

Canonical result envelope should contain:
- decision;
- approved size;
- approved leverage ceiling/selected leverage;
- approved monetary risk;
- required margin mode;
- risk snapshot ID/hash;
- reservation ID if created;
- expiry/revalidation conditions;
- warnings;
- veto/reduction reason codes;
- explainability payload.

Candidate decision codes:
- `RISK_APPROVED`;
- `RISK_APPROVED_REDUCED_SIZE`;
- `RISK_APPROVED_REDUCED_LEVERAGE`;
- `RISK_WAIT_REVALIDATION`;
- `RISK_VETO_BUDGET`;
- `RISK_VETO_TIER_TRANSITION`;
- `RISK_VETO_MARGIN_MODE`;
- `RISK_VETO_LIQUIDATION_BUFFER`;
- `RISK_VETO_CROSS_MARGIN_CONTAGION`;
- `RISK_VETO_PORTFOLIO_CONCENTRATION`;
- `RISK_VETO_DATA_UNCERTAIN`;
- `RISK_VETO_EXCHANGE_STATE_UNCERTAIN`;
- `RISK_NO_NEW_EXPOSURE`;
- `RISK_REDUCE_ONLY`;
- `RISK_EMERGENCY`.

---

# 15. Integration with OMS / execution

Risk and execution share a strict contract:

1. Risk creates approved snapshot and reservation.
2. Execution references snapshot/reservation IDs.
3. Pre-submit execution preflight confirms snapshot still valid.
4. Submit does not release reservation.
5. Exchange ACK/fill events flow to OMS.
6. OMS updates RRL deterministically.
7. Partial fills split reserved/open risk.
8. Cancel request retains reservation until confirmed.
9. Timeout => `UNCERTAIN`; reservation remains locked.
10. Reconciliation resolves final order/position state.
11. Risk state updates only from authoritative/reconciled evidence.

This prevents the classic failure mode where a timed-out order is assumed failed and risk is reused for a duplicate order.

---

# 16. Integration with Safety Governor

Risk approval is necessary but not sufficient.

Safety Governor may still veto because of:
- stale/untrusted market data;
- exchange degradation;
- reconciliation uncertainty;
- API/WS instability;
- protection integrity;
- abnormal spread/liquidity;
- global/tenant emergency controls;
- security/incidents.

Risk Engine cannot override Safety Governor.

Safety Governor cannot silently expand Risk Engine approval.

---

# 17. Continuous open-position risk monitoring

After entry, risk control remains active.

Monitor:
- live margin mode;
- current tier/MMR;
- liquidation distance/buffer;
- equity/drawdown;
- funding/fees;
- protection coverage;
- correlated exposure;
- cross-margin contagion;
- reconciliation confidence;
- market liquidity/volatility;
- collateral/stablecoin state;
- exchange risk-rule changes.

Risk responses can include:
- maintain;
- tighten no-new-exposure;
- reduce size;
- reduce leverage where safe/possible;
- strengthen protection;
- reduce-only mode;
- emergency close recommendation through deterministic execution path.

---

# 18. Validation requirements

Before production promotion, test at minimum:

## Unit/property testing
- tier boundary calculations;
- risk reservation conservation;
- no double release;
- no negative available risk;
- no stale snapshot execution;
- margin-mode mismatch;
- snapshot hash/version integrity.

## Scenario tests
- position crosses tier after partial fill;
- leverage becomes illegal after tier change;
- MMR changes between risk approval and submit;
- cross-margin second position creates contagion;
- concurrent orders overbook budget;
- timeout after submit;
- late cancel ACK;
- duplicated private events;
- reconciliation resolves previously uncertain order;
- stop exists but projected liquidation corridor becomes unsafe;
- account equity changes during order lifecycle.

## Stress/replay
- high-volatility burst;
- liquidity collapse;
- correlated crypto crash;
- stablecoin stress;
- exchange data degradation;
- simultaneous multi-position loss;
- rule/tier changes;
- extreme slippage/protection failure.

## Invariants
- no new exposure if critical exchange risk state is unknown;
- no release of reserved risk without authoritative resolution;
- no position size may exceed any upper-level risk budget;
- no leverage selection may exceed current exchange/platform/user ceilings;
- no AI/strategy output may alter reservation or hard-limit state.

---

# 19. Bootstrap infrastructure

This architecture remains compatible with the free-first policy.

V1 can implement conceptually with:
- in-process deterministic risk engine in persistent backend/worker;
- PostgreSQL/Supabase for durable snapshots, policies and reservation audit metadata;
- transactional database operations for reservation state where required;
- local/offline stress research;
- no paid external risk service.

Performance-sensitive read state may use an in-process hot snapshot, but durable reservation truth must survive process restart and be reconcilable.

---

# 20. Critical gap closure mapping

This architecture closes the design-level requirements for:
- `GAP-R03-02` Dynamic Risk Tier & Maintenance Margin Resolver;
- `GAP-R03-03` Post-trade liquidation preview;
- `GAP-R03-04` Cross-margin contagion guard;
- `GAP-R03-09` Risk budget consumption accounting;
- `GAP-R03-10` Pending-order/partial-fill risk reservation;
- `GAP-R03-15` Risk parameter provenance/snapshot hash;
- `GAP-R03-16` Risk snapshot expiry/revalidation.

They remain subject to later R03 audit and implementation validation.

## Next necessary R03 action
Harden the non-CRITICAL but HIGH institutional domains:
- tail risk / Expected Shortfall-style portfolio views;
- survival/risk-of-ruin budget;
- multi-horizon limits;
- operational margin reserve;
- stop/protection failure exposure;
- pyramiding/add-to-position rules;
- collateral/stablecoin concentration;
- ADL/venue extreme-event awareness;
- safe user-facing risk profiles;
- complete risk explainability contract.

## STOP CONDITION
Do not approve R03 until HIGH gaps are reconciled, validation requirements are complete, and the round receives an independent planning audit verdict of `APPROVED`. Implementation and live trading remain unauthorized.
