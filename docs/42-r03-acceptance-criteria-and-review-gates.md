# HCT-PLAN-0001-R03 — Acceptance Criteria & Review Gates

Status: `APPROVED`
Increment: `HCT-PLAN-0001-R03`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

## Purpose
Define the objective planning gates that must be satisfied before R03 can receive `APPROVED` and be promoted to a checkpoint.

## Gate A — Authority and invariants
Result: `PASS`

Required conditions:
- Safety Governor remains able to deny exposure after Risk approval;
- Risk Engine cannot be weakened by AI/agents/strategies;
- user policy can tighten but not exceed platform hard ceilings;
- unknown critical exchange/margin/reconciliation state blocks new exposure;
- leverage remains subordinate to monetary risk and survivability;
- no loss-recovery/martingale escalation is implicit or default.

## Gate B — Dynamic exchange risk state
Result: `PASS`

Covered:
- normalized exchange risk-tier contract;
- maintenance-margin and max-leverage discovery;
- current/projected tier evaluation;
- position-limit and margin-mode checks;
- liquidation-reference semantics;
- freshness/provenance and UNKNOWN state;
- revalidation on material venue-rule change.

## Gate C — Immutable post-trade RiskSnapshot
Result: `PASS`

Every exposure-increasing action requires immutable identity/hash, current and projected state, tier/MMR/leverage/liquidation state, risk-budget consumption, tail/collateral/protection factors, finite validity and binding to exact approved snapshot or reapproval.

## Gate D — Risk Reservation Ledger
Result: `PASS`

Conceptual conservation is defined across pending orders, partial fills, cancel pending, uncertain outcomes, late acknowledgements, reconciliation and idempotent/duplicate intents. Timeout or cancel request cannot release risk before authoritative resolution.

## Gate E — Cross-margin contagion
Result: `PASS`

Shared collateral evaluation includes relevant cross positions, open-order margin, unrealized PnL, MMR, correlated shocks, collateral confidence and projected effect on existing liquidation buffers.

## Gate F — Multi-horizon survival and tail risk
Result: `PASS`

Trade/intraday/daily/weekly/monthly/account-survival limits are hierarchical. Tail/Expected Shortfall-style research may only tighten authority. Higher-horizon exhaustion can veto lower-horizon remaining capacity.

## Gate G — Operational Margin Reserve
Result: `PASS`

A protected reserve for non-ideal operational outcomes is defined and excluded from normal opportunity sizing.

## Gate H — Protection failure exposure
Result: `PASS`

Planning distinguishes intended stop from guaranteed realized loss and includes gap-through-stop, rejection/cancellation, partial coverage, stale protective quantity, adverse fill and delayed/uncertain protection.

## Gate I — Adds / pyramiding
Result: `PASS`

Every ADD requires a fresh risk decision/reservation and cumulative projected state review. Implicit martingale/loss recovery is prohibited.

## Gate J — Collateral and extreme venue risk
Result: `PASS`

Collateral concentration/depeg uncertainty, Effective Risk Capital, partial/tiered liquidation, ADL/insurance mechanics where observable and conservative UNKNOWN states are covered.

## Gate K — Explainability
Result: `PASS`

Risk decisions expose requested/approved monetary risk, notional/size, leverage, reserved risk, margin mode, tier/MMR, liquidation corridor, tail/stress, correlation/cross-margin impact, collateral quality, protection confidence, multi-horizon survival state and exact reduction/veto reason codes. Critical failures cannot be hidden behind aggregate scores.

## Gate L — User risk presets
Result: `PASS`

`CONSERVATIVE`, `BALANCED`, `AGGRESSIVE` and `CUSTOM` are bounded policy bundles beneath platform ceilings. `AGGRESSIVE` is not an override mode.

## Gate M — Validation plan
Result: `PASS`

Required testing covers tier boundaries/transitions, snapshot expiry/invalidation, reservation conservation, concurrent overbooking, partial/uncertain outcomes, cross-margin cascade, correlated crash, gap-through-stop, protection rejection, collateral depeg, ADL/extreme venue state, pyramiding across tiers, weekly/monthly survival guard, OMR consumption and restart/reconciliation recovery.

## Gate N — Canonical document consistency
Result: `PASS`

- Decisions Ledger contains all accepted R03 decisions through `HCT-DEC-0049`.
- Requirements contain accepted R03 requirements.
- Scope continues to forbid implementation/live authorization.
- Module map remains consistent.
- `docs/39-r03-risk-gap-audit-and-institutional-hardening.md` records all CRITICAL/HIGH gaps as resolved in planning.
- PR description can be aligned to final branch state.
- `docs/43-r03-final-audit.md` exists with objective verdict `APPROVED`.

## Final verdict rule application
No unresolved CRITICAL/HIGH planning defect remains and no authoritative-source blocker prevents planning completion.

Final R03 verdict: `APPROVED`.

Implementation/live trading remains unauthorized even after R03 planning approval.