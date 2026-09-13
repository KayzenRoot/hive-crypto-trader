from dataclasses import FrozenInstanceError, replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from hct_backend.contracts import Environment, EnvironmentScopedId, IdentityKind, StableId
from hct_backend.exchange_reference import (
    CapabilityDeclaration,
    CapabilityName,
    CapabilitySnapshot,
    CapabilityState,
    ContractReference,
    ContractType,
    ExchangeDescriptor,
    LifecycleClass,
)
from hct_backend.market_truth import (
    ActionClass,
    ChannelCapability,
    ChannelVisibility,
    ClockHealth,
    DataAuthorityDecision,
    DataAuthorityState,
    GenerationRef,
    LifecycleRestriction,
    MarketStateSnapshot,
    MarketStateTrust,
    MarketTruthConsistencyError,
    MarketTruthInputError,
    NormalizedMarketEvent,
    ProjectionEnvelope,
    ProjectionLease,
    QualityAssessment,
    QualityReason,
    ResourceAdmissionEvidence,
    ResourceDisposition,
    SequenceEvaluation,
    SequenceMode,
    SequenceObservation,
    SequenceResultKind,
    SynchronizationProof,
    UniverseLifecycleEvidence,
    UpdateSemantics,
    accept_market_state,
    apply_universe_lifecycle,
    derive_data_authority,
    evaluate_sequence,
    invalidate_projection,
    project_state,
    replay_sequence,
)
from hct_backend.market_universe import (
    UniverseEligibilityState,
    UniverseReasonCode,
    recompute_universe,
)
from hct_backend.quota_governor import AdmissionDecision, AdmissionOutcome, AdmissionReason

NOW = datetime(2026, 1, 1, 12, 0, tzinfo=UTC)
SOURCE = StableId(kind=IdentityKind.EXCHANGE, value="exchange-reference")
CONTRACT = StableId(kind=IdentityKind.INSTRUMENT, value="btc-usdt-perpetual")
PROVENANCE = "a" * 64
PAYLOAD = "b" * 64
SNAPSHOT = "c" * 64


def generation(number: int = 1, *, retired: bool = False) -> GenerationRef:
    return GenerationRef(SOURCE, Environment.PAPER, number, retired)


def capability(mode: SequenceMode, *, contiguous: bool = False) -> ChannelCapability:
    return ChannelCapability(
        source_id=SOURCE,
        visibility=ChannelVisibility.PUBLIC,
        channel="public-events",
        contract_scope=CONTRACT,
        schema_version=1,
        snapshot_available=True,
        update_semantics=UpdateSemantics.SNAPSHOT_AND_DELTA,
        ordering_evidence="fixture-ordered",
        sequence_field="update-id"
        if mode in (SequenceMode.STRICT_SEQUENCE, SequenceMode.MONOTONIC_UPDATE_ID)
        else None,
        cadence_ms=100,
        heartbeat_ms=500,
        mode=mode,
        contiguous_proof=contiguous,
        timestamp_limit_ms=200 if mode is SequenceMode.TIMESTAMP_ORDERED_WITH_LIMITS else None,
    )


def observation(
    number: int,
    *,
    update_id: int | None = None,
    snapshot: bool = False,
    observed_at: datetime = NOW,
    gen: GenerationRef | None = None,
    cap: ChannelCapability | None = None,
    channel: str = "public-events",
    contract: StableId = CONTRACT,
    source: StableId = SOURCE,
    schema_version: int = 1,
    visibility: ChannelVisibility = ChannelVisibility.PUBLIC,
) -> SequenceObservation:
    current_capability = cap or capability(SequenceMode.STRICT_SEQUENCE)
    return SequenceObservation(
        generation=gen or generation(),
        observed_at=observed_at,
        event_fingerprint=(str(number) * 64)[:64],
        update_id=update_id,
        is_snapshot=snapshot,
        source_id=source,
        channel=channel,
        contract_id=contract,
        schema_version=schema_version,
        capability_fingerprint=current_capability.fingerprint,
        capability_policy_version=current_capability.policy_version,
        visibility=visibility,
    )


def event(
    number: int,
    *,
    update_id: int | None = None,
    snapshot: bool = True,
    gen: GenerationRef | None = None,
    event_environment: Environment = Environment.PAPER,
    cap: ChannelCapability | None = None,
    channel: str = "public-events",
    contract: StableId = CONTRACT,
    source: StableId = SOURCE,
    schema_version: int = 1,
) -> NormalizedMarketEvent:
    current_capability = cap or capability(SequenceMode.STRICT_SEQUENCE)
    current_generation = gen or generation()
    return NormalizedMarketEvent(
        event_id=EnvironmentScopedId(
            kind=IdentityKind.EVIDENCE,
            environment=event_environment,
            value=f"event-{number}",
        ),
        environment=event_environment,
        source_id=source,
        channel=channel,
        contract_id=contract,
        schema_version=schema_version,
        generation=current_generation,
        provenance_fingerprint=PROVENANCE,
        payload_fingerprint=PAYLOAD,
        event_time=NOW + timedelta(milliseconds=number),
        wall_receive_time=NOW + timedelta(milliseconds=number + 1),
        monotonic_elapsed_ms=number,
        capability_fingerprint=current_capability.fingerprint,
        capability_policy_version=current_capability.policy_version,
        update_id=update_id,
        is_snapshot=snapshot,
    )


def healthy_sequence() -> SequenceEvaluation:
    cap = capability(SequenceMode.STRICT_SEQUENCE)
    return evaluate_sequence(cap, None, observation(900, update_id=900, snapshot=True, cap=cap))


