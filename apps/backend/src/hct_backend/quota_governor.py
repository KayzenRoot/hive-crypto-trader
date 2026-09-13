"""Provider-neutral quota, generation and backpressure control decisions."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field, replace
from enum import StrEnum

from hct_backend.contracts import IdentityKind, StableId

_TOKEN_PATTERN = re.compile(r"^[A-Za-z0-9._:/-]{1,128}$")


class GovernorError(ValueError):
    """Base error for fail-closed governor validation."""


class GovernorInputError(GovernorError):
    """Raised when typed control evidence is missing or malformed."""


class GovernorConsistencyError(GovernorError):
    """Raised when immutable control evidence is contradictory."""


class QuotaKind(StrEnum):
    """Independent request and subscription budget domains."""

    REQUEST = "REQUEST"
    SUBSCRIPTION = "SUBSCRIPTION"


class PriorityClass(StrEnum):
    """Finite deterministic priority classes; lower rank is more protected."""

    PROTECTION = "PROTECTION"
    RECONCILIATION = "RECONCILIATION"
    NORMAL = "NORMAL"
    RESEARCH = "RESEARCH"

    @property
    def rank(self) -> int:
        return {
            PriorityClass.PROTECTION: 0,
            PriorityClass.RECONCILIATION: 1,
            PriorityClass.NORMAL: 2,
            PriorityClass.RESEARCH: 3,
        }[self]

    @property
    def may_use_protected_reserve(self) -> bool:
        return self.rank <= PriorityClass.RECONCILIATION.rank


class AdmissionOutcome(StrEnum):
    """Finite decision result; none of these outcomes performs I/O."""

    ADMIT = "ADMIT"
    DEFER = "DEFER"
    SHED = "SHED"
    CIRCUIT_OPEN = "CIRCUIT_OPEN"
    UNKNOWN = "UNKNOWN"


class AdmissionReason(StrEnum):
    """Finite deterministic reason taxonomy for admission decisions."""

    ADMITTED = "ADMITTED"
    UNKNOWN_BUDGET = "UNKNOWN_BUDGET"
    STALE_GENERATION = "STALE_GENERATION"
    RETRY_EXHAUSTED = "RETRY_EXHAUSTED"
    CIRCUIT_OPEN = "CIRCUIT_OPEN"
    PROBE_IN_FLIGHT = "PROBE_IN_FLIGHT"
    QUEUE_FULL = "QUEUE_FULL"
    PROTECTED_RESERVE = "PROTECTED_RESERVE"
    BUDGET_EXHAUSTED = "BUDGET_EXHAUSTED"


class CircuitState(StrEnum):
    """Pure circuit state machine states."""

    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class IntentState(StrEnum):
    """Planning state for a non-executable subscription intent."""

    REQUESTED = "REQUESTED"
    ACCEPTED = "ACCEPTED"
    DEFERRED = "DEFERRED"


def _positive(value: int, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise GovernorInputError(f"{label} must be a positive integer")
    return value


def _non_negative(value: int, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise GovernorInputError(f"{label} must be a non-negative integer")
    return value


def _text(value: str, label: str) -> str:
    if not isinstance(value, str) or not value or not _TOKEN_PATTERN.fullmatch(value):
        raise GovernorInputError(f"{label} must be a bounded canonical token")
    return value


def _hash(value: object) -> str:
    encoded = json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class BudgetLimit:
    """A typed limit; ``None`` capacity is explicit unknown evidence."""

    capacity: int | None
    replenishment: int | None = None

    def __post_init__(self) -> None:
        if self.capacity is not None:
            _positive(self.capacity, "capacity")
        if self.replenishment is not None:
            _positive(self.replenishment, "replenishment")
        if self.capacity is None and self.replenishment is not None:
            raise GovernorConsistencyError("unknown capacity cannot carry permissive replenishment")

    @property
    def known(self) -> bool:
        return self.capacity is not None


@dataclass(frozen=True, slots=True)
class BudgetPolicySnapshot:
    """Immutable versioned request/subscription policy material."""

    policy_version: int
    source: str
    window_ms: int
    request_limit: BudgetLimit
    subscription_limit: BudgetLimit
    protected_reserve: int = 0

    def __post_init__(self) -> None:
        _positive(self.policy_version, "policy version")
        _text(self.source, "policy source")
        _positive(self.window_ms, "window")
        _non_negative(self.protected_reserve, "protected reserve")
        for label, limit in (
            ("request", self.request_limit),
            ("subscription", self.subscription_limit),
        ):
            if limit.capacity is not None and self.protected_reserve > limit.capacity:
                raise GovernorConsistencyError(f"protected reserve exceeds {label} capacity")

    def _material(self) -> dict[str, object]:
        return {
            "policy_version": self.policy_version,
            "source": self.source,
            "window_ms": self.window_ms,
            "request": {
                "capacity": self.request_limit.capacity,
                "replenishment": self.request_limit.replenishment,
            },
            "subscription": {
                "capacity": self.subscription_limit.capacity,
                "replenishment": self.subscription_limit.replenishment,
            },
            "protected_reserve": self.protected_reserve,
        }

    @property
    def fingerprint(self) -> str:
        return _hash(self._material())


@dataclass(frozen=True, slots=True)
class BudgetSnapshot:
    """Immutable remaining-capacity evidence bound to one policy snapshot."""

    policy: BudgetPolicySnapshot
    request_remaining: int | None
    subscription_remaining: int | None
    elapsed_ms: int

    def __post_init__(self) -> None:
        if not isinstance(self.policy, BudgetPolicySnapshot):
            raise GovernorInputError("budget policy snapshot is required")
        _non_negative(self.elapsed_ms, "budget elapsed time")
        self._validate_remaining(self.request_remaining, self.policy.request_limit, "request")
        self._validate_remaining(
            self.subscription_remaining, self.policy.subscription_limit, "subscription"
        )

    @staticmethod
    def _validate_remaining(remaining: int | None, limit: BudgetLimit, label: str) -> None:
        if remaining is None:
            return
        _non_negative(remaining, f"{label} remaining")
        if limit.capacity is None:
            raise GovernorConsistencyError(f"{label} remaining requires known capacity")
        if remaining > limit.capacity:
            raise GovernorConsistencyError(f"{label} remaining exceeds capacity")

    def remaining_for(self, quota: QuotaKind) -> int | None:
        if not isinstance(quota, QuotaKind):
            raise GovernorInputError("invalid quota kind")
        return self.request_remaining if quota is QuotaKind.REQUEST else self.subscription_remaining

    @property
    def fingerprint(self) -> str:
        return _hash(
            {
                "policy_fingerprint": self.policy.fingerprint,
                "request_remaining": self.request_remaining,
                "subscription_remaining": self.subscription_remaining,
                "elapsed_ms": self.elapsed_ms,
            }
        )


@dataclass(frozen=True, slots=True)
class RetryBudget:
    """Finite retry and elapsed-time budget with explicit exhaustion."""

    max_attempts: int
    used_attempts: int = 0
    max_elapsed_ms: int = 1
    elapsed_ms: int = 0

    def __post_init__(self) -> None:
        _positive(self.max_attempts, "maximum attempts")
        _non_negative(self.used_attempts, "used attempts")
        if self.used_attempts > self.max_attempts:
            raise GovernorConsistencyError("used attempts exceed maximum attempts")
        _positive(self.max_elapsed_ms, "maximum retry elapsed time")
        _non_negative(self.elapsed_ms, "retry elapsed time")

    @property
    def exhausted(self) -> bool:
        return self.used_attempts >= self.max_attempts or self.elapsed_ms >= self.max_elapsed_ms

    def consume(self) -> RetryBudget:
        if self.exhausted:
            raise GovernorConsistencyError("retry budget is exhausted")
        return replace(self, used_attempts=self.used_attempts + 1)


@dataclass(frozen=True, slots=True)
class CircuitSnapshot:
    """Pure CLOSED/OPEN/HALF_OPEN circuit state."""

    state: CircuitState = CircuitState.CLOSED
    failure_count: int = 0
    failure_threshold: int = 3
    cooldown_ms: int = 1_000
    opened_at_ms: int | None = None
    probe_in_flight: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.state, CircuitState):
            raise GovernorInputError("invalid circuit state")
        _non_negative(self.failure_count, "circuit failure count")
        _positive(self.failure_threshold, "circuit failure threshold")
        _positive(self.cooldown_ms, "circuit cooldown")
        if self.state is CircuitState.OPEN and self.opened_at_ms is None:
            raise GovernorConsistencyError("open circuit requires opened time")
        if self.opened_at_ms is not None:
            _non_negative(self.opened_at_ms, "circuit opened time")
        if self.state is CircuitState.CLOSED:
            if self.opened_at_ms is not None or self.probe_in_flight:
                raise GovernorConsistencyError("closed circuit cannot carry open or probe state")
            if self.failure_count >= self.failure_threshold:
                raise GovernorConsistencyError("closed circuit cannot reach failure threshold")
        elif self.state is CircuitState.OPEN:
            if self.probe_in_flight:
                raise GovernorConsistencyError("open circuit cannot carry an in-flight probe")
            if self.failure_count < self.failure_threshold:
                raise GovernorConsistencyError("open circuit requires failure threshold")
        else:
            if self.opened_at_ms is not None:
                raise GovernorConsistencyError("half-open circuit cannot carry open time")
            if self.failure_count < self.failure_threshold:
                raise GovernorConsistencyError("half-open circuit requires failure threshold")

    @property
    def fingerprint(self) -> str:
        return _hash(
            {
                "state": self.state.value,
                "failure_count": self.failure_count,
                "failure_threshold": self.failure_threshold,
                "cooldown_ms": self.cooldown_ms,
                "opened_at_ms": self.opened_at_ms,
                "probe_in_flight": self.probe_in_flight,
            }
        )

    def transition(self, elapsed_ms: int) -> CircuitSnapshot:
        _non_negative(elapsed_ms, "circuit elapsed time")
        if self.state is not CircuitState.OPEN:
            return self
        assert self.opened_at_ms is not None
        if elapsed_ms < self.opened_at_ms:
            raise GovernorInputError("circuit time moved backwards")
        if elapsed_ms - self.opened_at_ms < self.cooldown_ms:
            return self
        return replace(
            self,
            state=CircuitState.HALF_OPEN,
            failure_count=self.failure_threshold,
            opened_at_ms=None,
            probe_in_flight=False,
        )

    def begin_probe(self, elapsed_ms: int) -> CircuitSnapshot:
        transitioned = self.transition(elapsed_ms)
        if transitioned.state is not CircuitState.HALF_OPEN or transitioned.probe_in_flight:
            raise GovernorConsistencyError("circuit probe is not available")
        return replace(transitioned, probe_in_flight=True)

    def record_failure(self, elapsed_ms: int) -> CircuitSnapshot:
        _non_negative(elapsed_ms, "circuit elapsed time")
        if self.state is CircuitState.OPEN:
            raise GovernorConsistencyError("open circuit has no admitted failure transition")
        if self.state is CircuitState.HALF_OPEN:
            if not self.probe_in_flight:
                raise GovernorConsistencyError("half-open failure requires an in-flight probe")
            return replace(
                self,
                state=CircuitState.OPEN,
                failure_count=self.failure_threshold,
                opened_at_ms=elapsed_ms,
                probe_in_flight=False,
            )
        next_count = self.failure_count + 1
        if next_count >= self.failure_threshold:
            return replace(
                self,
                state=CircuitState.OPEN,
                failure_count=next_count,
                opened_at_ms=elapsed_ms,
                probe_in_flight=False,
            )
        return replace(self, failure_count=next_count)

    def record_success(self) -> CircuitSnapshot:
        if self.state is not CircuitState.HALF_OPEN or not self.probe_in_flight:
            raise GovernorConsistencyError("success requires an in-flight half-open probe")
        return replace(
            self,
            state=CircuitState.CLOSED,
            failure_count=0,
            opened_at_ms=None,
            probe_in_flight=False,
        )


@dataclass(frozen=True, slots=True)
class SessionGeneration:
    """Local ordered identity for future transport generations."""

    number: int
    retired: bool = False

    def __post_init__(self) -> None:
        _positive(self.number, "generation number")
        if not isinstance(self.retired, bool):
            raise GovernorInputError("retired flag must be boolean")

    def rollover(self, next_number: int) -> SessionGeneration:
        _positive(next_number, "next generation number")
        if next_number <= self.number:
            raise GovernorConsistencyError("generation rollover must be strictly increasing")
        return SessionGeneration(next_number)

    def retire(self) -> SessionGeneration:
        return replace(self, retired=True)

    def accepts(self, incoming: SessionGeneration) -> bool:
        return (
            isinstance(incoming, SessionGeneration)
            and not self.retired
            and not incoming.retired
            and incoming.number == self.number
        )


@dataclass(frozen=True, slots=True)
class SubscriptionIntent:
    """Immutable planning intent; it contains no executable transport handle."""

    intent_id: str
    contract_id: StableId
    channel: str
    priority: PriorityClass
    generation: SessionGeneration
    state: IntentState = IntentState.REQUESTED

    def __post_init__(self) -> None:
        _text(self.intent_id, "intent id")
        if (
            not isinstance(self.contract_id, StableId)
            or self.contract_id.kind is not IdentityKind.INSTRUMENT
        ):
            raise GovernorInputError("contract id must be an INSTRUMENT StableId")
        _text(self.channel, "channel")
        if not isinstance(self.priority, PriorityClass):
            raise GovernorInputError("invalid intent priority")
        if not isinstance(self.generation, SessionGeneration) or self.generation.retired:
            raise GovernorInputError("intent requires a live generation")
        if not isinstance(self.state, IntentState):
            raise GovernorInputError("invalid intent state")

    @property
    def fingerprint(self) -> str:
        return _hash(
            {
                "intent_id": self.intent_id,
                "contract_id": self.contract_id.as_text(),
                "channel": self.channel,
                "priority": self.priority.value,
                "generation": self.generation.number,
                "state": self.state.value,
            }
        )


@dataclass(frozen=True, slots=True)
class QueueSnapshot:
    """Bounded queue state; depth cannot exceed capacity."""

    capacity: int
    depth: int = 0
    protected_depth: int = 0

    def __post_init__(self) -> None:
        _positive(self.capacity, "queue capacity")
        _non_negative(self.depth, "queue depth")
        _non_negative(self.protected_depth, "protected queue depth")
        if self.depth > self.capacity:
            raise GovernorConsistencyError("queue depth exceeds capacity")
        if self.protected_depth > self.depth:
            raise GovernorConsistencyError("protected queue depth exceeds queue depth")

    def has_room(self, units: int = 1) -> bool:
        _positive(units, "queue units")
        return self.depth + units <= self.capacity

    @property
    def fingerprint(self) -> str:
        return _hash(
            {
                "capacity": self.capacity,
                "depth": self.depth,
                "protected_depth": self.protected_depth,
            }
        )


@dataclass(frozen=True, slots=True)
class AdmissionRequest:
    """Typed control request with no payload or executable callback."""

    quota: QuotaKind
    units: int
    priority: PriorityClass
    generation: SessionGeneration
    queue_units: int = 1
    is_probe: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.quota, QuotaKind):
            raise GovernorInputError("invalid quota kind")
        _positive(self.units, "admission units")
        if not isinstance(self.priority, PriorityClass):
            raise GovernorInputError("invalid admission priority")
        if not isinstance(self.generation, SessionGeneration):
            raise GovernorInputError("admission generation is required")
        _positive(self.queue_units, "admission queue units")
        if not isinstance(self.is_probe, bool):
            raise GovernorInputError("probe flag must be boolean")

    @property
    def fingerprint(self) -> str:
        return _hash(
            {
                "quota": self.quota.value,
                "units": self.units,
                "priority": self.priority.value,
                "generation": {
                    "number": self.generation.number,
                    "retired": self.generation.retired,
                },
                "queue_units": self.queue_units,
                "is_probe": self.is_probe,
            }
        )


@dataclass(frozen=True, slots=True)
class AdmissionDecision:
    """Immutable deterministic outcome and reason evidence."""

    outcome: AdmissionOutcome
    reason: AdmissionReason
    fingerprint: str = field(init=False)

    def __init__(self) -> None:
        raise TypeError("Use AdmissionDecision.create(...)")

    @classmethod
    def create(
        cls,
        *,
        outcome: AdmissionOutcome,
        reason: AdmissionReason,
        material: object,
    ) -> AdmissionDecision:
        if not isinstance(outcome, AdmissionOutcome):
            raise GovernorInputError("invalid admission outcome")
        if not isinstance(reason, AdmissionReason):
            raise GovernorInputError("invalid admission reason")
        allowed = {
            AdmissionOutcome.ADMIT: frozenset({AdmissionReason.ADMITTED}),
            AdmissionOutcome.DEFER: frozenset(
                {
                    AdmissionReason.STALE_GENERATION,
                    AdmissionReason.RETRY_EXHAUSTED,
                    AdmissionReason.QUEUE_FULL,
                    AdmissionReason.PROTECTED_RESERVE,
                    AdmissionReason.BUDGET_EXHAUSTED,
                }
            ),
            AdmissionOutcome.SHED: frozenset(
                {
                    AdmissionReason.QUEUE_FULL,
                    AdmissionReason.PROTECTED_RESERVE,
                    AdmissionReason.BUDGET_EXHAUSTED,
                }
            ),
            AdmissionOutcome.CIRCUIT_OPEN: frozenset(
                {AdmissionReason.CIRCUIT_OPEN, AdmissionReason.PROBE_IN_FLIGHT}
            ),
            AdmissionOutcome.UNKNOWN: frozenset({AdmissionReason.UNKNOWN_BUDGET}),
        }
        if reason not in allowed[outcome]:
            raise GovernorConsistencyError("outcome and reason are not an allowed pair")
        instance = object.__new__(cls)
        object.__setattr__(instance, "outcome", outcome)
        object.__setattr__(instance, "reason", reason)
        object.__setattr__(
            instance,
            "fingerprint",
            _hash({"material": material, "outcome": outcome.value, "reason": reason.value}),
        )
        return instance


class QuotaGovernor:
    """Pure deterministic controller for future transport callers."""

    @staticmethod
    def decide(
        request: AdmissionRequest,
        budget: BudgetSnapshot,
        queue: QueueSnapshot,
        circuit: CircuitSnapshot,
        retry: RetryBudget,
        current_generation: SessionGeneration,
        *,
        elapsed_ms: int,
    ) -> AdmissionDecision:
        if not isinstance(request, AdmissionRequest):
            raise GovernorInputError("admission request is required")
        if not isinstance(budget, BudgetSnapshot):
            raise GovernorInputError("budget snapshot is required")
        if not isinstance(queue, QueueSnapshot):
            raise GovernorInputError("queue snapshot is required")
        if not isinstance(circuit, CircuitSnapshot):
            raise GovernorInputError("circuit snapshot is required")
        if not isinstance(retry, RetryBudget):
            raise GovernorInputError("retry budget is required")
        if not isinstance(current_generation, SessionGeneration):
            raise GovernorInputError("current generation is required")
        _non_negative(elapsed_ms, "decision elapsed time")

        effective_circuit = circuit.transition(elapsed_ms)
        remaining = budget.remaining_for(request.quota)
        if remaining is None:
            return QuotaGovernor._decision(
                request,
                budget,
                queue,
                effective_circuit,
                retry,
                current_generation,
                elapsed_ms,
                AdmissionOutcome.UNKNOWN,
                AdmissionReason.UNKNOWN_BUDGET,
            )
        if not current_generation.accepts(request.generation):
            return QuotaGovernor._decision(
                request,
                budget,
                queue,
                effective_circuit,
                retry,
                current_generation,
                elapsed_ms,
                AdmissionOutcome.DEFER,
                AdmissionReason.STALE_GENERATION,
            )
        if retry.exhausted:
            return QuotaGovernor._decision(
                request,
                budget,
                queue,
                effective_circuit,
                retry,
                current_generation,
                elapsed_ms,
                AdmissionOutcome.DEFER,
                AdmissionReason.RETRY_EXHAUSTED,
            )
        if effective_circuit.state is CircuitState.OPEN:
            return QuotaGovernor._decision(
                request,
                budget,
                queue,
                effective_circuit,
                retry,
                current_generation,
                elapsed_ms,
                AdmissionOutcome.CIRCUIT_OPEN,
                AdmissionReason.CIRCUIT_OPEN,
            )
        if effective_circuit.state is CircuitState.HALF_OPEN and (
            not request.is_probe or not effective_circuit.probe_in_flight
        ):
            reason = (
                AdmissionReason.PROBE_IN_FLIGHT
                if effective_circuit.probe_in_flight and not request.is_probe
                else AdmissionReason.CIRCUIT_OPEN
            )
            return QuotaGovernor._decision(
                request,
                budget,
                queue,
                effective_circuit,
                retry,
                current_generation,
                elapsed_ms,
                AdmissionOutcome.CIRCUIT_OPEN,
                reason,
            )
        if not queue.has_room(request.queue_units):
            outcome = (
                AdmissionOutcome.SHED
                if request.priority is PriorityClass.RESEARCH
                else AdmissionOutcome.DEFER
            )
            return QuotaGovernor._decision(
                request,
                budget,
                queue,
                effective_circuit,
                retry,
                current_generation,
                elapsed_ms,
                outcome,
                AdmissionReason.QUEUE_FULL,
            )
        if (
            not request.priority.may_use_protected_reserve
            and queue.depth + request.queue_units > queue.capacity - budget.policy.protected_reserve
        ):
            outcome = (
                AdmissionOutcome.SHED
                if request.priority is PriorityClass.RESEARCH
                else AdmissionOutcome.DEFER
            )
            return QuotaGovernor._decision(
                request,
                budget,
                queue,
                effective_circuit,
                retry,
                current_generation,
                elapsed_ms,
                outcome,
                AdmissionReason.PROTECTED_RESERVE,
            )
        if remaining < request.units:
            outcome = (
                AdmissionOutcome.SHED
                if request.priority is PriorityClass.RESEARCH
                else AdmissionOutcome.DEFER
            )
            return QuotaGovernor._decision(
                request,
                budget,
                queue,
                effective_circuit,
                retry,
                current_generation,
                elapsed_ms,
                outcome,
                AdmissionReason.BUDGET_EXHAUSTED,
            )
        if (
            not request.priority.may_use_protected_reserve
            and remaining - request.units < budget.policy.protected_reserve
        ):
            outcome = (
                AdmissionOutcome.SHED
                if request.priority is PriorityClass.RESEARCH
                else AdmissionOutcome.DEFER
            )
            return QuotaGovernor._decision(
                request,
                budget,
                queue,
                effective_circuit,
                retry,
                current_generation,
                elapsed_ms,
                outcome,
                AdmissionReason.PROTECTED_RESERVE,
            )
        return QuotaGovernor._decision(
            request,
            budget,
            queue,
            effective_circuit,
            retry,
            current_generation,
            elapsed_ms,
            AdmissionOutcome.ADMIT,
            AdmissionReason.ADMITTED,
        )

    @staticmethod
    def _decision(
        request: AdmissionRequest,
        budget: BudgetSnapshot,
        queue: QueueSnapshot,
        circuit: CircuitSnapshot,
        retry: RetryBudget,
        current_generation: SessionGeneration,
        elapsed_ms: int,
        outcome: AdmissionOutcome,
        reason: AdmissionReason,
    ) -> AdmissionDecision:
        return AdmissionDecision.create(
            outcome=outcome,
            reason=reason,
            material={
                "request": request.fingerprint,
                "budget": budget.fingerprint,
                "queue": queue.fingerprint,
                "circuit": circuit.fingerprint,
                "retry": {
                    "max_attempts": retry.max_attempts,
                    "used_attempts": retry.used_attempts,
                    "max_elapsed_ms": retry.max_elapsed_ms,
                    "elapsed_ms": retry.elapsed_ms,
                },
                "current_generation": {
                    "number": current_generation.number,
                    "retired": current_generation.retired,
                },
                "elapsed_ms": elapsed_ms,
            },
        )
