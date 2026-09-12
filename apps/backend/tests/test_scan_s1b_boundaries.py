import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))

import scan_s1b_boundaries as scanner


def test_production_scan_allows_only_the_fixed_provider_transport_imports() -> None:
    candidate = scanner.S1B_PRODUCTION_MODULE
    text = (
        'MEXC_BASE_URL = "https://api.mexc.com"\n'
        'MEXC_CONTRACT_DETAIL_PATH = "/api/v1/contract/detail"\n'
        "import http.client\n"
        "import ssl\n"
        "connection = http.client.HTTPSConnection(MEXC_HOST)\n"
        'connection.request("GET", "/api/v1/contract/detail")\n'
    )
    assert scanner.scan_production_python(candidate, text) == []


def test_production_scan_rejects_private_network_and_auth_shapes() -> None:
    candidate = scanner.S1B_PRODUCTION_MODULE
    assert scanner.scan_production_python(candidate, "import requests\n")
    assert scanner.scan_production_python(candidate, "import websocket\n")
    assert scanner.scan_production_python(candidate, "def sign_request(value): pass\n")
    assert scanner.scan_production_python(candidate, "def load(api_key): pass\n")
    assert scanner.scan_production_python(
        candidate, 'connection.request("GET", "/api/v1/private/order")\n'
    )


def test_production_scan_rejects_endpoint_escape_and_unauthorized_urls() -> None:
    candidate = scanner.S1B_PRODUCTION_MODULE
    assert scanner.scan_production_python(
        candidate,
        'MEXC_BASE_URL = "https://api.mexc.com"\n'
        'MEXC_CONTRACT_DETAIL_PATH = "/api/v1/contract/detail"\n'
        "import http.client\n"
        "connection = http.client.HTTPSConnection(user_host)\n"
        'connection.request("GET", user_path)\n',
    )
    assert scanner.scan_production_python(
        candidate,
        'MEXC_BASE_URL = "https://api.mexc.com"\n'
        'MEXC_CONTRACT_DETAIL_PATH = "/api/v1/contract/detail"\n'
        'OTHER = "https://example.invalid/route"\n',
    )


def test_production_scan_rejects_persistence_and_state_change_shapes() -> None:
    candidate = scanner.S1B_PRODUCTION_MODULE
    assert scanner.scan_production_python(candidate, "import sqlite3\n")
    assert scanner.scan_production_python(candidate, "def place_order(value): pass\n")
    assert scanner.scan_production_python(candidate, "def set_leverage(value): pass\n")


def test_production_scan_does_not_scan_docs_or_tests() -> None:
    assert scanner.scan_production_python("docs/example.md", "import requests\n") == []
    assert (
        scanner.scan_production_python(
            "apps/backend/tests/example.py", "def sign_request(): pass\n"
        )
        == []
    )


def test_secret_scan_rejects_secret_shaped_text() -> None:
    value = "password = '" + "x" * 20 + "'"
    assert scanner.scan_secrets(scanner.S1B_PRODUCTION_MODULE, value)
