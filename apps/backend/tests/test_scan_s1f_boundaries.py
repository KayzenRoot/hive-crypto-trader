import subprocess
import sys
from pathlib import Path


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
