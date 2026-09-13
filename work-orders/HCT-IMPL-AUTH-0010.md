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

- public unauthenticated realtime session ingest is `NECESSARY`, through one provider-neutral session/transport interface and the V1 concrete MEXC Futures public realtime adapter;
- typed immutable/versioned `TradeTick`, `TickerState`, `CandleBar`, `OrderBookSnapshot`, `OrderBookDelta`, `BookLevel`, `ReferencePriceEvidence` and `FundingEvidence`, with explicit `SUPPORTED`/`UNSUPPORTED`/`UNKNOWN` capability state;
- exact `Decimal` numeric representation using source decimal text or exact integer-plus-scale material, with `S1F_NUMERIC_MAX_PRECISION=38`, `S1F_NUMERIC_MAX_SCALE=18`, `S1F_NUMERIC_MAX_INTEGER_DIGITS=20` and `S1F_NUMERIC_POLICY_VERSION=DECIMAL_TEXT_V1`;
- canonical base-10 serialization with no exponent/leading plus, canonical zero, irrelevant trailing-zero removal, float rejection, no raw rounding/quantization, finite/invariant validation and typed overflow/underflow/empty/divide-by-zero outcomes;
- source/channel/contract/environment/generation/schema/version/provenance/originating-event/value-fingerprint identity;
- Market-State-owned coherent state and read-only consumers;
- ordered rolling/multi-timeframe input manifests or deterministic Merkle/content manifests with mutation visibility;
- UTC Unix-epoch-aligned fixed timeframes, half-open `[start, end)` intervals, explicit `event_time`/`knowledge_time`/`wall_receive_time`/monotonic axes, `OPEN`/`CLOSED` finality and immutable late-correction revisions;
- explicit truth-validity treatment of MarketStateTrust, DataAuthority/resource, Universe eligibility and lifecycle axes;
- deterministic fixtures/replay/tests/evidence and a bounded benchmark method tied to `docs/06-test-benchmark-plan.md`;
- MEXC session generation/reconnect/retirement, bounded retry/backoff/jitter/circuit, deterministic staged resubscription, Module 29 admission/backpressure, quarantine before canonical normalization and S1E generation/quality binding.

Protocol facts are restricted to the official source lock below. Unsupported provider fields remain explicit `UNSUPPORTED`/`UNKNOWN`; private/account/order/position/balance streams are forbidden.

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

Official MEXC public source lock: `https://mexcdevelop.github.io/apidocs/contract_v1_en/`, retrieved `2026-09-13`, raw response SHA-256 `57ebc13fea788a1c568c8aeabfdf50acc0c9f5b5a882af4855837d53499940e`. Bound sections are Native WS connection address `wss://contract.mexc.com/edge`; ping/pong and disconnect if no ping within one minute; public `sub.tickers`, `sub.deal`, `sub.depth`, `sub.depth.full`, `sub.kline`; and REST depth snapshot/version maintenance. Evidence uses URL/date/raw-response SHA-256 and deterministic pinned fixtures/fakes; CI does not fetch the network.

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
8. Public realtime session ingest is NECESSARY, public-only and bounded by the locked MEXC contract; session generations retire on reconnect and cannot mutate current state.

## CONSTRAINTS

- exactly four governance files in the candidate PR: the candidate document, this Work Order, `HCT-IMP-0010-S1F.md` and the pull-request-only workflow;
- exact base `625dd0c145087038bdbccd665548d811e187194c` and fail-closed CP0030 are mandatory;
- no `workflow_dispatch`, no runtime/product code, no dependency-lock changes, no frozen-source rewrite and no checkpoint mutation;
- canonical numeric policy is exactly `DECIMAL_TEXT_V1` with precision 38, scale 18 and integer digits 20; binary float input, raw rounding and arbitrary raw quantization are forbidden;
- no provider protocol fact may appear outside the official MEXC source lock; provider DTOs are quarantined and cannot become canonical truth;
- benchmark mode and profiles are exactly `BASELINE_ESTABLISHMENT_V1`, `S1F-CONTRACT-MICRO-V1`, `S1F-NOMINAL-MULTICHANNEL-V1` and `S1F-STRESS-BACKPRESSURE-V1`;
- planning freeze is not implementation authorization, and implementation authorization is not live-trading authorization.

## ACCEPTANCE CRITERIA

1. A typed public market-value plane and `NECESSARY` public MEXC session ingest close B001 at the contract level without inventing a second truth source.
2. The complete value-family manifest is explicit: `TradeTick`, `TickerState`, `CandleBar`, `OrderBookSnapshot`, `OrderBookDelta`, `BookLevel`, `ReferencePriceEvidence`, `FundingEvidence` and capability state.
3. Numeric policy is exactly `DECIMAL_TEXT_V1` with Decimal precision 38, scale 18, integer digits 20, base-10 no-exponent serialization and binary-float rejection.
4. Value fingerprints and ordered input manifests make insert/delete/reorder/correction/generation/value changes visible.
5. UTC Unix-epoch alignment, half-open `[start, end)`, `knowledge_time` admissibility, `OPEN`/`CLOSED` finality and immutable correction revisions are explicit.
6. The S1E truth-validity matrix preserves trust, quality, DataAuthority/resource, eligibility and lifecycle independently.
7. `docs/06-test-benchmark-plan.md` is bound and benchmark method/evidence fields are complete.
8. Exact traceability, negative scope and governance-only allowlist pass exact-head CI.

## TESTS

The future implementation must provide deterministic tests for public session generation/reconnect/retirement, staged resubscription, bounded retry/backoff/circuit and Module 29 admission; provider fixture schema validation/quarantine; exact Decimal parse/serialization/equality/fingerprint; rejection of binary float, NaN, Infinity, malformed, overflow/scale violation and negative/impossible invariants; Trade/Ticker/Candle/Book/ReferencePrice/Funding constructors and capability state; order-book snapshot/delta ordering, duplicate/gap/out-of-order/generation rollover/resync; half-open interval/UTC epoch/OPEN-CLOSED finality/immutable revisions; ordered lineage mutations; S1E axis matrix; LIVE/PAPER/SHADOW/REPLAY non-aliasing; negative scanner; and deterministic benchmark fixtures.

Benchmark evidence freezes `S1F_BENCHMARK_MODE=BASELINE_ESTABLISHMENT_V1` and: `S1F-CONTRACT-MICRO-V1` = 1 symbol, ticker 64/deal 256/depth 128/depth-full 32/kline 32, total 512, depth 5, 60-second replay; `S1F-NOMINAL-MULTICHANNEL-V1` = 8 symbols, ticker 1024/deal 4096/depth 2048/depth-full 512/kline 512, total 8192, depth 20, 900-second replay; `S1F-STRESS-BACKPRESSURE-V1` = 32 symbols, ticker 8192/deal 32768/depth 16384/depth-full 4096/kline 4096, total 65536, depth 20, queue capacity 4096, 3600-second replay. Mandatory measurements are normalization throughput, per-event/value-state update latency distribution, replay throughput, peak/steady memory and queue depth/age. Acceptance is correctness, bounded completion, no unbounded memory/queue growth and complete baseline publication, without a product SLO. Evidence records code/build/dependency/runtime, fixture/config/policy versions, seed, hardware/environment, tool, raw artifact/hash and limitations. Future regression thresholds are proposals until later governance.

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
