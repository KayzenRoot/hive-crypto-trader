# HCT-IMPL-AUTH-0009 — S2A Deterministic Feature & Indicator Foundation Authorization

Status: `PENDING_INDEPENDENT_HIGH_ASSURANCE_REVIEW`
Risk: `HIGH_ASSURANCE`
Canonical base: `main@625dd0c145087038bdbccd665548d811e187194c`
Current checkpoint: `HCT-CP-0030 / S1E_IMPLEMENTATION_APPROVED_MERGED`
Proposed implementation: `HCT-IMP-0009-S2A`
Authorization issue: `#68`
Governance branch: `governance/HCT-IMPL-AUTH-0009-S2A`

## OBJECTIVE

Prepare and independently review a governance-only authorization candidate for the first necessary frozen R11 Stage-2 dependency: a bounded Module 8 deterministic Feature & Indicator Foundation. This Work Order authorizes no product implementation and does not promote a checkpoint.

## CONTEXT

`HCT-CP-0030` records the approved merge of S1E and resets all implementation authority fail-closed. Frozen R11 Stage 2 is ordered as `features/indicators/patterns -> regime -> scanner -> strategy engine/catalog/signal -> minimum microstructure`. Module 8 is `V1_CORE`; Module 9 patterns are `V1_MINIMUM` and remain separate. The future S2A implementation would consume S1E Market-State/DataAuthority evidence read-only and would publish only non-authoritative analytical evidence.

## SCOPE

The authorization candidate may define only the following future S2A slice:

- immutable typed FeatureDefinition/FeatureVersion, canonical registry identity and behavior fingerprints;
- FeatureValue/FeatureSnapshot contracts bound to environment, contract, source Market-State fingerprint/generation, DataAuthority/freshness evidence, event time, knowledge time, definition version and validity;
- point-in-time windows with explicit close boundaries, timeframe, sample count, completeness and ordering;
- no-lookahead validation and future-knowledge/correction rejection;
- deterministic multi-timeframe alignment and mixed-generation rejection;
- explicit `VALID`, `UNKNOWN`, `INVALID`, `WARMUP` and `DEGRADED` states;
- deterministic public/standard V1_CORE feature families only when exact frozen requirements justify them; no proprietary R&D or pattern engine;
- fixture/replay-only evaluation, deterministic tests and evidence;
- a negative-capability scanner proving absence of network/provider/private/trading/persistence/deployment/live surfaces.

## OUT OF SCOPE

No S2A implementation code, runtime route, network or provider endpoint is authorized by this candidate. Out of scope are the full Module 9 pattern engine, regime, scanner/ranking, strategy/catalog/signal, microstructure, Brain, agents, RAG/memory, learning, calibration, Risk, Safety, Session Policy, sizing, leverage, OMS, Execution, reconciliation, protection, persistence, feature-store infrastructure, HA/fencing, deployment, credentials, private APIs, limited-live and live trading. S1E remains the sole Market-State/DataAuthority owner and may not be mutated.

## SOURCE LOCK

The implementation Work Order must be evaluated against the exact source identities in `docs/99-r12-frozen-requirements-baseline.md`, including:

- `docs/02-requirements.md` — `292da9552ae816e4d51b8a299456305da1658e55`;
- `docs/48-r04-execution-requirements-addendum.md` — `f20c1ed00bdb13801aaff8a3b648371bfcffba58`;
- `docs/54-r05-realtime-requirements-addendum.md` — `636ad01da9c25e760dd5e2f033b93a0f04578a17`;
- `docs/61-r06-intelligence-requirements-addendum.md` — `fea197e60532eb6ff3b11b628b9aabcbcfc00c41`;
- `docs/67-r07-validation-laboratory-requirements-addendum.md` — `c8a426966c5a0dc34704d1413f506332e770c2c7`;
- `docs/73-r08-multitenant-security-requirements-addendum.md` — `c859c0c4a718e3017c34aa50013d4c50959853b4`;
- `docs/80-r09-cockpit-uiux-requirements-addendum.md` — `bc897ebd470857a53055bdee85128b5bd31a5822`;
- `docs/87-r10-observability-audit-incident-finops-requirements-addendum.md` — `023187ef23b01d5a11f978bbfe6e38abf172bb3b`;
- `docs/93-r11-integration-requirements-addendum.md` — `6935e9973696d5b706546d63d847ea398780d936`.

