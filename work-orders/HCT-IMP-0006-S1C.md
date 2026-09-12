# HCT-IMP-0006-S1C - Market Universe Registry Foundation

Status: `AUTHORIZED`
Risk class: `HIGH_ASSURANCE`
Parent authorization increment: `HCT-IMPL-AUTH-0006 / COMPLETED_APPROVED`
Planning baseline: `HCT-CP-0014 / PLANNING_FREEZE_APPROVED`
Required pre-execution checkpoint: `HCT-CP-0025 / IMPLEMENTATION_AUTHORIZED_S1C`
Authorization ceiling: `NON_TRADING_STAGE_1_MARKET_UNIVERSE_REGISTRY_ONLY`
Implementation issue: `#58`

## Objective
Implement the Stage-1 Market Universe Registry as the HCT-owned provider-neutral owner of dynamic eligible-contract truth, consuming only completed S1A/S1B exchange reference/capability facts and remaining non-trading.

## Preconditions
Do not execute product-code mutation unless the canonical checkpoint proves exactly `HCT-CP-0025 / IMPLEMENTATION_AUTHORIZED_S1C`, authorizes only `HCT-IMP-0006-S1C`, and all production credentials/deployment/limited-live/live-trading flags are false. Before mutation, synchronize safely and fail closed on any base/head/checkpoint drift.

## Frozen inputs
- S0A typed contracts/identities/environment foundation;
- S0B SecurityContext/tenant-account-environment isolation;
- S0C audit/evidence/version semantics;
- S1A exchange descriptor/capability/contract reference models and fail-closed UNKNOWN semantics;
- S1B bounded MEXC public reference adapter and typed provider-to-canonical translation;
- R11 Stage-1 dependency order and Module-3 ownership.

## Required ADR before substantive code
Create a bounded ADR that records:
- Universe Registry ownership versus ExchangeReferenceAdapter, Quota/WS, Realtime Market Data, Data Quality, Market-State and Market Scanner;
- exact eligibility states and reason-code taxonomy;
- why `ELIGIBLE` means downstream-universe membership only, never trade authorization;
- exact required input references/versions/fingerprints;
- immutable snapshot identity/version/fingerprint semantics;
- recompute/refresh semantics and deterministic ordering;
- fail-closed UNKNOWN policy;
- no realtime/liquidity/ranking criteria in this slice;
- no persistence in this slice.

## Allowed implementation surface
S1C may add a provider-neutral universe domain module and tests plus bounded contract/schema changes only if required by cross-language shared contracts. It may consume the existing read-only ExchangeReferenceAdapter/S1A-S1B reference models.

Required concepts, names may vary if semantics remain exact:
- `UniverseEligibilityState`: `ELIGIBLE`, `INELIGIBLE`, `UNKNOWN`;
- machine-readable eligibility reason codes;
- immutable `UniverseEntry` bound to canonical ContractID and current reference fingerprint/version;
- immutable `UniverseSnapshot` bound to ExchangeID, environment, capability/reference snapshot identities, policy version and observation/recompute time;
- deterministic fingerprint/version evidence;
- deterministic canonical ordering independent of provider payload order;
- a pure/bounded registry/service that recomputes a snapshot from HCT-owned reference inputs.

## Bounded eligibility semantics
Eligibility may depend only on material reference facts already authorized and represented by S1A/S1B, including where applicable:
- exact exchange identity;
- canonical contract identity/native mapping;
- contract lifecycle/reference status;
- supported S1C contract type policy;
- required reference/capability state;
- valid price/quantity increments and required structural rule fields already validated by S1A/S1B.

Rules:
- every mandatory fact must be explicit and version-bound;
- material UNKNOWN/unavailable evidence -> `UNKNOWN`, never `ELIGIBLE`;
- explicit disqualifying fact -> `INELIGIBLE` with deterministic reason code;
- only fully proven structural eligibility -> `ELIGIBLE`;
- an entry may preserve why it is excluded/unknown without leaking provider-native raw payloads;
- no mutable display name/native symbol may replace canonical identity;
- duplicate canonical contracts or contradictory mapping evidence fail closed;
- deterministic input sets produce deterministic snapshots/fingerprints.

