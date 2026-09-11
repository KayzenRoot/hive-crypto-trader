# Checkpoint

Checkpoint ID: `HCT-CP-0004`
Status: `PRODUCT_DISCOVERY_ROUND_02_APPROVED`
Canonical branch: `main`
Last canonical planning merge: `1bcab0302c849b6711a5d5100a181ee0943099a5` (`HCT-PLAN-0001-R02`)
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

## Approved R01–R02 planning foundation
- MEXC Futures is the only live-trading exchange target for V1; the core is multi-exchange-ready through provider-neutral adapter contracts.
- Current planning module map contains 42 modules.
- Strategy Engine, approximately 10–15 default strategy families, user Strategy Builder and typed nodal strategy graph are first-class requirements.
- Strategy Ecology/Router, multi-timeframe evidence, redundancy/conflict handling and explicit `WAIT` / `NO_TRADE` paths are required.
- Institutional-grade agents and Agentic Copilot are governed by structured evidence and cannot directly bypass deterministic exchange authority.
- HCT Intelligence Brain uses calibrated evidence fusion, abstention/selective decision, uncertainty and expert reliability while remaining subordinate to Safety/Risk/Policy/Execution.
- Temporal Market Memory distinguishes event time from knowledge time and requires point-in-time correctness, leakage protection, drift controls and governed learning.
- Microstructure/order-flow/liquidity/breadth/cross-market intelligence is an evidence domain and must prove incremental value before promotion.
- Simulation/Replay/Paper/Shadow/Promotion Laboratory is required for point-in-time proof, realistic frictions, champion/challenger evaluation and live-parity validation.
- Safety & Protection Governor is independent and authoritative over strategy/AI output.
- Risk Engine hard limits, leverage and position sizing remain deterministic downstream authorities.
- Execution Intelligence, OMS, reconciliation, protective integrity and unknown-outcome recovery are required planning domains.
- Realtime market-state integrity, adaptive subscriptions, quota/backpressure protection, coherent feature state and deterministic load shedding are required.
- `Signals` is a first-class workspace. Telegram signal rooms are required as a separate governed publishing path, supporting structured LONG/SHORT signals, entry/TP/SL lifecycle, durable/idempotent publication, freshness gating and subscriber-realizability analytics.
- Telegram publishing is informational distribution and never becomes exchange execution authority.
- Frontend and backend are independently deployable surfaces; the frontend is an untrusted client and holds no trading secrets/authoritative risk logic.
- English is canonical (`en-US`) with `pt-BR` and `es` supported from implementation start; commercial catalog starts in USD.
- Bootstrap infrastructure is free-first: approximately USD 0/month target, narrowly justified soft exception up to about USD 3–4/month for indispensable persistent compute, with formal infrastructure review near 10–12 active paying customers or earlier technical/safety trigger.

## R02 audit
- Audit artifact: `docs/38-r02-planning-audit-and-closure.md`.
- Verdict: `APPROVED`.
- R02 scope drift was classified explicitly. R03–R07 pre-discovery artifacts are reusable inputs, not silently completed future rounds.
- Decisions Ledger is consolidated through `HCT-DEC-0041`.
- Historical transient direct-to-main create/delete operations were documented as governance/process debt; no surviving product-content defect remained.
- No implementation CI workflows existed at R02 closure; CI/check gates remain mandatory before implementation code promotion.

## Completed increments
- `HCT-BOOT-0001` — governance/checkpoint/handoff/prompt contract bootstrap.
- `HCT-PLAN-0001-R01` — market-universe/scanner and product-discovery foundation.
- `HCT-PLAN-0001-R02` — strategy, signal and indicator architecture, plus classified pre-discovery inputs and Telegram signal-room planning; audited and merged via PR #5.

## Current blockers
None for continuing structured planning. Production implementation and live trading remain blocked because planning is incomplete and implementation authorization has not been granted.

## Next necessary action
Continue `HCT-PLAN-0001` with formal `HCT-PLAN-0001-R03`: Safety, Risk, leverage and position-sizing discovery.

Use `docs/28-risk-intelligence-position-sizing-leverage-and-equity-guard.md` as pre-discovery input, but perform a formal R03 gap audit rather than treating the pre-work as already promoted.

Do not generate an implementation Work Order or authorize live trading yet.

## Resume rule
A new chat must read `docs/00-source-hierarchy.md`, `checkpoints/index.json`, the active workstream `latest.json`, its referenced history checkpoint, this file, Decisions Ledger, Scope, Requirements, module map and relevant round documents; validate Git state against the recorded canonical merge; then resume only from `next_necessary_action`.
