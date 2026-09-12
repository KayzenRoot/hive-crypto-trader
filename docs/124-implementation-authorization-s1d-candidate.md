# HCT-IMPL-AUTH-0007 — S1D Implementation Authorization Candidate

Status: `PRE_AUTHORIZATION_REVIEW_REQUIRED`
Risk: `HIGH_ASSURANCE`
Canonical base: `main@c9462c09523779921cc1cea48018d8d38d103275`
Current checkpoint: `HCT-CP-0026 / S1C_IMPLEMENTATION_APPROVED_MERGED`
Proposed implementation slice: `HCT-IMP-0007-S1D`
Proposed ceiling: `NON_TRADING_STAGE_1_QUOTA_WS_BACKPRESSURE_GOVERNOR_FOUNDATION_ONLY`
Authorization issue: `#60`

## Why this is the next dependency
The frozen R11 Stage-1 implementation DAG orders:
`Exchange Abstraction + MEXC adapter -> capability/rule resolver -> universe -> quota/WS governor -> market ingest/quality/Market-State/cache`.

S1A, S1B and S1C are completed and independently approved. Module 29, **API Quota, WebSocket & Backpressure Governor**, owns exchange request/subscription budgets, priority scheduling, retry/circuit policy and deterministic load shedding. It explicitly does not own market prices or account truth. Therefore the next bounded dependency is a provider-neutral quota/session/backpressure foundation, not realtime market-data ingestion.

## Proposed S1D responsibility
S1D may implement only provider-neutral deterministic control-state/contracts needed by later transport slices:
- typed request/subscription budget descriptors and immutable budget snapshots;
- finite priority classes and deterministic admission/scheduling decisions;
- explicit retry budgets and circuit states;
- local session/WebSocket generation identity and retired-generation suppression semantics as pure state/contracts;
- deterministic subscription-plan/intention objects, with no actual network subscription;
- bounded queue/backpressure state and deterministic load-shedding decisions;
- finite machine-readable reason codes and evidence/fingerprints;
- monotonic/elapsed-time-aware budget semantics where applicable;
- tests, evidence, static negative-scope scanning and exact-head CI.

## Required safety semantics
- Unknown or missing quota/capability evidence fails closed; it cannot become permissive capacity.
- Safety-critical/reserved priority cannot be silently consumed by lower classes.
- Retry budgets are finite; exhaustion is explicit and never converted to unlimited retry.
- Circuit states are explicit and deterministic.
- Retired session generations cannot mutate current-session control state.
- Shedding/admission outcomes are deterministic for equal normalized inputs.
- Governor outputs are control decisions/intents only; they do not become market-price, account, order, Risk or Execution truth.

## Explicitly forbidden
This authorization MUST NOT allow:
- actual WebSocket/socket/network connection creation;
- MEXC or other venue subscribe/unsubscribe calls;
- reconnect/resubscribe loops performing network I/O;
- new exchange REST endpoints or generic transport/client expansion;
- realtime ticker/trade/candle/order-book/funding/open-interest ingest;
- snapshot/delta reconstruction or trusted Market-State publication;
- Data Quality/Freshness ownership;
- Market Scanner/ranking/candidate discovery;
- raw provider DTO leakage into the governor core;
- credentials, API keys, authentication/signing or private/account/order/position/balance APIs/streams;
- order placement/cancel/replace, leverage/margin mutation or trading authority;
- Safety/Risk/Portfolio/Sizing/OMS/Execution authority;
- persistence/database/RLS;
- production deployment, limited-live or real-money trading;
- any later Stage-1/Stage-2 implementation slice.

## Authorization firewall
Before promotion, canonical authority remains fail closed:
- `implementation_authorized=false`
- `implementation_authorization_scope=[]`
- `implementation_authorization_ceiling="NONE_PENDING_NEXT_GOVERNED_AUTHORIZATION"`
- `production_credentials_authorized=false`
- `production_deployment_authorized=false`
- `limited_live_authorized=false`
- `live_trading_authorized=false`

If independently approved and merged, a separate checkpoint promotion may authorize exactly `HCT-IMP-0007-S1D` under `NON_TRADING_STAGE_1_QUOTA_WS_BACKPRESSURE_GOVERNOR_FOUNDATION_ONLY`.

## Required proof before authorization
- governance-only exact four-file PR;
- canonical `main` and CP0026 exact match;
- S1C completion provenance is canonical and independently approved;
- R11 proves quota/WS governor is next;
- Module 29 ownership does not include market prices/account truth;
- Work Order has deterministic state/admission/retry/circuit/generation/backpressure tests, negative-scope scanner, evidence and STOP CONDITION;
- exact-head pull-request-only authorization CI success;
- independent HIGH_ASSURANCE review with unresolved CRITICAL=0 and HIGH=0.

## STOP CONDITION
This candidate does not authorize product-code mutation. Keep the authorization PR open/unmerged until exact-head CI and independent HIGH_ASSURANCE review approve the exact candidate head. No product implementation may begin before a separate checkpoint promotion activates S1D.