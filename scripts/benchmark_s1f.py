"""Deterministic S1F baseline benchmark; it never opens a network connection."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import tracemalloc
from collections import deque
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "apps" / "backend" / "src"))

from hct_backend.contracts import Environment, IdentityKind, StableId  # noqa: E402
from hct_backend.market_truth import GenerationRef  # noqa: E402
from hct_backend.s1f_mexc import MexcDecodeContext, MexcPublicDecoder  # noqa: E402

PROFILES = {
    "S1F-CONTRACT-MICRO-V1": {
        "symbols": 1,
        "ticker": 64,
        "deal": 256,
        "depth": 128,
        "depth-full": 32,
        "kline": 32,
        "total": 512,
        "depth-levels": 5,
        "replay-seconds": 60,
    },
    "S1F-NOMINAL-MULTICHANNEL-V1": {
        "symbols": 8,
        "ticker": 1024,
        "deal": 4096,
        "depth": 2048,
        "depth-full": 512,
        "kline": 512,
        "total": 8192,
        "depth-levels": 20,
        "replay-seconds": 900,
    },
    "S1F-STRESS-BACKPRESSURE-V1": {
        "symbols": 32,
        "ticker": 8192,
        "deal": 32768,
        "depth": 16384,
        "depth-full": 4096,
        "kline": 4096,
        "total": 65536,
        "depth-levels": 20,
        "queue-capacity": 4096,
        "replay-seconds": 3600,
    },
}


def ticker_message(index: int) -> str:
    value = str(100 + (index % 1000))
    return json.dumps(
        {
            "channel": "push.ticker",
            "symbol": "BTC_USDT",
            "ts": str(1700000000000 + index),
            "data": {
                "lastPrice": value,
                "bid1": value,
                "ask1": value,
                "volume24": "10",
                "holdVol": "20",
                "indexPrice": value,
                "fairPrice": value,
                "fundingRate": "0.0001",
                "timestamp": str(1700000000000 + index),
            },
        },
        separators=(",", ":"),
    )


def deal_message(index: int) -> str:
    return json.dumps(
        {
            "channel": "push.deal",
            "symbol": "BTC_USDT",
            "ts": str(1700000000000 + index),
            "data": {
                "deals": [
                    {"p": "411.8", "v": "10", "T": "1", "t": str(1700000000000 + index)}
                ]
            },
        },
        separators=(",", ":"),
    )


def kline_message(index: int) -> str:
    return json.dumps(
        {
            "channel": "push.kline",
            "symbol": "BTC_USDT",
            "ts": str(1700000000000 + index),
            "data": {
                "interval": "Min1",
                "t": "1700000040",
                "o": "411.0",
                "h": "412.0",
                "l": "410.5",
                "c": "411.8",
                "q": "10",
                "a": "4118.0",
            },
        },
        separators=(",", ":"),
    )


def depth_message(index: int, levels: int) -> str:
    bids = [
        [str(Decimal("411.8") - Decimal(level) / 10), "10", "1"]
        for level in range(levels)
    ]
    asks = [
        [str(Decimal("412.0") + Decimal(level) / 10), "5", "1"]
        for level in range(levels)
    ]
    return json.dumps(
        {
            "channel": "push.depth",
            "symbol": "BTC_USDT",
            "ts": str(1700000000000 + index),
            "data": {
                "version": str(index + 1),
                "bids": bids,
                "asks": asks,
            },
        },
        separators=(",", ":"),
    )


def percentile(values: list[int], fraction: float) -> int:
    ordered = sorted(values)
    index = min(len(ordered) - 1, int((len(ordered) - 1) * fraction))
    return ordered[index]


def run(profile_name: str) -> dict[str, object]:
    profile = PROFILES[profile_name]
    source = StableId(kind=IdentityKind.EXCHANGE, value="mexc")
    contract = StableId(kind=IdentityKind.INSTRUMENT, value="btc-usdt")
    generation = GenerationRef(source, Environment.REPLAY, 1)
    decoder = MexcPublicDecoder()
    count = int(profile["total"])
    ticker_count = int(profile["ticker"])
    deal_count = int(profile["deal"])
    depth_count = int(profile["depth"])
    full_depth_count = int(profile["depth-full"])
    kline_count = int(profile["kline"])
    depth_levels = int(profile["depth-levels"])
    queue_capacity = int(profile.get("queue-capacity", 4096))
    queue: deque[tuple[str, int, str, int]] = deque()
    kinds = (
        ("ticker", ticker_count),
        ("deal", deal_count),
        ("depth", depth_count),
        ("depth-full", full_depth_count),
        ("kline", kline_count),
    )
    assert sum(amount for _, amount in kinds) == count
    cumulative: list[tuple[str, int]] = []
    running = 0
    for kind, amount in kinds:
        running += amount
        cumulative.append((kind, running))
    normalization_latencies_ns: list[int] = []
    publication_latencies_ns: list[int] = []
    queue_ages_ns: list[int] = []
    raw_hasher = hashlib.sha256()
    event_context_time = datetime(2026, 1, 1, tzinfo=UTC)
    stress = profile_name == "S1F-STRESS-BACKPRESSURE-V1"
    consumer_every = 8 if stress else 1
    produced = 0
    admitted = 0
    consumed = 0
    dropped = 0
    max_queue_depth = 0

    def consume_one() -> None:
        nonlocal consumed
        if not queue:
            return
        raw, enqueued_ns, kind, index = queue.popleft()
        queue_ages_ns.append(max(0, time.perf_counter_ns() - enqueued_ns))
        context = MexcDecodeContext(
            source,
            Environment.REPLAY,
            generation,
            contract,
            "BTC_USDT",
            event_context_time,
            event_context_time,
            0,
            "a" * 64,
            subscription_context=f"benchmark:{kind}",
            previous_depth_version=index if kind == "depth" else None,
            full_depth=kind == "depth-full",
        )
        normalization_started = time.perf_counter_ns()
        decoded = decoder.decode(raw, context)
        normalization_latencies_ns.append(
            time.perf_counter_ns() - normalization_started
        )
        publication_started = time.perf_counter_ns()
        published_fingerprints = tuple(
            getattr(value, "fingerprint") for value in decoded.values
        )
        if not published_fingerprints:
            raise AssertionError("canonical publication produced no value")
        publication_latencies_ns.append(time.perf_counter_ns() - publication_started)
        consumed += 1

    tracemalloc.start()
    started = time.perf_counter()
    for index in range(count):
        kind = next(name for name, limit in cumulative if index < limit)
        if kind == "ticker":
            raw = ticker_message(index)
        elif kind == "deal":
            raw = deal_message(index)
        elif kind == "kline":
            raw = kline_message(index)
        else:
            raw = depth_message(index, depth_levels)
        raw_hasher.update(raw.encode("utf-8"))
        produced += 1
        if len(queue) < queue_capacity:
            queue.append((raw, time.perf_counter_ns(), kind, index))
            admitted += 1
            max_queue_depth = max(max_queue_depth, len(queue))
        else:
            dropped += 1
        if (index + 1) % consumer_every == 0:
            consume_one()
    while queue:
        consume_one()
    elapsed = max(time.perf_counter() - started, 1e-9)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    normalization_latency = {
        "unit": "nanoseconds",
        "min": min(normalization_latencies_ns),
        "p50": percentile(normalization_latencies_ns, 0.50),
        "p95": percentile(normalization_latencies_ns, 0.95),
        "p99": percentile(normalization_latencies_ns, 0.99),
        "max": max(normalization_latencies_ns),
    }
    publication_latency = {
        "unit": "nanoseconds",
        "min": min(publication_latencies_ns),
        "p50": percentile(publication_latencies_ns, 0.50),
        "p95": percentile(publication_latencies_ns, 0.95),
        "p99": percentile(publication_latencies_ns, 0.99),
        "max": max(publication_latencies_ns),
    }
    queue_age_ms_max = max(queue_ages_ns, default=0) / 1_000_000
    completion_invariant = consumed + dropped == produced and admitted == consumed
    baseline_no_loss = not stress and dropped == 0 and consumed == produced
    stress_shed_invariant = stress and dropped > 0 and completion_invariant
    correctness = "PASS" if (baseline_no_loss or stress_shed_invariant) else "FAIL"
    return {
        "profile": profile_name,
        "parameters": profile,
        "seed": 0,
        "messages_produced": produced,
        "messages_decoded": consumed,
        "admitted_count": admitted,
        "consumed_count": consumed,
        "dropped_count": dropped,
        "elapsed_seconds": elapsed,
        "normalization_throughput_per_second": consumed / elapsed,
        "replay_throughput_per_second": consumed / elapsed,
        "normalization_latency_distribution": normalization_latency,
        "immutable_value_publication_latency_distribution": publication_latency,
        "peak_memory_bytes": peak,
        "steady_memory_bytes": current,
        "queue_capacity": queue_capacity,
        "queue_depth_max": max_queue_depth,
        "queue_age_ms_max": queue_age_ms_max,
        "queue_age_samples": len(queue_ages_ns),
        "queue_dropped": dropped,
        "correctness": correctness,
        "bounded_completion": completion_invariant
        and max_queue_depth <= queue_capacity,
        "producer_model": "deterministic_one_frame_per_iteration",
        "consumer_model": (
            "deterministic_one_frame_every_eight_produced_frames_with_final_drain"
            if stress
            else "deterministic_one_frame_per_produced_frame"
        ),
        "producer_rate_per_second": produced / elapsed,
        "consumer_rate_per_second": consumed / elapsed,
        "raw_artifact_hash": raw_hasher.hexdigest(),
        "limitations": [
            "synthetic pinned multichannel fixture stream",
            "no product latency SLO asserted",
            "no live network",
            "stress profile intentionally sheds under a deterministic bounded consumer "
            "rate",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--profile", choices=[*PROFILES, "all"], default="S1F-CONTRACT-MICRO-V1"
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    names = list(PROFILES) if args.profile == "all" else [args.profile]
    result = {
        "mode": "BASELINE_ESTABLISHMENT_V1",
        "profiles": [run(name) for name in names],
    }
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
