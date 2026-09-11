# Architecture

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R02`
Risk class: `HIGH_ASSURANCE`

Governance architecture remains:
`Analyze -> Source Check -> Next Necessary Increment -> Work Order -> Context Lock -> Preflight -> Executor -> Tests/Evidence -> PR -> Audit -> Verdict -> Checkpoint Delta -> Merge -> Next`

A correction never creates a new functional increment. It remains a Correction Delta under the same Work Order/PR when safe.

## Runtime architecture direction approved for discovery
Hive Crypto Trader will separate frontend and backend as independently deployable runtime surfaces.

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

### Backend
The backend owns all authoritative trading, risk, policy, data, security and orchestration responsibilities, including:
- exchange integration and credential isolation;
- market-data ingestion and normalization;
- scanner, indicators, strategies, signals and agents;
- Safety Governor, Risk Engine, policy enforcement, position sizing and leverage;
- execution, OMS and reconciliation;
- RAG/model lifecycle and research services;
- tenant/admin authorization;
- Harness/capability isolation;
- persistence, audit, observability and operational controls.

### Contract boundary
Frontend and backend are coupled through versioned contracts, not implementation details. Planned controls include:
- versioned REST/OpenAPI contracts where appropriate;
- versioned realtime/event schemas for WebSocket/SSE/event-stream paths;
- explicit backward-compatibility policy;
- contract tests in CI;
- generated or shared typed clients where useful;
- deprecation/version migration policy;
- no direct frontend dependency on backend internal database schemas.

### Deployment principle
Frontend and backend must support independent build, deploy, rollback and scaling lifecycles. A frontend release should not require rebuilding the trading backend unless contracts change. Backend services may later decompose further by bounded context where scale, fault isolation or security justify it, but discovery does not mandate premature microservices.

### Repository organization direction
Current planning preference is one canonical repository with clearly separated application roots and shared contract artifacts, unless a later deployment/security review proves separate repositories are materially better. Conceptual structure:

`apps/frontend/`
`apps/backend/`
`packages/contracts/`
`packages/shared-safe/`
`infra/`
`docs/`

`packages/shared-safe` may only contain code safe to consume on both sides; it must never become a path for secrets or server-only authority to leak into the client bundle.

### Security boundary
The frontend is always an untrusted client from the backend perspective. Every privileged action is authenticated, authorized and validated server-side, including admin/Harness actions.

### Operational advantage
This separation supports independent deployment, safer rollbacks, clearer ownership, differential scaling, fault isolation, CDN/static delivery for frontend assets and stricter security around exchange credentials/trading authority.
