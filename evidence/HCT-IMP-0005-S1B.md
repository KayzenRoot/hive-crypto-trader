# HCT-IMP-0005-S1B - Execution Evidence

Status: `CORRECTION_LOCAL_PREFLIGHT_PENDING_EXACT_HEAD_CI`
Risk: `HIGH_ASSURANCE`
UADS Work Order: `wo_cb644fc4f8742991`
UADS execution run: `er_b5631e8540a6f401`

## Context Lock

- Repository: `KayzenRoot/hive-crypto-trader`
- Implementation branch: `implementation/HCT-IMP-0005-S1B`
- Authorized base/main: `9fa01c483d503e2ca67a6509cc760e7ab3e88b68`
- Checkpoint: `HCT-CP-0023 / IMPLEMENTATION_AUTHORIZED_S1B`
- Issue: `#51` OPEN
- Scope: `HCT-IMP-0005-S1B`
- Ceiling: `NON_TRADING_STAGE_1_MEXC_PUBLIC_REFERENCE_CAPABILITY_RESOLVER_ONLY`
- `implementation_authorized=true`
- `production_credentials_authorized=false`
- `production_deployment_authorized=false`
- `limited_live_authorized=false`
- `live_trading_authorized=false`

The source repository was clean before the isolated worktree was created. The
shared checkout was not mutated. No reset, stash, force operation, rebase,
history rewrite, checkpoint update, or dependency-lock change was used.

## Authority and scope

CP0023 authorizes only the bounded S1B public-reference capability resolver.
This implementation is not implementation authorization beyond S1B, production
authorization, deployment authorization, credential authorization, limited-live
authorization, or live-trading authorization. The implementation PR must remain
OPEN and UNMERGED after exact-head CI and author-side preflight.

Explicitly deferred and absent: private endpoints, authentication, signing,
credentials, account or position state, orders, leverage, margin, risk or
safety mutation, market streams, ingestion, persistence, caching, quotas,
reconnect/session runtime, deployment, frontend controls, limited-live and
real-money trading.

## Provider authority and ADR

ADR: `adr/HCT-ADR-0046-s1b-mexc-public-reference.md`.

Official MEXC sources consulted on `2026-09-12T20:47:12Z`:

- `https://www.mexc.com/api-docs/futures/integration-guide`
- `https://www.mexc.com/api-docs/futures/market-endpoints/get-contract-info`
- `https://www.mexc.com/announcements/article/futures-api-access-domain-update-17827791532974`
- `https://www.mexc.com/mexc-api`

The fixed allowlist is HTTPS host `api.mexc.com`, base URL
`https://api.mexc.com`, and `GET /api/v1/contract/detail/country`.
Caller-supplied hosts, paths, queries, fragments, ports, credentials and
redirects are not accepted. The transport is one-shot with connect timeout
`2.0s`, read timeout `3.0s`, total deadline `5.0s`, maximum body `262144`
bytes and maximum read chunk `8192` bytes. It performs no retry, session,
reconnect, quota or stream runtime behavior.

The current detailed MEXC reference documents an object-shaped `data` value
and typed `futureType` (`1` perpetual, `2` delivery). The API overview still
mentions the legacy list-shaped `/api/v1/contract/detail` route for supported
pairs; that documentation conflict is not silently merged. The legacy shape is
rejected and remains deferred outside the selected canonical source. The one
permitted bounded diagnostic attempt to that legacy route exceeded the
262144-byte limit before completion; no raw payload or digest was retained.

## Mapping and fail-closed behavior

The adapter maps the official contract-detail shape as follows:

- `symbol` is native mapping metadata; it is not canonical identity.
- `baseCoin`, `quoteCoin`, and `settleCoin` become explicit canonical assets.
- `futureType=1` maps to `PERPETUAL`; `futureType=2` (delivery), missing or
  unknown values fail closed because S1B does not authorize delivery semantics.
- `displayNameEn` is only a presentation consistency check: `PERPETUAL` does
  not require a `SWAP` suffix, while an explicit typed/presentation conflict
  fails closed.
- provider state `0` maps to `ACTIVE`; states `1` through `4` map to
  `INACTIVE`; unknown states fail closed.
- `priceUnit`, `volUnit`, `priceScale`, `volScale`, `minVol`, and `maxVol` are
  validated with exact `Decimal` semantics and increment/bound alignment.
- canonical instrument identity is derived from normalized base, quote,
  settlement and contract type; the native symbol remains mapping evidence.
