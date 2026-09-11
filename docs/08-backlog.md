# Backlog

Status: `DISCOVERY_IN_PROGRESS`
Active increment: `HCT-PLAN-0001`

## NECESSARY next
- `HCT-PLAN-0001-R01`: Market Universe & Scanner discovery. **Completed / promoted.**
- `HCT-PLAN-0001-R02`: Strategy / signal / indicator architecture discovery. **Closure candidate; branch contains substantial approved-for-discovery pre-work for later rounds.**
- `HCT-PLAN-0001-R03`: Safety, risk, leverage and position-sizing discovery. Reuse `docs/28-risk-intelligence-position-sizing-leverage-and-equity-guard.md` as pre-discovery input, then formally reconcile/gap-audit against R03 scope.
- `HCT-PLAN-0001-R04`: Execution, OMS and reconciliation discovery. Reuse `docs/29-execution-intelligence-oms-reconciliation-and-recovery.md` as pre-discovery input, then formally reconcile/gap-audit against R04 scope.
- `HCT-PLAN-0001-R05`: Realtime data, API quota, WebSocket, caching and resilience discovery. Reuse `docs/30`–`docs/33` plus bootstrap infrastructure decisions as pre-discovery input, then formally benchmark/freeze R05 choices.
- `HCT-PLAN-0001-R06`: Intelligence Brain, RAG, memory and controlled learning lifecycle discovery. Reuse `docs/34`–`docs/35` as pre-discovery input, then formally reconcile/gap-audit against R06 scope.
- `HCT-PLAN-0001-R07`: Backtest, replay, paper/shadow trading and promotion-gate discovery. Reuse `docs/36-simulation-replay-paper-shadow-and-promotion-laboratory.md` as pre-discovery input.
- `HCT-PLAN-0001-R08`: Multi-tenant, security, secrets and commercialization-readiness discovery.
- `HCT-PLAN-0001-R09`: Realtime trading cockpit, UI/UX and design-system discovery, including the first-class `Signals` workspace.
- `HCT-PLAN-0001-R10`: Observability, audit, incidents, compliance, FinOps and operational readiness discovery, including signal-publication telemetry and commercial/regional review.
- `HCT-PLAN-0001-R11`: Integration review, dependency graph and V1/Future classification.
- `HCT-PLAN-0001-R12`: Planning freeze candidate, gap audit and Definition of Done alignment.

## IMPORTANT candidates
- Strategy Router / multi-strategy orchestration.
- Cross-symbol/correlation intelligence.
- Proprietary HCT indicator and microstructure R&D program.
- Model registry, feature store and governed experiment registry.
- Explainable decision-trace explorer.
- Subscriber-realizability and signal-room analytics beyond the V1 minimum.
- Tenant entitlement/plan engine once commercialization scope is approved.

## FUTURE candidates
- Additional exchanges after the MEXC-first architecture is stable and abstraction value is proven.
- Additional signal-distribution destinations beyond Telegram.
- White-label tenant branding.
- Advanced model ensembles / online-adaptation mechanisms only after safety and statistical evidence justify them.

## OUT OF SCOPE until explicitly approved
- real-money implementation;
- live production API credentials;
- autonomous self-modifying risk logic;
- ungoverned online learning that can change live execution behavior;
- guaranteed-return or guaranteed-profit claims.

## R02 scope-drift governance note
R02 began as strategy/signal/indicator discovery but accumulated pre-discovery decisions for R03–R07 plus Telegram signal publishing. These artifacts are not treated as silently completed future rounds. They are reusable inputs that must be formally reconciled, gap-audited and promoted in their canonical rounds. This preserves the original planning sequence while avoiding loss of already-approved discovery work.

No product feature enters implementation automatically. Discovery outputs must first be classified and reconciled with Scope, Architecture, Security, Test Plan and Definition of Done.
