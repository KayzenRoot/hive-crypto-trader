# Checkpoint

Checkpoint ID: `HCT-CP-0001`
Status: `GOVERNANCE_BOOTSTRAP_IN_REVIEW`
Canonical branch target: `main`
Bootstrap base SHA: `13ab977d56513db6e2d2a1958a2297feba4208e8`
Active increment: `HCT-BOOT-0001`
Active branch: `governance/HCT-BOOT-0001`
Risk class: `HIGH_ASSURANCE`
Functional product planning: `NOT_STARTED`
Implementation authorization: `NOT_GRANTED`

## Frozen bootstrap intent
- use Hive Plan-style governance from project birth;
- GitHub is canonical truth;
- checkpoint supports reliable chat changes;
- executor prompts are governed artifacts, not ad-hoc chat text;
- future financial/trading work uses HIGH_ASSURANCE by default.

## Current blockers
None for governance bootstrap review. Product implementation remains blocked because planning has not started.

## Next necessary action
Audit HCT-BOOT-0001. If APPROVED, merge it, promote the checkpoint to a post-merge canonical SHA, then open `HCT-PLAN-0001` for structured product discovery.

## Resume rule
A new chat must read `docs/00-source-hierarchy.md`, `checkpoints/index.json`, the selected workstream `latest.json`, its referenced history checkpoint, this file, the Decisions Ledger, Scope and DoD; then validate canonical Git SHA before proposing work.