# HCT-PLAN-0001-R10 — HIGH Observability, Compliance-Readiness & FinOps Hardening

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R10`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

## Purpose
Resolve GAP-R10-21 through GAP-R10-44 without prematurely selecting production vendors/topology.

## 21. Trading Golden Signals
Beyond generic RED/USE metrics, HCT operational views SHALL include domain signals such as:
- current authority state by platform/tenant/account;
- market/private-state freshness and generation trust;
- reconciliation watermark age;
- protection coverage/confidence;
- unresolved/uncertain orders and age;
- Risk Reservation backlog/age;
- decision freshness/signal-lifetime expiry;
- API/WS quota pressure;
- exchange capability/rule freshness;
- Safety/Harness state;
- OMS conflict count/age;
- incident count/severity;
- telemetry/evidence pipeline health.

## 22. SLI Definition Contract
Each production SLI definition must specify:
- scope/entity population;
- numerator;
- denominator;
- eligibility/exclusion conditions;
- event-time/window semantics;
- aggregation method;
- target/threshold ownership;
- source/evidence quality;
- missing-data semantics.

No averaging across tenants/symbols may hide a critical cohort failure.

## 23. Cardinality Budget
Metrics/log/traces use an explicit cardinality budget.

Rules:
- do not put raw order IDs, trace IDs or unbounded symbols/tenant IDs into globally aggregated metric labels without bounded strategy;
- high-cardinality identifiers belong in trace/log/audit storage with secure indexed lookup;
- model/tool/version attributes use bounded/versioned vocabularies where feasible;
- cardinality pressure is itself monitored and may trigger lower-priority telemetry degradation.

## 24. Sampling Policy
Sampling is signal-aware:
- retain 100% or policy-defined mandatory capture for security/audit/execution/protection/reconciliation critical events;
- favor errors, tail latency, uncertain orders and incidents;
- bound normal high-volume traces/market-data diagnostics;
- record sampling policy/version in evidence;
- a sampled-out absence cannot be treated as proof an event did not occur.

## 25. Retention Classes
Candidate retention classes:
- `R0_EPHEMERAL_DEBUG`;
- `R1_OPERATIONAL_SHORT`;
- `R2_TRADING_EVIDENCE`;
- `R3_SECURITY_INCIDENT`;
- `R4_AUDIT_GOVERNANCE`;
- `R5_LEGAL_HOLD` where legally required/authorized.

Exact durations require legal/business/storage review. High-frequency low-value telemetry is compacted/expired before durable money/security evidence.

## 26. Telemetry Pipeline Degradation
Collector/export/storage failures use explicit states:
`HEALTHY`, `DEGRADED`, `BUFFERING`, `DROPPING_NONCRITICAL`, `MANDATORY_EVIDENCE_AT_RISK`, `UNAVAILABLE`.

Hot safety paths do not block on remote observability backends. If mandatory evidence durability becomes uncertain beyond policy, new exposure may be restricted.

## 27. Observability of Observability
Track:
- collector health;
- queue/buffer occupancy;
- dropped log/span/metric counts;
- exporter retry/failure;
- ingest/storage lag;
- schema rejection;
- clock skew;
- sampling rate/policy;
- storage/retention capacity;
- mandatory-evidence durability status.

## 28. Alert Contract
Every actionable alert has:
- alert ID/rule version;
- owner;
- severity;
- affected scope;
- condition and evidence;
- dedup/grouping key;
- runbook;
- escalation target;
- inhibit/suppress rules;
- auto-resolution/expiry behavior;
- last-reviewed date.

Alerts without actionable owner/runbook are candidates for removal or downgrade.

## 29. Runbook Lifecycle
Runbooks are versioned artifacts defining:
- trigger/incident type;
- preconditions/required authority;
- safe diagnosis steps;
- allowed controls/actions;
- forbidden shortcuts;
- expected evidence;
- rollback/roll-forward;
- verification/restoration gates;
- escalation.

Runbooks do not grant authority beyond the actor/Harness/Safety policy.

## 30. On-call / escalation model
Bootstrap owner-only operation still defines:
- primary responder identity;
- backup/recovery contact process when available;
- paging channels;
- severity expectations;
- acknowledgement/escalation timers;
- maintenance/quiet-hours rules that never silence SEV0/SEV1 capital/security events.

Architecture remains ready for future multi-role rotations.

## 31. Post-Incident Review
Material incidents generate an evidence-driven review covering:
- impact/blast radius;
- timeline;
- root and contributing factors;
- detection successes/failures;
- containment/recovery behavior;
- control/process/documentation gaps;
- regression tests/evidence obligations;
- tracked corrective work;
- recurrence-prevention owner.

Focus is system learning, not blame, while preserving accountability for privileged actions.

## 32. Release/deploy observability
All runtime evidence can correlate to:
- build/release version;
- config/policy version;
- feature/capability flags;
- deployment start/end;
- migration/schema version;
- rollback/roll-forward events.

This enables change-failure and incident correlation without requiring microservices or a final deployment topology now.

## 33. Model/agent observability
Observe by version/profile where permitted:
- inference/tool latency;
- availability/failure/timeouts;
- cost/token/tool consumption;
- calibration/abstention rates;
- evidence admissibility failure;
- disagreement/escalation;
- drift/retrieval-health indicators;
- stale-work cancellation.

Raw prompts, hidden chain-of-thought, credentials and prohibited tenant data are not normal telemetry.

## 34. Retention vs deletion/legal hold
Tenant offboarding/privacy deletion and audit/security retention are reconciled through explicit data classes and legal-policy states.

Rules:
- ordinary product/RAG/cache data follows deletion policy;
- required audit/security/trading evidence may have separate retention justification;
- legal hold, if applicable, is explicit, scoped and audited;
- legal obligations vary by jurisdiction and require legal review before production/commercialization.

## 35. Evidence Export Bundle
Internal audit/incident/future assurance exports are reproducible bundles with:
- scope/time window;
- data/evidence manifest;
- schema/tool versions;
- integrity hashes;
- redaction/classification report;
- actor/export approval identity;
- tenant/account authorization;
- chain-of-custody metadata where applicable.

Raw secrets and unrelated tenants are excluded.

## 36. Cost Allocation Dimensions
When technically feasible, costs are attributed across:
- provider/service;
- environment;
- platform shared baseline;
- tenant/account;
- capability/workload;
- model/agent/tool;
- replay/research experiment;
- market-data/storage tier.

Shared costs use documented allocation rules rather than fabricated precision.

## 37. Cost anomaly and budget guardrails
FinOps controls include:
- actual + forecast burn;
- provider quota usage;
- 50/70/85/95% bootstrap warning bands where useful;
- unexpected cost-per-tenant/capability changes;
- budget ceiling approvals;
- automatic suppression of P4/P5 or research workloads before safety-critical capacity is endangered.

Cost shutdown never violates R10 FinOps Safety Boundary.

## 38. AI/Agent/Research Cost Budgets
Define budgets for:
- model inference;
- agent deliberation/tool calls;
- web/news retrieval;
- embeddings/vector retrieval;
- replay/backtests/Monte Carlo;
- dataset/storage/egress.

Track value/cost signals such as candidate decisions evaluated, accepted incremental evidence, avoided stale work and experiment value. Expensive agents remain shortlist/value driven.

## 39. Provider-neutral billing normalization
HCT maintains an internal cost schema. Where source providers expose compatible fields, FOCUS-aligned normalization is preferred for billing periods, currencies, services, resources, charges, corrections and allocation dimensions.

FOCUS compatibility is a normalization aid, not a guarantee every provider exposes identical granularity.

## 40. Unit economics and capacity triggers
Track, where meaningful:
- infrastructure cost / active tenant;
- cost / connected exchange account;
- cost / protected live-capable account;
- telemetry/storage cost / tenant;
- model/agent cost / evaluated opportunity;
- replay/research cost / experiment;
- provider quota headroom;
- p95/p99 latency/capacity pressure.

Infrastructure migration is triggered by measured reliability/security/capacity economics, not simply reaching a customer-count number.

## 41. Cost Data Truth Classes
Cost data is labeled:
- `REALTIME_ESTIMATE`;
- `PROVIDER_USAGE_REPORTED`;
- `BILLING_STATEMENT`;
- `INVOICED`;
- `CORRECTED`.

Forecast/estimated cost never masquerades as invoice truth. Provider corrections append/reconcile rather than rewriting prior evidence invisibly.

## 42. Compliance applicability/version drift
Compliance-readiness uses versioned applicability records containing:
- jurisdiction/region;
- product capability;
- customer/tenant class;
- exchange/provider constraints;
- framework/law/guidance version/date;
- owner/reviewer;
- last review;
- next review/trigger;
- legal-review status.

Locale or billing country alone does not establish legal eligibility.

## 43. Audit access governance
Sensitive observability/audit data requires least privilege and purpose limitation.

Access/export records capture:
- real actor/workload;
- scope;
- purpose/ticket/incident where required;
- time;
- tenant/account;
- exported dataset/bundle ID;
- privileged assumption/elevation state.

## 44. Dashboard Truth Hierarchy
Operational dashboards label information classes:
1. authoritative domain facts;
2. reconciled projections;
3. telemetry observations;
4. derived metrics/SLO calculations;
5. forecasts/estimates/scores;
6. unavailable/unknown.

A metric, score or forecast cannot visually masquerade as exchange-authoritative fact.

## External reference posture
- OpenTelemetry semantic conventions inform interoperable naming across traces/metrics/logs/resources, while HCT keeps trading-domain semantics versioned internally.
- NIST CSF 2.0 and SP 800-61r3 inform cybersecurity/incident-management process structure.
- FOCUS 1.4 informs vendor-neutral billing normalization where applicable.

These references guide architecture but do not establish HCT certification/compliance by themselves.

## HIGH closure
GAP-R10-21 through GAP-R10-44 have explicit planning-resolution contracts. Implementation remains unauthorized.
