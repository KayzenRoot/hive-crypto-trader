# HCT-IMP-0003-S0C - Audit/Evidence Integrity & Configuration/Version Semantics Foundation

Status: `PENDING_AUTHORIZATION`
Risk class: `HIGH_ASSURANCE`
Parent authorization increment: `HCT-IMPL-AUTH-0003 / PENDING_INDEPENDENT_REVIEW`
Current checkpoint: `HCT-CP-0018 / S0B_IMPLEMENTATION_APPROVED_MERGED`
Planning baseline: `HCT-CP-0014 / PLANNING_FREEZE_APPROVED`
Proposed authorization ceiling: `NON_TRADING_STAGE_0_AUDIT_EVIDENCE_CONFIG_VERSION_FOUNDATION_ONLY`

## OBJECTIVE
Finish the remaining bounded R11 Stage-0 provenance foundation by hardening the existing audit/evidence primitives and defining immutable release/config/policy version semantics, without persistence, exchange/network capability, production observability infrastructure or trading authority.

## AUTHORIZATION PRECONDITION
This Work Order MUST NOT be executed until a later canonical checkpoint explicitly sets:
- `implementation_authorized=true`;
- `implementation_authorization_scope=["HCT-IMP-0003-S0C"]`;
- `implementation_authorization_ceiling="NON_TRADING_STAGE_0_AUDIT_EVIDENCE_CONFIG_VERSION_FOUNDATION_ONLY"`.

Until then, product-code mutation is prohibited.

## CONTEXT
S0A created the canonical runtime/contracts/environment foundation and basic `AuditEnvelope` / `EvidenceEnvelope`. S0B created server-derived `SecurityContext`, tenant/account/environment isolation and opaque SecretStore references. R11 Stage 0 still requires mature audit/evidence primitives plus configuration/version semantics before Stage 1 exchange and realtime truth can be safely introduced.

S0C therefore creates only the provider-neutral provenance/integrity foundation later domains will bind to. It is not an observability platform, config service, audit database or trading subsystem.

## FROZEN SOURCE LOCATORS
At minimum:
- R08 `SEC-006` — audit integrity/isolation;
- R10 `R10-REQ-001` — observability non-authority;
- R10 `R10-REQ-002` — observability context envelope;
- R10 `R10-REQ-005` — telemetry data firewall;
- R10 `R10-REQ-007` — append-only audit;
- R10 `R10-REQ-008` — audit taxonomy;
- R10 `R10-REQ-032` — release/config observability;
- R11 §6 Source-of-Truth Matrix;
- R11 §10 live/paper/shadow/replay namespace contract;
- R11 §11 canonical identity/version registry;
- R11 §13 Stage-0 dependency DAG;
- R12 frozen requirements baseline and no-loss proof.

## FILES / SOURCES TO READ BEFORE MUTATION
At minimum:
- `checkpoints/workstreams/planning/latest.json`;
- the future checkpoint that authorizes this exact Work Order;
- `docs/00-source-hierarchy.md`;
- `docs/09-definition-of-done.md`;
- `docs/10-decisions-ledger.md`;
- `docs/11-checkpoint.md`;
- `docs/71-r08-high-security-commercialization-hardening.md`;
- `docs/73-r08-multitenant-security-requirements-addendum.md`;
- `docs/84-r10-critical-observability-incident-architecture.md`;
- `docs/87-r10-observability-audit-incident-finops-requirements-addendum.md`;
- `docs/91-r11-integrated-authority-state-dependency-architecture.md`;
- `docs/99-r12-frozen-requirements-baseline.md`;
- `docs/100-r12-requirements-traceability-and-no-loss-proof.md`;
- `docs/108-s0a-implementation-approval-and-checkpoint-promotion.md`;
- `docs/111-s0b-implementation-approval-and-checkpoint-promotion.md`;
- S0A/S0B contracts, security primitives, tests, CI and evidence;
- this Work Order.

## EXPECTED IMPLEMENTATION SURFACE
The executor SHOULD keep the slice within a small backend/domain surface such as:
- one ADR for S0C provenance/integrity/version boundaries;
- existing `apps/backend/src/hct_backend/contracts.py` only where existing S0A audit/evidence models must be compatibly hardened;
- one focused backend provenance/integrity module if separation is clearer;
- focused backend tests;
- one S0C boundary scanner/validator if required;
- one S0C exact-head governance workflow;
- `evidence/HCT-IMP-0003-S0C.md`.

Public OpenAPI/frontend contracts SHOULD remain unchanged unless a frozen requirement makes a minimal shared primitive unavoidable. Any such change must be deterministic, backward-safe for S0A/S0B and explicitly justified in the ADR/evidence.

## SCOPE
### S0C-1 — Canonical audit/evidence record hardening
Reuse/extend existing S0A primitives. The canonical record model shall carry only safe structured metadata and references, not arbitrary raw payloads.

