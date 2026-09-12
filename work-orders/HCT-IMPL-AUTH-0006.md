# HCT-IMPL-AUTH-0006 — Authorize S1C Market Universe Registry

Status: `PRE_AUTHORIZATION_REVIEW_REQUIRED`
Risk class: `HIGH_ASSURANCE`
Issue: `#56`
Canonical base: `main@cbd0208e05cd875582902a692167230b7a0ac20c`
Current checkpoint: `HCT-CP-0024 / S1B_IMPLEMENTATION_APPROVED_MERGED`
Proposed implementation slice: `HCT-IMP-0006-S1C`

## Objective
Prepare and independently review the bounded authorization package for the next frozen R11 Stage-1 dependency: Market Universe Registry.

## Source hierarchy
Checkpoint/current state -> Decisions Ledger/ADRs -> Scope -> DoD -> Architecture -> frozen requirements -> R11 dependency/classification artifacts -> prior approved implementation/completion evidence -> this Work Order.

## Required source proofs
- `checkpoints/workstreams/planning/latest.json` is CP0024 and fail closed;
- `docs/91-r11-integrated-authority-state-dependency-architecture.md` Stage 1 places `universe` after exchange adapter/capability resolver and before quota/WS/realtime ingest;
- `docs/14-product-module-map.md` Module 3 defines Market Universe Registry as dynamic discovery of futures contracts exposed and eligible through the active exchange adapter;
- `docs/92-r11-v1-module-classification-and-integration-hardening.md` classifies Module 3 as `V1_CORE` and dynamic eligible-contract truth;
- `docs/93-r11-integration-requirements-addendum.md` R11-REQ-014 requires implementation to follow the logical dependency DAG;
- S1B is completed under CP0024.

## Authorization package boundary
Exactly four files may be introduced by this authorization candidate:
- `docs/121-implementation-authorization-s1c-candidate.md`
- `work-orders/HCT-IMPL-AUTH-0006.md`
- `work-orders/HCT-IMP-0006-S1C.md`
- `.github/workflows/implementation-authorization-s1c-governance.yml`

No product/runtime/checkpoint/frozen-planning/dependency-lock/frontend mutation is permitted in the authorization PR.

## Proposed authorization
If independently approved and merged, a separate checkpoint promotion may set:
- `implementation_authorized=true`
- `implementation_authorization_scope=["HCT-IMP-0006-S1C"]`
- `implementation_authorization_ceiling="NON_TRADING_STAGE_1_MARKET_UNIVERSE_REGISTRY_ONLY"`
- all production credentials/deployment/limited-live/live-trading flags remain false.

## Negative-scope firewall
The candidate must not authorize new network/provider endpoints, WebSocket, quota/backpressure runtime, realtime market ingest, liquidity/ranking filters, scanner candidate discovery, private/auth/credentials, trading commands, Risk/OMS/Execution, persistence, deployment or live trading.

## Required gate
The authorization workflow must be pull-request-only, checkout exact PR head, pin canonical base, assert CP0024 fail-closed state, verify R11 dependency/classification source markers, enforce exactly four governance files, validate Work Order/STOP/negative-scope markers and run `git diff --check`.

## Independent review
APPROVED requires exact base/head/main, governance-only diff, source/dependency order, bounded S1C scope, complete implementation Work Order, exact-head hosted gate and unresolved CRITICAL=0/HIGH=0.

## STOP CONDITION
Stop with the authorization PR OPEN and UNMERGED after exact-head hosted evidence and independent review. Do not promote CP0025 or begin S1C product code in this Work Order.