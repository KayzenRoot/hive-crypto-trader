# HCT-ADR-0042 - S0A Toolchain and Runtime Boundaries

Status: `PROPOSED_FOR_S0A`
Date: `2026-09-12`
Work Order: `HCT-IMP-0001-S0A`
Authorization: `HCT-CP-0015 / IMPLEMENTATION_AUTHORIZED_S0A`

## Decision

S0A uses a small two-root monorepo with an independently buildable FastAPI/Python
backend and React/TypeScript/Vite frontend. The canonical cross-runtime source
is an OpenAPI 3.1 document under `packages/contracts/`; generated Python and
TypeScript contract modules are produced by a deterministic repository script.

The selected versions are pinned as follows:

| Concern | Selection |
|---|---|
| Backend runtime | Python 3.12 (repository-supported runtime) |
| Backend API | FastAPI 0.141.1, Uvicorn 0.52.4, Pydantic 2.13.5 |
| Python manager/lock | uv 0.12.13 with `apps/backend/uv.lock` |
| Backend tests | pytest 9.1.1, pytest-cov 7.1.0 |
| Backend quality | Ruff 0.16.7 and mypy 2.3.1 |
| Frontend runtime | Node.js 24.18.0 (execution/CI runtime line) |
| Frontend | React 19.3.0, React DOM 19.3.0, Vite 8.3.0 |
| Frontend language/tests | TypeScript 5.9.3, Vitest 5.0.0 |
| Frontend quality | ESLint 10.10.0, typescript-eslint 8.70.0, Prettier 3.9.6 |
| React tooling/types | @vitejs/plugin-react 6.1.1, @types/react 19.3.0, @types/react-dom 19.3.0 |
| Frontend manager/lock | npm 11.16.0 with `apps/frontend/package-lock.json` |
| CI | GitHub Actions on a clean Linux checkout with locked installs |

Versions were resolved from the package registries available at execution time
on 2026-09-12 and are recorded here so later upgrades are explicit reviewable
changes. Lockfiles remain the install authority.

## Contract and drift strategy

`packages/contracts/openapi.yaml` is the only normative API/domain contract
source for S0A. `scripts/generate_contracts.py` parses it with standard-library
code and emits deterministic, sorted Python and TypeScript representations.
The generator is intentionally narrow and has no network or exchange behavior.
The contract test regenerates into a temporary directory and compares byte-for-
byte output with committed generated artifacts.

## Boundary and safety rationale

- Frontend and backend have separate package manifests, lockfiles, build
  commands, and source roots, so either can build without the other.
- The backend owns endpoint behavior; the frontend only projects the safe
  health/readiness/version response and has no trading or risk action surface.
- The contract contains only S0A identity, environment, status, error, version,
  and audit/evidence shapes. It contains no exchange URL, credential, order,
  position, balance, risk, or mutation schema.
- Backend defaults bind only to local process settings and expose no production
  or live-capable endpoint. S0A has no exchange client, database, credential,
  deployment, or persistence dependency.
- Environment and typed-ID validation is fail-closed in backend code and is
  represented in the shared contract so frontend parsing cannot silently widen
  the backend authority boundary.

## Windows and Linux

Windows development uses system Python 3.12, uv, npm, and Node.js. CI uses the
same pinned project dependencies on Linux with `uv sync --locked` and `npm ci`.
No OS-specific path or shell behavior is part of the contract generation path.

## Rollback

The slice is persistence-free and has no external side effects. Rollback is a
normal commit revert or branch deletion before merge; no migration, production
state, credential, or deployment rollback is required.

## Consequences

This ADR deliberately leaves SecurityContext enforcement, SecretStore,
exchange/realtime, data persistence, trading state, and later Stage-0 slices to
separate governed Work Orders. Adding any of those capabilities is outside this
decision and requires a new authorization boundary.
