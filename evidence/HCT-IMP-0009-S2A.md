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
- final implementation head: recorded by the exact-head pull request CI and PR metadata
- source context lock: `evidence/HCT-IMP-0009-S2A-CONTEXT-LOCK.md`
- frozen source identities: 9/9 PASS
- prior-stage regression suite: `319 passed`

The execution base is the post-CP0033 `main` commit. No governance, checkpoint,
work-order, frozen-source, dependency-lock, S1E or S1F source was changed by
this implementation slice.

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

## Proof obligations

| Obligation | Evidence | Result |
|---|---|---|
| PO-F01 | deterministic vectors, canonical recursive state, all eight IDs | PASS |
| PO-F02 | definition/parameter/input/lineage mutation fingerprints | PASS |
| PO-F03 | future event/knowledge and no-lookahead rejection | PASS |
| PO-F04 | exact warmup boundaries and closed-input requirement | PASS |
| PO-F05 | UNKNOWN, INVALID and RESOURCE_DEGRADED propagation | PASS |
| PO-F06 | generation and `LIVE/PAPER/SHADOW/REPLAY` namespace isolation | PASS |
| PO-F07 | 5m/15m close boundaries, incomplete and post-close states | PASS |
| PO-F08 | immutable registry and material version collision rejection | PASS |
| PO-F09 | derived analytical provenance with no downstream action surface | PASS |
| PO-F10 | full/replayed serialized recursive state equality | PASS |

The local S2A test file contains the named `test_po_f01` through `test_po_f10`
coverage and the full backend suite passed with 319 tests.

## Benchmark receipt

Mode: `S2A_BASELINE_ESTABLISHMENT_V1`
Runtime: Python 3.12 Decimal feature engine
Seed: `S2A-FIXTURE-SEED-V1`
All eight features were evaluated over an authorized bounded buffer. The
memory number is a one-contract representative probe for each profile; the
throughput measurement covers the complete profile cardinality. These are
baseline measurements, not production SLOs or profitability claims.

| Profile | Contracts | Closed 1m/contract | Max window | Feature evals | Eval/s | Replay candles/s | Peak bytes | Warmup | Restrictive | No-lookahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| MICRO | 1 | 4,096 | 64 | 8 | 8.0693 | 4,131.47 | 255,174 | 81 | 0 | 1 |
| NOMINAL | 16 | 8,192 | 256 | 128 | 15.9427 | 16,325.29 | 820,137 | 1,296 | 0 | 16 |
| STRESS | 32 | 16,384 | 512 | 256 | 10.9533 | 22,432.32 | 1,615,603 | 2,592 | 96 | 32 |

Input manifest hashes:

- MICRO: `bc2140402cd5d4c7e4a1ea01aa2ddb456222e6fe4aa50b80c7d3647d15f54d1c`
- NOMINAL: `36db111043b1d16ea3f0cc8e5009e5bbeec887eed3f9a7074c059d1a80de09b6`
- STRESS: `9d42c12fdae774e147a54c312e709c904777050cc74e197ab68065cb1a931fa1`

Output manifest hashes:

- MICRO: `9bc2aa8eaeedcc1a4287624d5b407aa30e9443d871cb55c91bf56c63184178a3`
- NOMINAL: `9c085fb81a81c030bcb9fc992c9a9456a0ed8fa4b90444c03a5b329ee1c1b59c`
- STRESS: `87cd6974c0fd1e6587bafb1eca824dc1333b1f115f113dce27a549541c4f2bd4`

All three profiles returned `correctness=PASS` and `bounded_completion=true`.
STRESS exercised complete valid 15m alignment, missing post-close constituent
(`UNKNOWN`), corrected input fingerprint mutation and mixed-generation
(`INVALID`) evidence.

## Local validation receipt

- `python -m pytest -q apps/backend`: `319 passed`
- S2A feature tests: `18 passed`
- ruff check on changed S2A source/tests/scripts: PASS
- ruff format check on changed S2A source/tests/scripts: PASS
- mypy on backend source: `Success: no issues found in 17 source files`
- S2A negative-capability scan: PASS
- S2A MICRO/NOMINAL/STRESS benchmark: PASS
- frontend prior-stage gates: typecheck PASS, 13 tests PASS, lint PASS, format PASS, build PASS, audit 0 vulnerabilities
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

After the implementation PR is opened and its exact-head CI succeeds, stop.
Do not self-approve, merge, promote CP0034, alter frozen governance, add later
modules, configure credentials, deploy, activate limited-live or trade.
