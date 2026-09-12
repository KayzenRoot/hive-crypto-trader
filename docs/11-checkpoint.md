# Checkpoint

Checkpoint ID: `HCT-CP-0013`
Status: `PRODUCT_DISCOVERY_ROUND_11_APPROVED`
Canonical branch: `main`
Last canonical planning merge: `cf1d83874a34ac49e0a1417eba47a9410c29e765` (`HCT-PLAN-0001-R11`)
Risk class: `HIGH_ASSURANCE`
Functional product planning: `IN_PROGRESS`
Implementation authorization: `NOT_GRANTED`

## Approved through R11
- R01–R10 foundations remain approved and authoritative.
- R11 integrates the approved round stack into one system model rather than treating each module as an isolated design.
- Trading authority is a restrictive lattice across exchange capability/rules, Security/Tenant, Harness, Safety, Session Policy, Risk, R05 data authority/freshness, reconciliation/protection and R07 promotion/environment eligibility. No later component may relax another authoritative restriction.
- Position Sizing/Leverage use a bounded proposal followed by projected post-trade RiskSnapshot approval; Risk Reservation is committed before exposure-increasing submit.
- State-changing exchange commands consume a Canonical Authorization Bundle binding all required identity/environment/exchange/data/Safety/Session/Risk/Reservation/action/lease context.
- Degraded modes distinguish NEW/ADD exposure from REDUCE/CLOSE/PROTECT/RECONCILIATION so risk creation can stop without blindly disabling safety recovery.
- Harness/capability isolation may restrict but cannot weaken required Safety/Risk/protection/reconciliation paths.
- A Source-of-Truth Matrix gives each authoritative state family one domain owner; cache, UI, analytics and telemetry remain projections.
- Realtime ownership is separated among quota/WS resources, raw normalized ingest, data quality, coherent Market-State generation and cache/hot-state projections.
- RAG is the governed memory facade; Temporal Memory owns deeper temporal mechanisms; Learning Lifecycle owns candidates/versions; Promotion Laboratory remains independent proof authority.
- Strategy/Agents/News/Memory produce or route evidence; Brain fuses candidate decisions; Copilot orchestrates workflows; deterministic Safety/Session/Risk/Execution retain hard authority.
- LIVE/PAPER/SHADOW/REPLAY environment identity is a cross-domain high-assurance invariant.
- Typed cross-domain IDs and behaviorally material versions/hashes are required; mutable display names are non-authoritative.
- Failure/degradation propagation and logical implementation dependency stages are explicit.
- All 42 accepted modules are classified as `V1_CORE`, `V1_MINIMUM`, `IMPORTANT_POST_V1` or `FUTURE`; architecture readiness is distinct from production/live activation.
- Signals feedback cannot directly self-modify live behavior; Admin and Trading Cockpits retain separate privilege planes; observability references domain truth rather than creating shadow authority.
- Multi-tenancy/security, cockpit safety, Admin/Harness and minimum audit/observability/incident capabilities are explicit V1 foundations.
- Advanced microstructure, full agent/news depth and advanced continual-learning behavior are capability-gated beyond their minimum V1 foundations.
- Requirements freeze inputs are explicitly inventoried in `docs/96-r11-requirements-freeze-input-inventory.md` for lossless R12 consolidation.
- Canonical Architecture and Product Module Map were corrected during R11 final review to remove an obsolete sequential authority-chain representation.

## R11 audit
- Final audit: `docs/97-r11-final-integration-audit.md`
- Verdict: `APPROVED`
- Acceptance gates: 31/31 PASS
- Initial gaps: 32; unresolved CRITICAL/HIGH gaps: 0
- Decisions Ledger consolidated through `HCT-DEC-0141`

## Completed increments
- `HCT-BOOT-0001`
- `HCT-PLAN-0001-R01`
- `HCT-PLAN-0001-R02`
- `HCT-PLAN-0001-R03`
- `HCT-PLAN-0001-R04`
- `HCT-PLAN-0001-R05`
- `HCT-PLAN-0001-R06`
- `HCT-PLAN-0001-R07`
- `HCT-PLAN-0001-R08`
- `HCT-PLAN-0001-R09`
- `HCT-PLAN-0001-R10`
- `HCT-PLAN-0001-R11`

## Current blockers
None for entering the R12 planning-freeze candidate. Implementation, production secrets/credentials, deployment, limited-live and real-money trading remain not granted.

## Next necessary action
Continue `HCT-PLAN-0001` with formal `HCT-PLAN-0001-R12`: Planning Freeze Candidate.

R12 must:
- consolidate the nine canonical requirement inputs losslessly with objective source-to-frozen traceability;
- harden `docs/09-definition-of-done.md` from bootstrap status into the project-wide HIGH_ASSURANCE DoD;
- align source hierarchy/canonical statuses;
- run one final cross-document/cross-module contradiction and gap audit;
- issue an explicit freeze/no-freeze verdict.

Planning freeze must not automatically authorize implementation, production deployment, production credentials, limited-live activation or real-money trading.

## Global chat and prompt delivery policy
All HCT chats and executor handoffs SHALL follow `docs/104-chat-delivery-and-prompt-artifact-policy.md`.

Mandatory rule: every complete executable prompt for Codex, Cursor or another executor/reviewer MUST be generated as a downloadable PDF artifact and MUST NOT be reproduced as a complete prompt inside a writing block, code block, copyable box or long inline chat message.

The chat itself should contain only a concise artifact summary, execution boundary and PDF download link. If PDF generation fails, fail closed and regenerate the PDF rather than dumping the full prompt into chat.

For the first executor prompt of a repository/session, the PDF must include safe repository synchronization and exact-state Context Lock before execution or review.

This policy persists across chat changes and review cycles unless the user explicitly changes the project policy.

## Resume rule
A new chat must recover from the machine-readable planning checkpoint and repository source hierarchy, validate Git state, read `docs/104-chat-delivery-and-prompt-artifact-policy.md`, and resume only from `next_necessary_action`.

Before producing any executor prompt, a new chat MUST enforce the PDF-only prompt delivery rule from `docs/104-chat-delivery-and-prompt-artifact-policy.md`.
