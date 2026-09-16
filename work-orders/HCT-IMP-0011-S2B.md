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
authorizes nothing today: `HCT-CP-0034` leaves `implementation_authorized=false`, and this
document becomes executable only after its own authorization checkpoint is promoted and a
fresh independent HIGH_ASSURANCE review accepts the exact implementation head.

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

Only the existing upstream analytical timeframe tokens are permitted. Any other timeframe is
rejected `INVALID`. The allowlist may change only through a `PatternVersion` change.

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

`S2B_AXIS_SEPARATION=FeatureValidity;MarketStateTrust;DataAuthority;ResourceRestriction;UniverseLifecycleRestriction`

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
