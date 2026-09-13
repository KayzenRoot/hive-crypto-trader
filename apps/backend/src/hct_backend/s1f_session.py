"""Bounded public MEXC session and REST transport seams for S1F."""

from __future__ import annotations

import asyncio
import hashlib
import json
import random
from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Protocol

from hct_backend.contracts import Environment, StableId
from hct_backend.market_truth import GenerationRef
from hct_backend.quota_governor import AdmissionDecision, AdmissionOutcome
from hct_backend.s1f_mexc import (
    MEXC_PUBLIC_CHANNELS,
    MEXC_REST_DEPTH,
    MEXC_REST_DEPTH_COMMITS,
    MEXC_REST_KLINE,
    MEXC_WS_URL,
)


class SessionError(RuntimeError):
    """Bounded session failure."""


class CircuitState(StrEnum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class AdmissionPort(Protocol):
    def admit(self, *, priority: str, cost: int) -> AdmissionDecision: ...


@dataclass(frozen=True, slots=True)
class RetryPolicy:
    max_attempts: int = 5
    base_delay_ms: int = 250
    max_delay_ms: int = 10_000
    jitter_ms: int = 100
    seed: int = 0

    def __post_init__(self) -> None:
        if (
            self.max_attempts < 1
            or self.base_delay_ms < 0
            or self.max_delay_ms < self.base_delay_ms
            or self.jitter_ms < 0
        ):
            raise SessionError("retry policy is invalid")

    def delay_ms(self, attempt: int) -> int:
        if attempt < 1 or attempt > self.max_attempts:
            raise SessionError("retry attempt is outside the bounded budget")
        rng = random.Random(self.seed + attempt)
        exponential = min(self.max_delay_ms, self.base_delay_ms * (2 ** (attempt - 1)))
        return min(self.max_delay_ms, exponential + rng.randint(0, self.jitter_ms))


@dataclass(frozen=True, slots=True)
class SubscriptionIntent:
    channel: str
    symbol: str
    limit: int | None = None

    def __post_init__(self) -> None:
        if self.channel not in MEXC_PUBLIC_CHANNELS:
            raise SessionError("channel is not in the frozen public allowlist")
        if not self.symbol and self.channel != "sub.tickers":
            raise SessionError("subscription symbol is required")
        if self.channel == "sub.depth.full" and self.limit not in {5, 10, 20}:
            raise SessionError("full-depth limit must be 5, 10 or 20")
        if self.channel != "sub.depth.full" and self.limit is not None:
            raise SessionError("limit is only allowed for full-depth subscriptions")

    @property
    def fingerprint(self) -> str:
        return hashlib.sha256(
            json.dumps(self.payload, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()

    @property
    def payload(self) -> dict[str, Any]:
        item: dict[str, Any] = {"method": self.channel, "param": {"symbol": self.symbol}}
        if self.limit is not None:
            item["param"]["limit"] = self.limit
        if self.channel == "sub.depth":
            item["param"]["compress"] = False
        return item


@dataclass(frozen=True, slots=True)
class GenerationManager:
    source_id: StableId
    environment: Environment
    current: GenerationRef | None = None

    def publish_new(self) -> tuple[GenerationRef, GenerationRef | None]:
        previous = self.current
        if previous is None:
            current = GenerationRef(self.source_id, self.environment, 1)
        else:
            current = GenerationRef(self.source_id, self.environment, previous.number + 1)
        object.__setattr__(self, "current", current)
        return current, previous.retire() if previous is not None else None

    def accepts(self, generation: GenerationRef) -> bool:
        return self.current is not None and self.current.accepts(generation)


class BoundedInboundQueue:
    """Explicitly bounded queue; admission is checked before publication."""

    def __init__(self, capacity: int = 4096) -> None:
        if isinstance(capacity, bool) or not isinstance(capacity, int) or capacity < 1:
            raise SessionError("queue capacity must be positive")
        self._queue: asyncio.Queue[str] = asyncio.Queue(maxsize=capacity)
        self.dropped = 0

    @property
    def capacity(self) -> int:
        return self._queue.maxsize

    def publish(self, message: str, *, admission: AdmissionDecision | None = None) -> bool:
        if admission is not None and admission.outcome is not AdmissionOutcome.ADMIT:
            self.dropped += 1
            return False
        try:
            self._queue.put_nowait(message)
        except asyncio.QueueFull:
            self.dropped += 1
            return False
        return True

    async def receive(self) -> str:
        return await self._queue.get()

    def task_done(self) -> None:
        self._queue.task_done()

    @property
    def depth(self) -> int:
        return self._queue.qsize()


class MexcPublicSession:
    """One bounded connection generation using application-level MEXC ping."""

    def __init__(
        self,
        generation_manager: GenerationManager,
        *,
        retry_policy: RetryPolicy | None = None,
        queue_capacity: int = 4096,
        admission: AdmissionPort | None = None,
    ) -> None:
        self.generations = generation_manager
        self.retry_policy = retry_policy or RetryPolicy()
        self.inbound = BoundedInboundQueue(queue_capacity)
        self.admission = admission
        self.circuit = CircuitState.CLOSED
        self._failure_count = 0
        self._seen_intents: set[str] = set()

    def staged_subscriptions(
        self, intents: tuple[SubscriptionIntent, ...]
    ) -> tuple[dict[str, Any], ...]:
        staged: list[dict[str, Any]] = []
        for intent in intents:
            if intent.fingerprint in self._seen_intents:
                continue
            self._seen_intents.add(intent.fingerprint)
            staged.append(intent.payload)
        return tuple(staged)

    def open_generation(self) -> GenerationRef:
        if self.circuit is CircuitState.OPEN:
            raise SessionError("circuit is open")
        self._seen_intents.clear()
        generation, _ = self.generations.publish_new()
        return generation

    def record_failure(self) -> CircuitState:
        self._failure_count += 1
        if self._failure_count >= self.retry_policy.max_attempts:
            self.circuit = CircuitState.OPEN
        else:
            self.circuit = CircuitState.HALF_OPEN
        return self.circuit

    def record_success(self) -> None:
        self._failure_count = 0
        self.circuit = CircuitState.CLOSED

    def accept_message(self, generation: GenerationRef, message: str) -> bool:
        if not self.generations.accepts(generation):
            return False
        decision = (
            self.admission.admit(priority="PUBLIC_MARKET_DATA", cost=1) if self.admission else None
        )
        return self.inbound.publish(message, admission=decision)

    async def receive_once(self, websocket: Any) -> str:
        """Receive one frame; callers own the bounded loop and retry budget."""

        return await websocket.recv()

    async def send_application_ping(self, websocket: Any) -> None:
        await websocket.send(json.dumps({"method": "ping"}, separators=(",", ":")))

    async def connect_once(self, intents: tuple[SubscriptionIntent, ...]) -> GenerationRef:
        try:
            from websockets.asyncio.client import connect
        except ImportError as exc:  # pragma: no cover - dependency gate owns this path
            raise SessionError("websockets.asyncio.client is required") from exc
        if self.circuit is CircuitState.OPEN:
            raise SessionError("circuit is open")
        self._seen_intents.clear()
        staged = self.staged_subscriptions(intents)
        async with connect(
            MEXC_WS_URL,
            proxy=None,
            ping_interval=None,
            max_queue=self.inbound.capacity,
            open_timeout=5,
            close_timeout=5,
        ) as websocket:
            for payload in staged:
                await websocket.send(json.dumps(payload, separators=(",", ":")))
            await self.send_application_ping(websocket)
        generation = self.open_generation()
        self.record_success()
        return generation

    async def connect_with_retry(self, intents: tuple[SubscriptionIntent, ...]) -> GenerationRef:
        last_error: BaseException | None = None
        for attempt in range(1, self.retry_policy.max_attempts + 1):
            try:
                return await self.connect_once(intents)
            except Exception as exc:
                last_error = exc
                self.record_failure()
                if attempt == self.retry_policy.max_attempts:
                    break
                await asyncio.sleep(self.retry_policy.delay_ms(attempt) / 1000)
        raise SessionError("bounded public session retry budget exhausted") from last_error


class MexcPublicRest:
    """Allowlisted public REST calls with explicit transport bounds."""

    def __init__(
        self,
        *,
        timeout_seconds: float = 5.0,
        max_connections: int = 4,
        retry_policy: RetryPolicy | None = None,
        admission: AdmissionPort | None = None,
    ) -> None:
        if timeout_seconds <= 0 or max_connections < 1:
            raise SessionError("REST transport bounds are invalid")
        self.timeout_seconds = timeout_seconds
        self.max_connections = max_connections
        self.retry_policy = retry_policy or RetryPolicy(max_attempts=3)
        self.admission = admission

    async def _client(self) -> Any:
        try:
            import httpx
        except ImportError as exc:  # pragma: no cover - dependency gate owns this path
            raise SessionError("httpx is required") from exc
        return httpx.AsyncClient(
            base_url="https://contract.mexc.com",
            timeout=httpx.Timeout(self.timeout_seconds),
            limits=httpx.Limits(
                max_connections=self.max_connections, max_keepalive_connections=self.max_connections
            ),
            trust_env=False,
        )

    async def _get_json(self, path: str, *, params: dict[str, Any] | None = None) -> dict[str, Any]:
        if self.admission is not None:
            decision = self.admission.admit(priority="PUBLIC_MARKET_DATA", cost=1)
            if decision.outcome is not AdmissionOutcome.ADMIT:
                raise SessionError("public REST request denied by Module 29 admission")
        client = await self._client()
        async with client:
            last_error: BaseException | None = None
            for attempt in range(1, self.retry_policy.max_attempts + 1):
                try:
                    response = await client.get(path, params=params)
                    if response.status_code >= 500:
                        response.raise_for_status()
                    response.raise_for_status()
                    result = response.json()
                    if not isinstance(result, dict):
                        raise SessionError("public REST response must be an object")
                    return result
                except Exception as exc:
                    last_error = exc
                    if attempt == self.retry_policy.max_attempts:
                        break
                    await asyncio.sleep(self.retry_policy.delay_ms(attempt) / 1000)
            raise SessionError("bounded public REST retry budget exhausted") from last_error

    async def depth(self, symbol: str) -> dict[str, Any]:
        if not symbol:
            raise SessionError("symbol is required")
        return await self._get_json(MEXC_REST_DEPTH + symbol)

    async def depth_commits(self, symbol: str, limit: int) -> dict[str, Any]:
        if not symbol or limit < 1:
            raise SessionError("depth recovery parameters are invalid")
        return await self._get_json(f"{MEXC_REST_DEPTH_COMMITS}{symbol}/{limit}")

    async def kline(
        self, symbol: str, interval: str, start: int, end: int, limit: int = 2000
    ) -> dict[str, Any]:
        if not symbol or not interval or start < 0 or end <= start or not 1 <= limit <= 2000:
            raise SessionError("kline parameters are invalid")
        return await self._get_json(
            MEXC_REST_KLINE + symbol,
            params={"interval": interval, "start": start, "end": end, "limit": limit},
        )
