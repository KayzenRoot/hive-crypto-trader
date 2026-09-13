# HCT-IMPL-AUTH-0009 — S2A Deterministic Feature & Indicator Foundation Authorization Candidate

Status: `PRE_AUTHORIZATION_REVIEW_REQUIRED`
Risk: `HIGH_ASSURANCE`
Canonical base: `main@625dd0c145087038bdbccd665548d811e187194c`
Current checkpoint: `HCT-CP-0030 / S1E_IMPLEMENTATION_APPROVED_MERGED`
Proposed authorization increment: `HCT-IMPL-AUTH-0009`
Proposed implementation slice: `HCT-IMP-0009-S2A`
Scope name: `Deterministic Feature & Indicator Foundation`
Authorization Issue: `#68`
Governance branch: `governance/HCT-IMPL-AUTH-0009-S2A`

## Objective

Prepare a governance-only candidate for the smallest necessary next dependency after the completed S1E Market Truth Foundation: a deterministic, provider-neutral, point-in-time Feature & Indicator Foundation for Module 8. This artifact defines a possible future implementation boundary, traceability, proof obligations and negative capability firewall. It does not implement product/runtime code, authorize implementation, promote a checkpoint or grant any live authority.

## Dependency proof

The frozen R11 dependency DAG places Stage 2 in this order:

`features/indicators/patterns -> regime -> scanner -> strategy engine/catalog/signal -> minimum microstructure`.

The R11 V1 classification marks Module 8 `Indicator & Feature Engine` as `V1_CORE` and Module 9 `Candlestick & Chart Pattern Engine` as `V1_MINIMUM`. S1E is complete and remains the sole upstream Market-State/DataAuthority source. Therefore S2A targets only the first deterministic Module 8 foundation. Module 9 patterns are a separate dependency and are not silently included.

## Source lock

The candidate is bound to `HCT-CP-0030`, the canonical base above, the source hierarchy, the Decisions Ledger, approved ADRs, Scope, Architecture, DoD and the R12 frozen baseline. The nine frozen requirement source identities remain:

- `docs/02-requirements.md` — `292da9552ae816e4d51b8a299456305da1658e55`;
- `docs/48-r04-execution-requirements-addendum.md` — `f20c1ed00bdb13801aaff8a3b648371bfcffba58`;
- `docs/54-r05-realtime-requirements-addendum.md` — `636ad01da9c25e760dd5e2f033b93a0f04578a17`;
- `docs/61-r06-intelligence-requirements-addendum.md` — `fea197e60532eb6ff3b11b628b9aabcbcfc00c41`;
- `docs/67-r07-validation-laboratory-requirements-addendum.md` — `c8a426966c5a0dc34704d1413f506332e770c2c7`;
- `docs/73-r08-multitenant-security-requirements-addendum.md` — `c859c0c4a718e3017c34aa50013d4c50959853b4`;
- `docs/80-r09-cockpit-uiux-requirements-addendum.md` — `bc897ebd470857a53055bdee85128b5bd31a5822`;
- `docs/87-r10-observability-audit-incident-finops-requirements-addendum.md` — `023187ef23b01d5a11f978bbfe6e38abf172bb3b`;
- `docs/93-r11-integration-requirements-addendum.md` — `6935e9973696d5b706546d63d847ea398780d936`.

Primary integration sources are `docs/91-r11-integrated-authority-state-dependency-architecture.md`, `docs/92-r11-v1-module-classification-and-integration-hardening.md`, `docs/93-r11-integration-requirements-addendum.md`, `docs/99-r12-frozen-requirements-baseline.md`, `docs/100-r12-requirements-traceability-and-no-loss-proof.md`, `docs/101-r12-freeze-governance-change-control-and-deferred-decisions.md`, `docs/10-decisions-ledger.md`, `docs/04-architecture.md` and `adr/HCT-ADR-0049-s1e-market-truth-foundation.md`.

## Proposed responsibility

If separately authorized, S2A may implement only:

- immutable typed `FeatureDefinition` / `FeatureVersion` identity and behavior fingerprint;
- an immutable registry with canonical IDs, versioning and collision/redefinition rejection; display names remain non-authoritative;
- `FeatureValue` / `FeatureSnapshot` evidence carrying environment, contract, source Market-State fingerprint, Market-State generation, DataAuthority/freshness evidence, event time, knowledge time, version, window metadata and validity state;
- point-in-time window boundaries, sample count, completeness, ordering, timeframe and close-boundary semantics;
- deterministic no-lookahead validation before a value is admitted;
- explicit `VALID`, `UNKNOWN`, `INVALID`, `WARMUP` and `DEGRADED` outcomes with fail-closed handling of missing, insufficient, stale, untrusted or contradictory upstream evidence;
- deterministic multi-timeframe alignment against explicit event/knowledge-time and close boundaries;
- bounded V1_CORE public/standard deterministic families only when the frozen sources require them, such as returns, rolling statistics, moving averages and volatility/range; the exact accepted family list must remain source-derived rather than invented;
- fixture/replay evaluation and provenance sufficient to reproduce feature output.

S2A consumes S1E Market-State and DataAuthority evidence through read-only typed contracts. Module 8 is not a second Market-State, data-quality or exchange-truth owner. Feature evidence is non-authoritative analytical evidence and cannot create a candidate trade, scanner ranking, strategy signal, risk decision or execution authority.

## Explicit exclusions

This candidate does not include:

- the full Module 9 candlestick/chart pattern engine;
- regime, scanner/ranking, strategy engine, strategy catalog, signal engine or microstructure/order-flow implementation;
- Brain, agents, RAG, memory, learning, calibration or promotion authority;
- Risk, Safety, Session Policy, sizing, leverage, OMS, Execution, reconciliation or protection authority;
- any provider endpoint, socket, WebSocket, network client, credential, private API, signing or live data call;
- persistence, database, RLS, feature store, HA/fencing, deployment or infrastructure topology;
- mutation of S1E Market-State, DataAuthority, checkpoint, frozen requirements or dependency locks;
- production credentials, production deployment, limited-live or live/real-money trading.

## Required proof obligations

- `PO-F01` determinism: equal canonical inputs and definition versions produce equal values and fingerprints;
- `PO-F02` material mutation visibility: every behaviorally material definition, input, window, version and boundary mutation changes the relevant fingerprint;
- `PO-F03` no lookahead: future event, knowledge, correction, label or later-arriving information is rejected from a prior feature boundary;
- `PO-F04` warmup fail closed: insufficient samples produce `WARMUP`/`UNKNOWN`, never fabricated valid values;
- `PO-F05` trust propagation: stale, untrusted, contradictory or invalid S1E evidence cannot become `VALID` through scoring or default values;
- `PO-F06` generation/environment isolation: `PAPER`, `SHADOW`, `REPLAY` and `LIVE` identities and Market-State generations cannot alias;
- `PO-F07` multi-timeframe boundary: aligned windows use explicit close/event/knowledge boundaries and reject incomplete or mixed generations;
- `PO-F08` registry immutability/versioning: canonical IDs cannot be redefined silently and display names cannot substitute for identity;
- `PO-F09` non-authority: feature evidence cannot create trading, scanner, strategy, Brain, Risk or Execution authority;
- `PO-F10` replay fidelity: pinned fixtures/replay reproduce the same feature sequence and disclose degraded fidelity.

## Authorization firewall

Until a later authorization checkpoint is independently approved and promoted, canonical authority remains:

- `implementation_authorized=false`;
- `implementation_authorization_scope=[]`;
- `implementation_authorization_ceiling=NONE_PENDING_NEXT_GOVERNED_AUTHORIZATION`;
- `production_credentials_authorized=false`;
- `production_deployment_authorized=false`;
- `limited_live_authorized=false`;
- `live_trading_authorized=false`.

Planning readiness, a green governance workflow, this candidate, an open PR or an approved review must not be interpreted as implementation or live-trading authorization.

## Required independent review

The author-side candidate evidence is not independent approval. A fresh independent HIGH_ASSURANCE review must inspect the exact candidate head, the four-file governance-only diff, source traceability, S1E read-only dependency, no-lookahead contract, negative scope and exact-head CI. The candidate PR must remain OPEN and UNMERGED.

## Stop condition

Stop after the S2A authorization PR is OPEN and UNMERGED with exact-head pull-request-only governance CI green. Do not merge it, promote an S2A implementation checkpoint, create S2A product/runtime code, deploy, add credentials, call private APIs, activate limited-live or trade. Any base/checkpoint/source/ID ambiguity or any need for a runtime/product/checkpoint/frozen/dependency-lock file change is `BLOCKED`.
