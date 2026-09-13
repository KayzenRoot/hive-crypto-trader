# ADR-0048 — S1D quota and backpressure governor foundation

Status: Accepted for `HCT-IMP-0007-S1D` only

## Decision

S1D adds a provider-neutral, pure quota and backpressure decision surface for
the future realtime session boundary. The module accepts immutable typed
snapshots and returns immutable admission evidence. It performs no I/O, owns no
venue semantics, and cannot create a connection, subscription, request, order,
position or execution handle.

The governor owns only request/subscription budget evidence, priority ordering,
bounded queue admission, finite retry state, circuit state, session-generation
identity and non-executable subscription intent. Exchange reference, capability,
universe, market ingest, Data Quality, Market-State, cache, Scanner, Risk,
Safety, Session, OMS and Execution retain their existing authority boundaries.

## Fail-closed typed policy

Request and subscription quotas are independent. A missing capacity is explicit
unknown evidence and yields `UNKNOWN`; it is never converted into an unlimited
default. Capacities, replenishment values, queue sizes, retry attempts and
elapsed-time budgets are positive or bounded typed values. Contradictory
snapshots are rejected before a decision is produced.

Priority is finite and deterministic: `PROTECTION`, `RECONCILIATION`, `NORMAL`,
then `RESEARCH`. Protected reserve is available only to protection and
reconciliation classes for both quota units and queue capacity. Queue
saturation, protected reserve exhaustion, exhausted budget and exhausted retry
state defer protected work and shed research work. Every outcome carries a
finite reason and a content fingerprint.

Admission evidence has an explicit outcome/reason matrix: `ADMIT` only pairs
with `ADMITTED`; `UNKNOWN` only pairs with `UNKNOWN_BUDGET`; `CIRCUIT_OPEN`
only pairs with `CIRCUIT_OPEN` or `PROBE_IN_FLIGHT`; `DEFER` and `SHED` accept
only their declared stale, retry, queue, reserve and budget reasons. The public
factory recomputes the fingerprint from canonical material and does not accept
a caller-supplied digest.

## Retry, circuit and session identity

Retries are bounded by both attempts and monotonic elapsed time. Circuit state
is a pure `CLOSED`/`OPEN`/`HALF_OPEN` state machine with a single explicitly
reserved probe slot. `CLOSED` cannot carry open time, a probe or a reached
failure threshold; `OPEN` requires threshold evidence, open time and no probe;
`HALF_OPEN` can close only after an in-flight probe succeeds and can reopen only
after that probe fails. Direct contradictory construction and invalid recovery
transitions are rejected. The circuit fingerprint covers state, failure count,
failure threshold, cooldown, open time and probe state. Session generations are
strictly increasing, stale or retired generations cannot admit work, and
subscription intents bind a canonical `StableId(kind=INSTRUMENT)` to a live
generation without an executable transport reference. Fingerprints cover all
material policy, state, request and decision inputs so equal normalized inputs
produce equal evidence.

## Explicit non-goals and authorization firewall

This ADR authorizes no network client, URL or endpoint, WebSocket or realtime
ingest, venue subscribe/unsubscribe operation, reconnect I/O, credentials,
private/account state, trading, Risk, OMS, Execution, persistence, frontend
control, deployment, production credentials, limited-live or real-money
trading. The production boundary scanner also rejects `http://`, `https://`,
`ws://`, `wss://` and domain/host literals, while allowing only the exact
HCT-owned canonical identity import required by subscription intent validation.
Planning freeze and implementation authorization do not authorize live trading.
The S1D ceiling remains
`NON_TRADING_STAGE_1_QUOTA_WS_BACKPRESSURE_GOVERNOR_FOUNDATION_ONLY`.
