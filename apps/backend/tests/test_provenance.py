from dataclasses import replace
from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from hct_backend.contracts import Environment, EnvironmentScopedId, IdentityKind, StableId
from hct_backend.provenance import (
    AppendOnlyChain,
    AttributeKey,
    AuditRecord,
    AuthorityClass,
    ChainReceipt,
    ConfigAttribute,
    ConfigField,
    ConfigKind,
    ConfigProvenance,
    ConfigSnapshot,
    EvidenceRecord,
    IntegrityError,
    ProvenanceBoundaryError,
    ProvenanceScope,
    RecordAttribute,
    SourceClass,
    TruthClass,
    canonicalize,
    correct_audit_record,
    correct_evidence_record,
    fingerprint,
    verify_chain,
)
from hct_backend.security import (
    CredentialRef,
    ExchangeAccountID,
    PolicyVersion,
    SecretRef,
    TenantID,
)

NOW = datetime(2026, 9, 12, 12, 0, tzinfo=UTC)


def scope(environment: Environment = Environment.PAPER) -> ProvenanceScope:
    return ProvenanceScope(
        environment=environment,
        tenant_id=TenantID("tenant-a"),
        account_id=ExchangeAccountID("account-a"),
    )


def attr(key: AttributeKey, value: object) -> RecordAttribute:
    return RecordAttribute(key=key, value=value)  # type: ignore[arg-type]


def audit(event: str, *, attributes: tuple[RecordAttribute, ...] = ()):
    from hct_backend.provenance import AuditRecord

    return AuditRecord.create(
        event_id=EnvironmentScopedId(
            kind=IdentityKind.AUDIT, environment=Environment.PAPER, value=event
        ),
        environment=Environment.PAPER,
        event_type="FOUNDATION_CHECK",
        occurred_at=NOW,
        scope=scope(),
        truth=TruthClass.AUTHORITATIVE,
        source=SourceClass.SERVER_AUTHORITY,
        authority=AuthorityClass.AUDIT_EVIDENCE,
        attributes=attributes,
    )


def evidence(evidence_id: str, *, environment: Environment = Environment.PAPER) -> EvidenceRecord:
    return EvidenceRecord.create(
        evidence_id=EnvironmentScopedId(
            kind=IdentityKind.EVIDENCE, environment=environment, value=evidence_id
        ),
        environment=environment,
        evidence_type="VALIDATION_RESULT",
        recorded_at=NOW,
        scope=scope(environment),
        truth=TruthClass.OBSERVED,
        source=SourceClass.OBSERVATION,
        authority=AuthorityClass.AUDIT_EVIDENCE,
        attributes=(attr(AttributeKey.RESULT, "PASS"),),
    )


def test_canonicalization_is_order_independent_and_narrow() -> None:
    left = canonicalize((("record_type", "audit"), ("event_type", "FOUNDATION_CHECK")))
    right = canonicalize((("event_type", "FOUNDATION_CHECK"), ("record_type", "audit")))
    assert left == right
    assert fingerprint((("event_type", "one"),)) != fingerprint((("event_type", "two"),))
    with pytest.raises(ProvenanceBoundaryError):
        canonicalize((("arbitrary", "field"),))
    with pytest.raises(ProvenanceBoundaryError):
        canonicalize({"value": "not-a-field-tuple"})  # type: ignore[arg-type]
    with pytest.raises(ProvenanceBoundaryError):
        canonicalize((("value", {"nested": "payload"}),))  # type: ignore[arg-type]


def test_audit_hash_is_deterministic_and_material_attributes_change_it() -> None:
    first = audit(
        "event-1",
        attributes=(attr(AttributeKey.RESULT, "PASS"), attr(AttributeKey.COMPONENT, "audit")),
    )
    second = audit(
        "event-1",
        attributes=(attr(AttributeKey.COMPONENT, "audit"), attr(AttributeKey.RESULT, "PASS")),
    )
    changed = audit("event-1", attributes=(attr(AttributeKey.RESULT, "FAIL"),))
    assert first.envelope.payload_hash == second.envelope.payload_hash
    assert first.fingerprint == second.fingerprint
    assert first.fingerprint != changed.fingerprint
    assert first.envelope.payload_hash != changed.envelope.payload_hash


