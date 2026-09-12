import { afterEach, describe, expect, it, vi } from "vitest";

import { ENVIRONMENTS } from "./generated/contracts";
import { fetchSafeBackendStatus, parseEnvironment } from "./status";

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

  it("rejects malformed backend status payloads", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(async (path: string) => ({
        ok: true,
        json: async () =>
          path === "/health"
            ? { service: "hct-backend", status: "ok", extra: true }
            : path === "/ready"
              ? {
                  service: "hct-backend",
                  status: "ready",
                  checks: { application: "ready" },
                }
              : {
                  service: "hct-backend",
                  release: { kind: "RELEASE", value: "s0a-foundation" },
                  contract_sha256: "a".repeat(64),
                },
      })),
    );
    await expect(fetchSafeBackendStatus()).rejects.toThrow(
      "invalid HealthResponse",
    );
  });

  it("rejects invalid identity and hash data from the backend", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(async (path: string) => ({
        ok: true,
        json: async () =>
          path === "/health"
            ? { service: "hct-backend", status: "ok" }
            : path === "/ready"
              ? {
                  service: "hct-backend",
                  status: "ready",
                  checks: { application: "ready" },
                }
              : {
                  service: "hct-backend",
                  release: { kind: "RELEASE", value: "not valid" },
                  contract_sha256: "not-a-hash",
                },
      })),
    );
    await expect(fetchSafeBackendStatus()).rejects.toThrow(
      "invalid VersionResponse",
    );
  });
});
