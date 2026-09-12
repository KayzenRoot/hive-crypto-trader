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

Decision: realtime design will prefer WebSocket where appropriate and use REST for reference/reconciliation/control paths. A dedicated API Quota, WebSocket & Backpressure Governor will enforce documented limits, subscription planning, throttling, retry budgets and circuit breakers. The system must fail safe rather than risk abusive traffic or account blocking.

## HCT-DEC-0006 — Safety & Protection Governor is independent and authoritative
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: the product will include an independent Safety & Protection Governor capable of denying new exposure regardless of strategy or AI output. Hard risk/safety controls are not advisory and cannot be disabled by the intelligence layer.

## HCT-DEC-0007 — Indicator and pattern coverage is a first-class capability
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: the product will include an extensible Indicator & Feature Engine plus Candlestick & Chart Pattern Engine. Coverage should include the major public/standard technical-analysis indicator families and relevant patterns commonly used in professional charting environments. The requirement is functional coverage, not copying proprietary/closed-source TradingView or community scripts.

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

Decision: autonomous sessions must be governed by an immutable session policy snapshot containing configured loss limits, target mode, risk/trade, leverage ceiling, positions/exposure, strategies/symbols, hours, volatility/news behavior, cooldowns and emergency controls. User policy may tighten but not exceed platform/global safety ceilings.

## HCT-DEC-0016 — Proprietary indicators must seek genuinely incremental information
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT indicator R&D will explicitly investigate new features such as Regime Transition Probability, Multi-Timeframe Agreement Entropy, False Breakout Probability, Liquidity Vacuum Index, Exhaustion Resonance, Historical Analog Edge, Adversarial Confidence Gap, Signal Fragility, Opportunity Persistence, Contextual Risk-Reward Surface, Cycle Alignment and Decision Confidence Calibration. Novelty alone is insufficient; promotion requires incremental validated value.

## HCT-DEC-0017 — Copilot and strategy behavior must be visually inspectable
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: the trading cockpit must provide a dedicated Copilot session/setup experience and symbol chart workspace capable of visualizing actual executions, strategy signals, conditions, indicators/patterns, TP/SL/trailing behavior, regime, agent evidence/disagreement and proprietary HCT indicators while clearly distinguishing executed versus hypothetical/simulated paths.

## HCT-DEC-0018 — Owner-only Administrative Control Plane and Harness are required
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT will include an owner-only Administrative Control Plane plus dependency-aware Harness/Capability Isolation Engine. Initial policy allows one active super-admin identity. Privileged controls must support scoped enable/degrade/read-only/no-new-actions/pause/quarantine/disable/emergency-blackout behavior, blast-radius analysis, strong authentication and immutable audit evidence. Trading blackout semantics must preserve safe risk-reducing actions and reconciliation rather than blindly stopping everything.

## HCT-DEC-0019 — Frontend and backend are independently deployable runtime surfaces
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT frontend and backend will be separated as independently buildable/deployable runtime surfaces. The frontend is treated as an untrusted client and contains no exchange secrets or authoritative risk logic. Backend owns trading authority, security and business rules. Integration uses versioned API/realtime contracts and CI contract testing. Current repository preference is a canonical monorepo with separate application roots and shared safe contract packages, unless later evidence justifies multiple repositories.

## HCT-DEC-0020 — Multi-timeframe evidence uses governed adaptive weighting, not flat voting
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: timeframe importance will be strategy/regime/context dependent. HCT will preserve role-based multi-timeframe evidence, estimate redundancy/independence, and allow adaptive weights only inside governed/versioned bounds. Opportunity decisions retain explainable sub-scores before deriving a composite HCT Opportunity Score. No adaptive mechanism may silently rewrite hard production strategy semantics.

## HCT-DEC-0021 — Users may author declarative custom strategies
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT will provide a user Strategy Builder supporting flexible combinations of approved indicators/features, HCT indicators exposed to users, patterns, market structure, derivatives/liquidity/regime/timeframe context and supported entry/exit/position-management conditions. V1 user strategies are declarative and sandboxed rather than arbitrary executable backend code. Every runtime strategy is immutable/versioned and remains subordinate to exchange capabilities, Safety Governor, Risk Engine, Session Policy, tenancy/security and reconciliation.

## HCT-DEC-0022 — Initial product includes a documented default strategy catalog
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT should launch with approximately 10–15 built-in, documented strategy templates/families covering multiple market behaviors such as trend, pullback, breakout, momentum, mean reversion, reversal/exhaustion, multi-timeframe confluence, structure, liquidity, volume/volatility, regime-adaptive and HCT proprietary approaches. Exact formulas/parameters and live eligibility require governed validation; no template implies guaranteed profitability.

## HCT-DEC-0023 — V1 is MEXC-only live trading but core architecture is multi-exchange-ready
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: V1 will enable live trading only through MEXC Futures. Core HCT domains must use an HCT-owned Exchange Abstraction & Adapter Framework so future Binance and other exchanges can be integrated without rewriting strategy/risk/UI cores. Each venue retains explicit capability, order-semantics, authentication, quota and reconciliation behavior and requires independent HIGH_ASSURANCE production promotion.

## HCT-DEC-0024 — Strategy Builder uses a typed nodal graph as the primary visual authoring model
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: the primary custom-strategy authoring experience will use a ComfyUI-like nodal workflow paradigm adapted to trading. Users compose typed market/indicator/logic/timeframe/decision/position-management nodes and connect compatible ports. The graph compiles into the canonical declarative Strategy Definition; UI layout is non-semantic. Backend graph validation, static analysis, immutable version/hash, sandboxing, reproducible replay and governed promotion remain mandatory. Research technologies including graph redundancy analysis, sensitivity heatmaps, node attribution, counterfactual debugging, strategy fingerprints, shadow twins and graph optimization may be developed, but none may silently modify or self-promote live strategies.

## HCT-DEC-0025 — English-first product with continuous Portuguese and Spanish localization
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT's canonical/default product locale is `en-US`, with the initial commercial audience focused on the US/international English-speaking market. Product engineering, canonical identifiers, APIs, Strategy DSL/node types and technical documentation use English. `pt-BR` and Spanish (`es`, with future regional variants possible) are first-class supported localizations and must be maintained during feature development rather than retrofitted at the end. Localization must never change canonical trading semantics, risk rules or audit identity.

## HCT-DEC-0026 — Initial commercial catalog currency is USD
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT's initial subscription/plan catalog will be denominated in USD. Locale-specific formatting is separate from currency conversion or regional pricing. Future regional price books, local settlement currencies, taxes and FX behavior require explicit commercial/payment decisions rather than being inferred from UI language.

