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

- `TradeTick`: exact Decimal price and nonnegative Decimal quantity, event identity/times and optional side/aggressor only when provider-authoritative;
- `TickerState`: last price, bid/ask when present, reference fields and explicit unavailable state for every absent provider field;
- `CandleBar`: Decimal OHLC, sourced volume/amount, timeframe/interval/finality/revision and ordered lineage;
- `OrderBookSnapshot` and `OrderBookDelta` with ordered bid/ask `BookLevel(price, quantity)`, source/channel/contract/generation/schema/provenance, sequence/update evidence and snapshot/delta identity;
- `ReferencePriceEvidence` with typed kind `MARK`, `INDEX` or `FAIR`, exact value and provenance, plus `FundingEvidence` with rate/value, applicable time/boundary and provenance;
- capability state `SUPPORTED`, `UNSUPPORTED` or `UNKNOWN` per family/channel. Full analytical microstructure remains future; raw order-book value contracts are necessary now;
- every value object is typed, immutable, versioned and content-fingerprinted. A display string, opaque payload fingerprint or ordinary uncanonicalized float is not a substitute for a typed value.

### Numeric determinism

- exact canonical backend type: `Decimal` parsed from source decimal text or exact integer-plus-scale material; binary float input is rejected at authoritative constructors;
- exact bounds: `S1F_NUMERIC_MAX_PRECISION=38`, `S1F_NUMERIC_MAX_SCALE=18`, `S1F_NUMERIC_MAX_INTEGER_DIGITS=20`; these bounds cover the official MEXC examples and are safety limits, not truncation instructions;
- raw exchange values are never rounded to fit. Provider/contract precision and increments are validated when authoritative ContractReference/capability material supplies them;
- canonical cross-runtime serialization is base-10 decimal text with no exponent, no leading plus, canonical zero and removal of semantically irrelevant trailing fractional zeros; material scale is included separately in the policy fingerprint;
- `S1F_NUMERIC_POLICY_VERSION=DECIMAL_TEXT_V1` and its policy fingerprint bind grammar, bounds and validation rules;
- rejection of NaN, positive/negative Infinity, malformed numeric strings, nonpositive prices, invalid negative quantities and impossible OHLC relationships;
- explicit overflow and scale-limit rejection as typed `INVALID`/`UNKNOWN` with reason code; no clipping, saturation or fallback zero;
- raw-value quantization/rounding is forbidden. An operation requiring quantization must name its increment and rounding rule in a versioned policy;
- divide-by-zero, empty, undefined and insufficient-input cases produce typed `UNKNOWN`, `INVALID` or `WARMUP` states as appropriate, never a silent zero, platform exception or fabricated valid number.

### Lineage, windows and time

- source ID, channel, contract, environment, generation, schema/version, provenance, originating event identity and value fingerprint remain bound to every value;
- Market-State remains the coherent-state owner. Feature and later analytical consumers receive read-only value/state contracts;
- rolling and multi-timeframe series carry an ordered manifest of every input value fingerprint or a deterministic Merkle/content manifest. Insert, delete, reorder, correction, generation or value mutation must be visible;
- mixed source, contract, environment or generation fails closed unless an explicit legal cross-source contract exists;
- UTC canonical timestamps keep `event_time`, `knowledge_time`, `wall_receive_time` and monotonic age distinct;
- canonical time zone is UTC; standard fixed timeframes align to Unix epoch multiples of the duration unless an authoritative venue contract explicitly requires another alignment;
- canonical fixed-bar interval is half-open `[start, end)`: start inclusive, end exclusive; `S1F_INTERVAL_MODEL=HALF_OPEN_START_INCLUSIVE_END_EXCLUSIVE`;
- `event_time` is source market time, `wall_receive_time` is local UTC receive time, monotonic elapsed evidence measures age/latency, and `knowledge_time` is the earliest point HCT had admissible evidence of that value/version;
- point-in-time replay/admissibility is governed by `knowledge_time`, never future `event_time` alone;
- `CandleBar.finality` is explicitly `OPEN` or `CLOSED`; it becomes `CLOSED` only after the interval boundary and required source/finality evidence under capability policy;
- a late/corrected bar creates an immutable revision with predecessor/source lineage and a new fingerprint; prior point-in-time versions are never rewritten;
- an open/incomplete lower-timeframe bar cannot enter a closed higher-timeframe window; timeframe identity includes duration/alignment/version and mixed versions fail closed.

### S1E axis separation

