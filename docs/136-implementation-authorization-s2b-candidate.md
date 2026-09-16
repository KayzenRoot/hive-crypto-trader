# HCT-IMPL-AUTH-0011 - S2B Candlestick Pattern Foundation Authorization Candidate

Status: `PENDING_INDEPENDENT_HIGH_ASSURANCE_REVIEW`
Risk: `HIGH_ASSURANCE`
Canonical base: `main@c198a99167fa571802b16f6daf77b253a2b100b0`
Current checkpoint: `HCT-CP-0034 / S2A_IMPLEMENTATION_APPROVED_MERGED`
Recompile marker: `DERIVED_FROM_POST_CP0034_MAIN`
Proposed authorization increment: `HCT-IMPL-AUTH-0011`
Proposed implementation slice: `HCT-IMP-0011-S2B`
Scope name: `Candlestick Pattern Foundation`
Authorization Issue: `#75`
Governance branch: `governance/HCT-IMPL-AUTH-0011-S2B`
Author-side governance preflight: `AUTHOR_SIDE_GOVERNANCE_PREFLIGHT_NOT_INDEPENDENT_APPROVAL`

This document is a governance-only authorization candidate. It does not implement
product/runtime code, authorize implementation, promote a checkpoint, grant credentials or
grant any live authority.

## Canonical traceability

`S2B_FROZEN_BASELINE=HCT-REQ-BASELINE-V1-CANDIDATE`

`S2B_PLANNING_FREEZE=HCT-CP-0014/PLANNING_FREEZE_APPROVED`

`S2B_DOD_SECTIONS=2,4,5,11`


The candidate is bound to the post-CP0034 canonical
`main@c198a99167fa571802b16f6daf77b253a2b100b0` and satisfies the active R12 frozen
requirements baseline `HCT-REQ-BASELINE-V1-CANDIDATE` recorded by
`docs/99-r12-frozen-requirements-baseline.md`, whose traceability and no-loss obligations are
recorded by `docs/100-r12-requirements-traceability-and-no-loss-proof.md` under the change
control of `docs/101-r12-freeze-governance-change-control-and-deferred-decisions.md`.

Governing sources and locators:

- `docs/00-source-hierarchy.md` — source hierarchy and precedence;
- `docs/03-scope.md` — product scope;
- `docs/04-architecture.md` — architectural ownership and boundaries;
- `docs/06-test-benchmark-plan.md` — test and benchmark plan;
- `docs/09-definition-of-done.md` sections `2`, `4`, `5` and `11`;
- `docs/10-decisions-ledger.md` — `HCT-DEC-0140`, `HCT-DEC-0141`;
- `docs/92-r11-v1-module-classification-and-integration-hardening.md` — Module `9`
  `Candlestick & Chart Pattern Engine` classified `V1_MINIMUM`;
- `REQ02::Trading intelligence requirements::B2` — candlestick-pattern and
  chart/market-structure analysis;
- `R11-REQ-012` typed identity/version registry, `R11-REQ-014` logical dependency DAG,
  `R11-REQ-015` explicit V1 module classification, `R11-REQ-023` formal-over-exploratory
  precedence.

The nine frozen requirement source blobs included by exact identity:
`292da9552ae816e4d51b8a299456305da1658e55`,
`f20c1ed00bdb13801aaff8a3b648371bfcffba58`,
`636ad01da9c25e760dd5e2f033b93a0f04578a17`,
`fea197e60532eb6ff3b11b628b9aabcbcfc00c41`,
`c8a426966c5a0dc34704d1413f506332e770c2c7`,
`c859c0c4a718e3017c34aa50013d4c50959853b4`,
`bc897ebd470857a53055bdee85128b5bd31a5822`,
`023187ef23b01d5a11f978bbfe6e38abf172bb3b`,
`6935e9973696d5b706546d63d847ea398780d936`.

Additional locked planning documents: `docs/00`, `docs/03`, `docs/04`, `docs/06`,
`docs/09`, `docs/10`, `docs/92`, `docs/99`, `docs/100`, `docs/101`, together with the
CP0034 completion checkpoint, the planning latest pointer and the S2A authorization and
approval records. Any drift in these identities requires STOP and fresh governance review.

## Dependency position

The frozen R11 Stage-2 order is
`features/indicators/patterns -> regime -> scanner -> strategy engine/catalog/signal ->
minimum microstructure`. `HCT-IMP-0009-S2A` completed the features/indicators half and is
recorded by `HCT-CP-0034`. Module 9 patterns are the next dependency.

