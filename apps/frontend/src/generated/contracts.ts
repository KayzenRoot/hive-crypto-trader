// Generated from packages/contracts/openapi.json; do not edit.

export const CONTRACT_SHA256 = "f5a8f8077d26b733db5f227f62757bad0d3c298d719dfc0d9aac18233baa569b" as const;
export const CANONICAL_SCHEMAS = {"AuditEnvelope": {"additionalProperties": false, "properties": {"environment": {"$ref": "#/components/schemas/Environment"}, "event_id": {"$ref": "#/components/schemas/EnvironmentScopedId"}, "event_type": {"maxLength": 64, "minLength": 2, "pattern": "^[A-Z][A-Z0-9_.-]{1,63}$", "type": "string"}, "occurred_at": {"format": "date-time", "type": "string"}, "payload_hash": {"pattern": "^[0-9a-f]{64}$", "type": "string"}}, "required": ["event_id", "environment", "event_type", "payload_hash", "occurred_at"], "type": "object"}, "Environment": {"enum": ["LIVE", "PAPER", "SHADOW", "REPLAY"], "type": "string"}, "EnvironmentScopedId": {"additionalProperties": false, "properties": {"environment": {"$ref": "#/components/schemas/Environment"}, "kind": {"$ref": "#/components/schemas/IdentityKind"}, "value": {"maxLength": 64, "minLength": 1, "pattern": "^[a-z0-9][a-z0-9._-]{0,63}$", "type": "string"}}, "required": ["kind", "environment", "value"], "type": "object"}, "ErrorEnvelope": {"additionalProperties": false, "properties": {"code": {"enum": ["INVALID_REQUEST", "NOT_READY", "INTERNAL"], "type": "string"}, "message": {"maxLength": 256, "minLength": 1, "type": "string"}, "request_id": {"anyOf": [{"maxLength": 64, "type": "string"}, {"type": "null"}]}}, "required": ["code", "message"], "type": "object"}, "EvidenceEnvelope": {"additionalProperties": false, "properties": {"environment": {"$ref": "#/components/schemas/Environment"}, "evidence_id": {"$ref": "#/components/schemas/EnvironmentScopedId"}, "evidence_type": {"maxLength": 64, "minLength": 2, "pattern": "^[A-Z][A-Z0-9_.-]{1,63}$", "type": "string"}, "payload_hash": {"pattern": "^[0-9a-f]{64}$", "type": "string"}}, "required": ["evidence_id", "environment", "evidence_type", "payload_hash"], "type": "object"}, "HealthResponse": {"additionalProperties": false, "properties": {"service": {"const": "hct-backend", "type": "string"}, "status": {"const": "ok", "type": "string"}}, "required": ["service", "status"], "type": "object"}, "IdentityKind": {"enum": ["SERVICE", "RELEASE", "CONFIG", "AUDIT", "EVIDENCE", "EXCHANGE", "INSTRUMENT", "CAPABILITY_SNAPSHOT", "REFERENCE_SNAPSHOT", "UNIVERSE_SNAPSHOT"], "type": "string"}, "ReadinessResponse": {"additionalProperties": false, "properties": {"checks": {"additionalProperties": {"const": "ready", "type": "string"}, "type": "object"}, "service": {"const": "hct-backend", "type": "string"}, "status": {"const": "ready", "type": "string"}}, "required": ["service", "status", "checks"], "type": "object"}, "StableId": {"additionalProperties": false, "properties": {"kind": {"$ref": "#/components/schemas/IdentityKind"}, "value": {"maxLength": 64, "minLength": 1, "pattern": "^[a-z0-9][a-z0-9._-]{0,63}$", "type": "string"}}, "required": ["kind", "value"], "type": "object"}, "VersionResponse": {"additionalProperties": false, "properties": {"contract_sha256": {"pattern": "^[0-9a-f]{64}$", "type": "string"}, "release": {"$ref": "#/components/schemas/StableId"}, "service": {"const": "hct-backend", "type": "string"}}, "required": ["service", "release", "contract_sha256"], "type": "object"}} as const;
export const ENVIRONMENTS = ["LIVE", "PAPER", "SHADOW", "REPLAY"] as const;
export type Environment = "LIVE" | "PAPER" | "SHADOW" | "REPLAY";
export const IDENTITY_KINDS = ["SERVICE", "RELEASE", "CONFIG", "AUDIT", "EVIDENCE", "EXCHANGE", "INSTRUMENT", "CAPABILITY_SNAPSHOT", "REFERENCE_SNAPSHOT", "UNIVERSE_SNAPSHOT"] as const;
export type IdentityKind = "SERVICE" | "RELEASE" | "CONFIG" | "AUDIT" | "EVIDENCE" | "EXCHANGE" | "INSTRUMENT" | "CAPABILITY_SNAPSHOT" | "REFERENCE_SNAPSHOT" | "UNIVERSE_SNAPSHOT";
export const SAFE_ENDPOINTS = ["/health", "/ready", "/version"] as const;

