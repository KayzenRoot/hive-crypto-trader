# HCT-PLAN-0001-R11 — Integrated Authority, State Ownership & Dependency Architecture

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R11`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

## Purpose
Resolve the critical R11 integration gaps by defining how approved R01–R10 domains compose without circular authority or competing sources of truth.

## 1. Canonical authority model: deny/tighten lattice
HCT does not use one simplistic sequential authority chain. Trading authority is the intersection of independent restrictive domains.

### Preconditions
An exposure-increasing action is not even eligible for construction unless these preconditions are valid:
- authenticated `SecurityContext` and exact tenant/account/environment binding;
- exchange/account capability and current contract/risk-rule state;
- environment mode permits live mutation;
- Harness/capability state permits the action class;
- required market/private data authority is sufficiently trusted/fresh.

### Candidate authority
Strategy, Signal, Agent, News, Memory, Brain and Copilot components may produce evidence/candidate intent. None grants monetary authority.

### Restrictive authority lattice
The final permitted action is the intersection of:
- exchange constraints/capabilities;
- Security/Tenant authorization;
- Harness availability/restrictions;
- Safety & Protection Governor;
- Session Policy / User Operating Envelope;
- Risk Engine / survival / portfolio / collateral limits;
- R05 data-authority/freshness state;
- current reconciliation/protection state;
- R07 promotion/environment eligibility.

Every domain may deny or tighten within its own authority. No downstream component may relax a stricter upstream/parallel result.

## 2. Two-phase position construction
Resolve the Risk ↔ Size/Leverage apparent cycle through a governed construction loop.

### Phase A — bounded proposal
Inputs:
- candidate direction/thesis/invalidation;
- current account/portfolio state;
- session/global ceilings;
- exchange tier/leverage/MMR/capability rules;
- liquidity/execution constraints.

`PositionSizing` and `Leverage` calculate a bounded proposal, not an authorization.

### Phase B — post-trade risk approval
Risk Engine computes the immutable projected `RiskSnapshot` using proposed quantity/leverage and evaluates:
- monetary/cumulative risk;
- tier/MMR/liquidation corridor;
- cross-margin contagion;
- portfolio/correlation;
- OMR/survival budgets;
- collateral/extreme-venue risk;
- protection assumptions;
- reservation capacity.

Risk may reduce or veto the proposal. If reduction changes construction materially, the loop recomputes until one final internally consistent construction is approved or denied.

Only then is Risk Reservation committed before execution submit.

## 3. Canonical Command Authorization Bundle
Every state-changing exchange command binds to one immutable/versioned authorization bundle referencing at minimum, where applicable:
- `SecurityContextID` / tenant-account binding;
- environment/mode identity;
- exchange capability/rule snapshot;
- trusted market/account generation references;
- R05 trading-authority/freshness state;
- Safety decision/version;
- SessionPolicySnapshot ID/version;
- final approved RiskSnapshot ID/hash;
- RiskReservation ID/state;
- allowed action class (`INCREASE`, `REDUCE`, `CLOSE`, `PROTECT`, `CANCEL`, `RECONCILE_RECOVERY`);
- Execution Intent/Plan identity;
- Command Authorization Lease / expiry;
- release/policy versions.

Execution rejects a command if any required component is absent, expired, scope-mismatched or invalidated.

## 4. Action-class matrix under degraded states
Canonical action classes:
- `NEW_EXPOSURE`;
- `ADD_EXPOSURE`;
- `REDUCE_EXPOSURE`;
- `CLOSE_EXPOSURE`;
- `ESTABLISH_OR_REPAIR_PROTECTION`;
- `CANCEL_ENTRY`;
- `CANCEL_OR_REPLACE_PROTECTION`;
- `RECONCILIATION_RECOVERY`;
- `NON_TRADING_CONTROL`.

Typical policy direction:
- `ALLOW_NEW_EXPOSURE`: all policy-eligible classes;
- `DEGRADED_NEW_EXPOSURE`: only explicitly approved reduced new exposure plus safety actions;
- `NO_NEW_EXPOSURE`: deny NEW/ADD; preserve reduce/close/protect/cancel-entry/reconcile;
- `REDUCE_ONLY`: only reduction/close/protection/reconciliation-compatible operations;
- `RECONCILIATION_ONLY`: no ordinary trading mutation except narrowly governed protection/recovery if authoritative prerequisites exist;
- `EMERGENCY`: Harness/Safety emergency whitelist only.

Exact command semantics remain exchange-capability aware.

## 5. Harness and Safety precedence
Harness may restrict or isolate capabilities but cannot create a more dangerous state by disabling required safety dependencies.

Canonical rule:
`Harness restriction <= existing authority`.

Examples:
- disabling Strategy Engine stops new candidates but does not disable protection/reconciliation;
- exchange freeze stops new exposure but preserves safe reduce/protect/reconcile paths if available;
- model quarantine removes model evidence but cannot suppress deterministic Risk/Safety;
- global blackout uses dependency graph and emergency action whitelist rather than killing every process.

## 6. Source-of-Truth Matrix

| State / concept | Internal canonical owner | External authority / reconciliation | Projections/consumers |
|---|---|---|---|
| Tenant/member/role | Identity/Security domain | configured IdP/auth evidence | all protected services/UI |
| Raw exchange credential | SecretStore | exchange credential validity | opaque credential ref only |
| Contract/capability/risk rules | Exchange Adapter capability resolver | exchange API/docs/current venue state | Universe/Risk/Execution/UI |
| Raw/normalized market events | Realtime Market Data Engine | exchange public feed | Data Quality/Market-State Fabric |
| Trusted coherent market state | Market-State Fabric | validated exchange event stream | features/strategy/Brain/Risk/UI |
| Data-quality authority | Data Quality/Freshness + R05 authority policy | source continuity/cross-channel evidence | all time-sensitive domains |
| Strategy definition/version | Strategy registry/engine | approved promotion record | Router/Signal/UI |
| Model/agent/tool/skill version | Learning/Agent lifecycle registries | promotion evidence | Brain/Copilot/Audit |
| Session operating envelope | Session Policy Engine | user/admin policy within global ceilings | Risk/Safety/Execution/UI |
| Risk decision | Risk Engine / RiskSnapshot | current exchange/account state inputs | Reservation/Execution/UI/Audit |
| Reserved risk | Risk Reservation Ledger | resolved against exchange outcome | Risk/OMS/Execution |
| Execution intent/command | Execution domain + OMS event log | exchange acknowledgment/evidence | Reconciliation/UI/Audit |
| Fill | immutable exchange fill evidence | exchange | OMS/accounting/Risk/Reconciliation |
| Position/balance | Reconciliation authoritative projection | exchange account truth | Risk/UI/Brain |
| Protection coverage | Protective Integrity Monitor | exchange orders + position truth | Safety/Risk/UI |
| Audit event | Audit Ledger | referenced domain evidence | Admin/assurance |
| UI state | no independent truth; UI State Envelope projection | backend domain envelopes | human operator |
| Signal publication state | SignalPublisher/Outbox | Telegram/provider delivery evidence | Signals UI/analytics |
| Cost | FinOps cost ledger by truth class | provider usage/billing/invoice | dashboards/budgets |

No consumer may become a competing source merely because it caches or visualizes the state.

## 7. Realtime subsystem boundaries
Resolve modules 4/5/7/29/30:

### Module 29 — API Quota/WS/Backpressure Governor
Owns connection/subscription/request budgets, priority scheduling, retry/circuit policy and load shedding. It does not own market prices.

### Module 4 — Realtime Market Data Engine
Owns exchange session adapters and normalized immutable inbound event envelopes. It does not decide whether a reconstructed book/state is trustworthy enough to trade.

### Module 7 — Data Quality & Freshness Engine
Owns quality predicates, gap/sequence/clock/cross-channel evidence and quality authority outputs. It does not become the coherent market-state store.

### Module 5 — Market-State Fabric
Owns generation-scoped coherent reconstructed market state and feature-consumption barriers, using Module 7 quality decisions and Module 29 resource constraints.

### Module 30 — Cache/Hot State
Owns optimized read copies/freshness leases only. It never upgrades or originates exchange/account truth.

Primary direction:
`Quota/Subscription control -> Exchange session ingest -> normalized events -> quality/continuity -> coherent Market-State generation -> hot-state projections -> consumers`.

## 8. Memory and learning boundaries
### Module 18 — RAG & Market Memory
Acts as the governed query/access facade exposed to Brain/agents/product features. It returns point-in-time admissible memory/analog evidence under R06 contracts.

### Module 41 — Temporal Market Memory / Historical Analog / Continual Learning Intelligence
Owns the deeper temporal storage/index/retrieval/analog/drift/no-trade-learning mechanisms behind the facade. V1 includes the point-in-time foundation; advanced continual-learning optimization is capability-gated.

### Module 19 — Learning & Model Lifecycle
Owns candidate creation/version registry, training/fine-tuning/evaluation metadata, champion/challenger lifecycle and rollback metadata.

### Module 31 — Promotion Laboratory
Is the independent proof authority that determines whether a candidate has sufficient evidence for promotion. Module 19 cannot self-promote its own candidate.

## 9. Strategy / Agents / Brain / Copilot boundaries
- Strategy Engine: produces versioned strategy evidence/candidates.
- Strategy Ecology/Router: determines eligible strategy set/context/redundancy/conflict, not hard trade authority.
- Institutional Agents/News: produce structured contextual evidence under fixed authority ceilings.
- RAG/Memory: provides admissible historical/context evidence.
- Intelligence Brain: canonical evidence-fusion/selective candidate-decision authority (`LONG/SHORT/WAIT/NO_TRADE/REDUCE/EXIT` candidate semantics).
- Copilot Orchestrator: manages the autonomous workflow, tool/agent calls, task sequencing and downstream candidate-action lifecycle. It does not become a second hard Risk/Safety engine.
- Safety/Session/Risk/Execution: deterministic authority downstream.

Thus Copilot may automate the lifecycle but cannot invent a parallel approval path.

## 10. Live / paper / shadow / replay namespace contract
Every stateful domain includes environment namespace in canonical identity:
- tenant/account;
- RiskSnapshot/Reservation;
- OMS/order/fill simulator identity;
- position/account state;
- protection;
- audit;
- UI envelope;
- model/strategy evaluation;
- Signal publication where hypothetical content is allowed.

`PAPER`, `SHADOW`, `REPLAY` identities cannot reference a live exchange mutation capability.

## 11. Canonical identity/version registry
Every cross-domain contract uses globally unique/stable typed identity plus version/hash where behavior matters.

Key families:
- TenantID, MembershipID, ExchangeAccountID, CredentialRef;
- ExchangeID, ContractID, CapabilitySnapshotID;
- MarketGenerationID, DataAuthoritySnapshotID;
- StrategyID/Version, Model/Agent/Tool/Skill versions;
- DecisionID, RiskSnapshotID, RiskReservationID;
- OrderIntentID, ExecutionPlanID, CommandID, ExternalClientOrderID, ExchangeOrderID, FillID;
- Position identity/mode key;
- ProtectionSetID;
- ReconciliationCycle/Watermark ID;
- SessionPolicySnapshotID;
- Release/Config/Policy versions;
- IncidentID, AuditEventID, TraceID;
- Experiment/PromotionBundle IDs.

IDs are never overloaded with mutable display names.

## 12. Failure/degradation propagation
Every capability declares:
- dependencies;
- whether dependency failure affects new exposure, reduction, protection, reconciliation, research or UI only;
- fallback/degradation state;
- recovery proof.

Examples:
- public market feed stale -> no time-sensitive new exposure; positions still reconcile from private/account sources where possible;
- private account stream stale -> reconciliation/state confidence degrades; new exposure restricted;
- RAG/model unavailable -> Brain may fall back/abstain; deterministic risk remains;
- telemetry backend unavailable -> hot safety continues, but mandatory-evidence durability loss can eventually restrict exposure;
- Telegram unavailable -> trading unaffected; signal outbox retries/degrades separately;
- UI unavailable -> backend safety/trading state remains authoritative; no UI-dependent automation.

## 13. Implementation dependency DAG
Recommended dependency stages, allowing vertical slices inside each stage:

### Stage 0 — Canonical contracts/governance/security foundation
- shared domain IDs/contracts/errors;
- SecurityContext/tenant/account binding;
- SecretStore abstraction;
- audit/evidence primitives;
- configuration/version semantics;
- environment namespace.

### Stage 1 — Exchange and realtime truth
- Exchange Abstraction + MEXC adapter;
- capability/rule resolver;
- universe;
- quota/WS governor;
- market ingest, quality, Market-State Fabric, cache.

### Stage 2 — Deterministic market intelligence
- features/indicators/patterns;
- regime;
- scanner;
- strategy engine/catalog/signal;
- minimum microstructure.

### Stage 3 — Capital-safety authority
- Session Policy;
- Portfolio Exposure;
- Safety Governor;
- Position Sizing/Leverage proposal;
- Risk Engine/RiskSnapshot/Reservation;
- Harness safety scopes.

### Stage 4 — Execution truth
- Execution Intelligence;
- OMS;
- Exchange command adapter;
- Reconciliation/State Confidence;
- Protective Integrity;
- recovery/idempotency.

### Stage 5 — Validation proof system
- event replay/accounting/live-parity;
- backtest/walk-forward/OOS;
- paper/shadow;
- promotion evidence.

### Stage 6 — Intelligence/automation
- Temporal Memory/RAG facade;
- Learning lifecycle;
- Brain;
- minimum Agent Workforce/News;
- Copilot orchestration.

### Stage 7 — Operator/commercial surfaces
- Trading Cockpit/UI;
- Admin Control Plane;
- multi-tenant commercial/entitlement surfaces;
- Signals/Telegram;
- localization.

### Stage 8 — Operational hardening/promotion
- complete observability/SLO/incident/FinOps;
- chaos/failure testing;
- performance/capacity;
- security adversarial testing;
- R07 promotion gates.

Observability/audit/security skeletons begin in Stage 0 and mature continuously; Stage 8 is not permission to postpone critical instrumentation until the end.

## 14. Cross-module invariant
Every live-capable action must be explainable as:
`eligible identity + trusted state + promotable candidate + restrictive authority intersection + reserved risk + authorized command + exchange evidence + reconciled state + verified protection`.

If any required term is unknown/invalid/expired, HCT must degrade/abstain/reconcile rather than invent certainty.

These contracts resolve GAP-R11-01 through GAP-R11-16 at planning level. GAP-R11-17 and HIGH classification/integration items are resolved by the R11 classification matrix and hardening artifacts.
