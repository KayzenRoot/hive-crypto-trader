# Realtime Market Data Intelligence & Streaming R&D

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R02`
Risk class: `HIGH_ASSURANCE`

## Objective
The realtime data layer is the sensory system of HCT. Strategy quality, agent reasoning, risk decisions and execution quality cannot exceed the integrity, freshness and temporal correctness of the market state they consume.

This architecture therefore treats market data as a high-assurance decision dependency rather than a generic websocket feed.

Primary goals:
- minimize avoidable end-to-end market-state latency;
- detect stale, missing, reordered, duplicated or contradictory data before it reaches trading decisions;
- preserve event-time provenance from exchange receipt through feature/strategy consumption;
- support broad-universe scanning without overwhelming exchange/API quotas or internal compute;
- maintain deterministic replayability;
- continuously estimate whether the current market state is trustworthy enough for new exposure;
- scale from MEXC V1 to future exchange adapters without rewriting the trading brain;
- optimize decision timeliness and execution opportunity capture without claiming or guaranteeing profitability.

## External technology research snapshot — 2026-09-11
The following technologies are research candidates, not frozen implementation choices.

### Redpanda
Current Redpanda 26.x positions itself as Kafka-compatible event streaming with low latency, no JVM dependency, schema registry, tiered storage, idempotent/transactional patterns and broad Kafka-client compatibility.

Potential HCT fit:
- durable internal event backbone;
- market-event fanout;
- replayable event streams;
- decoupling scanners/features/agents/analytics;
- long-running production stream retention.

### NATS / JetStream
JetStream provides durable streams, acknowledgments, deduplication/exactly-once mechanisms, per-consumer flow control and push/pull consumption.

Potential HCT fit:
- lightweight low-latency service messaging;
- fast command/control/event fanout;
- durable queues for selected workflows;
- agent/tool/service request-reply.

### Aeron
Aeron Transport is designed for very high throughput with low and predictable latency; Aeron Archive supports recording/replay; Aeron Cluster adds ordered fault-tolerant messaging.

Potential HCT fit:
- ultra-low-latency in-process/inter-process market-state distribution;
- specialized hot-path transport where benchmark evidence justifies added complexity;
- deterministic stream recording/replay research.

Aeron is a candidate for selective hot paths, not an automatic default for the entire platform.

### QuestDB
QuestDB is a time-series database focused on high-throughput ingestion and low-latency analytics, with time-series joins and query operators useful for market data.

Potential HCT fit:
- ticks/trades/order-book-derived time series;
- feature research;
- high-speed historical analog queries;
- replay and diagnostics.

### ClickHouse
ClickHouse remains a strong candidate for large-scale realtime analytical workloads, high-cardinality telemetry and broad historical analytics.

Potential HCT fit:
- observability/telemetry analytics;
- strategy and execution research;
- aggregated market history;
- multi-tenant analytical workloads.

### RisingWave
RisingWave provides incremental stream processing and continuously maintained materialized views with low-latency serving.

Potential HCT fit:
- realtime derived market-state views;
- continuously updated cross-symbol metrics;
- streaming joins/windows;
- precomputed regime/breadth/liquidity features.

### TimescaleDB
TimescaleDB remains a candidate where PostgreSQL compatibility, hypertables and continuous/realtime aggregates provide operational simplicity.

Potential HCT fit:
- lower-complexity time-series persistence;
- operational data where Postgres compatibility is valuable;
- continuous aggregates for slower-path features.

## Technology selection rule
No external streaming/database technology is frozen merely because vendor benchmarks look impressive.

HCT must benchmark candidate components under HCT-specific workloads:
- MEXC-like tick rates;
- order-book updates;
- burst volatility;
- broad symbol universe;
- mixed realtime + replay workload;
- p50/p95/p99/p99.9 latency;
- throughput;
- memory/CPU utilization;
- recovery time;
- message loss/duplication behavior;
- operational complexity;
- multi-tenant cost;
- deterministic replay fidelity.

Technology may differ by path. HCT may use one system for durable event streaming, another for ultra-hot local state and another for analytical history.

## Three-plane market data architecture

### Plane A — Exchange Edge
Responsibilities:
- WebSocket/REST connectivity;
- subscription lifecycle;
- authentication where applicable;
- timestamp capture;
- sequence/channel normalization;
- exchange-specific payload validation;
- raw event provenance;
- reconnect/resubscribe logic;
- API/quota coordination.

### Plane B — Realtime Market-State Fabric
Responsibilities:
- normalization into canonical events;
- deduplication;
- ordering where defined;
- event-time/receive-time/processing-time preservation;
- local order-book construction;
- gap detection;
- freshness scoring;
- hot-state publication;
- lightweight derived state;
- fanout to scanner/features/risk/execution.

### Plane C — Durable Research & Replay
Responsibilities:
- raw/event-normalized retention;
- deterministic replay;
- feature reconstruction;
- post-trade evidence;
- research/backtest datasets;
- incident reconstruction;
- model/RAG historical access.

A slow analytical consumer must never block the realtime hot path.

## Canonical market event envelope
Every normalized event should preserve at least:
- exchange;
- instrument canonical ID;
- exchange symbol;
- event type;
- exchange event timestamp when supplied;
- local receive timestamp;
- normalization timestamp;
- sequence/update identifiers where supplied;
- source connection/session ID;
- payload/schema version;
- data-quality flags;
- provenance/raw reference;
- replay correlation ID.

Derived features should retain input-time boundaries and data-quality context.

## Clock model
HCT should distinguish:
- exchange/source event time;
- network receive time;
- local monotonic processing time;
- persistence time;
- feature-ready time;
- strategy-consumption time;
- order-intent time;
- exchange-acknowledgment time.

Wall-clock time alone is insufficient for latency analysis.

Clock synchronization monitoring should detect drift and avoid comparing timestamps from different clock domains as though they were exact.

## Order book reconstruction
Where the exchange provides incremental depth semantics, HCT should maintain deterministic local books with:
- snapshot + delta semantics where applicable;
- sequence validation;
- duplicate suppression;
- crossed-book checks;
- negative/invalid size checks;
- impossible price-level state checks;
- gap-triggered resynchronization;
- book age/freshness;
- reconstruction generation/version.

A book that cannot be proven coherent becomes `UNTRUSTED` rather than silently reused.

## HCT proprietary realtime technologies

### 1. HCT Market State Integrity Score (MSIS)
Composite confidence in the current market state using:
- feed freshness;
- sequence continuity;
- book coherence;
- cross-channel agreement;
- timestamp health;
- reconnect history;
- latency stability;
- source availability;
- recent gap-healing events.

Possible states:
`TRUSTED`, `DEGRADED`, `UNTRUSTED`, `UNKNOWN`.

MSIS can gate new exposure but cannot increase hard risk limits.

### 2. HCT Feed Confidence Matrix (FCM)
Maintain per-symbol/per-channel trust instead of one global feed-health flag.

Example dimensions:
- trades;
- ticker;
- candles;
- order book;
- mark/fair/index;
- funding;
- open interest;
- private order stream;
- private position stream.

A strategy requiring order-book data may be disabled while slower candle-based analytics continue safely.

### 3. HCT Adaptive Subscription Planner (ASP)
Dynamically allocate WebSocket/API subscription budget based on:
- active positions;
- pending orders;
- scanner rank;
- strategy dependencies;
- volatility;
- liquidity;
- user watchlists;
- agent investigation;
- exchange quota budget;
- compute pressure.

Subscription priority tiers:
`CRITICAL`, `HOT`, `WARM`, `COLD`, `ON_DEMAND`.

Critical position/protection/reconciliation feeds outrank exploratory scanning.

### 4. HCT Signal Freshness Decay (SFD)
Every strategy/feature signal has a useful temporal half-life rather than remaining equally valid until explicitly replaced.

Inputs may include:
- strategy horizon;
- market velocity;
- volatility;
- liquidity changes;
- event/news risk;
- feature update cadence;
- elapsed time since evidence formation.

SFD allows the system to reject execution of technically valid but temporally expired decisions.

### 5. HCT Latency Budget Controller (LBC)
Assign latency budgets to the decision chain:
`exchange -> ingest -> normalize -> feature -> strategy -> risk -> execution`.

Track both absolute latency and percentage of signal half-life consumed.

Example:
- signal useful lifetime: 2,000 ms;
- data + feature pipeline consumed: 1,450 ms;
- execution estimate: 700 ms;
- decision is now temporally invalid despite being logically valid.

### 6. HCT Order Book Consistency Engine (OBCE)
Continuously validates local depth state using structural invariants, sequence rules and cross-channel observations.

Research extensions:
- anomaly likelihood;
- liquidity spoof/noise indicators;
- depth stability;
- local-book confidence by level.

It is a data-integrity component first, not a market-manipulation oracle.

### 7. HCT Data Gap Healing Engine (DGHE)
When gaps are detected:
- isolate affected stream;
- preserve last-known-good generation;
- request/reconstruct authoritative state;
- replay buffered deltas only when validity can be proven;
- bump market-state generation;
- emit explicit recovery evidence.

No silent interpolation of order-book truth.

### 8. HCT Market Data Twin (MDT)
Run a non-authoritative shadow reconstruction of selected high-value market state.

Primary and twin pipelines can compare:
- event counts;
- order-book hashes;
- candle outputs;
- feature summaries;
- latency;
- missing/duplicate events.

Divergence becomes an operational alarm and research signal.

### 9. HCT Event-Time Provenance Graph (ETPG)
For any trade decision, reconstruct the exact causal data lineage:
`raw exchange event -> normalized event -> feature -> strategy node -> agent evidence -> risk decision -> execution intent`.

This supports audit, debugging, replay and false-signal investigation.

### 10. HCT Market Velocity Adaptive Compute (MVAC)
Allocate compute frequency according to how quickly the market is changing.

Quiet market:
- reduce expensive recomputation where safe.

Fast market:
- increase priority/frequency for relevant symbols/features while shedding low-value work.

Hard quota/safety limits remain fixed.

### 11. HCT Opportunity Compute Scheduler (OCS)
Rank computational work by expected decision relevance rather than process all symbols/features equally.

Pipeline:
`cheap universe screen -> lightweight features -> shortlist -> richer multi-timeframe analysis -> agents -> execution-grade state`.

This is intended to maximize useful intelligence per CPU/API unit and reduce latency on high-value opportunities.

### 12. HCT Cross-Channel Truth Reconciler (CCTR)
Compare semantically related feeds such as:
- ticker vs best bid/ask;
- trades vs candle construction;
- mark/fair/index relationships;
- position/order private streams vs REST reconciliation.

Contradictions lower confidence instead of being arbitrarily resolved.

### 13. HCT Realtime Candle Integrity Engine (RCIE)
Build canonical candles from raw trade/event data where appropriate and compare them with exchange-provided candles.

Track:
- completeness;
- late trades;
- boundary timing;
- exchange candle divergence;
- generation/version.

Strategies can declare whether they consume exchange-native or HCT-canonical candles.

### 14. HCT Microburst Detector (MBD)
Identify abrupt event-rate/price/liquidity bursts that may indicate the system should:
- increase compute priority;
- shorten cache TTL;
- widen safety assumptions;
- suppress stale strategies;
- increase execution scrutiny;
- pause low-priority research workloads.

### 15. HCT Data-to-Decision Age (DDA)
Every candidate decision carries the age of its oldest critical evidence and age distribution of contributing inputs.

A decision can be rejected if critical evidence exceeds strategy-specific freshness policy.

### 16. HCT Market-State Generation ID (MSGID)
Every coherent market-state rebuild/recovery receives a generation ID.

Strategy, risk and execution evidence can then prove they were computed against the same coherent generation rather than mixing pre-gap and post-gap state.

### 17. HCT Feature Coherency Barrier (FCB)
For strategies requiring synchronized multi-feature/multi-timeframe evidence, prevent accidental mixing of feature values computed from incompatible event-time windows.

This is especially important during reconnects, late data and catch-up processing.

### 18. HCT Hot-State Lease (HSL)
Hot-state entries are consumed only while an explicit freshness lease remains valid.

When the lease expires:
- consumers see `STALE` rather than an old value masquerading as current truth;
- safety policies may block new exposure;
- refresh/reconciliation is triggered according to dependency criticality.

### 19. HCT Stream Load Shedding Governor (SLSG)
Under CPU/memory/network pressure, shed work by deterministic priority:
1. protection/reconciliation;
2. open-position market state;
3. pending-order execution state;
4. top scanner candidates;
5. broad scanning;
6. research/visual extras.

Safety-critical processing is never sacrificed to preserve decorative dashboards or low-value analytics.

### 20. HCT Market Data Replay Fidelity Score (MRFS)
Measure whether historical replay reproduces the same canonical state/feature sequence expected from live processing.

A backtest/replay engine with poor fidelity must not be used to justify production promotion.

## Microstructure intelligence candidates
Beyond basic bid/ask, HCT research may derive:
- order-book imbalance by distance band;
- depth slope/convexity;
- spread regime;
- trade-sign imbalance;
- short-window aggressor pressure;
- liquidity replenishment rate;
- cancellation/appearance velocity where observable;
- microprice variants;
- realized short-horizon volatility;
- price impact estimate;
- liquidity vacuum risk;
- depth resilience after large trades;
- short-lived dislocation detection.

These are evidence features, not guaranteed alpha.

## Stream processing architecture candidate
A practical research architecture is:

`MEXC WebSocket/REST -> Exchange Edge -> Canonicalizer -> Hot Market-State Fabric -> Feature/Scanner Consumers`

with asynchronous durable branch:

`Canonical Events -> Durable Event Log -> Time-Series/Analytical Store -> Replay/Research/RAG`

Potential implementation mix to benchmark:
- Core NATS/Aeron/shared-memory style hot path for ultra-low latency;
- Redpanda/Kafka-compatible durable backbone for replay/fanout;
- QuestDB for high-frequency time-series research;
- ClickHouse for broad analytical/telemetry workloads;
- RisingWave for streaming materialized features where incremental SQL is advantageous;
- Redis or equivalent only for explicitly leased hot cache, never as exchange truth.

The final architecture may intentionally use fewer technologies if benchmarks show that operational simplicity produces better end-to-end reliability/latency.

## Performance engineering rules
- benchmark end-to-end, not only isolated broker throughput;
- track tail latency, not only averages;
- avoid unnecessary serialization/deserialization on hot paths;
- batch only where batching does not destroy signal timeliness;
- use bounded queues and explicit backpressure;
- avoid unbounded fanout;
- separate CPU-heavy analytics from safety/execution loops;
- prefer monotonic clocks for elapsed-time measurement;
- instrument queue wait, processing, serialization, network and persistence separately;
- use deterministic schemas and versioning;
- preserve raw evidence sufficient to reproduce incidents;
- benchmark failure/reconnect behavior, not just steady state.

## Market-data decision gate
Before a new exposure decision reaches Safety/Risk, the system should be able to answer:
- Are all required feeds available?
- Are they fresh enough for this strategy?
- Is the order book coherent if required?
- Are timestamps/sequence state trustworthy?
- Did a reconnect/gap occur inside the evidence window?
- Are multi-timeframe features coherent?
- How much of the signal's useful lifetime has already been consumed?
- Is internal compute under pressure?
- Is the current state generation consistent across strategy/risk/execution?

If critical answers are unknown, `NO_NEW_EXPOSURE` is valid.

## MEXC-specific current planning note
MEXC Futures API is now a live API product and official 2026 announcements state that API users can access realtime futures market data/trading information and trade eligible futures pairs. MEXC also changed its Futures API access domain in January 2026, illustrating why endpoints/capabilities must be treated as versioned external dependencies rather than hard-coded assumptions.

Exact WebSocket subscription/rate limits and current channel semantics must be verified from the official Futures API documentation during implementation/preflight and represented as adapter-provided runtime configuration rather than frozen globally in planning docs.

## Validation requirements
Before production promotion, the market-data layer should pass:
- synthetic gap/reorder/duplicate tests;
- disconnect/reconnect storms;
- burst-load tests;
- stale-source tests;
- clock-drift tests;
- order-book corruption tests;
- exchange snapshot disagreement;
- backpressure/load-shedding tests;
- replay determinism;
- primary-vs-twin divergence tests;
- storage outage tests;
- hot-cache expiry tests;
- multi-timeframe coherency tests;
- p50/p95/p99/p99.9 latency reporting;
- failure-recovery timing.

No technology candidate is considered production-ready solely because it is fast in a vendor benchmark.

## Research sources
- Redpanda Streaming documentation, 26.x: https://docs.redpanda.com/streaming/current/home/
- Redpanda Kafka compatibility: https://docs.redpanda.com/streaming/current/develop/kafka-clients/
- NATS JetStream documentation: https://docs.nats.io/nats-concepts/jetstream
- Aeron documentation: https://aeron.io/docs/
- QuestDB documentation: https://questdb.com/docs/
- ClickHouse realtime analytics resources: https://clickhouse.com/use-cases/real-time-analytics
- RisingWave documentation: https://docs.risingwave.com/
- TimescaleDB documentation: https://docs.timescale.com/
- MEXC Futures API announcements/documentation: https://www.mexc.com/announcements/api-updates and https://www.mexc.com/api-docs/futures/integration-guide
