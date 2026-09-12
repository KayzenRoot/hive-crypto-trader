import http.client
import json
from datetime import UTC, datetime
from decimal import Decimal

import pytest

import hct_backend.mexc_reference as mexc_reference
from hct_backend.contracts import IdentityKind, StableId
from hct_backend.exchange_reference import (
    CapabilityName,
    CapabilityState,
    CapabilityUnknownError,
    MalformedReferenceError,
    ReferenceUnavailableError,
)
from hct_backend.mexc_reference import (
    MAX_RESPONSE_BYTES,
    MEXC_CONTRACT_DETAIL_ENDPOINT,
    MexcPublicReferenceAdapter,
    _MexcHttpsTransport,
    _parse_payload,
    _validate_public_endpoint,
)

OBSERVED_AT = datetime(2026, 9, 12, 19, 0, tzinfo=UTC)


def _entry(**overrides: object) -> dict[str, object]:
    value: dict[str, object] = {
        "symbol": "BTC_USDT",
        "displayNameEn": "BTC_USDT SWAP",
        "baseCoin": "BTC",
        "quoteCoin": "USDT",
        "settleCoin": "USDT",
        "priceScale": 1,
        "volScale": 0,
        "priceUnit": 0.1,
        "volUnit": 1,
        "minVol": 1,
        "maxVol": 100,
        "state": 0,
        "apiAllowed": True,
        "unknownProviderField": "must not affect canonical output",
    }
    value.update(overrides)
    return value


def _payload(*entries: dict[str, object]) -> bytes:
    return json.dumps({"success": True, "code": 0, "data": list(entries)}).encode("utf-8")


class FakeTransport:
    def __init__(self, payload: bytes | Exception) -> None:
        self.payload = payload

    def fetch_contract_detail(self) -> bytes:
        if isinstance(self.payload, Exception):
            raise self.payload
        return self.payload


class FakeSocket:
    def __init__(self) -> None:
        self.timeouts: list[float] = []

    def settimeout(self, value: float) -> None:
        self.timeouts.append(value)


class FakeResponse:
    def __init__(
        self,
        *,
        status: int = 200,
        content_type: str = "application/json",
        chunks: tuple[bytes, ...] = (b"{}",),
        content_length: str | None = None,
    ) -> None:
        self.status = status
        self._content_type = content_type
        self._chunks = list(chunks)
        self._content_length = content_length

    def getheader(self, name: str) -> str | None:
        if name == "Content-Type":
            return self._content_type
        if name == "Content-Length":
            return self._content_length
        return None

    def read(self, _size: int) -> bytes:
        return self._chunks.pop(0) if self._chunks else b""


class FakeConnection:
    def __init__(self, response: FakeResponse) -> None:
        self.response = response
        self.sock = FakeSocket()
        self.requests: list[tuple[str, str, dict[str, str]]] = []
        self.closed = False

    def request(self, method: str, path: str, *, headers: dict[str, str]) -> None:
        self.requests.append((method, path, headers))

    def getresponse(self) -> FakeResponse:
        return self.response

    def close(self) -> None:
        self.closed = True


def _adapter(*entries: dict[str, object]) -> MexcPublicReferenceAdapter:
    return MexcPublicReferenceAdapter.load(
        transport=FakeTransport(_payload(*entries)),
        observed_at=OBSERVED_AT,
    )


def test_valid_official_shape_maps_to_immutable_s1a_reference() -> None:
    adapter = _adapter(_entry())
    reference = adapter.list_contract_references()[0]

    assert reference.native_symbol == "BTC_USDT"
    assert reference.base_asset == "BTC"
    assert reference.quote_asset == "USDT"
    assert reference.settlement_asset == "USDT"
    assert reference.price_increment == Decimal("0.1")
    assert reference.quantity_increment == 1
    assert reference.min_quantity == 1
    assert reference.max_quantity == 100
    assert adapter.describe_exchange().display_name == "MEXC Futures"
    assert (
        adapter.capability_snapshot().state_for(CapabilityName.CONTRACT_REFERENCE)
        is CapabilityState.SUPPORTED
    )


def test_unknown_provider_fields_cannot_change_canonical_semantics() -> None:
    with_unknown = _adapter(_entry(unknownProviderField={"different": "shape"}))
    without_unknown = _adapter(_entry())

    assert (
        with_unknown.list_contract_references()[0] == without_unknown.list_contract_references()[0]
    )
    assert (
        with_unknown.capability_snapshot().fingerprint
        == without_unknown.capability_snapshot().fingerprint
    )


