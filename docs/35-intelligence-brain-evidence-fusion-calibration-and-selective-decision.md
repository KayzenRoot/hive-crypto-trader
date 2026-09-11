# HCT Intelligence Brain — Evidence Fusion, Calibration & Selective Decision

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R02`
Risk class: `HIGH_ASSURANCE`

## Objective
The HCT Intelligence Brain is the governed decision-fusion layer that combines market-state integrity, microstructure/order flow, indicators, strategies, regime, temporal memory/RAG, news/events, institutional agents, portfolio/risk context and execution feasibility into an auditable candidate decision.

The Brain is **not** an unrestricted super-agent and is **not** authoritative over Safety, Risk, Session Policy, Position/Leverage or Execution. Its job is to produce the best evidence-calibrated candidate action possible, including the explicit option to abstain.

## Core principle
The system should maximize **validated decision quality and opportunity capture subject to uncertainty, freshness, execution feasibility and bounded risk**.

A high raw prediction score is insufficient. Every production candidate must answer:
- what evidence supports it;
- what evidence contradicts it;
- how fresh the evidence is;
- how independent the evidence is;
- what regime it applies to;
- how historically calibrated similar confidence has been;
- whether the decision is executable now;
- whether uncertainty is low enough to act;
- why WAIT/NO_TRADE may be better.

## Brain architecture
Conceptual flow:

`Market-State Integrity -> Microstructure/Breadth -> Features/Indicators -> Strategy Ecology -> Regime -> Temporal Memory/RAG -> News/Event -> Institutional Agents -> Evidence Board -> Conflict/Redundancy Engine -> Calibration -> Selective Decision Controller -> Candidate Action`

Then deterministic authority remains:

`Candidate Action -> Safety Governor -> Risk Engine -> Session Policy -> Position/Leverage -> Execution Intelligence -> OMS -> Exchange`

## Canonical evidence packet
Every contributor to the Brain produces a typed `EvidencePacket` rather than opaque prose-only output.

Candidate fields:
- evidence ID;
- producer/module/agent ID and version;
- symbol/universe;
- direction: bullish / bearish / neutral / volatility / risk-only;
- horizon;
- event time;
- knowledge time;
- generation ID / point-in-time state ID;
- confidence before calibration;
- calibrated confidence if available;
- freshness / expiry / half-life;
- reliability history;
- regime compatibility;
- source/provenance references;
- independence/redundancy family;
- contradiction references;
- required capabilities/data dependencies;
- latency/computation cost;
- expected impact type;
- abstention recommendation where applicable.

## Evidence families
The Brain must preserve evidence dimensions instead of flattening them too early:
1. trend / structure;
2. momentum;
3. volatility;
4. volume / participation;
5. liquidity / microstructure;
6. derivatives / funding / open interest;
7. candlestick / chart patterns;
8. multi-timeframe structure;
9. regime / cycle;
10. market breadth;
11. cross-asset propagation;
12. historical analog / temporal memory;
13. news / macro / event intelligence;
14. strategy ecology / decay / conflict;
15. agent specialist judgments;
16. data integrity / freshness;
17. portfolio interaction;
18. execution feasibility / adverse selection;
19. risk compatibility.

## No naive voting
Three correlated indicators are not three independent votes.

The Brain must use redundancy-aware aggregation. Candidate technologies include:
- Signal Redundancy Mapper;
- Effective Independent Evidence Count;
- Evidence Correlation Graph;
- Common-Cause Detector;
- Strategy DNA overlap;
- agent/model correlation history;
- shared-input lineage analysis.

If RSI, Stochastic RSI and momentum oscillator all arise from substantially the same price behavior, their combined contribution must be discounted.

## HCT Evidence Independence Graph (EIG)
R&D candidate.

Represent evidence packets as nodes and material dependencies/correlations as edges. Edge types may include:
- same raw source;
- same feature family;
- same strategy family;
- same model backbone;
- same historical episodes;
- common market-factor exposure;
- temporal overlap;
- causal/derived dependency.

The graph yields an `EffectiveIndependentEvidence` estimate used in fusion and confidence calibration.

## HCT Evidence Quality Tensor (EQT)
R&D candidate.

Do not compress evidence quality into one number too early. Preserve a vector such as:
- source quality;
- data integrity;
- freshness;
- historical reliability;
- regime fit;
- independence;
- calibration quality;
- execution relevance;
- contradiction burden;
- sample support.

The tensor can later derive context-specific scores, but the underlying dimensions remain inspectable.

## HCT Confidence Calibration Engine
The Brain must treat confidence as an empirically testable statement.

If the system says `70% confidence`, historically comparable decisions should approximately behave like 70% events under the same definition and horizon, otherwise the confidence is miscalibrated.

Candidate methods to evaluate:
- temperature scaling;
- isotonic regression;
- Platt-style calibration where appropriate;
- beta calibration;
- Bayesian calibration;
- regime-aware calibration;
- online calibration;
- conformal prediction / adaptive conformal methods;
- ensemble calibration.

Calibration is evaluated chronologically, never by leaking future labels.

## HCT Regime-Aware Calibration Surface (RACS)
R&D candidate.

Confidence may be calibrated conditionally across dimensions such as:
- market regime;
- volatility state;
- liquidity state;
- symbol class;
- horizon;
- strategy family;
- news/event state;
- data-quality tier;
- execution-quality tier.

Example:
A nominal `0.75` confidence from Strategy A may historically realize very differently in low-volatility range markets versus high-volatility event regimes. The system should learn separate calibration behavior rather than pretending confidence is universally portable.

## HCT Calibration Drift Monitor (CDM)
Continuously detect when previously calibrated confidence stops matching outcomes.

Monitor:
- Expected Calibration Error;
- Brier score;
- log loss where applicable;
- reliability diagrams;
- coverage error;
- selective risk;
- calibration by regime/symbol/horizon;
- confidence inflation;
- confidence collapse.

States:
`CALIBRATED`, `WATCH`, `DEGRADED`, `UNTRUSTED`.

A `UNTRUSTED` calibration state can tighten abstention thresholds or block confidence-dependent strategies.

## Uncertainty decomposition
The Brain should distinguish multiple uncertainty sources:
- aleatoric / market randomness;
- epistemic / model uncertainty;
- data-quality uncertainty;
- regime uncertainty;
- retrieval/memory uncertainty;
- event/news uncertainty;
- disagreement uncertainty;
- execution uncertainty;
- portfolio/risk uncertainty.

## HCT Uncertainty Budget Vector (UBV)
R&D candidate.

Instead of one vague uncertainty scalar, maintain a vector. Example:

`market=0.25, model=0.18, data=0.03, regime=0.31, memory=0.12, event=0.42, execution=0.08`

The Selective Decision Controller can abstain when a critical dimension exceeds policy limits even if average uncertainty looks moderate.

## Selective decision / abstention
The Brain must explicitly support:
- `LONG_CANDIDATE`;
- `SHORT_CANDIDATE`;
- `WAIT`;
- `NO_TRADE`;
- `HOLD`;
- `REDUCE`;
- `EXIT`;
- `DATA_UNCERTAIN`;
- `EVIDENCE_CONFLICT`;
- `CALIBRATION_UNTRUSTED`;
- `EVENT_RISK_WAIT`.

Abstention is a first-class outcome, not a failure.

## HCT Selective Decision Controller (SDC)
Candidate controller inputs:
- calibrated opportunity confidence;
- independent evidence count;
- contradiction level;
- uncertainty vector;
- signal freshness / half-life;
- market-state integrity;
- analog reliability;
- regime confidence;
- event risk;
- execution feasibility;
- portfolio/risk compatibility.

It decides whether evidence is sufficient to create a candidate action or whether the correct output is WAIT/NO_TRADE.

## HCT Risk-Coverage Frontier
R&D metric.

Measure how performance changes as the Brain acts on fewer but higher-confidence opportunities.

The goal is not maximum prediction coverage. Candidate operating points should compare:
- percentage of opportunities acted upon;
- selective error rate;
- calibration;
- expected value after realistic costs;
- drawdown;
- turnover;
- missed-opportunity cost;
- tail behavior.

This makes abstention quantitatively tunable rather than ideological.

## Agent deliberation integration
Agents communicate through structured evidence, not hidden free-form consensus.

Deliberation path:
`Parallel specialist analyses -> shared Evidence Board -> contradiction detector -> targeted cross-examination -> Devil's Advocate -> Supervisor synthesis -> calibration -> selective decision`

