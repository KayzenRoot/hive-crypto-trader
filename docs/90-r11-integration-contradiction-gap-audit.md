# HCT-PLAN-0001-R11 — Integration, Dependency & Cross-Round Contradiction Audit

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R11`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`
Initial verdict: `CORRECTION REQUIRED`

## Objective
Audit the complete approved R01–R10 plan as one system. R11 does not seek feature expansion. It seeks contradictions, overlapping authority, duplicate ownership, unsafe dependency cycles, ambiguous V1 classification and implementation-order hazards before the R12 planning-freeze candidate.

## CRITICAL integration gaps

### GAP-R11-01 — Sequential chain vs authority lattice
Several diagrams imply a strict sequential order among Safety, Risk, Session Policy, Position Sizing and Leverage, while approved decisions say exchange/security/global safety/risk/user policy can independently deny/tighten. A canonical deny/tighten authority lattice is required.

### GAP-R11-02 — Two-phase risk construction
Risk approval needs projected size/leverage/liquidation, while size/leverage are themselves subordinate to Risk. Define proposal → projected post-trade RiskSnapshot → final approved construction to avoid circular authority.

### GAP-R11-03 — Security/Tenant authority placement
SecurityContext, tenant/account binding and entitlement must be explicit preconditions to all protected trading domains, not optional nodes hidden in the business chain.

### GAP-R11-04 — Exchange capability/rule authority
Dynamic exchange rules/capabilities must gate Strategy/Risk/Execution/UI consistently. No core module may retain a conflicting static assumption.

### GAP-R11-05 — Reconciliation/protection recovery under restricted authority
When account truth is uncertain, ordinary new exposure is blocked but protection/reduce/reconciliation actions may remain allowed. Cross-module action classes and recovery authority need one canonical matrix.

### GAP-R11-06 — Harness vs Safety/Risk precedence
Harness can freeze/quarantine capabilities but may not disable required Safety/Risk/protection/reconciliation in a way that increases danger. Dependency-aware precedence must be canonical.

### GAP-R11-07 — Command authorization coherence
R03 RiskSnapshot/Reservation, R04 Command Authorization Lease, R08 SecurityContext and R05 freshness/authority all gate one exchange command. Define one canonical Authorization Bundle so execution cannot validate only a subset.

### GAP-R11-08 — State-source ownership
Orders, fills, positions, balances, market state, protection, risk reservations, tenant identity, policy, model versions and UI projections need one Source-of-Truth Matrix to prevent competing owners.

### GAP-R11-09 — Realtime subsystem ownership overlap
Modules 4, 5, 7, 29 and 30 overlap ingest, state, quality, quotas, backpressure and cache. Define boundaries and direction of dependency.

### GAP-R11-10 — Memory module overlap
Modules 18 and 41 overlap market memory/RAG/temporal analog/learning. Define facade vs temporal-intelligence implementation responsibilities and V1/advanced scope.

### GAP-R11-11 — Learning lifecycle vs Promotion Laboratory overlap
Module 19 and Module 31 both own evaluation/promotion/rollback concepts. Define candidate/model lifecycle ownership versus independent validation/promotion authority.

### GAP-R11-12 — Brain / Strategy Ecology / Agents / Copilot responsibility overlap
Routing, evidence fusion, debate/supervision and action orchestration must have distinct contracts. Agents cannot become a parallel strategy/risk authority.

### GAP-R11-13 — Live/paper/shadow namespace isolation across every module
R07 isolation must propagate through Exchange Adapter, Risk Reservation, OMS, Reconciliation, UI, audit and Signal Publishing; no shared state identity may accidentally bridge hypothetical and live authority.

### GAP-R11-14 — Cross-module identity/version registry
Canonical IDs/versions for tenant/account, symbol/contract, market generation, strategy, RiskSnapshot, reservation, command, exchange order, fill, position, model/prompt/tool, release and incident must compose without ambiguous reuse.

### GAP-R11-15 — Failure/degradation propagation graph
A failure in market data, private stream, cache, DB, SecretStore, model, observability, Telegram or UI should have an explicit blast-radius/degradation path rather than ad-hoc local behavior.