def test_envelopes_reject_malformed_hash_and_record_tamper() -> None:
    with pytest.raises(ValidationError):
        EnvironmentScopedId(kind=IdentityKind.AUDIT, environment=Environment.PAPER, value="bad id")
    record = audit("event-2")
    tampered_envelope = record.envelope.model_copy(update={"payload_hash": "a" * 64})
    with pytest.raises(IntegrityError, match="payload hash"):
        replace(record, envelope=tampered_envelope)
    with pytest.raises(ProvenanceBoundaryError):
        RecordAttribute(key=AttributeKey.RESULT, value={"raw": "payload"})  # type: ignore[arg-type]
    with pytest.raises(ProvenanceBoundaryError):
        RecordAttribute(key=AttributeKey.RESULT, value="private_key=raw-material")


def test_append_only_chain_detects_gap_reorder_and_predecessor_tamper() -> None:
    first = audit("chain-1")
    second = audit("chain-2")
    chain = AppendOnlyChain().append(first).append(second)
    verify_chain(chain.records)
    assert chain.records[0].sequence == 1
    assert chain.records[1].predecessor_fingerprint == chain.records[0].fingerprint
    with pytest.raises(IntegrityError, match="sequence"):
        verify_chain((chain.records[1], chain.records[0]))
    with pytest.raises(IntegrityError, match="sequence"):
        verify_chain((chain.records[1],))
    tampered = replace(chain.records[1], predecessor_fingerprint="b" * 64)
    with pytest.raises(IntegrityError, match="predecessor"):
        verify_chain((chain.records[0], tampered))
    with pytest.raises(IntegrityError):
        AppendOnlyChain(records=list(chain.records))  # type: ignore[arg-type]


def test_chain_receipt_detects_tail_truncation_and_terminal_tamper() -> None:
    chain = AppendOnlyChain().append(audit("receipt-1")).append(audit("receipt-2"))
    receipt = chain.receipt
    assert isinstance(receipt, ChainReceipt)
    verify_chain(chain.records, receipt=receipt)
    with pytest.raises(IntegrityError, match="receipt"):
        verify_chain(chain.records[:1], receipt=receipt)
    with pytest.raises(IntegrityError, match="receipt"):
        verify_chain(
            chain.records,
            receipt=replace(receipt, terminal_fingerprint="c" * 64),
        )


def test_correction_is_new_and_original_is_unchanged() -> None:
    original = audit("original", attributes=(attr(AttributeKey.RESULT, "FAIL"),))
    corrected = correct_audit_record(
        original,
        event_id=EnvironmentScopedId(
            kind=IdentityKind.AUDIT, environment=Environment.PAPER, value="correction"
        ),
        occurred_at=NOW,
        attributes=(
            attr(AttributeKey.RESULT, "PASS"),
            attr(AttributeKey.CORRECTION_REASON, "validated-recheck"),
        ),
    )
    assert original.correction_of is None
    assert corrected.correction_of == original.record_id
    assert corrected.record_id != original.record_id
    assert corrected.fingerprint != original.fingerprint
    with pytest.raises(IntegrityError, match="environment"):
        correct_audit_record(
            original,
            event_id=EnvironmentScopedId(
                kind=IdentityKind.AUDIT, environment=Environment.REPLAY, value="wrong-scope"
            ),
            occurred_at=NOW,
            attributes=(attr(AttributeKey.RESULT, "PASS"),),
        )


