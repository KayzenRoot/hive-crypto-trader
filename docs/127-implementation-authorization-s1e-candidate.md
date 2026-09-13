# HCT-IMPL-AUTH-0008 — S1E Market Truth Foundation Authorization Candidate

Status: `PRE_AUTHORIZATION_REVIEW_REQUIRED`
Risk: `HIGH_ASSURANCE`
Canonical base: `main@a92f1093b36b746ff77daa6d28f1ec4cf12f4fcb`
Current checkpoint: `HCT-CP-0028 / S1D_IMPLEMENTATION_APPROVED_MERGED`
Proposed implementation slice: `HCT-IMP-0008-S1E`
Proposed ceiling: `NON_TRADING_STAGE_1_MARKET_TRUTH_FOUNDATION_ONLY`
Authorization issue: `#64`
Governance branch: `governance/HCT-IMPL-AUTH-0008-S1E`

## Objective

Prepare a governance-only authorization candidate for the smallest necessary next dependency after completed S1D: a provider-neutral Market Truth Foundation covering normalized public market-event contracts, deterministic data-quality/freshness authority, generation-scoped coherent Market-State contracts and cache/hot-state projections.

This candidate does not implement product/runtime code and does not promote an authorization checkpoint. It proves that the proposed future Work Order is bounded, traceable, fail-closed and ready for a separate independent authorization review.

## Why this is the next dependency

The frozen R11 Stage-1 dependency order is:

`Exchange Abstraction + MEXC adapter -> capability/rule resolver -> universe -> quota/WS governor -> market ingest/quality/Market-State/cache`.

S1A, S1B, S1C and S1D are completed under canonical checkpoints. Module 29 now provides resource control, while the next missing dependency is the market truth chain owned by Modules 4, 7, 5 and 30. This candidate does not skip an earlier unfinished dependency and does not collapse later transport, trading or deployment capabilities into S1E.

## Proposed S1E responsibility

The future S1E Work Order may implement only provider-neutral, deterministic control/state contracts for:

- Module 4 normalized immutable public market-event envelopes with stable event identity, environment/generation/provenance binding, source/version fingerprints and explicit event-time, wall-receive-time and monotonic-time separation;
- Module 7 Data Quality/Freshness predicates and reason taxonomy for stale, gap, duplicate, out-of-order, `SEQUENCE_UNPROVABLE`, clock-health, schema/quarantine and cross-channel contradiction evidence;
- Module 5 generation-scoped coherent Market-State snapshot/fabric contracts, synchronization barriers, trust states and explicit rejection of mixed-generation or unproven continuity as trusted truth;
- Module 30 cache/hot-state projection contracts with freshness lease/TTL/invalidation metadata and an explicit no-authority-upgrade invariant;
- typed integration contracts proving that Module 29 quota/backpressure constrains resources and admission but never owns market truth;
- deterministic fixtures/replay inputs, negative-capability scanning, tests and evidence without live MEXC or external network calls.

## Required safety and authority semantics

- Unknown or unproven continuity, freshness, clock health, schema validity or cross-channel coherence fails closed and cannot become trusted market authority through an aggregate score.
- Retired generations cannot mutate the current trusted state.
- Snapshot/delta reconstruction cannot become trusted without explicit synchronization proof where applicable.
- Data Quality is an authority input and explanatory evidence; it is not replaced by a permissive composite confidence score.
- Market-State trust is distinct from raw event receipt, cache presence and UI projection.
- Cache/hot-state entries are projections with freshness leases, provenance and invalidation; they cannot originate or upgrade exchange, account, order, fill or position authority.
- `LIVE`, `PAPER`, `SHADOW` and `REPLAY` environment identity remains explicit in stateful contracts.
- Module 29 may deny/defer/shed resource admission, but it cannot publish market truth or relax Module 7/5 trust barriers.

## Explicitly forbidden

This authorization candidate must not grant:

- concrete MEXC WebSocket/socket/network transport, subscription, reconnect or resubscription I/O;
- new exchange endpoints, provider-host/path expansion or provider-native DTO truth leakage;
- private/account/order/position/balance streams, credentials, authentication or signing;
- order placement/cancel/replace, leverage/margin mutation, Risk, Safety, Session Policy, OMS or Execution authority;
- durable persistence, database/RLS schema, HA deployment topology or production infrastructure;
- market scanner ranking, strategy/Brain/agent authority or trading-signal execution;
- production deployment, limited-live, real-money trading or any next Stage-1 slice;
- checkpoint promotion from CP0028 in this authorization task.

## Authorization firewall

Before separate authorization promotion, canonical authority remains:

- `implementation_authorized=false`;
- `implementation_authorization_scope=[]`;
- `implementation_authorization_ceiling=NONE_PENDING_NEXT_GOVERNED_AUTHORIZATION`;
- `production_credentials_authorized=false`;
- `production_deployment_authorized=false`;
- `limited_live_authorized=false`;
- `live_trading_authorized=false`.

This candidate itself does not change those flags.

## Required proof before any later authorization

- governance-only exact four-file PR with no product/runtime/checkpoint/frozen-requirement/dependency-lock changes;
- canonical main and CP0028 exact match at `a92f1093b36b746ff77daa6d28f1ec4cf12f4fcb`;
- R11 dependency-order proof and Module 4/5/7/29/30 non-overlapping ownership proof;
- direct R05/R11/R12/Decisions Ledger traceability;
- complete S1E implementation Work Order with fail-closed tests, fixtures/replay, scanner and STOP CONDITION;
- pull-request-only exact-head authorization CI success;
- fresh independent HIGH_ASSURANCE/HEDS Delta review with unresolved CRITICAL=0 and HIGH=0.

## Review boundary

This artifact is an authorization candidate only. It is not implementation authorization, independent approval, checkpoint promotion, production deployment authorization, credentials authorization, limited-live authorization or live-trading authorization.

## STOP CONDITION

Keep the authorization PR open and unmerged after exact-head governance CI and author-side preflight. Do not promote CP0028, write S1E product/runtime code, open sockets, connect to a venue, add credentials/private APIs, persist state, deploy or activate limited-live/live trading until a separate independent review and governance acceptance explicitly complete the later authorization process.
