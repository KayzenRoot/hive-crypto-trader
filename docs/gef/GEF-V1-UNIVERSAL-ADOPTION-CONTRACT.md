# GEF Bootstrap V1.0.0 Universal Adoption Contract — Hive Crypto Trader

Status: `GOVERNED_CANDIDATE`
Source artifact: `GEF-V1-UNIVERSAL-ADOPTION-PROMPT.pdf`
Source SHA-256: `af1de7df4db966f1109992741191b58d3daccaa7d42a4bff218aaa63e80dc2f3`
Adoption Work Order: `HCT-GEF-ADOPT-0002`
Repository: `KayzenRoot/hive-crypto-trader`
Adoption base: `main@9e6014472df7723b21f9a1d7ab2aa207ac714ccc`

## Purpose

This document incorporates the user-supplied GEF Bootstrap V1.0.0 universal adoption model into HCT as a brownfield governance overlay. It does not replace HCT's stricter canonical source hierarchy, authorization model, HIGH_ASSURANCE requirements, frozen product requirements, or exact-head independent-review rules.

When this contract conflicts with a higher-precedence HCT source, the HCT source wins and the conflict becomes a fail-closed reconciliation item.

## Repository classification

`BROWNFIELD`

HCT is a mature, partially implemented and heavily governed repository with approved checkpoints, frozen requirements, ADRs/Decisions Ledger, bounded Work Orders, exact-head CI, independent HIGH_ASSURANCE review, evidence bundles, product/runtime code, tests, and active governed implementation work.

The universal GEF migration MUST wrap the existing project. It MUST NOT reshape HCT into a template.

## Canonical GEF lifecycle

`ANALYZE → SOURCE CHECK → NEXT NECESSARY INCREMENT → WORK ORDER → CONTEXT LOCK → PREFLIGHT → EXECUTOR → TESTS/EVIDENCE → PR → EXACT-HEAD AUDIT → CHECKPOINT DELTA → MERGE → NEXT`

For HCT, every step is additionally constrained by the current checkpoint authorization ceiling and the PDF-only handoff policy.

## Authority order

GEF adopts the HCT-compatible authority order:

1. current checkpoint / production state;
2. approved Decisions Ledger / ADRs;
3. approved Scope and frozen Requirements;
4. Definition of Done / acceptance criteria;
5. Architecture;
6. Security / policy;
7. current Work Order / Context Lock;
8. supporting governed documentation;
9. informal notes or chat prose.

The repository's `docs/00-source-hierarchy.md` remains the authoritative conflict-resolution source.

## Brownfield preservation rules

The migration SHALL:

- inspect the repository before mutation;
- preserve history, architecture, tests, CI, release evidence and approved decisions;
- prefer additive adoption and explicit mappings over renaming/reorganization;
- treat existing HCT conventions as authoritative where stricter or project-specific;
- never fabricate historical Work Orders, tests, releases, approvals or evidence;
- never convert `UNKNOWN` to pass/allow;
- never weaken tests, security, CI, branch/ruleset behavior or review gates merely to obtain a green result;
- never modify active product implementation work from the GEF adoption increment;
- separate pre-GEF history, adoption/upgrade baseline, and post-adoption governed work;
- record capability gaps instead of pretending unsupported controls exist.

## Discovery and collision model

Every GEF adoption/upgrade uses a Repository Discovery Receipt and Collision Map. Collision entries use:

- `CREATE_SAFE`
- `EXISTS_COMPATIBLE`
- `EXISTS_NEEDS_MERGE`
- `EXISTS_PROJECT_AUTHORITY`
- `COLLISION`
- `DEFER`
- `NOT_APPLICABLE`

For HCT, existing checkpoint, Work Order, evidence, ADR, source-hierarchy and CI structures are reused rather than duplicated into `.engineering/`.

## Work Order standard

Every governed increment keeps one stable ID across branch, PR, evidence, corrections and checkpoint delta. A Work Order includes at least:

- stable ID and title;
- objective and context;
- source inputs;
- scope and out-of-scope;
- allowed files/areas and preservation constraints;
- requirements;
- architecture and security constraints;
- acceptance criteria;
- tests;
- evidence requirements;
- review requirements;
- rollback/recovery;
- deliverables;
- STOP CONDITION.

## Context Lock acceleration

Before mutation, the executor compiles the smallest safe context and may include:

- Implementation Seed Tree;
- File Intent Capsule;
- Brownfield Patch Intent Capsule;
- Executor Navigation Map;
- Decision Closure Capsule;
- Execution Waves;
- Validation Reuse Plan;
- Critical Path;
- Marathon Execution Pack.

Full-repository rediscovery is not the default when a bounded context is sufficient.

## Testing and evidence

Validation expands by risk:

1. structural/static checks;
2. focused tests;
3. impacted dependency tests;
4. boundary/integration checks;
5. risk-expansion checks;
6. full candidate validation when required.

Existing HCT HIGH_ASSURANCE hosted gates remain mandatory. Proof reuse remains Shadow Assurance unless separately promoted by evidence and a governed decision.

Evidence must bind Work Order, exact candidate SHA, commands/checks, results, failures/corrections, security observations, remaining risks and external gate receipts. Missing evidence is not completion.

## Exact-head audit

A governed `APPROVED` verdict requires, at minimum:

- the reviewed candidate SHA is explicit;
- all mandatory exact-head checks are complete and successful;
- unresolved `CRITICAL = 0`;
- unresolved `HIGH = 0`;
- no scope, evidence, preservation or stale-head mismatch;
- an independent review stream when HCT requires it.

Any head change invalidates the prior exact-head verdict for the new head.

## GitHub governance

Use feature/governance branches and PRs compatible with existing HCT conventions. No force-push, history rewrite, destructive reset, direct canonical mutation that bypasses a required gate, or silent merge of active implementation work.

If branch protection/rulesets cannot be enforced or inspected through available capabilities, record `CAPABILITY_GAP`; do not invent protection.

## Security baseline

Applicable increments consider secret exposure, path traversal/symlink hazards, malicious configuration, dependencies, permissions, shell/process execution, generated artifacts, partial-mutation recovery, logging/redaction and token permissions.

Any unresolved HIGH/CRITICAL security issue blocks approval.

## HCT-specific invariants

- `docs/104-chat-delivery-and-prompt-artifact-policy.md` governs user-facing prompt delivery.
- Complete executor/reviewer prompts are PDF-only in chat.
- GEF never widens `implementation_authorization_scope` or its ceiling.
- Production credentials, production deployment, limited-live and live trading remain separately governed.
- Active PR `#78 / HCT-IMP-0011-S2B` is outside this adoption patch surface.
- `HCT-CP-0035` remains canonical until a separately reviewed checkpoint delta is promoted.

## Universal adoption STOP states

- `GEF_ADOPTION_IN_PROGRESS`
- `GEF_ADOPTION_EXACT_HEAD_EVIDENCE_REQUIRED`
- `GEF_ADOPTION_BLOCKED_BY_CAPABILITY_GAP`
- `GEF_V1_ADOPTED_READY_FOR_GOVERNED_DEVELOPMENT`

The finished state is legal only after exact-head evidence, independent review where required, merge, default-branch verification and post-adoption checkpoint/current-state promotion.
