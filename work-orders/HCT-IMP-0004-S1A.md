# HCT-IMP-0004-S1A - Exchange Abstraction, Capability & Contract Reference Foundation

Status: `AUTHORIZED`
Risk class: `HIGH_ASSURANCE`
Parent authorization increment: `HCT-IMPL-AUTH-0004 / COMPLETED_APPROVED`
Authorization checkpoint: `HCT-CP-0021 / IMPLEMENTATION_AUTHORIZED_S1A`
Planning baseline: `HCT-CP-0014 / PLANNING_FREEZE_APPROVED`
Authorization ceiling: `NON_TRADING_STAGE_1_EXCHANGE_ABSTRACTION_CAPABILITY_CONTRACT_FOUNDATION_ONLY`

## OBJECTIVE
Implement the first bounded Stage-1 exchange-domain foundation by creating an HCT-owned, provider-neutral, read-only exchange abstraction with immutable capability and contract/reference semantics, while introducing **no concrete exchange networking, credentials, market ingest, orders, money-state or trading authority**.

The implementation must make later MEXC integration safer by ensuring core HCT modules consume canonical HCT contracts rather than MEXC request/response payloads or exchange-native symbol strings.

## AUTHORIZATION PRECONDITION
Execution is authorized only while the canonical checkpoint proves all of the following exactly:
- `checkpoint_id="HCT-CP-0021"`;
- `status="IMPLEMENTATION_AUTHORIZED_S1A"`;
- `implementation_authorized=true`;
- `implementation_authorization_scope=["HCT-IMP-0004-S1A"]`;
- `implementation_authorization_ceiling="NON_TRADING_STAGE_1_EXCHANGE_ABSTRACTION_CAPABILITY_CONTRACT_FOUNDATION_ONLY"`;
- `production_credentials_authorized=false`;
- `production_deployment_authorized=false`;
- `limited_live_authorized=false`;
- `live_trading_authorized=false`.

Any context drift fails closed before product-code mutation.

Authorization evidence:
- authorization PR: `#46`;
- exact approved authorization head: `8e6ebe7a3ecf7b108a2bd57d5249b3eda310f388`;
- authorization merge: `7a458504de8721fdaffe6c3262781d1d5a675291`;
- exact-head governance run: `34705660182 / implementation-authorization-s1a-governance / success`;
- independent verdict: `APPROVED`, CRITICAL `0`, HIGH `0`;
- promotion record: `docs/116-s1a-implementation-authorization-approval-and-checkpoint-promotion.md`.

## CONTEXT
S0A established the canonical repository/runtime/shared-contract foundation. S0B established SecurityContext, tenant/account/environment binding and opaque secret-reference boundaries. S0C established audit/evidence/config-version integrity semantics. `HCT-CP-0020` consumed S0C authority and returned product implementation to fail closed; `HCT-CP-0021` now grants only this bounded S1A authority.

R11 Stage 1 begins `Exchange and realtime truth`. The first safe dependency is the exchange abstraction itself. A concrete MEXC adapter, universe engine, quota governor or market ingest must not become the place where canonical exchange identity and capability semantics are invented ad hoc.

This Work Order therefore implements only the domain/reference boundary needed for later Stage-1 slices.

## FROZEN SOURCE LOCATORS
Direct requirements:
- `REQ02::Market and exchange requirements::B2` — discover contract capabilities/constraints dynamically where exposed;
- `REQ02::Market and exchange requirements::B5` — exchange capability restrictions/API changes are versioned external dependencies;
- `REQ02::Market and exchange requirements::B7` — core modules depend on HCT-owned canonical exchange/domain interfaces;
- `REQ02::Market and exchange requirements::B8` — MEXC is the first concrete adapter and future venues require explicit mapping/governance;
- `REQ02::Market and exchange requirements::B9` — explicit capability matrix with visible reject/degrade behavior;
- `R11-REQ-006` — source-of-truth ownership;
- `R11-REQ-012` — typed identity/version registry;
- `R11-REQ-013` — failure/degradation propagation;
- `R11-REQ-014` — logical dependency DAG;
- `R11-REQ-024` — provider/topology neutrality.

Approved decision / architecture sources:
- `HCT-DEC-0023` in `docs/10-decisions-ledger.md`;
- `docs/14-product-module-map.md` Modules 1 and 2;
- `docs/23-multi-exchange-adapter-architecture.md`;
- `docs/91-r11-integrated-authority-state-dependency-architecture.md` Stage 1, Source-of-Truth Matrix and identity registry;
- `docs/99-r12-frozen-requirements-baseline.md` and `docs/100-r12-requirements-traceability-and-no-loss-proof.md`.

## FILES / SOURCES TO READ BEFORE MUTATION
Priority follows `docs/00-source-hierarchy.md`.

