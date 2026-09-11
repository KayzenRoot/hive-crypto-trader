# Scope

Status: `DISCOVERY_IN_PROGRESS`
Active increment: `HCT-PLAN-0001`

## Current planning scope
HCT-PLAN-0001 may define and refine the product architecture, module boundaries, safety model, market universe, intelligence/RAG approach, indicator program, realtime/data strategy, multi-tenant readiness, signal-distribution capabilities and UI/UX direction for Hive Crypto Trader.

Accepted planning themes include:
- MEXC Futures as the initial exchange integration target;
- dynamic discovery and scanning of API-eligible futures contracts;
- realtime WebSocket/REST integration with quota/backpressure protection;
- trusted realtime state using feed generations, synchronization proof, data-quality authority, freshness/coherency contracts and end-to-end decision-age control;
- indicators, candlestick/chart patterns and HCT proprietary indicator R&D;
- pluggable strategies, signal generation and market-regime intelligence;
- first-class signal-room publishing, with Telegram as the initial destination, structured entry/TP/SL lifecycle, freshness/idempotency, subscriber-realizability analytics and provider-neutral publisher boundaries;
- RAG/market memory, controlled learning and model lifecycle;
- canonical intelligence evidence, deterministic evidence admissibility, calibration, selective abstention, point-in-time Temporal Market Memory and governed continual-learning authority;
- bounded institutional-agent deliberation with explicit authority ceilings and no direct exchange authority;
- independent Safety & Protection Governor, hard Risk Engine, leverage and position sizing;
- dynamic exchange risk tiers, maintenance margin, position limits, margin modes and liquidation semantics;
- immutable/expiring post-trade RiskSnapshots and deterministic pre-submit Risk Reservation Ledger;
- cross-margin contagion, portfolio/common-factor/tail risk and multi-horizon survival budgets;
- protected Operational Margin Reserve, protection-failure exposure and risk-approval revalidation;
- governed ADD/pyramiding controls, collateral/stablecoin stress, Effective Risk Capital and venue-extreme mechanics such as partial liquidation/ADL where observable;
- execution command identity, authorization leases, idempotency and mutation lineage;
- OMS event sourcing, fill conservation, duplicate/late/out-of-order handling and unknown-outcome recovery;
- cancel/replace race resolution and position-mode-aware REDUCE/CLOSE correctness;
- protective-order dependency tracking, coverage verification and protection-establishment latency;
- reconciliation watermarks, conflict ledger, state confidence and restart/failover recovery proof;
- signed-command clock health, quota-priority protection and versioned execution capability/fee/schema dependencies;
- portfolio exposure and continuous open-position state reconciliation;
- caching/hot state with explicit freshness rules;
- backtest/replay/paper/shadow validation;
- multi-tenant commercialization-ready foundations with tenant/account/credential isolation;
- enterprise realtime trading cockpit with authoritative-state/freshness/safety communication;
- admin/Harness capability isolation and incident-aware operational controls;
- observability, append-only audit, trading-aware SLOs/incidents, resilience, security, FinOps and compliance-readiness planning.

## Current classification
Detailed per-module classification is canonical in `docs/92-r11-v1-module-classification-and-integration-hardening.md` for R11/R12 handoff.

### NECESSARY for V1 planning
- MEXC Futures adapter and exchange abstraction;
- market universe/scanner and realtime data integrity;
- strategy/signal/indicator architecture;
- Safety, Risk, leverage, position sizing, execution, OMS and reconciliation;
- dynamic exchange/margin risk-state resolution, post-trade risk preview, risk reservation and survival controls;
- deterministic execution identity/idempotency, fill conservation and unknown-outcome reconciliation;
- position-mode-safe reduction/closing, protection integrity and restart/failover recovery;
- backtest/replay/paper/shadow promotion path;
- HCT Intelligence Brain, canonical evidence/admissibility, point-in-time memory and governed learning foundations;
- multi-tenant identity/account isolation and secrets/security foundations;
- frontend/backend separation plus realtime cockpit safety/state-integrity contracts;
- owner Admin Control Plane and Harness/capability-isolation foundations;
- minimum audit/observability/incident-response evidence required for safe operation and recovery;
- `Signals` workspace and Telegram signal publishing as a separate non-execution product path;
- bootstrap/free-first infrastructure with safe migration path.

### IMPORTANT
- advanced proprietary microstructure technologies beyond the minimum validated V1 set;
- advanced cross-market/lead-lag/anomaly research;
- deeper agent/model routing optimization and full institutional-agent workforce depth beyond the V1 minimum set;
- advanced continual-learning optimization beyond the V1 point-in-time memory/analog foundation;
- richer subscriber-realizability and signal-room analytics after the core delivery path is stable;
- advanced execution-tactic optimization beyond the minimum validated MEXC capability set.

### FUTURE
- live trading on exchanges other than MEXC Futures;
- additional signal-distribution destinations beyond Telegram;
- multi-venue smart order routing;
- dedicated large-scale streaming/vector/graph infrastructure before measured need;
- advanced marketplace/white-label commercialization features unless separately promoted;
- unrestricted mobile live-trading authority;
- live availability in regions/accounts not explicitly eligible under legal/exchange/KYC/API/security policy.

## Explicitly not authorized yet
- production trading;
- live API credentials or secrets in the repository;
- real-money order execution;
- final strategy formulas or production parameter values;
- autonomous self-modifying production strategy/risk/execution/intelligence logic;
- final leverage limits;
- final commercial pricing/plans;
- production deployment topology;
- paid signal-room commercialization before legal/commercial/regional review;
- any implementation Work Order.

## Scope control
New ideas may be added during discovery, but each must be classified as NECESSARY, IMPORTANT, FUTURE or OUT OF SCOPE before implementation planning. No idea becomes production scope merely because it was discussed.

R11 adds an explicit rule: architecture readiness and live activation are separate. A module may be `V1_CORE` while its highest-risk live capability remains disabled until R07 promotion, production authorization and applicable security/eligibility gates pass.

All HCT-PLAN-0001 round approvals are planning approvals only and do not authorize implementation, production credentials, production deployment or live trading.
