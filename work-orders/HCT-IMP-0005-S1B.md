# HCT-IMP-0005-S1B - MEXC Public Reference Adapter & Capability/Rule Resolver

Status: `AUTHORIZED`
Risk class: `HIGH_ASSURANCE`
Parent authorization increment: `HCT-IMPL-AUTH-0005 / COMPLETED_APPROVED`
Planning baseline: `HCT-CP-0014 / PLANNING_FREEZE_APPROVED`
Required pre-execution checkpoint: `HCT-CP-0023 / IMPLEMENTATION_AUTHORIZED_S1B`
Authorization ceiling: `NON_TRADING_STAGE_1_MEXC_PUBLIC_REFERENCE_CAPABILITY_RESOLVER_ONLY`
Implementation issue: `#51`

## OBJECTIVE
Implement the smallest concrete MEXC dependency after S1A by adding a MEXC Futures adapter restricted to public, unauthenticated, read-only reference/capability discovery and deterministic translation into HCT-owned S1A exchange models.

The slice SHALL NOT implement streaming, private/account access, credentials, signing, market ingest, orders, money-state or trading authority.

## AUTHORIZATION PRECONDITION
Execution is forbidden until the canonical checkpoint proves exactly:
- `checkpoint_id="HCT-CP-0023"`;
- `status="IMPLEMENTATION_AUTHORIZED_S1B"`;
- `implementation_authorized=true`;
- `implementation_authorization_scope=["HCT-IMP-0005-S1B"]`;
- `implementation_authorization_ceiling="NON_TRADING_STAGE_1_MEXC_PUBLIC_REFERENCE_CAPABILITY_RESOLVER_ONLY"`;
- `production_credentials_authorized=false`;
- `production_deployment_authorized=false`;
- `limited_live_authorized=false`;
- `live_trading_authorized=false`.

Any context drift fails closed before product-code mutation.

## CONTEXT
S1A completed the provider-neutral exchange reference foundation: canonical exchange/contract identities, immutable capability/reference snapshots, fail-closed `SUPPORTED` / `UNSUPPORTED` / `UNKNOWN` semantics, exact decimal validation, a read-only `ExchangeReferenceAdapter` boundary and static scans preventing network/auth/trading capability from entering that slice.

R11 Stage 1 orders Exchange Abstraction + MEXC adapter before Universe, quota/WS, market ingest, quality, Market-State Fabric and cache. S1B is therefore the first concrete venue integration, intentionally limited to public reference REST reads so that real MEXC contract/rule facts can be normalized before realtime or trading authority is introduced.

## FROZEN SOURCE LOCATORS
Direct requirements:
- `REQ02::Market and exchange requirements::B1` - prefer WebSocket for realtime streams where appropriate and REST for reference paths;
- `REQ02::Market and exchange requirements::B2` - discover contract capabilities and constraints dynamically where exposed;
- `REQ02::Market and exchange requirements::B5` - exchange restrictions/API changes are versioned external dependencies;
- `REQ02::Market and exchange requirements::B7` - core modules depend on HCT-owned canonical exchange/domain interfaces;
- `REQ02::Market and exchange requirements::B8` - MEXC is the first concrete exchange adapter;
- `REQ02::Market and exchange requirements::B9` - explicit capability matrix with visible reject/degrade behavior;
- `R11-REQ-006` - canonical source-of-truth ownership;
- `R11-REQ-012` - typed/stable identity and material version/hash semantics;
- `R11-REQ-013` - explicit failure/degradation propagation;
- `R11-REQ-014` - implementation follows the dependency DAG;
- `R11-REQ-024` - provider/topology neutrality where applicable.

Supporting architecture:
- `HCT-DEC-0023` in `docs/10-decisions-ledger.md`;
- `docs/14-product-module-map.md` Modules 1, 2, 3, 4 and 29;
- `docs/23-multi-exchange-adapter-architecture.md`;
- `docs/54-r05-realtime-requirements-addendum.md`;
- `docs/91-r11-integrated-authority-state-dependency-architecture.md`;
- `docs/117-s1a-implementation-approval-and-checkpoint-promotion.md`;
- `docs/119-s1b-implementation-authorization-approval-and-checkpoint-promotion.md`.

## REQUIRED SOURCES TO READ BEFORE MUTATION
Priority follows `docs/00-source-hierarchy.md`.

