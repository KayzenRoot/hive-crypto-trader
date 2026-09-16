# HCT-IMPL-AUTH-0011 — S2B Candlestick & Chart Pattern Foundation Authorization Candidate

Status: `PENDING_INDEPENDENT_HIGH_ASSURANCE_REVIEW`
Risk: `HIGH_ASSURANCE`
Canonical base: `main@c198a99167fa571802b16f6daf77b253a2b100b0`
Current checkpoint: `HCT-CP-0034 / S2A_IMPLEMENTATION_APPROVED_MERGED`
Recompile marker: `DERIVED_FROM_POST_CP0034_MAIN`
Proposed authorization increment: `HCT-IMPL-AUTH-0011`
Proposed implementation slice: `HCT-IMP-0011-S2B`
Scope name: `Candlestick & Chart Pattern Foundation`
Authorization Issue: `#75`
Governance branch: `governance/HCT-IMPL-AUTH-0011-S2B`
Author-side governance preflight: `AUTHOR_SIDE_GOVERNANCE_PREFLIGHT_NOT_INDEPENDENT_APPROVAL`

This document is a governance-only authorization candidate. It does not implement
product/runtime code, authorize implementation, promote a checkpoint, grant credentials or
grant any live authority.

## Dependency position and prerequisite state

The frozen R11 Stage-2 order is
`features/indicators/patterns -> regime -> scanner -> strategy engine/catalog/signal ->
minimum microstructure`. `HCT-IMP-0009-S2A` completed the features/indicators half and is
recorded by `HCT-CP-0034` as independently approved and merged. Module 9
candlestick/chart patterns (`V1_MINIMUM`) is therefore the next candidate dependency.

- approved S2A implementation head: `40e67302fb80e329429be50430584ff9523a12a0`;
- governed S2A merge commit: `c862e5670465ef0f8d0c77dce163a1ece7c92ac4`;
- S2A independent review: `5220668487` / `APPROVED` / CRITICAL `0` / HIGH `0`;
- `HCT-CP-0034` status: `S2A_IMPLEMENTATION_APPROVED_MERGED`;
- `HCT-CP-0034` authority: `implementation_authorized=false`, empty scope,
  `NONE_PENDING_NEXT_GOVERNED_AUTHORIZATION`.

S2A, S1E and S1F artifacts are read-only upstream contracts. Module 9 cannot become a
second feature engine, a second Market-State owner, a DataAuthority owner, a strategy
engine or a signal engine.

## Objective

Freeze exact pattern scope, boundary semantics, Decimal tolerance semantics, ordered
lineage, revision handling, authority-axis separation, benchmark method and proof
obligations for a bounded `V1_MINIMUM` Module 9 foundation, before any future
implementation authorization.

## Source lock and provenance

The candidate is bound to the post-CP0034 canonical
`main@c198a99167fa571802b16f6daf77b253a2b100b0` and the following exact sources:

- `checkpoints/history/HCT-CP-0034.json` — `3003d873c343bf3fa31105c4dc0fd238f2bbe7fd`;
- `checkpoints/workstreams/planning/latest.json` — `0ac37f9daaa96a3f8ecdd53bc5bf9a397915559c`;
- `docs/06-test-benchmark-plan.md` — `29401ce8fe1616f9390a317bae62d3a157addaa5`;
- `docs/134-s2a-implementation-authorization-and-checkpoint-promotion.md` — `2c88dfc05dff16c767c0e1b4b206787f4dfe183b`;
- `docs/135-s2a-implementation-approval-and-checkpoint-promotion.md` — `7807b67d4270c46ab206a3ecfdb39cf028d5b148`;
- `work-orders/HCT-IMP-0009-S2A.md` — `592a07e6066b9ad28c1d626308338468ba548cbe`;
- `apps/backend/src/hct_backend/features.py` — `40dba614d6a146c42fc7c4755416bcedd55a7f1c`;
- `apps/backend/src/hct_backend/feature_engine.py` — `a46bca1b82ce0d9b168af5cf7b34a06ee2ef5f38`.

Any drift in the canonical base or these identities requires STOP and fresh governance
review.

## Frozen pattern scope

