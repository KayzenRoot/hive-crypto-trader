"""Fail-closed S0C changed-text secret and capability boundary scan."""

from __future__ import annotations

import os
import re
import subprocess

from generate_contracts import ROOT

AUTHORIZED_BASE = "29dc6636360953941a7e4fb41a0876c5bc46dcd6"
ALLOWED_PATHS = (
    re.compile(r"^adr/HCT-ADR-0044-s0c-audit-evidence-config-provenance\.md$"),
    re.compile(r"^apps/backend/"),
    re.compile(r"^scripts/scan_s0c_boundaries\.py$"),
    re.compile(r"^evidence/HCT-IMP-0003-S0C\.md$"),
    re.compile(r"^\.github/workflows/implementation-s0c-governance\.yml$"),
)
FORBIDDEN_SOURCE_PATTERNS = (
    re.compile(
        r"\b(?:requests|httpx|aiohttp|" + "web" + "socket|" + "web" + "sockets|socket)\b",
        re.IGNORECASE,
    ),
    re.compile(r"\b(?:boto3|botocore|hvac|vault|kms|hsm|keyvault)\b", re.IGNORECASE),
    re.compile(r"\b(?:oauth|oidc|sqlalchemy|alembic|asyncpg|psycopg|redis)\b", re.IGNORECASE),
    re.compile(
        r"\b(?:" + "m" + "exc|create" + "_order|cancel" + "_order|place" + "_order)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:" + "lever" + "age|posit" + "ions?|fills?|bal" + "ances?|pnl)\b",
        re.IGNORECASE,
    ),
    re.compile(r"\b(?:deploy|limited-live|real-money|production-trading)\b", re.IGNORECASE),
)
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----"),
    re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    re.compile(r"\b(?:gh[pousr]_|github_pat_)[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\b(?:sk|ghp|github_pat)[_-][A-Za-z0-9_]{20,}\b"),
    re.compile(
        r"(?i)\b(?:api[_-]?key|secret[_-]?value|access[_-]?token|password)\s*[:=]\s*"
        r"[\"'][^\"']{12,}[\"']"
    ),
)
TOOLING_FILES = {"scripts/scan_s0c_boundaries.py"}


class BoundaryScanError(RuntimeError):
    """Raised when a changed candidate cannot be inspected safely."""


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
    for diff_args in (("--",), ("--cached", "--")):
        working_tree = subprocess.run(
            ["git", "diff", "--name-only", *diff_args],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        names.update(line for line in working_tree.stdout.splitlines() if line)
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    names.update(line for line in untracked.stdout.splitlines() if line)
    return sorted(names)


def read_changed_text(name: str) -> str:
    path = ROOT / name
    if not path.is_file():
        raise BoundaryScanError(f"changed candidate is missing or unreadable: {name}")
    try:
        return path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        raise BoundaryScanError(f"changed candidate is not readable UTF-8 text: {name}") from None


def scan_secret_text(name: str, text: str) -> list[str]:
    return [
        f"secret pattern {pattern.pattern!r}: {name}"
        for pattern in SECRET_PATTERNS
        if pattern.search(text)
    ]


def scan_capability_text(name: str, text: str) -> list[str]:
    if name in TOOLING_FILES or not name.startswith("apps/backend/"):
        return []
    failures = [
        f"prohibited capability marker {pattern.pattern!r}: {name}"
        for pattern in FORBIDDEN_SOURCE_PATTERNS
        if pattern.search(text)
    ]
    if re.search(r"https?://", text, re.IGNORECASE):
        failures.append(f"external network URL in implementation surface: {name}")
    return failures


def main() -> int:
    base = os.environ.get("BASE_SHA", AUTHORIZED_BASE)
    failures: list[str] = []
    names = changed_names(base)

    for name in names:
        if not any(pattern.fullmatch(name) or pattern.match(name) for pattern in ALLOWED_PATHS):
            failures.append(f"changed path outside S0C boundary: {name}")
        if name.startswith(
            ("checkpoints/", "docs/", "work-orders/", "apps/frontend/", "packages/contracts/")
        ):
            failures.append(f"forbidden frozen/public surface changed: {name}")

        try:
            text = read_changed_text(name)
        except BoundaryScanError as error:
            failures.append(str(error))
            continue
        failures.extend(scan_secret_text(name, text))
        failures.extend(scan_capability_text(name, text))

    if failures:
        print("S0C secret/capability boundary: FAIL")
        print("\n".join(failures))
        return 1
    print(f"S0C secret/capability boundary: PASS ({len(names)} changed files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
