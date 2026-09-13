# HCT-IMPL-AUTH-0008 — Authorize S1E Market Truth Foundation

Status: `AUTHORIZATION_CANDIDATE`
Risk: `HIGH_ASSURANCE`
Authorization issue: `#64`
Canonical execution base: `main@a92f1093b36b746ff77daa6d28f1ec4cf12f4fcb`
Prerequisite checkpoint: `HCT-CP-0028 / S1D_IMPLEMENTATION_APPROVED_MERGED`
Candidate slice: `HCT-IMP-0008-S1E`
Candidate ceiling: `NON_TRADING_STAGE_1_MARKET_TRUTH_FOUNDATION_ONLY`

## OBJECTIVE

Authorize, but do not implement in this Work Order, the next bounded frozen R11 Stage-1 dependency: a provider-neutral Market Truth Foundation for normalized public market events, Data Quality/Freshness predicates, generation-scoped coherent Market-State contracts and cache/hot-state projections.

The candidate must preserve the one-owner Source-of-Truth Matrix and provide deterministic fail-closed contracts before any separately authorized transport or realtime ingest runtime.

## CONTEXT

The canonical R11 dependency DAG is:

`Exchange Abstraction + MEXC adapter -> capability/rule resolver -> universe -> quota/WS governor -> market ingest/quality/Market-State/cache`.

S1D is complete under CP0028. Module 29 controls request/subscription resources and backpressure but does not own market truth. The next necessary dependency is therefore the bounded contract foundation across Modules 4, 7, 5 and 30, with explicit integration to Module 29.

This authorization candidate is governance-only. Product implementation requires a later separately promoted authorization checkpoint.

## SOURCE LOCK

The implementation candidate shall use the repository source hierarchy and read at minimum:

- `checkpoints/workstreams/planning/latest.json`;
- `checkpoints/history/HCT-CP-0028.json`;
- `docs/00-source-hierarchy.md`;
- `docs/03-scope.md` and `docs/04-architecture.md` (higher-precedence scope and architecture controls);
- `docs/06-test-benchmark-plan.md` (mandatory proof-family and evidence guidance);
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
- `docs/124-implementation-authorization-s1d-candidate.md`;
- `work-orders/HCT-IMPL-AUTH-0007.md`;
- `work-orders/HCT-IMP-0007-S1D.md`;
- `docs/126-s1d-implementation-approval-and-checkpoint-promotion.md`.
- `adr/HCT-ADR-0047-s1c-market-universe-registry.md` (sole S1C universe/lifecycle owner);
- `adr/HCT-ADR-0048-s1d-quota-backpressure-governor.md` (Module 29 resource/admission boundary);
- active frozen baseline `HCT-REQ-BASELINE-V1-CANDIDATE` / `docs/99-r12-frozen-requirements-baseline.md`.

## SCOPE

If separately authorized, S1E may implement only provider-neutral immutable contracts and deterministic state/authority predicates for:

1. Module 4 normalized public event envelopes;
2. Module 7 Data Quality/Freshness evidence and hard predicates;
3. Module 5 generation-scoped coherent Market-State fabric contracts;
4. Module 30 cache/hot-state projections;
5. Module 29 integration contracts that constrain resource/admission state without owning market truth;
6. immutable provider-neutral Channel Capability / Sequence Policy contracts for public market channels;
7. a typed seam consuming S1C `UniverseSnapshot` / `UniverseEligibilityState` lifecycle evidence without becoming a second universe owner;
8. deterministic fixtures, replay inputs, tests, evidence and static negative-capability scanning for this scope.

The future implementation may use in-memory/pure state for the foundation, but it must not require live MEXC, external network calls or production infrastructure in CI.

## OUT OF SCOPE

The following are blocking violations of this Work Order:

- concrete WebSocket/socket/network client creation, venue subscription, reconnect or resubscribe I/O;
- MEXC endpoint/host/path expansion, provider-native DTO parsing as canonical truth or private stream integration;
- credentials, authentication, signing, private/account/order/position/balance streams;
- order placement/cancel/replace, leverage/margin mutation, Risk, Safety, Session Policy, OMS or Execution authority;
- persistence/database/RLS schema, durable event store or HA/fencing deployment topology;
- market scanner ranking, strategy, Brain, agent, signal or trading authority;
- production deployment, limited-live, real-money trading or checkpoint promotion;
- any later Stage-1 or Stage-2 capability.

## REQUIREMENTS

### Frozen traceability

