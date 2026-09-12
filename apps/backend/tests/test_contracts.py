from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from hct_backend.contracts import (
    AuditEnvelope,
    Environment,
    EnvironmentScopedId,
    ErrorCode,
    ErrorEnvelope,
    EvidenceEnvelope,
    IdentityKind,
    StableId,
    ensure_same_environment,
    parse_environment,
)
from hct_backend.main import app


def scoped(kind: IdentityKind, environment: Environment, value: str) -> EnvironmentScopedId:
    return EnvironmentScopedId(kind=kind, environment=environment, value=value)


def test_environment_values_are_distinct_and_exact() -> None:
    assert [item.value for item in Environment] == ["LIVE", "PAPER", "SHADOW", "REPLAY"]
    assert parse_environment("PAPER") is Environment.PAPER
    with pytest.raises(ValueError):
        parse_environment("paper")
    with pytest.raises(ValueError):
        parse_environment("UNKNOWN")


def test_typed_ids_fail_closed_and_round_trip() -> None:
    identity = EnvironmentScopedId.parse("AUDIT:SHADOW:incident-001")
    assert identity.kind is IdentityKind.AUDIT
    assert identity.environment is Environment.SHADOW
    assert identity.as_text() == "AUDIT:SHADOW:incident-001"
    with pytest.raises(ValueError):
        EnvironmentScopedId.parse("AUDIT:SHADOW")
    with pytest.raises(ValueError):
        EnvironmentScopedId.parse("AUDIT:UNKNOWN:incident-001")
    with pytest.raises(ValidationError):
        StableId(kind=IdentityKind.RELEASE, value="not valid")


def test_cross_environment_misuse_is_rejected() -> None:
    paper = scoped(IdentityKind.AUDIT, Environment.PAPER, "event-1")
    replay = scoped(IdentityKind.EVIDENCE, Environment.REPLAY, "evidence-1")
    assert ensure_same_environment(paper) is Environment.PAPER
    with pytest.raises(ValueError, match="cross-environment"):
        ensure_same_environment(paper, replay)


def test_envelopes_bind_environment_and_hashes() -> None:
    event_id = scoped(IdentityKind.AUDIT, Environment.REPLAY, "event-1")
    timestamp = datetime(2026, 9, 12, tzinfo=UTC)
    audit = AuditEnvelope(
        event_id=event_id,
        environment=Environment.REPLAY,
        event_type="FOUNDATION_CHECK",
        payload_hash="a" * 64,
        occurred_at=timestamp,
    )
    assert audit.event_id.environment is audit.environment
    with pytest.raises(ValidationError):
        AuditEnvelope(
            event_id=event_id,
            environment=Environment.PAPER,
            event_type="FOUNDATION_CHECK",
            payload_hash="a" * 64,
            occurred_at=timestamp,
        )
    with pytest.raises(ValidationError):
        EvidenceEnvelope(
            evidence_id=scoped(IdentityKind.EVIDENCE, Environment.REPLAY, "evidence-1"),
            environment=Environment.REPLAY,
            evidence_type="CHECK",
            payload_hash="invalid",
        )


def test_error_envelope_is_safe_and_typed() -> None:
    error = ErrorEnvelope(code=ErrorCode.INVALID_REQUEST, message="invalid input")
    assert error.code is ErrorCode.INVALID_REQUEST
    with pytest.raises(ValidationError):
        ErrorEnvelope(code="UNKNOWN", message="invalid input")


def test_safe_endpoints_are_deterministic() -> None:
    client = TestClient(app)
    assert client.get("/health").json() == {"service": "hct-backend", "status": "ok"}
    assert client.get("/ready").json() == {
        "service": "hct-backend",
        "status": "ready",
        "checks": {"application": "ready"},
    }
    version = client.get("/version")
    assert version.status_code == 200
    assert version.json()["service"] == "hct-backend"
    assert len(version.json()["contract_sha256"]) == 64


def test_runtime_routes_are_exactly_the_safe_allowlist() -> None:
    routes = {
        (route.path, tuple(sorted(route.methods or set())))
        for route in app.routes
        if hasattr(route, "methods")
    }
    assert routes == {
        ("/health", ("GET",)),
        ("/ready", ("GET",)),
        ("/version", ("GET",)),
    }
    client = TestClient(app)
    for path in ("/openapi.json", "/docs", "/redoc"):
        assert client.get(path).status_code == 404
