# HCT-IMPL-AUTH-0010 — Stage-1 Prerequisite Authorization Candidate

Status: `PENDING_INDEPENDENT_HIGH_ASSURANCE_REVIEW`
Risk: `HIGH_ASSURANCE`
Canonical base: `main@625dd0c145087038bdbccd665548d811e187194c`
Current checkpoint: `HCT-CP-0030 / S1E_IMPLEMENTATION_APPROVED_MERGED`
Authorization issue: `#70`
Proposed implementation: `HCT-IMP-0010-S1F`
Governance branch: `governance/HCT-IMPL-AUTH-0010-S1F`
Scope name: `Realtime Public Market Value Plane & Ingest Foundation`
Dependency handoff: `HCT-IMPL-AUTH-0009 / HCT-IMP-0009-S2A / PR #69 / Issue #68`

This is a governance-only candidate. It does not implement a runtime, authorize implementation, promote a checkpoint, grant credentials, permit deployment, or grant limited-live/live trading authority.

## OBJECTIVE

Define the smallest necessary STAGE-1 prerequisite that closes the confirmed B001 blocker before S2A can be independently reconsidered: a canonical, provider-neutral, typed public market-value plane and deterministic ingest/value-state contracts that later analytical consumers can read without inventing a second source of truth.

The candidate must be implementation-ready as a bounded contract, not implemented. It must make numeric values computable, reproducible, immutable, lineage-complete, time-bounded and compatible with the S1E authority axes. It must preserve the frozen Stage-1/Stage-2 order and leave S2A to a later recompiled authorization after this prerequisite is independently approved and merged.

## CONTEXT AND BLOCKER PROOF

The independent receipt for `HCT-IMPL-AUTH-0009 / HCT-IMP-0009-S2A` is `BLOCKED — CRITICAL 0 / HIGH 6`. B001 is the HIGH/BLOCKER: S1E `NormalizedMarketEvent` carries identity, timing, provenance and payload fingerprints but no typed numeric market values; S1E `MarketStateSnapshot` carries state, trust, authority and event fingerprints but no typed computable market values. S2A cannot calculate deterministic returns, averages, volatility or rolling features without inventing a second truth source.

The handoff also preserves H002–H006: the missing `docs/06-test-benchmark-plan.md` binding, unbounded feature-family scope, missing canonical numeric semantics, insufficient ordered rolling/multi-timeframe lineage and interval semantics, and missing explicit separation of MarketStateTrust from DataAuthority/resource, eligibility and lifecycle axes.

R11 Stage 1 places exchange/public market data, capability/rule, universe, quota/WS governance, ingest/quality, Market-State and cache before the Stage-2 chain `features/indicators/patterns -> regime -> scanner -> strategy engine/catalog/signal -> minimum microstructure`. Module 4 owns normalized immutable market-data envelopes, Module 5 owns coherent Market-State and Module 7 owns quality. This prerequisite must not create a competing truth owner or silently absorb Module 8.

## SCOPE

If separately authorized after independent review and a dedicated checkpoint, the S1F implementation may define and implement only the following contracts and supporting deterministic tests/evidence:

### Typed public market-value plane

- `TradeTick`: typed price and quantity, optional aggressor/side only when canonically available, event/knowledge/wall-receive times, and source/channel/contract/generation/provenance identity;
- `TickerState`: only the last/close/reference fields required by the frozen scope and supported by the canonical source; unsupported fields remain absent or explicitly unknown;
- `CandleBar`: timeframe, interval start/end/close, OHLC, volume where sourced, completeness/closed state, source generation and ordered input lineage;
- mark/index/fair-price and funding evidence only where required and source-supported;
- the minimum frozen Stage-1 order-book value plane. Full depth and advanced microstructure are deferred unless an exact frozen locator makes them necessary for this prerequisite;
- every value object is typed, immutable, versioned and content-fingerprinted. A display string, opaque payload fingerprint or ordinary uncanonicalized float is not a substitute for a typed value.

