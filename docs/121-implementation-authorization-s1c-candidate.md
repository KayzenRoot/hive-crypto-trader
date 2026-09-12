# HCT-IMPL-AUTH-0006 — S1C Implementation Authorization Candidate

Status: `PRE_AUTHORIZATION_REVIEW_REQUIRED`
Risk: `HIGH_ASSURANCE`
Canonical base: `main@cbd0208e05cd875582902a692167230b7a0ac20c`
Current checkpoint: `HCT-CP-0024 / S1B_IMPLEMENTATION_APPROVED_MERGED`
Proposed implementation slice: `HCT-IMP-0006-S1C`
Proposed ceiling: `NON_TRADING_STAGE_1_MARKET_UNIVERSE_REGISTRY_ONLY`
Authorization issue: `#56`

## Why this is the next dependency
The frozen R11 implementation DAG orders Stage 1 as:
`Exchange Abstraction + MEXC adapter -> capability/rule resolver -> universe -> quota/WS governor -> market ingest/quality/Market-State/cache`.

S1A completed the provider-neutral exchange reference foundation. S1B completed the bounded MEXC public reference/capability resolver. Module 3, Market Universe Registry, is `V1_CORE` and owns dynamic eligible-contract truth. Therefore the next bounded dependency is the universe registry, not WebSocket/quota/realtime ingest.

## Proposed S1C responsibility
S1C may implement only a provider-neutral Market Universe Registry that consumes already-authorized S1A/S1B HCT-owned exchange reference truth and produces immutable/versioned universe snapshots.

Allowed:
- typed/stable UniverseSnapshot/UniverseEntry identities where needed;
- explicit `ELIGIBLE`, `INELIGIBLE`, `UNKNOWN` eligibility semantics;
- deterministic machine-readable reason codes;
- exact exchange/environment/reference-snapshot binding;
- immutable/versioned/fingerprinted universe snapshots;
- deterministic eligibility derived only from completed S1A/S1B contract/reference/capability facts;
- fail-closed treatment of missing/unknown material facts;
- canonical/native symbol mapping preservation;
- deterministic refresh/recompute from a supplied/read-only ExchangeReferenceAdapter snapshot boundary;
- tests, evidence, static boundary scanning and exact-head CI.

## Eligibility boundary
S1C is reference-eligibility only. It may decide whether a contract is structurally eligible for downstream Stage-1/Stage-2 consumers based on authoritative contract/reference facts already available from S1A/S1B, such as exchange identity, canonical contract identity, lifecycle, supported contract type, required reference capabilities and valid contract-rule fields.

`UNKNOWN` required eligibility evidence must never become `ELIGIBLE` by fallback/default.

The Universe Registry is not a trading authority. `ELIGIBLE` means only that the contract belongs to the current downstream-consumer universe under the bounded universe policy. It does not mean safe-to-trade, liquid, fresh, promoted, risk-approved or live-authorized.

## Explicitly forbidden
This authorization MUST NOT allow:
- any new MEXC endpoint, generic transport client or provider DTO leakage into universe core;
- WebSocket, subscriptions, reconnect/resubscribe/session generation;
- API quota/backpressure governor runtime;
- ticker/trade/candle/order-book/funding/open-interest realtime ingest;
- liquidity/volume/spread/volatility/ranking filters requiring realtime market data;
- Market Scanner candidate discovery/ranking;
- Data Quality/Freshness or Market-State Fabric authority;
- credentials, API keys, signing, auth headers, private/account/order/position/balance APIs;
- order placement/cancel/replace, leverage/margin mutation or any trading command;
- Safety/Session/Risk/Portfolio/Sizing/OMS/Execution authority;
- persistence/database/RLS;
- production deployment;
- limited-live or real-money trading;
- later Stage-1/Stage-2+ implementation.

## Authorization firewall
Before promotion, canonical authority remains fail closed:
- `implementation_authorized=false`
- `implementation_authorization_scope=[]`
- `implementation_authorization_ceiling="NONE_PENDING_NEXT_GOVERNED_AUTHORIZATION"`
- `production_credentials_authorized=false`
- `production_deployment_authorized=false`
- `limited_live_authorized=false`
- `live_trading_authorized=false`

If independently approved and merged, a separate CP0025 promotion may authorize exactly `HCT-IMP-0006-S1C` under `NON_TRADING_STAGE_1_MARKET_UNIVERSE_REGISTRY_ONLY`.

## Required proof before authorization
- governance-only exact four-file PR;
- current `main` and CP0024 exact match;
- R11 Stage-1 dependency order proves universe is next;
- Module 3 remains `V1_CORE / dynamic eligible-contract truth`;
- S1B completion is canonical and independently approved;
- Work Order has deterministic tests, negative-scope scanner, evidence and STOP CONDITION;
- exact-head pull-request-only authorization CI success;
- independent HIGH_ASSURANCE review with unresolved CRITICAL=0 and HIGH=0.

## STOP CONDITION
This candidate and its PR do not authorize product-code mutation. Keep the authorization PR open/unmerged until exact-head CI and independent HIGH_ASSURANCE review approve the exact candidate head.