At minimum:
- `checkpoints/workstreams/planning/latest.json`;
- `checkpoints/history/HCT-CP-0023.json`;
- `docs/00-source-hierarchy.md`;
- `docs/03-scope.md`;
- `docs/09-definition-of-done.md`;
- `docs/10-decisions-ledger.md`;
- `docs/11-checkpoint.md`;
- `docs/14-product-module-map.md`;
- `docs/23-multi-exchange-adapter-architecture.md`;
- `docs/54-r05-realtime-requirements-addendum.md`;
- `docs/91-r11-integrated-authority-state-dependency-architecture.md`;
- `docs/93-r11-integration-requirements-addendum.md`;
- `docs/99-r12-frozen-requirements-baseline.md`;
- `docs/100-r12-requirements-traceability-and-no-loss-proof.md`;
- `docs/104-chat-delivery-and-prompt-artifact-policy.md`;
- `docs/117-s1a-implementation-approval-and-checkpoint-promotion.md`;
- `docs/118-implementation-authorization-s1b-candidate.md`;
- `docs/119-s1b-implementation-authorization-approval-and-checkpoint-promotion.md`;
- `work-orders/HCT-IMP-0005-S1B.md`;
- authorization Issue #49 and its exact approval evidence;
- implementation Issue #51;
- current S1A implementation/evidence/tests before choosing adapter integration points.

The executor must also consult official MEXC public API documentation for the exact public reference endpoints and fields used. Provider documentation is external evidence, not permission to widen scope.

## REQUIRED ADR
Before substantive product code, add one bounded ADR under `adr/` covering:
- why S1B permits public reference REST but still forbids WebSocket/private/auth/trading paths;
- exact MEXC public endpoints used and why each is in-scope;
- provider payload boundary and canonical translation strategy;
- official-provider source/version/date evidence strategy;
- fixed timeout and response-size policy;
- no automatic retry by default, or a narrowly justified bounded idempotent read retry policy;
- malformed/unknown payload policy and quarantine/evidence behavior;
- unknown capability/rule fail-closed semantics;
- symbol-to-canonical identity mapping rules;
- decimal/precision/rule normalization;
- why Universe, quota governor, realtime ingest and trading remain deferred.

## AUTHORIZED IMPLEMENTATION SCOPE
### A. MEXC public reference transport
Implement the minimal HTTPS client surface needed to retrieve MEXC Futures public reference metadata required by S1A models.

The transport SHALL:
- call only explicitly allowlisted public unauthenticated MEXC reference endpoints;
- use HTTPS only;
- use explicit finite connect/read/total timeout behavior supported by the chosen client;
- enforce bounded response size where practical;
- return structured transport/provider errors rather than uncontrolled exceptions;
- avoid background connections, long-lived sessions, streaming, subscriptions or reconnect loops;
- avoid generic retry/circuit/quota frameworks.

### B. Provider payload boundary
MEXC-specific payload models/parsers may exist only in the adapter/provider boundary. Core HCT domain code SHALL consume S1A canonical models, not MEXC dictionaries or DTOs.

Unknown extra provider fields may be preserved only as bounded diagnostic/evidence metadata when safe and explicitly allowlisted; do not create unrestricted raw-payload tunnels into canonical models.

### C. Exchange descriptor and capability translation
Build the MEXC implementation of the S1A read-only Exchange Reference Adapter sufficient to return:
- MEXC exchange descriptor/reference metadata;
- immutable capability snapshot based only on proven public evidence;
- public contract/reference specifications;
- canonical/native mapping lookup needed by the S1A port.

`UNKNOWN` remains fail closed. Unsupported functionality stays explicit. Do not infer support merely because an enum/capability exists in HCT.

### D. Contract/rule normalization
Map public MEXC contract fields into S1A canonical reference semantics using exact decimal-safe representations.

Reject or degrade on:
- malformed identifiers;
- missing material price/quantity increments;
- zero/negative forbidden increments;
- inconsistent min/max limits;
- unsupported/unrecognized lifecycle/contract types where safe mapping is impossible;
- contradictory public rule fields;
- materially unknown risk/reference rules that later consumers must not treat as proven.

Native MEXC symbol/name is mapping metadata, not sole canonical identity.

### E. Provider evidence and fixture model
Create deterministic fixtures derived from documented provider shapes and direct parser/translation tests.

