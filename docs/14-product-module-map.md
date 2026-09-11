# Product Module Map

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R11`
Risk class: `HIGH_ASSURANCE`

This document records the accepted planning module registry. It is not implementation or live-trading authorization. No accepted module may silently disappear; R11 classification is canonical in `docs/92-r11-v1-module-classification-and-integration-hardening.md`.

**R11 integration rule:** any linear diagram below describes evidence/data/action flow only. Trading authority is governed by the restrictive lattice in `docs/04-architecture.md` and `docs/91-r11-integrated-authority-state-dependency-architecture.md`; no later component can relax a stricter authoritative gate.

## Current module map

1. **Exchange Abstraction & Adapter Framework** — canonical exchange capability interface, normalized domain models, capability matrix and adapter contract for current/future exchanges.
2. **MEXC Futures Adapter** — V1 REST/WebSocket integration, authentication, signing, protocol translation and MEXC-specific capability discovery behind the exchange abstraction.
3. **Market Universe Registry** — dynamic discovery of futures contracts actually exposed and eligible through the active exchange adapter.
4. **Realtime Market Data Engine** — normalized immutable trades, tickers, candles, order book, mark/fair/index price, funding and related exchange event envelopes.
5. **Realtime Stream Processing, Market-State Fabric & Latency Intelligence** — generation-scoped coherent market state, event-time lineage, bounded queues/backpressure integration, latency budgeting and feature coherency barriers.
6. **Market Scanner** — continuous multi-symbol scanning, filtering, ranking and candidate discovery.
7. **Data Quality & Freshness Engine** — stale-feed detection, gaps, sequence/clock errors, malformed data, cross-channel contradictions and data-authority evidence.
8. **Indicator & Feature Engine** — canonical indicator library, derived features, multi-timeframe computation and feature/indicator versioning.
9. **Candlestick & Chart Pattern Engine** — governed public/standard candlestick and broader price/market-structure patterns.
10. **Proprietary Indicator R&D Lab** — HCT-created indicators/features treated as hypotheses until statistically validated and promoted.
11. **Strategy Engine** — versioned pluggable long/short strategy definitions and constraints.
12. **User Strategy Builder & Strategy DSL** — typed nodal/structured declarative strategy creation without arbitrary backend code execution.
13. **Default Strategy Catalog** — documented, versioned built-in strategy templates with regime/timeframe/entry/exit/risk/validation metadata.
14. **Strategy Ecology, Router, Ensemble & Conflict Engine** — strategy eligibility/context suitability, redundancy-aware ensembles, conflict handling and strategy-decay evidence.
15. **Signal Engine** — turns strategy evidence into candidate entry/exit/no-trade semantics with freshness and provenance.
16. **Market Regime Engine** — trend/range, volatility, liquidity, cycle and abnormal-regime classification.
17. **HCT Intelligence Brain** — calibrated admissible-evidence fusion and selective candidate-decision layer; never authoritative over deterministic Safety/Session/Risk/Execution.
18. **RAG & Market Memory** — governed consumer/query facade for relevant point-in-time historical context, setups, outcomes, incidents and lessons.
19. **Learning & Model Lifecycle** — candidate/model/version lifecycle, controlled learning, evaluation metadata, champion/challenger and rollback metadata; cannot self-promote.
20. **Risk Engine** — hard monetary, portfolio, drawdown, correlation, survival, collateral and market-state risk authority.
21. **Leverage Engine** — bounded leverage proposal subordinate to exchange/session/global ceilings and final Risk approval.
22. **Position Sizing Engine** — bounded quantity proposal from thesis invalidation, approved risk envelope, liquidity and portfolio state, finalized only after post-trade Risk approval.
23. **Safety & Protection Governor** — independent fail-safe deny/tighten authority over new exposure and safety-critical operating state.
24. **Execution Intelligence & Feasibility Engine** — converts approved intents into bounded execution plans using liquidity, slippage, impact, latency and tactic-capability constraints.
25. **Order Management System (OMS)** — event-sourced lifecycle of intents/orders/fills/cancel-replace/reject/expiry/uncertainty with idempotency and economic fill conservation.
26. **Position / Account Reconciliation & State Confidence** — continuous exchange-authoritative account/position/order/fill reconciliation, unknown-outcome resolution and restart recovery.
27. **Protective Order Integrity Monitor** — verifies stop/TP/trailing coverage, protected quantities, reduce-only semantics and protection recovery.
28. **Portfolio Exposure Engine** — aggregate directional, correlated/common-factor and concentration exposure.
29. **API Quota, WebSocket & Backpressure Governor** — exchange request/subscription budgets, priority scheduling, retries/circuits and deterministic load shedding. It does not own market prices or account truth.
30. **Caching & Hot-State Layer** — low-latency read projections with freshness leases/TTL/invalidation and no authority upgrade.
31. **Simulation, Replay, Paper, Shadow & Promotion Laboratory** — independent point-in-time proof authority for replay, realistic frictions, walk-forward/OOS, paper/shadow, stress, champion/challenger and promotion evidence.
32. **Multi-Tenant Platform Foundation** — tenant/account/environment isolation, credential boundaries, quotas, policy and commercialization-ready foundations.
33. **Realtime Trading Cockpit / UI-UX System** — non-authoritative operational UI with safety/freshness/evidence/environment semantics and accessible degraded-state communication.
34. **Agentic Copilot Orchestrator** — supervised orchestration of workflows, agents/tools and candidate-action lifecycle inside hard authority boundaries.
35. **Institutional Agent Workforce, Skills & Tool Gateway** — bounded specialized evidence agents, tool permissioning, skills lifecycle, model/tool routing and evaluation.
36. **Session Policy & User Operating Envelope Engine** — immutable user/session limits and operating-policy snapshots that may tighten but never exceed platform/global safety ceilings.
37. **News & Event Intelligence** — approved-source event/calendar/breaking-news evidence with provenance/corroboration and no direct trading authority.
38. **Administrative Control Plane** — owner-only operational surface for platform, tenant, incident, release and privileged controls under higher-assurance authorization.
39. **Harness / Capability Isolation & Blackout Engine** — dependency-aware capability restriction, quarantine, no-new-actions, maintenance and emergency blackout controls that cannot weaken required safety/recovery paths.
40. **Microstructure, Order-Flow, Liquidity, Breadth & Cross-Market Intelligence** — execution-relevant liquidity/order-flow plus advanced breadth/lead-lag/anomaly research subject to V1-minimum/post-V1 classification.
41. **Temporal Market Memory, Historical Analog & Continual Learning Intelligence** — point-in-time temporal store/index/retrieval/analog/drift mechanisms behind the RAG facade; advanced continual adaptation remains governed/capability-gated.
42. **Signal Publishing, Telegram Rooms & Subscriber Delivery Intelligence** — first-class Signals workspace, durable/idempotent Telegram delivery and lifecycle analytics isolated from exchange execution authority.

## R11 V1 classification
The authoritative per-module classification is maintained in `docs/92-r11-v1-module-classification-and-integration-hardening.md`.

Classification meanings:
- `V1_CORE`: required V1 architectural/product foundation;
- `V1_MINIMUM`: bounded useful V1 implementation, deeper capability deferred;
- `IMPORTANT_POST_V1`: valuable advanced depth not required for V1 completion;
- `FUTURE`: intentionally outside V1 unless explicitly promoted.

Module readiness never implies production/live activation.

## Cross-cutting platform capabilities
The following are architectural capabilities spanning multiple modules rather than shadow owners of domain truth:
- security, secrets, identity, tenant/account/environment authorization;
- restrictive authority lattice and Canonical Command Authorization Bundle;
- auditability and immutable/tamper-evident evidence;
- observability, tracing, metrics, trading-aware SLOs and incident response;
- persistence, schema evolution and typed identity/versioning;
- configuration/versioning;
- testing, CI/CD, promotion and release governance;
- performance, resilience and disaster recovery;
- event-time/knowledge-time provenance and replay fidelity;
- bounded queues, quota control, backpressure and deterministic load shedding;
- cache freshness leases and no-authority-upgrade semantics;
- temporal leakage prevention and point-in-time memory;
- calibrated abstention, evidence independence and model/agent reliability;
- realistic fees/funding/spread/slippage/latency/impact/partial-fill modeling;
- multi-tenant security, billing readiness and entitlement boundaries;
- localization with `en-US` canonical and `pt-BR`/`es` presentation support;
- FinOps/cost controls subordinate to safety/security/evidence;
- legal/compliance/regional eligibility checks;
- exchange capability normalization and portability;
- agent/tool/skill/prompt/model promotion governance;
- Signal/Telegram delivery security, freshness and idempotency.

## Canonical state/authority ownership
R11 Source-of-Truth Matrix in `docs/91-r11-integrated-authority-state-dependency-architecture.md` is authoritative for state ownership. Caches, UI, analytics and telemetry are projections, never competing owners.

## V1 exchange scope
Only **MEXC Futures** is a V1 live venue target. Binance and other exchanges are future live capabilities. Core domains depend on HCT exchange abstractions rather than MEXC payloads wherever practical.

## Evidence and candidate flow
A useful high-level evidence/data flow is:

`Exchange Adapter -> Realtime Market Data -> Data Quality -> Market-State Fabric -> Microstructure/Features/Patterns/Regime -> Strategy/Router + Temporal Memory + Agents/News -> Intelligence Brain -> Candidate Action`

That flow does **not** grant trading authority.

## Authoritative action flow
After a candidate exists, HCT evaluates the restrictive authority intersection:

`Candidate + Security/Tenant + Exchange Capability/Rules + Harness + Safety + Session Policy + Data Authority + Reconciliation/Protection + Promotion Eligibility -> bounded Size/Leverage proposal -> projected post-trade RiskSnapshot -> final Risk approval -> Risk Reservation -> Execution Plan -> Canonical Authorization Bundle -> OMS/Exchange Command -> Exchange Evidence -> Reconciliation -> Protection Verification`

Any failed/expired/unknown mandatory authority term causes deny, degrade, abstention or reconciliation rather than silent continuation.

## Separate Signal Publishing path
Signal distribution remains isolated from exchange execution:

`Approved Signal Strategy -> Signal Candidate -> Publication Policy/Freshness Gate -> Durable Outbox -> Signal Publisher -> Telegram -> Subscriber`

Subscriber analytics can become research evidence only through the governed Evidence/Memory/Learning/Promotion path and cannot directly self-modify live strategy behavior.

## Validation path
Simulation/Replay/Paper/Shadow/Promotion operates orthogonally against the same domain contracts. Learning Lifecycle may create candidates; Promotion Laboratory is the independent proof authority.

## Administrative/Harness path
Administrative Control Plane and Harness may restrict/degrade capabilities according to dependency/blast-radius analysis but cannot bypass or weaken Safety/Risk/protection/reconciliation requirements in a way that increases danger.

## Planning rule
A broad market universe, candidate signal, positive Brain output, commercial entitlement or Copilot action is never by itself authorization to trade.

Any AI/RAG/learned component must pass promotion gates before production eligibility, and even promoted intelligence remains subordinate to the full R11 restrictive authority lattice.

Implementation, production topology, production credentials, limited-live activation and real-money trading remain unauthorized.
