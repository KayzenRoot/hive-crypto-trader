"""Fail-closed S1A candidate boundary and capability scan."""

from __future__ import annotations

import ast
import os
import re
import subprocess

from generate_contracts import ROOT

AUTHORIZED_BASE = "ad8037a2e662eb2100d7626870f31bc97d824fc6"
S1A_SCRIPT = "scripts/scan_s1a_boundaries.py"
ALLOWED_PATHS = (
    re.compile(r"^adr/HCT-ADR-0045-s1a-exchange-reference-foundation\.md$"),
    re.compile(r"^apps/backend/src/hct_backend/(?:contracts|exchange_reference)\.py$"),
    re.compile(r"^apps/backend/tests/test_(?:exchange_reference|scan_s1a_boundaries)\.py$"),
    re.compile(r"^scripts/scan_s1a_boundaries\.py$"),
    re.compile(r"^evidence/HCT-IMP-0004-S1A\.md$"),
    re.compile(r"^\.github/workflows/s1a-quality\.yml$"),
    re.compile(r"^packages/contracts/openapi\.json$"),
    re.compile(r"^apps/backend/src/hct_backend/generated_contracts\.py$"),
    re.compile(r"^apps/frontend/src/generated/contracts\.ts$"),
)
FORBIDDEN_MODULES = frozenset(
    {
        "requests",
        "httpx",
        "aiohttp",
        "socket",
        "web" + "socket",
        "web" + "sockets",
        "urllib",
        "sqlalchemy",
        "alembic",
        "asyncpg",
        "psycopg",
        "redis",
    }
)
FORBIDDEN_CALLS = frozenset(
    {
        "open_connection",
        "urlopen",
        "create_connection",
        "authenticate",
        "sign" + "_request",
        "place" + "_order",
        "cancel" + "_order",
        "replace" + "_order",
        "submit" + "_order",
    }
)
FORBIDDEN_NAMES = frozenset(
    {
        "api" + "_key",
        "secret",
        "password",
        "access" + "_token",
        "private" + "_key",
    }
)
FORBIDDEN_TEXT = ("m" + "exc", "web" + "socket", "sign" + "ing")
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----"),
    re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    re.compile(r"\b(?:gh[pousr]_\w{20,}|github_pat_\w{20,})\b"),
    re.compile(r"(?i)\b(?:api[_-]?key|secret(?:[_-]?value)?|password)\s*[:=]\s*[\"'][^\"']{12,}[\"']"),
)


class BoundaryScanError(RuntimeError):
    """Raised when the candidate cannot be inspected safely."""


def changed_names(base: str) -> list[str]:
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True
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
    for diff_args in (("--",), ("--cached", "--")):
        names.update(
            subprocess.run(
                ["git", "diff", "--name-only", *diff_args],
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


def read_text(name: str) -> str:
    path = ROOT / name
    if not path.is_file():
        raise BoundaryScanError(f"changed candidate is missing: {name}")
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        raise BoundaryScanError(f"changed candidate is not readable UTF-8 text: {name}") from None


def _node_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def scan_production_python(name: str, text: str) -> list[str]:
    if not name.startswith("apps/backend/src/hct_backend/") or not name.endswith(".py"):
        return []
    try:
        tree = ast.parse(text, filename=name)
    except SyntaxError as error:
        raise BoundaryScanError(f"production candidate is not valid Python: {name}: {error}") from error
    failures: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules = [alias.name.split(".", 1)[0].lower() for alias in node.names]
            failures.extend(f"forbidden import {module}: {name}" for module in modules if module in FORBIDDEN_MODULES)
        elif isinstance(node, ast.ImportFrom) and node.module:
            module = node.module.split(".", 1)[0].lower()
            if module in FORBIDDEN_MODULES:
                failures.append(f"forbidden import {module}: {name}")
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if node.name.lower() in FORBIDDEN_CALLS:
                failures.append(f"forbidden state-changing definition {node.name}: {name}")
        elif isinstance(node, ast.Call):
            called = _node_name(node.func)
            if called is not None and called.lower() in FORBIDDEN_CALLS:
                failures.append(f"forbidden state-changing call {called}: {name}")
        elif isinstance(node, ast.Name) and node.id.lower() in FORBIDDEN_NAMES:
            failures.append(f"forbidden sensitive field name {node.id}: {name}")
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            if re.search(r"https?://", node.value, re.IGNORECASE):
                failures.append(f"external URL in production module: {name}")
    lowered = text.lower()
    for marker in FORBIDDEN_TEXT:
        if marker in lowered:
            failures.append(f"forbidden capability marker {marker}: {name}")
    return sorted(set(failures))


def scan_secrets(name: str, text: str) -> list[str]:
    return [f"secret pattern matched in {name}" for pattern in SECRET_PATTERNS if pattern.search(text)]


def main() -> int:
    base = os.environ.get("BASE_SHA", AUTHORIZED_BASE)
    failures: list[str] = []
    names = changed_names(base)
    for name in names:
        if not any(pattern.fullmatch(name) for pattern in ALLOWED_PATHS):
            failures.append(f"changed path outside S1A boundary: {name}")
        if name.startswith(("checkpoints/", "docs/", "work-orders/")) and not name.startswith("adr/"):
            failures.append(f"frozen governance surface changed: {name}")
        if name.startswith("apps/frontend/") and name != "apps/frontend/src/generated/contracts.ts":
            failures.append(f"frontend product surface changed: {name}")
        if name.startswith("packages/") and name != "packages/contracts/openapi.json":
            failures.append(f"shared package outside canonical source changed: {name}")
        try:
            text = read_text(name)
        except BoundaryScanError as error:
            failures.append(str(error))
            continue
        failures.extend(scan_secrets(name, text))
        failures.extend(scan_production_python(name, text))
    if failures:
        print("S1A boundary and secret scan: FAIL")
        print("\n".join(sorted(set(failures))))
        return 1
    print(f"S1A boundary and secret scan: PASS ({len(names)} changed files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
