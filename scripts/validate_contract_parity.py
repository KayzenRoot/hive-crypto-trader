"""Compare the canonical OpenAPI S0A schemas with backend runtime schemas."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from pydantic import TypeAdapter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "apps" / "backend" / "src"))

from hct_backend.contracts import (
    AuditEnvelope,
    Environment,
    EnvironmentScopedId,
    ErrorEnvelope,
    EvidenceEnvelope,
    HealthResponse,
    IdentityKind,
    ReadinessResponse,
    StableId,
    VersionResponse,
)
from hct_backend.generated_contracts import SCHEMAS

RUNTIME_TYPES = {
    "Environment": TypeAdapter(Environment),
    "IdentityKind": TypeAdapter(IdentityKind),
    "StableId": TypeAdapter(StableId),
    "EnvironmentScopedId": TypeAdapter(EnvironmentScopedId),
    "HealthResponse": TypeAdapter(HealthResponse),
    "ReadinessResponse": TypeAdapter(ReadinessResponse),
    "VersionResponse": TypeAdapter(VersionResponse),
    "ErrorEnvelope": TypeAdapter(ErrorEnvelope),
    "AuditEnvelope": TypeAdapter(AuditEnvelope),
    "EvidenceEnvelope": TypeAdapter(EvidenceEnvelope),
}


def _resolve(schema: dict[str, Any], definitions: dict[str, Any]) -> dict[str, Any]:
    reference = schema.get("$ref")
    if not isinstance(reference, str):
        return schema
    name = reference.rsplit("/", 1)[-1]
    return definitions.get(name, schema)


def _fingerprint(schema: dict[str, Any], definitions: dict[str, Any]) -> Any:
    schema = _resolve(schema, definitions)
    if "anyOf" in schema:
        return ("union", tuple(sorted(_fingerprint(item, definitions) for item in schema["anyOf"])))
    schema_type = schema.get("type")
    if isinstance(schema_type, list):
        return ("union", tuple(sorted((str(item),) for item in schema_type)))
    if schema_type == "object":
        properties = schema.get("properties", {})
        additional = schema.get("additionalProperties", True)
        additional_fingerprint = (
            _fingerprint(additional, definitions) if isinstance(additional, dict) else additional
        )
        return (
            "object",
            tuple(sorted(schema.get("required", []))),
            additional_fingerprint,
            tuple(
                sorted(
                    (name, _fingerprint(property_schema, definitions))
                    for name, property_schema in properties.items()
                )
            ),
        )
    if schema_type == "string":
        return (
            "string",
            tuple(schema.get("enum", [])),
            schema.get("const"),
            schema.get("minLength"),
            schema.get("maxLength"),
            schema.get("pattern"),
            schema.get("format"),
        )
    if schema_type == "null":
        return ("null",)
    return (schema_type, tuple(schema.get("enum", [])), schema.get("const"))


def main() -> int:
    failures: list[str] = []
    for name, adapter in RUNTIME_TYPES.items():
        runtime_schema = adapter.json_schema()
        canonical_schema = SCHEMAS[name]
        canonical_fingerprint = _fingerprint(canonical_schema, SCHEMAS)
        runtime_fingerprint = _fingerprint(runtime_schema, runtime_schema.get("$defs", {}))
        if canonical_fingerprint != runtime_fingerprint:
            failures.append(f"schema parity mismatch: {name}")

    if failures:
        print("contract schema parity: FAIL")
        print("\n".join(failures))
        return 1
    print(f"contract schema parity: PASS ({len(RUNTIME_TYPES)} schemas)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
