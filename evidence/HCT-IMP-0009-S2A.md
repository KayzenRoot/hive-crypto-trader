# HCT-IMP-0009-S2A — Author-Side Evidence Bundle

Status: `AUTHOR_PREFLIGHT`

This bundle is author-side evidence only. It is `NOT_INDEPENDENT_APPROVAL` and
does not authorize merge, a later checkpoint, production, limited-live or live
trading.

## Exact execution context

- implementation authorization: `HCT-IMPL-AUTH-0009`
- implementation increment: `HCT-IMP-0009-S2A`
- promoted checkpoint: `HCT-CP-0033`
- execution base: `fecb97b6c9513a6dc0114d22c5e3768017411157`
- branch: `implementation/HCT-IMP-0009-S2A`
- implementation pull request: `#74`, kept OPEN and UNMERGED
- `previousHead=a942cb0b02fdb6351ea4e3c0a53854279ab21366` (reviewed head that returned
  `CORRECTION REQUIRED / CRITICAL 0 / HIGH 4`)
- `correctedImplementationHead=4715b06fc1aafba87ead686655f5231d3f3f8b04` (head that
  carries the IMP-H001 — IMP-H004 corrections and passed a fresh exact-head run)
- `finalHead`: the exact-head pull request CI and PR #74 metadata below
- source context lock: `evidence/HCT-IMP-0009-S2A-CONTEXT-LOCK.md`
- frozen source identities: 9/9 PASS
- changed files: exactly the eight authorized S2A paths

The execution base is the post-CP0033 `main` commit. No governance, checkpoint,
work-order, frozen-source, dependency-lock, S1E or S1F source was changed by this
implementation slice.

## Bounded implementation

The implementation is limited to deterministic, provider-neutral feature
evidence and analytical 5m/15m alignment:

- immutable `FeatureDefinition`, `FeatureVersion` and persistent
  `FeatureRegistry` with material fingerprints;
- immutable point-in-time `FeatureSample`, `FeatureValue` and
  `FeatureSnapshot` with source, contract, environment, generation, market-state,
  event, knowledge, wall-receive and ordered lineage evidence;
- explicit `VALID`, `UNKNOWN`, `INVALID`, `WARMUP` and `DEGRADED` states;
- exactly the frozen feature set:
  `F-RET-001,F-SMA-001,F-EMA-001,F-ROC-001,F-RSI-001,F-TR-001,F-ATR-001,F-VSMA-001`;
- `FEATURE_DECIMAL_V1`, Decimal-only arithmetic, precision 76, canonical scale
  18, maximum precision 38 and `ROUND_HALF_EVEN`;
- canonical serialized recursive EMA/ATR/RSI state with bit-for-bit resume
  parity;
- exact closed-1m constituent alignment for 5m and 15m derived analytical
  evidence, with close-boundary, knowledge-time, generation and provenance
  checks.

No transport, provider endpoint, credential, persistence, downstream action,
deployment or live authority is present in this slice.

## S2A implementation correction delta (IMP-H001 — IMP-H004)

All four HIGH findings were corrected on the same pull request, without widening
the approved Module 8 scope.

| Finding | Severity | Author-side status |
|---|---|---|
| IMP-H001 canonical recursive state on every update | HIGH | `CLOSED_AUTHOR_SIDE_ONLY` |
| IMP-H002 recursive state identity and chain attestation | HIGH | `CLOSED_AUTHOR_SIDE_ONLY` |
| IMP-H003 restore the frozen axis separation | HIGH | `CLOSED_AUTHOR_SIDE_ONLY` |
| IMP-H004 derived window evidence must be content-bound | HIGH | `CLOSED_AUTHOR_SIDE_ONLY` |

`CLOSED_AUTHOR_SIDE_ONLY` records that the author-side correction, tests and
gates pass. It is not independent closure and does not authorize merge.

### IMP-H001 — canonical recursive state on every update

The pre-correction public batch path carried higher-precision Decimal state
through multiple EMA/ATR updates and canonicalized only at the end. The exact
defect was reproduced before correction: for `F-EMA-001` with `N=6` the batch
value was `119.012361629366448787` while the incremental series value was
`119.012361629366448786`, a 1e-18 divergence, and the recursive state
fingerprints differed for EMA, ATR and RSI at every tested `N`.

Correction:

- `evaluate_feature` and `evaluate_feature_series` now run one shared
  incremental loop (`_evaluate_steps`); the batch entry point is defined as the
  final step of that same loop, so parity holds by construction rather than by
  coincidence;
- the SMA(N) EMA seed and the mean(first N TR) ATR seed are canonicalized to
  scale 18 before the first recursive update;
- every EMA and ATR recurrence step canonicalizes its new component to scale 18
  with `ROUND_HALF_EVEN`, and only that canonical value feeds the next update;
- RSI keeps its per-step canonical `avg_gain`/`avg_loss` recurrence and now
  shares one `_rsi_output` formulation with the batch path;
- the batch and series states now also agree on `previous_input`,
  `previous_close`, generation and environment identity.

Receipts: batch/series parity was verified across `N` in
`{3,4,5,6,7,8,9,11,14}` for EMA/ATR/RSI with zero remaining value or state
fingerprint divergences, and the same parity is now asserted inside the
deterministic benchmark for MICRO/NOMINAL/STRESS.

### IMP-H002 — recursive state identity and chain attestation

Correction:

- `RecursiveAccumulatorState` is `init=False` and evaluator-issued through a
  private attestation sentinel, mirroring the S1E `SequenceContinuityState`
  pattern; direct construction and `dataclasses.replace` forgery fail closed;
- state material now binds feature ID/version, feature fingerprint, source
  field, `N`, timeframe fingerprint and version, algorithm version, Decimal
  policy version, source, contract, environment and generation;
- `previous_state_fingerprint` binds the predecessor state and is `None` only
  for the canonical seed state;
- ordered input lineage, market-state lineage and authority lineage are retained
  and cross-checked for equal length and uniqueness, and
  `processed_samples == len(lineage)` is enforced;
- carried market-state trust, data-authority state, resource restriction,
  lifecycle restriction and authority evidence are folded forward by the state
  so a resume cannot widen any axis;
- `deserialize` returns an inert, unattested state whose self-fingerprint is
  recomputed (tampering is detected) but which cannot be resumed from;
- `restore_recursive_state` is the only governed re-attestation seam: it
  recomputes the canonical state from the exact ordered consumed inputs and
  accepts the serialized payload only when every material field, the ordered
  input and authority lineage and the predecessor-chain link agree.

Receipts: cross-source, cross-contract, cross-environment, cross-generation,
cross-timeframe and changed-`N` injection all fail closed; forged
`previous_state_fingerprint`, tampered component and cross-context payloads are
rejected by recomputation; a legitimate serialized chain re-attests and resumes
bit-for-bit.

### IMP-H003 — restored frozen axis separation

Correction:

- new typed read-only `FeatureAuthorityEvidence` carries the actual
  `MarketStateSnapshot` fingerprint, `MarketStateTrust`, `DataAuthorityState`
  with decision fingerprint and governed reasons, `ResourceDisposition` with its
  admission fingerprint, `LifecycleRestriction` and a material fingerprint;
- `FeatureAuthorityEvidence.from_market_state` derives that evidence from the
  canonical S1E snapshot plus the governed Module 29 `ResourceAdmissionEvidence`
  seam; absent resource evidence stays `UNKNOWN` rather than being assumed
  available, and no axis is synthesized from display strings;
- `FeatureValidity` now maps only market-truth conditions (trust states and
  governed `STALE`, `GAP`, `SEQUENCE_UNPROVABLE`, `CLOCK_UNTRUSTED`,
  `SCHEMA_QUARANTINED`, `UNSYNCHRONIZED`, `RETIRED_GENERATION`,
  `CROSS_CHANNEL_CONTRADICTION` reasons);
- `TRUSTED` + resource `DEGRADED`/`DENIED`/`UNKNOWN` yields
  `FeatureValidity.VALID` with `resource_restriction=RESTRICTIVE`;
  `TRUSTED` + lifecycle ineligible yields `FeatureValidity.VALID` with
  `lifecycle_restriction=RESTRICTIVE`; market-truth `DEGRADED` still yields
  `FeatureValidity.DEGRADED`;
- `FeatureValue`, `FeatureSnapshot` and `RecursiveAccumulatorState` fingerprints
  include the axis identities and authority evidence fingerprint without
  granting downstream authority; no feature path can upgrade trust, authority,
  resource or lifecycle;