## HCT-DEC-0027 — Approved strategies participate in a governed Strategy Ecology and Router
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT will include a Strategy Ecology/Router layer that evaluates only policy-eligible strategy versions for context suitability, redundancy, conflicts, regime affinity, execution feasibility and portfolio interaction. Multiple agreeing strategies are treated as ensemble evidence rather than multiplied risk. Experimental/user/AI-generated candidates cannot self-promote to live; strategy routing remains subordinate to Safety Governor, Risk Engine, Session Policy and portfolio constraints.

## HCT-DEC-0028 — Strategy deterioration, diversity and conflict are explicit measurable concepts
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT will research explicit strategy-level measures including Strategy DNA, Effective Strategy Diversity, Strategy Decay Index, Strategy Regime Affinity Surface and Strategy Conflict Graph. These measures support explainability, routing, diagnostics, champion/challenger evaluation and governed quarantine/review, but do not constitute guaranteed edge and may not autonomously rewrite live strategy semantics.

## HCT-DEC-0029 — Agent specifications are canonical institutional-grade repository artifacts
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT agents will be specified in this repository as a coordinated institutional-grade financial/economic/market/risk workforce before implementation. Each agent specification must define expertise, tools, source hierarchy, structured evidence contract, memory/skill policy, evaluation and authority ceiling. External coding agents implement these specifications rather than inventing production behavior ad hoc.

## HCT-DEC-0030 — News & Event Intelligence receives governed realtime web/source research capability
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: a dedicated News & Event Intelligence Agent will research approved internet/data sources for breaking and scheduled events that may affect crypto over minutes, hours or the current session. It must prioritize primary/high-quality sources, preserve provenance/time validity/corroboration, distinguish event existence from directional certainty, and may recommend risk reduction or NO_TRADE. It cannot directly execute or override deterministic Safety/Risk/Policy.

## HCT-DEC-0031 — Agent tools and skills require explicit governance
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: agents access web/data/internal capabilities through a permissioned Tool Gateway. Reusable skills are versioned governed procedures; agents may propose new skills, but new/changed production skills require review, sandbox/evaluation and explicit activation. Model/tool/skill changes are observable and do not expand agent authority implicitly.

## HCT-DEC-0032 — Risk construction includes Daily Equity Guard, liquidation defense and portfolio-factor exposure
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT risk architecture will derive position size from approved monetary risk and thesis invalidation, keep leverage subordinate to survivability, enforce a deterministic Daily Equity Guard and evaluate correlated/common-factor portfolio exposure. Profit targets cannot trigger risk escalation. Research metrics such as Adaptive Risk Budget Surface, Liquidation Defense Distance, Margin Fragility Score, Correlated Exposure Equivalent, Portfolio Stress Lattice and Stop Quality Score may inform stricter decisions but cannot relax hard risk ceilings.

## HCT-DEC-0033 — Execution is an independent high-assurance decision domain
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: an approved trade candidate/order intent is not equivalent to successful execution. HCT will use an immutable canonical Order Intent, an Execution Intelligence/Feasibility layer, bounded slippage/latency policies and an event-sourced OMS. Execution optimization may adapt order tactics only within the already-approved quantity/risk and may not manufacture a new directional thesis or silently exceed slippage/risk limits.

## HCT-DEC-0034 — Unknown exchange outcomes require reconciliation before retry
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: timeout/network ambiguity after an order submission is classified as `UNCERTAIN`, not failed. HCT must block blind duplicate retries and reconcile against exchange-authoritative order/fill/position evidence before resolving or retrying. Persistent uncertainty reduces or blocks new exposure according to policy.

## HCT-DEC-0035 — Protective coverage and exchange-state confidence gate live exposure
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT will explicitly verify protective-order integrity and maintain a State Confidence view for local-versus-exchange truth. Required protection that is missing/partial/unknown and low-confidence reconciliation state can trigger no-new-exposure, protection recovery, reduce-only or emergency modes. Process restart/deployment/failover requires authoritative recovery/reconciliation before normal live operation resumes.

## HCT-DEC-0036 — Bootstrap infrastructure is free-first with portable provider abstractions
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT targets approximately USD 0/month recurring infrastructure during development and earliest commercialization, using credible free tiers where they satisfy security, latency and reliability requirements. A narrowly justified soft exception of approximately USD 3–4/month may be used for an indispensable persistent component when no safe free option exists. Architecture must abstract providers so later migration does not rewrite the trading core. Infrastructure receives a formal upgrade review near 10–12 active paying customers or earlier when measured capacity, latency, reliability, security or quota thresholds require it. Free pricing never justifies an unsafe live-trading design.

## HCT-DEC-0037 — Microstructure intelligence uses provider-neutral realtime feature serving
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT adopts Microstructure, Order-Flow, Liquidity, Breadth & Cross-Market Intelligence as a dedicated evidence domain. Realtime feature serving uses provider-neutral contracts; bootstrap implementation prefers in-process memory plus bounded durable evidence rather than per-tick cloud round trips. Proprietary microstructure features require point-in-time, OOS/walk-forward, realistic-cost and replay/paper/shadow validation before promotion.

## HCT-DEC-0038 — Market memory is point-in-time, temporal and governed
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT market memory must distinguish `event_time` from `knowledge_time`, preserve immutable ex-ante evidence, support global-plus-recent temporal retrieval, regime-conditioned analog search and explicit drift/forgetting controls. Material learning changes may not silently self-modify or self-promote production behavior.

## HCT-DEC-0039 — Intelligence Brain is calibrated, selective and non-authoritative over safety
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT Intelligence Brain fuses structured evidence with provenance, freshness, independence, contradiction and empirical calibration. `WAIT`, `NO_TRADE`, `DATA_UNCERTAIN`, `EVIDENCE_CONFLICT` and `CALIBRATION_UNTRUSTED` are first-class outputs. The Brain produces candidate decisions only and remains subordinate to Safety Governor, Risk Engine, Session Policy, Position/Leverage and Execution controls.

## HCT-DEC-0040 — Production promotion requires point-in-time proof and live-parity validation
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT will maintain a Simulation/Replay/Paper/Shadow/Promotion Laboratory. Promotion evidence must be point-in-time correct, include realistic frictions where relevant, use explicit staged validation and champion/challenger governance, preserve rollback and avoid hidden semantic divergence between research and live paths. Historical PnL alone is insufficient for production promotion.

