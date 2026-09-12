# ADR-0047 — S1C Market Universe Registry boundary

Status: Accepted for `HCT-IMP-0006-S1C` only

## Decision

S1C adds a provider-neutral, pure Market Universe Registry surface. It consumes
only the normalized S1A/S1B `ExchangeDescriptor`, `CapabilitySnapshot` and
`ContractReference` values and returns immutable structural snapshots. It does
not fetch, rank, persist or authorize trading.

The registry owns canonical structural universe membership and its
`ELIGIBLE`/`INELIGIBLE`/`UNKNOWN` state. `ExchangeReferenceAdapter`, the MEXC
provider layer, quota/session controls, realtime market data, Data Quality,
Market-State, cache, Scanner, Risk, Safety, Session, OMS and Execution retain
their existing boundaries and authority. `ELIGIBLE` means only that the
bounded structural policy is proven; it never means safe-to-trade, live-ready,
risk-approved or execution-authorized.

## Typed state and fail-closed policy

`UniverseEligibilityState` has exactly `ELIGIBLE`, `INELIGIBLE` and `UNKNOWN`.
`UniverseReasonCode` is a finite enum. A complete structural proof emits
`ELIGIBLE_REFERENCE_PROVEN`; an explicit lifecycle or contract-type
disqualifier emits an `INELIGIBLE_*` reason; missing or unknown mandatory
capability/reference evidence emits an `UNKNOWN_*` reason. Unknown is never
coerced to ineligible or eligible.

Duplicate canonical IDs, duplicate native mappings, contradictory mappings or
cross-exchange inputs are consistency failures and produce no snapshot. The
registry rejects malformed typed inputs instead of accepting booleans, defaults,
raw dictionaries or provider DTOs as evidence.

## Identity, environment, version and determinism

The canonical `IdentityKind.UNIVERSE_SNAPSHOT` identifies a universe snapshot;
`REFERENCE_SNAPSHOT` remains the source identity for a contract reference.
Each snapshot binds one `ExchangeID`, one `Environment`, the capability and
reference source identities/versions/fingerprints, a positive policy version,
deterministically ordered immutable entries and a SHA-256 fingerprint.

The recompute timestamp is metadata and is not fingerprint material. The
fingerprint uses sorted canonical IDs and normalized source material, so input
order and provider display/native metadata order cannot change an otherwise
identical result. A caller may inject `recomputed_at` for reproducible
observation metadata. S1C has no persistence or database-backed monotonic
counter; a material policy/source/input change changes the fingerprint.

## Explicit non-goals

This ADR authorizes no network client, URL/endpoint, WebSocket or realtime
ingest, quota/backpressure/retry runtime, liquidity/volume/spread/volatility,
ranking/scanning, credentials/private/account/order/position/balance path,
trading/risk/safety/session/OMS/execution behavior, persistence, frontend
trading control, deployment, limited-live or real-money trading.
