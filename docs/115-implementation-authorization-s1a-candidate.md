# HCT-IMPL-AUTH-0004 - S1A Implementation Authorization Candidate

Status: `INDEPENDENT_REVIEW_REQUIRED`
Risk class: `HIGH_ASSURANCE`
Authorization increment: `HCT-IMPL-AUTH-0004`
Issue: `#45`
Candidate implementation slice: `HCT-IMP-0004-S1A`
Canonical base: `main@aa2aea7e6bf9b148c6c212f454eb0e5c0db772e5`
Canonical checkpoint: `HCT-CP-0020 / S0C_IMPLEMENTATION_APPROVED_MERGED`
Proposed post-approval checkpoint: `HCT-CP-0021 / IMPLEMENTATION_AUTHORIZED_S1A`

## Purpose
Evaluate whether exactly one bounded first R11 Stage-1 contract slice may be authorized after the independently approved S0A, S0B and S0C foundations.

This candidate grants no product-code authority until a separate HIGH_ASSURANCE execution stream independently reviews the exact candidate head, the authorization-governance check succeeds on that same head, the authorization PR is governed-merged, and a checkpoint promotion explicitly authorizes only `HCT-IMP-0004-S1A`.

## Current authoritative state
At `HCT-CP-0020`:
- `implementation_authorized=false`
- `implementation_authorization_scope=[]`
- `implementation_authorization_ceiling="NONE_PENDING_NEXT_GOVERNED_AUTHORIZATION"`
- `production_credentials_authorized=false`
- `production_deployment_authorized=false`
- `limited_live_authorized=false`
- `live_trading_authorized=false`

Planning remains frozen under `HCT-CP-0014`. S0A, S0B and S0C are independently approved and merged. Stage 1 has not yet been authorized.

## Why S1A is the next bounded dependency
R11 Stage 1 is `Exchange and realtime truth` and begins with:
- Exchange Abstraction + MEXC adapter;
- capability/rule resolver;
- universe;
- quota/WS governor;
- market ingest, quality, Market-State Fabric and cache.

The first safe dependency inside that stage is the HCT-owned exchange abstraction and immutable capability/contract reference model. A concrete MEXC transport adapter cannot be introduced cleanly until core code has a provider-neutral boundary that prevents MEXC payloads, symbols and capability assumptions from becoming de facto canonical domain truth.

This ordering is also required by `HCT-DEC-0023`: V1 is MEXC-first, but core strategy/risk/UI domains depend on an HCT-owned Exchange Abstraction & Adapter Framework. `docs/23-multi-exchange-adapter-architecture.md` states the same boundary as `HCT Core -> Exchange Capability Interface -> Exchange Adapter -> MEXC/Binance/Future Exchange`.

S1A therefore authorizes only the abstraction/reference-contract substrate. It deliberately stops before concrete MEXC networking, universe discovery, realtime market data or trading commands.

## Frozen source alignment
This candidate is interpreted under `docs/00-source-hierarchy.md` and the R12 frozen composite baseline.

Direct requirement locators:
- `REQ02::Market and exchange requirements::B2` — discover contract capabilities/constraints dynamically where exposed;
- `REQ02::Market and exchange requirements::B5` — regional/API capability restrictions and exchange API changes are versioned external dependencies;
- `REQ02::Market and exchange requirements::B7` — core trading modules depend on HCT-owned canonical exchange/domain interfaces;
- `REQ02::Market and exchange requirements::B8` — MEXC is the first concrete adapter, future venues require explicit mapping/governance;
- `REQ02::Market and exchange requirements::B9` — maintain an explicit exchange capability matrix and reject/degrade unsupported functionality visibly;
- `R11-REQ-006` — one canonical owner per authoritative state family; projections do not become competing truth;
- `R11-REQ-012` — typed/stable cross-domain identity and explicit material versions/hashes;
- `R11-REQ-013` — capabilities declare dependencies, degraded behavior and recovery expectations;
- `R11-REQ-014` — implementation follows the dependency DAG and establishes exchange truth before higher intelligence/automation;
- `R11-REQ-024` — logical module boundaries remain provider/topology-neutral until separately authorized.

Supporting architecture/decision sources:
- `HCT-DEC-0023` in `docs/10-decisions-ledger.md`;
- `docs/14-product-module-map.md` Modules 1 and 2;
- `docs/23-multi-exchange-adapter-architecture.md`;
- `docs/91-r11-integrated-authority-state-dependency-architecture.md` Stage 1 and canonical identity/source-of-truth sections.