def resource(
    disposition: ResourceDisposition = ResourceDisposition.AVAILABLE,
) -> ResourceAdmissionEvidence:
    canonical = {
        ResourceDisposition.AVAILABLE: (AdmissionOutcome.ADMIT, AdmissionReason.ADMITTED),
        ResourceDisposition.DEGRADED: (AdmissionOutcome.DEFER, AdmissionReason.QUEUE_FULL),
        ResourceDisposition.DENIED: (AdmissionOutcome.SHED, AdmissionReason.QUEUE_FULL),
        ResourceDisposition.UNKNOWN: (
            AdmissionOutcome.UNKNOWN,
            AdmissionReason.UNKNOWN_BUDGET,
        ),
    }[disposition]
    decision = AdmissionDecision.create(
        outcome=canonical[0], reason=canonical[1], material={"fixture": disposition.value}
    )
    return ResourceAdmissionEvidence.from_admission(decision)


def assessment(
    *,
    age_ms: int | None = 10,
    freshness_limit_ms: int | None = 100,
    sequence: SequenceEvaluation | None = None,
    clock: ClockHealth = ClockHealth.HEALTHY,
    schema_valid: bool | None = True,
    provenance_valid: bool | None = True,
    generation_valid: bool | None = True,
    coherent: bool | None = True,
    disposition: ResourceDisposition = ResourceDisposition.AVAILABLE,
    contradiction: bool = False,
    score: int | None = 99,
) -> QualityAssessment:
    return QualityAssessment(
        age_ms=age_ms,
        freshness_limit_ms=freshness_limit_ms,
        sequence=sequence or healthy_sequence(),
        clock=clock,
        schema_valid=schema_valid,
        provenance_valid=provenance_valid,
        generation_valid=generation_valid,
        coherent=coherent,
        resource=resource(disposition),
        contradiction=contradiction,
        explanatory_score=score,
    )


def decision(
    state: DataAuthorityState = DataAuthorityState.ALLOW_NEW_EXPOSURE,
) -> DataAuthorityDecision:
    assessments = {
        DataAuthorityState.ALLOW_NEW_EXPOSURE: assessment(),
        DataAuthorityState.DEGRADED_NEW_EXPOSURE: assessment(
            disposition=ResourceDisposition.DEGRADED
        ),
        DataAuthorityState.NO_NEW_EXPOSURE: assessment(provenance_valid=False),
        DataAuthorityState.REDUCE_ONLY: assessment(disposition=ResourceDisposition.DENIED),
        DataAuthorityState.RECONCILIATION_ONLY: assessment(disposition=ResourceDisposition.UNKNOWN),
        DataAuthorityState.EMERGENCY: assessment(schema_valid=False),
    }
    return derive_data_authority(assessments[state])


def universe_snapshot(
    *, lifecycle: LifecycleClass = LifecycleClass.ACTIVE, unknown_capability: bool = False
) -> object:
    exchange = StableId(kind=IdentityKind.EXCHANGE, value="venue-a")
    descriptor = ExchangeDescriptor(
        exchange_id=exchange,
        display_name="Venue A",
        reference_version=1,
        source="declared-reference",
        observed_at=NOW,
        metadata=(("region", "global"),),
    )
    capability_state = CapabilityState.UNKNOWN if unknown_capability else CapabilityState.SUPPORTED
    capabilities = CapabilitySnapshot(
        snapshot_id=StableId(kind=IdentityKind.CAPABILITY_SNAPSHOT, value="cap-1"),
        exchange_id=exchange,
        version=1,
        source="declared-reference",
        observed_at=NOW,
        declarations=tuple(
            CapabilityDeclaration(
                name, capability_state, None if unknown_capability else "catalogue"
            )
            for name in (
                CapabilityName.EXCHANGE_DESCRIPTION,
                CapabilityName.PUBLIC_REFERENCE,
                CapabilityName.CONTRACT_REFERENCE,
            )
        ),
    )
    reference = ContractReference(
        reference_id=StableId(kind=IdentityKind.REFERENCE_SNAPSHOT, value="ref-1"),
        contract_id=CONTRACT,
        exchange_id=exchange,
        native_symbol="BTC_USDT",
        lifecycle=lifecycle,
        contract_type=ContractType.PERPETUAL,
        price_increment=Decimal("0.10"),
        quantity_increment=Decimal("0.001"),
        source="declared-reference",
        observed_at=NOW,
        base_asset="BTC",
        quote_asset="USDT",
        settlement_asset="USDT",
        price_precision=2,
        quantity_precision=3,
        min_quantity=Decimal("0.001"),
        max_quantity=Decimal("100"),
    )
    return recompute_universe(
        descriptor,
        capabilities,
        (reference,),
        environment=Environment.PAPER,
        recomputed_at=NOW,
    )


def state(
    *,
    gen: GenerationRef | None = None,
    trust: MarketStateTrust = MarketStateTrust.TRUSTED,
    authority: DataAuthorityDecision | None = None,
    synchronized: bool = True,
    proof: SynchronizationProof | None = None,
    lifecycle: LifecycleRestriction = LifecycleRestriction.NONE,
) -> MarketStateSnapshot:
    current_generation = gen or generation()
    current_capability = capability(SequenceMode.STRICT_SEQUENCE)
    sync_observation = observation(
        99, update_id=99, snapshot=True, gen=current_generation, cap=current_capability
    )
    sync_evaluation = evaluate_sequence(current_capability, None, sync_observation)
    current_proof = proof or SynchronizationProof.from_sequence_evaluation(
        capability=current_capability,
        generation=current_generation,
        evaluation=sync_evaluation,
    )
    return MarketStateSnapshot(
        contract_id=CONTRACT,
        environment=Environment.PAPER,
        generation=current_generation,
        source_id=SOURCE,
        source_version=1,
        provenance_fingerprint=PROVENANCE,
        event_fingerprints=(
            current_proof.synchronization_anchor_fingerprint,
            current_proof.latest_event_fingerprint,
        ),
        trust=trust,
        data_authority=authority or decision(),
        synchronized=synchronized,
        synchronization_proof=current_proof,
        capability_fingerprint=current_capability.fingerprint,
        capability_policy_version=current_capability.policy_version,
        channel=current_capability.channel,
        schema_version=current_capability.schema_version,
        visibility=current_capability.visibility,
        lifecycle_restriction=lifecycle,
    )


