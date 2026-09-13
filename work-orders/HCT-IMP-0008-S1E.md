# HCT-IMP-0008-S1E — Market Truth Foundation

Status: `PENDING_SEPARATE_AUTHORIZATION_CHECKPOINT`
Risk: `HIGH_ASSURANCE`
Prerequisite: a future checkpoint explicitly authorizing only this Work Order under `NON_TRADING_STAGE_1_MARKET_TRUTH_FOUNDATION_ONLY`.
Canonical preparation base: `main@a92f1093b36b746ff77daa6d28f1ec4cf12f4fcb`
Authorization candidate: `HCT-IMPL-AUTH-0008 / Issue #64`

## OBJECTIVE

Implement, only after a separately promoted authorization checkpoint, a provider-neutral Market Truth Foundation for the next frozen R11 Stage-1 dependency. S1E provides deterministic contracts and trust barriers for normalized public market events, Data Quality/Freshness, generation-scoped coherent Market-State and cache/hot-state projections.

S1E does not create a realtime transport or market-data network runtime. It owns bounded truth contracts and deterministic state predicates required before later transport/ingest work.

## CONTEXT

The frozen R11 Stage-1 dependency order is:

`Exchange Abstraction + MEXC adapter -> capability/rule resolver -> universe -> quota/WS governor -> market ingest/quality/Market-State/cache`.

Completed prerequisites are S1A Exchange Abstraction, S1B MEXC public reference, S1C Market Universe and S1D Quota/WS/Backpressure Governor. Module 29 supplies resource/admission control; it does not own market prices, data quality or coherent market truth.

S1E is a vertical foundation across Modules 4, 7, 5 and 30 with a narrow Module 29 integration seam. It must remain provider-neutral, deterministic, fixture/replay-testable and fail closed under unknown or contradictory evidence.

## SCOPE

### Module 4 — normalized public event envelope

Define immutable normalized public event envelopes with typed event identity, canonical contract/channel identity, source/provenance, schema/version, environment namespace, generation binding and deterministic content fingerprint. Preserve distinct `event_time`, `wall_receive_time` and monotonic elapsed-time evidence.

Add an immutable provider-neutral Channel Capability / Sequence Policy contract binding venue/exchange identity, public/private class, channel/topic identity, symbol/contract scope, schema/version, snapshot availability, delta/update semantics, ordering evidence, sequence/update identifiers where available, update cadence/heartbeat evidence where applicable and continuity policy. Its finite modes are `STRICT_SEQUENCE`, `MONOTONIC_UPDATE_ID`, `TIMESTAMP_ORDERED_WITH_LIMITS`, `SNAPSHOT_ONLY` and `NO_PROVABLE_SEQUENCE`. Concrete MEXC transport, subscription and reconnect I/O remain out of scope.

### Module 7 — Data Quality/Freshness

Define finite quality/freshness predicates and reason codes for fresh/valid, stale/expired, gap, duplicate, out-of-order, `SEQUENCE_UNPROVABLE`, clock unhealthy/drift/jump/untrusted, malformed/schema-quarantined, missing provenance/generation and cross-channel contradiction evidence. A score may explain evidence but cannot hide a failed critical predicate.

Module 7 must emit exactly the typed data-authority states `ALLOW_NEW_EXPOSURE`, `DEGRADED_NEW_EXPOSURE`, `NO_NEW_EXPOSURE`, `REDUCE_ONLY`, `RECONCILIATION_ONLY` and `EMERGENCY`. Hard predicates map deterministically to the finite result; aggregate scores are explanatory only. The result is restrictive-only input to the R11 authority lattice and cannot authorize trading, bypass Risk/Safety/Session/Exchange restrictions or create live authority.

### Module 5 — coherent Market-State

Define generation-scoped snapshots/fabric contracts, synchronization barriers, provenance and trust states. Mixed-generation, stale, gapped, contradictory or unsynchronized evidence cannot silently become trusted coherent state. Retired generations cannot mutate current trusted state.

### Module 30 — cache/hot-state projection

Define immutable projection envelopes with source/generation/provenance/fingerprint references, freshness lease/TTL/invalidation semantics and explicit stale/expired/unknown states. Cache is never a canonical owner and never upgrades authority.

