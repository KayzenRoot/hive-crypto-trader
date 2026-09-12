import { describe, expect, it } from "vitest";

import { ENVIRONMENTS } from "./generated/contracts";
import { parseEnvironment } from "./status";

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
});
