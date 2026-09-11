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
