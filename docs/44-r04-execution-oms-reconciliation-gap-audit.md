# HCT-PLAN-0001-R04 — Execution, OMS & Reconciliation Gap Audit

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R04`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

## Objective
Formally audit the pre-discovery execution architecture in `docs/29-execution-intelligence-oms-reconciliation-and-recovery.md` and identify the remaining institutional-grade controls required before R04 can be approved.

R04 is planning only. No implementation, production credentials or live trading are authorized.

## Current strengths inherited from pre-discovery
The existing design already establishes:
- canonical immutable Order Intent;
- Execution Feasibility Engine;
- bounded slippage budgets;
- fill/impact research model;
- bounded order mutation planner;
- explicit partial-fill state;
- Protective Order Integrity Monitor;
- event-sourced OMS concept;
- idempotency/duplicate-prevention principle;
- Unknown Outcome Protocol;
- event-driven plus periodic reconciliation;
- State Confidence Index;
- restart recovery;
- execution drift monitoring;
- recovery/degraded modes;
- prohibition on blind retry, inferred fills or risk expansion.

These are accepted as R04 foundation inputs subject to the gaps below.

## Current MEXC execution facts relevant to architecture
Official MEXC Futures API/support material checked on 2026-09-11 indicates:
- Futures API supports REST and WebSocket for order placement/cancellation, order management and trading subscriptions.
- Current REST order creation exposes `externalOid`, exchange `orderId`, `positionMode`, `reduceOnly`, STP mode, position ID, order type, margin mode and optional TP/SL fields.
- Order creation currently documents a rate limit of 4 requests per 2 seconds for the place-order endpoint.
- Private WebSocket order events expose order ID, external order ID, filled volume, remaining volume, order state, position mode, reduce-only and fee-rate fields.
- Private fill events expose a stable fill ID plus order ID/external order ID, fill price/volume/fee, maker/taker indication and position-mode/reduce-only context.
- Documented order states include pending/open/filled/canceled/invalid.
- Error enums include duplicate order IDs (`OID_DUPLICATE`, `CID_DUPLICATE`) and cancellation reasons such as IOC/FOK/Post-Only/market/ADL/system cancellation.
- MEXC supports Hedge Mode and One-Way Mode; mode changes have restrictions when positions/open orders exist and may apply account-wide.
- Reduce-only is documented as applicable to One-Way Mode in the current place-order API.
- Market orders can be partially filled under insufficient depth and remaining quantity may be canceled by the venue.
- API Futures fees currently effective from 2026-06-01 are maker 0.06% and taker 0.08%; fee schedules are external dynamic dependencies and must not be hard-coded forever.

Architectural consequence: HCT can use strong exchange identifiers and private-stream evidence, but must still treat REST acknowledgement, private events and reconciled REST/account state as separate evidence classes.

---

# R04 gap audit

## GAP-R04-01 — Canonical command identity and external-order-ID policy
Severity: `CRITICAL`

Need a deterministic policy for mapping one HCT state-changing intent to:
- immutable parent `order_intent_id`;
- attempt/mutation IDs;
- exchange `externalOid` where supported;
- exchange `orderId` once known;
- child-order IDs;
- replacement lineage.

Requirements:
- globally unique within tenant/account/exchange scope;
- stable enough for reconciliation after timeout/restart;
- no accidental reuse across semantically different commands;
- duplicate responses/events classified rather than blindly retried.

## GAP-R04-02 — REST acknowledgement is not execution truth
Severity: `CRITICAL`

A successful create-order response proves only that the endpoint returned success and an order identifier. It does not prove fill, protection or final position state.

Need explicit evidence levels:
`LOCAL_INTENT -> REQUEST_SENT -> REST_ACK -> ORDER_OBSERVED -> FILL_OBSERVED -> POSITION_RECONCILED -> PROTECTION_VERIFIED`.

No higher state may be inferred from a lower one without corroborating evidence.

## GAP-R04-03 — OMS event ordering, monotonicity and stale-event policy
Severity: `CRITICAL`

Private WebSocket and REST reconciliation evidence can arrive late, duplicated or out of order.

Need canonical event application rules using:
- exchange timestamps;
- local receive timestamps;
- order/fill IDs;
- update/version evidence where available;
- state precedence;
- reconciliation generation.

A late `open` event may not regress a locally reconciled `filled` or `canceled` order without authoritative contradictory evidence and explicit conflict handling.

## GAP-R04-04 — Fill identity, deduplication and aggregation
Severity: `CRITICAL`

Each exchange fill must be ingested exactly-once logically even if received more than once physically.

Need:
- stable fill key, preferring exchange fill ID;
- duplicate suppression;
- cumulative quantity/fee/PnL conservation;
- average-fill-price derivation rules;
- correction/reconciliation path if fills are missing or inconsistent;
- maker/taker and fee evidence preservation.

## GAP-R04-05 — Cancel/replace/modify race semantics
Severity: `CRITICAL`

Cancel or modify can race with fills.

Examples:
- fill arrives while cancel is pending;
- cancel ACK arrives after full fill;
- replacement is submitted before original cancel is authoritatively resolved;
- modification changes quantity while a concurrent fill changes remaining quantity.

Need deterministic race handling and a rule that `CANCEL_REQUESTED != CANCELLED`.

## GAP-R04-06 — Position mode as execution authority input
Severity: `HIGH`

Hedge and One-Way modes have different open/close semantics. A side/opposite-direction order can reduce, close or open an opposite position depending on mode.

Need:
- position mode in RiskSnapshot and Order Intent;
- exchange verification before exposure-changing commands;
- mismatch => revalidation/veto;
- prohibition on silent mode switching;
- account-wide mode-change implications captured.

## GAP-R04-07 — Reduce-only and close-intent correctness
Severity: `CRITICAL`

Need to prove that CLOSE/REDUCE commands cannot accidentally increase or reverse exposure.

Controls:
- canonical reduce/close semantics independent of UI language;
- `reduceOnly` capability/position-mode compatibility;
- current position size/side verification;
- bounded close quantity;
- close-all/reverse endpoints treated as distinct high-risk capabilities, not shortcuts;
- post-command reconciliation to prove intended reduction.

## GAP-R04-08 — Market-order partial fill and venue auto-cancel semantics
Severity: `HIGH`

Market-like execution is not guaranteed to fully fill. Remaining size may be canceled under venue constraints.

Need explicit state/results for:
- partial + remainder canceled;
- partial + still active where supported;
- no-fill/cancel;
- slippage ceiling reached;
- resulting under-sized position and protection repair.

## GAP-R04-09 — Protective-order dependency graph
Severity: `CRITICAL`

Protection cannot be modeled as independent loose orders.

Need graph relationships:
`Position/Fill -> Required Protection Set -> Exchange Protective Orders`.

Must handle:
- partial fills creating partial protection requirements;
- TP reducing position and requiring stop quantity adjustment;
- stop/TP triggered while sibling protection remains;
- replace/amend invalidating previous protection;
- position close leaving stale protection orders;
- exchange-side cancel/reject.

## GAP-R04-10 — Protection establishment deadline
Severity: `HIGH`

For policies requiring exchange-side protection, define a bounded period after first exposure fill during which required protection must become verified.

If exceeded:
- no additional exposure;
- protection recovery mode;
- risk-driven reduce/close path according to policy.

Research metric: `Protection Establishment Latency (PEL)`.

## GAP-R04-11 — Reconciliation watermarks and authoritative generations
Severity: `CRITICAL`

Need a reproducible way to know what exchange state has been reconciled.

Define:
- reconciliation cycle/generation ID;
- snapshot start/end timestamps;
- covered order/fill time range;
- private-stream watermark/health;
- unresolved identifiers carried forward;
- account/position/order evidence version.

Without watermarks, “reconciled” is too vague for HIGH_ASSURANCE recovery.

## GAP-R04-12 — State conflict ledger
Severity: `HIGH`

When REST, WebSocket, OMS projection and position/account state disagree, preserve the contradiction instead of overwriting history.

Introduce `ExecutionStateConflict` with:
- competing claims;
- source/provenance/time;
- severity;
- affected exposure;
- resolution evidence;
- final disposition.

Critical unresolved conflicts lower State Confidence and block new exposure.

## GAP-R04-13 — Restart recovery completeness proof
Severity: `CRITICAL`

Restart recovery must prove not only that state was loaded, but that all potentially live intents/orders were classified.

Need recovery inventory:
- durable unresolved intents;
- external OIDs/order IDs;
- current exchange orders;
- recent fills since durable watermark;
- actual positions;
- required protection;
- risk reservations;
- unresolved conflicts.

Resume only after recovery invariant passes.

## GAP-R04-14 — Time synchronization and signed-command freshness
Severity: `HIGH`

MEXC signed endpoints validate `Request-Time` within a bounded server window.

Need:
- clock-offset monitoring;
- monotonic elapsed timing for local budgets;
- command timestamp provenance;
- reject/retry policy for timestamp failures;
- no broad `Recv-Window` as a substitute for broken clocks.

## GAP-R04-15 — Endpoint-specific quota/concurrency budget
Severity: `HIGH`

Place, cancel, query, reconciliation and recovery traffic compete for venue quota.

Execution needs priority classes:
1. risk-reducing/protection recovery;
2. uncertain-outcome reconciliation;
3. cancel/replace;
4. normal new exposure;
5. noncritical history/research.

New exposure must yield quota to safety/reconciliation paths.

## GAP-R04-16 — Fee schedule and actual execution-cost truth
Severity: `HIGH`

Execution decisions must use versioned fee assumptions and reconcile against actual fee events.

Need:
- venue fee schedule observation/version;
- maker/taker actual classification;
- fee currency;
- promotional/displayed web rates excluded unless proven applicable to API account;
- fee assumption invalidation when venue changes pricing;
- execution-quality analytics based on realized, not hypothetical, costs.

## GAP-R04-17 — Self-trade prevention policy
Severity: `MEDIUM/HIGH`

MEXC exposes STP modes. Multi-strategy/multi-agent HCT can otherwise create orders that trade against each other or create needless fees/cancels.

Need platform policy for:
- STP mode selection where supported;
- same-account strategy conflict;
- parent/child crossing;
- user-strategy interaction;
- audit of self-trade prevention events.

## GAP-R04-18 — Special execution tactic capability boundaries
Severity: `HIGH`

Chase/BBO, market-to-limit, reverse, close-all, plan/trigger, trailing and batch endpoints must each be explicit capabilities with separate semantics and promotion evidence.

No generic `OrderType` abstraction may hide venue-specific behavior that affects risk or state transitions.

## GAP-R04-19 — Malformed/unknown private event quarantine
Severity: `HIGH`

Schema drift or unrecognized enum values must not be silently discarded or guessed.

Need:
- raw evidence retention;
- schema/version detection;
- quarantine/dead-letter path;
- state-confidence degradation;
- alert/escalation;
- controlled parser rollout/rollback.

## GAP-R04-20 — Reconciliation cadence must be adaptive
Severity: `MEDIUM/HIGH`

One fixed polling interval is insufficient.

Reconciliation frequency should tighten under:
- unresolved orders;
- WS gaps/reconnect;
- active execution;
- protection recovery;
- large exposure;
- exchange degradation;
- restart/failover.

It may relax during idle confirmed state while respecting maximum age policy and quota budgets.

## GAP-R04-21 — Execution command authorization binding
Severity: `CRITICAL`

Every state-changing command must prove it still belongs to:
- valid Session Policy snapshot;
- valid RiskSnapshot;
- active risk reservation where exposure can increase;
- current Safety state;
- canonical Order Intent and execution plan.

A stale command queued before a risk/policy/safety change cannot execute later merely because it was once approved.

## GAP-R04-22 — Reconciliation-to-risk reservation closure
Severity: `CRITICAL`

OMS/reconciliation outcomes must deterministically update the R03 Risk Reservation Ledger.

Need invariant:
`reserved + open-position risk + authoritatively released amount = approved reservation lifecycle accounting`, subject to clearly defined portfolio/tail non-additive measures.

Unknown order state cannot free reserved exposure budget.

---

## Proprietary R04 research/operational technologies
Candidates, not production claims:
1. HCT Execution State Confidence Graph (ESCG)
2. HCT Order Evidence Ladder (OEL)
3. HCT Reconciliation Watermark Protocol (RWP)
4. HCT Command Freshness Lease (CFL)
5. HCT Fill Conservation Ledger (FCL)
6. HCT Cancel/Replace Race Resolver (CR3)
7. HCT Protection Dependency Graph (PDG)
8. HCT Protection Establishment Latency (PEL)
9. HCT Execution Conflict Ledger (ECL)
10. HCT Recovery Completeness Proof (RCP)
11. HCT Quota Priority Governor (QPG)
12. HCT Realized Execution Cost Surface (RECS)
13. HCT Execution Tactic Capability Matrix (ETCM)
14. HCT Private Event Schema Sentinel (PESS)
15. HCT Adaptive Reconciliation Cadence (ARC)
16. HCT Command Authorization Chain (CAC)

Every construct must demonstrate correctness/safety/decision value before production promotion.

## Initial R04 verdict
`CORRECTION REQUIRED`

Reason: the R02 pre-discovery execution architecture is strong but several CRITICAL contracts remain implicit, especially command identity, evidence levels, event ordering, fill deduplication, cancel/replace races, reduce-only correctness, protection dependency, reconciliation watermarks, restart completeness, command authorization binding and Risk Reservation closure.

## Next necessary action
Create the formal R04 execution-state architecture closing the CRITICAL gaps first, then harden HIGH gaps and define objective acceptance gates.

## STOP CONDITION
Do not approve R04 until every CRITICAL/HIGH gap has canonical design coverage, explicit state transitions/invariants, validation requirements and clear integration with R03 RiskSnapshot/Risk Reservation authority. Implementation and live trading remain unauthorized.