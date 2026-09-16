# HCT-IMP-0011-S2B — Author-Side Evidence Bundle

Status: `AUTHOR_PREFLIGHT`

This bundle is author-side evidence only. It is `NOT_INDEPENDENT_APPROVAL` and does not
authorize merge, a completion checkpoint, production, limited-live or live trading.

## Exact execution context

- implementation authorization: `HCT-IMPL-AUTH-0011`
- implementation increment: `HCT-IMP-0011-S2B`
- authorizing checkpoint: `HCT-CP-0035 / IMPLEMENTATION_AUTHORIZED_S2B`
- implementation Issue: `#77`
- authorization Issue / PR: `#75` / `#76`
- implementation base: `9e6014472df7723b21f9a1d7ab2aa207ac714ccc` (exact post-CP0035 main)
- branch: `implementation/HCT-IMP-0011-S2B`
- context lock: `evidence/HCT-IMP-0011-S2B-CONTEXT-LOCK.md`
- frozen source identities: `17/17` planning artifacts and `9/9` requirement blobs PASS against the lock
- changed files: exactly the eight authorized implementation paths

The exact implementation head, the exact-head workflow run, check, job and conclusion are
recorded by the pull request CI and by the external author-side receipt published on the pull
request, so no tracked file has to contain its own commit identity.

## Superseded baseline (retained, not overwritten)

The first author-side receipt for this increment was recorded at head
`253fe3d2d8ebfd61c3401b3ffbe33d44d3019f5c`, exact-head run `35116041663`, job `104861600644`,
conclusion `success`, at that time with `430 passed`, `39` S2B pattern tests, coverage `90.37%`
and MICRO/NOMINAL/STRESS output manifests `0b5f7c458942c2444fbf2cc82e4ea35fce5dbd744b6c6d2e740cb2e6d7e0cc06`,
`ad084d56ddbed82486c43422f40dc2da344ab5d84cf6febec9018332298755dc` and
`d163aaa2d7a33e394f025c8cbf4b4e9a6c81018a1bd6b8d77fb74ae6464afcf9`. That receipt is retained
here as history for that head only.

The IMP-H001-H004 correction was recorded at head `5ae90efbddf35d755edc1edcab3095e8b4956e2c`,
exact-head run `35128709704`, job `104904061677`, conclusion `success`, at that time with
`449 passed`, `58` S2B pattern tests, coverage `90.37%` and MICRO/NOMINAL/STRESS output
manifests `505cbec6ca95de3574ae7f70acbdd0118515deaaaf9f5b5d7839331f0a1102b5`,
`98488d6400b9e143ba9e9314edab0fdf9ad511d4105052b4a7c5d9e6712d8244` and
`8d956cbb3a5a1838f3e4b9d9a59ab11c9f650bd54eab1af676cd59fd1c4a28e6`. That receipt is retained
here as history for that head only.

Independent review `5225276949` (`HIGH_ASSURANCE`, bound to the exact head
`253fe3d2d8ebfd61c3401b3ffbe33d44d3019f5c`) returned `CORRECTION REQUIRED` with
`CRITICAL 0` / `HIGH 4`: `S2B-IMP-H001` (exact bar cardinality not enforced),
`S2B-IMP-H002` (authoritative `PatternEvidence` still caller-mintable through
`_from_evaluator`), `S2B-IMP-H003` (revision/predecessor lineage caller-controlled) and
`S2B-IMP-H004` (`PatternDefinition`/`PatternVersion` identity not binding all frozen
behaviorally material semantics).

Independent review `5226463605` (`HIGH_ASSURANCE`, bound to the exact head
`5ae90efbddf35d755edc1edcab3095e8b4956e2c`) confirmed IMP-H001, IMP-H002 and IMP-H004 as
materially closed and returned `CORRECTION REQUIRED` with `CRITICAL 0` / `HIGH 1`:
`S2B-IMP-H003R` — a stale immutable `PatternEvaluationState` could still mint two
independently attested sibling successors from the same predecessor, so the public evaluator
did not enforce `S2B_REVISION_CHAIN=NO_SKIP_NO_FORK_NO_OVERWRITE` at the issuance boundary.

