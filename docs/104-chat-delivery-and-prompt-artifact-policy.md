# Chat Delivery and Prompt Artifact Policy

Status: `GOVERNED`
Applies to: all Hive Crypto Trader chats, review sessions and executor handoffs
Risk class: `PROCESS_GOVERNANCE`

## Purpose
Prevent long executor prompts from polluting chat history, make every executable handoff a durable downloadable artifact, and ensure governed work advances continuously without requiring redundant user messages between deterministic steps.

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

## Continuous auto-progression and next-prompt handoff rule
For HCT project-development work, the assistant SHALL continue automatically through every safe, deterministic, already-authorized next action that can be completed with the tools and evidence available in the current response. The user SHALL NOT be required to send `continue`, `prossiga`, `próximo`, or an equivalent message merely to advance a deterministic governance or development step.

Every user-visible HCT project-development response SHALL satisfy one of these outcomes:
1. continue through the available safe steps until an external dependency, governed gate, or STOP CONDITION is reached; and
2. when the next dependency is an executor/reviewer/user handoff, include the next complete executable prompt PDF in that SAME response.

Therefore, a response that finishes a review, merge, checkpoint promotion, authorization preparation, correction preparation or similar bounded step SHALL automatically prepare the next necessary governed action and its prompt artifact before returning to the user whenever source truth and tooling make that possible.

The assistant SHALL NOT end a normal project-development response with only `diga continue`, `quando quiser continuamos`, `peça o próximo prompt`, or equivalent passive wording when the next governed action is already determinable.

Automatic progression MUST stop and fail closed when any of the following applies:
- a source, base/head SHA, checkpoint, branch, PR or authority conflict is detected;
- a new scope/risk/architecture decision requires explicit governed approval;
- an independent-review boundary would be violated by self-approval under the governing Work Order;
- an external action or permission is required that the current tool context cannot perform;
- a required test, exact-head CI gate, evidence item or security check fails or is unavailable;
- a destructive action, force operation, credential action, deployment, limited-live or live-trading action would be required without explicit authority;
- the governing Work Order/PDF defines a STOP CONDITION that prohibits further mutation.

This rule changes delivery cadence only. It NEVER widens implementation scope, bypasses HIGH_ASSURANCE review, converts UNKNOWN to ALLOW, skips exact-head CI, overrides the source hierarchy, weakens fail-closed checkpoints, or grants production credentials, deployment, limited-live or live-trading authority.

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

A user instruction such as `continue do chat anterior`, `continue`, `faça o review`, or equivalent MUST preserve this PDF-only delivery and continuous-auto-progression policy unless the user explicitly changes the policy.

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
No complete executor prompt is considered delivered until its PDF artifact has been generated and made available for download. A project-development response is not complete while a deterministic next governed handoff is already known but its required PDF artifact has not yet been prepared, unless a fail-closed stop condition above applies.
