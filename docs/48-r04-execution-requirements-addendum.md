# HCT-PLAN-0001-R04 — Execution / OMS / Reconciliation Requirements Addendum

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R04`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

## Purpose
Capture the accepted R04 execution requirements in a canonical artifact without weakening or replacing the broader product requirements in `docs/02-requirements.md`.

This document is a planning requirement source for R04 and does not authorize implementation or live trading.

## Execution authority and command requirements
- Every state-changing execution command must bind to a still-valid Safety state, immutable RiskSnapshot, Risk Reservation and Session Policy through a Command Authorization Lease or equivalent deterministic contract.
- Queued commands whose authority expires or whose bound state changes before transmission must be revalidated or discarded.
- Execution may optimize how an already-approved action is performed but may not create new directional thesis, increase approved quantity/risk, raise leverage, weaken protection or bypass Safety/Risk/Policy.

## Canonical identity and idempotency requirements
- Distinguish immutable `OrderIntentID`, `ExecutionPlanID`, `ExecutionCommandID`, provider/client/external order identity, exchange order identity, fill identity and mutation lineage.
- Preserve parent/child order relationships and cancel/replace lineage.
- Use stable client/external order identity where supported by the venue.
- Duplicate commands or duplicate exchange events must not create duplicate economic effects.

## Evidence and OMS requirements
- REST/API acknowledgement is not fill truth.
- Maintain an explicit evidence hierarchy spanning local command transmission, exchange acknowledgement, exchange-visible order state, fill evidence, reconciled position state and verified protection.
- OMS must retain immutable source events with provenance and timestamps.
- Late/out-of-order/duplicate events may enrich history but must not regress a stronger current projection without stronger authoritative evidence.
- Each authoritative fill identity may change position, fee and risk accounting at most once.

## Unknown outcome requirements
- Timeout after state-changing submission is `UNCERTAIN`, not failed.
- Cancel request is not cancellation proof.
- Replace request is not proof that the original order ceased to exist.
- Unknown outcomes block blind retries and require reconciliation against client/external IDs, exchange order IDs, fills and position evidence.
- Persistent unresolved ambiguity can force `NO_NEW_ORDERS`, `RECONCILIATION_ONLY`, `REDUCE_ONLY` or stronger recovery states.

## Cancel/replace race requirements
- Explicitly handle fill-before-cancel, fill-during-cancel, partial-fill-before-replace, late cancel acknowledgement and old/new order coexistence.
- Replacement logic must not exceed the remaining approved parent intent or risk budget.
- Risk Reservation Ledger state must remain conserved through mutation races.

## Position mode / reduce / close requirements
- Every REDUCE/CLOSE/PROTECT action must validate current reconciled position mode, side, size, position identity and venue capability.
- One-Way and Hedge semantics are modeled explicitly where supported.
- Reduce/close behavior may not silently create, increase or reverse opposite exposure.
- When current position mode cannot be verified, exposure-increasing or ambiguous closing commands fail safe.

## Protection integrity requirements
- Represent required stop, TP, trailing and other protection as dependencies of actual filled exposure.
- Protection quantity must track partial fills, adds, reductions and exits.
- Verify exchange acceptance, trigger semantics, reduce-only/position-side semantics and current coverage.
- Track protection-establishment latency from first exposure-creating fill to verified protection.
- Missing, stale, partial or unknown required protection may block new exposure and trigger protection recovery or reduction.

## Reconciliation requirements
- Reconcile orders, fills, positions, balances/equity/margin, leverage/margin mode and protection using event-driven plus periodic/adaptive checks.
- Maintain explicit reconciliation watermarks/coverage age rather than a single boolean `reconciled` flag.
- Contradictory authoritative evidence creates a persisted conflict record instead of silent last-write-wins overwrite.
- New exposure requires a configured minimum state-confidence/reconciliation threshold.

## Restart / failover requirements
- On restart, deployment or failover, cached execution state is not trusted as current truth.
- Reload durable intents/commands/OMS events, query exchange-authoritative open orders/recent fills/positions/account state, classify potentially-live identities, restore Risk Reservation state and verify protection.
- Normal new exposure resumes only after a Recovery Completeness Proof (or equivalent deterministic recovery gate) succeeds.

## R03 risk integration requirements
- Exposure-increasing commands reference the exact RiskSnapshot and Risk Reservation approved in R03.
- Submission does not release reserved risk.
- Partial fills convert only the corresponding portion of reserved risk into open-position risk.
- Unfilled active or uncertain portions remain reserved.
- Cancel/timeout does not free reservation until exchange-confirmed or authoritatively reconciled final state.

## Time, quota and resilience requirements
- Monitor signed-request clock health and venue request-time/receive-window semantics.
- Untrusted clock state blocks affected signed commands rather than widening time windows without governance.
- API/WS quota allocation is priority-aware: emergency/protection/reconciliation/active-position control outrank new exposure and research/scanning.
- Research/scanning may not consume capacity required to protect or reconcile money already at risk.

## Cost / fee truth requirements
- Fee schedules are versioned external dependencies and must not be treated as perpetual constants.
- Capture expected versus realized maker/taker fees, funding where relevant, spread, slippage and other execution costs.
- Actual exchange fill/fee evidence is canonical for realized execution-cost truth.

## Tactic capability requirements
- Maintain an Execution Tactic Capability Matrix per exchange/market covering supported order types, TIF behavior, post-only/passive semantics, IOC/FOK-like semantics, market-order behavior, STP, position modes, reduce-only, amendments/cancel-replace and protective capabilities.
- Unsupported or unknown capabilities are rejected or degraded explicitly rather than silently emulated.
- Execution tactics cannot consume unlimited slippage or time budget simply to force a fill.

## Self-trade prevention requirements
- Use venue-supported STP where appropriate and model HCT-level conflicts across strategies/child orders sharing an account.
- Prevent avoidable self-crossing/fee churn without weakening required emergency reductions.

## Private event schema requirements
- Validate required fields and schema/semantic expectations on private order/fill/position streams.
- Preserve raw payload/provenance for investigation where permitted.
- Unknown or materially changed critical schema enters quarantine/degraded state rather than silently mapping to old semantics.

## Adaptive reconciliation requirements
- Reconciliation cadence may tighten during uncertain orders, private-stream gaps, protection changes, large fills, high volatility, conflicts or degraded API/WS state.
- Cadence may relax only within bounded policy under stable confirmed state.
- Adaptive cadence cannot suppress mandatory protection or risk checks.

## Observability requirements
Expose at minimum:
- Order Intent and command identities;
- external/client and exchange order IDs;
- parent/child/mutation lineage;
- evidence level;
- partial fill progress;
- expected versus realized price/cost;
- slippage/time budget consumption;
- protection coverage and establishment latency;
- reconciliation watermark/age;
- unresolved conflicts and uncertain orders;
- risk reservation linkage;
- quota/clock health;
- recovery mode and State Confidence.

## Validation requirements
R04 implementation-time evidence must test at minimum:
- duplicate submission and duplicate event delivery;
- timeout after submit;
- fill while cancel is in flight;
- partial fill then replace;
- late order/fill events;
- market order partial fill with remainder cancellation where venue behavior allows;
- One-Way versus Hedge mode close/reduce semantics;
- stop/TP quantity after partial fill/reduction;
- protection establishment timeout;
- restart with unknown live order;
- reconciliation conflict;
- private-stream gap/schema drift;
- quota exhaustion while protection is needed;
- clock drift/request-time rejection;
- fee schedule/version changes;
- R03 reservation conservation through all order lifecycle paths.

## Invariants
- REST success != fill truth.
- Timeout != failure.
- Cancel requested != cancelled.
- One fill identity cannot affect economics twice.
- Stale authorization cannot transmit new exposure.
- REDUCE/CLOSE cannot accidentally increase/reverse exposure.
- Required protection is verified against actual filled exposure.
- Unresolved critical reconciliation conflicts block new exposure.
- Restart cannot resume normal exposure until recovery proof passes.
- Risk reservation accounting is conserved through execution outcomes.

## STOP CONDITION
Do not mark R04 `APPROVED` until these requirements, Decisions Ledger entries, Scope, the 22-gap audit, the 19 acceptance gates and the PR state are mutually consistent with no unresolved CRITICAL/HIGH planning defect.
