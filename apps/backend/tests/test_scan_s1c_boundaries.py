import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))

import scan_s1c_boundaries as scanner


def test_production_scan_allows_the_provider_neutral_registry_surface() -> None:
    assert (
        scanner.scan_production_python(
            scanner.S1C_PRODUCTION_MODULE,
            "from dataclasses import dataclass\n"
            "from datetime import UTC, datetime\n"
            "from enum import StrEnum\n"
            "import hashlib\n"
            "import json\n",
        )
        == []
    )


def test_production_scan_rejects_network_realtime_trading_and_persistence_shapes() -> None:
    assert scanner.scan_production_python(scanner.S1C_PRODUCTION_MODULE, "import requests\n")
    assert scanner.scan_production_python(scanner.S1C_PRODUCTION_MODULE, "import websocket\n")
    assert scanner.scan_production_python(
        scanner.S1C_PRODUCTION_MODULE, "def place_order(value): pass\n"
    )
    assert scanner.scan_production_python(
        scanner.S1C_PRODUCTION_MODULE, "def persist_snapshot(value): pass\n"
    )
    assert scanner.scan_production_python(
        scanner.S1C_PRODUCTION_MODULE, 'url = "https://example.invalid"\n'
    )


def test_production_scan_does_not_scan_docs_or_tests() -> None:
    assert scanner.scan_production_python("docs/example.md", "import requests\n") == []
    assert scanner.scan_secrets("apps/backend/tests/example.py", "password = '" + "x" * 20 + "'")
