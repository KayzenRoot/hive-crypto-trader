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
- `OrderBookSnapshot` and `OrderBookDelta` with ordered bid/ask `BookLevel(price, quantity)`, sequence/update evidence and snapshot/delta identity;
- `ReferencePriceEvidence` with typed kind `MARK`/`INDEX`/`FAIR` and `FundingEvidence` with rate/value, applicable time/boundary and provenance;
- explicit `SUPPORTED`/`UNSUPPORTED`/`UNKNOWN` capability state per family/channel. Raw order-book value contracts are necessary; full analytical microstructure remains future.

All value objects are immutable, typed, versioned and content-fingerprinted. Unsupported or absent fields are not synthesized.

### Numeric policy

Use exactly `Decimal` semantics parsed from source decimal text or exact integer-plus-scale material. `S1F_NUMERIC_POLICY_VERSION=DECIMAL_TEXT_V1`, `S1F_NUMERIC_MAX_PRECISION=38`, `S1F_NUMERIC_MAX_SCALE=18` and `S1F_NUMERIC_MAX_INTEGER_DIGITS=20` are frozen safety bounds; binary float input is rejected at authoritative constructors. Raw exchange values are never rounded to fit. Canonical cross-runtime serialization is base-10 decimal text with no exponent, no leading plus, canonical zero and semantically irrelevant trailing-zero removal; material scale is separately fingerprinted. NaN, positive/negative Infinity, malformed text, nonpositive prices, negative quantities, impossible OHLC, overflow and scale-limit violations fail with typed reason codes. No silent clipping, saturation or fallback zero. Raw quantization/rounding is forbidden unless a versioned policy names the increment and rule. Empty, undefined, insufficient-input and divide-by-zero results are `UNKNOWN`, `INVALID` or `WARMUP`, never fabricated `VALID`.

### Lineage and state

Bind each value to source ID, channel, contract, environment, generation, schema/version, provenance, origin event and value fingerprint. Market-State owns coherence; the value plane and downstream feature engine consume or publish read-only evidence according to module ownership. Rolling/multi-timeframe consumers receive an ordered manifest for every input value fingerprint or a deterministic Merkle/content manifest. Insert/delete/reorder/correction/generation/value changes must alter the manifest/fingerprint. Mixed source, contract, environment or generation fails closed unless a separately approved cross-source contract exists.

### Time and interval

Use UTC canonical timestamps. Standard fixed timeframes align to Unix epoch multiples of the duration unless an authoritative venue contract requires another alignment. Fixed bars use half-open `[start, end)` intervals: start inclusive, end exclusive. `event_time` is source market time; `wall_receive_time` is local UTC receive time; monotonic elapsed evidence measures age/latency; `knowledge_time` is the earliest point HCT had admissible evidence of the value/version. Point-in-time replay/admissibility uses `knowledge_time`, never future `event_time` alone. `CandleBar.finality` is `OPEN` or `CLOSED`; closed requires the interval boundary and source/finality evidence. Corrections create immutable revisions with predecessor/source lineage and new fingerprint. Open lower-timeframe bars cannot enter closed higher-timeframe windows; timeframe identity includes duration/alignment/version and mixed versions fail closed.

### Ingest boundary

Public unauthenticated realtime session ingest is `NECESSARY`. Implement one provider-neutral session/transport interface and the V1 concrete MEXC Futures public realtime adapter from the official source lock below. The native endpoint is `wss://contract.mexc.com/edge`; public intents are `sub.tickers`, `sub.ticker`, `sub.deal`, `sub.depth`, `sub.depth.full` and `sub.kline`; `ping` is sent on the locked 10-20 second policy and absence for one minute is a disconnect condition. Each connection/reconnection creates a generation; replacement retires the previous generation before publication. Use bounded retry budget, exponential backoff with bounded jitter, circuit state, deterministic staged resubscription and idempotent duplicate intent. Module 29 admission/backpressure gates normalized publication. Provider payloads are quarantined/schema-validated before canonical typed values; DTOs never become truth. Private/account/order/position/balance channels are forbidden. CI uses pinned fixtures/fakes and no uncontrolled live network.

## FROZEN S1F DECISION VALUES

`S1F_TRANSPORT_MODE=NECESSARY_PUBLIC_UNAUTHENTICATED`

