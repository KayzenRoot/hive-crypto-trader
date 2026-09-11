# Product Module Map

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001`
Risk class: `HIGH_ASSURANCE`

This document records the current planning module map. It is a planning registry, not implementation authorization. Module priority may be refined during discovery, but no module may silently disappear once accepted without an explicit Decision Ledger entry.

## Current module map

1. **Exchange Abstraction & Adapter Framework** — canonical exchange capability interface, normalized domain models, capability matrix and adapter contract for current/future exchanges.
2. **MEXC Futures Adapter** — V1 REST/WebSocket integration, authentication, signing, protocol translation and MEXC-specific capability discovery behind the exchange abstraction.
3. **Market Universe Registry** — dynamic discovery of futures contracts actually exposed and eligible through the active exchange adapter.
4. **Realtime Market Data Engine** — trades, tickers, candles, order book, mark/fair/index price, funding and related feeds with canonical event envelopes and event/receive/processing timestamps.
5. **Realtime Stream Processing, Market-State Fabric & Latency Intelligence** — hot-path normalization/fanout, coherent market-state generations, event-time lineage, bounded queues/backpressure, latency budgeting, feature coherency, adaptive compute and realtime integrity gating.
6. **Market Scanner** — continuous multi-symbol scanning, filtering, ranking and opportunity candidate generation.
7. **Data Quality & Freshness Engine** — stale-feed detection, gaps, sequence errors, timestamp drift, malformed data, cross-channel contradictions, local-book coherence and recovery.
8. **Indicator & Feature Engine** — canonical indicator library, derived features, multi-timeframe computation and indicator versioning.
9. **Candlestick & Chart Pattern Engine** — recognized candlestick formations and broader price/market structure patterns.
10. **Proprietary Indicator R&D Lab** — HCT-created indicators/features treated as hypotheses until statistically validated.
11. **Strategy Engine** — pluggable long/short strategy definitions, versions and strategy-specific constraints.
12. **User Strategy Builder & Strategy DSL** — typed nodal/structured creation of user-owned strategies using validated declarative rules, indicators, timeframes and exits without arbitrary backend code execution.
13. **Default Strategy Catalog** — approximately 10–15 documented, versioned built-in strategy templates with regime, timeframe, entry/exit, risk and validation metadata.
14. **Strategy Ecology, Router, Ensemble & Conflict Engine** — context-aware suitability/routing of approved strategies, redundancy-aware ensembles, conflict resolution, strategy decay/drift and governed strategy-level risk-budget recommendations.
15. **Signal Engine** — transform strategy evidence into candidate entries/exits/no-trade decisions with confidence, freshness/half-life and provenance.
16. **Market Regime Engine** — trending/ranging, volatility, liquidity, cycle and abnormal-regime classification.
17. **HCT Intelligence Brain** — calibrated evidence-fusion and selective-decision layer combining indicators, strategies, microstructure, regime, temporal memory, news, agents, uncertainty, evidence independence, historical reliability and execution awareness before producing a candidate action for deterministic downstream safety/risk evaluation.
18. **RAG & Market Memory** — retrieve relevant historical contexts, prior setups, outcomes, regimes, incidents and lessons without allowing retrieved text to directly place orders.
19. **Learning & Model Lifecycle** — controlled offline learning, feature/model experimentation, optional fine-tuning where justified, evaluation, promotion and rollback.
20. **Risk Engine** — hard risk limits per trade, symbol, strategy, tenant/account, portfolio, drawdown, correlation and market state.
21. **Leverage Engine** — contract-aware leverage constraints and dynamic leverage recommendation subordinate to Risk Engine hard limits.
22. **Position Sizing Engine** — size positions from approved risk budget, stop distance, leverage constraints, liquidity and portfolio exposure.
23. **Safety & Protection Governor** — independent fail-safe layer capable of denying new exposure regardless of strategy or AI output.
24. **Execution Intelligence & Feasibility Engine** — converts approved intents into bounded execution plans using slippage budget, liquidity/impact analysis, fill-quality estimates, mutation/repricing policy and execution degradation rules.
25. **Order Management System (OMS)** — event-sourced lifecycle of parent intents, exchange orders, child orders, partial fills, cancel/replace, rejects, expiries and uncertain states with idempotency/duplicate prevention.
26. **Position / Account Reconciliation & State Confidence** — continuous exchange-authoritative reconciliation, unknown-outcome resolution, restart recovery and state-confidence gating for new exposure.
27. **Protective Order Integrity Monitor** — verifies stop/TP/trailing coverage, protective quantities, reduce-only semantics and recovery when required protection is missing/uncertain.
28. **Portfolio Exposure Engine** — aggregate directional, correlated and concentration exposure across open positions.
29. **API Quota, WebSocket & Backpressure Governor** — exchange-aware rate-limit management, adaptive subscription planning, throttling, retry budgets, circuit breakers, load shedding and account-ban prevention.
30. **Caching & Hot-State Layer** — low-latency caches/hot state with explicit freshness leases/TTL/invalidation rules and no hidden divergence from exchange truth.
31. **Simulation, Replay, Paper, Shadow & Promotion Laboratory** — point-in-time-correct event replay, realistic execution/friction simulation, walk-forward/OOS validation, paper/shadow modes, stress testing, champion/challenger comparison, simulation-to-live reality-gap tracking and governed production promotion.
32. **Multi-Tenant Platform Foundation** — tenant isolation, account boundaries, credentials isolation, quotas, per-tenant policy and future commercialization readiness.
33. **Realtime Trading Cockpit / UI-UX System** — enterprise dashboard, observability, diagnostics, explanations, risk state and the Hive Plan-aligned technological visual language.
34. **Agentic Copilot Orchestrator** — supervised multi-agent orchestration for market analysis, candidate actions, position management and autonomous lifecycle control within hard boundaries.
35. **Institutional Agent Workforce, Skills & Tool Gateway** — versioned senior-grade agent specifications, inter-agent evidence protocol, governed web/data/tool access, reusable skill lifecycle, model/tool routing, evaluation and audit.
36. **Session Policy & User Operating Envelope Engine** — immutable session policy snapshots covering daily loss, target mode, risk/trade, leverage ceiling, allowed strategies/symbols, hours, volatility/news behavior, cooldown and emergency controls.
37. **News & Event Intelligence** — approved-source event/calendar/breaking-news intelligence, web research, corroboration and near-term impact classification without bypassing deterministic safety/risk rules.
38. **Administrative Control Plane** — owner-only operational cockpit for platform-wide observability, tenant/system administration, incidents, releases and governed privileged controls.
39. **Harness / Capability Isolation & Blackout Engine** — dependency-aware feature flags, scoped freezes, quarantine, degradation, no-new-actions, maintenance and emergency blackout controls with blast-radius analysis and audit evidence.
40. **Microstructure, Order-Flow, Liquidity, Breadth & Cross-Market Intelligence** — low-latency order-book/trade-flow features, liquidity topology and impact, alternative bars, market breadth, dynamic lead/lag propagation, anomaly detection, realtime feature serving and proprietary HCT microstructure R&D with bootstrap-aware compute budgets.
41. **Temporal Market Memory, Historical Analog & Continual Learning Intelligence** — point-in-time-correct episode/event memory, temporal-causal graph relations, global-plus-recent retrieval, regime-conditioned analog search, no-trade learning, concept-drift localization, catastrophic-forgetting controls, champion/challenger evaluation and governed continual learning.
42. **Signal Publishing, Telegram Rooms & Subscriber Delivery Intelligence** — first-class HCT Signals workspace, versioned signal-room strategies, Telegram channel/group destinations, structured LONG/SHORT signal cards, entry/TP/SL lifecycle, durable outbox/idempotent delivery, publication freshness, subscriber-delay realism, performance analytics and provider-neutral signal publishing.

## Cross-cutting platform capabilities
These concerns span multiple modules and will be planned explicitly rather than buried inside individual components:
- security, secrets and privileged-access management;
- auditability and immutable evidence;
- observability, tracing, metrics and incident diagnostics;
- persistence and schema evolution;
- configuration/versioning;
- testing, CI/CD and release governance;
- performance, resilience and disaster recovery;
- realtime event-time provenance, replay fidelity and market-state-generation coherence;
- bounded queues, adaptive subscription planning, backpressure and deterministic load shedding;
- realtime feature freshness/coherence, point-in-time correctness and incremental computation;
- microstructure/order-flow validation, breadth/lead-lag decay and anomaly explainability;
- temporal event/knowledge timestamps, leakage prevention and immutable ex-ante evidence;
- regime-aware analog retrieval, memory diversity and historical-relevance decay;
- concept-drift detection/localization, catastrophic-forgetting prevention and champion/challenger governance;
- learning from executed trades, rejected candidates and no-trade decisions without selection bias;
- calibrated confidence, abstention/selective-decision quality, evidence independence and expert reliability;
- point-in-time replay, temporal non-interference, simulation/live parity and promotion evidence;
- realistic fees, funding, spread, slippage, latency, market impact, partial-fill and signal-expiry modeling;
- stress/failure injection, reality-gap monitoring, limited-live canary and rollback governance;
- Telegram/signal-room delivery security, idempotency, freshness, lifecycle updates and subscriber-realizability measurement;
- tenancy, billing-readiness and future plan/entitlement controls;
- internationalization/localization with `en-US` canonical and `pt-BR`/`es` supported from implementation start;
- USD-first commercial catalog and locale-aware presentation;
- FinOps/cost controls;
- bootstrap `Feature Value Density` so costly realtime features must justify compute/network/storage consumption;
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

`Exchange Adapter -> Realtime Market Data -> Market-State Fabric/Integrity -> Microstructure/Breadth/Cross-Market Intelligence -> Features/Indicators/Patterns -> Temporal Memory/Analog Intelligence -> Strategy -> Strategy Ecology/Router -> Institutional Agent Workforce -> HCT Intelligence Brain / Copilot Supervisor -> Candidate Action -> Safety Governor -> Risk Engine -> Session Policy -> Position/Leverage -> Execution Intelligence -> OMS -> Exchange Adapter -> Exchange -> Reconciliation/State Confidence -> Protective Integrity`

Signal publication is a separate governed branch:

`Approved Signal Strategy -> Signal Candidate -> Publication Policy/Freshness Gate -> Durable Outbox -> Signal Publisher -> Telegram Channel/Group -> Subscriber`

Telegram publication is informational distribution and never bypasses or becomes exchange execution authority.

The Simulation/Replay/Paper/Shadow/Promotion Laboratory runs orthogonally against the same domain contracts to validate new versions before live promotion.

The Administrative Control Plane and Harness sit orthogonally across the platform and may restrict/degrade capabilities, but cannot silently bypass Safety/Risk rules.

A user-authored strategy is treated as untrusted declarative policy input. It cannot bypass exchange capabilities, Safety Governor, Risk Engine, Session Policy, tenancy/security controls or reconciliation.

Any AI/RAG/learned component must pass explicit promotion gates before receiving production authority. Even in `FULL_COPILOT`, agents cannot override hard risk, platform safety, exchange, security or tenancy controls.
