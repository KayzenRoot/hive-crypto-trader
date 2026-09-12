# HCT-IMPL-AUTH-0004 - Implementation Authorization Work Order

Status: `COMPLETED_APPROVED`
Risk class: `HIGH_ASSURANCE`
Issue: `#45`
Candidate implementation slice: `HCT-IMP-0004-S1A`
Canonical base at start: `main@aa2aea7e6bf9b148c6c212f454eb0e5c0db772e5`
Checkpoint at start: `HCT-CP-0020 / S0C_IMPLEMENTATION_APPROVED_MERGED`
Promoted checkpoint: `HCT-CP-0021 / IMPLEMENTATION_AUTHORIZED_S1A`

## RESULT
`APPROVED`.

Independent review exact head:
`8e6ebe7a3ecf7b108a2bd57d5249b3eda310f388`

Exact-head governance run:
`34705660182 / implementation-authorization-s1a-governance / success`

Governed merge:
`PR #46 -> 7a458504de8721fdaffe6c3262781d1d5a675291`

Independent evidence:
- PR #46 comment `5647342250`;
- Issue #45 comment `5647342415`.

Approved implementation scope:
`HCT-IMP-0004-S1A`

Authorization ceiling:
`NON_TRADING_STAGE_1_EXCHANGE_ABSTRACTION_CAPABILITY_CONTRACT_FOUNDATION_ONLY`

CRITICAL findings: `0`
HIGH findings: `0`

## OBJECTIVE
Govern whether exactly one bounded first Stage-1 contract-foundation slice may begin after successful completion of S0A, S0B and S0C, without granting concrete exchange connectivity, credential, trading, deployment or live authority.

## CONTEXT
`HCT-CP-0020` was fail closed for implementation and confirmed the three approved Stage-0 implementation slices were complete. R11 Stage 1 begins with Exchange Abstraction + MEXC adapter, followed by capability/rule resolution, universe, quota/WS governance and realtime truth.

The approved next dependency is the HCT-owned exchange abstraction, capability semantics and canonical contract/reference model before any concrete MEXC transport code. This preserves `HCT-DEC-0023`, `docs/23-multi-exchange-adapter-architecture.md` and R11 provider-neutral boundaries.

## AUTHORIZATION QUESTION
May exactly this implementation slice be authorized?

`HCT-IMP-0004-S1A - Exchange Abstraction, Capability & Contract Reference Foundation`

Approved authorization ceiling:

`NON_TRADING_STAGE_1_EXCHANGE_ABSTRACTION_CAPABILITY_CONTRACT_FOUNDATION_ONLY`

## GOVERNANCE SCOPE
The authorization candidate changed only:
- `docs/115-implementation-authorization-s1a-candidate.md`;
- `work-orders/HCT-IMPL-AUTH-0004.md`;
- `work-orders/HCT-IMP-0004-S1A.md`;
- `.github/workflows/implementation-authorization-s1a-governance.yml`.

No product source, runtime contract, dependency lockfile, checkpoint, deployment file or production configuration was changed by the authorization candidate.

## REQUIRED SOURCE TRACEABILITY
The candidate and implementation Work Order preserve these direct locators:
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

The independent review also inspected `docs/14-product-module-map.md`, `docs/23-multi-exchange-adapter-architecture.md`, `docs/91-r11-integrated-authority-state-dependency-architecture.md`, the frozen R12 baseline and current checkpoint.

## APPROVED AUTHORIZED SUBJECT
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
This authorization does NOT grant:
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

## AUTHORIZATION ACCEPTANCE CRITERIA RESULT
A. Context Lock matched `main@aa2aea7e6bf9b148c6c212f454eb0e5c0db772e5` and `HCT-CP-0020`: `PASS`.
B. Implementation authority was fail closed before promotion: `PASS`.
C. Candidate chose exactly one bounded implementation slice: `PASS`.
D. R11 dependency order preserved: `PASS`.
E. Frozen locators / HCT-DEC-0023 / Modules 1-2 / docs/23 traceability: `PASS`.
F. Adapter boundary read-only and provider-neutral: `PASS`.
G. No concrete MEXC/network/auth/signing/secret implementation authorized: `PASS`.
H. No market ingest/universe/quota/Data Quality/Market-State/cache implementation authorized: `PASS`.
I. No exchange command/order/money-state/risk/execution authority authorized: `PASS`.
J. Implementation Work Order defines deterministic tests, scans, evidence and STOP CONDITION: `PASS`.
K. Authorization candidate delta exactly four governance files: `PASS`.
L. Authorization workflow pull-request-only, exact head/base, no manual-dispatch success path: `PASS`.
M. Exact-head governance CI success: `PASS`.
N. Independent HIGH_ASSURANCE/HEDS Delta verdict `APPROVED`: `PASS`.
O. Unresolved CRITICAL/HIGH `0/0`: `PASS`.

## POST-APPROVAL STATE
After promotion to `HCT-CP-0021`:
- `implementation_authorized=true`
- `implementation_authorization_scope=["HCT-IMP-0004-S1A"]`
- `implementation_authorization_ceiling="NON_TRADING_STAGE_1_EXCHANGE_ABSTRACTION_CAPABILITY_CONTRACT_FOUNDATION_ONLY"`
- `production_credentials_authorized=false`
- `production_deployment_authorized=false`
- `limited_live_authorized=false`
- `live_trading_authorized=false`

## KNOWN GOVERNANCE GAP
The stale historical S0B workflow base assertion recorded by `HCT-CP-0020` is not modified by this authorization increment. Any repair must be its own bounded governance/CI-maintenance increment. The S1A implementation workflow must directly prove S0B regression regardless of that historical workflow's result.

## COMPLETION EVIDENCE
- authorization candidate: `docs/115-implementation-authorization-s1a-candidate.md`;
- approval/promotion record: `docs/116-s1a-implementation-authorization-approval-and-checkpoint-promotion.md`;
- implementation Work Order: `work-orders/HCT-IMP-0004-S1A.md`;
- PR: `#46`;
- reviewed head: `8e6ebe7a3ecf7b108a2bd57d5249b3eda310f388`;
- governance run: `34705660182`;
- merge commit: `7a458504de8721fdaffe6c3262781d1d5a675291`;
- promoted checkpoint: `HCT-CP-0021`.

## NEXT NECESSARY ACTION
Execute `HCT-IMP-0004-S1A` from a fresh repository synchronization and exact Context Lock against `HCT-CP-0021`, satisfy its acceptance criteria/tests/evidence, and stop with the implementation PR open/unmerged for independent HIGH_ASSURANCE/HEDS Delta review.

## STOP CONDITION
The authorization gate is complete. No authority exists beyond the exact S1A ceiling above. Concrete MEXC connectivity, credentials, deployment, limited-live, real-money trading and later Stage-1/Stage-2 work remain blocked.