def test_generation_is_environment_scoped_and_retirement_is_fenced() -> None:
    first = generation()
    second = first.rollover(2)
    assert first.fingerprint != second.fingerprint
    assert not first.accepts(second)
    assert second.accepts(GenerationRef(SOURCE, Environment.PAPER, 2))
    assert second.retire().retired
    with pytest.raises(MarketTruthConsistencyError):
        first.rollover(1)
    with pytest.raises(MarketTruthInputError):
        GenerationRef(SOURCE, Environment.LIVE, 0)


@pytest.mark.parametrize(
    "mode",
    [
        SequenceMode.STRICT_SEQUENCE,
        SequenceMode.MONOTONIC_UPDATE_ID,
        SequenceMode.TIMESTAMP_ORDERED_WITH_LIMITS,
        SequenceMode.SNAPSHOT_ONLY,
        SequenceMode.NO_PROVABLE_SEQUENCE,
    ],
)
def test_all_sequence_modes_have_stable_material_fingerprints(mode: SequenceMode) -> None:
    first = capability(mode)
    assert first.fingerprint == capability(mode).fingerprint
    changed = replace(first, policy_version=2)
    assert first.fingerprint != changed.fingerprint


def test_strict_sequence_is_contiguous_and_fail_closed() -> None:
    cap = capability(SequenceMode.STRICT_SEQUENCE)
    first = observation(1, update_id=10, snapshot=True)
    assert evaluate_sequence(cap, None, first).synchronized
    assert (
        evaluate_sequence(cap, first, observation(2, update_id=10)).result
        is SequenceResultKind.DUPLICATE
    )
    assert (
        evaluate_sequence(cap, first, observation(3, update_id=9)).result
        is SequenceResultKind.OUT_OF_ORDER
    )
    gap = evaluate_sequence(cap, first, observation(4, update_id=12))
    assert gap.result is SequenceResultKind.GAP
    assert gap.requires_resynchronization
    accepted = evaluate_sequence(cap, first, observation(5, update_id=11))
    assert accepted.result is SequenceResultKind.ACCEPT


def test_monotonic_update_id_only_calls_jumps_gaps_when_proven() -> None:
    unproven = capability(SequenceMode.MONOTONIC_UPDATE_ID)
    proven = capability(SequenceMode.MONOTONIC_UPDATE_ID, contiguous=True)
    first = observation(1, update_id=10, cap=unproven)
    assert (
        evaluate_sequence(unproven, first, observation(2, update_id=12, cap=unproven)).result
        is SequenceResultKind.SEQUENCE_UNPROVABLE
    )
    proven_first = observation(3, update_id=10, cap=proven)
    assert (
        evaluate_sequence(proven, proven_first, observation(4, update_id=12, cap=proven)).result
        is SequenceResultKind.GAP
    )
    assert (
        evaluate_sequence(unproven, first, observation(5, cap=unproven)).result
        is SequenceResultKind.SEQUENCE_UNPROVABLE
    )


def test_sequence_evaluation_rejects_contradictory_authoritative_material() -> None:
    with pytest.raises(MarketTruthConsistencyError):
        SequenceEvaluation(SequenceResultKind.ACCEPT, True)
    with pytest.raises(MarketTruthConsistencyError):
        SequenceEvaluation(SequenceResultKind.ACCEPT, True, None)
    with pytest.raises(MarketTruthConsistencyError):
        SequenceEvaluation(SequenceResultKind.DUPLICATE, True, QualityReason.DUPLICATE)
    with pytest.raises(MarketTruthConsistencyError):
        SequenceEvaluation(SequenceResultKind.GAP, True, QualityReason.GAP)
    with pytest.raises(MarketTruthConsistencyError):
        SequenceEvaluation(SequenceResultKind.ACCEPT, True, QualityReason.GAP)
    with pytest.raises(MarketTruthConsistencyError):
        SequenceEvaluation(
            SequenceResultKind.SEQUENCE_UNPROVABLE,
            True,
            QualityReason.SEQUENCE_UNPROVABLE,
        )


def test_unproven_sequence_cannot_create_authority_and_snapshot_recovers() -> None:
    cap = capability(SequenceMode.STRICT_SEQUENCE)
    first_delta = observation(1, update_id=10, cap=cap)
    unsynchronized = evaluate_sequence(cap, None, first_delta)
    assert unsynchronized.result is SequenceResultKind.ACCEPT
    assert not unsynchronized.synchronized
    assert unsynchronized.reason is QualityReason.UNSYNCHRONIZED
    assert (
        derive_data_authority(assessment(sequence=unsynchronized)).state
        is DataAuthorityState.NO_NEW_EXPOSURE
    )
    snapshot = observation(2, update_id=11, snapshot=True, cap=cap)
    recovered = evaluate_sequence(cap, first_delta, snapshot)
    assert recovered.result is SequenceResultKind.ACCEPT
    assert recovered.synchronized


