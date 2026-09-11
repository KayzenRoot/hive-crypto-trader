# HCT-PLAN-0001-R05 — Realtime Market Data / WebSocket / Quota / Cache / Resilience Gap Audit

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R05`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`
Initial verdict: `CORRECTION REQUIRED`

## Objective
Formally reconcile the realtime/data pre-discovery captured in docs 30–33 against the needs of a HIGH_ASSURANCE automated futures platform and identify remaining gaps before R05 can be promoted.

This round covers the sensory and transport layer that feeds Scanner, Features, Strategy, Brain, Risk, Execution and Reconciliation. Bad realtime state must fail safe rather than silently become trading truth.

## Canonical pre-discovery inputs
- `docs/30-realtime-market-data-intelligence-and-streaming-rd.md`;
- `docs/31-realtime-performance-benchmark-and-technology-selection.md`;
- `docs/32-bootstrap-free-infrastructure-and-scale-migration.md`;
- `docs/33-microstructure-orderflow-liquidity-breadth-and-anomaly-intelligence.md`;
- R04 execution/reconciliation contracts;
- MEXC Futures API/WebSocket documentation and current API update announcements.

## Current strengths already accepted as foundation
- separation of Exchange Edge, hot Market-State Fabric and durable Research/Replay planes;
- canonical event envelope with exchange/event/receive/processing timestamps;
- order-book reconstruction with gap detection and `UNTRUSTED` state;
- Market State Integrity Score / Feed Confidence / Data-to-Decision Age concepts;
- adaptive subscription planning and bounded load shedding;
- feature freshness/coherency barriers and market-state generation IDs;
- replay fidelity and point-in-time provenance;
- provider-neutral infrastructure selection and free-first bootstrap policy;
- explicit rule that slow analytics may not block hot trading/safety paths.

## External facts revalidated for R05
- MEXC Futures API remains the current V1 venue target and provides realtime market-data access through the Futures API stack.
- Current API Futures fees effective 2026-06-01 are maker 0.06% / taker 0.08%; fee data is not a realtime-market-data primitive but remains an example of mutable provider state that cannot be frozen forever.
- MEXC publicly offers institutional users the possibility of higher API rate limits; therefore generic and account-specific limits must remain dynamically configurable rather than treated as universal constants.
- Current official API-update material confirms Futures API availability can vary by region and provider rules may change.

## R05 gaps

### GAP-R05-01 — Canonical channel capability registry
Severity: `CRITICAL`

Need a runtime registry of which public/private WS channels and REST fallbacks exist per venue/version, including payload schema, snapshot/delta semantics, update cadence, sequencing guarantees, symbol scope and subscription limits.

### GAP-R05-02 — WebSocket session generation and reconnect identity
Severity: `CRITICAL`

Every connection/reconnect must receive a generation/session identity. Data from an old socket must never silently mix with a new reconstructed market state after reconnect.

### GAP-R05-03 — Snapshot/delta synchronization barrier
Severity: `CRITICAL`

For any state reconstructed from snapshot + deltas, define the exact barrier for buffering, applying, rejecting and resyncing updates. Consumers must not see a book as trusted before synchronization is complete.

### GAP-R05-04 — Sequence-gap semantics by channel
Severity: `CRITICAL`

Do not assume all channels expose identical sequence semantics. Need per-channel gap detection, duplicate handling, out-of-order policy and explicit `SEQUENCE_UNPROVABLE` when the provider does not expose enough metadata.

### GAP-R05-05 — Cross-channel contradiction handling
Severity: `HIGH`

Ticker, trades, book, candles and REST snapshots can disagree temporarily. Define contradiction detection, authority hierarchy and when contradictions degrade confidence or trigger resync.

### GAP-R05-06 — Subscription budget accounting
Severity: `HIGH`

Adaptive Subscription Planner needs deterministic accounting for sockets, symbols, channels, messages/requests and reconnect/resubscribe pressure. There must be no unbounded subscribe-everything behavior.

### GAP-R05-07 — Reconnect storm governor
Severity: `CRITICAL`

A venue/network incident can trigger synchronized reconnect loops. Need jittered bounded exponential backoff, reconnect budgets, circuit states and protection against subscription thundering herd.

### GAP-R05-08 — Private-vs-public transport isolation
Severity: `HIGH`

Private account/order streams and public market-data streams must be isolated enough that public burst load cannot starve private execution/protection/reconciliation traffic.

### GAP-R05-09 — Backpressure contract by consumer class
Severity: `CRITICAL`

Define bounded queues, overflow policy and priority for Safety/Risk/Execution, active-position features, scanner, research and persistence. Dropping a scanner update is not equivalent to dropping a protection-critical state update.

### GAP-R05-10 — Deterministic load shedding
Severity: `CRITICAL`

Load shedding must be policy-driven and observable. It may reduce universe breadth, depth, feature richness or research work, but must preserve minimum safety/execution feeds and never silently pretend full fidelity.

### GAP-R05-11 — Event-time / receive-time / processing-time SLA classes
Severity: `HIGH`

Need explicit freshness/latency budgets by data class and consumer horizon. One global `stale after N ms` threshold is insufficient.

### GAP-R05-12 — Clock synchronization and monotonic-time contract
Severity: `CRITICAL`