### Numeric determinism

- Decimal or an equivalent fixed-point representation with a declared precision source, scale limits, quantization and rounding mode;
- canonical numeric serialization used by equality and fingerprints;
- rejection of NaN, positive/negative Infinity, malformed numeric strings, nonpositive prices, invalid negative quantities and impossible OHLC relationships;
- explicit overflow and underflow behavior;
- divide-by-zero, empty, undefined and insufficient-input cases produce typed `UNKNOWN`, `INVALID` or `WARMUP` states as appropriate, never a silent zero, platform exception or fabricated valid number.

### Lineage, windows and time

- source ID, channel, contract, environment, generation, schema/version, provenance, originating event identity and value fingerprint remain bound to every value;
- Market-State remains the coherent-state owner. Feature and later analytical consumers receive read-only value/state contracts;
- rolling and multi-timeframe series carry an ordered manifest of every input value fingerprint or a deterministic Merkle/content manifest. Insert, delete, reorder, correction, generation or value mutation must be visible;
- mixed source, contract, environment or generation fails closed unless an explicit legal cross-source contract exists;
- UTC canonical timestamps keep `event_time`, `knowledge_time`, `wall_receive_time` and monotonic age distinct;
- interval convention, timeframe ID/version/epoch, boundary inclusion, open/closed state and late-correction versioning are explicit and not implementation-defined;
- a late correction creates a new version and does not rewrite prior point-in-time history; an open/incomplete candle cannot feed a closed higher timeframe unless an explicit feature definition allows it.

### S1E axis separation

The contract must preserve a truth-validity matrix covering at least `TRUSTED+RESOURCE_DEGRADED`, `TRUSTED+INELIGIBLE`, `TRUSTED+UNKNOWN`, `STALE`, `GAP`, `SEQUENCE_UNPROVABLE`, `CLOCK_UNTRUSTED` and `RETIRED_GENERATION`. `MarketStateTrust`/quality determine whether a value is trusted, coherent and fresh enough for analytics. Restrictive `DataAuthority` metadata, `RESOURCE_DEGRADED` alone, or `Universe` `INELIGIBLE`/`UNKNOWN` must not falsify a trusted public price/candle. No feature, value or cache layer may upgrade Trust, DataAuthority, eligibility or lifecycle authority.

### Public ingest boundary

Provider-specific transport is `OUT OF SCOPE` when the canonical sources do not provide enough official detail to specify it without guessing. If the frozen Stage-1 contract objectively requires actual public unauthenticated ingest, the future implementation may include only the minimum public boundary, integrated with Module 29 quota/backpressure and S1E generation/quality contracts. It may not add credentials, private APIs, signing or live execution surfaces.

## OUT OF SCOPE

- S2A feature/indicator implementation, concrete feature-family expansion, patterns, regime, scanner, ranking, strategy, signal or microstructure logic;
- Brain, agents, RAG, memory, learning, calibration, promotion or decision authority;
- Risk, Safety, Session Policy, sizing, leverage, OMS, Execution, reconciliation, protection, positions, orders, balances or fills;
- credentials, private/authenticated APIs, signing, exchange account access or real-money behavior;
- persistence, database/RLS, feature stores, HA/fencing, deployment, infrastructure topology or production operations;
- checkpoint promotion, implementation authorization, production credentials, production deployment, limited-live or live trading;
- mutation of frozen requirements, source identities, existing checkpoint records, S1E ownership or PR #69 files;
- provider-specific MEXC protocol/channel claims unless independently supported by canonical official evidence.

## CAPABILITY CLASSIFICATION

`NECESSARY`:

- typed provider-neutral public market values and coherent value-state contracts;
- numeric determinism, validation and canonical serialization;
- immutable value fingerprints and complete source/generation/provenance lineage;
- ordered window/series manifests, interval/time-boundary semantics and late-correction versioning;
- S1E axis separation and restrictive validity matrix;
- deterministic tests, benchmark method and reproducible evidence;
- exact traceability, governance-only diff and negative-capability firewall.

