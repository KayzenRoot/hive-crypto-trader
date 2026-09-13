# HCT-IMP-0009-S2A — Deterministic Feature & Indicator Foundation

Status: `PENDING_SEPARATE_AUTHORIZATION_CHECKPOINT`
Risk: `HIGH_ASSURANCE`
Prerequisite: a future checkpoint explicitly authorizing only this Work Order under a dedicated S2A ceiling.
Canonical preparation base: `main@625dd0c145087038bdbccd665548d811e187194c`
Authorization candidate: `HCT-IMPL-AUTH-0009 / Issue #68`
Upstream dependency: `HCT-IMP-0008-S1E / HCT-CP-0030`
Scope name: `Deterministic Feature & Indicator Foundation`
Primary owner: `Module 8 — Indicator & Feature Engine (V1_CORE)`

## OBJECTIVE

Only after a separate authorization checkpoint, implement a deterministic, provider-neutral, fixture/replay-testable Module 8 foundation that derives versioned non-authoritative analytical evidence from trusted or explicitly degraded S1E Market-State/DataAuthority inputs. The slice must preserve point-in-time semantics, no-lookahead, generation/environment isolation, explicit validity degradation and reproducible fingerprints. It must not create trading authority.

## CONTEXT

R11 Stage 2 is ordered `features/indicators/patterns -> regime -> scanner -> strategy engine/catalog/signal -> minimum microstructure`. This Work Order is the first bounded Module 8 dependency only. Module 9 candlestick/chart patterns are separate. S1E owns normalized market truth, quality and Market-State/DataAuthority; S2A is a read-only consumer and must not become a second source of market truth.

Feature values are evidence, not candidate trades. They may be consumed by later governed modules, but S2A itself has no scanner-ranking, strategy, signal, Brain, Risk, Safety, Session Policy, sizing, leverage, OMS, Execution, reconciliation, protection, promotion or live authority.

## SCOPE

### Typed definitions and registry

- immutable typed `FeatureDefinition` with canonical ID, version, semantic family, input contract, timeframe/window policy, output type, validity policy and behaviorally material fingerprint;
- immutable `FeatureVersion` and registry operations that reject silent canonical-ID redefinition, version collision and behaviorally material mutation;
- display names, descriptions and UI labels remain non-authoritative metadata;
- only frozen-source-derived bounded public/standard V1_CORE families may be implemented, such as returns, rolling statistics, moving averages and volatility/range; the exact family set must be justified by source locators before coding; proprietary HCT R&D is not included.

### Point-in-time feature evidence

- immutable `FeatureValue` and `FeatureSnapshot` bound to tenant/account/environment identity where applicable, contract identity, source Market-State fingerprint, Market-State generation, DataAuthority/freshness evidence, definition/version, event time, knowledge time and replay provenance;
- explicit window start/end, close boundary, timeframe, ordering, completeness, sample count, required warmup and input lineage;
- event time, knowledge time, wall-receive time and monotonic age remain separate; no clock substitution may make a future value appear available earlier;
- no-lookahead gate rejects future event/knowledge time, later corrections unavailable at the boundary, immature labels and outcome-derived prior inputs.

### Validity and degradation

The public contract must represent at least:

- `VALID`: all required inputs are admissible, complete, coherent and within freshness policy;
- `UNKNOWN`: required input or trust proof is unavailable or cannot be established;
- `INVALID`: schema, identity, contract, source, generation or invariant validation failed;
- `WARMUP`: deterministic computation lacks required samples or a closed window;
- `DEGRADED`: computation is explicit but input fidelity/quality is below the normal contract and downstream policy must not treat it as normal valid evidence.

Missing, insufficient, stale, expired, untrusted, contradictory, schema-quarantined or mixed-generation S1E evidence must propagate to a restrictive state. Aggregate scores, defaults, zero-filling or display convenience cannot upgrade it to `VALID`.

