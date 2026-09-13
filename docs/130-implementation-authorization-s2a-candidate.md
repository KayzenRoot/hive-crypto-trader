# HCT-IMPL-AUTH-0009 — S2A Deterministic Feature & Indicator Foundation Authorization Candidate

Status: `PENDING_INDEPENDENT_HIGH_ASSURANCE_REVIEW`
Risk: `HIGH_ASSURANCE`
Canonical base: `main@3ee5ad4d967bb6ef051eae1982990d728c6ade9e`
Current checkpoint: `HCT-CP-0032 / S1F_IMPLEMENTATION_APPROVED_MERGED`
Recompile marker: `RECOMPILED_AFTER_S1F`
Proposed authorization increment: `HCT-IMPL-AUTH-0009`
Proposed implementation slice: `HCT-IMP-0009-S2A`
Scope name: `Deterministic Feature & Indicator Foundation`
Authorization Issue: `#68`
Governance branch: `governance/HCT-IMPL-AUTH-0009-S2A`

This document is a governance-only authorization candidate. It does not implement product/runtime code, authorize implementation, promote a checkpoint, grant credentials or grant any live authority.

## Historical blocked candidate and resolved prerequisite

The prior candidate was intentionally retained OPEN and UNMERGED with `BLOCKED_BY_PREREQUISITE`:

- historical base: `main@625dd0c145087038bdbccd665548d811e187194c`;
- historical candidate head: `b697dd031aa0c09ef6f5b047dfe3095e542f1043`;
- historical checkpoint: `HCT-CP-0030 / S1E_IMPLEMENTATION_APPROVED_MERGED`;
- PR / Issue: `#69 / #68`;
- blocker: `B001` — S1E did not expose a typed computable public market-value plane for deterministic analytics;
- historical exact S2A governance CI: run `34754584478`, job `103716700210`, completed/success.

`B001=RESOLVED_BY_HCT-IMP-0010-S1F_CP0032`.

The resolved prerequisite is `HCT-IMP-0010-S1F`, merged in implementation merge `b6acfb2466dc537c3aeb84c525be3e9663f51db2` from independently approved head `01b87c36dd27c76782727f1394404647806c1414`. S1F artifacts are read-only upstream contracts; S2A cannot create a second market-truth owner.

## Objective

Prepare and independently review the smallest necessary next dependency after the completed S1F Market Truth/value plane: a deterministic, provider-neutral, point-in-time Feature & Indicator Foundation for Module 8 (`V1_CORE`). The candidate freezes exact feature scope, decimal semantics, ordered lineage, authority-axis separation, benchmark method and proof obligations before any future implementation authorization.

Module 9 candlestick/chart patterns (`V1_MINIMUM`) remains separate. Regime, scanner, strategy, signal, microstructure, Brain, Risk, Safety, Session Policy, OMS and Execution remain later governed owners.

## Source lock and provenance

The candidate is bound to the post-CP0032 canonical `main@3ee5ad4d967bb6ef051eae1982990d728c6ade9e` and the following exact sources:

- `checkpoints/history/HCT-CP-0032.json` — `f910b60f0b2dc3c046cac12795dca29a8b7aa3a2`;
- `checkpoints/workstreams/planning/latest.json` — `3a8ad6d6887cca478f1d999feb8ba15421b817a4`;
- `docs/06-test-benchmark-plan.md` — `29401ce8fe1616f9390a317bae62d3a157addaa5`;
- `adr/HCT-ADR-0050-s1f-realtime-public-market-value-ingest.md` — `609ddc4656220027ce14503a6ba7ae71acc4c039`;
- `work-orders/HCT-IMP-0010-S1F.md` — `c9cf955dbb83c337760af3cff4d3136e32228319`;
- `evidence/HCT-IMP-0010-S1F.md` — `9061c9f072d8e111cda3d2983242fd6466e1101e`;
- S1F typed values — `apps/backend/src/hct_backend/s1f_values.py` — `38620bc4ea4f1fc5b14cd525c7a9ca0251d9cbfd`;
- S1F numeric policy — `apps/backend/src/hct_backend/s1f_numeric.py` — `76c74b1d746f74dfa0e0aac54a286584ab545cb8`;
- S1F session — `apps/backend/src/hct_backend/s1f_session.py` — `ca3c572e6f4eb0f6921b6c3f602dbc571fabab6f`;
- S1F source decoder — `apps/backend/src/hct_backend/s1f_mexc.py` — `48e90d8c29f77ee4c702057b8c737715a55f124e`.

