# HCT-IMPL-AUTH-0003 - Implementation Authorization Work Order

Status: `PENDING_INDEPENDENT_REVIEW`
Risk class: `HIGH_ASSURANCE`
Issue: `#39`
Candidate implementation slice: `HCT-IMP-0003-S0C`
Canonical base at start: `main@2cbc7d07adee06bc11e967ff7cfbd7671424cc1d`
Checkpoint at start: `HCT-CP-0018 / S0B_IMPLEMENTATION_APPROVED_MERGED`

## OBJECTIVE
Govern whether exactly one bounded remaining R11 Stage-0 foundation slice may begin without granting exchange, secret-material, persistence, deployment or live authority.

## CONTEXT
R11 Stage 0 requires shared contracts, SecurityContext/tenant/account binding, SecretStore, audit/evidence primitives, configuration/version semantics and environment namespace before Stage 1 exchange/realtime truth.

S0A completed the repository/runtime/canonical-contract/environment skeleton and basic audit/evidence envelopes. S0B completed SecurityContext, tenant/account/environment binding, fail-closed authorization guards and opaque SecretStore references. `HCT-CP-0018` consumed S0B authorization and returned implementation authority to fail closed.

The next bounded prerequisite is therefore the audit/evidence integrity plus release/config/policy version semantics needed to give later domains stable provenance and non-authoritative telemetry semantics without introducing exchange or production infrastructure.

## SOURCE AUTHORITY
Read and bind this authorization to, at minimum:
- `checkpoints/workstreams/planning/latest.json`;
- `checkpoints/history/HCT-CP-0018.json`;
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
- `docs/112-implementation-authorization-s0c-candidate.md`;
- `work-orders/HCT-IMP-0003-S0C.md`.

Priority remains checkpoint -> Decisions Ledger/ADRs -> Scope/DoD/Architecture -> frozen requirements -> other supporting artifacts.

## SCOPE
This authorization increment may only:
1. select `HCT-IMP-0003-S0C` as the next bounded implementation candidate;
2. prove R11 dependency ordering and frozen-source alignment;
3. define exact implementation scope, exclusions, acceptance criteria, tests, evidence and STOP CONDITION;
4. establish a ceiling that permits only non-trading Stage-0 audit/evidence/config-version foundation work;
5. run governance-only CI and independent review;
6. if and only if independently approved, merge governance artifacts and promote a later checkpoint authorizing exactly `HCT-IMP-0003-S0C`.

No product-code mutation is authorized by this Work Order itself.

## FROZEN REQUIREMENT LOCATORS
The candidate must preserve at minimum:
- R08 `SEC-006` audit integrity/isolation;
- R10 `R10-REQ-001` observability non-authority;
- R10 `R10-REQ-002` observability context envelope;
- R10 `R10-REQ-005` telemetry data firewall;
- R10 `R10-REQ-007` append-only audit;
- R10 `R10-REQ-008` audit event taxonomy;
- R10 `R10-REQ-032` release/config observability;
- R11 sections 6, 10, 11, 13;
- all R12 frozen-baseline source identity and no-loss rules.

## PROPOSED AUTHORIZED IMPLEMENTATION
Exactly:

`HCT-IMP-0003-S0C - Audit/Evidence Integrity & Configuration/Version Semantics Foundation`

Proposed authorization ceiling:

`NON_TRADING_STAGE_0_AUDIT_EVIDENCE_CONFIG_VERSION_FOUNDATION_ONLY`

## REQUIRED NEGATIVE BOUNDARY
Authorization SHALL NOT include:
- real secrets/credentials or credential lifecycle;
- production SecretStore provider integration, encryption, KMS/HSM;
- exchange/MEXC adapters, network clients, REST/WebSocket, signing or private/public feeds;
- market data, universe, quota/WS governor or Market-State Fabric;
- DB/RLS, audit persistence service, WORM/object lock or external signing infrastructure;
- external telemetry collector/exporter/backend;
- full incident response, SLO/error-budget, alerts/on-call or FinOps engines;
- compliance certification/legal determination;
- Safety/Session/Risk/Portfolio/Sizing/Leverage/Reservation/Harness trading authority;
- OMS/Execution/orders/fills/positions/balances/reconciliation/protection;
- strategy/signal/intelligence/RAG/agent/Brain/Copilot;
- production deployment;
- limited-live;
- live trading;
- any Stage 1+ product implementation.

## AUTHORIZATION ACCEPTANCE CRITERIA
A. Current `main` and `HCT-CP-0018` are recovered exactly before mutation.
B. `implementation_authorized=false` remains authoritative throughout this candidate.
C. Candidate selects exactly one bounded implementation slice.
D. Candidate is the next remaining R11 Stage-0 dependency after S0A/S0B.
E. Frozen requirement/source locators are explicit and lossless.
F. Scope reuses/hardens existing S0A audit/evidence contracts rather than defining a competing truth model.
G. Audit/evidence integrity and append-only correction semantics are bounded to provider-neutral primitives, not persistence infrastructure.
H. Config/release/policy version semantics are bounded to immutable provenance/fingerprint primitives, not production config control planes.
I. Telemetry/evidence cannot create or upgrade trading authority.
J. Secret/data-firewall requirements are explicit.
K. Implementation acceptance criteria contain deterministic tamper, canonicalization, scope/environment/version and regression tests.
L. No exchange/network/trading/persistence/deployment/live capability is authorized.
M. Higher authorization flags remain false.
N. Governance-only PR diff boundary passes.
O. Exact raw-head authorization-governance CI passes.
P. Independent HIGH_ASSURANCE review returns `APPROVED`, unresolved CRITICAL=0, HIGH=0.

## REQUIRED EVIDENCE
The authorization PR must expose:
- exact base/head SHA;
- candidate file list;
- governance-only diff proof;
- current checkpoint and fail-closed authorization flags;
- frozen source/requirement locator proof;
- Stage-0 ordering rationale;
- explicit implementation scope and ceiling;
- explicit prohibited capabilities;
- implementation Work Order completeness;
- exact-head CI run/check result;
- independent review verdict and finding counts.

## REVIEW FORMAT
Independent reviewer returns exactly one:
- `APPROVED`
- `CORRECTION REQUIRED`
- `BLOCKED`

The review must be performed from a separate execution stream and reconstruct the verdict from exact repository/CI evidence rather than trusting author assertions.

## STOP CONDITION
Stop with the authorization PR open and unmerged after exact-head governance CI and author-side evidence. Do not begin `HCT-IMP-0003-S0C`, do not promote a checkpoint and do not change any authorization flag until a separate HIGH_ASSURANCE review approves the exact authorization head with CRITICAL=0 and HIGH=0.

Production credentials, production deployment, limited-live and live trading remain false regardless of this authorization candidate.
