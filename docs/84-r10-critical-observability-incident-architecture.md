# HCT-PLAN-0001-R10 — Critical Observability, Audit & Incident Architecture

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R10`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

## Purpose
Resolve GAP-R10-01 through GAP-R10-20. Observability is a governed evidence plane and never a shortcut around exchange, OMS, reconciliation, Security, Safety or Risk truth.

## 1. Canonical Observability Envelope
Every structured log/event/trace/span/metric exemplar used for high-assurance operations should carry a versioned context envelope where applicable:
- `service.name` / service instance identity;
- environment and release/build identity;
- tenant/account scope in approved low-cardinality/privacy-safe form;
- SecurityContext actor/workload identity class where permitted;
- correlation/trace/request/command/decision IDs;
- market/account generation IDs;
- strategy/model/agent/tool/policy versions where material;
- event/receive/processing timestamps;
- monotonic duration fields where appropriate;
- trading-authority state;
- evidence/source class;
- data classification/redaction class.

OpenTelemetry-style semantic conventions are preferred for standard infrastructure/runtime fields where stable and applicable; HCT domain semantics remain HCT-owned/versioned.

## 2. Telemetry Non-Authority Rule
Telemetry can observe/report:
- exchange-authoritative state;
- HCT authoritative projections;
- estimated/derived states;
- forecasts/scores.

It must tag which class each datum belongs to.

Rules:
- log says `FILLED` != proof of fill unless linked to authoritative fill evidence;
- metric says `positions=0` != proof of no position if reconciliation is stale;
- dashboard green != permission to trade;
- missing telemetry != healthy zero;
- a telemetry pipeline may trigger safe degradation according to policy, but it does not create exchange truth.

## 3. Causal Trading Trace
HCT defines a `TradingTraceID` / causal lineage spanning, where applicable:
`Market State -> Feature/Strategy -> Brain Candidate -> Safety -> RiskSnapshot -> Risk Reservation -> Session Policy -> Execution Intent/Command -> Exchange ACK/Fills -> OMS -> Protection -> Reconciliation -> Outcome/Audit`.

Every domain retains its own immutable IDs; the trace links them rather than replacing them.

## 4. Time Integrity
Observability distinguishes:
- exchange/event time;
- HCT receive/knowledge time;
- processing time;
- persisted time;
- wall clock;
- monotonic elapsed duration.

Clock health is itself observed. Unknown clock integrity prevents latency/causal measurements from being presented with false precision.

## 5. Telemetry Data Firewall
Before telemetry emission/export, fields pass classification/redaction rules.

Never-normal-telemetry classes include:
- raw exchange/API secrets;
- signing material/private keys;
- session/bearer tokens;
- recovery secrets;
- password/MFA secrets;
- raw SecretStore payloads;
- prohibited prompt/tool secret context;
- tenant data classified as non-observable.

Use explicit allowlists/structured DTOs rather than hoping text log scrubbing catches everything.

## 6. Tenant-safe observability
Telemetry access and query/export paths enforce:
- tenant/account scope;
- admin/support purpose and actor identity;
- environment boundary;
- least privilege;
- cross-tenant aggregation only through approved de-identified/platform operations views.

High-cardinality tenant/order identifiers should be available through secure trace/audit lookup rather than uncontrolled metric labels.

## 7. Tamper-evident Audit Ledger
Security/trading/admin audit uses append-only logical events with:
- event ID;
- event type/schema version;
- actor/workload identity;
- tenant/account/environment;
- action and target scope;
- before/after references where applicable;
- reason/incident/change context;
- authoritative evidence references;
- timestamps;
- release/policy/version context;
- correlation identity.

For high-value evidence, HCT may use hash chaining, signed batches, WORM/object-lock or equivalent tamper-evidence according to deployment capability. Corrections append superseding events; history is not silently rewritten.

## 8. Audit taxonomy
Mandatory event families include:
- authentication/session/recovery;
- tenant membership/role/privilege;
- admin/support assumption/break-glass;
- SecretStore/credential lifecycle;
- Safety/Harness state changes;
- risk policy/RiskSnapshot/Reservation decisions;
- execution commands/mutations;
- OMS/reconciliation/protection conflicts/recovery;
- strategy/model/agent/skill/retriever promotion/quarantine;
- deployment/release/config changes;
- commercial entitlement/account state changes;
- incident lifecycle;
- audit/evidence export.

## 9. Trading-aware SLO model
HCT distinguishes safety/correctness/freshness SLOs from ordinary service availability.

Candidate SLO families:
- market-state freshness/coherency;
- private account-state freshness;
- protection establishment/verification;
- reconciliation convergence;
- uncertain-order resolution;
- Risk/Execution decision latency within signal lifetime;
- Safety/Harness command propagation;
- audit-evidence durability;
- SecretStore/auth availability for required protected operations;
- frontend trusted-state age for operational cockpit;
- general API/UI availability.

## 10. Correctness-over-availability invariant
HCT intentionally permits safe unavailability of new-exposure paths.

Examples:
- `NO_NEW_EXPOSURE` may be healthy safety behavior during exchange uncertainty;
- `RECONCILIATION_ONLY` may be the correct mode after restart;
- rejecting a trade because freshness expired is success for the safety SLO, not an uptime failure.

Availability KPIs may not incentivize bypassing hard gates.

## 11. Error-budget / authority coupling
SLO violations and burn rates are classified by safety significance.

Rules:
- generic UI/API error budget may page/degrade UX but not autonomously trade;
- sustained critical freshness/reconciliation/protection violations may feed deterministic Safety/Harness policy that restricts new exposure;
- telemetry-derived burn signals cannot relax authority;
- recovery to stronger authority requires underlying domain proof, not only error-budget recovery.

## 12. Protection and reconciliation SLIs
Measure at minimum:
- fill-to-protection-required latency;
- fill-to-protection-verified latency;
- verified protected quantity / required quantity;
- private-stream age;
- reconciliation watermark age/coverage;
- unresolved conflict duration;
- restart/failover time to classified authoritative state;
- uncertain order age;
- state-confidence recovery duration.

Thresholds are policy/versioned and finalized during implementation benchmarks.

## 13. Trading-aware incident severity
Incident severity considers:
- current money at risk;
- ability to protect/reduce;
- state certainty;
- tenant/account blast radius;
- secret/identity compromise;
- cross-tenant exposure;
- exchange connectivity/capability;
- Safety/Risk/OMS impairment;
- durability/audit loss;
- recoverability and time sensitivity.

Candidate severities: `SEV0`, `SEV1`, `SEV2`, `SEV3`, `SEV4`, with deterministic classification criteria defined before production.

## 14. Incident Response State Machine
Canonical flow:
`DETECT -> TRIAGE -> CLASSIFY -> CONTAIN -> SAFE_OPERATING_MODE -> PRESERVE_EVIDENCE -> RECONCILE -> REMEDIATE -> VERIFY -> PROGRESSIVE_RESTORE -> REVIEW -> CLOSE`.

Safety priorities:
1. prevent uncontrolled new exposure;
2. preserve/restore protection and risk-reducing ability;
3. establish exchange/account truth;
4. contain security/tenant blast radius;
5. preserve evidence;
6. repair and progressively restore.

NIST SP 800-61r3 / CSF 2.0 is used as external process guidance; HCT's trading-aware state machine is more domain-specific.

## 15. Automation authority boundary
Detection automation may:
- classify/suggest;
- page/notify;
- enrich incidents;
- execute pre-approved bounded containment through Harness/Safety policies.

It may not receive generic arbitrary exchange-order authority.

Examples of bounded automatic containment:
- tenant/account `NO_NEW_EXPOSURE`;
- quarantine a model/data source;
- revoke compromised session/token/credential via approved security path;
- suppress research load;
- force reconciliation/recovery workflow.

Money-moving reduction/close actions remain governed by existing Safety/Risk/Execution contracts.

## 16. Incident Evidence Bundle
Every material incident accumulates an immutable bundle containing:
- incident ID/severity;
- timeline;
- detections/alerts;
- affected tenant/account/capability/release/version;
- authority-state transitions;
- exchange/OMS/reconciliation evidence references;
- admin/Harness/security actions;
- relevant audit events;
- telemetry quality/gaps;
- forensic attachments/hashes where applicable;
- restore verification;
- post-incident actions.

Cleanup cannot erase required evidence before capture/retention policy permits.

## 17. Security Incident Coupling
Security incidents integrate R08 controls:
- credential/API key compromise;
- session/account takeover;
- privileged identity misuse;
- cross-tenant access;
- SecretStore/KMS anomaly;
- malicious/untrusted artifact;
- CI/CD/supply-chain compromise;
- data exfiltration indicators.

Containment may revoke credentials/sessions, quarantine tenant/account/release/capability, disable new exposure and force reconciliation/protection assessment.

## 18. Recovery Proof Gate
Before stronger authority resumes after material incident/restart/failover/control-plane outage, prove as applicable:
- current identity/credential validity;
- trusted market-data generation;
- private account-state coverage;
- orders/fills/positions classified;
- Risk Reservations reconciled;
- required protection verified;
- current exchange capabilities/rules loaded;
- critical configs/releases known;
- audit/evidence pipeline meets minimum mandatory durability;
- no active blocking incident predicate remains.

Recovery is progressive, not a single green button.

## 19. Compliance Evidence Map
HCT maintains a versioned `ControlEvidenceMap` with:
- internal requirement/control ID;
- purpose/risk addressed;
- owner;
- implementation/evidence artifact classes;
- review frequency;
- retention class;
- applicable product/region/tenant class;
- mapped external framework/control references where useful;
- status/gaps.

Mapping to NIST, SOC-type controls, privacy/security frameworks or future financial/regional obligations is readiness evidence only. HCT must not claim certification/compliance without the required independent/legal process.

## 20. FinOps Safety Boundary
Cost automation is subordinate to safety/security/evidence requirements.

Cost controls may reduce/suspend:
- research/replay;
- low-priority scanning;
- noncritical analytics;
- decorative telemetry;
- optional model enrichment.

Cost controls may NOT silently disable below required minimum:
- protection/reconciliation/execution-control telemetry;
- security/auth/secret controls;
- mandatory audit evidence;
- incident evidence preservation;
- Safety/Risk/Harness functions;
- minimum recovery/DR evidence.

## CRITICAL closure
GAP-R10-01 through GAP-R10-20 have explicit planning-resolution contracts. Implementation values, thresholds, vendors and deployment topology remain future evidence-driven decisions.
