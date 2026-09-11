# Scope

Status: `DISCOVERY_IN_PROGRESS`
Active increment: `HCT-PLAN-0001`

## Current planning scope
HCT-PLAN-0001 may define and refine the product architecture, module boundaries, safety model, market universe, intelligence/RAG approach, indicator program, realtime/data strategy, multi-tenant readiness and UI/UX direction for Hive Crypto Trader.

Accepted planning themes include:
- MEXC Futures as the initial exchange integration target;
- dynamic discovery and scanning of API-eligible futures contracts;
- realtime WebSocket/REST integration with quota/backpressure protection;
- indicators, candlestick/chart patterns and HCT proprietary indicator R&D;
- pluggable strategies, signal generation and market-regime intelligence;
- RAG/market memory, controlled learning and model lifecycle;
- independent Safety & Protection Governor, hard Risk Engine, leverage and position sizing;
- execution, OMS, reconciliation and portfolio exposure;
- caching/hot state with explicit freshness rules;
- backtest/replay/paper/shadow validation;
- future multi-tenant commercialization readiness;
- enterprise realtime trading cockpit and Hive Plan-aligned technological design language;
- observability, auditability, resilience, security, FinOps and compliance planning.

## Explicitly not authorized yet
- production trading;
- live API credentials or secrets in the repository;
- real-money order execution;
- final strategy formulas or production parameter values;
- autonomous self-modifying production strategy/risk logic;
- final leverage limits;
- final commercial pricing/plans;
- production deployment topology;
- any implementation Work Order.

## Scope control
New ideas may be added during discovery, but each must be classified as NECESSARY, IMPORTANT, FUTURE or OUT OF SCOPE before implementation planning. No idea becomes production scope merely because it was discussed.
