import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))

import scan_s1d_boundaries as scanner


def test_production_scan_allows_provider_neutral_control_state() -> None:
    assert (
        scanner.scan_production_python(
            scanner.S1D_PRODUCTION_MODULE,
            "from dataclasses import dataclass\n"
            "from enum import StrEnum\n"
            "import hashlib\n"
            "import json\n"
            "from hct_backend.contracts import IdentityKind, StableId\n",
        )
        == []
    )


def test_production_scan_rejects_network_provider_and_live_shapes() -> None:
    assert scanner.scan_production_python(scanner.S1D_PRODUCTION_MODULE, "import requests\n")
    assert scanner.scan_production_python(scanner.S1D_PRODUCTION_MODULE, "import socket\n")
    assert scanner.scan_production_python(
        scanner.S1D_PRODUCTION_MODULE, "def subscribe_to_venue(value): pass\n"
    )
    assert scanner.scan_production_python(
        scanner.S1D_PRODUCTION_MODULE, "def persist_state(value): pass\n"
    )
    assert scanner.scan_production_python(
        scanner.S1D_PRODUCTION_MODULE, 'url = "https://example.invalid"\n'
    )
    assert scanner.scan_production_python(
        scanner.S1D_PRODUCTION_MODULE, 'neutral = "ws://example.invalid"\n'
    )
    assert scanner.scan_production_python(
        scanner.S1D_PRODUCTION_MODULE, 'neutral = "wss://example.invalid/ws"\n'
    )
    assert scanner.scan_production_python(
        scanner.S1D_PRODUCTION_MODULE, 'neutral = "contract.mexc.com"\n'
    )
    assert scanner.scan_production_python(
        scanner.S1D_PRODUCTION_MODULE,
        "from hct_backend.contracts import Environment\n",
    )


def test_production_scan_does_not_scan_docs_or_tests() -> None:
    assert scanner.scan_production_python("docs/example.md", "import requests\n") == []
    assert scanner.scan_secrets("apps/backend/tests/example.py", "password = '" + "x" * 20 + "'")
