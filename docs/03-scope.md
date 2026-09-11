# Scope

Status: `DISCOVERY_IN_PROGRESS`
Active increment: `HCT-PLAN-0001`

## Current planning scope
HCT-PLAN-0001 may define and refine the product architecture, module boundaries, safety model, market universe, intelligence/RAG approach, indicator program, realtime/data strategy, multi-tenant readiness, signal-distribution capabilities and UI/UX direction for Hive Crypto Trader.

Accepted planning themes include:
- MEXC Futures as the initial exchange integration target;
- dynamic discovery and scanning of API-eligible futures contracts;
- realtime WebSocket/REST integration with quota/backpressure protection;
- indicators, candlestick/chart patterns and HCT proprietary indicator R&D;
- pluggable strategies, signal generation and market-regime intelligence;
- first-class signal-room publishing, with Telegram as the initial destination, structured entry/TP/SL lifecycle, freshness/idempotency, subscriber-realizability analytics and provider-neutral publisher boundaries;
- RAG/market memory, controlled learning and model lifecycle;
- independent Safety & Protection Governor, hard Risk Engine, leverage and position sizing;
- execution, OMS, reconciliation and portfolio exposure;
- caching/hot state with explicit freshness rules;
- backtest/replay/paper/shadow validation;
- future multi-tenant commercialization readiness;
- enterprise realtime trading cockpit and Hive Plan-aligned technological design language;
- observability, auditability, resilience, security, FinOps and compliance planning.

## Current classification
### NECESSARY for V1 planning
- MEXC Futures adapter and exchange abstraction;
- market universe/scanner and realtime data integrity;
- strategy/signal/indicator architecture;
- Safety, Risk, leverage, position sizing, execution, OMS and reconciliation;
- backtest/replay/paper/shadow promotion path;
- HCT Intelligence Brain and governed memory/learning foundations;
- frontend/backend separation, security and operational controls;
- `Signals` workspace and Telegram signal publishing as a separate non-execution product path;
- bootstrap/free-first infrastructure with safe migration path.

### IMPORTANT
- advanced proprietary microstructure technologies beyond the minimum validated V1 set;
- advanced cross-market/lead-lag research;
- deeper agent/model routing optimization;
- richer subscriber-realizability and signal-room analytics after the core delivery path is stable.

### FUTURE
- live trading on exchanges other than MEXC Futures;
- additional signal-distribution destinations beyond Telegram;
- dedicated large-scale streaming/vector/graph infrastructure before measured need;
- advanced marketplace/white-label commercialization features unless separately promoted.

## Explicitly not authorized yet
- production trading;
- live API credentials or secrets in the repository;
- real-money order execution;
- final strategy formulas or production parameter values;
- autonomous self-modifying production strategy/risk logic;
- final leverage limits;
- final commercial pricing/plans;
- production deployment topology;
- paid signal-room commercialization before legal/commercial/regional review;
- any implementation Work Order.

## Scope control
New ideas may be added during discovery, but each must be classified as NECESSARY, IMPORTANT, FUTURE or OUT OF SCOPE before implementation planning. No idea becomes production scope merely because it was discussed.