## Correction delta IMP-H001-H004 and IMP-H003R

The findings were closed author-side only on the same PR #78 and the same eight-file
implementation boundary. No prior successful S2B semantic was removed, no S1E/S1F/S2A runtime
source, Work Order, checkpoint, frozen requirement, Decisions Ledger, ADR, dependency lock or
frontend file was modified, and the exact six-pattern scope, the CP0035 authority ceiling and
the negative-capability firewall are unchanged.

- `S2B-IMP-H001` — the frozen definition owns an exact bar cardinality. `len < k` keeps the
  existing `WARMUP` behavior, `len == k` evaluates normally, and `len > k` now fails closed as
  `PatternValidity.INVALID` / `PatternMatchState.INDETERMINATE` with the stable reason
  `OVER_CARDINALITY_WINDOW`. Constituents are never silently sliced: every presented
  constituent remains part of the claimed evidence window (lineage, constituent revisions and
  window bounds all include it).
- `S2B-IMP-H002` — `PatternEvidence._from_evaluator` is removed. The only path that creates
  attested evidence is the module-private `_issue_pattern_evidence`, which receives only the
  frozen `PatternVersion`, the exact validated paired constituents, the evaluation boundary
  time and the typed prior evidence state, and recomputes span, axis fold, equation, direction,
  validity, timestamps, lineage, revision link and fingerprint material itself. The public
  `__init__` remains blocked and `__copy__`/`__deepcopy__`/`__reduce_ex__` refuse to produce
  unattested twins. Attestation is content-bound: the seal is a keyed digest over the complete
  evidence fingerprint, so any later field mutation, tampering or reconstruction invalidates
  the seal, and `canonical_evidence_order` rejects evidence that is not evaluator-issued.
- `S2B-IMP-H003` — `revision` and `predecessor_evidence_fingerprint` were removed from the
  caller-controlled evaluation inputs. The evaluator accepts only a typed
  `PatternEvaluationState`; the revision is derived as `head.revision + 1` and the predecessor
  as `head.fingerprint`. Exact predecessor scope is validated (pattern ID, definition version,
  source, contract, environment, timeframe identity, window start and window end) together with
  constituent revision continuity: an unchanged constituent may keep its fingerprint, while a
  changed `CandleBar` must prove the canonical immediate predecessor relation to the
  corresponding prior constituent fingerprint. A revision request with no behavior or evidence
  change is rejected, and the chain rejects a skip, a fork, a non-immediate predecessor and an
  overwrite.
- `S2B-IMP-H003R` — predecessor authorization is now linear at the evaluator issuance
  boundary. The evaluator owns an in-process consumption registry keyed by the attested
  predecessor evidence fingerprint plus the frozen predecessor scope (pattern ID, definition
  version, source, contract, environment, timeframe identity, window start and window end), so
  one logical predecessor head may authorize at most one distinct successor evidence. A second
  request that reuses an already-consumed predecessor for a different successor fails with
  `PatternEvaluationError` before any sibling is attested, independently of whether the first
  successor was inserted into a separately held `PatternEvaluationState` value and
  independently of a freshly rebuilt but equally stale state. An identical idempotent
  re-evaluation of the same transition returns the same canonical evidence identity instead of
  minting a new revision, a genuine correction still derives `head.revision + 1` with
  `predecessor = head.fingerprint`, and consumption never leaks across unrelated pattern/window
  keys. Raw caller-supplied hashes are never used as truth; only evaluator-attested typed
  evidence and evaluator-owned state are consumed.
- `S2B-IMP-H004` — `PatternDefinition` now binds every frozen behaviorally material semantic in
  its material and fingerprint: the exact input contract
  `CANDLEBAR_OHLC_PLUS_EVALUATOR_ISSUED_FEATURE_SAMPLE`, the ordered source fields
  `open,high,low,close`, a canonical per-pattern equation token for each of the six IDs
  (polarity predicates, inclusive engulfing inequalities, long/small thresholds, star midpoint
  inequality, no-gap V1 rule), the full structural timeframe identity tokens
  `Min1:60:1:UNIX_EPOCH_MULTIPLES`, `Min5:300:1:UNIX_EPOCH_MULTIPLES` and
  `Min15:900:1:UNIX_EPOCH_MULTIPLES`, the exact bar cardinality and its over-cardinality policy,
  the CLOSED-bar finality requirement, the canonical formation rule, the canonical evaluation
  boundary rule `S2B_CANONICAL_EVALUATION_BOUNDARY=max(window_end,knowledge_time)`, the
  zero-range policy, `FEATURE_DECIMAL_V1` at precision 76 with `ROUND_HALF_EVEN`, the frozen
  thresholds/equality and the direction/match-state policy. `PatternVersion.fingerprint` stays a
  deterministic function of the complete `PatternDefinition` material, and the existing correct
  V1 definitions remain definition version `1`.

