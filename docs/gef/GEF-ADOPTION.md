# UADS GEF V1 Adoption — Hive Crypto Trader

Status: `PREPARED_PENDING_INDEPENDENT_REVIEW`
GEF version: `UADS-GEF-V1`
Project mode: `PARTIALLY_GOVERNED`
Project fingerprint: `sha256:28ad059f859668b3447b58db4f45ecc09111b79d886f83ec60000b2ad72162bc`
Baseline head: `main@29dc6636360953941a7e4fb41a0876c5bc46dcd6`
Adoption branch: `governance/UADS-GEF-V1-adoption`
Adoption issue: `#43`
Active functional work preserved: `PR #42 / Issue #41 / implementation/HCT-IMP-0003-S0C`

## Purpose

Adopt UADS GEF V1 as a process, prompt-compilation, evidence and delta-review layer without replacing or weakening HCT's existing governance.

GEF is subordinate to the canonical HCT source hierarchy. It does not authorize product work, change a Work Order, change a checkpoint, widen an authorization ceiling, or convert an unknown state into allow.

## Classification

`PARTIALLY_GOVERNED`

HCT already has checkpoints, frozen requirements, Work Orders, ADRs, exact-head CI, independent HIGH_ASSURANCE review, bounded implementation authorization and PDF-only executor prompts. GEF adds task classification, context-radius control, budget governors, Machine Evidence, proof carry-forward/invalidation, HEDS Delta review, telemetry and deterministic-work-plane contracts.

## Preserved canonical process

- Default branch: `main`.
- Canonical baseline at adoption start: `29dc6636360953941a7e4fb41a0876c5bc46dcd6`.
- Current checkpoint at adoption start: `HCT-CP-0019 / IMPLEMENTATION_AUTHORIZED_S0C`.
- Existing source hierarchy remains authoritative.
- `docs/104-chat-delivery-and-prompt-artifact-policy.md` remains authoritative and keeps complete executor/reviewer prompts PDF-only.
- Existing HIGH_ASSURANCE rule remains: exact-head gates plus independent review before governed merge/promotion.
- Active PR #42 remains untouched by this adoption PR.
- Existing production credential, deployment, limited-live and live-trading authorization flags are not changed by GEF adoption.

## Immediate GEF operating mode

New prompt and correction artifacts SHALL use task classes `T0/T1/T2/T3`, context radius `C0..C4`, Decision Freeze Capsule, Context Slice, Patch Map/Patch Recipe, explicit Search/Patch/Retry budgets, `SOURCE_MATCH`, A0/A1/A2 local assurance, A3 hosted gates, compact Machine Evidence, exact-head HEDS Delta review and governed STOP states.

Current prompt mode: `GEF_V1`
Current review mode: `HEDS_DELTA`
Shadow Assurance: `ON`

Shadow Assurance means GEF may reduce prompt/context/report overhead immediately, but test skipping and proof carry-forward are advisory only until enough shadow cycles prove no loss of assurance.

## Existing-to-GEF compatibility map

| Existing HCT mechanism | GEF mapping |
|---|---|
| checkpoint/latest + docs/11 | Source Drift Sentinel / Current State |
| Work Order | UPIR / Task Manifest |
| ADR / Decisions Ledger | Decision Freeze Capsule |
| bounded changed-file surface | Patch Map + Patch Budget |
| exact-head workflows | A3 Gate Receipts |
| evidence markdown | Human projection of Machine Evidence |
| independent HIGH_ASSURANCE review | A4 / HEDS semantic assurance |
| correction review cycles | HEDS Delta + invalidated proofs |
| PDF-only prompt policy | GEF Execution/Correction Pack delivered as PDF |

## Adoption Gap Matrix

| CURRENT | TARGET | MIGRATION ACTION | RISK | OWNER |
|---|---|---|---|---|
| Work Orders are detailed but prompt packs can repeat repository history | Compiled GEF Execution/Correction Packs | Use task class, context radius, frozen decisions and bounded patch recipe in all new prompts | LOW | ChatGPT/HEDS |
| Exact-head CI exists | Gate Receipt model | Record exact-head run/check outside source head and reference it from Machine Evidence/HEDS | LOW | HEDS/GitHub |
| Evidence mostly narrative Markdown | Machine Evidence first | Introduce GEF evidence schema; keep human report as derived view | MEDIUM | Executor/HEDS |
| Review is rigorous but often full re-read | HEDS Delta | First review broad; later reviews delta-first with proof invalidation | MEDIUM | HEDS |
| No formal proof dependency map | Proof Map | Start conservative map; all carry-forward remains shadow-only initially | MEDIUM | HEDS |
| No source-to-test impact manifest | Test Impact Map | Seed from current workflows/tests; keep inference conservative | MEDIUM | Engineering |
| No deterministic budget governor | Search/Patch/Retry budgets | Require budgets in new prompt packs; stop on material overrun | LOW | Prompt compiler |
| No native DWP runtime | Deterministic Work Plane | Start with contracts/manifests only; add scripts later in a separate governed increment when ROI is proven | LOW | Future GEF automation |
| No measured token/time baseline | Telemetry baseline with UNKNOWN fields | Record known CI/test data and mark unavailable metrics UNKNOWN; start collection next Work Order | LOW | Runtime/executor |
| Historical workflow path filters can trigger stale slice gates | Impact-aware hosted gates | Track as explicit gap; do not rewrite active S0C in adoption PR | MEDIUM | Future CI governance |

## Native DWP decision

No native DWP script is added in this adoption PR. That would add automation behavior while PR #42 is active and could expand scope unnecessarily. Contracts for Machine Evidence, proof validity, budgets and receipts are prepared now. Native automation is a separate future governed increment.

## GEF ADOPTION RESULT

project: `Hive Crypto Trader`
mode: `PARTIALLY_GOVERNED`
projectFingerprint: `sha256:28ad059f859668b3447b58db4f45ecc09111b79d886f83ec60000b2ad72162bc`
baselineHead: `29dc6636360953941a7e4fb41a0876c5bc46dcd6`
adoptionBranch: `governance/UADS-GEF-V1-adoption`
pr: `PENDING_CREATION`
filesCreated: `docs/gef/* plus .github/workflows/gef-adoption-governance.yml`
filesAdapted: `none; existing canonical files preserved`
currentPromptMode: `GEF_V1`
currentReviewMode: `HEDS_DELTA`
shadowAssurance: `ON`
existingGates: `planning-freeze governance; implementation authorization gates; s0a-quality; s0b-quality; active s0c-quality`
gaps: `native DWP not yet implemented; token/search/time telemetry unavailable historically; proof carry-forward not yet authoritative; historical workflow impact filters require later cleanup`
risks: `proof reuse must stay shadow-only; GEF must not override HCT authorization/checkpoint semantics`
nextAction: `open and independently review the GEF adoption PR; after merge, use GEF packs/HEDS Delta by default`
status: `READY_WITH_GAPS`

## STOP CONDITION

This adoption is complete for preparation when the docs/governance PR is open, exact-head adoption checks pass, active functional work remains untouched, and independent review is requested. Do not merge this structural adoption without HCT review/gates.
