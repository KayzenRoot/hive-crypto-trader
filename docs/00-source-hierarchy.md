# Source Hierarchy

Hive Crypto Trader uses repository state as canonical truth. Conversation memory is never authoritative.

Priority order:
1. `docs/11-checkpoint.md` plus machine-readable checkpoint state under `checkpoints/`
2. `docs/10-decisions-ledger.md` and approved ADRs
3. `docs/03-scope.md`
4. `docs/09-definition-of-done.md`
5. `docs/04-architecture.md`
6. `docs/02-requirements.md`
7. Remaining governed documentation and evidence

Git state, executable code, tests, CI and objective evidence override prose when conflicts are discovered. Approved decisions must never be silently overwritten.