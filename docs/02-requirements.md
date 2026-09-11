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
- Provide a user-selectable Copilot mode capable of autonomous trade lifecycle management within hard user/platform constraints.

## Market and exchange requirements
- Prefer WebSocket for realtime market streams where appropriate and REST for reference/reconciliation/control paths.
- Discover contract capabilities and constraints dynamically where the exchange exposes them.
- Treat exchange state as authoritative for orders, fills, positions and balances; local state must be continuously reconcilable.
- Enforce API/WebSocket usage budgets, throttling, retry budgets, backpressure and circuit breakers so the platform stays within documented exchange limits and avoids abusive behavior/account blocking.
- Account for regional/API capability restrictions and future MEXC API changes as versioned external dependencies.
- Use exchange-native protective order capabilities such as TP/SL, trigger and trailing mechanisms where supported and appropriate, with reconciliation and platform-side safety oversight.

## Trading intelligence requirements
- Provide an extensible indicator and feature engine covering major public/standard technical-analysis indicator families relevant to the product.
- Provide candlestick-pattern and chart/market-structure analysis.
- Allow HCT proprietary indicators/features to be researched, including model-assisted and multi-source features, but treat them as experimental until statistically validated.
- Require proprietary indicators to demonstrate incremental information or decision value rather than merely rename correlated traditional indicators.
- Provide pluggable strategies and an explicit signal pipeline.
- Provide market-regime and cycle/context classification.
- Provide a controlled HCT Intelligence Brain that combines strategy evidence, indicators, patterns, regime, historical memory and risk context before candidate signals proceed.
- Provide RAG/market memory for retrieval of comparable historical contexts, outcomes, failure modes and operational lessons.
- Support controlled offline learning/model lifecycle and optional fine-tuning only when justified by evidence.
- Prevent future-information leakage in research/backtests and require provenance/time-awareness for learned/retrieved data.
- Preserve explainable/versioned decision traces suitable for audit and later learning.

## Agentic Copilot requirements
- Use a supervised multi-agent topology rather than unrestricted direct model access to exchange credentials.
- Candidate agents include market scout, technical analyst, regime/cycle, RAG/memory, strategy, risk proposal, execution planner, position manager, news/event context, adversarial reviewer, supervisor and post-trade reviewer.
- Agents produce structured candidate actions; only deterministic Safety/Risk/Policy/Execution components can authorize exchange actions.
- Support explicit autonomy modes: OFF, ADVISORY, GUARDED_AUTOPILOT and FULL_COPILOT.
- FULL_COPILOT may autonomously open, manage and close positions, including TP/SL, trailing, partial exits and order replacement, only inside the current session operating envelope.
- Every Copilot session must create an immutable policy snapshot containing user limits, strategy/model versions, enabled agents, allowed market universe and relevant operating settings.
- Provide a clear `NO_TRADE` path and fail-safe behavior when confidence, data, exchange state or policy evaluation is insufficient.

## Safety and risk requirements
- Safety & Protection Governor is a first-class independent subsystem and may deny new exposure regardless of strategy or AI output.
- Risk Engine hard limits dominate strategy, RAG and learned-model recommendations.
- AI/RAG/learned models may not autonomously raise hard risk limits, maximum leverage, disable safety controls or self-promote production versions.
- Leverage is subordinate to risk, contract constraints, position sizing and portfolio exposure.
- Provide kill-switch/circuit-breaker behavior and explicit uncertain-state handling.
- User/tenant settings may tighten but cannot exceed global/platform safety ceilings.
- Session policy controls include daily max loss, optional target/open-target mode, risk/trade, concurrent positions, exposure, leverage ceiling, strategy/symbol allowlists, operating hours, volatility/news tolerance, cooldown and emergency controls.
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
- Provide a dedicated Copilot session setup surface and realtime autonomous-operation cockpit.
- When a symbol is selected, provide a realtime chart with optional overlays for strategy behavior, actual executions, simulated signals, indicators/patterns, TP/SL/trailing paths, regime, agent evidence and proprietary HCT indicators.
- Clearly distinguish executed trades from hypothetical or paper/simulated strategy paths.
- Plan dedicated operational views for scanner, symbol intelligence, indicators/patterns, positions/orders, risk/leverage, Safety Governor, RAG/decision traces, backtest/paper trading, model lifecycle, tenancy and system/API health.

## Validation requirements
- Backtest alone is insufficient for strategy/model promotion.
- Research candidates should progress through reproducible backtest, out-of-sample/walk-forward checks, realistic fees/slippage/funding assumptions as applicable, paper/shadow validation and governed promotion.
- Proprietary indicators must include ablation and incremental-value analysis against baselines.
- Profitability is never guaranteed by an indicator/model; evidence must distinguish statistical edge from overfitting.

## Governance requirements already in force
- repository is canonical truth;
- every implementation increment requires a stable Work Order ID;
- every financial/trading increment defaults to HIGH_ASSURANCE unless explicitly proven otherwise;
- evidence is required before approval;
- chat handoff must be reproducible from GitHub without relying on conversation memory;
- prompts sent to external executors must follow the governed prompt contract.