Where applicable include:
- immutable event/evidence identity;
- schema/version identity;
- environment;
- actor/workload identity class and safe actor reference;
- tenant/account scope references compatible with S0B isolation;
- action/target/outcome/assurance/reason classifications;
- correlation/trace reference;
- release/build, config and policy version references;
- authority/truth/source class;
- data classification/redaction class;
- deterministic event/evidence timing fields;
- payload/evidence hash rather than unrestricted sensitive payload content.

### S0C-2 — Deterministic canonical integrity
Implement a deterministic provider-neutral canonicalization/fingerprint mechanism for the bounded records.

Required semantics:
- same semantic record -> same canonical bytes/text -> same SHA-256 fingerprint;
- ordering or irrelevant runtime representation differences do not create accidental drift where canonicalization says they are equivalent;
- semantically material changes alter the fingerprint;
- integrity validation fails closed on malformed/mismatched hashes;
- no hidden nondeterministic timestamp/random input inside fingerprint verification.

### S0C-3 — Append-only linkage and correction semantics
Provide pure/domain primitives sufficient to model and verify append-only integrity linkage.

Allowed:
- previous event ID/hash reference;
- deterministic chain/link verification over an in-memory/test sequence;
- supersedes/corrects reference to prior event/evidence;
- explicit correction reason/classification.

Required:
- corrections create new immutable records;
- prior record content is never mutated through the S0C API;
- tamper, deletion, insertion/reordering or mismatched predecessor references are detected by the verifier where the chain model applies.

This is not persistent ledger storage.

### S0C-4 — Authority/truth/source classification
Implement controlled enums/value objects sufficient to distinguish, where applicable:
- authoritative external evidence;
- authoritative internal domain state;
- reconciled projection;
- telemetry observation;
- derived/estimated evidence;
- unavailable/unknown state.

The exact final vocabulary may be smaller if the ADR proves it remains lossless for the frozen requirements.

No telemetry/evidence class grants monetary/trading authority. A lower-authority class cannot be relabeled/upgraded without new authoritative evidence under a future domain-specific rule.

### S0C-5 — Release/config/policy version provenance
Implement immutable version/provenance references reusing S0A/S0B identities wherever possible.

A bounded `ConfigSnapshot` / `ConfigProvenance` equivalent may contain only safe metadata such as:
- config stable identity/version;
- environment namespace;
- canonical non-secret fingerprint/hash;
- release/build reference;
- policy/version reference(s);
- created/effective timestamps;
- safe source/classification metadata;
- optional predecessor/supersession reference.

It shall not contain secret values and shall not operate a production config service.

### S0C-6 — Telemetry/evidence data firewall
High-assurance record constructors/serializers shall use structured allowlisted fields.

Prohibited in these record types:
- raw API keys/secret keys/private keys;
- bearer/session/recovery tokens;
- raw SecretStore values;
- unrestricted arbitrary payload dictionaries intended to carry sensitive values;
- prompt/private reasoning material;
- credentials disguised as config metadata.

Opaque `CredentialRef` / `SecretRef` may appear only in their governed non-secret reference form if a frozen requirement requires such linkage.

### S0C-7 — Regression and boundary proof
Preserve all S0A/S0B contracts and tests. S0C cannot weaken environment isolation, SecurityContext, SecretStore opacity, secret scanning, route allowlist, public API surface or frontend non-authority.

## OUT OF SCOPE
Do not implement:
- any product code unless this exact Work Order is checkpoint-authorized;
- audit database/schema/storage adapter, WORM/object lock, immutable object storage, blockchain or external signing/KMS service;
- external telemetry collector/exporter/agent/backend, OpenTelemetry deployment or metrics storage;
- full logging framework replacement;
- incident state machine, alerting/on-call, SLO/error-budget engine, recovery automation or runbook platform;
- compliance certification/legal determination, full Control Evidence Map or evidence export product;
- retention scheduler/legal-hold engine;
- production configuration service, remote feature-flag provider, admin config UI or deployment control plane;
- real secret material, credential lifecycle, encryption/KMS/HSM or production SecretStore provider;
- MEXC/exchange/network clients, REST/WebSocket, signing, market data, private streams or quota governor;
- database/RLS generally;
- Safety/Session/Risk/Portfolio/Sizing/Leverage/Reservation/Harness trading authority;
- OMS/Execution/orders/fills/positions/balances/reconciliation/protection;
- strategy/signal/intelligence/RAG/agent/Brain/Copilot;
- production deployment;
- limited-live;
- real-money trading;
- Stage 1+ implementation.

## REQUIREMENTS
### REQ-S0C-001 — No competing truth
Audit/evidence/telemetry primitives SHALL identify their source/authority class and SHALL NOT become a competing source of exchange, OMS, reconciliation, Security, Safety or Risk truth.

### REQ-S0C-002 — Safe structured provenance
High-assurance records SHALL use explicit immutable structured fields for environment, scope, correlation, release/config/policy and classification context where applicable.

### REQ-S0C-003 — Secret firewall
Raw secret material SHALL be structurally absent from bounded audit/evidence/config provenance APIs and tests.

### REQ-S0C-004 — Deterministic integrity
Canonicalization and fingerprints SHALL be reproducible and fail closed on mismatch.

