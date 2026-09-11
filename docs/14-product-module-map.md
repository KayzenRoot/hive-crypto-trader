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
11. **User Strategy Builder & Strategy DSL** — typed nodal/structured creation of user-owned strategies using validated declarative rules, indicators, timeframes and exits without arbitrary backend code execution.
12. **Default Strategy Catalog** — approximately 10–15 documented, versioned built-in strategy templates with regime, timeframe, entry/exit, risk and validation metadata.
13. **Strategy Ecology, Router, Ensemble & Conflict Engine** — context-aware suitability/routing of approved strategies, redundancy-aware ensembles, conflict resolution, strategy decay/drift and governed strategy-level risk-budget recommendations.
14. **Signal Engine** — transform strategy evidence into candidate entries/exits/no-trade decisions with confidence and provenance.
15. **Market Regime Engine** — trending/ranging, volatility, liquidity, cycle and abnormal-regime classification.
16. **HCT Intelligence Brain** — reasoning/orchestration layer that combines indicators, patterns, regime, historical memory and risk context before approving a candidate signal for downstream risk evaluation.
17. **RAG & Market Memory** — retrieve relevant historical contexts, prior setups, outcomes, regimes, incidents and lessons without allowing retrieved text to directly place orders.
18. **Learning & Model Lifecycle** — controlled offline learning, feature/model experimentation, optional fine-tuning where justified, evaluation, promotion and rollback.
19. **Risk Engine** — hard risk limits per trade, symbol, strategy, tenant/account, portfolio, drawdown, correlation and market state.
20. **Leverage Engine** — contract-aware leverage constraints and dynamic leverage recommendation subordinate to Risk Engine hard limits.
21. **Position Sizing Engine** — size positions from approved risk budget, stop distance, leverage constraints, liquidity and portfolio exposure.
22. **Safety & Protection Governor** — independent fail-safe layer capable of denying new exposure regardless of strategy/AI output.
23. **Execution Intelligence & Feasibility Engine** — converts approved intents into bounded execution plans using slippage budget, liquidity/impact analysis, fill-quality estimates, mutation/repricing policy and execution degradation rules.
24. **Order Management System (OMS)** — event-sourced lifecycle of parent intents, exchange orders, child orders, partial fills, cancel/replace, rejects, expiries and uncertain states with idempotency/duplicate prevention.
25. **Position / Account Reconciliation & State Confidence** — continuous exchange-authoritative reconciliation, unknown-outcome resolution, restart recovery and state-confidence gating for new exposure.
26. **Protective Order Integrity Monitor** — verifies stop/TP/trailing coverage, protective quantities, reduce-only semantics and recovery when required protection is missing/uncertain.
27. **Portfolio Exposure Engine** — aggregate directional, correlated and concentration exposure across open positions.
28. **API Quota, WebSocket & Backpressure Governor** — exchange-aware rate-limit management, subscription planning, throttling, retry budgets, circuit breakers and account-ban prevention.
29. **Caching & Hot-State Layer** — low-latency caches with explicit freshness/TTL rules and no hidden divergence from exchange truth.
30. **Backtest / Replay / Paper Trading / Simulation** — deterministic research path before production promotion, including user-authored strategies and execution shadow simulation.
31. **Multi-Tenant Platform Foundation** — tenant isolation, account boundaries, credentials isolation, quotas, per-tenant policy and future commercialization readiness.
32. **Realtime Trading Cockpit / UI-UX System** — enterprise dashboard, observability, diagnostics, explanations, risk state and the Hive Plan-aligned technological visual language.
33. **Agentic Copilot Orchestrator** — supervised multi-agent orchestration for market analysis, candidate actions, position management and autonomous lifecycle control within hard boundaries.
34. **Institutional Agent Workforce, Skills & Tool Gateway** — versioned senior-grade agent specifications, inter-agent evidence protocol, governed web/data/tool access, reusable skill lifecycle, model/tool routing, evaluation and audit.
35. **Session Policy & User Operating Envelope Engine** — immutable session policy snapshots covering daily loss, target mode, risk/trade, leverage ceiling, allowed strategies/symbols, hours, volatility/news behavior, cooldown and emergency controls.
36. **News & Event Intelligence** — approved-source event/calendar/breaking-news intelligence, web research, corroboration and near-term impact classification without bypassing deterministic safety/risk rules.
37. **Administrative Control Plane** — owner-only operational cockpit for platform-wide observability, tenant/system administration, incidents, releases and governed privileged controls.
38. **Harness / Capability Isolation & Blackout Engine** — dependency-aware feature flags, scoped freezes, quarantine, degradation, no-new-actions, maintenance and emergency blackout controls with blast-radius analysis and audit evidence.

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
- internationalization/localization with `en-US` canonical and `pt-BR`/`es` supported from implementation start;
- USD-first commercial catalog and locale-aware presentation;
- FinOps/cost controls;
- legal/compliance/regional capability checks;
- exchange capability normalization and portability governance;
- strategy ownership, versioning and compatibility governance;
- agent specification, tool-permission, skill-promotion and model-routing governance;
- web/news source provenance, corroboration and temporal-validity governance;
- canonical order-intent, execution, idempotency and unknown-outcome governance;
- exchange-authoritative reconciliation, protection verification and recovery governance.

## V1 exchange scope
Only **MEXC Futures** is enabled for live trading in V1. Binance and other exchanges are future capabilities. Core modules must depend on the exchange abstraction rather than MEXC-specific payloads wherever practical so future adapters can be added without rewriting the trading core.

## Planning rule
The system may analyze a broad market universe, but analysis is not authorization to trade. The evolved decision chain is conceptually:

`Exchange Adapter -> Market Data -> Features/Indicators/Patterns -> Strategy -> Strategy Ecology/Router -> Institutional Agent Workforce -> Copilot Supervisor -> Candidate Action -> Safety Governor -> Risk Engine -> Session Policy -> Position/Leverage -> Execution Intelligence -> OMS -> Exchange Adapter -> Exchange -> Reconciliation/State Confidence -> Protective Integrity`

The Administrative Control Plane and Harness sit orthogonally across the platform and may restrict/degrade capabilities, but cannot silently bypass Safety/Risk rules.

A user-authored strategy is treated as untrusted declarative policy input. It cannot bypass exchange capabilities, Safety Governor, Risk Engine, Session Policy, tenancy/security controls or reconciliation.

Any AI/RAG/learned component must pass explicit promotion gates before receiving production authority. Even in `FULL_COPILOT`, agents cannot override hard risk, platform safety, exchange, security or tenancy controls.
