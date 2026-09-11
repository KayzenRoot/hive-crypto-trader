# HCT-PLAN-0001-R04 — Execution State, Identity & Reconciliation Architecture

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R04`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

## Objective
Close the CRITICAL R04 planning gaps by defining deterministic contracts for execution identity, authorization freshness, exchange evidence, OMS event application, fill conservation, cancel/replace races, close/reduce correctness, protection dependencies, reconciliation generations, restart recovery and R03 risk-reservation closure.

Planning only. No implementation/live authorization.

---

# 1. Canonical execution authority chain

`Candidate Action`
`-> Safety Governor`
`-> Risk Engine / valid RiskSnapshot`
`-> Risk Reservation Ledger`
`-> Session Policy`
`-> Canonical Order Intent`
`-> Execution Plan`
`-> Command Authorization Lease`
`-> Exchange Command`
`-> Exchange Evidence`
`-> OMS Event Projection`
`-> Reconciliation`
`-> Position/Protection State`
`-> Risk Reservation Closure/Update`

Execution may choose an approved tactic inside bounded authority. It may not invent direction, quantity, leverage, risk or protection semantics.

---

# 2. Canonical identity model

Every state-changing execution operation has distinct identities.

## Parent identity
`order_intent_id`

Immutable business intent created after Risk/Safety/Policy approval. It survives retries, child orders, mutations and restart.

## Execution plan identity
`execution_plan_id`

Versioned plan for how the parent intent will be attempted.

## Command identity
`execution_command_id`

One exact state-changing outbound command attempt.

## Exchange external identity
`external_order_id`

HCT-generated value mapped to MEXC `externalOid` when the selected endpoint supports it.

Properties:
- unique inside tenant/account/exchange domain;
- deterministic relationship to parent intent + attempt lineage;
- never reused for a semantically different command;
- retained durably before network send where possible;
- searchable after timeout/restart;
- duplicate responses are interpreted as evidence, not permission for blind retry.

## Exchange-native identity
`exchange_order_id`

Assigned by the venue once known.

## Fill identity
`exchange_fill_id`

Stable venue fill identifier where provided; primary key for logical fill deduplication.

## Mutation lineage
Each replacement/amendment stores:
- previous command/order identity;
- new command identity;
- reason;
- requested delta;
- authority snapshot;
- consumed slippage/time budget;
- reconciliation state of predecessor.

---

# 3. Command Authorization Lease

A queued command cannot execute merely because it was approved earlier.

Before actual network send, the command must prove a valid authorization bundle:
- active Safety state permits the operation;
- exact Session Policy snapshot remains valid;
- exact RiskSnapshot remains valid when required;
- exposure-increasing command has active matching risk reservation;
- Order Intent has not expired/cancelled/superseded;
- execution plan version is current;
- position mode/margin mode assumptions still match exchange state;
- market/execution freshness remains within tolerance;
- Harness has not disabled the capability.

Research/operational construct: **HCT Command Freshness Lease (CFL)**.

Outcomes:
- `COMMAND_AUTHORIZED`;
- `COMMAND_REVALIDATE`;
- `COMMAND_SUPERSEDED`;
- `COMMAND_BLOCKED_SAFETY`;
- `COMMAND_BLOCKED_RISK`;
- `COMMAND_BLOCKED_POLICY`;
- `COMMAND_BLOCKED_STATE_UNCERTAIN`.

---

# 4. Order Evidence Ladder

HCT must preserve the difference between local intention and exchange truth.

Canonical evidence levels:
1. `INTENT_CREATED`
2. `PLAN_APPROVED`
3. `COMMAND_DURABLY_PREPARED`
4. `REQUEST_SENT`
5. `REST_ACKNOWLEDGED`
6. `ORDER_OBSERVED_ON_EXCHANGE`
7. `FILL_OBSERVED`
8. `POSITION_RECONCILED`
9. `PROTECTION_VERIFIED`

A lower level never proves a higher level.

Examples:
- REST success + `orderId` does not prove a fill.
- missing REST response does not prove rejection.
- WebSocket order event alone does not necessarily prove position/protection state.
- local position projection does not override reconciled exchange position evidence.

Research construct: **HCT Order Evidence Ladder (OEL)**.

---

# 5. Canonical OMS event envelope

Every execution-state event records:
- `oms_event_id`;
- tenant/account/exchange;
- parent intent ID;
- execution plan ID;
- command ID;
- external OID;
- exchange order ID;
- exchange fill ID where applicable;
- event type;
- exchange event timestamp;
- local receive timestamp;
- ingestion timestamp;
- source: REST_ACK / PRIVATE_WS_ORDER / PRIVATE_WS_FILL / REST_RECONCILIATION / POSITION_RECONCILIATION / INTERNAL_COMMAND;
- raw source reference;
- schema/parser version;
- reconciliation generation ID;
- event hash;
- quality/conflict flags.

Events are immutable. Projections may be corrected by later authoritative evidence without rewriting history.

---

# 6. Order state model

Canonical HCT order states:
- `INTENT_CREATED`
- `PREFLIGHTED`
- `COMMAND_PREPARED`
- `SUBMITTING`
- `ACKNOWLEDGED`
- `OPEN`
- `PARTIALLY_FILLED`
- `FILLED`
- `CANCEL_REQUESTED`
- `CANCEL_PENDING`
- `CANCELLED`
- `REPLACE_REQUESTED`
- `REPLACE_PENDING`
- `REJECTED`
- `EXPIRED`
- `INVALID`
- `UNCERTAIN`
- `RECONCILING`
- `QUARANTINED`

State projection is not a simple last-message-wins model.

---

# 7. Event ordering and state monotonicity

Introduce deterministic event application policy.

Use:
- exchange IDs;
- fill IDs;
- exchange/update timestamps;
- local receive order;
- event type/source authority;
- reconciliation generation;
- cumulative filled/remain quantity;
- current exchange query evidence.

Rules:
1. duplicate event => no second state/economic effect;
2. late event may append history but cannot blindly regress state;
3. terminal state can be challenged only by stronger contradictory exchange evidence;
4. contradictory evidence creates conflict record before correction;
5. cumulative fills can advance state even if order-status events are delayed;
6. fill evidence cannot be deleted by later stale `OPEN` event;
7. reconciled position may expose missing fills and trigger targeted backfill rather than fabricated fill events.

Research construct: **Execution State Confidence Graph (ESCG)**.

---

# 8. Fill Conservation Ledger

Each venue fill is logically applied once.

Canonical fill key:
`exchange + account + exchange_fill_id`

Fallback composite keys require explicit venue proof if a stable fill ID is unavailable.

Ledger stores:
- order/external IDs;
- fill ID;
- price;
- quantity;
- timestamp;
- fee + currency;
- maker/taker;
- realized PnL where applicable;
- side;
- position mode;
- reduce-only;
- source/provenance.

Invariants:
- duplicate fill cannot double quantity, fee or PnL;
- cumulative filled quantity cannot exceed valid order quantity without conflict;
- `remaining + filled` conservation must match venue semantics/tolerances;
- average fill price is derived from actual fills or venue-authoritative aggregate evidence;
- fee analytics reconcile actual fill fees, not static schedule assumptions.

Research construct: **HCT Fill Conservation Ledger (FCL)**.

---

# 9. Unknown Outcome Protocol v2

If network/transport outcome is unknown after state-changing send:
1. retain command identity and risk reservation;
2. classify `UNCERTAIN`;
3. block unsafe duplicate execution;
4. query by external OID/order ID where available;
5. inspect private order/fill events;
6. inspect current orders/history/recent fills;
7. inspect position delta;
8. resolve only from exchange evidence;
9. if still uncertain, remain uncertain and lower account State Confidence;
10. critical unresolved uncertainty can move account to `NO_NEW_ORDERS` or `RECONCILIATION_ONLY`.

A duplicate-ID response can be useful evidence that the venue has seen the identity and must trigger lookup/reconciliation, not a new identity retry by default.

---

# 10. Cancel/Replace Race Resolver

Canonical principle:
`CANCEL_REQUESTED != CANCELLED`.

Potential race cases:
- fill before cancel request reaches venue;
- fill while cancel is processing;
- cancel response after full fill;
- partial fill followed by cancel;
- private event arrives before REST cancel response;
- replacement submitted while predecessor remains live;
- amend conflicts with concurrent fill.

Rules:
1. predecessor exposure/order remains live-risk until authoritative final state;
2. replacement cannot create combined exposure above parent authorization;
3. risk reservation spans overlapping predecessor/replacement uncertainty;
4. fill arriving during cancel is applied normally;
5. cancel success must be reconciled with actual filled quantity;
6. non-atomic cancel/replace is treated explicitly as two commands unless venue proves atomic semantics;
7. race conflicts are recorded, not hidden.

Research construct: **HCT Cancel/Replace Race Resolver (CR3)**.

---

# 11. Position mode and close/reduce correctness

Position mode is an execution-critical state.

HCT canonical modes:
- `HEDGE_MODE`
- `ONE_WAY_MODE`
- `UNKNOWN`

Before an exposure-changing command:
- verify actual venue mode against Order Intent/RiskSnapshot assumptions;
- mismatch => revalidation or veto;
- never silently switch account position mode;
- mode-change capability belongs to privileged settings workflow, not trade execution tactic.

## Close/reduce invariant
A `REDUCE` or `CLOSE` intent may not increase absolute exposure or unintentionally create opposite exposure.

Checks:
- current reconciled side/size;
- intended reduction quantity <= policy-approved closeable exposure;
- position ID where required;
- correct venue side code;
- reduce-only support and mode compatibility;
- reverse/close-all endpoints require separate explicit capability and authority;
- reconcile final position after operation.

Failure to prove reduction semantics => do not send normal close command; enter safe reconciliation/recovery path.

---

# 12. Protection Dependency Graph

Protection is modeled as a dependency graph, not loose sibling orders.

Objects:
- exposure segment / fill;
- required protection policy;
- stop order(s);
- TP order(s);
- trailing protection;
- protection version;
- coverage quantity;
- validity state.

Relationships:
`Exposure -> ProtectionRequirement -> ExchangeProtectionOrder`

Events that require recalculation:
- new/partial fill;
- TP fill;
- manual/automated reduction;
- add/pyramiding;
- protection cancel/reject/expiry;
- replace/amend;
- position close;
- leverage/margin mode change;
- reconciliation correction.

Invariants:
- protection quantity never silently exceeds valid exposure except explicitly safe venue semantics;
- closing exposure removes or reconciles stale protection;
- required coverage gap is visible immediately;
- unknown protection state is not considered protected.

Research construct: **HCT Protection Dependency Graph (PDG)**.

---

# 13. Protection Establishment Deadline

For a strategy/policy requiring exchange-side protection, first fill starts a governed deadline.

Metric: **Protection Establishment Latency (PEL)**.

States:
- `PROTECTION_PENDING_WITHIN_BUDGET`
- `PROTECTION_VERIFIED`
- `PROTECTION_LATE`
- `PROTECTION_PARTIAL`
- `PROTECTION_FAILED`
- `PROTECTION_UNKNOWN`

Late/failed/unknown can trigger:
- no more exposure;
- `PROTECTION_RECOVERY`;
- deterministic reduce/close recommendation/command path according to risk policy.

---

# 14. Reconciliation Watermark Protocol

Each reconciliation cycle has immutable identity:
`reconciliation_generation_id`.

Record:
- account/exchange;
- cycle start/end;
- REST snapshots requested/received;
- current/open orders snapshot time;
- fill/history coverage range;
- position/account snapshot time;
- private-stream last healthy timestamp;
- private-stream reconnect/gap generation;
- unresolved IDs carried in;
- conflicts discovered/resolved;
- state confidence before/after.

Research construct: **HCT Reconciliation Watermark Protocol (RWP)**.

A system may not claim `RECONCILED` without a known generation and evidence scope.

---

# 15. Execution State Conflict Ledger

Contradictions are immutable objects until resolved.

Example:
`WS says OPEN; REST history says FILLED; position delta exists`.

Conflict object:
- conflict ID;
- entity/order/position;
- competing evidence;
- source timestamps;
- economic exposure;
- severity;
- temporary safest interpretation;
- actions blocked;
- resolution evidence;
- final result.

Critical conflict => State Confidence `UNCERTAIN/UNSAFE` and no new exposure.

Research construct: **HCT Execution Conflict Ledger (ECL)**.

---

# 16. Recovery Completeness Proof

Restart/failover recovery inventory:
1. durable unresolved parent intents;
2. command/external OIDs;
3. known exchange order IDs;
4. nonterminal OMS projections;
5. last reconciliation watermark;
6. current exchange open orders;
7. order history/recent fills since safe watermark;
8. actual positions/account state;
9. required protection graph;
10. R03 risk reservations;
11. unresolved conflicts;
12. private-stream health/reconnect state.

Recovery is complete only when every potentially live execution identity is one of:
- matched to exchange order/fills;
- authoritatively rejected/cancelled/expired;
- resolved as consumed into reconciled position;
- explicitly remains `UNCERTAIN/QUARANTINED` with new exposure blocked.

Research construct: **HCT Recovery Completeness Proof (RCP)**.

No “best effort then resume” for HIGH_ASSURANCE accounts.

---

# 17. Risk Reservation closure contract

R04 must close the accounting loop with R03.

For an exposure-increasing intent:
`APPROVED_RISK_RESERVATION = OPEN_POSITION_RISK_CONVERSION + STILL_RESERVED_RISK + AUTHORITATIVELY_RELEASED_RISK`

Subject to clearly separate non-additive portfolio/tail metrics.

Rules:
- REST timeout does not release;
- cancel request does not release;
- partial fill converts filled share and retains remainder;
- exchange reject can release after authoritative evidence;
- exchange cancel/expiry releases only unfilled remainder;
- unknown/conflicted state retains conservative reservation;
- restart must reconstruct reservation mapping before new exposure resumes.

---

# 18. Validation requirements

## Property/invariant tests
- one external OID never represents two business intents;
- one fill ID changes economics at most once;
- filled quantity conservation;
- no stale command authorization execution;
- reduce/close never increases exposure;
- risk reservation conservation;
- no order state regression from stale duplicate evidence without conflict workflow;
- no protection marked verified without exchange evidence;
- no restart resume with unresolved potentially-live identity unclassified.

## Race tests
- fill vs cancel;
- fill vs modify;
- cancel ACK vs fill event;
- replacement overlap;
- REST ACK lost + WS order event arrives;
- REST timeout + duplicate external OID on retry;
- WS fill duplicated/out of order;
- position update before fill event;
- TP fill concurrent with stop amendment.

## Failure tests
- private WS disconnect;
- REST query outage;
- timestamp rejection;
- malformed/new enum event;
- venue auto-cancel;
- partial market fill;
- protection rejection;
- restart mid-submit;
- restart with uncertain order;
- DB durable-event write interruption around network send.

## Recovery tests
- deterministic rebuild from durable log + exchange state;
- unresolved conflict forces safe mode;
- Risk Reservation Ledger reconstructed consistently;
- protection graph repaired or exposure reduced before normal operation.

---

## Critical gaps covered by this document
`GAP-R04-01`, `02`, `03`, `04`, `05`, `07`, `09`, `11`, `13`, `21`, `22` receive canonical design coverage here.

Remaining HIGH/MEDIUM hardening domains will be addressed separately before R04 approval.

## STOP CONDITION
This document closes critical architecture design only. R04 remains `CORRECTION REQUIRED` until HIGH gaps, canonical decisions, Requirements alignment, acceptance gates and final audit are complete.