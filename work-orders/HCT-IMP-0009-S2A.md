# HCT-IMP-0009-S2A — Deterministic Feature & Indicator Foundation

Status: `PENDING_SEPARATE_AUTHORIZATION_CHECKPOINT`
Risk: `HIGH_ASSURANCE`
Prerequisite: a future checkpoint explicitly authorizing only this Work Order under a dedicated S2A ceiling.
Canonical preparation base: `main@3ee5ad4d967bb6ef051eae1982990d728c6ade9e`
Current checkpoint: `HCT-CP-0032 / S1F_IMPLEMENTATION_APPROVED_MERGED`
Recompile marker: `RECOMPILED_AFTER_S1F`
Authorization candidate: `HCT-IMPL-AUTH-0009 / Issue #68`
Upstream dependency: `HCT-IMP-0010-S1F / HCT-CP-0032`
Scope name: `Deterministic Feature & Indicator Foundation`
Primary owner: `Module 8 — Indicator & Feature Engine (V1_CORE)`

This Work Order defines a possible future implementation slice. It does not authorize implementation, merge, checkpoint promotion, credentials, deployment, limited-live or live trading.

## OBJECTIVE

Only after a separate S2A authorization checkpoint, implement a deterministic, provider-neutral, fixture/replay-testable Module 8 foundation from trusted or explicitly degraded S1F/S1E read-only evidence. Preserve point-in-time semantics, no-lookahead, generation/environment isolation, explicit validity degradation and reproducible fingerprints. Do not create trading authority or a second market-truth owner.

## PREREQUISITE AND SOURCE CONTRACT

`B001=RESOLVED_BY_HCT-IMP-0010-S1F_CP0032`.

S1F supplies typed public market values and immutable fingerprints. S2A consumes `TradeTick`, `TickerState`, `CandleBar`, `OrderBookSnapshot`, `OrderBookDelta`, `ReferencePriceEvidence` and `FundingEvidence` read-only, together with S1E `MarketStateTrust` and `DataAuthority`. It may not recalculate, mutate, upgrade or replace upstream truth.

Exact source identities bound to this Work Order:

- canonical main: `3ee5ad4d967bb6ef051eae1982990d728c6ade9e`;
- `checkpoints/history/HCT-CP-0032.json`: `f910b60f0b2dc3c046cac12795dca29a8b7aa3a2`;
- `checkpoints/workstreams/planning/latest.json`: `3a8ad6d6887cca478f1d999feb8ba15421b817a4`;
- `docs/06-test-benchmark-plan.md`: `29401ce8fe1616f9390a317bae62d3a157addaa5`;
- `adr/HCT-ADR-0050-s1f-realtime-public-market-value-ingest.md`: `609ddc4656220027ce14503a6ba7ae71acc4c039`;
- `work-orders/HCT-IMP-0010-S1F.md`: `c9cf955dbb83c337760af3cff4d3136e32228319`;
- `evidence/HCT-IMP-0010-S1F.md`: `9061c9f072d8e111cda3d2983242fd6466e1101e`.

The nine frozen requirements remain those recorded by the R12 baseline: `docs/02` `292da9552ae816e4d51b8a299456305da1658e55`; `docs/48` `f20c1ed00bdb13801aaff8a3b648371bfcffba58`; `docs/54` `636ad01da9c25e760dd5e2f033b93a0f04578a17`; `docs/61` `fea197e60532eb6ff3b11b628b9aabcbcfc00c41`; `docs/67` `c8a426966c5a0dc34704d1413f506332e770c2c7`; `docs/73` `c859c0c4a718e3017c34aa50013d4c50959853b4`; `docs/80` `bc897ebd470857a53055bdee85128b5bd31a5822`; `docs/87` `023187ef23b01d5a11f978bbfe6e38abf172bb3b`; `docs/93` `6935e9973696d5b706546d63d847ea398780d936`.

## SCOPE

### Typed definitions and registry

- immutable typed `FeatureDefinition` with canonical ID, version, semantic family, input contract, timeframe/window policy, output type, validity policy and behaviorally material fingerprint;
- immutable `FeatureVersion` and registry operations that reject silent canonical-ID redefinition, version collision and material mutation;
- display names/descriptions/UI labels are non-authoritative;
- implement exactly the eight frozen public/standard V1_CORE families: `F-RET-001`, `F-SMA-001`, `F-EMA-001`, `F-ROC-001`, `F-RSI-001`, `F-TR-001`, `F-ATR-001`, `F-VSMA-001`.

### Point-in-time evidence

- immutable `FeatureValue` and `FeatureSnapshot` bound to source Market-State fingerprint, generation, contract, environment, DataAuthority/freshness evidence, definition/version, event time, knowledge time and replay provenance;
- explicit window start/end, close boundary, timeframe, ordering, completeness, sample count, required warmup and ordered input lineage;
- no-lookahead rejects future event/knowledge time, later corrections unavailable at the boundary, immature labels and outcome-derived prior inputs.

