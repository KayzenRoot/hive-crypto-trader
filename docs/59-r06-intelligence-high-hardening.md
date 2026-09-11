# HCT-PLAN-0001-R06 — Intelligence / Memory / Learning HIGH Hardening

Status: `DISCOVERY_IN_PROGRESS`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

## Purpose
Close the HIGH-severity gaps remaining after the R06 authority architecture.

## 1. Evidence Independence Graph
Every evidence item declares parent inputs and lineage. HCT constructs an evidence-dependency graph across raw feeds, features, indicators, strategies, models, agents and memory retrievals. Consensus is discounted when contributors share material upstream information. Effective independent evidence count is preserved alongside raw contributor count.

## 2. Uncertainty vector
Uncertainty remains decomposed into market/aleatoric, model/epistemic where estimable, data, regime, memory/analog, news/event and execution uncertainty. A critical uncertainty component may veto/abstain even if average uncertainty is low.

## 3. Bounded agent deliberation
Each decision session has maximum reasoning rounds, wall/monotonic deadline, inference/token/cost budget, tool-call budget and remaining-signal-lifetime budget. Expired or exhausted deliberation terminates with the best admissible evidence state and may abstain. Recursive agent loops are prohibited.

## 4. Adversarial review triggers
Devil's Advocate review is triggered by governed conditions such as high agent disagreement, narrow decision margin, high fragility, novel/uncertain regime, major news uncertainty, large portfolio impact, unusual leverage/margin stress, analog conflict or out-of-distribution evidence. Triggering adversarial review never bypasses the decision deadline.

## 5. Decision Stability Test
Before eligible directional candidates, selected decisions may be recomputed under bounded realistic perturbations to non-authoritative inputs: small price/feature changes, calibration uncertainty, analog subset changes and permissible model stochasticity. Material action flips or large probability swings increase fragility and can force `WAIT`/`NO_TRADE`.

## 6. Temporal retrieval policy
Retrieval ranks only point-in-time-admissible memories using a versioned combination of regime similarity, symbol/cluster relationship, horizon, microstructure, liquidity/volatility, event context, strategy state, execution environment, recency, historical relevance, drift penalty, provenance reliability and diversity.

## 7. Analog sufficiency
Analog evidence declares raw count, effective independent count, regime diversity, temporal dispersion, symbol/cluster diversity, retrieval score distribution and drift/relevance penalties. Below governed sufficiency thresholds, output is `INSUFFICIENT_ANALOG_EVIDENCE`; sparse anecdotes cannot be presented as strong statistical support.

## 8. Label maturity
Outcome labels have explicit horizons and maturity timestamps, including short horizons, session outcome, execution quality and risk/protection outcomes. A label may be used only for objectives whose maturity contract is satisfied. Later labels append evidence rather than rewriting ex-ante decisions.

## 9. Learning from abstention/no-trade
`WAIT`, `NO_TRADE`, `SAFETY_VETO` and `RISK_VETO` are evaluated later with bounded counterfactual analysis. Counterfactuals use realistic executable assumptions and are never recorded as actual fills/PnL. HCT measures both avoided harm and excessive conservatism while preserving selection-bias warnings.

## 10. Catastrophic forgetting / recurring regimes
Learning governance retains representative historical episodes and regime experts, monitors competence by regime, compares champion/challenger behavior and detects deterioration on previously learned conditions. Adaptation cannot erase useful historical competence without explicit promotion evidence.

## 11. Compute-aware intelligence routing
Escalation follows a cost/freshness ladder:
`cheap deterministic filters -> quantitative features -> shortlist -> temporal memory/analogs -> specialized agents/models -> adversarial review when triggered`.

Expensive work starts only when expected decision value, uncertainty reduction and remaining signal lifetime justify it. Work becomes cancellable when the opportunity expires or a hard upstream gate blocks exposure.

## 12. Decision Attribution Ledger
Each candidate decision links admissible evidence IDs, excluded/quarantined evidence, Brain/fusion version, calibration, memory retrieval set, agent board, strategy version, R05 state, decision result, downstream Safety/Risk/Execution decisions and matured outcomes. Attribution distinguishes opportunity error from risk veto, execution failure, data failure and post-decision market randomness.

## 13. Reproducible Brain replay
Deterministic components replay from pinned data/schema/version state. Stochastic/LLM components pin model/version, prompt/spec, tool/skill versions, retrieval snapshot, parameters and random seed where supported. If exact provider behavior cannot be reproduced, HCT labels the reproduction class explicitly rather than claiming bitwise determinism.

## 14. Observable reasoning without private chain-of-thought
Audit/cockpit exposes structured evidence IDs, provenance, calibration, uncertainty vector, disagreement, decision margin, stability result, retrieved episodes, exclusion reasons, model/agent versions, reason codes and final candidate state. Private chain-of-thought is neither required nor stored as an audit dependency.

## HIGH gap closure map
- GAP-03: section 1
- GAP-07: section 2
- GAP-09: section 3
- GAP-10: section 4
- GAP-11: section 5
- GAP-13: section 6
- GAP-14: section 7
- GAP-16: section 8
- GAP-17: section 9
- GAP-20: section 10
- GAP-23: section 11
- GAP-24: section 12
- GAP-27: section 13
- GAP-28: section 14

## Result
All 30 initial R06 CRITICAL/HIGH gaps now have explicit planning-resolution contracts across docs 58–59. Formal acceptance gates, requirements/decision consolidation and objective final audit are still required before R06 can be approved.