export interface StableId { kind: IdentityKind; value: string }
export interface EnvironmentScopedId { kind: IdentityKind; environment: Environment; value: string }
export interface HealthResponse { service: "hct-backend"; status: "ok" }
export interface ReadinessResponse { service: "hct-backend"; status: "ready"; checks: Record<string, "ready"> }
export interface VersionResponse { service: "hct-backend"; release: StableId; contract_sha256: string }
export type ErrorCode = "INVALID_REQUEST" | "NOT_READY" | "INTERNAL";
export interface ErrorEnvelope { code: ErrorCode; message: string; request_id?: string | null }
export interface AuditEnvelope { event_id: EnvironmentScopedId; environment: Environment; event_type: string; payload_hash: string; occurred_at: string }
export interface EvidenceEnvelope { evidence_id: EnvironmentScopedId; environment: Environment; evidence_type: string; payload_hash: string }

type Schema = Record<string, unknown>;
type RecordValue = Record<string, unknown>;

function isRecord(value: unknown): value is RecordValue {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function schemaFor(ref: string): Schema {
  const name = ref.split("/").at(-1);
  if (!name || !(name in CANONICAL_SCHEMAS)) throw new Error("unknown schema reference");
  return CANONICAL_SCHEMAS[name as keyof typeof CANONICAL_SCHEMAS] as Schema;
}

function validateNode(schema: Schema, value: unknown): boolean {
  if (typeof schema.$ref === "string") return validateNode(schemaFor(schema.$ref), value);
  if (Array.isArray(schema.anyOf)) return schema.anyOf.some((item) => validateNode(item as Schema, value));
  if ("const" in schema && value !== schema.const) return false;
  if (Array.isArray(schema.enum) && !schema.enum.includes(value)) return false;
  if (Array.isArray(schema.type)) return schema.type.some((kind) => validateNode({ ...schema, type: kind }, value));
  if (schema.type === "null") return value === null;
  if (schema.type === "string") {
    if (typeof value !== "string") return false;
    if (typeof schema.minLength === "number" && value.length < schema.minLength) return false;
    if (typeof schema.maxLength === "number" && value.length > schema.maxLength) return false;
    if (typeof schema.pattern === "string" && !new RegExp(schema.pattern).test(value)) return false;
    if (schema.format === "date-time" && Number.isNaN(Date.parse(value))) return false;
    return true;
  }
  if (schema.type === "object") {
    if (!isRecord(value)) return false;
    const properties = (schema.properties ?? {}) as RecordValue;
    const required = Array.isArray(schema.required) ? schema.required : [];
    if (required.some((key) => typeof key !== "string" || !(key in value))) return false;
    if (schema.additionalProperties === false && Object.keys(value).some((key) => !(key in properties))) return false;
    for (const [key, property] of Object.entries(properties)) {
      if (key in value && !validateNode(property as Schema, value[key])) return false;
    }
    if (isRecord(schema.additionalProperties)) {
      for (const [key, item] of Object.entries(value)) if (!(key in properties) && !validateNode(schema.additionalProperties, item)) return false;
    }
    return true;
  }
  return false;
}

function parseSchema<T>(name: string, value: unknown): T {
  if (!validateNode(schemaFor(`#/components/schemas/${name}`), value)) throw new Error(`invalid ${name}`);
  return value as T;
}

export function parseEnvironment(value: unknown): Environment { return parseSchema<Environment>("Environment", value); }
export function parseStableId(value: unknown): StableId { return parseSchema<StableId>("StableId", value); }
export function parseEnvironmentScopedId(value: unknown): EnvironmentScopedId { return parseSchema<EnvironmentScopedId>("EnvironmentScopedId", value); }
export function parseHealthResponse(value: unknown): HealthResponse { return parseSchema<HealthResponse>("HealthResponse", value); }
export function parseReadinessResponse(value: unknown): ReadinessResponse { return parseSchema<ReadinessResponse>("ReadinessResponse", value); }
export function parseVersionResponse(value: unknown): VersionResponse { return parseSchema<VersionResponse>("VersionResponse", value); }
export function parseErrorEnvelope(value: unknown): ErrorEnvelope { return parseSchema<ErrorEnvelope>("ErrorEnvelope", value); }
export function parseAuditEnvelope(value: unknown): AuditEnvelope {
  const parsed = parseSchema<AuditEnvelope>("AuditEnvelope", value);
  if (parsed.event_id.environment !== parsed.environment) throw new Error("cross-environment identity misuse");
  return parsed;
}
export function parseEvidenceEnvelope(value: unknown): EvidenceEnvelope {
  const parsed = parseSchema<EvidenceEnvelope>("EvidenceEnvelope", value);
  if (parsed.evidence_id.environment !== parsed.environment) throw new Error("cross-environment identity misuse");
  return parsed;
}
