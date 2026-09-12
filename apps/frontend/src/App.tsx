import { useEffect, useState } from "react";

import type { SafeBackendStatus } from "./status";
import { fetchSafeBackendStatus } from "./status";
import "./styles.css";

export function App() {
  const [status, setStatus] = useState<SafeBackendStatus | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    void fetchSafeBackendStatus()
      .then(setStatus)
      .catch(() =>
        setError(
          "Backend status is unavailable. This UI has no authority to act.",
        ),
      );
  }, []);

  return (
    <main className="shell">
      <header>
        <p className="eyebrow">HIVE CRYPTO TRADER · S0A</p>
        <h1>Runtime status</h1>
        <p className="lede">A read-only projection of safe service metadata.</p>
      </header>
      <section className="status-card" aria-live="polite">
        <div className="status-row">
          <span>Backend liveness</span>
          <strong>
            {status?.health.status ?? (error ? "unavailable" : "checking")}
          </strong>
        </div>
        <div className="status-row">
          <span>Backend readiness</span>
          <strong>
            {status?.readiness.status ?? (error ? "unavailable" : "checking")}
          </strong>
        </div>
        <div className="status-row">
          <span>Release</span>
          <strong>
            {status
              ? `${status.version.release.kind}:${status.version.release.value}`
              : "-"}
          </strong>
        </div>
      </section>
      <p className="boundary">
        {error ??
          "No trading actions, exchange controls, credentials, or risk authority are exposed here."}
      </p>
    </main>
  );
}
