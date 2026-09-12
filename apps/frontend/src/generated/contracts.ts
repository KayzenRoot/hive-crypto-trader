// Generated from packages/contracts/openapi.json; do not edit.

export const CONTRACT_SHA256 = "43e98281de732e5c81ef9d8683a92cac369634a57032e2ced7682882568c88b6" as const;
export const ENVIRONMENTS = ["LIVE", "PAPER", "SHADOW", "REPLAY"] as const;
export type Environment = "LIVE" | "PAPER" | "SHADOW" | "REPLAY";
export const IDENTITY_KINDS = ["SERVICE", "RELEASE", "CONFIG", "AUDIT", "EVIDENCE"] as const;
export type IdentityKind = "SERVICE" | "RELEASE" | "CONFIG" | "AUDIT" | "EVIDENCE";
export const SAFE_ENDPOINTS = ["/health", "/ready", "/version"] as const;

export interface StableId { kind: IdentityKind; value: string }
export interface HealthResponse { service: "hct-backend"; status: "ok" }
export interface ReadinessResponse { service: "hct-backend"; status: "ready"; checks: Record<string, "ready"> }
export interface VersionResponse { service: "hct-backend"; release: StableId; contract_sha256: string }
