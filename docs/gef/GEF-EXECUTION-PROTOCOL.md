# GEF Bootstrap V1.0.0 Universal Execution Protocol — HCT

Status: `GOVERNED_CANDIDATE`

## Canonical lifecycle

`ANALYZE → SOURCE CHECK → NEXT NECESSARY INCREMENT → WORK ORDER → CONTEXT LOCK → PREFLIGHT → EXECUTOR → TESTS/EVIDENCE → PR → EXACT-HEAD AUDIT → CHECKPOINT DELTA → MERGE → NEXT`

No step grants authority beyond the current HCT checkpoint and Work Order.

## Source Check

Before mutation establish:
- repository identity;
- canonical branch and exact base/head;
- current checkpoint/production state;
- applicable decisions, scope, frozen requirements, DoD, architecture and security policy;
- current Work Order;
- active PRs that must be preserved;
- allowed patch surface;
- capability gaps and source drift.

Mismatch produces `SOURCE_CONFLICT`.

## Work Order

Use one stable ID through branch, PR, evidence, corrections and checkpoint delta. Required semantics are governed by `docs/12-work-order-prompt-contract.md`.

## Context Lock

Compile the smallest safe executor context. Use, when helpful:
- Implementation Seed Tree;
- File Intent Capsule;
- Brownfield Patch Intent Capsule;
- Executor Navigation Map;
- Decision Closure Capsule;
- Execution Waves;
- Validation Reuse Plan;
- Critical Path;
- Marathon Execution Pack.

The executor must not reconstruct frozen architecture from chat memory when the repository already contains authoritative sources.

## Preflight

Verify:
- `SOURCE_MATCH`;
- exact expected Git identity;
- no unauthorized dirty/candidate drift;
- required tools/commands known;
- test/evidence plan appropriate to risk;
- rollback/recovery understood;
- no product/live authorization widening.

## Executor

Mutate only the Work Order allowlist. Prefer bounded, causal changes and one final publication when practical. Stop rather than broaden scope silently.

## Tests/Evidence

Validation expands by risk:
1. structural/static;
2. focused;
3. impacted dependencies;
4. boundary/integration;
5. risk-expansion;
6. full candidate when required;
7. hosted exact-head checks.

Evidence binds Work Order, candidate SHA, commands/checks, results, failures/corrections, security observations and remaining risks. External run IDs stay in checks/comments/artifacts where possible.

## PR and exact-head audit

The PR must identify base/head, Work Order, scope, evidence and STOP condition.

Final approval is prohibited until mandatory exact-head checks complete and the required independent review returns a verdict for that same head. Any head change requires re-audit.

## Checkpoint Delta / Merge / Next

The executor may propose a Checkpoint Delta but must not self-promote canonical truth where HCT requires independent approval.

After approved merge:
- verify default-branch state;
- promote only the reviewed checkpoint/current-state delta;
- compute the next legal increment from canonical truth;
- generate the next PDF handoff in the same user-facing response when deterministic and authorized.

## STOP states

- `COMPLETE_CANDIDATE`
- `SOURCE_CONFLICT`
- `SCOPE_EXPANSION_REQUIRED`
- `BLOCKED_EVIDENCE`
- `NEEDS_ARCHITECTURE`
- `GEF_ADOPTION_EXACT_HEAD_EVIDENCE_REQUIRED`
- `GEF_ADOPTION_BLOCKED_BY_CAPABILITY_GAP`

## HCT execution firewall

Product code may be changed only when the current canonical checkpoint explicitly authorizes the exact Work Order and ceiling. GEF adoption itself does not grant product authority.
