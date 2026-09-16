# HCT-IMPL-AUTH-0011 — S2B Candlestick Pattern Foundation Authorization

Status: `PENDING_INDEPENDENT_HIGH_ASSURANCE_REVIEW`
Risk: `HIGH_ASSURANCE`
Canonical base: `main@c198a99167fa571802b16f6daf77b253a2b100b0`
Current checkpoint: `HCT-CP-0034 / S2A_IMPLEMENTATION_APPROVED_MERGED`
Proposed implementation: `HCT-IMP-0011-S2B`
Authorization issue: `#75`
Governance branch: `governance/HCT-IMPL-AUTH-0011-S2B`
Author-side governance preflight: `AUTHOR_SIDE_GOVERNANCE_PREFLIGHT_NOT_INDEPENDENT_APPROVAL`

This is a governance-only authorization candidate. It authorizes no product implementation,
implements no runtime code and does not promote a checkpoint.

## OBJECTIVE

Prepare and independently review the next bounded Stage-2 dependency after the completed
and merged S2A deterministic feature/indicator foundation: the first Module 9
(`V1_MINIMUM`) slice, a finite, deterministic, provider-neutral, point-in-time
**Candlestick Pattern Foundation**.

The frozen R11 Stage-2 order is
`features/indicators/patterns -> regime -> scanner -> strategy engine/catalog/signal ->
minimum microstructure`. With S2A complete under `HCT-CP-0034`, patterns are the next
dependency. Regime, scanner, strategy/catalog/signal and microstructure remain later
governed owners and are not authorized here.

## CANONICAL TRACEABILITY

`S2B_FROZEN_BASELINE=HCT-REQ-BASELINE-V1-CANDIDATE`

`S2B_PLANNING_FREEZE=HCT-CP-0014/PLANNING_FREEZE_APPROVED`

`S2B_DOD_SECTIONS=2,4,5,11`


This candidate is derived from, and must satisfy, the following canonical sources:

- `docs/00-source-hierarchy.md` — source hierarchy and precedence;
- `docs/99-r12-frozen-requirements-baseline.md` — the active frozen requirements baseline
  `HCT-REQ-BASELINE-V1-CANDIDATE` and its exact nine frozen requirement source blobs;
- `docs/100-r12-requirements-traceability-and-no-loss-proof.md` — traceability and no-loss
  proof obligations;
- `docs/101-r12-freeze-governance-change-control-and-deferred-decisions.md` — freeze
  governance and change control;
- `docs/03-scope.md`, `docs/04-architecture.md`, `docs/06-test-benchmark-plan.md`;
- `docs/09-definition-of-done.md` sections `2`, `4`, `5` and `11`;
- `docs/10-decisions-ledger.md` — `HCT-DEC-0140` and `HCT-DEC-0141`;
- `docs/92-r11-v1-module-classification-and-integration-hardening.md` — Module `9`
  `Candlestick & Chart Pattern Engine` classified `V1_MINIMUM`.

Governing semantics: `REQ02::Trading intelligence requirements::B2`,
`R11-REQ-012`, `R11-REQ-014`, `R11-REQ-015`, `R11-REQ-023`, `HCT-DEC-0140`,
`HCT-DEC-0141`, and `docs/09-definition-of-done.md` sections `2`, `4`, `5` and `11`.

The nine frozen requirement source blobs are included by exact identity:
`292da9552ae816e4d51b8a299456305da1658e55`,
`f20c1ed00bdb13801aaff8a3b648371bfcffba58`,
`636ad01da9c25e760dd5e2f033b93a0f04578a17`,
`fea197e60532eb6ff3b11b628b9aabcbcfc00c41`,
`c8a426966c5a0dc34704d1413f506332e770c2c7`,
`c859c0c4a718e3017c34aa50013d4c50959853b4`,
`bc897ebd470857a53055bdee85128b5bd31a5822`,
`023187ef23b01d5a11f978bbfe6e38abf172bb3b`,
`6935e9973696d5b706546d63d847ea398780d936`.

## PRECONDITION AND PREREQUISITE STATE

- `HCT-CP-0034` records the independently approved and merged completion of
  `HCT-IMP-0009-S2A` at approved head
  `40e67302fb80e329429be50430584ff9523a12a0`, merge commit
  `c862e5670465ef0f8d0c77dce163a1ece7c92ac4`;
- `HCT-CP-0034` consumes the CP0033 implementation authorization and leaves
  `implementation_authorized=false`, an empty authorization scope and the
  `NONE_PENDING_NEXT_GOVERNED_AUTHORIZATION` ceiling;
- S2A, S1E and S1F are read-only upstream contracts. Module 9 may not restate, duplicate or
  re-own S2A feature semantics, S1E Market-State truth, S1F value evidence or
  DataAuthority;
