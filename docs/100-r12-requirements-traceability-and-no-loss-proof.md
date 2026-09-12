# HCT-PLAN-0001-R12 — Requirements Traceability & No-Loss Proof

Status: `FREEZE_CANDIDATE`
Increment: `HCT-PLAN-0001-R12`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

## Purpose
Provide an objectively reviewable bridge from every accepted requirement source into the R12 frozen requirements baseline and from requirement families into the integrated HCT module/cross-cutting architecture.

## No-loss proof model
R12 does not deduplicate by deleting source requirements. Instead, `docs/99-r12-frozen-requirements-baseline.md` includes each of the nine accepted requirement source blobs in full.

Therefore, for every normative source statement `r`:
- `r` exists in exactly one recorded source blob position;
- that complete blob is included by the frozen manifest;
- thus `r` is mapped into the baseline by identity inclusion;
- overlap with another source does not remove `r`;
- supersession requires an explicit authoritative conflict resolution, never omission.

This is stronger than a paraphrase-based checklist because the approved source text itself remains normative.

## Source-to-baseline traceability

| Source | Inclusion | Traceability locator | Primary integrated domains/modules |
|---|---|---|---|
| `docs/02-requirements.md` | FULL BLOB | `REQ02::<heading>::B<ordinal>` or named semantic section | Product intent, exchange, indicators/features, strategies, Signals, Agents, News, Copilot, Risk, realtime, tenancy, UI and R01–R03 promoted requirements |
| `docs/48-r04-execution-requirements-addendum.md` | FULL BLOB | `R04::<heading>::B<ordinal>` | 24 Execution Intelligence, 25 OMS, 26 Reconciliation, 27 Protection, 29 Quota/WS, 20 Risk integration |
| `docs/54-r05-realtime-requirements-addendum.md` | FULL BLOB | `R05::<heading>::B<ordinal>` | 4 Market Data, 5 Market-State Fabric, 7 Data Quality, 29 Quota/Backpressure, 30 Cache, realtime cross-cutting controls |
| `docs/61-r06-intelligence-requirements-addendum.md` | FULL BLOB | `INT-001..026` + named validation/safety clauses | 17 Brain, 18 RAG, 19 Learning, 35 Agents, 37 News, 41 Temporal Memory plus R05/Risk coupling |
| `docs/67-r07-validation-laboratory-requirements-addendum.md` | FULL BLOB | `VAL-001..032` + named validation/safety clauses | 31 Validation Lab plus Risk/Execution/Intelligence/live-parity cross-cutting proof |
| `docs/73-r08-multitenant-security-requirements-addendum.md` | FULL BLOB | TEN/SEC/IAM/ADM/COM/DATA/OPS IDs | 32 Multi-Tenant Foundation, 38 Admin, 39 Harness, SecretStore/Security/DR/Commercial readiness |
| `docs/80-r09-cockpit-uiux-requirements-addendum.md` | FULL BLOB | `R09-REQ-001..040` | 33 Trading Cockpit, 38 Admin UI, frontend contract/security/accessibility and state-truth projection |
| `docs/87-r10-observability-audit-incident-finops-requirements-addendum.md` | FULL BLOB | `R10-REQ-001..045` | cross-cutting observability, audit, incident, compliance-readiness, FinOps plus 38/39 operational controls |
| `docs/93-r11-integration-requirements-addendum.md` | FULL BLOB | `R11-REQ-001..025` | cross-module authority lattice, Source-of-Truth, dependency DAG, environment isolation and V1 classification |

## Requirement-family to module traceability

### Exchange and market truth
Frozen sources: CORE, R04, R05, R11.
Primary modules: 1–7, 29–30.
Required invariants include dynamic capability/rule discovery, generation/freshness proof, quota safety, no cache authority upgrade and exchange-authoritative account reconciliation.

### Technical intelligence and strategy
Frozen sources: CORE, R05, R06, R07, R11.
Primary modules: 8–19, 40–41.
Required invariants include point-in-time features/evidence, strategy versioning, evidence admissibility, abstention, no self-promotion, temporal leakage firewall and independent promotion proof.

### Capital safety and position construction
Frozen sources: CORE/R03, R04, R05, R06, R07, R11.
Primary modules: 20–23, 28, 36, 39.
Required invariants include restrictive authority, two-phase construction, RiskSnapshot, Risk Reservation, survival/OMR, protection-failure exposure, cross-margin/collateral safety and no AI risk escalation.

### Execution, OMS and exchange-state truth
Frozen sources: CORE, R04, R05, R07, R08, R09, R10, R11.
Primary modules: 24–27 plus Exchange Adapter and Quota Governor.
Required invariants include authorization lease/bundle, acknowledgement != fill, fill idempotency, uncertain outcomes, cancel/replace races, reconciliation watermarks, recovery proof and protection integrity.

