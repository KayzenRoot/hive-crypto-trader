# GEF Bootstrap V1.0.0 Universal Adoption — Hive Crypto Trader

Status: `UPGRADE_CANDIDATE_PENDING_EXACT_HEAD_REVIEW`
GEF version: `GEF-BOOTSTRAP-V1.0.0-UNIVERSAL`
Project classification: `BROWNFIELD`
Adoption Work Order: `HCT-GEF-ADOPT-0002`
Adoption Issue: `#79`
Adoption base: `main@9e6014472df7723b21f9a1d7ab2aa207ac714ccc`
Active product work preserved: `PR #78 / Issue #77 / HCT-IMP-0011-S2B`
Source artifact SHA-256: `af1de7df4db966f1109992741191b58d3daccaa7d42a4bff218aaa63e80dc2f3`

## Purpose

Upgrade HCT's previously merged `UADS-GEF-V1` overlay to the universal GEF Bootstrap V1.0.0 model while preserving all stricter HCT governance and all active user work.

The universal GEF layer optimizes discovery, Context Lock compilation, Work Order execution, evidence and delta review. It is subordinate to the HCT source hierarchy and cannot authorize product work, change checkpoint authority, widen a Work Order, or grant production/live authority.

## Brownfield result

HCT is not reshaped into a template. Existing canonical structures are reused:

- checkpoint/current state: `docs/11-checkpoint.md` + `checkpoints/`;
- decisions: `docs/10-decisions-ledger.md` + `adr/`;
- scope/requirements/DoD/architecture/security: existing governed docs;
- Work Orders: `work-orders/`;
- evidence/context locks: `evidence/`;
- exact-head CI: `.github/workflows/`;
- user-facing handoff: `docs/104-chat-delivery-and-prompt-artifact-policy.md`.

No parallel `.engineering/` tree is introduced.

## Universal operating loop

`ANALYZE → SOURCE CHECK → NEXT NECESSARY INCREMENT → WORK ORDER → CONTEXT LOCK → PREFLIGHT → EXECUTOR → TESTS/EVIDENCE → PR → EXACT-HEAD AUDIT → CHECKPOINT DELTA → MERGE → NEXT`

Current prompt mode: `GEF_BOOTSTRAP_V1_UNIVERSAL`
Current review mode: `GEF_EXACT_HEAD_DELTA`
Shadow Assurance: `ON`

HEDS Delta concepts from the first adoption remain compatible, but the universal lifecycle and exact-head acceptance contract are now the umbrella model.

## Preserved HCT invariants

- Source hierarchy remains authoritative.
- Complete executor/reviewer prompts remain PDF-only for user-facing delivery.
- HIGH_ASSURANCE changes retain exact-head hosted gates plus independent review.
- Proof carry-forward/test skipping remains advisory while Shadow Assurance is ON.
- `UNKNOWN -> ALLOW` is forbidden.
- Production credentials/deployment/limited-live/live trading remain separately governed.
- Active product PR #78 is outside the adoption patch.
- Current checkpoint remains `HCT-CP-0035` until a separately reviewed post-merge delta is promoted.

## Discovery/collision receipts

- `docs/gef/GEF-DISCOVERY-RECEIPT.json`
- `docs/gef/GEF-COLLISION-MAP.json`
- `docs/gef/GEF-V1-UNIVERSAL-ADOPTION-CONTRACT.md`

The key upgrade gaps discovered were stale legacy GEF current/profile state, an obsolete old-adoption CI base, a docs/12 vs docs/104 delivery contradiction, and stale proof/cache validity inputs.

## Capability gap

`main` was observed without enforced branch protection at the adoption baseline. This is recorded as a capability gap. The migration does not claim protection exists and does not weaken existing PR/exact-head/independent-review policy.

## Compatibility with legacy GEF assets

The following legacy assets remain usable as compatibility/shadow inputs only where their validity inputs still match:

- `GEF-PROOF-MAP.json`
- `GEF-TEST-IMPACT.json`
- `GEF-KNOWLEDGE-CACHE.json`
- `GEF-EVIDENCE-SPEC.md`

Old baseline facts are historical evidence, not current exact-head proof.

## Adoption acceptance gate

The upgrade may merge only when:

1. the PR base remains the locked adoption base;
2. the changed paths remain within the Work Order allowlist;
3. all required JSON and GEF artifacts validate;
4. exact-head `gef-adoption-governance` succeeds;
5. independent review of that exact head returns `APPROVED`;
6. unresolved CRITICAL=0 and HIGH=0;
7. no product/runtime/checkpoint/frozen-requirement drift exists.

After merge, verify the default branch and promote only a separately reviewed governance/current-state delta. The S2B product authorization must not be consumed or widened by GEF adoption.

## STOP CONDITION

Current candidate state: `GEF_ADOPTION_EXACT_HEAD_EVIDENCE_REQUIRED`.

Finished state is only:
`GEF_V1_ADOPTED_READY_FOR_GOVERNED_DEVELOPMENT`.
