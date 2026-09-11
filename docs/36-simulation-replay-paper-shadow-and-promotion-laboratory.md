# Simulation, Replay, Paper, Shadow & Promotion Laboratory

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R02`
Risk class: `HIGH_ASSURANCE`

## Objective
HCT requires a production-grade validation laboratory that tests strategies, indicators, models, agents, memory, Intelligence Brain logic, execution tactics and risk policies under point-in-time-correct, cost-aware, latency-aware, market-state-aware conditions before any production promotion.

The laboratory is not a cosmetic backtester. It is a proof system for trading behavior.

## Core principle
A candidate is not production-eligible because it generated attractive historical PnL. It must demonstrate robustness under realistic information timing, fees, funding, slippage, latency, partial fills, liquidity constraints, outages, stale data, execution uncertainty, portfolio interactions and regime changes.

## Validation ladder
Canonical lifecycle:

`RESEARCH -> STATIC_VALIDATION -> HISTORICAL_REPLAY -> WALK_FORWARD -> OUT_OF_SAMPLE -> STRESS/MONTE_CARLO -> PAPER -> SHADOW -> CHAMPION_CHALLENGER -> PRODUCTION_ELIGIBLE -> LIMITED_PRODUCTION -> PRODUCTION_ACTIVE`

Any stage may send a candidate back to research, quarantine it or retire it.

## Point-in-time correctness
Every replay decision must be limited to information that was actually available at that decision epoch.

Required temporal fields include:
- event/reference time;
- exchange time where available;
- HCT receive time;
- processing time;
- knowledge/availability time;
- revision/vintage time where applicable.

The Temporal Leakage Firewall defined by HCT memory architecture applies to the entire laboratory, including market data, news, external research, retrieved memories, labels, universe membership, model features and agent context.

Future knowledge may never enter a simulated historical decision merely because it exists in the current database or LLM training corpus.

## HCT Temporal Non-Interference Checker
Research/proposed HCT technology.

Purpose: validate that no decision-time pipeline consumes an input whose availability time exceeds the simulated decision epoch.

Target checks:
- feature windows;
- joins;
- resampling;
- market-universe membership;
- news/event retrieval;
- RAG retrieval;
- strategy state;
- agent evidence;
- labels/targets;
- execution outcomes;
- model metadata.

A candidate with unresolved temporal leakage is invalid regardless of reported performance.

## Event-driven replay engine
Prefer event-driven replay for promotion evidence where sequencing matters.

The engine should reproduce, where data permits:
- trades;
- tickers;
- candles;
- order-book updates/snapshots;
- mark/index/fair prices;
- funding events;
- symbol/rule changes;
- news/event arrival;
- scanner decisions;
- features/indicators;
- strategy decisions;
- agent/Brain evidence;
- Safety/Risk decisions;
- order intents;
- execution plans;
- fills/partials/cancels/rejects;
- position state;
- protective orders;
- reconciliation.

## Deterministic Replay Fingerprint
Every promoted replay should be reproducible from an immutable experiment identity containing at minimum:
- code commit;
- data snapshot/hash;
- strategy/model/agent versions;
- feature versions;
- configuration;
- exchange capability profile;
- fee/funding/slippage assumptions;
- random seeds;
- simulator version;
- experiment manifest hash.

Same fingerprint plus same deterministic inputs should reproduce materially equivalent outputs.

## Market Replay Fidelity Score (MRFS)
Measure how closely the replay engine reproduces known historical state transitions and live-captured behavior.

Candidate dimensions:
- event ordering fidelity;
- timestamp fidelity;
- candle reconstruction fidelity;
- order-book state fidelity;
- feature parity;
- strategy decision parity;
- execution-state parity;
- PnL/accounting parity.

Low replay fidelity blocks use of the affected dataset/feature for promotion evidence.

## Execution realism
Backtest and replay execution must model, where data permits:
- maker/taker fees;
- funding;
- spread;
- latency;
- slippage;
- market impact;
- partial fills;
- queue/priority approximation where feasible;
- participation limits;
- min quantity/notional/precision;
- order-type semantics;
- cancel/replace latency;
- signal expiration;
- protective-order behavior;
- rejected/uncertain orders;
- rate limits and degraded connectivity.

Optimistic same-bar/same-tick fills are prohibited unless mathematically justified by event availability and execution timing.

## HCT Fill Realism Envelope
Instead of assuming a single perfect fill, evaluate a distribution/range of plausible fills under the observed liquidity and latency environment.

Candidate outputs:
- optimistic but plausible fill;
- median plausible fill;
- conservative fill;
- tail/adverse fill;
- partial-fill probability;
- no-fill probability.

Promotion should not depend solely on an optimistic fill model.

## Latency Injection Laboratory
Replay should support deterministic and stochastic latency injection across:
- market-data receive;
- feature computation;
- agent/model inference;
- risk checks;
- execution planning;
- order submission;
- exchange acknowledgement;
- cancel/replace;
- private-stream updates;
- reconciliation.

Evaluate performance as latency increases and identify the point where signal edge expires.

## Signal Half-Life Stress
Every signal/strategy may have a context-specific useful lifetime.

Test:
`decision latency -> remaining signal lifetime -> realized performance`

A strategy whose backtest edge disappears under realistic latency is not live-eligible.

## Funding and carry realism
For futures, evaluation must include relevant funding/carry effects over holding horizons. PnL must distinguish:
- gross trading PnL;
- fees;
- funding;
- slippage;
- market impact;
- execution opportunity cost;
- net PnL.

## Regime-aware walk-forward validation
Use rolling/expanding point-in-time train/validation/test windows rather than fitting and testing on the same history.

Results should be segmented by:
- trend/range regime;
- volatility regime;
- liquidity regime;
- macro/news regime;
- symbol/cluster;
- market breadth state;
- execution-quality state.

## HCT Parameter Plateau Score (PPS)
Research technology to penalize strategies whose performance exists only at one narrow parameter value.

Prefer broad robust regions where nearby parameter combinations retain acceptable behavior.

Candidate dimensions:
- local sensitivity;
- neighboring-parameter performance;
- regime stability;
- turnover/cost sensitivity;
- drawdown stability.

## HCT Edge Survival Curve
Measure how estimated edge survives progressive realism.

Example stages:
1. idealized signal;
2. fees;
3. spread;
4. slippage;
5. latency;
6. partial fills;
7. funding;
8. portfolio constraints;
9. risk rules;
10. degraded market-data/execution conditions.

The shape of this curve matters more than raw idealized backtest PnL.

## HCT Reality Gap Score (RGS)
Compare expected behavior across:
`backtest -> replay -> paper -> shadow -> limited live`

Dimensions may include:
- PnL difference;
- hit-rate difference;
- slippage difference;
- fill-rate difference;
- turnover difference;
- drawdown difference;
- latency difference;
- calibration difference;
- decision-distribution difference.

Increasing reality gap triggers review/quarantine.

## Paper trading
Paper mode consumes realtime production-like market data and executes simulated orders without exchange financial exposure.

It must preserve:
- same strategy/Brain code path where practical;
- same policy/risk decisions;
- realtime latency measurements;
- realistic execution approximation;
- complete decision/evidence logs.

Paper success alone is insufficient for production promotion.

## Shadow mode
Shadow mode runs candidates beside production logic using the same live market inputs but with no trading authority.

Examples:
- new strategy vs current strategy;
- new Brain vs production Brain;
- new feature vs old feature;
- new agent/model vs current agent/model;
- new execution planner vs production planner.

Shadow results must be clearly marked hypothetical and must never mutate authoritative trading state.

## Champion-Challenger governance
For each promotable component, maintain:
- current Champion;
- one or more Challengers;
- immutable versions;
- evaluation windows;
- statistical and economic comparison;
- stability constraints;
- rollback target.

Promotion requires evidence that the Challenger improves or materially complements the Champion without unacceptable regression in safety, drawdown, calibration, latency, cost or robustness.

No AI/model/agent may self-promote.

## HCT Promotion Evidence Matrix
Every candidate promotion should include a structured evidence vector rather than a single metric.

Candidate fields:
- net PnL after costs;
- risk-adjusted return;
- max drawdown;
- tail loss;
- turnover;
- fee/funding burden;
- fill quality;
- calibration;
- abstention/selectivity quality;
- risk-coverage frontier;
- regime consistency;
- symbol/cluster consistency;
- parameter robustness;
- data quality sensitivity;
- latency sensitivity;
- execution sensitivity;
- reality gap;
- statistical uncertainty;
- sample independence;
- operational cost.

## HCT Evidence Sufficiency Score (ESS)
Research metric estimating whether a candidate has enough independent evidence for promotion.

It should account for:
- number of independent regimes;
- number of independent episodes;
- duration;
- symbol diversity where applicable;
- market-condition diversity;
- out-of-sample evidence;
- shadow duration;
- statistical uncertainty.

A large number of highly correlated trades from one event is not equivalent to broad evidence.

## Stress and failure simulation
Candidate test families:
- volatility shocks;
- liquidity collapse;
- spread explosion;
- flash move/gap;
- WebSocket interruption;
- delayed private stream;
- REST degradation;
- stale mark price;
- partial market data;
- sequence gaps;
- order acknowledgement timeout;
- duplicate/late event;
- position/reconciliation mismatch;
- protective-order failure;
- process restart;
- cache loss;
- database delay;
- model timeout;
- agent disagreement;
- news uncertainty;
- exchange rule change.

## HCT Synthetic Crisis Generator
Research-only generator for creating controlled stress sequences when historical examples are too sparse.

Synthetic scenarios are never mixed with historical evidence without explicit labeling. They test robustness and safety, not prove historical profitability.

## Monte Carlo / resampling laboratory
Where statistically valid, evaluate sensitivity to:
- trade ordering;
- fill variation;
- slippage variation;
- missed trades;
- delayed trades;
- parameter perturbation;
- regime composition;
- capital path.

Use these to estimate fragility and tail distributions, not to manufacture confidence.

## HCT Decision Twin
For selected historical/live-shadow episodes, run two or more controlled decision stacks against identical point-in-time evidence.

Examples:
- Brain v1 vs Brain v2;
- with-RAG vs without-RAG;
- indicator enabled vs disabled;
- agent enabled vs disabled;
- execution tactic A vs B.

This supports causal/ablation-style investigation of incremental value.

## Ablation requirements
New technology must prove incremental value where feasible by disabling or replacing it while holding other variables constant.

Questions include:
- Does temporal memory improve outcomes over no memory?
- Does microstructure improve decisions over candles/features alone?
- Does agent debate improve calibration or only latency/cost?
- Does a new proprietary indicator add information beyond correlated existing features?
- Does the execution model improve net fill outcomes?

## Counterfactual safety
Counterfactual experiments remain separate from actual history and cannot overwrite real outcomes.

Counterfactuals may test:
- later/earlier entry;
- alternate order type;
- alternate size within policy;
- alternate stop/TP;
- no-trade;
- different execution schedule.

## Promotion gates
A candidate may be promoted only if all required gates pass:
1. temporal correctness;
2. deterministic/reproducible experiment identity;
3. data/replay fidelity;
4. realistic frictions;
5. out-of-sample/walk-forward evidence;
6. robustness/parameter plateau;
7. acceptable tail/drawdown behavior;
8. no safety/risk regression;
9. paper/shadow evidence where required;
10. champion/challenger comparison;
11. statistical/economic significance appropriate to the component;
12. operational performance/cost acceptable;
13. rollback path defined;
14. independent review for HIGH_ASSURANCE components.

## Promotion states
`EXPERIMENTAL -> RESEARCH_VALIDATED -> REPLAY_VALIDATED -> PAPER_VALIDATED -> SHADOW_VALIDATED -> PRODUCTION_ELIGIBLE -> LIMITED_LIVE -> PRODUCTION_ACTIVE -> DEGRADED -> QUARANTINED -> RETIRED`

State transitions are auditable and version-specific.

## Live canary / limited production
If/when implementation reaches live promotion, new behavior should start under restricted scope where safe and technically meaningful, for example:
- restricted symbols;
- restricted tenants/accounts;
- lower risk ceiling;
- smaller position limits;
- limited operating window.

Canary exposure never relaxes platform safety boundaries.

## Bootstrap/free infrastructure compatibility
The laboratory must support a low-cost mode.

Bootstrap approach:
- local/controlled compute for heavy replay/research;
- compressed/selective datasets;
- PostgreSQL/Supabase for experiment metadata and promotion records;
- local columnar files (e.g. Parquet) for large replay datasets where appropriate;
- no requirement for paid streaming clusters or GPU services for baseline validation;
- queue expensive experiments rather than run them continuously;
- preserve provider-neutral interfaces so larger compute/storage can be added later.

## Research technologies introduced in this round
1. HCT Temporal Non-Interference Checker (TNIC)
2. Deterministic Replay Fingerprint (DRF)
3. Market Replay Fidelity Score (MRFS)
4. Fill Realism Envelope (FRE)
5. Latency Injection Laboratory (LIL)
6. Signal Half-Life Stress (SHLS)
7. Parameter Plateau Score (PPS)
8. Edge Survival Curve (ESC)
9. Reality Gap Score (RGS)
10. Promotion Evidence Matrix (PEM)
11. Evidence Sufficiency Score (ESS)
12. Synthetic Crisis Generator (SCG)
13. Decision Twin (DT)
14. Promotion Fragility Index (PFI)
15. Shadow Divergence Monitor (SDM)
16. Live-Parity Contract (LPC)

All begin as research/planning constructs and require implementation validation.

## Live-Parity Contract
Where feasible, paper/replay/shadow and live execution should share the same domain contracts and decision code. Environment-specific adapters may differ, but strategy, Brain, Safety, Risk and policy semantics should not be rewritten for backtests.

This reduces the risk that the backtested system and production system are secretly different products.

## Safety rule
No simulated result, however strong, grants direct production authority. Simulation evidence supports promotion decisions; deterministic Safety, Risk, Session Policy, execution/reconciliation controls and governance remain authoritative.