## HCT-DEC-0041 — Telegram signal rooms are a separate governed publishing path
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT will provide a first-class `Signals` workspace with versioned signal strategies and Telegram channel/group publishing behind a provider-neutral `SignalPublisher` boundary. Signal publishing is informational distribution, separate from exchange execution, uses durable/idempotent outbox semantics, supports structured entry/TP/SL lifecycle, publication freshness gating and subscriber-realizability measurement, and must not claim guaranteed profit.

## HCT-DEC-0042 — Exchange risk tiers, maintenance margin and leverage ceilings are dynamic runtime state
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT must resolve exchange/contract risk tiers, maximum leverage, maintenance-margin rates, position limits, margin modes and liquidation-trigger semantics dynamically through the exchange adapter wherever available. Strategies, UI and risk logic may not treat a static leverage or maintenance-margin constant as perpetual exchange truth. Unknown critical venue risk state blocks new exposure.

## HCT-DEC-0043 — Exposure-increasing actions require immutable, expiring post-trade RiskSnapshots
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: every candidate action that may increase exposure must be evaluated against an immutable/versioned `RiskSnapshot` that captures current and projected post-trade account, position, margin, risk-tier, maintenance-margin, leverage, liquidation-buffer, portfolio, policy and data-confidence state. The snapshot has a finite validity horizon and explicit revalidation triggers; execution may consume only a still-valid approved snapshot or must request reapproval.

## HCT-DEC-0044 — Risk is reserved before order submission and remains reserved until authoritative resolution
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT will maintain a deterministic Risk Reservation Ledger. Exposure-increasing intents reserve approved risk before exchange submission. Partial fills convert only the filled portion into open-position risk; unfilled/uncertain portions remain reserved. Cancel requests, network timeouts and unknown outcomes do not release risk. Reservations are released only after exchange-confirmed or authoritatively reconciled cancellation, rejection, expiry or final resolution. Agents and strategies cannot manually free reserved risk.

## HCT-DEC-0045 — Cross-margin shared-collateral contagion is an explicit deterministic risk gate
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: when cross margin is used, HCT must evaluate shared wallet/equity, all relevant cross positions, unrealized PnL, maintenance margin, open-order margin, correlated stress and collateral confidence before approving new exposure. A position that appears acceptable in isolation may be reduced or vetoed if it materially destabilizes the shared margin pool. Unknown critical cross-margin state blocks new exposure.

## HCT-DEC-0046 — Risk authority includes multi-horizon survival budgets
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT risk budgets span individual trade, intraday/session, daily, weekly, monthly and account-survival horizons. Exhaustion or breach at a longer survival horizon may tighten or veto shorter-horizon opportunity authority even when a local trade/day budget remains. Tail/survival models may tighten deterministic limits but may not expand them.

## HCT-DEC-0047 — Operational Margin Reserve is protected from ordinary opportunity sizing
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT will maintain a protected Operational Margin Reserve for non-ideal operational outcomes including fees/funding, slippage, partial fills, protective-order failure or delay, emergency closes, margin-rule changes and reconciliation uncertainty. Normal strategies, agents and opportunity sizing cannot consume the OMR as ordinary risk capital.

## HCT-DEC-0048 — Every ADD/pyramiding action requires fresh independent risk approval
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: adding exposure to an existing position requires a new RiskSnapshot, risk reservation, projected post-add tier/MMR/leverage/liquidation review and cumulative thesis/portfolio risk evaluation. Existing unrealized profit does not constitute free risk capacity. Implicit martingale or loss-recovery averaging is prohibited by default.

## HCT-DEC-0049 — Collateral quality and extreme venue mechanics are first-class risk inputs
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: nominal wallet equity is not automatically equal to usable risk capital. HCT must evaluate collateral/stablecoin concentration and may apply governed stress haircuts to derive Effective Risk Capital. Partial/tiered liquidation, insurance-fund/ADL mechanics and other venue-extreme behavior are explicit risk inputs where observable; unknown critical extreme-state information causes conservative degradation or no-new-exposure rather than optimistic assumptions.

## HCT-DEC-0050 — Execution commands require immutable identity and a current authorization lease
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT separates Order Intent, Execution Plan, Execution Command, client/external order identity, exchange order identity, fills and mutation lineage. Every state-changing command must bind to still-valid Safety, RiskSnapshot/Risk Reservation and Session Policy state through a Command Authorization Lease. A queued command whose authority has expired or changed must be revalidated before transmission.

## HCT-DEC-0051 — Exchange acknowledgements and fills are different evidence levels
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: REST/API success or an exchange order identifier proves acknowledgement/acceptance only to the extent documented by the venue and never proves a fill. HCT uses an explicit Order Evidence Ladder and resolves economic state from order, fill, position and reconciliation evidence with provenance. Unknown or contradictory evidence remains visible and may block new exposure.

## HCT-DEC-0052 — Fills are economically idempotent and OMS projections cannot regress on late events
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: each exchange fill identity may affect position, fees and risk accounting at most once. OMS stores immutable source events, deduplicates by authoritative identities where available, tolerates duplicate/late/out-of-order events and does not regress a stronger lifecycle projection solely because weaker or older evidence arrived later.

## HCT-DEC-0053 — Unknown outcomes and cancel/replace races require reconciliation, never blind retry
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: timeout after submission, cancel-pending, replace-pending and ambiguous mutation outcomes are not classified optimistically. HCT blocks unsafe duplicate commands, uses external/exchange IDs and authoritative order/fill/position evidence to resolve state, and explicitly handles fills racing with cancel/replace operations. A cancel request never proves cancellation.

## HCT-DEC-0054 — Reduce/close and protection semantics are position-mode aware and exposure-safe
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: REDUCE/CLOSE/PROTECT actions must be validated against current reconciled position mode, side, size, position identity and venue capability. They may not silently create or increase opposite exposure. Required stops/TP/trailing protection are represented as dependencies of actual filled exposure and must be verified/re-sized as fills and exits change the position.

## HCT-DEC-0055 — Reconciliation uses explicit watermarks, conflicts and restart completeness proof
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT reconciliation tracks the coverage/freshness of order, fill, position, account and protection evidence with explicit watermarks. Contradictory evidence creates a persisted conflict instead of silent overwrite. After restart/failover, normal new exposure remains disabled until potentially-live orders/intents, positions, fills, protection and risk reservations are authoritatively classified or the system remains in a restrictive recovery mode.

