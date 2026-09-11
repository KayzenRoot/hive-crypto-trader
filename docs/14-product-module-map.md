# Product Module Map

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001`
Risk class: `HIGH_ASSURANCE`

This document records the current planning module map. It is a planning registry, not implementation authorization. Module priority may be refined during discovery, but no module may silently disappear once accepted without an explicit Decision Ledger entry.

## Current module map

1. **Exchange Abstraction & Adapter Framework** — canonical exchange capability interface, normalized domain models, capability matrix and adapter contract for current/future exchanges.
2. **MEXC Futures Adapter** — V1 REST/WebSocket integration, authentication, signing, protocol translation and MEXC-specific capability discovery behind the exchange abstraction.
3. **Market Universe Registry** — dynamic discovery of futures contracts actually exposed and eligible through the active exchange adapter.
4. **Realtime Market Data Engine** — trades, tickers, candles, order book, mark/fair/index price, funding and related feeds.
5. **Market Scanner** — continuous multi-symbol scanning, filtering, ranking and opportunity candidate generation.
6. **Data Quality & Freshness Engine** — stale-feed detection, gaps, sequence errors, timestamp drift, malformed data and recovery.
7. **Indicator & Feature Engine** — canonical indicator library, derived features, multi-timeframe computation and indicator versioning.
8. **Candlestick & Chart Pattern Engine** — recognized candlestick formations and broader price/market structure patterns.
9. **Proprietary Indicator R&D Lab** — HCT-created indicators/features treated as hypotheses until statistically validated.
10. **Strategy Engine** — pluggable long/short strategy definitions, versions and strategy-specific constraints.
11. **User Strategy Builder & Strategy DSL** — visual/structured creation of user-owned strategies using validated declarative rules, indicators, timeframes and exits without arbitrary backend code execution.
12. **Default Strategy Catalog** — approximately 10–15 documented, versioned built-in strategy templates with regime, timeframe, entry/exit, risk and validation metadata.
13. **Signal Engine** — transform strategy evidence into candidate entries/exits/no-trade decisions with confidence and provenance.
14. **Market Regime Engine** — trending/ranging, volatility, liquidity, cycle and abnormal-regime classification.
15. **HCT Intelligence Brain** — reasoning/orchestration layer that combines indicators, patterns, regime, historical memory and risk context before approving a candidate signal for downstream risk evaluation.
16. **RAG & Market Memory** — retrieve relevant historical contexts, prior setups, outcomes, regimes, incidents and lessons without allowing retrieved text to directly place orders.
17. **Learning & Model Lifecycle** — controlled offline learning, feature/model experimentation, optional fine-tuning where justified, evaluation, promotion and rollback.
18. **Risk Engine** — hard risk limits per trade, symbol, strategy, tenant/account, portfolio, drawdown, correlation and market state.
19. **Leverage Engine** — contract-aware leverage constraints and dynamic leverage recommendation subordinate to Risk Engine hard limits.
20. **Position Sizing Engine** — size positions from approved risk budget, stop distance, leverage constraints, liquidity and portfolio exposure.
21. **Safety & Protection Governor** — independent fail-safe layer capable of denying new exposure regardless of strategy/AI output.
22. **Execution Engine** — safe entry, reduce, close, cancel/replace and execution policy handling.
23. **Order Management System (OMS)** — lifecycle of pending, partial, rejected, cancelled, duplicate and uncertain orders.
24. **Position / Account Reconciliation** — continuous local-state versus exchange-state reconciliation and discrepancy handling.
25. **Portfolio Exposure Engine** — aggregate directional, correlated and concentration exposure across open positions.
26. **API Quota, WebSocket & Backpressure Governor** — exchange-aware rate-limit management, subscription planning, throttling, retry budgets, circuit breakers and account-ban prevention.
27. **Caching & Hot-State Layer** — low-latency caches with explicit freshness/TTL rules and no hidden divergence from exchange truth.
28. **Backtest / Replay / Paper Trading / Simulation** — deterministic research path before production promotion, including user-authored strategies.
29. **Multi-Tenant Platform Foundation** — tenant isolation, account boundaries, credentials isolation, quotas, per-tenant policy and future commercialization readiness.
30. **Realtime Trading Cockpit / UI-UX System** — enterprise dashboard, observability, diagnostics, explanations, risk state and the Hive Plan-aligned technological visual language.
31. **Agentic Copilot Orchestrator** — supervised multi-agent orchestration for market analysis, candidate actions, position management and autonomous lifecycle control within hard boundaries.
32. **Session Policy & User Operating Envelope Engine** — immutable session policy snapshots covering daily loss, target mode, risk/trade, leverage ceiling, allowed strategies/symbols, hours, volatility/news behavior, cooldown and emergency controls.
33. **News & Event Intelligence** — approved-source event/calendar intelligence and event-risk classification used as context for Copilot decisions without bypassing deterministic safety/risk rules.
34. **Administrative Control Plane** — owner-only operational cockpit for platform-wide observability, tenant/system administration, incidents, releases and governed privileged controls.
35. **Harness / Capability Isolation & Blackout Engine** — dependency-aware feature flags, scoped freezes, quarantine, degradation, no-new-actions, maintenance and emergency blackout controls with blast-radius analysis and audit evidence.

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
- legal/compliance/regional capability checks;
- exchange capability normalization and portability governance;
- strategy ownership, versioning and compatibility governance.

## V1 exchange scope
Only **MEXC Futures** is enabled for live trading in V1. Binance and other exchanges are future capabilities. Core modules must depend on the exchange abstraction rather than MEXC-specific payloads wherever practical so future adapters can be added without rewriting the trading core.

## Planning rule
The system may analyze a broad market universe, but analysis is not authorization to trade. The evolved decision chain is conceptually:

`Exchange Adapter -> Market Data -> Features/Indicators/Patterns -> Strategy -> Multi-Agent Copilot -> Supervisor -> Candidate Action -> Safety Governor -> Risk Engine -> Session Policy -> Position/Leverage -> Execution -> Exchange Adapter -> Exchange -> Reconciliation`

The Administrative Control Plane and Harness sit orthogonally across the platform and may restrict/degrade capabilities, but cannot silently bypass Safety/Risk rules.

A user-authored strategy is treated as untrusted declarative policy input. It cannot bypass exchange capabilities, Safety Governor, Risk Engine, Session Policy, tenancy/security controls or reconciliation.

Any AI/RAG/learned component must pass explicit promotion gates before receiving production authority. Even in `FULL_COPILOT`, agents cannot override hard risk, platform safety, exchange, security or tenancy controls.
