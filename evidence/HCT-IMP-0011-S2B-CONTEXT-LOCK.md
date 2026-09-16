# HCT-IMP-0011-S2B — Fresh Post-CP0035 Context Lock

Status: `LOCKED_FOR_IMPLEMENTATION`
Risk: `HIGH_ASSURANCE`
Checkpoint: `HCT-CP-0035 / IMPLEMENTATION_AUTHORIZED_S2B`
Authorization: `HCT-IMPL-AUTH-0011 / PR #76 / Issue #75`
Implementation Issue: `#77`
Authorized scope: `HCT-IMP-0011-S2B only`
Authorization ceiling: `NON_TRADING_STAGE_2_CANDLESTICK_PATTERN_FOUNDATION_ONLY`
Author-side governance preflight: `AUTHOR_SIDE_GOVERNANCE_PREFLIGHT_NOT_INDEPENDENT_APPROVAL`

This Context Lock is the hard lifecycle gate between authorization and implementation. It is
captured against the exact post-CP0035 canonical main and binds every identity the
implementation is allowed to rely on. Any drift requires STOP and fresh governance review.

## Exact Git identity

- canonical main after CP0035 promotion: `9e6014472df7723b21f9a1d7ab2aa207ac714ccc`;
- implementation branch: `implementation/HCT-IMP-0011-S2B`;
- implementation base: `9e6014472df7723b21f9a1d7ab2aa207ac714ccc`;
- authorization merge commit consumed by CP0035: `1ed699b6e313d097a51dab21d1d40727e4dab850`;
- exact independently approved authorization head: `49935bacb6ba2f7a3a06dc864468a331feaa1588`;
- authorization base: `c198a99167fa571802b16f6daf77b253a2b100b0`.

## CP0035 identity

| Source | Blob |
|---|---|
| `checkpoints/history/HCT-CP-0035.json` | `4e7a67ddd196b4769734f1456e88ff5bce37ba30` |
| `checkpoints/workstreams/planning/latest.json` | `f5401dbbd5f4b3334ef713b075939d02f3e9ec18` |
| `docs/11-checkpoint.md` | `3029921016ed3bb93a2fbf5a2c944fc4c657290e` |
| `docs/137-s2b-implementation-authorization-and-checkpoint-promotion.md` | `e590ee6a20a4de64d6ed218514cc81bb10bc3e7c` |

`checkpoints/workstreams/planning/latest.json` moved from the CP0034 pointer to the CP0035
pointer as the expected canonical promotion update. No frozen planning artifact and no frozen
requirement source blob moved.

## Canonical Work Order and candidate identities

| Source | Blob |
|---|---|
| `work-orders/HCT-IMP-0011-S2B.md` | `205bbc21051f670c9a92bbacfb67a512bb544496` |
| `work-orders/HCT-IMPL-AUTH-0011.md` | `15d1ffa36e4e476544ac838a24d03beaddd5a646` |
| `docs/136-implementation-authorization-s2b-candidate.md` | `2075ffba83ccb0f6eb29d7d006d9ddc3166cf25d` |

## Frozen planning package (17 artifacts, `9/17` unchanged from the authorization lock)

