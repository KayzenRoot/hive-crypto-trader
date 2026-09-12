# Definition of Done

Status: `R12_FREEZE_CANDIDATE`
Risk class: `HIGH_ASSURANCE`
Canonical planning increment: `HCT-PLAN-0001-R12`

## Purpose
Define the objective completion contract for Hive Crypto Trader across planning, implementation, verification, deployment-readiness, promotion and live activation. A lower stage never grants authority belonging to a higher stage.

The governing rule is:

`done = scope satisfied + required evidence passed + no unresolved blocking defect + independent audit + governed checkpoint promotion`

A claim of completion without objective evidence is not completion.

## Global invariants
Every governed increment SHALL:
- use one stable Work Order ID across branch, PR, evidence, corrections and checkpoint;
- start from a fresh Context Lock bound to canonical Git/checkpoint state;
- remain within approved Scope and Decisions Ledger authority;
- satisfy its explicit acceptance criteria and STOP CONDITION;
- preserve HIGH_ASSURANCE safety/security/risk/execution invariants;
- preserve tenant/account/environment and `LIVE/PAPER/SHADOW/REPLAY` separation where applicable;
- provide reproducible evidence for all applicable tests/checks;
- close or explicitly disposition all introduced findings;
- contain zero unresolved CRITICAL/HIGH defects at approval time;
- receive an independent verdict of `APPROVED`, `CORRECTION REQUIRED` or `BLOCKED`;
- promote checkpoint truth only after objective approval and governed merge.

No model, agent, executor or author may self-promote its own work solely from implementation output.

## 1. Governance bootstrap DoD
`HCT-BOOT-0001` is complete only when:
- source hierarchy is versioned;
- checkpoint/handoff protocol is versioned;
- machine-readable current checkpoint exists;
- Work Order and prompt-delivery contract is versioned;
- review verdicts are defined;
- HIGH_ASSURANCE default is recorded;
- changes are reviewed and merged to `main`;
- checkpoint is promoted only after objective audit.

Bootstrap completion does not mean product planning or product implementation is complete.

## 2. Planning increment DoD
A planning increment is complete only when:
- objective, context, scope, out-of-scope, sources, architecture rules, constraints, acceptance criteria, tests/evidence, deliverables, review format and STOP CONDITION are explicit;
- every new capability is classified `NECESSARY`, `IMPORTANT`, `FUTURE` or `OUT_OF_SCOPE` and does not silently expand V1;
- affected canonical requirements/architecture/security/test/deployment/decision sources are updated or an explicit no-change justification exists;
- contradictions against higher-priority canonical sources are resolved;
- all CRITICAL/HIGH planning gaps identified by the increment are resolved or the increment is `BLOCKED`/`CORRECTION REQUIRED`;
- final planning audit is objective and reproducible;
- approval does not imply implementation or live authority unless a separate explicit authorization says so.

## 3. Planning freeze DoD
`HCT-PLAN-0001` may be frozen only when:
- all accepted requirement sources are included in a versioned frozen baseline;
- source-to-frozen traceability has zero unmapped accepted requirements and zero unexplained dropped requirements;
- every material conflict is resolved under source hierarchy/Decisions Ledger precedence;
- Scope, Architecture, Security, Test/Benchmark Plan, Module Map, Decisions Ledger and frozen requirements are mutually consistent;
- residual risks, intentional unknowns and deferred decisions are explicitly registered;
- source hierarchy names the frozen baseline and its change-control authority;
- a frozen system acceptance matrix exists;
- final freeze audit finds zero unresolved CRITICAL/HIGH planning defects;
- verdict is explicitly `FREEZE_APPROVED` or `FREEZE_REJECTED`;
- planning freeze explicitly preserves `implementation_authorized=false`, `production_credentials_authorized=false`, `production_deployment_authorized=false`, `limited_live_authorized=false` and `live_trading_authorized=false` unless separately changed by a later governed authorization.

## 4. Implementation increment DoD
An implementation Work Order, once separately authorized, is complete only when:
- it references the frozen baseline/version and exact governing requirement IDs/source locators;
- changed behavior is traceable to approved requirements/decisions;
- architecture boundaries and authority ceilings are preserved;
- code is functional and only implements approved scope;
- all applicable unit, integration, contract/schema, property/state-machine, negative/fail-closed and regression tests pass;
- applicable static analysis, lint, typecheck and build checks pass;
- data/schema/migration changes include compatibility, migration, rollback/roll-forward and integrity evidence;
- security-sensitive changes include applicable threat/abuse/authorization/secret-isolation tests;
- trading/risk/execution changes include deterministic safety, replay/scenario, unknown-outcome and recovery evidence;
- performance-sensitive changes satisfy defined benchmark methodology/thresholds or record an approved exception;
- observability/audit evidence required for safe diagnosis exists without creating shadow authority;
- documentation and contracts reflect proven code behavior;
- no CRITICAL/HIGH defect remains;
- independent audit returns `APPROVED` before checkpoint promotion/merge completion.

