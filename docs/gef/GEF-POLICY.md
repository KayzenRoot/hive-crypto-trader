# GEF Bootstrap V1.0.0 Universal Local Policy — Hive Crypto Trader

Status: `GOVERNED_CANDIDATE`
GEF version: `GEF-BOOTSTRAP-V1.0.0-UNIVERSAL`

## Authority

GEF is a governed engineering overlay, not a product authority.

HCT canonical precedence remains defined by `docs/00-source-hierarchy.md`. Operationally, GEF uses:

`checkpoint/current state > approved Decisions/ADRs > Scope + frozen Requirements > DoD/acceptance > Architecture > Security/policy > current Work Order/Context Lock > supporting docs > chat prose`

On conflict, record `SOURCE_CONFLICT`, preserve the higher-precedence source and stop.

## Non-negotiable HCT overrides

1. Complete user-facing executor/reviewer prompts remain PDF-only under `docs/104-chat-delivery-and-prompt-artifact-policy.md`.
2. HIGH_ASSURANCE work keeps exact-head hosted gates and independent review.
3. GEF never widens `implementation_authorization_scope` or authorization ceiling.
4. `UNKNOWN -> ALLOW` is forbidden.
5. Production credentials, deployment, limited-live and live trading remain independently governed.
6. Active product PRs are never silently modified, rebased, retargeted, closed or merged by a GEF adoption increment.
7. Old-head proof is never exact-head proof for a new head.
8. Existing tests/CI/security controls are never weakened merely to obtain a green result.
9. User work and repository history are preserved by default.
10. No fabricated history, tests, approvals, releases or evidence.

## Repository modes

- `GREENFIELD`
- `BROWNFIELD`
- `HYBRID`

HYBRID is treated conservatively as BROWNFIELD for preservation. HCT is `BROWNFIELD`.

## Task/context control

Legacy GEF `T0..T3` task class and `C0..C4` context radius remain valid optimization vocabulary. Use the smallest safe context; expand only for a material dependency, conflict, scope expansion or architecture need.

Context Lock may compile Implementation Seed Tree, File Intent Capsule, Brownfield Patch Intent Capsule, Executor Navigation Map, Decision Closure Capsule, Execution Waves, Validation Reuse Plan, Critical Path and Marathon Execution Pack.

## Budgets

Execution/correction packs should declare bounded search, files-opened, patch and retry budgets when relevant. Budgets are guardrails, never permission to truncate correctness. Material overrun becomes a STOP state.

## Assurance ladder

- structural/static;
- focused tests;
- impacted dependencies;
- boundary/integration;
- risk-expansion;
- full candidate validation where required;
- hosted exact-head gates;
- independent semantic review where required.

Legacy labels `A0..A4` may be retained as shorthand. HCT's stricter current Work Order and checkpoint always win.

## Shadow Assurance

`ON`

Proof carry-forward and impacted-test reduction are advisory until separately promoted through evidence and a governed decision. Mandatory HCT hosted gates are not skipped because a legacy proof map says `CARRY_FORWARD`.

## Git/GitHub

Prefer isolated branches and PRs. No force-push, history rewrite or destructive reset. A base/head mismatch is a source conflict. Exact-head receipts belong in checks/comments/artifacts rather than evidence-only commits that mutate the reviewed head.

Missing/enforceable branch protection is a capability fact, not a reason to invent protection or bypass PR governance.

## Security

Applicable work must consider secrets, traversal/symlink attacks, malicious configuration, dependencies, permissions, shell/process execution, generated artifacts, partial mutation recovery, logging/redaction and token permissions.

Unresolved HIGH/CRITICAL security findings block approval.

## Forbidden shortcuts

- `UNKNOWN -> ALLOW`;
- invented gate/proof/test result;
- old-head receipt presented as exact-head;
- silent scope expansion;
- broad repository search by default when a bounded context suffices;
- repeated retry without causal change;
- evidence-only commit after gates merely to record run IDs;
- merge before required checks/review;
- deletion/reorganization of existing governance for template aesthetics;
- optional adapter treated as mandatory without project authority;
- optimization target presented as measured result;
- carry-forward without validity-input checks.