`S1F_MEXC_WS_URL=wss://contract.mexc.com/edge`

`S1F_MEXC_PUBLIC_CHANNELS=sub.tickers,sub.ticker,sub.deal,sub.depth,sub.depth.full,sub.kline`

`S1F_SESSION_GENERATION=each connection/reconnection creates a generation; retired generations cannot publish`

`S1F_NUMERIC_TYPE=Decimal`; `S1F_NUMERIC_POLICY_VERSION=DECIMAL_TEXT_V1`; `S1F_NUMERIC_MAX_PRECISION=38`; `S1F_NUMERIC_MAX_SCALE=18`; `S1F_NUMERIC_MAX_INTEGER_DIGITS=20`

`S1F_FLOAT_INPUT=REJECTED`; `S1F_RAW_VALUES=exact; no raw rounding; no raw quantization`

`S1F_INTERVAL_MODEL=HALF_OPEN_START_INCLUSIVE_END_EXCLUSIVE`; `S1F_TIMEZONE=UTC`; `S1F_ALIGNMENT=UNIX_EPOCH_MULTIPLES`; `S1F_KNOWLEDGE_ADMISSIBILITY=knowledge_time`; `S1F_CANDLE_FINALITY=OPEN_UNTIL_BOUNDARY_AND_SOURCE_FINALITY`; `S1F_LATE_CORRECTION=NEW_IMMUTABLE_REVISION`

`S1F_VALUE_FAMILIES=TradeTick,TickerState,CandleBar,OrderBookSnapshot,OrderBookDelta,BookLevel,ReferencePriceEvidence,FundingEvidence`; `S1F_CAPABILITY_STATES=SUPPORTED,UNSUPPORTED,UNKNOWN`

`S1F_BENCHMARK_MODE=BASELINE_ESTABLISHMENT_V1`; `S1F_PROFILE_CONTRACT_MICRO_V1=symbols=1;ticker=64;deal=256;depth=128;depth-full=32;kline=32;total=512;depth-levels=5;replay-seconds=60`; `S1F_PROFILE_NOMINAL_MULTICHANNEL_V1=symbols=8;ticker=1024;deal=4096;depth=2048;depth-full=512;kline=512;total=8192;depth-levels=20;replay-seconds=900`; `S1F_PROFILE_STRESS_BACKPRESSURE_V1=symbols=32;ticker=8192;deal=32768;depth=16384;depth-full=4096;kline=4096;total=65536;depth-levels=20;queue-capacity=4096;replay-seconds=3600`

`S1F_BENCHMARK_MEASUREMENTS=normalization_throughput;value_state_latency_distribution;replay_throughput;peak_steady_memory;queue_depth_age`

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

Official MEXC source lock: `https://mexcdevelop.github.io/apidocs/contract_v1_en/`, retrieved `2026-09-13`, raw response SHA-256 `57ebc13fea788a1c568c8aeabfdf50acc0c9f5b5a882af4855837d53499940e`. Protocol facts are limited to the Native WS address `wss://contract.mexc.com/edge`; `ping`/`pong` and one-minute no-ping disconnect; public `sub.tickers`, `sub.ticker`, `sub.deal`, `sub.depth`, `sub.depth.full`, `sub.kline`; and REST depth snapshot/version maintenance. CI binds this URL/date/hash as provenance but uses deterministic pinned fixtures/fakes instead of live network.

## NORMALIZED MEXC SOURCE CONTRACT

`S1F_MEXC_SOURCE_CONTRACT_VERSION=S1F_MEXC_SOURCE_CONTRACT_V1`

This normalized contract is the implementation and audit source for the V1 public adapter. It is derived from the official sections `Native WS connection address`, `Detailed data interaction commands`, `Public Channels`, `Tickers`, `Ticker`, `Transaction`, `Depth`, `K-line`, `Funding rate`, `Index price`, `Fair price`, `How is depth information maintained`, `Market endpoints`, `Get the contract's depth information` and `Get a snapshot of the latest N depth information of the contract`. The URL, retrieval date and SHA-256 remain provenance; the hash alone is not claimed to reconstruct the mutable external page.

### Primary-source matrix

