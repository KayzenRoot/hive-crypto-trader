# Administrative Control Plane & Harness

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R02`
Risk class: `HIGH_ASSURANCE`

## Product requirement
Hive Crypto Trader requires a dedicated administrative control plane that is invisible and inaccessible to normal tenants/users. Initial product policy is a single owner/super-administrator identity. This is a product policy, not a reason to use weak authentication; privileged access requires strong authentication, re-authentication for dangerous actions, immutable audit evidence and recovery procedures.

## Administrative authority
The admin control plane must provide observability and governed control across the complete platform, including tenants, plans/entitlements when introduced, exchange integrations, strategies, indicators, models/agents, Copilot, market data, scanners, risk, execution, WebSocket/API health, caches, jobs, releases and infrastructure-facing application controls.

## Harness / capability control plane
Every independently degradable product capability should expose a governed capability identity and lifecycle state. Candidate states:
- `ENABLED`
- `DEGRADED`
- `READ_ONLY`
- `NO_NEW_ACTIONS`
- `PAUSED`
- `QUARANTINED`
- `DISABLED`
- `EMERGENCY_BLACKOUT`

Controls should be scoped rather than global whenever safe, including global, tenant, account, exchange, symbol/market, strategy, model/agent, indicator, execution route, feature and release/version scopes.

Example: if the proprietary indicator service fails, quarantine that capability while deterministic trading paths remain available if their dependencies and safety proofs remain healthy. If reconciliation becomes uncertain, execution policy may force `NO_NEW_ACTIONS` globally while allowing controlled risk-reducing closes.

## Dependency-aware isolation
A capability cannot be disabled in isolation if doing so would create a more dangerous downstream state. The Harness must maintain a dependency graph and calculate blast radius before applying a control. Emergency controls favor capital protection and state certainty.

## Trading-aware blackout semantics
`BLACKOUT` is not equivalent to blindly killing every process. Emergency policy must distinguish:
- stop opening new exposure;
- cancel eligible pending entry orders;
- preserve/verify exchange-native protective orders;
- allow or command risk-reducing actions where safe;
- reconcile actual exchange state;
- isolate compromised components;
- surface an explicit degraded/emergency state in the cockpit.

## Change safety
Dangerous admin actions require:
- explicit reason/ticket/incident context;
- confirmation and, for highest-impact actions, step-up authentication;
- before/after state snapshot;
- actor identity and timestamp;
- scope and expected blast radius;
- automatic expiry for temporary overrides where applicable;
- rollback/roll-forward plan;
- immutable audit event.

No hidden permanent override is allowed.

## Kill switches and feature controls
Plan distinct controls for:
- platform-wide no-new-trades;
- tenant/account freeze;
- exchange integration freeze;
- symbol freeze;
- strategy freeze;
- Copilot freeze;
- individual agent/model quarantine;
- proprietary indicator quarantine;
- order-type disablement;
- leverage reduction/ceiling override downward only;
- market-data source quarantine;
- API/WebSocket degradation;
- release/version rollback;
- cache bypass/flush under governed conditions;
- maintenance mode;
- full emergency blackout.

## Admin cockpit
The admin UI should include a real-time system map showing capability health, dependencies, tenant impact, trading exposure, open positions/orders, incidents, exchange/API/WebSocket health, data freshness, model/agent versions, active strategies, feature flags, releases and current safety state.

A control action should visually show expected blast radius before confirmation. System topology should behave as an operational map, not a static settings page.

## Tenant isolation
Normal tenants must not discover admin routes, data or controls through UI navigation or authorization failures that leak sensitive structure. Authorization is enforced server-side at every privileged boundary. Tenant data access from admin functions must be purpose-limited and audited.

## Initial single-admin policy
Initial business policy: exactly one active super-admin/owner identity. Architecture should still separate identity, role and policy so future delegated operational roles can be added without redesigning the platform. Adding another privileged administrator later requires an explicit governance decision.

## Harness principle
The desired operational behavior is surgical isolation: `fault -> identify dependency/capability -> contain blast radius -> preserve safety -> repair -> verify -> progressively restore`, rather than restarting or disabling the entire platform by default.
