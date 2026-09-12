# HCT-IMPL-AUTH-0004 - Implementation Authorization Work Order

Status: `PENDING_INDEPENDENT_REVIEW`
Risk class: `HIGH_ASSURANCE`
Issue: `#45`
Candidate implementation slice: `HCT-IMP-0004-S1A`
Canonical base at start: `main@aa2aea7e6bf9b148c6c212f454eb0e5c0db772e5`
Checkpoint at start: `HCT-CP-0020 / S0C_IMPLEMENTATION_APPROVED_MERGED`
Proposed promoted checkpoint: `HCT-CP-0021 / IMPLEMENTATION_AUTHORIZED_S1A`

## OBJECTIVE
Govern whether exactly one bounded first Stage-1 contract-foundation slice may begin after successful completion of S0A, S0B and S0C, without granting concrete exchange connectivity, credential, trading, deployment or live authority.

## CONTEXT
`HCT-CP-0020` is fail closed for implementation and confirms the three approved Stage-0 implementation slices are complete. R11 Stage 1 begins with Exchange Abstraction + MEXC adapter, followed by capability/rule resolution, universe, quota/WS governance and realtime truth.

The next safe dependency is to define the HCT-owned exchange abstraction, capability semantics and canonical contract/reference model before any concrete MEXC transport code is allowed. This preserves `HCT-DEC-0023`, `docs/23-multi-exchange-adapter-architecture.md` and R11 provider-neutral boundaries.

## AUTHORIZATION QUESTION
May exactly this implementation slice be authorized?

`HCT-IMP-0004-S1A - Exchange Abstraction, Capability & Contract Reference Foundation`

Proposed authorization ceiling:

`NON_TRADING_STAGE_1_EXCHANGE_ABSTRACTION_CAPABILITY_CONTRACT_FOUNDATION_ONLY`

## GOVERNANCE SCOPE
This authorization increment may change only governance artifacts needed to define and review the candidate authorization package:
- `docs/115-implementation-authorization-s1a-candidate.md`;
- `work-orders/HCT-IMPL-AUTH-0004.md`;
- `work-orders/HCT-IMP-0004-S1A.md`;
- `.github/workflows/implementation-authorization-s1a-governance.yml`.

No product source, runtime contract, dependency lockfile, checkpoint, deployment file or production configuration may be changed by the authorization candidate.

## REQUIRED SOURCE TRACEABILITY
The candidate and implementation Work Order SHALL preserve these direct locators:
- `REQ02::Market and exchange requirements::B2`;
- `REQ02::Market and exchange requirements::B5`;
- `REQ02::Market and exchange requirements::B7`;
- `REQ02::Market and exchange requirements::B8`;
- `REQ02::Market and exchange requirements::B9`;
- `R11-REQ-006`;
- `R11-REQ-012`;
- `R11-REQ-013`;
- `R11-REQ-014`;
- `R11-REQ-024`;
- `HCT-DEC-0023`.

The review SHALL also inspect `docs/14-product-module-map.md`, `docs/23-multi-exchange-adapter-architecture.md`, `docs/91-r11-integrated-authority-state-dependency-architecture.md`, the frozen R12 baseline and current checkpoint.

## PROPOSED AUTHORIZED SUBJECT
Only the provider-neutral non-trading exchange abstraction/reference foundation:
- canonical exchange/instrument/contract identity/version semantics;
- immutable capability snapshots with explicit supported/unsupported/unknown state;
- immutable provider-neutral contract/reference specification;
- read-only exchange reference adapter protocol/port;
- bounded canonical reference error/degradation classes;
- deterministic credential-free/network-free test doubles;
- canonical schema/generation changes when needed by the shared contract source;
- tests/evidence/CI required to prove all negative boundaries and preserve S0A/S0B/S0C.

## EXPLICITLY OUT OF SCOPE
This authorization SHALL NOT grant:
- product implementation before approval/checkpoint promotion;
- concrete MEXC adapter code;
- MEXC REST/WebSocket/SDK/network connectivity;
- runtime HTTP/WebSocket/socket clients or live external calls;
- authentication/signing/API keys/credential lifecycle/secret material;
- private/account streams;
- public realtime market-data ingest;
- dynamic Market Universe eligibility/runtime;
- API Quota/WS/Backpressure Governor runtime;
- reconnect/session-generation/subscription runtime;
- Data Quality, Market-State Fabric, order-book reconstruction or cache runtime;
- orders/cancel-replace/fills/positions/balances/OMS/reconciliation/protection;
- Safety/Session/Portfolio/Sizing/Leverage/Risk/Reservation;
- database persistence/RLS;
- production deployment;
- limited-live;
- real-money trading;
- later Stage-1 or Stage-2+ implementation.

## AUTHORIZATION ACCEPTANCE CRITERIA
A. Context Lock matches `main@aa2aea7e6bf9b148c6c212f454eb0e5c0db772e5` and `HCT-CP-0020`.
B. Current implementation authority remains fail closed in all canonical checkpoint flags.
C. Candidate chooses exactly one bounded implementation slice.
D. R11 dependency order is preserved: abstraction/reference contracts precede concrete MEXC transport and later realtime modules.
E. Candidate is traceable to the listed frozen locators, `HCT-DEC-0023`, Modules 1/2 and `docs/23`.
F. Proposed adapter boundary is read-only and provider-neutral.
G. No concrete MEXC/network/auth/signing/secret implementation is authorized.
H. No market ingest/universe/quota/Data Quality/Market-State/cache implementation is authorized.
I. No exchange command/order/money-state/risk/execution authority is authorized.
J. Implementation Work Order defines deterministic positive/negative tests, scans, exact-head evidence and STOP CONDITION.
K. Authorization PR contains only the four governance files listed above.
L. Authorization-governance workflow runs only on pull requests for the exact candidate head/base and exposes no manual-dispatch success path.
M. Exact-head authorization-governance CI is `success`.
N. Separate independent HIGH_ASSURANCE/HEDS Delta review returns `APPROVED` for the exact head.
O. Unresolved authorization CRITICAL findings = `0` and HIGH findings = `0`.

## REVIEW FORMAT
Independent review SHALL return exactly one verdict:
- `APPROVED`
- `CORRECTION REQUIRED`
- `BLOCKED`

The review must state the exact candidate head, base, CI run/check, CRITICAL/HIGH finding counts and whether the proposed authorization ceiling remains fail-closed outside S1A.

## PROPOSED POST-APPROVAL STATE
Only after governed merge and checkpoint promotion:
- `implementation_authorized=true`
- `implementation_authorization_scope=["HCT-IMP-0004-S1A"]`
- `implementation_authorization_ceiling="NON_TRADING_STAGE_1_EXCHANGE_ABSTRACTION_CAPABILITY_CONTRACT_FOUNDATION_ONLY"`
- `production_credentials_authorized=false`
- `production_deployment_authorized=false`
- `limited_live_authorized=false`
- `live_trading_authorized=false`

## KNOWN GOVERNANCE GAP
The stale historical S0B workflow base assertion recorded by `HCT-CP-0020` is not modified by this authorization increment. Any repair must be its own bounded governance/CI-maintenance increment. The future S1A implementation workflow must directly prove S0B regression regardless of that historical workflow's result.

## STOP CONDITION
Stop with the authorization PR OPEN and UNMERGED after exact-head governance CI and author-side preflight. Do not begin product implementation, promote `HCT-CP-0021`, add exchange connectivity, add credentials, deploy, activate limited-live or enable real-money trading until a separate independent HIGH_ASSURANCE review returns `APPROVED` on the exact authorization head.