The contract must preserve a truth-validity matrix covering at least `TRUSTED+RESOURCE_DEGRADED`, `TRUSTED+INELIGIBLE`, `TRUSTED+UNKNOWN`, `STALE`, `GAP`, `SEQUENCE_UNPROVABLE`, `CLOCK_UNTRUSTED` and `RETIRED_GENERATION`. `MarketStateTrust`/quality determine whether a value is trusted, coherent and fresh enough for analytics. Restrictive `DataAuthority` metadata, `RESOURCE_DEGRADED` alone, or `Universe` `INELIGIBLE`/`UNKNOWN` must not falsify a trusted public price/candle. No feature, value or cache layer may upgrade Trust, DataAuthority, eligibility or lifecycle authority.

### Public ingest boundary

Public unauthenticated realtime session ingest is `NECESSARY` for S1F. The future implementation includes one provider-neutral session/transport interface and the V1 concrete MEXC Futures public realtime adapter. The official source lock is the current MEXC Contract API page at `https://mexcdevelop.github.io/apidocs/contract_v1_en/`, retrieved `2026-09-13`, raw HTML SHA-256 `57ebc13fea788a1c568c8aeabfdf50acc0c9f5b5a882af4855837d53499940e`. Relevant official sections are Native WS connection address (`wss://contract.mexc.com/edge`), ping/pong and one-minute disconnect rule, Public Channels `sub.tickers`, `sub.deal`, `sub.depth`, `sub.depth.full` and `sub.kline`, and depth maintenance by REST snapshot/version followed by WS updates. The raw response is retained in the review evidence cache under the URL/date/SHA-256 convention; CI uses pinned fixtures/fakes and never fetches this URL.

The adapter is public-only and decodes provider payloads through quarantine/schema validation into canonical typed events; provider DTOs never become canonical truth. Session generation is created on each connection/reconnection and retired before the replacement can publish. Reconnect uses bounded retry budget, exponential backoff with bounded jitter and circuit state; staged resubscription is deterministic and duplicate intent is idempotent. Module 29 admission/backpressure is consumed before public messages enter normalization. Private/account/order/position/balance streams are forbidden. Transport loss, gap and resync evidence flows to S1E quality/Market-State owners.

## NORMATIVE DECISION LOCK

`S1F_TRANSPORT_MODE=NECESSARY_PUBLIC_UNAUTHENTICATED`

`S1F_MEXC_SOURCE_URL=https://mexcdevelop.github.io/apidocs/contract_v1_en/`

`S1F_MEXC_SOURCE_RETRIEVED=2026-09-13`

`S1F_MEXC_SOURCE_SHA256=57ebc13fea788a1c568c8aeabfdf50acc0c9f5b5a882af4855837d53499940e`

`S1F_MEXC_WS_URL=wss://contract.mexc.com/edge`

`S1F_MEXC_PUBLIC_CHANNELS=sub.tickers,sub.deal,sub.depth,sub.depth.full,sub.kline`

`S1F_MEXC_PING_POLICY=ping every 10-20 seconds; disconnect if no ping within 1 minute`

`S1F_NO_PRIVATE_CHANNELS=true`

`S1F_DECODE_BOUNDARY=provider payload -> quarantine/schema validation -> canonical typed public value event`

`S1F_SESSION_GENERATION=each connection/reconnection creates a generation; retired generations cannot publish`

`S1F_NUMERIC_TYPE=Decimal`

`S1F_NUMERIC_POLICY_VERSION=DECIMAL_TEXT_V1`

`S1F_NUMERIC_MAX_PRECISION=38`

`S1F_NUMERIC_MAX_SCALE=18`

`S1F_NUMERIC_MAX_INTEGER_DIGITS=20`

`S1F_NUMERIC_GRAMMAR=base-10 decimal text; no exponent; no leading plus; canonical zero`

`S1F_FLOAT_INPUT=REJECTED`

`S1F_RAW_VALUES=exact; no raw rounding; no raw quantization`

`S1F_INTERVAL_MODEL=HALF_OPEN_START_INCLUSIVE_END_EXCLUSIVE`

`S1F_TIMEZONE=UTC`

`S1F_ALIGNMENT=UNIX_EPOCH_MULTIPLES`

`S1F_KNOWLEDGE_ADMISSIBILITY=knowledge_time`

`S1F_CANDLE_FINALITY=OPEN_UNTIL_BOUNDARY_AND_SOURCE_FINALITY`

`S1F_LATE_CORRECTION=NEW_IMMUTABLE_REVISION`

`S1F_VALUE_FAMILIES=TradeTick,TickerState,CandleBar,OrderBookSnapshot,OrderBookDelta,BookLevel,ReferencePriceEvidence,FundingEvidence`

`S1F_CAPABILITY_STATES=SUPPORTED,UNSUPPORTED,UNKNOWN`

