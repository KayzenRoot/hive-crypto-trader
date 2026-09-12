# HCT-IMPL-AUTH-0005 - S1B Implementation Authorization Candidate

Status: `INDEPENDENT_REVIEW_REQUIRED`
Risk class: `HIGH_ASSURANCE`
Authorization increment: `HCT-IMPL-AUTH-0005`
Issue: `#49`
Candidate implementation slice: `HCT-IMP-0005-S1B`
Canonical base: `main@3ee039deafbfc5505f0b74ce38c721aa384a0953`
Canonical checkpoint: `HCT-CP-0022 / S1A_IMPLEMENTATION_APPROVED_MERGED`
Proposed post-approval checkpoint: `HCT-CP-0023 / IMPLEMENTATION_AUTHORIZED_S1B`

## Purpose
Evaluate whether exactly one bounded Stage-1 concrete-exchange slice may be authorized after the independently approved S1A provider-neutral exchange reference foundation.

This candidate grants no product-code authority until a separate HIGH_ASSURANCE execution stream independently reviews the exact candidate head, exact-head authorization governance succeeds on that same head, the authorization PR is governed-merged, and a checkpoint promotion explicitly authorizes only `HCT-IMP-0005-S1B`.

## Current authoritative state
At `HCT-CP-0022`:
- `implementation_authorized=false`
- `implementation_authorization_scope=[]`
- `implementation_authorization_ceiling="NONE_PENDING_NEXT_GOVERNED_AUTHORIZATION"`
- `production_credentials_authorized=false`
- `production_deployment_authorized=false`
- `limited_live_authorized=false`
- `live_trading_authorized=false`

Planning remains frozen under `HCT-CP-0014`. S0A, S0B, S0C and S1A are independently approved and merged. No further Stage-1 product-code mutation is authorized.

## Why S1B is the next bounded dependency
R11 Stage 1 is `Exchange and realtime truth` and orders:
- Exchange Abstraction + MEXC adapter;
- capability/rule resolver;
- universe;
- quota/WS governor;
- market ingest, quality, Market-State Fabric and cache.

S1A completed the HCT-owned provider-neutral exchange abstraction, immutable capability model and contract/reference specification while deliberately stopping before concrete venue networking.

The smallest remaining dependency before Universe and realtime work is therefore a concrete MEXC adapter restricted to public, read-only reference/capability discovery. This lets later modules consume real MEXC contract/rule evidence through S1A canonical models without introducing private credentials, WebSockets, market streams, order commands or money-state authority.

This ordering preserves `HCT-DEC-0023`, `docs/23-multi-exchange-adapter-architecture.md`, Module 2 in `docs/14-product-module-map.md`, and the R11 Stage-1 dependency DAG.

## Frozen source alignment
Direct requirement locators:
- `REQ02::Market and exchange requirements::B1` - REST is appropriate for reference paths while realtime streams prefer WebSocket later;
- `REQ02::Market and exchange requirements::B2` - discover contract capabilities and constraints dynamically where exposed;
- `REQ02::Market and exchange requirements::B5` - exchange restrictions/API changes are versioned external dependencies;
- `REQ02::Market and exchange requirements::B7` - core modules depend on HCT-owned canonical exchange/domain interfaces;
- `REQ02::Market and exchange requirements::B8` - MEXC is the first concrete exchange adapter;
- `REQ02::Market and exchange requirements::B9` - explicit capability matrix with visible reject/degrade behavior;
- `R11-REQ-006` - canonical source-of-truth ownership;
- `R11-REQ-012` - typed identity/version registry;
- `R11-REQ-013` - explicit failure/degradation propagation;
- `R11-REQ-014` - implementation follows the dependency DAG;
- `R11-REQ-024` - provider/topology neutrality where applicable.

Supporting architecture sources:
- `docs/14-product-module-map.md` Modules 1, 2 and 3;
- `docs/23-multi-exchange-adapter-architecture.md`;
- `docs/54-r05-realtime-requirements-addendum.md` for later transport/realtime boundary awareness;
- `docs/91-r11-integrated-authority-state-dependency-architecture.md` Stage 1, Source-of-Truth Matrix, realtime boundaries and identity registry;
- `docs/117-s1a-implementation-approval-and-checkpoint-promotion.md`.

R05 WebSocket/session-generation/backpressure/realtime requirements remain binding for later slices, but S1B does not claim to implement them.

## Proposed authorization
After independent approval, governed merge and checkpoint promotion, authorize exactly:

`HCT-IMP-0005-S1B - MEXC Public Reference Adapter & Capability/Rule Resolver`

Proposed ceiling:

`NON_TRADING_STAGE_1_MEXC_PUBLIC_REFERENCE_CAPABILITY_RESOLVER_ONLY`

## Proposed S1B scope
### 1. Public MEXC reference transport only
Implement a concrete MEXC Futures adapter behind the S1A read-only Exchange Reference Adapter boundary using only public, unauthenticated reference REST endpoints required to obtain exchange descriptor, contract specifications, lifecycle/reference metadata and publicly exposed capability/rule facts.

No private endpoint, API key, request signature, account identity, WebSocket or exchange state-changing command is permitted.

### 2. Canonical translation
Translate MEXC-native public reference payloads into the existing HCT-owned S1A models. MEXC payload classes/dictionaries may exist only at the adapter boundary and must not leak into core HCT domain contracts.

Native symbol strings remain mapping metadata, never sole canonical identity.

### 3. Capability/rule resolver
Resolve only capabilities/rules that are explicitly proven by public MEXC reference evidence. Unsupported and unknown facts remain explicit. Absence of proof must not be upgraded to supported.

This resolver describes exchange capability/reference truth only. It grants no Security, Risk, Execution or trading authority.