## 5. Test and benchmark evidence DoD
Applicable proof SHALL follow `docs/06-test-benchmark-plan.md` and record enough context to reproduce results, including where relevant:
- code/build/dependency/runtime identity;
- data/fixture/config/policy/model/prompt versions;
- random seed;
- hardware/environment profile;
- test/benchmark tool version;
- result/evidence hashes;
- known limitations and failed attempts corrected.

Mandatory HIGH_ASSURANCE proof cannot be waived for cost or convenience.

## 6. Security and tenant-integrity DoD
A security/identity/tenant-sensitive increment is not done unless evidence shows, where applicable:
- server-derived authorization context and object-level authorization;
- tenant/account/credential/environment isolation;
- secret lifecycle/redaction boundaries;
- least privilege and privileged-admin separation;
- negative/adversarial isolation tests;
- auditability without leaking secrets or private reasoning;
- safe backup/offboarding/recovery behavior;
- no security control is bypassed by cache, queue, UI, agent or operational tooling.

## 7. Data, execution and money-state integrity DoD
Any change affecting market truth, orders, fills, positions, balances, risk, protection or reconciliation is not done unless applicable evidence proves:
- authoritative ownership and version/identity consistency;
- idempotency and duplicate/late/out-of-order handling;
- acknowledgement is not treated as economic fill;
- unknown outcomes fail safe and reconcile before blind retry;
- position mode/reduce/close semantics are correct;
- protection coverage and reconciliation converge correctly;
- restart/failover recovery preserves economic truth;
- Risk/Safety/Session/Exchange restrictions cannot be relaxed by downstream components;
- no optimistic UI/cache/telemetry projection becomes money-state authority.

## 8. Deployment-readiness DoD
Deployment readiness is a separate gate and is not satisfied by implementation completion. Before any production deployment authorization:
- deployment topology and environment boundaries are explicitly approved;
- infrastructure/security/secrets/network/storage/backup/restore contracts are documented;
- migration/rollback/roll-forward and disaster-recovery procedures are tested;
- observability, incident response and runbooks are operationally validated;
- supply-chain/dependency/container/artifact provenance controls pass;
- capacity/cost/quotas and failure/degradation behavior are tested under representative load;
- production credentials are handled outside repository source and under approved secret controls;
- independent deployment-readiness audit returns `APPROVED`.

## 9. Promotion and limited-live DoD
A strategy/model/agent/runtime candidate cannot receive production or limited-live eligibility solely from code tests or historical PnL. Applicable R07 Promotion Laboratory evidence SHALL prove:
- point-in-time/temporal non-interference;
- OOS/holdout isolation;
- realistic simulator/fill/fee/funding/latency assumptions;
- accounting/Risk/Execution live-parity conformance;
- experiment-family/multiple-testing controls;
- robustness/regime/OOD evidence;
- rollback compatibility and expiry/revalidation rules;
- independent HIGH_ASSURANCE promotion review.

Any limited-live activation requires a separately approved bounded canary envelope, explicit exposure limits, kill/rollback controls and objective monitoring. Planning or implementation approval alone never grants it.

## 10. Production/live trading DoD
Real-money live authority is a distinct final authorization. It requires all lower applicable stages plus:
- explicit legal/regional/exchange/account eligibility evidence;
- approved production credentials/security posture;
- production deployment and recovery proof;
- applicable promotion evidence and validity lease;
- verified Safety/Risk/Execution/OMS/Reconciliation/protection invariants in the target environment;
- incident and emergency controls operational;
- independent HIGH_ASSURANCE live-readiness review;
- explicit checkpoint/decision stating `live_trading_authorized=true` for the bounded scope.

Absent that explicit authorization, live trading remains prohibited.

## 11. Documentation and checkpoint DoD
After an `APPROVED` increment:
- canonical docs affected by proven changes are updated;
- docs may not claim behavior unsupported by code/evidence;
- Decisions Ledger/ADR changes are recorded when material decisions changed;
- checkpoint delta records completed increment, evidence, verdict, risks and exact next necessary action;
- historical approved evidence remains traceable and is not silently rewritten;
- checkpoint promotion occurs only after governed merge.

## 12. Project/version completion rule
A project/version is complete only when every V1-required capability and every project-wide applicable DoD clause is objectively satisfied, all required evidence is present, zero CRITICAL/HIGH defects remain, residual risks/deferred items are correctly classified, and a final independent review returns `APPROVED`.

`Completed`, `implemented`, `green CI`, `planning frozen` or `merged` alone are never sufficient proof of version completion.
