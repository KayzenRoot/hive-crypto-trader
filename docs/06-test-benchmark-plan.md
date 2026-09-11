# Test and Benchmark Plan

Status: `DISCOVERY_IN_PROGRESS`
Risk class: `HIGH_ASSURANCE`
Active formalization through: `HCT-PLAN-0001-R10`

## Purpose
Define the evidence families that HCT must prove before implementation increments, production promotion and live authority can be granted. This document is a cross-round planning baseline; detailed numeric thresholds are finalized through implementation benchmarks and promotion evidence, not guessed during discovery.

## Governance validation
Every planning/implementation increment must preserve:
- canonical source hierarchy;
- checkpoint structural validity and current Git SHA;
- Work Order scope/acceptance/STOP CONDITION;
- no accidental implementation/live authorization;
- objective verdict `APPROVED`, `CORRECTION REQUIRED` or `BLOCKED`.

## Test families

### 1. Contract and schema tests
Cover versioned boundaries for:
- Exchange Adapter/capability/rules;
- market/realtime events and generations;
- RiskSnapshot/Risk Reservation;
- Execution Intent/Command/OMS events;
- reconciliation/protection evidence;
- Canonical Evidence Envelope / Brain decisions;
- SecurityContext/tenant scope;
- UI State Envelope;
- observability/audit envelopes.

Unknown/malformed critical schemas must fail safe rather than be guessed.

### 2. Deterministic safety/risk tests
Test hard invariants including:
- Safety Governor dominance;
- dynamic exchange risk tiers/MMR/leverage;
- post-trade risk preview;
- risk reservation conservation;
- cross-margin contagion;
- survival/OMR budgets;
- protection-confidence gating;
- pyramiding/add reapproval;
- no AI/agent override of hard risk.

### 3. Execution/OMS/reconciliation tests
Include:
- economic fill idempotency;
- duplicate/late/out-of-order private events;
- ACK vs fill semantics;
- timeout/unknown outcome;
- cancel/replace races;
- position-mode-safe reduce/close;
- protective coverage resizing;
- restart/failover recovery and reconciliation watermarks;
- no blind retry.

### 4. Realtime/data-integrity tests
Include:
- snapshot/delta synchronization;
- generation fencing;
- sequence/gap recovery;
- reconnect/resubscribe;
- stale/clock-drift behavior;
- backpressure/load shedding;
- quota prioritization;
- feature coherency;
- schema drift quarantine;
- cache freshness leases;
- Decision Freshness expiry.

### 5. Intelligence/learning tests
Include:
- evidence admissibility;
- temporal leakage firewall;
- calibration/sample sufficiency;
- selective abstention;
- evidence independence/redundancy;
- bounded agent deliberation;
- version attribution;
- memory/retrieval point-in-time behavior;
- drift/localized learning authority;
- no self-promotion.

### 6. Validation Laboratory tests
Promotion proof includes, where applicable:
- dataset eligibility and point-in-time universe truth;
- Temporal Non-Interference;
- holdout/OOS isolation;
- causal replay;
- fill/latency/fee/funding realism;
- accounting/Risk/OMS live-parity conformance;
- paper/shadow technical isolation;
- experiment-family/multiple-testing controls;
- effective-independent sample and regime/OOD coverage;
- parameter robustness;
- simulator calibration;
- portfolio interaction;
- paired ablation/Decision Twin;
- rollback compatibility;
- independent HIGH_ASSURANCE review.

### 7. Multi-tenant/security tests
Include adversarial negative cases for:
- object-level authorization;
- DB/RLS-equivalent isolation and pooled connections;
- cache/queue/event isolation;
- tenant–exchange-account binding;
- SecretStore lifecycle/redaction;
- auth/recovery/session revocation;
- workload/admin/support identities;
- break-glass/support assumption;
- noisy-neighbor isolation;
- tenant-safe backups/offboarding/RAG deletion;
- CI/CD/environment separation;
- incident/DR tenant integrity.

### 8. UI/UX operational-integrity tests
Include:
- UI State Envelope validation;
- stale/disconnected/resyncing presentation;
- R05 authority action matrix;
- order Evidence Ladder;
- uncertainty/reconciliation conflict UX;
- protection/risk survival state;
- live/paper/shadow/replay isolation;
- tenant/account/environment context switching;
- no optimistic money truth;
- dangerous/emergency actions;
- client lag/degraded presentation;
- safe loading/error/unknown semantics;
- accessibility and reduced motion;
- visual regression of critical semantic states.

### 9. Observability/audit/incident tests
Include:
- telemetry non-authority;
- secret/tenant data redaction;
- causal trace completeness;
- audit append-only/tamper-evidence behavior;
- trading SLI calculations and missing-data semantics;
- telemetry-pipeline degradation;
- alert dedup/escalation;
- runbook recovery proof;
- incident containment/evidence preservation;
- security incident coupling;
- progressive restore gates;
- evidence export integrity.

### 10. Performance/capacity benchmarks
Measure under representative workloads:
- market ingest throughput and lag;
- feature/strategy/Brain latency;
- Risk/Execution latency versus signal lifetime;
- OMS/private-state processing;
- reconciliation/protection convergence;
- UI stream-to-render age and interaction latency;
- DB/cache/queue pressure;
- CPU/RAM/storage/network;
- API/WS quota headroom;
- model/agent/tool latency/cost;
- replay throughput/cost;
- telemetry pipeline overhead/cardinality/storage.

No numeric target is considered canonical until workload assumptions and benchmark method are defined.

## SLO validation principle
HCT optimizes for safe/correct operation rather than raw uptime. Tests must confirm that degraded states such as `NO_NEW_EXPOSURE`, `REDUCE_ONLY` or `RECONCILIATION_ONLY` activate correctly under failures rather than being treated as availability defects.

## Evidence and reproducibility
High-assurance results should record:
- code/build version;
- dependency/runtime identity;
- data/fixture version;
- configuration/policy versions;
- random seed where relevant;
- environment/hardware profile where relevant;
- test/benchmark tool version;
- result/evidence hashes;
- known limitations.

## Cost-aware testing
Research and large replay workloads are resource-governed. Cost optimization may queue/downsample noncritical experiments but may not weaken mandatory HIGH_ASSURANCE proof.

## Promotion rule
Passing unit/integration tests alone never grants production/live authority. Production eligibility requires the applicable R07 promotion stages and all unresolved CRITICAL/HIGH defects closed with objective evidence.

Implementation and live trading remain unauthorized until explicitly granted by a later governed process.
