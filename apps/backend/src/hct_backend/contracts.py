"""Fail-closed S0A contract primitives."""

from __future__ import annotations

import re
from datetime import datetime
from enum import StrEnum
from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from hct_backend.generated_contracts import (
    ENVIRONMENTS,
    EVENT_TYPE_PATTERN,
    HASH_PATTERN,
    ID_VALUE_PATTERN,
    IDENTITY_KINDS,
)


class Environment(StrEnum):
    LIVE = "LIVE"
    PAPER = "PAPER"
    SHADOW = "SHADOW"
    REPLAY = "REPLAY"


class IdentityKind(StrEnum):
    SERVICE = "SERVICE"
    RELEASE = "RELEASE"
    CONFIG = "CONFIG"
    AUDIT = "AUDIT"
    EVIDENCE = "EVIDENCE"


class ErrorCode(StrEnum):
    INVALID_REQUEST = "INVALID_REQUEST"
    NOT_READY = "NOT_READY"
    INTERNAL = "INTERNAL"


if tuple(item.value for item in Environment) != ENVIRONMENTS:
    raise RuntimeError("generated environment contract drift")
if tuple(item.value for item in IdentityKind) != IDENTITY_KINDS:
    raise RuntimeError("generated identity contract drift")


class StableId(BaseModel):
    """An immutable non-stateful identifier with an explicit domain kind."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    kind: IdentityKind
    value: str = Field(min_length=1, max_length=64, pattern=ID_VALUE_PATTERN)

    @classmethod
    def parse(cls, raw: str) -> Self:
        parts = raw.split(":")
        if len(parts) != 2:
            raise ValueError("stable ID must be KIND:VALUE")
        return cls(kind=IdentityKind(parts[0]), value=parts[1])

    def as_text(self) -> str:
        return f"{self.kind.value}:{self.value}"


class EnvironmentScopedId(BaseModel):
    """An immutable state identity that cannot silently cross environments."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    kind: IdentityKind
    environment: Environment
    value: str = Field(min_length=1, max_length=64, pattern=ID_VALUE_PATTERN)

    @classmethod
    def parse(cls, raw: str) -> Self:
        parts = raw.split(":")
        if len(parts) != 3:
            raise ValueError("environment-scoped ID must be KIND:ENVIRONMENT:VALUE")
        return cls(kind=IdentityKind(parts[0]), environment=Environment(parts[1]), value=parts[2])

    def as_text(self) -> str:
        return f"{self.kind.value}:{self.environment.value}:{self.value}"


def parse_environment(raw: str) -> Environment:
    """Parse only exact canonical enum values; no case or alias coercion."""

    return Environment(raw)


def ensure_same_environment(*identities: EnvironmentScopedId) -> Environment:
    if not identities:
        raise ValueError("at least one identity is required")
    environments = {identity.environment for identity in identities}
    if len(environments) != 1:
        raise ValueError("cross-environment identity misuse")
    return identities[0].environment


class ErrorEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    code: ErrorCode
    message: str = Field(min_length=1, max_length=256)
    request_id: str | None = Field(default=None, max_length=64)


class HealthResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    service: Literal["hct-backend"]
    status: Literal["ok"]


class ReadinessResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    service: Literal["hct-backend"]
    status: Literal["ready"]
    checks: dict[str, Literal["ready"]]


class VersionResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    service: Literal["hct-backend"]
    release: StableId
    contract_sha256: str = Field(pattern=HASH_PATTERN)


class AuditEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    event_id: EnvironmentScopedId
    environment: Environment
    event_type: str = Field(min_length=2, max_length=64, pattern=EVENT_TYPE_PATTERN)
    payload_hash: str = Field(pattern=HASH_PATTERN)
    occurred_at: datetime

    @model_validator(mode="after")
    def validate_environment(self) -> Self:
        validation_id = EnvironmentScopedId(
            kind=IdentityKind.AUDIT,
            environment=self.environment,
            value="validation",
        )
        ensure_same_environment(self.event_id, validation_id)
        return self


class EvidenceEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    evidence_id: EnvironmentScopedId
    environment: Environment
    evidence_type: str = Field(min_length=2, max_length=64, pattern=EVENT_TYPE_PATTERN)
    payload_hash: str = Field(pattern=HASH_PATTERN)

    @model_validator(mode="after")
    def validate_environment(self) -> Self:
        validation_id = EnvironmentScopedId(
            kind=IdentityKind.EVIDENCE,
            environment=self.environment,
            value="validation",
        )
        ensure_same_environment(self.evidence_id, validation_id)
        return self


if not re.fullmatch(ID_VALUE_PATTERN, "s0a-foundation"):
    raise RuntimeError("ID contract pattern is invalid")
