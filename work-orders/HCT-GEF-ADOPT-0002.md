# HCT-GEF-ADOPT-0002 — GEF Bootstrap V1.0.0 Universal Brownfield Upgrade

Risk class: `PROCESS_GOVERNANCE / HIGH_ASSURANCE_COMPATIBILITY`
Issue: `#79`
Canonical base: `main@9e6014472df7723b21f9a1d7ab2aa207ac714ccc`
Target branch: `governance/HCT-GEF-ADOPT-0002-universal-v1`

## OBJECTIVE

Upgrade the existing legacy `UADS-GEF-V1` governance overlay to the user-supplied `GEF Bootstrap V1.0.0 — Universal Adoption Prompt` without altering HCT product behavior or weakening any existing HIGH_ASSURANCE control.

## CONTEXT

HCT is BROWNFIELD and already governed. The current checkpoint is `HCT-CP-0035 / IMPLEMENTATION_AUTHORIZED_S2B`; PR #78 is active S2B product implementation work awaiting exact-head independent review. The GEF upgrade must run as a separate governance-only increment.

## FILES/SOURCES TO READ

- `docs/00-source-hierarchy.md`
- `docs/11-checkpoint.md`
- `checkpoints/history/HCT-CP-0035.json`
- `docs/10-decisions-ledger.md`
- `docs/03-scope.md`
- `docs/09-definition-of-done.md`
- `docs/04-architecture.md`
- `docs/05-security.md`
- `docs/06-test-benchmark-plan.md`
- `docs/12-work-order-prompt-contract.md`
- `docs/104-chat-delivery-and-prompt-artifact-policy.md`
- `docs/gef/*`
- `.github/workflows/gef-adoption-governance.yml`
- user source artifact `GEF-V1-UNIVERSAL-ADOPTION-PROMPT.pdf` SHA-256 `af1de7df4db966f1109992741191b58d3daccaa7d42a4bff218aaa63e80dc2f3`

## SCOPE

- record current brownfield Repository Discovery Receipt;
- record Collision Map and preservation plan;
- incorporate universal GEF V1.0.0 adoption contract;
- refresh GEF current/profile/adoption/policy/execution/review/cache state;
- reconcile `docs/12` and `prompts/README.md` with governed PDF-only complete prompt delivery;
- update the GEF adoption workflow for the current exact base and bounded upgrade surface;
- create an adoption Evidence Bundle;
- open a governance-only PR and obtain exact-head CI;
- require fresh independent review before merge.

## OUT OF SCOPE

- product/runtime code;
- PR #78 candidate files or its review result;
- checkpoint promotion in the adoption candidate;
- frozen product requirements;
- product ADR semantics;
- dependency upgrades;
- deployment;
- exchange credentials;
- production credentials;
- limited-live/live trading;
- native DWP runtime;
- cleanup unrelated to this migration.

## ALLOWED PATCH SURFACE

- `docs/gef/**`
- `docs/12-work-order-prompt-contract.md`
- `prompts/README.md`
- `work-orders/HCT-GEF-ADOPT-0002.md`
- `evidence/HCT-GEF-ADOPT-0002.md`
- `.github/workflows/gef-adoption-governance.yml`

No other path is authorized.

## PRESERVATION CONSTRAINTS

- no force push or history rewrite;
- no direct mutation of `main`;
- no changes to `apps/`, `packages/`, `scripts/`, `adr/`, `checkpoints/` or product implementation evidence;
- no change to CP0035 authorization scope/ceiling;
- no weakening of exact-head CI or independent review;
- no `UNKNOWN -> ALLOW`;
- no fabricated evidence.

## REQUIREMENTS

1. The migration classifies HCT as BROWNFIELD.
2. Existing HCT paths are reused rather than duplicated into `.engineering/`.
3. GEF is subordinate to the HCT source hierarchy.
4. Future governed prompts/reviews use GEF Bootstrap V1.0.0 universal lifecycle semantics.
5. Complete user-facing executable/reviewer prompts remain PDF-only.
6. Shadow Assurance remains on until separately promoted.
7. Active S2B work remains untouched.
8. Branch-protection absence is recorded as a capability gap, not silently fixed or claimed.

## ARCHITECTURE / SECURITY RULES

This increment is governance-only. It must not change runtime architecture or security behavior. Existing HCT security, authorization and live-trading firewalls remain authoritative.

## CONTEXT LOCK

Expected source identity before mutation:
- repository `KayzenRoot/hive-crypto-trader`
- default branch `main`
- exact base `9e6014472df7723b21f9a1d7ab2aa207ac714ccc`
- checkpoint `HCT-CP-0035`
- active authorized increment `HCT-IMP-0011-S2B`
- active product PR `#78`
- GEF source SHA-256 `af1de7df4db966f1109992741191b58d3daccaa7d42a4bff218aaa63e80dc2f3`

Any drift requires `SOURCE_CONFLICT` and re-baselining.

## ACCEPTANCE CRITERIA

- discovery receipt and collision map are valid JSON;
- universal contract exists and preserves all HCT overrides;
- stale S0C-era `GEF-CURRENT` and `GEF-PROJECT-PROFILE` active-state fields are refreshed;
- GEF workflow validates exact head/base and rejects changes outside the allowed patch surface;
- docs/12 and prompts README no longer contradict docs/104 on complete prompt delivery;
- no runtime/checkpoint/frozen requirement file changes;
- exact-head adoption workflow succeeds;
- independent review of exact candidate head returns `APPROVED`, CRITICAL=0, HIGH=0 before merge.

## TESTS

Candidate-local/static:
- JSON parse for all `docs/gef/*.json`;
- workflow YAML parse or GitHub workflow acceptance;
- `git diff --check`;
- exact allowlist diff validation;
- grep/assertions for GEF version, source hash, CP0035, PR #78, Shadow Assurance and PDF-only rule.

Hosted:
- `.github/workflows/gef-adoption-governance.yml` at exact PR head.

Product suites are not re-run by default because this patch cannot touch product/runtime paths. Any unexpected product path delta invalidates this assumption and blocks.

## EVIDENCE

- exact base/head SHA;
- changed-file list;
- source PDF SHA-256;
- discovery/collision receipts;
- hosted run/check IDs and conclusion;
- independent review receipt;
- unresolved finding counts;
- explicit confirmation that CP0035 and PR #78 product authority were not modified.

## ROLLBACK / RECOVERY

Before merge: close the PR and delete only the isolated governance branch if needed. No runtime state is affected.
After merge: revert the governance merge through a new reviewed PR. Never rewrite history.

## DELIVERABLES

- updated `docs/gef` universal adoption package;
- reconciled Work Order/prompt delivery docs;
- exact-head adoption CI;
- PR tied to Issue #79;
- Evidence Bundle;
- independent review handoff;
- post-merge checkpoint delta only after approval/merge.

## REVIEW FORMAT

Verdict exactly one of:
- `APPROVED`
- `CORRECTION REQUIRED`
- `BLOCKED`

For approval: exact candidate SHA, mandatory checks successful, CRITICAL=0, HIGH=0, no scope/evidence/preservation/stale-head mismatch.

## STOP CONDITION

Before independent approval and merge: `GEF_ADOPTION_EXACT_HEAD_EVIDENCE_REQUIRED`.

If base/head/source drifts or required capabilities/evidence are unavailable: fail closed.

Finished only after approved merge, default-branch verification and post-adoption current-state/checkpoint promotion: `GEF_V1_ADOPTED_READY_FOR_GOVERNED_DEVELOPMENT`.
