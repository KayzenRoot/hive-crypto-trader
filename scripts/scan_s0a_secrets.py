"""Scan all changed text files for high-confidence secret material."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

from generate_contracts import ROOT

PATTERNS = (
    re.compile(r"-----BEGIN [A-Z ]+ PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\b(?:sk|ghp|github_pat)-[A-Za-z0-9_]{20,}\b"),
    re.compile(r"(?i)\b(?:api[_-]?key|secret|token|password)\s*[:=]\s*[\"'][^\"']{12,}[\"']"),
)
IGNORED_PARTS = {"node_modules", ".venv", ".tooling", "dist", "__pycache__", ".mypy_cache", ".pytest_cache"}


def changed_files() -> list[Path]:
    base = "c9fadaaf1aea61930d825b8247465c70963d2267"
    result = subprocess.run(
        ["git", "diff", "--name-only", f"{base}...HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    paths: list[Path] = []
    for name in result.stdout.splitlines():
        path = ROOT / name
        if path.is_file() and not IGNORED_PARTS.intersection(path.parts):
            try:
                path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            paths.append(path)
    return paths


def main() -> int:
    failures: list[str] = []
    for path in changed_files():
        text = path.read_text(encoding="utf-8")
        for pattern in PATTERNS:
            if pattern.search(text):
                failures.append(f"secret pattern {pattern.pattern!r}: {path.relative_to(ROOT)}")
    if failures:
        print("S0A secret scan: FAIL")
        print("\n".join(failures))
        return 1
    print(f"S0A secret scan: PASS ({len(changed_files())} changed text files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
