# HCT-PLAN-0001-R09 — Realtime Cockpit, UI/UX & Safety Communication Gap Audit

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R09`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`
Initial verdict: `CORRECTION REQUIRED`

## Objective
Audit the existing cockpit/UI pre-discovery material against the approved R03–R08 authority, risk, execution, realtime, intelligence, validation and multi-tenant contracts.

The UI is not authoritative trading state. It is a safety-critical projection of backend-authoritative state. A beautiful screen that is stale, ambiguous or optimistic is a defect.

Primary pre-discovery inputs:
- `docs/04-architecture.md`;
- `docs/16-ui-ux-design-language.md`;
- `docs/19-copilot-cockpit-and-strategy-visualization.md`;
- `docs/20-admin-control-plane-and-harness.md`;
- R03 risk/survival/protection contracts;
- R04 OMS/reconciliation/evidence contracts;
- R05 realtime/freshness/authority contracts;
- R06 Brain/evidence/abstention contracts;
- R07 replay/paper/shadow/promotion contracts;
- R08 SecurityContext/tenant/admin/secret contracts.

Accessibility baseline: WCAG 2.2 / ISO/IEC 40500:2025 principles, including non-color-only status communication, keyboard/focus access, target sizing and assistive-technology status announcements.

## CRITICAL gaps

### GAP-R09-01 — Canonical UI State Envelope
The frontend lacks a formal contract proving which backend authority state, generation, tenant/account, data age and version a rendered trading state belongs to.

### GAP-R09-02 — Stale/Disconnected UI cannot look live
No formal rule currently prevents stale cached values or disconnected realtime streams from retaining a visually normal/live appearance.

### GAP-R09-03 — Trading-authority state must dominate UI
`ALLOW_NEW_EXPOSURE`, `DEGRADED_NEW_EXPOSURE`, `NO_NEW_EXPOSURE`, `REDUCE_ONLY`, `RECONCILIATION_ONLY` and `EMERGENCY` need deterministic presentation and action gating, not generic warning badges.

### GAP-R09-04 — Command acknowledgement vs fill semantics
The UI must not display an acknowledged order as filled, cancelled or economically resolved until stronger exchange/reconciliation evidence exists.

### GAP-R09-05 — Unknown/uncertain order state
`UNCERTAIN`, cancel-pending, replace-pending and reconciliation-conflict states require first-class UI semantics and must block misleading retry affordances.

### GAP-R09-06 — Protection integrity visibility
`PROTECTION_VERIFIED`, `PROTECTION_DEGRADED`, `PROTECTION_PARTIAL`, `PROTECTION_UNKNOWN`, `PROTECTION_FAILED` need explicit position-level and portfolio-level visualization.

### GAP-R09-07 — Risk survival state visibility
Trade/day/week/month/account survival states and Operational Margin Reserve cannot be collapsed into a single green/red risk score.

### GAP-R09-08 — Liquidation/tier/MMR truth
Projected/current risk tier, MMR, liquidation corridor and post-trade preview require authoritative timestamp/provenance and clear current-vs-projected distinction.

### GAP-R09-09 — Live / paper / shadow / replay separation
Actual live state, paper state, shadow hypotheses and historical replay must be impossible to confuse by color theme alone.

### GAP-R09-10 — Tenant/account/exchange context lock
Every money-affecting screen/action must show the active tenant, exchange account and environment with mismatch-safe switching behavior.

### GAP-R09-11 — Dangerous action confirmation contract
Close-all, cancel-all, pause, blackout, credential revoke, account freeze and similar actions need consequence preview, scope, step-up requirements where applicable and authoritative completion evidence.

### GAP-R09-12 — Kill switch semantics
Emergency controls must communicate exactly what remains allowed: protection, risk-reducing close, reconciliation and recovery, rather than implying all processes stop.

### GAP-R09-13 — Frontend optimistic state prohibition
Money/risk/order/protection state may not be optimistically mutated client-side as if authoritative before backend/exchange evidence confirms it.

### GAP-R09-14 — SecurityContext / privilege projection
Admin/support/tenant mode, assumed support context and privilege elevation need explicit persistent UI context so privileged actions cannot occur under hidden identity state.

### GAP-R09-15 — Cross-tenant/admin data leakage through UI
Search, autocomplete, cached views, browser storage, notifications, exports and error messages need tenant-safe boundaries.

