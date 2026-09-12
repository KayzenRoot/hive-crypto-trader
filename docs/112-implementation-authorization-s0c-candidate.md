# HCT-IMPL-AUTH-0003 - S0C Implementation Authorization Candidate

Status: `INDEPENDENT_REVIEW_REQUIRED`
Risk class: `HIGH_ASSURANCE`
Authorization increment: `HCT-IMPL-AUTH-0003`
Issue: `#39`
Candidate implementation slice: `HCT-IMP-0003-S0C`
Canonical base: `main@2cbc7d07adee06bc11e967ff7cfbd7671424cc1d`
Canonical checkpoint: `HCT-CP-0018 / S0B_IMPLEMENTATION_APPROVED_MERGED`

## Purpose
Evaluate whether exactly one bounded continuation of R11 Stage 0 may be authorized after approved S0A and S0B completion. This candidate grants no implementation authority until independent HIGH_ASSURANCE review, governed merge and a new checkpoint promotion explicitly authorize only `HCT-IMP-0003-S0C`.

## Current authoritative state
At `HCT-CP-0018`:
- `implementation_authorized=false`
- `implementation_authorization_scope=[]`
- `implementation_authorization_ceiling="NONE_PENDING_NEXT_GOVERNED_AUTHORIZATION"`
- `production_credentials_authorized=false`
- `production_deployment_authorized=false`
- `limited_live_authorized=false`
- `live_trading_authorized=false`

Planning remains frozen under `HCT-CP-0014`. S0A and S0B are independently approved and merged.

## Why S0C is next
R11 Stage 0 requires, before Stage 1 exchange/realtime truth:
- shared domain IDs/contracts/errors;
- SecurityContext/tenant/account binding;
- SecretStore abstraction;
- audit/evidence primitives;
- configuration/version semantics;
- environment namespace.

S0A established the runtime/repository/canonical contract foundation, environment namespace and basic audit/evidence envelopes. S0B established SecurityContext, exact tenant/account/environment binding, fail-closed authorization guards and an opaque SecretStore reference boundary. The remaining bounded Stage-0 dependency is to harden audit/evidence integrity and configuration/release/policy version semantics so later exchange, realtime, risk and execution state can bind to stable provenance without inventing competing truth.

## Frozen source alignment
This candidate is bounded by the frozen R12 baseline and specifically traces to:
- R08 `SEC-006` audit integrity/isolation;
- R10 `R10-REQ-001` observability non-authority;
- R10 `R10-REQ-002` observability context envelope;
- R10 `R10-REQ-005` telemetry data firewall;
- R10 `R10-REQ-007` append-only audit;
- R10 `R10-REQ-008` audit event taxonomy;
- R10 `R10-REQ-032` release/config observability;
- R11 sections 6, 10, 11 and 13 for source-of-truth, environment namespace, canonical identity/version registry and Stage-0 dependency order.

This slice does not attempt to complete all R10 observability, incident, compliance or FinOps requirements.

## Proposed authorization
After independent approval, governed merge and checkpoint promotion, authorize exactly:

`HCT-IMP-0003-S0C - Audit/Evidence Integrity & Configuration/Version Semantics Foundation`

Proposed ceiling:

`NON_TRADING_STAGE_0_AUDIT_EVIDENCE_CONFIG_VERSION_FOUNDATION_ONLY`

## Proposed S0C scope
### 1. Harden existing audit/evidence primitives
Extend/reuse the S0A canonical primitives. Do not create a shadow contract system.

The bounded model may add immutable/versioned fields necessary to express, where applicable:
- event/evidence identity and schema version;
- environment;
- actor/workload identity class and safe actor reference;
- tenant/account scope references where applicable;
- operation/action/target class;
- outcome/assurance/reason classification;
- correlation/trace identity;
- release/build, config and policy version references;
- authoritative evidence/source class;
- data classification/redaction class;
- event/knowledge/processing time references where needed by the primitive.

### 2. Deterministic integrity and append-only correction semantics
Define deterministic canonical serialization/hash rules and provider-neutral integrity linkage sufficient to prove:
- identical canonical content produces identical integrity hash;
- modified content produces mismatch;
- environment/scope/version identity participates in integrity where material;
- an append-only correction/supersession references prior evidence rather than silently mutating history;
- optional previous-record/hash linkage can be verified without implementing a persistent audit database.

Hash chaining is an integrity primitive only. S0C SHALL NOT implement WORM/object lock, external signing infrastructure, persistent audit storage or a blockchain.

### 3. Authority/truth and classification semantics
Define controlled metadata sufficient to distinguish authoritative external evidence, authoritative internal state, reconciled projection, telemetry observation, derived/estimated evidence and unknown/unavailable state where applicable.

Telemetry/evidence metadata SHALL NOT create trading authority and SHALL NOT upgrade an observation into domain truth.

Use structured allowlisted metadata rather than arbitrary text maps for high-assurance fields.

### 4. Release/config/policy version semantics
Implement bounded immutable identity/provenance primitives for release/build, configuration and policy state, reusing existing S0A `StableId`/environment contracts where practical.

