# HCT-PLAN-0001-R05 — Acceptance Criteria & Review Gates

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R05`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

## Purpose
Define objective planning gates that must pass before R05 can receive `APPROVED`.

## Gate A — Channel capability truth
Channel/version/snapshot/delta/sequence/subscription behavior is explicit and provider-versioned. Unknown semantics remain UNKNOWN.

## Gate B — Feed generation isolation
Old/retired WebSocket generations cannot mutate the current trusted market state.

## Gate C — Snapshot/delta proof
State reconstructed from snapshot+deltas cannot be published trusted before synchronization proof succeeds.

## Gate D — Sequence/gap correctness
Each channel has explicit duplicate/out-of-order/gap policy, including `SEQUENCE_UNPROVABLE` when continuity cannot be proven.

## Gate E — Reconnect resilience
Reconnect storms are bounded by backoff, jitter, budgets, circuit breakers and staged resubscription.

## Gate F — Backpressure & load shedding
Queues are bounded by priority class and load shedding follows a deterministic observable ladder that protects Safety/Protection/Reconciliation.

## Gate G — Time integrity
Monotonic time drives elapsed-age calculations; exchange/wall-clock drift is separately monitored and untrusted clocks block time-sensitive exposure.

## Gate H — Market-state coherency
Features/decisions carry exact input generations and freshness, with explicit mixed/stale/untrusted states.

## Gate I — Persistence isolation
Durable-store failure cannot silently stall the hot safety path; evidence degradation is explicit and can tighten trading authority.

## Gate J — Schema resilience
Unknown/malformed critical payloads are quarantined, preserved and trigger confidence/reconciliation effects rather than guessed coercion.

## Gate K — Data quality authority
Data-quality/freshness/coherency failures map deterministically to ALLOW/DEGRADED/NO_NEW_EXPOSURE/REDUCE_ONLY/RECONCILIATION_ONLY/EMERGENCY.

## Gate L — Decision freshness
End-to-end Data-to-Decision Age and remaining signal lifetime propagate through Brain/Risk/Execution; expired opportunities cannot be forced through.

## Gate M — Cross-channel contradictions
Contradictions across ticker/trades/book/candles/REST are detected, classified and escalated when unresolved.

## Gate N — Subscription/quota budgets
Sockets/channels/symbols/REST fallback/reconnect cost and compute cost are bounded by deterministic subscription budgets.

## Gate O — Public/private isolation
Public market bursts cannot starve private order/fill/protection/reconciliation streams.

## Gate P — Candle, cache & replay integrity
Candle revisions/provenance, cache freshness leases and replay capture-completeness classes are explicit and point-in-time reproducible.

## Gate Q — Symbol lifecycle
Venue symbol status changes converge through subscriptions, caches, features, strategy eligibility and position safety without orphan state.

## Gate R — Burst/compute survivability
Microbursts use bounded admission/resource policies and stale/expired feature work is cancellable.

## Gate S — HA ownership
Future multi-instance operation has single-writer ownership, fencing and takeover resynchronization rules preventing split brain.

## Gate T — Bootstrap survivability
Free-first services are isolated from safety-critical hot-path assumptions and explicit migration triggers exist.

## Gate U — Observability
p50/p95/p99/p99.9, queue age/depth, gaps, resyncs, reconnects, drops/coalescing, freshness, coherency, schema, CPU/memory, persistence lag and RTTS are observable without material hot-path distortion.

## Gate V — Validation plan
Planning requires deterministic tests for reconnect/gap/reorder/schema/burst/clock/persistence/symbol/failover/freshness conditions and recovery-to-trusted-state timing.

## Gate W — Canonical consistency
Before approval:
- all R05 decisions are in Decisions Ledger;
- accepted R05 requirements are canonical;
- Scope still forbids implementation/live authorization;
- all 26 gaps are resolved in planning;
- PR matches branch content;
- objective final R05 audit exists.

## Verdict rule
- unresolved CRITICAL/HIGH planning defect => `CORRECTION REQUIRED`;
- missing authoritative dependency necessary for planning => `BLOCKED`;
- all gates pass => `APPROVED`.

Implementation and live trading remain unauthorized regardless of R05 planning approval.