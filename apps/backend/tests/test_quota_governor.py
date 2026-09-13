from dataclasses import FrozenInstanceError, replace

import pytest

from hct_backend.quota_governor import (
    AdmissionOutcome,
    AdmissionReason,
    AdmissionRequest,
    BudgetLimit,
    BudgetPolicySnapshot,
    BudgetSnapshot,
    CircuitSnapshot,
    CircuitState,
    GovernorConsistencyError,
    GovernorInputError,
    IntentState,
    PriorityClass,
    QueueSnapshot,
    QuotaGovernor,
    QuotaKind,
    RetryBudget,
    SessionGeneration,
    SubscriptionIntent,
)


def policy(
    *,
    request_capacity: int | None = 10,
    subscription_capacity: int | None = 4,
    protected_reserve: int = 2,
    policy_version: int = 1,
) -> BudgetPolicySnapshot:
    return BudgetPolicySnapshot(
        policy_version=policy_version,
        source="declared-policy",
        window_ms=1_000,
        request_limit=BudgetLimit(request_capacity),
        subscription_limit=BudgetLimit(subscription_capacity),
        protected_reserve=protected_reserve,
    )


def budget(
    *,
    request_remaining: int | None = 10,
    subscription_remaining: int | None = 4,
    policy_snapshot: BudgetPolicySnapshot | None = None,
) -> BudgetSnapshot:
    return BudgetSnapshot(
        policy=policy_snapshot or policy(),
        request_remaining=request_remaining,
        subscription_remaining=subscription_remaining,
        elapsed_ms=100,
    )


def request(
    *,
    quota: QuotaKind = QuotaKind.REQUEST,
    units: int = 1,
    priority: PriorityClass = PriorityClass.NORMAL,
    generation: SessionGeneration | None = None,
    queue_units: int = 1,
    is_probe: bool = False,
) -> AdmissionRequest:
    return AdmissionRequest(
        quota=quota,
        units=units,
        priority=priority,
        generation=generation or SessionGeneration(1),
        queue_units=queue_units,
        is_probe=is_probe,
    )


def decide(
    candidate: AdmissionRequest,
    *,
    evidence: BudgetSnapshot | None = None,
    queue: QueueSnapshot | None = None,
    circuit: CircuitSnapshot | None = None,
    retry: RetryBudget | None = None,
    current: SessionGeneration | None = None,
    elapsed_ms: int = 100,
):
    return QuotaGovernor.decide(
        candidate,
        evidence or budget(),
        queue or QueueSnapshot(capacity=4),
        circuit or CircuitSnapshot(),
        retry or RetryBudget(max_attempts=3, max_elapsed_ms=1_000),
        current or SessionGeneration(1),
        elapsed_ms=elapsed_ms,
    )


def test_budget_policy_is_versioned_and_fingerprinted() -> None:
    first = policy()
    changed_source = replace(first, source="approved-policy")
    changed_limit = replace(
        first,
        request_limit=BudgetLimit(11),
    )
    changed_version = replace(first, policy_version=2)
    assert first.fingerprint != changed_source.fingerprint
    assert first.fingerprint != changed_limit.fingerprint
    assert first.fingerprint != changed_version.fingerprint
    assert budget().fingerprint != budget(policy_snapshot=changed_limit).fingerprint


def test_unknown_budget_fails_closed_without_permissive_default() -> None:
    unknown = budget(
        request_remaining=None,
        policy_snapshot=policy(request_capacity=None, protected_reserve=0),
    )
    result = decide(request(), evidence=unknown)
    assert result.outcome is AdmissionOutcome.UNKNOWN
    assert result.reason is AdmissionReason.UNKNOWN_BUDGET