`S1F_BENCHMARK_MODE=BASELINE_ESTABLISHMENT_V1`

`S1F_PROFILE_CONTRACT_MICRO_V1=symbols=1;ticker=64;deal=256;depth=128;depth-full=32;kline=32;total=512;depth-levels=5;replay-seconds=60`

`S1F_PROFILE_NOMINAL_MULTICHANNEL_V1=symbols=8;ticker=1024;deal=4096;depth=2048;depth-full=512;kline=512;total=8192;depth-levels=20;replay-seconds=900`

`S1F_PROFILE_STRESS_BACKPRESSURE_V1=symbols=32;ticker=8192;deal=32768;depth=16384;depth-full=4096;kline=4096;total=65536;depth-levels=20;queue-capacity=4096;replay-seconds=3600`

`S1F_BENCHMARK_MEASUREMENTS=normalization_throughput;value_state_latency_distribution;replay_throughput;peak_steady_memory;queue_depth_age`

## OUT OF SCOPE

- S2A feature/indicator implementation, concrete feature-family expansion, patterns, regime, scanner, ranking, strategy, signal or microstructure logic;
- Brain, agents, RAG, memory, learning, calibration, promotion or decision authority;
- Risk, Safety, Session Policy, sizing, leverage, OMS, Execution, reconciliation, protection, positions, orders, balances or fills;
- credentials, private/authenticated APIs, signing, exchange account access or real-money behavior;
- persistence, database/RLS, feature stores, HA/fencing, deployment, infrastructure topology or production operations;
- checkpoint promotion, implementation authorization, production credentials, production deployment, limited-live or live trading;
- mutation of frozen requirements, source identities, existing checkpoint records, S1E ownership or PR #69 files;
- private/authenticated MEXC channels and any endpoint not in the official source lock;

## CAPABILITY CLASSIFICATION

`NECESSARY`:

- public unauthenticated realtime session ingest, provider-neutral session interface and V1 MEXC Futures public adapter;
- typed provider-neutral public market values and coherent value-state contracts;
- numeric determinism, validation and canonical serialization;
- immutable value fingerprints and complete source/generation/provenance lineage;
- ordered window/series manifests, interval/time-boundary semantics and late-correction versioning;
- S1E axis separation and restrictive validity matrix;
- deterministic tests, benchmark method and reproducible evidence;
- exact traceability, governance-only diff and negative-capability firewall.

`IMPORTANT`:

- public fixture/replay harness and separately gated integration smoke test using the locked MEXC source contract;
- operational tuning after the first `BASELINE_ESTABLISHMENT_V1` publication.

`FUTURE`:

- full analytical microstructure beyond raw order-book value contracts;
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

### Official MEXC public source lock

- URL: `https://mexcdevelop.github.io/apidocs/contract_v1_en/`;
- retrieved: `2026-09-13`;
- raw response SHA-256: `57ebc13fea788a1c568c8aeabfdf50acc0c9f5b5a882af4855837d53499940e`;
- protocol facts bound: `wss://contract.mexc.com/edge`, `ping`/`pong`, one-minute disconnect without ping, public `sub.tickers`, `sub.deal`, `sub.depth`, `sub.depth.full`, `sub.kline`, REST depth snapshot/version maintenance;
- evidence convention: raw URL response hash plus retrieval date is authoritative for protocol truth; deterministic CI uses pinned fixtures/fakes and does not make live network calls.

## ARCHITECTURE RULES

1. Module 4/5 owns normalized public market values and coherent Market-State; Module 7 owns quality. S1F cannot create a second truth source.
2. S1E `Market-State`, `MarketStateTrust`, `DataAuthority`, generation and provenance are read-only upstream inputs to later analytics. Values must remain tied to them without authority upgrades.
3. `LIVE`, `PAPER`, `SHADOW` and `REPLAY` are non-aliasing environment identities. Replay or fixtures cannot acquire live mutation capability.
4. Source/channel/contract/schema/version/generation/provenance are content-bearing identity, not UI metadata.
5. Unknown, invalid, warmup, stale, gap, sequence-unprovable, clock-untrusted and retired-generation cases fail closed and are observable.
6. A future feature engine consumes value/state contracts read-only and cannot mutate values, Market-State or authority.
7. Exact interval boundaries and point-in-time knowledge are mandatory; wall clock and sleeps are not substitutes for injected timestamps.
8. Public session ingest is NECESSARY, public-only and bounded by the locked MEXC contract; no private stream or live network is required by CI.

## CONSTRAINTS