### Alignment and replay

- deterministic multi-timeframe alignment uses explicit interval close boundaries, event/knowledge-time ordering and source/generation compatibility;
- incomplete current intervals and future interval data are excluded according to the declared policy;
- fixture/replay inputs are immutable and carry source, generation, completeness and fidelity identity;
- replay must reproduce the same canonical feature sequence for the same inputs and definition versions, with degraded fidelity explicit.

## OUT OF SCOPE

- Module 9 full candlestick/chart pattern engine;
- regime, scanner, ranking, strategy, catalog, signal or microstructure implementation;
- Brain, agents, RAG, temporal memory, learning, calibration and promotion authority;
- raw market ingest, socket/WebSocket/HTTP/REST/provider endpoints, subscriptions, reconnects and network calls;
- exchange/account/private data, credentials, authentication, signing, orders, positions, balances and fills;
- Risk, Safety, Session Policy, portfolio exposure, sizing, leverage, OMS, Execution, reconciliation and protection;
- persistent database/feature store/RLS, HA/fencing, deployment and infrastructure topology;
- production or limited-live activation, live credentials and real-money trading;
- mutation or ownership of S1E Market-State, DataAuthority, exchange truth, checkpoint, frozen requirements or dependency locks.

## FILES/SOURCES TO READ

Before implementation, read the exact frozen files and current canonical state:

- `docs/00-source-hierarchy.md`, `docs/02-requirements.md`, `docs/03-scope.md`, `docs/04-architecture.md`, `docs/09-definition-of-done.md`, `docs/10-decisions-ledger.md`, `docs/11-checkpoint.md`, `docs/14-product-module-map.md`;
- `docs/48-r04-execution-requirements-addendum.md`, `docs/54-r05-realtime-requirements-addendum.md`, `docs/61-r06-intelligence-requirements-addendum.md`, `docs/67-r07-validation-laboratory-requirements-addendum.md`, `docs/73-r08-multitenant-security-requirements-addendum.md`, `docs/80-r09-cockpit-uiux-requirements-addendum.md`, `docs/87-r10-observability-audit-incident-finops-requirements-addendum.md`, `docs/93-r11-integration-requirements-addendum.md`;
- `docs/91-r11-integrated-authority-state-dependency-architecture.md`, `docs/92-r11-v1-module-classification-and-integration-hardening.md`, `docs/99-r12-frozen-requirements-baseline.md`, `docs/100-r12-requirements-traceability-and-no-loss-proof.md`, `docs/101-r12-freeze-governance-change-control-and-deferred-decisions.md`;
- `adr/HCT-ADR-0049-s1e-market-truth-foundation.md`, `work-orders/HCT-IMPL-AUTH-0009.md`, and the canonical S1E contracts/evidence only as read-only upstream context.

## REQUIREMENTS

Trace every behavior and test to exact frozen locators. The minimum traceability set is:

- `REQ02::Trading intelligence requirements::B1`, `B7`, `B8`;
- `R05::Time and freshness requirements::B1`–`B5`, `R05::State coherency requirements::B1`–`B4`, `R05::Candle/cache/replay requirements::B1`–`B5`, `R05::Universe lifecycle requirements::B1`–`B2`, `R05::Authority requirements::B1`–`B3`;
- applicable `R05::Validation requirements::B2`, `B3`, `B6`, `B8`, `B9`, `B10`, `B13`, `B15`, `B17`;
- `INT-002`, `INT-003`, `INT-004`, `INT-011`, `INT-012`, `INT-018`, `INT-022`, `INT-024`, `INT-025`, `INT-026`;
- `VAL-003`, `VAL-005`, `VAL-006`, `VAL-011`, `VAL-012`, `VAL-013`, `VAL-023`, `VAL-028`, `VAL-030`;
- `R11-REQ-006`, `R11-REQ-007`, `R11-REQ-011`, `R11-REQ-012`, `R11-REQ-013`, `R11-REQ-014`, `R11-REQ-015`, `R11-REQ-020`, `R11-REQ-022`, `R11-REQ-024`, `R11-REQ-025`;
- `HCT-DEC-0007`, `HCT-DEC-0008`, `HCT-DEC-0012`, `HCT-DEC-0058`, `HCT-DEC-0060`, `HCT-DEC-0061`, `HCT-DEC-0062`, `HCT-DEC-0063`, `HCT-DEC-0064`, `HCT-DEC-0065`, `HCT-DEC-0068`, `HCT-DEC-0069`, `HCT-DEC-0071`, `HCT-DEC-0074`, `HCT-DEC-0077`, `HCT-DEC-0079`, `HCT-DEC-0083`, `HCT-DEC-0084`, `HCT-DEC-0089`, `HCT-DEC-0135`, `HCT-DEC-0136`, `HCT-DEC-0138`, `HCT-DEC-0139`, `HCT-DEC-0140`, `HCT-DEC-0141`;
- ADR-0049 `Decision`, `Deterministic safety rules` and `Explicit non-scope`.

## ARCHITECTURE RULES

1. Use S1E Market-State/DataAuthority snapshots only through read-only typed interfaces. Preserve source fingerprint, generation, contract, environment, provenance and freshness; never recalculate or upgrade upstream authority.
2. Make definition, version, registry and output fingerprints deterministic and mutation-complete. Canonical IDs are immutable; display names are not identity.
3. Require a declared point-in-time boundary before computation. Compare both event time and knowledge time; later knowledge cannot be used to compute an earlier feature.
4. Treat `UNKNOWN`, `INVALID`, `WARMUP` and `DEGRADED` as explicit outcomes, not nulls that downstream code may accidentally treat as valid.
5. Align timeframes by deterministic closed intervals and reject incomplete, contradictory, stale or mixed-generation input.
6. Keep `LIVE`, `PAPER`, `SHADOW` and `REPLAY` identities non-aliasing. S2A has no live mutation capability even when a LIVE-named evidence namespace is represented.
7. Keep feature evidence non-authoritative. Any later consumer must pass its own governed authority and promotion gates.
8. Keep the implementation provider-neutral, persistence-free and network-free; fixture/replay is the only input mechanism in this slice.

## CONSTRAINTS

- No implementation may change frozen requirement blobs, `docs/11-checkpoint.md`, `checkpoints/`, dependency locks, S1E source/ADR, or any later module.
- No new provider names, URLs, sockets, HTTP/WS clients, credentials, private API terms, orders, Risk/OMS/Execution routes, database/persistence or deployment code.
- No global mutable registry, silent redefinition, default-value authority upgrade or aggregate-confidence override.
- No sleep-based freshness proof; use explicit timestamps/monotonic evidence supplied by contracts.
- No proprietary indicator or model-assisted feature is eligible for this bounded deterministic foundation.
- Implementation must stop with PR OPEN and UNMERGED and must provide author-side evidence only.

## ACCEPTANCE CRITERIA

- all PO-F01 through PO-F10 below pass with deterministic evidence;
- every public constructor/API rejects missing identity, unsupported version, invalid lineage, mixed generation, future knowledge or insufficient warmup;
- `VALID`, `UNKNOWN`, `INVALID`, `WARMUP` and `DEGRADED` semantics are explicit and tested;
- no-lookahead tests cover future event/knowledge time, late corrections, immature labels and out-of-order replay;
- feature fingerprints change for every behaviorally material mutation and remain stable for canonical equivalent input;
- multi-timeframe windows close deterministically and reject incomplete/mixed-generation evidence;
- registry/version collisions and display-name identity substitution fail closed;
- S1E upstream evidence remains read-only and no feature path can upgrade DataAuthority or create trading authority;
- environment, contract, generation and replay-fidelity isolation passes;
- static negative capability scan and exact-head CI pass; all prior required regressions remain green;
- no unresolved CRITICAL/HIGH finding remains at independent approval time;
- production credentials, production deployment, limited-live and live trading remain false.

