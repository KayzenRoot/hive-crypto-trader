# HCT-IMP-0010-S1F — Realtime Public Market Value Plane & Ingest Foundation

Status: `PENDING_SEPARATE_AUTHORIZATION_CHECKPOINT`
Risk: `HIGH_ASSURANCE`
Prerequisite authorization: `HCT-IMPL-AUTH-0010 / Issue #70`
Canonical preparation base: `main@625dd0c145087038bdbccd665548d811e187194c`
Checkpoint at preparation: `HCT-CP-0030 / S1E_IMPLEMENTATION_APPROVED_MERGED`
Scope name: `Realtime Public Market Value Plane & Ingest Foundation`
Primary owners: `Module 4 — Realtime Market Data`, `Module 5 — Market-State`, `Module 7 — Data Quality`
Downstream consumer: `Module 8 — Indicator & Feature Engine`, read-only and later governed

## OBJECTIVE

Only after a dedicated authorization checkpoint, implement the smallest Stage-1 canonical typed public market-value plane needed for deterministic downstream analytics. The implementation must normalize source-supported public values, preserve point-in-time and generation identity, publish immutable value/state evidence and integrate with existing S1E Market-State/DataAuthority contracts without becoming a second truth owner.

It must close B001 at the contract/runtime boundary while preserving the blocked S2A handoff. It must not implement S2A feature families or any trading authority.

## CONTEXT

S1E currently provides event/state identity, trust, authority, provenance and fingerprints but not typed numeric values. S2A was independently blocked because returns, averages, volatility and rolling features cannot be computed without a canonical value plane. R11 orders Stage 1 before Stage 2 and assigns normalized public market data to Module 4, coherent state to Module 5 and quality to Module 7.

The implementation must use read-only upstream identity and must preserve `MarketStateTrust`, `DataAuthority`, resource, Universe eligibility and lifecycle as separate axes. A restrictive resource or eligibility state must not mutate or falsify trusted public numeric truth; conversely, no downstream consumer may upgrade a restrictive axis.

## SCOPE

### Typed value contracts

- `TradeTick`: positive typed price and nonnegative quantity, optional aggressor/side only if available from the authoritative source, event/knowledge/wall-receive/monotonic times, source/channel/contract/environment/generation/schema/provenance/originating event and value fingerprint;
- `TickerState`: only frozen/source-supported last, close or reference values, each with explicit availability and provenance;
- `CandleBar`: typed timeframe ID/version/epoch, explicit interval start/end/boundary convention, OHLC, sourced volume, complete/closed state, source generation and ordered input lineage;
- mark/index/fair-price and funding evidence only if required by frozen scope and source-supported;
- minimum Stage-1 order-book value contract required by the frozen source set. Full depth and advanced microstructure are deferred unless explicitly authorized by exact requirements.

All value objects are immutable, typed, versioned and content-fingerprinted. Unsupported or absent fields are not synthesized.

### Numeric policy

Use Decimal or fixed-point semantics, never ordinary floating-point equality. Declare precision source, scale limits, quantization and rounding. Canonical serialization must be stable across runtimes and included in fingerprints. Reject malformed numbers, NaN, positive/negative Infinity, nonpositive prices, negative quantities, impossible OHLC, overflow and underflow according to typed policy. Empty, undefined, insufficient-input and divide-by-zero results are `UNKNOWN`, `INVALID` or `WARMUP` with reason codes, never silent zero, platform exception or fabricated `VALID`.

### Lineage and state

Bind each value to source ID, channel, contract, environment, generation, schema/version, provenance, origin event and value fingerprint. Market-State owns coherence; the value plane and downstream feature engine consume or publish read-only evidence according to module ownership. Rolling/multi-timeframe consumers receive an ordered manifest for every input value fingerprint or a deterministic Merkle/content manifest. Insert/delete/reorder/correction/generation/value changes must alter the manifest/fingerprint. Mixed source, contract, environment or generation fails closed unless a separately approved cross-source contract exists.

### Time and interval

Use UTC canonical timestamps with distinct `event_time`, `knowledge_time`, `wall_receive_time` and monotonic age. Inject time in tests; do not use sleeps to define correctness. Declare interval inclusion/exclusion, timeframe ID/version/epoch, close boundary, open/incomplete semantics and late-correction versioning. A correction creates a new value version and never rewrites prior point-in-time history. An open/incomplete candle cannot be used as a closed higher timeframe without an explicit downstream feature rule.

### Ingest boundary

