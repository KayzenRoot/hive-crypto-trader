# Requirements

Status: `DISCOVERY_IN_PROGRESS`
Active planning increment: `HCT-PLAN-0001`
Risk class: `HIGH_ASSURANCE`

Product requirements are being discovered and refined. The following requirements are currently accepted as planning inputs; they are not implementation authorization.

## Product intent
- Build an automated futures-trading platform initially integrated with MEXC Futures.
- Analyze the dynamically eligible futures universe exposed by the exchange API rather than rely on a hard-coded symbol list.
- Support long and short workflows, leverage-aware operation and realtime decision/execution paths.
- Architect for eventual commercial multi-tenant use even if commercialization and paid plans are deferred beyond the first release.

## Market and exchange requirements
- Prefer WebSocket for realtime market streams where appropriate and REST for reference/reconciliation/control paths.
- Discover contract capabilities and constraints dynamically where the exchange exposes them.
- Treat exchange state as authoritative for orders, fills, positions and balances; local state must be continuously reconcilable.
- Enforce API/WebSocket usage budgets, throttling, retry budgets, backpressure and circuit breakers so the platform stays within documented exchange limits and avoids abusive behavior/account blocking.
- Account for regional/API capability restrictions and future MEXC API changes as versioned external dependencies.

## Trading intelligence requirements
- Provide an extensible indicator and feature engine covering major public/standard technical-analysis indicator families relevant to the product.
- Provide candlestick-pattern and chart/market-structure analysis.
- Allow HCT proprietary indicators/features to be researched, but treat them as experimental until statistically validated.
- Provide pluggable strategies and an explicit signal pipeline.
- Provide market-regime and cycle/context classification.
- Provide a controlled HCT Intelligence Brain that combines strategy evidence, indicators, patterns, regime, historical memory and risk context before candidate signals proceed.
- Provide RAG/market memory for retrieval of comparable historical contexts, outcomes, failure modes and operational lessons.
- Support controlled offline learning/model lifecycle and optional fine-tuning only when justified by evidence.
- Prevent future-information leakage in research/backtests and require provenance/time-awareness for learned/retrieved data.
- Preserve explainable/versioned decision traces suitable for audit and later learning.

## Safety and risk requirements
- Safety & Protection Governor is a first-class independent subsystem and may deny new exposure regardless of strategy or AI output.
- Risk Engine hard limits dominate strategy, RAG and learned-model recommendations.
- AI/RAG/learned models may not autonomously raise hard risk limits, maximum leverage, disable safety controls or self-promote production versions.
- Leverage is subordinate to risk, contract constraints, position sizing and portfolio exposure.
- Provide kill-switch/circuit-breaker behavior and explicit uncertain-state handling.
- No HIGH/CRITICAL known defect may be carried forward into a higher-assurance stage.

## Realtime and performance requirements
- Realtime market ingestion, signal state, risk state, order/position reconciliation and operational health must be observable.
- Provide cache/hot-state capabilities with explicit freshness/TTL/invalidation rules; cache must never silently become exchange truth.
- Support graceful degradation when data is stale, WebSocket sessions fail, API quotas are constrained or reconciliation becomes uncertain.

## Multi-tenant requirements
- Future tenant isolation must be anticipated in identity, credentials, data ownership, quotas, policies, strategy/model access and audit boundaries.
- Exchange API secrets/private credentials must be isolated per tenant/account and never appear in logs, prompts, RAG corpora or shared caches.
- Pricing plans/entitlements are intentionally deferred and will be planned separately.

## UI/UX requirements
- Establish a technological premium enterprise trading-cockpit design language aligned with the visual DNA of Hive Plan while remaining product-specific.
- Realtime risk, degraded-state and exchange-uncertainty signals must have visual priority over decorative/3D effects.
- Plan dedicated operational views for scanner, symbol intelligence, indicators/patterns, positions/orders, risk/leverage, Safety Governor, RAG/decision traces, backtest/paper trading, model lifecycle, tenancy and system/API health.

## Validation requirements
- Backtest alone is insufficient for strategy/model promotion.
- Research candidates should progress through reproducible backtest, out-of-sample/walk-forward checks, realistic fees/slippage/funding assumptions as applicable, paper/shadow validation and governed promotion.
- Profitability is never guaranteed by an indicator/model; evidence must distinguish statistical edge from overfitting.

## Governance requirements already in force
- repository is canonical truth;
- every implementation increment requires a stable Work Order ID;
- every financial/trading increment defaults to HIGH_ASSURANCE unless explicitly proven otherwise;
- evidence is required before approval;
- chat handoff must be reproducible from GitHub without relying on conversation memory;
- prompts sent to external executors must follow the governed prompt contract.
