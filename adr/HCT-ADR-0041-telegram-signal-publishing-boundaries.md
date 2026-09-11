# HCT-ADR-0041 — Telegram Signal Publishing Boundaries

Status: `PROPOSED_FOR_DISCOVERY`
Date: 2026-09-11
Risk class: `HIGH_ASSURANCE`

## Context
HCT requires a commercial/community signal-room capability that publishes strategy-generated LONG/SHORT opportunities to Telegram while keeping signal dissemination separate from autonomous exchange execution.

## Decision
1. HCT will add a first-class `Signals` area to the product UI.
2. Signal definitions reuse the canonical HCT Strategy Definition / Strategy Builder concepts wherever practical.
3. Telegram distribution is implemented behind a provider-neutral `SignalPublisher` / destination adapter boundary.
4. The recommended Telegram topology is a broadcast channel for official signals plus an optional linked discussion group; groups/supergroups remain supported destinations.
5. Telegram bot credentials are backend-only secrets and never exposed to the frontend or strategy definitions.
6. Signal publication uses a durable outbox and idempotent delivery semantics rather than coupling decision generation directly to a network send.
7. A published signal is an informational/recommendation artifact, not an HCT exchange order and not proof that a subscriber executed it.
8. HCT supports up to three take-profit levels and up to three stop/invalidation levels, but multiple stops require explicit strategy semantics and unambiguous user-facing labels. Default presentation should prefer three TPs plus one primary hard stop unless the strategy intentionally defines multiple stop profiles/staged reduction.
9. Signal publication has its own freshness/latency gate. A signal that decays or moves outside its publication tolerance before Telegram dispatch may be suppressed as stale.
10. Signal-room performance must account for publication delay and plausible subscriber reaction delay; internal decision-price backtests are not sufficient to claim subscriber realizability.
11. Telegram publishing failure must not alter HCT trading state. The Harness may isolate Telegram destinations independently from live trading.
12. Signal content and marketing must not claim guaranteed profit. Jurisdictional/commercial review remains required before selling access.

## Consequences
- New module/capability: `Signal Publishing, Telegram Rooms & Subscriber Delivery Intelligence`.
- New UI navigation: `Signals`.
- New canonical artifacts: `SignalStrategy`, `SignalArtifact`, `SignalPublication`, `SignalRoom`, `SignalTemplate`, `PublicationOutbox`.
- New telemetry: publication freshness, Telegram API latency/errors, delivery state, duplicate suppression, lifecycle updates, subscriber-realizability metrics.
- Bootstrap implementation can remain low-cost using existing Postgres/Supabase plus an in-process publisher worker.

## Non-goals
- auto-trading a subscriber's exchange account from Telegram;
- guaranteeing outcomes;
- making Telegram the source of truth for HCT trading state;
- exposing bot tokens to clients;
- treating channel-message delivery as proof of a user's order/fill.