At minimum:
- `checkpoints/workstreams/planning/latest.json`;
- `checkpoints/history/HCT-CP-0021.json`;
- `docs/00-source-hierarchy.md`;
- `docs/03-scope.md`;
- `docs/09-definition-of-done.md`;
- `docs/10-decisions-ledger.md`;
- `docs/11-checkpoint.md`;
- `docs/14-product-module-map.md`;
- `docs/23-multi-exchange-adapter-architecture.md`;
- `docs/54-r05-realtime-requirements-addendum.md` for later-stage boundary awareness;
- `docs/91-r11-integrated-authority-state-dependency-architecture.md`;
- `docs/93-r11-integration-requirements-addendum.md`;
- `docs/99-r12-frozen-requirements-baseline.md`;
- `docs/100-r12-requirements-traceability-and-no-loss-proof.md`;
- `docs/104-chat-delivery-and-prompt-artifact-policy.md`;
- `docs/108-s0a-implementation-approval-and-checkpoint-promotion.md`;
- `docs/111-s0b-implementation-approval-and-checkpoint-promotion.md`;
- `docs/114-s0c-implementation-approval-and-checkpoint-promotion.md`;
- `docs/116-s1a-implementation-authorization-approval-and-checkpoint-promotion.md`;
- `work-orders/HCT-IMP-0004-S1A.md`;
- authorization Issue #45 and its exact approval evidence.

The executor SHALL inspect current code before choosing new files/classes so existing S0A/S0B/S0C primitives are reused rather than duplicated.

## REQUIRED ADR
Before substantive product code, add a bounded ADR under `adr/` that records:
- why S1A is provider-neutral and read-only;
- which identities belong in canonical shared contracts versus backend-only domain objects;
- why exchange-native symbols are metadata rather than canonical identity;
- capability-state semantics, including `UNKNOWN` fail-closed behavior;
- how immutable capability/contract snapshots are versioned/fingerprinted;
- why the concrete MEXC transport adapter is deferred;
- how later MEXC/universe/quota/realtime slices will depend on this boundary;
- explicit proof that no state-changing exchange command surface exists in S1A.

The ADR must not silently authorize later slices.

## AUTHORIZED IMPLEMENTATION SCOPE
### A. Canonical exchange identity primitives
Implement or extend the canonical contract system with typed/stable identities needed by the exchange reference domain, for example:
- Exchange identity;
- canonical Instrument/Contract identity;
- CapabilitySnapshot identity;
- ContractSpec/ReferenceSnapshot identity where needed.

Use existing `StableId` / generated-contract conventions where they fit. If new identity kinds or canonical schemas are required, update the language-neutral source and generated/runtime parity deterministically.

Do not overload mutable display names or exchange-native symbols as canonical IDs.

### B. Exchange descriptor and source metadata
Add an immutable provider-neutral exchange descriptor/reference object sufficient to identify the venue and the version/source of capability/reference metadata.

It may contain only safe non-secret metadata. It must not contain API keys, signatures, session tokens, credential handles that expose values, or transport-client objects.

### C. Capability taxonomy and immutable snapshot
Add a controlled capability taxonomy and immutable/versioned capability snapshot.

At minimum, support explicit semantics equivalent to:
- `SUPPORTED`;
- `UNSUPPORTED`;
- `UNKNOWN` / not proven.

A stricter `RESTRICTED`-like state may be added only if justified and tested. No unknown state may coerce to supported. Capability declarations are descriptive reference evidence only and do not grant monetary/trading authority.

Capability families MAY describe future exchange features such as market/reference data availability, supported order semantics or margin modes, but this slice must not implement the corresponding runtime actions.

### D. Canonical contract/reference specification
Add an immutable provider-neutral reference model for venue contract facts needed by later modules. The exact model should be minimal but may cover:
- canonical contract identity;
- venue/exchange identity;
- exchange-native symbol mapping;
- lifecycle/status classification;
- base/quote/settlement asset identifiers or safe canonical codes;
- contract type;
- price increment / quantity increment / precision semantics;
- minimum/maximum quantity and notional fields where known;
- supported margin-mode or venue-rule references where represented;
- version/fingerprint/source timestamps where materially needed.

Use exact decimal-safe representations. Invalid, negative, zero-where-forbidden or internally inconsistent values fail closed. Unknown material values remain explicit rather than receiving permissive defaults.

This is reference metadata, not Risk Engine authority.

### E. Read-only Exchange Reference Adapter port
Define a narrow provider-neutral protocol/port used by future concrete adapters to expose reference data.

Allowed responsibilities are read-only and may include conceptually:
- describe exchange;
- obtain a capability snapshot;
- list reference contract specifications;
- resolve one contract reference by canonical or venue mapping.

