# Product Module Map

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001`
Risk class: `HIGH_ASSURANCE`

This document records the current planning module map. It is a planning registry, not implementation authorization. Module priority may be refined during discovery, but no module may silently disappear once accepted without an explicit Decision Ledger entry.

## Current module map

1. **MEXC Integration Layer** — REST/WebSocket integration, authentication, signing, protocol normalization and capability discovery.
2. **Market Universe Registry** — dynamic discovery of futures contracts actually exposed and eligible through the MEXC API.
3. **Realtime Market Data Engine** — trades, tickers, candles, order book, mark/fair/index price, funding and related feeds.
4. **Market Scanner** — continuous multi-symbol scanning, filtering, ranking and opportunity candidate generation.
5. **Data Quality & Freshness Engine** — stale-feed detection, gaps, sequence errors, timestamp drift, malformed data and recovery.
6. **Indicator & Feature Engine** — canonical indicator library, derived features, multi-timeframe computation and indicator versioning.
7. **Candlestick & Chart Pattern Engine** — recognized candlestick formations and broader price/market structure patterns.
8. **Proprietary Indicator R&D Lab** — HCT-created indicators/features treated as hypotheses until statistically validated.
9. **Strategy Engine** — pluggable long/short strategy definitions, versions and strategy-specific constraints.
10. **Signal Engine** — transform strategy evidence into candidate entries/exits/no-trade decisions with confidence and provenance.
11. **Market Regime Engine** — trending/ranging, volatility, liquidity, cycle and abnormal-regime classification.
12. **HCT Intelligence Brain** — reasoning/orchestration layer that combines indicators, patterns, regime, historical memory and risk context before approving a candidate signal for downstream risk evaluation.
13. **RAG & Market Memory** — retrieve relevant historical contexts, prior setups, outcomes, regimes, incidents and lessons without allowing retrieved text to directly place orders.
14. **Learning & Model Lifecycle** — controlled offline learning, feature/model experimentation, optional fine-tuning where justified, evaluation, promotion and rollback.
15. **Risk Engine** — hard risk limits per trade, symbol, strategy, tenant/account, portfolio, drawdown, correlation and market state.
16. **Leverage Engine** — contract-aware leverage constraints and dynamic leverage recommendation subordinate to Risk Engine hard limits.
17. **Position Sizing Engine** — size positions from approved risk budget, stop distance, leverage constraints, liquidity and portfolio exposure.
18. **Safety & Protection Governor** — independent fail-safe layer capable of denying new exposure regardless of strategy/AI output.
19. **Execution Engine** — safe entry, reduce, close, cancel/replace and execution policy handling.
20. **Order Management System (OMS)** — lifecycle of pending, partial, rejected, cancelled, duplicate and uncertain orders.
21. **Position / Account Reconciliation** — continuous local-state versus exchange-state reconciliation and discrepancy handling.
22. **Portfolio Exposure Engine** — aggregate directional, correlated and concentration exposure across open positions.
23. **API Quota, WebSocket & Backpressure Governor** — rate-limit awareness, subscription planning, throttling, retry budgets, circuit breakers and account-ban prevention.
24. **Caching & Hot-State Layer** — low-latency caches with explicit freshness/TTL rules and no hidden divergence from exchange truth.
25. **Backtest / Replay / Paper Trading / Simulation** — deterministic research path before production promotion.
26. **Multi-Tenant Platform Foundation** — tenant isolation, account boundaries, credentials isolation, quotas, per-tenant policy and future commercialization readiness.
27. **Realtime Trading Cockpit / UI-UX System** — enterprise dashboard, observability, diagnostics, explanations, risk state and the Hive Plan-aligned technological visual language.

## Cross-cutting platform capabilities
These concerns span multiple modules and will be planned explicitly rather than buried inside individual components:
- security, secrets and privileged-access management;
- auditability and immutable evidence;
- observability, tracing, metrics and incident diagnostics;
- persistence and schema evolution;
- configuration/versioning;
- testing, CI/CD and release governance;
- performance, resilience and disaster recovery;
- tenancy, billing-readiness and future plan/entitlement controls;
- FinOps/cost controls;
- legal/compliance/regional capability checks.

## Planning rule
The system may analyze a broad market universe, but analysis is not authorization to trade. The decision chain remains conceptually:

`Market Data -> Features/Indicators/Patterns -> Strategy -> Signal -> Intelligence Brain -> Safety Governor -> Risk Engine -> Position/Leverage -> Execution -> Reconciliation`

Any AI/RAG/learned component is advisory or decision-support only until it passes explicit promotion gates. It may never override hard risk, security, exchange or tenancy controls.
