"""Static negative-capability scan for the bounded S2B pattern surface."""

from __future__ import annotations

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = (
    ROOT / "apps/backend/src/hct_backend/patterns.py",
    ROOT / "apps/backend/src/hct_backend/pattern_engine.py",
    ROOT / "scripts/benchmark_s2b.py",
)
FORBIDDEN_IMPORTS = {
    "asyncio",
    "aiohttp",
    "httpx",
    "requests",
    "urllib",
    "socket",
    "websocket",
    "websockets",
    "subprocess",
    "sqlalchemy",
    "psycopg",
    "asyncpg",
}
FORBIDDEN_TEXT = (
    r"api\.mexc\.com",
    r"/api/v1/(?:private|order|orders|position|positions|account|balance|leverage|margin)",
    r"\b(?:accessKey|apiKey|secretKey|signature|signRequest|credential|private_key)\b",
    r"\b(?:database|persistence|deployment|production|real[-_ ]money|limited[-_ ]live)\b",
    r"\b(?:Risk|OMS|Execution|Brain|strategy|signal|order|position|balance|fill|regime|scanner)\b",
    r"\bworkflow_dispatch\b",
)
PATTERN_IDS = {
    "P-DC-001",
    "P-MB-001",
    "P-EC-001",
    "P-EC-002",
    "P-MS-001",
    "P-ES-001",
}
AUTHORIZED_FILES = {
    ".github/workflows/s2b-quality.yml",
    "apps/backend/src/hct_backend/patterns.py",
    "apps/backend/src/hct_backend/pattern_engine.py",
    "apps/backend/tests/test_patterns.py",
    "scripts/benchmark_s2b.py",
    "scripts/scan_s2b_boundaries.py",
    "evidence/HCT-IMP-0011-S2B-CONTEXT-LOCK.md",
    "evidence/HCT-IMP-0011-S2B.md",
}


def scan(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    failures: list[str] = []
    try:
        tree = ast.parse(text, filename=str(path))
    except SyntaxError as exc:
        return [f"{path}: syntax: {exc}"]
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules = (alias.name.split(".", 1)[0] for alias in node.names)
            failures.extend(
                f"{path}: forbidden import {module}"
                for module in modules
                if module in FORBIDDEN_IMPORTS
            )
        if isinstance(node, ast.ImportFrom) and node.module:
            module = node.module.split(".", 1)[0]
            if module in FORBIDDEN_IMPORTS:
                failures.append(f"{path}: forbidden import {module}")
    for pattern in FORBIDDEN_TEXT:
        if re.search(pattern, text, flags=re.IGNORECASE):
            failures.append(f"{path}: forbidden capability pattern {pattern}")
    urls = re.findall(r"(?:wss?|https?)://[^\"'\s)]+", text)
    failures.extend(f"{path}: unexpected URL {url}" for url in urls)
    return failures


def main() -> int:
    failures = [
        f"missing bounded source: {path}" for path in SOURCES if not path.is_file()
    ]
    for path in SOURCES:
        if path.is_file():
            failures.extend(scan(path))
    source_text = (ROOT / "apps/backend/src/hct_backend/patterns.py").read_text(
        encoding="utf-8"
    )
    for identifier in PATTERN_IDS:
        if source_text.count(identifier) < 1:
            failures.append(f"patterns.py: missing exact pattern {identifier}")
    if "EXCLUDED_FROM_V1_MINIMUM" in source_text:
        failures.append("patterns.py: chart-structure exclusion marker must not appear")
    workflow = ROOT / ".github/workflows/s2b-quality.yml"
    if workflow.exists() and "workflow_dispatch" in workflow.read_text(
        encoding="utf-8"
    ):
        failures.append("s2b-quality.yml: manual dispatch is forbidden")
    if failures:
        print("S2B negative-capability scan: FAIL")
        print("\n".join(failures))
        return 1
    print("S2B negative-capability scan: PASS")
    print(
        "No transport, credential, persistence, downstream-action or live-capability surface: PASS"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