| Canonical family | Primary source | Required provider material and boundary |
| --- | --- | --- |
| `TradeTick` | WS `sub.deal` -> `push.deal` | `data.p` price; `data.v` volume; `data.T` direction; `data.t` transaction time; outer `symbol`; outer `ts`; `O` and `M` remain provider metadata unless separately mapped. |
| `TickerState` | WS `sub.ticker` -> `push.ticker` | `data.lastPrice`, `bid1`, `ask1`, `volume24`, `holdVol`, `indexPrice`, `fairPrice`, `fundingRate`, `timestamp`; outer `symbol`; outer `ts`. |
| Bulk ticker projection | WS `sub.tickers` -> `push.tickers` | `symbol`, `lastPrice`, `volume24`, `riseFallRate`, `fairPrice`, outer `ts`; partial capability only and not a substitute for `TickerState` bid/ask or funding fields. |
| `CandleBar` | WS `sub.kline` -> `push.kline` | `data.o`, `h`, `l`, `c`, `q`, `a`, `interval`, `t` window start, `symbol`; outer `ts`; `t` is seconds. |
| `OrderBookSnapshot` | REST `GET /api/v1/contract/depth/{symbol}` | `asks`, `bids`, `version`, `timestamp`; each V1 level must satisfy `[price, order_count, order_quantity]`. |
| `OrderBookDelta` | WS `sub.depth` -> `push.depth` with `compress=false` | `asks`, `bids`, `version`, outer `symbol`, outer `ts`; uncompressed incremental continuity is required. |
| Bounded full-depth projection | WS `sub.depth.full` -> `push.depth` | subscription limit exactly `5`, `10` or `20`; explicit subscription-context identity; same level shape as `push.depth`; never inferred as an incremental delta from channel name alone. |
| `ReferencePriceEvidence` | Primary: WS `sub.ticker` fields | `MARK` and `FAIR` use `data.fairPrice`; `INDEX` uses `data.indexPrice`; dedicated `sub.index.price` and `sub.fair.price` are `OPTIONAL_CORROBORATION` only. |
| `FundingEvidence` | Primary: WS `sub.ticker` field | `data.fundingRate` plus `data.timestamp`; dedicated `sub.funding.rate` is `OPTIONAL_CORROBORATION` only. |

`S1F_MEXC_PRIMARY_SOURCE_MATRIX=TradeTick:sub.deal;TickerState:sub.ticker;BulkTicker:sub.tickers;CandleBar:sub.kline;OrderBookSnapshot:REST:/api/v1/contract/depth/{symbol};OrderBookDelta:sub.depth:compress=false;FullDepth:sub.depth.full;ReferencePriceEvidence:sub.ticker;FundingEvidence:sub.ticker`

`S1F_MEXC_PUBLIC_CHANNELS=sub.tickers,sub.ticker,sub.deal,sub.depth,sub.depth.full,sub.kline`

`S1F_MEXC_TICKER_PRIMARY=WS sub.ticker -> push.ticker;data.lastPrice,bid1,ask1,volume24,holdVol,indexPrice,fairPrice,fundingRate,timestamp;outer.symbol,outer.ts`

`S1F_MEXC_REFERENCE_PRIMARY=WS sub.ticker;MARK=fairPrice;FAIR=fairPrice;INDEX=indexPrice;dedicated_channels=OPTIONAL_CORROBORATION`

`S1F_MEXC_FUNDING_PRIMARY=WS sub.ticker;fundingRate+timestamp;dedicated_channel=OPTIONAL_CORROBORATION`

`S1F_MEXC_NO_OTHER_PUBLIC_ENDPOINTS=GOVERNED_SOURCE_CONTRACT_CHANGE_REQUIRED`

Dedicated `sub.funding.rate`, `sub.index.price` and `sub.fair.price` are not required for V1 because `sub.ticker` is the declared primary source; if used later, they remain explicit `OPTIONAL_CORROBORATION` and never become hidden dependencies. No other public MEXC endpoint or channel is authorized by S1F unless added through a future governed source-contract change.

### Frozen provider field and unit semantics

`S1F_MEXC_WS_TS_UNIT=MILLISECONDS`

`S1F_MEXC_TICKER_TIMESTAMP_UNIT=MILLISECONDS`