- approved S2A implementation head: `40e67302fb80e329429be50430584ff9523a12a0`;
- governed S2A merge commit: `c862e5670465ef0f8d0c77dce163a1ece7c92ac4`;
- S2A independent review: `5220668487` / `APPROVED` / CRITICAL `0` / HIGH `0`;
- `HCT-CP-0034` status: `S2A_IMPLEMENTATION_APPROVED_MERGED`;
- `HCT-CP-0034` authority: `implementation_authorized=false`, empty scope,
  `NONE_PENDING_NEXT_GOVERNED_AUTHORIZATION`.

## Objective

Freeze exact candlestick pattern scope, candle equations, boundary semantics, Decimal
tolerance semantics, timeframe allowlist, ordered lineage, revision handling, match/validity
separation, authority-axis separation, rollback semantics, benchmark method and proof
obligations for the first bounded Module 9 slice, before any future implementation
authorization.

## Module 9 slice decomposition

`S2B_SLICE_NAME=Candlestick Pattern Foundation`

`S2B_CHART_STRUCTURE_DISPOSITION=REQUIRED_FOLLOW_ON_MODULE9_SLICE_BEFORE_REGIME`

Module 9 is delivered as two bounded sequential slices so that neither half named by
`docs/92` is silently deferred:

1. this slice — `HCT-IMP-0011-S2B`, the six deterministic candlestick patterns below;
2. a **required follow-on within Module 9** — a separately governed causal
   chart/market-structure minimum, not post-V1 and not skipped.

`HCT-DEC-0140` forbids silent scope deletion, which is why the chart/market-structure half
is carried forward rather than excluded. The follow-on slice is **not pre-authorized** and
no Work Order or implementation ID is fabricated for it here. The next Stage-2 dependency
after successful S2B completion is that separately governed causal chart/market-structure
minimum, and only after **both** Module 9 slices are complete may regime work be considered.
The frozen Stage-2 order is unchanged: both slices live inside the `patterns` position.

No-lookahead for the follow-on slice: causal pivot/structure evidence may be recognized only
after its confirmation bars are known. Delayed confirmation is not lookahead when
`event_time` and `knowledge_time` are honored; the follow-on slice must freeze that
confirmation contract itself.

## Shared candle primitives

`S2B_CANDLE_RANGE=high-low`

`S2B_CANDLE_BODY=abs(close-open)`

`S2B_CANDLE_BODY_RATIO=body/range`

`S2B_CANDLE_BULLISH=close>open`

`S2B_CANDLE_BEARISH=close<open`

`S2B_CANDLE_NEUTRAL=close==open`

`S2B_CANDLE_ZERO_RANGE=VALIDITY_UNKNOWN_MATCH_INDETERMINATE`

`S2B_SMALL_BODY_MAX=0.10`

`S2B_LONG_BODY_MIN=0.90`

`S2B_COMPARISON=DECIMAL_FEATURE_DECIMAL_V1_ONLY`

If `range == 0`, validity is `UNKNOWN` and the match state is `INDETERMINATE`; no division
by zero is performed and no default direction is assumed.

`S2B_TIMEFRAME_ALLOWLIST=Min1,Min5,Min15`

`S2B_TIMEFRAME_IDENTITY=Min1:60:1:UNIX_EPOCH_MULTIPLES;Min5:300:1:UNIX_EPOCH_MULTIPLES;Min15:900:1:UNIX_EPOCH_MULTIPLES`

`S2B_TIMEFRAME_IDENTITY_MATERIAL=TRUE`

The name list above is a human-readable marker only. The normative authorization is the
complete upstream `Timeframe` identity — name, `duration_seconds`, `version` and
`alignment`:

| Token | duration_seconds | version | alignment |
|---|---:|---:|---|
| `Min1` | `60` | `1` | `UNIX_EPOCH_MULTIPLES` |
| `Min5` | `300` | `1` | `UNIX_EPOCH_MULTIPLES` |
| `Min15` | `900` | `1` | `UNIX_EPOCH_MULTIPLES` |

The future implementation must compare the complete `Timeframe` identity or its canonical
fingerprint, never the name alone. A correct name with a wrong duration, a wrong name with a
correct duration, a wrong version, a non-canonical alignment, or a cross-timeframe
constituent mixture is rejected `INVALID`. The complete timeframe identity and version are
material in `PatternDefinition` and `PatternEvidence` fingerprints. Any future timeframe
version, duration or alignment expansion requires separate governed authorization and a
`PatternVersion` change.

## Exact pattern equations

`S2B_PATTERN_ALLOWLIST=P-DC-001,P-MB-001,P-EC-001,P-EC-002,P-MS-001,P-ES-001`