Keep provider-specific transport out of scope if canonical sources do not contain enough official protocol/channel detail. If a frozen Stage-1 requirement objectively requires a public unauthenticated boundary, implement only that minimum, integrate Module 29 quota/backpressure and S1E generation/quality, and keep uncontrolled live network out of CI. No credential, private API, signing or account surface is allowed.

## OUT OF SCOPE

- S2A features/indicators, concrete family selection, patterns, regime, scanner, ranking, strategy, signal and advanced microstructure;
- Brain, agents, RAG, memory, learning, calibration, promotion, Risk, Safety, Session Policy, sizing, leverage, OMS, Execution, reconciliation, protection, orders, balances, positions and fills;
- private/authenticated market or account data, credentials, signing, persistence, database/RLS, feature stores, HA/fencing, deployment and infrastructure topology;
- checkpoint mutation, implementation or live authority not explicitly granted by a later gate; production credentials, production deployment, limited-live and live/real-money trading;
- mutation of S1E ownership, frozen requirement blobs, source hierarchy, dependency locks, CP0030, PR #69 or the S1F governance artifacts.

## FILES/SOURCES TO READ

Before implementation, read canonical `main@625dd0c145087038bdbccd665548d811e187194c`, CP0030 and:

- `docs/00-source-hierarchy.md`, `docs/02-requirements.md`, `docs/03-scope.md`, `docs/04-architecture.md`, `docs/06-test-benchmark-plan.md`, `docs/09-definition-of-done.md`, `docs/10-decisions-ledger.md`, `docs/11-checkpoint.md`, `docs/14-product-module-map.md`;
- `docs/48-r04-execution-requirements-addendum.md`, `docs/54-r05-realtime-requirements-addendum.md`, `docs/61-r06-intelligence-requirements-addendum.md`, `docs/67-r07-validation-laboratory-requirements-addendum.md`, `docs/73-r08-multitenant-security-requirements-addendum.md`, `docs/80-r09-cockpit-uiux-requirements-addendum.md`, `docs/87-r10-observability-audit-incident-finops-requirements-addendum.md`, `docs/93-r11-integration-requirements-addendum.md`;
- `docs/91-r11-integrated-authority-state-dependency-architecture.md`, `docs/92-r11-v1-module-classification-and-integration-hardening.md`, `docs/96-r11-requirements-freeze-input-inventory.md`, `docs/97-r11-final-integration-audit.md`, `docs/99-r12-frozen-requirements-baseline.md`, `docs/100-r12-requirements-traceability-and-no-loss-proof.md`, `docs/101-r12-freeze-governance-change-control-and-deferred-decisions.md`, `docs/102-r12-freeze-acceptance-matrix.md`, `docs/103-r12-final-planning-freeze-audit.md`;
- `docs/131-implementation-authorization-s1f-candidate.md`, `work-orders/HCT-IMPL-AUTH-0010.md`, `adr/HCT-ADR-0049-s1e-market-truth-foundation.md` and current S1E contracts/evidence read-only.

Frozen source identities are the nine requirement hashes in the authorization Work Order; `docs/06-test-benchmark-plan.md` is bound at blob `29401ce8fe1616f9390a317bae62d3a157addaa5`.

## REQUIREMENTS

Trace every contract, behavior, test and evidence item to exact locators. The minimum set is:

- R05 transport/feed, backpressure/resource, time/freshness, state coherency, candle/cache/replay, universe lifecycle, authority and applicable validation bullets;
- `INT-002`, `INT-003`, `INT-004`, `INT-011`, `INT-012`, `INT-018`, `INT-022`, `INT-024`, `INT-025`, `INT-026`;
- `VAL-003`, `VAL-005`, `VAL-006`, `VAL-011`, `VAL-012`, `VAL-013`, `VAL-023`, `VAL-028`, `VAL-030`;
- `R11-REQ-006`, `R11-REQ-007`, `R11-REQ-011`, `R11-REQ-012`, `R11-REQ-013`, `R11-REQ-014`, `R11-REQ-015`, `R11-REQ-020`, `R11-REQ-022`, `R11-REQ-024`, `R11-REQ-025`;
- `HCT-DEC-0007`, `0008`, `0012`, `0058`, `0060`–`0065`, `0068`, `0069`, `0071`, `0074`, `0077`, `0079`, `0083`, `0084`, `0089`, `0135`, `0136`, `0138`, `0139`, `0140`, `0141`; and ADR-0049.

## ARCHITECTURE RULES

