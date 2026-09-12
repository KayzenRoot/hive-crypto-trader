import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))

import scan_s1a_boundaries as scanner


def test_production_scan_rejects_representative_network_and_client_paths() -> None:
    candidate = "apps/backend/src/hct_backend/candidate.py"
    assert scanner.scan_production_python(candidate, "import httpx\n")
    assert scanner.scan_production_python(candidate, "from urllib import request\n")
    assert scanner.scan_production_python(candidate, "from http import client\n")
    assert scanner.scan_production_python(candidate, "client = Client()\n")


def test_production_scan_rejects_auth_and_signature_shapes() -> None:
    candidate = "apps/backend/src/hct_backend/candidate.py"
    assert scanner.scan_production_python(candidate, "def sign(payload): pass\n")
    assert scanner.scan_production_python(candidate, "def authenticate_request(): pass\n")
    assert scanner.scan_production_python(candidate, "def load_reference(api" + "_key): pass\n")
    assert scanner.scan_production_python(candidate, "request.signature = value\n")


def test_production_scan_rejects_exchange_mutation_and_market_runtime_shapes() -> None:
    candidate = "apps/backend/src/hct_backend/candidate.py"
    assert scanner.scan_production_python(candidate, "def set_" + "lever" + "age(value): pass\n")
    assert scanner.scan_production_python(candidate, "def set_margin_mode(mode): pass\n")
    assert scanner.scan_production_python(candidate, "def amend_order(order): pass\n")
    assert scanner.scan_production_python(candidate, "def subscribe_market_data(): pass\n")


def test_production_scan_rejects_persistence_imports_and_adapter_definitions() -> None:
    candidate = "apps/backend/src/hct_backend/candidate.py"
    assert scanner.scan_production_python(candidate, "import sqlite3\n")
    assert scanner.scan_production_python(candidate, "class ReferenceRepository: pass\n")


def test_production_scan_does_not_scan_documentation_vocabulary() -> None:
    assert (
        scanner.scan_production_python("docs/example.md", "def sign(): pass\nimport httpx\n") == []
    )
    assert (
        scanner.scan_production_python("apps/backend/tests/example.py", "def sign(): pass\n") == []
    )


def test_production_scan_does_not_treat_authority_as_authentication() -> None:
    assert scanner.scan_production_python(
        "apps/backend/src/hct_backend/candidate.py", "def authority(): pass\n"
    ) == []


def test_secret_scan_rejects_secret_shaped_text() -> None:
    value = "password = '" + "x" * 20 + "'"
    assert scanner.scan_secrets("apps/backend/src/hct_backend/candidate.py", value)
