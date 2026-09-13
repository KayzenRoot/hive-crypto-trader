# HCT-IMPL-AUTH-0009 — S2A Deterministic Feature & Indicator Foundation Authorization

Status: `PENDING_INDEPENDENT_HIGH_ASSURANCE_REVIEW`
Risk: `HIGH_ASSURANCE`
Canonical base: `main@3ee5ad4d967bb6ef051eae1982990d728c6ade9e`
Current checkpoint: `HCT-CP-0032 / S1F_IMPLEMENTATION_APPROVED_MERGED`
Recompile marker: `RECOMPILED_AFTER_S1F`
Proposed implementation: `HCT-IMP-0009-S2A`
Authorization issue: `#68`
Governance branch: `governance/HCT-IMPL-AUTH-0009-S2A`

This is a governance-only authorization candidate. It authorizes no product implementation and does not promote a checkpoint.

## HISTORICAL CONTEXT AND PREREQUISITE RESOLUTION

The prior candidate was `BLOCKED_BY_PREREQUISITE` on historical base `625dd0c145087038bdbccd665548d811e187194c`, historical head `b697dd031aa0c09ef6f5b047dfe3095e542f1043`, PR #69 / Issue #68, because S1E lacked typed computable public market values.

`B001=RESOLVED_BY_HCT-IMP-0010-S1F_CP0032`.

HCT-IMP-0010-S1F was independently approved at head `01b87c36dd27c76782727f1394404647806c1414`, merged as `b6acfb2466dc537c3aeb84c525be3e9663f51db2`, and promoted by HCT-CP-0032. The S1F value plane, ADR, Work Order and evidence are read-only upstream sources. S2A cannot create a second market-truth owner.

## OBJECTIVE

Prepare and independently review the first bounded Module 8 (`V1_CORE`) dependency: a deterministic, provider-neutral, point-in-time Feature & Indicator Foundation. Freeze exact feature scope, Decimal behavior, ordered lineage, S1E/S1F authority-axis separation, benchmark profiles and proof obligations before any later implementation authorization.

R11 Stage 2 remains ordered `features/indicators/patterns -> regime -> scanner -> strategy engine/catalog/signal -> minimum microstructure`. Module 9 patterns remain separate.

## SCOPE

The candidate may define only:

- immutable typed `FeatureDefinition`/`FeatureVersion`, canonical registry identity and behavior fingerprints;
- immutable `FeatureValue`/`FeatureSnapshot` bound to source Market-State fingerprint/generation, contract, environment, DataAuthority/freshness evidence, event time, knowledge time, definition version, window and lineage;
- explicit `VALID`, `UNKNOWN`, `INVALID`, `WARMUP` and `DEGRADED` outcomes with fail-closed propagation;
- point-in-time windows, half-open close boundaries, sample count, completeness, ordering, timeframe and no-lookahead validation;
- deterministic multi-timeframe alignment using CLOSED S1F candles and admissible `knowledge_time`;
- exactly the eight frozen public/standard V1_CORE feature IDs: `F-RET-001`, `F-SMA-001`, `F-EMA-001`, `F-ROC-001`, `F-RSI-001`, `F-TR-001`, `F-ATR-001`, `F-VSMA-001`;
- fixture/replay-only evaluation, deterministic tests and evidence;
- a negative-capability scanner and pull-request-only exact-head governance workflow.

No feature may create a candidate action, scanner rank, strategy signal, Brain admission, Risk approval, Execution plan or live authority.

## OUT OF SCOPE

No runtime/product implementation, network or provider endpoint, socket/WebSocket/HTTP client, credentials, private API, signing, persistence, database/RLS, deployment or infrastructure topology is authorized. Also excluded are Module 9 patterns, regime, scanner/ranking, strategy/catalog/signal, microstructure, Brain, agents, RAG/memory, learning, calibration, Risk, Safety, Session Policy, sizing, leverage, OMS, Execution, reconciliation, protection, orders, positions, balances, fills, limited-live and live trading.

S1F Market-State/value contracts, `DataAuthority`, checkpoints, frozen requirements and dependency locks are read-only and may not be mutated by S2A.

