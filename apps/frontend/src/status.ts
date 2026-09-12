import {
  parseEnvironment as parseCanonicalEnvironment,
  parseHealthResponse,
  parseReadinessResponse,
  parseVersionResponse,
  type Environment,
  type HealthResponse,
  type ReadinessResponse,
  type VersionResponse,
} from "./generated/contracts";

export interface SafeBackendStatus {
  health: HealthResponse;
  readiness: ReadinessResponse;
  version: VersionResponse;
}

export function parseEnvironment(value: unknown): Environment {
  try {
    return parseCanonicalEnvironment(value);
  } catch {
    throw new Error("unknown environment");
  }
}

export async function fetchSafeBackendStatus(): Promise<SafeBackendStatus> {
  const [healthResponse, readinessResponse, versionResponse] =
    await Promise.all([fetch("/health"), fetch("/ready"), fetch("/version")]);
  if (!healthResponse.ok || !readinessResponse.ok || !versionResponse.ok) {
    throw new Error("backend status unavailable");
  }
  return {
    health: parseHealthResponse(await healthResponse.json()),
    readiness: parseReadinessResponse(await readinessResponse.json()),
    version: parseVersionResponse(await versionResponse.json()),
  };
}
