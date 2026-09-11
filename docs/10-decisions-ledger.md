# Decisions Ledger

## HCT-DEC-0001 — Adopt Hive Plan governance model
Status: APPROVED_FOR_BOOTSTRAP
Date: 2026-09-11

Decision: Hive Crypto Trader will use the Hive Plan operating model for source hierarchy, checkpoints, cross-chat continuity, Work Orders, prompt rendering, review, evidence and checkpoint promotion.

## HCT-DEC-0002 — HIGH_ASSURANCE default
Status: APPROVED_FOR_BOOTSTRAP
Date: 2026-09-11

Decision: money/trading, exchange execution, signing/custody, privileged authentication, security-critical or irreversible actions are HIGH_ASSURANCE by default.

## HCT-DEC-0003 — GitHub over chat memory
Status: APPROVED_FOR_BOOTSTRAP
Date: 2026-09-11

Decision: new chats must recover state from repository checkpoints and validate Git state rather than trusting conversational memory.

## HCT-DEC-0004 — MEXC Futures is the initial exchange target
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: Hive Crypto Trader will initially target MEXC Futures. The market universe must be discovered dynamically from contracts actually exposed and eligible through the current API rather than maintained as a static hard-coded list. Regional/capability restrictions remain an explicit planning concern.

## HCT-DEC-0005 — Realtime exchange integration must be quota-aware
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: realtime design will prefer WebSocket where appropriate and use REST for reference/control/reconciliation paths. A dedicated API Quota, WebSocket & Backpressure Governor will enforce documented limits, subscription planning, throttling, retry budgets and circuit breakers. The system must fail safe rather than risk abusive traffic or account blocking.

## HCT-DEC-0006 — Safety & Protection Governor is independent and authoritative
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: the product will include an independent Safety & Protection Governor capable of denying new exposure regardless of strategy or AI output. Hard risk/safety controls are not advisory and cannot be disabled by the intelligence layer.

## HCT-DEC-0007 — Indicator and pattern coverage is a first-class capability
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: the product will include an extensible Indicator & Feature Engine plus Candlestick & Chart Pattern Engine. Coverage should include the major public/standard technical-analysis families and relevant patterns commonly used in professional charting environments. The requirement is functional coverage, not copying proprietary/closed-source TradingView or community scripts.

## HCT-DEC-0008 — HCT proprietary indicators are encouraged but must earn promotion
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT may invent proprietary indicators/features intended to improve signal quality, but every such idea begins as an experimental hypothesis. No proprietary indicator may be promoted on intuition or a single favorable backtest; it requires reproducible statistical validation, realistic trading assumptions, out-of-sample/walk-forward testing and leakage controls. No profitability is guaranteed.

## HCT-DEC-0009 — Intelligence Brain, RAG and controlled learning
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT will plan an Intelligence Brain that combines indicators, patterns, strategy evidence, regime/cycle context, historical memory and risk context. RAG will support time-aware retrieval of comparable setups, outcomes, failure modes and lessons. Controlled offline learning and optional fine-tuning may be evaluated. AI/RAG/models may lower confidence or veto a candidate, but may never autonomously raise hard risk/leverage, disable safety, self-promote a production model/strategy or bypass deterministic execution controls.

## HCT-DEC-0010 — Multi-tenant commercialization readiness
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: the architecture will anticipate future multi-tenant commercialization, including tenant isolation, credentials isolation, quotas, policy boundaries, audit boundaries and entitlement readiness. Final paid plans and pricing are intentionally deferred.

## HCT-DEC-0011 — Shared company visual DNA
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: Hive Crypto Trader will use a premium technological enterprise design language aligned with the visual DNA being established in Hive Plan, including selective depth/3D effects and rich realtime visualization. Product safety, degraded-state and risk communication always outrank decorative effects.

## HCT-DEC-0012 — Cache is an optimization, never exchange truth
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT will include a caching/hot-state layer for low-latency operation, but every cached datum must have explicit freshness/TTL/invalidation semantics. Exchange-authoritative state such as orders, fills, positions and balances must remain reconcilable and cache divergence must never be silently accepted.

## HCT-DEC-0013 — Copilot may become autonomously operational inside hard boundaries
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT will plan explicit autonomy modes culminating in `FULL_COPILOT`, where the system may autonomously scan, select, open, manage and close trades, including TP/SL, trailing, partial exits and order replacement. Autonomy remains subordinate to exchange constraints, platform Safety Governor, Risk Engine and the current user/tenant operating envelope.

## HCT-DEC-0014 — Copilot uses supervised specialized agents
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: autonomous reasoning will be decomposed into specialized agents including market scout, technical analysis, regime/cycle, RAG memory, strategy, risk proposal, execution planning, position management, news/event context, adversarial review, supervision and post-trade review. Agents do not receive unrestricted direct exchange authority.

## HCT-DEC-0015 — Daily/session operating envelope is mandatory for autonomous modes
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: autonomous sessions must be governed by an immutable session policy snapshot containing configured loss limits, target mode, risk/trade, leverage ceiling, positions/exposure, strategies/symbols, hours, volatility/news behavior, cooldowns and emergency controls. User policy may tighten but not exceed platform hard safety ceilings.

## HCT-DEC-0016 — Proprietary indicators must seek genuinely incremental information
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT indicator R&D will explicitly investigate new features such as Regime Transition Probability, Multi-Timeframe Agreement Entropy, False Breakout Probability, Liquidity Vacuum Index, Exhaustion Resonance, Historical Analog Edge, Adversarial Confidence Gap, Signal Fragility, Opportunity Persistence, Contextual Risk-Reward Surface, Cycle Alignment and Decision Confidence Calibration. Novelty alone is insufficient; promotion requires incremental validated value.

## HCT-DEC-0017 — Copilot and strategy behavior must be visually inspectable
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: the trading cockpit must provide a dedicated Copilot session/setup experience and symbol chart workspace capable of visualizing actual executions, strategy signals, conditions, indicators/patterns, TP/SL/trailing behavior, regime, agent evidence/disagreement and proprietary HCT indicators while clearly distinguishing executed versus hypothetical/simulated paths.