| Source | Blob |
|---|---|
| `docs/00-source-hierarchy.md` | `a195814d7514e438f3a1c7ec3eded494595e4817` |
| `docs/03-scope.md` | `3ecc8d6c8d1540005dbd78b7e7569ccbd010f22a` |
| `docs/04-architecture.md` | `24f2e7c72de5a9c9b362fb5e34ebfd7bcc076725` |
| `docs/05-security.md` | `4f63f584ee7f169402c5609ead7aa64304248bc0` |
| `docs/06-test-benchmark-plan.md` | `29401ce8fe1616f9390a317bae62d3a157addaa5` |
| `docs/09-definition-of-done.md` | `53741dab7a3e3ebfaf1a61ef89b638cb97e17cb1` |
| `docs/10-decisions-ledger.md` | `98697c87928dce8f53f32e23e7fefb6acd3bb7d3` |
| `docs/14-product-module-map.md` | `f2e254e493ed27a31c4986f006e6455bc1b58c3e` |
| `docs/91-r11-integrated-authority-state-dependency-architecture.md` | `faa7d0fc35481a73e0c5ae204a80e57d4856ef61` |
| `docs/92-r11-v1-module-classification-and-integration-hardening.md` | `aea9d476a6cf14f0e9e58872a48094aeda2f154f` |
| `docs/99-r12-frozen-requirements-baseline.md` | `cdaf66eab10f650292908679efbb7d0ec400ebf9` |
| `docs/100-r12-requirements-traceability-and-no-loss-proof.md` | `2ef416b4ea06e2aaee8b3545e1022f3459f3d647` |
| `docs/101-r12-freeze-governance-change-control-and-deferred-decisions.md` | `5ec4003c577fc4875c5cad494e8877f731d3f943` |
| `docs/102-r12-freeze-acceptance-matrix.md` | `886703addb72f277033005ea33e80bfa5f007766` |
| `docs/103-r12-final-planning-freeze-audit.md` | `9748ac220bdf83faa4579bfe8c6856eb28895712` |
| `docs/105-r12-freeze-approval-and-checkpoint-promotion.md` | `b95db9084312efac70af7f2c4ef71f34c7ae6cd4` |
| `checkpoints/history/HCT-CP-0014.json` | `99c94f226b7beb454c946fb6eb0fc9628a54531f` |

## Frozen requirement source blobs (9/9 PASS)

| Requirement source | Blob |
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

## Read-only upstream runtime identities

| Upstream source | Blob |
|---|---|
| `apps/backend/src/hct_backend/features.py` | `40dba614d6a146c42fc7c4755416bcedd55a7f1c` |
| `apps/backend/src/hct_backend/feature_engine.py` | `a46bca1b82ce0d9b168af5cf7b34a06ee2ef5f38` |
| `apps/backend/src/hct_backend/market_truth.py` | `01cdb87eff460f1d6761625bf6a722a3a4432bf5` |
| `apps/backend/src/hct_backend/s1f_values.py` | `38620bc4ea4f1fc5b14cd525c7a9ca0251d9cbfd` |
| `apps/backend/src/hct_backend/s1f_numeric.py` | `76c74b1d746f74dfa0e0aac54a286584ab545cb8` |
| `apps/backend/src/hct_backend/contracts.py` | `76893452f6221316f8a41be0288bc7b9596c26b0` |

These are read-only. S2B consumes them and must not modify them. S2B may not restate S2A
feature semantics, S1E Market-State truth, S1F value evidence or DataAuthority ownership.

## Bound frozen S2B contract