def test_h007_snapshot_multi_delta_continuity_persists_and_replay_matches() -> None:
    cap = capability(SequenceMode.STRICT_SEQUENCE)
    observations = tuple(
        observation(
            number,
            update_id=update_id,
            snapshot=number == 10,
            cap=cap,
        )
        for number, update_id in ((10, 10), (11, 11), (12, 12), (13, 13))
    )
    previous: SequenceObservation | None = None
    continuity = None
    direct: list[SequenceEvaluation] = []
    for current in observations:
        result = evaluate_sequence(cap, previous, current, continuity)
        direct.append(result)
        assert result.synchronized
        previous = current
        continuity = result.continuity
    replay = replay_sequence(
        cap,
        tuple(
            event(number, update_id=update_id, snapshot=number == 10, cap=cap)
            for number, update_id in ((10, 10), (11, 11), (12, 12), (13, 13))
        ),
    )
    assert all(result.synchronized for result in replay)
    assert [result.result for result in replay] == [result.result for result in direct]


def test_h007_gap_clears_continuity_until_explicit_snapshot_resync() -> None:
    cap = capability(SequenceMode.STRICT_SEQUENCE)
    snapshot = observation(10, update_id=10, snapshot=True, cap=cap)
    delta = observation(11, update_id=11, cap=cap)
    gap = observation(13, update_id=13, cap=cap)
    next_delta = observation(12, update_id=12, cap=cap)
    resync = observation(20, update_id=20, snapshot=True, cap=cap)

    first = evaluate_sequence(cap, None, snapshot)
    second = evaluate_sequence(cap, snapshot, delta, first.continuity)
    broken = evaluate_sequence(cap, delta, gap, second.continuity)
    assert second.synchronized
    assert broken.result is SequenceResultKind.GAP
    assert not broken.synchronized
    after_gap = evaluate_sequence(cap, delta, next_delta, broken.continuity)
    assert after_gap.result is SequenceResultKind.ACCEPT
    assert not after_gap.synchronized
    recovered = evaluate_sequence(cap, next_delta, resync, after_gap.continuity)
    assert recovered.result is SequenceResultKind.ACCEPT
    assert recovered.synchronized


def test_h007_monotonic_continuity_and_unproven_jump_are_fail_closed() -> None:
    proven = capability(SequenceMode.MONOTONIC_UPDATE_ID, contiguous=True)
    first = observation(10, update_id=10, snapshot=True, cap=proven)
    first_result = evaluate_sequence(proven, None, first)
    second_result = evaluate_sequence(
        proven, first, observation(11, update_id=11, cap=proven), first_result.continuity
    )
    third_result = evaluate_sequence(
        proven,
        observation(11, update_id=11, cap=proven),
        observation(12, update_id=12, cap=proven),
        second_result.continuity,
    )
    assert third_result.synchronized
    jumped = evaluate_sequence(
        proven,
        observation(12, update_id=12, cap=proven),
        observation(14, update_id=14, cap=proven),
        third_result.continuity,
    )
    assert jumped.result is SequenceResultKind.GAP
    assert not jumped.synchronized

    unproven = capability(SequenceMode.MONOTONIC_UPDATE_ID)
    unproven_first = observation(10, update_id=10, snapshot=True, cap=unproven)
    unproven_state = evaluate_sequence(unproven, None, unproven_first)
    unproven_jump = evaluate_sequence(
        unproven,
        unproven_first,
        observation(12, update_id=12, cap=unproven),
        unproven_state.continuity,
    )
    assert unproven_jump.result is SequenceResultKind.SEQUENCE_UNPROVABLE
    assert not unproven_jump.synchronized


def test_h011_synchronized_evaluations_require_evaluator_attested_continuity() -> None:
    cap = capability(SequenceMode.STRICT_SEQUENCE)
    snapshot = observation(10, update_id=10, snapshot=True, cap=cap)
    evaluation = evaluate_sequence(cap, None, snapshot)
    assert evaluation.continuity is not None
    assert evaluation.continuity.synchronization_anchor_fingerprint == snapshot.event_fingerprint
    with pytest.raises(MarketTruthConsistencyError):
        SequenceEvaluation(SequenceResultKind.ACCEPT, True, continuity=None)
    with pytest.raises(MarketTruthConsistencyError):
        SequenceEvaluation(SequenceResultKind.DUPLICATE, True, QualityReason.DUPLICATE)
    healthy = derive_data_authority(assessment(sequence=evaluation))
    assert healthy.state is DataAuthorityState.ALLOW_NEW_EXPOSURE


def test_h011_quality_assessment_rejects_unattested_synchronized_sequence() -> None:
    forged = object.__new__(SequenceEvaluation)
    object.__setattr__(forged, "result", SequenceResultKind.ACCEPT)
    object.__setattr__(forged, "synchronized", True)
    object.__setattr__(forged, "reason", None)
    object.__setattr__(forged, "continuity", None)
    object.__setattr__(forged, "_attestation", None)
    with pytest.raises(MarketTruthConsistencyError):
        assessment(sequence=forged)


def test_timestamp_ordering_bounds_lateness_without_inventing_gaps() -> None:
    cap = capability(SequenceMode.TIMESTAMP_ORDERED_WITH_LIMITS)
    first = observation(1, observed_at=NOW, cap=cap)
    late = observation(2, observed_at=NOW - timedelta(milliseconds=201), cap=cap)
    assert evaluate_sequence(cap, first, late).result is SequenceResultKind.OUT_OF_ORDER
    within = observation(3, observed_at=NOW - timedelta(milliseconds=100), cap=cap)
    assert evaluate_sequence(cap, first, within).result is SequenceResultKind.SEQUENCE_UNPROVABLE
    assert not evaluate_sequence(cap, first, within).synchronized