## Bounded implementation (current head)

The slice implements the first Module 9 `V1_MINIMUM` foundation:

- immutable `PatternDefinition`/`PatternVersion` with complete material fingerprints and a
  persistent `PatternRegistry` that rejects silent redefinition and version collision;
- exactly six canonical patterns `P-DC-001`, `P-MB-001`, `P-EC-001`, `P-EC-002`, `P-MS-001`,
  `P-ES-001` under algorithm `S2B_STANDARD_CANDLESTICK_PATTERNS_V1`, definition version `1`;
- structural timeframe identities only: `Min1`/60/v1/`UNIX_EPOCH_MULTIPLES`,
  `Min5`/300/v1, `Min15`/900/v1;
- `FEATURE_DECIMAL_V1` Decimal-only comparison at precision 76 with `ROUND_HALF_EVEN`,
  frozen `SMALL_BODY_MAX=0.10` and `LONG_BODY_MIN=0.90`, inclusive engulfing and star-midpoint
  semantics and no V1 gap requirement;
- the explicit paired constituent contract: one original S1F `CandleBar` plus the
  evaluator-issued S2A `FeatureSample` from that same candle, bound by
  `sample.fingerprint == candle.fingerprint`, so `open` is consumed only from the candle whose
  fingerprint commits it;
- the local `PatternValidity` axis with precedence `INVALID > UNKNOWN > WARMUP > DEGRADED >
  VALID`, with `ResourceRestriction` and `UniverseLifecycleRestriction` kept separate and a
  separate `PatternMatchState` axis;
- exact evaluable bar cardinality with fail-closed over-cardinality handling;
- the canonical evaluation boundary `max(window_end, knowledge_time)` with idempotent later
  re-evaluation and the canonical evidence identity, duplicate idempotency, overlap/conflict
  coexistence, deterministic sequence order and the typed immediate predecessor chain;
- evaluator-issued `PatternEvidence` with a content-bound attestation seal and canonical
  fingerprint v1.

No transport, provider endpoint, credential, private API, persistence, downstream decision,
deployment or live authority is present in this slice.

## Focused correction tests

The four findings are proven by focused tests that CI runs before the full suite:

| Finding | Focused tests |
|---|---|
| S2B-IMP-H001 | `test_s2b_imp_h001_over_cardinality_window_fails_closed`, `test_s2b_imp_h001_no_silent_slicing_of_presented_constituents`, `test_s2b_imp_h001_exact_cardinality_semantics_unchanged` |
| S2B-IMP-H002 | `test_s2b_imp_h002_no_arbitrary_material_issuance_api`, `test_s2b_imp_h002_coherent_forgery_is_impossible`, `test_s2b_imp_h002_caller_selected_fields_are_rejected`, `test_s2b_imp_h002_tampered_or_copied_evidence_is_rejected` |
| S2B-IMP-H003 | `test_s2b_imp_h003_raw_revision_and_predecessor_inputs_are_removed`, `test_s2b_imp_h003_scope_covers_pattern_identity_source_contract_environment`, `test_s2b_imp_h003_wrong_scope_is_rejected`, `test_s2b_imp_h003_skip_fork_and_overwrite_are_rejected`, `test_s2b_imp_h003_constituent_continuity_is_required`, `test_s2b_imp_h003_valid_correction_derives_the_immediate_link`, `test_s2b_imp_h003_no_change_revision_is_rejected`, `test_s2b_imp_h003_replay_reproduces_the_chain` |
| S2B-IMP-H003R | `test_s2b_imp_h003r_stale_predecessor_reuse_is_rejected_at_issuance`, `test_s2b_imp_h003r_consumption_does_not_leak_across_scopes` |
| S2B-IMP-H004 | `test_s2b_imp_h004_definition_golden_fingerprints`, `test_s2b_imp_h004_definition_material_binds_every_frozen_semantic`, `test_s2b_imp_h004_definition_mutation_is_rejected`, `test_s2b_imp_h004_every_material_key_is_fingerprint_visible` |