## HCT-DEC-0056 — Protective and reconciliation operations receive quota and time-integrity priority
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: signed exchange commands require monitored clock integrity and current venue request-time semantics. API/WebSocket budgets are priority-aware so emergency, protection, reconciliation and active-position control outrank new exposure and research traffic. Scanner/research demand may not consume the capacity required to protect or reconcile existing money-at-risk.

## HCT-DEC-0057 — Execution tactics, fees and private-event schemas are versioned external dependencies
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: supported order types, time-in-force behavior, STP, position modes, reduce-only semantics, fee schedules and private-event schemas are capability/versioned external state, not perpetual hardcoded assumptions. HCT maintains an Execution Tactic Capability Matrix, expected-versus-realized cost evidence, schema validation/quarantine and conservative degradation when critical semantics become unknown.

## HCT-DEC-0058 — Trusted realtime state requires generation and synchronization proof
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: every realtime feed/session uses explicit generation identity; retired generations cannot mutate current trusted state. Snapshot/delta reconstructed state becomes trusted only after synchronization continuity is proven under channel-specific semantics.

## HCT-DEC-0059 — Backpressure and load shedding preserve safety-critical traffic first
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: realtime queues and resource budgets are bounded and priority-aware. Emergency, protection, reconciliation, active-position and execution-critical state outrank scanner, research and RAG workloads. Load shedding is deterministic, observable and cannot silently claim full fidelity after data/work has been dropped.

## HCT-DEC-0060 — Realtime time integrity uses monotonic age and explicit clock health
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT separates exchange event time, wall-clock chronology and monotonic elapsed time. Signal/data age and latency budgets use monotonic timing where possible; material clock drift or untrusted time blocks time-sensitive new exposure.

## HCT-DEC-0061 — Market-state and feature coherency are explicit trading prerequisites
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: trusted market-state generations and derived features preserve exact input provenance, generation and freshness. Mixed/stale/untrusted generation combinations are explicit states and may block or degrade strategy/Brain authority according to horizon-specific policy.

## HCT-DEC-0062 — Critical schema/persistence failure is visible and may reduce trading authority
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: unknown/malformed critical realtime schemas are preserved and quarantined rather than guessed. Durable evidence-store failure is isolated from the hot safety path, but if audit/recovery evidence can no longer be guaranteed HCT must tighten or stop new exposure instead of continuing invisibly.

## HCT-DEC-0063 — Data quality maps deterministically to trading authority
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: feed confidence and data-quality scores are explanatory only. Hard realtime predicates deterministically map system state to `ALLOW_NEW_EXPOSURE`, `DEGRADED_NEW_EXPOSURE`, `NO_NEW_EXPOSURE`, `REDUCE_ONLY`, `RECONCILIATION_ONLY` or `EMERGENCY`; aggregate scores cannot mask a failed critical predicate.

## HCT-DEC-0064 — Decision freshness and signal lifetime propagate end-to-end
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: each candidate action carries a Decision Freshness Envelope from market reception through features, Brain, Risk and Execution. If the remaining signal lifetime is insufficient for safe downstream processing/execution, the action expires or waits rather than being forced through.

## HCT-DEC-0065 — Subscription, cache, replay and symbol lifecycle are governed realtime resources
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: subscriptions have deterministic quota/compute budgets; cache entries require freshness leases and never become exchange order/account truth; replay intervals require completeness/fidelity manifests; symbol lifecycle changes must converge safely through subscriptions, caches, features, strategies and position handling.

## HCT-DEC-0066 — Future HA realtime state requires single-writer ownership and fencing
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: future multi-instance realtime reconstruction/publication uses explicit ownership leases and fencing tokens so only one writer publishes canonical state per partition. Failover takeover requires resynchronization/recovery proof before trusted publication resumes.

## HCT-DEC-0067 — Brain fusion accepts only canonical admissible evidence
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: every machine-authoritative Brain input uses a versioned Canonical Evidence Envelope and passes a deterministic Evidence Admissibility Gate before fusion. Failed critical provenance, temporal, schema, generation, freshness, policy or R05 data-authority predicates cannot be hidden by confidence scores or LLM reasoning.

## HCT-DEC-0068 — Confidence, uncertainty and calibration remain semantically separated
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: directional probability, opportunity quality, data confidence, calibration reliability, evidence independence, regime fit, historical support, execution feasibility, risk compatibility and stability are separate quantities. Calibration uses explicit contextual hierarchy, sample sufficiency, drift and fallback rules; insufficient support produces `CALIBRATION_UNTRUSTED` rather than fabricated certainty.

## HCT-DEC-0069 — Selective abstention is a first-class intelligence outcome
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: `WAIT`, `NO_TRADE`, `DATA_UNCERTAIN`, `EVIDENCE_CONFLICT`, `CALIBRATION_UNTRUSTED`, `MODEL_UNAVAILABLE` and `MEMORY_UNAVAILABLE` are legitimate candidate outcomes. Near ties, missing required evidence, expired signal lifetime, material fragility or unresolved contradiction cannot be forced into LONG/SHORT simply to keep the system active.

## HCT-DEC-0070 — Agents are evidence producers under bounded deliberation and fixed authority ceilings
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: agents publish structured evidence with provenance, assumptions, temporal validity, uncertainty, contradictions, tools/sources and authority ceilings. Agent and supervisor deliberation is bounded by rounds, time, tool, inference/cost and signal-lifetime budgets. No agent has direct exchange-order, risk-limit, canonical-truth or self-promotion authority.

## HCT-DEC-0071 — Temporal memory is point-in-time and protected by a leakage firewall
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: canonical market memory preserves event, knowledge, ingestion, correction and label-maturity times plus market-state generation and provenance. Decision-time memory is immutable; later outcomes append separately. Historical replay/retrieval/training may not expose future knowledge, later unavailable corrections, outcome-derived prior features or immature labels.

## HCT-DEC-0072 — Historical analog evidence requires independence and sufficiency
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: temporal retrieval is versioned and context-aware, while historical analog support must report raw and effective-independent counts, regime/temporal/symbol diversity and drift/relevance penalties. Sparse, near-duplicate or overly concentrated analog sets produce `INSUFFICIENT_ANALOG_EVIDENCE` rather than strong statistical claims.

## HCT-DEC-0073 — Continual learning is localized, bounded and cannot self-promote
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: drift must be localized before adaptation. Only explicitly approved bounded online calibration/reliability/drift/regime statistics may adapt within frozen limits. Material model, strategy, behaviorally material prompt, retriever, agent-skill or memory-policy changes require immutable candidate versions, offline validation and governed promotion. Self-promotion is prohibited.