`S1F_MEXC_KLINE_T_UNIT=SECONDS`

`S1F_MEXC_KLINE_T_MEANING=windowStart`

`S1F_MEXC_DEAL_T_UNIT=EPOCH_MILLISECONDS_STRICT_13_DIGIT_VALIDATOR`

`S1F_MEXC_DEAL_T_AUTODETECT=REJECTED`

Outer WS `ts` and `sub.ticker.data.timestamp` are provider timestamps in epoch milliseconds and must pass the same strict 13-digit epoch-millisecond validator. `sub.kline.data.t` is epoch seconds and is the interval window start. `sub.deal.data.t` is locked to epoch milliseconds for V1 because the official transaction example supplies the 13-digit value `1587442049632`; the parser must reject values outside the frozen millisecond validator and must never auto-detect seconds versus milliseconds. Every conversion rule is included in the MEXC decoder policy fingerprint. `knowledge_time` is local admissible receipt/validation time; `wall_receive_time` and monotonic receive evidence are local observations, not provider fields.

### Frozen depth and candle semantics

`S1F_MEXC_DEPTH_SNAPSHOT_REST=GET /api/v1/contract/depth/{symbol}`

`S1F_MEXC_DEPTH_RECOVERY_REST=GET /api/v1/contract/depth_commits/{symbol}/{limit}`

`S1F_MEXC_DEPTH_SUBSCRIPTION=method=sub.depth;compress=false`

`S1F_MEXC_DEPTH_TUPLE=price,order_count,order_quantity`

`S1F_MEXC_DEPTH_QUANTITY=third_element_order_quantity`

`S1F_MEXC_DEPTH_VERSION_RULE=next_version=previous_version+1;else=GAP_RESYNC_REQUIRED`

`S1F_MEXC_DEPTH_ZERO_QUANTITY=REMOVE_LEVEL`

`S1F_MEXC_FULL_DEPTH_LIMITS=5,10,20`

`S1F_MEXC_FULL_DEPTH_IDENTITY=subscription_context_required`

The third depth tuple element is canonical executable quantity; the second is `order_count` metadata and is never quantity. Incremental depth uses `compress=false`; a new event must be exactly the previous version plus one. A gap or discontinuity is `GAP_RESYNC_REQUIRED` and reinitializes from the documented REST recovery path. Quantity zero removes the price level. Full-depth updates use the same `push.depth` shape and require subscription-intent identity.

`S1F_MEXC_CANDLE_CLOSE_PROOF=NEXT_WINDOW_OR_REST_CONFIRMATION`

`S1F_MEXC_KLINE_FINAL_FLAG=ABSENT;DO_NOT_FABRICATE`

The MEXC kline payload has no explicit final/closed boolean. A bar remains `OPEN` while updates remain admissible. V1 `CLOSED` requires the interval boundary to have passed and either a later kline window for the same contract/interval/generation or deterministic post-boundary REST kline confirmation. Without that proof finality remains `OPEN`/`UNKNOWN`; late corrections create immutable revisions with `knowledge_time` and predecessor lineage.

### Parser and fixture reproducibility contract

`S1F_MEXC_DECIMAL_PARSE=LEXICAL_PROVIDER_TOKEN_TO_DECIMAL_NO_BINARY_FLOAT`

Provider JSON decimal tokens are parsed from lexical numeric text directly into `Decimal`; no JSON-number-to-binary-float intermediate is permitted. Unknown extra fields may remain in quarantine/provenance but cannot alter canonical fingerprints until a governed schema version authorizes them. Missing required fields produce typed `UNSUPPORTED`, `UNKNOWN` or `INVALID` outcomes according to capability/schema policy, never default zero.

`S1F_MEXC_FIXTURE_MANIFEST=source_url;retrieved;source_sha256;normalized_schema_version;fixture_hashes`

Future S1F implementation must commit deterministic provider fixture payloads derived from this normalized schema and a provider-source evidence manifest containing the official source URL, retrieval date, source SHA-256, `S1F_MEXC_SOURCE_CONTRACT_VERSION` and every fixture hash. CI uses pinned fixtures/fakes and no uncontrolled live network. A payload incompatible with this contract is quarantined/fail-closed and requires a governed source-contract change; opportunistic parser expansion is forbidden.

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
7. Public session ingest is NECESSARY, public-only and bounded by the official MEXC lock; generation retirement, reconnect/backoff/circuit and Module 29 admission are part of the S1F boundary.

