# HCT-PLAN-0001-R03 — Acceptance Criteria & Review Gates

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R03`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

## Purpose
Define the objective planning gates that must be satisfied before R03 can receive `APPROVED` and be promoted to a checkpoint.

## Gate A — Authority and invariants
R03 passes only if all are explicit and mutually consistent:
- Safety Governor remains able to deny exposure after Risk approval;
- Risk Engine cannot be weakened by AI/agents/strategies;
- user policy can tighten but not exceed platform hard ceilings;
- unknown critical exchange/margin/reconciliation state blocks new exposure;
- leverage remains subordinate to monetary risk and survivability;
- no loss-recovery/martingale escalation is implicit or default.

## Gate B — Dynamic exchange risk state
Must define:
- normalized exchange risk-tier contract;
- maintenance-margin and max-leverage discovery;
- current and projected tier evaluation;
- position-limit checks;
- margin-mode checks;
- liquidation-reference semantics;
- freshness/provenance and explicit UNKNOWN state;
- revalidation on materially changed exchange rules.

## Gate C — Immutable post-trade RiskSnapshot
Every exposure-increasing action must have:
- immutable snapshot identity/hash;
- current account/portfolio/exchange state;
- projected post-fill state;
- projected tier/MMR/leverage/liquidation state;
- risk-budget consumption;
- tail/collateral/protection factors;
- finite validity/expiry;
- invalidation triggers;
- execution binding to exact snapshot or reapproval.

## Gate D — Risk Reservation Ledger
Must prove conceptual conservation across:
- pending orders;
- partial fills;
- cancel pending;
- uncertain outcomes;
- late acknowledgements;
- reconciliation;
- duplicate/idempotent intents.

No cancellation request or timeout may release risk before authoritative resolution.

## Gate E — Cross-margin contagion
Must evaluate the portfolio as shared collateral where applicable, including:
- all relevant cross positions;
- open-order margin;
- unrealized PnL;
- maintenance-margin requirements;
- correlated shocks;
- collateral confidence;
- projected effect of a new position on existing liquidation buffers.

## Gate F — Multi-horizon survival and tail risk
Must include:
- trade/intraday/daily/weekly/monthly/account-survival limits;
- deterministic hierarchy of budgets;
- tail stress / Expected Shortfall-style research path;
- high-water/drawdown state machine;
- higher-horizon veto even when a lower-horizon budget remains;
- no tail model allowed to relax hard ceilings.

## Gate G — Operational Margin Reserve
Must define a protected reserve for non-ideal operational outcomes and prove that normal opportunity sizing cannot consume it.

## Gate H — Protection failure exposure
Must distinguish intended stop from guaranteed realized risk and explicitly model:
- gap-through-stop;
- rejection/cancellation;
- partial coverage;
- stale protective quantity;
- adverse fill;
- delayed/uncertain protection.

## Gate I — Adds / pyramiding
Must require a fresh risk decision and reservation for every add, recompute cumulative risk and prohibit implicit martingale/loss recovery.

## Gate J — Collateral and extreme venue risk
Must explicitly cover:
- collateral concentration/depeg uncertainty;
- effective risk capital versus nominal equity;
- partial/tiered liquidation;
- insurance-fund/ADL mechanics where observable;
- unknown extreme-venue state;
- conservative degradation modes.

## Gate K — Explainability
Every risk decision must expose an auditable explanation bundle containing at least:
- requested and approved monetary risk;
- notional/size;
- leverage;
- reserved risk;
- margin mode;
- tier/MMR;
- liquidation corridor;
- tail/stress state;
- correlation/cross-margin impact;
- collateral quality;
- protection confidence;
- multi-horizon survival state;
- exact reduction/veto reason codes.

Critical subcondition failure may not be hidden behind an aggregate score.

## Gate L — User risk presets
If presets are offered, `CONSERVATIVE`, `BALANCED`, `AGGRESSIVE` and `CUSTOM` are configuration bundles beneath platform ceilings. `AGGRESSIVE` is not an override mode.

## Gate M — Validation plan
Planning must require tests for:
- tier boundary and tier transition;
- snapshot expiry/invalidation;
- reservation conservation;
- concurrent risk overbooking;
- partial fill and unknown outcome;
- cross-margin cascade;
- correlated crash;
- gap through stop;
- protection rejection;
- collateral depeg;
- ADL/extreme venue state;
- pyramiding across tier boundary;
- weekly/monthly survival guard;
- operational reserve consumption;
- restart/reconciliation recovery.

## Gate N — Canonical document consistency
Before approval:
- Decisions Ledger must contain all R03 decisions;
- Requirements must contain the accepted R03 product requirements;
- Scope must not imply implementation authorization;
- module map must remain consistent;
- R03 gap audit must have no unresolved CRITICAL/HIGH planning defect;
- PR description must match actual branch content;
- objective audit report must exist.

## Candidate verdict rule
- any unresolved CRITICAL/HIGH planning defect: `CORRECTION REQUIRED`;
- missing authoritative source needed to complete planning: `BLOCKED`;
- all gates satisfied with no CRITICAL/HIGH planning defect: `APPROVED`.

Implementation/live trading remains unauthorized even after R03 planning approval.