R05 realtime transport, quota, connection-generation, market ingest, Data Quality and Market-State requirements remain binding for later Stage-1 slices, but S1A does not claim to implement them.

## Proposed authorization
After independent approval, governed merge and checkpoint promotion, authorize exactly:

`HCT-IMP-0004-S1A - Exchange Abstraction, Capability & Contract Reference Foundation`

Proposed ceiling:

`NON_TRADING_STAGE_1_EXCHANGE_ABSTRACTION_CAPABILITY_CONTRACT_FOUNDATION_ONLY`

## Proposed S1A scope
### 1. Canonical exchange identity and reference contracts
Extend the existing canonical contract system rather than inventing a parallel identity layer.

The bounded slice may define immutable typed/versioned primitives for:
- exchange identity;
- canonical instrument/contract identity;
- exchange-native symbol mapping as metadata, never sole canonical identity;
- capability snapshot identity/version/fingerprint;
- contract-spec/reference snapshot identity/version/fingerprint;
- exchange descriptor/version metadata required to explain the source of a reference snapshot.

Stateful identities remain subject to the existing LIVE/PAPER/SHADOW/REPLAY rules where environment is materially applicable. Non-stateful exchange/contract reference identity must not be artificially overloaded with mutable display names.

### 2. Explicit capability semantics
Define a controlled capability taxonomy and immutable capability snapshot sufficient to represent at minimum:
- `SUPPORTED`;
- `UNSUPPORTED`;
- `UNKNOWN` / not proven.

Additional restrictive states such as regional/account restriction MAY be modeled when justified by frozen requirements, but `UNKNOWN` must never be silently treated as supported.

Capability metadata describes venue/reference capability only. It does not itself grant Security, Risk, Execution, credential or trading authority.

### 3. Canonical contract/reference specification
Define a provider-neutral immutable contract/reference model for the non-secret venue facts later adapters must normalize, such as canonical identity, venue symbol mapping, lifecycle state, base/quote/settlement concepts, contract type and bounded precision/quantity/rule metadata where known.

Unknown material values must remain explicit. The model must not invent permissive defaults for venue rules.

### 4. Read-only exchange reference adapter port
Define a narrow provider-neutral port/protocol for reading exchange descriptor, capability and contract-reference snapshots.

This port is a domain boundary only. S1A SHALL NOT implement a production MEXC adapter, HTTP/REST/WebSocket client, SDK integration, authentication, signing, private account access or any state-changing command method.

No method in this slice may place/cancel/replace orders, change leverage/margin mode, mutate exchange state or return secret material.

### 5. Deterministic test doubles only
A null/fake/in-memory deterministic adapter MAY exist solely for tests and architectural proof. It must not make network calls, read environment credentials, use real API keys or masquerade as a production venue adapter.

### 6. Canonical error/degradation semantics
Define only the bounded error/result vocabulary needed for this read-only reference boundary, such as unknown contract, unsupported/unknown capability, malformed reference data and reference unavailable.

No transient network retry engine, quota scheduler, circuit-breaker runtime or reconnect policy is implemented in S1A.

### 7. Proof and regression
Implementation must prove that the abstraction is deterministic, provider-neutral, fail-closed and does not introduce exchange connectivity or trading authority. Existing S0A/S0B/S0C contract, security and provenance guarantees remain green.

## Explicitly out of scope
S1A SHALL NOT implement or authorize:
- product-code mutation before authorization approval/checkpoint promotion;
- concrete MEXC adapter implementation;
- MEXC REST/WebSocket/SDK/network connectivity;
- any runtime HTTP/WebSocket/socket client or live external exchange call;
- authentication, request signing, API key handling, credential import/verification/rotation/revocation or secret material;
- private/account/order/position streams;
- public realtime market-data ingest;
- Market Universe eligibility/scanning lifecycle engine;
- API Quota, WebSocket & Backpressure Governor runtime;
- reconnect/resubscribe/session-generation logic;
- Data Quality & Freshness Engine;
- coherent Market-State Fabric, order-book reconstruction or cache/hot-state implementation;
- order placement, cancel/replace, trigger orders, TP/SL, trailing, leverage/margin mutation or any exchange command;
- fills, positions, balances, OMS, reconciliation or protection;
- Session Policy, Safety, Portfolio Exposure, Position Sizing, Leverage, RiskSnapshot or Risk Reservation;
- persistence/database/RLS;
- public API routes or frontend trading UI for these capabilities;
- production deployment;
- limited-live or real-money trading;
- later Stage-1 slices or Stage 2+ implementation.