def test_direct_correction_linkage_requires_controlled_original_path() -> None:
    from hct_backend.provenance import AuditRecord

    with pytest.raises(IntegrityError, match="controlled"):
        AuditRecord.create(
            event_id=EnvironmentScopedId(
                kind=IdentityKind.AUDIT, environment=Environment.PAPER, value="direct-correction"
            ),
            environment=Environment.PAPER,
            event_type="FOUNDATION_CHECK",
            occurred_at=NOW,
            scope=scope(),
            truth=TruthClass.AUTHORITATIVE,
            source=SourceClass.SERVER_AUTHORITY,
            authority=AuthorityClass.AUDIT_EVIDENCE,
            correction_of=EnvironmentScopedId(
                kind=IdentityKind.AUDIT, environment=Environment.PAPER, value="unproven-original"
            ),
        )
    with pytest.raises(IntegrityError, match="controlled"):
        EvidenceRecord.create(
            evidence_id=EnvironmentScopedId(
                kind=IdentityKind.EVIDENCE,
                environment=Environment.PAPER,
                value="direct-evidence-correction",
            ),
            environment=Environment.PAPER,
            evidence_type="VALIDATION_RESULT",
            recorded_at=NOW,
            scope=scope(),
            truth=TruthClass.OBSERVED,
            source=SourceClass.OBSERVATION,
            authority=AuthorityClass.AUDIT_EVIDENCE,
            correction_of=EnvironmentScopedId(
                kind=IdentityKind.EVIDENCE,
                environment=Environment.PAPER,
                value="unproven-evidence-original",
            ),
        )


def test_direct_record_construction_requires_verified_original_proof() -> None:
    audit_original = audit("direct-bound-audit-original")
    audit_correction = correct_audit_record(
        audit_original,
        event_id=EnvironmentScopedId(
            kind=IdentityKind.AUDIT, environment=Environment.PAPER, value="direct-bound-audit"
        ),
        occurred_at=NOW,
        attributes=(attr(AttributeKey.RESULT, "PASS"),),
    )
    with pytest.raises(IntegrityError, match="validated original proof"):
        AuditRecord(
            envelope=audit_correction.envelope,
            scope=audit_correction.scope,
            truth=audit_correction.truth,
            source=audit_correction.source,
            authority=audit_correction.authority,
            record_version=audit_correction.record_version,
            attributes=audit_correction.attributes,
            correction_of=audit_correction.correction_of,
            sequence=audit_correction.sequence,
            predecessor_fingerprint=audit_correction.predecessor_fingerprint,
        )
    audit_rebuilt = AuditRecord(
        envelope=audit_original.envelope,
        scope=audit_original.scope,
        truth=audit_original.truth,
        source=audit_original.source,
        authority=audit_original.authority,
        record_version=audit_original.record_version,
        attributes=audit_original.attributes,
    )
    assert audit_rebuilt == audit_original

    evidence_original = evidence("direct-bound-evidence-original")
    evidence_correction = correct_evidence_record(
        evidence_original,
        evidence_id=EnvironmentScopedId(
            kind=IdentityKind.EVIDENCE,
            environment=Environment.PAPER,
            value="direct-bound-evidence",
        ),
        recorded_at=NOW,
        attributes=(attr(AttributeKey.RESULT, "PASS"),),
    )
    with pytest.raises(IntegrityError, match="validated original proof"):
        EvidenceRecord(
            envelope=evidence_correction.envelope,
            recorded_at=evidence_correction.recorded_at,
            scope=evidence_correction.scope,
            truth=evidence_correction.truth,
            source=evidence_correction.source,
            authority=evidence_correction.authority,
            record_version=evidence_correction.record_version,
            attributes=evidence_correction.attributes,
            correction_of=evidence_correction.correction_of,
            sequence=evidence_correction.sequence,
            predecessor_fingerprint=evidence_correction.predecessor_fingerprint,
        )
    evidence_rebuilt = EvidenceRecord(
        envelope=evidence_original.envelope,
        recorded_at=evidence_original.recorded_at,
        scope=evidence_original.scope,
        truth=evidence_original.truth,
        source=evidence_original.source,
        authority=evidence_original.authority,
        record_version=evidence_original.record_version,
        attributes=evidence_original.attributes,
    )
    assert evidence_rebuilt == evidence_original