def test_snapshot_only_and_unprovable_modes_never_infer_continuity() -> None:
    snapshot_cap = capability(SequenceMode.SNAPSHOT_ONLY)
    first = observation(1, snapshot=True, cap=snapshot_cap)
    assert evaluate_sequence(snapshot_cap, None, first).synchronized
    assert (
        evaluate_sequence(
            snapshot_cap, first, observation(2, snapshot=False, cap=snapshot_cap)
        ).result
        is SequenceResultKind.SEQUENCE_UNPROVABLE
    )
    no_proof_cap = capability(SequenceMode.NO_PROVABLE_SEQUENCE)
    no_proof = evaluate_sequence(
        no_proof_cap, None, observation(2, snapshot=True, cap=no_proof_cap)
    )
    assert no_proof.result is SequenceResultKind.SEQUENCE_UNPROVABLE
    assert not no_proof.synchronized


def test_generation_mismatch_and_retired_evidence_require_resync() -> None:
    cap = capability(SequenceMode.STRICT_SEQUENCE)
    first = observation(1, update_id=1)
    mismatched = observation(2, update_id=2, gen=generation(2))
    assert evaluate_sequence(cap, first, mismatched).result is SequenceResultKind.RESYNC_REQUIRED
    retired = observation(3, update_id=3, gen=generation(1, retired=True))
    assert evaluate_sequence(cap, None, retired).reason is QualityReason.RETIRED_GENERATION


def test_normalized_event_identity_time_axes_and_fingerprint() -> None:
    first = event(1, update_id=1)
    assert first.fingerprint == event(1, update_id=1).fingerprint
    assert first.fingerprint != event(2, update_id=1).fingerprint
    assert first.sequence_observation().event_fingerprint == first.fingerprint
    with pytest.raises(FrozenInstanceError):
        first.channel = "changed"  # type: ignore[misc]
    with pytest.raises(MarketTruthConsistencyError):
        event(3, event_environment=Environment.LIVE)


def test_event_rejects_wrong_identity_provenance_and_generation() -> None:
    with pytest.raises(MarketTruthInputError):
        replace(event(1), contract_id=SOURCE)
    retired = replace(event(1), generation=generation(1).retire())
    assert (
        evaluate_sequence(
            capability(SequenceMode.STRICT_SEQUENCE), None, retired.sequence_observation()
        ).result
        is SequenceResultKind.RESYNC_REQUIRED
    )
    with pytest.raises(MarketTruthInputError):
        replace(event(1), provenance_fingerprint="bad")


def test_sequence_identity_is_bound_to_channel_contract_visibility_and_capability() -> None:
    eth = StableId(kind=IdentityKind.INSTRUMENT, value="eth-usdt-perpetual")
    eth_capability = replace(capability(SequenceMode.STRICT_SEQUENCE), contract_scope=eth)
    with pytest.raises(MarketTruthConsistencyError):
        evaluate_sequence(eth_capability, None, event(1, cap=eth_capability).sequence_observation())

    private = replace(
        capability(SequenceMode.STRICT_SEQUENCE), visibility=ChannelVisibility.PRIVATE
    )
    with pytest.raises(MarketTruthConsistencyError):
        evaluate_sequence(private, None, event(2, cap=private).sequence_observation())

    other_channel = replace(capability(SequenceMode.STRICT_SEQUENCE), channel="other-channel")
    with pytest.raises(MarketTruthConsistencyError):
        evaluate_sequence(other_channel, None, event(3, cap=other_channel).sequence_observation())

    with pytest.raises(MarketTruthConsistencyError):
        event(4, source=StableId(kind=IdentityKind.EXCHANGE, value="other-venue"))

    schema_two = replace(capability(SequenceMode.STRICT_SEQUENCE), schema_version=2)
    with pytest.raises(MarketTruthConsistencyError):
        evaluate_sequence(schema_two, None, event(5, cap=schema_two).sequence_observation())

    first = event(6).sequence_observation()
    policy_two = replace(capability(SequenceMode.STRICT_SEQUENCE), policy_version=2)
    changed_policy = event(7, cap=policy_two).sequence_observation()
    with pytest.raises(MarketTruthConsistencyError):
        evaluate_sequence(capability(SequenceMode.STRICT_SEQUENCE), first, changed_policy)


def test_replay_rejects_mixed_identity_before_sequence_semantics() -> None:
    first = event(1)
    mixed = replace(event(2), channel="other-channel")
    with pytest.raises(MarketTruthConsistencyError):
        replay_sequence(capability(SequenceMode.STRICT_SEQUENCE), (first, mixed))


@pytest.mark.parametrize(
    "kwargs,reason",
    [
        ({"age_ms": 101}, QualityReason.STALE),
        ({"age_ms": 201}, QualityReason.EXPIRED),
        (
            {"sequence": SequenceEvaluation(SequenceResultKind.GAP, False, QualityReason.GAP)},
            QualityReason.GAP,
        ),
        ({"clock": ClockHealth.DRIFT}, QualityReason.CLOCK_DRIFT),
        ({"clock": ClockHealth.JUMP}, QualityReason.CLOCK_JUMP),
        ({"clock": ClockHealth.UNTRUSTED}, QualityReason.CLOCK_UNTRUSTED),
    ],
)
def test_quality_predicates_are_individually_visible(
    kwargs: dict[str, object], reason: QualityReason
) -> None:
    result = derive_data_authority(assessment(**kwargs))  # type: ignore[arg-type]
    assert reason in result.reasons
    assert result.restrictive_only


def test_quality_critical_predicates_dominate_explanatory_score() -> None:
    assert (
        derive_data_authority(assessment(schema_valid=False, score=100)).state
        is DataAuthorityState.EMERGENCY
    )
    assert (
        derive_data_authority(assessment(contradiction=True, score=100)).state
        is DataAuthorityState.EMERGENCY
    )
    assert (
        derive_data_authority(assessment(provenance_valid=False)).state
        is DataAuthorityState.NO_NEW_EXPOSURE
    )
    assert (
        derive_data_authority(assessment(generation_valid=None)).state
        is DataAuthorityState.NO_NEW_EXPOSURE
    )
    assert derive_data_authority(assessment(coherent=False)).state is DataAuthorityState.EMERGENCY