### Module 29 — resource-control integration

Define a typed seam showing quota/backpressure admission, denial, deferral, shedding or resource degradation constrains work but cannot synthesize market events, mark data fresh, promote untrusted state or override quality/trust barriers.

### S1C universe/lifecycle seam

Consume typed immutable S1C `UniverseSnapshot` / `UniverseEligibilityState` evidence owned by ADR-0047, including snapshot identity/fingerprint, contract reference, universe generation, state/reason and source/policy versions. S1E is not a second universe owner. `INELIGIBLE`, `UNKNOWN`, retired or otherwise lifecycle-invalid evidence must deterministically invalidate, retire or degrade the affected Market-State/cache projection and prevent it from presenting as current trusted state.

### Test/evidence foundation

Provide deterministic fixtures/replay inputs, contract tests, state-transition tests and static negative-capability scanning for this scope. CI must not require live MEXC, external network calls or production infrastructure.

## OUT OF SCOPE

- WebSocket/socket/network client creation, venue subscription, reconnect or resubscribe I/O;
- MEXC endpoint/host/path expansion or provider-native DTO truth leakage;
- public/private transport runtime or live market-data ingestion;
- credentials, authentication, signing, private/account/order/position/balance streams;
- order placement/cancel/replace, leverage/margin mutation, Risk, Safety, Session Policy, OMS or Execution authority;
- persistence/database/RLS schema, durable event store or HA/fencing deployment topology;
- Market Scanner, strategies, Brain, agents, signals or trading authority;
- production deployment, limited-live, real-money trading or checkpoint promotion;
- any later Stage-1/Stage-2 implementation slice.

## FILES/SOURCES TO READ

- `checkpoints/workstreams/planning/latest.json`;
- `checkpoints/history/HCT-CP-0028.json`;
- `docs/00-source-hierarchy.md`;
- `docs/03-scope.md`;
- `docs/04-architecture.md`;
- `docs/06-test-benchmark-plan.md`;
- `docs/09-definition-of-done.md`;
- `docs/11-checkpoint.md`;
- `docs/14-product-module-map.md`, Modules 4, 5, 7, 29 and 30;
- `docs/53-r05-acceptance-criteria-and-review-gates.md`;
- `docs/54-r05-realtime-requirements-addendum.md`;
- `docs/91-r11-integrated-authority-state-dependency-architecture.md`;
- `docs/92-r11-v1-module-classification-and-integration-hardening.md`;
- `docs/93-r11-integration-requirements-addendum.md`;
- `docs/99-r12-frozen-requirements-baseline.md`;
- `docs/100-r12-requirements-traceability-and-no-loss-proof.md`;
- `docs/104-chat-delivery-and-prompt-artifact-policy.md`;
- `docs/10-decisions-ledger.md`, especially HCT-DEC-0005, HCT-DEC-0012, HCT-DEC-0132, HCT-DEC-0135, HCT-DEC-0136, HCT-DEC-0138 and HCT-DEC-0139;
- `docs/126-s1d-implementation-approval-and-checkpoint-promotion.md`;
- `adr/HCT-ADR-0047-s1c-market-universe-registry.md`;
- `adr/HCT-ADR-0048-s1d-quota-backpressure-governor.md`;
- `work-orders/HCT-IMPL-AUTH-0008.md`.

## REQUIREMENTS

### Event identity and provenance

- Event identity is immutable, typed and canonical; mutable display labels cannot substitute for identity.
- Environment namespace is explicit and separates `LIVE`, `PAPER`, `SHADOW` and `REPLAY`.
- Every event binds source, channel, contract, schema/version, generation and provenance evidence.
- Equal normalized material produces deterministic equal fingerprints; material identity/provenance/version/time changes alter the fingerprint.
- `event_time`, `wall_receive_time` and monotonic elapsed-time evidence remain separate; wall time alone cannot drive elapsed safety decisions.
- Missing, malformed, contradictory or unknown identity/provenance/time evidence is rejected or explicitly untrusted.

### Channel Capability / Sequence Policy

