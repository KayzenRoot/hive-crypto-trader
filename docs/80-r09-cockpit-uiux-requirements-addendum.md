# HCT-PLAN-0001-R09 — Realtime Cockpit & UI/UX Requirements Addendum

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R09`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

This addendum is canonical together with `docs/02-requirements.md` until planning-freeze consolidation.

## R09-REQ-001 — Frontend authority boundary
The frontend SHALL remain an untrusted presentation/client surface. It SHALL NOT contain or infer authoritative exchange, risk, policy, secret-signing or privileged security logic.

## R09-REQ-002 — UI State Envelope
Authoritative realtime projections SHALL include sufficient tenant/account/environment, generation, schema/version, source, freshness and authority metadata for the client to validate/render state safely.

## R09-REQ-003 — Explicit freshness
Realtime components SHALL expose trusted/degraded/stale/disconnected/resyncing/unknown state and SHALL NOT present stale or unknown state as live healthy state.

## R09-REQ-004 — Authority-driven actions
R05 authority states SHALL deterministically restrict frontend exposure-increasing, reducing and recovery actions. Client affordances SHALL be subordinate to backend authorization.

## R09-REQ-005 — Order evidence semantics
Order acknowledgement, fills, cancel/replace requests, cancellations and unknown outcomes SHALL remain semantically distinct. A desired/requested state SHALL NOT be presented as completed without authoritative evidence.

## R09-REQ-006 — Reconciliation uncertainty
Exchange uncertainty and reconciliation conflicts SHALL be first-class visible states with safe retry/action restrictions.

## R09-REQ-007 — Protection integrity
Open-position UI SHALL expose protection-confidence state, verified coverage and verification freshness. Unknown/failed protection SHALL receive safety-critical visual priority.

## R09-REQ-008 — Risk/survival visibility
The cockpit SHALL expose relevant monetary risk, reserved risk, multi-horizon survival state, portfolio exposure and Operational Margin Reserve without hiding failed hard conditions behind a composite score.

## R09-REQ-009 — Projected risk distinction
Current and projected post-trade tier/MMR/leverage/liquidation/risk state SHALL be visually and semantically distinct.

## R09-REQ-010 — Environment/mode separation
LIVE, PAPER, SHADOW, REPLAY and research/backtest surfaces SHALL use redundant non-color-only identification and capability separation.

## R09-REQ-011 — Context lock
Money-affecting screens SHALL persist active tenant, exchange account and environment/mode. Context switching SHALL invalidate unsafe transient state and require newly authorized/current data before actions resume.

## R09-REQ-012 — Dangerous-action confirmation
High-impact operational/admin actions SHALL present exact scope/consequence and applicable privilege/step-up/reason/blast-radius controls before execution, then show authoritative outcome/audit identity.

## R09-REQ-013 — Emergency semantics
Kill-switch/blackout UI SHALL accurately communicate preserved risk-reducing, protection and reconciliation behavior.

## R09-REQ-014 — No optimistic money truth
Orders, fills, balances, positions, risk reservations, margin and protection SHALL not be optimistically marked complete client-side.

## R09-REQ-015 — Privilege context
Admin/support/elevation/break-glass context SHALL be persistent, explicit and auditable. Support assumption SHALL retain the real actor identity.

## R09-REQ-016 — Tenant-safe client data
Frontend caches, storage, search/autocomplete, notifications, exports, errors and telemetry SHALL preserve R08 tenant isolation and data-classification boundaries.

## R09-REQ-017 — Decision freshness
Opportunity/Brain/Risk/Execution presentation SHALL expose applicable decision age, expiry and revalidation state.

## R09-REQ-018 — Critical accessibility
Safety-critical states SHALL be perceivable and operable without depending only on color, animation, hover or sound, and SHALL support keyboard/focus/assistive-technology semantics.

## R09-REQ-019 — Safety priority
Capital-safety and state-certainty messages SHALL pre-empt lower-priority opportunity/PnL/decorative effects.

## R09-REQ-020 — Reconnect/resync
Frontend transport reconnection SHALL NOT restore trusted-live presentation until synchronization and required reconciliation/state-confidence proof completes.

## R09-REQ-021 — Operational hierarchy
Required authority, context, money-at-risk, protection, execution and risk information SHALL remain visible in supported density/responsive modes.

## R09-REQ-022 — Chart provenance
Executed, confirmed, provisional and hypothetical chart elements SHALL be distinguishable and carry sufficient source/timeframe/version/mode provenance.

## R09-REQ-023 — PnL de-emphasis
The product SHALL avoid casino-like reward design and SHALL NOT visually prioritize PnL over protection, risk or uncertainty.

## R09-REQ-024 — UI performance integrity
The frontend SHALL define/render/stream performance budgets and detect/surface client lag or dropped/coalesced updates rather than silently displaying stale information.

## R09-REQ-025 — Alert lifecycle
Operational alerts SHALL support severity/priority, deduplication, acknowledgement, resolution and escalation. Critical safety alerts SHALL NOT be permanently suppressible by ordinary preferences.

## R09-REQ-026 — Audit trace
Executed actions SHALL be explorable as structured point-in-time traces of evidence, strategy/Brain, Safety/Risk/Policy, OMS/reconciliation and outcome without exposing raw secrets or private chain-of-thought.

## R09-REQ-027 — Intelligence decomposition
The UI SHALL keep directional probability, opportunity quality, data confidence, calibration reliability, historical support, execution feasibility and risk compatibility semantically separate.

## R09-REQ-028 — Agent authority representation
Agent visualization SHALL represent agents as evidence producers and SHALL NOT imply that majority agreement can override deterministic Safety/Risk/Policy gates.

## R09-REQ-029 — Strategy Builder states
The nodal Strategy Builder SHALL provide typed validation/static-analysis/version identity and governed lifecycle/promotion status. Active versions SHALL be immutable.

## R09-REQ-030 — Accessibility verification
Frontend acceptance SHALL include WCAG 2.2-oriented automated and manual accessibility evidence covering keyboard/focus, contrast, status messages, target size, zoom/reflow, drag alternatives and reduced motion where applicable.

## R09-REQ-031 — Motion governance
3D/depth/motion SHALL be optional semantic enhancement, obey reduced-motion preferences and never delay or obscure authoritative state updates.

## R09-REQ-032 — Financial localization
Locale formatting SHALL NOT change canonical financial/risk semantics. Currency, units, percentages, leverage and precision SHALL remain unambiguous.

## R09-REQ-033 — Time semantics
The UI SHALL distinguish relevant exchange/event time, HCT receive/knowledge time, user-local time, age and latency.

## R09-REQ-034 — Mobile/restricted capability
Mobile/responsive surfaces SHALL NOT implicitly inherit all desktop trading authority. Money-affecting mobile capabilities require separate validation and policy.

## R09-REQ-035 — Export privacy
UI exports/downloads SHALL respect tenant/data classification and SHALL never include raw credentials/secrets.

## R09-REQ-036 — Offline mode
Loss of backend authority SHALL place supported cached/history surfaces into explicit `OFFLINE_READ_ONLY` or equivalent restricted state and disable privileged live mutations.

## R09-REQ-037 — Safe unknown semantics
Missing/loading/error/partial data SHALL NOT be coerced into reassuring zero, no-order, no-position, healthy-protection or no-incident states.

## R09-REQ-038 — Semantic design tokens
The design system SHALL define semantic authority/protection/data-quality/evidence/environment/severity tokens independent of hard-coded theme colors.

## R09-REQ-039 — Frontend observability
HCT SHALL observe client contract version, stream generation, lag/render age, resync, dropped/coalesced updates, UI envelope-validation failures and action-to-authoritative-result latency without making frontend telemetry a source of account truth.

## R09-REQ-040 — Desktop-first command center
The initial full operational cockpit SHALL be desktop/web-first, high-density and dark-first while preserving accessibility and safety hierarchy. Mobile scope remains separately governed.

## Scope invariant
These requirements specify planning and validation contracts. They do not authorize frontend implementation, production deployment, credentials, limited-live activation or real-money trading.
