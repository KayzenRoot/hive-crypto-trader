# HCT-PLAN-0001-R06 — Intelligence Brain / Temporal Memory / Governed Learning Requirements Addendum

Status: `ACCEPTED_FOR_R06_PLANNING`
Increment: `HCT-PLAN-0001-R06`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

## Purpose
This addendum is the canonical R06 requirements source together with `docs/02-requirements.md` until planning-freeze consolidation. It converts the accepted R06 architecture in docs 57–60 into explicit product requirements.

## INT-001 — Candidate-decision authority only
The Intelligence Brain may rank, abstain, recommend and explain candidate actions. It SHALL NOT place exchange orders, raise hard risk/leverage, relax platform/session policy, override Safety/Risk/Execution/Reconciliation, or self-promote intelligence changes.

## INT-002 — Canonical Evidence Envelope
Every machine-authoritative evidence contribution entering Brain fusion SHALL use a versioned Evidence Envelope containing identity, semantic type, symbol/horizon, event/knowledge/ingestion time, expiration, market-state/input generations, source/provenance, producer and exact behavior versions, uncertainty/calibration state, freshness/data quality/coherency, lineage/independence, contradictions/assumptions, authority ceiling and immutable correlation/hash information.

## INT-003 — Deterministic evidence admissibility
Evidence SHALL receive `ADMIT`, `ADMIT_DEGRADED`, `QUARANTINE`, `REJECT` or `EXPIRED` before fusion. Unsupported schema, missing/invalid provenance, temporal contamination, expired validity, incompatible generation, failed critical R05 authority state or other failed critical predicate SHALL NOT be hidden by aggregate confidence.

## INT-004 — Separate confidence semantics
Directional probability, opportunity quality, data confidence, calibration reliability, evidence independence/diversity, regime fit, historical support, agent agreement, execution feasibility, risk compatibility and decision stability SHALL remain distinct. A composite UI score may exist only as a derived explainable view and SHALL NOT replace underlying authority-relevant components.

## INT-005 — Calibration hierarchy and distrust state
Calibration SHALL be versioned by applicable context with explicit sample sufficiency, recency, drift, validity and shrinkage/fallback rules. Insufficient or drifted calibration SHALL produce `CALIBRATION_UNTRUSTED` rather than fabricated certainty.

## INT-006 — Selective decision and abstention
`WAIT`, `NO_TRADE`, `DATA_UNCERTAIN`, `EVIDENCE_CONFLICT`, `CALIBRATION_UNTRUSTED`, `MODEL_UNAVAILABLE` and `MEMORY_UNAVAILABLE` SHALL be first-class outcomes. Directional candidates require governed thresholds for admissibility, calibration, data authority, decision margin, stability, freshness and required evidence families. Near-tie, expired or critically uncertain decisions SHALL abstain rather than be forced directional.

## INT-007 — Evidence independence and uncertainty decomposition
HCT SHALL track evidence lineage/dependence so correlated inputs are not double-counted as independent consensus. Uncertainty SHALL remain decomposed at minimum across market, model, data, regime, memory/analog, news/event and execution domains; a critical uncertainty component may independently force abstention/degradation.

## INT-008 — Agent structured evidence and bounded authority
Agents SHALL publish structured evidence with provenance, temporal validity, assumptions, confidence/uncertainty, contradiction targets, tools/sources and authority ceiling. No agent, including supervisor agents, SHALL directly place orders, mutate risk limits, write exchange truth or promote model/skill versions.

## INT-009 — Bounded deliberation
Multi-agent/model deliberation SHALL have governed round, time, token/inference-cost, tool-call and remaining-signal-lifetime budgets. Recursive unbounded loops are prohibited. Expired/exhausted deliberation SHALL terminate with an admissible abstention/fallback rather than consume stale opportunity lifetime.

## INT-010 — Adversarial and stability controls
Governed adversarial review triggers SHALL exist for fragile/high-impact/uncertain decisions. Selected directional candidates SHALL support bounded Decision Stability Tests under realistic perturbations; material action flips or probability instability SHALL tighten confidence or force abstention.

## INT-011 — Point-in-time Temporal Market Memory
Every canonical memory element SHALL preserve event time, knowledge time, ingestion time, correction time, label maturity time, market-state generation and source/version/provenance. Decision-time memory is immutable; later outcomes SHALL be appended separately and SHALL NOT rewrite ex-ante knowledge.

## INT-012 — Temporal Leakage Firewall
Historical replay, retrieval and training SHALL reject future knowledge, later corrections unavailable at the decision time, outcome-derived inputs masquerading as prior features and labels before maturity. A material leakage defect invalidates affected evaluation/promotion evidence.

## INT-013 — Governed temporal retrieval and analog sufficiency
Temporal retrieval SHALL use versioned point-in-time filters/ranking including regime, symbol/cluster, horizon, microstructure, event context, execution environment, recency, drift, provenance reliability and diversity. Historical analog evidence SHALL expose raw/effective independent counts and diversity. Sparse/duplicate evidence SHALL produce `INSUFFICIENT_ANALOG_EVIDENCE` rather than strong support.