- The capability contract is immutable, provider-neutral and fingerprinted from venue/exchange identity, public/private class, channel/topic, symbol/contract scope, schema/version, snapshot availability, delta/update semantics, ordering evidence, sequence/update identifiers, cadence/heartbeat evidence and continuity policy.
- `STRICT_SEQUENCE` requires contiguous identifiers; `MONOTONIC_UPDATE_ID` requires increasing identifiers and only treats jumps as gaps when contiguity is proven; `TIMESTAMP_ORDERED_WITH_LIMITS` bounds timestamp order but cannot infer missing updates; `SNAPSHOT_ONLY` treats each valid snapshot as a synchronization point; `NO_PROVABLE_SEQUENCE` yields `SEQUENCE_UNPROVABLE` for continuity-dependent decisions.
- Each mode defines deterministic duplicate, late/out-of-order, gap and resynchronization predicates. Unsupported proof is `SEQUENCE_UNPROVABLE`, never inferred certainty.
- Equal normalized capability material has equal fingerprints, while policy/version changes are fingerprint-visible.

### Data Quality and Freshness predicates

- Quality state is finite, machine-readable and separately inspectable.
- The taxonomy includes stale/expired, gap, duplicate, out-of-order, `SEQUENCE_UNPROVABLE`, clock-health failure, schema quarantine and cross-channel contradiction.
- Unknown/unproven freshness, continuity, clock health, schema or coherence fails closed.
- Aggregate scores are explanatory only and cannot convert a failed critical predicate into a trusted/allowing state.
- Quality outputs declare affected action classes, fallback/degradation and recovery/resynchronization expectations.
- The exact canonical data-authority state set is `ALLOW_NEW_EXPOSURE`, `DEGRADED_NEW_EXPOSURE`, `NO_NEW_EXPOSURE`, `REDUCE_ONLY`, `RECONCILIATION_ONLY` and `EMERGENCY`. A deterministic restrictive precedence selects the result; required-feed untrusted, severe unresolved contradiction, untrusted clock/time-sensitive state, required sequence-unprovable and Module 29 resource starvation cannot yield an allowing state. Module 7 is restrictive-only and cannot itself authorize trading or live authority.

### Market-State trust and synchronization

- Trust states distinguish `UNKNOWN`, `UNTRUSTED`, `RESYNC_REQUIRED`, `DEGRADED` and `TRUSTED`.
- Snapshot/delta reconstructed state requires explicit synchronization proof before `TRUSTED`.
- Mixed-generation, stale, gapped, contradictory, malformed or retired-generation evidence cannot silently enter trusted state.
- Retired generations cannot mutate current trusted state.
- State identity includes generation, provenance, source/version and environment namespace.

### Cache/hot-state projection

- Projections include source, generation, provenance, fingerprint, freshness lease/TTL and invalidation evidence.
- Expired, missing or unknown source evidence is explicit and cannot appear healthy by default.
- Cache cannot originate, replace or upgrade exchange, market, account, order, fill or position authority.
- Invalidation and resynchronization are deterministic and testable.

### Module ownership and integration

- Module 4 owns normalized public event envelopes.
- Module 7 owns quality/freshness predicates and data-authority outputs.
- Module 5 owns coherent Market-State and synchronization barriers.
- Module 30 owns projections and freshness leases only.
- Module 29 owns resource admission/backpressure only and cannot own market truth.
- Consumers cannot become competing truth owners through convenience caching, UI, telemetry or aggregate scoring.
- ADR-0047 remains the sole owner of structural universe/lifecycle truth; S1E consumes typed evidence only.
- ADR-0048 remains the sole owner of quota/backpressure decisions; S1E consumes resource/admission evidence only.

### Frozen source and Decision traceability

The active baseline is `HCT-REQ-BASELINE-V1-CANDIDATE` / `docs/99-r12-frozen-requirements-baseline.md`. Exact R05 locators are computed from `docs/54-r05-realtime-requirements-addendum.md` using `R05::<heading>::B<ordinal>`:

- `R05::Transport and feed requirements::B1`, `B2`, `B3`, `B4`;
- `R05::Backpressure and resource requirements::B1`, `B3`, `B4`;
- `R05::Time and freshness requirements::B1`, `B2`, `B3`;
- `R05::State coherency requirements::B1`, `B2`, `B3`, `B4`;
- `R05::Candle/cache/replay requirements::B3`, `B4`, `B5`;
- `R05::Persistence and schema requirements::B3`, `B4`;
- `R05::Universe lifecycle requirements::B1`, `B2`;
- `R05::Authority requirements::B1`, `B2`, `B3`;
- `R05::Validation requirements::B1`, `B2`, `B3`, `B6`, `B7`, `B8`, `B9`, `B12`, `B13`, `B18`.

Concrete reconnect/resubscription, private/public runtime isolation, downstream Decision Freshness propagation, candle-specific revision logic, persistence outage runtime, reconnect/HA/fencing runtime and other non-S1E validation items are explicitly deferred; their frozen requirements remain authoritative for their later owners.

Decision binding is explicit: `HCT-DEC-0058` applies to generation/sync fencing; `HCT-DEC-0059` applies at the Module 29 seam; `HCT-DEC-0060` applies to time/clock evidence; `HCT-DEC-0061` applies to coherency; `HCT-DEC-0062` applies to schema quarantine/evidence degradation while persistence runtime is deferred; `HCT-DEC-0063` applies directly to the six canonical data-authority states; `HCT-DEC-0064` applies only to S1E age/freshness evidence while downstream propagation is deferred; `HCT-DEC-0065` applies to cache/replay/lifecycle convergence; `HCT-DEC-0066` is explicitly deferred because HA single-writer/fencing is outside S1E. ADR-0047 and ADR-0048 preserve sole-owner boundaries.

## ARCHITECTURE RULES

- Apply the R11 Source-of-Truth Matrix and restrictive authority lattice.
- Preserve one canonical owner for each state family and explicit external reconciliation authority.
- Keep logical modules provider/topology neutral; no production topology is implied.
- Use typed stable IDs and explicit behaviorally material versions/hashes.
- Propagate failure/degradation and recovery proof requirements to consumers.
- Preserve `LIVE/PAPER/SHADOW/REPLAY` identity separation across stateful contracts.
- Preserve tenant/account/environment identity where applicable without introducing tenant or credential runtime in S1E.
- Treat frontend, cache and telemetry as projections, never authority.
- Never relax a stricter quality, trust, safety or reconciliation decision downstream.
- A `UniverseEligibilityState` transition to `INELIGIBLE`, `UNKNOWN`, retired or lifecycle-invalid deterministically invalidates, retires or degrades affected projections; no projection may silently survive as current trusted state.

## CONSTRAINTS

- No implementation may begin before a separate authorization checkpoint promotes this Work Order.
- Tests use deterministic typed time, fixtures and replay inputs; no sleeps and no live MEXC calls.
- No credentials, secrets, private APIs, persistence, deployment or live authority.
- No dependency-lock or frozen-requirement mutation is required or allowed by the bounded implementation.
- Shared contract changes require generation/parity and backward-compatibility evidence.
- All unknown/ambiguous authority fails closed.

## ACCEPTANCE CRITERIA

The S1E implementation is acceptable only if:

1. Event envelopes are immutable, normalized, typed, provenance-bound and deterministically fingerprinted.
2. Event time, wall receive time and monotonic elapsed time are distinct and tested.
3. All required Data Quality/Freshness predicates and reason codes are explicit and individually tested.
4. Stale, gap, duplicate, out-of-order, `SEQUENCE_UNPROVABLE`, clock and contradiction evidence cannot become trusted by scoring or fallback.
5. Generation rollover and retired-generation suppression prevent stale mutation of trusted state.
6. Snapshot/delta trust requires explicit synchronization proof.
7. Market-State trust states distinguish untrusted/degraded/resync from trusted coherent state.
8. Cache freshness leases/TTL/invalidation and no-authority-upgrade are explicit and tested.
9. Module 29 integration constrains resources without owning or upgrading market truth.
10. Environment namespace and typed identity/versioning are preserved.
11. Every sequence-policy mode has deterministic duplicate, late/out-of-order, gap and resynchronization/`SEQUENCE_UNPROVABLE` behavior, and capability fingerprints expose material policy/version changes.
12. Module 7 emits exactly the six canonical HCT-DEC-0063 data-authority states and cannot grant authority alone.
13. S1C lifecycle evidence is consumed through a typed seam and the required invalidation/degradation transitions are deterministic.
14. Deterministic fixtures/replay prove the foundation without live MEXC/network.
15. Negative-capability scanning rejects network, endpoints, credentials, private APIs, trading/Risk/OMS/Execution, persistence, deployment and live authority.
16. Full prior-stage regressions, coverage, contracts, static analysis, build, audits and exact-head CI pass.
17. No unresolved CRITICAL/HIGH finding remains and fresh independent HIGH_ASSURANCE/HEDS Delta review is `APPROVED`.

