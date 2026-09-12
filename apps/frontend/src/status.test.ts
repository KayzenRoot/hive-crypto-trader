import { afterEach, describe, expect, it, vi } from "vitest";

import {
  ENVIRONMENTS,
  parseAuditEnvelope,
  parseEvidenceEnvelope,
} from "./generated/contracts";
import { fetchSafeBackendStatus, parseEnvironment } from "./status";

const validHealth = { service: "hct-backend", status: "ok" };
const validReadiness = {
  service: "hct-backend",
  status: "ready",
  checks: { application: "ready" },
};
const validVersion = {
  service: "hct-backend",
  release: { kind: "RELEASE", value: "s0a-foundation" },
  contract_sha256: "a".repeat(64),
};

function stubBackend(
  overrides: {
    health?: unknown;
    readiness?: unknown;
    version?: unknown;
  } = {},
  ok = true,
): void {
  const payloads: Record<string, unknown> = {
    "/health": overrides.health ?? validHealth,
    "/ready": overrides.readiness ?? validReadiness,
    "/version": overrides.version ?? validVersion,
  };
  vi.stubGlobal(
    "fetch",
    vi.fn(async (path: string) => ({
      ok,
      json: async () => payloads[path],
    })),
  );
}

afterEach(() => vi.restoreAllMocks());

describe("canonical environment namespace", () => {
  it("keeps all four environments distinct", () => {
    expect(ENVIRONMENTS).toEqual(["LIVE", "PAPER", "SHADOW", "REPLAY"]);
    expect(parseEnvironment("PAPER")).toBe("PAPER");
  });

  it("fails closed for unknown or coerced values", () => {
    expect(() => parseEnvironment("paper")).toThrow("unknown environment");
    expect(() => parseEnvironment("UNKNOWN")).toThrow("unknown environment");
    expect(() => parseEnvironment(null)).toThrow("unknown environment");
  });

  it("rejects a health payload with a missing required field", async () => {
    stubBackend({ health: { service: "hct-backend" } });
    await expect(fetchSafeBackendStatus()).rejects.toThrow(
      "invalid HealthResponse",
    );
  });

  it("rejects a health payload with the wrong service", async () => {
    stubBackend({ health: { service: "other-service", status: "ok" } });
    await expect(fetchSafeBackendStatus()).rejects.toThrow(
      "invalid HealthResponse",
    );
  });

  it("rejects a readiness payload with a missing object", async () => {
    stubBackend({ readiness: { service: "hct-backend", status: "ready" } });
    await expect(fetchSafeBackendStatus()).rejects.toThrow(
      "invalid ReadinessResponse",
    );
  });

  it("rejects a readiness payload with an invalid check value", async () => {
    stubBackend({
      readiness: {
        service: "hct-backend",
        status: "ready",
        checks: { application: "not-ready" },
      },
    });
    await expect(fetchSafeBackendStatus()).rejects.toThrow(
      "invalid ReadinessResponse",
    );
  });

  it("rejects a forbidden extra property", async () => {
    stubBackend({ health: { ...validHealth, extra: true } });
    await expect(fetchSafeBackendStatus()).rejects.toThrow(
      "invalid HealthResponse",
    );
  });

  it("rejects an invalid release identity value", async () => {
    stubBackend({
      version: {
        ...validVersion,
        release: { kind: "RELEASE", value: "not valid" },
      },
    });
    await expect(fetchSafeBackendStatus()).rejects.toThrow(
      "invalid VersionResponse",
    );
  });

  it("rejects an invalid version hash", async () => {
    stubBackend({
      version: { ...validVersion, contract_sha256: "not-a-hash" },
    });
    await expect(fetchSafeBackendStatus()).rejects.toThrow(
      "invalid VersionResponse",
    );
  });

  it("rejects the wrong primitive type for a nested object", async () => {
    stubBackend({
      version: { ...validVersion, release: "RELEASE:s0a-foundation" },
    });
    await expect(fetchSafeBackendStatus()).rejects.toThrow(
      "invalid VersionResponse",
    );
  });

  it("rejects a non-OK HTTP response", async () => {
    stubBackend({}, false);
    await expect(fetchSafeBackendStatus()).rejects.toThrow(
      "backend status unavailable",
    );
  });
});

describe("generated cross-field envelope invariants", () => {
  it("accepts same-environment audit and rejects a cross-environment audit", () => {
    const payload = {
      event_id: { kind: "AUDIT", environment: "PAPER", value: "event-1" },
      environment: "PAPER",
      event_type: "FOUNDATION_CHECK",
      payload_hash: "a".repeat(64),
      occurred_at: "2026-09-12T00:00:00Z",
    };
    expect(parseAuditEnvelope(payload)).toEqual(payload);
    expect(() =>
      parseAuditEnvelope({ ...payload, environment: "REPLAY" }),
    ).toThrow("cross-environment identity misuse");
  });

  it("accepts same-environment evidence and rejects cross-environment evidence", () => {
    const payload = {
      evidence_id: {
        kind: "EVIDENCE",
        environment: "SHADOW",
        value: "evidence-1",
      },
      environment: "SHADOW",
      evidence_type: "FOUNDATION_CHECK",
      payload_hash: "b".repeat(64),
    };
    expect(parseEvidenceEnvelope(payload)).toEqual(payload);
    expect(() =>
      parseEvidenceEnvelope({ ...payload, environment: "LIVE" }),
    ).toThrow("cross-environment identity misuse");
  });
});
