"""Provider-neutral, immutable structural market-universe registry."""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum

from hct_backend.contracts import Environment, IdentityKind, StableId
from hct_backend.exchange_reference import (
    CapabilityName,
    CapabilitySnapshot,
    CapabilityState,
    ContractReference,
    ContractType,
    ExchangeDescriptor,
    LifecycleClass,
)

_HASH_PATTERN = re.compile(r"^[0-9a-f]{64}$")
_NATIVE_SYMBOL_PATTERN = re.compile(r"^[A-Za-z0-9._:/-]{1,64}$")


class UniverseEligibilityState(StrEnum):
    """Structural membership state; never a trading or risk decision."""

    ELIGIBLE = "ELIGIBLE"
    INELIGIBLE = "INELIGIBLE"
    UNKNOWN = "UNKNOWN"


class UniverseReasonCode(StrEnum):
    """Finite machine-readable reasons for the structural state."""

    ELIGIBLE_REFERENCE_PROVEN = "ELIGIBLE_REFERENCE_PROVEN"
    INELIGIBLE_CONTRACT_TYPE = "INELIGIBLE_CONTRACT_TYPE"
    INELIGIBLE_LIFECYCLE = "INELIGIBLE_LIFECYCLE"
    INELIGIBLE_REQUIRED_CAPABILITY_UNSUPPORTED = "INELIGIBLE_REQUIRED_CAPABILITY_UNSUPPORTED"
    UNKNOWN_REQUIRED_CAPABILITY = "UNKNOWN_REQUIRED_CAPABILITY"
    UNKNOWN_REQUIRED_REFERENCE = "UNKNOWN_REQUIRED_REFERENCE"


class UniverseError(ValueError):
    """Base error for fail-closed registry validation."""


class UniverseInputError(UniverseError):
    """Raised when typed evidence is missing or malformed."""


class UniverseConsistencyError(UniverseError):
    """Raised when canonical evidence is duplicate, contradictory or cross-boundary."""