@pytest.mark.parametrize(
    "disposition,expected,reason",
    [
        (
            ResourceDisposition.UNKNOWN,
            DataAuthorityState.RECONCILIATION_ONLY,
            QualityReason.RESOURCE_UNKNOWN,
        ),
        (
            ResourceDisposition.DENIED,
            DataAuthorityState.REDUCE_ONLY,
            QualityReason.RESOURCE_STARVATION,
        ),
        (
            ResourceDisposition.DEGRADED,
            DataAuthorityState.DEGRADED_NEW_EXPOSURE,
            QualityReason.RESOURCE_DEGRADED,
        ),
    ],
)
def test_resource_seam_can_restrict_but_never_upgrade(
    disposition: ResourceDisposition, expected: DataAuthorityState, reason: QualityReason
) -> None:
    result = derive_data_authority(assessment(disposition=disposition))
    assert result.state is expected
    assert reason in result.reasons


def test_resource_degradation_cannot_upgrade_stricter_quality() -> None:
    result = derive_data_authority(
        assessment(
            disposition=ResourceDisposition.DEGRADED,
            sequence=SequenceEvaluation(SequenceResultKind.GAP, False, QualityReason.GAP),
        )
    )
    assert result.state is DataAuthorityState.NO_NEW_EXPOSURE
    assert result.allowed_actions == ()
    available = derive_data_authority(
        assessment(
            disposition=ResourceDisposition.AVAILABLE,
            sequence=SequenceEvaluation(SequenceResultKind.GAP, False, QualityReason.GAP),
        )
    )
    assert available.state is DataAuthorityState.NO_NEW_EXPOSURE


def test_quality_missing_and_safe_action_semantics_are_explicit() -> None:
    result = derive_data_authority(assessment(age_ms=None, freshness_limit_ms=None))
    assert result.state is DataAuthorityState.NO_NEW_EXPOSURE
    assert ActionClass.NEW_EXPOSURE in result.affected_actions
    assert ActionClass.REDUCE_EXPOSURE not in result.affected_actions
    assert decision().affected_actions == ()
    assert decision(DataAuthorityState.EMERGENCY).allowed_actions == ()


def test_data_authority_direct_construction_is_rejected() -> None:
    with pytest.raises(MarketTruthInputError):
        DataAuthorityDecision(
            DataAuthorityState.ALLOW_NEW_EXPOSURE,
            (QualityReason.FRESH_VALID,),
            tuple(ActionClass),
            99,
        )


def test_trusted_state_requires_verified_synchronization_and_quality() -> None:
    assert state().trust is MarketStateTrust.TRUSTED
    with pytest.raises(MarketTruthInputError):
        SynchronizationProof(SOURCE, generation(), SequenceMode.STRICT_SEQUENCE, SNAPSHOT, True)
    with pytest.raises(MarketTruthConsistencyError):
        state(synchronized=False, proof=None)
    with pytest.raises(MarketTruthConsistencyError):
        state(authority=decision(DataAuthorityState.NO_NEW_EXPOSURE))
    with pytest.raises(MarketTruthInputError):
        SynchronizationProof(
            StableId(kind=IdentityKind.EXCHANGE, value="other"),
            generation(),
            SequenceMode.STRICT_SEQUENCE,
            SNAPSHOT,
            True,
        )


@pytest.mark.parametrize(
    "assessment_kwargs",
    [
        {"age_ms": 101},
        {
            "sequence": SequenceEvaluation(
                SequenceResultKind.DUPLICATE, False, QualityReason.DUPLICATE
            )
        },
        {"clock": ClockHealth.DRIFT},
    ],
)
def test_h008_market_truth_degradation_cannot_be_trusted(
    assessment_kwargs: dict[str, object],
) -> None:
    authority = derive_data_authority(assessment(**assessment_kwargs))  # type: ignore[arg-type]
    assert any(
        reason in authority.reasons
        for reason in (QualityReason.STALE, QualityReason.DUPLICATE, QualityReason.CLOCK_DRIFT)
    )
    with pytest.raises(MarketTruthConsistencyError):
        state(authority=authority)


def test_h008_resource_only_degradation_can_coexist_with_trusted_market_data() -> None:
    authority = derive_data_authority(assessment(disposition=ResourceDisposition.DEGRADED))
    trusted = state(authority=authority)
    assert trusted.trust is MarketStateTrust.TRUSTED
    assert QualityReason.RESOURCE_DEGRADED in authority.reasons


def test_h008_factory_proof_binds_generation_and_capability_context() -> None:
    cap = capability(SequenceMode.STRICT_SEQUENCE)
    current = observation(1, update_id=1, snapshot=True, cap=cap)
    evaluation = evaluate_sequence(cap, None, current)
    proof = SynchronizationProof.from_sequence_evaluation(
        capability=cap,
        generation=current.generation,
        evaluation=evaluation,
    )
    assert proof.verified
    assert proof.contract_id == CONTRACT
    assert proof.channel == cap.channel
    assert proof.schema_version == cap.schema_version
    assert proof.visibility is cap.visibility
    with pytest.raises(MarketTruthConsistencyError):
        state(gen=generation(2), proof=proof)


