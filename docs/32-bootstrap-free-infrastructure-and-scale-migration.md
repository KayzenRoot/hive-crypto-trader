# Bootstrap Free Infrastructure & Scale Migration

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R02`
Risk class: `HIGH_ASSURANCE`

## Objective
HCT must launch with an infrastructure cost target of approximately **USD 0/month**, using credible free tiers wherever possible, and tolerate only narrowly justified low-cost exceptions (soft ceiling approximately USD 3–4/month) before the product reaches early commercial traction.

The architecture must preserve a clean migration path to stronger paid infrastructure once usage, reliability requirements or customer count justify it. The initial commercial trigger discussed for reevaluation is approximately **10–12 active paying customers**, but migration may occur earlier if hard operational limits, safety, exchange connectivity, data volume or reliability require it.

## Core principle
Free-first does not mean architecture-first shortcuts that make later migration painful. HCT should separate logical interfaces from providers so infrastructure can evolve without rewriting the trading core.

Provider-specific free-tier constraints are external dependencies and must be monitored rather than hard-coded as eternal assumptions.

## Bootstrap infrastructure target
Candidate initial composition:

### Frontend / edge
- Cloudflare Pages/Workers Free where compatible with runtime requirements and terms.
- Static frontend delivery should prefer free CDN/edge hosting.
- Serverless edge components are appropriate for HTTP/API gateway, lightweight auth/session helpers, webhook endpoints, static delivery and non-persistent workloads.

### Primary application database / auth / storage
- Supabase Free is a candidate for early PostgreSQL, Auth and lightweight object storage needs.
- Current free-tier characteristics observed during discovery include 500 MB database, 1 GB file storage, 5 GB egress, 50,000 MAU and two active free projects; free projects may pause after a week of inactivity.
- Supabase is not automatically the authoritative realtime exchange-state engine merely because it hosts PostgreSQL.

### Hot state / lightweight cache
- Upstash Redis Free is a candidate for low-volume hot state, locks, ephemeral coordination and cache workloads.
- Current free-tier characteristics observed during discovery include 256 MB and 500,000 commands/month.
- High-frequency market ticks must not be blindly pushed through a command-metered free Redis tier because trading market-data volume can exhaust quotas quickly.

### Realtime trading worker
- The persistent exchange WebSocket/trading worker is the hardest component to host entirely on typical serverless free tiers.
- Cloudflare Workers Free currently allows 100,000 requests/day but has tight CPU-per-request limits; suitability for long-lived exchange market-data processing must be proven by prototype/benchmark rather than assumed.
- Render Free is acceptable for development/preview but its own documentation states free services are not intended for production and free services can spin down; therefore it is not a preferred production trading-worker foundation.
- For initial owner-only/pilot stages, the system may support a local or user-controlled always-on worker where operationally acceptable, keeping managed cloud services free.
- If a safe persistent production worker cannot be achieved on a free tier, a narrowly-scoped low-cost compute exception up to the agreed bootstrap ceiling may be preferable to abusing an unsuitable free service.

## Tiered deployment model

### Tier 0 — Development / owner-only validation
Target recurring infrastructure cost: `$0`.

Possible topology:
`Frontend CDN/edge free tier -> Supabase Free -> optional Upstash Free -> local/controlled trading worker -> MEXC`

Goals:
- development;
- paper trading;
- replay;
- owner account testing;
- operational instrumentation;
- proving quota/latency assumptions.

### Tier 1 — Early pilot / first customers
Target recurring infrastructure cost: `$0` where operationally safe; soft emergency ceiling `$3–4/month` for one indispensable persistent component.

Rules:
- free-tier quotas monitored continuously;
- no single free provider may become an unabstracted architectural dependency;
- customer onboarding may be capped by measured capacity;
- service degradation or quota exhaustion must fail safely;
- live-trading reliability wins over preserving a symbolic `$0` target.

### Tier 2 — approximately 10–12 active paying customers or earlier capacity trigger
Perform formal infrastructure migration review.

Possible upgrades:
- paid persistent compute;
- production-grade Postgres plan;
- larger hot cache;
- durable event-stream/replay infrastructure;
- stronger observability;
- backup/restore guarantees;
- HA/redundancy where justified;
- dedicated time-series/analytics storage if benchmark evidence warrants it.

The 10–12-customer figure is a business trigger, not a technical guarantee that free tiers will safely support that many live traders.

### Tier 3 — scale / professional infrastructure
Introduce technologies such as Redpanda, NATS/JetStream, Aeron, QuestDB, ClickHouse, RisingWave or managed equivalents only when benchmarked workload and business economics justify their operational complexity/cost.

## Portability architecture
Define internal interfaces for:
- `PrimaryDatabase`;
- `IdentityProvider`;
- `ObjectStorage`;
- `HotStateStore`;
- `EventBus`;
- `DurableEventLog`;
- `TimeSeriesStore`;
- `AnalyticsStore`;
- `RealtimeWorkerRuntime`;
- `Metrics/Tracing`;
- `SecretStore`.

Business/trading modules depend on these contracts, not directly on provider SDK semantics wherever practical.

## Cost Guardrails
Candidate HCT infrastructure FinOps controls:
- per-provider quota telemetry;
- daily/monthly consumption projections;
- alerts at 50/70/85/95% of free limits;
- hard budget ceilings where providers support them;
- automatic suppression of nonessential workloads before quota exhaustion;
- research/replay jobs lower priority than safety/execution/reconciliation;
- explicit approval before enabling a paid plan above bootstrap ceiling;
- monthly infrastructure cost per active tenant metric.

## Free-tier suitability policy
A free service is acceptable only if:
1. its terms permit the intended workload;
2. sleeping/pausing behavior cannot silently compromise live-trading safety;
3. latency and availability are measured and acceptable;
4. quota exhaustion behavior is understood;
5. security controls meet the workload's sensitivity;
6. backup/recovery semantics are understood;
7. provider portability exists;
8. a safe degradation path exists.

Free pricing alone is never sufficient evidence.

## Migration triggers
Migration review occurs when any threshold is met:
- approximately 10–12 active paying customers;
- sustained 70–80%+ free-tier resource usage;
- quota bursts threaten live operation;
- unacceptable p95/p99 latency;
- service sleep/pause/availability incompatibility;
- storage growth threatens limits;
- backups/retention insufficient;
- realtime worker reliability inadequate;
- multi-tenant isolation requirements exceed free-plan capabilities;
- security/compliance requirement cannot be met;
- observed business revenue makes stronger infrastructure economically rational.

## Data-retention strategy for bootstrap
Raw high-frequency market data can become extremely large. During bootstrap:
- do not store every tick forever by default;
- preserve the data necessary for audit, execution reconstruction and prioritized research;
- downsample/compact lower-value historical streams;
- use bounded retention for heavy raw feeds;
- store durable order/fill/risk/audit evidence at higher priority than general market telemetry;
- enable selective research capture windows for high-fidelity datasets.

This prevents a free 500 MB–1 GB storage tier from being consumed by indiscriminate raw market data.

## Reliability rule
For live trading, `free` must never mean `unsafe`.

If no safe zero-cost hosting option exists for a required always-on trading component, HCT should either:
- run that component in a controlled owner-managed environment during bootstrap; or
- use the smallest justified paid compute instance within the bootstrap budget.

The platform must not hide a known reliability defect simply to preserve zero infrastructure cost.

## Current provider observations — discovery snapshot (2026-09-11)
These values are planning inputs and must be rechecked before implementation because providers can change them:
- **Supabase Free:** $0; 500 MB database, 1 GB storage, 5 GB egress, 50k MAU, two active free projects; inactivity pause behavior applies.
- **Cloudflare Workers Free:** 100k requests/day; 10 ms CPU/request and 128 MB memory according to current limits; useful for edge/lightweight request workloads, not yet proven for the HCT streaming hot path.
- **Upstash Redis Free:** $0; 256 MB and 500k commands/month.
- **Render Free:** useful for prototypes; provider explicitly warns free instances should not be used for production, and free Postgres has expiration constraints.

## Decision rule for advanced realtime stack
The previously researched high-performance technologies remain valid target architecture candidates, but bootstrap implementation uses the **smallest architecture that passes HCT benchmarks and safety requirements**.

Preferred sequence:
`simple/free -> measure -> identify bottleneck -> upgrade one layer -> measure again`.

Do not deploy a six-component streaming stack before real workload evidence requires it.
