# HCT-ADR-0044 — S0C Audit/Evidence Integrity and Configuration Provenance

Status: `ACCEPTED_FOR_IMPLEMENTATION`

## Context

HCT-IMP-0003-S0C is authorized only for the non-trading Stage-0 foundation
for audit/evidence integrity and configuration, release, and policy provenance.
The public S0A envelopes and generated OpenAPI projections are already frozen.
S0B supplies typed environment, tenant, account, and opaque-reference
boundaries. S0C must therefore add backend-domain integrity semantics without
creating a second public contract or a route that can be called by a client.

## Decisions

1. S0C composes the existing S0A `AuditEnvelope` and `EvidenceEnvelope` and
   reuses S0A `Environment`/`EnvironmentScopedId` plus S0B typed scope and
   opaque-reference values. No public OpenAPI schema, generated projection,
   endpoint, or frontend authority changes.
2. Canonicalization is a narrow, explicit allowlist of scalar fields. Field
   names are controlled enums, ordering is sorted by the canonical field name,
   timestamps are UTC ISO-8601 with a `Z` suffix, null is represented as JSON
   `null`, and enum/typed-reference representations are explicit. There is
   no generic object serializer and no arbitrary payload/config mapping.
3. SHA-256 fingerprints cover the complete allowlisted record or snapshot
   field set. The S0A envelope payload hash covers the canonical record
   payload; the domain fingerprint additionally covers link and correction
   metadata. Repeated construction with equivalent input ordering is stable,
   while any material field change changes the fingerprint.
4. `AppendOnlyChain` is an immutable in-memory test/runtime value. It links
   records with a sequence and predecessor fingerprint and verifies insertion,
   reorder, tamper, environment, tenant, and account mismatches. Complete
   history verification uses an immutable `ChainReceipt` containing the
   record count, terminal sequence/fingerprint, and exact scope; an unanchored
   structural verifier does not claim suffix-deletion detection. It is not
   persistent ledger storage and has no database, WORM, object-store,
   blockchain, or external-signing behavior.
5. Corrections are new immutable records with a new identity and fingerprint
   referencing the predecessor. Public record creation rejects arbitrary
   correction links; controlled helpers require the actual original record,
   verify its integrity, and bind the correction to its exact environment and
   tenant/account scope. The original record is never rewritten.
6. Truth, source, and authority vocabularies are closed enums. Derived and
   telemetry records can only carry `NO_TRADING_AUTHORITY`; no class in this
   module grants trading, monetary, deployment, or production authority.
7. `ConfigSnapshot` and `ConfigProvenance` accept only typed safe metadata,
   controlled version/reference fields, and opaque references where a
   reference is genuinely required. Opaque reference identity is retained only
   through a deterministic domain-separated one-way digest; raw reference
   values are never canonicalized or serialized. Raw keys, tokens, private
   material, secret values, arbitrary dictionaries, unbounded text, and
   prompt/reasoning payloads are structurally rejected or fail closed.
8. Release, configuration, and policy identities are included in the
   provenance fingerprint and can be checked together for exact environment,
   version, and hash agreement. No runtime mutation, feature-flag provider,
   environment secret store, telemetry exporter, or external configuration
   provider is introduced.

## Scope and non-scope

The implementation is limited to `apps/backend` domain values, tests,
read-only boundary scanning, this ADR, the implementation evidence, and the
S0C governance workflow. It does not add persistence, providers, exchange or
network access, orders, balances, positions, risk, execution, deployment,
limited-live, or real-money trading. It does not change the public API.

## Platform, rollback, and authority

The implementation remains pure Python 3.12 and deterministic on Windows and
Linux. Rollback is removal of the S0C implementation PR before merge; no
checkpoint promotion is implied. Planning freeze is not implementation
authorization, and implementation authorization is not live-trading
authorization. Production credentials, production deployment, limited-live,
and live trading remain false.