- `FeatureSample.from_candle` no longer reuses
  `candle.context.provenance_fingerprint` as market-state identity; a
  non-REPLAY candle now requires the matching canonical `MarketStateSnapshot`
  (and resource evidence where applicable), validates source/contract/
  environment/generation consistency, and uses the real canonical state
  fingerprint;
- `FeatureSample.from_decimal` and the other synthetic scalar fixture
  constructors are REPLAY-only and reject `LIVE`, `PAPER` and `SHADOW`; a
  synthetic fixture authority can never travel on a non-REPLAY sample.

### IMP-H004 — derived window evidence is content-bound

Correction:

- `AlignedWindowEvidence` is `init=False` and evaluator-issued; only
  `align_closed_1m_candles` can emit `VALID`/`DEGRADED` evidence, and direct
  construction, `replace`-based forgery and material that disagrees with the
  constituents all fail closed;
- the evaluator recomputes first open, max high, min low, last close,
  native-quantity sum, lineage, source, contract, environment, generation,
  event/knowledge/wall times and `DERIVED_ANALYTICAL_V1` provenance from the
  exact ordered constituents;
- the fingerprint binds target timeframe/version, window start/end, derived
  times, ordered constituent fingerprints, constituent provenance fingerprints,
  ordered authority-axis evidence fingerprints and the restriction axes, so any
  constituent correction, revision, reorder or identity mutation changes it;
- `WARMUP`/`UNKNOWN`/`INVALID` evidence returned by the evaluator also binds the
  available constituents and the evaluation boundary deterministically;
- resource-degraded complete aligned evidence stays analytically `VALID` while
  carrying a separate restrictive resource axis.

## Exact-head CI receipt

- corrected implementation head: `4715b06fc1aafba87ead686655f5231d3f3f8b04`
- exact-head run: `35046100856`
- exact-head job: `104636126625`
- conclusion: `SUCCESS` on all 14 steps, including the corrected
  `Publish exact-head implementation summary` step, which now writes literal
  head/base/checkpoint/implementation values and asserts their presence
  (`Exact-head summary material verified for head/base/checkpoint/implementation: PASS`)
- no `command not found` lines remain in the exact-head step summary
- pull request `#74` remains `OPEN`, non-draft, `MERGEABLE`, unmerged, base
  `main@fecb97b6c9513a6dc0114d22c5e3768017411157`

## Proof obligations

| Obligation | Evidence | Result |
|---|---|---|
| PO-F01 | deterministic vectors, canonical recursive state, all eight IDs | PASS |
| PO-F02 | definition/parameter/input/lineage mutation fingerprints | PASS |
| PO-F03 | future event/knowledge and no-lookahead rejection | PASS |
| PO-F04 | exact warmup boundaries, first-valid cardinality, closed-input requirement | PASS |
| PO-F05 | UNKNOWN, INVALID and market-truth DEGRADED propagation | PASS |
| PO-F06 | generation and `LIVE/PAPER/SHADOW/REPLAY` namespace isolation | PASS |
| PO-F07 | 5m/15m close boundaries, incomplete and post-close states | PASS |
| PO-F08 | immutable registry and material version collision rejection | PASS |
| PO-F09 | derived analytical provenance with no downstream action surface | PASS |
| PO-F10 | full/replayed serialized recursive state equality | PASS |

The local S2A test file contains the named `test_po_f01` through `test_po_f10`
coverage plus the IMP-H001 to IMP-H004 adversarial matrix.

## Authority axis and upstream binding evidence

- non-fixture authority is derived only from `MarketStateSnapshot` and the
  Module 29 admission seam; `PAPER` candle samples without a canonical snapshot
  are rejected;
- `market_state_fingerprint` is the canonical S1E state fingerprint, proven
  distinct from `candle.context.provenance_fingerprint` by test;
- absent resource evidence resolves to `ResourceDisposition.UNKNOWN` and is
  carried as a restrictive axis, never as analytical invalidity;
- `LIVE`, `PAPER` and `SHADOW` synthetic fixture construction is rejected;
- S1E `market_truth.py` and the S1F value plane were consumed read-only and were
  not modified.

## Benchmark receipt

