# HCT-IMP-0011-S2B — S2B Candlestick & Chart Pattern Foundation

Status: `PENDING_SEPARATE_AUTHORIZATION_CHECKPOINT`
Risk: `HIGH_ASSURANCE`
Canonical base: `main@c198a99167fa571802b16f6daf77b253a2b100b0`
Current checkpoint: `HCT-CP-0034 / S2A_IMPLEMENTATION_APPROVED_MERGED`
Proposed implementation: `HCT-IMP-0011-S2B`
Proposed authorization: `HCT-IMPL-AUTH-0011`
Scope name: `Candlestick & Chart Pattern Foundation`
Governance branch: `governance/HCT-IMPL-AUTH-0011-S2B`
Author-side governance preflight: `AUTHOR_SIDE_GOVERNANCE_PREFLIGHT_NOT_INDEPENDENT_APPROVAL`

This Work Order is a frozen scope contract for a **future** bounded implementation. It
authorizes nothing today: `HCT-CP-0034` leaves `implementation_authorized=false`, and this
document becomes executable only after its own authorization checkpoint is promoted and a
fresh independent HIGH_ASSURANCE review accepts the exact implementation head.

## OBJECTIVE

Freeze the smallest useful `V1_MINIMUM` Module 9 foundation for public/standard
candlestick and chart-pattern evidence. Module 9 is a **consumer** of S2A feature/indicator
evidence and of read-only S1E/S1F market truth. It is not a second feature engine, not a
Market-State owner, not a DataAuthority owner, not a strategy engine and not a signal
engine.

## FROZEN SCOPE

### S2B_EXACT_V1_MINIMUM_PATTERN_SET

The authorized pattern allowlist is exactly six finite, deterministic, public/standard
patterns. No other pattern may be added without a new governed authorization.

| Pattern ID | Family | Bars | Definition anchor |
|---|---|---|---|
| `P-DC-001` | single-bar indecision | 1 | Doji body/range ratio at or below the frozen tolerance |
| `P-MB-001` | single-bar conviction | 1 | Marubozu body/range ratio at or above the frozen complement |
| `P-EC-001` | two-bar reversal | 2 | Bullish engulfing of the previous body with inclusive bounds |
| `P-EC-002` | two-bar reversal | 2 | Bearish engulfing of the previous body with inclusive bounds |
| `P-MS-001` | three-bar reversal | 3 | Morning star: long, small-body, then bullish recovery above the first body midpoint |
| `P-ES-001` | three-bar reversal | 3 | Evening star: the exact mirror of the morning star |

`S2B_PATTERN_ALLOWLIST=P-DC-001,P-MB-001,P-EC-001,P-EC-002,P-MS-001,P-ES-001`

`S2B_PATTERN_FAMILIES=SINGLE_BAR,TWO_BAR_REVERSAL,THREE_BAR_REVERSAL`

`S2B_PATTERN_COUNT=6`

`S2B_PATTERN_SET_SIZE_FINITE=TRUE`

### Inclusion justification and exclusion of chart-structure patterns

Each included pattern is justified on all five required axes:

| Pattern | Deterministic definition | Point-in-time provable | Dependency value | False-positive risk | Benchmark cost |
|---|---|---|---|---|---|
| `P-DC-001` | exact body/range ratio with frozen tolerance and equality | yes, single CLOSED bar | upstream primitive for stars | low, tightened by tolerance | O(1) per bar |
| `P-MB-001` | exact complement ratio | yes, single CLOSED bar | upstream primitive for stars | low | O(1) per bar |
| `P-EC-001` | exact two-bar body containment with inclusive bounds | yes, needs only bar t-1 and t | classic reversal evidence | medium, bounded by inclusive bounds | O(1) per bar |
| `P-EC-002` | exact mirror of `P-EC-001` | yes | classic reversal evidence | medium, as above | O(1) per bar |
| `P-MS-001` | exact three-bar cardinality plus frozen midpoint ratio | yes, needs only bars t-2..t | multi-bar reversal evidence | medium, bounded by small-body tolerance | O(1) per bar |
| `P-ES-001` | exact mirror of `P-MS-001` | yes | multi-bar reversal evidence | medium, as above | O(1) per bar |

`S2B_CHART_STRUCTURE_FAMILY=EXCLUDED_FROM_V1_MINIMUM`

Chart-structure patterns (for example head-and-shoulders, triangles, channels, wedges) are
**excluded** from `V1_MINIMUM` because a deterministic definition requires pivot
confirmation, and any pivot rule either consumes bars after the pivot (hidden future
dependency) or is revised retrospectively (repainting). Admitting one would violate the
strict no-lookahead contract below. Chart-structure recognition requires its own separate
governed authorization with an explicit pivot-confirmation contract.

### Frozen threshold, tolerance and equality contract

`S2B_PATTERN_DECIMAL_POLICY=FEATURE_DECIMAL_V1`

`S2B_PATTERN_NUMERIC_SEMANTICS=DECIMAL_ONLY`

`S2B_PATTERN_BINARY_FLOAT=FORBIDDEN`

`S2B_BODY_RATIO_TOLERANCE=0.10`

`S2B_BODY_RATIO_TOLERANCE_SCALE=18`

`S2B_STAR_MIDPOINT_RATIO=0.50`

`S2B_ENGULFING_BOUNDS=BOUNDS_INCLUSIVE`

`S2B_DEGENERATE_RANGE_RULE=ZERO_RANGE_YIELDS_UNKNOWN`

