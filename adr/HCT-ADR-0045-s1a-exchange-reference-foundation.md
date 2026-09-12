# HCT-ADR-0045 - S1A Exchange Reference Foundation

Status: `PROPOSED_FOR_IMPLEMENTATION`
Work Order: `HCT-IMP-0004-S1A`
Checkpoint: `HCT-CP-0021 / IMPLEMENTATION_AUTHORIZED_S1A`
Risk: `HIGH_ASSURANCE`

## Decision

S1A introduces a backend-owned, provider-neutral exchange reference boundary. The
boundary is immutable, read-only and network-free. It describes exchange metadata,
capability evidence and contract/reference facts; it does not execute exchange
actions or grant monetary authority.

## Identity placement

The existing canonical `StableId` and generated `IdentityKind` contract are
extended with the four identity kinds objectively required by this boundary:
`EXCHANGE`, `INSTRUMENT`, `CAPABILITY_SNAPSHOT` and `REFERENCE_SNAPSHOT`.
These kinds remain safe language-neutral identity values and are generated into
the existing backend/frontend projections. The exchange module owns only the
backend domain validation and reference behavior; it does not add frontend
product behavior.

Mutable display names and venue-native symbols are mapping metadata. They are
never the sole canonical identity of an exchange or contract. A native-symbol
mapping change produces different immutable reference/fingerprint evidence while
the canonical contract identity remains explicit.

## Capability semantics

Capability declarations use controlled states `SUPPORTED`, `UNSUPPORTED` and
`UNKNOWN`. `UNKNOWN` is an explicit absence of proof, is never truthy, and fails
closed in helper methods. A capability snapshot is immutable, versioned and
fingerprintable. Capability evidence describes reference truth only; it does not
authorize orders, leverage, account mutation or any other monetary action.

## Contract/reference semantics

Contract references use immutable provider-neutral records with canonical IDs,
exchange IDs, native-symbol mapping, lifecycle/type classification, safe asset
codes and exact `Decimal` increments and limits. Float values are rejected.
Zero/negative increments, invalid precision relationships and inconsistent bounds
are rejected. Material facts that are not known remain `None` and are not replaced
with permissive defaults. Fingerprints are deterministic over the complete
canonical reference content and source/version metadata.

## Adapter boundary

The `ExchangeReferenceAdapter` protocol exposes only description, capability
snapshot, reference listing and canonical/native reference resolution. It has no
state-changing exchange command surface. It does not authenticate, sign, open a
transport, read private account state or implement retry, quota, reconnect or
runtime session behavior.

The in-memory test adapter is deterministic, credential-free and network-free. It
is not a production venue adapter and does not claim live venue truth.

## Dependency order and deferred work

Concrete MEXC transport is deferred until later governed slices. Those slices may
depend on the S1A canonical reference and capability boundary, but must provide
their own authorization for transport, market ingestion, universe, quota,
realtime, account state and any mutation capability. S1A does not authorize those
slices and does not modify S0A, S0B or S0C authority/security/provenance
primitives.

## Authority proof

No S1A model or protocol method places, cancels or replaces an order, changes a
margin or risk setting, reads private account state, persists exchange state,
opens an external connection, handles credentials or changes deployment/live
authorization. The implementation therefore remains below the S1A authorization
ceiling and preserves the CP0021 production/live firewall.
