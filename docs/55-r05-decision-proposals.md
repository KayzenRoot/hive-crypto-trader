# HCT-PLAN-0001-R05 — Decision Proposals for Ledger Consolidation

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R05`
Date: `2026-09-11`

These decisions are accepted within R05 planning and must be copied into `docs/10-decisions-ledger.md` before final R05 approval.

## HCT-DEC-0058 — Trusted realtime state requires generation and synchronization proof
Status: APPROVED_FOR_DISCOVERY

Decision: every realtime feed/session uses explicit generation identity; retired generations cannot mutate current trusted state. Snapshot/delta reconstructed state becomes trusted only after synchronization continuity is proven under channel-specific semantics.

## HCT-DEC-0059 — Backpressure and load shedding preserve safety-critical traffic first
Status: APPROVED_FOR_DISCOVERY

Decision: realtime queues and resource budgets are bounded and priority-aware. Emergency, protection, reconciliation, active-position and execution-critical state outrank scanner, research and RAG workloads. Load shedding is deterministic, observable and cannot silently claim full fidelity after data/work has been dropped.

## HCT-DEC-0060 — Realtime time integrity uses monotonic age and explicit clock health
Status: APPROVED_FOR_DISCOVERY

Decision: HCT separates exchange event time, wall-clock chronology and monotonic elapsed time. Signal/data age and latency budgets use monotonic timing where possible; material clock drift or untrusted time blocks time-sensitive new exposure.

## HCT-DEC-0061 — Market-state and feature coherency are explicit trading prerequisites
Status: APPROVED_FOR_DISCOVERY

Decision: trusted market-state generations and derived features preserve exact input provenance, generation and freshness. Mixed/stale/untrusted generation combinations are explicit states and may block or degrade strategy/Brain authority according to horizon-specific policy.

## HCT-DEC-0062 — Critical schema/persistence failure is visible and may reduce trading authority
Status: APPROVED_FOR_DISCOVERY

Decision: unknown/malformed critical realtime schemas are preserved and quarantined rather than guessed. Durable evidence-store failure is isolated from the hot safety path, but if audit/recovery evidence can no longer be guaranteed HCT must tighten or stop new exposure instead of continuing invisibly.

## HCT-DEC-0063 — Data quality maps deterministically to trading authority
Status: APPROVED_FOR_DISCOVERY

Decision: feed confidence and data-quality scores are explanatory only. Hard realtime predicates deterministically map system state to `ALLOW_NEW_EXPOSURE`, `DEGRADED_NEW_EXPOSURE`, `NO_NEW_EXPOSURE`, `REDUCE_ONLY`, `RECONCILIATION_ONLY` or `EMERGENCY`; aggregate scores cannot mask a failed critical predicate.

## HCT-DEC-0064 — Decision freshness and signal lifetime propagate end-to-end
Status: APPROVED_FOR_DISCOVERY

Decision: each candidate action carries a Decision Freshness Envelope from market reception through features, Brain, Risk and Execution. If the remaining signal lifetime is insufficient for safe downstream processing/execution, the action expires or waits rather than being forced through.

## HCT-DEC-0065 — Subscription, cache, replay and symbol lifecycle are governed realtime resources
Status: APPROVED_FOR_DISCOVERY

Decision: subscriptions have deterministic quota/compute budgets; cache entries require freshness leases and never become exchange order/account truth; replay intervals require completeness/fidelity manifests; symbol lifecycle changes must converge safely through subscriptions, caches, features, strategies and position handling.

## HCT-DEC-0066 — Future HA realtime state requires single-writer ownership and fencing
Status: APPROVED_FOR_DISCOVERY

Decision: future multi-instance realtime reconstruction/publication uses explicit ownership leases and fencing tokens so only one writer publishes canonical state per partition. Failover takeover requires resynchronization/recovery proof before trusted publication resumes.
