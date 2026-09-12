# Work Order — HCT-IMP-0001-S0A

Status: `PENDING_AUTHORIZATION`
Risk: `HIGH_ASSURANCE`
Authorization dependency: `HCT-IMPL-AUTH-0001`
Planning baseline: `HCT-CP-0014 / PLANNING_FREEZE_APPROVED`

## OBJECTIVE
Implement the first bounded Stage-0 foundation slice after explicit authorization: runtime/repository skeleton plus canonical contract primitives, with no exchange, credentials, money-state or production/live capability.

## CONTEXT
R11 Stage 0 precedes all exchange/realtime/intelligence/risk/execution stages. This slice intentionally establishes only the non-secret, non-trading substrate required by later work.

## SCOPE
1. Establish independently buildable frontend and backend application roots inside the canonical monorepo.
2. Establish one canonical language-neutral contract source or deterministic generation path for cross-runtime contracts.
3. Implement typed identity primitives required by the first slice, including environment namespace.
4. Implement canonical error/version/release/audit-envelope primitives with no privileged behavior.
5. Implement backend health/readiness/version endpoints only.
6. Implement a frontend status shell that consumes only non-authoritative health/version information.
7. Add deterministic lint/type/static/unit/contract/build checks and lockfiles.
8. Record a technology/toolchain ADR before substantive implementation.

## OUT OF SCOPE
- MEXC or any exchange client/adapter;
- public/private exchange network calls;
- WebSocket market ingest;
- API keys, secrets, signing or SecretStore implementation;
- authentication provider integration or production SecurityContext enforcement;
- database-backed user/account/market/trading persistence;
- trading candidates, strategies, signals or indicators;
- Safety, Session Policy, Risk, sizing, leverage or reservation;
- OMS/orders/fills/positions/balances/reconciliation/protection;
- RAG/models/agents/Brain/Copilot;
- production deployment;
- limited-live/live trading.

## FILES / SOURCES TO READ
At minimum:
- `docs/11-checkpoint.md`;
- `docs/00-source-hierarchy.md`;
- `docs/09-definition-of-done.md`;
- `docs/04-architecture.md`;
- `docs/10-decisions-ledger.md`;
- `docs/91-r11-integrated-authority-state-dependency-architecture.md`;
- `docs/93-r11-integration-requirements-addendum.md`;
- `docs/99-r12-frozen-requirements-baseline.md`;
- `docs/100-r12-requirements-traceability-and-no-loss-proof.md`;
- `docs/101-r12-freeze-governance-change-control-and-deferred-decisions.md`;
- `docs/106-implementation-authorization-candidate.md`;
- this Work Order.

## REQUIREMENTS
- code begins only if canonical checkpoint explicitly authorizes this exact Work Order;
- every cross-domain identity is typed/stable and environment-aware where stateful;
- `LIVE`, `PAPER`, `SHADOW`, `REPLAY` are distinct canonical environment values and tests prevent accidental interchange;
- frontend is non-authoritative and contains no secrets or hard trading logic;
- cross-runtime contract generation is reproducible and drift-detectable;
- health/readiness/version surfaces expose no secret/private operational data;
- dependencies are pinned/locked;
- no hidden external calls are introduced;
- no production data mutation exists.

## ARCHITECTURE RULES
- follow Stage-0 dependency direction;
- choose the smallest architecture that preserves later extensibility without premature Stage-1+ implementation;
- backend is authority boundary; frontend is untrusted projection;
- one canonical contract source/generation path;
- deterministic validation and fail-closed parsing;
- no shadow source of truth;
- no material frozen-semantic change without governed change control.

## CONSTRAINTS
- no credentials of any kind;
- no exchange SDK/client dependency unless only a compile-time placeholder is objectively necessary, otherwise prohibited;
- no live-capable URL/client/config defaults;
- no production deployment;
- no force push/history rewrite;
- preserve repository documentation/governance history;
- first implementation prompt must synchronize repository and Context Lock exact state.

## ACCEPTANCE CRITERIA
A. Authorized checkpoint and exact main SHA validated before mutation.
B. Technology/toolchain ADR exists before substantive code.
C. Frontend and backend each build independently.
D. Contract source/generation is reproducible from a clean checkout.
E. Typed-ID and environment-isolation tests pass.
F. Invalid/unknown environment and malformed IDs fail closed.
G. Error/version/audit-envelope contract tests pass.
H. Health/readiness/version endpoints pass deterministic tests.
I. Frontend status shell uses only safe backend status/version contract.
J. Repository has working lint/type/static/unit/contract/build commands.
K. Dependency lockfiles are committed and no secret material is present.
L. No exchange/network-mutation/trading functionality exists in the diff.
M. CI passes on exact PR head.
N. Independent HIGH_ASSURANCE review returns `APPROVED` with zero unresolved CRITICAL/HIGH.

## TESTS
- unit tests for identity/environment/error/version primitives;
- negative tests for invalid namespace and cross-environment identity misuse;
- schema/contract generation reproducibility test;
- frontend/backend independent build tests;
- backend endpoint tests;
- static secret scan for committed candidate changes;
- dependency vulnerability/supply-chain scan appropriate to selected ecosystem;
- diff-boundary audit proving no unauthorized exchange/trading modules were introduced.

## DELIVERABLES
- toolchain ADR;
- application/runtime skeleton;
- canonical/shared contract source and generated artifacts if used;
- tests and CI configuration;
- implementation evidence summary;
- implementation PR;
- proposed checkpoint delta only after independent approval.

## REVIEW FORMAT
Independent reviewer returns exactly one:
- `APPROVED`
- `CORRECTION REQUIRED`
- `BLOCKED`

## STOP CONDITION
Stop with implementation PR OPEN/unmerged after exact-head CI/evidence. Do not self-approve, merge, promote checkpoint, add credentials, deploy production, activate limited-live or enable real-money trading.