Tests SHALL NOT require live MEXC availability. If optional live smoke tooling is created for manual developer diagnosis, it must be excluded from CI, disabled by default, explicitly non-authoritative, have no credentials and remain outside runtime/public API paths. Prefer no live smoke tooling in S1B unless objectively necessary.

### F. Bounded result/error semantics
Reuse/extend existing canonical errors only as required for public reference transport/provider mapping, for example:
- reference provider unavailable;
- provider timeout;
- malformed provider response;
- unsupported/unmapped provider contract;
- capability/rule unknown/unproven.

Do not add execution/order/account errors that belong to later slices.

### G. Evidence and exact-head CI
Add S1B-specific tests, static boundary checks and exact-head CI. The implementation PR remains open/unmerged for independent HIGH_ASSURANCE review.

## EXPLICITLY NOT AUTHORIZED
Do not implement:
- MEXC WebSocket client or any streaming socket transport;
- subscription/reconnect/resubscribe/session-generation runtime;
- ticker/trade/candle/order-book realtime ingest;
- funding/open-interest realtime pipeline;
- private/account/order/position/balance REST or stream endpoints;
- API keys, request signing, authentication headers, credential lifecycle or production SecretStore provider;
- order placement/cancel/replace/amend, trigger/TP/SL/trailing, leverage or margin mutation;
- fills, positions, balances, OMS, reconciliation or protection;
- Market Universe eligibility/scanner runtime;
- API Quota, WebSocket & Backpressure Governor runtime;
- Data Quality/Freshness Engine;
- Market-State Fabric, order-book reconstruction or cache/hot-state runtime;
- persistence/database/RLS;
- new public trading API routes;
- frontend trading controls;
- production deployment;
- limited-live;
- real-money trading;
- any later Stage-1 or Stage-2+ capability.

## ARCHITECTURE CONSTRAINTS
1. Core HCT code depends on S1A HCT-owned models/ports, never MEXC payload classes.
2. MEXC-specific code lives behind a dedicated adapter/provider boundary.
3. S1B is public/read-only/unauthenticated.
4. No WebSocket or background streaming path exists.
5. No secret-bearing fields or credential handling exists.
6. No state-changing exchange command API exists.
7. No persistence is required.
8. `UNKNOWN`/unproven provider facts fail closed.
9. Reference/capability metadata does not grant trading authority.
10. Universe/realtime/quota/Data Quality/Market-State remain separate later owners.
11. Existing S0A/S0B/S0C/S1A environment/security/provenance contracts remain authoritative.
12. Official MEXC docs/provider evidence inform mapping but cannot widen the frozen Work Order.

## REQUIRED TEST MATRIX
### Transport boundary
- only allowlisted HTTPS public reference endpoints accepted;
- private/account/order path patterns rejected by construction or explicit allowlist;
- non-HTTPS URL rejected;
- finite timeout configuration proven;
- oversized/malformed/non-JSON critical responses fail closed;
- timeout/provider error maps to bounded canonical failure;
- no background/streaming/WebSocket client path.

### Payload/schema translation
- representative valid MEXC fixture maps deterministically to canonical S1A models;
- unknown extra field does not mutate canonical semantics unless explicitly mapped;
- missing material fields fail closed;
- malformed decimal/precision values reject;
- contradictory min/max/increment data rejects;
- unsupported lifecycle/contract type remains explicit/unavailable;
- provider-native symbol change does not mutate canonical identity.

### Capability/rule resolver
- proven support maps to `SUPPORTED` only when provider evidence exists;
- explicit unsupported maps to `UNSUPPORTED`;
- absent/unproven provider field maps to `UNKNOWN`, never supported;
- materially different provider reference/capability input changes immutable fingerprint/version evidence;
- capability metadata grants no command/trading method.

### Security/negative capability
- no API-key/secret/signature/auth field or header in S1B production code;
- no private endpoint route;
- no WebSocket/socket/subscription/reconnect imports/surfaces;
- no order/leverage/margin mutation methods;
- no market-ingest pipeline;
- no persistence/database adapter;
- no public trading route/frontend control.

