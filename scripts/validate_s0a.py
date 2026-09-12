"""Read-only S0A compatibility boundary checks used locally and in CI."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from generate_contracts import ROOT, generate, load_source

sys.path.insert(0, str(ROOT / "apps" / "backend" / "src"))
from hct_backend.main import app

SOURCE_ROOTS = (ROOT / "apps", ROOT / "packages", ROOT / "scripts")
S0B_BOUNDARY_PATHS = {
    ROOT / "apps" / "backend" / "src" / "hct_backend" / "security.py",
    ROOT / "apps" / "backend" / "tests" / "test_security.py",
    ROOT / "scripts" / "scan_s0b_boundaries.py",
}
FORBIDDEN_SOURCE_MARKERS = (
    "mexc",
    "websocket",
    "api_key",
    "secretstore",
    "signing",
    "create_order",
    "/orders",
    "positions",
    "balances",
    "leverage",
)
def candidate_files() -> list[Path]:
    ignored = {"node_modules", ".venv", ".tooling", "dist", "__pycache__", ".mypy_cache", ".pytest_cache"}
    return [
        path
        for root in SOURCE_ROOTS
        for path in root.rglob("*")
        if path.is_file()
        and path.name != "validate_s0a.py"
        and path not in S0B_BOUNDARY_PATHS
        and path.name not in {"uv.lock", "package-lock.json"}
        and not ignored.intersection(path.parts)
    ]


def main() -> int:
    failures: list[str] = []
    document, contract_hash = load_source()
    python_text, typescript_text = generate(document, contract_hash)
    generated = (
        ROOT / "apps" / "backend" / "src" / "hct_backend" / "generated_contracts.py",
        ROOT / "apps" / "frontend" / "src" / "generated" / "contracts.ts",
    )
    expected = (python_text, typescript_text)
    for path, content in zip(generated, expected):
        if not path.exists() or path.read_text(encoding="utf-8") != content:
            failures.append(f"generated contract drift: {path.relative_to(ROOT)}")

    if tuple(document["components"]["schemas"]["Environment"]["enum"]) != (
        "LIVE",
        "PAPER",
        "SHADOW",
        "REPLAY",
    ):
        failures.append("environment namespace drift")
    if sorted(document["paths"]) != ["/health", "/ready", "/version"]:
        failures.append("unsafe endpoint added to canonical contract")

    runtime_routes = {
        (route.path, tuple(sorted(route.methods or set())))
        for route in app.routes
        if hasattr(route, "methods")
    }
    if runtime_routes != {
        ("/health", ("GET",)),
        ("/ready", ("GET",)),
        ("/version", ("GET",)),
    }:
        failures.append(f"runtime route allowlist drift: {sorted(runtime_routes)!r}")

    for path in candidate_files():
        text = path.read_text(encoding="utf-8", errors="replace")
        lowered = text.lower()
        for marker in FORBIDDEN_SOURCE_MARKERS:
            if marker in lowered:
                failures.append(f"unauthorized marker {marker!r}: {path.relative_to(ROOT)}")
        if re.search(r"https?://", text, re.IGNORECASE):
            failures.append(f"external URL in implementation source: {path.relative_to(ROOT)}")

    for path in (ROOT / "apps" / "backend" / "uv.lock", ROOT / "apps" / "frontend" / "package-lock.json"):
        if not path.exists():
            failures.append(f"missing lockfile: {path.relative_to(ROOT)}")

    if failures:
        print("S0A boundary validation: FAIL")
        print("\n".join(failures))
        return 1
    print("S0A boundary validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