## HCT-DEC-0074 — Intelligence behavior is fully version-pinned and attributable
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: every production-eligible candidate decision identifies the exact material versions/hashes of evidence schema, market-state generation, strategy, features, model, prompt/spec, agent, tool, skill, retriever, memory snapshot/index, calibration, policy and Brain fusion logic. HCT maintains a Decision Attribution Ledger linking evidence, exclusions, downstream Safety/Risk/Execution actions and matured outcomes.

## HCT-DEC-0075 — External web/news remains untrusted until temporally and evidentially qualified
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: external web/news content requires source identity, publication/event/knowledge timestamps, reliability, corroboration and expiration before it can enter trusted intelligence. Unverified content cannot silently become canonical factual memory, training truth or a direct execution instruction; contradictory sources remain explicit.

## HCT-DEC-0076 — Brain remains subordinate to R05 data authority and deterministic Risk
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: R05 hard data-authority states directly constrain evidence admission and candidate outputs. The Brain cannot reason around `NO_NEW_EXPOSURE`, `RECONCILIATION_ONLY` or equivalent failed critical data predicates. Brain confidence/opportunity quality cannot raise hard monetary risk, leverage, loss budgets, margin or portfolio ceilings.

## HCT-DEC-0077 — Intelligence changes require incremental-value promotion proof
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: material changes to models, retrievers, prompts/specs, agents/skills, calibration, fusion logic or memory policy require incremental-value proof through applicable offline evaluation, point-in-time replay, walk-forward/OOS, paper, shadow and champion/challenger stages. Promotion evaluates calibration, abstention, false-confidence harm, regime robustness, latency/cost/failure behavior and baseline/champion comparison. Better explanations alone do not prove better decisions.

## HCT-DEC-0078 — Promotion datasets require eligibility proof and point-in-time universe truth
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: promotion-grade experiments require immutable dataset eligibility/completeness manifests derived from R05 capture fidelity and a point-in-time universe/rule view. Current surviving symbols or current exchange rules may not be projected backward, and critically degraded/unknown historical intervals cannot silently count as full promotion evidence.

## HCT-DEC-0079 — Temporal leakage and holdout access are governed proof boundaries
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: promotion evidence requires end-to-end Temporal Non-Interference proof and an OOS/holdout firewall. Tuning/search cannot consume final promotion holdouts; access is auditable, temporal purge/embargo/nested validation are used where needed, and repeatedly inspected holdouts may be considered consumed rather than recycled as supposedly independent confirmation.

## HCT-DEC-0080 — Promotion experiments require complete reproducible environment identity
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: every promotion-grade experiment pins code/data/config/dependencies/runtime/container/build, simulator/accounting/fill/latency versions, strategy/model/prompt/tool/skill/retriever/calibration/policy versions, venue semantics, evaluator versions and stochastic reproduction identity. Materially unpinned behavior is not promotion-reproducible.

## HCT-DEC-0081 — Replay uses causal scheduling and historical venue/fill semantics
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT replay uses an explicit causal event scheduler and point-in-time venue semantics. Fill models expose realism/confidence class and model no-fill, partial fill, liquidity, latency, slippage and cancellation uncertainty. Impossible same-tick/same-bar causal shortcuts and optimistic-only fill assumptions cannot be promotion authority.

## HCT-DEC-0082 — Accounting and R03/R04/live-parity semantics are shared or conformance-tested
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: replay/paper/shadow use a canonical trading accounting/margin kernel and preserve R03/R04 RiskSnapshot, Risk Reservation, authorization, OMS, protection, uncertainty and reconciliation semantics. Research/live semantic forks must be explicit parity exceptions and block blanket live-parity claims.

## HCT-DEC-0083 — Paper and shadow are technically isolated from live trading authority
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: paper/shadow environments use separate capability/state namespaces and are technically unable to mutate live exchange orders, production positions, Risk Reservations, protection, balances or authoritative production configuration. Hypothetical fills cannot become real trading truth.

## HCT-DEC-0084 — Promotion evidence is immutable and experiment-family selection bias is governed
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: promotion decisions reference append-only immutable Promotion Evidence Bundles containing manifests, metrics, gate outcomes, evaluator/reviewer identity and relevant failed/search history. Related searches use ExperimentFamilyIDs with variant/search-space/holdout-access accounting and appropriate multiple-testing/selection-bias controls.

## HCT-DEC-0085 — Promotion eligibility expires and future limited-live uses an immutable canary envelope
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: production eligibility has a validity lease and revalidation triggers for material venue/data/model/runtime/regime/reality-gap/safety changes. Any future `LIMITED_LIVE` stage, if explicitly authorized in a later production process, requires immutable account/symbol/time/risk/loss/health/expiry limits plus automatic kill/rollback conditions; canary scope cannot silently broaden.

## HCT-DEC-0086 — Promotion proof measures independent, robust and economically material evidence
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: promotion evidence distinguishes raw from effective-independent samples, declares regime/OOD coverage, uses component-appropriate uncertainty and economic materiality, and applies nested search/parameter robustness controls. Narrow overfit optima, correlated observation counts or unsupported regimes cannot masquerade as broad proof.

## HCT-DEC-0087 — Simulator assumptions are empirically calibrated and degraded/synthetic evidence stays explicit
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: fee/funding/latency/fill/slippage/cancel models are versioned and empirically calibrated against available observations with confidence/age/error and conservative fallback. Degraded/imputed data, synthetic crises and Monte Carlo/resampling remain explicitly classified; synthetic or statistically invalid resampling cannot be presented as clean historical profitability evidence.

## HCT-DEC-0088 — Promotion evaluates portfolio interaction, paired comparisons, shadow divergence and component-level reality gaps
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: where components interact, promotion evaluates shared capital/risk reservations/correlation/cross-margin/quota/liquidity/resource effects. Paired Decision Twin/ablation tests disclose confounders, Shadow Divergence compares candidate vs Champion on aligned windows, and critical component-level reality gaps cannot be averaged away by a favorable composite.

## HCT-DEC-0089 — Typed promotion gates, rollback compatibility, independent review and resource governance are mandatory
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: promotion profiles are component-specific with mandatory metrics/stages/failure gates. HIGH_ASSURANCE promotion requires auditable independent review where practical and no self-approval. Rollback proof includes persisted state/schema/memory/OMS/open-position compatibility or a safe roll-forward plan. Experiment resource limits may delay/cancel work but cannot silently weaken required validation rigor.

