from dataclasses import FrozenInstanceError, replace
from datetime import UTC, datetime, timedelta

import pytest

from hct_backend.contracts import Environment, EnvironmentScopedId, IdentityKind, StableId
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
from hct_backend.market_universe import UniverseEligibilityState

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
) -> SequenceObservation:
    return SequenceObservation(
        generation=gen or generation(),
        observed_at=observed_at,
        event_fingerprint=(str(number) * 64)[:64],
        update_id=update_id,
        is_snapshot=snapshot,
    )


def event(
    number: int,
    *,
    update_id: int | None = None,
    snapshot: bool = True,
    gen: GenerationRef | None = None,
    event_environment: Environment = Environment.PAPER,
) -> NormalizedMarketEvent:
    current_generation = gen or generation()
    return NormalizedMarketEvent(
        event_id=EnvironmentScopedId(
            kind=IdentityKind.EVIDENCE,
            environment=event_environment,
            value=f"event-{number}",
        ),
        environment=event_environment,
        source_id=SOURCE,
        channel="public-events",
        contract_id=CONTRACT,
        schema_version=1,
        generation=current_generation,
        provenance_fingerprint=PROVENANCE,
        payload_fingerprint=PAYLOAD,
        event_time=NOW + timedelta(milliseconds=number),
        wall_receive_time=NOW + timedelta(milliseconds=number + 1),
        monotonic_elapsed_ms=number,
        update_id=update_id,
        is_snapshot=snapshot,
    )


def resource(
    disposition: ResourceDisposition = ResourceDisposition.AVAILABLE,
) -> ResourceAdmissionEvidence:
    return ResourceAdmissionEvidence(disposition, "fixture-state", SNAPSHOT)


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
        sequence=sequence or SequenceEvaluation(SequenceResultKind.ACCEPT, True),
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
    return DataAuthorityDecision(state, (QualityReason.FRESH_VALID,), tuple(ActionClass), 99)


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
    current_proof = proof or SynchronizationProof(
        SOURCE, current_generation, SequenceMode.STRICT_SEQUENCE, SNAPSHOT, True
    )
    return MarketStateSnapshot(
        contract_id=CONTRACT,
        environment=Environment.PAPER,
        generation=current_generation,
        source_id=SOURCE,
        source_version=1,
        provenance_fingerprint=PROVENANCE,
        event_fingerprints=(PAYLOAD,),
        trust=trust,
        data_authority=authority or decision(),
        synchronized=synchronized,
        synchronization_proof=current_proof,
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
    first = observation(1, update_id=10)
    assert (
        evaluate_sequence(unproven, first, observation(2, update_id=12)).result
        is SequenceResultKind.ACCEPT
    )
    assert (
        evaluate_sequence(proven, first, observation(3, update_id=12)).result
        is SequenceResultKind.GAP
    )
    assert (
        evaluate_sequence(unproven, first, observation(4)).result
        is SequenceResultKind.SEQUENCE_UNPROVABLE
    )


def test_timestamp_ordering_bounds_lateness_without_inventing_gaps() -> None:
    cap = capability(SequenceMode.TIMESTAMP_ORDERED_WITH_LIMITS)
    first = observation(1, observed_at=NOW)
    late = observation(2, observed_at=NOW - timedelta(milliseconds=201))
    assert evaluate_sequence(cap, first, late).result is SequenceResultKind.OUT_OF_ORDER
    within = observation(3, observed_at=NOW - timedelta(milliseconds=100))
    assert evaluate_sequence(cap, first, within).result is SequenceResultKind.ACCEPT


def test_snapshot_only_and_unprovable_modes_never_infer_continuity() -> None:
    snapshot_cap = capability(SequenceMode.SNAPSHOT_ONLY)
    first = observation(1, snapshot=True)
    assert evaluate_sequence(snapshot_cap, None, first).synchronized
    assert (
        evaluate_sequence(snapshot_cap, first, observation(2, snapshot=False)).result
        is SequenceResultKind.SEQUENCE_UNPROVABLE
    )
    no_proof = evaluate_sequence(capability(SequenceMode.NO_PROVABLE_SEQUENCE), None, first)
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
            DataAuthorityState.ALLOW_NEW_EXPOSURE,
            QualityReason.FRESH_VALID,
        ),
    ],
)
def test_resource_seam_can_restrict_but_never_upgrade(
    disposition: ResourceDisposition, expected: DataAuthorityState, reason: QualityReason
) -> None:
    result = derive_data_authority(assessment(disposition=disposition))
    assert result.state is expected
    assert reason in result.reasons


def test_quality_missing_and_safe_action_semantics_are_explicit() -> None:
    result = derive_data_authority(assessment(age_ms=None, freshness_limit_ms=None))
    assert result.state is DataAuthorityState.NO_NEW_EXPOSURE
    assert ActionClass.NEW_EXPOSURE not in result.affected_actions
    assert ActionClass.REDUCE_EXPOSURE in result.affected_actions
    assert set(decision().affected_actions) == set(ActionClass)


def test_trusted_state_requires_verified_synchronization_and_quality() -> None:
    proof = SynchronizationProof(SOURCE, generation(), SequenceMode.STRICT_SEQUENCE, SNAPSHOT, True)
    assert state(proof=proof).trust is MarketStateTrust.TRUSTED
    with pytest.raises(MarketTruthConsistencyError):
        state(synchronized=False, proof=None)
    with pytest.raises(MarketTruthConsistencyError):
        state(authority=decision(DataAuthorityState.NO_NEW_EXPOSURE))
    with pytest.raises(MarketTruthConsistencyError):
        SynchronizationProof(
            StableId(kind=IdentityKind.EXCHANGE, value="other"),
            generation(),
            SequenceMode.STRICT_SEQUENCE,
            SNAPSHOT,
            True,
        )


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
    ineligible = UniverseLifecycleEvidence(
        StableId(kind=IdentityKind.UNIVERSE_SNAPSHOT, value="universe-paper-fixture"),
        CONTRACT,
        1,
        # The exact S1C enum is consumed; S1E does not recreate its owner.
        UniverseEligibilityState.INELIGIBLE,
        ("INELIGIBLE_LIFECYCLE",),
        1,
        SNAPSHOT,
    )
    restricted = apply_universe_lifecycle(trusted, ineligible)
    assert restricted.trust is MarketStateTrust.TRUSTED
    assert restricted.lifecycle_restriction is LifecycleRestriction.NEW_EXPOSURE_DISABLED
    unknown = replace(ineligible, state=UniverseEligibilityState.UNKNOWN)
    assert (
        apply_universe_lifecycle(trusted, unknown).lifecycle_restriction
        is LifecycleRestriction.ELIGIBILITY_UNKNOWN
    )


def test_lifecycle_mismatch_cannot_rewrite_another_contract() -> None:
    evidence = UniverseLifecycleEvidence(
        StableId(kind=IdentityKind.UNIVERSE_SNAPSHOT, value="universe-paper-fixture"),
        CONTRACT,
        1,
        UniverseEligibilityState.ELIGIBLE,
        ("ELIGIBLE_REFERENCE_PROVEN",),
        1,
        SNAPSHOT,
    )
    other = replace(
        state(), contract_id=StableId(kind=IdentityKind.INSTRUMENT, value="eth-usdt-perpetual")
    )
    with pytest.raises(MarketTruthConsistencyError):
        apply_universe_lifecycle(other, evidence)


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
    events = (event(1, update_id=1), event(2, update_id=3), event(3, update_id=2))
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
    with pytest.raises(MarketTruthInputError):
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