## INT-014 — Label maturity and no-trade learning
Outcome labels SHALL mature under explicit horizons before they are eligible for relevant learning objectives. `WAIT`, `NO_TRADE`, `SAFETY_VETO` and `RISK_VETO` may be evaluated using bounded counterfactuals, but hypothetical fills/PnL SHALL never be recorded as actual execution.

## INT-015 — Drift localization before adaptation
Detected drift SHALL be localized to source/data, feature, symbol/cluster, regime, strategy, model/calibration, execution or infrastructure before adaptation. Unscoped `drift -> retrain everything` behavior is prohibited.

## INT-016 — Continual-learning authority boundary
Only explicitly approved bounded online statistics such as calibration/reliability/drift/regime estimates may adapt inside frozen limits. Material changes to model weights, strategy semantics, behaviorally material prompts, retrievers, agent skills or memory policies SHALL require a candidate version plus governed offline validation and promotion. Self-promotion is prohibited.

## INT-017 — Recurring-regime competence preservation
Learning governance SHALL retain representative historical episodes/regime competence, detect catastrophic forgetting and compare champion/challenger behavior across current and recurring regimes. Adaptation SHALL NOT silently erase previously useful competence.

## INT-018 — Full behavior version pinning
Every production-eligible candidate decision SHALL identify exact material versions/hashes for evidence schema, market-state generation, strategy, feature set, model, prompt/spec, agent, tool, skill, retriever, memory snapshot/index, calibration, policy and Brain fusion logic. Unpinned material behavior SHALL NOT receive normal production authority.

## INT-019 — External web/news contamination boundary
External web/news content SHALL remain untrusted until source identity, event/publication/knowledge timestamps, reliability, corroboration and expiration are established. Unverified external content SHALL NOT silently become canonical training truth, immutable factual memory or an execution instruction.

## INT-020 — Compute-aware intelligence routing
Expensive RAG/agent/LLM work SHALL be escalated only when shortlist value, expected uncertainty reduction, cost budget and remaining signal lifetime justify it. Intelligence work SHALL be cancellable when the opportunity expires or a deterministic upstream gate blocks exposure.

## INT-021 — Decision Attribution Ledger
Each candidate decision SHALL link admitted and excluded/quarantined evidence, Brain/fusion version, calibration, memory retrieval set, agent board, strategy, R05 state, candidate result, downstream Safety/Risk/Execution actions and matured outcomes. Attribution SHALL distinguish opportunity error from risk veto, execution failure, data failure and market randomness.

## INT-022 — R05 hard coupling
Critical R05 data-authority states SHALL directly constrain evidence admission and candidate outputs. The Brain SHALL NOT reason around `NO_NEW_EXPOSURE`, `RECONCILIATION_ONLY`, failed critical continuity/schema/freshness/coherency predicates or equivalent upstream authority states.

## INT-023 — Brain/Risk separation
Brain confidence/opportunity estimates SHALL NOT increase hard monetary risk, leverage, loss budgets, margin ceilings or portfolio limits. Risk compatibility is a constraint, never unused permission for the Brain to consume more risk.

## INT-024 — Explicit fail-safe modes
The Brain SHALL expose explicit operating states including `NORMAL`, `DEGRADED`, `MEMORY_UNAVAILABLE`, `CALIBRATION_UNTRUSTED`, `MODEL_UNAVAILABLE`, `EVIDENCE_CONFLICT`, `DATA_UNTRUSTED` and `NO_NEW_EXPOSURE_RECOMMENDED`, each with permitted outputs, fallback behavior and recovery proof.

## INT-025 — Reproducible replay and bounded observability
Deterministic components SHALL replay from pinned state. Stochastic/LLM reproduction SHALL pin available model/prompt/tool/retrieval/parameter/seed state and label reproduction fidelity honestly. Audit/cockpit SHALL expose structured evidence, provenance, calibration, uncertainty, disagreement, decision margin, stability, retrieved IDs, versions and reason codes without requiring or storing private chain-of-thought.

## INT-026 — Promotion proof
Material intelligence changes SHALL require incremental-value proof through applicable offline evaluation, point-in-time replay, walk-forward/OOS, paper, shadow and champion/challenger stages before production promotion. Evaluation SHALL include calibration, abstention quality, false-confidence harm, regime robustness, latency/cost/failure behavior and current-champion/no-component baselines. Better prose alone is not evidence of better trading decisions.

## Validation requirements
Future implementation Work Orders SHALL include deterministic tests for admissibility, generation/freshness coupling, temporal leakage, calibration fallback, near-tie abstention, agent authority, budget exhaustion, analog insufficiency, label maturity, drift localization, version pinning, external-source quarantine, R05 hard-state coupling, Brain/Risk separation, fail-safe recovery and promotion rollback.

## Safety
This document grants planning acceptance only. `implementation_authorized=false`; production credentials and live trading remain unauthorized.