Observed results: `21 passed, 39 deselected` for the focused selection. The over-cardinality
adversary covers two bars for each one-bar pattern, three bars for each two-bar pattern and
four bars for each three-bar pattern, and none of them may emit `MATCHED`/`NOT_MATCHED`; every
correct-cardinality golden window keeps identical match and direction semantics. The coherent
forgery attempt reuses the exact identity and time material of a legitimate `NOT_MATCHED`
evidence as coherent `MATCHED` evidence with a concrete direction and a non-empty reason, and
fails because no arbitrary-material issuance API exists; caller-selected validity, timestamps,
ordered lineage, authority lineage, constituent revisions and pattern definition identity are
rejected even when every value is individually well-typed. Definition fingerprints are frozen as
golden vectors for all six standard V1 definitions, and mutating an equation token, source
field, timeframe duration/version/alignment, boundary rule, finality rule, threshold/equality or
Decimal policy is rejected as non-V1 while every material key remains fingerprint-visible.

The H003R adversary creates head revision 0 with one predecessor state, issues correction A
from it as attested revision 1 with `predecessor = head`, then reuses the exact same unchanged
state for a different correction B: the second issuance raises `PatternEvaluationError` with
"predecessor already authorized a different successor" before any sibling exists, and a
separately held stale state for the same predecessor is rejected identically. The identical
re-evaluation of A returns the very same attested object, and only after advancing the
legitimate chain with A can revision 2 be issued. Consumption in one window does not block a
different window of the same pattern, nor the same window of a different pattern. The focused
test is mutation-proven: restoring the pre-correction behaviour (attesting the sibling instead
of rejecting it) makes it fail.

### Non-persistent runtime boundary

The consumption registry is in-process memory only: there is no durable store, no file,
network or provider state, and restart recovery is explicitly not authorized by this slice, so
a restarted evaluator starts with an empty registry. Within one process the decision is
deterministic and fail-closed, consumption is bounded by the number of issued corrections, and
entering a chain state carried across a restart is not a capability this slice grants.

## Proof obligations

| Obligation | Evidence | Result |
|---|---|---|
| S2B-PO-01 | exact six-pattern allowlist, frozen material, registry collision and redefinition rejection | PASS |
| S2B-PO-02 | golden positive, negative-valid and boundary-equality vectors per pattern and timeframe | PASS |
| S2B-PO-03 | one instant before the canonical boundary cannot match; delayed knowledge time is not lookahead | PASS |
| S2B-PO-04 | structural timeframe identity, reorder, duplicate, non-contiguity, mixed identity and retired generation rejection | PASS |
| S2B-PO-05 | `VALID`/`DEGRADED`/`WARMUP`/`UNKNOWN` semantics, zero-range primitive and separate axes | PASS |
| S2B-PO-06 | duplicate, overlap and conflict representation retained independently with no winner | PASS |
| S2B-PO-07 | replay determinism for identical definitions and exact ordered evidence | PASS |
| S2B-PO-08 | negative-capability scan | PASS |
| S2B-PO-09 | bounded MICRO/NOMINAL/STRESS baseline with correctness failing closed first | PASS |
| S2B-PO-10 | timing adversarial tests, late knowledge and revision linkage | PASS |
| S2B-PO-11 | timeframe identity negative tests | PASS |
| S2B-PO-12 | authority seam reuse and fixture isolation | PASS |
| S2B-PO-13 | paired constituent cross-binding, forged `open`, mismatched and unpaired inputs | PASS |
| S2B-PO-14 | benchmark markers, profile cardinalities and two-run deterministic projection | PASS |
| S2B-PO-15 | version, direction and canonical fingerprint semantics | PASS |
| S2B-PO-16 | validity fold precedence matrix and axis separation | PASS |
| S2B-PO-17 | evaluator-issued attestation, direct construction, `replace`/tamper and caller-selected fields rejection, and coherent forgery impossibility (`test_s2b_imp_h002_*`) | PASS |
| S2B-PO-18 | local `PatternValidity` axis with the superseded marker rejected | PASS |
| S2B-PO-19 | canonical boundary, idempotent later re-evaluation and evaluator-derived revision link | PASS |
| S2B-PO-20 | duplicate, overlap, conflict, canonical sequence order and no-winner semantics | PASS |
| S2B-PO-21 | immediate predecessor chain with no skip, fork or overwrite, evaluator-derived revision and predecessor, and no minted sibling at the issuance boundary (`test_s2b_imp_h003_*`, `test_s2b_imp_h003r_*`) | PASS |
| S2B-IMP-H001 | exact evaluable bar cardinality with fail-closed over-cardinality windows and no silent slicing | PASS |
| S2B-IMP-H002 | non-forgeable authoritative evidence with evaluator-owned issuance and content-bound attestation | PASS |
| S2B-IMP-H003 | evaluator-derived revision/predecessor chain with exact scope and constituent continuity | PASS |
| S2B-IMP-H003R | linear predecessor consumption at the issuance boundary with no minted sibling (`test_s2b_imp_h003r_*`) | PASS |
| S2B-IMP-H004 | fully content-bound `PatternDefinition`/`PatternVersion` identity with golden and mutation proofs | PASS |