Dissent is preserved.

The Supervisor cannot erase dissent by prose. If an agent issues a structured high-severity contradiction, the final packet must retain it and explain its treatment.

## HCT Dissent Materiality Score (DMS)
R&D candidate.

Estimate whether disagreement is:
- cosmetic;
- redundant;
- historically low-value;
- materially decision-changing;
- safety/risk critical.

The score can trigger additional analysis or abstention.

## HCT Adversarial Decision Challenge (ADC)
Before high-confidence candidates, run a bounded challenge:
- What evidence would invalidate this thesis?
- Are we double-counting evidence?
- Is the analog memory stale?
- Is this move already priced in?
- Is breadth contradictory?
- Is microstructure signaling adverse selection?
- Is news direction genuinely known or only volatility risk?
- Is execution still feasible at current price?
- Did confidence rise because many correlated models repeated the same input?

The challenge may reduce confidence or recommend WAIT but cannot increase risk ceilings.

## HCT Decision Stability Test (DST)
R&D candidate.

Perturb non-semantic inputs slightly within realistic uncertainty bounds and check whether the decision changes violently.

Examples:
- small spread shift;
- minor feature noise;
- one agent removed;
- one historical analog cluster removed;
- slightly changed timeframe weight;
- latency-induced evidence decay.

If tiny perturbations flip LONG to SHORT, the candidate is fragile and should be discounted or abstained.