## FILES/SOURCES TO READ

Before any future implementation, read the exact frozen files and canonical state: `docs/00-source-hierarchy.md`, `docs/02-requirements.md`, `docs/03-scope.md`, `docs/04-architecture.md`, `docs/06-test-benchmark-plan.md`, `docs/09-definition-of-done.md`, `docs/10-decisions-ledger.md`, `docs/11-checkpoint.md`, `docs/14-product-module-map.md`, `docs/48-r04-execution-requirements-addendum.md`, `docs/54-r05-realtime-requirements-addendum.md`, `docs/61-r06-intelligence-requirements-addendum.md`, `docs/67-r07-validation-laboratory-requirements-addendum.md`, `docs/73-r08-multitenant-security-requirements-addendum.md`, `docs/80-r09-cockpit-uiux-requirements-addendum.md`, `docs/87-r10-observability-audit-incident-finops-requirements-addendum.md`, `docs/91-r11-integrated-authority-state-dependency-architecture.md`, `docs/92-r11-v1-module-classification-and-integration-hardening.md`, `docs/93-r11-integration-requirements-addendum.md`, `docs/99-r12-frozen-requirements-baseline.md`, `docs/100-r12-requirements-traceability-and-no-loss-proof.md`, `docs/101-r12-freeze-governance-change-control-and-deferred-decisions.md`, `adr/HCT-ADR-0049-s1e-market-truth-foundation.md`, `adr/HCT-ADR-0050-s1f-realtime-public-market-value-ingest.md`, `work-orders/HCT-IMP-0010-S1F.md` and `evidence/HCT-IMP-0010-S1F.md`.

Canonical source identities for the S1F handoff are:

- `docs/06-test-benchmark-plan.md` — `29401ce8fe1616f9390a317bae62d3a157addaa5`;
- `checkpoints/history/HCT-CP-0032.json` — `f910b60f0b2dc3c046cac12795dca29a8b7aa3a2`;
- `checkpoints/workstreams/planning/latest.json` — `3a8ad6d6887cca478f1d999feb8ba15421b817a4`;
- `adr/HCT-ADR-0050-s1f-realtime-public-market-value-ingest.md` — `609ddc4656220027ce14503a6ba7ae71acc4c039`;
- `work-orders/HCT-IMP-0010-S1F.md` — `c9cf955dbb83c337760af3cff4d3136e32228319`;
- `evidence/HCT-IMP-0010-S1F.md` — `9061c9f072d8e111cda3d2983242fd6466e1101e`.

The nine frozen requirements remain bound to the identities in `docs/99-r12-frozen-requirements-baseline.md`, including `docs/02` `292da9552ae816e4d51b8a299456305da1658e55`, `docs/48` `f20c1ed00bdb13801aaff8a3b648371bfcffba58`, `docs/54` `636ad01da9c25e760dd5e2f033b93a0f04578a17`, `docs/61` `fea197e60532eb6ff3b11b628b9aabcbcfc00c41`, `docs/67` `c8a426966c5a0dc34704d1413f506332e770c2c7`, `docs/73` `c859c0c4a718e3017c34aa50013d4c50959853b4`, `docs/80` `bc897ebd470857a53055bdee85128b5bd31a5822`, `docs/87` `023187ef23b01d5a11f978bbfe6e38abf172bb3b` and `docs/93` `6935e9973696d5b706546d63d847ea398780d936`.

## NORMATIVE FEATURE AND NUMERIC LOCK

`S2A_EXACT_V1_CORE_FEATURE_SET=F-RET-001,F-SMA-001,F-EMA-001,F-ROC-001,F-RSI-001,F-TR-001,F-ATR-001,F-VSMA-001`

`FEATURE_DECIMAL_POLICY_VERSION=FEATURE_DECIMAL_V1`

`FEATURE_DECIMAL_INTERNAL_PRECISION=76`

`FEATURE_DECIMAL_MAX_PRECISION=38`

`FEATURE_DECIMAL_MAX_SCALE=18`

`FEATURE_DECIMAL_ROUNDING=ROUND_HALF_EVEN`