- planning/governance-only diff: exactly one candidate document, two Work Orders and one pull-request-only workflow;
- exact canonical base and exact-head CI are mandatory;
- no product/runtime code, dependency lock, frozen-source rewrite, checkpoint edit or PR #69 mutation;
- only the official MEXC source lock may define adapter protocol facts; unsupported fields remain `UNSUPPORTED`/`UNKNOWN`;
- numeric policy is exactly `DECIMAL_TEXT_V1`, precision 38, scale 18, integer digits 20, no binary float, no raw rounding and no arbitrary quantization;
- benchmark mode and profiles are exactly `BASELINE_ESTABLISHMENT_V1`, `S1F-CONTRACT-MICRO-V1`, `S1F-NOMINAL-MULTICHANNEL-V1` and `S1F-STRESS-BACKPRESSURE-V1` as frozen below;
- no authorization is implied by planning freeze or by this candidate; implementation authorization and live trading authorization remain separate gates.

## ACCEPTANCE CRITERIA

1. B001 is closed at the contract level by a typed value plane that can support deterministic public analytics without a second truth source.
2. The complete value-kind manifest is explicit: `TradeTick`, `TickerState`, `CandleBar`, `OrderBookSnapshot`, `OrderBookDelta`, `BookLevel`, `ReferencePriceEvidence`, `FundingEvidence` and capability state.
3. Numeric policy is exactly `DECIMAL_TEXT_V1` with precision 38, scale 18, integer digits 20, base-10 no-exponent serialization and binary-float rejection.
4. Every value and every rolling/multi-timeframe input series has immutable fingerprint and complete ordered lineage; mutations and mixed identities fail closed.
5. UTC, Unix-epoch alignment, half-open `[start, end)`, `knowledge_time` admissibility, `OPEN`/`CLOSED` finality and immutable correction revisions are explicit.
6. The truth-validity matrix preserves `MarketStateTrust` versus `DataAuthority`, resource, eligibility and lifecycle axes, including `TRUSTED+RESOURCE_DEGRADED` and `TRUSTED+INELIGIBLE`.
7. `docs/06-test-benchmark-plan.md` is in the source lock and the benchmark method defines workload assumptions, deterministic procedure, evidence context and limitations.
8. Exact traceability covers source hierarchy, R05/R06/R07/R11 locators, decisions, ADR-0049, DoD and frozen baseline/change-control rules.
9. Negative tests prove no credentials, private APIs, trading, Risk/OMS/Execution, persistence, deployment, checkpoint or live authority.
10. Exact-head governance CI proves the four-file allowlist, base/CP0030 lock and planning-only boundary.

## TESTS AND BENCHMARK EVIDENCE

Required future tests include public session generation/reconnect/retirement, staged resubscription, retry/backoff/circuit and Module 29 admission; provider fixture schema validation/quarantine; exact Decimal parse/serialization/equality/fingerprint; float/NaN/Infinity/malformed/overflow/scale/invariant rejection; all value-family constructors and capability states; order-book snapshot/delta ordering, duplicate/gap/out-of-order/generation rollover/resync; half-open interval, UTC epoch, OPEN/CLOSED finality and immutable revisions; ordered lineage mutation properties; S1E axis matrix; LIVE/PAPER/SHADOW/REPLAY non-aliasing; negative capability; and deterministic benchmark fixtures.

Benchmark method must bind `docs/06-test-benchmark-plan.md` with `S1F_BENCHMARK_MODE=BASELINE_ESTABLISHMENT_V1`. Freeze these deterministic profiles: `S1F-CONTRACT-MICRO-V1` = 1 symbol, ticker 64/deal 256/depth 128/depth-full 32/kline 32, total 512 messages, depth 5, 60-second replay; `S1F-NOMINAL-MULTICHANNEL-V1` = 8 symbols, ticker 1024/deal 4096/depth 2048/depth-full 512/kline 512, total 8192 messages, depth 20, 900-second replay; `S1F-STRESS-BACKPRESSURE-V1` = 32 symbols, ticker 8192/deal 32768/depth 16384/depth-full 4096/kline 4096, total 65536 messages, depth 20, queue capacity 4096 and 3600-second replay. Mandatory measurements are normalization throughput, per-event/value-state update latency distribution, replay throughput, peak/steady memory and queue depth/age. Acceptance is correctness, bounded completion, no unbounded memory/queue growth and complete baseline publication; no product SLO is asserted. Evidence records code/build/dependency/runtime, fixture/config/policy versions, seed, hardware/environment, benchmark tool, raw artifact/hash and limitations. Future regression thresholds are proposals until a later governed decision/checkpoint. No uncontrolled live network is used in CI.

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