The implementation must trace to the frozen R05/R11 requirements and retain the applicable restrictions from the R12 baseline. R05 locators below are exact `R05::<heading>::B<ordinal>` positions computed from the frozen `docs/54-r05-realtime-requirements-addendum.md` blob; no topic-only locator is sufficient:

- `R05::Transport and feed requirements::B1`;
- `R05::Transport and feed requirements::B2`;
- `R05::Transport and feed requirements::B3`;
- `R05::Transport and feed requirements::B4`;
- `R05::Backpressure and resource requirements::B1`;
- `R05::Backpressure and resource requirements::B3`;
- `R05::Backpressure and resource requirements::B4`;
- `R05::Time and freshness requirements::B1`;
- `R05::Time and freshness requirements::B2`;
- `R05::Time and freshness requirements::B3`;
- `R05::State coherency requirements::B1`;
- `R05::State coherency requirements::B2`;
- `R05::State coherency requirements::B3`;
- `R05::State coherency requirements::B4`;
- `R05::Candle/cache/replay requirements::B3`;
- `R05::Candle/cache/replay requirements::B4`;
- `R05::Candle/cache/replay requirements::B5`;
- `R05::Persistence and schema requirements::B3`;
- `R05::Persistence and schema requirements::B4`;
- `R05::Universe lifecycle requirements::B1`;
- `R05::Universe lifecycle requirements::B2`;
- `R05::Authority requirements::B1`;
- `R05::Authority requirements::B2`;
- `R05::Authority requirements::B3`;
- `R05::Validation requirements::B1`;
- `R05::Validation requirements::B2`;
- `R05::Validation requirements::B3`;
- `R05::Validation requirements::B6`;
- `R05::Validation requirements::B7`;
- `R05::Validation requirements::B8`;
- `R05::Validation requirements::B9`;
- `R05::Validation requirements::B12`;
- `R05::Validation requirements::B13`;
- `R05::Validation requirements::B18`.

The following R05 requirements are intentionally deferred because their concrete runtime owners are outside S1E: `R05::Transport and feed requirements::B5`, `R05::Transport and feed requirements::B6`, `R05::Time and freshness requirements::B4`, `R05::Time and freshness requirements::B5`, `R05::Time and freshness requirements::B6`, `R05::Candle/cache/replay requirements::B1`, `R05::Candle/cache/replay requirements::B2`, `R05::Persistence and schema requirements::B1`, `R05::Persistence and schema requirements::B2`, `R05::Validation requirements::B4`, `R05::Validation requirements::B5`, `R05::Validation requirements::B10`, `R05::Validation requirements::B11`, `R05::Validation requirements::B14`, `R05::Validation requirements::B15`, `R05::Validation requirements::B16`, `R05::Validation requirements::B17`, `R05::HA and bootstrap requirements::B1`, `R05::HA and bootstrap requirements::B2`, `R05::HA and bootstrap requirements::B3` and `R05::HA and bootstrap requirements::B4`. Deferral does not weaken the frozen source.

The active baseline is explicitly `HCT-REQ-BASELINE-V1-CANDIDATE` / `docs/99-r12-frozen-requirements-baseline.md`. At minimum the candidate retains:

- R05 transport/generation and snapshot/delta proof requirements;
- R05 sequence/gap/duplicate/out-of-order and `SEQUENCE_UNPROVABLE` requirements;
- R05 time/freshness, clock-health, coherency and cache/replay requirements;
- R05 authority, schema quarantine and validation requirements;
- `R11-REQ-006` one Source-of-Truth owner and projections-only cache/UI/telemetry;
- `R11-REQ-007` distinct quota, ingest, quality, Market-State and cache ownership;
- `R11-REQ-011` environment namespace isolation;
- `R11-REQ-012` typed stable identity/version/hash;
- `R11-REQ-013` failure/degradation propagation and recovery proof;
- `R11-REQ-014` staged dependency DAG;
- `R11-REQ-018` audit/telemetry references domain truth without competing authority;
- `R11-REQ-020` explicit optional-evidence degradation;
- `R11-REQ-024` provider/topology neutrality;
- `HCT-DEC-0005`, `HCT-DEC-0012`, `HCT-DEC-0132`, `HCT-DEC-0135`, `HCT-DEC-0136`, `HCT-DEC-0138` and `HCT-DEC-0139`.

### Decision and ADR applicability matrix

