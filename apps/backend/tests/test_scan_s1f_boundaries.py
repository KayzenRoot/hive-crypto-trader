import subprocess
import sys
from pathlib import Path

from scripts.scan_s1f_boundaries import scan_text


def test_s1f_boundary_scanner_passes() -> None:
    root = Path(__file__).parents[3]
    result = subprocess.run(
        [sys.executable, "scripts/scan_s1f_boundaries.py"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_s1f_boundary_scanner_rejects_unapproved_public_endpoint() -> None:
    failures = scan_text(
        Path("synthetic_s1f.py"),
        'MEXC_REST_NEW = "/api/v1/contract/funding_rate/"\n',
    )
    assert any("unauthorized MEXC REST path" in failure for failure in failures)


def test_s1f_boundary_scanner_rejects_changed_ws_intent_allowlist() -> None:
    failures = scan_text(
        Path("synthetic_s1f.py"),
        'MEXC_PUBLIC_CHANNELS = ("sub.ticker",)\n',
    )
    assert any("public WS intent allowlist changed" in failure for failure in failures)