- exchange description, public reference and contract reference are
  `SUPPORTED`; private state, state change and margin configuration remain
  `UNKNOWN` and cannot be upgraded implicitly.

`contractSize`, leverage, margin, risk, fee, and provider `apiAllowed` fields
remain explicitly deferred because they are not needed for the authorized
public-reference ceiling. Unknown or contradictory material data is rejected.

Fixtures are deterministic and local. No live MEXC call is used by tests or CI.
The public production `load()` has no caller-supplied transport, endpoint or
observation time; private `_from_payload` construction is used only for
deterministic tests. The provider payload is parsed at the adapter boundary and
cannot leak into canonical domain semantics.

## Changed files and justification

- `adr/HCT-ADR-0046-s1b-mexc-public-reference.md` - bounded provider decision,
  official source record, allowlist, mapping and deferred-field proof.
- `apps/backend/src/hct_backend/mexc_reference.py` - fixed public endpoint
  transport, bounded parser, reference mapping and explicit capability state.
- `apps/backend/tests/test_mexc_reference.py` - deterministic success,
  identity, timeout, size, transport, envelope, duplicate, malformed and
  fail-closed coverage.
- `apps/backend/tests/test_scan_s1b_boundaries.py` - scanner regression tests.
- `scripts/scan_s1b_boundaries.py` - AST-aware S1B scope, endpoint, import,
  capability, secret and changed-file boundary scan.
- `.github/workflows/s1b-quality.yml` - PR-only exact-head governance receipt
  with full regression, audit, build and targeted Ruff-format gates.
- `evidence/HCT-IMP-0005-S1B.md` - this bounded evidence handoff.

No checkpoint, frozen requirement, Scope, Decisions Ledger, Work Order,
frontend product surface, backend lockfile, unrelated workflow or dependency
was changed.

## Local verification

Recorded local results for the current candidate before hosted CI:

- Full backend suite with coverage: `125 passed`, `90%` total coverage
  (`1407` statements, `138` missed); the new MEXC module is `93%`.
- Focused S0A/S0B/S0C/S1A/S1B regression matrix: `124 passed`.
- Focused MEXC adapter/parser tests: `38 passed`.
- Contract generation reproducibility: `PASS`; canonical/runtime parity:
  `PASS (10 schemas)`.
- S1B boundary and secret scan: `PASS`.
- Backend Ruff: `PASS`; strict mypy: `PASS`.
- Backend build: `PASS`; Python dependency audit: `PASS / no known
  vulnerabilities`.
- Frontend typecheck: `PASS`; frontend tests: `13 passed`; frontend lint:
  `PASS`; changed generated-contract format: `PASS`; frontend build: `PASS`;
  npm audit: `PASS / 0 vulnerabilities`.
- `git diff --check`: `PASS`.

Correction-specific local verification after the independent H001-H003
findings:

- Focused MEXC adapter and S1B scanner tests: `52 passed`.
- Backend Ruff check: `PASS`; strict mypy: `PASS`.
- Targeted Ruff format check over the four changed Python files: `PASS`.
- Production load signature has no transport/time injection parameters:
  `PASS`.

The legacy S0A
whole-tree lexical validator is not invoked because its frozen marker list
intentionally rejects the authorized MEXC provider vocabulary; its S0A
contract/regression tests remain in the direct regression matrix and the
S1B-aware scanner provides the applicable changed-candidate secret and
capability boundary. The prior UADS non-review gates were recorded PASS in the
sidecar ledger against the pre-correction candidate digest. For this correction,
the existing UADS run is already stopped; `uads verify` refused with
`cannot verify before dispatch or after the run has stopped`. Therefore no new
UADS digest/evidence claim is made here; the correction-specific local gates
above are direct command evidence. The UADS assurance packet still requires distinct non-implementer
`independent-reviewer` and `security-reviewer` sessions; this execution will
not self-approve or replace them.

## Hosted handoff and stop condition

- Correction findings H001-H003: locally addressed; final exact implementation
  head pending commit and push.
- The broad pre-existing repository format check remains out of scope; the
  hosted gate checks the four changed Python files explicitly.
- Exact `s1b-quality` run/check: pending fresh CI for the final head.
- Author-side findings: pending final preflight.
- Independent review: not performed by this execution and not replaced by
  author-side evidence.

After exact-head CI and author-side preflight, the implementation PR remains
OPEN and UNMERGED. This artifact does not authorize merge, checkpoint
promotion, implementation beyond S1B, credentials, deployment, limited-live or
live trading.