## HCT-DEC-0090 — Protected operations require canonical server-derived tenant security context
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: every protected request, job, event, worker action and authoritative state transition derives an authenticated immutable SecurityContext containing principal, tenant/membership/account scope, policy/role/assurance/session state and correlation identity. Client-supplied tenant IDs or resource IDs never prove authority by themselves; every tenant-owned object/action requires server-side ownership/operation authorization.

## HCT-DEC-0091 — Tenant isolation spans database, connection pools, cache and asynchronous messaging
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT uses enforceable tenant ownership for persistence plus database defense-in-depth where appropriate; ordinary tenant paths do not use bypass authority. Pooled connection/async context cannot leak tenant state. Tenant-sensitive caches are namespaced/authorized, and queued/events are authenticated producer envelopes whose tenant metadata is routing context rather than authorization proof.

## HCT-DEC-0092 — Trading authority is bound to one canonical tenant–exchange-account identity
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: private streams, RiskSnapshots/Reservations, execution commands, OMS, positions, protection and reconciliation bind to a canonical tenant–exchange-account–credential identity. Cross-tenant/account binding mismatch is rejected before exchange transmission. Shared cross-tenant exchange credentials/accounts are not an implicit V1 capability.

## HCT-DEC-0093 — Exchange credentials live behind a cryptographically separated SecretStore lifecycle
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: raw exchange credentials are backend-only SecretStore objects protected by provider-neutral envelope/key-management semantics with environment and tenant/account blast-radius separation. Import/verify/activate/rotate/revoke/compromise/delete is an audited lifecycle; ordinary database/admin/frontend paths retain opaque references only.

## HCT-DEC-0094 — Raw secrets are never normal telemetry, prompt or support data
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: raw secrets are `NEVER_LOG`, `NEVER_TRACE`, `NEVER_PROMPT`, `NEVER_EXPORT`. HCT uses secret-aware DTO/redaction, CI/artifact scanning and opaque capabilities for agents/tools. Invalid/compromised tenant exchange credentials block new exposure and trigger account-specific reconciliation/protection assessment.

## HCT-DEC-0095 — Human identity security includes strong authentication, step-up, recovery and revocable sessions
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT supports strong MFA and phishing-resistant authenticators such as passkeys/WebAuthn where supported, with higher assurance for admin/live-sensitive actions. Recovery is a governed security-critical flow, and sessions/tokens are scoped, bounded, revocable and revalidated after material identity/role/recovery changes.

## HCT-DEC-0096 — Workload, admin and support authorities are distinct, least-privileged identities
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: services/workers use authenticated least-privileged workload principals distinct from human/CI identities. Admin authority uses a separate high-assurance, reason/scope/time-bounded privilege plane plus protected break-glass. Future support assumption preserves real actor plus assumed tenant identity, is read-only by default and may never silently impersonate or reveal secrets.

## HCT-DEC-0097 — Harness scope is tenant-aware and commercial entitlement never equals trading authorization
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: Harness controls use exact typed tenant/account/capability scope and dependency/blast-radius analysis; global wildcard actions require stronger privilege. Commercial entitlement only states purchased feature availability and cannot grant admin, Safety/Risk bypass or trading authority. Billing changes preserve required close/protection/reconciliation of existing exposure.

## HCT-DEC-0098 — Multi-tenant resource scheduling preserves safety reserves before tenant workloads
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT enforces hierarchical platform/safety/tenant/account/workload quotas across exchange/API/WS, scanner, agents/models, replay, queues, storage/cache and compute. A noisy tenant is throttled/degraded locally before unrelated tenants lose protection/reconciliation capacity.

## HCT-DEC-0099 — Tenant-sensitive data, telemetry, audit, backup and offboarding have explicit lifecycle boundaries
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT classifies data sensitivity and defines encryption, observability, audit, retention/export and access rules. Backups preserve tenant/key isolation; offboarding safely handles open exposure, credential revocation, export, legal/audit retention and deletion from ordinary stores, caches and RAG/vector indexes without cross-tenant contamination.

## HCT-DEC-0100 — Production environments and software supply chain are isolated from development and tenant artifacts
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: production/non-production identities, secrets and data are separated. CI/CD uses least-privileged protected deployment identities and secret/provenance/dependency controls; forks/untrusted jobs cannot inherit production secrets. User strategies/uploads remain tenant-scoped untrusted declarative artifacts and receive no arbitrary filesystem/network/process/SecretStore capability.

## HCT-DEC-0101 — Security incidents and disaster recovery are tenant-scoped and trading-aware
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: incident/anomaly handling identifies exact tenant/account/principal/capability/secret/release blast radius, contains narrowly while preserving safe protection/reconciliation, and audits recovery. DR restores Identity, SecretStore, tenant data, Risk/OMS/reconciliation and audit integrity without tenant mixing, resuming new exposure only after restrictive recovery proof.

## HCT-DEC-0102 — Commercial account state cannot strand money-at-risk
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: trial/paid/grace/past-due/cancelled/suspended/offboarding states have deterministic feature/entitlement behavior while preserving mandatory risk-reducing close, protection, reconciliation, export and safe offboarding actions for existing exposure.

## HCT-DEC-0103 — Commercial eligibility, external APIs and security assurance require explicit governed evidence
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: region/exchange/KYC/API capability eligibility is server-side policy independent from locale/payment; required terms/privacy/risk agreements are versioned acceptance evidence subject to legal review. Future public APIs/webhooks/browser sessions require scoped tenant-bound security controls. Broad commercialization requires an adversarial multi-tenant security test matrix plus an auditable vulnerability/supply-chain lifecycle and penetration-test readiness.

## HCT-DEC-0104 — Frontend is a non-authoritative projection governed by a Canonical UI State Envelope
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: authoritative realtime cockpit projections use a versioned UI State Envelope containing tenant/account/environment, generation, schema/version, source, freshness and trading-authority metadata. The frontend may derive presentation but cannot infer or upgrade stronger exchange/risk/security authority than the backend supplied.

## HCT-DEC-0105 — Stale, disconnected and resyncing state deterministically restricts UI authority
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: realtime UI distinguishes `LIVE_TRUSTED`, `LIVE_DEGRADED`, `STALE`, `DISCONNECTED`, `RESYNCING` and `UNKNOWN`. R05 authority states map to a deterministic action matrix. Transport reconnection alone never restores trusted-live presentation; generation synchronization and required reconciliation proof must complete first.

