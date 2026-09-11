# HCT-PLAN-0001-R05 — Realtime Requirements Addendum

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R05`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

This addendum is the canonical R05 requirements source set pending final planning-freeze consolidation into the product-wide Requirements document.

## Transport and feed requirements
- Maintain a versioned channel capability registry for every venue/channel used by HCT.
- Assign a local generation identity to each WebSocket connection/reconnection and prevent retired generations from mutating current trusted state.
- Require explicit synchronization proof before snapshot+delta reconstructed state becomes trusted.
- Define sequence/gap/duplicate/out-of-order policy per channel; unsupported sequence proof must be represented as `SEQUENCE_UNPROVABLE`.
- Apply bounded reconnect backoff, jitter, retry budgets, circuit breakers and staged resubscription.
- Isolate private execution/account streams from public market-data burst load where practical.

## Backpressure and resource requirements
- Use bounded queues by priority class.
- Preserve emergency, protection, reconciliation, active-position and execution-critical workloads before scanner/research workloads.
- Implement deterministic, observable load shedding.
- Maintain resource reserves for safety-critical realtime paths.
- Cancel stale/expired feature or agent work whose opportunity is no longer relevant.

## Time and freshness requirements
- Separate exchange event time, wall receive time and monotonic elapsed time.
- Use monotonic time for latency/age budgets wherever possible.
- Monitor exchange/wall clock drift and expose explicit clock-health states.
- Propagate Data-to-Decision Age and remaining signal lifetime through feature, Brain, Risk and Execution stages.
- Expired opportunities must not be forced through execution.
- Define freshness/latency SLA classes by consumer horizon rather than one global timeout.

## State coherency requirements
- Assign generation/provenance to market state and derived feature bundles.
- Prevent materially incoherent cross-generation feature sets from silently entering strategy/Brain decisions.
- Detect and classify contradictions across ticker, trades, order book, candles and REST evidence.
- Represent unresolved critical contradiction as degraded/untrusted authority rather than averaging it away.

## Candle/cache/replay requirements
- Record candle provenance, source, finality and revisions.
- Preserve point-in-time reproducibility of the candle version knowable at historical decision time.
- Hot-cache entries require generation, TTL/freshness lease, provenance and invalidation semantics.
- Cache may not become authoritative truth for orders, fills, balances or positions.
- Replay captures require completeness manifests and explicit fidelity classes.

## Persistence and schema requirements
- Durable storage failure must be isolated from the hot safety path with bounded buffering and explicit evidence-degraded state.
- If safe recovery/audit evidence can no longer be guaranteed, new exposure must tighten or stop.
- Critical realtime payloads require schema validation.
- Unknown/malformed critical payloads are preserved and quarantined, reduce confidence and trigger reconciliation/resync as appropriate.

## Universe lifecycle requirements
- Symbols/contracts require explicit lifecycle states and safe convergence across subscriptions, caches, features, strategies and open-position handling.
- Paused/delisted/ineligible symbols cannot remain silently active in scanner or strategy state.

## Authority requirements
- Data-quality scores are explanatory; deterministic hard predicates map realtime health to trading-authority states.
- Required feed untrusted, unresolved critical private-state uncertainty, severe contradiction or safety-critical resource starvation can block new exposure.
- No aggregate confidence score may hide a failed critical realtime predicate.

## HA and bootstrap requirements
- Future multi-instance state reconstruction requires single-writer ownership and fencing to prevent split brain.
- Failover takeover requires synchronization/recovery proof before publishing trusted state.
- Free-first cloud services must not become hidden safety-critical hot-path single points of failure.
- Migration triggers include measured quota, tail-latency, evidence-lag, reliability, HA, security/compliance and customer-scale thresholds.

## Observability requirements
- Measure p50/p95/p99/p99.9 stage and end-to-end latency.
- Observe event/byte rates, queue depth/age, gaps, resyncs, reconnects, drops/coalescing, freshness, coherency, schema quarantine, CPU/memory, persistence lag and Recovery-to-Trusted-State Time.
- Telemetry itself must be bounded and shed before it materially harms safety-critical hot-path work.

## Validation requirements
Implementation planning must test at least:
- retired-generation late events;
- snapshot/delta synchronization races;
- duplicate/missing/out-of-order events;
- reconnect storms;
- public/private load isolation;
- priority queue saturation;
- deterministic shedding;
- clock drift/jumps;
- mixed-generation feature inputs;
- candle revisions;
- persistence outage;
- schema drift;
- symbol lifecycle changes;
- microbursts;
- stale-work cancellation;
- ownership/failover fencing;
- end-to-end signal expiry;
- recovery-to-trusted-state timing.

## Safety
These are planning requirements only. They do not authorize implementation, production credentials or live trading.