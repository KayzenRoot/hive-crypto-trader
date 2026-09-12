# HCT-PLAN-0001-R12 — Freeze Governance, Change Control and Deferred Decisions

Status: `FREEZE_CANDIDATE`
Increment: `HCT-PLAN-0001-R12`
Risk class: `HIGH_ASSURANCE`

## Freeze semantics
`FREEZE_APPROVED` means the planning baseline is coherent, lossless, traceable and change-controlled enough to serve as the normative input to a later implementation-authorization process.

Freeze does **not** mean the product can never change. It means material change must be explicit, impact-assessed, reviewed and checkpointed.

Freeze does not authorize implementation, production credentials, production deployment, limited-live activation or real-money trading.

## Frozen planning package
Upon governed R12 approval/merge/checkpoint promotion, the frozen planning package consists of:
- frozen composite requirements manifest and its exact source blob identities;
- requirement traceability/no-loss proof;
- Scope;
- Architecture;
- Security;
- Test & Benchmark Plan;
- project-wide HIGH_ASSURANCE Definition of Done;
- Decisions Ledger and approved ADRs;
- Product Module Map and R11 integration/classification artifacts;
- R12 deferred/residual-risk registry;
- R12 final freeze audit and checkpoint.

The checkpoint and Decisions Ledger remain higher precedence than the frozen requirements package under `docs/00-source-hierarchy.md`.

## Material change rule
A change is material when it modifies any accepted requirement meaning, module authority, safety/security/risk/execution invariant, V1 classification, external contract, data/economic truth ownership, implementation dependency, test obligation, DoD obligation, promotion/live boundary or deferred-decision disposition.

Material post-freeze changes require:
1. a new governed Work Order / change increment;
2. exact frozen baseline/version being changed;
3. affected requirement IDs/source locators and modules;
4. rationale and impact analysis across Scope, Architecture, Security, Tests, DoD, migration/recovery and dependent modules;
5. explicit Decisions Ledger/ADR update when decision authority changes;
6. updated frozen manifest/traceability version where requirements change;
7. applicable regression/re-audit evidence;
8. independent review;
9. governed merge and checkpoint promotion.

Silent semantic edits to frozen components are prohibited.

## Non-material editorial changes
Spelling, formatting or link corrections that provably do not change semantics may use a bounded documentation Work Order. Evidence must show no normative meaning, identifier, authority, classification or acceptance condition changed.

## Drift detection contract
After freeze, any change in blob identity for a frozen requirement component, Scope, Architecture, Security, DoD, Decisions Ledger or other source designated frozen-critical triggers impact review before the changed state may become canonical.

Future automation SHOULD compare frozen-critical path/blob identities and fail closed on unexplained drift.

## Deferred decisions and exceptions registry
The following items are intentional deferred decisions, not unresolved R12 planning defects, provided their current safety boundary remains intact.

| ID | Deferred item | Current classification | Why deferred | Required future gate | Current authority |
|---|---|---|---|---|---|
| `R12-DEF-001` | production deployment topology | `DEFERRED_EVIDENCE_DEPENDENT` | topology should follow measured workload/security/cost needs, not be guessed during discovery | separate deployment/infrastructure Work Order + DoD §8 | not authorized |
| `R12-DEF-002` | production strategy formulas/parameters | `DEFERRED_VALIDATION_DEPENDENT` | must be derived and validated through governed research/promotion evidence | implementation + R07 Promotion Laboratory | not authorized |
| `R12-DEF-003` | final leverage/exposure limits | `DEFERRED_RISK_EVIDENCE_DEPENDENT` | requires exchange rules, empirical risk evidence and bounded live-readiness review | Risk implementation + validation + live gate | not authorized |
| `R12-DEF-004` | final commercial plans/pricing | `IMPORTANT_POST_V1_OR_SEPARATE_COMMERCIAL_DECISION` | product/commercial evidence still required | governed commercialization increment | not required for technical V1 freeze |
| `R12-DEF-005` | jurisdiction-specific legal/compliance conclusions | `DEFERRED_EXTERNAL_AUTHORITY` | requires current qualified/legal/exchange/regional evidence | explicit eligibility/compliance review before availability | no unsupported compliance claim |
| `R12-DEF-006` | paid Signals commercialization | `DEFERRED_LEGAL_COMMERCIAL` | requires legal/commercial/regional review | separate Signals commercialization gate | technical publishing path may be planned only |
| `R12-DEF-007` | additional live exchanges beyond MEXC Futures | `FUTURE` | current V1 target is MEXC Futures | explicit scope promotion + adapter validation | no live authority |
| `R12-DEF-008` | unrestricted mobile live-trading authority | `FUTURE` | high-risk operator/security/UX surface | explicit future decision and live-readiness proof | prohibited |
| `R12-DEF-009` | production credentials/secrets | `DEFERRED_UNTIL_DEPLOYMENT_AUTHORIZATION` | secrets must never be placed in repository planning | SecretStore/environment authorization | absent/prohibited in repo |
| `R12-DEF-010` | limited-live activation | `DEFERRED_PROMOTION_AND_LIVE_READINESS` | requires R07 evidence and bounded canary approval | DoD §9 + explicit authorization | false |
| `R12-DEF-011` | real-money trading | `DEFERRED_FINAL_AUTHORIZATION` | requires all lower gates and explicit decision | DoD §10 | false |

## Residual-risk registry
Planning freeze acknowledges these residual categories without treating them as resolved production evidence:
- exchange/API behavior may change after planning and must be revalidated during adapter implementation/preflight;
- numeric performance/capacity thresholds require implementation workload measurements;
- model/strategy statistical quality requires empirical datasets and independent promotion evidence;
- regional/compliance availability requires current external review;
- deployment/DR effectiveness requires implemented infrastructure and recovery tests;
- third-party provider failure/cost characteristics require implementation-time measurement;
- production incident/on-call processes require operational rehearsal before live authority.

These residual risks cannot be used to bypass a future DoD gate.

## Implementation handoff rule
If implementation is separately authorized after planning freeze, future Work Orders SHALL consume the R11 logical dependency DAG and frozen requirement traceability. They may refine implementation detail but may not relax upstream authority restrictions or silently reinterpret frozen requirements.

## Freeze exception rule
An exception to a freeze requirement may be accepted only if:
- it is explicitly identified;
- the affected requirement/gate is named;
- safety/security/economic impact is bounded;
- compensating controls and expiry/review date are defined where applicable;
- it does not waive a CRITICAL/HIGH safety, security, money-integrity or live-authorization proof obligation;
- independent review approves it.

Otherwise the freeze verdict is `FREEZE_REJECTED` or `CORRECTION REQUIRED`.
