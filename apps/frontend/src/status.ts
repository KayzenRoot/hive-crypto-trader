import {
  ENVIRONMENTS,
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
  if (
    typeof value !== "string" ||
    !ENVIRONMENTS.includes(value as Environment)
  ) {
    throw new Error("unknown environment");
  }
  return value as Environment;
}

export async function fetchSafeBackendStatus(): Promise<SafeBackendStatus> {
  const [healthResponse, readinessResponse, versionResponse] =
    await Promise.all([fetch("/health"), fetch("/ready"), fetch("/version")]);
  if (!healthResponse.ok || !readinessResponse.ok || !versionResponse.ok) {
    throw new Error("backend status unavailable");
  }
  return {
    health: (await healthResponse.json()) as HealthResponse,
    readiness: (await readinessResponse.json()) as ReadinessResponse,
    version: (await versionResponse.json()) as VersionResponse,
  };
}
