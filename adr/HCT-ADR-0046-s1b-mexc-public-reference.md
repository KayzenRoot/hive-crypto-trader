# HCT-ADR-0046 — S1B MEXC Public Reference Boundary

Status: `IMPLEMENTED_FOR_HCT-IMP-0005-S1B`
Risk: `HIGH_ASSURANCE`
Checkpoint: `HCT-CP-0023 / IMPLEMENTATION_AUTHORIZED_S1B`
Authorization ceiling: `NON_TRADING_STAGE_1_MEXC_PUBLIC_REFERENCE_CAPABILITY_RESOLVER_ONLY`

## Decision

S1B uses one concrete MEXC Futures public reference read, `GET
https://api.mexc.com/api/v1/contract/detail`, behind the approved S1A
`ExchangeReferenceAdapter` port. The production transport is HTTPS-only,
unauthenticated, finite, bounded and read-only. Provider-native values are
parsed inside the MEXC boundary and translated into immutable S1A canonical
models. No MEXC payload dictionary or provider DTO crosses that boundary.

This decision adds reference evidence only. It does not grant Security, Risk,
Execution, order, account, private-state, deployment or live-trading authority.

## Official provider evidence

The following first-party MEXC sources were consulted on `2026-09-12` at
`2026-09-12T19:29:32Z` UTC. The timestamp records this execution's access
time; the source content remains external evidence and is not authorization.

1. [MEXC Futures integration guide](https://www.mexc.com/api-docs/futures/integration-guide)
   — current official documentation entry point and Futures API scope.
2. [MEXC Contract API reference](https://mexcdevelop.github.io/apidocs/contract_v1_en/)
   — `Get the contract information`, `GET api/v1/contract/detail`, response
   fields `symbol`, `displayNameEn`, `baseCoin`, `quoteCoin`, `settleCoin`,
   `priceScale`, `volScale`, `priceUnit`, `volUnit`, `minVol`, `maxVol` and
   `state`.
3. [MEXC Futures API access domain update](https://www.mexc.com/announcements/article/futures-api-access-domain-update-17827791532974)
   — official migration from `https://contract.mexc.com` to
   `https://api.mexc.com`; the old host is not allowlisted.
4. [MEXC API overview](https://www.mexc.com/mexc-api)
   — current official reference to the Futures contract-detail endpoint at
   `https://api.mexc.com/api/v1/contract/detail`.

## Allowlist and transport policy

- Allowlisted host: `api.mexc.com` only.
- Allowlisted base URL: `https://api.mexc.com` only.
- Allowlisted path: `/api/v1/contract/detail` only.
- Method: `GET` only; no query string, caller-supplied path or caller-supplied
  URL is accepted.
- TLS is required. Redirects are not followed by the bounded transport.
- Connect timeout: `2.0` seconds.
- Per-read timeout: `3.0` seconds.
- Total operation deadline: `5.0` seconds.
- Maximum response body: `262144` bytes; body is read in bounded `8192` byte
  chunks.
- Required response status: `200`.
- Required content type: JSON media type (`application/json`, including a
  permitted media-type parameter).
- No automatic retry, connection pool, background session, streaming,
  subscription, reconnect or circuit/quota runtime is introduced.
- Transport failures become bounded `ReferenceUnavailableError` failures;
  they never produce an apparent successful empty/default reference.

## Provider boundary and canonical translation

The response envelope must contain `success=true`, `code=0` and a non-empty
`data` list. Each material contract entry is validated before translation.
Unknown extra provider fields are ignored; they cannot mutate canonical
semantics. Missing, malformed, contradictory or unrecognized material values
fail closed with a bounded reference error.

| MEXC field | S1A canonical result | Rule |
| --- | --- | --- |
| `symbol` | `ContractReference.native_symbol` | Mapping metadata only; validated string, never the sole canonical identity. |
| `baseCoin` | `base_asset` | Uppercase canonical token; participates in deterministic instrument identity. |
| `quoteCoin` | `quote_asset` | Uppercase canonical token; participates in deterministic instrument identity. |
| `settleCoin` | `settlement_asset` | Uppercase canonical token; participates in deterministic instrument identity. |
| `displayNameEn` | `contract_type=PERPETUAL` | Accepted only when the documented reference shape explicitly identifies a `SWAP`; otherwise unavailable. |
| `state=0` | `lifecycle=ACTIVE` | Official meaning: enabled. |
| `state=1..4` | `lifecycle=INACTIVE` | Official meanings: delivery, completed, offline or pause. Unknown states fail closed. |
| `priceUnit` | `price_increment` | Parsed as exact JSON decimal; positive and finite. |
| `volUnit` | `quantity_increment` | Parsed as exact JSON decimal; positive and finite. |
| `priceScale` | `price_precision` | Non-negative integer and not less precise than `priceUnit`. |
| `volScale` | `quantity_precision` | Non-negative integer and not less precise than `volUnit`. |
| `minVol` / `maxVol` | `min_quantity` / `max_quantity` | Positive exact decimals, ordered and aligned to `volUnit`. |
| `contractSize` | deferred | Not represented by the approved S1A model; not silently substituted for quantity increment. |
| leverage, margin, risk-tier and fee fields | deferred/unknown | Provider facts are not mapped into trading authority or a new risk model in S1B. |
| `apiAllowed` | deferred/unknown | The S1B public reference transport is already proven by the endpoint; this field cannot authorize private or state-changing API use. |

Canonical instrument IDs are deterministic hashes of the normalized
`baseCoin`, `quoteCoin`, `settleCoin` and `PERPETUAL` type. A native symbol or
display-name change therefore changes mapping/reference evidence but does not
silently redefine the canonical identity. Snapshot/reference IDs are derived
from normalized material evidence and are immutable for the loaded result.

Capability declarations are conservative: exchange description, public
reference and contract reference are `SUPPORTED` only after the bounded
response validates; private state, state change and margin configuration remain
`UNKNOWN` because this slice neither proves nor implements those capabilities.
`UNKNOWN` is never truthy or default-upgraded, and capability metadata exposes
no command method.

## Deferred scope

Universe eligibility, API quota and backpressure, WebSocket/session/reconnect,
realtime market data, Data Quality/Freshness, Market-State, cache/hot state,
private/account state, credentials/signing, orders, fills, positions, balances,
OMS, reconciliation, protection, persistence, public trading routes,
deployment, limited-live and real-money trading remain deferred to separately
authorized slices.

## Validation strategy

Tests use deterministic JSON fixtures derived from the documented response
shape and an injected fake transport. CI never calls MEXC, DNS or the public
internet. Focused negative tests cover URL/host/path enforcement, timeout and
response bounds, JSON/content/schema failures, decimal/rule contradictions,
unknown lifecycle/type, canonical identity stability and UNKNOWN capability
semantics. The S1B scanner fails closed for changed-file escape, unauthorized
network/auth/private/stream/order/persistence/deployment surfaces and generic
external URLs.
