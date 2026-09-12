"""Bounded, public-only MEXC Futures reference adapter for S1B."""

from __future__ import annotations

import hashlib
import http.client
import json
import re
import ssl
import time
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from urllib.parse import urlsplit

from hct_backend.contracts import IdentityKind, StableId
from hct_backend.exchange_reference import (
    CapabilityDeclaration,
    CapabilityName,
    CapabilitySnapshot,
    CapabilityState,
    ContractReference,
    ContractType,
    ExchangeDescriptor,
    LifecycleClass,
    MalformedReferenceError,
    ReferenceUnavailableError,
    UnknownContractError,
)

MEXC_BASE_URL = "https://api.mexc.com"
MEXC_CONTRACT_DETAIL_ENDPOINT = f"{MEXC_BASE_URL}/api/v1/contract/detail/country"
MEXC_HOST = "api.mexc.com"
MEXC_CONTRACT_DETAIL_PATH = "/api/v1/contract/detail/country"
MEXC_REFERENCE_SOURCE = "mexc-public-contract-detail-country"
CONNECT_TIMEOUT_SECONDS = 2.0
READ_TIMEOUT_SECONDS = 3.0
TOTAL_TIMEOUT_SECONDS = 5.0
MAX_RESPONSE_BYTES = 262_144
READ_CHUNK_BYTES = 8_192

_ASSET_PATTERN = re.compile(r"^[A-Z][A-Z0-9._-]{0,31}$")
_NATIVE_SYMBOL_PATTERN = re.compile(r"^[A-Za-z0-9._:/-]{1,64}$")
_MATERIAL_FIELDS = frozenset(
    {
        "symbol",
        "baseCoin",
        "quoteCoin",
        "settleCoin",
        "displayNameEn",
        "futureType",
        "priceScale",
        "volScale",
        "priceUnit",
        "volUnit",
        "minVol",
        "maxVol",
        "state",
    }
)


def _reject_json_constant(value: str) -> object:
    raise ValueError(f"unsupported JSON constant: {value}")


def _bounded_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value or "\x00" in value:
        raise MalformedReferenceError(f"invalid MEXC {label}")
    return value


def _asset(value: object, label: str) -> str:
    text = _bounded_text(value, label)
    if text != text.upper() or not _ASSET_PATTERN.fullmatch(text):
        raise MalformedReferenceError(f"invalid MEXC {label}")
    return text


def _native_symbol(value: object) -> str:
    text = _bounded_text(value, "symbol")
    if not _NATIVE_SYMBOL_PATTERN.fullmatch(text):
        raise MalformedReferenceError("invalid MEXC symbol")
    return text


def _decimal(value: object, label: str) -> Decimal:
    if isinstance(value, int) and not isinstance(value, bool):
        value = Decimal(value)
    if not isinstance(value, Decimal) or not value.is_finite() or value <= 0:
        raise MalformedReferenceError(f"MEXC {label} must be a positive exact decimal")
    return value


