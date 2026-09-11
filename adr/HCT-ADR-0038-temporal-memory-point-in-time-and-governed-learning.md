# HCT-ADR-0038 — Temporal Memory, Point-in-Time Retrieval & Governed Continual Learning

Status: `APPROVED_FOR_DISCOVERY`
Date: 2026-09-11
Risk class: `HIGH_ASSURANCE`

## Decision
HCT will treat market memory as a temporal, event-aware, regime-aware and point-in-time-correct institutional memory rather than a generic vector database. Canonical memories must distinguish when something happened (`event_time`) from when HCT knew it (`knowledge_time`). Retrieval, model training, replay and post-trade analysis must preserve that distinction to prevent future leakage and hindsight contamination.

HCT will use a dual-horizon memory architecture combining:
- global historical memory for recurring structures and long-horizon evidence; and
- recent memory for local behavior and fast concept drift.

Historical analog retrieval must return distributions and uncertainty across multiple independent episodes, not a single convenient anecdote.

Continual learning is governed. Production models/strategies/features may not silently self-modify or self-promote from live data. Online adaptation is limited to explicitly approved bounded statistics and reliability estimates unless a later separately validated online-learning policy is approved. Material model or strategy changes follow controlled evaluation and promotion gates.

## Required properties
- point-in-time correctness;
- immutable ex-ante decision evidence;
- explicit ex-post outcome attachment rather than historical rewrite;
- temporal/event provenance;
- regime-aware retrieval;
- analog diversity checks;
- concept-drift detection and localization;
- catastrophic-forgetting controls;
- champion/challenger shadow evaluation;
- reproducible replay;
- learning from executed trades and rejected/no-trade opportunities;
- rollback and quarantine.

## Authority boundary
Memory, RAG, analog search and learned models may recommend, explain, lower confidence, propose experiments or support vetoes. They may not:
- bypass Safety/Risk/Session Policy;
- raise hard risk or leverage ceilings;
- directly authorize exchange execution;
- erase negative/failure evidence;
- rewrite canonical historical decisions;
- train directly from unverified web content as canonical fact;
- self-promote model/strategy/skill versions.

## Bootstrap implementation
The initial implementation should favor free/near-free infrastructure:
- Supabase/PostgreSQL for compact episode/event/decision metadata;
- `pgvector` where useful for modest similarity retrieval;
- relational temporal/event edges before adopting a dedicated graph database;
- recent-memory cache in-process in the trading worker;
- selective/compressed episode persistence rather than unrestricted raw market-data retention;
- local/offline batch retrieval and model evaluation where practical.

Specialized vector databases, graph databases and dedicated model-serving infrastructure require benchmark/capacity justification.

## Research metrics introduced
- Analog Reliability Score (ARS)
- Temporal Leakage Firewall (TLF)
- Regime-Conditioned Similarity Kernel (RCSK)
- Historical Relevance Horizon (HRH)
- Memory Freshness Decay Surface (MFDS)
- Hindsight Bias Guard (HBG)
- Memory Diversity Score (MDS)
- Episode Surprise Score (ESS)
- Regime Memory Conflict Score (RMCS)
- Concept Drift Tensor (CDT)
- Drift Localization Engine (DLE)
- Catastrophic Forgetting Sentinel (CFS)
- Experience Replay Governor (ERG)
- Decision Regret Decomposition (DRD)
- Memory-to-Decision Attribution (MDA)

These are research candidates. None are assumed to improve trading performance until validated against a no-memory/no-adaptation baseline with realistic fees, slippage, latency and market regimes.
