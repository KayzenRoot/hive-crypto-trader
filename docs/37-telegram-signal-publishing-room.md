# Telegram Signal Publishing & Signal Room

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R02`
Risk class: `HIGH_ASSURANCE`

## Objective
Add a first-class **Signals** product area to HCT and a governed Telegram distribution capability so approved signal strategies can publish structured LONG/SHORT trading signals to a Telegram signal room.

This is a publishing/distribution capability, not a bypass around HCT strategy, data-quality, intelligence, safety or audit governance.

## Product experience
The HCT sidebar includes a dedicated **Signals** menu.

Candidate sub-areas:
- `Signal Rooms`
- `Signal Strategies`
- `Telegram Connections`
- `Templates`
- `Published Signals`
- `Performance`
- `Subscribers / Entitlements` (commercial phase)
- `Delivery Health`
- `Audit Trail`

## Recommended Telegram topology
Preferred commercial pattern:

`HCT Signal Publisher -> Telegram Broadcast Channel -> Subscribers`

Optionally:

`Telegram Broadcast Channel <-> Linked Discussion Group`

Why:
- the channel keeps official signals clean and chronological;
- the discussion group can host community conversation without polluting the signal feed;
- HCT remains able to support a supergroup/group destination when explicitly configured.

The Telegram Bot API supports sending formatted text messages to target chats/channels. Posting to channels requires the bot to have the necessary administrative/posting permission.

## Signal Strategy concept
A signal room does not need to use the same strategy that autonomously trades an HCT account.

Each Signal Strategy is an immutable/versioned declarative strategy profile that may define:
- market universe / symbol allow-list;
- LONG / SHORT / both;
- timeframes;
- indicators and parameters;
- HCT proprietary indicators where exposed;
- candlestick/chart patterns;
- market structure;
- microstructure/order-flow features;
- liquidity/breadth/cross-market evidence;
- regime conditions;
- temporal-memory / historical-analog evidence where approved;
- news/event restrictions;
- minimum data-quality and market-state integrity;
- minimum calibrated confidence;
- minimum opportunity score/components;
- cooldown / duplicate suppression;
- entry model;
- stop model;
- TP model;
- expiration/time-to-live;
- publishing schedule / allowed hours;
- delivery destinations;
- localization/template.

Signal strategies use the same Strategy Definition and validation concepts as the HCT Strategy Engine wherever practical, avoiding a second incompatible strategy language.

## Separation from autonomous trading
A published signal is a **recommendation artifact**, not an exchange order.

Conceptual path:

`Market Data -> HCT Intelligence -> Signal Strategy -> Signal Candidate -> Signal Publication Policy -> Telegram Publisher`

The Telegram Publisher never receives exchange credentials and never converts a Telegram publication into an HCT live order.

The user receiving the signal decides whether and how to trade it.

## Canonical Signal Artifact
Every signal receives an immutable ID and versioned evidence snapshot.

Candidate fields:
- signal ID;
- tenant/room ID;
- strategy ID/version;
- symbol and exchange market;
- direction `LONG` / `SHORT`;
- creation time;
- source market-state generation ID;
- valid-from / expires-at;
- entry model and entry zone;
- reference market price at publication;
- up to three take-profit levels;
- up to three stop/invalidation levels when enabled;
- recommended/default stop profile;
- optional leverage information only if policy allows it;
- confidence and calibration state;
- market/regime context;
- risk/reward estimates;
- signal rationale summary;
- risk/disclaimer text;
- evidence/provenance reference;
- Telegram destination(s);
- publication status;
- Telegram message ID(s);
- outcome lifecycle state.

## Three TP / three SL requirement
HCT supports up to:
- `TP1`, `TP2`, `TP3`;
- `SL1`, `SL2`, `SL3`.

However multiple stops must be semantically explicit. Three unrelated stop prices can confuse subscribers and create unsafe copy behavior.

Recommended default:
- three staged profit targets;
- one clearly marked **Primary / Hard Stop**;
- optional `SL2` and `SL3` only when the strategy explicitly defines staged risk reduction, alternative risk profiles, or invalidation zones.

If multiple SL levels are published, the message must explain their meaning. HCT must never display three stops as if all should be blindly placed simultaneously when the strategy does not define that behavior.

## Example Telegram rendering
Illustrative only:

`🚨 HCT SIGNAL | LONG`

`🪙 BTCUSDT PERP`
`🏦 MEXC Futures`

`🎯 Entry: 61,180 - 61,260`

`✅ TP1: 61,650`
`✅ TP2: 62,050`
`✅ TP3: 62,780`

`🛡️ SL1 / Primary: 60,840`
`🛡️ SL2 / Conservative: 60,620` *(only if strategy semantics support it)*
`🛡️ SL3 / Hard invalidation: 60,300` *(only if enabled)*

`📊 Confidence: 78% (CALIBRATED)`
`🌊 Regime: Bullish volatility expansion`
`⏳ Signal TTL: 18 min`

`🧠 Context: trend + breadth + order-flow confirmation`

`⚠️ Trading futures involves substantial risk. This is a market signal, not a guarantee of profit.`

The actual production message template is localized and versioned.

## Telegram formatting
Prefer Bot API regular formatted messages using HTML or MarkdownV2 for concise signal cards. Richer Telegram message capabilities may be evaluated later, but HCT must preserve a plain-text-compatible representation.

Message construction must safely escape Telegram formatting characters/content generated from external data.

## Signal lifecycle
Candidate lifecycle:

`CANDIDATE -> POLICY_VALIDATED -> READY_TO_PUBLISH -> PUBLISHING -> PUBLISHED -> ACTIVE -> PARTIAL_TARGET -> TARGET_COMPLETE / STOPPED / EXPIRED / CANCELLED / INVALIDATED`

Failures:

`DELIVERY_FAILED -> RETRY_PENDING -> DELIVERED / DEAD_LETTER`

Telegram delivery failure must not alter exchange/trading state.

## Updates after publication
HCT may publish follow-up messages for:
- entry reached;
- TP1 / TP2 / TP3 reached;
- stop/invalidation reached;
- signal expired;
- signal cancelled;
- protective stop moved if the signal strategy allows updates;
- strategy-specific partial-close guidance;
- corrected message only under explicit correction policy.

Prefer replies/linked updates using stored Telegram message IDs where practical so the room has a traceable signal thread.

## Duplicate and spam control
Signal Publisher must prevent noisy rooms:
- canonical idempotency key per signal publication;
- symbol/strategy cooldown;
- duplicate-equivalence detection;
- minimum material-change threshold for update posts;
- destination rate control;
- retry with bounded exponential backoff;
- dead-letter state after retry exhaustion;
- publishing circuit breaker if Telegram/API health degrades.

## Publication Policy Gate
Before publishing a new entry signal, the publisher verifies:
- Signal Strategy version is active;
- destination is enabled;
- market data is sufficiently fresh;
- signal has not expired;
- required evidence remains coherent;
- current price has not moved outside publication tolerance;
- duplicate/cooldown rules pass;
- Telegram destination is healthy enough;
- room policy allows the symbol/direction/session;
- disclaimer/template version is current.

A signal may become stale between decision and Telegram delivery. Therefore publication has its own latency/freshness budget.

## HCT Signal Publication Age
Research metric:

`signal decision time -> rendered message -> Telegram API accepted -> observed delivery/ack where available`

This tracks how much of the signal lifetime is consumed before subscribers can act.

Possible states:
- `FRESH`
- `AGING`
- `STALE_DO_NOT_PUBLISH`

## Performance analytics
Signal room performance must not be evaluated using cherry-picked calls.

Track:
- signals generated;
- signals suppressed and why;
- LONG/SHORT counts;
- expired before publication;
- delivery success/failure/latency;
- TP1/TP2/TP3 hit rates;
- primary stop hit rate;
- max favorable/adverse excursion after publication;
- time to target/stop;
- hypothetical return under explicitly defined evaluation rules;
- performance by strategy/version/symbol/regime/timeframe;
- calibration/reliability;
- signal coverage/selectivity;
- performance after realistic subscriber-reaction latency assumptions.

Public marketing metrics require separate governance and must not imply guaranteed future returns.

## Subscriber delay realism
A Telegram subscriber does not execute at the HCT decision timestamp.

Signal evaluation should include configurable reaction delays such as:
- publication/API latency;
- Telegram delivery delay;
- human reading/reaction time;
- manual exchange-entry delay;
- price movement after publication.

This produces a more honest **Subscriber Realizability** measure rather than scoring only against the ideal internal decision price.

## Proprietary HCT signal-room research candidates
1. **HCT Signal Publication Freshness Score (SPFS)** — measures signal usefulness remaining at subscriber publication time.
2. **HCT Subscriber Realizability Score (SRS)** — estimates whether a typical delayed human follower could plausibly obtain a useful entry.
3. **HCT Signal Clarity Score (SCS)** — validates that entry/TP/SL semantics are sufficiently unambiguous for publication.
4. **HCT Signal Crowd-Delay Simulator (SCDS)** — evaluates signal outcome under distributions of follower reaction delays.
5. **HCT Signal Lifecycle Quality Score (SLQS)** — combines freshness, delivery, clarity, realized path and update quality.
6. **HCT Publication Opportunity Decay (POD)** — estimates how quickly the edge decays between internal detection and public dissemination.

All are research concepts until validated.

## Security
- Telegram bot token is a backend secret and never exposed to frontend clients.
- Tokens use SecretStore abstraction and rotation policy.
- Signal-room configuration is tenant/admin scoped.
- Sending privileges are least-privilege.
- Webhook endpoints, if used, require Telegram-compatible validation/secret controls and HCT gateway protections.
- Telegram destination IDs and configuration changes are audited.
- Users cannot inject arbitrary unsanitized Telegram markup into protected templates.
- A compromised Telegram destination must be isolatable by the Harness without disabling trading.

## Harness controls
Scopes:
- global Telegram publishing;
- tenant;
- signal room;
- destination;
- strategy;
- symbol/direction;
- new-signal publishing;
- lifecycle-update publishing.

States may include:
`ENABLED / DEGRADED / PAUSED / QUARANTINED / DISABLED`.

Pausing Telegram publishing must not pause HCT trading unless an independent trading control also requires it.

## UI requirements
### Sidebar
Add `Signals` as a first-class product navigation item.

### Signal Room editor
Candidate controls:
- room name;
- Telegram destination;
- active strategy/version;
- symbols/universe;
- direction;
- timeframe;
- required confidence;
- entry/stop/TP configuration;
- up to 3 TP and 3 SL levels;
- publication TTL;
- cooldown;
- template/language;
- disclaimer;
- enabled state;
- test-message action;
- preview;
- delivery-health indicator.

### Signal strategy workspace
Reuse Strategy Builder/nodal graph where practical instead of inventing a separate rules engine.

### Signal timeline
Show:
- candidate time;
- publish time;
- Telegram message status;
- current lifecycle;
- target/stop events;
- outcome and metrics;
- evidence snapshot;
- message preview/history.

## Localization
Canonical templates and identifiers are English-first (`en-US`), with first-class `pt-BR` and `es` template resources. Room owners choose the publication locale per destination.

## Bootstrap cost
Telegram Bot API publishing itself does not require a paid HCT infrastructure provider. The module should run inside the existing backend/trading-worker topology where safe.

For early scale:
- no separate paid queue is required initially;
- a durable outbox table in Postgres/Supabase can hold publication jobs/status;
- an in-process worker can dispatch messages;
- migrate to dedicated queue/event infrastructure only when measured volume/reliability justifies it.

## Durable Outbox rule
Do not couple signal creation directly to a fragile network send.

Preferred bootstrap pattern:

`Signal Approved -> DB transaction writes Signal + PublicationOutbox -> Publisher Worker -> Telegram API -> store Telegram message ID/status`

This prevents a transient Telegram failure from losing an approved publication artifact and enables idempotent retry.

## Compliance / communication guardrails
The product must clearly distinguish:
- market signal;
- hypothetical performance;
- actual HCT live execution;
- user manual execution;
- past results;
- future expectations.

Signal messages must not claim guaranteed profit or certainty. Regional/legal/commercial review remains required before selling signal-room access in specific jurisdictions.

## Current Telegram API discovery snapshot — 2026-09-11
Official Telegram documentation currently confirms:
- Bot API `sendMessage` can target a chat, supergroup or channel username/ID;
- text messages support formatting including HTML and MarkdownV2;
- channels are designed for broadcast to large audiences;
- a bot needs the appropriate administrator/posting rights to publish into a channel.

These external API details must be verified again during implementation.

## Planning status
This document adds product discovery only. It does not authorize implementation, subscriber commercialization or public performance claims.
