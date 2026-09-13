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

## H007-H010 correction boundary

Sequence continuity is evaluator-issued typed state. A synchronization point
may be carried only through that state across accepted contiguous deltas;
gaps, out-of-order, unprovable sequence, retired generation and context
changes invalidate it. A later explicit valid snapshot is the deterministic
resynchronization point. Sequence modes that cannot prove continuity never
invent it.

Synchronization proofs, cache projections and resource evidence do not have
permissive public constructors. Synchronization proofs are derived from an
evaluator-issued successful observation and bind source, generation, capability
fingerprint and policy version. `project_state` is the only projection path;
invalidation preserves source authority material and only tightens freshness.
Module 29 resource evidence is derived only from a canonical
`AdmissionDecision` from ADR-0048. The bounded mapping is `ADMIT` to
`AVAILABLE`, `DEFER` to `DEGRADED`, `SHED`/`CIRCUIT_OPEN` to `DENIED` and
`UNKNOWN` to `UNKNOWN`, preserving the decision fingerprint and typed outcome
and reason.

`TRUSTED` Market-State requires clean market-truth reasons, evaluator-issued
matching synchronization proof, coherent provenance and a non-retired current
generation. `RESOURCE_DEGRADED` alone remains a separate restrictive resource
axis and may coexist with otherwise trusted market truth. Resource evidence,
projections and lifecycle restrictions cannot upgrade stale, gapped,
contradictory, expired or otherwise untrusted market data.

The H011/H012 hardening closes the remaining permissive paths. A synchronized
`SequenceEvaluation` is evaluator-issued only and carries valid attested
continuity with a synchronization anchor; direct synchronized construction,
missing continuity and synchronized duplicate evidence fail closed. The quality
assessment and authority derivation repeat this fence defensively, so
`ALLOW_NEW_EXPOSURE` cannot arise from caller-created or unproven continuity.

`SynchronizationProof` materializes contract, channel, schema and visibility
from the `ChannelCapability`, and requires a non-null contract scope for a
trusted contract-scoped state. It binds both the exact synchronization anchor
and the latest accepted event. `MarketStateSnapshot` must match that context
and contain both proof fingerprints in its event lineage; cross-contract,
cross-channel, schema/visibility-mismatched, retired-generation or incomplete
lineage evidence is rejected before `TRUSTED`.

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
