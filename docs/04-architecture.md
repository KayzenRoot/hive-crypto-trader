# Architecture

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R11`
Risk class: `HIGH_ASSURANCE`

Governance architecture remains:
`Analyze -> Source Check -> Next Necessary Increment -> Work Order -> Context Lock -> Preflight -> Executor -> Tests/Evidence -> PR -> Audit -> Verdict -> Checkpoint Delta -> Merge -> Next`

A correction never creates a new functional increment. It remains a Correction Delta under the same Work Order/PR when safe.

## Canonical runtime architecture
Hive Crypto Trader separates frontend and backend as independently deployable runtime surfaces while treating the backend as the authoritative execution/security boundary.

### Frontend
The frontend owns presentation, realtime visualization, user interaction, local ephemeral UI state and client-safe orchestration only. It must not contain exchange secrets, privileged signing logic, authoritative risk rules or security-sensitive business logic.

Planned frontend surfaces include:
- user trading cockpit;
- Copilot setup/session UI;
- scanner and symbol intelligence;
- strategy/indicator visualizations;
- orders/positions/risk views;
- user account/tenant settings;
- owner-only admin control-plane UI.

The frontend consumes versioned Canonical UI State Envelopes and is never a source of exchange/account/risk truth.

### Backend
The backend owns authoritative trading, risk, policy, data, security and orchestration responsibilities, including:
- exchange integration and credential isolation;
- market-data ingestion and normalization;
- scanner, indicators, strategies, signals and agents;
- Safety Governor, Risk Engine, Session Policy, position sizing and leverage;
- execution, OMS, reconciliation and protection integrity;
- RAG/model lifecycle and research services;
- tenant/admin authorization;
- Harness/capability isolation;
- persistence, audit, observability and operational controls.

## R11 integrated authority model
Trading authority is **not** a relaxable sequential chain. An exposure-increasing action is permitted only by the intersection of all applicable restrictive authorities:
- current exchange capabilities/rules;
- authenticated SecurityContext plus tenant/account/environment binding;
- Harness/capability state;
- Safety & Protection Governor;
- Session Policy / User Operating Envelope;
- Risk Engine / portfolio / survival / collateral limits;
- R05 data-authority/freshness state;
- current reconciliation/protection state;
- R07 promotion/environment eligibility.

Any authoritative domain may deny or tighten within its scope. No later component may relax a stricter result from another domain.

## Two-phase position construction
The apparent dependency cycle between Risk, Position Sizing and Leverage is resolved through two phases:
1. Position Sizing/Leverage produce a bounded proposal under exchange/session/global ceilings.
2. Risk computes the projected post-trade RiskSnapshot and may reduce, veto or require recomputation until a consistent construction is approved.

Exposure-increasing execution requires final Risk approval plus a committed Risk Reservation.

## Canonical Command Authorization Bundle
Every state-changing exchange command binds the applicable:
- SecurityContext and tenant/account/environment identity;
- exchange capability/rule snapshot;
- trusted market/account generation and R05 authority/freshness state;
- Safety decision/version;
- SessionPolicySnapshot;
- final RiskSnapshot/hash;
- RiskReservation;
- action class;
- Execution Intent/Plan identity;
- Command Authorization Lease/expiry;
- material release/config/policy versions.

Missing, expired or scope-mismatched required authority rejects the command.

## Action classes and degraded authority
HCT distinguishes `NEW_EXPOSURE`, `ADD_EXPOSURE`, `REDUCE_EXPOSURE`, `CLOSE_EXPOSURE`, `ESTABLISH_OR_REPAIR_PROTECTION`, cancellation, reconciliation/recovery and non-trading control actions.

Therefore a restrictive state can deny NEW/ADD exposure while preserving safe reduce/close/protect/reconcile behavior where exchange capability and authoritative state permit it.

## Source-of-truth principle
Each state family has one canonical internal owner and an explicit external/reconciliation source where relevant. Exchange/account truth is reconciled from the venue. Risk, OMS, Security, Strategy/Model lifecycle, Protection and Audit each own their domain records. Caches, UI and telemetry remain projections and never gain authority merely because they are convenient read models.

The detailed Source-of-Truth Matrix is canonical in `docs/91-r11-integrated-authority-state-dependency-architecture.md`.

## Realtime ownership boundaries
- API Quota/WS/Backpressure Governor owns resource budgets, subscription/request priority and load shedding.
- Realtime Market Data Engine owns normalized immutable inbound exchange market events.
- Data Quality & Freshness Engine owns continuity/freshness/quality predicates and data-authority evidence.
- Market-State Fabric owns generation-scoped coherent reconstructed market state.
- Cache/Hot-State owns optimized read projections with freshness leases only.

## Intelligence ownership boundaries
- Strategy/Agents/News/Memory produce or route evidence.
- Strategy Ecology resolves eligibility, redundancy and strategy conflict.
- Intelligence Brain is the canonical selective candidate-decision fusion layer.
- Copilot orchestrates workflows, agents/tools and action lifecycle.
- Safety/Session/Risk/Execution remain deterministic downstream authority.
- Learning Lifecycle owns candidate/version lifecycle; Promotion Laboratory remains independent promotion-proof authority.

## Environment isolation
`LIVE`, `PAPER`, `SHADOW` and `REPLAY` are part of canonical high-assurance state identity across Risk, OMS, positions, protection, audit and UI. Hypothetical environments cannot reference live exchange mutation authority.

## Contract boundary
Frontend and backend are coupled through versioned contracts, not implementation details. Planned controls include:
- versioned REST/OpenAPI contracts where appropriate;
- versioned realtime/event schemas for WebSocket/SSE/event-stream paths;
- explicit backward-compatibility policy;
- contract tests in CI;
- generated or shared typed clients where useful;
- deprecation/version migration policy;
- no direct frontend dependency on backend internal database schemas.

### Deployment principle
Frontend and backend must support independent build, deploy, rollback and scaling lifecycles. Backend bounded contexts may later decompose where measured scale, fault isolation or security justify it, but discovery does not mandate premature microservices or a particular cloud topology.

### Repository organization direction
Current planning preference remains one canonical repository with separated application roots and shared safe contract artifacts:

`apps/frontend/`
`apps/backend/`
`packages/contracts/`
`packages/shared-safe/`
`infra/`
`docs/`

`packages/shared-safe` may only contain code safe to consume on both sides; it must never become a path for secrets or server-only authority to leak into the client bundle.

## Logical implementation dependency direction
R11 defines staged logical dependencies, not deployment units:
0. canonical contracts/security/audit/environment namespace;
1. exchange and realtime truth;
2. deterministic market intelligence;
3. capital-safety authority;
4. execution/OMS/reconciliation/protection truth;
5. replay/paper/shadow/promotion proof;
6. memory/Brain/agents/Copilot automation;
7. trading/admin/commercial/signal surfaces;
8. full operational hardening and promotion evidence.

Security, audit and observability skeletons begin at Stage 0 and mature continuously.

## Cross-module invariant
Every live-capable action must be explainable as:
`eligible identity + trusted state + promotable candidate + restrictive authority intersection + reserved risk + authorized command + exchange evidence + reconciled state + verified protection`.

If a required term is unknown, invalid or expired, HCT degrades, abstains or reconciles rather than inventing certainty.

Detailed R11 architecture and module classification are canonical in:
- `docs/91-r11-integrated-authority-state-dependency-architecture.md`;
- `docs/92-r11-v1-module-classification-and-integration-hardening.md`.

Implementation, production deployment topology, production credentials and live trading remain unauthorized.
