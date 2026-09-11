# HCT-PLAN-0001-R04 — Acceptance Criteria & Review Gates

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R04`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

## Purpose
Define objective planning gates required before R04 Execution/OMS/Reconciliation discovery may receive `APPROVED`.

## Gate A — Authority binding
Must prove every state-changing command is bound to current Safety state, Session Policy, Order Intent/execution plan and valid RiskSnapshot/risk reservation where applicable. Stale queued commands cannot execute later without revalidation.

## Gate B — Identity and idempotency
Must define parent intent, execution plan, command, external OID, exchange order ID, fill ID and mutation lineage with duplicate-safe semantics.

## Gate C — Evidence hierarchy
Must distinguish request send, REST ACK, exchange-observed order, fill evidence, position reconciliation and protection verification. No lower evidence class may masquerade as a higher one.

## Gate D — OMS ordering and fill conservation
Must handle duplicate, late and out-of-order events without state regression or double economic effects. Fill quantity/fee/PnL conservation must be explicit.

## Gate E — Unknown outcomes
Timeout/ambiguous submit must remain `UNCERTAIN`; duplicate retry is blocked until authoritative reconciliation resolves or safely quarantines the outcome.

## Gate F — Cancel/replace races
Must define fill-vs-cancel, fill-vs-modify, cancel ACK after fill, partial-before-cancel and replacement overlap behavior. `CANCEL_REQUESTED` must never equal `CANCELLED`.

## Gate G — Close/reduce correctness
Must prove REDUCE/CLOSE cannot unintentionally increase/reverse exposure and position-mode assumptions are verified. Reverse/close-all are separately governed high-risk capabilities.

## Gate H — Protection dependency and deadline
Must model protection as dependent on actual filled exposure, maintain coverage through partial fills/reductions/adds and enforce a bounded protection-establishment deadline where required.

## Gate I — Reconciliation watermarks/conflicts
Must define reconciliation generations, evidence coverage, private-stream watermarks and an immutable conflict ledger. Critical unresolved conflict blocks new exposure.

## Gate J — Restart/failover recovery proof
Every potentially live durable intent/order must be classified against exchange-authoritative order/fill/position/protection evidence before normal new exposure resumes.

## Gate K — R03 risk-reservation closure
Execution/reconciliation outcomes must deterministically consume, retain or authoritatively release R03 risk reservations. Timeout/cancel request/unknown state cannot free reserved risk.

## Gate L — Protocol time and quota safety
Must monitor signed-request time integrity and prioritize emergency/protection/reconciliation traffic over new exposure under finite endpoint quotas.

## Gate M — Execution-cost truth
Expected fees/slippage are versioned assumptions; realized maker/taker fees and fill costs are reconciled from exchange evidence. Current provider rates are external dependencies, not permanent constants.

## Gate N — Tactic capability boundaries
Market, limit, IOC, FOK, Post-Only, BBO/chase, modify, trigger, TP/SL, trailing, STP, reverse and close-all must have explicit venue capabilities/semantics rather than one misleading generic abstraction.

## Gate O — Private event schema resilience
Unknown/malformed critical private events must be retained/quarantined, lower State Confidence and trigger reconciliation rather than guessed/discarded.

## Gate P — Adaptive reconciliation
Cadence must tighten during active/uncertain/protection/restart states and may relax only within maximum-age/quota safety policies.

## Gate Q — Observability and explainability
Execution cockpit/evidence must expose identity lineage, evidence level, requested/filled/remaining quantity, actual cost, races, protection state, risk reservation, reconciliation generation, State Confidence and conflicts.

## Gate R — Validation plan
Planning must require property, race, failure, restart/recovery and exchange-semantic tests for all critical invariants.

## Gate S — Canonical consistency
Before approval:
- all R04 decisions are in Decisions Ledger;
- Requirements include accepted R04 product requirements;
- Scope still forbids implementation/live authorization;
- R04 gap audit records CRITICAL/HIGH gaps resolved in planning;
- PR matches branch content;
- objective final R04 audit exists.

## Verdict rule
- unresolved CRITICAL/HIGH planning defect => `CORRECTION REQUIRED`;
- missing authoritative dependency necessary to complete planning => `BLOCKED`;
- all gates pass => `APPROVED`.

Implementation and live trading remain unauthorized regardless of R04 planning approval.