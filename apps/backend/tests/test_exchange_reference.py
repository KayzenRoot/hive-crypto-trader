from dataclasses import FrozenInstanceError, replace
from datetime import UTC, datetime
from decimal import Decimal

import pytest

from hct_backend.contracts import IdentityKind, StableId
from hct_backend.exchange_reference import (
    CapabilityDeclaration,
    CapabilityName,
    CapabilitySnapshot,
    CapabilityState,
    CapabilityUnknownError,
    ContractReference,
    ContractType,
    ExchangeDescriptor,
    InMemoryExchangeReferenceAdapter,
    LifecycleClass,
    MalformedReferenceError,
    UnsupportedCapabilityError,
)

NOW = datetime(2026, 9, 12, 12, 0, tzinfo=UTC)


def stable(kind: IdentityKind, value: str) -> StableId:
    return StableId(kind=kind, value=value)


def descriptor() -> ExchangeDescriptor:
    return ExchangeDescriptor(
        exchange_id=stable(IdentityKind.EXCHANGE, "venue-a"),
        display_name="Venue A",
        reference_version=1,
        source="declared-reference",
        observed_at=NOW,
        metadata=(("region", "global"),),
    )


def capabilities() -> CapabilitySnapshot:
    return CapabilitySnapshot(
        snapshot_id=stable(IdentityKind.CAPABILITY_SNAPSHOT, "cap-1"),
        exchange_id=descriptor().exchange_id,
        version=1,
        source="declared-reference",
        observed_at=NOW,
        declarations=(
            CapabilityDeclaration(
                CapabilityName.EXCHANGE_DESCRIPTION,
                CapabilityState.SUPPORTED,
                "reference-descriptor",
            ),
            CapabilityDeclaration(
                CapabilityName.CONTRACT_REFERENCE,
                CapabilityState.SUPPORTED,
                "contract-catalog",
            ),
            CapabilityDeclaration(CapabilityName.STATE_CHANGE, CapabilityState.UNKNOWN),
        ),
    )


def reference(native_symbol: str = "BTC_USDT", reference_value: str = "ref-1") -> ContractReference:
    return ContractReference(
        reference_id=stable(IdentityKind.REFERENCE_SNAPSHOT, reference_value),
        contract_id=stable(IdentityKind.INSTRUMENT, "btc-usdt-perpetual"),
        exchange_id=descriptor().exchange_id,
        native_symbol=native_symbol,
        lifecycle=LifecycleClass.ACTIVE,
        contract_type=ContractType.PERPETUAL,
        price_increment=Decimal("0.10"),
        quantity_increment=Decimal("0.001"),
        source="declared-reference",
        observed_at=NOW,
        base_asset="BTC",
        quote_asset="USDT",
        settlement_asset="USDT",
        price_precision=2,
        quantity_precision=3,
        min_quantity=Decimal("0.001"),
        max_quantity=Decimal("100"),
    )


def adapter() -> InMemoryExchangeReferenceAdapter:
    return InMemoryExchangeReferenceAdapter(
        descriptor=descriptor(),
        capabilities=capabilities(),
        references=(reference(),),
    )


def test_new_identity_kinds_round_trip_through_canonical_stable_id() -> None:
    identity = StableId.parse("EXCHANGE:venue-a")
    assert identity.kind is IdentityKind.EXCHANGE
    assert identity.as_text() == "EXCHANGE:venue-a"
    assert stable(IdentityKind.INSTRUMENT, "btc-usdt-perpetual").kind is IdentityKind.INSTRUMENT


def test_exchange_descriptor_is_immutable_and_fingerprintable() -> None:
    item = descriptor()
    assert len(item.fingerprint) == 64
    with pytest.raises(FrozenInstanceError):
        item.display_name = "other"  # type: ignore[misc]


def test_capability_states_are_explicit_and_unknown_fails_closed() -> None:
    snapshot = capabilities()
    assert snapshot.is_supported(CapabilityName.CONTRACT_REFERENCE) is True
    assert snapshot.is_supported(CapabilityName.STATE_CHANGE) is False
    assert snapshot.is_supported(CapabilityName.PRIVATE_STATE_READ) is False
    assert bool(CapabilityState.UNKNOWN) is False
    snapshot.require_supported(CapabilityName.CONTRACT_REFERENCE)
    with pytest.raises(CapabilityUnknownError):
        snapshot.require_supported(CapabilityName.PRIVATE_STATE_READ)
    with pytest.raises(CapabilityUnknownError):
        snapshot.require_supported(CapabilityName.STATE_CHANGE)


