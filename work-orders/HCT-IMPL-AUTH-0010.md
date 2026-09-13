# HCT-IMPL-AUTH-0010 — Realtime Public Market Value Plane & Ingest Foundation Authorization

Status: `PENDING_INDEPENDENT_HIGH_ASSURANCE_REVIEW`
Risk: `HIGH_ASSURANCE`
Canonical base: `main@625dd0c145087038bdbccd665548d811e187194c`
Checkpoint: `HCT-CP-0030 / S1E_IMPLEMENTATION_APPROVED_MERGED`
Authorization Issue: `#70`
Proposed implementation: `HCT-IMP-0010-S1F`
Governance branch: `governance/HCT-IMPL-AUTH-0010-S1F`
Scope name: `Realtime Public Market Value Plane & Ingest Foundation`

## OBJECTIVE

Prepare a governance-only authorization candidate for the smallest Stage-1 prerequisite required by the independent B001 blocker on `HCT-IMPL-AUTH-0009 / HCT-IMP-0009-S2A`. The candidate defines a canonical provider-neutral typed public market-value plane and deterministic ingest/value-state contracts. It does not implement product/runtime code, authorize implementation, promote a checkpoint or grant operational/live authority.

## CONTEXT

The blocked S2A candidate is `PR #69 / Issue #68`, head `b697dd031aa0c09ef6f5b047dfe3095e542f1043`, against `main@625dd0c145087038bdbccd665548d811e187194c`. Its independent receipt is `BLOCKED — CRITICAL 0 / HIGH 6`. B001 is a HIGH/BLOCKER because S1E `NormalizedMarketEvent` and `MarketStateSnapshot` expose identity, fingerprints, timing, trust and authority but no typed numeric market values from which deterministic analytics can be computed. H002–H006 remain part of the handoff: missing `docs/06-test-benchmark-plan.md` binding, unbounded feature families, missing numeric policy, insufficient ordered window/interval semantics and missing S1E axis separation.

R11 Stage 1 owns the dependency chain through public market data, capability/rule, universe, quota/WS governance, market ingest/quality, Market-State and cache. Stage 2 consumes that plane. S1F is a prerequisite only; it does not repurpose AUTH-0009 and S2A must be recompiled after an eventual independent approval and merge.

## SCOPE

The future separately authorized S1F implementation may define and implement only:

- typed immutable/versioned `TradeTick`, `TickerState`, `CandleBar` and source-supported mark/index/fair/funding evidence;
- the minimum frozen Stage-1 order-book value plane, with full depth/advanced microstructure explicitly deferred unless a frozen locator proves it necessary;
- Decimal or fixed-point numeric representation, precision/scale/quantization/rounding, canonical serialization, finite-value and invariant validation, overflow/underflow and typed empty/divide-by-zero semantics;
- source/channel/contract/environment/generation/schema/version/provenance/originating-event/value-fingerprint identity;
- Market-State-owned coherent state and read-only consumers;
- ordered rolling/multi-timeframe input manifests or deterministic Merkle/content manifests with mutation visibility;
- UTC event/knowledge/wall-receive/monotonic time axes, explicit interval/timeframe ID/version/epoch, close/incomplete semantics and late-correction versioning;
- explicit truth-validity treatment of MarketStateTrust, DataAuthority/resource, Universe eligibility and lifecycle axes;
- deterministic fixtures/replay/tests/evidence and a bounded benchmark method tied to `docs/06-test-benchmark-plan.md`;
- a minimum public unauthenticated transport boundary only when frozen sources objectively require it and only with Module 29 quota/backpressure and S1E generation/quality binding.

No concrete provider protocol may be guessed from this Work Order. Unsupported provider details remain deferred.

## OUT OF SCOPE

No S1F product implementation is authorized by this Work Order. Out of scope are S2A feature families and all patterns, regime, scanner, ranking, strategy, signal, advanced microstructure, Brain, agents, RAG, memory, learning, calibration, promotion authority, Risk, Safety, Session Policy, sizing, leverage, OMS, Execution, reconciliation, protection, account/private data, credentials, signing, persistence, database/RLS, feature stores, HA/fencing, deployment, checkpoint promotion, production credentials, production deployment, limited-live and live/real-money trading. S1E ownership, frozen requirements, source identities, checkpoint files and PR #69 must not be mutated.

## FILES/SOURCES TO READ

Read the exact canonical base and checkpoint before any future implementation:

- `docs/00-source-hierarchy.md`, `docs/02-requirements.md`, `docs/03-scope.md`, `docs/04-architecture.md`, `docs/06-test-benchmark-plan.md`, `docs/09-definition-of-done.md`, `docs/10-decisions-ledger.md`, `docs/11-checkpoint.md`, `docs/14-product-module-map.md`;
- `docs/48-r04-execution-requirements-addendum.md`, `docs/54-r05-realtime-requirements-addendum.md`, `docs/61-r06-intelligence-requirements-addendum.md`, `docs/67-r07-validation-laboratory-requirements-addendum.md`, `docs/73-r08-multitenant-security-requirements-addendum.md`, `docs/80-r09-cockpit-uiux-requirements-addendum.md`, `docs/87-r10-observability-audit-incident-finops-requirements-addendum.md`, `docs/93-r11-integration-requirements-addendum.md`;
- `docs/91-r11-integrated-authority-state-dependency-architecture.md`, `docs/92-r11-v1-module-classification-and-integration-hardening.md`, `docs/96-r11-requirements-freeze-input-inventory.md`, `docs/97-r11-final-integration-audit.md`, `docs/99-r12-frozen-requirements-baseline.md`, `docs/100-r12-requirements-traceability-and-no-loss-proof.md`, `docs/101-r12-freeze-governance-change-control-and-deferred-decisions.md`, `docs/102-r12-freeze-acceptance-matrix.md`, `docs/103-r12-final-planning-freeze-audit.md`;
- `adr/HCT-ADR-0049-s1e-market-truth-foundation.md`, `docs/131-implementation-authorization-s1f-candidate.md`, and canonical S1E contracts/evidence as read-only context.

Frozen requirement blob identities are:

`docs/02-requirements.md=292da9552ae816e4d51b8a299456305da1658e55`, `docs/48-r04-execution-requirements-addendum.md=f20c1ed00bdb13801aaff8a3b648371bfcffba58`, `docs/54-r05-realtime-requirements-addendum.md=636ad01da9c25e760dd5e2f033b93a0f04578a17`, `docs/61-r06-intelligence-requirements-addendum.md=fea197e60532eb6ff3b11b628b9aabcbcfc00c41`, `docs/67-r07-validation-laboratory-requirements-addendum.md=c8a426966c5a0dc34704d1413f506332e770c2c7`, `docs/73-r08-multitenant-security-requirements-addendum.md=c859c0c4a718e3017c34aa50013d4c50959853b4`, `docs/80-r09-cockpit-uiux-requirements-addendum.md=bc897ebd470857a53055bdee85128b5bd31a5822`, `docs/87-r10-observability-audit-incident-finops-requirements-addendum.md=023187ef23b01d5a11f978bbfe6e38abf172bb3b`, and `docs/93-r11-integration-requirements-addendum.md=6935e9973696d5b706546d63d847ea398780d936`.

`docs/06-test-benchmark-plan.md` is an additional mandatory source lock (`29401ce8fe1616f9390a317bae62d3a157addaa5`) because H002 exposed its omission from S2A.

## REQUIREMENTS

Every future behavior, test and evidence item must carry exact locators and preserve source authority. Minimum traceability includes:

- `REQ02::Trading intelligence requirements::B1,B7,B8`;
- R05 `Transport and feed requirements::B1-B6`, `Backpressure and resource requirements::B1-B5`, `Time and freshness requirements::B1-B6`, `State coherency requirements::B1-B4`, `Candle/cache/replay requirements::B1-B5`, `Universe lifecycle requirements::B1-B2`, `Authority requirements::B1-B3`, and the applicable `Validation requirements::B2,B3,B6,B8,B9,B10,B13,B15,B17`;
- `INT-002`, `INT-003`, `INT-004`, `INT-011`, `INT-012`, `INT-018`, `INT-022`, `INT-024`, `INT-025`, `INT-026`;
- `VAL-003`, `VAL-005`, `VAL-006`, `VAL-011`, `VAL-012`, `VAL-013`, `VAL-023`, `VAL-028`, `VAL-030`;
- `R11-REQ-006`, `R11-REQ-007`, `R11-REQ-011`, `R11-REQ-012`, `R11-REQ-013`, `R11-REQ-014`, `R11-REQ-015`, `R11-REQ-020`, `R11-REQ-022`, `R11-REQ-024`, `R11-REQ-025`;
- `HCT-DEC-0007`, `HCT-DEC-0008`, `HCT-DEC-0012`, `HCT-DEC-0058`, `HCT-DEC-0060`, `HCT-DEC-0061`, `HCT-DEC-0062`, `HCT-DEC-0063`, `HCT-DEC-0064`, `HCT-DEC-0065`, `HCT-DEC-0068`, `HCT-DEC-0069`, `HCT-DEC-0071`, `HCT-DEC-0074`, `HCT-DEC-0077`, `HCT-DEC-0079`, `HCT-DEC-0083`, `HCT-DEC-0084`, `HCT-DEC-0089`, `HCT-DEC-0135`, `HCT-DEC-0136`, `HCT-DEC-0138`, `HCT-DEC-0139`, `HCT-DEC-0140`, `HCT-DEC-0141` and ADR-0049.

## ARCHITECTURE RULES

