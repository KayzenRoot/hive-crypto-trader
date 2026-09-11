# HCT-PLAN-0001-R11 — System Integration Requirements Addendum

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R11`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

This addendum is canonical with prior accepted requirements until R12 freeze consolidation.

## R11-REQ-001 — Restrictive authority lattice
Live-capable actions SHALL require the intersection of applicable exchange capability, Security/Tenant, Harness, Safety, Session Policy, Risk, data-authority/freshness, reconciliation/protection and promotion/environment eligibility. No layer SHALL relax a stricter result from another authoritative domain.

## R11-REQ-002 — Two-phase position construction
Position sizing/leverage SHALL produce bounded proposals that receive final projected post-trade RiskSnapshot approval and Risk Reservation before exposure-increasing execution.

## R11-REQ-003 — Canonical Authorization Bundle
State-changing exchange commands SHALL bind all required security, exchange capability, data authority, Safety, Session Policy, RiskSnapshot, Risk Reservation, action-class and authorization-lease references.

## R11-REQ-004 — Action classes under degradation
HCT SHALL distinguish exposure-increasing, reducing, closing, protection, cancellation and reconciliation/recovery action classes so degraded modes can block risk creation without preventing required safety recovery.

## R11-REQ-005 — Harness cannot weaken safety
Harness/capability isolation SHALL restrict or quarantine capabilities without disabling required Safety/Risk/protection/reconciliation paths in a way that increases danger.

## R11-REQ-006 — Source-of-truth ownership
Each authoritative state family SHALL have one canonical internal owner and defined external authority/reconciliation source. Caches, UI and telemetry SHALL remain projections.

## R11-REQ-007 — Realtime subsystem boundaries
Quota/WS control, raw market ingest, data quality, coherent Market-State reconstruction and cache/hot-state projection SHALL have distinct ownership/contracts.

## R11-REQ-008 — Memory facade vs temporal engine
The product SHALL separate RAG/Market Memory consumer facade responsibilities from Temporal Memory/Analog/Continual Learning implementation responsibilities.

## R11-REQ-009 — Learning lifecycle vs promotion authority
Learning/Model Lifecycle MAY create/evaluate candidate versions but SHALL NOT self-promote them; R07 Promotion Laboratory retains independent promotion proof authority.

## R11-REQ-010 — Strategy/agent/Brain/Copilot separation
Strategies/agents/news/memory SHALL produce evidence; Strategy Ecology SHALL route/resolve redundancy; Brain SHALL fuse evidence into candidate decisions; Copilot SHALL orchestrate workflow. None bypasses deterministic Safety/Session/Risk/Execution.

## R11-REQ-011 — Environment namespace isolation
LIVE/PAPER/SHADOW/REPLAY SHALL be part of canonical state identities across Risk, OMS, positions, protection, audit and UI so hypothetical states cannot mutate live authority.

## R11-REQ-012 — Typed identity/version registry
Cross-domain IDs SHALL be typed/stable and behaviorally material versions/hashes SHALL be explicit. Mutable display names SHALL NOT substitute for canonical identity.

## R11-REQ-013 — Failure/degradation propagation
Every capability SHALL declare dependencies, affected action classes, fallback/degraded behavior and recovery proof expectations.

## R11-REQ-014 — Logical dependency DAG
Implementation planning SHALL follow dependency stages that establish contracts/security/exchange truth before higher intelligence/automation and preserve vertical-slice testing.

## R11-REQ-015 — Explicit module classification
Every accepted product module SHALL be classified `V1_CORE`, `V1_MINIMUM`, `IMPORTANT_POST_V1` or `FUTURE`, with architectural readiness separated from live activation.

## R11-REQ-016 — Signals feedback isolation
Signal-room/subscriber analytics SHALL NOT directly alter live trading behavior. Any learned use SHALL re-enter canonical evidence/learning/promotion governance.

## R11-REQ-017 — Admin/trading authority separation
Trading Cockpit and Admin Control Plane MAY share components but SHALL preserve distinct authorization surfaces and server-side privilege enforcement.

## R11-REQ-018 — Observability references domain truth
Audit/telemetry SHALL reference canonical domain evidence and SHALL NOT create competing shadow truth for orders, Risk, Security or account state.

## R11-REQ-019 — V1 foundations include tenancy/security/UI/operations
Multi-tenant/security foundations, cockpit safety, Harness/admin and minimum audit/observability SHALL be treated as V1 foundations rather than deferred commercialization polish.

## R11-REQ-020 — Optional evidence degradation is explicit
When FinOps/backpressure/availability suppresses optional agents/features/news/research, their evidence SHALL become explicitly unavailable/degraded; Brain/Strategy SHALL recompute/abstain rather than silently reuse stale values.

## R11-REQ-021 — Canonical localization boundary
Localization SHALL affect presentation only, never canonical IDs, enums, Strategy DSL/node types, audit codes or numeric execution semantics.

## R11-REQ-022 — Requirements traceability into R12
R12 SHALL consolidate `docs/02-requirements.md` plus accepted round addenda into a frozen traceable baseline without dropping accepted requirements.

## R11-REQ-023 — Formal-over-exploratory precedence
Where wording conflicts, approved formal round artifacts and Decisions Ledger SHALL override older exploratory/pre-discovery documents unless a later decision explicitly restores them.

## R11-REQ-024 — Provider/topology neutrality
Logical module/dependency boundaries SHALL NOT imply a specific production process/service/cloud topology before deployment planning/benchmark evidence authorizes it.

## R11-REQ-025 — System-level V1 success composition
Planning-complete V1 SHALL demonstrate a coherent path for exchange/data truth, deterministic capital safety, execution/reconciliation/protection, validation/promotion, tenant/security isolation, intelligence abstention, cockpit truth, incident/audit recovery and bounded operational cost.

## Scope invariant
R11 is integration planning only. It does not authorize any implementation Work Order, production topology, credentials, limited-live activation or real-money execution.
