# HCT-PLAN-0001-R11 — Requirements Freeze Input Inventory

Status: `R12_HANDOFF_INPUT`
Increment: `HCT-PLAN-0001-R11`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

## Purpose
Define the exact canonical requirement sources that R12 must consolidate losslessly into the planning-freeze baseline. This inventory closes R11 Gate AA and prevents accepted requirements from disappearing during document cleanup.

## Canonical requirement inputs

### Baseline requirements
1. `docs/02-requirements.md`
   - contains the original R01/R02 product requirements and subsequent promoted requirements;
   - contains the formal R03 institutional risk requirements that were consolidated directly into the canonical requirements file rather than maintained as a separate addendum.

### Formal round addenda
2. `docs/48-r04-execution-requirements-addendum.md`
   - Execution, OMS, reconciliation, command identity, uncertainty and protection requirements.

3. `docs/54-r05-realtime-requirements-addendum.md`
   - realtime transport, market-state generation, data authority/freshness, backpressure, quota and resilience requirements.

4. `docs/61-r06-intelligence-requirements-addendum.md`
   - Intelligence Brain, evidence admissibility, temporal memory, calibration, abstention, agents and learning-governance requirements.

5. `docs/67-r07-validation-laboratory-requirements-addendum.md`
   - point-in-time validation, replay, OOS/holdout, simulator realism, paper/shadow, promotion, rollback and independent-review requirements.

6. `docs/73-r08-multitenant-security-requirements-addendum.md`
   - tenant isolation, SecurityContext, SecretStore, authentication, privileged access, commercialization and security-lifecycle requirements.

7. `docs/80-r09-cockpit-uiux-requirements-addendum.md`
   - cockpit authority/freshness semantics, order evidence UX, protection/risk UI, accessibility, environment separation and frontend-integrity requirements.

8. `docs/87-r10-observability-audit-incident-finops-requirements-addendum.md`
   - observability non-authority, audit, SLO/SLI, incident response, compliance-readiness, retention/evidence and FinOps requirements.

9. `docs/93-r11-integration-requirements-addendum.md`
   - restrictive authority lattice, Authorization Bundle, Source-of-Truth ownership, dependency/failure propagation, module classification and cross-round integration requirements.

## Supporting authoritative sources
R12 requirement consolidation must be cross-checked against, at minimum:
- `docs/03-scope.md`;
- `docs/04-architecture.md`;
- `docs/05-security.md`;
- `docs/06-test-benchmark-plan.md`;
- `docs/09-definition-of-done.md` after R12 hardening;
- `docs/10-decisions-ledger.md`;
- `docs/14-product-module-map.md`;
- `docs/91-r11-integrated-authority-state-dependency-architecture.md`;
- `docs/92-r11-v1-module-classification-and-integration-hardening.md`.

Round final audits remain evidence that a set of requirements was reviewed/approved; they are not substitutes for the requirement text itself.

## R12 consolidation rules
R12 SHALL:
1. inventory every requirement from all nine canonical inputs above;
2. assign a stable frozen requirement ID or preserve an unambiguous source-to-frozen mapping;
3. preserve requirement intent, authority ceilings, safety predicates and scope classification;
4. deduplicate only when requirements are semantically equivalent, recording all source IDs/locations in traceability;
5. resolve wording conflicts according to Decisions Ledger and the latest approved formal-round contract;
6. never weaken a hard safety/security/risk/execution requirement merely to simplify prose;
7. explicitly mark `V1_CORE`, `V1_MINIMUM`, `IMPORTANT_POST_V1` or `FUTURE` applicability where relevant;
8. preserve `LIVE/PAPER/SHADOW/REPLAY` and tenant/account/environment distinctions;
9. preserve implementation/live prohibitions during planning freeze;
10. produce a traceability artifact proving every accepted source requirement maps to at least one frozen requirement or an explicit supersession decision.

## No-loss proof
The R12 freeze SHALL NOT be approved unless an automated or objectively reviewable traceability check demonstrates:
- source requirement count/inventory completed;
- zero unmapped accepted requirements;
- zero unexplained dropped requirements;
- zero unresolved contradictory authoritative requirements;
- zero CRITICAL/HIGH planning gaps.

## Precedence
If any input conflicts:
1. current approved Decisions Ledger;
2. later formal round requirement/architecture contract;
3. earlier formal requirement;
4. exploratory/pre-discovery material.

Any material conflict resolution that changes accepted scope or behavior requires explicit documentation and, where appropriate, a new Decision Ledger entry.

## R11 conclusion
All accepted formal requirement sources are now explicitly inventoried for R12. No implementation, production deployment, credentials, limited-live or real-money trading authority is created by this inventory.
