# HCT-PLAN-0001-R07 — Validation Laboratory Critical Architecture

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R07`
Risk class: `HIGH_ASSURANCE`
Date: `2026-09-11`

## Purpose
Close the 17 CRITICAL R07 gaps and define the minimum proof architecture required before any candidate can become production-eligible.

## 1. Dataset Eligibility Gate
Every promotion-grade experiment begins with an immutable `DatasetManifest` that records:
- dataset/capture IDs and hashes;
- source/channel/version provenance;
- start/end/event-time coverage;
- R05 capture completeness/fidelity classes;
- known gaps, schema quarantines and corrections/vintages;
- symbol/universe membership history;
- venue-rule/capability history references;
- allowed uses: `RESEARCH_ONLY`, `REPLAY_ELIGIBLE`, `PROMOTION_ELIGIBLE`;
- exclusion reasons and approving evaluator version.

A dataset with unresolved critical continuity, temporal, schema or provenance defects cannot be upgraded to promotion evidence merely because strategy PnL looks attractive.

## 2. Point-in-Time Universe Snapshot
Every simulated decision references a `UniverseEpoch` containing the contracts that were actually available/eligible at that epoch plus status, listing/delisting/pauses, API eligibility and relevant contract/rule identifiers.

Current listings may never be projected backward. Historical delisted failures remain in eligible historical samples where they truly existed.

## 3. Temporal Non-Interference Proof
TNIC becomes a mandatory precondition for promotion-grade historical evidence.

The proof graph spans:
`source event -> normalization -> join/resample -> feature -> strategy/Brain -> memory/RAG/news -> Risk -> Execution -> outcome label`.

Every edge checks `availability/knowledge_time <= simulated decision time` for information consumed by that decision. Later corrections/vintages and labels remain inaccessible until their historical availability/maturity time.

A TNIC violation invalidates the affected experiment/fold and cannot be waived by performance.

## 4. Holdout Governance & OOS Firewall
Experiments use explicit data roles:
`TRAIN`, `TUNE/VALIDATE`, `WALK_FORWARD`, `PROMOTION_HOLDOUT`, `POST_PROMOTION_MONITORING`.

Rules:
- final promotion holdouts are immutable experiment resources;
- tuning/search processes cannot query holdout outcomes;
- holdout access is logged and budgeted;
- repeated manual inspection consumes the holdout and can require a new untouched holdout;
- temporal dependence uses governed purge/embargo windows where needed;
- model/parameter selection occurs inside nested validation, not on final holdout.

## 5. Experiment Reproduction Manifest
Promotion experiments carry a complete immutable identity:
- `experiment_id` / parent experiment family;
- Git commit/tree;
- source/data hashes;
- dependency lock/runtime/container/build identity;
- relevant hardware/runtime behavior class;
- all configs/policies;
- strategy/feature/Brain/model/prompt/tool/skill/retriever/calibration versions;
- simulator/accounting/fill/latency model versions;
- venue capability/rule profile;
- RNG stream names/seeds where supported;
- evaluator suite/version;
- manifest content hash.

Unpinned material behavior is `NOT_REPRODUCIBLE_FOR_PROMOTION`.

## 6. Causal Event Scheduler
Replay uses a causal event scheduler rather than arbitrary loop ordering.

Every event has logical/source time plus receive/processing/scheduled availability as appropriate. Scheduler semantics define ordering/tie-break rules for:
- market updates;
- candidate decisions;
- RiskSnapshot/reservation creation;
- order submit/ack/fill;
- cancel/replace races;
- private events;
- protection establishment;
- reconciliation;
- funding/rule/status changes.

Zero-time impossible feedback loops are prohibited. An event created by a consequence cannot be observed by its cause.

## 7. Historical Venue Semantics Resolver
The simulator consumes a versioned `VenueSemanticsSnapshot` appropriate to each experiment epoch, covering where known:
- order types/TIF/STP/reduce-only;
- hedge/one-way and position modes;
- price/quantity precision and min constraints;
- risk tiers, max leverage, MMR/position limits;
- margin/liquidation semantics;
- funding/fees;
- rate/request-time behavior relevant to execution;
- symbol trading states and capability changes.

Unknown critical historical semantics are explicit and may make a period ineligible for promotion evidence.

## 8. Fill Realism Authority
Each execution simulation declares a fill-model class and confidence:
- `L1_COARSE_CONSERVATIVE`;
- `L2_TRADE_SPREAD_AWARE`;
- `L3_BOOK_LIQUIDITY_AWARE`;
- `L4_QUEUE_APPROXIMATED`;
- `SHADOW_CALIBRATED` where real observation supports it.

Fill simulation must model appropriate no-fill, partial fill, participation, spread, latency, slippage and cancellation behavior. Same-tick/same-bar perfect fills are forbidden unless causal ordering proves they were executable.

Promotion compares at least median/conservative/adverse plausible fill assumptions when model uncertainty matters. A candidate that survives only the optimistic envelope is not production-eligible.

## 9. Canonical Trading Accounting Kernel
Replay/paper/shadow share a versioned accounting/margin kernel implementing the same canonical definitions used by production domains for:
- position quantity/side/mode;
- realized/unrealized PnL;
- fees/funding;
- initial/maintenance margin;
- cross/isolated collateral effects;
- risk-tier transitions;
- liquidation corridor/partial-liquidation approximations where supported;
- collateral haircuts/effective risk capital where applicable;
- precision/rounding.

Accounting parity tests against captured exchange examples are required before promotional trust.

## 10. Deterministic State-Machine Parity
Replay/paper/shadow cannot shortcut approved R03/R04 contracts.

They preserve the logical semantics of:
- RiskSnapshot validity and revalidation;
- Risk Reservation Ledger;
- Command Authorization Lease;
- immutable Order Intent/Execution Command identities;
- fill conservation/idempotency;
- unknown outcome protocol;
- cancel/replace races;
- position-mode-safe reduce/close;
- protection dependency/coverage/deadline;
- reconciliation watermark/conflict state;
- restart/failover recovery proof.

Environment adapters may simulate exchange effects, but the domain state machine remains shared.

## 11. Live-Parity Conformance Suite
Every promotable component exposes a parity test mapping between research/replay/paper/shadow and production domain contracts.

The suite compares:
- strategy/Brain candidate decisions;
- Safety/Risk decisions;
- policy reasons;
- position sizing/leverage outputs;
- OMS transitions;
- protection logic;
- accounting;
- expected external commands.

Any semantic fork is registered as a `PARITY_EXCEPTION` with scope/reason and blocks blanket claims of live parity.

## 12. Paper/Shadow Capability Isolation
Paper/shadow uses a distinct capability namespace and credential boundary.

Hard invariants:
- no production exchange-order tool capability;
- no mutation of production positions/orders/reservations/protection;
- no write to authoritative live account state;
- no production-secret exposure unless a read-only private-data capability has separately approved necessity and isolation;
- all hypothetical outputs are namespace-marked and cannot be consumed as real fills.

Isolation is enforced by Tool Gateway/capability policy, not by prompts alone.

## 13. Immutable Promotion Evidence Bundle
Every promotion candidate produces an append-only `PromotionEvidenceBundle` containing experiment manifests, datasets, metrics, gate outcomes, failed experiments/search history summaries, evaluator versions, reviewer identities, evidence hashes and promotion/denial rationale.

A promotion decision references exact bundle hash/version. New evidence creates a new bundle/version; previously reviewed results are never silently overwritten.

## 14. Experiment Family & Multiple-Testing Governor
All related strategy/model/feature searches are grouped under an `ExperimentFamilyID`.

The governor tracks:
- number of attempted variants;
- parameter/model search space;
- datasets/folds repeatedly consulted;
- primary vs exploratory metrics;
- candidate-selection rule;
- holdout accesses;
- selection-bias/multiple-testing adjustment method appropriate to the experiment.

Repeated mining of the same evidence lowers promotion confidence and can exhaust a dataset/holdout for further confirmatory use.

## 15. Stochastic Reproduction Classes
Each experiment declares one reproduction class:
- `BITWISE_EXPECTED`;
- `DETERMINISTIC_WITH_TOLERANCE`;
- `STATISTICALLY_REPRODUCIBLE`;
- `PROVIDER_NONDETERMINISTIC_PINNED_CONTEXT`;
- `NON_REPRODUCIBLE_NOT_PROMOTION_ELIGIBLE`.

Named independent RNG streams are used for fills, latency, resampling and other stochastic mechanisms where possible. LLM/model/provider nondeterminism is recorded rather than disguised.

## 16. Promotion Validity Lease
Promotion evidence has a validity lease, not perpetual truth.

Revalidation triggers include:
- material venue capability/risk-rule change;
- data/schema/feature contract change;
- strategy/Brain/model/retriever/prompt/skill change;
- significant execution reality-gap drift;
- material regime/distribution drift;
- prolonged inactivity/new market structure;
- critical safety/reconciliation defect;
- dependency/runtime change affecting behavior.

Triggered candidates transition to `REVALIDATION_REQUIRED`, `DEGRADED` or `QUARANTINED` according to severity.

## 17. Limited-Live Canary Envelope
Future `LIMITED_LIVE` promotion, if separately implementation-authorized, requires an immutable canary envelope:
- allowed accounts/tenants/symbols;
- max gross/net exposure and risk/trade;
- max daily/session loss;
- lower leverage/position ceilings than platform maxima;
- allowed hours/conditions;
- health/data/reconciliation prerequisites;
- automatic stop/rollback triggers;
- exact rollback target and state-compatibility proof;
- expiry/review time.

Canary scope may automatically tighten. It cannot silently expand. Any real-money activation remains outside R07 planning authority and requires later explicit production authorization.

## CRITICAL gap closure map
- GAP-01: section 1
- GAP-02: section 2
- GAP-03: section 3
- GAP-04: section 4
- GAP-05: section 5
- GAP-06: section 6
- GAP-07: section 7
- GAP-08: section 8
- GAP-09: section 9
- GAP-10: section 10
- GAP-11: section 11
- GAP-12: section 12
- GAP-13: section 13
- GAP-14: section 14
- GAP-15: section 15
- GAP-16: section 16
- GAP-17: section 17

## Result
All 17 CRITICAL R07 gaps now have explicit planning-resolution contracts. HIGH hardening, acceptance gates, decisions/requirements consolidation and final audit remain required before R07 approval.