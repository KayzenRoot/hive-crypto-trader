# HCT-PLAN-0001-R11 — V1 Module Classification & Integration Hardening

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R11`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

## Classification semantics
- `V1_CORE`: required for the intended V1 product/safety architecture. A production-live activation may still remain separately gated.
- `V1_MINIMUM`: include a bounded minimum useful implementation in V1; advanced depth is deferred.
- `IMPORTANT_POST_V1`: architecturally anticipated and valuable, but not required to declare V1 functionally complete.
- `FUTURE`: intentionally excluded from V1 implementation scope unless later promoted.

Architecture readiness is not the same as production/live authorization.

## 42-module classification

| # | Module | Classification | V1 interpretation |
|---|---|---|---|
| 1 | Exchange Abstraction & Adapter Framework | V1_CORE | Mandatory provider boundary even though only MEXC is live in V1. |
| 2 | MEXC Futures Adapter | V1_CORE | Only V1 live venue adapter. |
| 3 | Market Universe Registry | V1_CORE | Dynamic eligible-contract truth. |
| 4 | Realtime Market Data Engine | V1_CORE | Public market event ingest. |
| 5 | Realtime Stream Processing / Market-State Fabric | V1_CORE | Trusted coherent market-state generation. |
| 6 | Market Scanner | V1_CORE | Broad-universe candidate discovery. |
| 7 | Data Quality & Freshness Engine | V1_CORE | Hard data-authority input. |
| 8 | Indicator & Feature Engine | V1_CORE | Major validated indicator/feature families. |
| 9 | Candlestick & Chart Pattern Engine | V1_MINIMUM | Useful public/standard patterns; breadth can expand later. |
| 10 | Proprietary Indicator R&D Lab | V1_MINIMUM | Framework + initial hypotheses; large proprietary library deferred. |
| 11 | Strategy Engine | V1_CORE | Versioned deterministic strategy runtime. |
| 12 | User Strategy Builder & Strategy DSL | V1_MINIMUM | Typed declarative builder baseline; advanced graph optimization deferred. |
| 13 | Default Strategy Catalog | V1_MINIMUM | Initial documented validated set; not every researched family must be live. |
| 14 | Strategy Ecology / Router / Ensemble | V1_MINIMUM | Eligibility/redundancy/conflict baseline; advanced adaptive routing later. |
| 15 | Signal Engine | V1_CORE | Candidate action semantics/freshness/provenance. |
| 16 | Market Regime Engine | V1_CORE | Minimum regime context required for strategy/Brain. |
| 17 | HCT Intelligence Brain | V1_CORE | Selective evidence fusion/candidate decisions; still non-authoritative over Risk/Safety. |
| 18 | RAG & Market Memory | V1_CORE | Governed query facade and minimum point-in-time memory support. |
| 19 | Learning & Model Lifecycle | V1_CORE | Candidate/version/promotion metadata and rollback governance; online self-learning not required. |
| 20 | Risk Engine | V1_CORE | Hard monetary/survival authority. |
| 21 | Leverage Engine | V1_CORE | Bounded construction under exchange/Risk ceilings. |
| 22 | Position Sizing Engine | V1_CORE | Risk-derived quantity construction. |
| 23 | Safety & Protection Governor | V1_CORE | Independent fail-safe deny/tighten authority. |
| 24 | Execution Intelligence & Feasibility | V1_CORE | Safe executable plan under bounded tactics. |
| 25 | OMS | V1_CORE | Canonical order lifecycle/idempotency/economic fill processing. |
| 26 | Position/Account Reconciliation & State Confidence | V1_CORE | Exchange truth and unknown-outcome recovery. |
| 27 | Protective Order Integrity Monitor | V1_CORE | Required protection verification/recovery. |
| 28 | Portfolio Exposure Engine | V1_CORE | Common-factor/concentration exposure. |
| 29 | API Quota / WS / Backpressure Governor | V1_CORE | Exchange quota/safety resource control. |
| 30 | Caching & Hot-State Layer | V1_CORE | Low-latency state projection with freshness leases. |
| 31 | Simulation / Replay / Paper / Shadow / Promotion Lab | V1_CORE | Mandatory proof system before production activation. |
| 32 | Multi-Tenant Platform Foundation | V1_CORE | Tenant/security/account boundaries must not be retrofitted after V1. |
| 33 | Realtime Trading Cockpit / UI-UX | V1_CORE | Main operator/customer surface with safety semantics. |
| 34 | Agentic Copilot Orchestrator | V1_CORE | Automated workflow architecture; FULL_COPILOT live activation remains separately gated. |
| 35 | Institutional Agent Workforce / Skills / Tool Gateway | V1_MINIMUM | Minimum specialist set/tool governance in V1; full 20-agent depth is capability-gated. |
| 36 | Session Policy & User Operating Envelope | V1_CORE | Mandatory autonomous/user risk envelope. |
| 37 | News & Event Intelligence | V1_MINIMUM | Governed approved-source minimum; richer feeds/agents later. |
| 38 | Administrative Control Plane | V1_CORE | Owner operations/safety/security/tenant control. |
| 39 | Harness / Capability Isolation & Blackout | V1_CORE | Required fault containment/kill/degradation plane. |
| 40 | Microstructure / Order-Flow / Liquidity / Breadth / Cross-Market | V1_MINIMUM | V1: liquidity/order-flow/execution-relevant subset; advanced breadth/lead-lag/anomaly R&D is IMPORTANT_POST_V1. |
| 41 | Temporal Market Memory / Historical Analog / Continual Learning | V1_CORE | V1 point-in-time temporal memory/analog foundation; advanced continual adaptation is IMPORTANT_POST_V1. |
| 42 | Signal Publishing / Telegram Rooms | V1_CORE | Explicit product requirement, isolated from exchange execution; advanced subscriber intelligence can expand later. |

## Explicit FUTURE live capabilities
Regardless of module readiness, the following remain `FUTURE` for live activation:
- exchanges other than MEXC Futures;
- multi-venue smart order routing;
- arbitrary user executable code;
- self-modifying production Risk/Safety/Execution/Brain logic;
- dedicated large-scale streaming/vector/graph infrastructure before measured need;
- advanced marketplace/white-label capabilities not separately promoted;
- unrestricted mobile live-trading authority;
- legal/commercial availability in regions not explicitly reviewed/eligible.

## Integration hardening for HIGH gaps

### Signals feedback isolation — GAP-R11-18
Telegram/subscriber delivery and realizability metrics belong to Signal Publishing analytics. They may become research evidence only through the Canonical Evidence/Temporal Memory/Learning/Promotion path. They never directly modify live strategy parameters or trading authority.

### Admin vs Trading Cockpit — GAP-R11-19
Shared visual components are allowed, but authority surfaces remain separate:
- Trading Cockpit: tenant/account trading observation/actions within policy;
- Admin Control Plane: owner/platform capability/tenant/incident/release controls under higher-assurance privilege.
Normal tenant routes never discover privileged actions through client hiding alone.

### Observability vs domain audit — GAP-R11-20
R10 Audit Ledger references immutable domain IDs/evidence. Telemetry/search indexes may denormalize for query performance but are projections and must not become competing OMS/Risk/Security history.

### Explicit V1 cross-cutting prerequisites — GAP-R11-21
V1_CORE includes:
- multi-tenant identity/security foundation;
- secrets/auth/session controls;
- cockpit safety semantics;
- audit/observability minimums;
- Harness/admin operations;
- replay/promotion proof.
These are foundations, not polish postponed until commercialization.

### Microstructure split — GAP-R11-22
V1 minimum includes execution-relevant liquidity/order-flow/spread/impact/book integrity features that measurably improve feasibility/risk. Advanced cross-asset propagation, broad anomaly R&D and expensive feature families must earn value/cost promotion.

### Agents/news split — GAP-R11-23
The system can operate with deterministic paths and a reduced agent set. Missing optional agent/model/news capability lowers available evidence and may trigger abstention, but must not make Risk/Safety unavailable. Full workforce depth is not a V1 launch blocker unless a promoted strategy explicitly depends on it.

### Copilot architecture vs activation — GAP-R11-24
V1 implements the governed orchestration architecture needed for automation. Any production `FULL_COPILOT` activation remains conditional on R07 evidence, tenant/session policy, security/region/exchange eligibility and future live authorization.

### Commercial entitlement vs live eligibility — GAP-R11-25
`paid/entitled` is never equivalent to `live eligible`. Live ability is an intersection of commercial entitlement, region/legal/exchange/KYC/API capability, SecurityContext, account credential health, promotion, Safety/Risk and current operational authority.

### Retention vs replay evidence — GAP-R11-26
Retention priority order:
1. exchange/order/fill/account/risk/protection/audit/security evidence required for money/recovery;
2. promotion/replay datasets whose manifest declares required fidelity;
3. calibrated research datasets;
4. general analytics/low-value raw telemetry.
Compaction must update completeness manifests so missing raw history never masquerades as full-fidelity replay data.

### FinOps/load shedding vs evidence availability — GAP-R11-27
If optional features/agents/research are suppressed, their evidence state becomes `UNAVAILABLE/DEGRADED`; Strategy/Brain consumes that explicit state and recomputes/abstains. Last-known optional evidence cannot remain silently fresh.

### Localization vs canonical contracts — GAP-R11-28
Only presentation is localized. Canonical IDs, state enums, API/event schemas, Strategy DSL/node IDs, audit reason codes and numeric execution values remain language-neutral/English canonical.

### Requirements fragmentation — GAP-R11-29
R11 inventories accepted addenda but does not rewrite all requirements. R12 must consolidate them into a frozen requirements baseline with traceability back to each round. No accepted requirement may disappear during consolidation.

### Pre-discovery precedence — GAP-R11-30
Formal round artifacts R03–R11 and Decisions Ledger override conflicting exploratory R02/pre-discovery wording. Older docs remain research/context unless explicitly promoted by later requirements/decisions.

### Provider/topology neutrality — GAP-R11-31
The dependency DAG specifies logical contracts, not deployment units. A module may be an in-process component, worker, service or library until benchmark/security/reliability evidence justifies topology. `docs/07-deployment.md` remains intentionally unapproved.

### System-level V1 success themes — GAP-R11-32
A V1 planning-complete system must be capable of proving:
- exchange/data/state correctness;
- deterministic safety/risk/execution/reconciliation/protection;
- point-in-time validation/promotion;
- tenant/security/secret isolation;
- intelligence abstention/no-self-promotion;
- cockpit state truth/accessibility;
- audit/incident/recovery evidence;
- bounded costs/quotas;
- no unresolved HIGH/CRITICAL planning contradiction.

## Classification rule
R12 may refine wording and acceptance traceability, but changing a module from `V1_CORE`/`V1_MINIMUM` to deferred status requires an explicit Decision Ledger entry with impact analysis. No accepted module silently disappears during freeze.

All R11 HIGH integration gaps are resolved at planning level by these contracts. Implementation remains unauthorized.
