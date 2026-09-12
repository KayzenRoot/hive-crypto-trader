# HCT-IMPL-AUTH-0002 - Implementation Authorization Work Order

Status: `INDEPENDENT_REVIEW_REQUIRED`
Risk class: `HIGH_ASSURANCE`
Issue: `#35`
Candidate implementation slice: `HCT-IMP-0002-S0B`
Canonical base: `main@9353cd691d73a4b769d1ccd13823142b2ebf8168`
Canonical checkpoint: `HCT-CP-0016 / S0A_IMPLEMENTATION_APPROVED_MERGED`

## OBJECTIVE
Determine whether exactly one bounded Stage-0 security-foundation implementation slice may be authorized without granting exchange, secret-material, deployment or live authority.

## CONTEXT
S0A was independently approved and merged through PR #34, then promoted to HCT-CP-0016. The canonical checkpoint explicitly closes implementation authorization again and requires a separate HIGH_ASSURANCE gate before the next product-code mutation.

R11 Stage 0 still requires SecurityContext/tenant/account binding and SecretStore abstraction before later exchange/realtime/risk/execution stages. R08 makes these boundaries security-critical and fail-closed.

## SCOPE
This authorization increment may change governance artifacts only. It SHALL define and review:
- candidate authorization semantics for `HCT-IMP-0002-S0B`;
- exact S0B implementation scope and exclusions;
- proof obligations, acceptance criteria, tests and evidence;
- a phase-specific CI governance gate;
- the future authorization ceiling.

## OUT OF SCOPE
This authorization increment SHALL NOT:
- modify application/product code;
- create SecurityContext implementation code;
- create SecretStore implementation code;
- add real credentials/secrets;
- connect to MEXC or any exchange;
- create deployment infrastructure;
- authorize production credentials/deployment, limited-live or real-money trading;
- alter the R12 frozen requirements baseline.

## FILES / SOURCES TO READ
At minimum:
- `checkpoints/workstreams/planning/latest.json`
- `checkpoints/history/HCT-CP-0016.json`
- `docs/11-checkpoint.md`
- `docs/00-source-hierarchy.md`
- `docs/09-definition-of-done.md`
- `docs/10-decisions-ledger.md`
- `docs/73-r08-multitenant-security-requirements-addendum.md`
- `docs/70-r08-critical-tenant-security-architecture.md`
- `docs/91-r11-integrated-authority-state-dependency-architecture.md`
- `docs/100-r12-requirements-traceability-and-no-loss-proof.md`
- `docs/108-s0a-implementation-approval-and-checkpoint-promotion.md`
- `evidence/HCT-IMP-0001-S0A.md`
- `docs/109-implementation-authorization-s0b-candidate.md`
- `work-orders/HCT-IMP-0002-S0B.md`
- Issue #35 and candidate PR discussion.

## REQUIREMENTS
### AUTH-001 - Exact bounded scope
Any approval SHALL authorize only `HCT-IMP-0002-S0B`.

### AUTH-002 - Ceiling
The only proposed ceiling is:
`NON_TRADING_STAGE_0_SECURITY_FOUNDATION_ONLY`.

### AUTH-003 - Current fail-closed state
Until checkpoint promotion:
- `implementation_authorized=false`
- `production_credentials_authorized=false`
- `production_deployment_authorized=false`
- `limited_live_authorized=false`
- `live_trading_authorized=false`.

### AUTH-004 - No raw-secret semantics
The S0B Work Order SHALL NOT authorize real secret values, provider integrations, encryption/decryption, credential lifecycle or exchange authentication.

### AUTH-005 - SecurityContext authority
The future implementation SHALL model server-derived immutable authority and reject client-supplied tenant/account identifiers as proof of authorization.

### AUTH-006 - Binding isolation
The future implementation SHALL include exact tenant/account/environment binding and deterministic cross-tenant/account negative tests.

### AUTH-007 - Independent review
Approval requires a separate HIGH_ASSURANCE review execution against the exact candidate head and exact-head governance CI.

## ARCHITECTURE RULES
- SecurityContext is backend authority, not frontend state.
- Tenant/account identifiers are not authorization by themselves.
- CredentialRef/SecretRef is opaque reference metadata, never secret material.
- SecretStore in S0B is a provider-neutral capability boundary only.
- S0B introduces no external network dependency.
- S0B introduces no persistence requirement.
- S0B cannot create trading authority.
- Frozen requirements remain unchanged.

## CONSTRAINTS
- Governance-only PR.
- No product code.
- No force push/history rewrite.
- No self-promotion.
- No CRITICAL/HIGH finding may be carried forward.
- Same GitHub identity is acceptable only when independent execution/context reconstructs the verdict from evidence.

## ACCEPTANCE CRITERIA
A. Candidate base is exactly the canonical CP0016 main state.
B. Governance diff contains only the declared S0B authorization package/workflow.
C. Candidate clearly states `INDEPENDENT_REVIEW_REQUIRED`.
D. Current implementation authorization remains false.
E. Proposed authorization scope is exactly `HCT-IMP-0002-S0B`.
F. Proposed ceiling is exactly `NON_TRADING_STAGE_0_SECURITY_FOUNDATION_ONLY`.
G. Real secret values/provider implementations are explicitly prohibited.
H. Exchange/trading/money-state capability is explicitly prohibited.
I. Production credentials/deployment/limited-live/live remain false.
J. S0B implementation Work Order contains objective, context, scope, out of scope, sources, requirements, architecture rules, constraints, acceptance criteria, tests, deliverables, review format and STOP CONDITION.
K. Cross-tenant/account/environment and client-authority negative tests are mandatory in the future Work Order.
L. Exact-head governance CI is successful.
M. Independent review finds zero unresolved CRITICAL/HIGH defects.

## TESTS
Authorization governance SHALL verify automatically:
- exact raw PR-head checkout;
- required files exist and are non-empty;
- HCT-CP-0016 provenance marker exists;
- current `implementation_authorized=false` marker remains authoritative;
- candidate status is `INDEPENDENT_REVIEW_REQUIRED`;
- candidate mentions only `HCT-IMP-0002-S0B` as the proposed scope;
- ceiling marker is exact;
- all higher operational gates remain false;
- required prohibited-capability markers exist;
- diff is governance-only.

Independent review SHALL inspect semantics, not merely string presence.

## DELIVERABLES
- `docs/109-implementation-authorization-s0b-candidate.md`
- `work-orders/HCT-IMPL-AUTH-0002.md`
- `work-orders/HCT-IMP-0002-S0B.md`
- `.github/workflows/implementation-authorization-s0b-governance.yml`
- Issue #35
- one authorization PR to `main`
- exact-head CI evidence
- independent review verdict.

## REVIEW FORMAT
Exactly one:
- `APPROVED`
- `CORRECTION REQUIRED`
- `BLOCKED`

Review evidence SHALL include exact head, CP0016 integrity, Stage-0 ordering, scope/ceiling, negative scope, Work Order completeness, CI result, CRITICAL count and HIGH count.

## STOP CONDITION
Stop with the authorization PR OPEN and UNMERGED after exact-head CI and author-side preflight. Do not implement S0B, promote a checkpoint, add credentials, deploy, activate limited-live or enable real-money trading before independent `APPROVED` and governed merge/promotion.