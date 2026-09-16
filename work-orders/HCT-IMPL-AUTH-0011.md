# HCT-IMPL-AUTH-0011 — S2B Candlestick & Chart Pattern Foundation Authorization

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
and merged S2A deterministic feature/indicator foundation: a finite, deterministic,
provider-neutral, point-in-time Candlestick & Chart Pattern Foundation for Module 9
(`V1_MINIMUM`).

The frozen R11 Stage-2 order is
`features/indicators/patterns -> regime -> scanner -> strategy engine/catalog/signal ->
minimum microstructure`. With S2A complete under `HCT-CP-0034`, patterns are the next
dependency. Regime, scanner, strategy/catalog/signal and microstructure remain later
governed owners and are not authorized here.

## PRECONDITION AND PREREQUISITE STATE

- `HCT-CP-0034` records the independently approved and merged completion of
  `HCT-IMP-0009-S2A` at approved head
  `40e67302fb80e329429be50430584ff9523a12a0`, merge commit
  `c862e5670465ef0f8d0c77dce163a1ece7c92ac4`;
- `HCT-CP-0034` consumes the CP0033 implementation authorization and leaves
  `implementation_authorized=false`, an empty authorization scope and the
  `NONE_PENDING_NEXT_GOVERNED_AUTHORIZATION` ceiling;
- S2A is a read-only upstream contract for this candidate. Module 9 may not restate,
  duplicate or re-own S2A feature semantics, S1E Market-State truth, S1F value evidence or
  DataAuthority;
- no S2B implementation Issue exists yet; the implementation Issue is expected to be
  created only when this authorization is accepted and a separate authorization checkpoint
  is promoted.

## SCOPE

The candidate may define only:

- immutable typed `PatternDefinition` / `PatternVersion` with canonical ID, version,
  family, bar cardinality, frozen source fields, timeframe/version, tolerance and equality
  semantics, formation/completion boundary rule and behaviorally material fingerprints;
- a finite registry that rejects silent canonical-ID redefinition, version collision and
  material mutation;
- immutable `PatternEvidence` bound to source, contract, environment, generation,
  timeframe/version, ordered constituent lineage, event and knowledge times, wall-receive
  time, window boundaries, revision/predecessor semantics, validity state and the exact
  consumed upstream evidence fingerprints;
- exactly the six frozen `V1_MINIMUM` pattern IDs
  `P-DC-001`, `P-MB-001`, `P-EC-001`, `P-EC-002`, `P-MS-001`, `P-ES-001`;
- explicit `VALID`, `UNKNOWN`, `INVALID`, `WARMUP` and `DEGRADED` outcomes with fail-closed
  propagation and separate resource and lifecycle restriction axes;
- point-in-time formation boundaries, exact bar cardinality, CLOSED-input requirements,
  ordering, duplicate/overlap/conflict representation and strict no-lookahead validation;
- Decimal-only threshold and tolerance evaluation under `FEATURE_DECIMAL_V1`;
- deterministic fixture/replay evidence, deterministic tests and bounded benchmark
  profiles tied to `docs/06-test-benchmark-plan.md`;
- a negative-capability scanner and a pull-request-only exact-head quality workflow for the
  future implementation slice.

No pattern may create a candidate action, ranking, directional probability, expected
return, strategy suitability, signal, Brain admission, Risk approval, Execution plan or
live authority. Structural pattern evidence is not a trade authorization.

## OUT OF SCOPE

No runtime/product implementation in this governance candidate. No network transport,
provider endpoint, socket/WebSocket/HTTP client, credential, private API, signing,
persistence, database/RLS, feature store, deployment or infrastructure topology. Excluded
from `V1_MINIMUM`: chart-structure patterns requiring pivot confirmation, Module 10
proprietary indicator R&D, regime classification, scanner/ranking, strategy/catalog/signal,
microstructure, Brain, agents, RAG/memory, learning, calibration, Risk, Safety, Session
Policy, sizing, leverage, OMS, Execution, reconciliation, protection, orders, positions,
balances, fills, limited-live and live trading. An unbounded internet pattern catalog is
not authorized.

## FINITE PATTERN SET AND EXCLUSION

`S2B_PATTERN_ALLOWLIST=P-DC-001,P-MB-001,P-EC-001,P-EC-002,P-MS-001,P-ES-001`

`S2B_PATTERN_COUNT=6`

`S2B_CHART_STRUCTURE_FAMILY=EXCLUDED_FROM_V1_MINIMUM`

Single-bar patterns are admitted only with frozen equality and tolerance semantics. Two-bar
and three-bar reversal patterns are admitted only with exact bar cardinality and a
deterministic formation boundary. Chart-structure patterns are excluded because a
deterministic definition requires pivot confirmation that either consumes future bars or is
revised retrospectively, which would violate the strict no-lookahead contract.

## FROZEN NUMERIC AND LINEAGE CONTRACT

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

## PROOF OBLIGATIONS

`S2B-PO-01` finite exact allowlist and version collision protection;

`S2B-PO-02` golden vectors for every selected pattern including the exact one-step-before
boundary and the exact completion boundary;

`S2B-PO-03` no-lookahead tests using `event_time` and `knowledge_time`;

`S2B-PO-04` mutation tests for constituent correction, revision, reorder, missing bar,
changed timeframe, changed tolerance/version, cross-generation and cross-environment input;

`S2B-PO-05` `WARMUP` / `UNKNOWN` / `INVALID` / `DEGRADED` semantics with separate resource
and lifecycle restrictions;

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