### GAP-R11-16 — Implementation dependency DAG
The current 42-module registry lacks a canonical build sequence. Implementing Brain/UI/agents before foundational contracts could create rewrites or unsafe mock semantics.

### GAP-R11-17 — V1 module classification ambiguity
Scope classifies themes, not every module. Each of the 42 modules needs `V1_CORE`, `V1_MINIMUM`, `IMPORTANT_POST_V1`, or `FUTURE` classification, with activation scope distinct from architectural readiness.

## HIGH integration gaps

### GAP-R11-18 — Signals/Telegram feedback isolation
Subscriber delivery/performance analytics must not silently become trading evidence or self-optimize strategies without entering the governed evidence/learning/promotion path.

### GAP-R11-19 — Admin Cockpit vs Trading Cockpit boundaries
Owner/admin operational actions and tenant trading actions must remain separate authority surfaces even if they share visualization components.

### GAP-R11-20 — Observability vs domain audit duplication
R10 telemetry/audit must reference domain evidence rather than create shadow copies that can diverge from OMS/Risk/Security records.

### GAP-R11-21 — Scope classification of multi-tenancy/security/observability/UI
These are clearly architectural prerequisites for a commercial V1, but the NECESSARY list is too broad/implicit. R11 should make classification explicit.

### GAP-R11-22 — Microstructure scope split
Module 40 contains both useful V1 microstructure features and advanced cross-market/lead-lag/anomaly R&D. The minimum V1 subset must be separated from advanced research.

### GAP-R11-23 — Agent/news scope split
Institutional agents and News/Event Intelligence are core intelligence inputs, but expensive/full workforce behavior should be capability-gated so V1 can run deterministic/cheap paths without requiring every agent.

### GAP-R11-24 — Full Copilot activation vs architecture readiness
V1 may include autonomous-capable architecture while live FULL_COPILOT activation remains gated by R07 promotion, policy, safety and future production authorization.

### GAP-R11-25 — Commercialization vs live eligibility
Multi-tenant billing/entitlement readiness must not imply every tenant/region/exchange account is legally/operationally eligible for live trading.

### GAP-R11-26 — Retention vs replay evidence
Bootstrap compaction must preserve enough point-in-time data/evidence for R07 promotion, incidents, audit and reconciliation. Data-retention priority needs one integrated rule.

### GAP-R11-27 — Cost/load shedding vs model/feature availability
FinOps/backpressure may drop optional computation, but Strategy/Brain must know which evidence became unavailable and abstain/degrade rather than consume stale last-known features silently.

### GAP-R11-28 — Localization vs canonical contracts
Localized UI text/number formatting cannot alter canonical IDs, state enums, DSL, audit meaning or execution parameters across frontend/backend.

### GAP-R11-29 — Cross-cutting requirements fragmentation
Canonical requirements now span `docs/02` plus multiple round addenda. R11 must inventory them and R12 must consolidate/freeze without dropping accepted requirements.

### GAP-R11-30 — Pre-discovery document precedence
R02-era exploratory docs remain valuable but may use older terminology/status. R11 must clarify that later formal round contracts override conflicting pre-discovery text while preserving historical context.

### GAP-R11-31 — Deployment topology still intentionally open
Integration design must remain provider/topology neutral; no dependency graph may accidentally require a specific cloud/streaming stack before deployment planning is authorized.

### GAP-R11-32 — V1 success criteria composition
Individual modules have gates, but V1 planning needs system-level acceptance themes spanning safety, correctness, replay proof, tenancy/security, cockpit integrity and operations.

## Initial assessment
The approved rounds are broadly compatible, but R11 identified 32 integration gaps: 17 CRITICAL and 15 HIGH. Most are boundary/ownership/classification problems rather than missing product capabilities. Closing them should reduce implementation rework and make R12 freeze a genuine system plan rather than a stack of excellent but independent module documents.

## Verdict rule
Any unresolved CRITICAL/HIGH R11 integration defect => `CORRECTION REQUIRED`. A missing authoritative dependency that prevents safe integration planning => `BLOCKED`. R11 approval remains planning-only.
