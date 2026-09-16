# GEF Bootstrap V1.0.0 Universal Exact-Head Delta Review Protocol — HCT

Status: `GOVERNED_CANDIDATE`
Review mode: `GEF_EXACT_HEAD_DELTA`

## Pipeline

`LOCK BASE/HEAD → SOURCE CHECK → SCOPE/PRESERVATION AUDIT → INVALIDATED PROOFS → SEMANTIC DELTA REVIEW → GATE RECEIPTS → EXACT-HEAD VERDICT`

## First candidate

Review the complete authorized delta, source hierarchy, architecture/security boundary, evidence model, preservation constraints and mandatory gate set.

## Correction candidates

Subsequent review is delta-first:
1. bind the exact base/head and prior reviewed head;
2. identify the correction delta;
3. determine which prior proofs remain byte/validity compatible;
4. invalidate affected proofs;
5. review changed and invalidated semantic areas;
6. combine only with current exact-head mandatory receipts;
7. issue a fresh verdict.

Accepted findings are not reopened without a material validity change, but authorization itself is never carried forward.

## Proof reuse

A proof may be informative `CARRY_FORWARD` only when all material validity inputs still match, including source/symbol hashes where relevant, contracts/schemas, test code, toolchain/lockfiles, workflow/config/policy, platform and canonical checkpoint/authorization state.

Otherwise mark `INVALIDATED`.

While Shadow Assurance is ON, proof reuse never skips a mandatory HCT hosted gate.

## Preservation review

For BROWNFIELD work, explicitly verify:
- user work preserved;
- no unauthorized rename/reorganization;
- existing tests/CI/security not weakened;
- no fabricated history/evidence;
- no hidden scope expansion;
- active unrelated PRs untouched.

## Verdicts

Exactly one:
- `APPROVED`
- `CORRECTION REQUIRED`
- `BLOCKED`

For HCT approval:
- candidate SHA explicit;
- mandatory exact-head checks complete and successful;
- unresolved CRITICAL=0;
- unresolved HIGH=0;
- no scope/evidence/preservation/stale-head mismatch;
- required review independence satisfied.

Any head change invalidates the approval for the new head.

## Independent review

Independence is governed by HCT policy. The review stream must reconstruct its verdict from repository evidence and not merely reuse the authoring stream's conclusion. Same GitHub account alone does not determine independence.

## Receipts

External gate/review IDs belong in PR comments/checks/artifacts or separately governed post-merge promotion records. Avoid source commits whose only purpose is to store a CI run ID and thereby invalidate the head just tested.

## Security/authority invalidation

A changed checkpoint, authorization scope/ceiling, secret policy, deployment/live gate, or material security policy invalidates affected security/authority proofs automatically.