## Explicit negative scope
S1C MUST NOT implement or authorize:
- new MEXC endpoint/host/path/client or generic exchange transport;
- WebSocket, subscription, reconnect/resubscribe/session-generation logic;
- API quota/backpressure scheduling/retry/circuit runtime;
- ticker/trade/candle/order-book/funding/open-interest realtime ingest;
- Data Quality/Freshness authority;
- coherent Market-State Fabric or cache/hot-state runtime;
- liquidity/volume/spread/volatility eligibility requiring realtime market data;
- Market Scanner ranking/candidate discovery;
- strategy/signal/regime/features/intelligence;
- credentials/API keys/auth/signing/private/account/order/position/balance APIs;
- order commands, leverage/margin mutation, Risk/Safety/Session/Portfolio/Sizing/OMS/Execution authority;
- persistence/database/RLS;
- frontend trading controls/public trading routes;
- production deployment, limited-live or real-money trading.

## Required tests
### Eligibility state
- fully proven active supported structural contract -> ELIGIBLE;
- inactive/explicitly disallowed structural contract -> INELIGIBLE with reason;
- required capability UNKNOWN -> UNKNOWN;
- required capability UNSUPPORTED -> INELIGIBLE when policy explicitly requires support;
- missing material reference fact -> UNKNOWN/fail closed;
- no bool/default coercion upgrades UNKNOWN.

### Identity/version
- stable canonical contract identity independent of native display changes;
- deterministic snapshot ordering/fingerprint independent of provider list order;
- material reference/capability/policy-version change changes universe fingerprint;
- identical normalized inputs reproduce the same fingerprint;
- duplicate/contradictory canonical mapping fails closed;
- snapshot/entries immutable.

### Boundary
- no network-client/provider endpoint implementation in universe production module;
- no WebSocket/quota/realtime ingest/scanner/ranking/persistence/trading command surfaces;
- provider-native DTO/dict does not cross into universe core;
- no credentials/auth/signing/secret values.

### Regression/quality
- full backend tests and coverage at or above accepted baseline unless separately approved;
- direct S0A/S0B/S0C/S1A/S1B regressions;
- contract generation/parity if contracts change;
- Ruff lint + format check;
- strict mypy;
- backend build;
- Python dependency audit;
- frontend typecheck/tests/lint/generated-format/build/npm audit;
- secret/unauthorized-capability scan;
- `git diff --check`.

## Static S1C boundary scan
Add/extend a deterministic AST/structured scanner that fails on representative production-code violations: new external network clients/URLs/endpoints, WebSocket/stream/subscription/reconnect, quota/backpressure runtime, realtime market ingest vocabulary tied to implementation, scanner/ranking surfaces, credentials/auth/signing, private/account/order state, state-changing commands, persistence/database adapters, deployment/live configuration and changed-file escape.

The scanner must intentionally avoid false positives from docs/tests while remaining strict on production code.

## Evidence artifact
Create `evidence/HCT-IMP-0006-S1C.md` recording exact Context Lock, ADR, changed files, universe state/reason model, input provenance/version bindings, deterministic snapshot evidence, tests/coverage/regressions, contract parity, scans/audits/builds, known limitations/deferred Stage-1 work and all production/live flags false. Do not fabricate PASS results.

## Implementation CI
Create a pull-request-only exact-head workflow, preferably `s1c-quality`, that:
- checks out exact PR head;
- pins the authorized CP0025 execution base;
- verifies exact authorization scope/ceiling and higher-risk flags false;
- validates changed-file boundary;
- runs full backend tests/coverage, direct S0A-S1B regressions, contract parity, Ruff lint+format, mypy, build, Python audit;
- runs S1C boundary/secret scans;
- runs frontend typecheck/tests/lint/format/build/npm audit;
- runs `git diff --check`;
- requires no credentials/secrets and no live external exchange calls;
- exposes no `workflow_dispatch` success path under the same receipt identity.

## Author preflight
Any new network/provider endpoint, WebSocket/quota/realtime ingest, scanner/ranking, credentials/private/trading, persistence, deployment or live capability is BLOCKING. Author handoff is not independent approval.

## Independent review
APPROVED requires exact head/base, bounded diff, deterministic/fail-closed universe semantics, tests/scans/CI, CRITICAL=0 and HIGH=0.

## STOP CONDITION
Stop with the S1C implementation PR OPEN and UNMERGED after fresh exact-head CI and author-side handoff. Do not self-approve, merge, promote completion checkpoint, start quota/WS/realtime work, add credentials, deploy, activate limited-live/live trading, or begin a later slice.