Read and preserve `docs/00-source-hierarchy.md`, `docs/03-scope.md`, `docs/04-architecture.md`, `docs/09-definition-of-done.md`, `docs/10-decisions-ledger.md`, `docs/11-checkpoint.md`, `docs/14-product-module-map.md`, `docs/91-r11-integrated-authority-state-dependency-architecture.md`, `docs/92-r11-v1-module-classification-and-integration-hardening.md`, `docs/93-r11-integration-requirements-addendum.md`, `docs/99-r12-frozen-requirements-baseline.md`, `docs/100-r12-requirements-traceability-and-no-loss-proof.md`, `docs/101-r12-freeze-governance-change-control-and-deferred-decisions.md` and `adr/HCT-ADR-0049-s1e-market-truth-foundation.md`.

## REQUIREMENTS

Every future implementation behavior and test must carry exact traceability to applicable locators, including:

- `REQ02::Trading intelligence requirements::B1`, `B7`, `B8`;
- `R05::Time and freshness requirements::B1` through `B5`;
- `R05::State coherency requirements::B1` through `B4`;
- `R05::Candle/cache/replay requirements::B1` through `B5`;
- `R05::Universe lifecycle requirements::B1` and `B2`;
- `R05::Authority requirements::B1` through `B3`;
- `R05::Validation requirements::B2`, `B3`, `B6`, `B8`, `B9`, `B10`, `B13`, `B15` and `B17` where applicable;
- `INT-002`, `INT-003`, `INT-004`, `INT-011`, `INT-012`, `INT-018`, `INT-022`, `INT-024`, `INT-025` and `INT-026`;
- `VAL-003`, `VAL-005`, `VAL-006`, `VAL-011`, `VAL-012`, `VAL-013`, `VAL-023`, `VAL-028` and `VAL-030`;
- `R11-REQ-006`, `R11-REQ-007`, `R11-REQ-011`, `R11-REQ-012`, `R11-REQ-013`, `R11-REQ-014`, `R11-REQ-015`, `R11-REQ-020`, `R11-REQ-022`, `R11-REQ-024` and `R11-REQ-025`;
- `HCT-DEC-0007`, `HCT-DEC-0008`, `HCT-DEC-0012`, `HCT-DEC-0058`, `HCT-DEC-0060`, `HCT-DEC-0061`, `HCT-DEC-0062`, `HCT-DEC-0063`, `HCT-DEC-0064`, `HCT-DEC-0065`, `HCT-DEC-0067`, `HCT-DEC-0068`, `HCT-DEC-0069`, `HCT-DEC-0071`, `HCT-DEC-0074`, `HCT-DEC-0077`, `HCT-DEC-0079`, `HCT-DEC-0083`, `HCT-DEC-0084`, `HCT-DEC-0089`, `HCT-DEC-0132`, `HCT-DEC-0135`, `HCT-DEC-0136`, `HCT-DEC-0138`, `HCT-DEC-0139`, `HCT-DEC-0140` and `HCT-DEC-0141`;
- ADR-0049 `Decision`, `Deterministic safety rules` and `Explicit non-scope`, especially the S1E Market-State/DataAuthority read-only boundary.

## ARCHITECTURE RULES

1. S1E Market-State and DataAuthority are the only upstream market-truth inputs. S2A accepts typed read-only snapshots and preserves source fingerprint, generation, environment, contract and freshness; it cannot recalculate, upgrade, replace or publish market truth.
2. Feature definitions and versions are immutable. Canonical IDs and behaviorally material hashes are authoritative; display names and UI labels are not.
3. Event time, knowledge time, wall-receive time and monotonic age are distinct. A feature is admissible only if its inputs were knowable by the declared point-in-time boundary.
4. Window closure, timeframe alignment, ordering, completeness and sample sufficiency are explicit. Mixed generation, stale/untrusted input, contradictory input, missing input and insufficient warmup produce restrictive typed states.
5. A feature value is analytical evidence only. It cannot create a candidate action, scanner rank, strategy signal, Brain admission, Risk approval, Execution plan or live authority.
6. `LIVE`, `PAPER`, `SHADOW` and `REPLAY` are non-aliasing environment identities. Fixture/replay data cannot reference live mutation capability.
7. Module 9 pattern ownership, regime, scanner, strategy, signal, microstructure, Brain, Risk and Execution remain separate owners and future work orders.
8. S2A remains provider/topology neutral and contains no network, persistence, deployment or credential behavior.

