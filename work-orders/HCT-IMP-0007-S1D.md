# HCT-IMP-0007-S1D — API Quota, Session Generation & Backpressure Governor Foundation

Status: `PENDING_SEPARATE_AUTHORIZATION_CHECKPOINT`
Risk: `HIGH_ASSURANCE`
Prerequisite: a future checkpoint explicitly authorizing only this Work Order under `NON_TRADING_STAGE_1_QUOTA_WS_BACKPRESSURE_GOVERNOR_FOUNDATION_ONLY`.

## Objective
Implement a provider-neutral, deterministic quota/session/backpressure control foundation required before actual realtime transport and market-data ingestion. S1D owns bounded control decisions and evidence only. It does not create sockets, subscribe to venues, ingest market data, own market prices/account truth, persist state, trade, deploy or activate live authority.

## Frozen dependencies
- S0A/S0B/S0C foundations.
- S1A exchange/capability/reference abstractions.
- S1B bounded MEXC public-reference truth.
- S1C Market Universe Registry structural truth.
- R11 Stage-1 dependency order.
- Module 29 ownership: request/subscription budgets, priority scheduling, retries/circuits and deterministic load shedding; no market-price/account truth ownership.
- R05 requirements for generation identity, retired-generation suppression, bounded retry/backoff/circuits, priority queues and deterministic shedding.

## Required ADR before substantive code
Create one bounded ADR defining:
- governor ownership and boundaries;
- request/subscription budget model and units;
- immutable/versioned budget-policy snapshots and fingerprints;
- priority classes and reserved-capacity semantics;
- admission outcome taxonomy;
- bounded queue/backpressure semantics;
- retry-budget and circuit-state transitions;
- local session-generation identity and retirement semantics;
- subscription plan/intention objects versus actual transport;
- monotonic elapsed-time semantics for windows/ages where applicable;
- deterministic load-shedding policy;
- why actual network/WebSocket/realtime ingestion is deferred.

## Required domain model
Use provider-neutral immutable types. Exact names may differ if semantics are equivalent.

### Budget policy / snapshot
Represent explicit limits for request and subscription control. Required characteristics:
- positive, typed capacities/limits;
- explicit window or replenishment semantics where applicable;
- source/version/policy fingerprint evidence;
- UNKNOWN/unproven capacity remains fail closed and cannot become permissive capacity;
- no provider-native raw DTO/dict as core truth.

### Priority classes
Use a finite enum and deterministic ordering. Preserve higher-priority/reserved capacity from lower classes. The bounded foundation should support concepts equivalent to:
- EMERGENCY/PROTECTION or reserved safety-critical class;
- RECONCILIATION/ACTIVE_POSITION/EXECUTION_CRITICAL intent classes where planning requires reserve semantics;
- NORMAL/REFERENCE;
- SCANNER/RESEARCH or low-priority disposable work.
S1D does not implement the downstream systems represented by these labels; it only provides deterministic priority semantics.

### Admission outcome
Finite machine-readable result, equivalent to:
- ADMIT
- DEFER
- SHED
- CIRCUIT_OPEN
- UNKNOWN/BLOCKED_EVIDENCE
Each result must carry deterministic reason codes and must not execute network work itself.

### Retry budget / circuit
- finite retry count and elapsed-time budget;
- explicit exhaustion;
- deterministic circuit states such as CLOSED/OPEN/HALF_OPEN where justified;
- no infinite retry;
- no network reconnect loop in S1D;
- transitions are pure/state-machine decisions driven by typed inputs/time evidence.

### Session generation
- local typed generation identity for a future WebSocket connection/reconnection;
- monotonically ordered or otherwise deterministic generation semantics without requiring persistence;
- retired generation is explicit and cannot be treated as current;
- generation comparison/rejection is pure control logic only;
- no actual WebSocket connection object/handle.

### Subscription plan intents
Represent immutable requested/accepted/deferred subscription intents with canonical contract/channel identifiers only. They are plans, not executable subscribe/unsubscribe operations.

### Backpressure / queue state
- bounded queue capacity/state snapshots;
- priority-aware deterministic admission and shedding;
- reserve protection for safety-critical class;
- queue saturation never silently becomes unbounded buffering;
- stale/expired low-priority work may be rejected/shed when typed expiry evidence is available;
- no market payload processing is required.

## Time semantics
Use monotonic elapsed-time inputs for retry/window/age decisions wherever wall-clock rollback could violate correctness. Wall timestamps may be metadata, but must not be the sole basis for elapsed-time safety decisions. Tests must be deterministic by supplying typed time/elapsed evidence; do not sleep in tests.

## Fail-closed semantics
- unknown/missing required budget evidence -> UNKNOWN/BLOCKED or DEFER, never ADMIT;
- exhausted budget -> DEFER/SHED according to explicit policy;
- open circuit -> no admission for governed class except explicitly modeled probe semantics;
- retired session generation -> reject/ignore control mutation;
- lower priority cannot consume protected reserve;
- equal normalized inputs produce equal decision/reason output.

