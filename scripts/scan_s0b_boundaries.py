"""Fail-closed S0B changed-text secret and capability boundary scan."""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

from generate_contracts import ROOT

AUTHORIZED_BASE = "aef99bcb9ed3c4af3b27bd97e9629caf4dbf6faf"
ALLOWED_PATHS = (
    re.compile(r"^adr/HCT-ADR-0043-s0b-security-context-secret-boundary\.md$"),
    re.compile(r"^apps/backend/"),
    re.compile(r"^scripts/(?:scan_s0b_boundaries|validate_s0a)\.py$"),
    re.compile(r"^evidence/HCT-IMP-0002-S0B\.md$"),
    re.compile(r"^\.github/workflows/implementation-s0b-governance\.yml$"),
)
FORBIDDEN_SOURCE_PATTERNS = (
    re.compile(r"\b(?:requests|httpx|aiohttp|websocket|websockets|socket)\b", re.IGNORECASE),
    re.compile(r"\b(?:boto3|botocore|hvac|vault|kms|hsm|keyvault)\b", re.IGNORECASE),
    re.compile(r"\b(?:oauth|oidc|sqlalchemy|alembic|asyncpg|psycopg|redis)\b", re.IGNORECASE),
    re.compile(r"\b(?:mexc|create_order|cancel_order|place_order)\b", re.IGNORECASE),
    re.compile(r"\b(?:leverage|positions?|fills?|balances?|pnl)\b", re.IGNORECASE),
)
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN [A-Z ]+ PRIVATE KEY-----"),
    re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    re.compile(r"\b(?:sk|ghp|github_pat)-[A-Za-z0-9_]{20,}\b"),
    re.compile(r"(?i)\b(?:api[_-]?key|secret(?:[_-]?key)?|token|password)\s*[:=]\s*[\"'][^\"']{12,}[\"']"),
)
IGNORED_BINARY_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".ico", ".pyc", ".whl"}
TOOLING_FILES = {"scripts/scan_s0b_boundaries.py", "scripts/validate_s0a.py"}


def changed_names(base: str) -> list[str]:
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    diff_selector = f"{base}...HEAD" if head != base else base
    result = subprocess.run(
        ["git", "diff", "--name-only", diff_selector],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    names = {line for line in result.stdout.splitlines() if line}
    if head == base:
        untracked = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        names.update(line for line in untracked.stdout.splitlines() if line)
    return sorted(names)


def read_changed_text(name: str) -> str | None:
    path = ROOT / name
    if not path.is_file() or path.suffix.lower() in IGNORED_BINARY_SUFFIXES:
        return None
    try:
        return path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None


def main() -> int:
    base = os.environ.get("BASE_SHA", AUTHORIZED_BASE)
    failures: list[str] = []
    names = changed_names(base)

    for name in names:
        if not any(pattern.fullmatch(name) or pattern.match(name) for pattern in ALLOWED_PATHS):
            failures.append(f"changed path outside S0B boundary: {name}")
        if name.startswith(("checkpoints/", "docs/", "work-orders/", "apps/frontend/", "packages/contracts/")):
            failures.append(f"forbidden frozen/public surface changed: {name}")

        text = read_changed_text(name)
        if text is None:
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                failures.append(f"secret pattern {pattern.pattern!r}: {name}")
        if name in TOOLING_FILES or not name.startswith(("apps/backend/", "packages/")):
            continue
        for pattern in FORBIDDEN_SOURCE_PATTERNS:
            if pattern.search(text):
                failures.append(f"prohibited capability marker {pattern.pattern!r}: {name}")
        if re.search(r"https?://", text, re.IGNORECASE):
            failures.append(f"external network URL in implementation surface: {name}")

    if failures:
        print("S0B secret/capability boundary: FAIL")
        print("\n".join(failures))
        return 1
    print(f"S0B secret/capability boundary: PASS ({len(names)} changed files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
