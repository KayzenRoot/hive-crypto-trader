"""Provider-neutral, immutable and read-only exchange reference primitives."""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from enum import StrEnum
from typing import Protocol

from hct_backend.contracts import IdentityKind, StableId

_TEXT_PATTERN = re.compile(r"^[^\x00-\x1f\x7f]{1,256}$")
_TOKEN_PATTERN = re.compile(r"^[A-Z][A-Z0-9._-]{0,31}$")
_SYMBOL_PATTERN = re.compile(r"^[A-Za-z0-9._:/-]{1,64}$")
_METADATA_KEY_PATTERN = re.compile(r"^[a-z][a-z0-9_.-]{0,63}$")
_FORBIDDEN_METADATA_TERMS = ("api", "credential", "password", "secret", "sign", "token")
_SECRET_MARKER_PATTERN = re.compile(
    r"(?i)(?:-----begin|"
    + "api"
    + r"[_-]?key|"
    + "private"
    + r"[_-]?key|"
    + "access"
    + r"[_-]?token|password)"
)


class ExchangeReferenceError(ValueError):
    """Base error for fail-closed reference boundary validation."""


class UnknownContractError(ExchangeReferenceError):
    """Raised when a canonical or native mapping is not known."""


class UnsupportedCapabilityError(ExchangeReferenceError):
    """Raised when a capability is explicitly unsupported."""


class CapabilityUnknownError(ExchangeReferenceError):
    """Raised when capability evidence is absent or explicitly unknown."""


class MalformedReferenceError(ExchangeReferenceError):
    """Raised when reference facts are malformed or internally inconsistent."""


class ReferenceUnavailableError(ExchangeReferenceError):
    """Raised when a bounded reference operation cannot return evidence."""


class CapabilityName(StrEnum):
    EXCHANGE_DESCRIPTION = "EXCHANGE_DESCRIPTION"
    CONTRACT_REFERENCE = "CONTRACT_REFERENCE"
    PUBLIC_REFERENCE = "PUBLIC_REFERENCE"
    PRIVATE_STATE_READ = "PRIVATE_STATE_READ"
    STATE_CHANGE = "STATE_CHANGE"
    MARGIN_CONFIGURATION = "MARGIN_CONFIGURATION"


class CapabilityState(StrEnum):
    SUPPORTED = "SUPPORTED"
    UNSUPPORTED = "UNSUPPORTED"
    UNKNOWN = "UNKNOWN"

    def __bool__(self) -> bool:
        """Only proven support can evaluate as true."""

        return self is CapabilityState.SUPPORTED