Wall clock, exchange time and monotonic elapsed time have different roles. Need clock-health state, drift detection and clear prohibition on using unstable wall-clock differences for latency/signal-age decisions.

### GAP-R05-13 — Candle integrity and late-trade correction policy
Severity: `HIGH`

Define whether candles are venue-native, locally reconstructed or both; how late/out-of-order trades affect open/closed bars; how revisions are versioned; and how strategy/replay reproducibility is preserved.

### GAP-R05-14 — Market-state generation / feature coherency barrier
Severity: `CRITICAL`

Multi-input features cannot combine book generation N, trade generation N+4 and stale candle generation N-2 without explicit coherency policy. Need a consumer-visible generation/coherency contract.

### GAP-R05-15 — Hot-cache truth boundaries
Severity: `HIGH`

Define which data may be served from local/in-process/Redis-like cache, TTL/freshness leases, invalidation, and hard prohibition on cache becoming authoritative exchange order/fill/account truth.

### GAP-R05-16 — Persistence failure isolation
Severity: `CRITICAL`

Durable event-log/time-series/database outage must not block the hot safety/execution path indefinitely. Need bounded spill/degraded behavior and explicit evidence-loss state.

### GAP-R05-17 — Replay-capture completeness watermark
Severity: `HIGH`

Research replay must know whether a captured interval is complete, degraded or missing channels. Need capture manifests/watermarks and no false claim of full-fidelity replay.

### GAP-R05-18 — Schema evolution / unknown-field quarantine
Severity: `CRITICAL`

Critical public/private payload schema drift must trigger validation, quarantine and confidence degradation rather than silent coercion into old structures.

### GAP-R05-19 — Symbol lifecycle and universe churn
Severity: `HIGH`

Contracts can appear, disappear, pause or change trading state. Universe Registry, subscriptions, caches, features and strategies must converge safely without orphaned stale symbol state.

### GAP-R05-20 — Data-quality influence on authority
Severity: `CRITICAL`

Define exactly how MSIS/feed confidence/freshness/coherency states map to `ALLOW`, `DEGRADED`, `NO_NEW_EXPOSURE`, `REDUCE_ONLY`, `RECONCILIATION_ONLY` and emergency behavior. Scores alone are insufficient without deterministic gates.

### GAP-R05-21 — Burst isolation and microburst admission control
Severity: `HIGH`

Market shocks can multiply event rate. Need admission control, aggregation/coalescing rules where safe, CPU-budget isolation and tail-latency monitoring so bursts do not starve Safety/Risk/Execution.

### GAP-R05-22 — Feature compute budget and cancellation
Severity: `HIGH`

Features/agents requested for opportunities that expire or leave the shortlist should be cancellable. Need CPU/memory budget accounting and stale-work cancellation to preserve decision freshness.

### GAP-R05-23 — Data-to-decision age budget propagation
Severity: `CRITICAL`

Latency budget must propagate from event reception through normalization, features, Brain, Risk and execution so the final decision knows how much signal lifetime has already been consumed.

### GAP-R05-24 — Multi-instance/failover ownership
Severity: `HIGH`

If multiple workers or future HA instances exist, define single-writer/leader/ownership rules for market-state reconstruction, subscriptions and authoritative hot-state publication to avoid duplicate or divergent state.

### GAP-R05-25 — Bootstrap free-tier survivability
Severity: `HIGH`

Free-first infrastructure must define what remains local/in-process, what can safely use free cloud tiers, quota exhaustion behavior and migration triggers. Free service suspension/pausing must never become a hidden live-trading single point of failure.

### GAP-R05-26 — Observability without hot-path distortion
Severity: `HIGH`

Metrics/traces/logging must expose p50/p95/p99/p99.9 latency, queue depth, gaps, resyncs, drops, reconnects, freshness, CPU/memory and recovery time without itself becoming a material hot-path bottleneck.

## Priority closure order
### CRITICAL first
1. channel capability registry;
2. WS generation/reconnect identity;
3. snapshot/delta synchronization barrier;
4. per-channel sequence/gap semantics;
5. reconnect storm governor;
6. backpressure contracts;
7. deterministic load shedding;
8. clock/monotonic-time contract;
9. feature coherency barrier;
10. persistence failure isolation;
11. schema evolution/quarantine;
12. deterministic data-quality authority mapping;
13. data-to-decision age propagation.

### HIGH next
Cross-channel contradiction, subscription budgets, private/public isolation, SLA classes, candle integrity, cache boundaries, replay watermark, symbol lifecycle, microburst admission, feature compute budget, multi-instance ownership, free-tier survivability and low-distortion observability.

## Initial R05 verdict
`CORRECTION REQUIRED`

Reason: the pre-discovery architecture is strong, but the CRITICAL contracts above must be made canonical before R05 can be promoted.

## Next necessary action
Create the formal R05 realtime transport/state-resilience architecture that closes the CRITICAL gaps first, then define R05 acceptance gates and run the final audit.

## STOP CONDITION
Do not approve R05 until all CRITICAL/HIGH planning gaps have canonical resolution, deterministic authority mapping, recovery behavior, validation requirements and explicit provider/version dependencies. No implementation Work Order or live-trading authorization before checkpoint promotion.
