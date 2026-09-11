# HCT-PLAN-0001-R08 — Critical Tenant Security Architecture

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R08`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

## Purpose
Close the 20 CRITICAL R08 gaps and define machine-enforceable authority boundaries for multi-tenant trading, identity, exchange credentials, privileged administration and resource isolation.

## 1. Canonical Security Context
Every protected operation consumes a server-constructed immutable `SecurityContext`, never a naked client-supplied tenant identifier.

Minimum fields:
- `actor_principal_id`;
- `human_user_id` when human;
- `workload_principal_id` when service/worker;
- `tenant_id`;
- `tenant_membership_id`;
- role/policy version or hash;
- allowed account/resource scopes;
- authentication assurance / step-up state;
- session/token identity and issue/expiry epoch;
- entitlement snapshot reference where needed;
- admin/support-assumption state where applicable;
- trace/correlation/security-context ID.

External requests resolve tenant membership from authenticated identity and server-side membership data. Internal propagation uses authenticated service channels and an integrity-protected context or re-resolves authority; arbitrary forwarded headers/message fields are never sufficient authorization proof.

`SecurityContext` expires/revalidates after membership, role, session, tenant status or critical policy changes.

## 2. Resource Authorization Invariant
Every tenant-owned resource has one authoritative ownership/security scope. Access requires both:
1. authenticated principal/context; and
2. explicit operation authorization against current resource ownership/policy.

Server-side authorization occurs on every protected read/write/action, including internal APIs. Guessing a valid resource ID, knowing an exchange account ID, receiving an event ID or being inside the private network never grants access.

A centralized policy-decision contract may use RBAC + ABAC/capabilities, but policy enforcement remains local at each authoritative boundary. Authorization failures are non-enumerating where practical.

## 3. Database Isolation Contract
Tenant-owned rows/tables/objects use enforceable tenant ownership semantics. Preferred relational baseline:
- canonical `tenant_id`/ownership relationship on tenant-bound data;
- composite uniqueness/foreign-key strategies where cross-tenant identifier collision could matter;
- PostgreSQL RLS or equivalent database-level defense-in-depth for ordinary tenant request paths where feasible;
- application authorization in addition to RLS, not instead of it;
- no ordinary tenant-facing connection using superuser or `BYPASSRLS` authority;
- privileged migrations/jobs use separate identities and audited paths;
- automated negative tests attempt cross-tenant reads/writes for every material repository/domain.

Tables that are intentionally global are explicitly classified and cannot contain tenant-confidential data by accident.

## 4. Connection-Pool & Async Context Isolation
Tenant identity may never survive accidentally across reused DB connections, threads, coroutines, workers or job runners.

Rules:
- tenant database context is transaction-local or otherwise reset safely on checkout/check-in;
- connection reuse tests intentionally alternate tenants at high concurrency;
- async/background work reconstructs SecurityContext from authenticated job identity rather than ambient global/thread-local state;
- failed/cancelled transactions cannot leave privileged or tenant state attached to a pooled connection;
- migrations/admin jobs use explicitly different pools/roles where appropriate.

## 5. Cache Isolation Contract
Every cache value is classified `GLOBAL_SAFE`, `TENANT`, `USER`, or `SECURITY_SENSITIVE`.

Tenant/user-sensitive cache keys include at minimum the applicable tenant plus any user/account/policy/version attributes that change authorization or result semantics. Protected cache access is authorized before serving the value; key separation does not replace authorization.

Intentionally global entries use an explicit global namespace and documented justification. Security/permission changes invalidate or version affected cached authorization-sensitive values. High-sensitivity tenants may later receive physically separate cache partitions/instances without changing domain contracts.

## 6. Queue / Event / Job Security Envelope
Every tenant-bound asynchronous message uses a versioned `TenantWorkEnvelope` containing:
- immutable message/work ID;
- tenant/account/resource scope;
- producer workload principal;
- originating SecurityContext/correlation reference where appropriate;
- operation/capability type;
- policy/version references;
- creation/expiry time;
- idempotency identity;
- integrity/authentication metadata.

The consumer authenticates the producer channel and re-authorizes the requested operation/resource. A `tenant_id` field is routing metadata, not authorization proof. Dead-letter/retry storage preserves tenant isolation and redaction rules.

## 7. Tenant–Exchange Account Binding
A canonical immutable/versioned `TenantExchangeAccountBinding` links:
`tenant -> exchange account -> credential reference -> account capabilities -> risk/policy namespace -> OMS/reconciliation namespace`.

Every market-private stream, RiskSnapshot, Risk Reservation, Execution Command, OMS event, position, protective order and reconciliation state carries or resolves this binding.

A command is rejected before exchange transmission if its tenant/account/credential binding is inconsistent. One tenant may not reuse another tenant's exchange credential or authoritative account state. Any future intentionally shared institutional account model requires a new explicit architecture decision; it is not allowed implicitly in V1.

## 8. Exchange Credential Vault Boundary
Applications store `SecretReference`s, never raw long-lived exchange credentials in ordinary tenant tables/configs.

Requirements:
- encrypted SecretStore/Vault abstraction;
- one credential identity per tenant/exchange account purpose;
- backend-only retrieval by explicitly authorized workload;
- no frontend/browser access;
- no raw-secret return via ordinary admin/support APIs;
- least-privilege exchange permissions, excluding withdrawal/transfer powers unless a future separate requirement explicitly justifies them;
- IP binding/venue restrictions used where supported and operationally safe;
- secret metadata (status, last rotation, permissions, fingerprint) may be queryable separately from secret material;
- credential validation occurs through a controlled exchange adapter, not by displaying the key back to the user.

## 9. Secret Key Hierarchy & Cryptographic Separation
HCT uses envelope-style secret protection through a provider-neutral KMS/SecretStore boundary.

Logical hierarchy:
`root/provider trust -> environment KEK -> scoped DEK/secret encryption -> tenant/account credential`.

Design goals:
- production and non-production cryptographic roots are separate;
- compromise of one tenant/account data-encryption key does not automatically expose every tenant;
- key/algorithm/version metadata supports rotation and migration;
- cryptographic key access is narrower than database access;
- database backup alone must not be sufficient to decrypt exchange credentials;
- key destruction/rotation semantics are explicit and auditable.

Exact cipher/provider selection is deferred to implementation preflight and current cryptographic guidance.

## 10. Secret Lifecycle State Machine
Credential lifecycle is explicit:
`PENDING_IMPORT -> VERIFYING -> ACTIVE -> ROTATION_PENDING -> ROTATING -> ACTIVE_NEW -> REVOKED | INVALID | COMPROMISED | DELETING -> DELETED`.

Rules:
- imported raw secret is accepted only over a protected backend route and written directly to SecretStore;
- verification returns capability/status evidence, never the secret;
- rotation may use overlap only where provider semantics support it safely;
- compromised/invalid credentials immediately block new exposure for that account and initiate reconciliation/protection assessment;
- revocation/deletion waits for safety checks if the credential is still required to reduce/manage existing exposure, or escalates to explicit emergency handling;
- every lifecycle transition is audited;
- old secret material is destroyed/disabled according to provider and retention semantics.

## 11. Secret Exfiltration Firewall
Raw secrets are classified as `NEVER_LOG / NEVER_TRACE / NEVER_PROMPT / NEVER_EXPORT` data.

Controls must include:
- structured redaction at logging/tracing/error boundaries;
- secret-aware serialization/DTO types that cannot be casually rendered;
- no raw secret in analytics, support screenshots, crash reports or audit payloads;
- CI/build output and artifacts scanned for secret leakage;
- agents/LLMs/tools receive opaque capability references instead of credential values;
- memory dumps/debug endpoints restricted or disabled in sensitive production processes;
- clipboard/reveal UI avoided by default; any future reveal capability requires a separate decision.

## 12. Human Authentication Assurance
Authentication policy is risk-tiered and informed by current digital-identity guidance without claiming external certification.

Baseline:
- phishing-resistant authentication such as passkeys/WebAuthn should be supported and preferred;
- MFA is mandatory for privileged administration and required/strongly enforced for live-trading-capable tenants before production authorization;
- dangerous actions require fresh step-up authentication;
- password fallback, if retained, uses modern password hashing, breached/common-password checks and no arbitrary composition theater;
- authentication events carry assurance level/method into SecurityContext;
- sensitive operations can require a higher assurance than ordinary dashboard reads.

## 13. Account Recovery Security
Recovery is a security-critical state machine, not a support shortcut.

Requirements:
- recovery methods are enrolled/changed under strong authenticated conditions;
- one-time recovery codes are hashed/protected and single-use;
- sensitive recovery can trigger cooling period, out-of-band notification and temporary restriction on credential/admin changes;
- successful recovery revokes or revalidates existing sessions/tokens according to policy;
- owner/super-admin recovery uses a stricter offline/break-glass recovery procedure with immutable evidence;
- support personnel cannot bypass recovery proof merely by editing a database field.

## 14. Session / Token Lifecycle
Sessions/tokens include tenant/user/principal scope, audience, issue/expiry, assurance and security version.

Controls:
- bounded access-token lifetime;
- protected refresh/session token lifecycle and rotation/reuse detection where applicable;
- device/session inventory and selective/global revocation;
- revocation/security-version bump after password/MFA/recovery/role/tenant-critical changes;
- fixation prevention and token-binding/device-risk mechanisms where practical;
- no long-lived bearer token with unrestricted tenant+admin authority;
- logout/revocation propagates to backend authorization and sensitive websocket/private channels within bounded time.

## 15. Workload Identity & Service Authorization
Each backend service/worker category receives a distinct workload principal and least-privileged capabilities.

Requirements:
- short-lived workload credentials/tokens where practical;
- explicit service audience/scope;
- only the exchange execution/credential broker path can resolve raw exchange secret material when required;
- market-data workers do not inherit admin or tenant-secret authority;
- CI/CD identities are different from runtime identities;
- service-to-service authentication is mandatory even inside private networks;
- workload compromise blast radius is documented and bounded.

## 16. Privileged Admin & Break-Glass Boundary
Administrative authority uses a distinct privileged policy/session plane.

Dangerous actions require:
- owner/super-admin identity;
- high-assurance authentication plus recent step-up;
- explicit reason/ticket/incident reference;
- exact scope/blast-radius preview;
- short-lived elevation/authorization lease;
- before/after state snapshots;
- immutable audit and alerting;
- automatic expiry for temporary overrides.

Break-glass credentials/procedure are separate from routine admin sessions, strongly protected, tested, and generate high-severity audit/notification. Initial single-owner policy means two-person approval cannot be assumed; architecture remains ready for future delegated/dual-control roles.

## 17. Support Access / Impersonation Contract
Any future tenant-assistance session preserves two identities simultaneously:
- real support/admin actor;
- assumed tenant/user view/scope.

Default is read-only and cannot access raw secrets. Mutating actions require explicit privileged reauthorization and retain the real actor in every audit/event record.

Support assumption is time-limited, visually obvious, reason/ticket-bound and queryable by audit. Silent impersonation, password takeover, secret reveal and “login as user” without persistent actor attribution are prohibited.

## 18. Tenant-Scoped Harness Authority
Every Harness action uses a typed `CapabilityScope` such as:
`GLOBAL`, `TENANT`, `ACCOUNT`, `EXCHANGE`, `SYMBOL`, `STRATEGY`, `MODEL_AGENT`, `FEATURE`, `RELEASE`.

A tenant/account-scoped control requires an exact Tenant Security Context and dependency/blast-radius calculation. Wildcard/global controls require separate stronger privilege and confirmation.

The Harness must preserve safety actions such as protection/reconciliation while blocking new exposure when a tenant/account is frozen. Scope resolution is tested to prove one tenant’s quarantine cannot spill into another tenant accidentally.

## 19. Entitlement Is Not Authorization
The commercial Entitlement service answers questions such as “is feature X included in this tenant’s plan?” It is not an execution authorization service.

Final operation authority remains the intersection of:
`identity/authentication ∩ tenant membership ∩ authorization policy ∩ entitlement ∩ session policy ∩ Safety/Risk ∩ exchange capability/state`.

A plan upgrade cannot grant admin privileges, bypass Risk or enable unsupported exchange actions. Trial expiry/downgrade/past-due states may stop new optional actions but must preserve required risk-reducing position management, protection and reconciliation for already-open exposure.

## 20. Tenant Resource & Noisy-Neighbor Governor
Shared resource scheduling is hierarchical:
`platform reserve -> safety reserve -> tenant budget -> account/workload budget`.

Governed dimensions include:
- API/rate-limit consumption;
- WS/private/public subscriptions;
- scanner universe/breadth;
- agent/model/token spend;
- replay/Monte Carlo jobs;
- queue depth/concurrency;
- database/storage/egress;
- cache/memory;
- worker CPU/GPU/time.

Emergency/protection/reconciliation traffic retains reserved capacity. A noisy tenant is throttled/degraded locally before unrelated tenants lose safety-critical service. Quota state is visible in tenant/admin observability and cannot silently drop protected work.

## CRITICAL gap closure map
- GAP-01: section 1
- GAP-02: section 2
- GAP-03: section 3
- GAP-04: section 4
- GAP-05: section 5
- GAP-06: section 6
- GAP-07: section 7
- GAP-08: section 8
- GAP-09: section 9
- GAP-10: section 10
- GAP-11: section 11
- GAP-12: section 12
- GAP-13: section 13
- GAP-14: section 14
- GAP-15: section 15
- GAP-16: section 16
- GAP-17: section 17
- GAP-18: section 18
- GAP-19: section 19
- GAP-20: section 20

## Result
All 20 CRITICAL R08 gaps now have explicit planning-resolution contracts. HIGH hardening, requirements/decision consolidation, acceptance gates and final audit remain required before R08 approval.