### Validity and axis separation

`FeatureValidity` is separate from `MarketStateTrust`, `DataAuthority`, resource restriction and Universe/lifecycle restriction. The required matrix includes `TRUSTED+RESOURCE_DEGRADED` and `TRUSTED+INELIGIBLE` without upgrading the restrictive axis.

`VALID`, `UNKNOWN`, `INVALID`, `WARMUP` and `DEGRADED` are explicit. Missing, insufficient, stale, expired, untrusted, contradictory, schema-quarantined or mixed-generation evidence remains restrictive. Aggregate scores, defaults and zero-filling cannot produce unrestricted `VALID`.

### Alignment and replay

- deterministic multi-timeframe alignment uses CLOSED 1m constituent windows, explicit event/knowledge-time boundaries and source/generation compatibility;
- windows are UTC half-open `[start,end)`, start-inclusive/end-exclusive, and Unix-epoch aligned;
- fixture/replay inputs are immutable, carry source/generation/completeness/fidelity identity and reproduce the same canonical feature sequence for identical inputs and definitions.

## OUT OF SCOPE

Module 9 patterns, regime, scanner/ranking, strategy/catalog/signal, microstructure, Brain, agents, RAG/memory, learning, calibration, Risk, Safety, Session Policy, sizing, leverage, OMS, Execution, reconciliation, protection, raw ingest, socket/WebSocket/HTTP/REST/provider endpoints, credentials, private APIs, signing, orders, positions, balances, fills, persistence/database/RLS, feature stores, HA/fencing, deployment, production or limited-live activation and real-money trading are forbidden.

S1F Market-State/value contracts, DataAuthority, checkpoints, frozen requirements and dependency locks are read-only and remain owned by their upstream governance.

## NORMATIVE NUMERIC POLICY

`FEATURE_DECIMAL_POLICY_VERSION=FEATURE_DECIMAL_V1`

`FEATURE_DECIMAL_INTERNAL_PRECISION=76`

`FEATURE_DECIMAL_MAX_PRECISION=38`

`FEATURE_DECIMAL_MAX_SCALE=18`

`FEATURE_DECIMAL_ROUNDING=ROUND_HALF_EVEN`

`FEATURE_DECIMAL_BINARY_FLOAT=FORBIDDEN`

`FEATURE_DECIMAL_NONFINITE=FORBIDDEN`

Use S1F Decimal inputs only. Exact operations that fit bounds must not be rounded for convenience. Non-terminating division/smoothing quantizes final canonical output to scale 18 with `ROUND_HALF_EVEN`; policy, N/window, seed, source field, timeframe, version and rounding mode are fingerprint-visible. Overflow, invalid denominator, impossible input, mixed unit, missing input or unsupported operation produces typed restrictive validity, never zero/default/NaN/Infinity.

## ARCHITECTURE RULES

1. S1F/S1E are the sole upstream market-truth/value owners; S2A is read-only.
2. Definition, registry, input-lineage and output fingerprints are deterministic and mutation-complete.
3. Event time, knowledge time, wall-receive time and monotonic age remain distinct; admissibility uses knowledge time.
4. Mixed source, contract, environment, generation or timeframe version fails closed.
5. `LIVE`, `PAPER`, `SHADOW` and `REPLAY` are non-aliasing; fixtures/replay cannot gain live mutation capability.
6. Feature evidence cannot create scanner, strategy, Brain, Risk, Execution or live authority.
7. Provider transport, persistence and deployment are absent; fixture/replay is the only input mechanism.

## CONSTRAINTS

- Do not change frozen requirement blobs, `docs/11-checkpoint.md`, `checkpoints/`, dependency locks, S1E source/ADR, or any later module.
- Do not add provider names/URLs, sockets, HTTP/WS clients, credentials, private APIs, orders, Risk/OMS/Execution routes, database/persistence, deployment or live flags.
- Do not use global mutable registries, silent redefinition, defaults or aggregate confidence to upgrade authority.
- Do not use sleep-based freshness proof; use explicit timestamps and monotonic evidence.
- Stop with PR OPEN and UNMERGED and author-side evidence only.

## ACCEPTANCE CRITERIA

- `PO-F01` through `PO-F10` pass with deterministic evidence;
- all eight feature IDs have golden vectors and exact `FEATURE_DECIMAL_V1` behavior;
- every material definition/input/version/window/boundary mutation changes fingerprints;
- future event/knowledge/correction/label, warmup, stale/untrusted/contradictory/degraded and mixed-generation cases fail closed;
- S1F upstream evidence remains read-only and no path upgrades DataAuthority or creates trading authority;
- `LIVE/PAPER/SHADOW/REPLAY` isolation and replay fidelity pass;
- static negative scan, exact-head CI and required prior regressions pass;
- production credentials, production deployment, limited-live and live trading remain false.

