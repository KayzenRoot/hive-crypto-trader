import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))

import scan_s1a_boundaries as scanner


def test_production_scan_rejects_network_and_state_change_shapes() -> None:
    assert scanner.scan_production_python(
        "apps/backend/src/hct_backend/candidate.py", "import httpx\n"
    )
    assert scanner.scan_production_python(
        "apps/backend/src/hct_backend/candidate.py", "def place_order(): pass\n"
    )


def test_production_scan_does_not_scan_documentation_vocabulary() -> None:
    marker = "m" + "exc"
    assert scanner.scan_production_python("docs/example.md", marker) == []


def test_secret_scan_rejects_secret_shaped_text() -> None:
    value = "password = '" + "x" * 20 + "'"
    assert scanner.scan_secrets("apps/backend/src/hct_backend/candidate.py", value)
