# HCT-IMPL-AUTH-0007 — Authorize S1D Quota/WS Backpressure Governor Foundation

Status: `AUTHORIZATION_CANDIDATE`
Risk: `HIGH_ASSURANCE`
Authorization issue: `#60`
Canonical execution base: `main@c9462c09523779921cc1cea48018d8d38d103275`
Prerequisite checkpoint: `HCT-CP-0026 / S1C_IMPLEMENTATION_APPROVED_MERGED`
Candidate slice: `HCT-IMP-0007-S1D`
Candidate ceiling: `NON_TRADING_STAGE_1_QUOTA_WS_BACKPRESSURE_GOVERNOR_FOUNDATION_ONLY`

## Objective
Authorize, but do not implement, the next bounded R11 Stage-1 dependency: a provider-neutral API quota, session-generation and backpressure governor foundation. The authorization must not open actual WebSocket/network connectivity or realtime market-data ingestion.

## Source lock
Use canonical source hierarchy. Required locators include:
- `checkpoints/workstreams/planning/latest.json`
- `checkpoints/history/HCT-CP-0026.json`
- `docs/11-checkpoint.md`
- `docs/10-decisions-ledger.md`
- `docs/14-product-module-map.md` Module 29
- `docs/54-r05-realtime-requirements-addendum.md`
- `docs/91-r11-integrated-authority-state-dependency-architecture.md`
- `docs/93-r11-integration-requirements-addendum.md`
- `docs/123-s1c-implementation-approval-and-checkpoint-promotion.md`
- `work-orders/HCT-IMP-0007-S1D.md`

## Preconditions
- `main` must equal `c9462c09523779921cc1cea48018d8d38d103275` during this authorization review.
- CP0026 must be fail closed with no implementation authorization open.
- S1C must be completed and independently approved.
- No product code may change in this authorization PR.

## Authorization candidate requirements
The candidate must prove that S1D is the next dependency and that its Work Order is executable, deterministic and fail closed. It may authorize only pure/provider-neutral quota/session/backpressure contracts and decision logic, including budget snapshots, priorities, admission outcomes, retry/circuit semantics, generation identity/retirement semantics, subscription intents and deterministic shedding.

## Negative authority
No actual WebSocket/socket/network connection, subscribe/unsubscribe call, reconnect I/O loop, realtime market ingest, MEXC/private endpoint expansion, credentials/auth/signing, order/trading/Risk/OMS/Execution, persistence, deployment or live capability may be authorized.

## Required authorization evidence
- exact governance-only four-file delta;
- exact-base/head PR assertions;
- CP0026 fail-closed proof;
- R11 dependency-order proof;
- Module 29 ownership proof;
- S1D negative-scope firewall proof;
- Work Order completeness proof;
- `git diff --check`;
- exact-head pull-request-only CI;
- fresh independent HIGH_ASSURANCE review with CRITICAL=0 and HIGH=0.

## STOP CONDITION
STOP with the authorization PR OPEN and UNMERGED after exact-head governance CI and author-side preflight. Do not create an S1D implementation branch, mutate product code, promote an authorization checkpoint, connect to an exchange, deploy or activate any live authority until independent review and governance acceptance complete.