# Proprietary Indicator Research Program

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R02`
Risk class: `HIGH_ASSURANCE`

## Goal
Research genuinely new HCT indicators/features that combine market microstructure, multi-timeframe context, historical memory and model-assisted inference. These are research candidates, not assumed profitable signals.

## Research principle
A new indicator must encode information that is plausibly incremental, not merely repackage RSI/MACD/EMA under a new name. Promotion requires evidence of incremental value after transaction costs, funding, slippage, latency assumptions and out-of-sample validation.

## HCT candidate indicator families

### 1. HCT Regime Transition Probability (RTP)
Estimates the probability that the current market regime is about to change, rather than only classifying the current regime. Inputs may include volatility structure, trend persistence, liquidity, funding, open interest, volume participation, price compression/expansion and cross-timeframe instability.

Research question: can anticipating regime transitions reduce entries immediately before trend failure or breakout failure?

### 2. HCT Multi-Timeframe Agreement Entropy (MTAE)
Measures directional agreement and disagreement across timeframes while discounting redundant indicators. Instead of counting ten correlated bullish indicators as ten votes, it estimates information diversity and directional entropy.

Research question: can low-entropy multi-timeframe agreement identify cleaner setups than naive confluence counts?

### 3. HCT False Breakout Probability (FBP)
Produces a calibrated probability that an apparent breakout will fail. Candidate inputs include breakout distance, volume participation, order-book depth/imbalance, volatility expansion, prior failed breakouts, liquidity gaps, funding context and historical analogues.

### 4. HCT Liquidity Vacuum Index (LVI)
Measures how fragile the nearby market depth is around current price. Candidate inputs include bid/ask depth decay, spread, depth asymmetry, local gaps, estimated slippage and recent sweep behavior.

Research question: can this feature identify situations where a small order-flow shock may cause outsized price movement or poor execution?

### 5. HCT Exhaustion Resonance Score (ERS)
Attempts to detect trend exhaustion by combining price extension, momentum deceleration, declining participation, volatility behavior, wick/rejection structure, divergence and historical regime-specific exhaustion patterns.

### 6. HCT Historical Analog Edge Score (HAES)
Uses time-aware market memory/RAG to retrieve comparable historical states and summarizes how frequently similar contexts produced favorable versus unfavorable outcomes after controlling for regime and horizon.

The score must include retrieval quality, sample size, recency weighting and uncertainty. It is not a direct trading instruction.

### 7. HCT Adversarial Confidence Gap (ACG)
Measures disagreement between the pro-trade evidence stack and the Devil's Advocate Agent. A large unresolved contradiction should reduce trade confidence or produce `NO_TRADE`.

### 8. HCT Signal Fragility Index (SFI)
Measures how sensitive a signal is to small perturbations in parameters, timeframe boundaries, data noise and execution assumptions. Signals that disappear after tiny perturbations are treated as fragile and receive lower confidence.

### 9. HCT Opportunity Persistence Score (OPS)
Estimates whether an opportunity remains valid long enough to execute safely. It combines signal half-life, volatility, liquidity, spread, latency budget and historical decay of similar setups.

### 10. HCT Contextual Risk-Reward Surface (CRRS)
Instead of one static risk/reward ratio, models a surface of possible outcomes under different stop distances, volatility states, trailing policies and partial-exit paths. The system can search for an execution policy that remains acceptable across a range of plausible conditions.

### 11. HCT Cycle Alignment Score (CAS)
Measures alignment between short-term setup, medium-term regime and long-horizon crypto cycle context. Long-cycle context cannot override realtime risk but may adjust strategy confidence or aggressiveness within configured limits.

### 12. HCT Decision Confidence Calibration Score (DCCS)
Tracks whether the system's historical 70%, 80%, 90% confidence claims actually behaved like 70%, 80%, 90% outcomes. The goal is calibrated confidence rather than impressive-looking raw scores.

## AI-assisted indicator synthesis
The research platform may allow an Indicator Research Agent to propose new mathematical combinations/features. Candidate generation must be separated from validation.

`Hypothesis generation -> symbolic/feature definition -> dataset lock -> leakage checks -> backtest -> ablation -> out-of-sample -> walk-forward -> paper/shadow -> promotion review`

The generator must not repeatedly optimize against the same holdout dataset.

## Required evaluation
For each proprietary indicator record:
- hypothesis and economic/market rationale;
- exact formula or model version;
- required data and provenance;
- supported symbols/timeframes;
- training/validation/test period boundaries when learned;
- ablation versus baseline strategy;
- incremental predictive value;
- precision/recall or ranking/calibration metrics where appropriate;
- PnL contribution after realistic costs when used in a strategy;
- drawdown and tail-risk impact;
- stability across symbols/regimes;
- sensitivity/perturbation results;
- failure modes;
- promotion verdict.

## Promotion rule
No indicator becomes production-authoritative because it is novel. Novelty earns a research slot; evidence earns promotion.