## TESTS

At minimum, provide:

- event identity, source/channel/contract identity and fingerprint determinism tests;
- provenance, schema/version and environment/generation binding tests;
- event-time/wall-receive/monotonic separation and clock drift/jump tests;
- stale/expiry, missing/freshness lease and recovery tests;
- duplicate, out-of-order, gap and `SEQUENCE_UNPROVABLE` tests;
- malformed/schema quarantine and cross-channel contradiction tests;
- generation rollover, retired-generation and mixed-generation tests;
- snapshot/delta synchronization and trust-state transition tests;
- cache TTL/lease/invalidation and no-authority-upgrade tests;
- equal normalized Channel Capability fingerprint tests and policy/version-change fingerprint tests;
- one deterministic duplicate, late/out-of-order, gap and resynchronization/`SEQUENCE_UNPROVABLE` test family for every sequence-policy mode;
- canonical data-authority tests for required-feed untrusted, severe unresolved contradiction, untrusted clock/time-sensitive state, required sequence-unprovable and Module 29 resource starvation;
- S1C lifecycle tests for `ELIGIBLE -> INELIGIBLE`, `ELIGIBLE -> UNKNOWN`, snapshot generation/version change, retired source generation and cache invalidation/lease behavior;
- Module 29 admission/resource-starvation integration tests;
- deterministic fixtures/replay tests with no live network;
- `LIVE/PAPER/SHADOW/REPLAY` namespace isolation tests where applicable;
- negative tests for network/provider endpoints, credentials/private APIs, order/trading/Risk/OMS/Execution, persistence, deployment and live authority;
- full S0A/S0B/S0C/S1A/S1B/S1C/S1D regressions;
- contract generation/parity, Ruff lint/format, strict mypy, build and dependency audits;
- frontend regression suite and `git diff --check`.

## DELIVERABLES

- one bounded implementation PR after separate S1E authorization promotion;
- immutable provider-neutral event/quality/state/cache contracts;
- deterministic fixtures/replay and complete test/evidence artifact;
- negative-capability scanner and exact-head pull-request-only CI;
- author-side preflight and fresh independent HIGH_ASSURANCE/HEDS Delta review;
- explicit known limitations and deferred transport/persistence/deployment/live work.

## REVIEW FORMAT

Report: repositorySync, sourceMatch, canonicalMain, checkpoint, implementationHead, changedFiles, eventIdentity, timeSemantics, provenanceFingerprint, dataQualityTaxonomy, marketStateTrust, generationIsolation, cacheNoAuthorityUpgrade, module29Boundary, fixtureReplayProof, contractParity, backendTests, backendCoverage, priorStageRegressions, frontendTests, staticAnalysis, build, audits, boundaryScan, exactHeadRun, exactHeadJob, exactHeadConclusion, criticalRemaining, highRemaining, prOpenUnmerged, implementationAuthorized, productionCredentials, productionDeployment, limitedLive, liveTrading and stopConditionRespected.

## STOP CONDITION

Stop with the S1E implementation PR OPEN and UNMERGED after fresh exact-head implementation CI and author-side preflight. Do not self-approve, merge, promote a checkpoint, open sockets, connect to a venue, ingest live data, add credentials/private APIs, trade, persist state, deploy or activate limited-live/live trading. Independent HIGH_ASSURANCE/HEDS Delta review and separate governance acceptance remain mandatory.
