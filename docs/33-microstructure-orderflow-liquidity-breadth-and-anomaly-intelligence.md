# Microstructure, Order-Flow, Liquidity, Breadth & Anomaly Intelligence

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R02`
Risk class: `HIGH_ASSURANCE`

## Objective
Transform HCT's realtime market-state infrastructure into low-latency, explainable market intelligence that can detect pressure, fragility, liquidity shifts, cross-asset propagation and abnormal behavior earlier than slow aggregate indicators alone.

This layer is an evidence engine, not a guarantee of profitability. All proprietary signals begin as research hypotheses and require leakage-safe validation, realistic fees/slippage, out-of-sample/walk-forward evidence, replay/paper/shadow evaluation and promotion governance.

Bootstrap constraint: the V1 design must remain compatible with the `Free-first, not free-at-any-cost` infrastructure policy. Expensive dedicated streaming/feature-store infrastructure is optional until measurements justify it.

## Architecture position

`Exchange market events -> canonical market state -> microstructure/order-flow features -> liquidity/breadth/lead-lag/anomaly intelligence -> Feature Store -> Scanner/Indicators/Strategies/Agents/Brain -> Safety/Risk/Execution`

The layer never executes orders directly.

## Research basis
Current 2026 research continues to support order-book imbalance, microprice/order-flow information, spread and adverse-selection features as meaningful short-horizon microstructure variables in crypto, while also demonstrating that execution assumptions and maker/taker behavior materially change realized results. HCT therefore separates predictive research from tradability/execution validation.

## Feature families

### 1. Order-book structure
Candidate features:
- L1/LN bid-ask imbalance;
- weighted depth imbalance;
- depth slope and convexity;
- microprice and microprice displacement from mid;
- spread, relative spread and spread regime;
- distance/size to visible liquidity walls;
- replenishment after aggressive trades;
- cancellation/addition velocity;
- queue-shape change;
- depth resilience after impact;
- book pressure persistence;
- local-book entropy/concentration;
- bid/ask asymmetry by distance from mid;
- near-touch liquidity migration.

### 2. Trade-flow / aggressor behavior
Candidate features:
- buy/sell aggressor imbalance;
- signed trade flow;
- rolling trade-flow imbalance;
- volume-at-price pressure;
- trade-size distribution shift;
- large-trade burst detection;
- aggressive-flow persistence;
- price response per unit aggressive volume;
- impact asymmetry for buys versus sells;
- absorption signatures;
- exhaustion signatures;
- trade clustering and inter-arrival acceleration.

### 3. Liquidity intelligence
Candidate features:
- effective visible liquidity by price distance;
- liquidity vacuum detection;
- spread/depth stress;
- depth decay speed;
- refill/replenishment speed;
- execution-capacity estimate;
- expected impact curve;
- liquidity regime classification;
- transient versus persistent liquidity;
- fragility under hypothetical market-order sizes;
- slippage surface by size;
- stop-density proxy where inferable only from public market behavior, never from invented hidden orders.

### 4. Alternative bars
Research beyond fixed time candles:
- volume bars;
- tick bars;
- dollar/notional-volume bars;
- volatility bars;
- event bars;
- imbalance bars;
- run bars;
- adaptive bars triggered by information arrival.

Every bar type is canonical/versioned and must preserve point-in-time reproducibility. Alternative bars are research features until they demonstrate incremental value over time bars.

### 5. Cross-asset lead/lag intelligence
Goal: detect whether one market or market cluster tends to move before another under specific regimes.

Candidate relationships:
- BTC -> major alt beta;
- ETH -> ecosystem assets;
- sector/narrative leaders -> followers;
- index/breadth -> individual symbol;
- volatility leader -> lagging symbols;
- funding/OI shocks -> price/liquidity response;
- market-wide liquidation/flow proxies -> correlated contracts.

Methods may include lagged correlation, cross-correlation, Granger-style research, transfer entropy research, directed information approximations, dynamic time warping for pattern alignment, regime-conditioned lead/lag and event-study analysis.

No relationship is assumed permanent. Lead/lag edges are versioned, decayed and revalidated.

### 6. Market breadth intelligence
HCT should maintain crypto-futures breadth features such as:
- advance/decline ratio;
- percentage above/below selected trend measures;
- percentage in volatility expansion;
- percentage with positive/negative momentum;
- cross-sectional dispersion;
- correlation compression/expansion;
- breadth thrust/exhaustion;
- volume breadth;
- liquidity breadth;
- funding breadth;
- open-interest breadth;
- long/short opportunity breadth;
- fraction of market in abnormal/degraded state.

Breadth can distinguish an isolated coin move from a market-wide impulse.

### 7. Anomaly intelligence
Anomaly detection should combine deterministic and model-assisted methods.

Candidate anomalies:
- sudden spread widening;
- depth collapse;
- crossed/incoherent book;
- extreme order-flow burst;
- price move unsupported by normal liquidity;
- abnormal volume/volatility coupling;
- cross-asset decorrelation;
- correlation-to-one stress regime;
- funding/OI dislocation;
- abrupt microprice divergence;
- flash-crash / rebound signature;
- stale/frozen market feed versus active peer markets;
- abnormal feature-distribution shift.

Model candidates may include robust z-scores, EWMA/CUSUM, change-point detection, isolation methods, robust covariance, streaming quantile models, online density estimates and governed ML. Complexity must earn its cost through benchmarked incremental value.

## Proprietary HCT R&D technologies

### 1. HCT Liquidity Topology Map (LTM)
A multi-distance representation of where liquidity is concentrated, migrating or disappearing around current price. Intended to distinguish a visually large book from genuinely executable depth.

### 2. HCT Liquidity Vacuum Probability (LVP)
Research score estimating the risk that price can traverse a nearby region quickly because executable depth is thin, unstable or being withdrawn.

### 3. HCT Order-Flow Pressure Tensor (OFPT)
Multi-horizon, multi-depth representation of aggressor pressure, book imbalance, microprice displacement and response efficiency instead of one scalar imbalance value.

### 4. HCT Absorption & Exhaustion Matrix (AEM)
Attempts to distinguish aggressive flow that moves price from aggressive flow absorbed without proportional movement, including horizon and side asymmetry.

### 5. HCT Liquidity Replenishment Half-Life (LRHL)
Measures how quickly depleted depth tends to rebuild after impact. Slow replenishment may indicate a fragile market; fast replenishment may indicate resilient liquidity.

### 6. HCT Market Impact Elasticity (MIE)
Versioned estimate of price movement per unit of aggressive notional at different sizes and regimes. Used by execution and risk as evidence, not a guaranteed fill model.

### 7. HCT Flow-to-Price Efficiency (FPE)
Measures how efficiently signed flow converts into price displacement. Divergence can help detect absorption, exhaustion or changing market-maker behavior.

### 8. HCT Microstructure Regime Vector (MRV)
State vector combining spread, depth, replenishment, flow, volatility, impact and quote stability to classify microstructure regimes independently from slower price-trend regimes.

### 9. HCT Cross-Asset Propagation Graph (CAPG)
Dynamic directed graph of empirically observed lead/lag and shock propagation relationships among futures contracts. Edges carry horizon, regime, confidence, decay and evidence window.

### 10. HCT Propagation Confidence Score (PCS)
Rates whether an observed leader move has historically propagated reliably enough in a comparable regime to become supporting evidence for a lagging symbol.

### 11. HCT Breadth Pressure Field (BPF)
Cross-sectional field summarizing direction, momentum, volatility, liquidity and derivatives pressure across the eligible universe rather than a single advance/decline count.

### 12. HCT Breadth Divergence Alarm (BDA)
Detects when a major asset move is unsupported or contradicted by broader market participation, or when breadth moves before headline assets.

### 13. HCT Correlation Compression Sentinel (CCS)
Tracks rising common-factor dependence and the tendency for many symbols to collapse into one effective market exposure during stress.

### 14. HCT Shock Propagation Velocity (SPV)
Measures how rapidly a market shock spreads from leaders to related assets and whether propagation is accelerating or stalling.

### 15. HCT Market Anomaly Composite (MAC)
Explainable ensemble of deterministic and statistical anomaly detectors with component scores and reason codes. It must never be an opaque veto without traceability.

### 16. HCT Regime Change Early Warning (RCEW)
Combines microstructure, breadth, volatility and correlation change points to flag a possible regime transition before slower indicators fully reclassify.

### 17. HCT Feature Freshness Vector (FFV)
Every realtime decision receives per-feature age, source generation, freshness lease and validity status rather than one global `fresh=true` flag.

### 18. HCT Feature Coherence Score (FCS)
Measures whether the features entering one decision were built from compatible market-state generations and event-time windows.

### 19. HCT Feature Value Density (FVD)
Research metric estimating incremental predictive/decision value per unit of CPU, memory, bandwidth and latency. Designed specifically for the bootstrap free-infrastructure phase so expensive features can be disabled if they do not earn their resource budget.

### 20. HCT Adaptive Feature Tiering (AFT)
Classifies features as `CRITICAL`, `HOT`, `WARM`, `COLD` or `RESEARCH` depending on strategy needs, symbol priority, market velocity and resource pressure. Safety/execution features always outrank research extras.

### 21. HCT Opportunity Precognition Window (OPW)
Research-only measure of how early a microstructure/breadth/lead-lag signal begins to improve decision quality before a conventional strategy trigger. The name describes lead time, not literal prediction certainty.

### 22. HCT Adverse Selection Risk Index (ASRI)
Estimates the risk that apparently attractive liquidity is likely to become toxic immediately after entry, using flow, spread, impact, volatility and book-instability evidence.

### 23. HCT False Liquidity / Ephemerality Score (FLES)
Measures visible depth persistence and cancellation behavior to discount highly transient order-book liquidity. It is not a claim of detecting illegal spoofing without evidence.

### 24. HCT Multi-Horizon Flow Consensus (MHFC)
Combines flow evidence across milliseconds/seconds/minutes while discounting redundant windows and exposing disagreement between horizons.

### 25. HCT Information Arrival Rate (IAR)
Measures event intensity and surprise to drive adaptive compute, subscription priority, alternative-bar generation and signal-decay behavior.

## Realtime Feature Store architecture
HCT should define a logical `RealtimeFeatureStore` interface with:
- canonical feature key;
- feature schema/version;
- symbol/instrument identity;
- event-time and compute-time;
- market-state generation ID;
- freshness lease/expiry;
- provenance/dependencies;
- value and quality flags;
- optional uncertainty/confidence;
- feature family;
- compute-cost class.

The store is not a permanent truth database. It serves current validated features to low-latency consumers while durable/replay paths retain sufficient source evidence for reconstruction.

### Bootstrap implementation
For owner/early users, prefer an in-process memory store plus bounded persistence for essential snapshots where safe, avoiding per-tick cloud round trips and command-metered external caches.

Candidate bootstrap pattern:
`MEXC WS -> local trading worker -> in-process market state + feature cache -> strategy/agents/risk/execution`

Supabase remains metadata/audit/application persistence, not the per-event feature hot path. Upstash/Redis-compatible free tiers can be used selectively for coordination/session data, not every tick/feature update.

### Scale path
Only after benchmarks justify it, evaluate Redis/Valkey/Dragonfly or a formal feature-store framework such as Feast for shared online feature serving. Current Feast supports multiple online stores including Redis, PostgreSQL and Dragonfly, but adding a feature-store framework is not a V1 requirement.

## Computation model
Use incremental computation whenever possible:
- update rolling statistics instead of recomputing entire windows;
- share common primitives among multiple features;
- update only symbols/timeframes affected by new events;
- precompute reusable order-book aggregates;
- vectorize/batch cold analytics where useful;
- keep critical hot path free from research-only joins;
- use bounded ring buffers for short histories;
- avoid serialization/network hops for same-process hot-path consumers during bootstrap.

## Scanner cascade integration
Microstructure compute must be staged:

`full universe -> cheap breadth/liquidity screening -> shortlist -> richer order-flow/depth features -> deep microstructure/agent analysis -> candidate`

This prevents high-cost L2 analysis of every contract at full fidelity when no opportunity exists.

## Brain integration contract
Microstructure evidence presented to strategies/agents/brain must include:
- feature values;
- timestamps/ages;
- source/generation;
- integrity/confidence;
- expected horizon/half-life;
- regime;
- conflicting evidence;
- provenance;
- validation status (`RESEARCH`, `PAPER`, `PRODUCTION_ELIGIBLE`, etc.).

The brain may not treat a research-only feature as production-authoritative without promotion.

## Risk and execution integration
Microstructure can:
- reduce opportunity confidence;
- improve entry timing;
- reject stale/fragile opportunities;
- reduce size;
- lower permitted leverage;
- widen execution scrutiny;
- prefer wait/no-trade;
- inform slippage/impact budgets;
- inform liquidity caps;
- trigger execution degradation.

It cannot increase hard risk ceilings or bypass Safety/Risk/Session Policy.

## Validation protocol
For every proprietary microstructure feature/model:
1. point-in-time dataset lock;
2. feature timestamp audit;
3. leakage checks;
4. baseline comparison;
5. ablation/incremental-value test;
6. multiple assets and regimes;
7. walk-forward/OOS;
8. fee/slippage/funding-aware simulation where relevant;
9. maker/taker sensitivity where relevant;
10. turnover and capacity analysis;
11. paper/shadow deployment;
12. drift monitoring;
13. independent promotion review.

Metrics should include calibration/precision where applicable, information coefficient or suitable predictive metric, decision utility, net expectancy after realistic costs, drawdown interaction, false-positive cost, latency/resource cost and stability across regimes.

## Guard against overfitting
HCT must not maximize the count of proprietary indicators. A smaller set with stable incremental value is preferable to dozens of correlated features.

Candidate features can be retired when they:
- lose OOS value;
- become redundant;
- consume disproportionate compute;
- increase turnover without net benefit;
- become too sensitive to parameters;
- fail after market structure changes.

## Cockpit visualization
The premium cockpit may expose:
- liquidity topology heatmap;
- order-flow pressure;
- microprice versus mid;
- aggressor-flow ribbon;
- impact/slippage surface;
- breadth pressure field;
- cross-asset propagation graph;
- anomaly timeline;
- microstructure regime;
- feature freshness/coherence;
- signal half-life;
- explanation of which microstructure evidence affected a trade.

Visuals must clearly distinguish raw observed data, derived production features and experimental research overlays.

## Cost/performance rule
During the bootstrap phase, every high-cost realtime feature must justify itself through `Feature Value Density`: measurable incremental value relative to compute/network/storage cost.

The design priority is:
`correctness -> freshness -> safety -> useful information -> latency -> cost -> feature count`.

## No-profit-guarantee rule
The objective is to improve validated opportunity capture and reduce avoidable execution/risk mistakes. No microstructure feature, lead/lag relationship, anomaly detector or proprietary technology is represented as guaranteeing user profit.