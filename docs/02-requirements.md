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
- Provide both curated built-in strategies and a user-facing strategy builder for creating private custom strategies.
- Provide a first-class `Signals` workspace capable of publishing governed strategy-generated LONG/SHORT signals to Telegram channels/groups as a product capability separate from autonomous exchange execution.
- Keep V1 live trading limited to MEXC Futures while preserving an exchange-adapter architecture for future Binance and additional venue integrations.
- Build HCT as an English-first commercial product targeting the US/international English-speaking market, while supporting first-class Portuguese (Brazil) and Spanish localization from implementation start.
- Use USD as the initial canonical commercial plan/catalog currency.
- Build the agent layer as a coordinated institutional-grade workforce whose canonical specifications are authored and versioned in this repository before implementation.

## Internationalization and localization requirements
- Canonical/default product locale is `en-US`.
- Initial supported UI locales are `en-US`, `pt-BR` and `es`, with architecture ready for additional regional locales later.
- Source code identifiers, APIs, domain/database fields, events, telemetry keys, configuration keys, Strategy DSL/node type identifiers and canonical technical documentation use English.
- User-facing strings must use localization resources/keys rather than being hard-coded where localization is appropriate.
- New user-facing features must add/queue English, Portuguese and Spanish copy during the same development workflow rather than deferring translation to a late retrofit.
- Machine semantics must be locale-independent: changing UI language must not alter strategy logic, Safety/Risk decisions, order semantics, numeric calculations or audit identity.
- Locale-aware presentation must cover dates/times, time zones, numbers, percentages, currencies, pluralization, validation/error text, chart labels/tooltips and accessibility labels.
- Strategy graphs and saved strategies must use stable canonical identifiers so the same graph can be displayed in any supported language without semantic changes.
- Financial/risk/security/autonomy/emergency-control translations require stricter review and automated coverage checks.
- Backend-generated user-facing messages and notifications should expose structured codes/templates suitable for localization rather than uncontrolled English-only prose.
- Initial plan/catalog pricing is denominated in USD. Localization of a price does not imply automatic FX conversion or regional pricing; those require explicit future commercial policy.
- CI/testing should cover missing translation keys, fallback behavior, interpolation integrity, long-string layouts and locale switching without state/semantic mutation.

## Market and exchange requirements
- Prefer WebSocket for realtime market streams where appropriate and REST for reference/reconciliation/control paths.
- Discover contract capabilities and constraints dynamically where the exchange exposes them.
- Treat exchange state as authoritative for orders, fills, positions and balances; local state must be continuously reconcilable.
- Enforce API/WebSocket usage budgets, throttling, retry budgets, backpressure and circuit breakers so the platform stays within documented exchange limits and avoids abusive behavior/account blocking.
- Account for regional/API capability restrictions and future exchange API changes as versioned external dependencies.
- Use exchange-native protective order capabilities such as TP/SL, trigger and trailing mechanisms where supported and appropriate, with reconciliation and platform-side safety oversight.
- Core trading modules must depend on HCT-owned canonical exchange/domain interfaces wherever practical rather than directly on MEXC payloads.
- MEXC must be implemented as the first concrete exchange adapter; future exchanges require their own capability mapping, signing/authentication, quota, reconciliation and HIGH_ASSURANCE promotion.
- Maintain an explicit exchange capability matrix so unsupported venue functionality is rejected or degraded visibly rather than silently emulated.

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

## Strategy requirements
- Ship approximately 10–15 documented built-in strategy templates/families for the initial product experience.
- Every built-in strategy must explain intended regime, direction, required indicators/features, timeframe template, entry, invalidation/exit, protective-order behavior, limitations/failure modes and validation status.
- Provide a visual user Strategy Builder backed by the same canonical versioned Strategy Definition/DSL used by runtime, backtest and paper trading.
- User strategy conditions may combine allowed indicators, proprietary HCT indicators exposed to the user, patterns, price structure, volume, volatility, liquidity, derivatives context, regime, multi-timeframe logic, news/event filters where supported, time/session filters and Boolean/grouped conditions.
- User strategies may define long/short/both direction, entry, confirmation, invalidation, exit, stop-loss, take-profit, trailing, partial exits and other supported position-management rules.
- V1 custom strategy execution must be declarative/sandboxed; users may not upload arbitrary backend-executable code.
- Every custom strategy must be owned by a tenant/user and immutably versioned for runtime evidence. Editing a strategy creates a new version rather than mutating prior trading history.
- Strategy compatibility must be evaluated against the active exchange capabilities and available datasets.
- The platform may require schema validation, backtest, replay and/or paper validation before a custom strategy becomes live-eligible.
- Custom strategy rules may tighten risk constraints but may never raise platform hard ceilings or bypass Safety, Risk, Session Policy, tenancy/security or reconciliation.
- Architecture should allow future controlled sharing/import/export/marketplace/plan entitlements without requiring core Strategy Engine redesign.

