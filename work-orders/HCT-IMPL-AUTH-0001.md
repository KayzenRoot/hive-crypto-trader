# Work Order — HCT-IMPL-AUTH-0001

Status: `OPEN_FOR_INDEPENDENT_REVIEW`
Risk: `HIGH_ASSURANCE`
Baseline: `main@f201d866f96eb6bb86ecc2212535b6129a9511d4`
Checkpoint: `HCT-CP-0014 / PLANNING_FREEZE_APPROVED`

## OBJECTIVE
Govern whether the first bounded product-code slice may begin, without weakening the Planning Freeze or granting any production/live authority.

## CONTEXT
R12 is frozen and approved. The R11 implementation dependency DAG requires Stage 0 canonical contract/governance/security foundations before exchange truth, deterministic intelligence, capital safety, execution, validation, automation, UI/commercial surfaces and operational promotion.

## SCOPE
- select one bounded Stage-0 implementation slice;
- define its exact authority ceiling;
- define explicit out-of-scope behaviors;
- define implementation acceptance criteria, required tests/evidence and STOP CONDITION;
- define checkpoint semantics for bounded implementation authorization;
- obtain independent HIGH_ASSURANCE review before authorization becomes canonical.

## OUT OF SCOPE
- product code;
- exchange connectivity;
- secrets/credentials;
- production deployment;
- limited-live;
- real-money trading;
- later Stage-0 slices;
- Stage 1+ capabilities.

## SOURCES TO READ
Priority follows `docs/00-source-hierarchy.md`:
- `docs/11-checkpoint.md` and `checkpoints/workstreams/planning/latest.json`;
- `docs/10-decisions-ledger.md`;
- `docs/03-scope.md`;
- `docs/09-definition-of-done.md`;
- `docs/04-architecture.md`;
- R12 frozen requirements authority (`docs/99`, `docs/100`, exact nine source blobs, `docs/101`);
- `docs/91-r11-integrated-authority-state-dependency-architecture.md`;
- `docs/92-r11-v1-module-classification-and-integration-hardening.md`;
- `docs/93-r11-integration-requirements-addendum.md`;
- `docs/102-r12-freeze-acceptance-matrix.md`;
- `docs/105-r12-freeze-approval-and-checkpoint-promotion.md`;
- `docs/104-chat-delivery-and-prompt-artifact-policy.md`.

## REQUIREMENTS
- authorization SHALL be bounded to one stable implementation ID;
- no authorization language may imply production/live authority;
- first slice SHALL respect R11 Stage-0 dependency order;
- no live/exchange mutation path may exist in the first slice;
- all higher operational flags remain false;
- executor/reviewer prompts remain PDF-only;
- independent review must reconstruct verdict from repository evidence.

## ARCHITECTURE RULES
- frontend is untrusted;
- backend owns authority/security/business rules;
- environment identity is part of every stateful high-assurance identity;
- shared contracts cannot create shadow authority;
- implementation choices cannot weaken frozen semantics;
- unknown/ambiguous authorization state fails closed.

## CONSTRAINTS
- no product code during this Work Order;
- no credentials;
- no external exchange calls;
- no force push/history rewrite;
- no checkpoint promotion before independent approval and governed merge.

## ACCEPTANCE CRITERIA
- candidate authorization artifact exists and is internally consistent;
- proposed first slice is bounded and Stage-0 aligned;
- explicit prohibited scope covers all exchange/money/live paths;
- implementation tests/evidence classes are specified;
- checkpoint delta is bounded and retains all higher flags false;
- zero unresolved CRITICAL/HIGH authorization defect;
- independent verdict is `APPROVED` for the exact candidate head;
- governance CI for the exact candidate head is successful.

## TESTS / EVIDENCE
- exact-head/base Context Lock;
- diff-boundary check ensuring governance/docs only;
- fail-closed flag check;
- Stage-0 source-reference check;
- scope-negative assertions for exchange/credentials/deployment/live;
- independent semantic review.

## DELIVERABLES
- `docs/106-implementation-authorization-candidate.md`;
- `work-orders/HCT-IMPL-AUTH-0001.md`;
- `work-orders/HCT-IMP-0001-S0A.md` in `PENDING_AUTHORIZATION` state;
- authorization governance CI;
- PR with evidence;
- proposed `HCT-CP-0015` delta after approval.

## REVIEW FORMAT
Exactly one verdict:
- `APPROVED`
- `CORRECTION REQUIRED`
- `BLOCKED`

Reviewer must identify exact reviewed head and list CRITICAL/HIGH findings.

## STOP CONDITION
Keep the authorization PR open/unmerged after exact-head evidence. Do not begin product implementation or promote `HCT-CP-0015` until independent HIGH_ASSURANCE review returns `APPROVED` and the governed merge/checkpoint sequence completes.