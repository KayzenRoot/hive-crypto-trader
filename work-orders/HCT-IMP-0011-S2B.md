# HCT-IMP-0011-S2B — S2B Candlestick Pattern Foundation

Status: `PENDING_SEPARATE_AUTHORIZATION_CHECKPOINT`
Risk: `HIGH_ASSURANCE`
Canonical base: `main@c198a99167fa571802b16f6daf77b253a2b100b0`
Current checkpoint: `HCT-CP-0034 / S2A_IMPLEMENTATION_APPROVED_MERGED`
Proposed implementation: `HCT-IMP-0011-S2B`
Proposed authorization: `HCT-IMPL-AUTH-0011`
Scope name: `Candlestick Pattern Foundation`
Governance branch: `governance/HCT-IMPL-AUTH-0011-S2B`
Author-side governance preflight: `AUTHOR_SIDE_GOVERNANCE_PREFLIGHT_NOT_INDEPENDENT_APPROVAL`

This Work Order is a frozen scope contract for a **future** bounded implementation. It
authorizes nothing today: `HCT-CP-0034` leaves `implementation_authorized=false`. The Work
Order is non-executable until its separate authorization checkpoint is promoted and a fresh
post-checkpoint Context Lock is captured against the exact post-checkpoint canonical main.

Fresh independent HIGH_ASSURANCE review is required at two different phases and they are not
interchangeable: the exact **authorization** head must be independently approved before the
authorization merge, and the exact **implementation** head must be independently approved
before the implementation merge. The implementation-head review follows implementation
execution and its exact-head CI and Evidence Bundle; it is never a precondition of
implementation executability, because no implementation head can exist before implementation
is executed.

## GOVERNED EXECUTION LIFECYCLE

`S2B_AUTHORIZATION_REVIEW_GATE=EXACT_AUTHORIZATION_HEAD_INDEPENDENT_APPROVAL_BEFORE_AUTHORIZATION_MERGE`

`S2B_AUTHORIZATION_CHECKPOINT_GATE=SEPARATE_CHECKPOINT_AUTHORIZES_HCT-IMP-0011-S2B_ONLY`

`S2B_IMPLEMENTATION_EXECUTABLE_AFTER=AUTHORIZED_CHECKPOINT_AND_FRESH_POST_CHECKPOINT_CONTEXT_LOCK`

`S2B_IMPLEMENTATION_STOP=OPEN_UNMERGED_AFTER_EXACT_HEAD_CI_AND_COMPLETE_EVIDENCE_BUNDLE`

`S2B_IMPLEMENTATION_REVIEW_GATE=EXACT_IMPLEMENTATION_HEAD_INDEPENDENT_APPROVAL_BEFORE_IMPLEMENTATION_MERGE`

`S2B_NO_PREIMPLEMENTATION_IMPLEMENTATION_HEAD_REVIEW=TRUE`

The governed order is fixed:

1. governance candidate review — an independent HIGH_ASSURANCE review accepts the exact
   authorization head;
2. authorization — expected-head merge of the governance PR, followed by a separate
   authorization checkpoint for `HCT-IMP-0011-S2B` only;
3. executability — this Work Order becomes executable after that authorization checkpoint and
   a fresh post-checkpoint Context Lock;
4. implementation — only `HCT-IMP-0011-S2B` is implemented, producing exact-head CI and the
   Evidence Bundle;
5. implementation review — stop with the implementation PR OPEN and UNMERGED, then an
   independent HIGH_ASSURANCE review accepts the exact implementation head before any
   implementation merge.

The authorization checkpoint identifier is assigned by the later authorization/promotion step
only after the authorization PR is independently approved. It is deliberately not fabricated
here, no implementation Issue is created and no implementation checkpoint is promoted by this
document.

## OBJECTIVE

Freeze the first of the two bounded Module 9 `V1_MINIMUM` slices: a deterministic,
provider-neutral, point-in-time **Candlestick Pattern Foundation** for public/standard
candlestick patterns. Module 9 is a **consumer** of S2A feature/indicator evidence and of
read-only S1E/S1F market truth. It is not a second feature engine, not a Market-State
owner, not a DataAuthority owner, not a strategy engine and not a signal engine.

## CANONICAL TRACEABILITY