The nine frozen requirement source identities remain unchanged: `docs/02-requirements.md` `292da9552ae816e4d51b8a299456305da1658e55`; `docs/48-r04-execution-requirements-addendum.md` `f20c1ed00bdb13801aaff8a3b648371bfcffba58`; `docs/54-r05-realtime-requirements-addendum.md` `636ad01da9c25e760dd5e2f033b93a0f04578a17`; `docs/61-r06-intelligence-requirements-addendum.md` `fea197e60532eb6ff3b11b628b9aabcbcfc00c41`; `docs/67-r07-validation-laboratory-requirements-addendum.md` `c8a426966c5a0dc34704d1413f506332e770c2c7`; `docs/73-r08-multitenant-security-requirements-addendum.md` `c859c0c4a718e3017c34aa50013d4c50959853b4`; `docs/80-r09-cockpit-uiux-requirements-addendum.md` `bc897ebd470857a53055bdee85128b5bd31a5822`; `docs/87-r10-observability-audit-incident-finops-requirements-addendum.md` `023187ef23b01d5a11f978bbfe6e38abf172bb3b`; `docs/93-r11-integration-requirements-addendum.md` `6935e9973696d5b706546d63d847ea398780d936`.

Required governance/integration sources include `docs/00-source-hierarchy.md`, `docs/03-scope.md`, `docs/04-architecture.md`, `docs/09-definition-of-done.md`, `docs/10-decisions-ledger.md`, `docs/11-checkpoint.md`, `docs/14-product-module-map.md`, `docs/91-r11-integrated-authority-state-dependency-architecture.md`, `docs/92-r11-v1-module-classification-and-integration-hardening.md`, `docs/99-r12-frozen-requirements-baseline.md`, `docs/100-r12-requirements-traceability-and-no-loss-proof.md`, `docs/101-r12-freeze-governance-change-control-and-deferred-decisions.md` and the S1F ADR/evidence above.

## Dependency proof and read-only upstream boundary

R11 Stage 2 remains ordered:

`features/indicators/patterns -> regime -> scanner -> strategy engine/catalog/signal -> minimum microstructure`.

S1F now supplies typed `TradeTick`, `TickerState`, `CandleBar`, `OrderBookSnapshot`, `OrderBookDelta`, `ReferencePriceEvidence` and `FundingEvidence` with Decimal values, immutable fingerprints, source/contract/environment/generation/time identity, knowledge-time admissibility and authority evidence. S2A consumes these S1F contracts and S1E `MarketStateTrust`/`DataAuthority` read-only. It may not recalculate, mutate, upgrade or replace market truth.

`S2A_UPSTREAM_MARKET_TRUTH=HCT-IMP-0010-S1F_READ_ONLY`

`B001=RESOLVED_BY_HCT-IMP-0010-S1F_CP0032`

## Exact V1_CORE feature allowlist

Only these eight public/standard deterministic feature IDs are in this candidate:

| ID | Family | Frozen definition boundary |
|---|---|---|
| `F-RET-001` | Simple return | `close_t / close_t-1 - 1`; `WARMUP` until prior closed value exists |
| `F-SMA-001` | Simple moving average | Arithmetic mean of N closed prices |
| `F-EMA-001` | Exponential moving average | `alpha=2/(N+1)`; deterministic seed is `SMA(N)` |
| `F-ROC-001` | Rate of change | `(close_t - close_t-N) / close_t-N`; zero denominator is `INVALID` |
| `F-RSI-001` | RSI Wilder | N-period Wilder gain/loss smoothing; default fixture reference N=14 |
| `F-TR-001` | True range | `max(high-low, abs(high-prev_close), abs(low-prev_close))` |
| `F-ATR-001` | ATR Wilder | Wilder-smoothed True Range with deterministic N and seed |
| `F-VSMA-001` | Volume SMA | SMA over `CONTRACTS_PROVIDER_NATIVE_V1` only; no base-asset normalization |

`S2A_EXACT_V1_CORE_FEATURE_SET=F-RET-001,F-SMA-001,F-EMA-001,F-ROC-001,F-RSI-001,F-TR-001,F-ATR-001,F-VSMA-001`

Everything else is deferred: MACD, Bollinger Bands, stochastic, ADX/DMI, pivots, support/resistance, patterns, regime, scanner, strategy, proprietary indicators, funding/basis/OI composites, microstructure, Module 9 and all authority-producing consumers.