## TESTS

### Proof obligations

- `PO-F01` deterministic equal-input output and canonical serialization;
- `PO-F02` material mutation visibility in definition, registry, input, window, version and boundary fingerprints;
- `PO-F03` future event/knowledge/correction/label rejection;
- `PO-F04` insufficient samples/open-window warmup fail closed;
- `PO-F05` stale, expired, untrusted, contradictory and unknown propagation;
- `PO-F06` generation and `LIVE/PAPER/SHADOW/REPLAY` isolation;
- `PO-F07` multi-timeframe close boundary and incomplete-interval behavior;
- `PO-F08` canonical registry immutability/versioning;
- `PO-F09` non-authority and no downstream action creation;
- `PO-F10` fixture/replay fidelity and sequence reproduction.

### Adversarial and property tests

Test all eight feature IDs for zero denominator, warmup, boundary ties, corrections and exact rounding. Test canonical-order and fingerprint mutation properties, future knowledge, later correction, gaps, duplicates, out-of-order input, stale leases, contradictory channels, retired generations, mixed identities, registry overwrite/version collisions, display-name substitution, axis separation, namespace aliasing, replay parity and no-lookahead.

### Benchmark contract

`S2A_BENCHMARK_MODE=S2A_BASELINE_ESTABLISHMENT_V1`

- `MICRO`: 1 contract, 4096 CLOSED 1m candles, all authorized features, max window 64;
- `NOMINAL`: 16 contracts, 8192 CLOSED 1m candles per contract, all authorized features, max window 256;
- `STRESS`: 32 contracts, 16384 CLOSED 1m candles per contract plus deterministic 5m/15m closed-window alignment, all authorized features, max window 512.

Measure feature evaluations/second, per-feature compute latency p50/p95/p99/max, replay throughput, peak/steady memory, window-buffer depth, warmup counts, restrictive-state propagation counts, no-lookahead rejection counts and deterministic output-manifest hash. Accept correctness, deterministic same-input hash, bounded completion and bounded memory/window growth. Record hardware/runtime/seed/source fixture identity; make no profitability or production SLO claim.

### Negative capability and prior regressions

The scanner must reject network/provider/private/trading/persistence/deployment/live capabilities in the bounded implementation. Exact-head CI must run `git diff --check`, source/contract validation, all required S0A-S1F regressions, type/lint/format/build/audit and deterministic benchmark gates.

## DELIVERABLES

- immutable typed feature definitions, versions, registry and deterministic fingerprints;
- point-in-time FeatureValue/FeatureSnapshot contracts with lineage and validity/degradation;
- exactly the eight frozen V1_CORE feature families;
- multi-timeframe/no-lookahead evaluator;
- fixture/replay inputs, adversarial/property tests and Evidence Bundle;
- negative-capability scanner and exact-head pull-request-only CI;
- author-side preflight with exact base/head/checkpoint/flags and known limitations.

## REVIEW FORMAT

Report `repositorySync`, `sourceMatch`, `canonicalMain`, `checkpoint`, `implementationHead`, `changedFiles`, `exactFeatureSet`, `numericPolicy`, `fingerprintDeterminism`, `mutationVisibility`, `pointInTime`, `noLookahead`, `validityStates`, `warmupFailClosed`, `trustPropagation`, `generationIsolation`, `environmentIsolation`, `multiTimeframeBoundary`, `replayFidelity`, `upstreamMarketTruthReadOnly`, `nonAuthority`, `negativeScopeFirewall`, `priorStageRegressions`, `exactHeadRun`, `exactHeadJob`, `exactHeadConclusion`, `criticalRemaining`, `highRemaining`, `prOpenUnmerged`, `implementationAuthorized`, `productionCredentials`, `productionDeployment`, `limitedLive`, `liveTrading` and `stopConditionRespected`.

## AUTHORIZATION FIREWALL

`implementation_authorized=false`

`implementation_authorization_scope=[]`

`implementation_authorization_ceiling=NONE_PENDING_NEXT_GOVERNED_AUTHORIZATION`

`production_credentials_authorized=false`

`production_deployment_authorized=false`

`limited_live_authorized=false`

`live_trading_authorized=false`

Planning Freeze is not implementation authorization, and implementation authorization is not live-trading authorization.

## STOP CONDITION

Stop with the S2A implementation PR OPEN and UNMERGED after exact-head CI and author-side evidence. Do not self-approve, merge, promote a checkpoint, add network/provider/private APIs, persist state, deploy, activate limited-live or trade. A fresh independent HIGH_ASSURANCE review and separate governance acceptance are mandatory before any merge or authorization promotion.
