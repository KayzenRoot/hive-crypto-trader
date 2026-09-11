# HCT-PLAN-0001-R06 — Intelligence Brain / Temporal RAG / Market Memory / Governed Learning Gap Audit

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R06`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`
Initial verdict: `CORRECTION REQUIRED`

## Objective
Formally reconcile the Intelligence Brain, temporal market memory, RAG, agent evidence, calibration and continual-learning pre-discovery against the needs of a HIGH_ASSURANCE automated futures platform.

The Brain is a candidate-decision authority only. It never bypasses Safety, Risk, Session Policy, Position/Leverage, Execution or Reconciliation.

## Canonical pre-discovery inputs
- `docs/34-temporal-market-memory-rag-and-continual-learning.md`
- `docs/35-intelligence-brain-evidence-fusion-calibration-and-selective-decision.md`
- `docs/27-institutional-agent-workforce-and-news-intelligence.md`
- `docs/26-strategy-ecology-router-ensemble-and-conflict-resolution.md`
- `docs/21-adaptive-multi-timeframe-and-opportunity-score.md`
- R03 Risk, R04 Execution and R05 realtime/data-quality contracts

## Strengths already present
- structured evidence fusion instead of unconstrained model output;
- explicit abstention / `WAIT` / `NO_TRADE` paths;
- confidence calibration and expert reliability concepts;
- redundancy-aware evidence aggregation;
- temporal market memory with `event_time` vs `knowledge_time`;
- global + recent memory routing;
- historical analog retrieval returning distributions instead of anecdotes;
- immutable ex-ante decision memory;
- governed continual learning and champion/challenger concepts;
- agent/tool/skill governance and authority ceilings;
- deterministic downstream Safety/Risk/Execution boundaries.

## R06 gaps

### GAP-R06-01 — Canonical Evidence Envelope
Severity: `CRITICAL`
Need one versioned schema for every evidence contribution entering the Brain, including source identity, feature/model/agent version, symbol/timeframe, event/knowledge time, market-state generation, freshness, confidence, calibration state, provenance, independence family and contradiction metadata.

### GAP-R06-02 — Evidence admissibility gate
Severity: `CRITICAL`
The Brain needs deterministic admission rules that reject/quarantine evidence with stale market generation, missing provenance, temporal contamination, unsupported schema, expired validity or failed data-quality predicates before fusion.

### GAP-R06-03 — Evidence independence graph contract
Severity: `HIGH`
Need a reproducible method for tracking shared inputs, correlated indicators, derivative features, agent dependence and model lineage so apparent consensus is not double-counted.

### GAP-R06-04 — Confidence semantics separation
Severity: `CRITICAL`
Directional probability, opportunity quality, data confidence, execution feasibility, calibration reliability and risk compatibility must remain distinct. One global “confidence” number cannot silently mix incompatible meanings.

### GAP-R06-05 — Calibration hierarchy and fallback
Severity: `CRITICAL`
Need explicit calibration levels by strategy/model/regime/symbol/horizon with minimum sample requirements, shrinkage/fallback behavior and `CALIBRATION_UNTRUSTED` when evidence is insufficient or drifted.

### GAP-R06-06 — Selective prediction / abstention policy
Severity: `CRITICAL`
Need deterministic decision thresholds/margins for `LONG`, `SHORT`, `WAIT`, `NO_TRADE`, `DATA_UNCERTAIN`, `EVIDENCE_CONFLICT` and `CALIBRATION_UNTRUSTED`, including what happens when top actions are nearly tied.

### GAP-R06-07 — Uncertainty decomposition
Severity: `HIGH`
Need explicit separation of market randomness, model uncertainty, data uncertainty, regime uncertainty, memory uncertainty, news uncertainty and execution uncertainty so one average uncertainty score cannot hide a critical component.

### GAP-R06-08 — Agent evidence contract and authority
Severity: `CRITICAL`
All agents must emit structured evidence, not free-form trade authority. Agent output requires provenance, temporal validity, confidence/uncertainty, assumptions, conflicts and authority ceiling. No agent may directly place orders.

### GAP-R06-09 — Deliberation termination and bounded cost
Severity: `HIGH`
Need bounded rounds, timeout/cost/token budgets, escalation conditions and stop rules for agent debate so multi-agent reasoning cannot consume the signal lifetime or create runaway inference cost.

### GAP-R06-10 — Adversarial review trigger policy
Severity: `HIGH`
Need deterministic conditions for invoking Devil’s Advocate / adversarial review, especially high disagreement, high risk, event uncertainty, fragile decisions, novel regime or large position impact.

### GAP-R06-11 — Decision Stability Test contract
Severity: `HIGH`
Need reproducible perturbation tests for fragile decisions and explicit rules for how sensitivity to small realistic changes reduces confidence or forces abstention.

### GAP-R06-12 — Memory point-in-time contract
Severity: `CRITICAL`
Every retrievable memory element must preserve `event_time`, `knowledge_time`, ingestion/correction times and market-state generation so historical retrieval cannot leak future information.

### GAP-R06-13 — Temporal retrieval policy
Severity: `HIGH`
Need deterministic filters/ranking combining recency, regime, symbol/cluster, microstructure, event context, strategy state, execution environment, drift penalty, diversity and historical reliability.

### GAP-R06-14 — Analog-set sufficiency and diversity
Severity: `HIGH`
Need minimum independent episode counts, regime diversity, recency/relevance checks and explicit `INSUFFICIENT_ANALOG_EVIDENCE`; a small cluster of near-duplicate episodes cannot masquerade as strong history.