### Regression/quality
- full backend suite PASS;
- S0A/S0B/S0C/S1A targeted regressions PASS;
- contract generation/parity PASS;
- frontend regression suite PASS;
- Ruff/format PASS;
- strict mypy PASS;
- backend build PASS;
- frontend typecheck/lint/format/build PASS;
- Python dependency audit PASS with no silently accepted HIGH/CRITICAL known vulnerability;
- npm audit PASS under project threshold;
- lockfile integrity PASS;
- secret scan PASS;
- S1A/S1B unauthorized-capability scans PASS;
- `git diff --check` PASS;
- exact raw-head CI PASS.

Coverage must not regress below the accepted baseline without independent approval. New S1B adapter/parser logic requires focused negative branch coverage.

## REQUIRED STATIC BOUNDARY SCAN
Add or extend deterministic scans that fail closed if S1B production code introduces:
- WebSocket/socket/stream/subscription/reconnect runtime;
- private MEXC routes or account/order/position/balance endpoints;
- auth/signing/API-key/credential fields/headers/functions;
- state-changing order/leverage/margin methods;
- generic external URLs outside explicit MEXC public reference allowlist;
- persistence/database clients;
- deployment configuration;
- later Stage-1 module implementations.

Prefer AST/structured/config-aware checks and explicit endpoint allowlists over naive broad string scans. Tests/documentation fixtures must not create false positives.

## ALLOWED FILE SURFACE
The executor may add/modify only files objectively required for S1B, such as:
- one ADR under `adr/`;
- backend MEXC public reference adapter/provider modules;
- backend tests/fixtures;
- narrowly required dependency/lockfile changes for the chosen HTTPS client only if not already available;
- S1B boundary/validation scripts;
- S1B implementation workflow;
- `evidence/HCT-IMP-0005-S1B.md`.

Canonical S1A contract changes are discouraged and require explicit proof that a frozen requirement cannot be met with the approved S1A models. No checkpoint, frozen planning source, Scope, Decisions Ledger, frontend product feature or unrelated historical workflow may be modified by the executor without governed scope change.

## EVIDENCE ARTIFACT
Create `evidence/HCT-IMP-0005-S1B.md` and record:
- Context Lock / HCT-CP-0023;
- exact execution base;
- ADR and exact official MEXC provider documentation consulted;
- allowlisted public endpoint set and why each is required;
- changed files;
- provider-to-canonical field mapping;
- explicit unknown/deferred fields;
- timeout/response-bound behavior;
- fixture provenance strategy;
- test counts and coverage;
- S0A/S0B/S0C/S1A regressions;
- secret/private-route/WebSocket/order/persistence scans;
- dependency audits and builds;
- limitations/deferred Stage-1 work;
- all production/live flags false.

Do not fabricate passes. Final exact candidate head and hosted run/check IDs belong in PR/Issue handoff after CI rather than a self-referential tracked-file cycle.

## IMPLEMENTATION CI REQUIREMENTS
Create a pull-request-only S1B workflow/check, preferably `s1b-quality`.

It SHALL:
- checkout exact `github.event.pull_request.head.sha`;
- pin/assert the authorized execution base from HCT-CP-0023;
- validate exact S1B scope/ceiling and all higher-risk flags false;
- validate changed-file boundary;
- run S1B endpoint/auth/WebSocket/order/persistence negative scans;
- run full backend tests + coverage, Ruff, strict mypy, build and Python audit;
- run S0A/S0B/S0C/S1A regressions directly;
- run contract generation/parity;
- run frontend regression/build/audit;
- run `git diff --check`;
- require no repository/exchange secrets.

No `workflow_dispatch` may share the same required check identity.

## REVIEW FORMAT
Independent implementation review SHALL report:
- exact base/head;
- Context Lock;
- endpoint allowlist and public-only proof;
- provider-to-canonical mapping correctness;
- UNKNOWN fail-closed behavior;
- auth/signing/private-route absence;
- WebSocket/stream absence;
- order/money-state absence;
- tests/coverage/regressions;
- audits/scans;
- exact-head CI;
- CRITICAL count;
- HIGH count;
- verdict exactly `APPROVED`, `CORRECTION REQUIRED` or `BLOCKED`.

## STOP CONDITION
STOP with the implementation PR OPEN and UNMERGED after exact-head CI/evidence and author-side preflight. Do not self-approve, merge, promote the completion checkpoint, add credentials, connect WebSockets/private APIs, implement trading commands, deploy production, activate limited-live/live trading or begin later Stage-1/Stage-2 work. Fresh independent HIGH_ASSURANCE/HEDS Delta review is mandatory before merge.
