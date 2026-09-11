# Chat Handoff and Resume Protocol

Goal: changing chats must not change project truth.

## Canonical resume path
1. Locate `KayzenRoot/hive-crypto-trader`.
2. Read `docs/00-source-hierarchy.md`.
3. Read `checkpoints/index.json`.
4. Resolve the active workstream and open `checkpoints/workstreams/<id>/latest.json`.
5. Open the referenced immutable checkpoint under `checkpoints/history/`.
6. Read `docs/11-checkpoint.md`, `docs/10-decisions-ledger.md`, `docs/03-scope.md`, `docs/09-definition-of-done.md`, `docs/04-architecture.md`, `docs/02-requirements.md`.
7. Validate repository/branch/head SHA and critical-source fingerprints recorded by the checkpoint when present.
8. If a critical source changed, mark context `STALE` and rebuild/rebase Context Lock before continuing.
9. Resume only from `next_necessary_action`; never infer a later step from chat memory.

## User shorthand
When the user says a phrase such as `continue do chat anterior` for Hive Crypto Trader, the new chat should execute this recovery procedure before generating the next increment.

## Safety gate
If checkpoint, Scope, DoD, Architecture or a relevant approved decision changed, no executor prompt may be issued until context is refreshed.