- `HCT-DEC-0058`: applies; generation identity, synchronization proof and retired-generation fencing are S1E trust barriers.
- `HCT-DEC-0059`: applies at the Module 29 seam; bounded priority/admission/resource-starvation evidence may constrain S1E work, but S1E does not reimplement the governor.
- `HCT-DEC-0060`: applies; event time, wall receive time, monotonic age and clock health remain distinct and fail closed.
- `HCT-DEC-0061`: applies; generation, provenance, freshness and coherency are explicit Market-State prerequisites.
- `HCT-DEC-0062`: applies to schema quarantine and explicit evidence degradation; durable persistence-failure runtime remains deferred and no persistence is added in S1E.
- `HCT-DEC-0063`: applies directly; Module 7 emits exactly the canonical data-authority states defined below, as restrictive-only input to the R11 lattice.
- `HCT-DEC-0064`: applies only to S1E age/freshness evidence; downstream feature/Brain/Risk/Execution propagation is deferred to those owners and is not implemented here.
- `HCT-DEC-0065`: applies to cache freshness/invalidation, replay evidence and lifecycle convergence; concrete subscription and strategy/position handling remain deferred.
- `HCT-DEC-0066`: explicitly deferred; future HA single-writer/fencing is outside S1E and no HA runtime is authorized.
- `ADR-0047`: S1C remains the sole `UniverseSnapshot` / `UniverseEligibilityState` owner; S1E consumes typed lifecycle evidence only.
- `ADR-0048`: Module 29 remains the sole quota/backpressure owner; S1E consumes admission/resource evidence only.

### Channel Capability / Sequence Policy contract

S1E shall define an immutable provider-neutral capability record binding venue/exchange identity, public/private class, channel/topic identity, symbol/contract scope, schema/version, snapshot availability, delta/update semantics, ordering evidence, sequence/update identifiers where available, update cadence/heartbeat evidence where applicable and a deterministic capability fingerprint. The record includes one finite mode:

- `STRICT_SEQUENCE`: contiguous sequence is required; a duplicate is the same normalized identity, a lower/late identifier is out-of-order, a jump is a gap, and either gap or contradictory evidence requires resynchronization;
- `MONOTONIC_UPDATE_ID`: identifiers must increase; equal identical material is duplicate, lower identifiers are late/out-of-order, and a jump is a gap only when the capability proves contiguity; otherwise continuity is `SEQUENCE_UNPROVABLE` and resynchronization is required;
- `TIMESTAMP_ORDERED_WITH_LIMITS`: timestamps must be nondecreasing within explicit skew/watermark limits; timestamp order cannot prove missing updates, so unsupported gap proof is `SEQUENCE_UNPROVABLE` and requires resynchronization;
- `SNAPSHOT_ONLY`: each valid snapshot is a synchronization point; no delta continuity is inferred between snapshots, and stale/retired/contradictory snapshots require resynchronization;
- `NO_PROVABLE_SEQUENCE`: all continuity-dependent trust decisions are `SEQUENCE_UNPROVABLE`, never inferred from arrival order.

For every mode, duplicate, late/out-of-order, gap and resynchronization predicates are typed and deterministic. Equal normalized capability material has equal fingerprints; any material policy/version change changes the fingerprint. Concrete MEXC transport, subscriptions and reconnect I/O remain out of scope.

### Event identity, time and provenance

Define immutable normalized public event envelopes with:

- typed event identity and canonical source/channel/contract identity;
- tenant/account/environment namespace where applicable, with `LIVE/PAPER/SHADOW/REPLAY` separation;
- current/retired generation identity and provenance binding;
- explicit `event_time`, `wall_receive_time` and monotonic elapsed-time evidence as distinct fields;
- source, schema/version, normalization and policy fingerprints;
- deterministic equality/fingerprint behavior for equal normalized material and changed fingerprints for material changes;
- unknown/malformed identity, provenance, version or time evidence rejected or marked untrusted rather than guessed.

### Data Quality and Freshness authority

Define a finite reason/state taxonomy covering at minimum:

- fresh/valid;
- stale/expired;
- gap/continuity failure;
- duplicate;
- out-of-order;
- `SEQUENCE_UNPROVABLE`;
- clock unhealthy/drift/jump/untrusted;
- malformed/schema-quarantined;
- cross-channel contradiction;
- missing/unknown provenance or generation;
- persistence/evidence degradation where applicable.

Quality predicates must be deterministic and individually inspectable. An aggregate score may explain evidence but cannot hide a failed critical predicate. Unknown or unproven continuity/freshness/coherency must fail closed.

