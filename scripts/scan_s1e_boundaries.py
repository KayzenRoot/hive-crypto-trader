"""Fail-closed S1E changed-file, capability, and secret scanner."""

from __future__ import annotations

import ast
import os
import re
import subprocess

from generate_contracts import ROOT

AUTHORIZED_BASE = "2662f81dafb848724bfba0d2f445b03f0c96b959"
S1E_PRODUCTION_MODULE = "apps/backend/src/hct_backend/market_truth.py"
ALLOWED_PATHS = (
    re.compile(r"^adr/HCT-ADR-0049-s1e-market-truth-foundation\.md$"),
    re.compile(r"^apps/backend/src/hct_backend/market_truth\.py$"),
    re.compile(r"^apps/backend/tests/test_market_truth\.py$"),
    re.compile(r"^apps/backend/tests/test_scan_s1e_boundaries\.py$"),
    re.compile(r"^scripts/scan_s1e_boundaries\.py$"),
    re.compile(r"^evidence/HCT-IMP-0008-S1E\.md$"),
    re.compile(r"^\.github/workflows/s1e-quality\.yml$"),
)
ALLOWED_PRODUCTION_IMPORTS = frozenset(
    {
        "__future__",
        "datetime",
        "dataclasses",
        "enum",
        "hashlib",
        "json",
        "re",
        "typing",
        "hct_backend.contracts",
        "hct_backend.market_universe",
    }
)
FORBIDDEN_IMPORT_ROOTS = frozenset(
    {
        "aiohttp",
        "asyncio",
        "databases",
        "grpc",
        "httpx",
        "psycopg",
        "pymongo",
        "redis",
        "requests",
        "socket",
        "sqlalchemy",
        "subprocess",
        "urllib",
        "websocket",
    }
)
FORBIDDEN_CAPABILITY_PATTERNS = (
    re.compile(r"(?i)(?:https?|wss?)://"),
    re.compile(r"(?i)\b(?:api[_-]?key|credential|password|secret[_-]?value)\b"),
    re.compile(r"(?i)/(?:private|account|order|position|balance|trade)(?:/|$)"),
    re.compile(
        r"(?i)\b(?:place[_-]?order|cancel[_-]?order|sign(?:ing|ature)?|persist(?:ence)?|deploy(?:ment)?|real[_-]?money)\b"
    ),
)
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----"),
    re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    re.compile(r"\b(?:gh[pousr]_\w{20,}|github_pat_\w{20,})\b"),
)


class BoundaryScanError(RuntimeError):
    """Raised when the production boundary cannot be inspected safely."""


def changed_names(base: str) -> list[str]:
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    selector = f"{base}...HEAD" if head != base else base
    names = set(
        subprocess.run(
            ["git", "diff", "--name-only", selector],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
    )
    names.update(
        subprocess.run(
            ["git", "diff", "--name-only", "--"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
    )
    names.update(
        subprocess.run(
            ["git", "diff", "--name-only", "--cached", "--"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
    )
    names.update(
        subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
    )
    return sorted(name for name in names if name)


def _imports(tree: ast.AST) -> list[str]:
    values: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            values.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            values.append(node.module or "")
    return values


def scan_production_python(name: str, text: str) -> list[str]:
    if name != S1E_PRODUCTION_MODULE:
        return []
    try:
        tree = ast.parse(text, filename=name)
    except SyntaxError as error:
        raise BoundaryScanError(
            f"invalid production Python: {name}: {error}"
        ) from error
    failures: list[str] = []
    for module in _imports(tree):
        root = module.split(".", 1)[0].lower()
        if root in FORBIDDEN_IMPORT_ROOTS:
            failures.append(f"forbidden import {module}")
        if module not in ALLOWED_PRODUCTION_IMPORTS:
            failures.append(f"unapproved production import {module}")
    for pattern in FORBIDDEN_CAPABILITY_PATTERNS:
        if pattern.search(text):
            failures.append(f"forbidden capability pattern {pattern.pattern}")
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            failures.append(f"secret pattern {pattern.pattern}")
    return sorted(set(failures))


def scan_secrets(name: str, text: str) -> list[str]:
    return [
        f"secret pattern matched in {name}"
        for pattern in SECRET_PATTERNS
        if pattern.search(text)
    ]


def main() -> int:
    base = os.environ.get("BASE_SHA", AUTHORIZED_BASE)
    failures: list[str] = []
    names = changed_names(base)
    for name in names:
        if not any(pattern.fullmatch(name) for pattern in ALLOWED_PATHS):
            failures.append(f"changed path outside S1E boundary: {name}")
        try:
            text = (ROOT / name).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            failures.append(f"changed candidate is not readable UTF-8 text: {name}")
            continue
        failures.extend(scan_secrets(name, text))
        failures.extend(scan_production_python(name, text))
    if failures:
        print("S1E boundary and secret scan: FAIL")
        print("\n".join(sorted(set(failures))))
        return 1
    print(f"S1E boundary and secret scan: PASS ({len(names)} changed files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
