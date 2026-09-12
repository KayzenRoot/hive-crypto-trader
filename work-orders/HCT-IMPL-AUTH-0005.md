# HCT-IMPL-AUTH-0005 - Implementation Authorization Work Order

Status: `COMPLETED_APPROVED`
Risk class: `HIGH_ASSURANCE`
Authorization issue: `#49`
Authorization PR: `#50`
Implementation issue: `#51`
Canonical pre-authorization checkpoint: `HCT-CP-0022 / S1A_IMPLEMENTATION_APPROVED_MERGED`
Canonical authorization checkpoint: `HCT-CP-0023 / IMPLEMENTATION_AUTHORIZED_S1B`
Authorization base: `main@3ee039deafbfc5505f0b74ce38c721aa384a0953`
Approved authorization candidate head: `692ebfe5ffa18546e72ae047ac6073d3ffd59442`
Authorization merge: `e7077ab949ca0ecde5fd04d33c869d9d7404b34c`
Authorized implementation slice: `HCT-IMP-0005-S1B`
Authorization ceiling: `NON_TRADING_STAGE_1_MEXC_PUBLIC_REFERENCE_CAPABILITY_RESOLVER_ONLY`

## OBJECTIVE
Decide whether HCT may authorize exactly one new bounded Stage-1 implementation slice that introduces a concrete MEXC Futures adapter only for public, unauthenticated, read-only reference/capability discovery behind the completed S1A provider-neutral boundary.

Decision: `APPROVED` and promoted through `HCT-CP-0023`.

## CONTEXT
`HCT-CP-0022` recorded S1A as independently approved and merged and reset product implementation authority to fail closed. R11 Stage 1 orders Exchange Abstraction + MEXC adapter before Universe, quota/WS, market ingest, quality, Market-State Fabric and cache.

S1A established HCT-owned exchange identities, immutable capability/reference models and a read-only adapter port without concrete venue networking. The next smallest dependency is a public-reference-only MEXC implementation that can translate official public contract/rule evidence into those canonical models while remaining unauthenticated and non-trading.

## REQUIRED SOURCES
Priority follows `docs/00-source-hierarchy.md`.

The authorization review covered at minimum:
- `checkpoints/workstreams/planning/latest.json`;
- `checkpoints/history/HCT-CP-0022.json`;
- `docs/11-checkpoint.md`;
- `docs/02-requirements.md` Market and exchange requirements;
- `docs/10-decisions-ledger.md` including `HCT-DEC-0023`;
- `docs/14-product-module-map.md` Modules 1-4 and 29;
- `docs/23-multi-exchange-adapter-architecture.md`;
- `docs/54-r05-realtime-requirements-addendum.md`;
- `docs/91-r11-integrated-authority-state-dependency-architecture.md`;
- `docs/93-r11-integration-requirements-addendum.md`;
- `docs/99-r12-frozen-requirements-baseline.md`;
- `docs/100-r12-requirements-traceability-and-no-loss-proof.md`;
- `docs/117-s1a-implementation-approval-and-checkpoint-promotion.md`;
- `docs/118-implementation-authorization-s1b-candidate.md`;
- `work-orders/HCT-IMP-0005-S1B.md`;
- Issue #49 and PR #50 evidence.

## APPROVED AUTHORIZATION BOUNDARY
Exactly:

`HCT-IMP-0005-S1B - MEXC Public Reference Adapter & Capability/Rule Resolver`

The implementation Work Order may authorize only:
- concrete MEXC Futures public reference REST transport needed for exchange/contract/rule discovery;
- translation into existing S1A HCT-owned canonical reference/capability models;
- explicit fail-closed capability/rule resolution;
- strict payload/schema/decimal validation;
- fixed timeout/response-bound handling appropriate to public reference reads;
- deterministic fixture/mocked-transport tests;
- official-provider mapping evidence;
- S0A/S0B/S0C/S1A regression, scans, audits and exact-head CI.

## EXPLICITLY NOT AUTHORIZED
- WebSocket/streaming/subscription/reconnect/session generation;
- public realtime market ingest;
- private/account/order/position/balance APIs or streams;
- API keys/authentication/signing/credential lifecycle;
- order placement/cancel/replace or leverage/margin mutations;
- OMS/fills/positions/balances/reconciliation/protection;
- Market Universe eligibility runtime;
- quota/WS/backpressure governor runtime;
- Data Quality/Freshness, Market-State Fabric, order-book reconstruction or cache;
- persistence/database/RLS;
- public trading routes/frontend controls;
- production deployment;
- limited-live/real-money trading;
- later Stage-1 or Stage-2+ work.

## INDEPENDENT REVIEW RESULT
Independent reviewer stream: `Codex independent execution stream`

Verdict: `APPROVED`

Exact reviewed base:
`3ee039deafbfc5505f0b74ce38c721aa384a0953`

Exact reviewed head:
`692ebfe5ffa18546e72ae047ac6073d3ffd59442`

Finding counts:
- CRITICAL: `0`
- HIGH: `0`

Independent evidence:
- PR #50 comment `5647988390`;
- Issue #49 comment `5647988480`.

Governance acceptance evidence:
- PR #50 comment `5648018965`;
- Issue #49 comment `5648019880`.

Exact-head authorization CI:
- workflow: `HCT-IMPL-AUTH-0005 S1B Authorization Governance`;
- run: `34712055642`;
- job/check: `implementation-authorization-s1b-governance / 103602466585`;
- event: `pull_request`;
- conclusion: `success`;
- all substantive steps: `PASS`.

## POST-APPROVAL AUTHORITY
`HCT-CP-0023` establishes:
- `implementation_authorized=true`;
- `implementation_authorization_scope=["HCT-IMP-0005-S1B"]`;
- `implementation_authorization_ceiling="NON_TRADING_STAGE_1_MEXC_PUBLIC_REFERENCE_CAPABILITY_RESOLVER_ONLY"`;
- `production_credentials_authorized=false`;
- `production_deployment_authorized=false`;
- `limited_live_authorized=false`;
- `live_trading_authorized=false`.

Unknown or ambiguous authority fails closed.

## RESOLUTION
Authorization gate: `COMPLETED_APPROVED`.

The authoring/review stream STOP CONDITION was satisfied before governance acceptance. PR #50 was merged only after independent approval and fresh exact-base/head/CI revalidation. Product implementation may begin only under the separate execution flow anchored to `HCT-CP-0023` and Work Order `HCT-IMP-0005-S1B`.
