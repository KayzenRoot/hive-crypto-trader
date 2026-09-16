# Evidence Bundle — HCT-GEF-ADOPT-0002

Status: `AUTHOR_CANDIDATE / INDEPENDENT_REVIEW_REQUIRED`
Risk: `PROCESS_GOVERNANCE / HIGH_ASSURANCE_COMPATIBILITY`
Issue: `#79`
Base: `9e6014472df7723b21f9a1d7ab2aa207ac714ccc`

## Source evidence

- source artifact: `GEF-V1-UNIVERSAL-ADOPTION-PROMPT.pdf`
- source SHA-256: `af1de7df4db966f1109992741191b58d3daccaa7d42a4bff218aaa63e80dc2f3`
- repository classification: `BROWNFIELD`
- discovery receipt: `docs/gef/GEF-DISCOVERY-RECEIPT.json`
- collision map: `docs/gef/GEF-COLLISION-MAP.json`
- universal adoption contract: `docs/gef/GEF-V1-UNIVERSAL-ADOPTION-CONTRACT.md`

## Canonical pre-adoption state

- main head at Context Lock: `9e6014472df7723b21f9a1d7ab2aa207ac714ccc`
- checkpoint: `HCT-CP-0035 / IMPLEMENTATION_AUTHORIZED_S2B`
- authorized product increment: `HCT-IMP-0011-S2B`
- active implementation PR: `#78`
- production credentials authorized: `false`
- production deployment authorized: `false`
- limited-live authorized: `false`
- live trading authorized: `false`

## Discovery findings addressed

- stale S0C-era GEF current/profile state: refreshed by this candidate;
- stale old-adoption workflow base and S0C assertions: replaced with Universal V1.0.0 upgrade checks;
- docs/12 vs docs/104 complete-prompt delivery contradiction: reconciled in favor of governed PDF-only delivery;
- old GEF proof/test-impact/cache validity: retained only as Shadow Assurance/compatibility unless revalidated;
- main branch protection observed disabled: recorded as `CAPABILITY_GAP`, not represented as enforced protection.

## Patch boundary

Authorized:
- `docs/gef/**`
- `docs/12-work-order-prompt-contract.md`
- `prompts/README.md`
- `work-orders/HCT-GEF-ADOPT-0002.md`
- `evidence/HCT-GEF-ADOPT-0002.md`
- `.github/workflows/gef-adoption-governance.yml`

Forbidden:
- product/runtime source;
- active PR #78 candidate files;
- checkpoints;
- frozen product requirements;
- product ADRs;
- deployment/live authority.

## Validation plan and receipts

Author-side static validation is encoded in the adoption workflow:
- exact PR event/head/base assertion;
- merge-base assertion;
- allowlist diff;
- `git diff --check`;
- required artifact presence;
- JSON parsing;
- universal contract/source hash assertions;
- CP0035/PR78/Shadow Assurance/PDF-only assertions;
- negative assertion that runtime/checkpoint/product-governance paths did not change.

Hosted exact-head run IDs belong in GitHub checks/comments after the PR head is published. They are intentionally not committed after CI merely to store receipts.

## Product regression rationale

No product runtime path is authorized in this candidate. Therefore product test suites are not duplicated solely for this governance-only migration. Any unexpected product path change causes the adoption workflow to fail closed and invalidates this rationale.

## Remaining gates

- exact-head `gef-adoption-governance`: `PENDING` until PR execution;
- independent semantic review: `PENDING`;
- unresolved CRITICAL/HIGH: `UNKNOWN` until independent review;
- merge: `FORBIDDEN` until exact-head gate success and independent `APPROVED`.

## Checkpoint Delta proposal

Do not promote a new checkpoint from the author stream.

After independently approved merge, propose a governance-only delta that records:
- GEF version `GEF Bootstrap V1.0.0 Universal`;
- adoption merge SHA and review/gate receipts;
- no consumption or widening of `HCT-IMP-0011-S2B` authority;
- next legal product action remains governed by the then-current S2B state.

## STOP CONDITION

`GEF_ADOPTION_EXACT_HEAD_EVIDENCE_REQUIRED`
