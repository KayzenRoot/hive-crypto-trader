# Strategy Ecology, Router, Ensemble & Conflict Resolution

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R02`
Risk class: `HIGH_ASSURANCE`

## Objective
HCT should not treat every approved strategy as equally suitable at every moment. The platform needs a governed layer that estimates which approved strategies deserve attention for the current symbol, regime, timeframe, volatility/liquidity state and execution conditions, while preventing strategy competition from bypassing portfolio risk.

## Core principle
A strategy signal answers: `does this strategy see a setup?`

The Strategy Ecology layer answers: `how relevant and trustworthy is this approved strategy in the current context, relative to the other approved strategies?`

Routing/ensemble logic never grants trading authority. It produces strategy-level evidence for the existing Safety/Risk/Policy/Execution chain.

## Strategy lifecycle states
Candidate states:
- `RESEARCH`
- `BACKTEST_VALIDATED`
- `PAPER`
- `SHADOW`
- `PRODUCTION_ELIGIBLE`
- `PRODUCTION_ACTIVE`
- `DEGRADED`
- `QUARANTINED`
- `RETIRED`

Only explicitly promoted versions may participate in live routing. User-created strategies follow equivalent governed eligibility rules.

## Strategy Suitability Engine
For each eligible strategy/version, HCT may estimate a multidimensional suitability profile using evidence such as:
- current market regime;
- symbol/market characteristics;
- timeframe-role compatibility;
- volatility state;
- liquidity/spread/depth;
- funding/derivatives context where available;
- recent strategy calibration;
- historical out-of-sample reliability in comparable contexts;
- current data quality;
- execution feasibility;
- strategy fragility/parameter sensitivity;
- correlation with already-active strategies and positions;
- drawdown/decay indicators;
- event/news risk where approved data exists.

Suitability is not a probability of profit and must not be presented as one.

## HCT Strategy Ecology Engine
The Strategy Ecology Engine maintains the relationship between strategies as a portfolio of decision processes rather than isolated bots.

Candidate functions:
- identify strategies competing for the same underlying edge;
- estimate effective strategy diversity;
- detect correlated exposures hidden behind different strategy names;
- identify regime niches in which strategies historically perform more reliably;
- reduce duplicate strategy votes;
- detect strategy deterioration/decay;
- support governed capital/risk-budget recommendations;
- surface conflicts and complementary evidence to Copilot and users.

## HCT Strategy DNA
Each strategy version may have a Strategy DNA Fingerprint containing stable research descriptors such as:
- trend dependence;
- momentum dependence;
- mean-reversion dependence;
- volatility dependence;
- liquidity dependence;
- timeframe footprint;
- average holding horizon;
- turnover;
- long/short asymmetry;
- regime sensitivity;
- feature-family dependence;
- execution sensitivity;
- tail-risk profile;
- correlation clusters with other strategies.

Strategy DNA supports comparison and redundancy analysis but is not itself a live-trading signal.

## Strategy Router
The Router considers only strategies already eligible under policy and produces a ranked/filtered candidate set.

Conceptual flow:
`Eligible Strategy Registry -> Context/Suitability -> Redundancy/Conflict -> Router -> Candidate Strategy Set -> Strategy Signals -> Copilot/Signal Evidence`

Router responsibilities:
- exclude incompatible exchange/symbol/data-capability strategies;
- exclude quarantined/disabled versions;
- apply regime suitability;
- apply timeframe/data availability constraints;
- account for execution feasibility;
- discount redundant strategy families;
- respect tenant/session strategy allowlists;
- preserve explainable reasons for selection/rejection.

The Router cannot invent a live strategy, change a strategy definition or promote an experimental strategy.

## Strategy Ensemble
Where multiple independent eligible strategies support the same directional action, HCT may construct an ensemble evidence object rather than blindly count votes.

Potential ensemble evidence dimensions:
- independent strategy count;
- effective diversity;
- regime fit;
- calibration quality;
- confidence dispersion;
- timeframe agreement;
- execution compatibility;
- historical co-performance;
- shared-feature redundancy;
- portfolio exposure impact.

An ensemble must distinguish `five strategies agree` from `five nearly identical strategies agree`.

## Conflict Resolver
Conflicts are expected, not treated as system errors.

Examples:
- trend strategy says LONG while mean reversion says SHORT;
- breakout strategy says ENTER while liquidity strategy says WAIT;
- strategy says LONG while event-risk layer recommends NO_TRADE;
- two strategies want opposing positions on the same symbol;
- multiple strategies want the same exposure and would accidentally multiply risk.

Candidate conflict outcomes:
- `SELECT_LONG`
- `SELECT_SHORT`
- `WAIT`
- `NO_TRADE`
- `REDUCE_CONFIDENCE`
- `REQUEST_ADVERSARIAL_REVIEW`
- `ROUTE_TO_DIFFERENT_TIME_HORIZON`
- `BLOCK_DUE_TO_PORTFOLIO_CONFLICT`

Conflict resolution must be deterministic/auditable at the authority boundary even when AI contributes contextual evidence.

## HCT Effective Strategy Diversity (ESD)
Research metric: estimate how many genuinely different strategy theses are represented in an ensemble after discounting shared indicators, features, timeframes, regimes and historical return correlation.

Example concept:
`8 nominal strategies -> 3.1 effective independent strategy theses`

This metric is experimental until validated.

## HCT Strategy Decay Index (SDI)
Research metric: detect evidence that an approved strategy's observed behavior is drifting away from its validated profile.

Candidate evidence:
- rolling expectancy deterioration;
- calibration drift;
- regime-specific degradation;
- rising adverse excursion;
- slippage/execution deterioration;
- loss-cluster changes;
- feature distribution shift;
- divergence from shadow/replay expectations.

SDI cannot automatically rewrite the strategy. Depending on governed thresholds it may reduce routing priority, trigger review, restrict new exposure or recommend quarantine. Hard automated quarantine requires explicit policy and evidence thresholds.

## HCT Strategy Regime Affinity Surface (SRAS)
Research object mapping a strategy's validated behavior across regime dimensions rather than assigning one simplistic label.

Possible dimensions:
- trend strength/direction;
- realized volatility;
- liquidity;
- funding/derivatives state;
- market breadth/correlation;
- event-risk state;
- session/time-of-day;
- timeframe horizon.

The surface is versioned and must distinguish training/research evidence from live observations.

## HCT Strategy Conflict Graph (SCG)
Maintain a graph of relationships between active/eligible strategies:
- positive correlation;
- negative correlation;
- shared feature dependence;
- shared timeframe dependence;
- opposing directional thesis;
- complementary regime niche;
- shared execution bottleneck;
- common tail-risk exposure.

This can power cockpit visualization and portfolio-level risk diagnostics.

## HCT Capital & Risk Budget Allocator
Future/advanced capability: recommend how a fixed user-approved risk budget could be distributed among eligible strategies based on diversification, regime suitability, drawdown state and portfolio exposure.

Hard rule: the allocator cannot increase the user's/platform's approved total risk budget. It only proposes/distributes inside that budget and remains subordinate to Risk Engine and Position Sizing.

## AI-generated strategy candidates
The Intelligence Brain may eventually propose new Strategy Graph candidates by combining approved nodes, historical observations and research hypotheses.

Required boundary:
`AI proposal -> RESEARCH only -> static analysis -> backtest -> OOS/walk-forward -> paper -> shadow -> independent promotion review -> production eligibility`

AI-generated candidates can never self-promote or trade live merely because historical results look favorable.

## Strategy Tournament / Challenger Framework
HCT may run controlled research tournaments among strategy versions/candidates using locked datasets and realistic cost assumptions.

A tournament must not optimize repeatedly against the final holdout. Candidate winners progress only to the next validation stage rather than directly to production.

This enables champion/challenger workflows:
- production champion;
- shadow challenger(s);
- comparable evidence windows;
- explicit promotion/rollback criteria.

## Cockpit UX
The cockpit should eventually visualize:
- strategies currently eligible;
- selected/routed strategies;
- rejected strategies and reasons;
- regime affinity;
- strategy DNA;
- strategy conflicts;
- effective diversity;
- decay/drift warnings;
- ensemble evidence;
- risk-budget allocation;
- champion/challenger state.

A user should be able to answer: `Why did HCT listen to Strategy A and ignore Strategy B at this moment?`

## Safety boundary
No Strategy Ecology component may:
- exceed platform/user risk ceilings;
- promote a research strategy to live autonomously;
- disable Safety Governor;
- bypass Session Policy;
- multiply exposure merely because multiple strategies agree;
- hide conflicts or correlated exposure;
- treat recent profitability alone as evidence of persistent edge.