## HCT Confidence Fragility Index (CFI)
Quantifies how much confidence depends on fragile assumptions, a narrow data slice, one model, one analog cluster or one agent.

## HCT Decision Margin
Maintain the margin between the selected action and alternatives, not only the top action score.

Example:
- LONG 0.61
- WAIT 0.59
- SHORT 0.10

A naive system may report LONG. HCT should recognize the LONG-vs-WAIT margin is tiny and likely abstain.

## HCT Opportunity Conviction Profile (OCP)
Preserve a multi-dimensional profile rather than a single score:
- directional evidence;
- regime fit;
- historical analog support;
- breadth support;
- microstructure support;
- event/news support;
- data confidence;
- calibration quality;
- execution quality;
- portfolio compatibility;
- adversarial resilience;
- freshness;
- uncertainty.

The existing HCT Opportunity Score can be derived from this profile for ranking, but the profile remains the inspectable source.

## Dynamic mixture of experts
R&D direction only.

Different expert/model families may specialize by:
- regime;
- horizon;
- symbol class;
- liquidity state;
- volatility state;
- event conditions.

A gating layer may route weight dynamically, but:
- routing is versioned;
- routing cannot self-promote;
- expert weights remain auditable;
- historical calibration is required;
- gating failures can revert to a safe baseline;
- no model gets authority merely because it predicts confidently.

## HCT Expert Reliability Ledger
Track every expert/agent/model over time by:
- accuracy/utility by regime;
- calibration;
- contribution after costs;
- false positives;
- false negatives;
- abstention quality;
- drift;
- latency/cost;
- correlation with other experts;
- rare-event performance.

The Brain can discount an expert whose recent reliability deteriorated without deleting its historical record.

## HCT Contextual Expert Routing Score (CERS)
R&D candidate combining:
- regime affinity;
- recent calibration;
- long-run reliability;
- feature availability;
- data quality;
- latency budget;
- current drift;
- redundancy;
- symbol/horizon specialization.

## News/event integration
News contributes structured impact evidence, not an unbounded language-model opinion.

The Brain distinguishes:
- event confirmed;
- event relevance;
- directional inference;
- volatility-only inference;
- liquidity/execution risk;
- uncertainty/rumor burden;
- event horizon and decay.

A high-impact but directionally uncertain event may strengthen `WAIT` rather than LONG/SHORT.

## Memory/RAG integration
Temporal memory contributes:
- analog distributions;
- regime-specific lessons;
- failure modes;
- historical reliability;
- comparable execution conditions;
- analog diversity/relevance;
- point-in-time-safe evidence.

Retrieved text or analogs never directly trigger orders.

## Execution-aware cognition
A theoretical edge that cannot be executed is not a valid candidate.

The Brain should receive:
- spread;
- depth;
- expected slippage;
- adverse-selection estimate;
- fill probability;
- signal remaining lifetime;
- execution quality score;
- API/WS health.

Candidate confidence may remain high while decision status changes to `WAIT` or `NO_TRADE` due to execution infeasibility.

## Decision provenance
Every Brain decision must be reproducible from a `DecisionEvidenceBundle` containing:
- market generation ID;
- evidence packets;
- feature/model/strategy versions;
- retrieved memory IDs;
- agent versions;
- source/news references;
- calibration version;
- aggregation/routing version;
- uncertainty vector;
- disagreement records;
- final candidate state;
- abstention/selection reason;
- timestamp and expiry.

