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
