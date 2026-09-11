# Work Order and Prompt Delivery Contract

Every governed increment uses one stable ID across prompt, branch, PR, evidence, corrections and checkpoint.

## Mandatory Work Order sections
`OBJECTIVE`
`CONTEXT`
`SCOPE`
`OUT OF SCOPE`
`FILES/SOURCES TO READ`
`REQUIREMENTS`
`ARCHITECTURE RULES`
`CONSTRAINTS`
`ACCEPTANCE CRITERIA`
`TESTS`
`DELIVERABLES`
`REVIEW FORMAT`
`STOP CONDITION`

For implementation-oriented prompts, use the Hive Plan sequence:
`Context Lock -> Work Order -> Implementation Blueprint -> Rendered Executor Prompt`.
Any blueprint deviation must be explicit and auditable.

## Prompt delivery to the user
For relevant executor Work Orders, deliver:
1. a human-readable `.md` prompt;
2. a `.pdf` version for direct use/download;
3. a `.zip` execution bundle containing the prompt plus governed supporting artifacts when useful;
4. optional machine-readable `.json` when automation benefits from it.

The PDF/MD content must be self-contained enough for the executor to run without reconstructing missing requirements from chat history.

## Review return contract
Executor evidence must include, as applicable: base/head SHA, changed files, decisions, tests, lint, typecheck, build, security/architecture/migration/benchmark evidence, corrected failures, risks, diffs/evidence links and proposed Checkpoint Delta.

Auditor verdict is exactly one of:
- `APPROVED`
- `CORRECTION REQUIRED`
- `BLOCKED`

No next increment is generated while the current increment still requires correction, validation, approval, merge or required post-merge checks.