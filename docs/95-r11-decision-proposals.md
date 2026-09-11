# HCT-PLAN-0001-R11 — Decision Proposals for Ledger Consolidation

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R11`
Date: `2026-09-11`

These decisions are accepted within R11 planning and must be consolidated into `docs/10-decisions-ledger.md` before final approval.

## HCT-DEC-0132 — Trading authority composes as a restrictive lattice, not a relaxable sequential chain
Status: APPROVED_FOR_DISCOVERY

Decision: exchange capability, Security/Tenant, Harness restrictions, Safety, Session Policy, Risk, data authority/freshness, reconciliation/protection and promotion/environment eligibility independently deny or tighten live-capable actions. No later module may relax a stricter decision from another authoritative domain.

## HCT-DEC-0133 — Position sizing/leverage use a two-phase proposal then final Risk approval
Status: APPROVED_FOR_DISCOVERY

Decision: Position Sizing and Leverage produce bounded construction proposals; Risk then computes the projected post-trade RiskSnapshot and may reduce/veto/recompute until one internally consistent construction is approved. Risk Reservation is committed before exposure-increasing submit.

## HCT-DEC-0134 — Every exchange mutation uses one canonical Authorization Bundle
Status: APPROVED_FOR_DISCOVERY

Decision: state-changing exchange commands bind required SecurityContext/tenant-account scope, environment, exchange capability/rules, data-authority/freshness, Safety, Session Policy, final RiskSnapshot, Risk Reservation, action class, execution intent and Command Authorization Lease. Missing/expired/mismatched authority rejects the command.

## HCT-DEC-0135 — Canonical state families have one source-of-truth owner and projections never become competing authority
Status: APPROVED_FOR_DISCOVERY

Decision: HCT adopts the R11 Source-of-Truth Matrix. Exchange/account truth is reconciled from the venue, domain owners maintain canonical internal state, and caches/UI/telemetry remain projections. Consumer convenience never creates a second authoritative owner.

## HCT-DEC-0136 — Realtime, memory, learning and promotion modules have explicit non-overlapping ownership boundaries
Status: APPROVED_FOR_DISCOVERY

Decision: Quota/WS, market ingest, data quality, Market-State Fabric and cache remain distinct realtime responsibilities. RAG is the governed consumer facade over Temporal Memory; Learning Lifecycle owns candidate/version lifecycle; Promotion Laboratory remains independent proof authority and prevents self-promotion.

## HCT-DEC-0137 — Strategy, agents, Brain and Copilot are separate evidence/orchestration layers
Status: APPROVED_FOR_DISCOVERY

Decision: Strategy/Agents/News/Memory produce or route evidence; Intelligence Brain is the canonical selective candidate-decision fusion layer; Copilot orchestrates workflow/tool/agent/action lifecycle. None becomes a parallel Safety/Risk/Execution authority.

## HCT-DEC-0138 — Environment namespace and typed identity/versioning are cross-domain invariants
Status: APPROVED_FOR_DISCOVERY

Decision: LIVE/PAPER/SHADOW/REPLAY environment identity is part of stateful high-assurance object identity. Cross-domain IDs are typed/stable, and behaviorally material versions/hashes are explicit; mutable display labels never substitute for canonical identity.

## HCT-DEC-0139 — HCT uses an explicit dependency/failure graph and staged logical implementation DAG
Status: APPROVED_FOR_DISCOVERY

Decision: every capability declares dependencies, action-class impact, degradation/fallback and recovery proof. Implementation planning follows the R11 logical stages from shared security/contracts through exchange/data, deterministic intelligence, capital safety, execution truth, validation, AI automation, operator surfaces and operational hardening, while allowing vertical slices and early security/audit/observability instrumentation.

## HCT-DEC-0140 — The 42 accepted modules receive explicit V1 classification without silent scope deletion
Status: APPROVED_FOR_DISCOVERY

Decision: R11 classifies every accepted module as `V1_CORE`, `V1_MINIMUM`, `IMPORTANT_POST_V1` or `FUTURE`. V1 module readiness is distinct from live activation. Deferring an accepted V1 module later requires an explicit Decision Ledger entry with impact analysis.

## HCT-DEC-0141 — Formal round contracts override conflicting exploratory wording and R12 must consolidate requirements losslessly
Status: APPROVED_FOR_DISCOVERY

Decision: approved formal round artifacts and Decisions Ledger take precedence over conflicting older exploratory/pre-discovery text. R12 must consolidate `docs/02-requirements.md` and accepted round addenda into one traceable freeze baseline without dropping accepted requirements, while preserving provider/topology neutrality and implementation/live prohibitions.
