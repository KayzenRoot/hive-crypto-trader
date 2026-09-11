# Temporal Market Memory, RAG & Continual Learning

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R02`
Risk class: `HIGH_ASSURANCE`

## Objective
Design HCT's market memory as a temporal, event-aware and regime-aware institutional memory rather than a generic embedding store. The system must remember what happened, when it happened, under which market regime, what evidence was known at decision time, what action was taken, what actually happened afterward, and how reliable the lesson remains today.

The learning objective is not unrestricted self-modification. HCT may retrieve analogs, estimate similarity, detect drift, propose model/strategy/feature updates and learn from post-trade outcomes, but production authority remains governed by explicit validation, promotion and rollback gates.

## Core principles
1. **Time is first-class.** Retrieval must preserve chronology, event validity windows and information available at the historical decision point.
2. **Causality is not inferred from proximity.** Correlation, temporal order and causal hypothesis are stored separately.
3. **No future leakage.** Historical analog retrieval must exclude information that was unavailable at the original decision timestamp.
4. **Regime-aware memory.** Similar price shapes from incompatible regimes are not equivalent evidence.
5. **Outcome-aware but not outcome-dominated.** Memory records outcomes while preserving ex-ante evidence to avoid hindsight bias.
6. **Recent and global history coexist.** Recent market behavior can matter more during fast drift while global history preserves recurring patterns.
7. **Learning is reversible.** Every promoted change is versioned, benchmarked and rollback-capable.
8. **Evidence over narrative.** Structured episodes/events are canonical; LLM-generated summaries are derived views.

## Memory classes
### 1. Immutable decision memory
For every material candidate and trade:
- decision timestamp;
- market-state generation id;
- symbol/instrument;
- strategy/version;
- feature/version snapshot;
- regime state;
- agent evidence board;
- news/event context available at the time;
- risk state;
- execution feasibility;
- decision outcome (`LONG_CANDIDATE`, `WAIT`, `NO_TRADE`, etc.);
- order intent if any;
- reason codes;
- model/skill/tool versions;
- data-confidence state.

This record must never be rewritten by later knowledge.

### 2. Market episode memory
An episode is a bounded temporal segment representing a coherent setup and its aftermath.

Candidate fields:
- episode id;
- start/end timestamps;
- symbol and cross-asset cluster;
- regime labels;
- market microstructure summary;
- multi-timeframe feature vector;
- liquidity/volatility state;
- event/news context;
- strategy candidates;
- expected horizon;
- subsequent path statistics;
- maximum favorable/adverse excursion;
- execution conditions;
- fees/slippage/funding;
- result classification;
- anomaly tags;
- confidence and provenance.

### 3. Event memory
Structured temporal events including macro, regulatory, exchange, protocol, security, token-specific and abnormal market events.

Each event has:
- event time;
- detection time;
- publication time;
- source reliability;
- affected symbols/classes;
- expected/observed horizon;
- contradiction/corroboration links;
- impact observations;
- expiry/decay.

### 4. Strategy memory
Tracks performance by:
- strategy version;
- symbol;
- regime;
- timeframe;
- liquidity bucket;
- volatility bucket;
- event state;
- execution regime;
- recent versus long-term windows.

### 5. Model/feature memory
Stores:
- training/evaluation dataset identity;
- feature versions;
- calibration history;
- drift indicators;
- errors by regime;
- false positive/negative patterns;
- shadow/champion-challenger results;
- retirement/quarantine reasons.

### 6. Operational memory
Incidents and recovery episodes:
- exchange disconnects;
- stale data;
- order uncertainty;
- reconciliation mismatch;
- rate-limit events;
- partial-fill anomalies;
- protective-order failures;
- infrastructure degradation.

Operational lessons must remain separate from market-alpha memory but can affect safety/execution policy.

## Temporal retrieval architecture
Generic nearest-neighbor vector similarity is insufficient. Retrieval should combine multiple channels:

`Query Context -> Temporal Filter -> Regime Filter -> Symbol/Cluster Filter -> Structured Similarity -> Vector Similarity -> Event-Graph Expansion -> Reliability/Relevance Ranking -> Analog Set`

Candidate dimensions:
- price/return trajectory similarity;
- volatility trajectory;
- order-flow/microstructure similarity;
- breadth state;
- regime similarity;
- liquidity similarity;
- funding/open-interest state;
- news/event context;
- strategy state;
- execution environment;
- recency;
- historical reliability.

## HCT Temporal-Causal Memory Graph
R&D candidate inspired by modern event-centric/temporal graph retrieval, adapted to trading.

Separate graph concepts:
- `Entity`: symbol, asset, exchange, sector, macro factor, event source, strategy, model;
- `Event`: price shock, news release, funding spike, liquidity vacuum, breakout, incident, trade decision;
- `Relation`: leads, follows, coincides-with, affects, contradicts, corroborates, belongs-to-regime, executed-by, invalidated-by;
- `Validity interval`: when relation/event evidence was active;
- `Knowledge timestamp`: when HCT first knew it.

Crucially, `event_time` and `knowledge_time` are distinct to prevent future leakage.

## Global + Recent Memory Router
Markets exhibit both recurring historical structure and fast-changing local behavior.

HCT should retrieve from two memory horizons:
- **Global Memory:** long historical archive emphasizing recurrence and broad regime analogs.
- **Recent Memory:** high-weight recent episodes emphasizing current drift and local behavior.

The router estimates how much weight each deserves according to:
- detected drift;
- regime stability;
- recent forecast error;
- calibration change;
- liquidity/volatility transition;
- event density;
- symbol behavior shift.

Research metric: **HCT Historical Relevance Horizon (HRH)**, estimating how far back useful evidence remains predictive in the current state.

## Historical Analog Engine
Purpose: answer questions such as:
- When has this symbol/cluster exhibited a similar regime + order-flow + liquidity configuration?
- What happened over 5m, 15m, 1h, 4h afterward?
- How did comparable strategies perform?
- What were common failure modes?

Analog retrieval returns a distribution, not a single anecdote.

Example output:
```text
Current setup: SOLUSDT
Regime: high-volatility bullish expansion
Microstructure: aggressive buying + thinning asks
Breadth: strong
Event risk: low