## Proof obligations
An implementation candidate under this authorization SHALL prove at minimum:
1. Exchange identity, contract identity and snapshot identity/version semantics reuse/extend the canonical S0A contract model rather than create an ungoverned shadow identity system.
2. Canonical identity never relies only on an exchange-native mutable/display symbol.
3. Capability snapshots are immutable/versioned/fingerprintable and materially changed capability state changes the fingerprint/version evidence.
4. `UNKNOWN` capability state fails closed and is never interpreted as supported.
5. Unsupported capability remains explicit; no silent emulation path exists in S1A.
6. Contract/reference snapshots are immutable and reject malformed or internally inconsistent precision/quantity/rule metadata.
7. Missing material venue rule/reference state remains explicit rather than receiving a permissive default.
8. The provider-neutral adapter port is read-only and contains no state-changing exchange command surface.
9. Test doubles are deterministic, network-free and credential-free.
10. Core canonical models contain no MEXC request/response payload types.
11. S1A introduces no production MEXC client, runtime HTTP/WebSocket/socket client, authentication/signing code or credential/secret material.
12. S1A introduces no market ingest, universe engine, quota governor, Data Quality, Market-State or cache runtime.
13. S1A introduces no order/OMS/reconciliation/protection/risk/trading authority.
14. Existing S0A/S0B/S0C tests, contract generation/parity, security/provenance boundaries and secret scans remain green.
15. Dependency audits, lint/format/type/build and unauthorized-capability scans pass on the exact candidate head.
16. Exact raw-head implementation CI/evidence passes before independent implementation review.
17. A fresh independent HIGH_ASSURANCE review returns `APPROVED` with unresolved CRITICAL=0 and HIGH=0 before merge.

## Proposed post-approval flags
Only after a later checkpoint promotion:
- `implementation_authorized=true`
- `implementation_authorization_scope=["HCT-IMP-0004-S1A"]`
- `implementation_authorization_ceiling="NON_TRADING_STAGE_1_EXCHANGE_ABSTRACTION_CAPABILITY_CONTRACT_FOUNDATION_ONLY"`
- `production_credentials_authorized=false`
- `production_deployment_authorized=false`
- `limited_live_authorized=false`
- `live_trading_authorized=false`

Authorization of an exchange abstraction does not imply authorization of a concrete exchange connection.

## Known governance-maintenance gap
`HCT-CP-0020` records that the historical S0B workflow contains a stale hardcoded authorization-base assertion and may fail on later broad backend changes. This candidate does not silently modify that unrelated workflow. If its remediation becomes necessary, it must be handled by an explicit bounded governance/CI-maintenance increment. S1A implementation evidence must directly rerun the required S0B regression regardless of that historical workflow's status.

## Independent review requirements
The reviewer SHALL reconstruct the verdict from repository evidence and verify:
- exact PR base/head identity;
- canonical `HCT-CP-0020` fail-closed state;
- S0A/S0B/S0C completion provenance;
- R11 transition from completed Stage 0 into the first bounded Stage-1 dependency;
- `HCT-DEC-0023`, Modules 1/2 and `docs/23` alignment;
- all direct frozen locators listed above;
- provider-neutral/read-only scope and no concrete MEXC/network implementation;
- no credentials/signing/private streams/market ingest/order commands;
- implementation Work Order completeness, negative tests, evidence obligations and STOP CONDITION;
- exact-head authorization-governance CI success;
- zero unresolved CRITICAL/HIGH findings.

Verdict exactly one of:
- `APPROVED`
- `CORRECTION REQUIRED`
- `BLOCKED`

## STOP CONDITION
Do not begin product implementation from this document. Keep the authorization PR open and unmerged until exact-head authorization-governance CI succeeds and a separate HIGH_ASSURANCE/HEDS Delta execution stream publishes its verdict for the exact head. Merge/promotion may authorize only `HCT-IMP-0004-S1A`. No concrete exchange connectivity, production credentials, production deployment, limited-live or live trading are authorized by this candidate.
