# Checkpoint

Checkpoint ID: `HCT-CP-0005`
Status: `PRODUCT_DISCOVERY_ROUND_03_APPROVED`
Canonical branch: `main`
Last canonical planning merge: `26045a553f8c84b5c88a1eb0ea514ea361ad2422` (`HCT-PLAN-0001-R03`)
Risk class: `HIGH_ASSURANCE`
Functional product planning: `IN_PROGRESS`
Implementation authorization: `NOT_GRANTED`

## Frozen governance foundation
- Hive Plan-style source hierarchy and governance are active.
- GitHub is canonical truth; conversation memory is advisory only.
- Cross-chat resume uses machine-readable workstream checkpoints and Git validation.
- Work Orders use stable HCT IDs across prompts, branches, PRs, evidence, corrections and checkpoints.
- Review verdicts are APPROVED / CORRECTION REQUIRED / BLOCKED.
- Financial/trading, signing/custody, privileged auth, security-critical and irreversible actions default to HIGH_ASSURANCE.

## Approved R01–R02 foundation
- MEXC Futures is the V1 live-trading exchange target; the core remains multi-exchange-ready.
- Current planning module map contains 42 modules.
- Strategy Engine, default strategy catalog, user Strategy Builder, typed nodal strategy graph and Strategy Ecology/Router are first-class requirements.
- Institutional-grade agents and Agentic Copilot are governed by structured evidence and cannot directly bypass deterministic exchange authority.
- HCT Intelligence Brain uses calibrated evidence fusion, abstention/selective decision, uncertainty and expert reliability while remaining subordinate to Safety/Risk/Policy/Execution.
- Temporal Market Memory requires point-in-time correctness, leakage protection, drift controls and governed learning.
- Microstructure/order-flow/liquidity/breadth/cross-market intelligence is an evidence domain requiring incremental-value proof.
- Simulation/Replay/Paper/Shadow/Promotion Laboratory is required for point-in-time proof, realistic frictions and live-parity validation.
- `Signals` is a first-class workspace; Telegram signal rooms are a governed publishing path separate from exchange execution.
- Frontend/backend separation, English-first i18n (`en-US`, `pt-BR`, `es`) and free-first bootstrap infrastructure remain approved planning constraints.

## Approved R03 institutional risk foundation
- Dynamic venue risk tiers, maintenance-margin rates, leverage ceilings, position limits, margin modes and liquidation semantics are runtime state, not permanent constants.
- Every exposure-increasing action requires an immutable/versioned and expiring `RiskSnapshot` containing current and projected post-trade state.
- Risk approval is based on projected post-fill state, including tier transition, MMR, leverage legality and liquidation corridor.
- A deterministic Risk Reservation Ledger reserves risk before order submit and conserves it across pending, partial, cancel-pending and uncertain order states until authoritative resolution.
- Cross margin is treated as shared collateral and requires deterministic contagion analysis across relevant positions and open-order margin.
- Risk budgets span trade, intraday/session, daily, weekly, monthly and account-survival horizons; longer-horizon exhaustion can veto shorter-horizon opportunity capacity.
- Tail/Expected Shortfall-style models and stress surfaces may only tighten deterministic hard limits.
- Operational Margin Reserve is protected from ordinary opportunity sizing.
- Protection Failure Exposure explicitly accounts for gap-through-stop, rejection/cancellation, partial coverage, stale protective quantity, adverse fills and delayed/uncertain protection.
- Every ADD/pyramiding action is a fresh exposure-increasing decision with a new RiskSnapshot/reservation; martingale or loss-recovery escalation is prohibited by default.
- Collateral/stablecoin concentration can reduce Effective Risk Capital through governed stress haircuts.
- Partial/tiered liquidation and ADL/extreme venue mechanics are explicit risk inputs where observable, with conservative UNKNOWN degradation otherwise.
- User risk presets are bounded policy bundles under platform hard ceilings and never override Safety/Risk authority.
- Risk explainability must expose monetary/open/reserved risk, notional, leverage, margin mode, tier/MMR, liquidation corridor, survival/tail state, collateral quality, protection confidence and exact veto/reduction reasons.

## R03 audit
- Final audit artifact: `docs/43-r03-final-audit.md`.
- Verdict: `APPROVED`.
- Acceptance gates passed: 14/14.
- Initial gap audit identified 18 institutional gaps; all are now `RESOLVED_IN_PLANNING`.
- No unresolved CRITICAL/HIGH R03 planning defect remains.
- Decisions Ledger is consolidated through `HCT-DEC-0049`.
- Implementation proof remains deferred to future HIGH_ASSURANCE Work Orders/tests/replay/preflight.

## Completed increments
- `HCT-BOOT-0001` — governance/checkpoint/handoff/prompt contract bootstrap.
- `HCT-PLAN-0001-R01` — market-universe/scanner and product-discovery foundation.
- `HCT-PLAN-0001-R02` — strategy/signal/indicator architecture and classified pre-discovery extensions; audited and merged.
- `HCT-PLAN-0001-R03` — institutional Safety/Risk/leverage/position-sizing discovery; audited and merged via PR #7.

## Current blockers
None for continuing structured planning. Production implementation and live trading remain blocked because planning is incomplete and implementation authorization has not been granted.

## Next necessary action
Continue `HCT-PLAN-0001` with formal `HCT-PLAN-0001-R04`: Execution, OMS and reconciliation discovery.

Use `docs/29-execution-intelligence-oms-reconciliation-and-recovery.md` as pre-discovery input, perform a formal R04-specific gap audit, and preserve the R03 RiskSnapshot/Risk Reservation contracts as upstream authority constraints.

Do not generate an implementation Work Order or authorize live trading yet.

## Resume rule
A new chat must read `docs/00-source-hierarchy.md`, `checkpoints/index.json`, the active workstream `latest.json`, its referenced history checkpoint, this file, Decisions Ledger, Scope, Requirements, module map and relevant round documents; validate Git state against the recorded canonical merge; then resume only from `next_necessary_action`.
