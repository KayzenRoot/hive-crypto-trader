# User Strategy Builder & Default Strategy Catalog

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R02`
Risk class: `HIGH_ASSURANCE`

## Objective
Hive Crypto Trader must support both a curated catalog of built-in strategies and user-authored strategies. User flexibility is a first-class product requirement, but user-authored logic remains subordinate to deterministic Safety, Risk, exchange constraints, tenancy policy and entitlement boundaries.

## Strategy Catalog
The product should launch with a clear, versioned set of approximately 10–15 built-in strategy templates. Each strategy must explain:
- what market condition it targets;
- preferred regime(s);
- supported direction(s): long, short or both;
- required indicators/features;
- timeframe template;
- entry conditions;
- confirmation conditions;
- invalidation/exit logic;
- stop-loss policy;
- take-profit/trailing options;
- known failure modes;
- suitability and limitations;
- historical validation status/version;
- whether it is production-approved, experimental, paper-only or disabled.

## Candidate built-in V1 strategy families
The exact formulas and production parameters remain to be validated. Candidate initial catalog:
1. Trend Following
2. Pullback Continuation
3. Breakout / Volatility Expansion
4. Momentum Continuation
5. Mean Reversion / Range
6. Reversal / Exhaustion
7. Multi-Timeframe Confluence
8. Support/Resistance Structure
9. Liquidity / Microstructure Confirmation
10. Volume Participation / Expansion
11. Volatility Compression-to-Expansion
12. Regime-Adaptive Hybrid
13. Funding / Derivatives Context Strategy
14. False-Breakout Avoidance / Re-entry
15. HCT Proprietary Composite Strategy

These names define research families, not promises of profitability. Every production template requires governed validation and versioning.

## User Strategy Builder
Users may create private strategies using a first-class nodal visual builder and, where appropriate, an advanced structured rule editor. The nodal paradigm is an architectural product requirement: users add typed nodes, connect compatible ports and compose a strategy graph visually. Strategies remain representable as a validated Strategy Definition rather than arbitrary executable server code.

The node graph and advanced editor compile to the same canonical Strategy Definition. Visual layout changes do not alter trading semantics unless actual graph logic/parameters change.

### Candidate building blocks
- indicators and their parameters;
- proprietary HCT indicators explicitly exposed to users;
- candlestick/pattern conditions;
- price/market-structure rules;
- volume/participation conditions;
- volatility conditions;
- funding/open-interest/derivatives context where available;
- liquidity/spread/order-book context where available;
- market regime filters;
- multi-timeframe conditions;
- news/event filters where supported;
- time/session/day filters;
- symbol/universe filters;
- long/short/both direction;
- AND / OR / NOT / grouped Boolean logic;
- threshold, crossover, slope, change, distance and persistence conditions;
- confirmation count/window;
- cooldown conditions;
- entry, add, reduce, exit and invalidation rules;
- stop-loss, take-profit, trailing and partial-exit policies;
- optional Strategy Builder variables/parameters within safe bounds.

## Example conceptual rule
`IF 1H trend is bullish AND 15M pullback reaches configured EMA zone AND 5M momentum turns positive AND HCT False Breakout Probability < threshold AND liquidity is acceptable THEN create LONG_CANDIDATE`.

The result is still a candidate signal. It must pass Safety Governor, Risk Engine, Session Policy, Position Sizing, exchange capability checks and execution policy.

## Nodal graph direction
The builder should support typed node families for market inputs, indicators/features, logic, multi-timeframe aggregation, regime filters, decision intents and position-management policies. Invalid connections are rejected before runtime. Reusable subgraphs/macros may package recurring logic while remaining expanded/auditable in the compiled strategy definition.

Conceptual authoring path:
`Node Palette -> Visual Graph -> Typed Validation -> Canonical Strategy Definition -> Static Analysis -> Backtest/Paper -> Governed Live Eligibility`.

See `docs/24-nodal-strategy-graph-and-rd-technologies.md` for the deeper graph architecture and R&D technologies.

## Strategy Definition / DSL
Use a declarative, versioned strategy schema/DSL rather than allowing users to upload arbitrary executable code in V1. Candidate sections:
- metadata and ownership;
- strategy version;
- applicable market/exchange capability requirements;
- parameter schema;
- timeframe roles;
- feature dependencies;
- entry rules;
- exit rules;
- protective-order policy;
- position-management rules;
- risk constraints that can only tighten platform limits;
- validation status;
- compatibility matrix;
- audit/provenance information.

A visual builder should compile to the same canonical Strategy Definition used by advanced tooling, backtests and runtime evaluation.

## Validation workflow
User strategies should progress through states such as:
`DRAFT -> VALIDATED_SCHEMA -> STATIC_ANALYZED -> BACKTESTED -> PAPER_READY -> PAPER_RUNNING -> USER_APPROVED_FOR_LIVE -> LIVE_ELIGIBLE`

Platform policy may require minimum validation before live use. HIGH_ASSURANCE safeguards remain mandatory.

## Strategy sandbox
Before live use, provide:
- syntax/schema validation;
- graph type validation;
- unreachable/contradictory branch analysis;
- unavailable-indicator detection;
- unsupported exchange-capability detection;
- timeframe consistency checks;
- lookahead/leakage checks where applicable;
- conflict and redundancy analysis;
- estimated compute/latency cost;
- API/data dependency analysis;
- backtest/replay;
- paper trading;
- safety-policy validation.

## Strategy versioning and reproducibility
Every edit creates a new immutable strategy version for executed/paper decisions. Trading traces must record the exact strategy version, graph hash and parameter snapshot. Editing a live strategy must never retroactively mutate prior evidence.

## Sharing and commercialization readiness
V1 may keep custom strategies private. Architecture should allow future strategy templates, import/export, controlled sharing, marketplace or plan-based entitlements without redesigning the core Strategy Definition.

## Security boundary
A user-defined strategy cannot:
- execute arbitrary backend code;
- access filesystem/process/network primitives;
- access another tenant's data;
- read exchange secrets;
- bypass Safety/Risk/Session Policy;
- raise platform maximum leverage/risk;
- create unsupported exchange operations;
- disable audit/reconciliation.

## UX direction
The Strategy Builder should offer:
- searchable node palette;
- drag/drop canvas;
- typed ports and visual compatibility;
- zoom/pan/minimap;
- grouped frames and comments;
- reusable subgraphs/macros;
- human-readable explanation of resulting logic;
- realtime chart preview;
- selected indicators/timeframes as overlays;
- live/replay node-state inspection in research mode;
- warnings for redundant/conflicting conditions;
- estimated complexity/data/latency requirements;
- backtest/paper results;
- strategy version/history;
- save/clone/compare workflow.
