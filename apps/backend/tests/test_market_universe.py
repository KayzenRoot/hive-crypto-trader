from dataclasses import FrozenInstanceError, replace
from datetime import UTC, datetime
from decimal import Decimal

import pytest

from hct_backend.contracts import Environment, IdentityKind, StableId
from hct_backend.exchange_reference import (
    CapabilityDeclaration,
    CapabilityName,
    CapabilitySnapshot,
    CapabilityState,
    ContractReference,
    ContractType,
    ExchangeDescriptor,
    LifecycleClass,
)
from hct_backend.market_universe import (
    MarketUniverseRegistry,
    UniverseConsistencyError,
    UniverseEligibilityState,
    UniverseInputError,
    UniverseReasonCode,
    recompute_universe,
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


def capabilities(
    states: dict[CapabilityName, CapabilityState] | None = None,
) -> CapabilitySnapshot:
    values = {
        CapabilityName.EXCHANGE_DESCRIPTION: CapabilityState.SUPPORTED,
        CapabilityName.PUBLIC_REFERENCE: CapabilityState.SUPPORTED,
        CapabilityName.CONTRACT_REFERENCE: CapabilityState.SUPPORTED,
    }
    if states is not None:
        values.update(states)
    declarations = tuple(
        CapabilityDeclaration(
            name,
            state,
            None if state is CapabilityState.UNKNOWN else "catalogue",
        )
        for name, state in values.items()
    )
    return CapabilitySnapshot(
        snapshot_id=stable(IdentityKind.CAPABILITY_SNAPSHOT, "cap-1"),
        exchange_id=descriptor().exchange_id,
        version=1,
        source="declared-reference",
        observed_at=NOW,
        declarations=declarations,
    )


def reference(
    contract_value: str = "btc-usdt-perpetual",
    reference_value: str = "ref-1",
    *,
    native_symbol: str = "BTC_USDT",
    lifecycle: LifecycleClass = LifecycleClass.ACTIVE,
    contract_type: ContractType = ContractType.PERPETUAL,
) -> ContractReference:
    return ContractReference(
        reference_id=stable(IdentityKind.REFERENCE_SNAPSHOT, reference_value),
        contract_id=stable(IdentityKind.INSTRUMENT, contract_value),
        exchange_id=descriptor().exchange_id,
        native_symbol=native_symbol,
        lifecycle=lifecycle,
        contract_type=contract_type,
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


def snapshot(*references: ContractReference, **kwargs: object):
    return recompute_universe(
        descriptor(),
        capabilities(),
        references,
        environment=Environment.PAPER,
        recomputed_at=NOW,
        **kwargs,
    )


def test_active_supported_perpetual_is_structurally_eligible() -> None:
    item = snapshot(reference()).entries[0]
    assert item.state is UniverseEligibilityState.ELIGIBLE
    assert item.reason_codes == (UniverseReasonCode.ELIGIBLE_REFERENCE_PROVEN,)


def test_inactive_or_non_perpetual_is_ineligible_with_deterministic_reasons() -> None:
    item = snapshot(
        reference(
            lifecycle=LifecycleClass.INACTIVE,
            contract_type=ContractType.FUTURES,
        )
    ).entries[0]
    assert item.state is UniverseEligibilityState.INELIGIBLE
    assert item.reason_codes == (
        UniverseReasonCode.INELIGIBLE_CONTRACT_TYPE,
        UniverseReasonCode.INELIGIBLE_LIFECYCLE,
    )


def test_unknown_and_unsupported_capabilities_fail_closed() -> None:
    unknown = recompute_universe(
        descriptor(),
        capabilities({CapabilityName.EXCHANGE_DESCRIPTION: CapabilityState.UNKNOWN}),
        (reference(),),
        environment=Environment.PAPER,
        recomputed_at=NOW,
    ).entries[0]
    assert unknown.state is UniverseEligibilityState.UNKNOWN
    assert unknown.reason_codes == (UniverseReasonCode.UNKNOWN_REQUIRED_CAPABILITY,)

    unsupported = recompute_universe(
        descriptor(),
        capabilities({CapabilityName.PUBLIC_REFERENCE: CapabilityState.UNSUPPORTED}),
        (reference(),),
        environment=Environment.PAPER,
        recomputed_at=NOW,
    ).entries[0]
    assert unsupported.state is UniverseEligibilityState.INELIGIBLE
    assert unsupported.reason_codes == (
        UniverseReasonCode.INELIGIBLE_REQUIRED_CAPABILITY_UNSUPPORTED,
    )


def test_missing_material_reference_fact_is_unknown() -> None:
    incomplete = replace(reference(), base_asset=None)
    item = snapshot(incomplete).entries[0]
    assert item.state is UniverseEligibilityState.UNKNOWN
    assert item.reason_codes == (UniverseReasonCode.UNKNOWN_REQUIRED_REFERENCE,)


def test_order_and_recompute_time_do_not_change_snapshot_fingerprint() -> None:
    first = snapshot(
        reference(), reference("eth-usdt-perpetual", "ref-2", native_symbol="ETH_USDT")
    )
    second = recompute_universe(
        descriptor(),
        capabilities(),
        (reference("eth-usdt-perpetual", "ref-2", native_symbol="ETH_USDT"), reference()),
        environment=Environment.PAPER,
        recomputed_at=datetime(2030, 1, 1, tzinfo=UTC),
    )
    assert first.entries[0].contract_id.as_text() < first.entries[1].contract_id.as_text()
    assert first.fingerprint == second.fingerprint
    assert first.recomputed_at != second.recomputed_at


def test_material_source_policy_and_mapping_changes_change_fingerprint() -> None:
    base = snapshot(reference())
    changed_mapping = snapshot(replace(reference(), native_symbol="BTCUSDT"))
    changed_policy = snapshot(reference(), policy_version=2)
    changed_capability = recompute_universe(
        descriptor(),
        replace(capabilities(), version=2),
        (reference(),),
        environment=Environment.PAPER,
        recomputed_at=NOW,
    )
    assert base.entries[0].contract_id == changed_mapping.entries[0].contract_id
    assert base.fingerprint != changed_mapping.fingerprint
    assert base.fingerprint != changed_policy.fingerprint
    assert base.fingerprint != changed_capability.fingerprint


def test_duplicate_contradictory_and_cross_exchange_evidence_fails_closed() -> None:
    with pytest.raises(UniverseConsistencyError):
        snapshot(reference(), reference("eth-usdt-perpetual", "ref-1", native_symbol="ETH_USDT"))
    with pytest.raises(UniverseConsistencyError):
        snapshot(reference(), reference("eth-usdt-perpetual", "ref-2", native_symbol="BTC_USDT"))
    other_exchange = replace(reference(), exchange_id=stable(IdentityKind.EXCHANGE, "venue-b"))
    with pytest.raises(UniverseConsistencyError):
        snapshot(other_exchange)


def test_registry_rejects_empty_raw_or_boolean_inputs() -> None:
    with pytest.raises(UniverseInputError):
        MarketUniverseRegistry().recompute(
            descriptor(), capabilities(), (), environment=Environment.PAPER, recomputed_at=NOW
        )
    with pytest.raises(UniverseInputError):
        MarketUniverseRegistry().recompute(  # type: ignore[arg-type]
            descriptor(), capabilities(), {"contract": "raw"}, environment=Environment.PAPER
        )
    with pytest.raises(UniverseInputError):
        MarketUniverseRegistry(policy_version=True)  # type: ignore[arg-type]


def test_registry_policy_and_typed_input_validation_is_fail_closed() -> None:
    with pytest.raises(UniverseInputError):
        MarketUniverseRegistry(required_capabilities=())
    with pytest.raises(UniverseInputError):
        MarketUniverseRegistry(required_capabilities=("PUBLIC_REFERENCE",))  # type: ignore[arg-type]
    with pytest.raises(UniverseInputError):
        MarketUniverseRegistry(required_capabilities=(CapabilityName.PUBLIC_REFERENCE,) * 2)
    with pytest.raises(UniverseInputError):
        MarketUniverseRegistry(required_contract_type="PERPETUAL")  # type: ignore[arg-type]
    with pytest.raises(UniverseInputError):
        MarketUniverseRegistry().recompute(
            descriptor(),
            capabilities(),
            (reference(),),
            environment="PAPER",  # type: ignore[arg-type]
        )
    with pytest.raises(UniverseInputError):
        MarketUniverseRegistry().recompute(
            descriptor(),
            capabilities(),
            (object(),),
            environment=Environment.PAPER,  # type: ignore[arg-type]
        )


def test_entries_and_snapshots_are_immutable_and_identity_is_dedicated() -> None:
    item = snapshot(reference())
    assert item.snapshot_id.kind is IdentityKind.UNIVERSE_SNAPSHOT
    assert item.exchange_id == descriptor().exchange_id
    with pytest.raises(UniverseConsistencyError):
        replace(item, environment=Environment.REPLAY)
    with pytest.raises(UniverseInputError):
        replace(
            item,
            snapshot_id=stable(IdentityKind.REFERENCE_SNAPSHOT, "reference-identity"),
        )
    with pytest.raises(UniverseInputError):
        replace(
            item.entries[0],
            reason_codes=(
                UniverseReasonCode.ELIGIBLE_REFERENCE_PROVEN,
                UniverseReasonCode.ELIGIBLE_REFERENCE_PROVEN,
            ),
        )
    with pytest.raises(FrozenInstanceError):
        item.entries = ()  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        item.entries[0].state = UniverseEligibilityState.UNKNOWN  # type: ignore[misc]