1. Module 4/5 remains the owner of normalized public market values and coherent Market-State; Module 7 remains the quality owner. S1F must not create a second truth source.
2. `MarketStateTrust`, `DataAuthority`, generation, provenance and lifecycle are read-only upstream axes. `RESOURCE_DEGRADED` or Universe `INELIGIBLE`/`UNKNOWN` cannot falsify trusted public prices/candles and no downstream layer may upgrade authority.
3. All value objects are immutable/versioned and fingerprinted over canonical typed fields. Source/channel/contract/environment/generation/schema/version are identity.
4. `LIVE`, `PAPER`, `SHADOW` and `REPLAY` are non-aliasing environments. Fixture/replay input cannot gain live mutation capability.
5. Event, knowledge, wall-receive and monotonic time are distinct. Intervals, close boundaries, timeframe ID/version/epoch and correction versions are explicit.
6. Mixed generation/source/contract/environment, missing/invalid/unknown, stale/gap, sequence-unprovable, clock-untrusted and retired-generation cases fail closed.
7. S2A and future analytical consumers are read-only. Feature evidence cannot create a candidate trade, Risk approval, Execution plan or live authority.

## CONSTRAINTS

- exactly four governance files in the candidate PR: the candidate document, this Work Order, `HCT-IMP-0010-S1F.md` and the pull-request-only workflow;
- exact base `625dd0c145087038bdbccd665548d811e187194c` and fail-closed CP0030 are mandatory;
- no `workflow_dispatch`, no runtime/product code, no dependency-lock changes, no frozen-source rewrite and no checkpoint mutation;
- no provider-specific MEXC transport/channel detail without canonical official support;
- no numeric performance target may be invented; workload assumptions and method must be declared with a baseline/regression threshold or approved no-hard-target rationale;
- planning freeze is not implementation authorization, and implementation authorization is not live-trading authorization.

## ACCEPTANCE CRITERIA

1. A typed public market-value plane closes B001 at the contract level without inventing a second truth source.
2. `TradeTick`, `TickerState`, `CandleBar`, supported mark/index/fair/funding evidence and minimum order-book scope are explicit; unsupported fields are absent/unknown and deferred scope is stated.
3. Decimal/fixed-point representation, precision/scale, quantization/rounding, canonical serialization, finite-value, invalid-value, overflow/underflow, empty and divide-by-zero semantics are testable.
4. Value fingerprints and ordered input manifests make insert/delete/reorder/correction/generation/value changes visible.
5. UTC axes, interval/timeframe identity, completeness/close semantics and point-in-time corrections are explicit.
6. The S1E truth-validity matrix preserves trust, quality, DataAuthority/resource, eligibility and lifecycle independently.
7. `docs/06-test-benchmark-plan.md` is bound and benchmark method/evidence fields are complete.
8. Exact traceability, negative scope and governance-only allowlist pass exact-head CI.

## TESTS

The future implementation must provide deterministic tests for typed parsing, canonical numeric serialization, Decimal/fixed-point equality, NaN/Infinity/malformed/nonpositive/negative/impossible-OHLC rejection, overflow/underflow, empty/divide-by-zero/warmup outcomes, fingerprint immutability, ordered manifests, Merkle/content changes, interval boundary/close/incomplete behavior, late-correction versioning, mixed identity rejection, UTC injected time, source/generation fencing, S1E truth-validity matrix, fixture/replay repeatability, schema drift, sequence/gap/stale/reconnect/backpressure/quota cases where transport is included, and a negative-capability scanner.

Benchmark evidence must declare symbols, channels, event rate, candle intervals, depth, fixture sizes, deterministic procedure, baseline/regression thresholds or an approved no-hard-target rationale, code/build/dependency, fixture/config/policy, seed, hardware/environment, tool version, hashes and limitations. At minimum measure normalization throughput, value-state update latency, memory footprint and replay throughput. Public transport queue/backpressure is measured only if included, with no uncontrolled live network in CI.

## DELIVERABLES

- this authorization Work Order;
- `HCT-IMP-0010-S1F` implementation Work Order;
- candidate document `docs/131-implementation-authorization-s1f-candidate.md`;
- exact-head pull-request-only governance workflow;
- Issue `#70`, open/unmerged prerequisite PR and author-side evidence;
- a fresh independent HIGH_ASSURANCE review request. No checkpoint or implementation follows automatically.

## REVIEW FORMAT

Report the required fields from the candidate document, including `repositorySync`, `sourceMatch`, `blockedCandidateMarked`, `blockerB001Confirmed`, typed-value presence/search result, `canonicalMain`, `checkpointFailClosed`, `prerequisiteAuthorizationId`, `prerequisiteImplementationId`, capability classification, typed value kinds, numeric policy, ordered lineage, interval semantics, S1E axis separation, `docs06Bound`, benchmark method, exact traceability, governance-only diff, new Issue/branch/PR/head/CI run/job/conclusion, author findings, all authorization firewall flags and `stopConditionRespected`.

## STOP CONDITION

Publish author-side evidence and stop with the candidate OPEN/UNMERGED. Do not merge PR #69 or the prerequisite PR, create a checkpoint, implement S1F/S2A, configure credentials, use private APIs, deploy, activate limited-live or trade real money. Require independent HIGH_ASSURANCE review before any further governed action.
