# Institutional Agent Workforce & News Intelligence

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R02`
Risk class: `HIGH_ASSURANCE`

## Objective
HCT agents must behave as a coordinated institutional-grade decision team, not isolated chat personas. The design target is a multidisciplinary financial, economic, risk, execution, market-structure and intelligence desk whose members can use approved tools, retrieve evidence, challenge one another, create governed reusable skills, and produce auditable structured recommendations.

The canonical agent specifications will be authored and versioned inside this repository before implementation. External executors such as Codex should implement those specifications rather than inventing agent behavior ad hoc.

## Agent quality bar
Every production-capable agent specification should define:
- mission and domain scope;
- explicit non-goals;
- senior/expert competence profile;
- required inputs and expected outputs;
- approved tools and prohibited tools;
- source-quality hierarchy;
- uncertainty/calibration behavior;
- escalation rules;
- communication protocol with other agents;
- memory/RAG access policy;
- skill usage/creation policy;
- failure/degraded behavior;
- evaluation suite;
- audit fields;
- authority ceiling.

No agent receives direct unrestricted exchange credentials or authority to bypass deterministic controls.

## Institutional agent roster
The current candidate workforce expands the earlier topology into explicit desks/roles.

### 1. Market Scout Agent
Discovers and ranks relevant symbols, liquidity conditions and emerging opportunities. Optimized for breadth and triage, not final trade authority.

### 2. Technical & Quantitative Analyst Agent
Interprets indicator families, proprietary features, market structure, pattern evidence, multi-timeframe state and quantitative signal quality.

### 3. Macro Economist Agent
Tracks monetary policy, rates, inflation, employment, growth, liquidity conditions, dollar conditions and macro risk relevant to crypto markets.

### 4. Crypto Market Structure Agent
Focuses on derivatives structure, funding, basis, open interest, liquidations, exchange flows/data where available, breadth/correlation and crypto-native market mechanics.

### 5. Regime & Cycle Agent
Classifies trend/range, volatility, liquidity, abnormal states and broader cycle context; estimates regime transitions and uncertainty.

### 6. Strategy Specialist Agent
Evaluates setup validity against exact versioned strategy semantics, detects violated assumptions and explains why a strategy should or should not participate.

### 7. Strategy Ecology Agent
Evaluates strategy suitability, redundancy, conflict, decay, effective diversity and regime affinity before strategies reach the supervisor.

### 8. Historical Memory / RAG Agent
Retrieves time-valid historical analogues, previous trades, incidents, similar regimes, failure modes and lessons, with provenance and temporal leakage controls.

### 9. Risk Officer Agent
Acts like a senior risk officer: identifies downside, concentration, correlated exposures, liquidation proximity, adverse scenarios and portfolio fragility. It proposes stricter risk but cannot relax deterministic Risk Engine ceilings.

### 10. Portfolio & Exposure Agent
Analyzes aggregate long/short bias, factor/correlation clusters, symbol concentration, common-driver exposure and interaction among open/pending trades.

### 11. Leverage & Position Construction Agent
Proposes position size, leverage, stop distance, scaling and risk-budget use inside deterministic limits.

### 12. Execution & Microstructure Agent
Assesses spread, depth, volatility, order type, urgency, expected slippage, partial fills, maker/taker tradeoffs and execution feasibility.

### 13. Position Manager Agent
Monitors open positions, thesis health, trailing behavior, partial exits, time stops, invalidation and risk-reduction opportunities.

### 14. News & Event Intelligence Agent
Continuously/when invoked searches approved internet/data sources for current and upcoming information that could materially affect crypto markets in the next minutes, hours or trading session.

### 15. Geopolitical & Regulatory Agent
Focuses on regulation, enforcement, elections/policy where economically relevant, sanctions, geopolitical shocks and market-access implications.

### 16. Security / Exploit Intelligence Agent
Tracks major exchange/protocol security incidents, exploits, chain halts, stablecoin events, custody incidents and cyber events that may create immediate market risk.

### 17. Adversarial / Devil's Advocate Agent
Attempts to invalidate the prevailing thesis. Required to inspect overlooked evidence, correlation, crowded reasoning, stale assumptions and confirmation bias.

### 18. Supervisor / Chief Investment Decision Agent
Synthesizes evidence and disagreements into a structured candidate action. Must preserve minority/dissenting evidence and uncertainty; it cannot override deterministic Safety/Risk/Policy.

### 19. Post-Trade Review Agent
Performs structured postmortems, attribution, expectation-vs-outcome comparison and writes learning episodes without rewriting history.

### 20. Agent Auditor / Model Risk Agent
Evaluates other agents for calibration drift, hallucination/source errors, behavioral regressions, tool misuse, prompt/skill changes and model-version risk.

## News & Event Intelligence Agent
This agent is a first-class capability because time-sensitive information can invalidate otherwise strong technical setups.

### Mission
Determine whether known, emerging or scheduled information may materially change risk, volatility, liquidity, correlation or directional conditions over relevant horizons such as:
- next 5–15 minutes;
- next 15–60 minutes;
- next 1–4 hours;
- remainder of trading session;
- next 24 hours where relevant.

It does not predict the future with certainty. It estimates event risk, source reliability, relevance, timing and plausible transmission channels.

### Source hierarchy
The agent should prefer, when technically/commercially available:
1. official central-bank/government/regulator sources;
2. official exchange/project/protocol announcements;
3. primary filings/releases/calendars;
4. high-quality financial news wires/publications;
5. specialized crypto-security/market sources;
6. broader web search for discovery;
7. social media only as low-trust discovery unless independently corroborated.

Rumors and unverified posts must be labeled and cannot silently become factual inputs.

### Event classes
- central bank decisions/speeches;
- CPI/PPI/PCE/employment/GDP and major macro releases;
- Treasury/rates/liquidity events;
- regulatory/enforcement developments;
- exchange listings/delistings/outages;
- major token unlocks/issuance/governance events;
- ETF/fund flows and related major announcements where reliable;
- protocol upgrades/chain incidents;
- hacks/exploits/security incidents;
- stablecoin depeg/reserve concerns;
- major bankruptcies/legal events;
- geopolitical shocks;
- large scheduled market events;
- unexpected breaking news with plausible crypto transmission.

### Structured event object
Each event should preserve:
- event id;
- detected/published/scheduled timestamps;
- source URLs/references;
- source reliability tier;
- whether confirmed/corroborated/unverified;
- affected symbols/market classes;
- expected time horizon;
- possible positive/negative/volatility-only impact;
- confidence/uncertainty;
- expected transmission mechanism;
- decay/expiry time;
- contradiction/corroboration set;
- agent/model/tool version.

### Impact reasoning
The agent should separate:
- `EVENT_EXISTS`
- `EVENT_RELEVANCE`
- `IMPACT_DIRECTION_UNCERTAIN`
- `VOLATILITY_RISK`
- `LIQUIDITY_RISK`
- `EXECUTION_RISK`
- `NO_TRADE_RECOMMENDED`

It must not reduce complex news to a naive bullish/bearish label.

## Agent communication protocol
Agents communicate through structured evidence envelopes rather than free-form hidden conversations as the system of record.

Each envelope should include:
- claim/recommendation;
- evidence references;
- confidence/calibration metadata;
- uncertainty;
- assumptions;
- time validity/expiry;
- affected symbols/timeframes;
- conflicts with other agents;
- requested follow-up work;
- agent identity/version;
- skill/tool versions used.

Free-form reasoning may assist an agent internally, but production decisions rely on structured, persisted evidence.

## Deliberation pattern
Candidate workflow:
`Parallel specialist analysis -> evidence board -> contradiction detection -> targeted cross-examination -> adversarial review -> supervisor synthesis -> deterministic Safety/Risk/Policy`

The goal is not unanimous agreement. The system must preserve dissent and be able to conclude `WAIT` or `NO_TRADE`.

## Tool Gateway
Agents access tools through a governed Tool Gateway. Candidate tool classes:
- web search/browsing;
- approved financial/economic/news APIs;
- exchange/market data read tools;
- chart/indicator/feature query tools;
- RAG retrieval;
- strategy/backtest/replay tools;
- portfolio/risk read tools;
- calculators/statistical tools;
- document/report retrieval;
- internal diagnostics.

Write/action tools require separate authorization policies. Agents do not obtain arbitrary shell/network/filesystem/exchange-write access merely because a model can call tools.

## Skill architecture
Agents may use reusable `skills`, defined as versioned governed procedures/tool recipes/analysis protocols.

Examples:
- `analyze_macro_release`
- `verify_breaking_crypto_news`
- `assess_exchange_outage_risk`
- `evaluate_pre_event_trade_risk`
- `compare_historical_event_analogs`
- `audit_strategy_conflict`

### Skill creation
Agents may propose new skills when repeated tasks lack an adequate existing procedure. Proposed skills enter:
`DRAFT -> STATIC_REVIEW -> SANDBOX_TEST -> EVALUATED -> APPROVED -> ACTIVE`

An agent may not silently create and activate a new production skill that expands its authority. Every active skill is versioned, permission-scoped, testable and auditable.

## Model/tool routing
Different agents may use different approved models/tools according to task requirements, latency, reliability and cost. Model choice is governed and observable; changing a model version must not silently alter authority.

## Memory
Use separate memory classes:
- immutable decision/audit history;
- market/event memory;
- strategy/trade episodes;
- agent operational lessons;
- short-lived working context.

Memories require provenance, timestamps and scope. Unverified web content must not contaminate canonical factual memory without validation.

## Agent evaluation
Each agent receives domain-specific tests, including:
- factual/source accuracy;
- calibration;
- false-positive/false-negative behavior;
- latency;
- tool selection quality;
- stale information detection;
- adversarial robustness;
- cross-agent communication quality;
- policy compliance;
- degraded-mode behavior.

For the News Agent specifically, evaluate event detection latency, source quality, duplication, rumor rejection, timing accuracy and whether risk classifications improve decisions without excessive no-trade behavior.

## Authority boundary
Even the Supervisor cannot place orders directly. Production flow remains:
`Agent Workforce -> Supervisor Candidate -> Safety Governor -> Risk Engine -> Session Policy -> Position/Leverage -> Execution -> Exchange Adapter -> Reconciliation`

Agents can recommend stricter actions or `NO_TRADE`; they cannot raise hard limits, bypass safety, self-promote models/skills/strategies or hide dissenting evidence.