## HCT-DEC-0106 — Order UI follows the exchange evidence ladder and never optimistically invents economic truth
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: intent, submit, acknowledgement, partial fill, fill, cancel/replace pending, uncertain, reconciliation and terminal states remain distinct. Acknowledgement is not fill; cancel request is not cancellation; timeout is not failure when venue outcome is unknown. Money/risk/order/protection state cannot be optimistically marked complete client-side.

## HCT-DEC-0107 — Protection integrity and multi-horizon survival outrank PnL presentation
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: open-position/cockpit UI exposes protection confidence/coverage/freshness plus monetary/reserved risk, survival budgets and Operational Margin Reserve. Unknown/failed protection and survival restrictions visually outrank profit/opportunity content and cannot disappear inside a composite score.

## HCT-DEC-0108 — Current truth, projected post-trade risk and decision freshness remain separate
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: current tier/MMR/leverage/liquidation/risk truth is distinct from projected post-fill state. Opportunities/actions expose applicable data-to-decision age, remaining signal lifetime, expiry and Risk/Execution revalidation state.

## HCT-DEC-0109 — LIVE/PAPER/SHADOW/REPLAY and tenant/account/environment contexts are locked and unmistakable
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: environment/mode identity uses redundant text/icon/layout semantics, not color alone. Money-affecting surfaces persist active tenant, exchange account and environment. Context switching invalidates unsafe transient/cached state and loads newly authorized authoritative state before actions resume.

## HCT-DEC-0110 — Dangerous and emergency actions use trading-aware consequence semantics
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: close-all, cancel-all, freeze, blackout, credential revoke, rollback/quarantine and comparable actions expose exact scope/consequence, applicable step-up/reason/blast radius and authoritative completion evidence. Emergency blackout communicates preserved protection, risk-reducing actions and reconciliation instead of implying blind shutdown.

## HCT-DEC-0111 — Privileged UI context and tenant-sensitive client data are explicit security boundaries
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: admin/support/elevation/break-glass context is persistent and retains the real actor identity. Browser caches/storage/search/notifications/exports/errors/telemetry obey R08 tenant/data-classification boundaries and are invalidated appropriately on context switch, logout or revocation.

## HCT-DEC-0112 — Safety communication is accessible and pre-empts lower-priority visual effects
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: critical state cannot rely only on color, motion, sound or hover. It uses semantic text/icon/structure, keyboard/focus and assistive-technology behavior with reduced-motion equivalents. A UI priority scheduler ensures capital-safety/state-certainty events suppress lower-priority PnL/opportunity/decorative effects.

## HCT-DEC-0113 — Chart, Brain and agent visualization preserve evidence semantics rather than fabricate authority
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: executed/confirmed/provisional/hypothetical chart elements carry source/timeframe/version/generation/mode semantics. Brain dimensions remain separated rather than collapsed into one confidence percentage. Agent agreement is visualized as evidence and cannot appear to override deterministic Safety/Risk/Policy gates.

## HCT-DEC-0114 — Realtime UI performance degradation must be observable and explicit
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: frontend render/update budgets, virtualization/coalescing and client-lag telemetry are planned as integrity controls. A client that cannot keep up visibly degrades rather than silently displaying stale information. Alerts use governed priority, deduplication, acknowledgement, resolution and escalation semantics.

## HCT-DEC-0115 — Strategy authoring and audit UX are versioned, immutable and evidence-linked
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: the nodal Strategy Builder uses typed validation, immutable published versions and explicit research/paper/shadow/production eligibility lifecycle; editing active behavior creates a new candidate version. Executed actions can be explored through structured point-in-time decision/audit traces without exposing raw secrets or private chain-of-thought.

## HCT-DEC-0116 — WCAG 2.2-oriented accessibility and semantic design tokens are design-system requirements
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: R09 adopts WCAG 2.2-oriented automated/manual accessibility verification as the minimum web baseline. Motion/depth obey reduced-motion and performance constraints. Authority/protection/data/evidence/environment/severity use semantic design tokens independent of hard-coded colors. Localization/time formatting cannot change canonical financial/risk meaning.

## HCT-DEC-0117 — Mobile, offline, export and unknown-state behavior are restrictive by default
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: the full command center is desktop/web-first. Mobile does not automatically inherit desktop money authority. Loss of backend authority creates explicit offline/read-only behavior. Missing/loading/error/partial data never becomes reassuring zero/healthy state. Exports obey R08 classification, and frontend observability diagnoses state age/lag without becoming account truth.

## HCT-DEC-0118 — Observability is a governed evidence plane, never authoritative trading truth
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT telemetry uses a versioned observability context envelope and explicitly classifies authoritative facts, reconciled projections, observations, derived metrics and estimates. Logs/metrics/traces can explain exchange/OMS/Risk state but cannot replace it or relax authority.

## HCT-DEC-0119 — Trading decisions and outcomes require end-to-end causal/time lineage
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT maintains causal correlation from market state through Brain, Safety/Risk, Risk Reservation, execution, exchange evidence, OMS, protection and reconciliation while preserving immutable domain IDs. Event/receive/processing/monotonic time and clock health remain explicit to prevent false latency or causality claims.

## HCT-DEC-0120 — Telemetry is secret-safe and tenant-safe by construction
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: observability uses structured allowlisted/redacted fields; raw credentials, signing material, tokens and prohibited sensitive context are never normal telemetry. Query/search/export/admin/support access inherits R08 tenant/account/environment isolation and least privilege.

## HCT-DEC-0121 — High-value audit is append-only, attributable and tamper-evident
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT maintains append-only audit events covering auth/privilege/secrets/Safety/Risk/execution/OMS/reconciliation/promotion/release/commercial/incident actions. Corrections append superseding evidence; high-value evidence supports appropriate hash-chain/signature/WORM-style tamper-evidence according to deployment capability.

## HCT-DEC-0122 — SLOs prioritize safety, correctness, freshness and reconciliation over raw uptime
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT defines trading-aware SLO/SLI families and accepts safe restriction/refusal of new exposure as correct behavior. Critical SLO burn may tighten authority only through governed deterministic policy; stronger authority resumes only after underlying domain recovery proof.

## HCT-DEC-0123 — Protection and reconciliation are measurable operational contracts
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: protection establishment/verification, protected quantity, private-state freshness, reconciliation coverage/conflict age, uncertain-order age and recovery convergence are first-class SLIs with policy/versioned targets finalized through implementation benchmarks.