def _positive(value: int, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise UniverseInputError(f"{label} must be a positive integer")
    return value


def _utc(value: datetime, label: str) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise UniverseInputError(f"{label} must be timezone-aware")
    return value.astimezone(UTC)


def _hash(value: object) -> str:
    encoded = json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _identity(value: StableId, kind: IdentityKind, label: str) -> StableId:
    if not isinstance(value, StableId) or value.kind is not kind:
        raise UniverseInputError(f"{label} has the wrong identity kind")
    return value


def _fingerprint(value: str, label: str) -> str:
    if not isinstance(value, str) or not _HASH_PATTERN.fullmatch(value):
        raise UniverseInputError(f"{label} must be a lowercase SHA-256 fingerprint")
    return value


def _safe_symbol(value: str) -> str:
    if not isinstance(value, str) or not _NATIVE_SYMBOL_PATTERN.fullmatch(value):
        raise UniverseInputError("native symbol is invalid")
    return value


@dataclass(frozen=True, slots=True)
class UniverseEntry:
    """Immutable structural membership for one canonical contract."""

    contract_id: StableId
    reference_id: StableId
    reference_version: int
    reference_source: str
    reference_fingerprint: str
    native_symbol: str
    state: UniverseEligibilityState
    reason_codes: tuple[UniverseReasonCode, ...]

    def __post_init__(self) -> None:
        _identity(self.contract_id, IdentityKind.INSTRUMENT, "contract")
        _identity(self.reference_id, IdentityKind.REFERENCE_SNAPSHOT, "reference")
        _positive(self.reference_version, "reference version")
        _fingerprint(self.reference_fingerprint, "reference fingerprint")
        if not isinstance(self.reference_source, str) or not self.reference_source:
            raise UniverseInputError("reference source is required")
        _safe_symbol(self.native_symbol)
        if not isinstance(self.state, UniverseEligibilityState):
            raise UniverseInputError("invalid universe state")
        if not isinstance(self.reason_codes, tuple) or not self.reason_codes:
            raise UniverseInputError("universe reason codes are required")
        if any(not isinstance(reason, UniverseReasonCode) for reason in self.reason_codes):
            raise UniverseInputError("invalid universe reason code")
        if tuple(sorted(set(self.reason_codes), key=lambda item: item.value)) != self.reason_codes:
            raise UniverseInputError("universe reason codes must be unique and ordered")

    @property
    def fingerprint(self) -> str:
        return _hash(
            {
                "contract_id": self.contract_id.as_text(),
                "reference_id": self.reference_id.as_text(),
                "reference_version": self.reference_version,
                "reference_source": self.reference_source,
                "reference_fingerprint": self.reference_fingerprint,
                "native_symbol": self.native_symbol,
                "state": self.state.value,
                "reason_codes": [reason.value for reason in self.reason_codes],
            }
        )


@dataclass(frozen=True, slots=True)
class UniverseSnapshot:
    """Immutable/versioned structural universe result with no persistence semantics."""

    snapshot_id: StableId
    exchange_id: StableId
    environment: Environment
    exchange_reference_version: int
    exchange_source: str
    exchange_fingerprint: str
    capability_snapshot_id: StableId
    capability_version: int
    capability_source: str
    capability_fingerprint: str
    policy_version: int
    recomputed_at: datetime
    entries: tuple[UniverseEntry, ...]

    def __post_init__(self) -> None:
        _identity(self.snapshot_id, IdentityKind.UNIVERSE_SNAPSHOT, "universe snapshot")
        _identity(self.exchange_id, IdentityKind.EXCHANGE, "exchange")
        if not isinstance(self.environment, Environment):
            raise UniverseInputError("invalid universe environment")
        if not self.snapshot_id.value.startswith(f"universe-{self.environment.value.lower()}-"):
            raise UniverseConsistencyError("universe snapshot identity crosses environments")
        _positive(self.exchange_reference_version, "exchange reference version")
        _positive(self.capability_version, "capability version")
        _positive(self.policy_version, "policy version")
        _fingerprint(self.exchange_fingerprint, "exchange fingerprint")
        _identity(self.capability_snapshot_id, IdentityKind.CAPABILITY_SNAPSHOT, "capability")
        _fingerprint(self.capability_fingerprint, "capability fingerprint")
        if not isinstance(self.exchange_source, str) or not self.exchange_source:
            raise UniverseInputError("exchange source is required")
        if not isinstance(self.capability_source, str) or not self.capability_source:
            raise UniverseInputError("capability source is required")
        object.__setattr__(self, "recomputed_at", _utc(self.recomputed_at, "recomputed_at"))
        if not isinstance(self.entries, tuple) or not self.entries:
            raise UniverseInputError("universe snapshot requires at least one entry")
        if any(not isinstance(entry, UniverseEntry) for entry in self.entries):
            raise UniverseInputError("invalid universe entry")
        if tuple(sorted(self.entries, key=lambda item: item.contract_id.as_text())) != self.entries:
            raise UniverseInputError("universe entries must be canonically ordered")
        contract_ids = [entry.contract_id for entry in self.entries]
        if len(contract_ids) != len(set(contract_ids)):
            raise UniverseConsistencyError("universe snapshot contains duplicate contracts")

    @property
    def fingerprint(self) -> str:
        return _hash(
            {
                "exchange_id": self.exchange_id.as_text(),
                "environment": self.environment.value,
                "exchange_reference_version": self.exchange_reference_version,
                "exchange_source": self.exchange_source,
                "exchange_fingerprint": self.exchange_fingerprint,
                "capability_snapshot_id": self.capability_snapshot_id.as_text(),
                "capability_version": self.capability_version,
                "capability_source": self.capability_source,
                "capability_fingerprint": self.capability_fingerprint,
                "policy_version": self.policy_version,
                "entries": [entry.fingerprint for entry in self.entries],
            }
        )


@dataclass(frozen=True, slots=True)
class MarketUniverseRegistry:
    """Pure registry for bounded structural eligibility recomputation."""

    policy_version: int = 1
    required_capabilities: tuple[CapabilityName, ...] = (
        CapabilityName.EXCHANGE_DESCRIPTION,
        CapabilityName.PUBLIC_REFERENCE,
        CapabilityName.CONTRACT_REFERENCE,
    )
    required_contract_type: ContractType = ContractType.PERPETUAL

    def __post_init__(self) -> None:
        _positive(self.policy_version, "policy version")
        if not isinstance(self.required_capabilities, tuple) or not self.required_capabilities:
            raise UniverseInputError("required capabilities are required")
        if any(not isinstance(item, CapabilityName) for item in self.required_capabilities):
            raise UniverseInputError("invalid required capability")
        if len(set(self.required_capabilities)) != len(self.required_capabilities):
            raise UniverseInputError("duplicate required capability")
        if not isinstance(self.required_contract_type, ContractType):
            raise UniverseInputError("invalid required contract type")

    def recompute(
        self,
        descriptor: ExchangeDescriptor,
        capabilities: CapabilitySnapshot,
        references: Sequence[ContractReference],
        *,
        environment: Environment,
        recomputed_at: datetime | None = None,
    ) -> UniverseSnapshot:
        if not isinstance(descriptor, ExchangeDescriptor):
            raise UniverseInputError("exchange descriptor is required")
        if not isinstance(capabilities, CapabilitySnapshot):
            raise UniverseInputError("capability snapshot is required")
        if not isinstance(environment, Environment):
            raise UniverseInputError("environment must be an Environment")
        if isinstance(references, (str, bytes, dict)) or not isinstance(references, Sequence):
            raise UniverseInputError("references must be a typed sequence")
        normalized = tuple(references)
        if not normalized:
            raise UniverseInputError("material contract reference evidence is missing")
        if any(not isinstance(reference, ContractReference) for reference in normalized):
            raise UniverseInputError("references must contain ContractReference values")
        self._validate_consistency(descriptor, capabilities, normalized)
        entries = tuple(
            sorted(
                (self._entry(reference, capabilities) for reference in normalized),
                key=lambda item: item.contract_id.as_text(),
            )
        )
        observed = recomputed_at if recomputed_at is not None else datetime.now(UTC)
        observed = _utc(observed, "recomputed_at")
        material = {
            "exchange_id": descriptor.exchange_id.as_text(),
            "environment": environment.value,
            "exchange_reference_version": descriptor.reference_version,
            "exchange_source": descriptor.source,
            "exchange_fingerprint": descriptor.fingerprint,
            "capability_snapshot_id": capabilities.snapshot_id.as_text(),
            "capability_version": capabilities.version,
            "capability_source": capabilities.source,
            "capability_fingerprint": capabilities.fingerprint,
            "policy_version": self.policy_version,
            "entries": [entry.fingerprint for entry in entries],
        }
        fingerprint = _hash(material)
        snapshot_id = StableId(
            kind=IdentityKind.UNIVERSE_SNAPSHOT,
            value=f"universe-{environment.value.lower()}-{fingerprint[:32]}",
        )
        return UniverseSnapshot(
            snapshot_id=snapshot_id,
            exchange_id=descriptor.exchange_id,
            environment=environment,
            exchange_reference_version=descriptor.reference_version,
            exchange_source=descriptor.source,
            exchange_fingerprint=descriptor.fingerprint,
            capability_snapshot_id=capabilities.snapshot_id,
            capability_version=capabilities.version,
            capability_source=capabilities.source,
            capability_fingerprint=capabilities.fingerprint,
            policy_version=self.policy_version,
            recomputed_at=observed,
            entries=entries,
        )

    def _validate_consistency(
        self,
        descriptor: ExchangeDescriptor,
        capabilities: CapabilitySnapshot,
        references: tuple[ContractReference, ...],
    ) -> None:
        if capabilities.exchange_id != descriptor.exchange_id:
            raise UniverseConsistencyError("capability exchange does not match descriptor")
        if any(reference.exchange_id != descriptor.exchange_id for reference in references):
            raise UniverseConsistencyError("reference exchange does not match descriptor")
        contract_ids = [reference.contract_id for reference in references]
        native_symbols = [reference.native_symbol for reference in references]
        reference_ids = [reference.reference_id for reference in references]
        if len(set(contract_ids)) != len(contract_ids):
            raise UniverseConsistencyError("duplicate canonical contract evidence")
        if len(set(native_symbols)) != len(native_symbols):
            raise UniverseConsistencyError("contradictory native contract mapping")
        if len(set(reference_ids)) != len(reference_ids):
            raise UniverseConsistencyError("duplicate reference identity evidence")

    def _entry(
        self, reference: ContractReference, capabilities: CapabilitySnapshot
    ) -> UniverseEntry:
        reasons: tuple[UniverseReasonCode, ...]
        capability_states = tuple(
            capabilities.state_for(name) for name in self.required_capabilities
        )
        if any(state is CapabilityState.UNKNOWN for state in capability_states):
            state = UniverseEligibilityState.UNKNOWN
            reasons = (UniverseReasonCode.UNKNOWN_REQUIRED_CAPABILITY,)
        elif any(state is CapabilityState.UNSUPPORTED for state in capability_states):
            state = UniverseEligibilityState.INELIGIBLE
            reasons = (UniverseReasonCode.INELIGIBLE_REQUIRED_CAPABILITY_UNSUPPORTED,)
        elif not self._reference_is_complete(reference):
            state = UniverseEligibilityState.UNKNOWN
            reasons = (UniverseReasonCode.UNKNOWN_REQUIRED_REFERENCE,)
        else:
            reasons_list: list[UniverseReasonCode] = []
            if reference.lifecycle is not LifecycleClass.ACTIVE:
                reasons_list.append(UniverseReasonCode.INELIGIBLE_LIFECYCLE)
            if reference.contract_type is not self.required_contract_type:
                reasons_list.append(UniverseReasonCode.INELIGIBLE_CONTRACT_TYPE)
            if not reasons_list:
                reasons_list.append(UniverseReasonCode.ELIGIBLE_REFERENCE_PROVEN)
                state = UniverseEligibilityState.ELIGIBLE
            else:
                state = UniverseEligibilityState.INELIGIBLE
            reasons = tuple(sorted(set(reasons_list), key=lambda item: item.value))
        return UniverseEntry(
            contract_id=reference.contract_id,
            reference_id=reference.reference_id,
            reference_version=reference.version,
            reference_source=reference.source,
            reference_fingerprint=reference.fingerprint,
            native_symbol=reference.native_symbol,
            state=state,
            reason_codes=reasons,
        )

    @staticmethod
    def _reference_is_complete(reference: ContractReference) -> bool:
        return all(
            value is not None
            for value in (
                reference.base_asset,
                reference.quote_asset,
                reference.settlement_asset,
                reference.price_precision,
                reference.quantity_precision,
            )
        )


def recompute_universe(
    descriptor: ExchangeDescriptor,
    capabilities: CapabilitySnapshot,
    references: Sequence[ContractReference],
    *,
    environment: Environment,
    policy_version: int = 1,
    recomputed_at: datetime | None = None,
) -> UniverseSnapshot:
    """Convenience entry point for one pure, non-persistent recomputation."""

    return MarketUniverseRegistry(policy_version=policy_version).recompute(
        descriptor,
        capabilities,
        references,
        environment=environment,
        recomputed_at=recomputed_at,
    )