### Validation and production promotion
Frozen sources: CORE, R06, R07, R10, R11.
Primary module: 31 with dependencies across all material domains.
Required invariants include point-in-time universe/rules, OOS/holdout firewall, causal replay, realistic fills/frictions, environment isolation, immutable Promotion Evidence Bundles and independent HIGH_ASSURANCE review.

### Tenant, security and privileged operations
Frozen sources: CORE, R08, R09, R10, R11.
Primary modules: 32, 38, 39 plus cross-cutting Identity/SecretStore/Audit.
Required invariants include server-derived SecurityContext, exact tenant-account binding, secret isolation, admin/support identity, tenant-safe queues/cache/observability, environment isolation and trading-aware incident/DR recovery.

### Trading cockpit and operator truth
Frozen sources: CORE, R09, R10, R11.
Primary modules: 33 and 38.
Required invariants include frontend non-authority, UI State Envelope, stale/resync semantics, order Evidence Ladder, protection/risk priority, environment/context lock, accessibility and dashboard truth hierarchy.

### Autonomous intelligence and agents
Frozen sources: CORE, R06, R07, R08, R10, R11.
Primary modules: 17–19, 34–37, 41.
Required invariants include structured evidence, authority ceilings, bounded deliberation, tool/skill governance, model/prompt/version attribution, cost budgets and Copilot orchestration without parallel hard authority.

### Signal publishing
Frozen sources: CORE, R08, R10, R11.
Primary module: 42.
Required invariants include execution isolation, backend-only destination credentials, durable/idempotent outbox, freshness, lifecycle evidence, realizability metrics and governed feedback into research only.

### Observability, audit, incidents and FinOps
Frozen sources: R08, R09, R10, R11 plus `docs/06-test-benchmark-plan.md` as proof guidance.
Cross-cutting capability, strongly surfaced in modules 33, 38, 39.
Required invariants include telemetry non-authority, secret/tenant-safe telemetry, append-only audit, trading-aware SLOs, evidence-preserving incident recovery and FinOps safety boundary.

## V1 applicability traceability
`docs/92-r11-v1-module-classification-and-integration-hardening.md` is the authoritative module-classification source.

Requirement applicability rule:
- if a requirement belongs to a `V1_CORE` module/cross-cutting safety foundation, it is required for V1 implementation unless explicitly marked as future conditional behavior;
- if it belongs to a `V1_MINIMUM` module, the bounded minimum defined by Scope/R11 is required; advanced variants remain governed but can be deferred;
- `IMPORTANT_POST_V1` and `FUTURE` requirements remain part of architecture/change-control truth but do not block V1 completion unless explicitly promoted;
- hard safety/security/authority restrictions apply whenever the related capability is present, independent of release label.

## Decision traceability
Requirements are interpreted together with `docs/10-decisions-ledger.md`.

Key integration decisions:
- `HCT-DEC-0132`: restrictive authority lattice;
- `HCT-DEC-0133`: two-phase position construction;
- `HCT-DEC-0134`: Canonical Authorization Bundle;
- `HCT-DEC-0135`: one Source-of-Truth owner;
- `HCT-DEC-0136`: realtime/memory/learning/promotion boundaries;
- `HCT-DEC-0137`: Strategy/Agents/Brain/Copilot separation;
- `HCT-DEC-0138`: environment namespace + typed IDs;
- `HCT-DEC-0139`: dependency/failure graph + logical DAG;
- `HCT-DEC-0140`: 42-module classification;
- `HCT-DEC-0141`: formal precedence and lossless R12 consolidation.

Earlier Decisions remain authoritative for their domains and are not superseded merely because R12 freezes the planning set.

## Implementation Work Order traceability contract
Future implementation Work Orders, if separately authorized, SHALL reference:
- frozen baseline ID/version;
- exact requirement IDs or deterministic source locators implemented;
- modules/cross-cutting domains affected;
- Decisions/ADRs controlling behavior;
- applicable DoD clauses;
- tests/benchmarks/evidence required;
- rollback/recovery implications;
- any deferred/future requirement explicitly out of scope.

A Work Order that cannot identify its governing frozen requirements is incomplete.

## No-loss verification checklist
R12 final audit SHALL verify:
1. nine source paths exist;
2. nine source blob SHAs match `docs/99-r12-frozen-requirements-baseline.md`;
3. all explicit namespaces/ranges listed in the manifest remain present in their source blobs;
4. CORE/R04/R05 entire blobs are included by identity, making their unnumbered requirements non-droppable;
5. no later file silently claims to replace a source without a Decision Ledger entry;
6. Scope/module classifications do not erase hard authority restrictions;
7. implementation/live authorization remains false.

## Result
If the six content-integrity conditions above and authorization invariant pass, R12 has an objective no-loss mapping from all accepted requirements into one composite frozen baseline.