def test_explicit_unsupported_capability_is_not_unknown() -> None:
    snapshot = replace(
        capabilities(),
        declarations=(
            *capabilities().declarations[:2],
            CapabilityDeclaration(
                CapabilityName.STATE_CHANGE, CapabilityState.UNSUPPORTED, "policy"
            ),
        ),
    )
    with pytest.raises(UnsupportedCapabilityError):
        snapshot.require_supported(CapabilityName.STATE_CHANGE)


def test_capability_snapshot_is_immutable_and_material_changes_fingerprint() -> None:
    item = capabilities()
    changed = replace(item, version=2)
    assert item.fingerprint != changed.fingerprint
    with pytest.raises(FrozenInstanceError):
        item.version = 2  # type: ignore[misc]


def test_contract_identity_is_distinct_from_native_symbol() -> None:
    item = reference()
    changed_mapping = replace(item, native_symbol="BTCUSDT")
    assert item.contract_id != stable(IdentityKind.INSTRUMENT, "other-contract")
    assert item.contract_id == changed_mapping.contract_id
    assert item.native_symbol != changed_mapping.native_symbol
    assert item.fingerprint != changed_mapping.fingerprint


@pytest.mark.parametrize(
    "field",
    ["price_increment", "quantity_increment"],
)
def test_zero_and_negative_increments_fail_closed(field: str) -> None:
    with pytest.raises(MalformedReferenceError):
        replace(reference(), **{field: Decimal("0")})
    with pytest.raises(MalformedReferenceError):
        replace(reference(), **{field: Decimal("-0.1")})


def test_float_increment_is_rejected_as_not_exact_decimal() -> None:
    values = {
        "reference_id": stable(IdentityKind.REFERENCE_SNAPSHOT, "ref-float"),
        "contract_id": stable(IdentityKind.INSTRUMENT, "btc-usdt-perpetual"),
        "exchange_id": descriptor().exchange_id,
        "native_symbol": "BTC_USDT",
        "lifecycle": LifecycleClass.ACTIVE,
        "contract_type": ContractType.PERPETUAL,
        "price_increment": 0.1,
        "quantity_increment": Decimal("0.001"),
        "source": "declared-reference",
        "observed_at": NOW,
    }
    with pytest.raises(MalformedReferenceError):
        ContractReference(**values)  # type: ignore[arg-type]


def test_precision_and_min_max_consistency_fail_closed() -> None:
    with pytest.raises(MalformedReferenceError):
        replace(reference(), price_precision=0)
    with pytest.raises(MalformedReferenceError):
        replace(reference(), min_quantity=Decimal("2"), max_quantity=Decimal("1"))


def test_unknown_lifecycle_is_not_accepted_as_usable_reference() -> None:
    with pytest.raises(MalformedReferenceError):
        replace(reference(), lifecycle=LifecycleClass.UNKNOWN)


def test_reference_adapter_is_deterministic_and_only_exposes_reference_reads() -> None:
    item = adapter()
    assert item.describe_exchange() == descriptor()
    assert item.capability_snapshot() == capabilities()
    assert item.list_contract_references() == (reference(),)
    assert item.resolve_reference(contract_id=reference().contract_id) == reference()
    assert item.resolve_reference(native_symbol="BTC_USDT") == reference()
    assert set(item.__class__.__dict__) >= {
        "describe_exchange",
        "capability_snapshot",
        "list_contract_references",
        "resolve_reference",
    }


def test_reference_lookup_unknown_and_ambiguous_inputs_fail_closed() -> None:
    item = adapter()
    with pytest.raises(ValueError):
        item.resolve_reference()
    with pytest.raises(ValueError):
        item.resolve_reference(native_symbol="UNKNOWN SYMBOL")
    with pytest.raises(ValueError):
        item.resolve_reference(contract_id=stable(IdentityKind.EXCHANGE, "wrong-kind"))


def test_unsafe_descriptor_metadata_and_duplicate_declarations_are_rejected() -> None:
    with pytest.raises(MalformedReferenceError):
        replace(descriptor(), metadata=(("token_value", "not allowed"),))
    declaration = CapabilityDeclaration(
        CapabilityName.CONTRACT_REFERENCE,
        CapabilityState.SUPPORTED,
        "catalog",
    )
    with pytest.raises(MalformedReferenceError):
        replace(capabilities(), declarations=(declaration, declaration))