`FEATURE_DECIMAL_BINARY_FLOAT=FORBIDDEN`

Non-finite values, binary floats at authoritative boundaries, invalid denominators, overflow, impossible OHLC, mixed units and unsupported operations fail closed. Exact operations are not rounded for convenience. Non-terminating feature operations quantize final canonical output to scale 18 with `ROUND_HALF_EVEN`; policy, seed, N/window, source field, timeframe, version and rounding mode are fingerprint-visible.

## ARCHITECTURE RULES

1. S1F typed values and S1E Market-State/DataAuthority are read-only upstream inputs; no second truth owner or authority upgrade is allowed.
2. Definition, version, registry, input-lineage and output fingerprints are deterministic and mutation-complete; canonical IDs cannot be silently redefined.
3. Both event time and `knowledge_time` are checked against the declared point-in-time boundary; later knowledge cannot populate an earlier feature.
4. `UNKNOWN`, `INVALID`, `WARMUP` and `DEGRADED` are restrictive typed outcomes, never null/default/zero aliases.
5. Windows are UTC half-open `[start,end)`, CLOSED-only for candle-derived features, and mixed source/contract/environment/generation/timeframe fails closed.
6. `LIVE`, `PAPER`, `SHADOW` and `REPLAY` are non-aliasing environment identities; replay cannot gain live mutation capability.
7. Feature evidence is analytical only and cannot create scanner, strategy, Brain, Risk, Execution or live authority.
8. The implementation remains provider-neutral, persistence-free and network-free; only deterministic fixtures/replay are allowed.

## REQUIREMENTS AND TRACEABILITY

Every future behavior/test must trace to applicable frozen locators: `REQ02::Trading intelligence requirements::B1`, `B7`, `B8`; `R05::Time and freshness requirements::B1-B5`; `R05::State coherency requirements::B1-B4`; `R05::Candle/cache/replay requirements::B1-B5`; `R05::Universe lifecycle requirements::B1-B2`; `R05::Authority requirements::B1-B3`; applicable `R05::Validation requirements::B2`, `B3`, `B6`, `B8`, `B9`, `B10`, `B13`, `B15`, `B17`; `INT-002`, `INT-003`, `INT-004`, `INT-011`, `INT-012`, `INT-018`, `INT-022`, `INT-024`, `INT-025`, `INT-026`; `VAL-003`, `VAL-005`, `VAL-006`, `VAL-011`, `VAL-012`, `VAL-013`, `VAL-023`, `VAL-028`, `VAL-030`; `R11-REQ-006`, `R11-REQ-007`, `R11-REQ-011`, `R11-REQ-012`, `R11-REQ-013`, `R11-REQ-014`, `R11-REQ-015`, `R11-REQ-020`, `R11-REQ-022`, `R11-REQ-024`, `R11-REQ-025`; `HCT-DEC-0007`, `HCT-DEC-0008`, `HCT-DEC-0012`, `HCT-DEC-0058`, `HCT-DEC-0060` through `HCT-DEC-0065`, `HCT-DEC-0068`, `HCT-DEC-0069`, `HCT-DEC-0071`, `HCT-DEC-0074`, `HCT-DEC-0077`, `HCT-DEC-0079`, `HCT-DEC-0083`, `HCT-DEC-0084`, `HCT-DEC-0089`, `HCT-DEC-0135`, `HCT-DEC-0136`, `HCT-DEC-0138`, `HCT-DEC-0139`, `HCT-DEC-0140`, `HCT-DEC-0141`; and ADR-0049 deterministic safety rules/explicit non-scope.

## ACCEPTANCE CRITERIA

- `B001` is materially resolved by the typed S1F public market-value plane and CP0032 merge;
- exact canonical base is `3ee5ad4d967bb6ef051eae1982990d728c6ade9` and CP0032 is fail-closed;
- the future implementation is restricted to the eight feature IDs and `FEATURE_DECIMAL_V1`;
- no-lookahead, warmup, stale/untrusted/unknown/degraded propagation, lineage and multi-timeframe boundaries are explicit;
- axis separation preserves `FeatureValidity`, `MarketStateTrust`, `DataAuthority`, resource restriction and Universe/lifecycle restriction;
- the S2A benchmark method defines fixed MICRO/NOMINAL/STRESS profiles, measurements, reproducibility and no production SLO claim;
- exact governance CI validates base, CP0032 flags, source hashes, four-file allowlist, markers and negative scope;
- PR #69 remains OPEN and UNMERGED for fresh independent HIGH_ASSURANCE review.

