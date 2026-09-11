# HCT-ADR-0039 — Intelligence Brain Calibration, Abstention & Authority

Status: `APPROVED_FOR_DISCOVERY`
Date: 2026-09-11
Increment: `HCT-PLAN-0001-R02`
Risk class: `HIGH_ASSURANCE`

## Context
HCT now includes realtime market-state integrity, microstructure/order flow, indicators/features, strategy ecology, temporal memory/RAG, institutional agents, news/events, risk context and execution feasibility. A governed fusion layer is required to prevent these systems from becoming an opaque collection of correlated votes or an unrestricted LLM decision-maker.

## Decision
HCT will implement the Intelligence Brain as a structured, evidence-calibrated **candidate-decision layer**.

1. Every material contributor emits versioned structured evidence with provenance, event/knowledge time, freshness, horizon, confidence, reliability and contradiction metadata.
2. Evidence fusion must account for redundancy and common-cause dependence. Correlated evidence may not be counted as independent confirmation.
3. Confidence must be empirically calibrated chronologically and monitored for calibration drift.
4. Uncertainty is multi-dimensional. Critical data/regime/event/execution uncertainty may cause abstention even when aggregate directional confidence is high.
5. `WAIT`, `NO_TRADE`, `DATA_UNCERTAIN`, `EVIDENCE_CONFLICT` and `CALIBRATION_UNTRUSTED` are first-class outputs.
6. Agent dissent must remain visible in the final evidence bundle and cannot be erased through narrative synthesis.
7. The Brain remains subordinate to deterministic Safety Governor, Risk Engine, Session Policy, Position/Leverage and Execution controls.
8. Dynamic expert/model routing may be researched, but routing, calibration and model versions require governed promotion and rollback.
9. Expensive agent/LLM analysis is selectively escalated only for shortlisted opportunities; no LLM-per-tick architecture is required.
10. Promotion requires chronological OOS/walk-forward, calibration, risk-coverage, ablation, fragility, realistic-cost, paper/shadow and independent HIGH_ASSURANCE evidence.

## Research directions approved
- Evidence Independence Graph;
- Evidence Quality Tensor;
- Regime-Aware Calibration Surface;
- Calibration Drift Monitor;
- Uncertainty Budget Vector;
- Selective Decision Controller;
- Risk-Coverage Frontier;
- Dissent Materiality Score;
- Adversarial Decision Challenge;
- Decision Stability Test;
- Confidence Fragility Index;
- Opportunity Conviction Profile;
- Expert Reliability Ledger;
- Contextual Expert Routing Score;
- Intelligence Compute Governor.

## Consequences
HCT optimizes for **validated decision quality under bounded uncertainty**, not maximum trading frequency and not maximum nominal confidence. A system that abstains intelligently can be preferable to a system that always predicts.

No research technology defined here implies profitability. Each must demonstrate incremental value after fees, slippage, funding, latency, drawdown and calibration effects before promotion.
