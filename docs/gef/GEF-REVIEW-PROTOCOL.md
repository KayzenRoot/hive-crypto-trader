# UADS GEF V1 HEDS Delta Review Protocol — HCT

Status: `GOVERNED_CANDIDATE`
Review mode: `HEDS_DELTA`

## Pipeline

`ANALYZE DELTA -> SOURCE CHECK -> INVALIDATED PROOFS -> SEMANTIC REVIEW -> GATE RECEIPTS -> EXACT-HEAD VERDICT`

## First candidate of an increment

The first review may inspect the full authorized delta, architecture boundary, evidence model and mandatory gate set.

## Subsequent correction reviews

Reviews become delta-first:
1. lock exact base/head;
2. compare against the last reviewed head;
3. identify byte-identical files and changed validity inputs;
4. carry forward only proofs whose complete dependency fingerprints remain compatible;
5. invalidate affected proofs;
6. inspect the semantic delta and newly invalidated areas;
7. combine with current exact-head gate receipts;
8. issue the governed verdict.

Accepted findings are not reopened without a new delta/validity change that invalidates their proof.

## Proof validity

A proof may be marked `CARRY_FORWARD` only when all material inputs match, including where relevant source file hashes/symbol hashes, contract/schema hashes, test code, toolchain/lockfiles, workflow/config/policy, OS/platform and canonical checkpoint/authorization state.

Otherwise mark `INVALIDATED`.

During Shadow Assurance, carry-forward is informational and does not skip HCT-required hosted gates.

## Review concurrency

HEDS semantic delta review may begin while CI runs. Final APPROVED status still waits for every mandatory exact-head A3 gate.

## Verdicts

Use the project-governed verdicts:
- `APPROVED`
- `CORRECTION REQUIRED`
- `BLOCKED`

For HCT HIGH_ASSURANCE, APPROVED requires unresolved CRITICAL=0 and HIGH=0 plus all required exact-head receipts.

## Receipt rule

Run IDs/check results belong in PR comments/checks/artifacts or other external receipts. Avoid evidence-only commits that change the head after the gate was produced.

## Security

HEDS Delta never carries forward authorization itself. A changed checkpoint, authorization scope, ceiling, secret policy or live/deployment gate automatically invalidates affected security/authority proofs.
