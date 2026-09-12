# Chat Delivery and Prompt Artifact Policy

Status: `GOVERNED`
Applies to: all Hive Crypto Trader chats, review sessions and executor handoffs
Risk class: `PROCESS_GOVERNANCE`

## Purpose
Prevent long executor prompts from polluting chat history and make every executable handoff a durable, downloadable artifact.

## Mandatory PDF-only prompt rule
Every complete executable prompt, Work Order execution prompt, correction prompt, bootstrap prompt, review prompt, Codex prompt, Cursor prompt, agent prompt or equivalent instruction package produced for the user SHALL be delivered as a downloadable PDF artifact.

The assistant SHALL NOT place the complete prompt in:
- a writing block;
- a code block;
- a copyable prompt box;
- a long inline chat message;
- any other chat-native container intended to reproduce the full executable prompt.

The chat response SHALL contain only a concise summary of the artifact, its purpose, important execution boundary, and a download link to the PDF.

If PDF generation fails, the assistant SHALL fail closed: report the artifact-generation failure and fix/regenerate the PDF. It SHALL NOT fall back to publishing the full prompt inline unless the user explicitly revokes this policy for that specific artifact.

## First-prompt repository synchronization rule
When an executor such as Codex or Cursor is receiving its first prompt for a repository/session, the PDF SHALL include a repository synchronization and Context Lock phase before any mutation or review work. At minimum it SHALL:
- identify the canonical repository and target PR/branch/SHA when applicable;
- verify authentication/access;
- fetch/synchronize remote state safely;
- avoid destructive reset/force operations;
- preserve dirty local work by using an isolated clone/worktree when necessary;
- validate the exact expected Git state before proceeding;
- fail closed on unexpected head/base/state drift.

## Required prompt metadata
Every prompt PDF SHOULD identify, when applicable:
- project and repository;
- Work Order/increment ID;
- risk class;
- expected branch/base/head SHA;
- source documents to read;
- objective and scope;
- out-of-scope boundary;
- constraints;
- acceptance criteria;
- required tests/evidence;
- allowed writes/actions;
- forbidden actions;
- review/evidence format;
- STOP CONDITION.

For HIGH_ASSURANCE work, these fields are mandatory when applicable.

## Review prompts
Independent-review prompts SHALL also be delivered only as PDF artifacts. They SHALL preserve execution-stream independence, identify the exact reviewed head, prohibit silent mutation during read-only review, and require an explicit governed verdict when the governing Work Order requires one.

Use of the same GitHub account does not by itself invalidate review independence. Independence is established by a separate review/execution stream that reconstructs its verdict from repository evidence and does not merely reuse the authoring stream's conclusion.

## Chat-resume rule
Every new HCT chat SHALL recover repository state from the canonical checkpoint/source hierarchy and SHALL read this policy before producing any executor prompt.

A user instruction such as `continue do chat anterior`, `continue`, `faça o review`, or equivalent MUST preserve this PDF-only delivery rule unless the user explicitly changes the policy.

## Artifact versus canonical truth
Prompt PDFs are execution/delivery artifacts. They do not outrank the canonical repository source hierarchy. If a prompt conflicts with Checkpoint, Decisions Ledger/ADR, Scope, DoD, Architecture, frozen Requirements or an approved Work Order, the canonical repository source wins and execution SHALL stop for reconciliation.

Any durable policy or decision introduced through a prompt MUST also be reflected in the appropriate canonical repository document/checkpoint before it is treated as project truth.

## Naming convention
Prefer deterministic, descriptive filenames such as:

`HCT-<WORK-ORDER>-<PURPOSE>-<REVISION>.pdf`

Examples:
- `HCT-PLAN-0001-R12-INDEPENDENT-REVIEW-CODEX-V1.pdf`
- `HCT-IMPL-0001-CORRECTION-PROMPT-V2.pdf`

## STOP CONDITION
No complete executor prompt is considered delivered until its PDF artifact has been generated and made available for download.