def test_correction_rejects_tenant_and_account_scope_changes() -> None:
    original = audit("scope-correction")
    with pytest.raises(IntegrityError, match="scope"):
        correct_audit_record(
            original,
            event_id=EnvironmentScopedId(
                kind=IdentityKind.AUDIT, environment=Environment.PAPER, value="tenant-change"
            ),
            occurred_at=NOW,
            attributes=(attr(AttributeKey.RESULT, "PASS"),),
            scope=ProvenanceScope(
                environment=Environment.PAPER,
                tenant_id=TenantID("tenant-b"),
                account_id=ExchangeAccountID("account-a"),
            ),
        )
    with pytest.raises(IntegrityError, match="scope"):
        correct_audit_record(
            original,
            event_id=EnvironmentScopedId(
                kind=IdentityKind.AUDIT, environment=Environment.PAPER, value="account-change"
            ),
            occurred_at=NOW,
            attributes=(attr(AttributeKey.RESULT, "PASS"),),
            scope=ProvenanceScope(
                environment=Environment.PAPER,
                tenant_id=TenantID("tenant-a"),
                account_id=ExchangeAccountID("account-b"),
            ),
        )


@pytest.mark.parametrize("environment", list(Environment))
def test_environment_namespaces_are_all_explicit_and_isolated(environment: Environment) -> None:
    record = evidence(f"evidence-{environment.value.lower()}", environment=environment)
    assert record.environment is environment
    assert record.scope.environment is environment
    assert record.record_id.environment is environment


def test_evidence_correction_is_new_and_preserves_original() -> None:
    original = evidence("evidence-original")
    corrected = correct_evidence_record(
        original,
        evidence_id=EnvironmentScopedId(
            kind=IdentityKind.EVIDENCE, environment=Environment.PAPER, value="evidence-correction"
        ),
        recorded_at=NOW,
        attributes=(attr(AttributeKey.RESULT, "PASS"),),
    )
    assert original.correction_of is None
    assert corrected.correction_of == original.record_id
    assert corrected.record_id != original.record_id
    assert corrected.fingerprint != original.fingerprint


def test_environment_tenant_and_account_scope_is_exact() -> None:
    with pytest.raises(IntegrityError, match="environment"):
        from hct_backend.provenance import AuditRecord

        AuditRecord.create(
            event_id=EnvironmentScopedId(
                kind=IdentityKind.AUDIT, environment=Environment.PAPER, value="x"
            ),
            environment=Environment.PAPER,
            event_type="FOUNDATION_CHECK",
            occurred_at=NOW,
            scope=scope(Environment.REPLAY),
            truth=TruthClass.AUTHORITATIVE,
            source=SourceClass.SERVER_AUTHORITY,
            authority=AuthorityClass.AUDIT_EVIDENCE,
        )
    first = audit("scope-1")
    other_scope = ProvenanceScope(
        environment=Environment.PAPER,
        tenant_id=TenantID("tenant-b"),
        account_id=ExchangeAccountID("account-a"),
    )
    from hct_backend.provenance import AuditRecord

    second = AuditRecord.create(
        event_id=EnvironmentScopedId(
            kind=IdentityKind.AUDIT, environment=Environment.PAPER, value="scope-2"
        ),
        environment=Environment.PAPER,
        event_type="FOUNDATION_CHECK",
        occurred_at=NOW,
        scope=other_scope,
        truth=TruthClass.AUTHORITATIVE,
        source=SourceClass.SERVER_AUTHORITY,
        authority=AuthorityClass.AUDIT_EVIDENCE,
    )
    from hct_backend.provenance import link_record

    linked_first = link_record(first, sequence=1, predecessor_fingerprint=None)
    linked_second = link_record(
        second, sequence=2, predecessor_fingerprint=linked_first.fingerprint
    )
    with pytest.raises(IntegrityError, match="scope"):
        verify_chain((linked_first, linked_second))


