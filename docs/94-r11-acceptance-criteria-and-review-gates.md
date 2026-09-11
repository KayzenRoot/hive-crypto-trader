# HCT-PLAN-0001-R11 — Acceptance Criteria & Review Gates

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R11`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

## Gate A — Restrictive authority lattice
All live-capable action authority composes as deny/tighten intersections rather than a sequence where later modules can relax earlier gates.

## Gate B — Two-phase construction
Sizing/leverage proposal and final post-trade Risk approval resolve the Risk ↔ construction dependency without circular authorization.

## Gate C — Security/exchange/data preconditions
SecurityContext/tenant binding, exchange capability/rules, environment mode and R05 data authority are explicit prerequisites to protected actions.

## Gate D — Canonical Authorization Bundle
Execution validates all required security, policy, risk, reservation, freshness and lease references together.

## Gate E — Degraded action-class matrix
New/add exposure can be denied while reduce/close/protect/reconcile actions remain separately governable.

## Gate F — Harness/Safety precedence
Harness cannot disable required safety/recovery dependencies in a way that increases risk or bypasses Risk/Safety.

## Gate G — Source-of-truth matrix
Each state family has one internal canonical owner and explicit external authority/reconciliation source; cache/UI/telemetry remain projections.

## Gate H — Realtime boundary clarity
Modules 4/5/7/29/30 have non-overlapping ownership contracts and safe dependency direction.

## Gate I — Memory boundary clarity
RAG facade, Temporal Memory engine, Learning Lifecycle and Promotion Laboratory have separate responsibilities and no self-promotion cycle.

## Gate J — Strategy/agents/Brain/Copilot separation
Evidence routing, evidence production, fusion and orchestration are distinct; no parallel hard trading authority exists.

## Gate K — Environment namespace isolation
LIVE/PAPER/SHADOW/REPLAY identity propagates through every stateful high-assurance domain.

## Gate L — Typed identity/version registry
Cross-domain identity and material behavior versions are explicit and not based on mutable display names.

## Gate M — Failure/degradation propagation
Dependencies declare action-class impact, fallback/degraded state and recovery proof.

## Gate N — Implementation dependency DAG
A safe logical build order exists while permitting vertical slices and early observability/security foundations.

## Gate O — 42-module classification
Every accepted module is classified and no accepted module silently disappears.

## Gate P — Signals feedback isolation
Signal/subscriber analytics cannot directly self-modify live strategy/authority.

## Gate Q — Admin vs trading surface separation
Shared UI components do not collapse admin and tenant trading privilege planes.

## Gate R — Domain audit vs observability
R10 telemetry/audit references canonical domain evidence rather than creating shadow OMS/Risk/Security truth.

## Gate S — V1 cross-cutting foundations
Multi-tenancy/security/cockpit/Harness/minimum observability are explicitly V1 foundations.

## Gate T — Microstructure V1 split
Execution-relevant minimum is V1; advanced cross-market/anomaly R&D remains post-V1 unless promoted.

## Gate U — Agents/news V1 split
A minimum governed evidence workforce exists without making every expensive agent a launch dependency.

## Gate V — Copilot readiness vs activation
Autonomous-capable architecture does not imply production FULL_COPILOT authorization.

## Gate W — Commercial entitlement vs live eligibility
Billing/entitlement never substitutes for legal/exchange/security/promotion/Safety/Risk eligibility.

## Gate X — Retention vs replay/audit evidence
Compaction preserves mandatory recovery/audit/promotion evidence or explicitly downgrades dataset fidelity manifests.

## Gate Y — Load shedding/evidence availability
Suppressed optional evidence becomes explicitly unavailable/degraded and cannot remain silently fresh.

## Gate Z — Localization contract boundary
Localized presentation cannot mutate canonical contracts or execution semantics.

## Gate AA — Requirements consolidation handoff
All accepted round addenda are inventoried and R12 has an explicit no-loss consolidation obligation.

## Gate AB — Formal precedence over exploratory docs
Later approved formal contracts have explicit precedence over conflicting pre-discovery text.

## Gate AC — Topology neutrality
Logical dependency architecture does not prematurely select a cloud/service/process topology.

## Gate AD — System-level V1 success themes
Cross-module planning success criteria cover truth, safety, execution, proof, tenancy/security, intelligence, UI, incident recovery and cost.

## Gate AE — Canonical consistency
Scope, Module Map, Decisions, integration requirements, branch/PR state and checkpoint direction agree; implementation/live remains unauthorized and an objective final R11 audit exists.

## Verdict rule
- unresolved CRITICAL/HIGH integration defect => `CORRECTION REQUIRED`;
- missing dependency required to safely reconcile the system => `BLOCKED`;
- all gates pass => `APPROVED`.

R11 approval means the plan composes; it does not authorize implementation or production/live activity.
