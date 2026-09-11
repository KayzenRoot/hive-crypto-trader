# Checkpoint

Checkpoint ID: `HCT-CP-0002`
Status: `GOVERNANCE_BOOTSTRAP_APPROVED`
Canonical branch: `main`
Last canonical governance merge: `a9ba61954fd332ebfa3505a1fc9bd0ad2bfe6b19` (`HCT-BOOT-0001`)
Risk class: `HIGH_ASSURANCE`
Functional product planning: `NOT_STARTED`
Implementation authorization: `NOT_GRANTED`

## Frozen bootstrap foundation
- Hive Plan-style source hierarchy and governance are active from project birth.
- GitHub is canonical truth; conversation memory is advisory only.
- Cross-chat resume uses machine-readable workstream checkpoints and Git validation.
- Work Orders use stable HCT IDs across prompts, branches, PRs, evidence, corrections and checkpoints.
- Relevant executor prompts are delivered as MD + PDF + ZIP, with optional JSON automation artifact.
- Review verdicts are APPROVED / CORRECTION REQUIRED / BLOCKED.
- Financial/trading, signing/custody, privileged auth, security-critical and irreversible actions default to HIGH_ASSURANCE.
- Product implementation remains blocked until planning and later authorization gates are satisfied.

## Completed increments
- `HCT-BOOT-0001` — governance, checkpoint/handoff, prompt contract and Source Pack bootstrap; audited and merged via PR #1.

## Current blockers
None for starting structured product discovery. Production implementation remains blocked because functional planning has not started.

## Next necessary action
Open `HCT-PLAN-0001` and begin structured product discovery/planning. Do not generate an implementation Work Order yet.

## Resume rule
A new chat must read `docs/00-source-hierarchy.md`, `checkpoints/index.json`, the active workstream `latest.json`, its referenced history checkpoint, this file, Decisions Ledger, Scope and DoD; validate Git state against the recorded canonical merge; then resume only from `next_necessary_action`.