`S2B_FROZEN_BASELINE=HCT-REQ-BASELINE-V1-CANDIDATE`

`S2B_PLANNING_FREEZE=HCT-CP-0014/PLANNING_FREEZE_APPROVED`

`S2B_DOD_SECTIONS=2,4,5,11`


This Work Order is derived from, and must satisfy, the following canonical sources:

- `docs/00-source-hierarchy.md` — source hierarchy and precedence;
- `docs/99-r12-frozen-requirements-baseline.md` — the active frozen requirements baseline
  `HCT-REQ-BASELINE-V1-CANDIDATE` and the exact nine frozen requirement source blobs;
- `docs/100-r12-requirements-traceability-and-no-loss-proof.md` — traceability and
  no-loss proof obligations;
- `docs/101-r12-freeze-governance-change-control-and-deferred-decisions.md` — freeze
  governance, change control and deferred decisions;
- `docs/03-scope.md` — product scope;
- `docs/04-architecture.md` — architectural ownership and module boundaries;
- `docs/06-test-benchmark-plan.md` — test and benchmark plan;
- `docs/09-definition-of-done.md` — sections `2` (planning increment), `4`
  (implementation increment), `5` (test and benchmark evidence) and `11`
  (documentation and checkpoint);
- `docs/10-decisions-ledger.md` — `HCT-DEC-0140` (42-module classification without silent
  scope deletion) and `HCT-DEC-0141` (formal-round contracts override conflicting
  exploratory wording; R12 consolidates requirements losslessly);
- `docs/92-r11-v1-module-classification-and-integration-hardening.md` — Module `9`
  `Candlestick & Chart Pattern Engine` classified `V1_MINIMUM`.

The nine frozen requirement source blobs are included by exact identity:

| Requirement source | Frozen blob |
|---|---|
| `docs/02-requirements.md` | `292da9552ae816e4d51b8a299456305da1658e55` |
| `docs/48-r04-execution-requirements-addendum.md` | `f20c1ed00bdb13801aaff8a3b648371bfcffba58` |
| `docs/54-r05-realtime-requirements-addendum.md` | `636ad01da9c25e760dd5e2f033b93a0f04578a17` |
| `docs/61-r06-intelligence-requirements-addendum.md` | `fea197e60532eb6ff3b11b628b9aabcbcfc00c41` |
| `docs/67-r07-validation-laboratory-requirements-addendum.md` | `c8a426966c5a0dc34704d1413f506332e770c2c7` |
| `docs/73-r08-multitenant-security-requirements-addendum.md` | `c859c0c4a718e3017c34aa50013d4c50959853b4` |
| `docs/80-r09-cockpit-uiux-requirements-addendum.md` | `bc897ebd470857a53055bdee85128b5bd31a5822` |
| `docs/87-r10-observability-audit-incident-finops-requirements-addendum.md` | `023187ef23b01d5a11f978bbfe6e38abf172bb3b` |
| `docs/93-r11-integration-requirements-addendum.md` | `6935e9973696d5b706546d63d847ea398780d936` |

Governing semantics identified for this slice:

- `REQ02::Trading intelligence requirements::B2` — candlestick-pattern and
  chart/market-structure analysis;
- `R11-REQ-012` — typed identity/version registry;
- `R11-REQ-014` — logical dependency DAG;
- `R11-REQ-015` — explicit V1 module classification;
- `R11-REQ-023` — formal-over-exploratory precedence;
- `HCT-DEC-0140` — 42-module classification without silent scope deletion;
- `HCT-DEC-0141` — formal precedence and lossless R12 consolidation.

Module `9` remains classified `V1_MINIMUM`. `HCT-DEC-0140` forbids silent scope deletion,
which is why the chart/market-structure half of Module 9 is carried forward as a required
follow-on slice rather than dropped.

## MODULE 9 SLICE DECOMPOSITION

`S2B_SLICE_NAME=Candlestick Pattern Foundation`

Module 9 is delivered as two bounded sequential slices so that neither half is silently
deferred or deleted:

1. **this slice** — `HCT-IMP-0011-S2B`, the six deterministic candlestick patterns below;
2. **required follow-on** — a separately governed causal chart/market-structure minimum.

