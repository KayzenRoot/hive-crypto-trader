# HCT-ADR-0040 — Promotion Laboratory, Point-in-Time Proof and Live Parity

Status: `APPROVED_FOR_DISCOVERY`
Date: 2026-09-11
Increment: `HCT-PLAN-0001-R02`
Risk class: `HIGH_ASSURANCE`

## Context
HCT contains strategies, proprietary indicators, agents, temporal memory, continual learning, microstructure intelligence, an Intelligence Brain and adaptive execution. Historical PnL alone is insufficient evidence for production promotion because optimistic fills, look-ahead leakage, overfitting, stale assumptions, regime concentration and simulation/live code divergence can create false confidence.

Recent financial research continues to emphasize point-in-time correctness, temporal non-interference, out-of-time validation and governed champion/challenger promotion. HCT must therefore treat validation as an independent safety-critical domain.

## Decision
HCT will maintain a dedicated Simulation / Replay / Paper / Shadow / Promotion Laboratory with the following mandatory principles:

1. promotion evidence must be point-in-time correct;
2. historical decisions may consume only information available at that simulated epoch;
3. event-driven replay is preferred where event ordering or execution timing matters;
4. fees, funding, spread, slippage, latency, partial fills and exchange constraints must be represented where relevant;
5. candidates progress through explicit validation states rather than jumping from backtest to live;
6. paper and shadow modes do not receive financial trading authority;
7. Champion/Challenger promotion is versioned, auditable and statistically/economically evaluated;
8. no model, strategy, agent or AI component can self-promote;
9. replay/paper/shadow and live paths should share domain contracts and decision semantics wherever feasible through a Live-Parity Contract;
10. HIGH_ASSURANCE promotion requires rollback and independent review evidence.

## Validation ladder
`RESEARCH -> STATIC_VALIDATION -> HISTORICAL_REPLAY -> WALK_FORWARD -> OUT_OF_SAMPLE -> STRESS/MONTE_CARLO -> PAPER -> SHADOW -> CHAMPION_CHALLENGER -> PRODUCTION_ELIGIBLE -> LIMITED_PRODUCTION -> PRODUCTION_ACTIVE`

## Explicitly rejected patterns
- same-bar/same-tick optimistic fills without temporal justification;
- evaluation on information that was revised or published later;
- using current web/LLM knowledge inside historical agent simulations without point-in-time controls;
- parameter selection and evaluation on the same window;
- promotion from one profitable backtest;
- hidden differences between backtest strategy semantics and live strategy semantics;
- self-promotion by learned systems;
- treating synthetic scenarios as proof of historical profitability.

## Proprietary research constructs
The laboratory may research TNIC, DRF, MRFS, FRE, LIL, SHLS, PPS, ESC, RGS, PEM, ESS, SCG, Decision Twin, PFI, SDM and LPC as described in `docs/36-simulation-replay-paper-shadow-and-promotion-laboratory.md`.

## Bootstrap cost constraint
The laboratory must support local/controlled replay compute and low-cost storage during bootstrap. No paid streaming cluster, dedicated vector service or GPU fleet is mandatory for V1 validation. Scale infrastructure only when measured workloads and business economics justify it.

## Consequences
Positive:
- lower look-ahead and overfitting risk;
- realistic estimate of edge after costs;
- measurable simulation-to-live gap;
- safer incremental promotion;
- reproducible evidence and rollback.

Costs:
- more engineering effort;
- slower promotion cadence;
- heavier data/version management;
- some market phenomena cannot be reconstructed perfectly from available history.

These costs are accepted because HCT is HIGH_ASSURANCE and operates with user capital.