### GAP-R09-16 — Decision freshness propagation
The Decision Freshness Envelope and signal expiry need visible age/expiry semantics at opportunity, Brain, Risk and execution surfaces.

### GAP-R09-17 — Accessibility of critical state
Critical state cannot rely only on red/green, animation, sound or hover. It needs text/icon/structure, keyboard/focus support and assistive-technology announcements.

### GAP-R09-18 — Safety notification precedence
Profit, opportunity and decorative animations must be pre-empted/suppressed by higher-priority safety, stale-data, exchange-uncertainty and protection-failure states.

### GAP-R09-19 — Reconnect/resync transition safety
After reconnect, the UI cannot resume normal trading appearance until synchronization/reconciliation proof says the projected state is trustworthy.

## HIGH gaps

### GAP-R09-20 — Information hierarchy and density modes
Define operational hierarchy, progressive disclosure and density presets so critical information stays visible at high data volume.

### GAP-R09-21 — Chart truth/provenance
Chart overlays need source/timeframe/generation/version provenance and explicit distinction between confirmed, provisional and hypothetical annotations.

### GAP-R09-22 — PnL salience bias
UI must avoid making profit/loss animation visually stronger than risk, uncertainty or exposure, reducing behavioral pressure toward unsafe action.

### GAP-R09-23 — Realtime performance budget
Define render/update/interaction budgets, virtualization/coalescing and graceful degradation so UI load cannot create stale presentation without warning.

### GAP-R09-24 — Notification fatigue / alert deduplication
Critical alerts need priority, deduplication, acknowledgement/escalation and suppression rules to prevent alarm blindness.

### GAP-R09-25 — Audit trace UX
Executed actions need navigable, point-in-time decision traces without exposing private chain-of-thought or raw secrets.

### GAP-R09-26 — Brain confidence semantics
Probability, opportunity quality, data confidence, calibration reliability, execution feasibility and risk compatibility must not be merged into one misleading percentage.

### GAP-R09-27 — Agent visualization semantics
Agent agreement/disagreement is evidence, not authority. Visual voting must not imply that majority opinion overrides Safety/Risk.

### GAP-R09-28 — User strategy builder safety UX
Typed nodal strategy UI needs compile/validation errors, incompatible-port prevention, version identity, simulation/live eligibility and explicit unpublished/unpromoted state.

### GAP-R09-29 — Accessibility test strategy
Define automated/manual accessibility tests for keyboard, focus, contrast, status messages, zoom/reflow, target size and reduced motion.

### GAP-R09-30 — Reduced motion / animation governance
3D, depth and motion require reduced-motion behavior and hard caps so decoration cannot interfere with latency or cognition.

### GAP-R09-31 — Localization of numeric/risk semantics
Locale may format text/numbers, but decimals, percentages, prices, leverage and canonical risk meaning must remain unambiguous.

### GAP-R09-32 — Time-zone and timestamp semantics
Exchange event time, local/user time and age/latency need explicit labels to avoid temporal misinterpretation.

### GAP-R09-33 — Responsive/mobile authority scope
Define which operations, if any, may be performed on mobile; default to safer read-only/restricted behavior until separately validated.

### GAP-R09-34 — Export/screenshot privacy
Exports, screenshots and downloadable reports need tenant/account/privacy-aware redaction policy.

### GAP-R09-35 — Offline/read-only mode
If backend connectivity is lost, cached historical information may remain viewable only with unmistakable offline/read-only state and disabled privileged actions.

### GAP-R09-36 — Empty/error/loading state safety
Loading, partial data, API error and unknown state must never be rendered as zero exposure, no orders, healthy protection or no incident.

### GAP-R09-37 — Design-system semantic tokens
Risk/authority/protection/data-quality states need semantic design tokens independent from specific colors/themes to keep meaning consistent across products and accessibility modes.

### GAP-R09-38 — UI contract observability
Measure client generation, stream lag, render age, dropped updates, client errors and contract-version mismatch so visual staleness is diagnosable.

## Initial assessment
The pre-discovery UX vision is directionally strong and already prioritizes safety over decoration. However, R09 cannot be approved until the 38 gaps above are converted into explicit architecture, requirements, decisions and objective acceptance gates.

## Verdict rule
Any unresolved CRITICAL/HIGH R09 planning defect keeps the verdict at `CORRECTION REQUIRED`. Missing authoritative dependency required to plan safely yields `BLOCKED`. Approval does not authorize frontend implementation, deployment, production credentials or live trading.
