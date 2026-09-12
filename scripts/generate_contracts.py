"""Generate deterministic cross-runtime S0A contract projections."""

from __future__ import annotations

import argparse
import hashlib
import json
import pprint
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
    schema_literal = pprint.pformat(schemas, sort_dicts=True, width=72)

    py = "\n".join(
        [
            '"""Generated from packages/contracts/openapi.json; do not edit."""',
            "# ruff: noqa: E501",
            "",
            f'CONTRACT_SHA256 = "{contract_hash}"',
            f"SCHEMAS = {schema_literal}",
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
            f"export const CANONICAL_SCHEMAS = {json.dumps(schemas, ensure_ascii=False, sort_keys=True)} as const;",
            f"export const ENVIRONMENTS = {json.dumps(environments)} as const;",
            f"export type Environment = {env_union};",
            f"export const IDENTITY_KINDS = {json.dumps(identity_kinds)} as const;",
            f"export type IdentityKind = {kind_union};",
            f"export const SAFE_ENDPOINTS = {json.dumps(paths)} as const;",
            "",
            "export interface StableId { kind: IdentityKind; value: string }",
            "export interface EnvironmentScopedId { kind: IdentityKind; environment: Environment; value: string }",
            "export interface HealthResponse { service: \"hct-backend\"; status: \"ok\" }",
            "export interface ReadinessResponse { service: \"hct-backend\"; status: \"ready\"; checks: Record<string, \"ready\"> }",
            "export interface VersionResponse { service: \"hct-backend\"; release: StableId; contract_sha256: string }",
            'export type ErrorCode = "INVALID_REQUEST" | "NOT_READY" | "INTERNAL";',
            "export interface ErrorEnvelope { code: ErrorCode; message: string; request_id?: string | null }",
            "export interface AuditEnvelope { event_id: EnvironmentScopedId; environment: Environment; event_type: string; payload_hash: string; occurred_at: string }",
            "export interface EvidenceEnvelope { evidence_id: EnvironmentScopedId; environment: Environment; evidence_type: string; payload_hash: string }",
            "",
            "type Schema = Record<string, unknown>;",
            "type RecordValue = Record<string, unknown>;",
            "",
            "function isRecord(value: unknown): value is RecordValue {",
            '  return typeof value === "object" && value !== null && !Array.isArray(value);',
            "}",
            "",
            "function schemaFor(ref: string): Schema {",
            '  const name = ref.split("/").at(-1);',
            '  if (!name || !(name in CANONICAL_SCHEMAS)) throw new Error("unknown schema reference");',
            "  return CANONICAL_SCHEMAS[name as keyof typeof CANONICAL_SCHEMAS] as Schema;",
            "}",
            "",
            "function validateNode(schema: Schema, value: unknown): boolean {",
            '  if (typeof schema.$ref === "string") return validateNode(schemaFor(schema.$ref), value);',
            '  if (Array.isArray(schema.anyOf)) return schema.anyOf.some((item) => validateNode(item as Schema, value));',
            '  if ("const" in schema && value !== schema.const) return false;',
            "  if (Array.isArray(schema.enum) && !schema.enum.includes(value)) return false;",
            '  if (Array.isArray(schema.type)) return schema.type.some((kind) => validateNode({ ...schema, type: kind }, value));',
            '  if (schema.type === "null") return value === null;',
            '  if (schema.type === "string") {',
            '    if (typeof value !== "string") return false;',
            '    if (typeof schema.minLength === "number" && value.length < schema.minLength) return false;',
            '    if (typeof schema.maxLength === "number" && value.length > schema.maxLength) return false;',
            '    if (typeof schema.pattern === "string" && !new RegExp(schema.pattern).test(value)) return false;',
            '    if (schema.format === "date-time" && Number.isNaN(Date.parse(value))) return false;',
            "    return true;",
            "  }",
            '  if (schema.type === "object") {',
            '    if (!isRecord(value)) return false;',
            '    const properties = (schema.properties ?? {}) as RecordValue;',
            '    const required = Array.isArray(schema.required) ? schema.required : [];',
            '    if (required.some((key) => typeof key !== "string" || !(key in value))) return false;',
            '    if (schema.additionalProperties === false && Object.keys(value).some((key) => !(key in properties))) return false;',
            '    for (const [key, property] of Object.entries(properties)) {',
            '      if (key in value && !validateNode(property as Schema, value[key])) return false;',
            "    }",
            '    if (isRecord(schema.additionalProperties)) {',
            '      for (const [key, item] of Object.entries(value)) if (!(key in properties) && !validateNode(schema.additionalProperties, item)) return false;',
            "    }",
            "    return true;",
            "  }",
            "  return false;",
            "}",
            "",
            "function parseSchema<T>(name: string, value: unknown): T {",
            '  if (!validateNode(schemaFor(`#/components/schemas/${name}`), value)) throw new Error(`invalid ${name}`);',
            "  return value as T;",
            "}",
            "",
            'export function parseEnvironment(value: unknown): Environment { return parseSchema<Environment>("Environment", value); }',
            'export function parseStableId(value: unknown): StableId { return parseSchema<StableId>("StableId", value); }',
            'export function parseEnvironmentScopedId(value: unknown): EnvironmentScopedId { return parseSchema<EnvironmentScopedId>("EnvironmentScopedId", value); }',
            'export function parseHealthResponse(value: unknown): HealthResponse { return parseSchema<HealthResponse>("HealthResponse", value); }',
            'export function parseReadinessResponse(value: unknown): ReadinessResponse { return parseSchema<ReadinessResponse>("ReadinessResponse", value); }',
            'export function parseVersionResponse(value: unknown): VersionResponse { return parseSchema<VersionResponse>("VersionResponse", value); }',
            'export function parseErrorEnvelope(value: unknown): ErrorEnvelope { return parseSchema<ErrorEnvelope>("ErrorEnvelope", value); }',
            "export function parseAuditEnvelope(value: unknown): AuditEnvelope {",
            '  const parsed = parseSchema<AuditEnvelope>("AuditEnvelope", value);',
            '  if (parsed.event_id.environment !== parsed.environment) throw new Error("cross-environment identity misuse");',
            "  return parsed;",
            "}",
            "export function parseEvidenceEnvelope(value: unknown): EvidenceEnvelope {",
            '  const parsed = parseSchema<EvidenceEnvelope>("EvidenceEnvelope", value);',
            '  if (parsed.evidence_id.environment !== parsed.environment) throw new Error("cross-environment identity misuse");',
            "  return parsed;",
            "}",
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