### REQ-S0C-005 — Append-only correction
Correction/supersession SHALL create a new record linked to prior evidence. No in-place history rewrite API is permitted.

### REQ-S0C-006 — Scope/environment integrity
Environment and tenant/account scope metadata, when present, SHALL remain exact and compatible with S0B fail-closed isolation.

### REQ-S0C-007 — Explicit release/config/policy provenance
Behaviorally relevant release/config/policy state SHALL be referenceable by immutable identity/version/fingerprint semantics.

### REQ-S0C-008 — No production infrastructure
S0C SHALL not add persistence, external telemetry/config providers, exchange/network capability or production deployment authority.

### REQ-S0C-009 — Regression
S0A and S0B guarantees SHALL remain green and unweakened.

### REQ-S0C-010 — Evidence
Exact-head CI/evidence and independent HIGH_ASSURANCE review are mandatory before merge.

## ACCEPTANCE CRITERIA
A. Exact authorized checkpoint/context lock passes before mutation.
B. Existing audit/evidence contracts are reused or compatibly migrated; no shadow model exists.
C. Records are immutable and versioned.
D. Canonical serialization/fingerprint is deterministic.
E. A material field change changes expected hash and verifier rejects mismatch.
F. Append-only chain/link verifier detects predecessor/hash tamper where applicable.
G. Correction/supersession creates a new record and preserves original evidence identity/hash.
H. Cross-environment record/config provenance mismatch fails closed.
I. Tenant/account scope mismatch, when modeled, fails closed using S0B-compatible typed semantics.
J. Release/config/policy references reject wrong identity kind/version/hash semantics.
K. Authority/truth/source classes are controlled, explicit and non-upgradable by arbitrary caller text.
L. Safe serialization contains no raw secret/ref value beyond explicitly governed opaque-reference metadata.
M. No unrestricted secret-bearing payload/config map exists in the high-assurance primitive surface.
N. No persistence, external telemetry/config provider, exchange/network/trading or deployment capability exists.
O. S0A/S0B full regression passes.
P. Backend lint/type/build/tests and dependency audit pass.
Q. Frontend regression remains green.
R. Static secret and prohibited-capability scans pass.
S. Candidate-aware `git diff --check` passes against exact authorized base.
T. Exact raw-head CI passes.
U. Independent HIGH_ASSURANCE review returns `APPROVED` with CRITICAL=0 and HIGH=0.

## REQUIRED TEST MATRIX
At minimum:
- immutable/frozen audit/evidence/config provenance records;
- deterministic canonicalization repeated construction;
- canonicalization stability across supported field ordering/representation cases;
- malformed hash rejected;
- payload/reference/hash tamper detected;
- predecessor hash/ID mismatch detected;
- deletion/insertion/reordering detection where chain verifier applies;
- append-only correction/supersession preserves prior record and produces new identity/hash;
- correction referencing wrong environment/scope rejected;
- `LIVE`/`PAPER`/`SHADOW`/`REPLAY` mismatch cases;
- tenant/account mismatch cases where scoped audit/evidence is modeled;
- release/config identity kind mismatch rejected;
- policy/config/release version/fingerprint mismatch rejected;
- controlled authority/truth/source enum rejects arbitrary values;
- derived/telemetry class cannot be treated as authoritative by primitive helper/validator;
- secret-like raw fields/values are rejected or structurally impossible;
- opaque SecretRef/CredentialRef remains non-secret if referenced;
- no arbitrary raw payload serialization path;
- S0A contract generation/parity and route allowlist regression;
- S0B SecurityContext/binding/SecretStore/scanner regression;
- backend Ruff, strict mypy, build, full tests and dependency audit;
- frontend typecheck/tests/lint/format/build/npm audit;
- changed-text secret/capability boundary scan;
- `git diff --check` against exact PR base.

Property/fuzz tests SHOULD be used for canonicalization, typed identity/version validation and tamper permutations when they improve proof quality without adding unnecessary dependency weight.

## DELIVERABLES
- one S0C ADR before substantive code;
- bounded canonical audit/evidence/config-version implementation;
- deterministic integrity/correction primitives;
- complete negative test matrix;
- boundary scanner/governance updates if required;
- `evidence/HCT-IMP-0003-S0C.md`;
- one implementation PR;
- exact raw-head CI evidence;
- author-side handoff;
- fresh independent HIGH_ASSURANCE review verdict.

## REVIEW FORMAT
Independent reviewer returns exactly one:
- `APPROVED`
- `CORRECTION REQUIRED`
- `BLOCKED`

Review SHALL report exact base/head, requirement/source locators, no-shadow-contract proof, integrity/tamper/correction tests, scope/environment/version tests, secret firewall, prohibited-capability audit, full regression, CI identity, CRITICAL count and HIGH count.

## STOP CONDITION
After implementation, stop with the S0C implementation PR OPEN and UNMERGED after exact-head CI/evidence and author-side preflight. Do not merge, promote checkpoint, add persistence, add real secrets, connect telemetry/config providers, connect to an exchange, deploy production, activate limited-live or enable real-money trading. A separate independent HIGH_ASSURANCE review is mandatory.
