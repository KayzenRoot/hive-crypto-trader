"""Fail-closed S1C production boundary, changed-file and secret scanner."""

from __future__ import annotations

import ast
import os
import re
import subprocess

from generate_contracts import ROOT

AUTHORIZED_BASE = "d9f9ea664bc38801c8c6a0b99ddf528f9743862d"
S1C_PRODUCTION_MODULE = "apps/backend/src/hct_backend/market_universe.py"
ALLOWED_PATHS = (
    re.compile(r"^adr/HCT-ADR-0047-s1c-market-universe-registry\.md$"),
    re.compile(r"^apps/backend/src/hct_backend/market_universe\.py$"),
    re.compile(r"^apps/backend/src/hct_backend/contracts\.py$"),
    re.compile(r"^apps/backend/src/hct_backend/generated_contracts\.py$"),
    re.compile(r"^apps/backend/tests/test_market_universe\.py$"),
    re.compile(r"^apps/backend/tests/test_scan_s1c_boundaries\.py$"),
    re.compile(r"^scripts/scan_s1c_boundaries\.py$"),
    re.compile(r"^scripts/validate_contract_parity\.py$"),
    re.compile(r"^packages/contracts/openapi\.json$"),
    re.compile(r"^apps/frontend/src/generated/contracts\.ts$"),
    re.compile(r"^evidence/HCT-IMP-0006-S1C\.md$"),
    re.compile(r"^\.github/workflows/s1c-quality\.yml$"),
)
ALLOWED_PRODUCTION_IMPORTS = frozenset(
    {
        "__future__",
        "collections.abc",
        "dataclasses",
        "datetime",
        "enum",
        "hashlib",
        "json",
        "re",
        "typing",
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
        "urllib3",
        "websocket",
    }
)
FORBIDDEN_NAME_PATTERNS = (
    re.compile(
        r"(?i)(?:api[_-]?key|secret|password|credential|signature|signing|auth(?:enticate|entication)?)"
    ),
    re.compile(
        r"(?i)(?:websocket|socket|subscribe|unsubscribe|stream|reconnect|resubscribe)"
    ),
    re.compile(
        r"(?i)(?:place|submit|cancel|replace|amend|modify|delete|execute)_.*(?:order|position)"
    ),
    re.compile(
        r"(?i)(?:set|change|update|configure|enable|disable|reset)_.*(?:leverage|margin)"
    ),
    re.compile(
        r"(?i)(?:repository|persistence|persist|database|storage|sqlalchemy|redis|mongo|postgres|sqlite)"
    ),
    re.compile(r"(?i)(?:liquidity|volume|spread|volatility|scanner|ranking|candidate)"),
    re.compile(r"(?i)(?:deploy|production|limited[_-]?live|real[_-]?money|trading)"),
)
FORBIDDEN_ROUTE_TERMS = re.compile(
    r"(?i)/(?:private|account|order|position|balance|trade|ticker|depth|kline|funding|open_interest)(?:/|$)"
)
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----"),
    re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    re.compile(r"\b(?:gh[pousr]_\w{20,}|github_pat_\w{20,})\b"),
    re.compile(
        r"(?i)\b(?:api[_-]?key|secret(?:[_-]?value)?|password)\s*[:=]\s*[\"'][^\"']{12,}[\"']"
    ),
)


class BoundaryScanError(RuntimeError):
    """Raised when a candidate cannot be inspected safely."""


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


def _node_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def _forbidden_name(name: str) -> bool:
    return any(pattern.search(name) for pattern in FORBIDDEN_NAME_PATTERNS)


def _import_names(node: ast.Import | ast.ImportFrom) -> list[str]:
    if isinstance(node, ast.Import):
        return [alias.name for alias in node.names]
    return [node.module or ""]


def scan_production_python(name: str, text: str) -> list[str]:
    if name != S1C_PRODUCTION_MODULE:
        return []
    try:
        tree = ast.parse(text, filename=name)
    except SyntaxError as error:
        raise BoundaryScanError(
            f"production candidate is not valid Python: {name}: {error}"
        ) from error
    failures: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for module in _import_names(node):
                root = module.split(".", 1)[0].lower()
                if root in FORBIDDEN_IMPORT_ROOTS:
                    failures.append(f"forbidden import {module}: {name}")
                if module not in ALLOWED_PRODUCTION_IMPORTS and root != "hct_backend":
                    failures.append(f"unapproved production import {module}: {name}")
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if _forbidden_name(node.name):
                failures.append(f"forbidden production symbol {node.name}: {name}")
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                arguments = (
                    *node.args.posonlyargs,
                    *node.args.args,
                    *node.args.kwonlyargs,
                )
                if node.args.vararg is not None:
                    arguments = (*arguments, node.args.vararg)
                if node.args.kwarg is not None:
                    arguments = (*arguments, node.args.kwarg)
                for argument in arguments:
                    if _forbidden_name(argument.arg):
                        failures.append(
                            f"forbidden production argument {argument.arg}: {name}"
                        )
        elif isinstance(node, ast.Call):
            called = _node_name(node.func)
            if called is not None and _forbidden_name(called):
                failures.append(f"forbidden production call {called}: {name}")
        elif isinstance(node, ast.Name) and _forbidden_name(node.id):
            failures.append(f"forbidden production name {node.id}: {name}")
        elif isinstance(node, ast.Attribute) and _forbidden_name(node.attr):
            failures.append(f"forbidden production attribute {node.attr}: {name}")
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Constant)
            and isinstance(node.value, str)
            and (
                "http://" in node.value
                or "https://" in node.value
                or FORBIDDEN_ROUTE_TERMS.search(node.value)
            )
        ):
            failures.append(
                f"network or exchange route vocabulary in production module: {name}"
            )
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
            failures.append(f"changed path outside S1C boundary: {name}")
        try:
            text = (ROOT / name).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            failures.append(f"changed candidate is not readable UTF-8 text: {name}")
            continue
        failures.extend(scan_secrets(name, text))
        failures.extend(scan_production_python(name, text))
    if failures:
        print("S1C boundary and secret scan: FAIL")
        print("\n".join(sorted(set(failures))))
        return 1
    print(f"S1C boundary and secret scan: PASS ({len(names)} changed files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