- no S2B implementation Issue exists yet; the implementation Issue is expected to be
  created only when this authorization is accepted and a separate authorization checkpoint
  is promoted.

## MODULE 9 SLICE DECOMPOSITION

`S2B_SLICE_NAME=Candlestick Pattern Foundation`

`S2B_CHART_STRUCTURE_DISPOSITION=REQUIRED_FOLLOW_ON_MODULE9_SLICE_BEFORE_REGIME`

Module 9 is delivered as two bounded sequential slices: this candlestick slice, and a
**required follow-on within Module 9** for causal chart/market-structure evidence. The
follow-on slice is not post-V1 and is not skipped, and `HCT-DEC-0140` forbids deleting it
silently. It is **not pre-authorized** here and no Work Order or implementation ID is
fabricated for it. The next Stage-2 dependency after successful S2B completion is that
separately governed causal chart/market-structure minimum, and only after **both** Module 9
slices are complete may regime work be considered. The frozen Stage-2 order is unchanged.

No-lookahead for the follow-on slice: causal pivot/structure evidence may be recognized only
after its confirmation bars are known; delayed confirmation is not lookahead when
`event_time` and `knowledge_time` are honored, and that confirmation contract must be frozen
by the follow-on slice itself.

## SCOPE

The candidate may define only:

- immutable typed `PatternDefinition` / `PatternVersion` with canonical ID, version,
  family, bar cardinality, frozen source fields, timeframe and version allowlist, threshold
  and equality semantics, midpoint and gap policy, formation/completion boundary rule and
  behaviorally material fingerprints;
- a finite registry that rejects silent canonical-ID redefinition, version collision and
  material mutation;
- immutable `PatternEvidence` bound to source, contract, environment, generation,
  timeframe/version, ordered constituent lineage, event and knowledge times, wall-receive
  time, window boundaries, revision/predecessor lineage, validity state, match state and the
  exact consumed upstream evidence fingerprints;
- exactly the six frozen `V1_MINIMUM` candlestick pattern IDs
  `P-DC-001`, `P-MB-001`, `P-EC-001`, `P-EC-002`, `P-MS-001`, `P-ES-001`;
- explicit `VALID`, `UNKNOWN`, `INVALID`, `WARMUP` and `DEGRADED` validity outcomes with
  fail-closed propagation, the separate `PatternMatchState` axis and separate resource and
  lifecycle restriction axes;
- point-in-time formation boundaries, exact bar cardinality, CLOSED-input requirements,
  ordering, duplicate/overlap/conflict representation and strict no-lookahead validation;
- Decimal-only threshold and tolerance evaluation under `FEATURE_DECIMAL_V1`;
- deterministic fixture/replay evidence, deterministic tests and bounded benchmark profiles
  tied to `docs/06-test-benchmark-plan.md`;
- a negative-capability scanner and a pull-request-only exact-head quality workflow for the
  future implementation slice.

No pattern may create a candidate action, ranking, directional probability, expected return,
strategy suitability, signal, Brain admission, Risk approval, Execution plan or live
authority. Structural pattern evidence is not a trade authorization.

## OUT OF SCOPE

No runtime/product implementation in this governance candidate. No network transport,
provider endpoint, socket/WebSocket/HTTP client, credential, private API, signing,
persistence, database/RLS, feature store, deployment or infrastructure topology. Also out of
scope: the Module 9 chart/market-structure follow-on slice itself, Module 10 proprietary
indicator R&D, regime classification, scanner/ranking, strategy/catalog/signal,
microstructure, Brain, agents, RAG/memory, learning, calibration, Risk, Safety, Session
Policy, sizing, leverage, OMS, Execution, reconciliation, protection, orders, positions,
balances, fills, limited-live and live trading. An unbounded internet pattern catalog is not
authorized.

## FROZEN CANDLE PRIMITIVES

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

`S2B_TIMEFRAME_ALLOWLIST=Min1,Min5,Min15`

`S2B_PATTERN_DECIMAL_POLICY=FEATURE_DECIMAL_V1`

`S2B_PATTERN_BINARY_FLOAT=FORBIDDEN`

## FROZEN PATTERN EQUATIONS

`S2B_PATTERN_ALLOWLIST=P-DC-001,P-MB-001,P-EC-001,P-EC-002,P-MS-001,P-ES-001`

`S2B_PATTERN_COUNT=6`

`S2B_PATTERN_FAMILIES=SINGLE_BAR,TWO_BAR_REVERSAL,THREE_BAR_REVERSAL`

`P-DC-001` Doji — one CLOSED bar; `body_ratio <= 0.10`; direction `NEUTRAL`.

