# Realtime Performance Benchmark & Technology Selection Plan

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R02`
Risk class: `HIGH_ASSURANCE`

## Purpose
Select realtime infrastructure using reproducible HCT workloads rather than marketing benchmarks. The winning architecture is the one that delivers the best end-to-end decision freshness, reliability, replay fidelity and operational simplicity for HCT, not necessarily the lowest isolated broker latency.

## Candidate classes

### Hot transport / service messaging
- Core NATS
- NATS JetStream where durability is required
- Aeron for selected ultra-low-latency paths if justified
- direct in-process/shared-memory channels where architecture permits

### Durable event log
- Redpanda
- Kafka-compatible alternatives only if benchmarked
- NATS JetStream for smaller durable workloads where simpler topology wins

### Streaming computation
- native HCT incremental processors
- RisingWave for SQL-oriented streaming materialized views
- application-level windowed processing where lower complexity is superior

### High-frequency time-series store
- QuestDB
- TimescaleDB
- ClickHouse where workload characteristics justify it

### Broad analytics / telemetry
- ClickHouse
- Postgres/Timescale for smaller operational workloads

## Benchmark profiles

### Profile A — Quiet market
- broad symbol universe;
- low/moderate event rates;
- full scanner active;
- normal dashboard and agents.

### Profile B — Volatility burst
- concentrated burst across top symbols;
- rapidly changing order books;
- increased trades/ticker rate;
- feature recomputation pressure;
- simultaneous execution activity.

### Profile C — Market-wide shock
- high event rates across most eligible contracts;
- multiple reconnects/gaps;
- increased news/event traffic;
- active positions requiring priority;
- scanner workload intentionally shed if needed.

### Profile D — Catch-up/reconnect
- WebSocket reconnect;
- snapshot refresh;
- buffered deltas;
- replay/catch-up without mixing stale/current generations.

### Profile E — Replay research
- accelerated historical replay;
- feature reconstruction;
- deterministic equivalence checks;
- concurrent analytical queries.

### Profile F — Failure injection
- broker unavailable;
- time-series store unavailable;
- consumer stalls;
- network latency/jitter;
- duplicate/reordered messages;
- clock drift;
- memory pressure;
- CPU saturation.

## Measurements
For each pipeline stage record:
- p50 latency;
- p95 latency;
- p99 latency;
- p99.9 latency;
- maximum observed latency;
- events/sec;
- bytes/sec;
- CPU utilization;
- memory/GC behavior where relevant;
- queue depth;
- drop/retry count;
- duplicate count;
- recovery time;
- reconnect/resubscribe time;
- replay throughput;
- replay fidelity;
- persistence lag;
- storage growth;
- operational failure rate.

## HCT decision-oriented metrics
Traditional throughput metrics are insufficient. Also measure:

### Data-to-Feature Latency
Exchange receipt to feature readiness.

### Data-to-Decision Latency
Exchange receipt to strategy/supervisor candidate readiness.

### Decision-to-Intent Latency
Approved candidate to canonical Order Intent.

### Signal Lifetime Consumed
Percentage of estimated signal useful life consumed before execution begins.

### Market-State Coherency Rate
Percentage of decisions computed from one proven coherent market-state generation.

### Stale Decision Rejection Rate
How often the freshness system correctly prevents execution of expired evidence.

### Recovery-to-Trusted-State Time
Failure/reconnect to restored `TRUSTED` market state.

### Replay Equivalence Rate
Percentage of replayed canonical states/features matching expected live semantics.

## Benchmark acceptance philosophy
The architecture should favor:
1. correctness and recoverability;
2. predictable tail latency;
3. data freshness/coherency;
4. safety-path isolation;
5. sufficient throughput headroom;
6. observability/debuggability;
7. operational simplicity;
8. cost efficiency.

Raw average latency is not the primary criterion.

## Candidate architecture experiments

### Experiment 1 — NATS-centric
`Exchange Edge -> Core NATS hot fanout -> selected JetStream durable streams -> processors -> QuestDB/ClickHouse`

Hypothesis: strong simplicity/latency for V1 with selective durability.

### Experiment 2 — Redpanda durable backbone
`Exchange Edge -> Redpanda -> hot consumers -> market-state fabric -> QuestDB/ClickHouse`

Hypothesis: strong durability/replay/fanout while maintaining acceptable realtime latency.

### Experiment 3 — Split hot/durable path
`Exchange Edge -> direct/Core NATS/Aeron hot path -> decision fabric`

plus

`Exchange Edge -> Redpanda durable async path -> research/replay`

Hypothesis: best separation between trading latency and durable analytical workloads at the cost of higher architectural complexity.

### Experiment 4 — Streaming materialization
Add RisingWave for selected continuously updated cross-symbol/market-state views.

Hypothesis: simplify complex realtime joins/windows; reject if added latency/operations outweigh benefit.

## Benchmark invariants
All experiments must use:
- same canonical event schema;
- same captured input datasets;
- same hardware class;
- same failure scenarios;
- same feature workload;
- same observation tooling;
- version-pinned dependencies;
- reproducible scripts.

## Promotion rule
No candidate is selected from benchmark performance alone. A production decision requires:
- performance evidence;
- correctness evidence;
- failure/recovery evidence;
- security review;
- operational complexity assessment;
- cost estimate;
- rollback/migration plan;
- compatibility with HCT frontend/backend deployment model;
- explicit ADR/Decision Ledger promotion.
