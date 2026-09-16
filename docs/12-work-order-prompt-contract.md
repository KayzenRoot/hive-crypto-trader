# Work Order and Prompt Delivery Contract

Every governed increment uses one stable ID across Work Order, branch, PR, evidence, corrections and checkpoint delta.

GEF Bootstrap V1.0.0 Universal is the default engineering workflow overlay. It remains subordinate to the HCT source hierarchy and current checkpoint authority.

## Mandatory Work Order sections

`ID / TITLE`
`OBJECTIVE`
`CONTEXT`
`FILES/SOURCES TO READ`
`SCOPE`
`OUT OF SCOPE`
`ALLOWED FILES / AREAS`
`PRESERVATION CONSTRAINTS`
`REQUIREMENTS`
`ARCHITECTURE / SECURITY RULES`
`CONTEXT LOCK`
`ACCEPTANCE CRITERIA`
`TESTS`
`EVIDENCE`
`ROLLBACK / RECOVERY`
`DELIVERABLES`
`REVIEW FORMAT`
`STOP CONDITION`

Equivalent headings from an already-approved historical Work Order remain valid; do not rewrite old Work Orders merely for template conformity.

## Governed sequence

For implementation-oriented work:

`Source Check -> Work Order -> Context Lock -> Preflight -> Executor -> Tests/Evidence -> PR -> Exact-Head Audit -> Checkpoint Delta -> Merge -> Next`

A Context Lock should compile the smallest safe executor context and may include the GEF Implementation Seed Tree, File Intent Capsule, Brownfield Patch Intent Capsule, Executor Navigation Map, Decision Closure Capsule, Execution Waves, Validation Reuse Plan, Critical Path and Marathon Execution Pack.

Any blueprint/Work Order deviation must be explicit, bounded and auditable.

## Repository artifact versus user-facing prompt

The canonical Work Order may be stored as Markdown in `work-orders/`. Evidence and machine-readable manifests may also live in the repository.

A **complete executable prompt or independent-review prompt delivered to the user is PDF-only** under `docs/104-chat-delivery-and-prompt-artifact-policy.md`.

Therefore:
- do not require a duplicate full `.md` prompt in chat;
- do not publish the complete prompt inline merely because the Work Order is Markdown;
- a repository `.md` Work Order is source material, not a waiver of the PDF-only delivery rule;
- optional ZIP/JSON support artifacts may accompany the PDF when useful, but they never replace it.

If this document and `docs/104` differ on user-facing prompt delivery, `docs/104` controls.

## Review return contract

Executor evidence must include, as applicable:
- exact base/head SHA;
- changed files;
- source/decision bindings;
- tests, lint, typecheck, build;
- security/architecture/migration/benchmark evidence;
- corrected failures;
- remaining risks;
- gate/review receipts;
- proposed Checkpoint Delta.

Auditor verdict is exactly one of:
- `APPROVED`
- `CORRECTION REQUIRED`
- `BLOCKED`

Approval requires the exact reviewed/tested head, all mandatory gates, no unresolved CRITICAL/HIGH for HIGH_ASSURANCE work, and no scope/evidence/preservation/stale-head mismatch.

No next implementation increment is generated while the current increment still requires correction, validation, approval, merge or required post-merge checks. Deterministic next handoffs must still be prepared automatically as PDF artifacts when `docs/104` requires them.
