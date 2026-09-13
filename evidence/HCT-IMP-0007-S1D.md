# HCT-IMP-0007-S1D implementation evidence

## Context Lock

- Repository: `KayzenRoot/hive-crypto-trader`
- Work Order and Issue: `HCT-IMP-0007-S1D`, Issue `#62`
- Execution base: `457d52827ac6e688a81cdbc08dc7999310ca5d17`
- Branch: `implementation/HCT-IMP-0007-S1D`
- Checkpoint: `HCT-CP-0027/IMPLEMENTATION_AUTHORIZED_S1D`
- Authorization scope: `HCT-IMP-0007-S1D` only
- Authorization ceiling: `NON_TRADING_STAGE_1_QUOTA_WS_BACKPRESSURE_GOVERNOR_FOUNDATION_ONLY`
- Higher-risk flags: production credentials, production deployment, limited-live and
  live-trading are all `false`.
- Authorization evidence: PR `#61` approved at exact head
  `3904540eba859b370a8d276717750c7c1c2aae06`, merged as
  `185bc27842a5410a8bd40bf9ff805be64f037297`, with governed run `34725814293`.
- The Work Order locator `docs/02-definition-of-done.md` does not exist in the
  repository. Source hierarchy identifies `docs/09-definition-of-done.md` as the
  canonical Definition of Done, and that file was used for the context lock.

The candidate was implemented in a fresh isolated clone from the exact execution
base. The shared workspace was not modified.

## ADR and changed-file inventory

ADR: `adr/HCT-ADR-0048-s1d-quota-backpressure-governor.md`.

The bounded candidate surface contains exactly these seven files:

1. `adr/HCT-ADR-0048-s1d-quota-backpressure-governor.md`
2. `apps/backend/src/hct_backend/quota_governor.py`
3. `apps/backend/tests/test_quota_governor.py`
4. `apps/backend/tests/test_scan_s1d_boundaries.py`
5. `scripts/scan_s1d_boundaries.py`
6. `evidence/HCT-IMP-0007-S1D.md`
7. `.github/workflows/s1d-quality.yml`

No checkpoint, frozen requirement, Work Order, dependency-lock, frontend source,
shared-contract or generated-contract file was changed.

## Domain and boundary result

The implementation provides immutable provider-neutral types for:

- independent request and subscription limits with versioned source material,
  explicit unknown capacity and SHA-256 policy fingerprints;
- finite `PROTECTION`, `RECONCILIATION`, `NORMAL` and `RESEARCH` priority classes;
- deterministic `ADMIT`, `DEFER`, `SHED`, `CIRCUIT_OPEN` and `UNKNOWN` outcomes with
  an explicit allowed reason matrix and content-bound decision fingerprints;
- bounded queue state with protected reserve enforcement for both quota units and
  queue capacity;
- finite retry count and monotonic elapsed-time budgets;
- pure `CLOSED`, `OPEN` and `HALF_OPEN` circuit transitions with full material
  fingerprints, fail-closed invariants and one explicitly reserved probe slot;
- strictly increasing, explicitly retired session generations;
- immutable requested/accepted/deferred subscription intents bound to the frozen
  `StableId(kind=INSTRUMENT)` identity and containing no executable transport
  handle, callback or network payload.

Unknown evidence never admits work. Stale or retired generations, exhausted
retry state, open circuits, queue saturation and protected reserve conflicts are
deterministically deferred or shed according to priority. Contradictory circuit
states, invalid probe recovery, contradictory outcome/reason pairs and
caller-supplied fingerprints are rejected. No method performs I/O.

The S1D scanner rejects production network/socket/WebSocket imports and calls,
provider routes, `http://`, `https://`, `ws://`, `wss://` and generic domain/host
literals, credentials/private concepts, market-ingest/trading/persistence/
deployment/live surfaces, secrets and changed paths outside the authorized
seven-file boundary. Only the exact HCT-owned canonical identity import required
by S1D is permitted.

## Verification

- H001 circuit fingerprint mutation tests: `PASS`.
- H002 circuit-state invariants and probe-recovery tests: `PASS`.
- H003 content-bound evidence, outcome/reason matrix and closed direct-constructor tests: `PASS`.
- H004 canonical INSTRUMENT identity and negative tests: `PASS`.
- H005 URL/host scanner negative tests: `PASS`.
- Focused H001-H005/S1D tests: `23 passed`.
- Full backend suite: `176 passed`, coverage `90.87%` (threshold `90%`).
- Direct S0A/S0B/S0C/S1A/S1B/S1C plus S1D regressions: `169 passed`.
- Contract generation reproducibility: `PASS`.
- Contract schema parity: `PASS (10 schemas)`.
- Ruff lint: `PASS`.
- Ruff format check: `PASS`.
- Strict mypy: `PASS`.
- Backend build: `PASS`.
- Python dependency audit: `0 known vulnerabilities`.
- Frontend typecheck: `PASS`.
- Frontend tests: `13 passed`.
- Frontend lint: `PASS`.
- Generated-contract Prettier check: `PASS`.
- Frontend build: `PASS`.
- npm audit: `0 vulnerabilities`.
- S1D boundary and secret scan: `PASS`.
- `git diff --check`: `PASS`.

The pull-request-only `s1d-quality` workflow checks out the raw PR head,
asserts the authorized base and CP0027 scope, rejects manual dispatch, enforces
the path boundary, runs all listed backend/frontend/parity/audit gates, and
performs no external exchange calls. Final PR head and hosted run identifiers
are intentionally recorded only in the PR/Issue handoff, not in this tracked
evidence artifact.

## Deferred and prohibited scope

Actual sockets, WebSockets, venue subscribe/unsubscribe, reconnect I/O,
realtime ingestion, provider endpoints or DTOs, credentials/private APIs,
market/account truth, Data Quality, Market-State, Risk, Safety, OMS, Execution,
orders, positions, persistence, deployment, production credentials,
limited-live and real-money trading remain outside S1D. Independent
HIGH_ASSURANCE review is required on the exact final PR head. This evidence is
author-side preflight and is not an approval or authorization for later stages.