### 4. Strict payload validation
Unknown, malformed or internally inconsistent critical reference payloads fail closed and produce bounded canonical unavailable/malformed/unknown results. No permissive guessing of price/quantity increments, lifecycle state, leverage/risk rules or contract identity is allowed.

### 5. Network boundary
S1B may introduce only the minimal outbound HTTPS client surface needed for public reference reads, with explicit fixed timeout and bounded response-size/schema handling. It must not introduce a general retry engine, connection pool governor, rate-limit scheduler, circuit runtime, WebSocket engine or session-generation subsystem; those belong to later Stage-1 slices.

Automatic retries should be absent unless the implementation Work Order proves a narrowly bounded idempotent single-read policy that does not become a shadow quota/resilience subsystem.

### 6. Deterministic fixtures and provider evidence
Tests must use deterministic fixtures/mocked transport and must not require live MEXC availability. Implementation evidence must identify the official MEXC public documentation/provider source used to map the supported reference fields and explicitly list unknown/deferred fields.

### 7. Proof and regression
Implementation must prove that concrete MEXC reference connectivity remains public/read-only/non-trading and does not introduce private credentials, streaming, market ingest, money-state or state-changing exchange authority. S0A/S0B/S0C/S1A guarantees remain green.

## Explicitly out of scope
S1B SHALL NOT implement or authorize:
- MEXC WebSocket or any streaming transport;
- market trades/ticker/candle/order-book realtime ingest;
- funding/open-interest realtime engine;
- private/account/order/position/balance endpoints or streams;
- API keys, request signing, authentication, credential lifecycle or production SecretStore provider;
- order placement/cancel/replace, triggers, TP/SL, trailing, leverage/margin mutation or any exchange command;
- fills, positions, balances, OMS, reconciliation or protection;
- Market Universe eligibility/scanner runtime beyond a later consumer of S1B references;
- API Quota/WS/Backpressure Governor runtime;
- reconnect/resubscribe/session-generation logic;
- Data Quality/Freshness Engine;
- coherent Market-State Fabric, order-book reconstruction or cache/hot state;
- persistent reference database/RLS;
- public trading API routes or frontend trading controls;
- production deployment;
- limited-live or real-money trading;
- later Stage-1 slices or Stage 2+ implementation.

## Proof obligations
An implementation candidate under this authorization SHALL prove at minimum:
1. Concrete MEXC adapter implements only the existing read-only S1A reference port or a strictly compatible refinement approved by the Work Order.
2. No MEXC transport/payload type leaks into canonical core HCT models.
3. Only public unauthenticated HTTPS reference endpoints are reachable from S1B production code.
4. No credential, API-key, signing, private-route or account-state code path exists.
5. No WebSocket, socket stream, subscription, reconnect or realtime ingest path exists.
6. No order/leverage/margin or other state-changing exchange command surface exists.
7. Contract/rule mapping is decimal-safe, deterministic and fail-closed on malformed/inconsistent data.
8. Unknown or unproven capability/rule state remains `UNKNOWN`/unavailable rather than supported/permissive.
9. Canonical identity remains independent from mutable MEXC native symbol/display fields.
10. Official-provider field mapping and deferred/unknown facts are evidenced; tests use deterministic fixtures/mocked transport rather than live-network dependence.
11. Network timeouts/response bounds are explicit and cannot become unbounded waits/resource consumption.
12. S1B does not implement Universe eligibility, quota governor, WebSocket, Data Quality, Market-State Fabric or cache runtime.
13. S1B introduces no persistence, Risk/OMS/Execution authority, production deployment or live-trading enablement.
14. S0A/S0B/S0C/S1A regressions, contract generation/parity, secret scans and boundary scans remain green.
15. Static scans fail closed on unauthorized private/auth/signing/WebSocket/order/persistence capability additions.
16. Exact raw-head implementation CI succeeds before independent implementation review.
17. Fresh independent HIGH_ASSURANCE review returns `APPROVED` with unresolved CRITICAL=0 and HIGH=0 before merge.

## Proposed post-approval flags
Only after a later checkpoint promotion:
- `implementation_authorized=true`
- `implementation_authorization_scope=["HCT-IMP-0005-S1B"]`
- `implementation_authorization_ceiling="NON_TRADING_STAGE_1_MEXC_PUBLIC_REFERENCE_CAPABILITY_RESOLVER_ONLY"`
- `production_credentials_authorized=false`
- `production_deployment_authorized=false`
- `limited_live_authorized=false`
- `live_trading_authorized=false`

Authorization of public MEXC reference reads does not authorize streaming, private APIs, trading commands or production/live activation.

## Independent review requirements
The reviewer SHALL reconstruct the verdict from repository evidence and verify:
- exact PR base/head identity;
- canonical `HCT-CP-0022` fail-closed state;
- S1A completion provenance and provider-neutral boundary;
- R11 Stage-1 ordering from S1A into the concrete MEXC reference dependency before Universe/realtime work;
- all direct frozen locators listed above;
- public/read-only/unauthenticated scope;
- no WebSocket/private/auth/signing/order/money-state implementation authority;
- implementation Work Order completeness, negative tests, evidence obligations and STOP CONDITION;
- exact-head authorization-governance CI success;
- zero unresolved CRITICAL/HIGH findings.

Verdict exactly one of:
- `APPROVED`
- `CORRECTION REQUIRED`
- `BLOCKED`

## STOP CONDITION
Do not begin product implementation from this document. Keep the authorization PR open and unmerged until exact-head authorization-governance CI succeeds and a separate HIGH_ASSURANCE/HEDS Delta execution stream publishes its verdict for the exact head. Merge/promotion may authorize only `HCT-IMP-0005-S1B`. No WebSocket/private exchange connectivity, production credentials, production deployment, limited-live or live trading are authorized by this candidate.