## Derived numeric semantics

`FEATURE_DECIMAL_POLICY_VERSION=FEATURE_DECIMAL_V1`

`FEATURE_DECIMAL_INTERNAL_PRECISION=76`

`FEATURE_DECIMAL_MAX_PRECISION=38`

`FEATURE_DECIMAL_MAX_SCALE=18`

`FEATURE_DECIMAL_ROUNDING=ROUND_HALF_EVEN`

`FEATURE_DECIMAL_BINARY_FLOAT=FORBIDDEN`

`FEATURE_DECIMAL_NONFINITE=FORBIDDEN`

Feature inputs are S1F Decimal values only. Exact operations that fit the bounds are not rounded for convenience. Mathematically non-terminating division/smoothing quantizes only the final canonical output to scale 18 with `ROUND_HALF_EVEN`; the policy, N/window, seed, source field, timeframe, version and rounding mode are fingerprint-visible. Overflow, invalid denominator, impossible input, mixed units, missing input or unsupported operation produces restrictive typed validity, never zero/default/NaN/Infinity.

Serialization is base-10 with no exponent, no leading plus, canonical zero and deterministic trailing-zero normalization. `FEATURE_DECIMAL_V1` is behaviorally material registry identity.

## Ordered lineage, windows and point-in-time rules

- Every `FeatureValue`/`FeatureSnapshot` carries an ordered manifest of exact S1F input fingerprints; insert, delete, reorder, correction, revision, generation or value mutation changes the manifest and output fingerprint.
- Windows are UTC half-open `[start,end)`, start-inclusive/end-exclusive, aligned to Unix epoch multiples, and candle-derived features consume CLOSED inputs only.
- `knowledge_time` is the point-in-time admissibility boundary; an input learned after the evaluation boundary is forbidden even when its event time is earlier.
- A window identity includes source, contract, environment, generation, timeframe/version, start/end, ordered inputs, sample count, required warmup, definition/version and replay-fidelity identity.
- Mixed contract/environment/generation/timeframe version fails closed.
- 5m/15m alignment may consume only complete CLOSED constituent 1m windows whose `knowledge_time` is admissible by the higher-timeframe boundary; open/incomplete windows remain `WARMUP`/`UNKNOWN`.
- Corrections create new immutable input lineage and new feature fingerprints; earlier point-in-time results remain reproducible.

## S1E/S1F authority-axis separation

`S2A_AXIS_SEPARATION=FeatureValidity;MarketStateTrust;DataAuthority;ResourceRestriction;UniverseLifecycleRestriction`

`FeatureValidity` is derived only from market-truth quality, completeness, lineage, numeric invariants, time admissibility and warmup. `MarketStateTrust`, `DataAuthority`, resource restriction and Universe/lifecycle restriction remain separate typed fields. A feature cannot upgrade any upstream axis.

`TRUSTED+RESOURCE_DEGRADED=FeatureValidity:VALID;resource_restriction:RESTRICTIVE`

`TRUSTED+INELIGIBLE=FeatureValidity:VALID;lifecycle_restriction:RESTRICTIVE`

`UNKNOWN/INVALID/WARMUP/DEGRADED=NO_UPGRADE`

`STALE`, `GAP`, `SEQUENCE_UNPROVABLE`, `CLOCK_UNTRUSTED`, `RESYNC_REQUIRED`, schema quarantine, contradictory truth, retired generation or missing authoritative value cannot produce normal `VALID` evidence. No aggregate score, fallback, resource admission, eligibility status or later module can turn `UNKNOWN`/`INVALID`/`WARMUP`/`DEGRADED` into unrestricted `VALID`.

## Bounded benchmark contract

`S2A_BENCHMARK_MODE=S2A_BASELINE_ESTABLISHMENT_V1`

- `MICRO`: 1 contract, 4096 CLOSED 1m candles, all authorized features, max window 64;
- `NOMINAL`: 16 contracts, 8192 CLOSED 1m candles per contract, all authorized features, max window 256;
- `STRESS`: 32 contracts, 16384 CLOSED 1m candles per contract plus deterministic 5m/15m closed-window alignment, all authorized features, max window 512.