`S2B_PATTERN_COUNT=6`

`S2B_PATTERN_FAMILIES=SINGLE_BAR,TWO_BAR_REVERSAL,THREE_BAR_REVERSAL`

`S2B_PATTERN_DECIMAL_POLICY=FEATURE_DECIMAL_V1`

`S2B_PATTERN_BINARY_FLOAT=FORBIDDEN`

`P-DC-001` Doji — one CLOSED bar; `body_ratio <= 0.10`; direction `NEUTRAL`.

`P-MB-001` Marubozu — one CLOSED bar; `body_ratio >= 0.90`; direction `BULLISH` if
`close > open`, `BEARISH` if `close < open`.

`P-EC-001` Bullish Engulfing — previous `bearish`, current `bullish`,
`current.open <= previous.close`, `current.close >= previous.open`; inclusive bounds.

`P-EC-002` Bearish Engulfing — previous `bullish`, current `bearish`,
`current.open >= previous.close`, `current.close <= previous.open`; inclusive mirror.

`P-MS-001` Morning Star — bar1 `bearish` long-body (`>= 0.90`), bar2 small-body
(`<= 0.10`), bar3 `bullish` long-body (`>= 0.90`), `bar3.close >= midpoint(bar1.open,
bar1.close)`.

`P-ES-001` Evening Star — exact mirror: bar1 `bullish` long-body, bar2 small-body, bar3
`bearish` long-body, `bar3.close <= midpoint(bar1.open, bar1.close)`.

`S2B_MIDPOINT_EQUALITY=BOUNDS_INCLUSIVE`

`S2B_STAR_GAP_POLICY=NONE_IN_V1`

Any later change to thresholds, inequalities, gap policy, polarity, bar count, timeframe
allowlist or Decimal policy is behaviorally material and requires a `PatternVersion` change.

## FROZEN PACKAGE LOCK

`S2B_FROZEN_PACKAGE_COUNT=17`

The governance check locks the complete applicable freeze package at the canonical base, in
addition to the nine frozen requirement source blobs:

- `docs/00-source-hierarchy.md`, `docs/03-scope.md`, `docs/04-architecture.md`,
  `docs/05-security.md`, `docs/06-test-benchmark-plan.md`, `docs/09-definition-of-done.md`,
  `docs/10-decisions-ledger.md`;
- `docs/14-product-module-map.md` — the accepted planning module registry, which must keep
  Module `9` as `Candlestick & Chart Pattern Engine` and must not let an accepted module
  silently disappear;
- `docs/91-r11-integrated-authority-state-dependency-architecture.md` — Stage 2 keeps
  `features/indicators/patterns` before `regime` and preserves the restrictive-authority
  intersection semantics;
- `docs/99-r12-frozen-requirements-baseline.md`,
  `docs/100-r12-requirements-traceability-and-no-loss-proof.md`,
  `docs/101-r12-freeze-governance-change-control-and-deferred-decisions.md`,
  `docs/102-r12-freeze-acceptance-matrix.md`,
  `docs/103-r12-final-planning-freeze-audit.md`,
  `docs/105-r12-freeze-approval-and-checkpoint-promotion.md`;
- `docs/92-r11-v1-module-classification-and-integration-hardening.md`;
- `checkpoints/history/HCT-CP-0014.json` — `PLANNING_FREEZE_APPROVED` for `HCT-PLAN-0001-R12`.

Every blob identity is resolved from the canonical base with `git rev-parse :`; no identity
is guessed or carried stale. If the canonical freeze promotion package designates another
R12 artifact as frozen-critical, it is added rather than keeping an artificial fixed count,
and no existing lock is weakened.

## CANONICAL NON-REPLAY INPUT AND AUTHORITY SEAM

`S2B_AUTHORITY_SEAM=EVALUATOR_ISSUED_FEATURE_SAMPLE_FROM_CANDLE_AND_FEATURE_AUTHORITY_EVIDENCE`

`S2B_PER_CONSTITUENT_AUTHORITY=EXACTLY_ONE_INDEPENDENTLY_ATTESTED_BINDING_PER_CONSTITUENT`

`S2B_CONSTITUENT_CONTIGUITY=left.end==right.start`

`S2B_AXIS_FOLD=EXISTING_S2A_MOST_RESTRICTIVE`

`S2B_FIXTURE_SCOPE=REPLAY_ONLY`

