"""Static negative-capability scanner for the bounded S1F runtime surface."""

from __future__ import annotations

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "apps/backend/src/hct_backend"
S1F_FILES = tuple(sorted(SOURCE_ROOT.glob("s1f_*.py")))
ALLOWED_URLS = {"wss://contract.mexc.com/edge", "https://contract.mexc.com"}
ALLOWED_WS_INTENTS = {
    "sub.tickers",
    "sub.ticker",
    "sub.deal",
    "sub.depth",
    "sub.depth.full",
    "sub.kline",
}
ALLOWED_REST_PATHS = {
    "/api/v1/contract/depth/",
    "/api/v1/contract/depth_commits/",
    "/api/v1/contract/kline/",
}
FORBIDDEN_TEXT = (
    r"api\.mexc\.com",
    r"/api/v1/(?:private|order|orders|position|positions|account|balance|leverage|margin)",
    r"\b(?:accessKey|apiKey|secretKey|signature|signRequest|credential)\b",
    r"\b(?:postgres|sqlalchemy|psycopg|asyncpg|sqlite3)\b",
    r"\b(?:Risk|OMS|Execution|database|persistence|deployment|live[-_ ]trading)\b",
    r"\b(?:requests|urllib|aiohttp)\b",
    r"\bworkflow_dispatch\b",
)


def scan_text(path: Path, text: str) -> list[str]:
    failures: list[str] = []
    try:
        tree = ast.parse(text, filename=str(path))
    except SyntaxError as exc:
        return [f"{path}: syntax: {exc}"]
    for pattern in FORBIDDEN_TEXT:
        if re.search(pattern, text, flags=re.IGNORECASE):
            failures.append(f"{path}: forbidden capability pattern {pattern}")
    urls = set(re.findall(r"(?:wss?|https?)://[^\"'\s)]+", text))
    for url in urls:
        normalized = url.rstrip("/")
        if normalized not in ALLOWED_URLS and not normalized.startswith(
            "https://contract.mexc.com"
        ):
            failures.append(f"{path}: unapproved URL {url}")
    rest_literals = set(re.findall(r"['\"](/api/v1/contract/[^'\"]*)['\"]", text))
    for literal in rest_literals:
        if literal not in ALLOWED_REST_PATHS:
            failures.append(f"{path}: unauthorized MEXC REST path {literal}")
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if not isinstance(target, ast.Name):
            continue
        if target.id == "MEXC_PUBLIC_CHANNELS":
            try:
                channels = set(ast.literal_eval(node.value))
            except (ValueError, TypeError):
                channels = set()
            if channels != ALLOWED_WS_INTENTS:
                failures.append(f"{path}: public WS intent allowlist changed")
        if target.id in {
            "MEXC_REST_DEPTH",
            "MEXC_REST_DEPTH_COMMITS",
            "MEXC_REST_KLINE",
        }:
            try:
                value = ast.literal_eval(node.value)
            except (ValueError, TypeError):
                value = None
            if value not in ALLOWED_REST_PATHS:
                failures.append(
                    f"{path}: unauthorized REST family constant {target.id}"
                )
    if "async for" in text and "websocket" in text.lower():
        failures.append(
            f"{path}: infinite library-managed receive iterator is forbidden"
        )
    return failures


def main() -> int:
    if not S1F_FILES:
        raise SystemExit("no S1F source files found")
    failures: list[str] = []
    for path in S1F_FILES:
        failures.extend(scan_text(path, path.read_text(encoding="utf-8")))
    if failures:
        print("S1F boundary scan: FAIL")
        print("\n".join(failures))
        return 1
    print(f"S1F boundary scan: PASS ({len(S1F_FILES)} source files)")
    print(
        "Public MEXC URL/path allowlist, no credential/private/mutation surface, "
        "no generic escape hatch: PASS"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