## Decision explainability
User-facing explanations should answer:
- What does HCT believe?
- Why?
- What contradicts it?
- How confident is it after calibration?
- How much independent evidence exists?
- What could invalidate the thesis?
- How long is the signal expected to remain useful?
- Why did the Brain choose WAIT/NO_TRADE if it did?

Explainability must be generated from structured evidence, not hallucinated after the fact.

## Bootstrap / cost architecture
Initial Brain should remain cheap:
- deterministic feature fusion in-process;
- lightweight statistical calibrators;
- small structured evidence packets;
- selective invocation of expensive LLM/agent analysis only for shortlisted opportunities;
- no LLM call per tick;
- cache stable contextual analyses;
- use local/open models where validated and cost-effective;
- cloud model calls routed by value/latency/cost policy;
- persist compact decision/evidence metadata to PostgreSQL/Supabase;
- heavy research jobs run offline or opportunistically.

## HCT Intelligence Compute Governor
R&D/architecture component.

Compute tiers:
- `TIER_0`: deterministic realtime features only;
- `TIER_1`: lightweight strategy/regime fusion;
- `TIER_2`: memory analog search / specialist models;
- `TIER_3`: multi-agent deliberation / external LLM research.

Only sufficiently valuable candidates escalate to expensive tiers.

This supports the bootstrap free-first policy while preserving a path to institutional-scale intelligence later.

## Evaluation
The Intelligence Brain must be evaluated chronologically and against simpler baselines.

Candidate metrics:
- precision/recall where meaningful;
- Brier score;
- ECE / calibration curves;
- selective risk;
- risk-coverage curves;
- PnL after fees/slippage/funding;
- Sharpe/Sortino as secondary summaries, not sole metrics;
- max drawdown;
- tail loss;
- turnover;
- false-confidence rate;
- abstention quality;
- missed-opportunity cost;
- stability under perturbation;
- regime-specific performance;
- calibration under drift;
- latency and compute cost;
- benefit versus no-memory/no-agent/no-news/no-microstructure ablations.

## Promotion gates
A Brain version cannot be promoted merely because aggregate PnL improved.

Required evidence should include:
1. chronological train/validation/test discipline;
2. no point-in-time leakage;
3. out-of-sample evaluation;
4. walk-forward evaluation;
5. realistic execution/cost assumptions;
6. calibration analysis;
7. risk-coverage analysis;
8. regime-specific analysis;
9. ablations by evidence family;
10. perturbation/fragility testing;
11. paper/shadow deployment;
12. rollback path;
13. independent HIGH_ASSURANCE review.

## Research technologies in this round
1. Evidence Independence Graph (EIG)
2. Evidence Quality Tensor (EQT)
3. Regime-Aware Calibration Surface (RACS)
4. Calibration Drift Monitor (CDM)
5. Uncertainty Budget Vector (UBV)
6. Selective Decision Controller (SDC)
7. Risk-Coverage Frontier
8. Dissent Materiality Score (DMS)
9. Adversarial Decision Challenge (ADC)
10. Decision Stability Test (DST)
11. Confidence Fragility Index (CFI)
12. Decision Margin
13. Opportunity Conviction Profile (OCP)
14. Expert Reliability Ledger
15. Contextual Expert Routing Score (CERS)
16. Intelligence Compute Governor
17. Evidence Half-Life Aggregator
18. Contradiction Burden Index
19. Confidence Inflation Sentinel
20. Decision Reproducibility Score

All remain hypotheses or architecture candidates until implementation and empirical validation.

## Safety boundaries
The Intelligence Brain may:
- rank opportunities;
- recommend LONG/SHORT/WAIT/NO_TRADE/HOLD/REDUCE/EXIT candidates;
- reduce confidence;
- abstain;
- request additional evidence;
- recommend stricter risk treatment;
- explain decisions.

It may not:
- raise hard risk ceilings;
- raise max leverage beyond policy;
- disable Safety Governor;
- bypass Session Policy;
- directly sign/order on an exchange;
- self-promote models/strategies/calibrators;
- hide dissent or uncertainty;
- rewrite audit history.

## Research grounding snapshot — 2026-09-11
Current research supports several directions worth evaluating rather than blindly adopting:
- online model aggregation with conformal sets for adaptive uncertainty-aware ensembles;
- model-agnostic online calibration under temporal dependence and distribution shift;
- regime-aware mixture-of-experts approaches in financial forecasting/allocation;
- selective financial forecasting architectures that abstain when evidence is stale, contradictory or uncertain.

These research results are not evidence that HCT will be profitable. They justify controlled experiments around calibration, routing and abstention.
