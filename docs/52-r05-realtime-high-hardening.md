# HCT-PLAN-0001-R05 — Realtime HIGH Hardening

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R05`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

## Purpose
Resolve the remaining HIGH R05 gaps after the CRITICAL transport/state contracts in `docs/51-r05-realtime-transport-state-resilience-architecture.md`.

## GAP-R05-05 — Cross-channel contradiction handling
Create a `CrossChannelTruthReconciler` that compares ticker/trade/book/candle/REST evidence without assuming temporary disagreement is automatically corruption.

Contradiction classes:
- `EXPECTED_TRANSIENT`;
- `LAGGING_CHANNEL`;
- `MISSING_UPDATE`;
- `STATE_DIVERGENCE`;
- `AUTHORITY_CONFLICT`;
- `UNKNOWN`.

Critical unresolved contradiction lowers authority; no aggregate confidence score may mask it.

## GAP-R05-06 — Subscription budget accounting
`AdaptiveSubscriptionPlanner` maintains deterministic budgets for:
- active sockets;
- channel subscriptions;
- symbols;
- message throughput;
- REST fallback/resync calls;
- reconnect/resubscribe cost;
- CPU/memory cost per subscribed feed.

Subscription decisions are priority-aware and support downgrade plans rather than subscribe-everything behavior.

## GAP-R05-08 — Public/private transport isolation
Private account/order/fill/protection streams are isolated from public market-data burst pressure through separate connections, queues, resource reservations and circuit states where practical.

Private/control capacity may not be borrowed by research/scanner traffic in a way that threatens protection or reconciliation.

## GAP-R05-11 — SLA classes
Define policy-driven freshness classes rather than one global timeout.

Candidate classes:
- `ULTRA_SHORT_TRIGGER`;
- `SHORT_HORIZON_EXECUTION`;
- `ACTIVE_POSITION_MONITORING`;
- `SCANNER`;
- `RESEARCH_REPLAY`.

Each class defines max data age, processing latency, queue age, coherency tolerance and degraded behavior.

## GAP-R05-13 — Candle integrity
Every bar records provenance:
- venue-native vs locally reconstructed;
- source trades/channels;
- open/close interval semantics;
- revision generation;
- late-trade correction policy;
- finalization state.

States:
`OPEN`, `PROVISIONAL_CLOSED`, `FINAL`, `REVISED`, `UNTRUSTED`.

Strategies must declare whether revised/provisional bars are permitted. Replay reproduces the version that was knowable at decision time.

## GAP-R05-15 — Hot-cache truth boundary
Hot caches may store market state/features/session state with explicit freshness leases. They may never become authoritative truth for orders, fills, balances or positions.

Every cache entry exposes:
- generation;
- created/updated time;
- TTL/freshness lease;
- source/provenance;
- invalidation reason;
- stale-read policy.

## GAP-R05-17 — Replay capture completeness
Each captured interval receives a `CaptureCompletenessManifest` containing expected channels, observed continuity, gaps, schema changes, clock health, load shedding, persistence lag and capture finality.

Replay fidelity classes:
- `FULL_FIDELITY`;
- `PARTIAL_FIDELITY`;
- `DEGRADED`;
- `INVALID_FOR_PROMOTION`.

## GAP-R05-19 — Symbol lifecycle
Universe state machine:
`DISCOVERED -> ELIGIBLE -> ACTIVE -> PAUSED/DEGRADED -> DELISTING -> INACTIVE`.

Transitions drive subscription cleanup, cache invalidation, feature retirement, strategy eligibility and open-position safety handling. Stale symbol state cannot survive silently after venue status changes.

## GAP-R05-21 — Microburst admission control
Create bounded burst envelopes per priority class using:
- queue-depth thresholds;
- event coalescing where semantically safe;
- batch limits;
- CPU reservation;
- memory ceilings;
- burst duration thresholds;
- tail-latency alarms.

Coalescing is forbidden where every event is economically/safety relevant.

## GAP-R05-22 — Feature compute budget and cancellation
Every expensive feature/agent task carries:
- candidate/symbol identity;
- deadline;
- expected value tier;
- CPU/memory cost estimate;
- cancellation token;
- freshness dependency.

Expired/evicted opportunities cancel pending work so stale analysis cannot consume scarce realtime capacity.

## GAP-R05-24 — Multi-instance/failover ownership
Future HA operation uses explicit ownership leases for stateful reconstruction/publication.

Rules:
- one active writer per authoritative reconstructed state partition;
- standby instances may observe/prepare but cannot publish competing canonical generations;
- lease expiry/fencing token prevents split brain;
- takeover requires state/replay/resync proof before publishing trusted state.

## GAP-R05-25 — Free-tier survivability
Bootstrap topology must keep the safety-critical hot path on reliable persistent/local compute, not on free services that can pause unpredictably.

Free cloud services may support auth/config/metadata/low-frequency persistence where failure is isolated.

Migration triggers include:
- sustained quota >70–85%;
- p99 latency budget breach;
- evidence durability lag beyond policy;
- customer count near 10–12;
- need for HA/multi-region;
- provider pause/suspension risk;
- security/compliance requirements.

## GAP-R05-26 — Low-distortion observability
Hot-path telemetry uses bounded, asynchronous measurement.

Required metrics:
- p50/p95/p99/p99.9 latency;
- event/byte rate;
- queue depth/age;
- drop/coalesce counts;
- gaps/resyncs;
- reconnect count/circuit state;
- feed freshness;
- coherency failures;
- schema quarantine;
- CPU/memory;
- persistence lag;
- RTTS;
- Data-to-Decision Age.

Telemetry overload must itself be detectable and shed before safety-critical work.

## Additional R05 technologies
1. **Cross-Channel Contradiction Index (CCCI)**.
2. **Subscription Value Density (SVD)** — decision value per subscription/quota/compute cost.
3. **Private Stream Isolation Reserve (PSIR)**.
4. **Freshness SLA Matrix (FSM)**.
5. **Candle Revision Provenance (CRP)**.
6. **Hot-State Lease Certificate (HSLC)**.
7. **Capture Completeness Manifest (CCM)**.
8. **Symbol Lifecycle Convergence Score (SLCS)**.
9. **Microburst Survival Ratio (MSR)**.
10. **Stale Work Waste Ratio (SWWR)**.
11. **State Ownership Fencing Token (SOFT)**.
12. **Bootstrap Reliability Margin (BRM)**.
13. **Observability Distortion Budget (ODB)**.

These are research/operational constructs and require validation before production promotion.

## HIGH gap closure mapping
- GAP-R05-05 resolved: CrossChannelTruthReconciler.
- GAP-R05-06 resolved: deterministic subscription budgets.
- GAP-R05-08 resolved: private/public isolation.
- GAP-R05-11 resolved: freshness SLA matrix.
- GAP-R05-13 resolved: candle provenance/revision contract.
- GAP-R05-15 resolved: hot-cache lease/truth boundaries.
- GAP-R05-17 resolved: capture completeness manifest.
- GAP-R05-19 resolved: symbol lifecycle state machine.
- GAP-R05-21 resolved: microburst admission control.
- GAP-R05-22 resolved: compute budgets/cancellation.
- GAP-R05-24 resolved: ownership lease/fencing.
- GAP-R05-25 resolved: free-tier survivability/migration triggers.
- GAP-R05-26 resolved: bounded observability.

## Result
All 26 R05 gaps now have planning resolutions. Final approval still requires canonical decisions/requirements, acceptance gates and objective final audit.