# HCT-ADR-0037 — Microstructure Intelligence & Bootstrap Feature Serving

Status: `APPROVED_FOR_DISCOVERY`
Date: `2026-09-11`
Increment: `HCT-PLAN-0001-R02`
Risk class: `HIGH_ASSURANCE`

## Context
HCT's realtime infrastructure must provide the Intelligence Brain with information that is fresher and more structurally informative than slow aggregate indicators alone, while preserving the bootstrap free-infrastructure policy.

## Decision
1. HCT adopts a dedicated **Microstructure, Order-Flow, Liquidity, Breadth & Cross-Market Intelligence** planning domain.
2. Order-book/trade-flow features, liquidity topology, breadth, cross-asset lead/lag, alternative bars and anomaly detection are evidence sources, not direct trading authority.
3. Proprietary microstructure technologies begin as research hypotheses and require point-in-time correctness, leakage controls, OOS/walk-forward validation, realistic costs, replay/paper/shadow evaluation and governed promotion.
4. Realtime feature serving uses a provider-neutral `RealtimeFeatureStore` contract.
5. During bootstrap, the preferred implementation is in-process memory within the persistent trading worker plus bounded durable evidence, avoiding per-tick cloud/database/cache round trips.
6. Supabase remains application/metadata/audit persistence rather than the high-frequency feature hot path.
7. External Redis-compatible/feature-store infrastructure is introduced only when measured scaling needs justify it.
8. HCT introduces **Feature Value Density** as a bootstrap research metric: expensive realtime features must demonstrate incremental decision value relative to CPU, memory, bandwidth, storage and latency cost.
9. Microstructure/AI evidence may tighten or veto a decision, but cannot raise hard risk ceilings or bypass Safety, Risk, Session Policy or Execution controls.

## Consequences
- V1 can research sophisticated market intelligence without requiring an expensive streaming stack.
- Later migration to shared online feature infrastructure remains possible without changing feature semantics.
- Feature count is not a success metric; validated, non-redundant information is.
- Realtime compute must be tiered and load-sheddable, preserving safety/execution/reconciliation before research features.

## Related artifacts
- `docs/30-realtime-market-data-intelligence-and-streaming-rd.md`
- `docs/31-realtime-performance-benchmark-and-technology-selection.md`
- `docs/32-bootstrap-free-infrastructure-and-scale-migration.md`
- `docs/33-microstructure-orderflow-liquidity-breadth-and-anomaly-intelligence.md`
- `docs/14-product-module-map.md`