Module 7 emits exactly this finite typed `DataAuthorityState` set: `ALLOW_NEW_EXPOSURE`, `DEGRADED_NEW_EXPOSURE`, `NO_NEW_EXPOSURE`, `REDUCE_ONLY`, `RECONCILIATION_ONLY` and `EMERGENCY`. Hard predicates map deterministically using a documented restrictive precedence; failed required-feed trust, stale/expired data, sequence unprovability where required, severe contradiction, untrusted time/clock or Module 29 resource starvation cannot produce an allowing state. Aggregate scores remain explanatory only. This result is one restrictive input to the R11 authority lattice and cannot itself authorize trading, bypass Risk/Safety/Session/Exchange restrictions or create live authority.

### Market-State trust and synchronization

Define generation-scoped coherent Market-State snapshot/fabric contracts with explicit states equivalent to:

- `UNKNOWN`;
- `UNTRUSTED`;
- `RESYNC_REQUIRED`;
- `DEGRADED`;
- `TRUSTED`.

The contracts must prove:

- retired generations cannot mutate trusted current state;
- mixed-generation input cannot silently become trusted coherent state;
- snapshot/delta reconstruction requires explicit synchronization proof when applicable;
- unresolved gap, contradiction, stale, clock or schema evidence lowers trust or requires resynchronization;
- trust state is separate from receipt, cache presence, UI rendering or consumer convenience.

### Cache and hot-state projection

Define immutable projection contracts with:

- source/generation/provenance/fingerprint references;
- freshness lease, TTL and invalidation semantics;
- explicit stale/expired/unknown state;
- no-authority-upgrade invariant;
- no canonical ownership of market, account, order, fill or position truth;
- deterministic behavior under missing, retired or contradictory source evidence.

### Module 29 integration

Define typed integration boundaries showing that quota/backpressure admission and resource starvation can deny, defer, shed or degrade work, but cannot:

- synthesize market events;
- mark data fresh or coherent;
- promote untrusted state to trusted;
- override Module 7 quality or Module 5 trust barriers;
- become a second market-truth owner.

### S1C universe/lifecycle seam

S1E shall consume a typed immutable lifecycle evidence reference containing the canonical S1C `UniverseSnapshot` identity/fingerprint, contract reference, universe generation, `UniverseEligibilityState`, reason code and source/policy versions. `ELIGIBLE` is not trading authority. `INELIGIBLE`, `UNKNOWN`, retired or lifecycle-invalid evidence deterministically invalidates, retires or degrades the affected Market-State/cache projection, prevents it from presenting as current trusted state and requires recovery/resynchronization. S1E does not create, recompute or persist universe membership.

## ARCHITECTURE RULES

- One canonical owner per state family; all caches/UI/telemetry are projections.
- Module 4 owns normalized inbound public event envelopes, not quality trust.
- Module 7 owns quality/freshness predicates and data-authority outputs, not coherent state storage.
- Module 5 owns generation-scoped coherent Market-State and synchronization barriers, not raw transport or cache truth.
- Module 30 owns low-latency projections and freshness leases, never authority upgrade.
- Module 29 owns resource control only.
- ADR-0047 owns the structural universe/lifecycle state; S1E consumes lifecycle evidence and never becomes a competing universe owner.
- ADR-0048 owns quota/backpressure decisions; S1E cannot synthesize resource admission or relax a quality/trust barrier.
- Provider/topology neutrality is mandatory; logical modules do not prescribe production deployment.
- All material behavior uses typed identity, version and deterministic fingerprints.
- Failure and degradation state is explicit and propagates to consumers.
- No later layer may relax a stricter authority result.

## CONSTRAINTS

- This Work Order is not implementation authorization until a separate checkpoint explicitly promotes it.
- CI must use deterministic fixtures/replay inputs and make no live external calls.
- No sleep-dependent timing proof; supply typed deterministic time evidence.
- No new dependency lock changes or infrastructure files.
- No credentials, secrets or private endpoints.
- No checkpoint, frozen requirement, architecture semantic or Decisions Ledger mutation is part of a future implementation PR unless separately governed.
- All higher-risk flags remain false.

## ACCEPTANCE CRITERIA

The future implementation may be accepted only when:

- event identity/provenance/time/version/fingerprint semantics are immutable, typed and deterministic;
- all required Data Quality/Freshness states and reasons are explicit and fail closed;
- stale, gap, duplicate, out-of-order, `SEQUENCE_UNPROVABLE`, clock and contradiction predicates are individually tested;
- mixed-generation or unsynchronized state cannot become trusted;
- retired generations cannot mutate trusted current state;
- cache leases/TTL/invalidation are explicit and cache cannot originate or upgrade authority;
- Module 29 resource control is integrated without market-truth ownership overlap;
- Channel Capability/Sequence Policy modes are immutable, provider-neutral, fingerprinted and fail closed to `SEQUENCE_UNPROVABLE`/resynchronization;
- Module 7 emits exactly the six canonical HCT-DEC-0063 data-authority states and remains restrictive-only;
- S1C lifecycle evidence is referenced through a typed seam and invalidation is deterministic for `ELIGIBLE -> INELIGIBLE`, `ELIGIBLE -> UNKNOWN`, generation/version change and retired source generation;
- environment namespace separation is preserved;
- deterministic fixtures/replay are sufficient for CI without live MEXC;
- negative-capability scanner rejects credentials/private/order/Risk/OMS/Execution/persistence/deploy/live surfaces;
- all required tests, static analysis, build, audit and exact-head CI pass;
- no CRITICAL/HIGH finding remains and a fresh independent HIGH_ASSURANCE/HEDS Delta review returns `APPROVED`.

## TESTS AND EVIDENCE

The future implementation Work Order must provide at minimum:

- event identity/version/provenance and fingerprint determinism tests;
- event-time/wall-receive/monotonic-time separation and clock-health tests;
- equal normalized Channel Capability material has equal fingerprints and policy/version changes are fingerprint-visible;
- every sequence-policy mode has deterministic duplicate, late/out-of-order, gap and resynchronization/`SEQUENCE_UNPROVABLE` tests;
- stale/expiry, gap, duplicate, out-of-order and `SEQUENCE_UNPROVABLE` tests;
- schema/malformed/quarantine and cross-channel contradiction tests;
- generation rollover, retired-generation rejection and mixed-generation tests;
- snapshot/delta synchronization proof and trust-state transition tests;
- cache freshness lease/TTL/invalidation/no-authority-upgrade tests;
- Module 29 resource-starvation/admission integration tests;
- canonical data-authority tests for required-feed untrusted, severe contradiction, untrusted clock/time-sensitive state, required sequence-unprovable and Module 29 resource starvation;
- S1C lifecycle tests for `ELIGIBLE -> INELIGIBLE`, `ELIGIBLE -> UNKNOWN`, snapshot generation/version change, retired source generation and cache invalidation/lease behavior;
- LIVE/PAPER/SHADOW/REPLAY namespace isolation tests where applicable;
- deterministic fixture/replay tests without live MEXC/network;
- negative tests for network/provider endpoint, credentials/private APIs, trading/Risk/OMS/Execution, persistence, deployment and live authority;
- full prior-stage regression suite and accepted coverage threshold;
- contract generation/parity where shared schemas change;
- lint, format, strict typecheck, build, dependency audits and `git diff --check`;
- exact-head pull-request-only CI evidence bound to the final implementation head.

The evidence must record exact source/base/checkpoint identity, changed files, requirement locators, test counts/coverage, fixture/replay identity, fingerprints, audit results, boundary scan results, known limitations and all production/live flags false.

## DELIVERABLES

- one bounded S1E implementation PR only after separate authorization promotion;
- provider-neutral implementation and tests within its explicitly allowlisted surface;
- evidence artifact with requirement traceability and deterministic proof;
- negative-capability scanner and exact-head implementation CI;
- author-side preflight followed by fresh independent HIGH_ASSURANCE/HEDS Delta review;
- no merge or checkpoint promotion in this authorization candidate.

## REVIEW FORMAT

The future executor/reviewer handoff must report, at minimum: repositorySync, sourceMatch, canonicalMain, checkpoint, checkpointFailClosed, implementationHead, changedFiles, eventIdentity, timeSemantics, provenanceFingerprint, dataQualityTaxonomy, marketStateTrust, generationIsolation, cacheNoAuthorityUpgrade, module29Boundary, fixtureReplayProof, contractParity, backendTests, backendCoverage, priorStageRegressions, frontendTests, staticAnalysis, build, audits, boundaryScan, exactHeadRun, exactHeadJob, criticalRemaining, highRemaining, prOpenUnmerged, implementationAuthorized, productionCredentials, productionDeployment, limitedLive, liveTrading and stopConditionRespected.

## STOP CONDITION

Stop with the future S1E implementation PR OPEN and UNMERGED after implementation exact-head CI and author-side preflight. Do not self-approve, merge, promote a checkpoint, open sockets, connect to a venue, ingest live market data, add credentials/private APIs, trade, persist state, deploy or activate limited-live/live trading. Fresh independent HIGH_ASSURANCE/HEDS Delta review is mandatory before any later governance acceptance.