Comparable episodes: 184
High-quality analogs: 37

15m outcomes:
positive continuation: 54%
mean-revert: 30%
flat/noise: 16%

Median MFE: +0.84%
Median MAE: -0.31%
Confidence: MODERATE
Drift penalty: 0.18
```

This is evidence for the Brain, never direct order authority.

## New HCT R&D technologies
### 1. Analog Reliability Score (ARS)
Scores how trustworthy an analog set is based on sample size, regime match, feature coherency, temporal distance, execution similarity and drift.

### 2. Temporal Leakage Firewall (TLF)
Enforces point-in-time retrieval. Every feature/event/news item must prove it existed before the historical decision time.

### 3. Regime-Conditioned Similarity Kernel (RCSK)
Similarity weights change by regime. Features important during a liquidity shock may receive different weights during a quiet trend.

### 4. Historical Relevance Horizon (HRH)
Estimates how rapidly old evidence loses relevance for a symbol/strategy/regime.

### 5. Memory Freshness Decay Surface (MFDS)
Applies multi-dimensional decay rather than simple age decay. A lesson can age quickly in one regime and remain useful for years in another.

### 6. Counterfactual Episode Memory (CEM)
Stores what would have happened under bounded alternative actions during replay/shadow testing: wait, enter later, smaller size, alternative exit, no trade. Never rewrites actual history.

### 7. Hindsight Bias Guard (HBG)
Separates ex-ante evidence from ex-post outcomes and prevents learned summaries from describing future information as if it had been known earlier.

### 8. Failure Pattern Miner (FPM)
Clusters losing/invalidated trades by recurring causes: stale signal, false breakout, liquidity vacuum, event shock, correlated exposure, execution degradation, strategy-regime mismatch.

### 9. Success Fragility Analyzer (SFA)
Tests whether profitable episodes depended on a fragile combination of lucky fill, unusually low slippage, single event or narrow parameter range.

### 10. Memory Diversity Score (MDS)
Detects when retrieved analogs are near-duplicates from one period rather than genuinely independent historical evidence.

### 11. Recurrence Strength Index (RSI-HCT)
Measures whether a pattern genuinely recurs across independent regimes/time periods/assets rather than being concentrated in one era.

### 12. Episode Surprise Score (ESS)
Measures how much actual outcome differed from the system's ex-ante expected distribution. High-surprise episodes become priority learning material.

### 13. Regime Memory Conflict Score (RMCS)
Detects when global history and recent history disagree strongly.

### 14. Learning Value Score (LVS)
Prioritizes episodes for expensive analysis based on surprise, financial impact, novelty, recurrence potential, model disagreement and data quality.

### 15. Knowledge Contamination Score (KCS)
Estimates whether a memory item is low quality due to uncertain source, future leakage, inconsistent timestamps, retrospective edits or low-confidence reconstruction.

### 16. Strategy Lesson Attribution Ledger (SLAL)
Links each proposed strategy/model change to specific episodes, evidence and evaluation results.

### 17. Concept Drift Tensor (CDT)
Tracks drift across multiple dimensions simultaneously: returns, volatility, liquidity, microstructure, correlations, feature importance, calibration and execution quality.

### 18. Drift Localization Engine (DLE)
Answers: what changed? Symbol, regime, feature family, strategy, horizon, liquidity state or execution environment.

### 19. Catastrophic Forgetting Sentinel (CFS)
Ensures adaptation to recent markets does not destroy competence in recurring older regimes.

### 20. Experience Replay Governor (ERG)
Builds balanced replay datasets across regimes, symbols, successes/failures and rare stress events.

### 21. Regime Expert Bank (REB)
Candidate architecture: maintain specialized models/experts for distinct regimes and route among them rather than forcing one model to learn everything.

### 22. Champion-Challenger Memory Arena (CCMA)
New models/strategies run shadow comparisons against production versions on identical event streams before promotion.

### 23. Forecast Calibration Memory (FCM)
Stores predicted probabilities versus realized frequencies by regime/horizon to measure calibration drift.

### 24. Decision Regret Decomposition (DRD)
Separates regret caused by bad signal, risk sizing, execution, timing, exit or data quality instead of labeling every losing trade 'bad strategy'.

### 25. Memory-to-Decision Attribution (MDA)
Records which retrieved analogs/events materially influenced a decision and whether they improved or degraded it.

## Continual learning architecture
Production learning must not mean live unrestricted gradient updates.

Candidate lifecycle:
`Observe -> Store immutable episode -> Label when outcome matures -> Drift analysis -> Candidate dataset -> Offline/controlled update -> Backtest -> Walk-forward -> OOS -> Replay -> Paper -> Shadow -> Champion/Challenger -> Governance review -> Promotion`

Online components may update safe statistics such as:
- rolling calibration;
- drift measures;
- feature distributions;
- analog weights inside bounded policy;
- regime probabilities;
- reliability estimates.

Model parameters that affect trading decisions require governed promotion unless a later explicitly validated online-learning policy is approved.

## Drift model
Distinguish at least:
- sudden/micro drift;
- gradual drift;
- recurring regime drift;
- structural/macro drift;
- execution/infrastructure drift;
- source/data drift.

The system must avoid the naive response `drift detected -> retrain everything`.

Flow:
`Detect -> Localize -> Determine severity -> Compare historical recurring concepts -> Choose adaptation candidate -> Validate -> Promote or reject`.

## Point-in-time data contract
Every historical record used for training/evaluation must support point-in-time correctness.

Required concepts:
- event timestamp;
- ingestion timestamp;
- knowledge timestamp;
- correction timestamp if revised;
- feature computation timestamp;
- source/version;
- market-state generation;
- data-quality flags.

Training queries must reproduce what the system could actually have known at that moment.

## Labels and maturation windows
Outcomes mature at different horizons. Do not label immediately.

Example episode can receive:
- 1m outcome;
- 5m outcome;
- 15m outcome;
- 1h outcome;
- 4h outcome;
- session outcome;
- execution outcome;
- risk outcome.

This supports horizon-specific learning and prevents one coarse PnL label from hiding useful information.

## Learning from no-trades
HCT must learn from rejected opportunities as well as executed trades.

For `WAIT`, `NO_TRADE`, `SAFETY_VETO`, `RISK_VETO` candidates, replay later evaluates:
- what happened after rejection;
- whether veto prevented loss;
- whether system was overly conservative;
- which gate caused the decision;
- counterfactual bounded outcomes.

This is essential because otherwise the dataset is selection-biased toward trades actually taken.

## Agent memory policy
Agents may read approved memory views but cannot alter canonical history.

Agent-generated lessons are proposals with:
- source episodes;
- confidence;
- scope;
- expiry;
- author agent/version;
- review status.

No agent may promote its own lesson/model/skill into production authority.

## RAG answer contract
Any material memory-backed recommendation should be able to expose:
- retrieved episode ids;
- retrieval query/context hash;
- time window;
- regime filters;
- similarity dimensions;
- source provenance;
- analog count;
- diversity;
- drift penalty;
- confidence;
- conflicts;
- model/retriever version.

## Bootstrap/free infrastructure implementation
V1 must preserve the free-first architecture.

Candidate bootstrap stack:
- PostgreSQL/Supabase Free for episode metadata, decisions, outcomes, compact feature summaries and governance records;
- `pgvector` where available/appropriate for modest semantic/vector retrieval;
- local/in-process recent-memory cache in trading worker;
- compressed selective historical episode storage rather than raw tick retention;
- offline batch similarity/reindex jobs on owner-controlled/local compute where possible;
- no mandatory managed vector database;
- no mandatory dedicated knowledge-graph database;
- no mandatory GPU inference service for basic retrieval.

Graph relationships can initially live in relational tables (`events`, `entities`, `relations`, `validity_intervals`) and migrate later if graph workload justifies a specialized database.

## Scale migration
When customer count/workload grows, benchmark candidates can include:
- dedicated Postgres/pgvector;
- specialized vector database if proven useful;
- ClickHouse/QuestDB for large episode/time-series analysis;
- graph storage if temporal graph traversal becomes a bottleneck;
- streaming/event log for durable learning pipelines;
- dedicated model-serving infrastructure.

Migration must be driven by measured query latency, dataset size, ingestion pressure, retrieval quality and cost.

## Validation requirements
Memory/RAG technologies must be evaluated on:
- temporal leakage rate;
- retrieval precision/relevance;
- analog diversity;
- regime consistency;
- calibration improvement;
- decision improvement versus no-memory baseline;
- false-confidence rate;
- stale-memory harm;
- drift handling;
- latency/cost;
- reproducibility;
- robustness under corrupted/noisy memories.

A useful RAG system must prove incremental decision value, not merely produce convincing explanations.

## Safety constraints
- Retrieved memory cannot bypass Safety/Risk/Session Policy.
- Historical profitability does not authorize higher risk.
- No self-training directly on unverified web content.
- No direct production model update from a single episode.
- No future leakage in training/retrieval.
- No retrospective mutation of canonical decisions.
- No automatic deletion of negative/failure memories because they reduce apparent performance.
- Uncertainty and conflicting historical evidence must remain visible.

## Research context snapshot — 2026-09-11
Current research reinforces several architectural choices:
- Temporal/event-centric RAG work shows that preserving event chronology and causal/temporal relationships can outperform naive embedding-only retrieval in tasks requiring temporal consistency.
- Recent temporal knowledge graph research explicitly combines global history with recent history, supporting HCT's proposed Global + Recent Memory Router.
- Continual-learning research in financial/non-stationary streams emphasizes concept drift, recurring concepts and catastrophic forgetting, supporting HCT's concept-history, replay and regime-expert approach.

These findings are research inspiration, not proof of trading edge. Every HCT adaptation must be validated on HCT-specific market, execution and cost data.
