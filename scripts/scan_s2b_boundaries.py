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
FORBIDDEN_FUNCTION_NAMES = (
    "_from_evaluator",
    "_from_material",
    "_mint",
    "_attach_attestation",
)
FORBIDDEN_EVALUATION_PARAMETERS = (
    "revision",
    "revisions",
    "predecessor_evidence_fingerprint",
    "predecessor_evidence_fingerprints",
    "material",
)
EVALUATION_FUNCTIONS = ("evaluate_pattern", "evaluate_patterns")
REQUIRED_MARKERS = (
    "OVER_CARDINALITY_WINDOW",
    "EXACT_CARDINALITY_OVER_CARDINALITY_WINDOW_INVALID",
    "PatternEvaluationState",
    "CANDLEBAR_OHLC_PLUS_EVALUATOR_ISSUED_FEATURE_SAMPLE",
    "UNIX_EPOCH_MULTIPLES",
    "(60, 1, _ALIGNMENT)",
    "(300, 1, _ALIGNMENT)",
    "(900, 1, _ALIGNMENT)",
    "S2B_CANONICAL_EVALUATION_BOUNDARY=max(window_end,knowledge_time)",
    "CLOSED_BAR_REQUIRED",
    "ZERO_RANGE_PRIMITIVE_UNKNOWN",
    "constituent_revisions",
    "_evidence_seal",
    "S2B_REVISION_CHAIN=NO_SKIP_NO_FORK_NO_OVERWRITE",
    "NO_FORK",
    "_CONSUMED_PREDECESSORS",
    "_consumption_key",
    "predecessor already authorized a different successor",
    "DOJI:r[0]<=SMALL_BODY_MAX",
    "LONG_BODY:r[0]>=LONG_BODY_MIN",
    "BULLISH_ENGULFING:close[0]<open[0]",
    "BEARISH_ENGULFING:close[0]>open[0]",
    "MORNING_STAR:close[0]<open[0]",
    "EVENING_STAR:close[0]>open[0]",
)
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


def _argument_names(node: ast.FunctionDef | ast.AsyncFunctionDef) -> set[str]:
    arguments = node.args
    names = {
        item.arg
        for item in (*arguments.posonlyargs, *arguments.args, *arguments.kwonlyargs)
    }
    if arguments.vararg is not None:
        names.add(arguments.vararg.arg)
    if arguments.kwarg is not None:
        names.add(arguments.kwarg.arg)
    return names


def _contract_violations(path: Path, tree: ast.AST) -> list[str]:
    """Reject a reintroduced arbitrary-material issuance or raw evaluator inputs."""

    failures: list[str] = []
    for node in tree.body:
        if (
            isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name.startswith(("_issue", "_from", "_mint"))
            and node.name != "_issue_pattern_evidence"
        ):
            failures.append(f"{path}: unexpected issuance helper {node.name}")
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if "material" in _argument_names(node):
                failures.append(f"{path}: {node.name} accepts caller material")
            if node.name in FORBIDDEN_FUNCTION_NAMES:
                failures.append(
                    f"{path}: arbitrary evidence issuance function {node.name}"
                )
            if node.name in EVALUATION_FUNCTIONS:
                forbidden = sorted(
                    _argument_names(node) & set(FORBIDDEN_EVALUATION_PARAMETERS)
                )
                if forbidden:
                    failures.append(
                        f"{path}: raw evaluator input(s) {forbidden} in {node.name}"
                    )
        if isinstance(node, ast.ClassDef) and node.name == "PatternEvidence":
            for item in node.body:
                if not isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    continue
                # ``__init__`` is the deliberately blocked constructor: it accepts
                # arbitrary arguments only in order to refuse them.
                if item.name == "__init__":
                    continue
                if item.args.kwarg is not None:
                    failures.append(
                        f"{path}: PatternEvidence.{item.name} accepts arbitrary material"
                    )
                if "material" in _argument_names(item):
                    failures.append(
                        f"{path}: PatternEvidence.{item.name} accepts material"
                    )
    return failures


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
    if path.name == "patterns.py":
        failures.extend(_contract_violations(path, tree))
        for marker in REQUIRED_MARKERS:
            if marker not in text:
                failures.append(f"{path}: missing corrected marker {marker}")
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