## Signal publishing and Telegram room requirements
- Provide a top-level `Signals` area in the product sidebar and cockpit navigation.
- Allow creation of versioned signal-room strategies using canonical Strategy Definition / Strategy Builder semantics wherever practical.
- Permit an operator to select strategy, indicators/features, symbols/universe, direction, timeframes, minimum confidence/evidence requirements, operating windows, cooldown, entry logic, validity/expiry and publication policy.
- Support Telegram broadcast channels as the recommended official-signal destination, with optional linked discussion group; direct groups/supergroups may also be supported.
- Implement Telegram behind a provider-neutral `SignalPublisher` / destination adapter interface so other delivery destinations can be added later without changing signal semantics.
- Keep Telegram bot credentials backend-only and isolated from exchange API credentials, frontend clients, prompts and user-authored strategy content.
- Use a durable publication outbox with idempotency, retry policy, duplicate suppression and observable delivery state.
- Support structured LONG and SHORT signal artifacts with symbol/contract, exchange, direction, entry price or zone, up to three take-profit levels, one primary stop by default, optional additional explicitly-labelled stop/invalidation profiles, confidence/context, creation time and validity/expiry.
- Multiple stop levels must have explicit semantics and must not be presented ambiguously as if a subscriber could simultaneously use mutually inconsistent hard stops.
- Publication must pass an independent freshness/opportunity-decay gate; stale or excessively moved opportunities may be suppressed rather than sent late.
- Signal lifecycle may emit controlled updates such as entry reached, TP1/TP2/TP3 reached, stop/invalidation reached, cancelled, expired or closed.
- Store Telegram destination/message identifiers and publication lifecycle evidence sufficient for deduplication, updates, auditing and performance reconstruction.
- Telegram availability/failure must not alter HCT live-trading state; the Harness must be able to degrade/disable only signal publishing.
- Signal-room analytics must distinguish HCT internal decision price from Telegram publication price and plausible subscriber execution after human reaction delay.
- Evaluate subscriber realizability using publication latency, market movement, signal half-life, liquidity and configurable reaction-delay scenarios rather than claiming performance from ideal internal prices.
- A strategy suitable for automated low-latency HCT execution may be classified as unsuitable for human Telegram distribution when its opportunity half-life is too short.
- Signal content and commercial presentation must not imply guaranteed profit and require legal/commercial/regional review before paid commercialization.

## Institutional agent workforce requirements
- Agent specifications are canonical repository artifacts authored before implementation, not improvised by the execution model.
- Each agent must define mission, scope, non-goals, expertise profile, approved inputs/outputs, tools, source hierarchy, uncertainty behavior, escalation, communication contract, memory policy, skill policy, degraded behavior, evaluation suite and authority ceiling.
- Initial workforce should cover market scanning, technical/quant analysis, macroeconomics, crypto market structure, regime/cycle, strategy specialization/ecology, RAG memory, risk, portfolio exposure, leverage/position construction, execution/microstructure, position management, news/events, geopolitical/regulatory risk, security/exploits, adversarial review, supervision, post-trade review and agent/model-risk audit.
- Agents communicate production evidence through structured, persisted envelopes containing claims, source references, confidence/uncertainty, assumptions, temporal validity, symbol/timeframe scope, conflicts and tool/skill/model versions.
- Inter-agent deliberation must preserve dissent and support `WAIT` / `NO_TRADE`; forced consensus is not required.
- Agents access internet/data/internal capabilities through a governed Tool Gateway with explicit read/write permissions and auditability.
- Agents may propose reusable skills, but production skill creation follows a governed lifecycle such as DRAFT -> STATIC_REVIEW -> SANDBOX_TEST -> EVALUATED -> APPROVED -> ACTIVE.
- No agent may silently activate a skill that expands its authority.
- Different approved models may be routed to different agents based on quality, latency, reliability and cost, but model choice/version is observable and cannot alter authority boundaries.
- An Agent Auditor / Model Risk Agent must monitor calibration drift, source errors, hallucinations, tool misuse, prompt/skill/model changes and behavioral regressions.