## CONSTRAINTS

- implement only after a new authorization checkpoint explicitly grants S1F;
- preserve exact frozen source identities and CP0030 history; no force/reset/rewrite or unrelated cleanup;
- exact numeric policy is `DECIMAL_TEXT_V1` with Decimal precision 38, scale 18 and integer digits 20; no binary float, raw rounding or arbitrary raw quantization;
- no provider protocol fact may be used outside the official MEXC source lock; provider DTOs remain quarantined;
- tests and benchmark evidence must be deterministic and reproducible; no uncontrolled live network in CI;
- no code path may create implementation, production, deployment, limited-live or live-trading authority implicitly.

## ACCEPTANCE CRITERIA

1. A typed `TradeTick`/`TickerState`/`CandleBar`/order-book/reference/funding plane and NECESSARY public MEXC session ingest are available to read-only consumers, with explicit capability state.
2. Numeric semantics are exactly `DECIMAL_TEXT_V1`, finite, invariant-checked and deterministic across supported runtimes.
3. Immutable value fingerprints include canonical numeric fields and all material identity; ordered window lineage detects every material mutation.
4. UTC Unix-epoch alignment, half-open `[start, end)`, `knowledge_time` admissibility, OPEN/CLOSED finality and immutable correction semantics are explicit and tested.
5. S1E trust/DataAuthority/resource/eligibility/lifecycle axes are preserved without authority upgrades or truth falsification.
6. Public transport is the locked unauthenticated MEXC adapter, bound to quota/backpressure/generation/quality and proven with fixtures/fakes.
7. Tests cover session generation/reconnect/retirement, quarantine, exact numeric failure states, all families, order-book ordering/resync, lineage, time, S1E matrix, replay and negative firewall.
8. Benchmark method binds `docs/06-test-benchmark-plan.md`, `BASELINE_ESTABLISHMENT_V1`, the exact three profiles/counts and mandatory throughput/latency/replay/memory/queue measurements below.
9. Exact traceability and independent HIGH_ASSURANCE review are complete before checkpoint consideration.

## TESTS

Test public session generation/reconnect/retirement, staged resubscription, bounded retry/backoff/circuit and Module 29 admission; provider fixture schema validation/quarantine; exact Decimal parse/serialization/equality/fingerprint; reject binary float, NaN, Infinity, malformed, overflow/scale violation and negative/impossible invariants; Trade/Ticker/Candle/Book/ReferencePrice/Funding type constructors and capability state; order-book snapshot/delta ordering, duplicate/gap/out-of-order/generation rollover/resync; half-open interval, UTC epoch alignment, OPEN/CLOSED finality and late immutable revisions; ordered lineage mutations; S1E axis matrix; LIVE/PAPER/SHADOW/REPLAY non-aliasing; negative scanner; and deterministic benchmark fixtures.

## BENCHMARK AND EVIDENCE

Freeze `S1F_BENCHMARK_MODE=BASELINE_ESTABLISHMENT_V1`: `S1F-CONTRACT-MICRO-V1` = 1 symbol, ticker 64/deal 256/depth 128/depth-full 32/kline 32, total 512, depth 5, 60-second replay; `S1F-NOMINAL-MULTICHANNEL-V1` = 8 symbols, ticker 1024/deal 4096/depth 2048/depth-full 512/kline 512, total 8192, depth 20, 900-second replay; `S1F-STRESS-BACKPRESSURE-V1` = 32 symbols, ticker 8192/deal 32768/depth 16384/depth-full 4096/kline 4096, total 65536, depth 20, queue capacity 4096, 3600-second replay. Declare the locked public channels, fixture configuration, seed, code/build/dependency/runtime, hardware/environment, tool version and hashes. Mandatory measurements are normalization throughput, per-event/value-state update latency distribution, replay throughput, peak/steady memory and queue depth/age. Acceptance is correctness, bounded completion, no unbounded memory/queue growth and complete baseline publication, with no product SLO. Evidence records raw artifact/hash and limitations; future regression thresholds are proposals until later governance. No uncontrolled live network is used in CI.

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