## Hard negative scope
Blocking violations:
- `httpx`, `requests`, `aiohttp`, socket/WebSocket client creation in S1D production code;
- actual connect/subscribe/unsubscribe/reconnect/resubscribe network I/O;
- MEXC endpoint/path/host additions or provider DTO parsing;
- realtime ticker/trade/candle/order-book/funding/open-interest ingest;
- snapshot/delta book reconstruction;
- Data Quality/Freshness or Market-State ownership;
- market-price or account-truth publication;
- Market Scanner ranking/candidate discovery;
- credentials/API keys/auth/signing/private APIs;
- order/trading/Risk/OMS/Execution authority;
- persistence/database/RLS;
- production deployment, limited-live or real-money trading.

## Required tests
At minimum:
- exact capacity admission and off-by-one boundaries;
- UNKNOWN/missing quota evidence fails closed;
- lower-priority work cannot consume protected reserve;
- priority ordering deterministic under saturation;
- queue full causes deterministic DEFER/SHED, not unbounded growth;
- retry budget exhaustion;
- circuit CLOSED -> OPEN -> bounded HALF_OPEN/probe semantics if implemented;
- open circuit denies ordinary admission;
- session generation rollover creates a new current generation;
- retired generation cannot mutate current control state;
- stale generation comparison is deterministic;
- subscription intent is immutable and contains no network handle/callback;
- identical normalized inputs yield identical fingerprints/decisions;
- material policy/budget change changes fingerprint;
- invalid zero/negative capacities reject;
- malformed priority/circuit/generation inputs reject;
- no network/socket/WebSocket imports or executable transport calls;
- no exchange endpoint/provider DTO leakage;
- no market ingest/trading/persistence/deployment surfaces;
- full S0A/S0B/S0C/S1A/S1B/S1C regressions;
- backend coverage remains at or above accepted baseline unless separately governed;
- frontend regression suite even if unchanged;
- contract generation/parity if shared schemas change;
- Ruff lint/format, strict mypy, build, dependency audits and `git diff --check`.

## Static boundary scanner
Create/extend an AST/structured S1D scanner that fails closed on production-code introduction of:
- network/WebSocket/socket clients;
- endpoint/URL/host literals and provider routes;
- subscribe/unsubscribe/connect/reconnect calls tied to I/O;
- realtime market payload/ingest surfaces;
- credentials/auth/signing/private exchange concepts in executable constructs;
- trading/order/Risk/Execution methods;
- persistence/database adapters;
- deployment/live configuration;
- changed paths outside the authorized S1D surface.
Tests/docs/fixtures must be handled intentionally to avoid weakening production checks.

## Evidence artifact
Create `evidence/HCT-IMP-0007-S1D.md` containing:
- exact Context Lock/checkpoint/base;
- ADR;
- changed-file inventory;
- budget/priority/admission/retry/circuit/generation/backpressure model;
- deterministic fingerprint/time semantics;
- focused and full test counts/coverage;
- prior-stage regressions;
- contract parity;
- lint/format/mypy/build/audits;
- boundary/secret scans;
- frontend regression results;
- known limitations/deferred actual transport/realtime work;
- all production/live flags false.
Final PR head/run IDs remain in PR/Issue handoff to avoid tracked self-reference.

## Implementation CI
Create one pull-request-only exact-head workflow, preferably `s1d-quality`, that:
- checks out exact PR raw head;
- pins the future authorized execution base;
- asserts exact future authorization checkpoint/scope/ceiling and all higher-risk flags false;
- has no `workflow_dispatch` under the same receipt identity;
- validates changed-file boundary;
- runs full backend tests/coverage and direct prior-stage regressions;
- runs focused S1D state-machine/backpressure tests;
- runs contract generation/parity as applicable;
- runs Ruff lint/format, strict mypy, build, Python audit;
- runs S1D boundary/secret scan;
- runs frontend typecheck/tests/lint/generated format/build/npm audit;
- runs `git diff --check`;
- requires no exchange credentials/secrets and performs no live external exchange calls.

## Author preflight
Review the complete candidate diff. Any actual network/WebSocket connection, provider endpoint, market-data ingest, account/private access, trading authority, persistence, deploy or live capability is BLOCKING.

## Independent review
Final implementation PR requires fresh independent HIGH_ASSURANCE/HEDS Delta review on the exact head. APPROVED requires unresolved CRITICAL=0 and HIGH=0 plus exact-head hosted evidence.

## STOP CONDITION
STOP with the future S1D implementation PR OPEN and UNMERGED after fresh exact-head CI and author-side handoff. Do not self-approve, merge, promote completion, open sockets, subscribe to venues, ingest realtime market data, add credentials/private APIs, trade, persist state, deploy or activate limited-live/live trading.