## CONSTRAINTS

- Do not modify `checkpoints/`, frozen requirement sources, dependency locks, ADR-0049, S1E product files or any runtime/product path in the authorization candidate.
- Candidate PR changed-file allowlist is exactly the candidate document, this authorization Work Order, the S2A implementation Work Order and the pull-request-only S2A governance workflow.
- The candidate cannot promote `HCT-CP-0030`, set implementation authority true or pre-authorize S2A.
- No claim of independent approval may be authored by the candidate creator.
- Any source drift, ambiguous dependency, ID collision, need for a fifth file or contradiction with a higher source is `BLOCKED`.

## ACCEPTANCE CRITERIA

- canonical base is exactly `625dd0c145087038bdbccd665548d811e187194c` and CP0030 is fail-closed;
- the four-file allowlist is exact and `git diff --check` passes;
- all required Work Order sections and source markers are present;
- S2A is bound read-only to S1E Market-State/DataAuthority and does not create a second market-truth owner;
- no-lookahead, warmup, stale/untrusted/unknown/degraded behavior and multi-timeframe boundaries are explicit;
- PO-F01 through PO-F10 are defined before implementation;
- the negative-scope firewall forbids network/provider/private/trading/persistence/deployment/live capability;
- exact-head pull-request-only CI validates base, head, checkpoint flags, allowlist, traceability and negative scope;
- candidate PR remains OPEN and UNMERGED for fresh independent HIGH_ASSURANCE review.

## TESTS

The future S2A implementation Work Order must predefine deterministic tests for:

- equal-input determinism and canonical serialization;
- mutation/fingerprint coverage for every material definition, input, version, window and boundary field;
- no-lookahead with future event time, knowledge time, later correction, late arrival, label maturity and replay ordering;
- warmup and insufficient sample failure; missing/unknown/invalid/stale/untrusted/contradictory/degraded input propagation;
- generation, contract, environment and source fingerprint isolation;
- deterministic multi-timeframe close-boundary alignment, incomplete intervals and mixed-generation rejection;
- registry canonical-ID immutability, version collision and display-name non-authority;
- non-authority attempts to produce scanner/strategy/signal/Brain/Risk/Execution outputs;
- fixture/replay sequence equality and explicit fidelity degradation;
- static negative scans for sockets, HTTP/WS URLs, provider hosts/DTOs, credentials, private APIs, orders, Risk/OMS/Execution, persistence, deployment and live flags.

## DELIVERABLES

- governance-only candidate document;
- complete S2A implementation Work Order;
- exact-head pull-request-only S2A governance workflow;
- author-side preflight evidence that is explicitly non-independent;
- one open, unmerged authorization PR and one authorization Issue;
- no S2A product/runtime code and no checkpoint promotion.

## REVIEW FORMAT

The independent review must report: `repositorySync`, `sourceMatch`, `canonicalBase`, `checkpoint`, `candidateAuthorizationId`, `candidateImplementationId`, `candidateScopeName`, `dependencyOrder`, `module8Classification`, `module9Separate`, `changedFiles`, `governanceOnlyDiff`, `exactTraceability`, `upstreamMarketTruthReadOnly`, `noLookaheadContract`, `validityAndWarmup`, `multiTimeframeBoundary`, `registryImmutability`, `proofObligations`, `negativeScopeFirewall`, `exactHeadRun`, `exactHeadJob`, `exactHeadConclusion`, `criticalFindings`, `highFindings`, `candidatePrOpenUnmerged` and `stopConditionRespected`.

## STOP CONDITION

Keep the candidate authorization PR OPEN and UNMERGED after exact-head governance CI. Do not merge it, promote an S2A implementation checkpoint, implement S2A, modify S1E, deploy, configure credentials, call private APIs, activate limited-live or trade. Fresh independent HIGH_ASSURANCE review is mandatory.
