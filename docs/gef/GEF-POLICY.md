# UADS GEF V1 Local Policy — Hive Crypto Trader

Status: `GOVERNED_CANDIDATE`

## Authority

GEF is an optimization layer. Canonical HCT source priority remains:

`checkpoint/current state > ADR/Decision Ledger > Scope > Definition of Done > Architecture > Requirements > planning notes > chat prose`

When GEF conflicts with a newer/higher HCT source, record `SOURCE_CONFLICT`, preserve the higher source, and stop for reconciliation.

## Non-negotiable HCT overrides

1. Complete executor/reviewer prompts remain PDF-only under `docs/104-chat-delivery-and-prompt-artifact-policy.md`.
2. HIGH_ASSURANCE changes keep exact-head CI and independent review.
3. GEF never widens `implementation_authorization_scope` or the checkpoint authorization ceiling.
4. `UNKNOWN -> ALLOW` is forbidden.
5. Production credentials, production deployment, limited-live and live-trading gates remain independently governed.
6. Active PRs are not silently rebased, retargeted, closed or merged by GEF adoption.
7. Proof from an old head is not exact-head proof for a new head.

## Task classes

- `T0`: mechanical, no architecture exploration.
- `T1`: bounded patch with prescribed recipe and minimal search.
- `T2`: semantic correction within frozen architecture.
- `T3`: architecture work; broad analysis allowed only when explicitly governed.

## Context radius

- `C0`: symbol/function + direct test.
- `C1`: target symbols + direct dependencies + tests.
- `C2`: module + interfaces.
- `C3`: related architecture + cross-module contracts.
- `C4`: broad project architecture.

Start at the smallest safe radius. Expansion requires a real dependency, `SOURCE_CONFLICT`, `SCOPE_EXPANSION_REQUIRED`, or `NEEDS_ARCHITECTURE`.

## Budget policy

Every Execution Pack/Correction Pack SHALL declare search budget, files-opened budget, patch files/LOC budget, retry budget and output discipline.

Budgets are guardrails, not permission to truncate correctness. A material overrun triggers a STOP state instead of unbounded exploration.

## Assurance

- `A0`: syntax/static/basic local.
- `A1`: focused local tests.
- `A2`: impacted local tests/evals.
- `A3`: hosted CI/security/platform/release gates.
- `A4`: HEDS independent semantic assurance.

Do not duplicate a full local suite and full hosted suite by default. Full local reproduction is for diagnosis or when HCT explicitly requires it.

## Shadow Assurance

`ON` for GEF V1 adoption.

Until promoted by separate evidence:
- HEDS may calculate `CARRY_FORWARD`/`INVALIDATED`;
- HEDS may recommend impacted tests;
- hosted required gates are NOT skipped because of GEF proof reuse;
- existing HCT exact-head workflows remain authoritative.

## Model/executor routing

Record requested/applied executor/model when runtime supports it. T0/T1 may use cheaper/faster capable executors when no Model Lock exists. T3 remains on architecture-capable models/agents. Silent substitution under a Model Lock is forbidden.

## Forbidden shortcuts

- UNKNOWN -> ALLOW
- invented test/gate/proof
- old-head receipt presented as exact-head
- silent scope expansion
- executor rediscovery of frozen architecture
- full-repo search by default
- repeated identical retry without causal change
- evidence-only commit after gates just to store run IDs
- merge before required review/gates
- deleting existing governance to simplify adoption
- treating optimization targets as measured results
- carry-forward without validity-input checks