### GAP-R06-15 — Hindsight bias and outcome leakage
Severity: `CRITICAL`
Decision-time memory must remain immutable and separate from later outcome labels. Retrieval used for a historical/replay decision may only expose knowledge actually available at that time.

### GAP-R06-16 — Learning-label maturity
Severity: `HIGH`
Need explicit maturation windows for labels such as 1m/5m/15m/1h/4h/session/execution/risk outcome so partially matured outcomes do not silently train long-horizon behavior.

### GAP-R06-17 — Learn-from-no-trade contract
Severity: `HIGH`
WAIT/NO_TRADE/SAFETY_VETO/RISK_VETO decisions must be evaluated later using bounded counterfactuals without pretending hypothetical fills were guaranteed.

### GAP-R06-18 — Concept drift localization
Severity: `CRITICAL`
Drift must be localized to data/source, feature, symbol, regime, strategy, model, execution or infrastructure before adaptation. `drift -> retrain everything` is prohibited.

### GAP-R06-19 — Continual-learning authority boundary
Severity: `CRITICAL`
Safe online adaptation may update bounded calibration/reliability/drift statistics, but material strategy/model parameters require governed offline validation and promotion. No self-promotion.

### GAP-R06-20 — Catastrophic forgetting / recurring regime control
Severity: `HIGH`
Need experience-replay/regime-expert/champion-challenger policies that preserve historically useful competence while adapting to recurring or new market regimes.

### GAP-R06-21 — Model/tool/skill version pinning
Severity: `CRITICAL`
Every production decision must identify exact model, prompt/spec, skill, tool, retriever, calibration and policy versions so behavior is reproducible and changes are auditable.

### GAP-R06-22 — External web/news contamination boundary
Severity: `CRITICAL`
Unverified web/news content cannot silently enter canonical market memory or training data. Source reliability, corroboration, event/knowledge timestamps and expiration must be explicit.

### GAP-R06-23 — Compute-aware intelligence routing
Severity: `HIGH`
Need deterministic escalation from cheap quantitative layers to expensive memory/agent/LLM analysis based on shortlist value, uncertainty and signal lifetime. Costly reasoning must be cancellable when opportunity expires.

### GAP-R06-24 — Decision-to-outcome attribution
Severity: `HIGH`
Need an immutable attribution ledger connecting evidence, model/agent versions, decision, downstream Safety/Risk/Execution actions and matured outcomes so post-trade learning does not credit or blame the wrong component.

### GAP-R06-25 — Brain/data-quality coupling
Severity: `CRITICAL`
R05 realtime authority states must directly constrain Brain evidence admission and decision output. A sophisticated model cannot “reason through” failed critical feed predicates.

### GAP-R06-26 — Brain/Risk separation
Severity: `CRITICAL`
The Brain may estimate opportunity and uncertainty but must not convert high confidence into higher hard risk/leverage. Risk compatibility is an input/output constraint, not a permission to rewrite ceilings.

### GAP-R06-27 — Reproducible Brain replay
Severity: `HIGH`
Need replay contracts for deterministic quantitative components and controlled reproduction for stochastic/LLM components with pinned versions, prompts, tools, memory snapshot and random seeds where applicable.

### GAP-R06-28 — Brain observability without hidden reasoning exposure
Severity: `HIGH`
Cockpit/audit must expose structured evidence, sources, calibration, disagreement, decision margin, uncertainty, retrieved episode IDs and reason codes without exposing private chain-of-thought.

### GAP-R06-29 — Brain fail-safe modes
Severity: `CRITICAL`
Need explicit states such as `NORMAL`, `DEGRADED`, `MEMORY_UNAVAILABLE`, `CALIBRATION_UNTRUSTED`, `MODEL_UNAVAILABLE`, `EVIDENCE_CONFLICT`, `NO_NEW_EXPOSURE_RECOMMENDED` and deterministic fallbacks.

### GAP-R06-30 — Promotion proof for intelligence changes
Severity: `CRITICAL`
New models, retrievers, prompts, agent skills, calibration methods and memory policies require incremental-value proof in the Simulation/Replay/Paper/Shadow laboratory. Better explanations alone do not prove better decisions.

## Priority closure order
### CRITICAL first
1. Canonical Evidence Envelope
2. Evidence admissibility
3. confidence semantics separation
4. calibration hierarchy/fallback
5. selective prediction/abstention
6. agent evidence/authority
7. point-in-time memory contract
8. hindsight/outcome leakage firewall
9. drift localization
10. continual-learning authority
11. model/tool/skill pinning
12. external-source contamination boundary
13. realtime data-quality coupling
14. Brain/Risk separation
15. fail-safe modes
16. promotion proof

### HIGH next
Independence graph, uncertainty decomposition, bounded deliberation, adversarial trigger policy, stability testing, temporal retrieval, analog sufficiency/diversity, label maturity, no-trade learning, catastrophic forgetting, compute-aware routing, decision attribution, reproducible replay and observability.

## Initial R06 verdict
`CORRECTION REQUIRED`

Reason: the pre-discovery is strong, but the Brain and memory/learning domains still need explicit admissibility, authority, temporal, calibration, adaptation and promotion contracts before formal approval.

## Next necessary action
Create the formal R06 Intelligence Brain / evidence-fusion / temporal-memory authority architecture closing CRITICAL gaps first, then harden HIGH gaps, define acceptance gates and run the final audit.

## STOP CONDITION
Do not approve R06 while any CRITICAL/HIGH planning gap remains unresolved. No implementation Work Order and no live authority are granted by this round.