Exact method names are implementation detail, but there SHALL be **no state-changing command methods**.

The port SHALL NOT:
- place/cancel/replace orders;
- mutate leverage or margin mode;
- submit triggers/TP/SL/trailing commands;
- authenticate/sign requests;
- expose private account/position/balance data;
- open REST/WebSocket connections in S1A.

### F. Bounded canonical result/error semantics
Add only the controlled result/error vocabulary needed by the read-only reference boundary, for example:
- unknown contract;
- unsupported capability;
- capability unknown/unproven;
- malformed/inconsistent reference data;
- reference unavailable.

Do not build retry/circuit/backoff/quota/reconnect runtime in this slice.

### G. Deterministic test adapters
A null/fake/in-memory adapter may exist for tests only. It must be deterministic, credential-free, network-free and obviously non-production.

No fake may claim real MEXC truth or be wired to production/runtime endpoints.

### H. Contract generation and compatibility
If S1A adds canonical shared schemas:
- update only the existing canonical contract source/generator path;
- regenerate deterministic backend/runtime outputs;
- preserve exact schema parity checks;
- avoid hand-maintained duplicate models when generation is intended;
- do not add frontend behavior or trading UI.

### I. Evidence and CI
Add S1A-specific static boundary checks, tests, exact-head CI and evidence. The implementation PR must remain open/unmerged for independent HIGH_ASSURANCE review.

## EXPLICITLY NOT AUTHORIZED
Do not implement:
- concrete MEXC adapter/client/transport;
- MEXC REST, WebSocket, SDK or network calls;
- any runtime HTTP/WebSocket/socket exchange client;
- official/private API authentication or request signing;
- API keys, secret values, credential lifecycle or production SecretStore provider;
- private user/account/order/position feeds;
- public realtime market-data ingest;
- exchange subscription/session/reconnect generation runtime;
- Market Universe eligibility/scanner runtime;
- API quota/WS/backpressure scheduler or circuit runtime;
- Data Quality & Freshness runtime;
- order-book reconstruction, Market-State Fabric or cache/hot state;
- order placement/cancel/replace, trigger/TP/SL/trailing execution;
- fills/positions/balances/OMS/reconciliation/protection;
- Safety, Session Policy, Risk, Portfolio Exposure, Position Sizing, Leverage or Risk Reservation;
- persistent exchange/reference database or RLS;
- new public trading API routes;
- frontend trading controls or cockpit exchange controls;
- production deployment;
- limited-live;
- real-money trading;
- any later Stage-1 or Stage-2+ capability.

## ARCHITECTURE CONSTRAINTS
1. Core HCT domain code depends on HCT-owned canonical exchange interfaces, never MEXC payload classes.
2. Exchange-native symbol/name is mapping metadata, not sole canonical identity.
3. Capability state is immutable/versioned and explicit; `UNKNOWN` fails closed.
4. Capability/reference data does not grant Security/Risk/Execution authority.
5. S1A remains read-only and network-free.
6. No secret-bearing field or credential path is introduced.
7. No public/private stream ingest or exchange session lifecycle exists.
8. No state-changing exchange command API exists.
9. No persistence is required for S1A proof.
10. Existing environment/tenant/account/provenance rules continue to apply where materially relevant.
11. Frozen planning semantics are not modified by product code.
12. The known stale historical S0B workflow is not silently edited by this slice.

## REQUIRED TEST MATRIX
At minimum, deterministic tests/evidence SHALL cover:

### Identity and canonical contracts
- exchange identity round-trip/stability;
- canonical contract identity distinct from venue symbol/display name;
- malformed identity rejection;
- generated contract reproducibility and runtime parity if shared schemas change;
- version/hash identity changes when behaviorally material canonical content changes.

### Capability semantics
- supported capability remains explicit;
- unsupported capability remains explicit;
- unknown/unproven capability fails closed;
- no boolean/default coercion upgrades unknown to supported;
- materially different capability snapshot changes fingerprint/version evidence;
- capability snapshot is immutable;
- unsupported/unknown capability cannot be silently emulated by helper APIs.

### Contract/reference semantics
- immutable contract/reference snapshot;
- deterministic fingerprinting/version evidence where used;
- zero/negative/invalid increments or limits reject where forbidden;
- invalid precision/increment relationships reject;
- inconsistent min/max relationships reject;
- unknown material venue rule remains explicit;
- lifecycle/status unknown or malformed input fails closed;
- exchange-native symbol changes do not mutate canonical identity unless governed mapping/version semantics require a new reference snapshot.

### Adapter boundary
- protocol/port exposes only read/reference semantics;
- no state-changing order/leverage/margin mutation methods;
- fake/null adapter is deterministic;
- fake/null adapter performs no network access;
- no production MEXC adapter is present;
- no runtime network-client import exists in newly added S1A production modules;
- no auth/signing/credential handling exists in S1A code.

