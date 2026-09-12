"""Generate the deliberately small cross-runtime S0A contract projections."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "packages" / "contracts" / "openapi.json"
PYTHON_OUTPUT = ROOT / "apps" / "backend" / "src" / "hct_backend" / "generated_contracts.py"
TYPESCRIPT_OUTPUT = ROOT / "apps" / "frontend" / "src" / "generated" / "contracts.ts"


def load_source() -> tuple[dict[str, Any], str]:
    raw = SOURCE.read_bytes()
    document = json.loads(raw)
    canonical = json.dumps(document, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return document, hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def generate(document: dict[str, Any], contract_hash: str) -> tuple[str, str]:
    schemas = document["components"]["schemas"]
    environments = schemas["Environment"]["enum"]
    identity_kinds = schemas["IdentityKind"]["enum"]
    paths = sorted(document["paths"])
    error_codes = schemas["ErrorEnvelope"]["properties"]["code"]["enum"]

    py = "\n".join(
        [
            '"""Generated from packages/contracts/openapi.json; do not edit."""',
            "",
            f'CONTRACT_SHA256 = "{contract_hash}"',
            f"ENVIRONMENTS = {tuple(environments)!r}",
            f"IDENTITY_KINDS = {tuple(identity_kinds)!r}",
            f"ERROR_CODES = {tuple(error_codes)!r}",
            f"SAFE_ENDPOINTS = {tuple(paths)!r}",
            'ID_VALUE_PATTERN = r"^[a-z0-9][a-z0-9._-]{0,63}$"',
            'EVENT_TYPE_PATTERN = r"^[A-Z][A-Z0-9_.-]{1,63}$"',
            'HASH_PATTERN = r"^[0-9a-f]{64}$"',
            "",
        ]
    )
    env_union = " | ".join(f'"{value}"' for value in environments)
    kind_union = " | ".join(f'"{value}"' for value in identity_kinds)
    ts = "\n".join(
        [
            "// Generated from packages/contracts/openapi.json; do not edit.",
            "",
            f'export const CONTRACT_SHA256 = "{contract_hash}" as const;',
            f"export const ENVIRONMENTS = {json.dumps(environments)} as const;",
            f"export type Environment = {env_union};",
            f"export const IDENTITY_KINDS = {json.dumps(identity_kinds)} as const;",
            f"export type IdentityKind = {kind_union};",
            f"export const SAFE_ENDPOINTS = {json.dumps(paths)} as const;",
            "",
            "export interface StableId { kind: IdentityKind; value: string }",
            "export interface HealthResponse { service: \"hct-backend\"; status: \"ok\" }",
            "export interface ReadinessResponse { service: \"hct-backend\"; status: \"ready\"; checks: Record<string, \"ready\"> }",
            "export interface VersionResponse { service: \"hct-backend\"; release: StableId; contract_sha256: string }",
            "",
        ]
    )
    return py, ts


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    document, contract_hash = load_source()
    python_text, typescript_text = generate(document, contract_hash)
    outputs = ((PYTHON_OUTPUT, python_text), (TYPESCRIPT_OUTPUT, typescript_text))
    mismatches = [path for path, content in outputs if not path.exists() or path.read_text(encoding="utf-8") != content]
    if args.check:
        if mismatches:
            for path in mismatches:
                print(f"contract drift: {path.relative_to(ROOT)}")
            return 1
        print("contract generation reproducibility: PASS")
        return 0
    for path, content in outputs:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
    print("generated contract projections")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
