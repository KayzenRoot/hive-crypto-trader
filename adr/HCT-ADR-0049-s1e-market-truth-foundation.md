# ADR-0049 — S1E Market Truth Foundation boundary

Status: `IMPLEMENTATION_AUTHORIZED_S1E`
Risk: `HIGH_ASSURANCE`

## Decision

S1E owns only provider-neutral immutable contracts and deterministic predicates
for normalized public market events, channel sequence capability, Data Quality,
generation-scoped Market-State trust, cache projections and read-only seams to
S1C lifecycle evidence and Module 29 resource evidence.

Module 4 owns normalized event identity and provenance. Module 7 owns quality
predicates and the six canonical restrictive `DataAuthorityState` values.
Module 5 is the sole Market-State trust owner and requires explicit generation
and synchronization proof. Module 30 owns projections and freshness leases
only. ADR-0047 remains the sole universe/lifecycle owner and ADR-0048 remains
the sole resource/admission owner.

`INELIGIBLE` and `UNKNOWN` universe evidence block new/add exposure and
candidate admission through separate lifecycle restriction metadata. They do
not by themselves downgrade valid Market-State trust or remove safety-oriented
consumer evidence. Independent stale, gap, clock, contradiction, schema,
generation or synchronization evidence controls trust and data authority.

## Deterministic safety rules

- All five sequence modes are finite and fail closed when proof is absent.
- `NO_PROVABLE_SEQUENCE` yields `SEQUENCE_UNPROVABLE` for continuity-dependent
  use; monotonic jumps are gaps only when contiguity is proven.
- A retired or prior generation cannot mutate current trusted state.
- A cache projection carries source, generation, provenance, fingerprint,
  freshness lease, invalidation and lifecycle metadata; it has no reverse path
  that originates or upgrades authority.
- Resource denial/unknown is restrictive evidence and cannot mark data fresh or
  promote trust.

## Explicit non-scope

No socket, WebSocket, endpoint, venue DTO, network client, credential, private
API, persistence, database, deployment, scanner/ranking, strategy, Brain,
agent, order, Risk, OMS, Execution, limited-live or live-trading capability is
implemented here. Fixtures and replay are deterministic and contain no live
calls.

## Authorization and verification

The implementation is authorized only by `HCT-CP-0029` for
`HCT-IMP-0008-S1E`, with ceiling
`NON_TRADING_STAGE_1_MARKET_TRUTH_FOUNDATION_ONLY`. The implementation PR must
remain open and unmerged for fresh independent HIGH_ASSURANCE review.