Measurements are feature evaluations/second, per-feature compute latency p50/p95/p99/max, replay throughput, peak/steady memory, window-buffer depth, warmup counts, restrictive-state propagation counts, no-lookahead rejection counts and deterministic output-manifest hash. Acceptance is correctness, deterministic same-input hash, bounded completion and bounded memory/window growth. Record hardware/runtime/seed/source fixture identity. No profitability or production SLO claim is made.

## Required proof obligations and tests

- `PO-F01` through `PO-F10` remain mandatory: determinism, mutation-complete fingerprinting, no-lookahead, warmup fail-closed behavior, trust propagation, generation/environment isolation, multi-timeframe boundaries, registry immutability/versioning, non-authority and replay fidelity.
- Add golden vectors for all eight feature IDs, including zero denominator, warmup, boundary ties, corrections and exact rounding cases.
- Add property tests for ordered-lineage mutation, no-lookahead, point-in-time knowledge and same-input hash reproducibility.
- Add the axis-separation matrix as adversarial tests, including `TRUSTED+RESOURCE_DEGRADED` and `TRUSTED+INELIGIBLE`.
- Prove `LIVE`, `PAPER`, `SHADOW` and `REPLAY` non-aliasing; replay/fixtures cannot gain live mutation capability.
- Negative scanner remains restrictive for network/provider/private/trading/persistence/deployment/live capabilities.

Required traceability includes `REQ02::Trading intelligence requirements::B1`, `B7`, `B8`; `R05::Time and freshness requirements::B1-B5`; `R05::State coherency requirements::B1-B4`; `R05::Candle/cache/replay requirements::B1-B5`; `R05::Authority requirements::B1-B3`; `INT-002`, `INT-003`, `INT-004`, `INT-011`, `INT-012`, `INT-018`, `INT-022`, `INT-024`, `INT-025`, `INT-026`; `VAL-003`, `VAL-005`, `VAL-006`, `VAL-011`, `VAL-012`, `VAL-013`, `VAL-023`, `VAL-028`, `VAL-030`; `R11-REQ-006`, `R11-REQ-007`, `R11-REQ-011`, `R11-REQ-012`, `R11-REQ-013`, `R11-REQ-014`, `R11-REQ-015`, `R11-REQ-020`, `R11-REQ-022`, `R11-REQ-024`, `R11-REQ-025`; `HCT-DEC-0007`, `HCT-DEC-0008`, `HCT-DEC-0012`, `HCT-DEC-0058`, `HCT-DEC-0060` through `HCT-DEC-0065`, `HCT-DEC-0068`, `HCT-DEC-0069`, `HCT-DEC-0071`, `HCT-DEC-0074`, `HCT-DEC-0077`, `HCT-DEC-0079`, `HCT-DEC-0083`, `HCT-DEC-0084`, `HCT-DEC-0089`, `HCT-DEC-0135`, `HCT-DEC-0136`, `HCT-DEC-0138`, `HCT-DEC-0139`, `HCT-DEC-0140`, `HCT-DEC-0141`; and `ADR-0049`/S1F ADR decisions, deterministic safety rules and explicit non-scope.

## Authorization firewall

Until a later authorization checkpoint is independently approved and promoted:

- `implementation_authorized=false`;
- `implementation_authorization_scope=[]`;
- `implementation_authorization_ceiling=NONE_PENDING_NEXT_GOVERNED_AUTHORIZATION`;
- `production_credentials_authorized=false`;
- `production_deployment_authorized=false`;
- `limited_live_authorized=false`;
- `live_trading_authorized=false`.

PLANNING_FREEZE is not IMPLEMENTATION_AUTHORIZATION. IMPLEMENTATION_AUTHORIZATION is not LIVE_TRADING_AUTHORIZATION. A planning candidate, green governance CI or approved review cannot change these flags.

## Required independent review and stop condition

The candidate is `AUTHOR_SIDE_GOVERNANCE_PREFLIGHT_NOT_INDEPENDENT_APPROVAL`. A fresh independent HIGH_ASSURANCE review must validate the exact recompiled head, CP0032/base lock, source blobs, B001 resolution, exact eight-feature allowlist, numeric policy, ordered lineage, axis separation, benchmark contract, four-file diff and fail-closed firewall.

After exact-head pull-request-only governance CI passes, keep PR #69 OPEN and UNMERGED. Do not implement S2A, merge PR #69, promote an S2A checkpoint, modify S1F, change frozen sources, add dependency/runtime/product files, deploy, configure credentials, call private APIs, activate limited-live or trade.
