# UI/UX Design Language

Status: `DISCOVERY_IN_PROGRESS`
Active formalization: `HCT-PLAN-0001-R09`
Risk class: `HIGH_ASSURANCE`

Hive Crypto Trader shares the recognizable visual DNA established across the company's products, with Hive Plan as a reference direction rather than a literal clone. R09 upgrades this file from aesthetic direction into a safety-aware design-system baseline.

## Design intent
- technological, premium and enterprise-grade visual language;
- dark-first desktop trading cockpit with high information density without visual clutter;
- selective 3D/depth, glass/metal/volumetric cues and motion used only to reinforce hierarchy;
- strong realtime visual feedback for market state, execution, connectivity, risk, protection, incidents and intelligence status;
- consistent component, typography, spacing, iconography, motion and accessibility tokens;
- English-first canonical product language with `pt-BR` and `es` localization;
- responsive/mobile views separately capability-governed rather than automatically inheriting desktop authority.

## Non-negotiable hierarchy
Visual priority is:
1. trading authority / emergency state / active tenant-account-environment context;
2. money-at-risk, positions and protection integrity;
3. OMS/execution/reconciliation/state certainty;
4. risk/survival budgets and portfolio exposure;
5. market-data/decision freshness;
6. intelligence and opportunities;
7. research/diagnostics;
8. decorative brand effects.

Profit-oriented presentation never outranks safety or certainty.

## Authoritative-state rule
The frontend is an untrusted projection surface. It does not own exchange truth, risk authority, Safety policy, secrets or privileged business rules.

Realtime authoritative projections are consumed through the R09 Canonical UI State Envelope, which carries the applicable tenant/account/environment, source/generation, version, freshness and authority context.

A frontend may display `PENDING`, `REQUESTED`, `STALE`, `UNKNOWN` and similar presentation states, but it may not optimistically convert them into authoritative fill/cancel/protection/account truth.

## Canonical operational state families
The design system must provide semantic tokens and accessible component behavior for at least:

### Trading authority
- `ALLOW_NEW_EXPOSURE`
- `DEGRADED_NEW_EXPOSURE`
- `NO_NEW_EXPOSURE`
- `REDUCE_ONLY`
- `RECONCILIATION_ONLY`
- `EMERGENCY`

### Realtime confidence
- `LIVE_TRUSTED`
- `LIVE_DEGRADED`
- `STALE`
- `DISCONNECTED`
- `RESYNCING`
- `UNKNOWN`

### Protection
- `PROTECTION_VERIFIED`
- `PROTECTION_DEGRADED`
- `PROTECTION_PARTIAL`
- `PROTECTION_UNKNOWN`
- `PROTECTION_FAILED`

### Operating mode
- `LIVE`
- `PAPER`
- `SHADOW`
- `REPLAY`
- `BACKTEST/RESEARCH`

Meaning may never depend on color alone.

## Accessibility baseline
R09 uses WCAG 2.2-oriented accessibility verification as the minimum web baseline.

Requirements include:
- keyboard-operable critical controls;
- visible/unobscured focus;
- accessible names/roles/status announcements;
- sufficient contrast and non-color-only state;
- reduced-motion equivalents;
- target sizing and drag alternatives where applicable;
- zoom/reflow validation where applicable;
- accessible authentication surfaces inherited from R08.

Accessibility claims require evidence, not merely choosing an accessible component library.

## Realtime integrity
A visually live dashboard must actually be live enough for its declared purpose.

The UI exposes or internally validates:
- state generation;
- last authoritative update;
- data/render age;
- reconnect/resync state;
- contract version;
- stream lag where material.

Stale, disconnected or resyncing data cannot retain a normal `LIVE_TRUSTED` appearance.

## PnL and behavioral safety
PnL remains visible but the UI avoids casino-like reward design. No confetti, reward loops or profit animation may dominate protection, risk, uncertainty or execution state.

## Motion / 3D
Motion and depth are semantic enhancements, never required to understand safety state.

- respect reduced-motion preferences;
- automatically reduce expensive effects under client performance pressure;
- do not use indefinite pulsing for ordinary opportunities;
- do not delay authoritative state updates for animation;
- suppress decorative effects during P0/P1 capital-safety or state-certainty incidents.

## Core product surfaces
- realtime command center / trading cockpit;
- Copilot setup/session UI;
- market universe scanner and opportunity ranking;
- symbol intelligence/chart workspace;
- Strategy Builder and strategy lifecycle;
- indicators/patterns/Brain/agent evidence;
- positions/orders/execution/reconciliation;
- risk, leverage, survival and portfolio exposure;
- Safety Governor / protection / incidents / kill switches;
- RAG memory and decision trace explorer;
- backtest/replay/paper/shadow/promotion laboratory;
- tenant/account settings;
- owner-only Admin/Harness control plane;
- API/WebSocket/data/cache health;
- audit/evidence/diagnostics;
- Signals/Telegram publishing workspace.

## Canonical R09 detail
Detailed contracts live in:
- `docs/76-r09-cockpit-uiux-safety-gap-audit.md`;
- `docs/77-r09-critical-cockpit-safety-architecture.md`;
- `docs/78-r09-uiux-high-hardening.md`;
- `docs/79-r09-acceptance-criteria-and-review-gates.md`;
- `docs/80-r09-cockpit-uiux-requirements-addendum.md`.

## Product rule
A beautiful dashboard that hides risk, uncertainty, stale data, exchange mismatch, protection failure or tenant/account context is a failed dashboard.

Implementation remains unauthorized until the planning process explicitly grants it.
