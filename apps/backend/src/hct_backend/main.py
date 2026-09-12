"""Safe S0A service endpoints; no exchange, database, or trading state."""

from fastapi import FastAPI

from hct_backend.contracts import HealthResponse, ReadinessResponse, VersionResponse

app = FastAPI(
    title="Hive Crypto Trader S0A Backend",
    version="0.1.0",
    docs_url=None,
    redoc_url=None,
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse()


@app.get("/ready", response_model=ReadinessResponse)
def readiness() -> ReadinessResponse:
    return ReadinessResponse()


@app.get("/version", response_model=VersionResponse)
def version() -> VersionResponse:
    return VersionResponse()
