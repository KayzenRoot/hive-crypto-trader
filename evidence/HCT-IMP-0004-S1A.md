# HCT-IMP-0004-S1A - Execution Evidence

Status: `CORRECTION_LOCAL_ASSURANCE_PENDING_EXACT_HEAD_CI`
Risk: `HIGH_ASSURANCE`
UADS Work Order: `wo_139098d83c6aed63`
UADS execution run: `er_0bfdeaed47eae52f`

## Context Lock

- Repository: `KayzenRoot/hive-crypto-trader`
- Implementation branch: `implementation/HCT-IMP-0004-S1A`
- Authorized base/main: `ad8037a2e662eb2100d7626870f31bc97d824fc6`
- Remote implementation branch before mutation: `ad8037a2e662eb2100d7626870f31bc97d824fc6`
- Checkpoint: `HCT-CP-0021 / IMPLEMENTATION_AUTHORIZED_S1A`
- Issue: `#47` OPEN
- Scope: `HCT-IMP-0004-S1A`
- Ceiling: `NON_TRADING_STAGE_1_EXCHANGE_ABSTRACTION_CAPABILITY_CONTRACT_FOUNDATION_ONLY`
- `implementation_authorized=true`
- `production_credentials_authorized=false`
- `production_deployment_authorized=false`
- `limited_live_authorized=false`
- `live_trading_authorized=false`

The local working tree was clean before mutation. No reset, stash, force operation,
rebase, or history rewrite was used. The final exact candidate head and hosted run
IDs are intentionally recorded in the PR/Issue handoff after CI to avoid a
self-referential tracked-file cycle.

## Correction scope

- Previous reviewed head: `c4b3bb16d041eac0cab57e1cf3b2b3a15341d0f0`.
- Correction authority: HCT-IMP-0004-S1A Correction Pack GEF V1.
- H001: broaden the structured production AST boundary scan and add direct
  regression coverage for the required negative-capability families.
- H002: remove the deterministic in-memory fake from the shipped package and
  keep it in `apps/backend/tests/test_exchange_reference.py` only.
- No contract, checkpoint, Work Order, workflow, lockfile, dependency, exchange
  connection, credential, deployment or live-trading surface was changed.

## Changed files and justification

- `adr/HCT-ADR-0045-s1a-exchange-reference-foundation.md` - bounded design decision and authority proof.
- `packages/contracts/openapi.json` - canonical identity-kind extension required by `StableId` reuse.
- `apps/backend/src/hct_backend/contracts.py` - runtime enum projection for the canonical identity kinds.
- `apps/backend/src/hct_backend/generated_contracts.py` - deterministic generated backend projection.
- `apps/frontend/src/generated/contracts.ts` - deterministic generated safe-contract projection; no frontend behavior added.
- `apps/backend/src/hct_backend/exchange_reference.py` - S1A provider-neutral reference domain and read-only port.
- `apps/backend/tests/test_exchange_reference.py` - identity, capability, immutability, Decimal validation and adapter-boundary tests.
- `scripts/scan_s1a_boundaries.py` - AST-aware changed-candidate boundary and secret scan.
- `.github/workflows/s1a-quality.yml` - pull-request-only exact-head S1A governance receipt.
- `evidence/HCT-IMP-0004-S1A.md` - truthful execution evidence and limitations.

No checkpoint, frozen requirement, Scope, Decisions Ledger, Work Order, unrelated
historical workflow, backend lockfile, persistence, deployment or product UI file
was changed.

## Contract and capability decisions

The existing canonical `StableId`/`IdentityKind` contract was extended with
`EXCHANGE`, `INSTRUMENT`, `CAPABILITY_SNAPSHOT` and `REFERENCE_SNAPSHOT`, then
regenerated deterministically. No new parallel identity system was introduced.

The backend reference domain provides immutable exchange descriptors, explicit
`SUPPORTED`/`UNSUPPORTED`/`UNKNOWN` capability declarations, fail-closed
capability helpers, immutable/versioned fingerprints, exact `Decimal` contract
increments and optional known bounds. Unknown material facts remain explicit and
are never assigned permissive defaults. Native symbols are mapping metadata and do
not define canonical contract identity.

