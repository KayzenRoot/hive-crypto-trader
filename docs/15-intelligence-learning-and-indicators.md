# Intelligence, Learning & Indicator Program

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001`
Risk class: `HIGH_ASSURANCE`

## Goal
Create a controlled decision-support intelligence layer that can combine technical indicators, candlestick/chart patterns, market regime, historical analogues, prior outcomes and risk context to reduce low-quality or false-positive signals. This program does not promise profitability and must be evaluated statistically before any production use.

## Indicator program
The target is an extensible library covering the major public/standard technical-analysis families commonly used in professional charting platforms, including:
- trend and moving-average families;
- momentum and oscillator families;
- volatility and range measures;
- volume, money-flow and participation measures;
- support/resistance, pivots and price-structure measures;
- channels, bands and breakout measures;
- trend-strength and directional movement measures;
- multi-timeframe derived features;
- funding, basis, open-interest/liquidity features when supported by reliable data;
- recognized candlestick formations;
- recognized chart/market-structure patterns.

The requirement is conceptual/functional coverage of relevant public indicators and patterns, not copying proprietary or closed-source TradingView/community scripts.

## HCT proprietary indicator R&D
New HCT indicators are allowed and encouraged, but each begins as an experimental hypothesis. Candidate families may combine:
- regime-adjusted momentum;
- liquidity/volatility dislocation;
- multi-timeframe confirmation/conflict;
- trend persistence versus exhaustion;
- false-breakout probability;
- funding/price divergence where data quality permits;
- order-book imbalance and microstructure where reliable;
- cross-symbol/correlation context;
- signal reliability conditioned on historical regime.

No proprietary indicator may be promoted because it looks good on one backtest. Promotion requires defined datasets, fees/slippage assumptions, out-of-sample testing, walk-forward evaluation, sensitivity analysis, leakage checks and reproducibility.

## RAG & market memory
RAG is intended for retrieval of relevant historical context such as:
- similar market regimes and setups;
- historical outcomes for comparable indicator combinations;
- symbol-specific behavioral tendencies;
- strategy incidents and failure patterns;
- prior false-positive patterns;
- volatility/liquidity context;
- operational lessons and post-trade explanations.

RAG memory must be time-aware and provenance-aware. Future information must never leak into historical decisions or backtests.

## Learning architecture
The learning path is deliberately separated from live execution:

`Raw observations -> curated datasets -> feature store -> research/training -> offline evaluation -> paper/shadow validation -> approval gate -> versioned production model`

Potential techniques may include supervised models, ranking models, anomaly detection, representation learning and optional fine-tuning where justified by evidence. Fine-tuning is not assumed to be automatically useful.

## Non-negotiable safety rule
The Intelligence Brain, RAG and any learned model:
- may reduce confidence, veto a candidate signal or recommend no-trade;
- may provide evidence and explanations;
- may propose experiments for later review;
- must not autonomously increase hard risk limits;
- must not autonomously increase maximum leverage;
- must not disable Safety Governor rules;
- must not change production strategy/model versions without governed promotion;
- must not place orders directly without passing deterministic safety/risk/execution controls.

## Explainability requirement
For every future trade decision the architecture should be able to preserve a machine-readable decision trace including relevant inputs, indicator/pattern evidence, regime, retrieved memory, model/version identifiers, confidence, risk constraints, final decision and actual outcome. This becomes material for audit, debugging and future learning.
