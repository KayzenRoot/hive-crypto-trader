# HCT-PLAN-0001-R04 — Execution High-Assurance Hardening

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R04`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

## Purpose
Close the remaining HIGH/MEDIUM-HIGH R04 gaps after the critical execution-state architecture in `docs/45-r04-execution-state-identity-reconciliation-architecture.md`.

Planning only. No implementation/live authorization.

---

# 1. Position mode policy

HCT supports venue-observed position modes as explicit execution state:
- `HEDGE_MODE`
- `ONE_WAY_MODE`
- `UNKNOWN`

Rules:
- actual venue mode is verified before commands whose semantics depend on it;
- strategy/user setting cannot silently switch account mode;
- mismatch between approved intent and venue mode => revalidation/veto;
- mode changes are privileged configuration operations with no live/open-order ambiguity;
- account-wide implications are visible and audited.

In Hedge Mode, opening/closing direction semantics are explicit. In One-Way Mode, opposite-direction orders may reduce/reverse depending on quantity and venue semantics, so HCT never infers intent solely from buy/sell direction.

Covers `GAP-R04-06`.

---

# 2. Market/IOC/FOK/Post-Only completion semantics

Execution plan must preserve order-type-specific semantics.

## Market
- may be partially filled;
- remaining quantity may be canceled by venue under depth/market constraints;
- completion state is based on fill/order evidence, not assumption of full execution.

## IOC
- execute immediately to available amount and cancel remainder according to venue semantics;
- canceled remainder is not a failed whole order.

## FOK
- success/failure semantics remain venue-specific and must be confirmed from actual order/fill evidence.

## Post-Only
- venue may auto-cancel if order would immediately take liquidity;
- such cancellation is expected tactic outcome, not infrastructure failure.

Canonical result distinguishes:
- `COMPLETE_FILLED`
- `PARTIAL_REMAINDER_CANCELLED`
- `NO_FILL_CANCELLED`
- `ACTIVE_REMAINDER`
- `REJECTED`
- `UNCERTAIN`

Any under-filled OPEN intent triggers position/protection/risk re-evaluation.

Covers `GAP-R04-08`.

---

# 3. Signed-command clock integrity

MEXC private REST requests require bounded Request-Time validity.

Introduce `CommandClockHealth`:
- estimated exchange/local clock offset;
- offset uncertainty;
- last successful signed request age;
- timestamp rejection rate;
- local monotonic timer health;
- NTP/system clock change detection where practical.

States:
- `CLOCK_HEALTHY`
- `CLOCK_DEGRADED`
- `CLOCK_UNTRUSTED`

Rules:
- elapsed budgets use monotonic time locally;
- wall time is used for protocol timestamping/audit with drift monitoring;
- broad Recv-Window cannot be used to hide broken clocks;
- repeated timestamp/signature failures can stop new exposure while preserving risk-reducing/reconciliation capability where safe.

Covers `GAP-R04-14`.

---

# 4. Quota Priority Governor

Execution/reconciliation share finite exchange/API capacity.

Priority classes:

`P0 EMERGENCY`
- required protective action;
- risk-reducing emergency close;
- critical unknown-outcome reconciliation.

`P1 SAFETY_RECOVERY`
- protection repair;
- cancel dangerous/stale orders;
- restart recovery;
- high-severity state reconciliation.

`P2 ACTIVE_EXECUTION_CONTROL`
- cancel/replace of active authorized intent;
- targeted order/fill query.

`P3 NEW_EXPOSURE`
- ordinary new OPEN/ADD commands.

`P4 NONCRITICAL`
- history/research/analytics/backfill.

Rules:
- new exposure yields quota to P0/P1/P2;
- query storms are bounded;
- retries consume budget and have retry ceilings;
- account-ban/abuse prevention outranks opportunity capture;
- institutional/higher-limit account support is future capacity, not an assumption.

Research construct: **HCT Quota Priority Governor (QPG)**.

Covers `GAP-R04-15`.

---

# 5. Versioned execution cost truth

Execution cost uses two layers:

## Expected cost policy
Versioned assumptions before execution:
- maker/taker schedule;
- funding estimate where relevant;
- expected spread/slippage;
- market impact;
- venue/plan-specific fee rules if proven applicable.

## Realized cost truth
After execution:
- actual fee per fill;
- fee currency;
- maker/taker actual status;
- realized average price;
- realized slippage versus decision/reference price;
- funding later attached to position lifecycle;
- rebates/negative fees where venue reports them.

Current planning reference verified on 2026-09-11: MEXC API Futures fee announcement effective 2026-06-01 lists maker 0.06% and taker 0.08%. This is an external dependency and must be revalidated before implementation/live use.

A displayed website/app promotional fee cannot be substituted for API fee truth unless explicitly applicable.

Research construct: **Realized Execution Cost Surface (RECS)**.

Covers `GAP-R04-16`.

---

# 6. Self-Trade Prevention

MEXC currently exposes an STP mode on order creation. HCT needs a deterministic account-level strategy-conflict policy.

Potential STP policies where venue capability permits:
- `NONE`
- `CANCEL_BOTH`
- `CANCEL_MAKER`
- `CANCEL_TAKER`

HCT selection must be policy-driven, not strategy-invented per order without approval.

Before placing potentially crossing same-account orders:
- inspect live/open HCT orders;
- identify parent/strategy ownership;
- determine whether opposite intents are legitimate Hedge Mode exposure or accidental self-crossing;
- apply venue STP where appropriate;
- preserve STP cancellation as explicit execution evidence.

Research metric: **Self-Cross Risk Score (SCRS)**.

Covers `GAP-R04-17`.

---

# 7. Execution Tactic Capability Matrix

Each venue-specific tactic is a capability, not merely an enum.

Candidate capabilities:
- LIMIT
- MARKET
- POST_ONLY
- IOC
- FOK
- BBO/CHASE
- MARKET_TO_LIMIT if exposed by event semantics
- MODIFY_PRICE_QUANTITY
- CANCEL_BY_ORDER_ID
- CANCEL_BY_EXTERNAL_ID
- BATCH_PLACE
- BATCH_CANCEL
- PLAN/TRIGGER
- TP_SL_BY_POSITION
- TRAILING
- REVERSE_POSITION
- CLOSE_ALL
- STP

For each capability record:
- endpoint support;
- externalOid support;
- supported position modes;
- reduce-only behavior;
- atomicity assumptions;
- response/evidence semantics;
- rate limit class;
- failure/cancel enums;
- test/promotion status.

High-risk shortcuts such as REVERSE_POSITION/CLOSE_ALL remain disabled unless separately validated and authorized.

Research construct: **Execution Tactic Capability Matrix (ETCM)**.

Covers `GAP-R04-18`.

---

# 8. Private Event Schema Sentinel

Private WebSocket events can change or contain unknown enum/schema values.

Introduce **HCT Private Event Schema Sentinel (PESS)**.

On unknown/malformed critical event:
1. retain raw payload securely;
2. attach parser/schema version;
3. do not guess unknown semantics;
4. quarantine event/entity if economically material;
5. lower State Confidence;
6. trigger targeted REST reconciliation;
7. alert observability/admin layer;
8. block new exposure if uncertainty affects order/position/protection truth.

Parser upgrades require replay against captured fixtures and rollback capability.

Covers `GAP-R04-19`.

---

# 9. Adaptive Reconciliation Cadence

Reconciliation is event-driven plus adaptive periodic safety verification.

Cadence inputs:
- active exposure count/notional;
- open/pending/uncertain orders;
- protection state;
- private WS health;
- recent reconnect/gap;
- execution activity;
- risk-reservation uncertainty;
- conflict ledger severity;
- venue/API health;
- quota availability;
- time since last confirmed generation.

Cadence states:
- `IDLE_CONFIRMED`
- `ACTIVE_CONFIRMED`
- `FAST_VERIFY`
- `UNCERTAIN_RECOVERY`
- `PROTECTION_RECOVERY`
- `RESTART_RECOVERY`

Rules:
- urgent uncertainty tightens cadence;
- normal idle state may relax within max-age ceiling;
- no adaptive policy may starve P0/P1 command quota;
- reconciliation itself is bounded against retry/query storms.

Research construct: **Adaptive Reconciliation Cadence (ARC)**.

Covers `GAP-R04-20`.

---

# 10. State Confidence model hardening

State Confidence is a vector before it is a label.

Candidate dimensions:
- order identity confidence;
- fill completeness confidence;
- position confidence;
- protection confidence;
- account/margin confidence;
- private stream confidence;
- REST reconciliation freshness;
- conflict burden;
- clock health;
- parser/schema health;
- risk-reservation consistency.

Derived account states:
- `CONFIRMED`
- `HIGH_CONFIDENCE`
- `DEGRADED`
- `UNCERTAIN`
- `UNSAFE`

Critical dimension failure cannot be hidden by a high average score.

---

# 11. Execution observability minimums

Per parent intent expose:
- Order Intent identity;
- execution plan/current tactic;
- command/external/exchange IDs;
- evidence ladder level;
- requested/filled/remaining size;
- actual weighted fill;
- fees/maker-taker;
- slippage budget used;
- active cancel/replace race state;
- protection dependency/coverage;
- risk reservation link;
- last reconciliation generation;
- State Confidence vector/state;
- conflict ledger references;
- command authorization freshness;
- current recovery mode.

---

# 12. Additional validation scenarios

- One-Way opposite order would unintentionally reverse exposure;
- Hedge Mode close uses wrong side/position ID;
- market partial fill + remainder venue cancel;
- Post-Only auto-cancel;
- IOC partial/cancel;
- FOK failure;
- duplicate external OID;
- STP cancel maker/taker/both paths;
- fee schedule changes between strategy validation and live preflight;
- local clock drifts outside signed-request tolerance;
- unknown private event enum;
- private WS healthy but targeted REST reconciliation contradicts order state;
- quota stress while protection repair and new-exposure requests compete;
- adaptive reconciliation increases frequency during uncertainty then safely relaxes.

---

## Gap coverage
This document provides canonical planning coverage for `GAP-R04-06`, `08`, `14`, `15`, `16`, `17`, `18`, `19`, `20`, and strengthens state confidence across the round.

Together with `docs/45`, all CRITICAL/HIGH gaps identified by the initial R04 audit now have architecture coverage. They still require Decisions Ledger/Requirements alignment, objective acceptance gates and final audit before R04 can be approved.

## STOP CONDITION
R04 remains `CORRECTION REQUIRED` until canonical decisions, Requirements alignment, acceptance gates and objective final audit are complete. Implementation/live trading remain unauthorized.