## TESTS AND PROOF OBLIGATIONS

The future implementation Work Order must predefine `PO-F01` through `PO-F10`: deterministic equal-input output; mutation-complete fingerprinting; future event/knowledge/correction/label rejection; warmup fail closed; stale/expired/untrusted/contradictory/unknown propagation; generation/environment isolation; multi-timeframe close boundaries; registry immutability/versioning; non-authority; and replay fidelity.

Mandatory adversarial/property/golden tests cover all eight feature IDs, zero denominator, exact rounding, warmup, boundary ties, corrections, no-lookahead, ordered-lineage mutation, `TRUSTED+RESOURCE_DEGRADED`, `TRUSTED+INELIGIBLE`, mixed generation, replay hash equality, axis separation and `LIVE/PAPER/SHADOW/REPLAY` non-aliasing.

`S2A_BENCHMARK_MODE=S2A_BASELINE_ESTABLISHMENT_V1` with fixed profiles:

- `MICRO`: 1 contract, 4096 CLOSED 1m candles, max window 64;
- `NOMINAL`: 16 contracts, 8192 CLOSED 1m candles per contract, max window 256;
- `STRESS`: 32 contracts, 16384 CLOSED 1m candles per contract plus deterministic 5m/15m alignment, max window 512.

Measurements include evaluations/second, feature latency p50/p95/p99/max, replay throughput, peak/steady memory, window-buffer depth, warmup/restrictive propagation, no-lookahead rejections and output-manifest hash. Acceptance is correctness, deterministic same-input hash, bounded completion and bounded memory; no profitability or production SLO is claimed.

## DELIVERABLES

- one governance candidate document, this authorization Work Order and one implementation Work Order;
- one exact-head pull-request-only governance workflow;
- author-side evidence labeled `AUTHOR_SIDE_GOVERNANCE_PREFLIGHT_NOT_INDEPENDENT_APPROVAL`;
- PR #69 and Issue #68 preserved and updated in place only after the four-file recompile;
- no S2A product/runtime code, checkpoint promotion or implementation authorization.

## REVIEW FORMAT

The independent review must report `repositorySync`, `sourceMatch`, `canonicalMain`, `checkpoint`, `B001`, `candidateAuthorizationId`, `candidateImplementationId`, `exactFeatureSet`, `numericPolicy`, `orderedLineage`, `axisSeparation`, `benchmarkContract`, `changedFiles`, `governanceOnlyDiff`, `exactHeadRun`, `exactHeadJob`, `exactHeadConclusion`, `criticalFindings`, `highFindings`, `candidatePrOpenUnmerged`, `implementationAuthorized`, `productionCredentials`, `productionDeployment`, `limitedLive`, `liveTrading` and `stopConditionRespected`.

## AUTHORIZATION FIREWALL

`implementation_authorized=false`

`implementation_authorization_scope=[]`

`implementation_authorization_ceiling=NONE_PENDING_NEXT_GOVERNED_AUTHORIZATION`

`production_credentials_authorized=false`

`production_deployment_authorized=false`

`limited_live_authorized=false`

`live_trading_authorized=false`

PLANNING_FREEZE is not IMPLEMENTATION_AUTHORIZATION. IMPLEMENTATION_AUTHORIZATION is not LIVE_TRADING_AUTHORIZATION. This candidate, an open PR, green governance CI or independent approval cannot change the firewall.

## STOP CONDITION

Keep PR #69 OPEN and UNMERGED after exact-head governance CI and author-side evidence. Do not merge it, promote an S2A checkpoint, implement S2A, modify S1F, change frozen sources, add dependency/runtime/product files, deploy, configure credentials, call private APIs, activate limited-live or trade. Fresh independent HIGH_ASSURANCE review is mandatory.
