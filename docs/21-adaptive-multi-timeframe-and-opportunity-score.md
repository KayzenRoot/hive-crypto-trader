# Adaptive Multi-Timeframe Intelligence & Opportunity Score

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R02`
Risk class: `HIGH_ASSURANCE`

## Objective
Define how Hive Crypto Trader combines multiple timeframes, evidence families and strategy context without naïvely counting correlated signals as independent confirmation.

## Multi-timeframe principle
A timeframe is not inherently authoritative. Its usefulness depends on strategy, symbol, volatility, liquidity, regime and execution horizon. HCT will therefore plan a hierarchy of roles rather than a flat vote.

Candidate roles:
- `MACRO_CONTEXT`: broad directional/regime context;
- `STRUCTURE`: trend/range/support/resistance and setup structure;
- `SETUP`: signal formation and confluence;
- `TRIGGER`: timing/entry confirmation;
- `MICROSTRUCTURE`: optional execution-quality/order-book context.

Illustrative only, not frozen defaults:
- 4h / 1h may serve macro/structure;
- 15m / 5m may serve setup;
- 1m / tick/order-book may serve trigger/execution when justified.

Exact timeframe sets remain strategy-specific and must be validated.

## Adaptive weighting
HCT should not permanently assign equal weights to every timeframe. Candidate weighting inputs:
- historical reliability for that strategy/symbol/regime;
- current volatility regime;
- liquidity and spread;
- signal half-life/opportunity persistence;
- distance between timeframe horizon and expected holding period;
- data quality/freshness;
- recent calibration drift;
- cross-timeframe agreement/conflict;
- correlation/redundancy between derived evidence.

Adaptive weights may move inside governed bounds, but models/agents may not silently redefine hard strategy semantics in production.

## Signal-independence control
Ten indicators or timeframes derived from nearly identical price information must not count as ten independent confirmations.

Plan a `Signal Independence / Redundancy Layer` that estimates:
- feature-family overlap;
- historical correlation;
- conditional correlation by regime;
- shared input dependency;
- temporal overlap;
- effective independent evidence count.

This layer can penalize duplicated confirmation and feed the HCT proprietary `Signal Independence Score` / `Multi-Timeframe Agreement Entropy` research program.

## Evidence families
The opportunity model should preserve separate evidence channels before aggregation:
1. Trend/structure evidence.
2. Momentum evidence.
3. Volatility evidence.
4. Volume/participation evidence.
5. Liquidity/microstructure evidence.
6. Derivatives evidence such as funding/basis/open interest when reliable.
7. Candlestick/chart-pattern evidence.
8. Multi-timeframe alignment/conflict.
9. Market-regime fit.
10. Historical/RAG analogue reliability.
11. Agent consensus/adversarial disagreement.
12. Execution feasibility.
13. Data-quality confidence.
14. Risk compatibility.

## Opportunity Score
Do not reduce every dimension to one opaque number too early. Preserve a vector of sub-scores, then derive an auditable composite when useful.

Candidate representation:
- `technical_strength`
- `regime_fit`
- `historical_edge`
- `data_confidence`
- `signal_independence`
- `execution_quality`
- `agent_consensus`
- `adversarial_risk`
- `risk_compatibility`
- `opportunity_persistence`

The final `HCT Opportunity Score` must expose its components, weighting/version and veto reasons.

## Decision states
Candidate signal states:
- `LONG_CANDIDATE`
- `SHORT_CANDIDATE`
- `WAIT`
- `HOLD`
- `REDUCE`
- `CLOSE`
- `NO_TRADE`
- `DATA_UNCERTAIN`
- `SAFETY_VETO`
- `RISK_VETO`

A candidate is not an order. Only downstream deterministic policy/safety/risk/execution layers can turn an approved candidate into exchange actions.

## Strategy-timeframe profiles
Each strategy version should declare:
- intended holding horizon;
- allowed timeframe roles;
- required evidence families;
- optional evidence families;
- forbidden combinations where leakage/redundancy is known;
- minimum data quality;
- signal expiration/half-life;
- entry/exit semantics;
- confidence calibration version.

## Performance concern
HCT may scan hundreds of MEXC futures contracts. It must not calculate every expensive indicator on every timeframe for every symbol continuously.

Plan staged computation:
`cheap universe filters -> lightweight scanner -> shortlist -> richer multi-timeframe features -> agent/research-intensive analysis -> candidate decision`.

This reduces compute cost, API pressure and latency while preserving broad market coverage.

## Validation
Adaptive weights and composite scores require:
- walk-forward testing;
- out-of-sample evaluation;
- ablation by evidence family;
- regime-stratified metrics;
- calibration tests;
- turnover/fee/slippage impact;
- latency sensitivity;
- robustness to parameter perturbation;
- paper/shadow validation before production promotion.

No timeframe hierarchy, weight or score component is assumed profitable merely because it is sophisticated.