S2A already solved point-in-time authority. Module 9 must not create a second, weaker
adapter for authoritative input. For `LIVE`, `PAPER` and `SHADOW` environments, every
candlestick constituent is consumed through the evaluator-issued S2A
`FeatureSample.from_candle(candle, market_state=..., resource=...)` and its
`FeatureAuthorityEvidence`, reusing that validation path exactly rather than re-implementing
it. Reusing `FeatureAuthorityEvidence` also means Module 9 references S2A ownership instead
of re-defining `DataAuthority` inside Module 9.

Raw `CandleBar` values combined with caller-supplied trust strings or caller-supplied hashes
are not authoritative Module 9 input and must be rejected. Public construction of
authoritative pattern input evidence from arbitrary values or fingerprints is forbidden.
`REPLAY` synthetic fixtures remain `REPLAY`-only and unmistakably synthetic, and synthetic
authority can never cross into `PAPER`, `LIVE` or `SHADOW`.

Per-constituent invariants:

- exactly one independently attested authority binding per constituent; one later
  `MarketStateSnapshot` cannot blanket earlier bars;
- identical `source_id`, `contract_id`, `environment`, `generation`, exact `Timeframe`
  identity/version and quantity contract where applicable;
- each non-fixture authority proves its exact originating event and its exact bound candle
  and value evidence;
- constituent windows strictly ordered, unique and contiguous with `left.end == right.start`;
- ordered constituent and authority fingerprints are material, so reorder, duplicate,
  correction or revision changes `PatternEvidence`;
- mismatched or retired generation fails closed.

Axis propagation keeps `MarketStateTrust`, `DataAuthority`, `ResourceRestriction` and
`UniverseLifecycleRestriction` separate. Each axis is folded across all constituents with the
existing S2A most-restrictive semantics, and no later constituent may upgrade an earlier
restrictive one. Pattern analytical validity remains separate from the resource and
lifecycle restrictions.

## EXPLICIT PAIRED CONSTITUENT CONTRACT

`S2B_CONSTITUENT_PAIR=EXACT_CANDLEBAR_PLUS_EVALUATOR_ISSUED_FEATURE_SAMPLE_FROM_SAME_CANDLE`

`S2B_PAIR_OPEN_SOURCE=CANDLEBAR_OPEN`

`S2B_PAIR_AUTHORITY_SOURCE=EVALUATOR_ISSUED_FEATURE_SAMPLE`

`S2B_PAIR_FINGERPRINT_EQUALITY=sample.fingerprint==candle.fingerprint`

`S2B_PAIR_OPEN_BINDING=CANDLEBAR_FINGERPRINT_COMMITS_OPEN`

The authority seam alone is not sufficient for pattern evaluation: the evaluator-issued S2A
`FeatureSample` deliberately carries `high`, `low`, `close`, quantity, timing and identity
evidence but does **not** carry `open`, while every one of the six frozen pattern equations
needs `open` directly or through `body = abs(close - open)`. Leaving that unreconciled would
force the implementation to invent where authoritative `open` comes from.

The frozen resolution is an explicit pair. Every non-REPLAY pattern constituent is the pair
of the original typed S1F `CandleBar` and the evaluator-issued S2A `FeatureSample` produced
from that **same** `CandleBar` through `FeatureSample.from_candle(...)`:

- the `CandleBar` supplies the authoritative OHLC, including `open`;
- the `FeatureSample` and its `FeatureAuthorityEvidence` supply the canonical point-in-time
  authority proof.

The evaluator must not accept an unpaired raw `CandleBar`, an unpaired `FeatureSample`,
caller-supplied trust strings, caller-supplied hashes, or a reconstructed synthetic `open`.
The exact name of a future runtime type is not pre-authorized; the semantics below are.

Exact cross-binding, required for every pair:

- `sample.fingerprint == candle.fingerprint`;
- `sample.source_id == candle.context.source_id`;
- `sample.contract_id == candle.context.contract_id`;
- `sample.environment == candle.context.environment`;
- `sample.generation_fingerprint == candle.context.generation.fingerprint`;
- `sample.timeframe.fingerprint == candle.timeframe.fingerprint`;
- `sample.interval_start == candle.start` and `sample.interval_end == candle.end`;
- `sample.closed == (candle.finality == CLOSED)`;
- `sample.high == candle.high`, `sample.low == candle.low`, `sample.close == candle.close`
  and `sample.quantity == candle.volume`;
- `sample.authority` is evaluator-issued and exact-event and exact-value-evidence bound
  under the existing S2A rules.

`open` is consumed only from the exact `CandleBar` whose fingerprint equals
`sample.fingerprint`. Because `CandleBar.fingerprint` commits `open` (alongside high, low,
close, volume, amount, timeframe, interval, finality, lineage, revision and predecessor), a
forged or mutated `open` necessarily breaks the pair and fails closed.