`IMPORTANT`:

- the minimum public unauthenticated transport boundary only if the frozen Stage-1 sources objectively require it;
- explicit Module 29 quota/backpressure integration and public fixture/replay harness where transport is in scope.

`FUTURE`:

- provider-specific MEXC channel/protocol details not established by canonical sources;
- full-depth order book and advanced microstructure;
- multi-provider reconciliation beyond an explicitly approved cross-source contract;
- persistence, HA/fencing, deployment and operations.

`OUT_OF_SCOPE`:

- credentials/private APIs, orders, trading, Risk/OMS/Execution, live authority and every negative capability listed above.

## FILES AND SOURCE LOCK

The candidate and future implementation must be evaluated against canonical `main@625dd0c145087038bdbccd665548d811e187194c` and `HCT-CP-0030`. Frozen requirement blobs:

- `docs/02-requirements.md` — `292da9552ae816e4d51b8a299456305da1658e55`;
- `docs/48-r04-execution-requirements-addendum.md` — `f20c1ed00bdb13801aaff8a3b648371bfcffba58`;
- `docs/54-r05-realtime-requirements-addendum.md` — `636ad01da9c25e760dd5e2f033b93a0f04578a17`;
- `docs/61-r06-intelligence-requirements-addendum.md` — `fea197e60532eb6ff3b11b628b9aabcbcfc00c41`;
- `docs/67-r07-validation-laboratory-requirements-addendum.md` — `c8a426966c5a0dc34704d1413f506332e770c2c7`;
- `docs/73-r08-multitenant-security-requirements-addendum.md` — `c859c0c4a718e3017c34aa50013d4c50959853b4`;
- `docs/80-r09-cockpit-uiux-requirements-addendum.md` — `bc897ebd470857a53055bdee85128b5bd31a5822`;
- `docs/87-r10-observability-audit-incident-finops-requirements-addendum.md` — `023187ef23b01d5a11f978bbfe6e38abf172bb3b`;
- `docs/93-r11-integration-requirements-addendum.md` — `6935e9973696d5b706546d63d847ea398780d936`.

Required governance and integration sources include `docs/00-source-hierarchy.md`, `docs/03-scope.md`, `docs/04-architecture.md`, `docs/06-test-benchmark-plan.md` (`29401ce8fe1616f9390a317bae62d3a157addaa5`), `docs/09-definition-of-done.md`, `docs/10-decisions-ledger.md`, `docs/11-checkpoint.md`, `docs/14-product-module-map.md`, `docs/91-r11-integrated-authority-state-dependency-architecture.md`, `docs/92-r11-v1-module-classification-and-integration-hardening.md`, `docs/96-r11-requirements-freeze-input-inventory.md`, `docs/97-r11-final-integration-audit.md`, `docs/99-r12-frozen-requirements-baseline.md`, `docs/100-r12-requirements-traceability-and-no-loss-proof.md`, `docs/101-r12-freeze-governance-change-control-and-deferred-decisions.md`, `docs/102-r12-freeze-acceptance-matrix.md`, `docs/103-r12-final-planning-freeze-audit.md`, and `adr/HCT-ADR-0049-s1e-market-truth-foundation.md`.