def test_derived_and_telemetry_cannot_upgrade_authority() -> None:
    from hct_backend.provenance import AuditRecord

    with pytest.raises(ProvenanceBoundaryError, match="authority"):
        AuditRecord.create(
            event_id=EnvironmentScopedId(
                kind=IdentityKind.AUDIT, environment=Environment.PAPER, value="derived"
            ),
            environment=Environment.PAPER,
            event_type="FOUNDATION_CHECK",
            occurred_at=NOW,
            scope=scope(),
            truth=TruthClass.DERIVED,
            source=SourceClass.DERIVATION,
            authority=AuthorityClass.AUDIT_EVIDENCE,
        )
    record = AuditRecord.create(
        event_id=EnvironmentScopedId(
            kind=IdentityKind.AUDIT, environment=Environment.PAPER, value="derived-ok"
        ),
        environment=Environment.PAPER,
        event_type="FOUNDATION_CHECK",
        occurred_at=NOW,
        scope=scope(),
        truth=TruthClass.DERIVED,
        source=SourceClass.DERIVATION,
        authority=AuthorityClass.NO_TRADING_AUTHORITY,
    )
    assert record.authority is AuthorityClass.NO_TRADING_AUTHORITY


def test_opaque_reference_is_safe_and_not_hashed_as_raw_value() -> None:
    reference = SecretRef("secret-ref-audit-1")
    record = audit("opaque", attributes=(attr(AttributeKey.REFERENCE, reference),))
    same_reference = SecretRef("secret-ref-audit-1")
    different_reference = SecretRef("secret-ref-audit-2")
    credential_reference = CredentialRef("cred-ref-audit-1")
    canonical = canonicalize((("attribute.reference", reference),))
    assert b"secret-ref-audit-1" not in record.envelope.payload_hash.encode()
    assert b"secret-ref-audit-1" not in canonical
    assert canonical == canonicalize((("attribute.reference", same_reference),))
    assert canonical != canonicalize((("attribute.reference", different_reference),))
    assert canonical != canonicalize((("attribute.reference", credential_reference),))
    assert b"secret-ref-audit-1" not in repr(record).encode()
    assert record.fingerprint != audit(
        "opaque", attributes=(attr(AttributeKey.REFERENCE, different_reference),)
    ).fingerprint


def test_config_snapshot_and_provenance_bind_release_config_policy_and_scope() -> None:
    snapshot = ConfigSnapshot(
        snapshot_id=EnvironmentScopedId(
            kind=IdentityKind.CONFIG, environment=Environment.PAPER, value="config-1"
        ),
        environment=Environment.PAPER,
        config_kind=ConfigKind.CONFIGURATION,
        version=3,
        attributes=(
            ConfigAttribute(ConfigField.COMPONENT, "audit"),
            ConfigAttribute(ConfigField.SCHEMA_VERSION, 1),
        ),
    )
    provenance = ConfigProvenance(
        provenance_id=EnvironmentScopedId(
            kind=IdentityKind.CONFIG, environment=Environment.PAPER, value="provenance-1"
        ),
        scope=scope(),
        release_id=StableId(kind=IdentityKind.RELEASE, value="release-1"),
        snapshot=snapshot,
        policy_version=PolicyVersion("policy-v1"),
    )
    provenance.assert_matches(
        release_id=StableId(kind=IdentityKind.RELEASE, value="release-1"),
        config_fingerprint=snapshot.fingerprint,
        policy_version=PolicyVersion("policy-v1"),
    )
    with pytest.raises(IntegrityError, match="release"):
        provenance.assert_matches(
            release_id=StableId(kind=IdentityKind.RELEASE, value="release-2"),
            config_fingerprint=snapshot.fingerprint,
            policy_version=PolicyVersion("policy-v1"),
        )
    with pytest.raises(IntegrityError, match="configuration"):
        provenance.assert_matches(
            release_id=StableId(kind=IdentityKind.RELEASE, value="release-1"),
            config_fingerprint="a" * 64,
            policy_version=PolicyVersion("policy-v1"),
        )
    with pytest.raises(ProvenanceBoundaryError):
        ConfigSnapshot(
            snapshot_id=EnvironmentScopedId(
                kind=IdentityKind.CONFIG, environment=Environment.PAPER, value="config-2"
            ),
            environment=Environment.PAPER,
            config_kind=ConfigKind.CONFIGURATION,
            version=1,
            attributes=({"mode": "PAPER"},),  # type: ignore[arg-type]
        )
