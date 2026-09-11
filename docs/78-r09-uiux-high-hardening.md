# HCT-PLAN-0001-R09 — UI/UX HIGH-Severity Hardening

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R09`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

## Purpose
Resolve GAP-R09-20 through GAP-R09-38. These controls improve operability, accessibility, interpretability and resilience without changing backend trading authority.

## 20. Operational information hierarchy
Cockpit hierarchy is fixed by safety relevance, not visual novelty:
1. authority/safety/account context;
2. open money-at-risk and protection;
3. order/execution/reconciliation state;
4. risk budgets/exposure;
5. market/decision freshness;
6. intelligence/opportunity;
7. research/diagnostics;
8. decorative/brand treatment.

Support density presets such as `STANDARD`, `DENSE`, `FOCUS` while preserving mandatory safety chrome.

## 21. Chart Truth Contract
Every rendered overlay/annotation may expose:
- source domain;
- symbol/timeframe;
- data generation;
- strategy/indicator/model version;
- computed timestamp;
- provisional/final/hypothetical status;
- live/paper/shadow/replay identity.

Actual fills and protection use visually and semantically different markers from signals, candidates and counterfactual paths.

## 22. PnL de-emphasis rule
PnL is visible but does not receive stronger motion, saturation, screen area or alert priority than risk/protection/state certainty. No confetti, casino-like celebration or urgency loops in trading surfaces.

## 23. Realtime frontend performance budget
Define measurable budgets for:
- input-to-render latency;
- stream-to-visible-state age;
- maximum retained chart points per viewport;
- virtualization thresholds;
- update coalescing;
- dropped-frame/update telemetry;
- client memory/CPU budgets.

When the client cannot keep up, it degrades explicitly and surfaces render lag rather than silently showing old data.

## 24. Alert lifecycle and fatigue control
Alerts have:
- severity and safety priority;
- deduplication key;
- first/last occurrence;
- count;
- acknowledgement state;
- expiry/resolution semantics;
- escalation rules;
- source/correlation identity.

P0/P1 alerts cannot be permanently muted through ordinary user preference.

## 25. Decision/audit trace explorer
Audit UX should reconstruct:
- point-in-time market/account context;
- strategy/Brain evidence inputs and exclusions;
- model/agent/tool versions;
- Safety/Risk/Policy decisions;
- order/OMS/reconciliation timeline;
- matured outcome.

The explorer exposes structured evidence and reason codes, not hidden private chain-of-thought or raw secrets.

## 26. Intelligence semantic decomposition
Do not show a single generic confidence percentage. Use clearly labeled dimensions such as:
- directional probability;
- opportunity quality;
- data confidence;
- calibration reliability;
- historical support;
- execution feasibility;
- risk compatibility;
- decision stability.

Missing/untrusted calibration is represented explicitly.

## 27. Agent evidence visualization
Agent nodes visualize evidence production and disagreement, not democratic voting power. The graph terminates through Supervisor then deterministic Safety/Risk/Policy/Execution gates. `AGREE x 9` cannot visually imply authority to override one failed hard gate.

## 28. Strategy Builder safety UX
The nodal Strategy Builder requires:
- typed ports and incompatible-link prevention;
- graph validation state;
- compiler/static-analysis findings;
- immutable version/hash after publish;
- clear `DRAFT`, `RESEARCH`, `PAPER`, `SHADOW`, `PRODUCTION_ELIGIBLE`, `ACTIVE`, `QUARANTINED`, `RETIRED` status;
- promotion evidence links;
- no direct arbitrary code/network/filesystem/SecretStore control.

Editing an active version creates a new draft/version rather than mutating live behavior in place.

## 29. Accessibility verification plan
R09 planning adopts WCAG 2.2 as the minimum web accessibility baseline. Verification combines automated and manual tests covering:
- keyboard-only operation;
- visible/unobscured focus;
- screen-reader names, roles and status announcements;
- contrast and non-color-only state;
- 200%+ zoom/reflow where applicable;
- target size;
- accessible authentication surfaces inherited from R08;
- drag alternatives;
- reduced motion;
- high-density data/table/chart alternatives where feasible.

Accessibility conformance claims require evidence, not library choice.

## 30. Motion/depth governance
Motion and 3D/depth are semantic tools, not baseline requirements.

Rules:
- obey reduced-motion preference;
- no motion required to understand critical state;
- no indefinite pulsing for noncritical opportunity;
- expensive effects automatically reduce under client performance pressure;
- motion never delays command acknowledgement/state updates.

## 31. Locale-safe numbers and financial semantics
Canonical numeric values are transmitted independent of locale formatting. The UI localizes display only.

Requirements:
- unambiguous decimal/group separators;
- explicit currency/unit;
- explicit `%` and leverage `x`;
- sufficient precision for price/quantity without hiding canonical exchange increments;
- no locale translation of canonical state IDs in machine contracts;
- localized labels cannot change Safety/Risk meaning.

## 32. Time Semantics Standard
Every temporal surface distinguishes when relevant:
- exchange/event time;
- HCT receive/knowledge time;
- user-local display time;
- elapsed age;
- latency.

Relative times (`3s ago`) should have inspectable exact timestamp. Session/day boundaries follow policy/exchange definitions, not browser timezone guesswork.

## 33. Responsive/mobile capability policy
Initial R09 direction:
- desktop/web is the authoritative full operations surface;
- mobile may support monitoring, alerts, acknowledgement and narrowly approved risk-reducing actions only after separate validation;
- mobile does not automatically inherit every desktop money-affecting action;
- hidden/compact responsive layouts cannot remove mandatory authority/context/protection indicators.

## 34. Export/redaction policy
Exports and reports classify fields by sensitivity. Tenant/account identifiers, private strategy data, audit identities and operational internals follow R08 authorization/redaction. Raw secrets are never exportable.

## 35. Offline/read-only workspace
When backend authority is unavailable, the UI may expose cached/history/research content under persistent `OFFLINE_READ_ONLY` identity. Live trading mutation controls are removed/disabled and cached financial state includes last-authoritative timestamp.

## 36. Safe zero/loading/error semantics
A missing value is never coerced into a reassuring zero.

Examples:
- unknown position != zero position;
- loading orders != no orders;
- protection query failure != protected;
- empty incident response due error != healthy;
- missing PnL != zero PnL.

Use explicit `LOADING`, `UNAVAILABLE`, `UNKNOWN`, `PARTIAL`, `ERROR` states.

## 37. Semantic design-token model
Design system defines semantic tokens such as:
- `authority.allow/degraded/block/reduce/reconcile/emergency`;
- `protection.verified/degraded/partial/unknown/failed`;
- `data.live/degraded/stale/disconnected/resyncing`;
- `evidence.confirmed/provisional/hypothetical`;
- `environment.live/paper/shadow/replay`;
- `severity.info/warning/high/critical`.

Components consume semantic tokens rather than hard-coded colors. Themes map tokens to accessible visual treatments.

## 38. Client/UI observability
Frontend telemetry includes, without tenant-secret leakage:
- active contract version;
- stream generation/subscription state;
- server-to-client and client render age;
- resync duration;
- dropped/coalesced updates;
- render-loop lag;
- chart worker failures;
- websocket/SSE client state;
- UI state-envelope validation errors;
- stale-state transitions;
- action-intent-to-authoritative-result latency.

Client telemetry cannot become a second source of account truth.

## R09 design-system direction
The product may remain visually premium, dark-first, high-density and selectively volumetric. The safety rule is stronger: visual sophistication is accepted only when it preserves semantic hierarchy, accessibility, latency awareness and state certainty.

These contracts resolve the 19 HIGH gaps at planning level. Implementation remains unauthorized.
