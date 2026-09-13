import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
SCANNER_PATH = ROOT / "scripts" / "scan_s1e_boundaries.py"
SPEC = importlib.util.spec_from_file_location("scan_s1e_boundaries", SCANNER_PATH)
assert SPEC is not None and SPEC.loader is not None
SCANNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SCANNER)


def test_s1e_production_boundary_is_clean() -> None:
    source = (ROOT / SCANNER.S1E_PRODUCTION_MODULE).read_text(encoding="utf-8")
    assert SCANNER.scan_production_python(SCANNER.S1E_PRODUCTION_MODULE, source) == []


def test_scanner_rejects_transport_and_secret_capabilities() -> None:
    assert SCANNER.scan_production_python(SCANNER.S1E_PRODUCTION_MODULE, "import socket")
    assert SCANNER.scan_production_python(SCANNER.S1E_PRODUCTION_MODULE, "import httpx")
    assert SCANNER.scan_production_python(
        SCANNER.S1E_PRODUCTION_MODULE, "api_key = 'not-a-real-secret'"
    )
    assert SCANNER.scan_production_python(
        SCANNER.S1E_PRODUCTION_MODULE, "client.post('/private/order')"
    )


def test_scanner_ignores_unscoped_files_and_finds_secrets() -> None:
    assert SCANNER.scan_production_python("other.py", "import socket") == []
    assert SCANNER.scan_secrets("fixture.py", "-----BEGIN " + "PRIVATE KEY-----")