Minimum traceability locators include `R05::Transport and feed requirements::B1-B6`, `R05::Backpressure and resource requirements::B1-B5`, `R05::Time and freshness requirements::B1-B6`, `R05::State coherency requirements::B1-B4`, `R05::Candle/cache/replay requirements::B1-B5`, `R05::Authority requirements::B1-B3`, `R05::Validation requirements::B2,B3,B6,B8,B9,B10,B13,B15,B17`, `INT-002`, `INT-003`, `INT-004`, `INT-011`, `INT-012`, `INT-018`, `INT-022`, `INT-024`, `INT-025`, `INT-026`, `VAL-003`, `VAL-005`, `VAL-006`, `VAL-011`, `VAL-012`, `VAL-013`, `VAL-023`, `VAL-028`, `VAL-030`, `R11-REQ-006`, `R11-REQ-007`, `R11-REQ-011`, `R11-REQ-012`, `R11-REQ-013`, `R11-REQ-014`, `R11-REQ-015`, `R11-REQ-020`, `R11-REQ-022`, `R11-REQ-024`, `R11-REQ-025`, and Decisions `HCT-DEC-0007`, `0008`, `0012`, `0058`, `0060` through `0065`, `0068`, `0069`, `0071`, `0074`, `0077`, `0079`, `0083`, `0084`, `0089`, `0135`, `0136`, `0138`, `0139`, `0140`, `0141`.

## ARCHITECTURE RULES

1. Module 4/5 owns normalized public market values and coherent Market-State; Module 7 owns quality. S1F cannot create a second truth source.
2. S1E `Market-State`, `MarketStateTrust`, `DataAuthority`, generation and provenance are read-only upstream inputs to later analytics. Values must remain tied to them without authority upgrades.
3. `LIVE`, `PAPER`, `SHADOW` and `REPLAY` are non-aliasing environment identities. Replay or fixtures cannot acquire live mutation capability.
4. Source/channel/contract/schema/version/generation/provenance are content-bearing identity, not UI metadata.
5. Unknown, invalid, warmup, stale, gap, sequence-unprovable, clock-untrusted and retired-generation cases fail closed and are observable.
6. A future feature engine consumes value/state contracts read-only and cannot mutate values, Market-State or authority.
7. Exact interval boundaries and point-in-time knowledge are mandatory; wall clock and sleeps are not substitutes for injected timestamps.

## CONSTRAINTS

- planning/governance-only diff: exactly one candidate document, two Work Orders and one pull-request-only workflow;
- exact canonical base and exact-head CI are mandatory;
- no product/runtime code, dependency lock, frozen-source rewrite, checkpoint edit or PR #69 mutation;
- no provider detail may be guessed; unsupported fields remain absent/unknown;
- benchmark targets are not invented. Workload assumptions, deterministic method, baseline/regression thresholds or an approved no-hard-target rationale are required;
- no authorization is implied by planning freeze or by this candidate; implementation authorization and live trading authorization remain separate gates.

## ACCEPTANCE CRITERIA

1. B001 is closed at the contract level by a typed value plane that can support deterministic public analytics without a second truth source.
2. Typed value kinds, supported fields and minimum order-book scope are explicit; unsupported/provider-specific details are explicitly deferred.
3. Numeric representation, precision, scale, rounding, finite-value, invariant, overflow, empty and divide-by-zero semantics are canonical and testable.
4. Every value and every rolling/multi-timeframe input series has immutable fingerprint and complete ordered lineage; mutations and mixed identities fail closed.
5. UTC event/knowledge/receive/monotonic semantics, timeframe ID/version/epoch, interval boundaries, incomplete state and correction versioning are explicit.
6. The truth-validity matrix preserves `MarketStateTrust` versus `DataAuthority`, resource, eligibility and lifecycle axes, including `TRUSTED+RESOURCE_DEGRADED` and `TRUSTED+INELIGIBLE`.
7. `docs/06-test-benchmark-plan.md` is in the source lock and the benchmark method defines workload assumptions, deterministic procedure, evidence context and limitations.
8. Exact traceability covers source hierarchy, R05/R06/R07/R11 locators, decisions, ADR-0049, DoD and frozen baseline/change-control rules.
9. Negative tests prove no credentials, private APIs, trading, Risk/OMS/Execution, persistence, deployment, checkpoint or live authority.
10. Exact-head governance CI proves the four-file allowlist, base/CP0030 lock and planning-only boundary.

## TESTS AND BENCHMARK EVIDENCE