def _scale(value: object, increment: Decimal, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise MalformedReferenceError(f"invalid MEXC {label}")
    increment_text = format(increment, "f")
    places = len(increment_text.partition(".")[2].rstrip("0"))
    if places > value:
        raise MalformedReferenceError(f"MEXC {label} is smaller than its increment precision")
    return value


def _multiple(value: Decimal, increment: Decimal, label: str) -> None:
    if value % increment != 0:
        raise MalformedReferenceError(f"MEXC {label} is not aligned to its increment")


def _digest(*parts: str) -> str:
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()


def _stable(kind: IdentityKind, value: str) -> StableId:
    return StableId(kind=kind, value=value)


def _canonical_instrument_id(
    *, base_asset: str, quote_asset: str, settlement_asset: str, contract_type: ContractType
) -> StableId:
    material = _digest(base_asset, quote_asset, settlement_asset, contract_type.value)
    return _stable(IdentityKind.INSTRUMENT, f"mexc-instrument-{material[:32]}")


def _validate_public_endpoint(raw_url: str) -> None:
    parsed = urlsplit(raw_url)
    if (
        parsed.scheme != "https"
        or parsed.hostname != MEXC_HOST
        or parsed.netloc != MEXC_HOST
        or parsed.path != MEXC_CONTRACT_DETAIL_PATH
        or parsed.query
        or parsed.fragment
    ):
        raise ReferenceUnavailableError("MEXC endpoint is outside the public reference allowlist")


class _MexcHttpsTransport:
    """One-shot fixed-endpoint HTTPS transport with bounded reads."""

    def fetch_contract_detail(self) -> bytes:
        _validate_public_endpoint(MEXC_CONTRACT_DETAIL_ENDPOINT)
        started = time.monotonic()
        connection: http.client.HTTPSConnection | None = None
        try:
            connection = http.client.HTTPSConnection(
                MEXC_HOST,
                timeout=CONNECT_TIMEOUT_SECONDS,
                context=ssl.create_default_context(),
            )
            connection.request(
                "GET",
                MEXC_CONTRACT_DETAIL_PATH,
                headers={"Accept": "application/json"},
            )
            response = connection.getresponse()
            if response.status != 200:
                raise ReferenceUnavailableError(
                    "MEXC public reference returned a non-success status"
                )
            content_type = response.getheader("Content-Type") or ""
            if content_type.split(";", 1)[0].strip().lower() != "application/json":
                raise MalformedReferenceError("MEXC public reference is not JSON")
            content_length = response.getheader("Content-Length")
            if content_length is not None:
                try:
                    declared_length = int(content_length)
                except ValueError as error:
                    raise MalformedReferenceError("invalid MEXC response length") from error
                if declared_length < 0 or declared_length > MAX_RESPONSE_BYTES:
                    raise ReferenceUnavailableError("MEXC public reference response is oversized")

            payload = bytearray()
            while True:
                remaining = TOTAL_TIMEOUT_SECONDS - (time.monotonic() - started)
                if remaining <= 0:
                    raise ReferenceUnavailableError("MEXC public reference exceeded total timeout")
                if connection.sock is not None:
                    connection.sock.settimeout(min(READ_TIMEOUT_SECONDS, remaining))
                chunk = response.read(min(READ_CHUNK_BYTES, MAX_RESPONSE_BYTES - len(payload) + 1))
                if not chunk:
                    break
                payload.extend(chunk)
                if len(payload) > MAX_RESPONSE_BYTES:
                    raise ReferenceUnavailableError("MEXC public reference response is oversized")
            return bytes(payload)
        except (ReferenceUnavailableError, MalformedReferenceError):
            raise
        except (http.client.HTTPException, OSError, TimeoutError) as error:
            raise ReferenceUnavailableError("MEXC public reference transport failed") from error
        finally:
            if connection is not None:
                connection.close()


def _parse_payload(payload: bytes, observed_at: datetime) -> tuple[ContractReference, ...]:
    if not isinstance(payload, bytes) or not payload or len(payload) > MAX_RESPONSE_BYTES:
        raise MalformedReferenceError("MEXC response body is missing or oversized")
    try:
        document = json.loads(
            payload.decode("utf-8"),
            parse_float=Decimal,
            parse_int=int,
            parse_constant=_reject_json_constant,
        )
    except (UnicodeDecodeError, ValueError) as error:
        raise MalformedReferenceError("MEXC response is not valid JSON") from error
    if not isinstance(document, Mapping):
        raise MalformedReferenceError("MEXC response envelope is not an object")
    if document.get("success") is not True or document.get("code") != 0:
        raise ReferenceUnavailableError("MEXC public reference reported failure")
    entry = document.get("data")
    if not isinstance(entry, Mapping):
        raise MalformedReferenceError("MEXC contract detail data is not the documented object")
    return (_parse_entry(entry, observed_at),)


def _parse_entry(entry: object, observed_at: datetime) -> ContractReference:
    if not isinstance(entry, Mapping):
        raise MalformedReferenceError("MEXC contract entry is not an object")
    if not _MATERIAL_FIELDS.issubset(entry):
        raise MalformedReferenceError("MEXC contract entry is missing material fields")

    native_symbol = _native_symbol(entry["symbol"])
    base_asset = _asset(entry["baseCoin"], "base asset")
    quote_asset = _asset(entry["quoteCoin"], "quote asset")
    settlement_asset = _asset(entry["settleCoin"], "settlement asset")
    display_name = _bounded_text(entry["displayNameEn"], "English display name")

    raw_future_type = entry["futureType"]
    if not isinstance(raw_future_type, int) or isinstance(raw_future_type, bool):
        raise MalformedReferenceError("MEXC futureType is not an integer")
    presentation = display_name.upper()
    presentation_type = (
        ContractType.PERPETUAL
        if "PERPETUAL" in presentation or presentation.endswith("SWAP")
        else ContractType.FUTURES
        if "DELIVERY" in presentation
        else None
    )
    if raw_future_type == 1:
        contract_type = ContractType.PERPETUAL
    elif raw_future_type == 2:
        raise MalformedReferenceError("MEXC delivery contracts are unsupported in S1B")
    else:
        raise MalformedReferenceError("MEXC futureType is unknown")
    if presentation_type is not None and presentation_type is not contract_type:
        raise MalformedReferenceError("MEXC typed contract type conflicts with display name")

    raw_state = entry["state"]
    if not isinstance(raw_state, int) or isinstance(raw_state, bool):
        raise MalformedReferenceError("MEXC lifecycle state is not an integer")
    lifecycle = (
        LifecycleClass.ACTIVE
        if raw_state == 0
        else LifecycleClass.INACTIVE
        if raw_state in {1, 2, 3, 4}
        else LifecycleClass.UNKNOWN
    )
    if lifecycle is LifecycleClass.UNKNOWN:
        raise MalformedReferenceError("MEXC lifecycle state is unknown")

    price_increment = _decimal(entry["priceUnit"], "priceUnit")
    quantity_increment = _decimal(entry["volUnit"], "volUnit")
    price_precision = _scale(entry["priceScale"], price_increment, "priceScale")
    quantity_precision = _scale(entry["volScale"], quantity_increment, "volScale")
    min_quantity = _decimal(entry["minVol"], "minVol")
    max_quantity = _decimal(entry["maxVol"], "maxVol")
    if max_quantity < min_quantity:
        raise MalformedReferenceError("MEXC quantity bounds are contradictory")
    _multiple(min_quantity, quantity_increment, "minVol")
    _multiple(max_quantity, quantity_increment, "maxVol")

    contract_id = _canonical_instrument_id(
        base_asset=base_asset,
        quote_asset=quote_asset,
        settlement_asset=settlement_asset,
        contract_type=contract_type,
    )
    reference_material = (
        contract_id.as_text(),
        native_symbol,
        lifecycle.value,
        contract_type.value,
        base_asset,
        quote_asset,
        settlement_asset,
        format(price_increment, "f"),
        format(quantity_increment, "f"),
        format(min_quantity, "f"),
        format(max_quantity, "f"),
    )
    reference_id = _stable(
        IdentityKind.REFERENCE_SNAPSHOT,
        f"mexc-reference-{_digest(*reference_material)[:32]}",
    )
    return ContractReference(
        reference_id=reference_id,
        contract_id=contract_id,
        exchange_id=_stable(IdentityKind.EXCHANGE, "mexc-futures"),
        native_symbol=native_symbol,
        lifecycle=lifecycle,
        contract_type=contract_type,
        price_increment=price_increment,
        quantity_increment=quantity_increment,
        source=MEXC_REFERENCE_SOURCE,
        observed_at=observed_at,
        base_asset=base_asset,
        quote_asset=quote_asset,
        settlement_asset=settlement_asset,
        price_precision=price_precision,
        quantity_precision=quantity_precision,
        min_quantity=min_quantity,
        max_quantity=max_quantity,
    )


def _descriptor(observed_at: datetime) -> ExchangeDescriptor:
    exchange_id = _stable(IdentityKind.EXCHANGE, "mexc-futures")
    return ExchangeDescriptor(
        exchange_id=exchange_id,
        display_name="MEXC Futures",
        reference_version=1,
        source=MEXC_REFERENCE_SOURCE,
        observed_at=observed_at,
        metadata=(
            ("endpoint", MEXC_CONTRACT_DETAIL_PATH),
            ("provider_host", MEXC_HOST),
            ("scope", "public-reference"),
        ),
    )


def _capabilities(
    references: tuple[ContractReference, ...], observed_at: datetime
) -> CapabilitySnapshot:
    exchange_id = _stable(IdentityKind.EXCHANGE, "mexc-futures")
    evidence_digest = _digest(*(reference.fingerprint for reference in references))
    snapshot_id = _stable(
        IdentityKind.CAPABILITY_SNAPSHOT, f"mexc-capability-{evidence_digest[:32]}"
    )
    evidence = f"{MEXC_REFERENCE_SOURCE}-validated"
    return CapabilitySnapshot(
        snapshot_id=snapshot_id,
        exchange_id=exchange_id,
        version=1,
        source=MEXC_REFERENCE_SOURCE,
        observed_at=observed_at,
        declarations=(
            CapabilityDeclaration(
                CapabilityName.EXCHANGE_DESCRIPTION, CapabilityState.SUPPORTED, evidence
            ),
            CapabilityDeclaration(
                CapabilityName.PUBLIC_REFERENCE, CapabilityState.SUPPORTED, evidence
            ),
            CapabilityDeclaration(
                CapabilityName.CONTRACT_REFERENCE, CapabilityState.SUPPORTED, evidence
            ),
            CapabilityDeclaration(CapabilityName.PRIVATE_STATE_READ, CapabilityState.UNKNOWN),
            CapabilityDeclaration(CapabilityName.STATE_CHANGE, CapabilityState.UNKNOWN),
            CapabilityDeclaration(CapabilityName.MARGIN_CONFIGURATION, CapabilityState.UNKNOWN),
        ),
    )


@dataclass(frozen=True, slots=True)
class MexcPublicReferenceAdapter:
    """Immutable S1A reference adapter backed by one validated provider snapshot."""

    _descriptor_value: ExchangeDescriptor
    _capabilities_value: CapabilitySnapshot
    _references: tuple[ContractReference, ...]

    def __post_init__(self) -> None:
        if not isinstance(self._references, tuple) or not self._references:
            raise MalformedReferenceError("MEXC adapter requires validated references")
        if self._capabilities_value.exchange_id != self._descriptor_value.exchange_id:
            raise MalformedReferenceError("MEXC capability exchange does not match descriptor")
        if any(
            reference.exchange_id != self._descriptor_value.exchange_id
            for reference in self._references
        ):
            raise MalformedReferenceError("MEXC reference exchange does not match descriptor")
        if len({reference.contract_id for reference in self._references}) != len(self._references):
            raise MalformedReferenceError("MEXC adapter has duplicate canonical references")
        if len({reference.native_symbol for reference in self._references}) != len(
            self._references
        ):
            raise MalformedReferenceError("MEXC adapter has duplicate native references")

    @classmethod
    def load(cls) -> MexcPublicReferenceAdapter:
        timestamp = datetime.now(UTC)
        try:
            payload = _MexcHttpsTransport().fetch_contract_detail()
        except (ReferenceUnavailableError, MalformedReferenceError):
            raise
        except (OSError, TimeoutError) as error:
            raise ReferenceUnavailableError("MEXC public reference transport failed") from error
        return cls._from_payload(payload, timestamp)

    @classmethod
    def _from_payload(cls, payload: bytes, observed_at: datetime) -> MexcPublicReferenceAdapter:
        timestamp = observed_at
        if timestamp.tzinfo is None or timestamp.utcoffset() is None:
            raise MalformedReferenceError("MEXC observation time must be timezone-aware")
        references = _parse_payload(payload, timestamp.astimezone(UTC))
        descriptor = _descriptor(timestamp.astimezone(UTC))
        capabilities = _capabilities(references, timestamp.astimezone(UTC))
        return cls(descriptor, capabilities, references)

    def describe_exchange(self) -> ExchangeDescriptor:
        return self._descriptor_value

    def capability_snapshot(self) -> CapabilitySnapshot:
        return self._capabilities_value

    def list_contract_references(self) -> tuple[ContractReference, ...]:
        return self._references

    def resolve_reference(
        self,
        *,
        contract_id: StableId | None = None,
        native_symbol: str | None = None,
    ) -> ContractReference:
        if contract_id is None and native_symbol is None:
            raise UnknownContractError("a canonical or native reference is required")
        if contract_id is not None and (
            not isinstance(contract_id, StableId) or contract_id.kind is not IdentityKind.INSTRUMENT
        ):
            raise MalformedReferenceError("contract has the wrong identity kind")
        if native_symbol is not None and not _NATIVE_SYMBOL_PATTERN.fullmatch(native_symbol):
            raise MalformedReferenceError("invalid native symbol")
        matches = tuple(
            reference
            for reference in self._references
            if (contract_id is None or reference.contract_id == contract_id)
            and (native_symbol is None or reference.native_symbol == native_symbol)
        )
        if not matches:
            raise UnknownContractError("MEXC reference is unknown")
        if len(matches) != 1:
            raise ReferenceUnavailableError("MEXC reference mapping is ambiguous")
        return matches[0]