def test_h012_proof_binds_contract_channel_schema_visibility_and_event_lineage() -> None:
    valid = state()
    with pytest.raises(MarketTruthConsistencyError):
        replace(
            valid,
            contract_id=StableId(kind=IdentityKind.INSTRUMENT, value="eth-usdt-perpetual"),
        )
    with pytest.raises(MarketTruthConsistencyError):
        replace(valid, channel="other-channel")
    with pytest.raises(MarketTruthConsistencyError):
        replace(valid, schema_version=2)
    with pytest.raises(MarketTruthConsistencyError):
        replace(valid, visibility=ChannelVisibility.PRIVATE)
    with pytest.raises(MarketTruthConsistencyError):
        replace(valid, capability_fingerprint="d" * 64)
    with pytest.raises(MarketTruthConsistencyError):
        replace(valid, capability_policy_version=2)

    cap = capability(SequenceMode.STRICT_SEQUENCE)
    snapshot = observation(10, update_id=10, snapshot=True, cap=cap)
    delta_one = observation(11, update_id=11, cap=cap)
    delta_two = observation(12, update_id=12, cap=cap)
    first = evaluate_sequence(cap, None, snapshot)
    second = evaluate_sequence(cap, snapshot, delta_one, first.continuity)
    third = evaluate_sequence(cap, delta_one, delta_two, second.continuity)
    proof = SynchronizationProof.from_sequence_evaluation(
        capability=cap, generation=delta_two.generation, evaluation=third
    )
    assert proof.synchronization_anchor_fingerprint == snapshot.event_fingerprint
    assert proof.latest_event_fingerprint == delta_two.event_fingerprint
    assert proof.synchronization_anchor_fingerprint != proof.latest_event_fingerprint
    coherent = replace(
        valid,
        synchronization_proof=proof,
        event_fingerprints=(
            proof.synchronization_anchor_fingerprint,
            proof.latest_event_fingerprint,
        ),
    )
    assert coherent.synchronization_proof is proof
    with pytest.raises(MarketTruthConsistencyError):
        replace(
            coherent,
            event_fingerprints=(proof.synchronization_anchor_fingerprint,),
        )


def test_h012_retired_generation_and_cross_context_proofs_fail_closed() -> None:
    cap = capability(SequenceMode.STRICT_SEQUENCE)
    snapshot = observation(1, update_id=1, snapshot=True, cap=cap)
    evaluation = evaluate_sequence(cap, None, snapshot)
    with pytest.raises(MarketTruthConsistencyError):
        SynchronizationProof.from_sequence_evaluation(
            capability=cap,
            generation=snapshot.generation.retire(),
            evaluation=evaluation,
        )


def test_h009_projection_constructor_and_upgrade_paths_are_closed() -> None:
    with pytest.raises(MarketTruthInputError):
        ProjectionEnvelope(
            SOURCE,
            generation(),
            SNAPSHOT,
            PROVENANCE,
            MarketStateTrust.TRUSTED,
            DataAuthorityState.ALLOW_NEW_EXPOSURE,
            ProjectionLease(1, 10),
            LifecycleRestriction.NONE,
        )
    projection = project_state(state(), issued_elapsed_ms=1, ttl_ms=10)
    assert projection.state_fingerprint == state().fingerprint
    assert projection.trust is MarketStateTrust.TRUSTED
    with pytest.raises(MarketTruthInputError):
        replace(projection, trust=MarketStateTrust.TRUSTED)
    invalidated = invalidate_projection(projection, "expired-fixture")
    assert invalidated.trust is projection.trust
    assert invalidated.data_authority is projection.data_authority
    assert invalidated.state_fingerprint == projection.state_fingerprint
    assert not invalidated.fresh_at(1)


@pytest.mark.parametrize(
    "outcome,reason,expected",
    [
        (AdmissionOutcome.ADMIT, AdmissionReason.ADMITTED, ResourceDisposition.AVAILABLE),
        (AdmissionOutcome.DEFER, AdmissionReason.QUEUE_FULL, ResourceDisposition.DEGRADED),
        (AdmissionOutcome.SHED, AdmissionReason.QUEUE_FULL, ResourceDisposition.DENIED),
        (AdmissionOutcome.CIRCUIT_OPEN, AdmissionReason.CIRCUIT_OPEN, ResourceDisposition.DENIED),
        (AdmissionOutcome.UNKNOWN, AdmissionReason.UNKNOWN_BUDGET, ResourceDisposition.UNKNOWN),
    ],
)
def test_h010_canonical_governor_evidence_mapping(
    outcome: AdmissionOutcome, reason: AdmissionReason, expected: ResourceDisposition
) -> None:
    decision_value = AdmissionDecision.create(
        outcome=outcome, reason=reason, material={"h010": outcome.value}
    )
    evidence = ResourceAdmissionEvidence.from_admission(decision_value)
    assert evidence.disposition is expected
    assert evidence.admission_fingerprint == decision_value.fingerprint
    assert evidence.admission_outcome is outcome
    assert evidence.admission_reason is reason


def test_h010_resource_evidence_direct_and_lookalike_construction_are_rejected() -> None:
    with pytest.raises(MarketTruthInputError):
        ResourceAdmissionEvidence(ResourceDisposition.AVAILABLE, "arbitrary", SNAPSHOT)

    class LookalikeAdmission:
        outcome = AdmissionOutcome.ADMIT
        reason = AdmissionReason.ADMITTED
        fingerprint = SNAPSHOT

    with pytest.raises(MarketTruthInputError):
        ResourceAdmissionEvidence.from_admission(LookalikeAdmission())  # type: ignore[arg-type]


def test_h010_available_resource_cannot_upgrade_market_truth_restriction() -> None:
    gap = SequenceEvaluation(SequenceResultKind.GAP, False, QualityReason.GAP)
    expired = derive_data_authority(
        assessment(age_ms=201, disposition=ResourceDisposition.AVAILABLE)
    )
    emergency = derive_data_authority(
        assessment(schema_valid=False, disposition=ResourceDisposition.AVAILABLE)
    )
    for authority in (
        derive_data_authority(assessment(sequence=gap, disposition=ResourceDisposition.AVAILABLE)),
        expired,
        emergency,
    ):
        assert authority.state is not DataAuthorityState.ALLOW_NEW_EXPOSURE
        with pytest.raises(MarketTruthConsistencyError):
            state(authority=authority)