`S2B_TOLERANCE_COMPARISON=CLOSED_INTERVAL`

All thresholds, tolerances, equality rules and comparison directions are behaviorally
material `PatternDefinition` fields and are covered by the version fingerprint. No
authoritative comparison may use binary floating point. Where a named public pattern has
multiple incompatible definitions, this Work Order freezes exactly one HCT definition and
version per pattern ID.

### Frozen identities and evidence

- immutable `PatternDefinition` and `PatternVersion` with material fingerprints covering
  pattern ID, version, family, bar cardinality, exact source fields, timeframe and
  version, tolerance and equality semantics, formation/completion boundary rule,
  `FEATURE_DECIMAL_V1` policy version and rounding mode;
- immutable `PatternEvidence` bound to source, contract, environment, generation,
  timeframe/version, ordered constituent lineage, event time, knowledge time, wall-receive
  time, window start/end, revision/predecessor semantics, validity state and the exact
  S2A/S1E/S1F evidence fingerprints it consumed;
- explicit `VALID`, `UNKNOWN`, `INVALID`, `WARMUP` and `DEGRADED` outcomes with the
  separate analytic and restrictive axes preserved;
- corrections and revisions create new evidence and new fingerprints; historical evidence
  is never silently mutated.

### No-lookahead contract

`S2B_NO_LOOKAHEAD=STRICT_ONE_STEP_BEFORE_FORMATION_BOUNDARY_NOT_RECOGNIZED`

A pattern with bar cardinality `k` may be recognized only at the CLOSE of its final bar
`t`. One instant before that boundary — that is, while `t` is not yet a CLOSED bar, or
while `knowledge_time` of any constituent exceeds the evaluation boundary — the pattern
must not be reported as `VALID`. `WARMUP` is the only admissible pre-boundary outcome, and
an objectively known stronger `INVALID` or `UNKNOWN` condition dominates `WARMUP`.

### Axis separation

`S2B_AXIS_SEPARATION=FeatureValidity;MarketStateTrust;DataAuthority;ResourceRestriction;UniverseLifecycleRestriction`

Structural pattern evidence stays separate from directional probability, expected return,
strategy suitability, ranking, signal and trade authorization. Module 9 may not upgrade
`MarketStateTrust`, `DataAuthority`, resource restriction or lifecycle restriction, and it
inherits the S2A restriction axes without reinterpreting them.

## OUT OF SCOPE

No runtime/product implementation is authorized by this Work Order as written. No network
transport, provider endpoint, socket/WebSocket/HTTP client, credential, private API,
request signing, persistence, database/RLS, feature store, deployment, limited-live or
live trading. Also excluded: Module 10 proprietary indicator R&D, regime classification,
scanner/ranking, strategy/catalog/signal, microstructure, Brain, agents, RAG/memory,
learning, calibration, Risk, Safety, Session Policy, position sizing, leverage, OMS,
Execution, reconciliation, protection, orders, positions, balances and fills. An unbounded
internet pattern catalog is explicitly not authorized.

## PROOF OBLIGATIONS

`S2B-PO-01` finite exact allowlist of six pattern IDs with version collision protection.

`S2B-PO-02` golden vectors for every selected pattern, including the exact one-step-before
boundary and the exact completion boundary.

`S2B-PO-03` no-lookahead tests driven by `event_time` and `knowledge_time`.

`S2B-PO-04` mutation tests for constituent correction, revision, reorder, missing bar,
changed timeframe, changed tolerance or version, cross-generation and cross-environment
input.

`S2B-PO-05` `WARMUP`, `UNKNOWN`, `INVALID` and `DEGRADED` semantics with separate resource
and lifecycle restrictions.

`S2B-PO-06` duplicate, overlap and conflict representation with deterministic ordering and
fingerprints.

`S2B-PO-07` replay determinism: identical definitions over identical ordered evidence
produce identical pattern sequences and fingerprints.

`S2B-PO-08` negative-capability scan proving no network transport, credential, private
API, persistence, strategy/signal, order, position, risk, deployment or live authority.

`S2B-PO-09` bounded MICRO/NOMINAL/STRESS baseline tied to
`docs/06-test-benchmark-plan.md`, where correctness fails closed before performance
metrics are considered.

## REQUIRED EXECUTOR REPORT

`repositorySync`, `sourceMatch`, `canonicalMain`, `checkpoint`, `implementationHead`,
`changedFiles`, `exactPatternSet`, `patternSetFinite`, `chartStructureExcluded`,
`numericPolicy`, `toleranceContract`, `fingerprintDeterminism`, `formationBoundary`,
`noLookahead`, `validityStates`, `lineageAndRevision`, `axisSeparation`,
`resourceRestrictionSeparate`, `lifecycleRestrictionSeparate`, `priorStageRegressions`,
`exactHeadRun`, `exactHeadJob`, `exactHeadConclusion`, `criticalRemaining`,
`highRemaining`, `prOpenUnmerged`, `implementationAuthorized`,
`productionCredentials`, `productionDeployment`, `limitedLive`, `liveTrading`,
`stopConditionRespected`.

## STOP CONDITION

Stop with the S2B implementation PR OPEN and UNMERGED after fresh exact-head CI and a
complete author-side Evidence Bundle. Require a fresh independent HIGH_ASSURANCE review
before any merge. Do not implement pattern, regime, scanner, strategy, signal, Brain, Risk,
Safety, Session Policy, OMS or Execution capability, and do not configure credentials,
private APIs, persistence, deployment, limited-live or live trading.