`S2B_CHART_STRUCTURE_DISPOSITION=REQUIRED_FOLLOW_ON_MODULE9_SLICE_BEFORE_REGIME`

The chart/market-structure slice is a **required follow-on within Module 9**, not post-V1
and not skipped. It is **not pre-authorized** and no Work Order or implementation ID is
fabricated for it here. The next Stage-2 dependency after successful S2B completion is that
separately governed causal chart/market-structure minimum, and only after **both** Module 9
slices are complete may regime work be considered. The frozen Stage-2 order
`features/indicators/patterns -> regime -> scanner -> strategy engine/catalog/signal ->
minimum microstructure` is preserved unchanged: both Module 9 slices live inside the
`patterns` position.

No-lookahead for the follow-on slice: causal pivot/structure evidence may be recognized
only **after** its confirmation bars are known. Delayed confirmation is not lookahead when
`event_time` and `knowledge_time` are honored. The follow-on slice must freeze that
confirmation contract itself; it is not frozen here.

## FROZEN SCOPE — SHARED CANDLE PRIMITIVES

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

If `range == 0`, the bar's pattern evidence validity is `UNKNOWN` and the match state is
`INDETERMINATE`; no division by zero is performed and no default direction is assumed.

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

## FROZEN SCOPE — EXACT PATTERN EQUATIONS

`S2B_PATTERN_ALLOWLIST=P-DC-001,P-MB-001,P-EC-001,P-EC-002,P-MS-001,P-ES-001`

`S2B_PATTERN_COUNT=6`

`S2B_PATTERN_FAMILIES=SINGLE_BAR,TWO_BAR_REVERSAL,THREE_BAR_REVERSAL`

`S2B_PATTERN_DECIMAL_POLICY=FEATURE_DECIMAL_V1`

`S2B_PATTERN_BINARY_FLOAT=FORBIDDEN`

**`P-DC-001` Doji** — one CLOSED bar; `body_ratio <= 0.10`; direction `NEUTRAL`.

**`P-MB-001` Marubozu** — one CLOSED bar; `body_ratio >= 0.90`; direction `BULLISH` if
`close > open`, `BEARISH` if `close < open`.

**`P-EC-001` Bullish Engulfing** — two CLOSED bars; previous bar `bearish`, current bar
`bullish`, `current.open <= previous.close`, `current.close >= previous.open`; inclusive
body bounds.

**`P-EC-002` Bearish Engulfing** — two CLOSED bars; previous bar `bullish`, current bar
`bearish`, `current.open >= previous.close`, `current.close <= previous.open`; inclusive
mirror of `P-EC-001`.

**`P-MS-001` Morning Star** — three CLOSED bars; bar1 `bearish` and long-body
(`body_ratio >= 0.90`), bar2 small-body (`body_ratio <= 0.10`), bar3 `bullish` and long-body
(`body_ratio >= 0.90`), and `bar3.close >= midpoint(bar1.open, bar1.close)`.

**`P-ES-001` Evening Star** — exact mirror of `P-MS-001`: bar1 `bullish` and long-body,
bar2 small-body, bar3 `bearish` and long-body, and
`bar3.close <= midpoint(bar1.open, bar1.close)`.

`S2B_MIDPOINT_EQUALITY=BOUNDS_INCLUSIVE`

`S2B_STAR_GAP_POLICY=NONE_IN_V1`

The star midpoint comparison is inclusive (`>=` for the morning star, `<=` for the evening
star) and the midpoint value is fingerprint-bound. `V1` imposes no gap requirement between
the three star bars; gap semantics, if ever required, are a later `PatternVersion` change.

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

## PATTERN MATCH SEPARATION FROM EVIDENCE VALIDITY

`S2B_PATTERN_MATCH_STATE=MATCHED,NOT_MATCHED,INDETERMINATE`

`S2B_MATCH_VALIDITY_RULE=VALID_OR_DEGRADED_REQUIRES_MATCHED_OR_NOT_MATCHED`

`S2B_RESTRICTIVE_VALIDITY_RULE=WARMUP_UNKNOWN_INVALID_REQUIRES_INDETERMINATE`

`S2B_VALID_NON_MATCH=NOT_MATCHED_NEVER_UNKNOWN`