## HCT-DEC-0124 — Incident severity and response are trading-aware
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: incident severity considers money-at-risk, state certainty, tenant/security blast radius, protection/reduction capability and recoverability. Canonical response progresses through detection, containment, safe operating mode, evidence preservation, reconciliation, remediation, verification and progressive restore.

## HCT-DEC-0125 — Incident automation is bounded and recovery requires objective proof
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: detection automation may page/enrich and execute only pre-approved bounded containment through Harness/Safety/security controls; it never gains arbitrary trading authority. Material incidents preserve evidence bundles, and stronger trading authority returns only after explicit recovery gates pass.

## HCT-DEC-0126 — Compliance readiness is evidence mapping, not an unsupported compliance claim
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT maintains a versioned Control Evidence Map with internal controls, owners, evidence, retention and applicability plus external-framework mappings where useful. Jurisdiction/product applicability is versioned and legally reviewed as needed; framework alignment alone does not constitute certification or legal compliance.

## HCT-DEC-0127 — FinOps is subordinate to capital safety, security and evidence durability
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: cost controls may suppress research/optional workloads first but may not silently disable minimum Safety/Risk/protection/reconciliation/security/audit/incident evidence. P0/P1 safety capacity is protected from budget optimization.

## HCT-DEC-0128 — Telemetry cardinality, sampling, retention and pipeline degradation are governed resources
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT budgets telemetry cardinality, preserves mandatory/tail/security/trading evidence under sampling, uses evidence-class retention and exposes observability-pipeline degradation. If mandatory evidence durability is at risk beyond policy, new exposure may be restricted without making remote observability a synchronous hot-path dependency.

## HCT-DEC-0129 — Alerting, runbooks, on-call and postmortems are lifecycle-managed operational artifacts
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: actionable alerts have owners/severity/dedup/runbooks/escalation; runbooks are versioned and authority-bounded; bootstrap owner-only response still has explicit paging/escalation; material incidents produce evidence-driven reviews and tracked corrective/regression actions.

## HCT-DEC-0130 — FinOps uses provider-neutral cost truth, allocation and bounded AI/research budgets
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT distinguishes realtime estimates, provider-reported usage, statements, invoices and corrections; allocates costs by relevant provider/environment/tenant/capability/model/experiment dimensions where feasible; budgets AI/agent/retrieval/replay workloads; and uses FOCUS-compatible normalization where source billing data supports it.

## HCT-DEC-0131 — Infrastructure migration is driven by measured reliability, capacity and unit economics
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT tracks cost/headroom/latency per relevant tenant/account/capability/workload and uses observed reliability/security/capacity economics rather than customer count alone to trigger infrastructure upgrades. Operational dashboards preserve a truth hierarchy so forecasts/cost scores never masquerade as authoritative facts.

## HCT-DEC-0132 — Trading authority composes as a restrictive lattice, not a relaxable sequential chain
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: exchange capability, Security/Tenant, Harness restrictions, Safety, Session Policy, Risk, data authority/freshness, reconciliation/protection and promotion/environment eligibility independently deny or tighten live-capable actions. No later module may relax a stricter decision from another authoritative domain.

## HCT-DEC-0133 — Position sizing/leverage use a two-phase proposal then final Risk approval
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: Position Sizing and Leverage produce bounded construction proposals; Risk then computes the projected post-trade RiskSnapshot and may reduce/veto/recompute until one internally consistent construction is approved. Risk Reservation is committed before exposure-increasing submit.

## HCT-DEC-0134 — Every exchange mutation uses one canonical Authorization Bundle
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: state-changing exchange commands bind required SecurityContext/tenant-account scope, environment, exchange capability/rules, data-authority/freshness, Safety, Session Policy, final RiskSnapshot, Risk Reservation, action class, execution intent and Command Authorization Lease. Missing/expired/mismatched authority rejects the command.

## HCT-DEC-0135 — Canonical state families have one source-of-truth owner and projections never become competing authority
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: HCT adopts the R11 Source-of-Truth Matrix. Exchange/account truth is reconciled from the venue, domain owners maintain canonical internal state, and caches/UI/telemetry remain projections. Consumer convenience never creates a second authoritative owner.

## HCT-DEC-0136 — Realtime, memory, learning and promotion modules have explicit non-overlapping ownership boundaries
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: Quota/WS, market ingest, data quality, Market-State Fabric and cache remain distinct realtime responsibilities. RAG is the governed consumer facade over Temporal Memory; Learning Lifecycle owns candidate/version lifecycle; Promotion Laboratory remains independent proof authority and prevents self-promotion.

## HCT-DEC-0137 — Strategy, agents, Brain and Copilot are separate evidence/orchestration layers
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: Strategy/Agents/News/Memory produce or route evidence; Intelligence Brain is the canonical selective candidate-decision fusion layer; Copilot orchestrates workflow/tool/agent/action lifecycle. None becomes a parallel Safety/Risk/Execution authority.

## HCT-DEC-0138 — Environment namespace and typed identity/versioning are cross-domain invariants
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: LIVE/PAPER/SHADOW/REPLAY environment identity is part of stateful high-assurance object identity. Cross-domain IDs are typed/stable, and behaviorally material versions/hashes are explicit; mutable display labels never substitute for canonical identity.

## HCT-DEC-0139 — HCT uses an explicit dependency/failure graph and staged logical implementation DAG
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: every capability declares dependencies, action-class impact, degradation/fallback and recovery proof. Implementation planning follows the R11 logical stages from shared security/contracts through exchange/data, deterministic intelligence, capital safety, execution truth, validation, AI automation, operator surfaces and operational hardening, while allowing vertical slices and early security/audit/observability instrumentation.

## HCT-DEC-0140 — The 42 accepted modules receive explicit V1 classification without silent scope deletion
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: R11 classifies every accepted module as `V1_CORE`, `V1_MINIMUM`, `IMPORTANT_POST_V1` or `FUTURE`. V1 module readiness is distinct from live activation. Deferring an accepted V1 module later requires an explicit Decision Ledger entry with impact analysis.

## HCT-DEC-0141 — Formal round contracts override conflicting exploratory wording and R12 must consolidate requirements losslessly
Status: APPROVED_FOR_DISCOVERY
Date: 2026-09-11

Decision: approved formal round artifacts and Decisions Ledger take precedence over conflicting older exploratory/pre-discovery text. R12 must consolidate `docs/02-requirements.md` and accepted round addenda into one traceable freeze baseline without dropping accepted requirements, while preserving provider/topology neutrality and implementation/live prohibitions.
