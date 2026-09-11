# HCT-PLAN-0001-R09 — Acceptance Criteria & Review Gates

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R09`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

## Gate A — UI authority boundary
Frontend is explicitly non-authoritative for exchange, risk, policy and security state and cannot upgrade backend authority.

## Gate B — Canonical UI State Envelope
Realtime authoritative projections carry tenant/account/environment, generation, contract version, source, freshness and authority metadata.

## Gate C — Stale/disconnect firewall
Stale, disconnected, resyncing and unknown data cannot look `LIVE_TRUSTED` and actions requiring fresh state are gated.

## Gate D — Trading-authority action matrix
R05 authority states deterministically control visible/enabled exposure actions; aggregate visual scores cannot override hard state.

## Gate E — Order Evidence Ladder
Acknowledgement, partial fill, fill, cancel request, cancellation and uncertainty remain visually/semantically distinct.

## Gate F — Uncertain/reconciliation conflict UX
Unknown exchange outcomes and contradictory evidence are first-class states with safe action restrictions and reconciliation progress.

## Gate G — Protection integrity
Position/portfolio UI exposes protection confidence, coverage and verification freshness; unknown/failed protection dominates PnL decoration.

## Gate H — Risk survival/OMR
Multi-horizon survival, reserved risk and Operational Margin Reserve remain visible and cannot collapse into one reassuring score.

## Gate I — Current vs projected risk
Current account truth and projected post-trade tier/MMR/leverage/liquidation state are unmistakably separated.

## Gate J — Environment/mode separation
LIVE, PAPER, SHADOW, REPLAY and research/backtest contexts use redundant semantic identity and incompatible mutation capabilities.

## Gate K — Tenant/account/environment context lock
Money-affecting UI persists active context and context switching invalidates unsafe transient/cached state before new actions.

## Gate L — Dangerous actions
High-impact actions show exact scope/consequence, applicable step-up/reason/blast-radius and authoritative completion evidence.

## Gate M — Trading-aware emergency controls
Kill switch/blackout UX communicates preserved protection, risk-reduction and reconciliation behavior rather than implying blind shutdown.

## Gate N — No optimistic money-state mutation
Orders, fills, positions, balances, margin, risk reservations and protection use pending states until authoritative completion evidence.

## Gate O — Privileged identity projection
Admin/support/elevated/break-glass context is persistent, explicit, auditable and never silently impersonates a tenant.

## Gate P — Tenant-safe frontend data
Browser cache/search/storage/notification/export/error paths respect R08 tenant and data-classification boundaries.

## Gate Q — Decision freshness
Opportunities and candidate actions expose age/expiry/revalidation state end to end.

## Gate R — Critical accessibility
Critical states do not rely solely on color/motion/sound and support keyboard/focus/AT semantics and reduced motion.

## Gate S — Safety priority scheduler
P0/P1 capital-safety/state-certainty communication pre-empts lower-priority PnL/opportunity/decorative effects.

## Gate T — Reconnect/resync proof
Transport reconnect does not restore trusted presentation until generation synchronization and required reconciliation proof succeed.

## Gate U — Information hierarchy
Mandatory authority/context/protection/execution/risk surfaces remain visible across supported density and responsive modes.

## Gate V — Chart truth
Executed, confirmed, provisional and hypothetical overlays have source/timeframe/generation/version/mode provenance and distinct semantics.

## Gate W — Intelligence semantics
Directional probability, opportunity quality, data confidence, calibration, feasibility and risk compatibility remain separate; agent consensus cannot appear authoritative over hard gates.

## Gate X — Strategy Builder safety
Typed nodal authoring exposes compile/static-validation/version/promotion state and cannot mutate an active version in place.

## Gate Y — Realtime UI performance
Client update/render budgets, lag detection, coalescing/virtualization and explicit degraded presentation prevent silent visual staleness.

## Gate Z — Alert lifecycle
Alerts have priority, deduplication, acknowledgement/resolution/escalation and safety-critical mute restrictions.

## Gate AA — Audit trace
Point-in-time decision/action traces are inspectable without exposing secrets or private chain-of-thought.

## Gate AB — Accessibility verification
WCAG 2.2-oriented automated/manual verification plan covers focus, keyboard, status messages, contrast, zoom/reflow, target size, drag alternatives and motion.

## Gate AC — Localization/time semantics
Financial numbers, canonical state meaning, exchange/user time and relative age remain unambiguous across locale/timezone changes.

## Gate AD — Offline/error/observability/design-system consistency
Offline, loading, unknown, partial and error states never masquerade as safe zero/healthy state; semantic design tokens and frontend observability make state meaning and staleness consistent/diagnosable.

## Verdict rule
- unresolved CRITICAL/HIGH R09 planning defect => `CORRECTION REQUIRED`;
- missing authoritative dependency necessary for planning => `BLOCKED`;
- all gates pass and canonical sources agree => `APPROVED`.

R09 approval is planning-only. It never authorizes frontend implementation, production deployment, credentials, limited-live operation or real-money trading.