### Security/provenance regression
- S0A canonical contract/environment regression PASS;
- S0B SecurityContext/tenant/account/SecretRef regression PASS;
- S0C audit/evidence/provenance regression PASS;
- secret scan PASS;
- unauthorized-capability scan PASS;
- no raw secret material in source/fixtures/log output.

### Engineering quality
- backend unit suite PASS;
- frontend regression suite PASS even if frontend is unchanged;
- Ruff/format PASS;
- strict mypy PASS;
- backend build PASS;
- frontend typecheck/lint/format/build PASS;
- Python dependency audit PASS with no known HIGH/CRITICAL vulnerabilities accepted silently;
- npm audit PASS under existing project threshold;
- lockfile integrity PASS;
- `git diff --check` PASS;
- changed-file boundary PASS;
- exact raw-head CI PASS.

Coverage must not regress below the currently accepted project baseline without explicit independent approval. New exchange-domain logic should receive focused branch/negative coverage rather than relying only on total-project percentage.

## REQUIRED STATIC BOUNDARY SCAN
Add or extend a deterministic S1A boundary scan that fails closed if S1A production code introduces unauthorized capabilities.

The scan should inspect the changed candidate and/or authorized exchange-domain modules for concrete evidence of prohibited runtime behavior, including:
- network client imports/usages intended for external exchange calls;
- WebSocket/socket transport implementation;
- MEXC SDK/client implementation;
- authentication/signing functions;
- secret-shaped material or raw credential fields;
- order placement/cancel/replace/state-changing method surfaces;
- market ingest/subscription runtime;
- persistence/database adapter implementation;
- production deployment configuration introduced by S1A.

The scan must avoid naive false positives against documentation/test vocabulary. Prefer AST/structured checks where practical.

## ALLOWED FILE SURFACE
The executor may add/modify only files objectively required for S1A, such as:
- a new ADR under `adr/`;
- canonical shared schemas/generator outputs under the existing contract system when required;
- backend exchange-domain modules under `apps/backend/src/hct_backend/`;
- backend tests;
- S1A validation/boundary scripts;
- S1A implementation governance workflow;
- `evidence/HCT-IMP-0004-S1A.md`.

No checkpoint, frozen requirements, Scope, Decisions Ledger, unrelated historical workflow, deployment or frontend product feature file may be modified by the executor unless the Work Order is first changed through governance.

## EVIDENCE ARTIFACT
Create `evidence/HCT-IMP-0004-S1A.md` or the exact established equivalent and record:
- Context Lock and authorized checkpoint;
- exact base/head;
- ADR;
- changed files and why each is required;
- canonical identity/schema decisions;
- capability-state model;
- adapter-port API summary proving read-only semantics;
- test counts/results and coverage;
- contract generation/parity result;
- S0A/S0B/S0C regression results;
- secret scan and unauthorized-capability scan;
- dependency audits;
- backend/frontend build/type/lint/format results;
- known limitations and explicitly deferred Stage-1 work;
- final exact PR head and CI run/checks;
- `production_credentials_authorized=false`;
- `production_deployment_authorized=false`;
- `limited_live_authorized=false`;
- `live_trading_authorized=false`.

No pass may be fabricated.

## IMPLEMENTATION PR
After all local/author evidence passes:
- push exactly one implementation branch, preferably `implementation/HCT-IMP-0004-S1A`;
- open one PR to `main` titled `HCT-IMP-0004-S1A - Exchange Abstraction, Capability & Contract Reference Foundation`;
- reference the implementation issue created after authorization promotion;
- include Context Lock, authorization ceiling, scope, negative-scope confirmation, ADR, tests/evidence, CI and limitations;
- run exact raw-head S1A governance CI;
- publish author-side preflight evidence clearly marked as **not independent approval**.

## INDEPENDENT REVIEW
A separate HIGH_ASSURANCE/HEDS Delta execution stream must review the exact implementation head. It must inspect the full diff, tests, CI, architecture, canonical contract changes and negative capability boundary.

Required verdict exactly one:
- `APPROVED`
- `CORRECTION REQUIRED`
- `BLOCKED`

Merge is prohibited unless the exact reviewed head remains unchanged, exact-head CI is green, unresolved CRITICAL=0 and HIGH=0, and the independent verdict is `APPROVED`.

## STOP CONDITION
STOP with the S1A implementation PR OPEN and UNMERGED after exact-head evidence and author-side preflight. Do not self-approve, merge, promote the completion checkpoint, implement concrete MEXC connectivity, add credentials, deploy production, activate limited-live, enable real-money trading or begin any later Stage-1/Stage-2 slice.