Ordered multi-bar windows apply the pair contract independently to every constituent, and
preserve the existing same source/contract/environment/generation/timeframe-version rules,
strict ordering, uniqueness and contiguity with `left.candle.end == right.candle.start`.
Ordered `CandleBar` fingerprints and ordered `FeatureSample`/authority fingerprints are
fingerprint material. A correction or revision requires a new `CandleBar` fingerprint, a new
S2A sample and authority binding, and new `PatternEvidence` and predecessor lineage.

## POINT-IN-TIME DERIVED TIMESTAMPS

`S2B_WINDOW_START=FIRST_ORDERED_CONSTITUENT_INTERVAL_START`

`S2B_WINDOW_END=FINAL_ORDERED_CONSTITUENT_INTERVAL_END`

`S2B_EVENT_TIME=MAX_CONSTITUENT_EVENT_TIME`

`S2B_KNOWLEDGE_TIME=MAX_CONSTITUENT_KNOWLEDGE_TIME`

`S2B_WALL_RECEIVE_TIME=MAX_CONSTITUENT_WALL_RECEIVE_TIME`

`S2B_PRE_BOUNDARY_RULE=MATCHED_FORBIDDEN_BEFORE_FINAL_CLOSED_BAR_AND_ALL_KNOWLEDGE_TIMES`

The `PatternEvidence` timestamps are deterministic functions of the exact ordered
constituents: `window_start` is the first ordered constituent `interval_start`/`start`,
`window_end` is the final ordered constituent `interval_end`/`end`, `event_time` is the
maximum constituent `event_time`, `knowledge_time` is the maximum constituent
`knowledge_time`, and `wall_receive_time` is the maximum constituent `wall_receive_time`.

The first observable evaluation boundary requires the final CLOSED bar **and** the
availability of every required constituent at its `knowledge_time`. Before both conditions
hold, `MATCHED` is forbidden. If any constituent `knowledge_time` is after the evaluation
boundary, the frozen `WARMUP` / `UNKNOWN` / `INVALID` semantics apply and `MATCHED` is never
emitted. Correction or revision creates new `PatternEvidence` and a new fingerprint;
historical evidence is not mutated.

## Match separation from evidence validity

`S2B_PATTERN_MATCH_STATE=MATCHED,NOT_MATCHED,INDETERMINATE`

`S2B_MATCH_VALIDITY_RULE=VALID_OR_DEGRADED_REQUIRES_MATCHED_OR_NOT_MATCHED`

`S2B_RESTRICTIVE_VALIDITY_RULE=WARMUP_UNKNOWN_INVALID_REQUIRES_INDETERMINATE`

`S2B_VALID_NON_MATCH=NOT_MATCHED_NEVER_UNKNOWN`

Input validity and whether the named pattern occurred are separate axes. `VALID` or
`DEGRADED` requires `MATCHED` or `NOT_MATCHED`; `WARMUP`, `UNKNOWN` or `INVALID` requires
`INDETERMINATE`. A normal, fully valid window that fails a pattern equation is
`NOT_MATCHED`, never `UNKNOWN`, and never indistinguishable from "the evaluator did not
run". `PatternEvidence` fingerprint material must include pattern ID/version, match state,
validity, direction/polarity, timeframe/version, exact ordered bar and evidence lineage,
event/knowledge/wall-receive times, generation and environment, revision/predecessor
lineage, thresholds and equality semantics, and all restrictive upstream axes. A downstream
consumer must never infer `MATCHED` from validity alone.

## No-lookahead and axis separation

`S2B_NO_LOOKAHEAD=STRICT_ONE_STEP_BEFORE_FORMATION_BOUNDARY_NOT_RECOGNIZED`

A pattern with bar cardinality `k` is recognized only at the CLOSE of its final bar. One
instant before that boundary the pattern must not be `MATCHED`; `WARMUP` is the only
admissible pre-boundary outcome and yields `INDETERMINATE`, and a stronger `INVALID` or
`UNKNOWN` condition dominates `WARMUP`.

`S2B_AXIS_SEPARATION=FeatureValidity;MarketStateTrust;DataAuthority;ResourceRestriction;UniverseLifecycleRestriction`

Structural pattern evidence stays separate from directional probability, expected return,
strategy suitability, ranking, signal and trade authorization. No downstream authority
upgrade is permitted.

## Rollback and recovery

S2B is derived analytical evidence only and owns no upstream truth. Rollback must be able to
disable or revert the S2B producer and registry and return consumers to S2A/S1F inputs
without mutating upstream S1E/S1F/S2A truth; historical `PatternEvidence` is append-only and
must never be rewritten or silently reinterpreted; reverting to an earlier `PatternVersion`
must leave later-version evidence attributable to that version; no migration, persistence or
storage authority is granted.

