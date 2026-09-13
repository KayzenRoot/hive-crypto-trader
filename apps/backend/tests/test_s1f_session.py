import asyncio

import pytest

from hct_backend.contracts import Environment, IdentityKind, StableId
from hct_backend.quota_governor import AdmissionDecision, AdmissionOutcome, AdmissionReason
from hct_backend.s1f_session import (
    BoundedInboundQueue,
    GenerationManager,
    MexcPublicRest,
    MexcPublicSession,
    RetryPolicy,
    SessionError,
    SubscriptionIntent,
)


def test_generation_retirement_and_queue_are_bounded() -> None:
    source = StableId(kind=IdentityKind.EXCHANGE, value="mexc")
    manager = GenerationManager(source, Environment.REPLAY)
    session = MexcPublicSession(manager, queue_capacity=1)
    first = session.open_generation()
    second = session.open_generation()
    assert first.retired is False
    assert second.number == 2
    assert not manager.accepts(first)
    assert manager.accepts(second)
    assert session.accept_message(second, "one") is True
    assert session.accept_message(second, "two") is False


def test_subscription_staging_is_idempotent_and_full_depth_is_frozen() -> None:
    manager = GenerationManager(
        StableId(kind=IdentityKind.EXCHANGE, value="mexc"), Environment.REPLAY
    )
    session = MexcPublicSession(manager)
    intent = SubscriptionIntent("sub.depth.full", "BTC_USDT", 20)
    incremental = SubscriptionIntent("sub.depth", "BTC_USDT")
    assert incremental.payload["param"]["compress"] is False  # type: ignore[index]
    assert len(session.staged_subscriptions((intent, intent))) == 1
    assert session.staged_subscriptions((intent,)) == ()
    try:
        SubscriptionIntent("sub.depth.full", "BTC_USDT", 25)
    except SessionError:
        pass
    else:
        raise AssertionError("invalid full-depth limit was accepted")


