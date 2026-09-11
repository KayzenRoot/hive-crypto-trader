# Multi-Exchange Adapter Architecture

Status: `DISCOVERY_IN_PROGRESS`
Increment: `HCT-PLAN-0001-R02`
Risk class: `HIGH_ASSURANCE`

## Scope decision
V1 trades only on MEXC Futures. Multi-exchange live trading is OUT OF SCOPE for V1 implementation, but the architecture must avoid MEXC-specific coupling in core trading, strategy, risk and UI domains so Binance and additional exchanges can be added later with bounded work.

## Core principle
Core HCT modules depend on a canonical exchange interface, not directly on MEXC request/response models.

Conceptual boundary:
`HCT Core -> Exchange Capability Interface -> Exchange Adapter -> MEXC/Binance/Future Exchange`

MEXC is the first concrete adapter and the only enabled live adapter in V1.

## Exchange Capability Interface
A normalized exchange contract should represent capabilities rather than assuming every exchange behaves identically. Candidate capability families:
- market/symbol discovery;
- contract specification;
- price/ticker/candle streams;
- trades/order-book streams;
- mark/index/fair-price concepts where supported;
- funding/open-interest data where supported;
- account/balance queries;
- positions;
- order placement;
- order cancel/replace;
- trigger/conditional orders;
- TP/SL;
- trailing-stop variants;
- leverage/margin configuration;
- private user streams;
- rate-limit metadata;
- authentication/signing requirements;
- reconciliation semantics.

## Capability matrix
Each adapter must expose a versioned capability matrix. HCT should query capabilities and degrade or hide unsupported functionality rather than emulate silently.

Example fields:
- `supports_market_order`
- `supports_limit_order`
- `supports_reduce_only`
- `supports_native_tp_sl`
- `supports_native_trailing`
- `supports_partial_close`
- `supports_hedge_mode`
- `supports_isolated_margin`
- `supports_cross_margin`
- `supports_private_ws`
- `supports_funding_data`
- `supports_open_interest`
- supported trigger price types
- supported time-in-force values
- symbol-specific leverage/size/precision limits

## Canonical domain models
Normalize core concepts into HCT-owned models for:
- Exchange
- Market
- Instrument/Contract
- Ticker
- Candle
- Trade
- OrderBook
- Funding
- OpenInterest
- OrderIntent
- ExchangeOrder
- Fill
- Position
- Balance
- AccountSnapshot
- CapabilitySnapshot
- RateLimitBudget

Raw exchange payloads may be retained for evidence/debugging, but must not leak throughout the domain model.

## Symbol identity
Do not use exchange-native strings as the only identity. Maintain canonical instrument identity plus exchange mapping, because names, quote assets, contract types and precision differ across venues.

## Error normalization
Adapters map exchange-specific errors into HCT canonical classes while retaining raw codes/messages for audit:
- authentication/permission;
- rate limit;
- invalid order;
- insufficient balance/margin;
- stale/invalid timestamp;
- unavailable market;
- unsupported capability;
- transient exchange failure;
- uncertain execution outcome;
- reconciliation mismatch.

## Rate limits and resilience
Rate limits remain exchange-specific. Each adapter publishes its quota/budget semantics to the API Quota, WebSocket & Backpressure Governor. No generic adapter may assume equal limits or subscription behavior.

## Exchange state remains authoritative
Order/fill/position/balance truth is scoped per exchange account. Reconciliation must operate through the adapter and preserve venue-specific evidence.

## Strategy portability
Strategy definitions should express required capabilities, not hard-code an exchange where avoidable. A strategy may be portable only when its required data/order semantics exist on the target exchange. Compatibility must be evaluated explicitly.

## UI portability
The cockpit may show a future exchange selector/account selector, but V1 exposes only MEXC for live trading. Unsupported future venues must not appear as functional choices before implementation/authorization.

## Future exchanges
Expected future candidates include Binance and other approved exchanges. Adding any new venue requires:
1. adapter implementation;
2. capability mapping;
3. security/key-management integration;
4. rate-limit policy;
5. reconciliation tests;
6. order-semantics tests;
7. paper/shadow validation;
8. HIGH_ASSURANCE review;
9. explicit production promotion.

## Non-goal
This architecture does not claim 'write once, identical behavior everywhere'. Exchanges differ materially. The goal is controlled isolation of venue differences so core HCT logic remains stable while exchange-specific behavior is explicit and testable.
