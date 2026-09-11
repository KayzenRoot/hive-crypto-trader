# HCT-PLAN-0001-R09 — Decision Proposals for Ledger Consolidation

Status: `CONSOLIDATED`
Increment: `HCT-PLAN-0001-R09`
Date: `2026-09-11`

`HCT-DEC-0104` through `HCT-DEC-0117` were accepted during R09 planning and are now consolidated into `docs/10-decisions-ledger.md`. This file remains as round-local provenance and must not be treated as a competing decisions source.

## HCT-DEC-0104 — Frontend is a non-authoritative projection governed by a Canonical UI State Envelope
Status: APPROVED_FOR_DISCOVERY

Decision: authoritative realtime cockpit projections use a versioned UI State Envelope containing tenant/account/environment, generation, schema/version, source, freshness and trading-authority metadata. The frontend may derive presentation but cannot infer or upgrade stronger exchange/risk/security authority than the backend supplied.

## HCT-DEC-0105 — Stale, disconnected and resyncing state deterministically restricts UI authority
Status: APPROVED_FOR_DISCOVERY

Decision: realtime UI distinguishes `LIVE_TRUSTED`, `LIVE_DEGRADED`, `STALE`, `DISCONNECTED`, `RESYNCING` and `UNKNOWN`. R05 authority states map to a deterministic action matrix. Transport reconnection alone never restores trusted-live presentation; generation synchronization and required reconciliation proof must complete first.

## HCT-DEC-0106 — Order UI follows the exchange evidence ladder and never optimistically invents economic truth
Status: APPROVED_FOR_DISCOVERY

Decision: intent, submit, acknowledgement, partial fill, fill, cancel/replace pending, uncertain, reconciliation and terminal states remain distinct. Acknowledgement is not fill; cancel request is not cancellation; timeout is not failure when venue outcome is unknown. Money/risk/order/protection state cannot be optimistically marked complete client-side.

## HCT-DEC-0107 — Protection integrity and multi-horizon survival outrank PnL presentation
Status: APPROVED_FOR_DISCOVERY

Decision: open-position/cockpit UI exposes protection confidence/coverage/freshness plus monetary/reserved risk, survival budgets and Operational Margin Reserve. Unknown/failed protection and survival restrictions visually outrank profit/opportunity content and cannot disappear inside a composite score.

## HCT-DEC-0108 — Current truth, projected post-trade risk and decision freshness remain separate
Status: APPROVED_FOR_DISCOVERY

Decision: current tier/MMR/leverage/liquidation/risk truth is distinct from projected post-fill state. Opportunities/actions expose applicable data-to-decision age, remaining signal lifetime, expiry and Risk/Execution revalidation state.

## HCT-DEC-0109 — LIVE/PAPER/SHADOW/REPLAY and tenant/account/environment contexts are locked and unmistakable
Status: APPROVED_FOR_DISCOVERY

Decision: environment/mode identity uses redundant text/icon/layout semantics, not color alone. Money-affecting surfaces persist active tenant, exchange account and environment. Context switching invalidates unsafe transient/cached state and loads newly authorized authoritative state before actions resume.

## HCT-DEC-0110 — Dangerous and emergency actions use trading-aware consequence semantics
Status: APPROVED_FOR_DISCOVERY

Decision: close-all, cancel-all, freeze, blackout, credential revoke, rollback/quarantine and comparable actions expose exact scope/consequence, applicable step-up/reason/blast radius and authoritative completion evidence. Emergency blackout communicates preserved protection, risk-reducing actions and reconciliation instead of implying blind shutdown.

## HCT-DEC-0111 — Privileged UI context and tenant-sensitive client data are explicit security boundaries
Status: APPROVED_FOR_DISCOVERY

Decision: admin/support/elevation/break-glass context is persistent and retains the real actor identity. Browser caches/storage/search/notifications/exports/errors/telemetry obey R08 tenant/data-classification boundaries and are invalidated appropriately on context switch, logout or revocation.

## HCT-DEC-0112 — Safety communication is accessible and pre-empts lower-priority visual effects
Status: APPROVED_FOR_DISCOVERY

Decision: critical state cannot rely only on color, motion, sound or hover. It uses semantic text/icon/structure, keyboard/focus and assistive-technology behavior with reduced-motion equivalents. A UI priority scheduler ensures capital-safety/state-certainty events suppress lower-priority PnL/opportunity/decorative effects.

## HCT-DEC-0113 — Chart, Brain and agent visualization preserve evidence semantics rather than fabricate authority
Status: APPROVED_FOR_DISCOVERY

Decision: executed/confirmed/provisional/hypothetical chart elements carry source/timeframe/version/generation/mode semantics. Brain dimensions remain separated rather than collapsed into one confidence percentage. Agent agreement is visualized as evidence and cannot appear to override deterministic Safety/Risk/Policy gates.

## HCT-DEC-0114 — Realtime UI performance degradation must be observable and explicit
Status: APPROVED_FOR_DISCOVERY

Decision: frontend render/update budgets, virtualization/coalescing and client-lag telemetry are planned as integrity controls. A client that cannot keep up visibly degrades rather than silently displaying stale information. Alerts use governed priority, deduplication, acknowledgement, resolution and escalation semantics.

## HCT-DEC-0115 — Strategy authoring and audit UX are versioned, immutable and evidence-linked
Status: APPROVED_FOR_DISCOVERY

Decision: the nodal Strategy Builder uses typed validation, immutable published versions and explicit research/paper/shadow/production eligibility lifecycle; editing active behavior creates a new candidate version. Executed actions can be explored through structured point-in-time decision/audit traces without exposing raw secrets or private chain-of-thought.

## HCT-DEC-0116 — WCAG 2.2-oriented accessibility and semantic design tokens are design-system requirements
Status: APPROVED_FOR_DISCOVERY

Decision: R09 adopts WCAG 2.2-oriented automated/manual accessibility verification as the minimum web baseline. Motion/depth obey reduced-motion and performance constraints. Authority/protection/data/evidence/environment/severity use semantic design tokens independent of hard-coded colors. Localization/time formatting cannot change canonical financial/risk meaning.

## HCT-DEC-0117 — Mobile, offline, export and unknown-state behavior are restrictive by default
Status: APPROVED_FOR_DISCOVERY

Decision: the full command center is desktop/web-first. Mobile does not automatically inherit desktop money authority. Loss of backend authority creates explicit offline/read-only behavior. Missing/loading/error/partial data never becomes reassuring zero/healthy state. Exports obey R08 classification, and frontend observability diagnoses state age/lag without becoming account truth.