## News and event intelligence requirements
- Provide a dedicated News & Event Intelligence Agent capable of current web/source research for known, emerging and scheduled events that may affect the market over minutes, hours, the current session or near-term horizon.
- Prefer primary/official and high-quality financial sources; social/unverified sources are discovery-only until corroborated.
- Preserve event provenance, publish/detection/scheduled timestamps, source reliability tier, corroboration state, affected assets, impact horizon, uncertainty, transmission mechanism and expiry/decay.
- Distinguish event existence from directional impact; the agent may classify volatility, liquidity, execution or no-trade risk without pretending directional certainty.
- News intelligence should cover macro releases/central banks, regulation/enforcement, exchange events, token/protocol events, security exploits, stablecoin risks, major legal/bankruptcy events, geopolitical shocks and other materially relevant scheduled/breaking developments.
- Unverified web content must not silently become canonical factual memory.
- News/event agents may reduce confidence or recommend `NO_TRADE`, but cannot directly place orders or override deterministic Safety/Risk/Policy.
- Evaluate the News Agent for detection latency, source quality, rumor rejection, duplication, timing, calibration and excessive-veto behavior.

## Agentic Copilot requirements
- Use a supervised multi-agent topology rather than unrestricted direct model access to exchange credentials.
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
- Position size must derive from approved monetary risk/invalidation and account for liquidity, slippage, fees/funding, portfolio exposure and exchange constraints rather than leverage-first sizing.
- Provide deterministic daily/session equity protection including hard daily maximum loss and explicit drawdown/no-new-exposure states.
- Optional profit targets may stop/reduce risk or trail session profit, but may never increase leverage, risk or trade frequency to reach a target.
- Maintain a risk-budget hierarchy across platform, tenant/account, session/day, portfolio, strategy, symbol/correlation cluster and individual trade.
- Evaluate portfolio concentration using correlation/common-factor/strategy exposure rather than assuming different crypto tickers are independent.
- Leverage evaluation must include liquidation distance/buffer, maintenance-margin rules and uncertainty around protective execution.
- No new position should be authorized if liquidation/margin state cannot be evaluated reliably.
- Resolve exchange risk tiers, maintenance-margin rates, maximum leverage, position limits, margin modes and liquidation semantics dynamically through the exchange adapter where available; unknown critical venue risk state blocks new exposure.
- Require an immutable, versioned and expiring `RiskSnapshot` for every exposure-increasing action, including projected post-trade tier, maintenance margin, leverage legality, liquidation buffer, portfolio state, policy versions and data confidence.
- Require deterministic risk reservation before order submission; pending, partial and uncertain orders continue consuming reserved risk until authoritative exchange/reconciliation resolution.
- Cross-margin approval must evaluate shared collateral contagion across relevant positions, unrealized PnL, open-order margin, correlation/common-factor exposure and reconciliation confidence.
- Maintain multi-horizon risk budgets spanning trade, intraday/session, daily, weekly, monthly and account-survival horizons; shorter-horizon availability may not override exhausted longer-horizon survival budgets.
- Maintain a protected `Operational Margin Reserve` that is excluded from ordinary opportunity sizing and preserved for fees, funding, slippage, partial fills, protective-order uncertainty, emergency closes, margin-rule changes and operational stress.
- Tail-risk models such as Expected Shortfall-style estimates, stress surfaces and survival metrics may only preserve or tighten approved risk, never relax deterministic hard ceilings.
- Treat protective-stop failure, delayed/rejected protection, gap-through-stop and partial protective fills as explicit contingent risk rather than assuming stops perfectly cap losses.
- Treat every `ADD`/pyramiding action as a fresh exposure-increasing decision requiring a new RiskSnapshot, risk reservation and post-add liquidation/portfolio review; martingale or loss-recovery escalation is prohibited by default.
- Evaluate collateral/stablecoin concentration and allow governed stress haircuts to derive conservative `Effective Risk Capital`; nominal wallet equity is not automatically equal to risk-usable capital under collateral stress.
- Model observable extreme venue mechanics, including tiered/partial liquidation and ADL exposure where supported by the venue, and degrade conservatively when such state is unknown.
- User-facing risk presets such as Conservative/Balanced/Aggressive must map only to bounded policy configurations beneath platform hard ceilings; labels themselves never authorize increased risk.
- Risk decisions must provide structured explainability including monetary risk, reserved/open risk, notional, leverage, margin mode, tier/MMR, liquidation corridor, Operational Margin Reserve, tail/survival state, collateral quality, portfolio concentration, protection-failure exposure and veto/reduction reasons.
- Risk research may include Adaptive Risk Budget Surface, Liquidation Defense Distance, Margin Fragility Score, Correlated Exposure Equivalent, Portfolio Stress Lattice, Stop Quality Score, Tier Transition Risk, Liquidation Buffer Confidence Interval, Stop-to-Liquidation Safety Corridor, Cross-Margin Contagion Index, Tail Loss Envelope, Expected Shortfall Surface, Survival Probability Floor, Collateral Stress Haircut and ADL Exposure Score, all subordinate to deterministic hard limits.
- Drawdown state may progress through governed states such as NORMAL, CAUTION, RISK_REDUCED, NO_NEW_EXPOSURE, RECOVERY_ONLY and EMERGENCY.
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
- Pricing plan definitions/entitlements are intentionally deferred, while the initial commercial catalog currency is USD.

