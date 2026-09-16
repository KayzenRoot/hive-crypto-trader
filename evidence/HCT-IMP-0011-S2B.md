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

## Bounded implementation

The slice implements the first Module 9 `V1_MINIMUM` foundation:

- immutable `PatternDefinition`/`PatternVersion` with material fingerprints and a persistent
  `PatternRegistry` that rejects silent redefinition and version collision;
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
- the canonical evaluation boundary `max(window_end, knowledge_time)` with idempotent later
  re-evaluation and the canonical evidence identity, duplicate idempotency, overlap/conflict
  coexistence, deterministic sequence order and immediate predecessor chain;
- evaluator-issued `PatternEvidence` with a private attestation and canonical fingerprint v1.

No transport, provider endpoint, credential, private API, persistence, downstream decision,
deployment or live authority is present in this slice.

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
| S2B-PO-17 | evaluator-issued attestation, direct construction, `replace`/tamper and caller-selected fields rejection | PASS |
| S2B-PO-18 | local `PatternValidity` axis with the superseded marker rejected | PASS |
| S2B-PO-19 | canonical boundary and idempotent later re-evaluation | PASS |
| S2B-PO-20 | duplicate, overlap, conflict, canonical ordering and no-winner semantics | PASS |
| S2B-PO-21 | immediate predecessor chain with no skip, fork or overwrite | PASS |

## Local validation receipt

- `python -m pytest -q apps/backend`: `430 passed`
- S2B pattern tests: `39 passed`
- global coverage: `90.37%` (gate `>= 90%`); `patterns.py` coverage `91%`
- ruff check on S2B source/tests/scripts: PASS
- ruff format check on S2B source/tests/scripts: PASS
- strict mypy on backend source: `Success: no issues found in 19 source files`
- backend sdist/wheel build: PASS
- pip-audit: no known vulnerabilities
- S2B negative-capability scan: PASS
- frontend prior-stage gates: typecheck PASS, `13 passed`, lint PASS, generated-format PASS, build PASS, `npm audit` 0 vulnerabilities
- `git diff --check`: clean
- no frontend file changed

## Benchmark receipt

Mode: `S2B_BASELINE_ESTABLISHMENT_V1`
Fixture: `S2B_PATTERN_FIXTURE_V1`, seed `0`, no network, no uncontrolled randomness.
Runtime: Python 3.12 Decimal pattern engine.

The frozen profile cardinality fixes the corpus; pattern evaluation runs over a deterministic
bounded sample of that corpus with the recorded stride, so these are baseline measurements and
not product SLOs.

| Profile | Contracts | Closed pairs/contract/timeframe | Stride | Windows | Evaluations | Eval/s | Replay pairs/s | Peak bytes | Depth |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| MICRO | 1 | 2048 | 4 | 1536 | 9,234 | 329.13 | 218.99 | 8,040,027 | 3 |
| NOMINAL | 8 | 4096 | 8 | 12288 | 73,872 | 389.05 | 517.72 | 15,972,416 | 3 |
| STRESS | 16 | 8192 | 16 | 24576 | 148,320 | 194.60 | 515.92 | 32,024,013 | 3 |

Validity and match counts:

| Profile | `VALID` | `DEGRADED` | `WARMUP` | `UNKNOWN` | `INVALID` | `MATCHED` | `NOT_MATCHED` | `INDETERMINATE` | No-lookahead rejections |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| MICRO | 6,156 | 0 | 18 | 3,060 | 0 | 1,020 | 5,136 | 3,078 | 18 |
| NOMINAL | 49,104 | 0 | 144 | 24,624 | 0 | 8,136 | 40,968 | 24,768 | 144 |
| STRESS | 98,784 | 288 | 288 | 48,960 | 0 | 16,416 | 82,656 | 49,248 | 288 |

Input manifest hashes:

- MICRO: `64199221cee04bb2afea125a1cd17ce5efc62ad610097926bb4ddebba27eba1f`
- NOMINAL: `b18ece1e957fb0ca49b25f93668a87f37ce041040d2b37da8797d943e2682638`
- STRESS: `00152ae58bfefe7f2ab7f77302e681f1312a1d96eef0e21b078902d4f1873553`

Output manifest hashes:

- MICRO: `0b5f7c458942c2444fbf2cc82e4ea35fce5dbd744b6c6d2e740cb2e6d7e0cc06`
- NOMINAL: `ad084d56ddbed82486c43422f40dc2da344ab5d84cf6febec9018332298755dc`
- STRESS: `d163aaa2d7a33e394f025c8cbf4b4e9a6c81018a1bd6b8d77fb74ae6464afcf9`

Two consecutive runs produced an identical deterministic projection, and the validator
confirmed exact profiles, frozen cardinalities, no-lookahead rejections and replay hash parity
across both runs. STRESS additionally exercised the adversarial corpus: mixed identity,
resource-degraded and lifecycle-restricted constituents and degraded market truth.

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
independent approval is claimed. The next mandatory action is a fresh independent
HIGH_ASSURANCE review of the exact implementation head.
