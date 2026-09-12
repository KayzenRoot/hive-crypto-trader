# UADS GEF V1 Execution Protocol — HCT

Status: `GOVERNED_CANDIDATE`

## Pipeline

`REQUEST -> Source Drift Sentinel -> Task Class -> Context Radius -> UPIR/Task Manifest -> Decision Freeze Capsule -> Context Slice -> Patch Recipe -> Budgets -> SOURCE_MATCH -> bounded executor -> A0/A1/A2 -> one final publication -> A3 hosted gates + HEDS Delta -> exact-head verdict`

## Prompt-pack header

Every new implementation/correction prompt SHALL state project/repository, Work Order, PR/branch/base/head, task class, context radius, assurance level and prompt compiler version.

For HCT, the full executable pack remains a downloadable PDF.

## Required pack sections

1. `ACCEPTED_AND_FROZEN`
2. `OPEN_GOAL` or `ONLY_OPEN_FINDING`
3. `ROOT_CAUSE / ENGINEERING_DECISION`
4. `PATCH_MAP`
5. `PRESCRIBED_ALGORITHM`
6. `FORBIDDEN_SHORTCUTS`
7. `REQUIRED_TESTS`
8. `SEARCH_BUDGET`
9. `PATCH_BUDGET`
10. `RETRY_BUDGET`
11. `LOCAL_ASSURANCE`
12. `PUBLICATION`
13. `MACHINE_OUTPUT`
14. `STOP_CONDITION`

## SOURCE_MATCH

Before mutation the executor must prove repository identity, expected base/head/branch, checkpoint and Work Order identity, relevant frozen source versions and absence of unexpected drift in the allowed patch surface.

Failure becomes `SOURCE_CONFLICT` or `BLOCKED_EVIDENCE`; it is not permission to explore broadly.

## Correction Pack default

Small corrections should default to task class `T1` or `T2`, context radius `C0` or `C1`, 1–3 source files and 1–3 test files unless evidence requires expansion, a small search budget, one causal retry per failure mode before escalation and one final push when feasible.

## One-shot publication

The executor should locally reach `COMPLETE_CANDIDATE`, then publish one final candidate push whenever practical. Gate receipts are attached outside source HEAD through GitHub checks/comments/artifacts.

## STOP states

- `COMPLETE_CANDIDATE`
- `SOURCE_CONFLICT`
- `SCOPE_EXPANSION_REQUIRED`
- `BLOCKED_EVIDENCE`
- `NEEDS_ARCHITECTURE`

The executor must not silently expand context or scope after a STOP state.

## HCT-specific execution firewall

GEF does not alter HCT's authorization model. An executor can only mutate product code when the current canonical checkpoint explicitly authorizes that exact Work Order/scope/ceiling.
