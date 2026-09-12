# HCT-IMPL-AUTH-0005 - Implementation Authorization Work Order

Status: `INDEPENDENT_REVIEW_REQUIRED`
Risk class: `HIGH_ASSURANCE`
Authorization issue: `#49`
Canonical checkpoint: `HCT-CP-0022 / S1A_IMPLEMENTATION_APPROVED_MERGED`
Canonical base: `main@3ee039deafbfc5505f0b74ce38c721aa384a0953`
Candidate implementation slice: `HCT-IMP-0005-S1B`
Proposed authorization ceiling: `NON_TRADING_STAGE_1_MEXC_PUBLIC_REFERENCE_CAPABILITY_RESOLVER_ONLY`

## OBJECTIVE
Decide whether HCT may authorize exactly one new bounded Stage-1 implementation slice that introduces a concrete MEXC Futures adapter only for public, unauthenticated, read-only reference/capability discovery behind the completed S1A provider-neutral boundary.

No product code is authorized by this Work Order itself.

## CONTEXT
`HCT-CP-0022` records S1A as independently approved and merged and resets product implementation authority to fail closed. R11 Stage 1 orders Exchange Abstraction + MEXC adapter before Universe, quota/WS, market ingest, quality, Market-State Fabric and cache.

S1A established HCT-owned exchange identities, immutable capability/reference models and a read-only adapter port without concrete venue networking. The next smallest dependency is a public-reference-only MEXC implementation that can translate official public contract/rule evidence into those canonical models while remaining unauthenticated and non-trading.

## REQUIRED SOURCES
Priority follows `docs/00-source-hierarchy.md`.

At minimum review:
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
- Issue #49.

## AUTHORIZATION PRECONDITION
Candidate review is valid only while canonical main remains `3ee039deafbfc5505f0b74ce38c721aa384a0953` and `HCT-CP-0022` proves:
- `implementation_authorized=false`;
- `implementation_authorization_scope=[]`;
- `implementation_authorization_ceiling="NONE_PENDING_NEXT_GOVERNED_AUTHORIZATION"`;
- `production_credentials_authorized=false`;
- `production_deployment_authorized=false`;
- `limited_live_authorized=false`;
- `live_trading_authorized=false`.

Any drift fails closed until explicitly reconciled.

## CANDIDATE AUTHORIZATION
Exactly:

`HCT-IMP-0005-S1B - MEXC Public Reference Adapter & Capability/Rule Resolver`

Ceiling:

`NON_TRADING_STAGE_1_MEXC_PUBLIC_REFERENCE_CAPABILITY_RESOLVER_ONLY`

## REQUIRED AUTHORIZATION BOUNDARY
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

## REVIEW OBLIGATIONS
Independent reviewer must verify:
1. exact base/head and governance-only candidate diff;
2. CP0022 fail-closed state;
3. S1A completion provenance;
4. R11 dependency ordering and direct frozen requirement alignment;
5. public/read-only/unauthenticated scope;
6. no WebSocket/private/auth/signing/trading/money-state authority;
7. implementation Work Order includes objective, context, scope, negative scope, architecture constraints, acceptance criteria, tests/evidence, review format and STOP CONDITION;
8. exact-head authorization-governance CI succeeds;
9. CRITICAL=0 and HIGH=0 for approval.

## VERDICT
Exactly one:
- `APPROVED`
- `CORRECTION REQUIRED`
- `BLOCKED`

## STOP CONDITION
Do not merge the authorization PR, promote `HCT-CP-0023`, begin S1B product code, create credentials, connect WebSockets/private APIs, deploy production, activate limited-live or enable real-money trading from the authoring stream. Stop after exact-head evidence and independent review handoff.