class LifecycleClass(StrEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    UNKNOWN = "UNKNOWN"


class ContractType(StrEnum):
    SPOT = "SPOT"
    PERPETUAL = "PERPETUAL"
    FUTURES = "FUTURES"
    OPTION = "OPTION"
    UNKNOWN = "UNKNOWN"


def _safe_text(value: str, label: str) -> str:
    if not isinstance(value, str) or not _TEXT_PATTERN.fullmatch(value):
        raise MalformedReferenceError(f"invalid {label}")
    if _SECRET_MARKER_PATTERN.search(value):
        raise MalformedReferenceError(f"secret-shaped {label} is not permitted")
    return value


def _safe_identity(value: StableId, kind: IdentityKind, label: str) -> StableId:
    if not isinstance(value, StableId) or value.kind is not kind:
        raise MalformedReferenceError(f"{label} has the wrong identity kind")
    return value


def _utc(value: datetime, label: str) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise MalformedReferenceError(f"{label} must be timezone-aware")
    return value.astimezone(UTC)


def _positive_version(value: int, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise MalformedReferenceError(f"invalid {label}")
    return value


def _fingerprint(payload: Mapping[str, object]) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _decimal_text(value: object, label: str) -> str:
    if not isinstance(value, Decimal) or not value.is_finite() or value <= 0:
        raise MalformedReferenceError(f"{label} must be a positive finite Decimal")
    return format(value, "f")


def _precision(value: int | None, increment_text: str, label: str) -> int | None:
    if value is None:
        return None
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise MalformedReferenceError(f"invalid {label}")
    decimal_places = len(increment_text.partition(".")[2].rstrip("0"))
    if decimal_places > value:
        raise MalformedReferenceError(f"{label} is smaller than its increment precision")
    return value


def _optional_decimal(value: object, label: str) -> str | None:
    if value is None:
        return None
    return _decimal_text(value, label)


@dataclass(frozen=True, slots=True)
class ExchangeDescriptor:
    """Safe provider-neutral identity and source metadata for an exchange."""

    exchange_id: StableId
    display_name: str
    reference_version: int
    source: str
    observed_at: datetime
    metadata: tuple[tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        _safe_identity(self.exchange_id, IdentityKind.EXCHANGE, "exchange")
        _safe_text(self.display_name, "display name")
        _positive_version(self.reference_version, "reference version")
        _safe_text(self.source, "source")
        object.__setattr__(self, "observed_at", _utc(self.observed_at, "observed_at"))
        if not isinstance(self.metadata, tuple):
            object.__setattr__(self, "metadata", tuple(self.metadata))
        object.__setattr__(
            self,
            "metadata",
            tuple((key, value) for key, value in self.metadata),
        )
        seen: set[str] = set()
        for key, value in self.metadata:
            if (
                not isinstance(key, str)
                or not _METADATA_KEY_PATTERN.fullmatch(key)
                or key in seen
                or any(term in key for term in _FORBIDDEN_METADATA_TERMS)
            ):
                raise MalformedReferenceError("invalid or unsafe exchange metadata key")
            seen.add(key)
            _safe_text(value, f"metadata.{key}")

    @property
    def fingerprint(self) -> str:
        return _fingerprint(
            {
                "exchange_id": self.exchange_id.as_text(),
                "display_name": self.display_name,
                "reference_version": self.reference_version,
                "source": self.source,
                "observed_at": self.observed_at.isoformat(),
                "metadata": dict(sorted(self.metadata)),
            }
        )


@dataclass(frozen=True, slots=True)
class CapabilityDeclaration:
    """One explicit capability state and its safe evidence note."""

    name: CapabilityName
    state: CapabilityState
    evidence: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.name, CapabilityName) or not isinstance(self.state, CapabilityState):
            raise MalformedReferenceError("invalid capability declaration")
        if self.state is not CapabilityState.UNKNOWN and self.evidence is None:
            raise MalformedReferenceError("known capability state requires evidence")
        if self.evidence is not None:
            _safe_text(self.evidence, "capability evidence")


@dataclass(frozen=True, slots=True)
class CapabilitySnapshot:
    """Immutable, versioned and fail-closed capability evidence."""

    snapshot_id: StableId
    exchange_id: StableId
    version: int
    source: str
    observed_at: datetime
    declarations: tuple[CapabilityDeclaration, ...]

    def __post_init__(self) -> None:
        _safe_identity(self.snapshot_id, IdentityKind.CAPABILITY_SNAPSHOT, "capability snapshot")
        _safe_identity(self.exchange_id, IdentityKind.EXCHANGE, "exchange")
        _positive_version(self.version, "capability version")
        _safe_text(self.source, "source")
        object.__setattr__(self, "observed_at", _utc(self.observed_at, "observed_at"))
        if not isinstance(self.declarations, tuple):
            object.__setattr__(self, "declarations", tuple(self.declarations))
        if not self.declarations:
            raise MalformedReferenceError("capability snapshot must contain declarations")
        if any(not isinstance(item, CapabilityDeclaration) for item in self.declarations):
            raise MalformedReferenceError("invalid capability declaration")
        names = [item.name for item in self.declarations]
        if len(names) != len(set(names)):
            raise MalformedReferenceError("duplicate capability declaration")

    def state_for(self, name: CapabilityName) -> CapabilityState:
        if not isinstance(name, CapabilityName):
            raise MalformedReferenceError("invalid capability name")
        for declaration in self.declarations:
            if declaration.name is name:
                return declaration.state
        return CapabilityState.UNKNOWN

    def is_supported(self, name: CapabilityName) -> bool:
        return self.state_for(name) is CapabilityState.SUPPORTED

    def require_supported(self, name: CapabilityName) -> None:
        state = self.state_for(name)
        if state is CapabilityState.SUPPORTED:
            return
        if state is CapabilityState.UNKNOWN:
            raise CapabilityUnknownError(f"capability is unknown: {name.value}")
        raise UnsupportedCapabilityError(f"capability is unsupported: {name.value}")

    @property
    def fingerprint(self) -> str:
        declarations = [
            {"name": item.name.value, "state": item.state.value, "evidence": item.evidence}
            for item in sorted(self.declarations, key=lambda item: item.name.value)
        ]
        return _fingerprint(
            {
                "snapshot_id": self.snapshot_id.as_text(),
                "exchange_id": self.exchange_id.as_text(),
                "version": self.version,
                "source": self.source,
                "observed_at": self.observed_at.isoformat(),
                "declarations": declarations,
            }
        )


@dataclass(frozen=True, slots=True)
class ContractReference:
    """Immutable canonical contract facts and venue mapping metadata."""

    reference_id: StableId
    contract_id: StableId
    exchange_id: StableId
    native_symbol: str
    lifecycle: LifecycleClass
    contract_type: ContractType
    price_increment: Decimal
    quantity_increment: Decimal
    source: str
    observed_at: datetime
    base_asset: str | None = None
    quote_asset: str | None = None
    settlement_asset: str | None = None
    price_precision: int | None = None
    quantity_precision: int | None = None
    min_quantity: Decimal | None = None
    max_quantity: Decimal | None = None
    min_notional: Decimal | None = None
    max_notional: Decimal | None = None
    version: int = 1

    def __post_init__(self) -> None:
        _safe_identity(self.reference_id, IdentityKind.REFERENCE_SNAPSHOT, "reference")
        _safe_identity(self.contract_id, IdentityKind.INSTRUMENT, "contract")
        _safe_identity(self.exchange_id, IdentityKind.EXCHANGE, "exchange")
        if not isinstance(self.native_symbol, str) or not _SYMBOL_PATTERN.fullmatch(
            self.native_symbol
        ):
            raise MalformedReferenceError("invalid native symbol")
        if not isinstance(self.lifecycle, LifecycleClass) or not isinstance(
            self.contract_type, ContractType
        ):
            raise MalformedReferenceError("invalid lifecycle or contract type")
        if self.lifecycle is LifecycleClass.UNKNOWN or self.contract_type is ContractType.UNKNOWN:
            raise MalformedReferenceError(
                "unknown lifecycle or contract type is not executable reference data"
            )
        price_text = _decimal_text(self.price_increment, "price increment")
        quantity_text = _decimal_text(self.quantity_increment, "quantity increment")
        _precision(self.price_precision, price_text, "price precision")
        _precision(self.quantity_precision, quantity_text, "quantity precision")
        for label, decimal_value in (
            ("min quantity", self.min_quantity),
            ("max quantity", self.max_quantity),
            ("min notional", self.min_notional),
            ("max notional", self.max_notional),
        ):
            _optional_decimal(decimal_value, label)
        self._validate_bounds(self.min_quantity, self.max_quantity, "quantity")
        self._validate_bounds(self.min_notional, self.max_notional, "notional")
        for label, asset_value in (
            ("base asset", self.base_asset),
            ("quote asset", self.quote_asset),
            ("settlement asset", self.settlement_asset),
        ):
            if asset_value is not None and (
                not isinstance(asset_value, str) or not _TOKEN_PATTERN.fullmatch(asset_value)
            ):
                raise MalformedReferenceError(f"invalid {label}")
        _safe_text(self.source, "source")
        object.__setattr__(self, "observed_at", _utc(self.observed_at, "observed_at"))
        _positive_version(self.version, "reference version")

    @staticmethod
    def _validate_bounds(lower: Decimal | None, upper: Decimal | None, label: str) -> None:
        if lower is not None and not isinstance(lower, Decimal):
            raise MalformedReferenceError(f"{label} bounds must use Decimal")
        if upper is not None and not isinstance(upper, Decimal):
            raise MalformedReferenceError(f"{label} bounds must use Decimal")
        if lower is not None and upper is not None and upper < lower:
            raise MalformedReferenceError(f"inconsistent {label} bounds")

    @property
    def fingerprint(self) -> str:
        return _fingerprint(
            {
                "reference_id": self.reference_id.as_text(),
                "contract_id": self.contract_id.as_text(),
                "exchange_id": self.exchange_id.as_text(),
                "native_symbol": self.native_symbol,
                "lifecycle": self.lifecycle.value,
                "contract_type": self.contract_type.value,
                "base_asset": self.base_asset,
                "quote_asset": self.quote_asset,
                "settlement_asset": self.settlement_asset,
                "price_increment": _decimal_text(self.price_increment, "price increment"),
                "quantity_increment": _decimal_text(self.quantity_increment, "quantity increment"),
                "price_precision": self.price_precision,
                "quantity_precision": self.quantity_precision,
                "min_quantity": _optional_decimal(self.min_quantity, "min quantity"),
                "max_quantity": _optional_decimal(self.max_quantity, "max quantity"),
                "min_notional": _optional_decimal(self.min_notional, "min notional"),
                "max_notional": _optional_decimal(self.max_notional, "max notional"),
                "source": self.source,
                "observed_at": self.observed_at.isoformat(),
                "version": self.version,
            }
        )


class ExchangeReferenceAdapter(Protocol):
    """Read-only reference port for future concrete adapters."""

    def describe_exchange(self) -> ExchangeDescriptor: ...

    def capability_snapshot(self) -> CapabilitySnapshot: ...

    def list_contract_references(self) -> tuple[ContractReference, ...]: ...

    def resolve_reference(
        self,
        *,
        contract_id: StableId | None = None,
        native_symbol: str | None = None,
    ) -> ContractReference: ...