## Benchmark source lock

`S2B_BENCHMARK_MODE=S2B_BASELINE_ESTABLISHMENT_V1`

`S2B_BENCHMARK_PROFILES=MICRO,NOMINAL,STRESS`

Profiles, cardinality conventions and the correctness-before-performance rule are inherited
from `docs/06-test-benchmark-plan.md`
(`29401ce8fe1616f9390a317bae62d3a157addaa5`), following the S2A precedent that a profile's
correctness fails closed before any performance metric is considered.

## FROZEN BENCHMARK WORKLOAD AND METHOD

`S2B_BENCHMARK_MODE=S2B_BASELINE_ESTABLISHMENT_V1`

`S2B_BENCHMARK_FIXTURE_VERSION=S2B_PATTERN_FIXTURE_V1`

`S2B_BENCHMARK_SEED=0`

`S2B_BENCHMARK_TIMEFRAMES=Min1,Min5,Min15`

`S2B_BENCHMARK_PATTERNS=P-DC-001,P-MB-001,P-EC-001,P-EC-002,P-MS-001,P-ES-001`

`S2B_BENCHMARK_PROFILES=MICRO,NOMINAL,STRESS`

`S2B_BENCHMARK_PROFILE_MICRO=1:2048`

`S2B_BENCHMARK_PROFILE_NOMINAL=8:4096`

`S2B_BENCHMARK_PROFILE_STRESS=16:8192`

`S2B_BENCHMARK_RANDOMNESS=NONE`

`S2B_BENCHMARK_NETWORK=NONE`

Benchmark targets are not canonical until the workload assumptions and the benchmark
method are defined. This contract is normative; the profile names alone are not.
`S2B_BENCHMARK_PROFILE_<name>=<contracts>:<closed_pairs_per_contract_per_timeframe>`.

| Profile | Contracts | CLOSED pairs / contract / timeframe | Required content |
|---|---:|---:|---|
| `MICRO` | `1` | `2048` | all six patterns across `Min1`/`Min5`/`Min15`; deterministic valid and valid-non-match corpus |
| `NOMINAL` | `8` | `4096` | all six patterns across all three timeframes; positive, negative and boundary cases with deterministic restrictive-state counts |
| `STRESS` | `16` | `8192` | all six patterns and timeframes plus a deterministic adversarial corpus: late knowledge, correction/revision, mixed generation or environment, non-contiguous or reordered pairs, resource-degraded and lifecycle-restricted cases |

No uncontrolled wall-clock randomness and no network or provider dependency is permitted in
fixture generation or evaluation.

Measurements: pattern evaluations per second; `p50`/`p95`/`p99`/`max` evaluation latency
broken down by pattern family and timeframe; replay throughput; peak and steady memory;
active window-buffer depth; counts by `PatternValidity` and by `PatternMatchState`;
no-lookahead rejections; and a deterministic output-manifest SHA-256.

Each profile runs twice from the same fixture manifest and seed, and the deterministic
projection must be identical across both runs. Profile correctness is `PASS` only when every
expected match, non-match and indeterminate outcome, every pair and authority invariant,
every no-lookahead rule and every evidence fingerprint are correct and the mismatch count is
zero. A correctness failure makes the benchmark command and CI fail non-zero. Timing and
memory numbers are baseline evidence, not product SLOs. The benchmark records runtime,
dependency and build identity, hardware profile, fixture generator version, seed, profile
cardinalities and result hashes.

## FROZEN VERSION, DIRECTION AND FINGERPRINT SEMANTICS

`S2B_PATTERN_ALGORITHM_VERSION=S2B_STANDARD_CANDLESTICK_PATTERNS_V1`

`S2B_PATTERN_DEFINITION_VERSION=1`

`S2B_PATTERN_DIRECTIONS=BULLISH,BEARISH,NEUTRAL,NONE,UNKNOWN`

`S2B_FINGERPRINT_VERSION=S2B_SHA256_CANONICAL_JSON_V1`

`S2B_FINGERPRINT_SERIALIZATION=UTF8_JSON_ENSURE_ASCII_TRUE_SORT_KEYS_TRUE_SEPARATORS_COMMA_COLON`

Each of the six authorized canonical pattern IDs is definition version `1` under the
algorithm above. Any change to an equation, threshold, polarity, bar cardinality, gap policy,
timeframe, Decimal policy, direction or validity semantic requires a new `PatternVersion`.

