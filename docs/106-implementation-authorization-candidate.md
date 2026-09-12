# HCT-IMPL-AUTH-0001 — Bounded Implementation Authorization Candidate

Status: `INDEPENDENT_REVIEW_REQUIRED`
Risk class: `HIGH_ASSURANCE`
Canonical baseline: `HCT-CP-0014 / PLANNING_FREEZE_APPROVED`
Baseline main: `f201d866f96eb6bb86ecc2212535b6129a9511d4`
Frozen requirements authority: R12 composite baseline promoted by `HCT-CP-0014`

## Objective
Authorize the first bounded product-code increment only after independent HIGH_ASSURANCE review. The authorization is deliberately narrow and does not grant exchange connectivity, production credentials, production deployment, limited-live, or real-money trading authority.

## Proposed authorized slice
`HCT-IMP-0001-S0A — Runtime, Repository & Canonical Contract Foundation`

The slice implements only the first safe portion of R11 Stage 0:
- canonical repository/runtime skeleton;
- independently buildable frontend and backend application roots;
- language-neutral/shared API/domain contract source;
- typed cross-domain identity primitives;
- environment namespace primitives (`LIVE`, `PAPER`, `SHADOW`, `REPLAY`) with fail-closed separation semantics;
- canonical error envelope;
- configuration/version/release identity primitives;
- audit/evidence envelope primitives;
- health/readiness/version endpoints and a non-authoritative frontend status shell;
- CI/build/lint/type/test scaffolding for the slice.

## Explicitly NOT authorized in S0A
- MEXC or any exchange API connectivity;
- API keys, secrets, credential storage, credential validation or signing;
- order creation, cancellation, replacement or any state-changing exchange command;
- portfolio/risk/sizing/leverage logic;
- OMS, fills, positions, balances, reconciliation or protection logic;
- market-data WebSocket/REST ingest;
- strategy, indicators, scanner, Brain, agents, RAG, learning or Copilot;
- database persistence containing production/user/exchange state;
- production deployment;
- limited-live or real-money trading;
- simulated functionality that can accidentally route to a live mutation capability.

## Architecture basis
R11 dependency Stage 0 requires canonical contracts/governance/security foundations before exchange truth or higher intelligence. S0A intentionally implements the non-secret/non-exchange contract/runtime substrate first, while leaving SecurityContext enforcement and SecretStore implementation for subsequent bounded Stage-0 slices.

Frontend remains an untrusted client. Backend owns authority/security/business logic. Shared contracts may describe state but never move authority into the UI.

## Technology-selection boundary
The implementation executor may select and pin current stable language/framework/tool versions only within the following architecture constraints:
- backend technology must support deterministic typed validation, async/network services, strong testing and future quantitative/ML integration;
- frontend technology must support a modern typed web application and independent build/deploy lifecycle;
- cross-runtime contracts must have one canonical language-neutral source or generation path to prevent semantic drift;
- dependencies must be pinned/locked and pass supply-chain/security review appropriate to this non-production slice;
- a short ADR must record the chosen stack and why it satisfies the frozen architecture before substantive code is added.

Technology choice must not change product scope or authority semantics. If the choice would materially alter the frozen architecture, STOP and request governed change control.

## Authorization semantics
If this candidate receives independent `APPROVED`, is merged and checkpoint-promoted:
- `implementation_authorized=true` only for `HCT-IMP-0001-S0A`;
- authorization ceiling = `NON_TRADING_STAGE_0_FOUNDATION_ONLY`;
- every other product-code increment remains unauthorized until separately governed or explicitly included by a later checkpoint;
- `production_credentials_authorized=false`;
- `production_deployment_authorized=false`;
- `limited_live_authorized=false`;
- `live_trading_authorized=false`.

## Required implementation controls
The implementation Work Order SHALL:
- Context Lock to the exact authorization checkpoint and `main` SHA;
- map every implemented primitive to frozen requirements/architecture source locators;
- keep all exchange/live mutation capabilities absent;
- use deterministic tests for environment/identity/error/version contract semantics;
- prove frontend/backend independent builds;
- prove generated/shared contracts are reproducible and drift-detectable;
- include lint/type/static checks, unit/contract tests and dependency lockfiles;
- include no secret material;
- preserve a clean rollback path because no persistent production data exists in this slice;
- stop with implementation PR open for independent review.

## Acceptance criteria for authorization
1. Planning Freeze remains `APPROVED` and unchanged.
2. Selected slice follows R11 Stage-0 dependency ordering.
3. Slice scope cannot reach external money/exchange mutation.
4. Exact out-of-scope list is explicit and enforceable.
5. Required evidence/test classes are explicit.
6. Authorization is bounded to one stable implementation Work Order.
7. Higher-stage authorization flags remain false.
8. Independent reviewer finds zero unresolved CRITICAL/HIGH authorization defect.

## Proposed checkpoint delta after approval
- next checkpoint: `HCT-CP-0015`;
- status: `IMPLEMENTATION_AUTHORIZED_S0A`;
- completed increment: `HCT-IMPL-AUTH-0001`;
- `implementation_authorized=true`;
- `implementation_authorization_scope=["HCT-IMP-0001-S0A"]`;
- `implementation_authorization_ceiling="NON_TRADING_STAGE_0_FOUNDATION_ONLY"`;
- all production/live authorization flags remain false;
- next necessary action: execute `HCT-IMP-0001-S0A` through governed branch → tests/evidence → PR → independent review.

## Independent review verdict
Exactly one:
- `APPROVED`
- `CORRECTION REQUIRED`
- `BLOCKED`

## STOP CONDITION
Do not begin product implementation from this candidate. Keep implementation unauthorized until this authorization candidate receives an independent HIGH_ASSURANCE `APPROVED`, is merged into `main`, and `HCT-CP-0015` is promoted. No production/live authority is granted by this document.