Mode: `S2A_BASELINE_ESTABLISHMENT_V1`
Runtime: Python 3.12 Decimal feature engine
Seed: `S2A-FIXTURE-SEED-V1`
Profiles remain exactly MICRO/NOMINAL/STRESS with the frozen cardinalities. The
memory number is a one-contract representative probe; these are baseline
measurements, not production SLOs or profitability claims.

| Profile | Contracts | Closed 1m/contract | Max window | Feature evals | Warmup | Restrictive | No-lookahead | Recursive parity |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| MICRO | 1 | 4,096 | 64 | 8 | 81 | 0 | 1 | PASS (0 mismatches) |
| NOMINAL | 16 | 8,192 | 256 | 128 | 1,296 | 0 | 16 | PASS (0 mismatches) |
| STRESS | 32 | 16,384 | 512 | 256 | 2,592 | 96 | 32 | PASS (0 mismatches) |

Input manifest hashes (unchanged from the pre-correction baseline):

- MICRO: `bc2140402cd5d4c7e4a1ea01aa2ddb456222e6fe4aa50b80c7d3647d15f54d1c`
- NOMINAL: `36db111043b1d16ea3f0cc8e5009e5bbeec887eed3f9a7074c059d1a80de09b6`
- STRESS: `9d42c12fdae774e147a54c312e709c904777050cc74e197ab68065cb1a931fa1`

Output manifest hashes (regenerated only after the corrected tests passed):

- MICRO: `5d5367a0b6a6769b276a3780cd4d068176fcd02b5e927318f3061f4f3c97e204`
- NOMINAL: `7a5cc38a7a9051476ea9f5ec1094227ceb05391998c4594eba8da3d05a58599a`
- STRESS: `91f1cdfcc88ad1e12bb1d61cca25e472da5cd72506fc7d5a298cf530bab0131e`

Recursive-path parity fingerprints:

- MICRO: `a941a0aa26c7ec86e919a4168492ad2118bb7d2c1df64a0dc9009e9f71f3ed6d`
- NOMINAL: `b2e4cb155704b7e282607acff068a296206fa395e358809e3342a37b4e3f9278`
- STRESS: `35ad4a699c7e1804f836440957a02c988583df4070081826937e4ded293d4b3e`

The deterministic profile projection (including `recursive_parity`,
`recursive_parity_fingerprint` and `recursive_parity_mismatches`) was identical
across two consecutive runs. STRESS exercised complete valid 15m alignment,
missing post-close constituent (`UNKNOWN`), corrected input fingerprint mutation
and mixed-generation (`INVALID`) evidence.

## Local validation receipt

- `python -m pytest -q apps/backend`: `361 passed`
- S2A feature tests: `60 passed`
- coverage: `90.59%` (gate `>= 90%`) over `5333` statements
- ruff check on S2A source/tests/scripts: PASS
- ruff format check on S2A source/tests/scripts: PASS
- mypy on backend source: `Success: no issues found in 17 source files`
- backend build: sdist and wheel built
- pip-audit: no known vulnerabilities
- S2A negative-capability scan: PASS
- S2A MICRO/NOMINAL/STRESS benchmark: PASS, deterministic projection equal
- frontend prior-stage gates: typecheck PASS, 13 tests PASS, lint PASS,
  generated-format PASS, build PASS, audit 0 vulnerabilities
- `git diff --check`: clean
- no frontend file changed

## Authorization firewall

The CP0033 authorization is bounded and non-trading:

- `implementation_authorized=true` for scope `HCT-IMP-0009-S2A` only;
- `implementation_authorization_ceiling=NON_TRADING_STAGE_2_DETERMINISTIC_FEATURE_INDICATOR_FOUNDATION_ONLY`;
- `production_credentials_authorized=false`;
- `production_deployment_authorized=false`;
- `limited_live_authorized=false`;
- `live_trading_authorized=false`.

Planning Freeze is not implementation authorization, and implementation
authorization is not live-trading authorization. Independent HIGH_ASSURANCE
review and separate governance acceptance remain mandatory. The implementation
PR must remain OPEN and UNMERGED after exact-head CI.

## Required stop condition

After the corrected implementation reaches a fresh exact-head s2a-quality
SUCCESS, stop. Do not self-approve, merge, promote CP0034, alter frozen
governance, add later modules, configure credentials, deploy, activate
limited-live or trade. The next mandatory action is a fresh independent
HIGH_ASSURANCE review of the final exact implementation head.