`PatternDefinition`/`PatternVersion` identity binds algorithm version, pattern ID, definition
version, family, bar cardinality, exact equations, thresholds and equality semantics, Decimal
policy and the structural timeframe allowlist.

`PatternDirection=BULLISH,BEARISH,NEUTRAL,NONE,UNKNOWN` with exact semantics:

- `MATCHED` `P-DC-001` => `NEUTRAL`;
- `MATCHED` `P-MB-001` => `BULLISH` when `close > open`, `BEARISH` when `close < open`;
- `MATCHED` `P-EC-001` => `BULLISH`; `MATCHED` `P-EC-002` => `BEARISH`;
- `MATCHED` `P-MS-001` => `BULLISH`; `MATCHED` `P-ES-001` => `BEARISH`;
- `NOT_MATCHED` => `NONE` regardless of the candidate pattern ID;
- `INDETERMINATE` => `UNKNOWN`.

Direction is behaviorally material and fingerprint-visible. Fingerprints use
`S2B_SHA256_CANONICAL_JSON_V1`: canonical serialization as UTF-8 JSON with
`ensure_ascii=true`, `sort_keys=true`, comma/colon separators with no spaces, and no
non-finite or binary-float material. The `PatternEvidence` fingerprint binds fingerprint
version, `PatternDefinition` fingerprint, match state, direction, validity, every authority
and restriction axis, structural timeframe identity, exact ordered `CandleBar` fingerprints,
exact ordered `FeatureSample`/authority fingerprints, window, event, knowledge and
wall-receive times, generation, environment, source and contract, revision and predecessor
lineage, and the evaluation boundary. The fingerprint is recomputed from material and is
never accepted as caller truth.

## FROZEN VALIDITY FOLD PRECEDENCE

`S2B_VALIDITY_FOLD_PRECEDENCE=INVALID>UNKNOWN>WARMUP>DEGRADED>VALID`

`S2B_RESOURCE_LIFECYCLE_DO_NOT_DOWNGRADE=TRUE`

The fold is applied after pair validation and before match evaluation, and a stronger state
dominates every weaker state:

| Priority | `PatternValidity` | Normative condition |
|---:|---|---|
| 1 | `INVALID` | any structural or provenance contradiction: malformed pair, impossible OHLC, unsupported or wrong timeframe identity, duplicate, reorder, overlap or non-contiguous window, mixed source/contract/environment/generation, retired generation or contradictory lineage |
| 2 | `UNKNOWN` | no `INVALID`, but a required value, authority or state is unavailable, unprovable, stale or expired, `GAP`/`RESYNC_REQUIRED`/`SEQUENCE_UNPROVABLE`/`CLOCK_UNTRUSTED`, a zero-range primitive, or otherwise analytically unknowable at the evaluation boundary |
| 3 | `WARMUP` | no `INVALID` or `UNKNOWN`, but a required future constituent close or knowledge boundary has not occurred, or exact bar cardinality is not yet mature |
| 4 | `DEGRADED` | complete coherent computable analytical evidence exists, but at least one governed analytical truth or input is explicitly degraded |
| 5 | `VALID` | complete coherent admissible analytical evidence with no stronger condition |

`ResourceRestriction` and `UniverseLifecycleRestriction` remain separate axes and do not by
themselves downgrade otherwise `VALID` analytical pattern truth. `DataAuthority` and
`MarketStateTrust` remain separate but may make analytical evidence `UNKNOWN` or `INVALID`
only through governed truth and admissibility semantics, and no later constituent upgrades an
earlier restrictive state. Compatibility is unchanged: `VALID`/`DEGRADED` implies `MATCHED`
or `NOT_MATCHED`, while `WARMUP`/`UNKNOWN`/`INVALID` implies `INDETERMINATE`.

## EVALUATOR-ISSUED PATTERN EVIDENCE

`S2B_PATTERN_EVIDENCE_ISSUANCE=EVALUATOR_ISSUED_PRIVATE_ATTESTATION`

`S2B_PATTERN_EVIDENCE_FORGERY=FAIL_CLOSED`

Authoritative `PatternEvidence` is evaluator-issued through a private attestation
(`init=False` or equivalent) or, failing that, performs complete recomputation and content
validation strong enough that caller minting is impossible; evaluator-issued is preferred.
The evaluator receives one frozen `PatternDefinition`/`PatternVersion` plus the exact ordered
validated constituent pairs and the evaluation boundary, and it computes the validity fold,
match state, direction, timestamps, lineage, predecessor relation and fingerprint.

