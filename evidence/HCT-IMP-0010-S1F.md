# HCT-IMP-0010-S1F — Execution Evidence Bundle

Status: `AUTHOR_PREFLIGHT`
Risk: `HIGH_ASSURANCE`

Prior correction heads: `d0fc7a43a7ca1e94bae3efca0b2007b84b8a0270`, `ae3949514e1bd6163b5abbe9ba0e0e32177dac94`, `a511dfbd0717f6fef5c4cd7a1c21971de6f44458`; final H006R functional correction head: `5227918c644a463a9e28dcf3139f382bdb1e40b7`.

Previous reviewed head for this correction: `07230415a5dc0efff4aa5f4069a19e7d0a97e949`.

This bundle records the author-side correction handoff for IMP-H001 through IMP-H007. Independent review remains required; this status is not approval.

## Context lock

- authorization: `HCT-IMPL-AUTH-0010`;
- authorization checkpoint: `HCT-CP-0031 / IMPLEMENTATION_AUTHORIZED_S1F`;
- authorized execution base: `main@3b972bd7e2016d333fa5d07d8c694a990bd1be88`;
- canonical implementation base: `main@b2a79d1a6096457e9ee209dad218a6eec350c6d6`;
- implementation issue: `#72`;
- implementation branch: `implementation/HCT-IMP-0010-S1F`;
- scope: exactly `HCT-IMP-0010-S1F`;
- production credentials/deployment/limited-live/live-trading: `false`.

## Bounded changed-file manifest

The implementation candidate may contain only the following focused surfaces:

- `adr/HCT-ADR-0050-s1f-realtime-public-market-value-ingest.md`;
- `apps/backend/pyproject.toml` and `apps/backend/uv.lock` for the exact H013 delta only;
- `apps/backend/src/hct_backend/s1f_numeric.py`;
- `apps/backend/src/hct_backend/s1f_values.py`;
- `apps/backend/src/hct_backend/s1f_mexc.py`;
- `apps/backend/src/hct_backend/s1f_session.py`;
- focused S1F tests and pinned fixtures under `apps/backend/tests/`;
- `scripts/scan_s1f_boundaries.py` and `scripts/benchmark_s1f.py`;
- `.github/workflows/s1f-quality.yml`;
- this evidence bundle and deterministic benchmark output under `evidence/benchmarks-s1f-{micro,nominal,stress}.json`.

Checkpoint files, frozen requirements, AUTH-0010 candidate/Work Orders, PR #69, frontend product source and deployment files are outside this manifest.

## Frozen source and dependency lock

The official source is `https://mexcdevelop.github.io/apidocs/contract_v1_en/`, retrieved `2026-09-13`, raw SHA-256 `57ebc13fea788a1c568c8aeabfdf50acc0c9f5b5a882af4855837d53499940e3`, normalized contract `S1F_MEXC_SOURCE_CONTRACT_V1`.

The only runtime dependency delta is `httpx==0.28.1:dev_to_runtime` and `websockets==17.1:add_direct_runtime`; unrelated drift is `STOP_DEPENDENCY_DRIFT`.

Remaining sections are completed only from executed evidence. A green local result or `COMPLETE_CANDIDATE` is not independent approval.

## Normalized MEXC source contract and traceability

`S1F_MEXC_SOURCE_URL=https://mexcdevelop.github.io/apidocs/contract_v1_en/`

`S1F_MEXC_SOURCE_RETRIEVED=2026-09-13`

`S1F_MEXC_SOURCE_SHA256=57ebc13fea788a1c568c8aeabfdf50acc0c9f5b5a882af4855837d53499940e3`

`S1F_MEXC_SOURCE_CONTRACT_VERSION=S1F_MEXC_SOURCE_CONTRACT_V1`

`S1F_MEXC_WS_URL=wss://contract.mexc.com/edge`

`S1F_MEXC_PUBLIC_CHANNELS=sub.tickers,sub.ticker,sub.deal,sub.depth,sub.depth.full,sub.kline`

`S1F_MEXC_AUTHORIZED_PUBLIC_REST=GET /api/v1/contract/depth/{symbol};GET /api/v1/contract/depth_commits/{symbol}/{limit};GET /api/v1/contract/kline/{symbol}`

`S1F_MEXC_NO_OTHER_PUBLIC_ENDPOINTS=ONLY_AUTHORIZED_REST_SET_OR_FUTURE_GOVERNED_SOURCE_CONTRACT_CHANGE_REQUIRED`

The implementation binds the primary matrix as follows: `TradeTick` from `sub.deal`, `TickerState` from `sub.ticker`, bulk ticker as a partial `sub.tickers` capability, `CandleBar` from `sub.kline`, order-book snapshot from REST depth, incremental order-book from `sub.depth` with `compress=false`, bounded full depth from `sub.depth.full`, and reference/funding evidence from `sub.ticker`. Dedicated reference/funding channels remain optional corroboration only.

