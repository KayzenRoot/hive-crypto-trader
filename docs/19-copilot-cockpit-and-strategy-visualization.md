# Copilot Cockpit & Strategy Visualization

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R02`

## Design direction
The Copilot experience is a first-class operational cockpit, visually aligned with the premium technological company design language established by Hive Plan while remaining specific to trading.

The cockpit should feel like a living realtime system: motion, depth, 3D/volumetric cues and rich data visualization may be used, but never at the expense of legibility, latency awareness or risk communication.

## Copilot session setup screen
Before autonomous operation starts, present a governed session configuration surface with clear, reviewable controls for:
- autonomy mode;
- daily maximum loss;
- daily profit target or open-target mode;
- risk per trade;
- leverage ceiling/policy;
- maximum concurrent positions;
- maximum portfolio exposure;
- allowed strategies;
- allowed/blocked symbols;
- operating hours;
- volatility tolerance;
- news/event behavior;
- cooldown rules;
- trailing-stop policy;
- TP/SL policy;
- partial-exit policy;
- emergency-stop behavior.

Before activation, render a human-readable summary of what the Copilot is allowed and forbidden to do.

## Main Copilot cockpit
Candidate realtime regions:
1. account equity / realized and unrealized PnL;
2. daily loss budget consumed/remaining;
3. current autonomy mode and session policy hash/version;
4. Safety Governor state;
5. scanner/opportunity queue;
6. current positions and orders;
7. active strategy/model versions;
8. agent activity/status;
9. agent disagreement / adversarial review state;
10. API/WebSocket/data freshness health;
11. news/event risk status;
12. current market regime;
13. decision timeline;
14. kill switch / pause-new-trades control.

## Symbol workspace
When a user selects a symbol, show a realtime chart and an explainable intelligence layer around it.

Potential overlays:
- entries/exits;
- stop-loss / take-profit / trailing-stop paths;
- strategy signal markers;
- indicator overlays;
- detected candle/chart patterns;
- market-regime bands;
- liquidity/volatility zones;
- support/resistance/structure;
- proprietary HCT indicator panels;
- historical analogue markers;
- agent confidence/disagreement events;
- current position average price and liquidation-distance context when applicable.

## Strategy visualization
Users should be able to select a strategy and inspect how it is behaving on the chosen symbol/timeframe.

Plan for:
- historical signal overlays;
- active setup state;
- current entry/exit conditions;
- which conditions are satisfied/not satisfied;
- confidence and uncertainty;
- simulated/paper performance context;
- regime compatibility;
- reasons for `NO_TRADE`;
- agent disagreements;
- projected TP/SL/trailing scenarios where appropriate.

The chart must distinguish clearly between actual executed orders and hypothetical/simulated strategy paths.

## Agent visualization
The cockpit may expose agents as operational nodes rather than chat avatars. Each node can show status such as `OBSERVING`, `ANALYZING`, `AGREE`, `DISAGREE`, `VETO_RECOMMENDED`, `WAITING`, `DEGRADED`.

A trade decision may be visualized as an evidence graph flowing from market data through agents to Supervisor, Safety, Risk, Policy and Execution.

## Realtime safety UX
Critical states such as stale market data, exchange uncertainty, reconciliation failure, exceeded daily loss, disconnected user stream or Safety Governor intervention must visually dominate profit animations and decorative 3D elements.

## Audit UX
Every executed action should be explorable later as a decision trace: what the market looked like, which strategy/model/agents participated, which limits were active, what evidence supported/opposed the trade and what happened afterward.