Input/evidence validity and whether the named pattern actually occurred are separate axes.
If evidence validity is `VALID` or `DEGRADED`, `match_state` MUST be `MATCHED` or
`NOT_MATCHED`. If validity is `WARMUP`, `UNKNOWN` or `INVALID`, `match_state` MUST be
`INDETERMINATE`. A normal, fully valid window that fails a pattern equation is
`NOT_MATCHED`, never `UNKNOWN`, and never indistinguishable from "the evaluator did not
run". A downstream consumer must never infer `MATCHED` from validity alone.

## FROZEN IDENTITIES AND EVIDENCE

- immutable `PatternDefinition` and `PatternVersion` with material fingerprints covering
  pattern ID, version, family, bar cardinality, exact source fields, timeframe and version
  allowlist, threshold and equality semantics, midpoint and gap policy, formation and
  completion boundary rule, `FEATURE_DECIMAL_V1` policy version and rounding mode;
- immutable `PatternEvidence` bound to source, contract, environment, generation,
  timeframe/version, ordered constituent lineage, event time, knowledge time, wall-receive
  time, window boundaries, revision/predecessor lineage, validity state, match state and the
  exact consumed upstream evidence fingerprints;
- explicit `VALID`, `UNKNOWN`, `INVALID`, `WARMUP` and `DEGRADED` outcomes with the separate
  match axis above and the separate resource/lifecycle restriction axes preserved;
- corrections and revisions create new evidence and new fingerprints; historical evidence is
  never silently mutated.

`P-DC-001`, `P-MB-001`, `P-EC-001`, `P-EC-002`, `P-MS-001` and `P-ES-001` are the only
authorized pattern IDs. Exceeding this set requires a new governed authorization.

## NO-LOOKAHEAD CONTRACT

`S2B_NO_LOOKAHEAD=STRICT_ONE_STEP_BEFORE_FORMATION_BOUNDARY_NOT_RECOGNIZED`

A pattern with bar cardinality `k` may be recognized only at the CLOSE of its final bar
`t`. One instant before that boundary — while `t` is not yet a CLOSED bar, or while the
`knowledge_time` of any constituent exceeds the evaluation boundary — the pattern must not
be reported as `MATCHED`. `WARMUP` is the only admissible pre-boundary outcome and yields
`INDETERMINATE`, and an objectively known stronger `INVALID` or `UNKNOWN` condition
dominates `WARMUP`.

## AXIS SEPARATION

`S2B_AXIS_SEPARATION=PatternValidity;MarketStateTrust;DataAuthority;ResourceRestriction;UniverseLifecycleRestriction`

Structural pattern evidence stays separate from directional probability, expected return,
strategy suitability, ranking, signal and trade authorization. Module 9 may not upgrade
`MarketStateTrust`, `DataAuthority`, resource restriction or lifecycle restriction, and it
inherits the S2A restriction axes without reinterpreting them.

## ROLLBACK AND RECOVERY SEMANTICS

S2B is derived analytical evidence only and owns no upstream truth. For the future
implementation:

- rollback must be able to disable or revert the S2B producer and its
  `PatternDefinition`/`PatternVersion` registry and return consumers to S2A/S1F inputs
  without mutating upstream S1E, S1F or S2A truth;
- historical `PatternEvidence` is append-only: rollback must never rewrite, delete or
  silently reinterpret previously emitted evidence or its fingerprints;
- recovering to an earlier `PatternVersion` must leave the later version's evidence
  attributable to that later version;
- no migration, persistence, database or storage authority is granted by this slice;
- disabling S2B must not require any change to frozen requirements or upstream contracts.

## OUT OF SCOPE

No runtime/product implementation is authorized by this Work Order as written. No network
transport, provider endpoint, socket/WebSocket/HTTP client, credential, private API, request
signing, persistence, database/RLS, feature store, deployment, limited-live or live trading.
Also excluded: the Module 9 chart/market-structure follow-on slice itself, Module 10
proprietary indicator R&D, regime classification, scanner/ranking, strategy/catalog/signal,
microstructure, Brain, agents, RAG/memory, learning, calibration, Risk, Safety, Session
Policy, position sizing, leverage, OMS, Execution, reconciliation, protection, orders,
positions, balances and fills. An unbounded internet pattern catalog is explicitly not
authorized.

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

