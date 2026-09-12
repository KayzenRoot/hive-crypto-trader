# Hive Crypto Trader

Governed monorepo for the Hive Crypto Trader project.

> Status: HCT-CP-0015 / IMPLEMENTATION_AUTHORIZED_S0A. The repository contains
> only the bounded, non-trading Stage-0 foundation under Work Order
> `HCT-IMP-0001-S0A`; production credentials, deployment, limited-live and
> real-money trading remain unauthorized.

The repository follows the Hive Plan operating model for checkpoints, chat handoff, Work Orders, prompt delivery, review, evidence, and canonical source control.

## Developer workflow

- Backend: `cd apps/backend && uv sync --locked && uv run pytest`
- Frontend: `cd apps/frontend && npm ci && npm run build`
- Full deterministic checks: `python scripts/validate_s0a.py`

The frontend and backend are independently buildable. The backend is the
authority boundary; the frontend is only a safe health/version projection.