Required future tests include typed parsing and canonical serialization; Decimal/fixed-point round trips; NaN/Infinity/malformed/negative/nonpositive/impossible-OHLC rejection; overflow/underflow; empty/divide-by-zero/warmup states; immutable fingerprint mutation detection; ordered insertion/deletion/reorder/correction/generation tests; interval and close-boundary tests; late-correction versioning; mixed source/contract/environment/generation rejection; UTC/time-axis and no-sleep injected-clock tests; state/value truth-validity matrix tests; public fixture/replay determinism; schema drift and sequence/gap/reconnect/stale/backpressure/quota cases where transport is in scope; and negative-capability scanning.

Benchmark method must bind `docs/06-test-benchmark-plan.md`: declare symbols, channels, event rate, candle intervals, depth and fixture sizes; use deterministic fixtures and a pinned tool/runtime/dependency environment; measure normalization throughput, value-state update latency, memory footprint and replay throughput; add queue/backpressure measurements only if public transport is in scope; report baseline and regression thresholds or an approved no-hard-target rationale; and publish code/build/dependency, fixture/config/policy, seed, hardware/environment, tool version, hashes and limitations. No uncontrolled live network is allowed in CI.

## DELIVERABLES

- one governance candidate document;
- `work-orders/HCT-IMPL-AUTH-0010.md` and `work-orders/HCT-IMP-0010-S1F.md`;
- one exact-head pull-request-only governance workflow;
- one new authorization Issue `#70`;
- one open/unmerged governance PR against `main@625dd0c145087038bdbccd665548d811e187194c`;
- author-side exact-head CI evidence and a fresh independent HIGH_ASSURANCE review request.

## REVIEW FORMAT

The independent review must report: `repositorySync`, `sourceMatch`, `blockedCandidateId`, `blockedCandidatePr`, `blockedCandidateHead`, `blockedCandidateMarked`, `blockerB001Confirmed`, `normalizedEventCarriesTypedValues`, `marketStateCarriesTypedValues`, `existingCanonicalValuePlaneSearch`, `canonicalMain`, `checkpoint`, `checkpointFailClosed`, `prerequisiteAuthorizationId`, `prerequisiteImplementationId`, `prerequisiteScopeName`, `capabilityClassification`, `typedValueKinds`, `canonicalNumericPolicy`, `orderedInputLineage`, `intervalSemantics`, `s1eAxisSeparation`, `docs06Bound`, `benchmarkMethodDefined`, `exactTraceability`, `governanceOnlyDiff`, `newIssue`, `newBranch`, `newPr`, `newCandidateHead`, `exactHeadRun`, `exactHeadJob`, `exactHeadConclusion`, `criticalAuthorFindings`, `highAuthorFindings`, `implementationAuthorized`, `productionCredentials`, `productionDeployment`, `limitedLive`, `liveTrading`, `stopConditionRespected`.

## AUTHORIZATION FIREWALL

`implementation_authorized=false`

`production_credentials_authorized=false`

`production_deployment_authorized=false`

`limited_live_authorized=false`

`live_trading_authorized=false`

PLANNING FREEZE is not IMPLEMENTATION AUTHORIZATION. IMPLEMENTATION AUTHORIZATION is not LIVE TRADING AUTHORIZATION. No implicit interpretation may change these flags.

## REQUIRED INDEPENDENT REVIEW

Keep this candidate and its PR OPEN/UNMERGED. A fresh independent HIGH_ASSURANCE review must validate exact head, source identity, no-loss/no-weakening, B001 closure, all typed/numeric/lineage/time/axis/benchmark contracts, exact governance-only diff and the authorization firewall. This author-side candidate is not approval.

## STOP CONDITION

After author-side evidence is published, stop. Do not merge PR #69 or this prerequisite PR, do not create a checkpoint, do not implement S1F/S2A, do not authorize credentials/private APIs, do not deploy, and do not activate limited-live or live/real-money trading. The next mandatory action is independent HIGH_ASSURANCE review of this prerequisite candidate.