1. Module ownership and the R11 dependency DAG are authoritative: public normalized values -> coherent Market-State/quality -> later read-only analytics.
2. S1E trust, DataAuthority, resource state, Universe eligibility and lifecycle remain separate axes. `TRUSTED+RESOURCE_DEGRADED`, `TRUSTED+INELIGIBLE`, `TRUSTED+UNKNOWN`, `STALE`, `GAP`, `SEQUENCE_UNPROVABLE`, `CLOCK_UNTRUSTED` and `RETIRED_GENERATION` are explicit test cases.
3. Source/channel/contract/environment/generation/schema/version/provenance and originating event are immutable identity. `LIVE`, `PAPER`, `SHADOW` and `REPLAY` cannot alias.
4. The coherent-state owner is the only authority for state assembly; value/feature layers cannot rewrite or upgrade it.
5. Time, interval, completeness, correction and ordered lineage are content-bearing and fingerprinted.
6. No missing, contradictory, stale, invalid, mixed or unprovable input can become a normal valid value through defaults, zero-fill or scoring.

## CONSTRAINTS

- implement only after a new authorization checkpoint explicitly grants S1F;
- preserve exact frozen source identities and CP0030 history; no force/reset/rewrite or unrelated cleanup;
- no ordinary float as canonical value identity; no guessed provider protocol;
- tests and benchmark evidence must be deterministic and reproducible; no uncontrolled live network in CI;
- no code path may create implementation, production, deployment, limited-live or live-trading authority implicitly.

## ACCEPTANCE CRITERIA

1. A typed `TradeTick`/`TickerState`/`CandleBar` and source-supported reference-value plane is available to read-only consumers, with explicit absent/unknown fields.
2. Numeric semantics are canonical, finite, invariant-checked and deterministic across supported runtimes.
3. Immutable value fingerprints include canonical numeric fields and all material identity; ordered window lineage detects every material mutation.
4. UTC point-in-time and interval/close/correction semantics are explicit and tested.
5. S1E trust/DataAuthority/resource/eligibility/lifecycle axes are preserved without authority upgrades or truth falsification.
6. Public transport, if objectively required, is unauthenticated/minimal and bound to quota/backpressure/generation/quality; otherwise it is deferred with no invented protocol.
7. Tests cover parsing, numeric failure states, lineage, time, windows, generation fences, quality/trust matrix, replay and negative firewall.
8. Benchmark method binds `docs/06-test-benchmark-plan.md` and reports assumptions, method, normalization throughput, value-state latency, memory, replay and reproducible evidence; transport queue/backpressure only if in scope.
9. Exact traceability and independent HIGH_ASSURANCE review are complete before checkpoint consideration.

## TESTS

Test typed parsing and canonical serialization; Decimal/fixed-point round trip and rounding; NaN/Infinity/malformed/nonpositive/negative/impossible-OHLC/overflow/underflow rejection; empty/divide-by-zero/undefined/warmup typed outcomes; immutable fingerprint and ordered manifest/Merkle mutation detection; mixed identity/generation rejection; interval inclusion, close and incomplete candles; late correction versioning; UTC injected time and no-lookahead; S1E truth-validity matrix; fixture/replay determinism; schema drift, sequence/gap, reconnect, stale, quota/backpressure and public ingest only if that boundary is authorized; and negative-capability scanning for credentials/private/trading/persistence/deployment/live surfaces.

## BENCHMARK AND EVIDENCE

Declare symbols, channels, event rate, candle intervals, depth, fixture sizes and workload assumptions. Run deterministic fixtures with pinned code/build/dependency, configuration/policy, seed, hardware/environment and tool version. Measure normalization throughput, value-state update latency, memory footprint and replay throughput. If public transport is included, measure bounded queue/backpressure without uncontrolled live network CI. Report baseline and regression thresholds or a separately approved no-hard-target rationale, plus hashes and limitations.

## DELIVERABLES

- S1F runtime contracts and implementation only after authorization;
- deterministic tests, fixtures/replay and benchmark evidence;
- source/lineage/time/authority documentation and exact traceability;
- negative-capability result and independent review package;
- no checkpoint or production/live activation as an implicit consequence.

## REVIEW FORMAT

The implementation review must bind the fields in the authorization candidate, including exact base/head, source identities, typed value kinds, numeric policy, ordered lineage, interval semantics, S1E axis matrix, `docs06Bound`, benchmark evidence, governance and authorization firewalls. A green test suite or `COMPLETE_CANDIDATE` is not approval.

## STOP CONDITION

Stop on any source mismatch, changed canonical main, checkpoint flag drift, missing traceability, unsupported provider assumption, authority upgrade, unresolved numeric/lineage/time ambiguity, uncontrolled network, or negative-scope violation. Stop after producing candidate evidence; do not merge, checkpoint, deploy, enable credentials, limited-live or live trading without separate governed approvals.
