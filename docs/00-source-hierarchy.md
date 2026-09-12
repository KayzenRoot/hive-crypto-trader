# Source Hierarchy

Status: `R12_FREEZE_CANDIDATE`

Hive Crypto Trader uses repository state as canonical truth. Conversation memory is never authoritative.

## Priority order
1. `docs/11-checkpoint.md` plus machine-readable checkpoint state under `checkpoints/`
2. `docs/10-decisions-ledger.md` and approved ADRs
3. `docs/03-scope.md`
4. `docs/09-definition-of-done.md`
5. `docs/04-architecture.md`
6. frozen requirements authority
7. remaining governed documentation and evidence

## Frozen requirements authority
Before R12 is independently approved, merged and checkpoint-promoted, the currently approved requirement sources remain the planning authority described by `docs/96-r11-requirements-freeze-input-inventory.md`.

On governed `FREEZE_APPROVED` promotion, frozen requirements authority becomes the composite baseline defined by:
- `docs/99-r12-frozen-requirements-baseline.md`;
- `docs/100-r12-requirements-traceability-and-no-loss-proof.md`;
- the exact nine requirement source blobs recorded by that manifest;
- `docs/101-r12-freeze-governance-change-control-and-deferred-decisions.md` for post-freeze change control and deferred decisions.

The composite baseline does not lower the precedence of Checkpoint, Decisions Ledger, Scope, DoD or Architecture. It replaces direct reliance on only `docs/02-requirements.md` as the complete requirements layer.

## Conflict and evidence rules
Git state, executable code, tests, CI and objective evidence override prose when conflicts are discovered. Approved decisions must never be silently overwritten.

Within frozen requirements, genuine conflicts are resolved by:
1. approved Decisions Ledger/ADR;
2. later approved formal-round contract within its scope;
3. stricter HIGH_ASSURANCE safety/security/risk restriction when the conflict is only permissive versus restrictive and no decision says otherwise;
4. otherwise the conflict blocks approval until explicitly resolved.

Historical round-local status labels do not nullify a requirement whose exact source blob is included by an approved frozen baseline.

## Change control
After freeze, unexplained semantic or blob drift in frozen-critical sources requires impact analysis and governed revalidation before the changed state may become canonical. The detailed contract is in `docs/101-r12-freeze-governance-change-control-and-deferred-decisions.md`.