def test_exact_capacity_admits_and_off_by_one_exhaustion_defers() -> None:
    exact = decide(
        request(units=3, priority=PriorityClass.PROTECTION),
        evidence=budget(request_remaining=3),
    )
    exhausted = decide(request(units=4), evidence=budget(request_remaining=3))
    assert exact.outcome is AdmissionOutcome.ADMIT
    assert exact.reason is AdmissionReason.ADMITTED
    assert exhausted.outcome is AdmissionOutcome.DEFER
    assert exhausted.reason is AdmissionReason.BUDGET_EXHAUSTED


def test_protected_reserve_is_unavailable_to_lower_priority() -> None:
    normal = decide(request(units=2), evidence=budget(request_remaining=3))
    exact_reserve = decide(request(units=1), evidence=budget(request_remaining=3))
    protection = decide(
        request(units=2, priority=PriorityClass.PROTECTION),
        evidence=budget(request_remaining=3),
    )
    assert normal.outcome is AdmissionOutcome.DEFER
    assert normal.reason is AdmissionReason.PROTECTED_RESERVE
    assert exact_reserve.outcome is AdmissionOutcome.ADMIT
    assert protection.outcome is AdmissionOutcome.ADMIT


def test_priority_order_is_deterministic_under_saturation() -> None:
    saturated = QueueSnapshot(capacity=1, depth=1)
    protected = decide(request(priority=PriorityClass.RECONCILIATION), queue=saturated)
    research = decide(request(priority=PriorityClass.RESEARCH), queue=saturated)
    assert protected.outcome is AdmissionOutcome.DEFER
    assert research.outcome is AdmissionOutcome.SHED
    assert protected.reason is research.reason is AdmissionReason.QUEUE_FULL


def test_lower_priority_cannot_consume_protected_queue_reserve() -> None:
    queue = QueueSnapshot(capacity=4, depth=1)
    normal = decide(request(queue_units=2), queue=queue)
    protection = decide(
        request(priority=PriorityClass.PROTECTION, queue_units=2),
        queue=queue,
    )
    assert normal.outcome is AdmissionOutcome.DEFER
    assert normal.reason is AdmissionReason.PROTECTED_RESERVE
    assert protection.outcome is AdmissionOutcome.ADMIT


def test_subscription_capacity_is_independent_and_bounded() -> None:
    result = decide(
        request(quota=QuotaKind.SUBSCRIPTION, units=4, priority=PriorityClass.PROTECTION),
        evidence=budget(subscription_remaining=4),
    )
    assert result.outcome is AdmissionOutcome.ADMIT
    assert (
        decide(
            request(quota=QuotaKind.SUBSCRIPTION, units=1),
            evidence=budget(subscription_remaining=0),
        ).reason
        is AdmissionReason.BUDGET_EXHAUSTED
    )


def test_retry_budget_is_finite_and_exhaustion_is_explicit() -> None:
    available = RetryBudget(max_attempts=2, max_elapsed_ms=100)
    consumed = available.consume()
    assert consumed.used_attempts == 1
    assert not consumed.exhausted
    exhausted = replace(consumed, used_attempts=2)
    assert exhausted.exhausted
    with pytest.raises(GovernorConsistencyError):
        exhausted.consume()
    assert decide(request(), retry=exhausted).reason is AdmissionReason.RETRY_EXHAUSTED


def test_retry_elapsed_budget_exhaustion_cannot_reset_to_unlimited() -> None:
    exhausted = RetryBudget(max_attempts=3, max_elapsed_ms=10, elapsed_ms=10)
    assert exhausted.exhausted
    with pytest.raises(GovernorConsistencyError):
        exhausted.consume()