`P-MB-001` Marubozu — one CLOSED bar; `body_ratio >= 0.90`; direction `BULLISH` if
`close > open`, `BEARISH` if `close < open`.

`P-EC-001` Bullish Engulfing — previous bar `bearish`, current bar `bullish`,
`current.open <= previous.close`, `current.close >= previous.open`; inclusive body bounds.

`P-EC-002` Bearish Engulfing — previous bar `bullish`, current bar `bearish`,
`current.open >= previous.close`, `current.close <= previous.open`; inclusive mirror.

`P-MS-001` Morning Star — bar1 `bearish` long-body (`>= 0.90`), bar2 small-body
(`<= 0.10`), bar3 `bullish` long-body (`>= 0.90`), and
`bar3.close >= midpoint(bar1.open, bar1.close)`.

`P-ES-001` Evening Star — exact mirror: bar1 `bullish` long-body, bar2 small-body, bar3
`bearish` long-body, and `bar3.close <= midpoint(bar1.open, bar1.close)`.

`S2B_MIDPOINT_EQUALITY=BOUNDS_INCLUSIVE`

`S2B_STAR_GAP_POLICY=NONE_IN_V1`

`S2B_NO_LOOKAHEAD=STRICT_ONE_STEP_BEFORE_FORMATION_BOUNDARY_NOT_RECOGNIZED`

`S2B_REPLAY_DETERMINISM=IDENTICAL_DEFINITIONS_AND_ORDERED_EVIDENCE_IDENTICAL_OUTPUT`

`S2B_AXIS_SEPARATION=FeatureValidity;MarketStateTrust;DataAuthority;ResourceRestriction;UniverseLifecycleRestriction`

`S2B_BENCHMARK_MODE=S2B_BASELINE_ESTABLISHMENT_V1`

`S2B_BENCHMARK_PROFILES=MICRO,NOMINAL,STRESS`

## MATCH SEPARATION AND ROLLBACK

`S2B_PATTERN_MATCH_STATE=MATCHED,NOT_MATCHED,INDETERMINATE`

`S2B_MATCH_VALIDITY_RULE=VALID_OR_DEGRADED_REQUIRES_MATCHED_OR_NOT_MATCHED`

`S2B_RESTRICTIVE_VALIDITY_RULE=WARMUP_UNKNOWN_INVALID_REQUIRES_INDETERMINATE`

`S2B_VALID_NON_MATCH=NOT_MATCHED_NEVER_UNKNOWN`

A valid window that fails a pattern equation is `NOT_MATCHED`, never `UNKNOWN`, and never
indistinguishable from "the evaluator did not run". Rollback must be able to disable or
revert the S2B producer and registry and return consumers to S2A/S1F inputs without
mutating upstream S1E/S1F/S2A truth; historical `PatternEvidence` is append-only and no
migration or persistence authority is granted.

## PROOF OBLIGATIONS

`S2B-PO-01` finite exact allowlist and version collision protection;

`S2B-PO-02` golden vectors for every pattern family containing positive, negative-valid,
boundary-equality, pre-close, zero-range, revision, cross-generation, cross-environment and
timeframe-rejection cases, including the exact one-step-before and exact-completion
boundaries;

`S2B-PO-03` no-lookahead tests using `event_time` and `knowledge_time`;

`S2B-PO-04` mutation tests for constituent correction, revision, reorder, missing bar,
changed timeframe, changed threshold/version, cross-generation and cross-environment input;

`S2B-PO-05` `WARMUP` / `UNKNOWN` / `INVALID` / `DEGRADED` validity semantics with separate
resource and lifecycle restrictions, and the `PatternMatchState` compatibility rule;

`S2B-PO-06` duplicate, overlap and conflict representation with deterministic ordering and
fingerprints;

`S2B-PO-07` replay determinism for identical definitions and exact ordered evidence;

`S2B-PO-08` negative-capability scan proving no network transport, credential, private API,
persistence, strategy/signal, order, position, risk, deployment or live authority;

`S2B-PO-09` bounded MICRO/NOMINAL/STRESS baseline tied to `docs/06-test-benchmark-plan.md`
where correctness fails closed before performance metrics matter.

## AUTHORITY FIREWALL

This candidate authorizes nothing until its own authorization checkpoint is promoted:

- `implementation_authorized=false`;
- `implementation_authorization_scope=[]`;
- `implementation_authorization_ceiling=NONE_PENDING_NEXT_GOVERNED_AUTHORIZATION`;
- `production_credentials_authorized=false`;
- `production_deployment_authorized=false`;
- `limited_live_authorized=false`;
- `live_trading_authorized=false`.

Planning Freeze remains approved and the nine frozen R12 requirement source blobs remain
unmodified. The S2B governance PR must remain OPEN and UNMERGED for a fresh independent
HIGH_ASSURANCE review.