## UI/UX requirements
- Establish a technological premium enterprise trading-cockpit design language aligned with the visual DNA of Hive Plan while remaining product-specific.
- Realtime risk, degraded-state and exchange-uncertainty signals must have visual priority over decorative/3D effects.
- Provide a dedicated Copilot session setup surface and realtime autonomous-operation cockpit.
- Provide a top-level `Signals` workspace for signal-room strategy configuration, Telegram destination health, template preview, published-signal lifecycle, freshness/latency warnings and subscriber-realizability/performance analytics.
- When a symbol is selected, provide a realtime chart with optional overlays for strategy behavior, actual executions, simulated signals, indicators/patterns, TP/SL/trailing paths, regime, agent evidence and proprietary HCT indicators.
- Clearly distinguish executed trades from hypothetical or paper/simulated strategy paths.
- Provide Strategy Catalog and Strategy Builder views with visual rules, human-readable explanation, chart preview, timeframe/indicator overlays, validation warnings, backtest/paper evidence, cloning/comparison and version history.
- Provide an agent/evidence view showing which agents participated, their status, evidence, disagreement, tool/source freshness and supervisor synthesis without exposing private hidden reasoning.
- Provide risk explainability covering monetary risk, notional size, leverage, stop/invalidation, liquidation buffer, expected slippage/fees, portfolio-correlation impact, budget remaining, Daily Equity Guard state and veto/reduction reasons.
- Plan dedicated operational views for scanner, symbol intelligence, indicators/patterns, positions/orders, risk/leverage, Safety Governor, RAG/decision traces, backtest/paper trading, model lifecycle, tenancy and system/API health.

## Validation requirements
- Backtest alone is insufficient for strategy/model promotion.
- Research candidates should progress through reproducible backtest, out-of-sample/walk-forward checks, realistic fees/slippage/funding assumptions as applicable, paper/shadow validation and governed promotion.
- Proprietary indicators must include ablation and incremental-value analysis against baselines.
- Profitability is never guaranteed by an indicator/model; evidence must distinguish statistical edge from overfitting.
- User-authored strategies require reproducible versioned evaluation and must not silently use future data or unavailable exchange capabilities.
- Agent changes, model changes and active skill changes require regression/evaluation evidence appropriate to their authority and risk.
- Signal-room strategies must be validated for subscriber realizability under Telegram publication delay, plausible human reaction delay, market movement, liquidity and signal-expiry assumptions rather than only internal decision-price results.
- Publication-path testing must cover idempotency, retry/duplicate suppression, stale-signal suppression, destination outage, lifecycle update consistency and independent Harness isolation.
- R03 risk validation must cover tier-boundary transitions, maintenance-margin changes, stale RiskSnapshots, reservation conservation, partial/uncertain orders, cross-margin contagion, tail scenarios, survival-budget exhaustion, Operational Margin Reserve protection, stop/protection failure, pyramiding, collateral stress/depeg, partial liquidation/ADL scenarios where representable, and structured explainability.

## Governance requirements already in force
- repository is canonical truth;
- every implementation increment requires a stable Work Order ID;
- every financial/trading increment defaults to HIGH_ASSURANCE unless explicitly proven otherwise;
- evidence is required before approval;
- chat handoff must be reproducible from GitHub without relying on conversation memory;
- prompts sent to external executors must follow the governed prompt contract.