`S1F_MEXC_DEPTH_TUPLE=price,contract_volume,order_count`; the second tuple element is `QuantityUnit.CONTRACTS_PROVIDER_NATIVE_V1`, the third is order-count metadata, and zero second-element quantity removes a level. Incremental depth requires `next_version=previous_version+1`; discontinuity requires resync. Full-depth limits are exactly `5,10,20` and subscription context is part of identity.

`S1F_MEXC_CANDLE_CLOSE_PROOF=NEXT_WINDOW_OR_REST_CONFIRMATION`; `S1F_MEXC_KLINE_FINAL_FLAG=ABSENT;DO_NOT_FABRICATE`; close proof binds contract, interval, expected half-open window and returned `time` array. Unknown or contradictory payloads quarantine; no missing value becomes zero.

`S1F_MEXC_DECIMAL_PARSE=LEXICAL_PROVIDER_TOKEN_TO_DECIMAL_NO_BINARY_FLOAT`; source fixtures and manifest bind `source_url`, retrieval date, source SHA-256, normalized schema version and fixture SHA-256 `57bbfd602b807361bbc6b60e682adf3731e1a8a42a3330d2c288bdf6584e08fd`.

Traceability is bounded to the authorized work order: R05 transport/feed, backpressure/resource, time/freshness, coherency, candle/cache/replay and authority bullets are implemented in `s1f_session.py`, `s1f_mexc.py`, `s1f_values.py` and `s1f_numeric.py`; INT-002/003/004/011/012/018/022/024/025/026 and VAL-003/005/006/011/012/013/023/028/030 are covered by the typed contracts, quarantine tests, scanner and benchmark; R11-REQ-006/007/011/012/013/014/015/020/022/024/025 remain separated through `ValueContext`, `GenerationRef`, capability state and read-only value objects. HCT-DEC-0007/0008/0012/0058/0060-0065/0068/0069/0071/0074/0077/0079/0083/0084/0089/0135/0136/0138/0139/0140/0141 and ADR-0049 are bound by ADR-0050, the frozen source contract and this evidence bundle.

## Numeric, unit, time and authority firewall

`S1F_NUMERIC_TYPE=Decimal`; `S1F_NUMERIC_POLICY_VERSION=DECIMAL_TEXT_V1`; precision is `38`, scale is `18`, integer digits are `20`; binary float, exponent, non-finite, malformed, negative/impossible and overflow inputs fail closed. Canonical serialization is base-10 without exponent or leading plus; material scale remains in the fingerprint and raw values are never rounded or quantized.

`QuantityUnit.CONTRACTS_PROVIDER_NATIVE_V1` is used by `TradeTick`, book levels, locked ticker volume fields and candle `q`. `CandleBar.a` is `ProviderTransactionAmount`, a distinct type. No implicit base-asset conversion exists; unsupported conversion and mixed-unit series fail closed.

`S1F_INTERVAL_MODEL=HALF_OPEN_START_INCLUSIVE_END_EXCLUSIVE`; timestamps are UTC and Unix-epoch aligned. `knowledge_time`, `event_time`, `wall_receive_time` and monotonic evidence remain distinct. `CandleBar` stays `OPEN` until exact source/finality proof; a late correction requires a new immutable revision, predecessor fingerprint and ordered lineage.

S1E trust, DataAuthority, resource, eligibility and lifecycle remain separate; values carry source/channel/contract/environment/generation/schema/provenance/originating-event identity. No S1F path creates implementation, credential, deployment, limited-live or live-trading authority.

## Runtime dependency and audit evidence

`S1F_RUNTIME_DEPENDENCY_ALLOWLIST=apps/backend/pyproject.toml;apps/backend/uv.lock`

`S1F_RUNTIME_DEPENDENCY_DELTA=httpx==0.28.1:dev_to_runtime;websockets==17.1:add_direct_runtime`

`S1F_RUNTIME_TRANSITIVE_LOCK=unavoidable_deterministic_entries_only`; the lock diff is 33 additions and 2 removals, consisting only of the direct metadata movement/addition and the resolver block for `websockets==17.1`. The direct dependency graph is `fastapi==0.141.1`, `httpx==0.28.1`, `pydantic==2.13.5`, `uvicorn==0.52.4`, `websockets==17.1`; dev tools remain `mypy==2.3.1`, `pytest==9.1.1`, `pytest-cov==7.1.0`, `ruff==0.16.7`.

Package license evidence from the locked environment: `httpx 0.28.1 BSD-3-Clause`, `websockets 17.1 BSD-3-Clause`, `fastapi 0.141.1 MIT`, `pydantic 2.13.5 MIT`, `uvicorn 0.52.4 BSD-3-Clause`; the complete `pip-licenses --format=json --with-urls` result was inspected. `pip-audit==2.10.1 --local` returned `No known vulnerabilities found` in the isolated project environment after updating its audit-tool bootstrap package. Exact local artifact hashes were recorded for the fixture (`57bbfd602b807361bbc6b60e682adf3731e1a8a42a3330d2c288bdf6584e08fd`) and source manifest (`413e9bb8e0d2efa568846aec73815d3b1c513f2023421c498d214ed48375d659`); the functional correction commit above binds the source state.