The slice may define a provider-neutral `ConfigSnapshot`/descriptor-equivalent containing only approved non-secret provenance such as:
- config identity/version;
- environment;
- canonical content/fingerprint hash;
- release/build reference;
- policy/version references;
- effective/created time metadata;
- safe source/classification metadata.

It SHALL NOT implement a production config service, remote feature-flag provider, deployment control plane or secret-bearing configuration store.

### 5. Data firewall at the primitive boundary
Audit/evidence/config metadata APIs SHALL use controlled fields and safe representations. Raw credentials, secret material, bearer/session/recovery tokens and unrestricted secret-like payload maps are prohibited.

### 6. Proof and regression
Add deterministic tests for integrity, tamper detection, append-only supersession, environment/scope/version mismatch, safe metadata, no secret leakage, canonical hash reproducibility and S0A/S0B regression. Exact-head CI and independent HIGH_ASSURANCE review are mandatory before merge.

## Explicitly out of scope
S0C SHALL NOT implement:
- product code before this authorization is independently approved and checkpoint-promoted;
- real API keys, secret keys, private keys, tokens, seed phrases or secret values;
- credential lifecycle, encryption/KMS/HSM or production secret-provider integrations;
- MEXC or any exchange client/adapter/REST/WebSocket/authentication/signing;
- market-data ingest, quota/WS governor, universe or Market-State Fabric;
- database persistence, RLS, append-only database tables, audit storage service, WORM/object lock or external signing service;
- external OpenTelemetry collector/exporter/backend or production telemetry transport;
- full incident state machine, alert manager, on-call/paging, SLO/error-budget engine or recovery automation;
- compliance certification/legal determination, Control Evidence Map completion or evidence export product;
- FinOps billing/cost allocation engine;
- Safety, Session Policy, Portfolio Exposure, Risk, sizing, leverage, reservations or Harness trading controls;
- OMS, orders, fills, positions, balances, reconciliation or protection;
- strategies, signals, models, agents, Brain, RAG or Copilot;
- production deployment;
- limited-live or real-money trading;
- Stage 1+ implementation.

## Proof obligations
An implementation candidate under this authorization SHALL prove at minimum:
1. Existing S0A audit/evidence semantics are extended or compatibly migrated, not duplicated by a shadow contract model.
2. Audit/evidence/config/version records are immutable and versioned.
3. Canonical serialization/fingerprinting is deterministic across repeated construction.
4. Mutation/tampering changes the expected integrity result and is detected.
5. Append-only correction/supersession is modeled by a new record/reference; there is no in-place history rewrite API.
6. Environment mismatch fails closed for environment-scoped evidence/config provenance.
7. Tenant/account scope metadata, when present, remains compatible with S0B typed isolation and cannot silently cross scope.
8. Release/config/policy references are explicit, immutable and included in provenance where required.
9. Authority/truth classes are controlled and telemetry/derived evidence cannot masquerade as authoritative domain truth.
10. Raw secret material and arbitrary secret-bearing metadata are absent from source, fixtures, serialization, logs and test output.
11. No persistent audit store, external telemetry backend, exchange/network/trading capability or production config provider is introduced.
12. Existing S0A/S0B contract/security regression remains green.
13. Exact raw-head CI/evidence passes.
14. A fresh independent HIGH_ASSURANCE review returns `APPROVED` with unresolved CRITICAL=0 and HIGH=0 before merge.

## Proposed post-approval flags
Only after a later checkpoint promotion:
- `implementation_authorized=true`
- `implementation_authorization_scope=["HCT-IMP-0003-S0C"]`
- `implementation_authorization_ceiling="NON_TRADING_STAGE_0_AUDIT_EVIDENCE_CONFIG_VERSION_FOUNDATION_ONLY"`
- `production_credentials_authorized=false`
- `production_deployment_authorized=false`
- `limited_live_authorized=false`
- `live_trading_authorized=false`

## Independent review requirements
The reviewer SHALL verify:
- exact PR base/head identity;
- `HCT-CP-0018` provenance and fail-closed authorization state;
- S0A/S0B completion provenance;
- R11 Stage-0 dependency ordering;
- R08 `SEC-006` and R10-REQ-001/002/005/007/008/032 alignment;
- no semantic expansion into Stage 1 or production observability/storage/config infrastructure;
- no secret material/provider implementation;
- no exchange, trading, deployment or live authority;
- implementation Work Order completeness, negative tests and STOP CONDITION;
- exact-head authorization-governance CI success;
- zero unresolved CRITICAL/HIGH findings.

Verdict exactly one of:
- `APPROVED`
- `CORRECTION REQUIRED`
- `BLOCKED`

## STOP CONDITION
Do not begin product implementation from this document. Keep the authorization PR open and unmerged until exact-head governance CI succeeds and a separate HIGH_ASSURANCE execution stream publishes its verdict. Merge/promotion may authorize only `HCT-IMP-0003-S0C`. No production credentials, production deployment, limited-live or live trading are authorized by this candidate.
