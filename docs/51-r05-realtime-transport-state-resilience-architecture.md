# HCT-PLAN-0001-R05 — Realtime Transport & Market-State Resilience Architecture

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R05`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

## Objective
Close the CRITICAL R05 gaps by defining deterministic contracts for realtime transport, feed generations, synchronization, backpressure, load shedding, time integrity, state coherency, schema drift, persistence isolation and data-age propagation.

No implementation or live-trading authorization is granted by this document.

## Core invariant
Realtime data is not trusted merely because a WebSocket is connected or messages are arriving.

A consumer may act only on market state whose transport generation, synchronization state, sequence/gap status, freshness, schema, coherency and authority class satisfy that consumer's policy.

## Canonical transport state machine
Each logical realtime feed maintains an explicit state:

`DISCONNECTED -> CONNECTING -> CONNECTED_UNSYNCED -> SYNCHRONIZING -> TRUSTED`

Alternative/degraded states:
- `DEGRADED`;
- `GAP_DETECTED`;
- `SCHEMA_UNKNOWN`;
- `CLOCK_UNTRUSTED`;
- `RESYNC_REQUIRED`;
- `CIRCUIT_OPEN`;
- `QUARANTINED`.

Only `TRUSTED`, or an explicitly policy-accepted degraded state, may feed exposure-increasing decisions.

## 1. Channel Capability Registry
Every venue/channel/version must publish a runtime capability record containing at least:
- venue and API/version identity;
- public/private classification;
- channel/topic identity;
- symbol scope;
- subscription method;
- snapshot availability;
- delta/update semantics;
- sequence/update identifiers where exposed;
- ordering guarantees if documented;
- update cadence/heartbeat expectations;
- message/schema version;
- maximum supported subscriptions/connections where known;
- REST fallback/resync source;
- authority class;
- current validation status;
- source-document/provenance timestamp.

Provider behavior not explicitly established is `UNKNOWN`, never inferred as guaranteed.

## 2. WebSocket Session Generation
Every physical connection receives a monotonically increasing local `FeedSessionGeneration` scoped by venue/account/channel class.

Example:
`MEXC-PUBLIC-GEN-000104`

Every decoded event carries:
- socket/session generation;
- connection-open monotonic timestamp;
- local receive monotonic timestamp;
- exchange/event timestamp when available;
- channel identity;
- symbol;
- schema version;
- synchronization generation.

Events from a closed/retired generation may be preserved for evidence but cannot mutate the current trusted market state.

## 3. Snapshot + Delta Synchronization Barrier
For stateful feeds reconstructed from snapshots and deltas, use an explicit synchronization barrier:

1. open a new feed generation;
2. mark state `CONNECTED_UNSYNCED`;
3. start bounded buffering of eligible deltas;
4. obtain authoritative snapshot/resync state;
5. validate snapshot timestamp/sequence/generation;
6. discard impossible/duplicate/pre-snapshot deltas according to channel semantics;
7. apply eligible buffered deltas deterministically;
8. validate continuity/invariants;
9. publish a new `MarketStateGeneration` only after barrier success;
10. enter `TRUSTED`.

If continuity cannot be proven, state becomes `RESYNC_REQUIRED`, not approximately trusted.

## 4. Per-Channel Sequence & Gap Policy
No universal sequence algorithm exists.

Each channel capability defines one of:
- `STRICT_SEQUENCE`;
- `MONOTONIC_UPDATE_ID`;
- `TIMESTAMP_ORDERED_WITH_LIMITS`;
- `SNAPSHOT_ONLY`;
- `NO_PROVABLE_SEQUENCE`.

For each mode define:
- duplicate rule;
- late-event rule;
- out-of-order tolerance;
- gap predicate;
- resync predicate;
- confidence impact.

When the provider exposes insufficient ordering evidence, HCT explicitly emits `SEQUENCE_UNPROVABLE` and tightens downstream authority.

## 5. Reconnect Storm Governor
Reconnect behavior is governed per venue/account/channel class.

Controls:
- bounded exponential backoff;
- randomized jitter;
- reconnect-attempt budget per rolling window;
- maximum concurrent reconnects;
- staged resubscription;
- circuit breaker after repeated failures;
- cool-down windows;
- protection/private-stream priority;
- no synchronized thundering-herd resubscription.

Circuit states:
`CLOSED`, `HALF_OPEN`, `OPEN`.

Repeated reconnect success without successful synchronization does not count as healthy recovery.

## 6. Backpressure Classes
Queues are bounded and consumer-class-specific.

Priority classes:
- `P0_EMERGENCY_SAFETY`;
- `P1_PROTECTION_RECONCILIATION`;
- `P2_ACTIVE_POSITION_EXECUTION_STATE`;
- `P3_EXECUTION_CRITICAL_MARKET_STATE`;
- `P4_STRATEGY_CANDIDATE_FEATURES`;
- `P5_SCANNER_BREADTH`;
- `P6_RESEARCH_RAG_ANALYTICS`.

Each class defines:
- max queue depth/age;
- admissible coalescing;
- drop/overwrite prohibition or allowance;
- escalation thresholds;
- CPU/memory budget;
- observability requirements.

A lower-priority queue cannot consume resources reserved for higher-priority classes.

## 7. Deterministic Load Shedding Ladder
When capacity is exceeded, HCT degrades in a fixed observable order rather than randomly losing work.

Candidate ladder:
1. cancel stale research/RAG tasks;
2. reduce nonessential telemetry detail;
3. reduce scanner breadth;
4. reduce noncritical feature richness;
5. reduce public-channel depth/frequency where policy permits;
6. freeze new candidate creation;
7. enter `NO_NEW_EXPOSURE` if minimum trusted inputs cannot be preserved.

Never shed required active-position, protection, reconciliation or emergency state while claiming normal authority.

Every shed decision records reason, start/end time, affected feeds/features and authority impact.

## 8. Time Integrity Contract
HCT distinguishes:
- `exchange_event_time`;
- `wall_receive_time`;
- `monotonic_receive_time`;
- `normalization_time`;
- `feature_ready_time`;
- `decision_time`;
- `risk_approval_time`;
- `execution_command_time`.

Rules:
- elapsed latency is measured from monotonic clocks where possible;
- wall clock is for human/audit chronology, not trusted elapsed-time arithmetic;
- exchange clock offset/drift is monitored separately;
- clock jumps cannot produce negative/false latency;
- clock state is `HEALTHY`, `DEGRADED`, or `UNTRUSTED`;
- `UNTRUSTED` clock state blocks time-sensitive new exposure.

## 9. Market-State Generation & Feature Coherency Barrier
Every trusted reconstructed market state receives a `MarketStateGenerationID`.

Derived feature bundles record the exact generations/timestamps of all inputs.

A feature set is classified:
- `COHERENT`;
- `COHERENT_WITH_TOLERANCE`;
- `MIXED_GENERATION`;
- `STALE_INPUT`;
- `UNTRUSTED`.

Strategy/Brain/Risk policies define acceptable classes by horizon. A low-latency strategy cannot silently combine a fresh book with materially stale trades/candles.

## 10. Persistence Failure Isolation
Durable storage is evidence/replay infrastructure, not a synchronous prerequisite for every hot-path decision.

Hot path rules:
- bounded asynchronous persistence;
- no unbounded blocking on database/event-log outage;
- finite in-memory/local spill buffer where safe;
- explicit `EVIDENCE_DEGRADED` state when persistence falls behind;
- maximum tolerated evidence-loss window by data class;
- trading authority may tighten if required audit/recovery evidence can no longer be guaranteed;
- Safety/Protection/Reconciliation remain prioritized over research persistence.

If required durable evidence for safe recovery can no longer be guaranteed, HCT transitions toward `NO_NEW_EXPOSURE` rather than continuing invisibly.

## 11. Schema Evolution & Quarantine
All critical realtime payloads pass versioned structural/semantic validation.

Unknown/malformed critical payload behavior:
1. preserve raw payload/provenance;
2. mark event `SCHEMA_UNKNOWN` or `SCHEMA_INVALID`;
3. quarantine from canonical state mutation;
4. lower Feed Confidence / State Confidence;
5. trigger reconciliation/resync where relevant;
6. emit operator alert;
7. do not guess/coerce missing critical semantics.

Additive unknown fields may be retained without failure only when known required semantics remain validated.

## 12. Data Quality -> Trading Authority Matrix
Scores such as MSIS/Feed Confidence are explanatory, but authority is deterministic.

Canonical authority states:
- `ALLOW_NEW_EXPOSURE`;
- `DEGRADED_NEW_EXPOSURE`;
- `NO_NEW_EXPOSURE`;
- `REDUCE_ONLY`;
- `RECONCILIATION_ONLY`;
- `EMERGENCY`.

Example hard mappings:
- required feed `UNTRUSTED` => `NO_NEW_EXPOSURE`;
- critical private/reconciliation uncertainty => at least `NO_NEW_EXPOSURE`, potentially `RECONCILIATION_ONLY`;
- missing required protection state => `REDUCE_ONLY`/`PROTECTION_RECOVERY` through upstream safety policy;
- severe multi-feed contradiction + no authoritative resolution => `NO_NEW_EXPOSURE`;
- P0/P1 resource starvation risk => `EMERGENCY` or controlled shutdown of new exposure.

Aggregate scores may not hide a critical failed predicate.

## 13. Data-to-Decision Age Budget Propagation
Every candidate action carries a `DecisionFreshnessEnvelope` containing at least:
- oldest required input receive time;
- newest required input receive time;
- market-state generation;
- feature-ready time;
- Brain decision time;
- Risk approval time;
- current monotonic age;
- strategy signal half-life/expiry;
- consumed latency budget;
- remaining latency budget;
- stale/expired reason codes.

At each stage:
`remaining_budget = approved_signal_lifetime - elapsed_monotonic_age - required_downstream_safety_margin`.

If remaining budget is insufficient for safe execution/revalidation, result becomes `WAIT`, `EXPIRED`, or `NO_NEW_EXPOSURE` rather than forcing an order.

## Cross-cutting proprietary R05 technologies
1. **Feed Generation Firewall (FGF)** — prevents retired socket generations from mutating current state.
2. **Synchronization Proof Token (SPT)** — attests snapshot/delta barrier completion for a market-state generation.
3. **Sequence Provability Index (SPI)** — expresses how strongly a channel's continuity can be proven from provider metadata.
4. **Reconnect Pressure Index (RPI)** — quantifies reconnect/resubscribe instability and circuit pressure.
5. **Priority Preservation Ratio (PPR)** — measures whether P0–P3 latency remains protected during bursts.
6. **Shedding Transparency Ledger (STL)** — immutable record of fidelity intentionally removed under load.
7. **Market-State Coherency Envelope (MSCE)** — exact cross-input generation/age constraints for a feature bundle.
8. **Evidence Durability Lag (EDL)** — distance between hot-path truth and durable replay/audit persistence.
9. **Schema Trust Score (STS)** — version/semantic validation confidence per feed generation.
10. **Decision Freshness Envelope (DFE)** — end-to-end age and remaining signal-lifetime contract.
11. **Authority Degradation Matrix (ADM)** — deterministic mapping from data failures to trading authority.
12. **Recovery-to-Trusted-State Time (RTTS)** — time from detected feed failure until synchronized trusted state returns.
13. **Realtime Survivability Budget (RSB)** — reserved CPU/memory/network capacity for P0–P3 during burst/failure.

All are research/operational constructs and require validation before production claims.

## Validation requirements
R05 implementation planning must later require tests for:
- old-generation late event injection;
- reconnect during buffered synchronization;
- missing/duplicate/out-of-order delta;
- provider channel without provable sequence;
- reconnect storm/thundering herd;
- queue saturation per priority class;
- deterministic load shedding;
- clock jump/drift;
- mixed-generation feature inputs;
- persistence outage and recovery;
- malformed/changed schema;
- data-quality authority transitions;
- end-to-end freshness expiration;
- burst p50/p95/p99/p99.9 latency;
- recovery-to-trusted-state timing.

## Critical gap closure mapping
- GAP-R05-01: resolved by Channel Capability Registry.
- GAP-R05-02: resolved by FeedSessionGeneration/FGF.
- GAP-R05-03: resolved by Snapshot+Delta Synchronization Barrier/SPT.
- GAP-R05-04: resolved by per-channel Sequence Policy/SPI.
- GAP-R05-07: resolved by Reconnect Storm Governor/RPI.
- GAP-R05-09: resolved by Backpressure Classes/PPR.
- GAP-R05-10: resolved by deterministic Load Shedding/STL.
- GAP-R05-12: resolved by Time Integrity Contract.
- GAP-R05-14: resolved by Market-State Generation/MSCE.
- GAP-R05-16: resolved by Persistence Failure Isolation/EDL.
- GAP-R05-18: resolved by Schema Evolution & Quarantine/STS.
- GAP-R05-20: resolved by Authority Degradation Matrix.
- GAP-R05-23: resolved by Decision Freshness Envelope.

## Remaining R05 work
Close HIGH gaps, consolidate decisions/requirements, define objective acceptance gates and run final R05 audit.

## STOP CONDITION
Do not approve R05 until all HIGH gaps are also resolved in planning and final acceptance gates pass. Implementation/live trading remain unauthorized.