## Deterministic validation and benchmark evidence

- backend: `301 passed`, global coverage `90.14%` with `--cov-fail-under=90`;
- focused H006R/S1F: `27 passed`; all focused S1F tests PASS;
- Ruff check and format check: PASS for all backend source/tests and S1F scripts;
- mypy strict: PASS for 15 backend source files;
- backend package build: PASS for sdist and wheel (the pre-existing package warning about a missing README does not fail the build);
- negative capability scanner: PASS, four S1F source files, no private/authenticated endpoint, credentials, persistence, mutation, unauthorized URL or infinite reconnect iterator;
- frontend regression: typecheck PASS, 13 tests PASS, ESLint PASS, generated contract format PASS, Vite build PASS, `npm ci` audit reported 0 vulnerabilities.

`S1F_BENCHMARK_MODE=BASELINE_ESTABLISHMENT_V1` ran the exact three profiles with seed `0`, synthetic pinned multichannel fixtures, no live network, normalization/replay throughput, per-event latency distribution, peak/steady memory and bounded queue depth/age. Artifacts are `evidence/benchmarks-s1f-micro.json`, `evidence/benchmarks-s1f-nominal.json` and `evidence/benchmarks-s1f-stress.json`; each reports `correctness=PASS` and `bounded_completion=true`. Artifact SHA-256 values are `micro=fa9b4c293ed2e021d68572b378b92153e76f67fb1528e633db24de08a1bcc280`, `nominal=cb322fe5a659c6fbe20da7dee0378c09a62979a03ef8da45b871acf828085da2`, and `stress=5f8ec9a9ee48468ce4f84a504687502b32a746f3ccb6aba717ae0a31cc845cd8`.

The micro profile produced/admitted/consumed `512/512/512` with `0` drops and maximum queue age `0.117 ms`; nominal produced/admitted/consumed `8192/8192/8192` with `0` drops and maximum queue age `0.2179 ms`; stress produced `65536`, admitted/consumed `12287`, and deterministically dropped `53249` at bounded queue capacity `4096`, with maximum depth `4096` and measured maximum queue age `44062.4342 ms`. This is bounded backpressure evidence, not a product SLO. No product SLO is asserted.

## IMP-H001 through IMP-H007 correction closure

- `IMP-H001`: the WebSocket generation remains active through the open connection, receive loop and heartbeat; retirement occurs on finalization and stale generations are rejected.
- `IMP-H002`: application ping runs on a recurring `15 s` cadence, with `60 s` no-ping ceiling, injected clock/sleeper coverage and cancellation on retirement.
- `IMP-H003`: Module 29 admission is fresh immediately before every HTTP retry, WebSocket connection and staged subscription send; the scanner enforces exactly six WebSocket intents and three REST families.
- `IMP-H004`: REST klines use the official `success/code/data` wrapper and `{time,open,close,high,low,vol,amount}` shape; synthetic shapes are rejected and close proof binds request/window/source/generation context.
- `IMP-H005`: official `depth_commits` has a dedicated decoder, explicit absent provider event time, typed recovery/resync evidence and contiguous delta enforcement.
- `IMP-H006`: DecimalValue is content-bound; OrderedLineage recomputes its manifest; CandleCloseProof is typed and admissible only as `NEXT_WINDOW` or `REST_CONFIRMATION`.
- `IMP-H006R`: `CLOSED_AUTHOR_SIDE_ONLY`; accepted CandleCloseProof instances carry a private evaluator attestation, direct construction and public hash factories are removed, NEXT_WINDOW requires actual compatible next CandleBar evidence, and REST_CONFIRMATION is issued only by the validated official MEXC decoder path.
- `IMP-H007`: benchmark publication is separated from normalization, uses deterministic producer/consumer behavior, measured queue age and explicit producer/consumer/admitted/dropped counters; nominal has no drops and stress records bounded shedding.

The correction is author-side only: `criticalAuthorFindings=0`, `highAuthorFindings=0`; no independent verdict is claimed.

## Author-side findings and stop state

`criticalAuthorFindings=0`

`highAuthorFindings=0`

`implementation_authorized=true` only under `HCT-CP-0031` for `HCT-IMP-0010-S1F`; `production_credentials_authorized=false`; `production_deployment_authorized=false`; `limited_live_authorized=false`; `live_trading_authorized=false`.

This bundle is author-side implementation evidence only. It is not an independent review, GitHub approval, merge authorization, checkpoint-completion promotion or live-trading authorization. The required terminal state is an OPEN, UNMERGED implementation pull request with exact-head `s1f-quality` success and evidence publication, followed by a fresh independent HIGH_ASSURANCE review.