`S2B_PATTERN_ALLOWLIST=P-DC-001,P-MB-001,P-EC-001,P-EC-002,P-MS-001,P-ES-001`

`S2B_PATTERN_COUNT=6`

`S2B_PATTERN_FAMILIES=SINGLE_BAR,TWO_BAR_REVERSAL,THREE_BAR_REVERSAL`

The allowlist is finite and closed. Each selected pattern is admitted only because it has a
deterministic definition, is point-in-time provable from CLOSED bars alone, carries
dependency value for later Stage-2 owners, has bounded false-positive risk through frozen
tolerance semantics, and has an O(1)-per-bar benchmark cost.

`S2B_CHART_STRUCTURE_FAMILY=EXCLUDED_FROM_V1_MINIMUM`

Chart-structure patterns are excluded from `V1_MINIMUM`. A deterministic chart-structure
definition requires pivot confirmation, and any pivot rule either consumes bars after the
pivot (a hidden future dependency) or is revised retrospectively (repainting). Where a
named public pattern has multiple incompatible definitions, this candidate freezes exactly
one HCT definition and version per pattern ID, or excludes the pattern.

## Frozen numeric, boundary and lineage contract

`S2B_PATTERN_DECIMAL_POLICY=FEATURE_DECIMAL_V1`

`S2B_PATTERN_NUMERIC_SEMANTICS=DECIMAL_ONLY`

`S2B_PATTERN_BINARY_FLOAT=FORBIDDEN`

`S2B_BODY_RATIO_TOLERANCE=0.10`

`S2B_BODY_RATIO_TOLERANCE_SCALE=18`

`S2B_STAR_MIDPOINT_RATIO=0.50`

`S2B_ENGULFING_BOUNDS=BOUNDS_INCLUSIVE`

`S2B_DEGENERATE_RANGE_RULE=ZERO_RANGE_YIELDS_UNKNOWN`

`S2B_TOLERANCE_COMPARISON=CLOSED_INTERVAL`

`S2B_NO_LOOKAHEAD=STRICT_ONE_STEP_BEFORE_FORMATION_BOUNDARY_NOT_RECOGNIZED`

`S2B_REPLAY_DETERMINISM=IDENTICAL_DEFINITIONS_AND_ORDERED_EVIDENCE_IDENTICAL_OUTPUT`

`S2B_AXIS_SEPARATION=FeatureValidity;MarketStateTrust;DataAuthority;ResourceRestriction;UniverseLifecycleRestriction`

`S2B_BENCHMARK_MODE=S2B_BASELINE_ESTABLISHMENT_V1`

`S2B_BENCHMARK_PROFILES=MICRO,NOMINAL,STRESS`

A pattern with bar cardinality `k` is recognized only at the CLOSE of its final bar.
`WARMUP` is the only admissible pre-boundary outcome, and an objectively known stronger
`INVALID` or `UNKNOWN` condition dominates `WARMUP`. Corrections and revisions create new
`PatternEvidence` and new fingerprints; historical evidence is never silently mutated.

## Benchmark source lock

Benchmark profiles, cardinality conventions and the correctness-before-performance rule are
inherited from `docs/06-test-benchmark-plan.md`
(`29401ce8fe1616f9390a317bae62d3a157addaa5`) and must follow the S2A precedent that a
profile's correctness fails closed before any performance metric is considered.

## Proof obligations

`S2B-PO-01` finite exact allowlist and version collision protection;

`S2B-PO-02` golden vectors for every selected pattern including the exact one-step-before
and exact-completion boundaries;

`S2B-PO-03` no-lookahead tests using `event_time` and `knowledge_time`;

`S2B-PO-04` mutation tests for constituent correction, revision, reorder, missing bar,
changed timeframe, changed tolerance/version, cross-generation and cross-environment input;

`S2B-PO-05` `WARMUP` / `UNKNOWN` / `INVALID` / `DEGRADED` semantics with separate resource
and lifecycle restrictions;

`S2B-PO-06` duplicate, overlap and conflict representation with deterministic ordering and
fingerprints;

`S2B-PO-07` replay determinism;

`S2B-PO-08` negative-capability scan;

`S2B-PO-09` bounded MICRO/NOMINAL/STRESS baseline.
