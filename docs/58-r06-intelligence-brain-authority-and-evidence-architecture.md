# HCT-PLAN-0001-R06 — Intelligence Brain Authority & Evidence Architecture

Status: `DISCOVERY_IN_PROGRESS`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

## Purpose
Close the CRITICAL R06 gaps by defining how evidence becomes admissible, calibrated candidate decisions without allowing intelligence components to bypass deterministic safety, risk, policy or execution authority.

## 1. Authority chain
`Realtime/Data Quality -> Evidence Admission -> Intelligence Brain -> Candidate Decision -> Safety Governor -> Risk Engine -> Session Policy -> Position/Leverage -> Execution -> OMS -> Exchange -> Reconciliation`

The Brain may rank, abstain, recommend and explain. It may not place orders, raise hard risk/leverage, relax platform policy, reinterpret unknown exchange state optimistically, or self-promote intelligence changes.

## 2. Canonical Evidence Envelope
Every contribution entering fusion MUST carry a versioned envelope containing at minimum:
- `evidence_id`, schema/version and evidence family;
- tenant/account scope where applicable;
- exchange, canonical instrument, symbol/cluster and timeframe/horizon;
- `event_time`, `knowledge_time`, ingestion/computation time and expiration;
- `market_state_generation` and input-generation references;
- source identity, provenance and source reliability class;
- producer identity and exact feature/model/agent/retriever/prompt/skill/tool versions;
- value/distribution plus semantic type;
- confidence/uncertainty fields appropriate to that semantic type;
- calibration state/version;
- freshness/data-quality/coherency state;
- independence family, parent inputs and lineage references;
- contradictions/assumptions/limitations;
- authority ceiling and allowed use;
- immutable content hash/correlation identifiers.

Free-form prose may accompany evidence for humans, but it is never the authoritative machine contract.

## 3. Evidence Admissibility Gate
Before fusion, evidence receives one of `ADMIT`, `ADMIT_DEGRADED`, `QUARANTINE`, `REJECT`, `EXPIRED`.

Critical predicates include supported schema, known provenance, permitted producer/version, point-in-time validity, valid knowledge time, compatible market generation, required freshness, R05 data authority, no unresolved critical contradiction, calibration requirements where mandatory, tenant/policy scope and expiration.

A failed critical predicate cannot be hidden by a high aggregate score. `UNKNOWN` on a critical predicate is conservative and may force quarantine/rejection.

## 4. Confidence semantics
The Brain MUST preserve separate quantities rather than a universal confidence scalar:
- directional probability/distribution;
- opportunity quality;
- data confidence;
- calibration reliability;
- evidence independence/diversity;
- regime fit;
- historical/analog support;
- agent agreement/disagreement;
- execution feasibility;
- risk compatibility;
- decision stability/fragility.

A UI composite may exist only as a derived, versioned, explainable view and may not replace underlying components in authority decisions.

## 5. Calibration hierarchy
Calibration is versioned by applicable context. Candidate hierarchy may include strategy/model + horizon + regime + symbol/cluster, with fallback toward broader calibrated populations when sample support is insufficient.

Every calibration layer declares minimum effective sample size, recency window, drift status, error metrics, shrinkage/fallback rule and validity horizon. Insufficient or drifted support produces `CALIBRATION_UNTRUSTED`, never invented certainty.

## 6. Selective decision and abstention
Canonical candidate outputs include:
`LONG_CANDIDATE`, `SHORT_CANDIDATE`, `WAIT`, `NO_TRADE`, `DATA_UNCERTAIN`, `EVIDENCE_CONFLICT`, `CALIBRATION_UNTRUSTED`, `MODEL_UNAVAILABLE`, `MEMORY_UNAVAILABLE`.

Directional action requires explicit policy thresholds for calibrated evidence, decision margin, data authority, freshness, stability and required evidence families. Near ties, missing critical evidence, expired signal lifetime or unresolved contradictions prefer abstention.

`NO_TRADE` is a valid positive decision, not an error condition.

## 7. Agent evidence and authority
Agents publish structured Evidence Envelopes to an Evidence Board. They may question or contradict one another through bounded structured messages. They cannot write canonical market truth, mutate risk limits, place orders or directly promote models/skills.

Every agent output records assumptions, evidence references, temporal validity, uncertainty, contradiction targets, tool/source provenance and authority ceiling. Supervisor output remains a Brain candidate decision and is still subordinate to deterministic downstream gates.

