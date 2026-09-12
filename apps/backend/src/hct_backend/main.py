"""Safe S0A service endpoints; no exchange, database, or trading state."""

from fastapi import FastAPI

from hct_backend.contracts import (
    HealthResponse,
    IdentityKind,
    ReadinessResponse,
    StableId,
    VersionResponse,
)
from hct_backend.generated_contracts import CONTRACT_SHA256

app = FastAPI(
    title="Hive Crypto Trader S0A Backend",
    version="0.1.0",
    openapi_url=None,
    docs_url=None,
    redoc_url=None,
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(service="hct-backend", status="ok")


@app.get("/ready", response_model=ReadinessResponse)
def readiness() -> ReadinessResponse:
    return ReadinessResponse(service="hct-backend", status="ready", checks={"application": "ready"})


@app.get("/version", response_model=VersionResponse)
def version() -> VersionResponse:
    return VersionResponse(
        service="hct-backend",
        release=StableId(kind=IdentityKind.RELEASE, value="s0a-foundation"),
        contract_sha256=CONTRACT_SHA256,
    )