def test_market_state_fingerprint_includes_generation_trust_and_lifecycle() -> None:
    first = state()
    assert first.fingerprint != state(gen=generation(2)).fingerprint
    restricted = replace(first, lifecycle_restriction=LifecycleRestriction.NEW_EXPOSURE_DISABLED)
    assert first.fingerprint != restricted.fingerprint


def test_generation_firewall_rejects_retired_and_late_states() -> None:
    current = state(gen=generation(2))
    with pytest.raises(MarketTruthConsistencyError):
        accept_market_state(current, state(gen=generation(1, retired=True)))
    with pytest.raises(MarketTruthConsistencyError):
        accept_market_state(current, state(gen=generation(1)))
    unsynchronized_new = state(
        gen=generation(3), synchronized=False, proof=None, trust=MarketStateTrust.RESYNC_REQUIRED
    )
    with pytest.raises(MarketTruthConsistencyError):
        accept_market_state(current, unsynchronized_new)
    accepted = accept_market_state(current, state(gen=generation(2)))
    assert accepted.generation.number == 2


def test_lifecycle_restriction_is_separate_from_market_trust() -> None:
    trusted = state()
    ineligible = UniverseLifecycleEvidence.from_snapshot(
        universe_snapshot(lifecycle=LifecycleClass.INACTIVE), CONTRACT
    )
    restricted = apply_universe_lifecycle(trusted, ineligible)
    assert restricted.trust is MarketStateTrust.TRUSTED
    assert restricted.lifecycle_restriction is LifecycleRestriction.NEW_EXPOSURE_DISABLED
    unknown = UniverseLifecycleEvidence.from_snapshot(
        universe_snapshot(unknown_capability=True), CONTRACT
    )
    assert (
        apply_universe_lifecycle(trusted, unknown).lifecycle_restriction
        is LifecycleRestriction.ELIGIBILITY_UNKNOWN
    )


def test_lifecycle_evidence_binds_to_the_canonical_s1c_entry() -> None:
    snapshot = universe_snapshot()
    canonical = snapshot.entries[0]
    evidence = UniverseLifecycleEvidence.from_entry(snapshot, canonical)
    assert evidence == UniverseLifecycleEvidence.from_snapshot(snapshot, CONTRACT)
    forged_state = replace(
        canonical,
        state=UniverseEligibilityState.INELIGIBLE,
        reason_codes=(UniverseReasonCode.INELIGIBLE_LIFECYCLE,),
    )
    with pytest.raises(MarketTruthConsistencyError):
        UniverseLifecycleEvidence.from_entry(snapshot, forged_state)
    forged_reference = replace(canonical, reference_fingerprint="d" * 64)
    with pytest.raises(MarketTruthConsistencyError):
        UniverseLifecycleEvidence.from_entry(snapshot, forged_reference)
    with pytest.raises(MarketTruthConsistencyError):
        UniverseLifecycleEvidence.from_snapshot(
            snapshot,
            StableId(kind=IdentityKind.INSTRUMENT, value="missing-contract"),
        )


def test_lifecycle_evidence_direct_construction_is_rejected() -> None:
    with pytest.raises(MarketTruthInputError):
        UniverseLifecycleEvidence(
            StableId(kind=IdentityKind.UNIVERSE_SNAPSHOT, value="forged"),
            CONTRACT,
            1,
            UniverseEligibilityState.ELIGIBLE,
            ("ELIGIBLE_REFERENCE_PROVEN",),
            1,
            SNAPSHOT,
            SNAPSHOT,
        )


def test_lifecycle_mismatch_cannot_rewrite_another_contract() -> None:
    with pytest.raises(MarketTruthConsistencyError):
        replace(
            state(),
            contract_id=StableId(kind=IdentityKind.INSTRUMENT, value="eth-usdt-perpetual"),
        )


def test_projection_has_lease_invalidation_and_no_reverse_authority_path() -> None:
    projection = project_state(
        state(lifecycle=LifecycleRestriction.NEW_EXPOSURE_DISABLED), issued_elapsed_ms=10, ttl_ms=20
    )
    assert projection.fresh_at(10)
    assert not projection.fresh_at(30)
    invalid = invalidate_projection(projection, "stale-fixture")
    assert not invalid.fresh_at(10)
    assert invalid.lease.invalidation_reason == "stale-fixture"
    with pytest.raises(MarketTruthConsistencyError):
        ProjectionLease(1, 10, True)


def test_replay_is_deterministic_and_only_advances_on_accepted_evidence() -> None:
    cap = capability(SequenceMode.STRICT_SEQUENCE)
    events = (
        event(1, update_id=1, snapshot=True),
        event(2, update_id=3, snapshot=False),
        event(3, update_id=2, snapshot=False),
    )
    first = replay_sequence(cap, events)
    second = replay_sequence(cap, events)
    assert first == second
    assert first[1].result is SequenceResultKind.GAP
    assert first[2].result is SequenceResultKind.ACCEPT


def test_invalid_capability_and_assessment_boundaries_fail_closed() -> None:
    with pytest.raises(MarketTruthConsistencyError):
        replace(capability(SequenceMode.SNAPSHOT_ONLY), snapshot_available=False)
    with pytest.raises(MarketTruthInputError):
        ResourceAdmissionEvidence(ResourceDisposition.AVAILABLE, "bad reason", "bad")
    with pytest.raises(MarketTruthConsistencyError):
        QualityAssessment(
            0,
            1,
            SequenceEvaluation(SequenceResultKind.ACCEPT, True),
            ClockHealth.HEALTHY,
            True,
            True,
            True,
            True,
            resource(),
            explanatory_score=101,
        )