`S2B-PO-17`, `S2B-PO-21` and `S2B-IMP-H003R` are asserted only through the focused
correction tests above, not merely because the earlier suite was green.

## Local validation receipt

- `python -m pytest -q apps/backend`: `451 passed`
- S2B pattern tests: `60 passed`
- focused IMP-H001-H003R-H004 selection: `21 passed, 39 deselected`
- global coverage: `90.39%` (gate `>= 90%`); `patterns.py` coverage `91%`
- ruff check on S2B source/tests/scripts: PASS
- ruff format check on S2B source/tests/scripts: PASS
- strict mypy on backend source: `Success: no issues found in 19 source files`
- backend sdist/wheel build: PASS
- pip-audit: no known vulnerabilities
- S2B negative-capability scan: PASS, including the contract checks that reject a reintroduced
  arbitrary-material issuance helper, raw `revision`/`predecessor_evidence_fingerprint`
  evaluator inputs and removal of the no-fork issuance markers; each new rule was
  mutation-tested and fires on the reintroduced defect
- CI contract gate executed locally with the same assertions: PASS, and mutation-tested against a
  reintroduced raw evaluator input and a removed required marker
- frontend prior-stage gates: typecheck PASS, `13 passed`, lint PASS, generated-format PASS, build PASS, `npm audit` 0 vulnerabilities
- `git diff --check`: clean
- no frontend file changed

## Benchmark receipt

Mode: `S2B_BASELINE_ESTABLISHMENT_V1`
Fixture: `S2B_PATTERN_FIXTURE_V1`, seed `0`, no network, no uncontrolled randomness.
Runtime: Python 3.12 Decimal pattern engine.

The frozen profile cardinality fixes the corpus. Each pattern is evaluated only over its own
exact evaluable bar cardinality, sampled deterministically with the recorded stride, so these
are baseline measurements and not product SLOs. The H003R no-fork enforcement consumes
predecessors per logical key and changes no evidence material, so the manifest hashes below are
identical to the ones recorded for the previous corrected head.

| Profile | Contracts | Closed pairs/contract/timeframe | Stride | Windows | Evaluations | Eval/s | Replay pairs/s | Peak bytes | Depth |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| MICRO | 1 | 2048 | 4 | 1536 | 9,270 | 369.67 | 245.01 | 8,183,858 | 3 |
| NOMINAL | 8 | 4096 | 8 | 12288 | 74,160 | 518.70 | 687.57 | 16,018,080 | 3 |
| STRESS | 16 | 8192 | 16 | 24576 | 148,896 | 330.69 | 873.31 | 32,062,379 | 3 |

Validity and match counts:

| Profile | `VALID` | `DEGRADED` | `WARMUP` | `UNKNOWN` | `INVALID` | `MATCHED` | `NOT_MATCHED` | `INDETERMINATE` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| MICRO | 8,214 | 0 | 18 | 1,020 | 18 | 1,530 | 6,684 | 1,056 |
| NOMINAL | 65,664 | 0 | 144 | 8,208 | 144 | 12,264 | 53,400 | 8,496 |
| STRESS | 131,712 | 288 | 288 | 16,320 | 288 | 24,672 | 107,328 | 16,896 |

Deterministic probes, per profile (all fail closed):

- pre-boundary rejections (`WARMUP`, exactly equal to the `WARMUP` count): MICRO `18`,
  NOMINAL `144`, STRESS `288`;
- over-cardinality rejections (`INVALID` / `OVER_CARDINALITY_WINDOW`, exactly equal to the
  `INVALID` count): MICRO `18`, NOMINAL `144`, STRESS `288`;
- revision-chain probe: MICRO `18/18`, NOMINAL `144/144`, STRESS `288/288` links derived the
  immediate predecessor with `revision = head.revision + 1`;
- no-lookahead rejections: MICRO `18`, NOMINAL `144`, STRESS `288`.

Input manifest hashes (unchanged by the correction):

- MICRO: `64199221cee04bb2afea125a1cd17ce5efc62ad610097926bb4ddebba27eba1f`
- NOMINAL: `b18ece1e957fb0ca49b25f93668a87f37ce041040d2b37da8797d943e2682638`
- STRESS: `00152ae58bfefe7f2ab7f77302e681f1312a1d96eef0e21b078902d4f1873553`

Output manifest hashes at the current head:

- MICRO: `505cbec6ca95de3574ae7f70acbdd0118515deaaaf9f5b5d7839331f0a1102b5`
- NOMINAL: `98488d6400b9e143ba9e9314edab0fdf9ad511d4105052b4a7c5d9e6712d8244`
- STRESS: `8d956cbb3a5a1838f3e4b9d9a59ab11c9f650bd54eab1af676cd59fd1c4a28e6`

STRESS additionally exercises the adversarial corpus: resource-degraded and lifecycle-restricted
constituents and degraded market truth, each over exact cardinality windows.

Two consecutive runs produced identical input and output manifests and an identical
deterministic projection. The validator reported `S2B exact profiles, cardinalities,
no-lookahead rejections and replay hash parity across both runs: PASS`, and it now also fails
closed unless the exact cardinality groups are `1/2/3`, the `INVALID` count is exactly the
over-cardinality probe, the `WARMUP` count is exactly the pre-boundary probe, the pre-boundary
and over-cardinality probes are non-zero, and every revision-chain link is the exact immediate
predecessor.

## Authorization firewall

The CP0035 authorization is bounded and non-trading:

- `implementation_authorized=true` for scope `HCT-IMP-0011-S2B` only;
- `implementation_authorization_ceiling=NON_TRADING_STAGE_2_CANDLESTICK_PATTERN_FOUNDATION_ONLY`;
- `production_credentials_authorized=false`;
- `production_deployment_authorized=false`;
- `limited_live_authorized=false`;
- `live_trading_authorized=false`.

`productionCredentials=false`, `productionDeployment=false`, `limitedLive=false`,
`liveTrading=false`.

The required chart/market-structure follow-on within Module 9, Module 10 proprietary indicator
R&D, regime, scanner/ranking, strategy/catalog/signal, microstructure, Brain, agents,
RAG/memory, learning, calibration, Risk, Safety, Session Policy, sizing, leverage, OMS,
Execution, reconciliation, protection, orders, positions, balances, fills, deployment,
limited-live and live trading remain unauthorized.

## Required stop condition

The implementation PR remains OPEN and UNMERGED. No completion checkpoint is promoted and no
independent approval is claimed. `S2B-IMP-H001` through `S2B-IMP-H004` and `S2B-IMP-H003R` are closed `AUTHOR_SIDE_ONLY`;
review `5226463605` is retained as a historical record for head
`5ae90efbddf35d755edc1edcab3095e8b4956e2c`. The next mandatory action is a fresh independent
`HIGH_ASSURANCE` review of the exact corrected head.