## 8. Temporal memory point-in-time contract
Canonical memory distinguishes:
- event time;
- knowledge time;
- ingestion time;
- correction time;
- label maturity time;
- market-state generation;
- source/version/provenance.

Decision-time memory is immutable. Later outcomes are appended as separate labels/relations and never rewrite what was known ex ante. Historical replay may retrieve only information whose `knowledge_time` was available at the replay decision time.

## 9. Hindsight / leakage firewall
The Temporal Leakage Firewall rejects retrieval/training examples that expose future knowledge, later corrections unavailable at decision time, outcome-derived features, post-event summaries presented as prior knowledge or labels before their maturity horizon.

Leakage violations are auditable HIGH_ASSURANCE defects and invalidate affected evaluation evidence.

## 10. Drift localization and learning authority
Drift categories include source/data, feature, symbol/cluster, regime, strategy, model/calibration, execution and infrastructure. Adaptation starts only after localization and severity classification.

Permitted bounded online adaptation may include rolling calibration statistics, reliability estimates, drift scores, analog weighting inside frozen bounds and regime probabilities. Material model weights, strategy semantics, prompts with behavioral impact, retrievers, agent skills or memory policies require governed candidate creation and promotion.

No component can self-promote.

## 11. Version pinning
Every production candidate decision records exact versions/hashes for evidence schema, market-state generation, strategy, feature set, model, prompt/spec, agent, tool, skill, retriever, memory snapshot/index, calibration, policy and Brain fusion logic.

Unpinned material behavior is not production-reproducible and cannot receive normal live authority.

## 12. External web/news contamination boundary
External content is untrusted evidence until source identity, publication/event/knowledge timestamps, reliability, corroboration and expiration are established. Web/news content may be stored in a quarantine/research tier before canonical promotion.

Unverified external content cannot silently become training truth, immutable factual memory or a direct execution instruction. Conflicting sources remain explicit.

## 13. R05 Data Quality coupling
R05 authority states are hard upstream constraints. Failed continuity, schema, freshness, coherency, generation or clock predicates can reject evidence or restrict candidate outputs. The Brain cannot reason around an R05 `NO_NEW_EXPOSURE`, `RECONCILIATION_ONLY` or equivalent hard state.

## 14. Brain / Risk separation
Brain output describes opportunity, uncertainty and evidence. Risk determines permitted monetary exposure. High Brain confidence does not increase hard risk, leverage, loss budgets or portfolio ceilings.

Risk compatibility may veto or reduce a candidate but cannot be interpreted by the Brain as unused permission to consume more risk.

## 15. Fail-safe state machine
Brain operating states include:
`NORMAL`, `DEGRADED`, `MEMORY_UNAVAILABLE`, `CALIBRATION_UNTRUSTED`, `MODEL_UNAVAILABLE`, `EVIDENCE_CONFLICT`, `DATA_UNTRUSTED`, `NO_NEW_EXPOSURE_RECOMMENDED`.

Each state defines allowed evidence classes, allowed candidate outputs, fallback path, observability and recovery proof. Loss of an optional intelligence layer may degrade to deterministic evidence only; loss of a required critical predicate causes abstention/restriction.

## 16. Promotion proof
Changes to models, retrievers, prompts/specs, agent skills, calibration, fusion logic or memory policy require an immutable candidate version and incremental-value proof through applicable stages:
`offline evaluation -> point-in-time replay -> walk-forward/OOS -> paper -> shadow -> champion/challenger -> governance promotion`.

Evaluation includes decision quality, calibration, abstention quality, false-confidence harm, regime robustness, costs/frictions, latency, failure behavior and comparison with the current champion/no-component baseline. Better prose or explanation quality alone is insufficient.

## CRITICAL gap closure map
- GAP-01: sections 2–3
- GAP-02: section 3
- GAP-04: section 4
- GAP-05: section 5
- GAP-06: section 6
- GAP-08: section 7
- GAP-12: section 8
- GAP-15: section 9
- GAP-18: section 10
- GAP-19: section 10
- GAP-21: section 11
- GAP-22: section 12
- GAP-25: section 13
- GAP-26: section 14
- GAP-29: section 15
- GAP-30: section 16

## Safety invariant
Intelligence is permitted to become more selective, better calibrated and more informative. It is never permitted to become a hidden authority escalation path.