## LOCAL VALIDITY AXIS, CANONICAL BOUNDARY AND IDEMPOTENT EVIDENCE

`S2B_LOCAL_VALIDITY_AXIS=PatternValidity`

`S2B_UPSTREAM_FEATURE_VALIDITY=READ_ONLY_NEVER_SUBSTITUTES`

`S2B_CANONICAL_EVALUATION_BOUNDARY=max(window_end,knowledge_time)`

`S2B_BOUNDARY_STORED=CANONICAL_NEVER_CALL_TIME`

`S2B_WALL_RECEIVE_SUBSTITUTION=FORBIDDEN`

`S2B_LATER_REEVALUATION=IDEMPOTENT_SAME_FINGERPRINT`

`S2B_PATTERN_EVIDENCE_KEY=pattern_id;definition_version;source_id;contract_id;environment;generation;timeframe_fingerprint;window_start;window_end;ordered_constituent_candle_fingerprints`

`S2B_EVIDENCE_DUPLICATE_SUPPRESSION=NONE_IDEMPOTENT_BY_KEY`

`S2B_EVIDENCE_CONFLICT_POLICY=INDEPENDENT_NO_WINNER_NO_RANKING`

`S2B_EVIDENCE_ORDER=timeframe_duration_asc;window_end_asc;pattern_id_asc;definition_version_asc;evidence_fingerprint_asc`

`S2B_EVIDENCE_ORDER_AUTHORITY=NONE_SEQUENCE_DETERMINISM_ONLY`

`S2B_PREDECESSOR_SCOPE=same_pattern_id;definition_version;source;contract;environment;timeframe;window_start;window_end`

`S2B_PREDECESSOR_NONE_ONLY_WHEN_NO_EARLIER_EVIDENCE=TRUE`

`S2B_REVISION_CHAIN=NO_SKIP_NO_FORK_NO_OVERWRITE`

Module 9 owns a **local** analytical validity axis. `PatternValidity` owns `VALID`,
`DEGRADED`, `WARMUP`, `UNKNOWN` and `INVALID` for `PatternEvidence`, and the shared axis
marker names it accordingly. Upstream `FeatureValidity` remains a read-only S2A concept: if
Module 9 ever consumes it, it never substitutes for `PatternValidity`.
`ResourceRestriction` and `UniverseLifecycleRestriction` stay separate axes and do not by
themselves downgrade otherwise `VALID` `PatternValidity`. `MarketStateTrust` and
`DataAuthority` stay upstream restrictive axes that Module 9 may propagate but never
upgrade.

The canonical evaluation boundary is `max(window_end, knowledge_time)`, where `window_end` is
the final ordered constituent `interval_end` and `knowledge_time` is the maximum constituent
`knowledge_time` under the frozen H006 derivation. A supplied boundary earlier than canonical
cannot emit `MATCHED` or `NOT_MATCHED` and follows the frozen restrictive semantics. A
supplied boundary at or after canonical may evaluate, but `PatternEvidence` stores and
fingerprints the **canonical** boundary, never an arbitrary later call time.
`wall_receive_time` remains evidence material but is never substituted for the knowledge-time
admissibility boundary. The same definition over the same ordered pairs with the same
revision lineage, evaluated later without new evidence, returns the same `PatternEvidence`
fingerprint and must not mint a duplicate.

`S2B_PATTERN_EVIDENCE_KEY` is the canonical evidence identity: repeated evaluation of an
unchanged key and material is idempotent and yields one canonical evidence identity and
fingerprint with no duplicate emission.

Overlap and conflict semantics: different pattern IDs may `MATCH` on the same window and are
retained independently with no winner, suppression, score, ranking or trade preference;
overlapping windows across adjacent closes are independent by distinct window identity;
`NOT_MATCHED` for one pattern never suppresses `MATCHED` for another; bullish and bearish
structural evidence may coexist and Module 9 does not resolve it into a directional decision.

Deterministic order for evidence at the same canonical boundary is
`timeframe.duration_seconds ASC`, then `window_end ASC`, then `pattern_id ASC`, then
`definition_version ASC`, then evidence fingerprint ASC. This ordering is sequence
determinism only and grants no rank or authority.