def test_connection_uses_modern_direct_transport_and_application_ping(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class Socket:
        def __init__(self) -> None:
            self.sent: list[str] = []

        async def send(self, message: str) -> None:
            self.sent.append(message)

    class Connection:
        def __init__(self) -> None:
            self.socket = Socket()

        async def __aenter__(self) -> Socket:
            return self.socket

        async def __aexit__(self, *args: object) -> None:
            return None

    captured: dict[str, object] = {}

    def fake_connect(url: str, **kwargs: object) -> Connection:
        captured.update(url=url, **kwargs)
        return Connection()

    monkeypatch.setattr("websockets.asyncio.client.connect", fake_connect)

    async def exercise() -> None:
        source = StableId(kind=IdentityKind.EXCHANGE, value="mexc")
        session = MexcPublicSession(GenerationManager(source, Environment.REPLAY))
        generation = await session.connect_once((SubscriptionIntent("sub.ticker", "BTC_USDT"),))
        assert generation.number == 1

    asyncio.run(exercise())
    assert captured["url"] == "wss://contract.mexc.com/edge"
    assert captured["proxy"] is None
    assert captured["ping_interval"] is None


def test_invalid_rest_transport_bounds_are_rejected() -> None:
    with pytest.raises(SessionError):
        MexcPublicRest(timeout_seconds=0)
    with pytest.raises(SessionError):
        MexcPublicRest(max_connections=0)


def test_retry_policy_is_bounded_and_deterministic() -> None:
    policy = RetryPolicy(max_attempts=3, seed=7)
    assert policy.delay_ms(1) == policy.delay_ms(1)
    assert policy.delay_ms(3) >= policy.delay_ms(1)
    try:
        policy.delay_ms(4)
    except SessionError:
        pass
    else:
        raise AssertionError("retry budget was not bounded")
    with pytest.raises(SessionError):
        RetryPolicy(max_attempts=0)
    with pytest.raises(SessionError):
        RetryPolicy(base_delay_ms=10, max_delay_ms=1)
    with pytest.raises(SessionError):
        RetryPolicy(jitter_ms=-1)


def test_queue_rejects_non_admitted_work_without_authority_upgrade() -> None:
    queue = BoundedInboundQueue(2)
    denied = AdmissionDecision.create(
        outcome=AdmissionOutcome.SHED,
        reason=AdmissionReason.QUEUE_FULL,
        material={"test": "denied"},
    )
    assert queue.publish("blocked", admission=denied) is False
    assert queue.dropped == 1
    assert queue.depth == 0
    with pytest.raises(SessionError):
        BoundedInboundQueue(0)
    with pytest.raises(SessionError):
        SubscriptionIntent("private.order", "BTC_USDT")
    with pytest.raises(SessionError):
        SubscriptionIntent("sub.depth", "")
    with pytest.raises(SessionError):
        SubscriptionIntent("sub.ticker", "BTC_USDT", 5)


def test_session_ping_receive_and_circuit_are_explicit() -> None:
    class Socket:
        def __init__(self) -> None:
            self.sent: list[str] = []

        async def send(self, message: str) -> None:
            self.sent.append(message)

        async def recv(self) -> str:
            return "frame"

    async def exercise() -> None:
        source = StableId(kind=IdentityKind.EXCHANGE, value="mexc")
        session = MexcPublicSession(
            GenerationManager(source, Environment.REPLAY),
            retry_policy=RetryPolicy(max_attempts=2, base_delay_ms=0, jitter_ms=0),
            queue_capacity=2,
        )
        socket = Socket()
        assert await session.receive_once(socket) == "frame"
        await session.send_application_ping(socket)
        assert socket.sent == ['{"method":"ping"}']
        assert session.record_failure().value == "HALF_OPEN"
        assert session.record_failure().value == "OPEN"
        with pytest.raises(SessionError):
            session.open_generation()
        session.record_success()
        generation = session.open_generation()
        assert session.accept_message(generation, "one") is True
        assert await session.inbound.receive() == "one"
        session.inbound.task_done()
        stale = generation
        current = session.open_generation()
        assert session.accept_message(stale, "stale") is False
        assert session.accept_message(current, "current") is True

    asyncio.run(exercise())


def test_public_rest_has_explicit_paths_limits_and_bounded_retry() -> None:
    class Response:
        def __init__(self, payload: object, failures: int = 0) -> None:
            self.status_code = 500 if failures else 200
            self.payload = payload
            self.failures = failures

        def raise_for_status(self) -> None:
            if self.failures:
                self.failures -= 1
                raise RuntimeError("temporary provider failure")

        def json(self) -> object:
            return self.payload

    class Client:
        def __init__(self) -> None:
            self.response = Response({"ok": True}, failures=1)
            self.calls: list[tuple[str, dict[str, object] | None]] = []

        async def __aenter__(self) -> "Client":
            return self

        async def __aexit__(self, *args: object) -> None:
            return None

        async def get(self, path: str, params: dict[str, object] | None = None) -> Response:
            self.calls.append((path, params))
            response = self.response
            response.status_code = 500 if response.failures else 200
            return response

    async def exercise() -> None:
        client = Client()
        rest = MexcPublicRest(
            retry_policy=RetryPolicy(max_attempts=2, base_delay_ms=0, jitter_ms=0)
        )

        async def fake_client() -> Client:
            return client

        rest._client = fake_client  # type: ignore[method-assign]
        assert await rest.depth("BTC_USDT") == {"ok": True}
        assert await rest.depth_commits("BTC_USDT", 20) == {"ok": True}
        assert await rest.kline("BTC_USDT", "Min1", 1, 61) == {"ok": True}
        assert client.calls[0][0] == "/api/v1/contract/depth/BTC_USDT"
        assert client.calls[2][0] == "/api/v1/contract/depth_commits/BTC_USDT/20"
        assert client.calls[3][1] == {"interval": "Min1", "start": 1, "end": 61, "limit": 2000}
        with pytest.raises(SessionError):
            await rest.depth("")
        with pytest.raises(SessionError):
            await rest.kline("BTC_USDT", "Min1", 1, 1)
        real_client = await MexcPublicRest()._client()
        await real_client.aclose()

        class Denied:
            def admit(self, *, priority: str, cost: int) -> AdmissionDecision:
                return AdmissionDecision.create(
                    outcome=AdmissionOutcome.SHED,
                    reason=AdmissionReason.QUEUE_FULL,
                    material={"priority": priority, "cost": cost},
                )

        denied_rest = MexcPublicRest(admission=Denied())
        with pytest.raises(SessionError):
            await denied_rest.depth("BTC_USDT")

        class BadClient(Client):
            async def get(self, path: str, params: dict[str, object] | None = None) -> Response:
                self.calls.append((path, params))
                return Response([], failures=0)

        bad_rest = MexcPublicRest(retry_policy=RetryPolicy(max_attempts=1))
        bad_client = BadClient()

        async def bad_fake_client() -> BadClient:
            return bad_client

        bad_rest._client = bad_fake_client  # type: ignore[method-assign]
        with pytest.raises(SessionError):
            await bad_rest.depth("BTC_USDT")
        with pytest.raises(SessionError):
            await rest.depth_commits("BTC_USDT", 0)

    asyncio.run(exercise())