def test_circuit_transitions_closed_open_half_open_and_probe() -> None:
    closed = CircuitSnapshot(failure_threshold=2, cooldown_ms=10)
    one_failure = closed.record_failure(1)
    opened = one_failure.record_failure(2)
    assert one_failure.state is CircuitState.CLOSED
    assert opened.state is CircuitState.OPEN
    assert decide(request(), circuit=opened, elapsed_ms=5).outcome is AdmissionOutcome.CIRCUIT_OPEN
    half_open = opened.transition(12)
    assert half_open.state is CircuitState.HALF_OPEN
    assert (
        decide(request(), circuit=half_open, elapsed_ms=12).reason is AdmissionReason.CIRCUIT_OPEN
    )
    probe = decide(request(is_probe=True), circuit=half_open, elapsed_ms=12)
    assert probe.outcome is AdmissionOutcome.ADMIT
    probing = half_open.begin_probe(12)
    assert (
        decide(request(is_probe=True), circuit=probing, elapsed_ms=12).reason
        is AdmissionReason.PROBE_IN_FLIGHT
    )
    assert probing.record_success().state is CircuitState.CLOSED


def test_circuit_time_rollback_is_rejected() -> None:
    opened = CircuitSnapshot(state=CircuitState.OPEN, opened_at_ms=10)
    with pytest.raises(GovernorInputError):
        opened.transition(9)


def test_generation_rollover_and_retirement_reject_stale_control() -> None:
    first = SessionGeneration(1)
    second = first.rollover(2)
    assert not first.accepts(second)
    assert second.accepts(SessionGeneration(2))
    stale = decide(request(generation=first), current=second)
    assert stale.outcome is AdmissionOutcome.DEFER
    assert stale.reason is AdmissionReason.STALE_GENERATION
    retired = second.retire()
    assert not retired.accepts(SessionGeneration(2))
    assert (
        decide(request(generation=second), current=retired).reason
        is AdmissionReason.STALE_GENERATION
    )
    with pytest.raises(GovernorConsistencyError):
        first.rollover(1)


def test_subscription_intent_is_immutable_and_non_executable() -> None:
    intent = SubscriptionIntent(
        intent_id="intent-1",
        contract_id="btc-usdt-perpetual",
        channel="trades",
        priority=PriorityClass.NORMAL,
        generation=SessionGeneration(1),
    )
    assert intent.state is IntentState.REQUESTED
    assert replace(intent, state=IntentState.ACCEPTED).fingerprint != intent.fingerprint
    with pytest.raises(FrozenInstanceError):
        intent.state = IntentState.ACCEPTED  # type: ignore[misc]
    with pytest.raises(GovernorInputError):
        replace(intent, generation=SessionGeneration(1, retired=True))


def test_decisions_are_deterministic_for_equal_normalized_inputs() -> None:
    first = decide(request(), elapsed_ms=100)
    second = decide(request(), elapsed_ms=100)
    assert first == second
    assert first.fingerprint == second.fingerprint


def test_queue_and_policy_inputs_reject_invalid_or_contradictory_values() -> None:
    with pytest.raises(GovernorInputError):
        BudgetLimit(0)
    with pytest.raises(GovernorInputError):
        BudgetLimit(1, 0)
    with pytest.raises(GovernorConsistencyError):
        BudgetLimit(None, 1)
    with pytest.raises(GovernorInputError):
        QueueSnapshot(capacity=0)
    with pytest.raises(GovernorConsistencyError):
        QueueSnapshot(capacity=2, depth=3)
    with pytest.raises(GovernorConsistencyError):
        BudgetPolicySnapshot(
            policy_version=1,
            source="policy",
            window_ms=1,
            request_limit=BudgetLimit(1),
            subscription_limit=BudgetLimit(1),
            protected_reserve=2,
        )


def test_circuit_and_generation_inputs_reject_malformed_values() -> None:
    with pytest.raises(GovernorInputError):
        CircuitSnapshot(state="OPEN")  # type: ignore[arg-type]
    with pytest.raises(GovernorConsistencyError):
        CircuitSnapshot(state=CircuitState.OPEN)
    with pytest.raises(GovernorInputError):
        SessionGeneration(0)
    with pytest.raises(GovernorInputError):
        request(priority="LOW")  # type: ignore[arg-type]