## TESTS

### Proof obligations

- `PO-F01` deterministic equal-input output and serialization;
- `PO-F02` material mutation visibility in definition, registry, input, window, version and boundary fingerprints;
- `PO-F03` future event/knowledge/correction/label rejection;
- `PO-F04` insufficient sample and open-window warmup fail-closed behavior;
- `PO-F05` stale, expired, untrusted, contradictory and unknown input trust propagation;
- `PO-F06` generation and `LIVE/PAPER/SHADOW/REPLAY` isolation;
- `PO-F07` multi-timeframe close-boundary and incomplete-interval behavior;
- `PO-F08` canonical registry immutability and versioning;
- `PO-F09` non-authority and no downstream action creation;
- `PO-F10` fixture/replay fidelity and sequence reproduction.

### Adversarial and property tests

- canonical-order and fingerprint mutation properties;
- invalid enum/identity/contract/source/generation constructors;
- future knowledge, later corrections, outcome-derived input and immature labels;
- gaps, duplicates, out-of-order inputs, stale leases, contradictory channels and retired generations;
- warmup, missing, insufficient, degraded and schema-quarantined inputs;
- timeframe boundary ties, timezone/clock ambiguity and mixed-generation windows;
- registry overwrite/version collision/display-name substitution;
- namespace aliasing and attempted live-authority escalation;
- replay parity and explicit fidelity manifests.

### Negative-capability and regression tests

The scanner must reject network/provider endpoints, sockets, HTTP/WS clients, provider DTO truth, credentials/private APIs, order/trading/Risk/OMS/Execution terms, persistence/database/RLS, deployment and live-authority mutation in the bounded implementation surface. Exact-head CI must also execute full required prior regressions S0A–S1E, contract generation/parity, lint/format, strict typing, builds, dependency audits, frontend regressions and `git diff --check`.

## DELIVERABLES

- immutable typed feature definitions, versions, registry and deterministic fingerprints;
- point-in-time FeatureValue/FeatureSnapshot contracts with lineage and validity/degradation;
- deterministic public/standard V1_CORE feature family implementations justified by frozen locators;
- multi-timeframe/no-lookahead evaluator;
- fixtures/replay inputs and Evidence Bundle;
- adversarial/property/state-machine/fingerprint/namespace/replay tests;
- negative-capability scanner and exact-head pull-request-only CI;
- author-side preflight with exact base/head/checkpoint/flags and known limitations.

## REVIEW FORMAT

Report: `repositorySync`, `sourceMatch`, `canonicalMain`, `checkpoint`, `implementationHead`, `changedFiles`, `definitionRegistry`, `fingerprintDeterminism`, `mutationVisibility`, `pointInTime`, `noLookahead`, `validityStates`, `warmupFailClosed`, `trustPropagation`, `generationIsolation`, `environmentIsolation`, `multiTimeframeBoundary`, `replayFidelity`, `upstreamMarketTruthReadOnly`, `nonAuthority`, `negativeScopeFirewall`, `priorStageRegressions`, `exactHeadRun`, `exactHeadJob`, `exactHeadConclusion`, `criticalRemaining`, `highRemaining`, `prOpenUnmerged`, `implementationAuthorized`, `productionCredentials`, `productionDeployment`, `limitedLive`, `liveTrading` and `stopConditionRespected`.

## STOP CONDITION

Stop with the S2A implementation PR OPEN and UNMERGED after exact-head CI and author-side evidence. Do not self-approve, merge, promote a checkpoint, add network/provider/private APIs, persist state, deploy, activate limited-live or trade. A fresh independent HIGH_ASSURANCE review and separate governance acceptance are mandatory before any merge or authorization promotion.