On correction or revision, `predecessor_evidence_fingerprint` points to the immediately
superseded `PatternEvidence` for the same `pattern_id`, `definition_version`, source,
contract, environment, timeframe, `window_start` and `window_end`. It is `None` only when no
earlier evidence exists, and revision chains cannot skip, fork or overwrite history.

## PROOF OBLIGATIONS

`S2B-PO-01` finite exact allowlist of six pattern IDs with version collision protection.

`S2B-PO-02` golden vectors for every pattern family containing positive, negative-valid,
boundary-equality, pre-close, zero-range, revision, cross-generation, cross-environment and
timeframe-rejection cases, including the exact one-step-before and exact-completion
boundaries.

`S2B-PO-03` no-lookahead tests driven by `event_time` and `knowledge_time`.

`S2B-PO-04` mutation tests for constituent correction, revision, reorder, missing bar,
changed timeframe, changed threshold or version, cross-generation and cross-environment
input.

`S2B-PO-05` `WARMUP`, `UNKNOWN`, `INVALID` and `DEGRADED` validity semantics with separate
resource and lifecycle restrictions, and the `PatternMatchState` compatibility rule.

`S2B-PO-06` duplicate, overlap and conflict representation with deterministic ordering and
fingerprints.

`S2B-PO-07` replay determinism: identical definitions over identical ordered evidence
produce identical pattern sequences and fingerprints.

`S2B-PO-08` negative-capability scan proving no network transport, credential, private API,
persistence, strategy/signal, order, position, risk, deployment or live authority.

`S2B-PO-09` bounded MICRO/NOMINAL/STRESS baseline tied to
`docs/06-test-benchmark-plan.md`, where correctness fails closed before performance metrics
are considered.

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

`S2B-PO-18` local-axis tests: `PatternValidity` is canonical for `PatternEvidence` and the
superseded marker naming `FeatureValidity` is rejected.

`S2B-PO-19` canonical-boundary and idempotency tests: one instant before
`max(window_end, knowledge_time)` cannot emit `MATCHED`; at the canonical boundary the
evaluator may emit `MATCHED` or `NOT_MATCHED` per the equation; re-evaluation later with
unchanged evidence returns the same fingerprint with no duplicate; and a later knowledge-time
correction or revision changes the canonical boundary and produces new revision-linked
evidence.

`S2B-PO-20` duplicate, overlap and conflict tests: exact duplicate evaluation returns the same
fingerprint with no duplicate emission; two matching pattern IDs on the same window are both
retained in canonical order; adjacent overlapping windows remain independent; and no winner,
suppression, score or ranking is applied.

`S2B-PO-21` predecessor-chain tests: `predecessor_evidence_fingerprint` points to the
immediately superseded evidence, is `None` only when no earlier evidence exists, and chains
cannot skip, fork or overwrite history.

## REQUIRED EXECUTOR REPORT


`repositorySync`, `sourceMatch`, `canonicalMain`, `checkpoint`, `implementationHead`,
`changedFiles`, `exactPatternSet`, `patternSetFinite`, `chartStructureDisposition`,
`numericPolicy`, `candleEquations`, `timeframeAllowlist`, `fingerprintDeterminism`,
`formationBoundary`, `noLookahead`, `validityStates`, `matchValiditySeparation`,
`lineageAndRevision`, `axisSeparation`, `resourceRestrictionSeparate`,
`lifecycleRestrictionSeparate`, `rollbackSemantics`, `priorStageRegressions`,
`exactHeadRun`, `exactHeadJob`, `exactHeadConclusion`, `criticalRemaining`,
`highRemaining`, `prOpenUnmerged`, `implementationAuthorized`, `productionCredentials`,
`productionDeployment`, `limitedLive`, `liveTrading`, `stopConditionRespected`.

## STOP CONDITION

Stop with the S2B implementation PR OPEN and UNMERGED after fresh exact-head CI and a
complete author-side Evidence Bundle. Require a fresh independent HIGH_ASSURANCE review
before any merge. Do not implement the chart/market-structure follow-on slice, regime,
scanner, strategy, signal, Brain, Risk, Safety, Session Policy, OMS or Execution
capability, and do not configure credentials, private APIs, persistence, deployment,
limited-live or live trading.
