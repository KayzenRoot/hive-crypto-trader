# ADR-0050 — S1F realtime public market-value and ingest boundary

Status: `IMPLEMENTATION_AUTHORIZED_S1F`
Risk: `HIGH_ASSURANCE`

## Decision

S1F adds an immutable typed public market-value plane and a bounded public MEXC decoder/session seam. Module 4 owns normalized public values and provider quarantine; Module 5 remains the sole coherent Market-State owner; Module 7 remains the sole quality/DataAuthority owner; Module 29 remains the resource/admission owner. S1F never upgrades trust, resource, eligibility or lifecycle authority.

The canonical numeric policy is `DECIMAL_TEXT_V1` using `Decimal` only. Values are bound to source, channel, contract, environment, generation, schema, provenance, originating event and ordered lineage. `LIVE`, `PAPER`, `SHADOW` and `REPLAY` identities do not alias.

The MEXC surface is limited to `wss://contract.mexc.com/edge`, the six approved public channels and the three approved public REST path families from `S1F_MEXC_SOURCE_CONTRACT_V1`. Payloads are schema-validated before construction; unknown or contradictory data is quarantined. CI uses deterministic fixtures and never performs uncontrolled live network calls.

`S1F_MEXC_SOURCE_URL=https://mexcdevelop.github.io/apidocs/contract_v1_en/`

`S1F_MEXC_SOURCE_RETRIEVED=2026-09-13`

`S1F_MEXC_SOURCE_SHA256=57ebc13fea788a1c568c8aeabfdf50acc0c9f5b5a882af4855837d53499940e3`

`S1F_MEXC_SOURCE_CONTRACT_VERSION=S1F_MEXC_SOURCE_CONTRACT_V1`

`S1F_MEXC_PUBLIC_CHANNELS=sub.tickers,sub.ticker,sub.deal,sub.depth,sub.depth.full,sub.kline`

`S1F_MEXC_AUTHORIZED_PUBLIC_REST=GET /api/v1/contract/depth/{symbol};GET /api/v1/contract/depth_commits/{symbol}/{limit};GET /api/v1/contract/kline/{symbol}`

The primary source matrix is `TradeTick:sub.deal`, `TickerState:sub.ticker`, `BulkTicker:sub.tickers`, `CandleBar:sub.kline`, `OrderBookSnapshot:REST:/api/v1/contract/depth/{symbol}`, `OrderBookDelta:sub.depth:compress=false`, `FullDepth:sub.depth.full`, `ReferencePriceEvidence:sub.ticker`, `FundingEvidence:sub.ticker`; dedicated reference/funding channels are `OPTIONAL_CORROBORATION` only. Depth is `[price,contract_volume,order_count]`, with zero second-element removal and strict contiguous versioning. Kline closure is `NEXT_WINDOW_OR_REST_CONFIRMATION`; the provider has no final flag and the adapter never fabricates one.

`S1F_NUMERIC_POLICY_VERSION=DECIMAL_TEXT_V1` uses `Decimal`, precision `38`, scale `18`, integer digits `20`, lexical provider tokens and no binary floats. `S1F_INTERVAL_MODEL=HALF_OPEN_START_INCLUSIVE_END_EXCLUSIVE`; timestamps are UTC and values bind source, channel, contract, environment, generation, schema, provenance, originating event and ordered lineage.

## Quantity and authority rules

Trade, book, ticker and candle `q` values use `CONTRACTS_PROVIDER_NATIVE_V1`. `CandleBar.a` is a distinct `ProviderTransactionAmount`. No implicit conversion to base asset is available; mixed units fail closed. Public values are evidence, not orders, balances, positions, risk approval or execution authority.

## Runtime ownership

HCT owns bounded retry/backoff/circuit state, generation retirement, staged idempotent subscriptions, application-level MEXC ping and bounded admission. The library reconnect iterator is not used. REST transport has explicit timeout/connection bounds and `trust_env=False` so ambient proxy behavior cannot silently redirect it.

`S1F_RUNTIME_WS_CLIENT=websockets==17.1`

`S1F_RUNTIME_HTTP_CLIENT=httpx==0.28.1`

`S1F_RUNTIME_WS_API=websockets.asyncio.client`

`S1F_RUNTIME_DEPENDENCY_ALLOWLIST=apps/backend/pyproject.toml;apps/backend/uv.lock`

`S1F_RUNTIME_DEPENDENCY_DELTA=httpx==0.28.1:dev_to_runtime;websockets==17.1:add_direct_runtime`

`S1F_RUNTIME_RECONNECT_OWNERSHIP=HCT_BOUNDED_RETRY_BACKOFF_CIRCUIT;NO_INFINITE_LIBRARY_MANAGED_ITERATOR`

`S1F_RUNTIME_PROVIDER_PING=application_level_MEXC_ping_authoritative;library_ping_frames_not_substitute`

`S1F_RUNTIME_QUEUE_POLICY=explicit_bounded_inbound_queue;Module29_backpressure;no_unbounded_receive_queue`

`S1F_QUANTITY_UNIT_KIND=QuantityUnit:CONTRACTS_PROVIDER_NATIVE_V1`; `CandleBar.a` remains `ProviderTransactionAmount`; no implicit base-asset conversion or mixed-unit upgrade exists.