def test_native_symbol_change_preserves_canonical_identity_but_changes_mapping_evidence() -> None:
    original = _adapter(_entry(symbol="BTC_USDT"))
    renamed = _adapter(_entry(symbol="BTCUSDT"))

    original_reference = original.list_contract_references()[0]
    renamed_reference = renamed.list_contract_references()[0]
    assert original_reference.contract_id == renamed_reference.contract_id
    assert original_reference.native_symbol != renamed_reference.native_symbol
    assert original_reference.fingerprint != renamed_reference.fingerprint


def test_capability_unknown_is_not_truthy_or_default_upgraded() -> None:
    snapshot = _adapter(_entry()).capability_snapshot()

    assert snapshot.state_for(CapabilityName.PRIVATE_STATE_READ) is CapabilityState.UNKNOWN
    assert snapshot.is_supported(CapabilityName.STATE_CHANGE) is False
    with pytest.raises(CapabilityUnknownError):
        snapshot.require_supported(CapabilityName.STATE_CHANGE)


@pytest.mark.parametrize(
    "overrides",
    [
        {"priceUnit": 0},
        {"volUnit": -1},
        {"minVol": 3, "volUnit": 2},
        {"minVol": 20, "maxVol": 10},
        {"state": 99},
        {"displayNameEn": "BTC_USDT FUTURE"},
        {"priceUnit": "0.1"},
        {"baseCoin": "btc"},
    ],
)
def test_material_provider_inconsistency_fails_closed(overrides: dict[str, object]) -> None:
    with pytest.raises(MalformedReferenceError):
        _adapter(_entry(**overrides))


def test_missing_material_field_fails_closed() -> None:
    value = _entry()
    del value["priceUnit"]
    with pytest.raises(MalformedReferenceError):
        _adapter(value)


@pytest.mark.parametrize(
    "url",
    [
        "http://api.mexc.com/api/v1/contract/detail",
        "https://contract.mexc.com/api/v1/contract/detail",
        "https://api.mexc.com/api/v1/private/order/list",
        "https://api.mexc.com/api/v1/contract/detail?symbol=BTC_USDT",
        "https://api.mexc.com/api/v1/contract/detail/../private/order",
    ],
)
def test_public_endpoint_allowlist_rejects_substitution(url: str) -> None:
    with pytest.raises(ReferenceUnavailableError):
        _validate_public_endpoint(url)


def test_fixed_endpoint_is_the_only_production_endpoint() -> None:
    _validate_public_endpoint(MEXC_CONTRACT_DETAIL_ENDPOINT)
    assert MEXC_CONTRACT_DETAIL_ENDPOINT == "https://api.mexc.com/api/v1/contract/detail"


def test_malformed_or_oversized_payload_fails_closed() -> None:
    with pytest.raises(MalformedReferenceError):
        MexcPublicReferenceAdapter.load(
            transport=FakeTransport(b"not-json"),
            observed_at=OBSERVED_AT,
        )
    with pytest.raises(MalformedReferenceError):
        MexcPublicReferenceAdapter.load(
            transport=FakeTransport(b"{" + b"a" * MAX_RESPONSE_BYTES + b"}"),
            observed_at=OBSERVED_AT,
        )


def test_transport_failure_is_bounded_provider_error() -> None:
    with pytest.raises(ReferenceUnavailableError):
        MexcPublicReferenceAdapter.load(
            transport=FakeTransport(TimeoutError("test timeout")),
            observed_at=OBSERVED_AT,
        )


def test_fixed_https_transport_gets_bounded_json_response(monkeypatch: pytest.MonkeyPatch) -> None:
    response = FakeResponse(chunks=(b"{", b"}"), content_length="2")
    connection = FakeConnection(response)
    monkeypatch.setattr(
        mexc_reference.http.client,
        "HTTPSConnection",
        lambda *args, **kwargs: connection,
    )

    assert _MexcHttpsTransport().fetch_contract_detail() == b"{}"
    assert connection.requests == [
        ("GET", "/api/v1/contract/detail", {"Accept": "application/json"})
    ]
    assert connection.sock.timeouts
    assert connection.closed is True


@pytest.mark.parametrize(
    "response, expected",
    [
        (FakeResponse(status=503), ReferenceUnavailableError),
        (FakeResponse(content_type="text/html"), MalformedReferenceError),
        (FakeResponse(content_length="not-an-int"), MalformedReferenceError),
        (FakeResponse(content_length=str(MAX_RESPONSE_BYTES + 1)), ReferenceUnavailableError),
    ],
)
def test_https_transport_rejects_status_content_type_and_declared_size(
    monkeypatch: pytest.MonkeyPatch,
    response: FakeResponse,
    expected: type[Exception],
) -> None:
    connection = FakeConnection(response)
    monkeypatch.setattr(
        mexc_reference.http.client,
        "HTTPSConnection",
        lambda *args, **kwargs: connection,
    )

    with pytest.raises(expected):
        _MexcHttpsTransport().fetch_contract_detail()
    assert connection.closed is True


