# HCT-PLAN-0001-R09 — Critical Cockpit Safety Architecture

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R09`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

## Purpose
Resolve GAP-R09-01 through GAP-R09-19 with explicit UI safety contracts. The frontend remains an untrusted projection surface. It never upgrades trading authority and never manufactures exchange truth.

## 1. Canonical UI State Envelope
Every realtime authoritative projection consumed by the cockpit must carry a versioned `UIStateEnvelope` containing, as applicable:
- `tenant_id`;
- `exchange_account_id`;
- `environment`;
- backend contract/schema version;
- source domain and authoritative state identity;
- market/account generation IDs;
- backend event/knowledge/receive time;
- frontend receive time;
- freshness/expiry policy;
- reconciliation/state-confidence status;
- current trading-authority state;
- correlation/trace identity.

The frontend may derive presentation state from this envelope but may not infer a stronger authority state than the backend provided.

## 2. Freshness classes and stale-state firewall
Every realtime component is classified as:
- `LIVE_TRUSTED`;
- `LIVE_DEGRADED`;
- `STALE`;
- `DISCONNECTED`;
- `RESYNCING`;
- `UNKNOWN`.

Rules:
- age/freshness is computed from authoritative timestamps and monotonic client timing where possible;
- stale/disconnected/resyncing data never retains normal live styling;
- actions requiring fresh state are disabled when their prerequisite envelope is stale/unknown;
- cached values may remain visible for context only with explicit age and non-authoritative labeling;
- reconnect never clears degraded styling by transport connection alone.

## 3. Trading Authority Banner and Action Matrix
The cockpit maintains one persistent top-level authority projection derived from R05:
- `ALLOW_NEW_EXPOSURE`;
- `DEGRADED_NEW_EXPOSURE`;
- `NO_NEW_EXPOSURE`;
- `REDUCE_ONLY`;
- `RECONCILIATION_ONLY`;
- `EMERGENCY`.

Each state maps to a deterministic action matrix. Example:
- `ALLOW_NEW_EXPOSURE`: actions still require all normal Safety/Risk/Policy gates;
- `DEGRADED_NEW_EXPOSURE`: only policy-approved reduced authority, with visible cause;
- `NO_NEW_EXPOSURE`: create/add/reopen controls disabled;
- `REDUCE_ONLY`: only exposure-reducing actions permitted;
- `RECONCILIATION_ONLY`: trading mutation controls disabled except explicitly governed recovery actions;
- `EMERGENCY`: emergency policy view dominates and only whitelisted protective/recovery operations appear.

A decorative score cannot override this matrix.

## 4. Order Evidence Ladder in UI
Order presentation mirrors R04 evidence levels.

Distinct visible states include:
`INTENT_CREATED -> COMMAND_AUTHORIZED -> SUBMITTING -> ACKNOWLEDGED -> PARTIALLY_FILLED -> FILLED`
plus mutation/recovery states such as:
`CANCEL_REQUESTED`, `CANCEL_PENDING`, `REPLACE_PENDING`, `UNCERTAIN`, `RECONCILING`, `REJECTED`, `CANCELLED`, `EXPIRED`.

Rules:
- acknowledgement is never rendered as fill;
- cancel request is never rendered as cancelled;
- local timeout is never rendered as failed if exchange outcome is unknown;
- economic PnL/position effects are displayed only from authoritative fill/reconciliation evidence;
- duplicate retry affordances are suppressed while outcome is unresolved.

## 5. Uncertainty and conflict surface
`UNCERTAIN` and reconciliation conflicts are first-class objects with:
- affected order/position/account;
- last known authoritative evidence;
- missing/contradictory evidence;
- current allowed actions;
- reconciliation progress;
- explicit warning that state may differ at the exchange.

No generic spinner may represent monetary uncertainty.

## 6. Protection Integrity Contract
Every open position exposes protection confidence:
- `PROTECTION_VERIFIED`;
- `PROTECTION_DEGRADED`;
- `PROTECTION_PARTIAL`;
- `PROTECTION_UNKNOWN`;
- `PROTECTION_FAILED`.

The cockpit shows:
- required protective quantity;
- verified covered quantity;
- stop/TP/trailing identities where safe to expose;
- trigger reference type;
- last verification time;
- exact degradation reason.

`UNKNOWN` and `FAILED` visually outrank unrealized PnL and cannot be hidden in a secondary panel.

## 7. Risk Survival Surface
The risk workspace separates:
- per-trade monetary risk;
- reserved risk;
- intraday/day/week/month survival budgets;
- account-survival reserve;
- Operational Margin Reserve;
- portfolio/common-factor exposure;
- collateral/venue stress state.

Canonical survival states are presented explicitly rather than averaged into one score:
`SURVIVAL_HEALTHY`, `SURVIVAL_CAUTION`, `SURVIVAL_REDUCED_RISK`, `SURVIVAL_NO_NEW_EXPOSURE`, `RECOVERY_ONLY`, `EMERGENCY`.

## 8. Current vs projected post-trade risk
Trade tickets and Copilot candidate actions distinguish:
- current tier/MMR/leverage/liquidation corridor;
- projected post-fill tier/MMR/leverage/liquidation corridor;
- stop-to-liquidation safety corridor;
- risk reservation before submit;
- snapshot expiry/revalidation status.

Projected values are never styled as current account truth.

## 9. Environment / mode identity
Every trading workspace has a persistent mode identity:
- `LIVE`;
- `PAPER`;
- `SHADOW`;
- `REPLAY`;
- `BACKTEST/RESEARCH` where applicable.

Mode identity uses multiple channels: explicit text, iconography, layout treatment and environment label. Color alone is insufficient.

Paper/shadow/replay screens cannot expose live exchange mutation controls.

## 10. Tenant–account–environment context lock
Money-affecting screens show a persistent Context Bar containing:
- tenant/workspace;
- exchange;
- exchange account alias/id-safe representation;
- environment/mode;
- current autonomy/session mode when relevant.

Switching context requires:
1. explicit selection;
2. cancellation/closure of unsafe transient UI state such as draft live order tickets;
3. backend authorization;
4. new authoritative state load;
5. visible context-confirmed transition.

Cross-context cached data cannot bleed into the new context.

## 11. Dangerous Action Contract
Actions such as close-all, cancel-all, freeze, blackout, credential revoke, session termination, release rollback and capability quarantine use a governed confirmation flow containing:
- exact scope;
- actor identity/context;
- affected tenant/account/exchange/capability;
- expected operational effect;
- preserved safety actions;
- estimated blast radius where relevant;
- step-up requirement if policy demands;
- reason/incident context where required;
- authoritative result and audit reference.

Typed confirmation phrases are optional UX aids, not security controls.

## 12. Trading-aware kill-switch UX
Emergency controls explain that blackout may:
- stop new exposure;
- cancel eligible entry orders;
- preserve/verify exchange-native protection;
- allow controlled risk-reducing closes;
- continue reconciliation;
- isolate compromised capabilities.

The UI must never imply that `EMERGENCY_BLACKOUT` simply turns every process off.

## 13. No optimistic money-state mutation
For orders, fills, positions, balances, margin, protection, trading authority and risk reservations:
- local UI may show `REQUESTED`/`PENDING` states immediately;
- it may not render the desired result as completed before authoritative confirmation;
- temporary optimistic UI patterns are permitted only for non-authoritative cosmetic/preferences state.

## 14. Privileged identity projection
Admin/support views maintain a persistent privilege header showing:
- authenticated actor;
- current role/assurance level;
- tenant/account scope;
- assumed support context if any;
- elevation/break-glass state and expiry;
- read-only vs mutation capability.

Support assumption never hides the real actor. Privilege context cannot be reduced to a transient toast.

## 15. Tenant-safe client data boundary
Tenant-sensitive UI data follows R08 classification and isolation rules across:
- browser cache/storage;
- query caches;
- search/autocomplete;
- browser history/title where sensitive;
- desktop notifications;
- exports/downloads;
- error diagnostics;
- telemetry.

Context switch/logout/revocation invalidates relevant client caches and subscriptions.

## 16. Decision Freshness UX
Opportunity/Brain/Risk/Execution surfaces expose a `Decision Freshness` contract:
- source market-state time;
- total data-to-decision age;
- remaining signal lifetime where defined;
- expiry state;
- whether downstream Risk/Execution must revalidate.

Expired opportunities are visibly non-actionable and cannot be resurrected from a stale card.

## 17. Critical-state accessibility contract
Safety-critical communication must provide at least:
- text label;
- semantic icon/shape/pattern where useful;
- programmatic accessible name/description;
- keyboard-accessible details/actions;
- sufficient contrast;
- no color-only distinction;
- assistive-technology status/alert announcements appropriate to urgency;
- reduced-motion equivalent.

Focus must move only when necessary for safety and never trap the user unintentionally.

## 18. Safety Priority Scheduler for UI
UI events use priority classes:
1. `P0_CAPITAL_SAFETY`;
2. `P1_STATE_CERTAINTY`;
3. `P2_EXECUTION_CONTROL`;
4. `P3_RISK_INTELLIGENCE`;
5. `P4_OPPORTUNITY`;
6. `P5_DECORATIVE`.

Higher priority can suppress/coalesce lower-priority animation and notification. Profit celebrations or opportunity animations are disabled while P0/P1 states are active.

## 19. Reconnect / resync state machine
Frontend realtime recovery states:
`CONNECTED_TRUSTED -> DEGRADED -> DISCONNECTED -> RECONNECTING -> RESYNCING -> RECONCILING -> TRUST_RESTORED`.

Transport reconnection alone reaches only `RESYNCING`.
Normal authority presentation returns only after backend generation synchronization and, where private account state is affected, reconciliation/state-confidence proof.

## HIGH_ASSURANCE invariants
- UI never upgrades backend authority.
- UI never infers fill/cancel/protection from intent alone.
- stale, unknown and disconnected are explicit states.
- live/paper/shadow/replay cannot be confused.
- tenant/account/environment context is persistent for money-affecting actions.
- critical state is accessible without color, animation or sound.
- profit/opportunity visuals never outrank capital-safety/state-certainty communication.

These contracts resolve the 19 CRITICAL gaps at planning level. Implementation remains unauthorized.