The `ExchangeReferenceAdapter` protocol exposes only exchange description,
capability snapshot, reference listing and canonical/native lookup. The deterministic
in-memory adapter is defined only in the backend test module and is not included in
the installed production package. No command surface, transport, account-state
read, persistence or runtime session behavior is present.

The corrected production scanner remains AST/structured and fail-closed. It covers
direct and alternate network/client imports, connection/client/session creation,
auth/signing definitions and calls, credential-shaped arguments/fields, order and
leverage/margin mutations, position mutations, market ingest/subscription runtime,
persistence imports and recognizable persistence adapter definitions. Its tests
also prove documentation/test vocabulary is ignored and `authority` is not treated
as an authentication marker.

## Prior-head evidence carried forward

- Contract generation reproducibility: `PASS`.
- Canonical/runtime parity: `PASS (10 schemas)`.
- Full backend suite: `77 passed`.
- Backend coverage: `89%` total (`1214` statements, equal to the accepted baseline).
- Focused S0A/S0B/S0C regressions: `59 passed`.
- S1A boundary and secret scan: `PASS`.
- S0A boundary validation: `PASS` with the generated local `.ruff_cache` directory excluded; a clean CI checkout has no cache artifact.
- S0A secret scan: `PASS`.
- Backend Ruff: `PASS`.
- Strict mypy: `PASS`.
- Backend build: `PASS`.
- Python dependency audit: `PASS / no known vulnerabilities`.
- Frontend typecheck: `PASS`.
- Frontend tests: `13 passed`.
- Frontend lint: `PASS`.
- Changed generated-contract format: `PASS`.
- Frontend build: `PASS`.
- npm audit: `PASS / 0 vulnerabilities`.
- `git diff --check`: `PASS`.

These values describe the prior reviewed head and remain valid carried evidence
unless changed inputs invalidate them. The corrected head has fresh local results
below.

## Correction local evidence

- Focused scanner and exchange-reference tests: `21 passed`.
- Full backend suite with coverage: `81 passed`, `90%` total (`1177` statements).
- Focused S0A/S0B/S0C regressions: `59 passed`.
- Contract generation reproducibility: `PASS`; canonical/runtime parity: `PASS (10 schemas)`.
- S0A boundary validation: `PASS`.
- S0A secret scan: `PASS`.
- S1A boundary and secret scan: `PASS (11 changed files)`.
- Backend Ruff: `PASS`; strict mypy: `PASS`; backend build: `PASS`.
- Python dependency audit: `PASS / no known vulnerabilities`.
- Frontend typecheck: `PASS`; frontend tests: `13 passed`; frontend lint: `PASS`.
- Changed generated-contract format: `PASS`; frontend build: `PASS`.
- npm audit: `PASS / 0 vulnerabilities`.
- `git diff --check`: `PASS`.

UADS `verify` bound the current change digest but then stopped with a scope
classifier mismatch: it marked the Work Order's explicitly authorized ADR,
backend, generated-contract, scanner, workflow and evidence paths as out of
scope. The failure was recorded as `fail_fd04434bdf2a4d1a` and diagnosed as
`needs-evidence` with no ranked root-cause hypothesis. This is a UADS fallback
classifier limitation; the repository Work Order and PDF remain the governing
scope, so local gates continued sequentially without widening the implementation.

The repository-wide frontend `format:check` was also run. It reports 11
pre-existing files on the authorized base as unformatted; the changed generated
contract passes independently. Those unrelated files were not reformatted because
they are outside the S1A allowed surface. This is recorded as a baseline
limitation, not as a fabricated pass.

## Deferred work and firewall

Concrete venue transport, external connections, authentication/signing, raw
credentials, public/private streams, market ingestion, universe/scanner runtime,
quota/reconnect/session runtime, data quality, market-state/cache runtime, commands,
money-state, risk/safety/session/sizing/margin authority, persistence/RLS, public
trading routes, frontend controls, deployment, limited-live, real-money trading and
later Stage-1/Stage-2 slices remain explicitly deferred and unauthorized.

## Hosted handoff

- Final exact implementation head: recorded in the PR/Issue handoff after push.
- Exact `s1a-quality` run/check: recorded in the PR/Issue handoff after fresh CI.
- Author-side findings: to be recorded after exact-head preflight.
- This artifact is not independent approval and does not authorize merge or
  checkpoint promotion.