Callers may not directly choose `MATCHED`, `NOT_MATCHED`, `INDETERMINATE`, direction,
validity, event, knowledge or wall-receive time, window boundaries, constituent lineage,
definition fingerprint or evidence fingerprint. `dataclasses.replace` and copy-style mutation
of authoritative `PatternEvidence` must fail attestation or content validation. Direct
construction of plausible `MATCHED` evidence without evaluator attestation fails, and
tampered direction, timestamps, lineage, pattern version, pair order or fingerprint fails.
Correction or revision creates new evaluator-issued `PatternEvidence` with new predecessor
and fingerprint lineage, and historical evidence is immutable.

## Proof obligations

`S2B-PO-01` finite exact allowlist and version collision protection;

`S2B-PO-02` golden vectors for every pattern family containing positive, negative-valid,
boundary-equality, pre-close, zero-range, revision, cross-generation, cross-environment and
timeframe-rejection cases, including the exact one-step-before and exact-completion
boundaries;

`S2B-PO-03` no-lookahead tests using `event_time` and `knowledge_time`;

`S2B-PO-04` mutation tests for constituent correction, revision, reorder, missing bar,
changed timeframe, changed threshold/version, cross-generation and cross-environment input;

`S2B-PO-05` `WARMUP` / `UNKNOWN` / `INVALID` / `DEGRADED` semantics with separate resource
and lifecycle restrictions, and the `PatternMatchState` compatibility rule;

`S2B-PO-06` duplicate, overlap and conflict representation with deterministic ordering and
fingerprints;

`S2B-PO-07` replay determinism;

`S2B-PO-08` negative-capability scan;

`S2B-PO-09` bounded MICRO/NOMINAL/STRESS baseline with correctness failing closed first.

`S2B-PO-10` timing adversarial tests: identical OHLC with one later `knowledge_time` changes
derived evidence and fingerprint and blocks premature recognition; changed
`wall_receive_time` changes derived evidence and fingerprint where material; one instant
before the final close/knowledge boundary is not `MATCHED` while the exact boundary can
evaluate; non-contiguous and reordered bars are `INVALID`; cross-generation,
cross-environment, cross-timeframe and cross-version mixtures are `INVALID`; a revised
candle requires a new exact authority binding and a new predecessor/evidence lineage.

`S2B-PO-11` timeframe identity negative tests: correct full identity admitted; correct name
with wrong duration rejected; wrong name with correct duration rejected; wrong version
rejected; non-canonical alignment rejected; cross-timeframe constituent mixture rejected.

`S2B-PO-12` authority-seam tests: authoritative non-REPLAY constituents are admitted only
through the evaluator-issued S2A `FeatureSample.from_candle` and `FeatureAuthorityEvidence`;
one later snapshot cannot blanket earlier bars; raw candle plus caller-supplied trust strings
or hashes is rejected; `REPLAY` fixtures cannot cross into `PAPER`/`LIVE`/`SHADOW`.

`S2B-PO-13` paired-constituent adversarial tests: a valid `CandleBar` plus
`FeatureSample.from_candle` of that same candle passes; the same sample paired with a
different `CandleBar` fails; a `CandleBar` with a forged or mutated `open` while reusing the
sample fails by fingerprint mismatch; the same OHLC with only `open` changed fails; a
mismatched sample or candle source, contract, environment, generation, timeframe, interval,
finality or revision fails; an unpaired raw `CandleBar` fails in non-REPLAY; an unpaired
`FeatureSample` fails because `open` cannot be proven or consumed; caller-supplied authority
or an arbitrary fingerprint fails; `REPLAY` fixture pairing remains explicitly `REPLAY`-only;
cross-pair reorder, duplicate, non-contiguous window or mixed identity remains `INVALID`.

`S2B-PO-14` benchmark profile and method tests: exact MICRO/NOMINAL/STRESS cardinalities, all
timeframes and all six patterns present, per-run fixture manifest determinism, two-run
deterministic projection equality, and a fail-closed synthetic profile failure.

`S2B-PO-15` version, direction and fingerprint golden vectors, including
`NOT_MATCHED => NONE`, `INDETERMINATE => UNKNOWN` and recomputed canonical fingerprints.

`S2B-PO-16` validity-fold precedence matrix covering mixed simultaneous conditions:
`INVALID` dominates `UNKNOWN` and `WARMUP`, `UNKNOWN` dominates `WARMUP`, analytically
`VALID` plus resource-restrictive remains `VALID`, and analytically `VALID` plus
lifecycle-restrictive remains `VALID`.

`S2B-PO-17` PatternEvidence attestation and forgery tests: direct constructor, `replace` and
tamper, caller-selected match state, direction, times or fingerprint, and mismatched
definition or pair lineage are all rejected.