- `S2B_PATTERN_ALLOWLIST=P-DC-001,P-MB-001,P-EC-001,P-EC-002,P-MS-001,P-ES-001`;
- `S2B_PATTERN_ALGORITHM_VERSION=S2B_STANDARD_CANDLESTICK_PATTERNS_V1`, `S2B_PATTERN_DEFINITION_VERSION=1`;
- `S2B_TIMEFRAME_IDENTITY=Min1:60:1:UNIX_EPOCH_MULTIPLES;Min5:300:1:UNIX_EPOCH_MULTIPLES;Min15:900:1:UNIX_EPOCH_MULTIPLES`;
- `S2B_PATTERN_DECIMAL_POLICY=FEATURE_DECIMAL_V1`, `S2B_PATTERN_BINARY_FLOAT=FORBIDDEN`;
- `S2B_CANDLE_ZERO_RANGE=VALIDITY_UNKNOWN_MATCH_INDETERMINATE`, `S2B_SMALL_BODY_MAX=0.10`, `S2B_LONG_BODY_MIN=0.90`;
- `S2B_CONSTITUENT_PAIR=EXACT_CANDLEBAR_PLUS_EVALUATOR_ISSUED_FEATURE_SAMPLE_FROM_SAME_CANDLE`, `S2B_PAIR_OPEN_SOURCE=CANDLEBAR_OPEN`;
- `S2B_AUTHORITY_SEAM=EVALUATOR_ISSUED_FEATURE_SAMPLE_FROM_CANDLE_AND_FEATURE_AUTHORITY_EVIDENCE`, `S2B_AXIS_FOLD=EXISTING_S2A_MOST_RESTRICTIVE`;
- `S2B_AXIS_SEPARATION=PatternValidity;MarketStateTrust;DataAuthority;ResourceRestriction;UniverseLifecycleRestriction`;
- `S2B_VALIDITY_FOLD_PRECEDENCE=INVALID>UNKNOWN>WARMUP>DEGRADED>VALID`, `S2B_RESOURCE_LIFECYCLE_DO_NOT_DOWNGRADE=TRUE`;
- `S2B_CANONICAL_EVALUATION_BOUNDARY=max(window_end,knowledge_time)`, `S2B_BOUNDARY_STORED=CANONICAL_NEVER_CALL_TIME`, `S2B_LATER_REEVALUATION=IDEMPOTENT_SAME_FINGERPRINT`;
- `S2B_FINGERPRINT_VERSION=S2B_SHA256_CANONICAL_JSON_V1`;
- `S2B_PATTERN_EVIDENCE_ISSUANCE=EVALUATOR_ISSUED_PRIVATE_ATTESTATION`, `S2B_PATTERN_EVIDENCE_FORGERY=FAIL_CLOSED`;
- `S2B_PATTERN_EVIDENCE_KEY=pattern_id;definition_version;source_id;contract_id;environment;generation;timeframe_fingerprint;window_start;window_end;ordered_constituent_candle_fingerprints`;
- `S2B_EVIDENCE_DUPLICATE_SUPPRESSION=NONE_IDEMPOTENT_BY_KEY`, `S2B_EVIDENCE_CONFLICT_POLICY=INDEPENDENT_NO_WINNER_NO_RANKING`, `S2B_REVISION_CHAIN=NO_SKIP_NO_FORK_NO_OVERWRITE`;
- `S2B_BENCHMARK_MODE=S2B_BASELINE_ESTABLISHMENT_V1`, `S2B_BENCHMARK_FIXTURE_VERSION=S2B_PATTERN_FIXTURE_V1`, `S2B_BENCHMARK_SEED=0`, `S2B_BENCHMARK_PROFILE_MICRO=1:2048`, `S2B_BENCHMARK_PROFILE_NOMINAL=8:4096`, `S2B_BENCHMARK_PROFILE_STRESS=16:8192`;
- proof obligations `S2B-PO-01` through `S2B-PO-21`;
- `S2B_NO_PREIMPLEMENTATION_IMPLEMENTATION_HEAD_REVIEW=TRUE`.

## Authorization state at this lock

- `implementation_authorized=true`;
- `implementation_authorization_scope=[HCT-IMP-0011-S2B]`;
- `implementation_authorization_ceiling=NON_TRADING_STAGE_2_CANDLESTICK_PATTERN_FOUNDATION_ONLY`;
- `production_credentials_authorized=false`;
- `production_deployment_authorized=false`;
- `limited_live_authorized=false`;
- `live_trading_authorized=false`.

## Implementation boundary

The implementation may change exactly eight files:
`.github/workflows/s2b-quality.yml`, `apps/backend/src/hct_backend/patterns.py`,
`apps/backend/src/hct_backend/pattern_engine.py`, `apps/backend/tests/test_patterns.py`,
`scripts/benchmark_s2b.py`, `scripts/scan_s2b_boundaries.py`,
`evidence/HCT-IMP-0011-S2B-CONTEXT-LOCK.md` and `evidence/HCT-IMP-0011-S2B.md`.

If one additional package-export file is objectively unavoidable, STOP BLOCKED and report the
exact import/export blocker instead of widening the boundary silently.

## Context Lock conclusion

`repositorySync=PASS`

`sourceMatch=PASS` — all seventeen frozen planning artifacts and all nine frozen requirement
source blobs match their recorded identities, with the CP0035 planning-pointer transition
explicitly accounted for and no other drift.

`contextLock=PASS`

The next permitted action is bounded Module 9 implementation of `HCT-IMP-0011-S2B` only, on
this branch. The implementation PR must remain OPEN and UNMERGED after exact-head CI and a
complete Evidence Bundle, and a fresh independent HIGH_ASSURANCE review of the exact
implementation head is required before any implementation merge.