def test_https_transport_rejects_actual_oversize_and_transport_exceptions(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    response = FakeResponse(chunks=(b"x" * (MAX_RESPONSE_BYTES + 1),))
    connection = FakeConnection(response)
    monkeypatch.setattr(
        mexc_reference.http.client,
        "HTTPSConnection",
        lambda *args, **kwargs: connection,
    )
    with pytest.raises(ReferenceUnavailableError):
        _MexcHttpsTransport().fetch_contract_detail()
    assert connection.closed is True

    def raise_os_error(*_args: object, **_kwargs: object) -> FakeConnection:
        raise OSError("transport unavailable")

    monkeypatch.setattr(mexc_reference.http.client, "HTTPSConnection", raise_os_error)
    with pytest.raises(ReferenceUnavailableError):
        _MexcHttpsTransport().fetch_contract_detail()


def test_https_transport_maps_http_exception_and_total_deadline(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    response = FakeResponse()
    connection = FakeConnection(response)
    monkeypatch.setattr(
        mexc_reference.http.client,
        "HTTPSConnection",
        lambda *args, **kwargs: connection,
    )
    clock = iter((0.0, 6.0))
    monkeypatch.setattr(mexc_reference.time, "monotonic", lambda: next(clock))
    with pytest.raises(ReferenceUnavailableError):
        _MexcHttpsTransport().fetch_contract_detail()

    def raise_http_exception(*_args: object, **_kwargs: object) -> FakeConnection:
        raise http.client.HTTPException("bad response")

    monkeypatch.setattr(mexc_reference.http.client, "HTTPSConnection", raise_http_exception)
    monkeypatch.setattr(mexc_reference.time, "monotonic", lambda: 0.0)
    with pytest.raises(ReferenceUnavailableError):
        _MexcHttpsTransport().fetch_contract_detail()


@pytest.mark.parametrize(
    "payload",
    [
        b"[]",
        b'{"success":true,"code":0,"data":[]}',
        b'{"success":true,"code":0,"data":{}}',
        b'{"success":true,"code":0,"data":[1]}',
        b'{"success":true,"code":0,"data":[{"symbol":"BTC_USDT"}]}',
    ],
)
def test_payload_envelope_and_entries_fail_closed(payload: bytes) -> None:
    with pytest.raises(MalformedReferenceError):
        _parse_payload(payload, OBSERVED_AT)


def test_provider_failure_envelope_is_unavailable() -> None:
    with pytest.raises(ReferenceUnavailableError):
        _parse_payload(b'{"success":false,"code":1001,"data":[]}', OBSERVED_AT)


def test_duplicate_canonical_or_native_entries_fail_closed() -> None:
    with pytest.raises(MalformedReferenceError):
        _parse_payload(_payload(_entry(), _entry(symbol="BTCUSDT")), OBSERVED_AT)
    with pytest.raises(MalformedReferenceError):
        _parse_payload(_payload(_entry(), _entry(baseCoin="ETH", symbol="BTC_USDT")), OBSERVED_AT)


def test_inactive_provider_state_maps_to_inactive() -> None:
    reference = _adapter(_entry(state=1)).list_contract_references()[0]
    assert reference.lifecycle.value == "INACTIVE"


def test_load_requires_timezone_aware_observation_and_translates_transport_errors() -> None:
    with pytest.raises(MalformedReferenceError):
        MexcPublicReferenceAdapter.load(
            transport=FakeTransport(_payload(_entry())),
            observed_at=datetime(2026, 9, 12, 19, 0),
        )
    with pytest.raises(ReferenceUnavailableError):
        MexcPublicReferenceAdapter.load(
            transport=FakeTransport(OSError("socket failure")),
            observed_at=OBSERVED_AT,
        )


def test_reference_resolution_requires_canonical_instrument_identity_or_native_mapping() -> None:
    adapter = _adapter(_entry())
    reference = adapter.list_contract_references()[0]

    assert adapter.resolve_reference(native_symbol="BTC_USDT") == reference
    assert adapter.resolve_reference(contract_id=reference.contract_id) == reference
    with pytest.raises(ValueError):
        adapter.resolve_reference()
    with pytest.raises(ValueError):
        adapter.resolve_reference(
            contract_id=StableId(kind=IdentityKind.EXCHANGE, value="mexc-futures")
        )
