# Nodal Strategy Graph & R&D Technologies

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R02`
Risk class: `HIGH_ASSURANCE`

## Nodal Strategy Builder
The Strategy Builder will use a graph-based visual paradigm inspired by professional node/workflow editors. Users compose strategies by adding typed nodes and connecting compatible inputs/outputs. The graph compiles to the same canonical, declarative, versioned Strategy Definition used by validation, backtest, paper trading and production runtime.

The visual graph is an authoring surface, not an execution bypass. Runtime authority remains in backend Strategy, Safety, Risk, Session Policy, Exchange Capability and Execution components.

## Candidate node families
### Market inputs
- price/OHLCV
- mark/fair/index price
- funding/open interest
- order book/liquidity
- spread/slippage estimate
- session/time/calendar
- approved news/event context
- exchange capability/context

### Indicator and feature nodes
- standard indicators
- HCT proprietary indicators exposed to users
- candlestick and chart patterns
- price structure/support/resistance
- volatility/volume/momentum/trend features
- market regime/cycle features
- historical/RAG-derived read-only context where allowed

### Logic nodes
- AND / OR / NOT
- threshold/comparison
- crossover/crossunder
- slope/rate-of-change
- persistence/window
- N-of-M confirmation
- weighted evidence
- multi-timeframe join
- regime gate
- cooldown/debounce
- state machine / phase gate

### Decision nodes
- LONG_CANDIDATE
- SHORT_CANDIDATE
- WAIT
- NO_TRADE
- REDUCE
- EXIT
- INVALIDATE

### Position-management nodes
- stop-loss
- take-profit
- trailing-stop
- break-even
- partial exits
- time-based exit
- volatility-adjusted exit
- invalidation exit

### Safety/risk references
User graphs may reference platform-safe risk values or impose stricter limits, but cannot create nodes that weaken platform risk/safety ceilings.

## Typed graph contract
Every node has:
- stable node type ID;
- schema version;
- typed inputs/outputs;
- deterministic parameter schema where applicable;
- data/timeframe dependencies;
- capability requirements;
- compute-cost class;
- warmup/history requirements;
- provenance/version metadata;
- validation rules;
- runtime eligibility state.

Invalid links are rejected visually and by backend validation. Example: a Boolean output cannot be connected directly to a numeric-period input without an explicit conversion/aggregation node.

## Graph compilation
Conceptual flow:
`Visual Graph -> Graph Validation -> Typed Intermediate Representation -> Canonical Strategy Definition -> Static Analysis -> Backtest/Paper Runtime -> Production Runtime`

The graph layout itself is UI metadata. Trading semantics live in the canonical compiled definition so moving a node on screen never changes strategy behavior.

## Debugging and observability
The builder should support:
- live node-state inspection;
- per-node input/output preview;
- timeline playback against historical data;
- breakpoint/watch nodes in research mode;
- branch highlighting showing why a signal did/did not fire;
- graph-level warnings and errors;
- data freshness indicators;
- execution trace overlay on the chart;
- comparison between strategy versions.

Production mode remains deterministic and auditable; debugging features cannot alter live semantics.

## New HCT R&D technology candidates
The following are research candidates, not production claims.

### 1. HCT Strategy Graph Static Analyzer (SGSA)
Analyzes a graph before runtime for impossible branches, contradictory conditions, missing exits, unreachable nodes, circular dependencies, lookahead leakage risks, unavailable data and unsafe capability requirements.

### 2. HCT Signal Redundancy Mapper (SRM)
Maps correlation/mutual-information relationships between indicator branches and warns when a visually complex strategy is effectively repeating the same evidence many times.

### 3. HCT Strategy DNA Fingerprint (SDF)
Produces a compact behavioral fingerprint describing what a strategy actually depends on: trend/momentum/volatility/liquidity/timeframe concentration, turnover, holding horizon, regime sensitivity and risk shape. Used for comparison, clustering and portfolio diversification of strategies.

### 4. HCT Counterfactual Trade Debugger (CTD)
After a trade or missed trade, replays nearby alternatives such as slightly later entry, tighter/wider stop, removal of one confirmation, different timeframe or disabled node. It is an analysis tool, not an automatic retroactive optimizer.

### 5. HCT Graph Sensitivity Heatmap (GSH)
Measures how strategy behavior changes when safe parameters are perturbed. Visually marks brittle nodes/edges where tiny parameter changes produce large outcome changes. Feeds Signal Fragility research and overfitting detection.

### 6. HCT Node Attribution Ledger (NAL)
For each candidate/trade, records which nodes contributed positively, negatively, vetoed, or were irrelevant. Enables explainability, post-trade analysis and RAG retrieval without reducing a decision to one opaque score.

### 7. HCT Regime Compatibility Matrix (RCM)
Learns/evaluates which approved strategies and graph substructures have historically behaved acceptably in specific regimes. May lower suitability or recommend NO_TRADE, but cannot override hard safety/risk.

### 8. HCT Strategy Graph Optimizer (SGO)
Research-only system that may suggest removing redundant nodes, simplifying branches or proposing candidate parameter ranges based on governed experiments. Suggestions never silently modify production strategies; every change creates a new version and requires validation.

### 9. HCT Shadow Twin Runtime (STR)
Runs a non-authoritative shadow copy of a live strategy version or candidate revision against the same realtime feed, allowing comparison of live-approved versus proposed behavior without placing duplicate orders.

### 10. HCT Opportunity Path Visualizer (OPV)
Shows the real decision path from raw market data through graph nodes, proprietary indicators, strategy conditions, agents, Safety, Risk and Execution. Intended to make the product's 'living organism' behavior inspectable in realtime.

### 11. HCT Graph Cost & Latency Estimator (GCLE)
Estimates compute, data, API/subscription and latency requirements before a strategy is enabled. Prevents a user graph from creating unreasonable resource pressure across a multi-tenant environment.

### 12. HCT Strategy Portfolio Correlation Engine (SPCE)
Measures behavioral and realized correlation between multiple user/default strategies so apparently different strategies do not accidentally multiply the same market exposure.

## Safety constraints
- no arbitrary user code in V1;
- no graph node can expose secrets/filesystem/process/network primitives;
- no node can directly sign/send exchange orders;
- execution nodes compile only to candidate intents handled by governed backend services;
- no research optimizer can self-promote or mutate a live strategy;
- every live graph has immutable version/hash and exact runtime dependency versions;
- strategy graphs remain tenant-isolated.

## UX direction
The editor should feel spatial and exploratory: searchable node palette, drag/drop canvas, zoom/pan/minimap, typed ports, grouped frames, reusable subgraphs/macros, comments, graph validation badges, chart preview and simulation controls. Safety/risk states use unambiguous visual priority over decorative effects.
