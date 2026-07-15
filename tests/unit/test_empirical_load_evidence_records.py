from dataclasses import FrozenInstanceError, replace
import math

import pytest

from modern_powley.modernized.empirical_load_records import (
    EMPIRICAL_LOAD_EVIDENCE_SCHEMA_ID,
    ActivationState,
    AggregateOrigin,
    AggregateStatistic,
    AggregateSummaryRecord,
    ArtifactReference,
    ArtifactRetentionState,
    ChronographSeriesRecord,
    ComponentKind,
    ConflictGroup,
    EmpiricalRecordType,
    EquipmentIdentity,
    EquipmentKind,
    EvidenceUncertainty,
    EvidenceUncertaintyKind,
    ExactRecordReference,
    ExcludedWindow,
    Exclusion,
    ExclusionState,
    LineageLink,
    LiteralLoadStatementRecord,
    LoadSeriesRecord,
    MissingValue,
    ObservationLevel,
    OrderedMember,
    PhysicalLoadConfigurationRecord,
    PhysicalQuantityEvidence,
    PowderIdentityReference,
    PrecisionKind,
    PressureAcquisitionState,
    PressureLocation,
    PressureObservation,
    PressureOrigin,
    PressureQuantity,
    PressureTraceMetadataRecord,
    PressureUnit,
    QuantityOrMissing,
    RecordEnvelope,
    ReferenceOrMissing,
    ReferenceRole,
    ReportedPrecision,
    ReportedValue,
    ReportedValueKind,
    ReviewContext,
    ReviewState,
    ScopedComponentIdentity,
    ShotObservationRecord,
    SourceCustodyRecord,
    SourceDeclarationState,
    TraceArtifactState,
    VelocityCorrectionState,
    VelocityObservation,
    VelocityQuantity,
    VelocityUnit,
)
from modern_powley.modernized.missing_values import IdentityQualifier, MissingState
from modern_powley.modernized.property_observations import SourceLocator, TranscriptionStatus
from modern_powley.modernized.provenance import EvidenceClass, ModelMaturity
from modern_powley.modernized.uncertainty import Uncertainty
from modern_powley.modernized.units import Quantity, Unit


def present(value="SYN-ELE-VALUE"):
    return IdentityQualifier.present(value)


def missing(state=MissingState.UNKNOWN, explanation="synthetic field is explicitly unknown"):
    return IdentityQualifier.missing(state, explanation)


def ref(
    role=ReferenceRole.SOURCE,
    record_type="synthetic_record",
    record_id="SYN-ELE-REF-1",
    schema_id="synthetic.schema.v1",
    version=1,
):
    return ExactRecordReference(
        schema_id=schema_id,
        record_type=record_type,
        record_id=record_id,
        version=version,
        role=role,
    )


def missing_value(state=MissingState.NOT_MEASURED):
    return MissingValue(state=state, explanation="synthetic missing evidence")


def ref_or_missing(reference=None, state=MissingState.NOT_REPORTED if hasattr(MissingState, "NOT_REPORTED") else MissingState.NOT_SUPPLIED_BY_SOURCE):
    if reference is not None:
        return ReferenceOrMissing(reference=reference, missing=None)
    return ReferenceOrMissing(reference=None, missing=missing_value(state))


def precision(kind=PrecisionKind.EXACT_AS_REPORTED, digits=None):
    return ReportedPrecision(kind=kind, statement="synthetic printed precision", digits=digits)


def evidence_uncertainty(kind=EvidenceUncertaintyKind.UNKNOWN, reference=None):
    return EvidenceUncertainty(kind=kind, description="synthetic uncertainty declaration", reference=reference)


def reported(kind, decimal="1.2340", unit="SYN-UNIT", **changes):
    values = dict(
        kind=kind,
        decimal_text=decimal,
        source_unit_label=unit,
        source_wording=f"synthetic reported {decimal} {unit}",
        precision=precision(PrecisionKind.DECIMAL_PLACES, 4),
        uncertainty=evidence_uncertainty(),
    )
    values.update(changes)
    return ReportedValue(**values)


def review(state=ReviewState.REVIEWED):
    reviewed = state in {ReviewState.REVIEWED, ReviewState.QUALIFIED}
    return ReviewContext(
        created_by="SYN-ELE-ACTOR",
        created_at="2026-01-01T00:00:00Z",
        state=state,
        reviewed_by=present("SYN-ELE-REVIEWER") if reviewed else missing(MissingState.NOT_APPLICABLE, "review has not occurred"),
        reviewed_at=present("2026-01-02T00:00:00Z") if reviewed else missing(MissingState.NOT_APPLICABLE, "review has not occurred"),
        notes="synthetic review context",
    )


def envelope(record_type, record_id=None, **changes):
    record_id = record_id or f"SYN-ELE-{record_type.value.upper().replace('_', '-')}"
    source = ref(record_id="SYN-ELE-SOURCE-REF")
    values = dict(
        record_type=record_type,
        record_id=record_id,
        record_version=1,
        activation=ActivationState.ACTIVE,
        evidence_class=EvidenceClass.EXPLORATORY_HYPOTHESIS,
        model_maturity=ModelMaturity.RETAINED_CANDIDATE,
        review=review(),
        source_references=(source,),
        parent_references=(),
        lineage=(),
        conflicts=(),
        supersedes=None,
        synthetic_fixture=True,
    )
    values.update(changes)
    return RecordEnvelope(**values)


def component(kind, suffix):
    return ScopedComponentIdentity(
        component_id=f"SYN-ELE-{suffix}",
        kind=kind,
        manufacturer=present("Fictional Components Organization"),
        product_designation=present(f"Synthetic {suffix}"),
        revision=missing(MissingState.NOT_SUPPLIED_BY_SOURCE, "synthetic source supplied no revision"),
        lot=missing(MissingState.UNKNOWN, "synthetic lot intentionally unknown"),
        source_wording=f"synthetic {suffix} wording",
        source_references=(ref(record_id=f"SYN-ELE-{suffix}-SOURCE"),),
    )


def equipment(kind, suffix):
    return EquipmentIdentity(
        equipment_id=f"SYN-ELE-{suffix}",
        kind=kind,
        organization=present("Example Laboratory L-0001"),
        designation=present(f"Synthetic Instrument {suffix}"),
        revision=missing(MissingState.NOT_SUPPLIED_BY_SOURCE, "synthetic revision omitted"),
        source_wording=f"synthetic equipment {suffix}",
    )


def pressure(level=ObservationLevel.SHOT, origin=PressureOrigin.PIEZOELECTRIC_TRANSDUCER):
    state = PressureAcquisitionState.MODELED if origin is PressureOrigin.MODELED else PressureAcquisitionState.RAW_MEASUREMENT
    return PressureObservation(
        reported_value=reported(ReportedValueKind.PRESSURE, unit="psi"),
        quantity=PressureQuantity.PEAK,
        origin=origin,
        location=PressureLocation.CHAMBER,
        acquisition_state=state,
        unit=PressureUnit.PSI,
        source_unit_label="psi",
        standard=ref_or_missing(ref(ReferenceRole.APPARATUS, "standard", "SYN-ELE-STANDARD")),
        instrument=ref_or_missing(ref(ReferenceRole.APPARATUS, "instrument", "SYN-ELE-INSTRUMENT")),
        sensor=ref_or_missing(ref(ReferenceRole.APPARATUS, "sensor", "SYN-ELE-SENSOR")),
        calibration=ref_or_missing(ref(ReferenceRole.APPARATUS, "calibration", "SYN-ELE-CALIBRATION")),
        filtering_state=missing(MissingState.NOT_SUPPLIED_BY_SOURCE, "synthetic filtering not supplied"),
        peak_definition=present("synthetic source peak definition"),
        observation_level=level,
    )


def velocity(level=ObservationLevel.SHOT, correction=VelocityCorrectionState.RAW):
    correction_ref = (
        ref_or_missing(ref(ReferenceRole.METHOD, "method", "SYN-ELE-VELOCITY-METHOD"))
        if correction in {VelocityCorrectionState.CORRECTED, VelocityCorrectionState.MUZZLE_EXTRAPOLATED}
        else ref_or_missing()
    )
    distance = PhysicalQuantityEvidence(
        quantity=Quantity(1, Unit.CENTIMETRE),
        source_value_text="1.0",
        precision=precision(PrecisionKind.DECIMAL_PLACES, 1),
        uncertainty=Uncertainty.unknown(),
    )
    return VelocityObservation(
        reported_value=reported(ReportedValueKind.VELOCITY, decimal="2.3450", unit="m/s"),
        quantity=VelocityQuantity.INDIVIDUAL_SHOT_SPEED if level is ObservationLevel.SHOT else VelocityQuantity.SOURCE_REPORTED_MEAN,
        correction_state=correction,
        unit=VelocityUnit.METRE_PER_SECOND,
        source_unit_label="m/s",
        measurement_distance=QuantityOrMissing(value=distance, missing=None),
        correction_method=correction_ref,
        atmospheric_context=missing(MissingState.NOT_SUPPLIED_BY_SOURCE, "synthetic atmosphere not supplied"),
        instrument=ref_or_missing(ref(ReferenceRole.APPARATUS, "instrument", "SYN-ELE-CHRONOGRAPH")),
        firearm=ref_or_missing(ref(ReferenceRole.APPARATUS, "firearm", "SYN-ELE-FIREARM")),
        barrel=ref_or_missing(ref(ReferenceRole.APPARATUS, "barrel", "SYN-ELE-BARREL")),
        observation_level=level,
    )


def source_record(**changes):
    custody_ref = ref(ReferenceRole.CUSTODY, "source_custody", "SYN-ELE-CUSTODY")
    artifact = ArtifactReference(
        artifact_id="SYN-ELE-ARTIFACT",
        retention_state=ArtifactRetentionState.RETAINED,
        sha256=present("a" * 64),
        media_type="application/x-synthetic",
        custody_reference=custody_ref,
        custody_limitation="synthetic bytes do not represent scientific evidence",
    )
    values = dict(
        envelope=envelope(EmpiricalRecordType.SOURCE_CUSTODY),
        source_title="Synthetic Source S-0001",
        originating_organization=present("Fictional Source Organization"),
        edition_or_revision=present("Synthetic Edition 1"),
        locator=SourceLocator("SYN-ELE-SOURCE", "synthetic locator", TranscriptionStatus.NOT_APPLICABLE),
        acquisition_context="created solely for structural testing",
        retention_context="test fixture only",
        artifacts=(artifact,),
        custody_lineage=(custody_ref,),
    )
    values.update(changes)
    return SourceCustodyRecord(**values)


def literal_record(**changes):
    duplicate = ref(ReferenceRole.DUPLICATE_PUBLICATION_OF, "literal_load_statement", "SYN-ELE-UNDERLYING-PUBLICATION")
    line = LineageLink(role=ReferenceRole.DUPLICATE_PUBLICATION_OF, reference=duplicate, statement="same fictional underlying test")
    conflict = ConflictGroup(
        conflict_id="SYN-ELE-CONFLICT",
        subject="synthetic transcription disagreement",
        members=(ref(record_id="SYN-ELE-CONFLICT-A"), ref(record_id="SYN-ELE-CONFLICT-B")),
        explanation="both fictional alternatives remain retained",
    )
    values = dict(
        envelope=envelope(EmpiricalRecordType.LITERAL_LOAD_STATEMENT, lineage=(line,), conflicts=(conflict,)),
        source_reference=ref(record_id="SYN-ELE-SOURCE-STATEMENT"),
        locator=SourceLocator("SYN-ELE-SOURCE", "synthetic statement", TranscriptionStatus.NOT_APPLICABLE),
        exact_source_wording="fictional statement for schema testing only",
        source_declared_component_wording=("Synthetic Propellant P-001", "Fictional Cartridge FC-01"),
        declared_values=(reported(ReportedValueKind.CHARGE_MASS, decimal="0.1234", unit="SYN-MASS"),),
        qualifications=("not load data",),
        conditions=("synthetic condition",),
        declaration_state=SourceDeclarationState.LITERAL,
        unresolved_wording=missing(MissingState.NOT_APPLICABLE, "literal synthetic wording is not unresolved"),
        normalized_record_references=(ref(ReferenceRole.NORMALIZED_FROM, "physical_load_configuration", "SYN-ELE-CONFIG"),),
    )
    values.update(changes)
    return LiteralLoadStatementRecord(**values)


def configuration_record(**changes):
    charge = PhysicalQuantityEvidence(
        quantity=Quantity(1, Unit.GRAIN),
        source_value_text="1.000",
        precision=precision(PrecisionKind.DECIMAL_PLACES, 3),
        uncertainty=Uncertainty.unknown(),
    )
    values = dict(
        envelope=envelope(EmpiricalRecordType.PHYSICAL_LOAD_CONFIGURATION),
        cartridge_designation=present("Fictional Cartridge FC-01"),
        powder=PowderIdentityReference(
            reference=ref(ReferenceRole.PARENT, "powder_identity", "SYN-ELE-POWDER", "modern_powley.m02.v1", 1),
            lot=missing(MissingState.UNKNOWN, "synthetic powder lot unknown"),
        ),
        bullet=component(ComponentKind.BULLET, "BULLET"),
        case=component(ComponentKind.CASE, "CASE"),
        primer=component(ComponentKind.PRIMER, "PRIMER"),
        charge=QuantityOrMissing(value=charge, missing=None),
        geometry_references=(ref(ReferenceRole.PARENT, "firearm_record", "SYN-ELE-GEOMETRY", "modern_powley.m01.v1", 1),),
        equipment=(equipment(EquipmentKind.FIREARM, "FIREARM"), equipment(EquipmentKind.BARREL, "BARREL"), equipment(EquipmentKind.CHAMBER, "CHAMBER"), equipment(EquipmentKind.THROAT_OR_FREEBORE, "THROAT")),
        preparation=("synthetic preparation",),
        conditions=("synthetic environment",),
        exclusion=Exclusion(state=ExclusionState.NOT_APPLICABLE, reason=missing(MissingState.NOT_APPLICABLE, "configuration exclusion not applicable"), authority=missing(MissingState.NOT_APPLICABLE, "configuration exclusion not applicable"), review_context="synthetic configuration review"),
    )
    values.update(changes)
    return PhysicalLoadConfigurationRecord(**values)


def shot_record(**changes):
    values = dict(
        envelope=envelope(EmpiricalRecordType.SHOT_OBSERVATION),
        load_configuration_reference=ref(
            ReferenceRole.CONFIGURATION,
            "physical_load_configuration",
            "SYN-ELE-CONFIG",
            schema_id=EMPIRICAL_LOAD_EVIDENCE_SCHEMA_ID,
        ),
        acquisition_sequence=1,
        acquisition_timestamp=present("2026-01-03T00:00:00Z"),
        apparatus_references=(ref(ReferenceRole.APPARATUS, "instrument", "SYN-ELE-INSTRUMENT"),),
        conditions=("synthetic shot condition",),
        pressure_observations=(pressure(),),
        pressure_missing=None,
        velocity_observations=(velocity(),),
        velocity_missing=None,
        trace_references=(ref(ReferenceRole.TRACE, "pressure_trace_metadata", "SYN-ELE-TRACE"),),
        exclusion=Exclusion(state=ExclusionState.EXCLUDED, reason=present("synthetic deliberate exclusion"), authority=present("SYN-ELE-REVIEWER"), review_context="synthetic exclusion review"),
        underlying_test_reference=ref_or_missing(ref(ReferenceRole.UNDERLYING_TEST, "underlying_test", "SYN-ELE-UNDERLYING-TEST")),
    )
    values.update(changes)
    return ShotObservationRecord(**values)


def members(prefix="SHOT"):
    return (
        OrderedMember(position=1, reference=ref(ReferenceRole.MEMBER, "shot_observation", f"SYN-ELE-{prefix}-1"), source_role="first fictional member"),
        OrderedMember(position=2, reference=ref(ReferenceRole.MEMBER, "shot_observation", f"SYN-ELE-{prefix}-2"), source_role="second fictional member"),
    )


def series_record(**changes):
    values = dict(
        envelope=envelope(EmpiricalRecordType.LOAD_SERIES),
        members=members(),
        purpose="synthetic ordering test",
        ordering_variable=present("fictional source order"),
        changed_variables=("synthetic declared variable",),
        controlled_variables=("synthetic controlled variable",),
        stopping_rule=missing(MissingState.NOT_SUPPLIED_BY_SOURCE, "no synthetic stopping rule supplied"),
        missing_members=(missing_value(MissingState.NOT_MEASURED),),
    )
    values.update(changes)
    return LoadSeriesRecord(**values)


def trace_record(state=TraceArtifactState.PROCESSED_EXTERNALLY, **changes):
    custody = ref(ReferenceRole.CUSTODY, "source_custody", "SYN-ELE-CUSTODY")
    artifact = ArtifactReference(artifact_id="SYN-ELE-TRACE-ARTIFACT", retention_state=ArtifactRetentionState.RETAINED, sha256=present("b" * 64), media_type="application/x-synthetic-trace", custody_reference=custody, custody_limitation="synthetic metadata only")
    method = ref(ReferenceRole.METHOD, "method", "SYN-ELE-EXTERNAL-PROCESSING") if state in {TraceArtifactState.PROCESSED_EXTERNALLY, TraceArtifactState.DERIVATIVE_TRANSCRIPTION_OR_EXPORT} else None
    values = dict(
        envelope=envelope(EmpiricalRecordType.PRESSURE_TRACE_METADATA),
        artifact=artifact,
        shot_reference=ref(
            ReferenceRole.SHOT,
            "shot_observation",
            "SYN-ELE-SHOT-1",
            schema_id=EMPIRICAL_LOAD_EVIDENCE_SCHEMA_ID,
        ),
        instrument=ref_or_missing(ref(ReferenceRole.APPARATUS, "instrument", "SYN-ELE-INSTRUMENT")),
        sensor=ref_or_missing(ref(ReferenceRole.APPARATUS, "sensor", "SYN-ELE-SENSOR")),
        channel=ref_or_missing(ref(ReferenceRole.APPARATUS, "channel", "SYN-ELE-CHANNEL")),
        sampling_rate=reported(ReportedValueKind.SAMPLING_RATE, decimal="10.000", unit="SYN-SAMPLES/S"),
        time_base=present("synthetic monotonic time base"),
        trigger_metadata=present("synthetic external trigger"),
        alignment_metadata=missing(MissingState.NOT_SUPPLIED_BY_SOURCE, "synthetic alignment omitted"),
        pressure_quantity=PressureQuantity.PEAK,
        pressure_location=PressureLocation.CHAMBER,
        calibration=ref_or_missing(ref(ReferenceRole.APPARATUS, "calibration", "SYN-ELE-CALIBRATION")),
        artifact_state=state,
        processing_method=method,
        excluded_windows=(ExcludedWindow(window_id="SYN-ELE-WINDOW-1", source_wording="synthetic excluded window", reason="structural test"),),
    )
    values.update(changes)
    return PressureTraceMetadataRecord(**values)


def chronograph_record(**changes):
    distance = PhysicalQuantityEvidence(quantity=Quantity(1, Unit.METRE), source_value_text="1", precision=precision(), uncertainty=Uncertainty.unknown())
    values = dict(
        envelope=envelope(EmpiricalRecordType.CHRONOGRAPH_SERIES),
        members=members("CHRONO-SHOT"),
        instrument=ref_or_missing(ref(ReferenceRole.APPARATUS, "instrument", "SYN-ELE-CHRONOGRAPH")),
        setup="synthetic chronograph setup",
        measurement_distance=QuantityOrMissing(value=distance, missing=None),
        correction_state=VelocityCorrectionState.RAW,
        correction_method=None,
        atmospheric_context=missing(MissingState.NOT_SUPPLIED_BY_SOURCE, "synthetic atmosphere omitted"),
        firearm=ref_or_missing(ref(ReferenceRole.APPARATUS, "firearm", "SYN-ELE-FIREARM")),
        barrel=ref_or_missing(ref(ReferenceRole.APPARATUS, "barrel", "SYN-ELE-BARREL")),
        missing_measurements=(missing_value(),),
        precision=precision(),
        uncertainty=evidence_uncertainty(),
    )
    values.update(changes)
    return ChronographSeriesRecord(**values)


def aggregate_record(**changes):
    values = dict(
        envelope=envelope(
            EmpiricalRecordType.AGGREGATE_SUMMARY,
            activation=ActivationState.INACTIVE,
            supersedes=ref(
                ReferenceRole.PARENT,
                "aggregate_summary",
                "SYN-ELE-AGGREGATE-PRIOR",
                schema_id=EMPIRICAL_LOAD_EVIDENCE_SCHEMA_ID,
            ),
        ),
        statistic=AggregateStatistic.MEAN,
        statistic_definition="synthetic externally supplied arithmetic mean identity",
        calculation_origin=AggregateOrigin.EXTERNALLY_CALCULATED,
        calculation_method=ref(ReferenceRole.METHOD, "method", "SYN-ELE-AGGREGATE-METHOD"),
        value=velocity(ObservationLevel.AGGREGATE),
        member_references=tuple(item.reference for item in members("AGG-SHOT")),
        membership_missing=None,
        exclusions=(ref(ReferenceRole.MEMBER, "shot_observation", "SYN-ELE-AGG-EXCLUDED"),),
        source_wording="synthetic external aggregate; no calculation performed here",
        precision=precision(),
        uncertainty=evidence_uncertainty(EvidenceUncertaintyKind.NOT_REPORTED),
    )
    values.update(changes)
    return AggregateSummaryRecord(**values)


def all_records():
    return (
        source_record(), literal_record(), configuration_record(), shot_record(),
        series_record(), trace_record(), chronograph_record(), aggregate_record(),
    )


def test_all_eight_record_families_construct_and_are_noninterchangeable():
    records = all_records()
    assert len(records) == 8
    assert len({type(item) for item in records}) == 8
    assert {item.envelope.record_type for item in records} == set(EmpiricalRecordType)
    with pytest.raises(ValueError, match="source_custody"):
        replace(source_record(), envelope=envelope(EmpiricalRecordType.SHOT_OBSERVATION))


def test_records_and_nested_collections_are_immutable_and_defensively_copied():
    item = series_record()
    with pytest.raises(FrozenInstanceError):
        item.purpose = "changed"
    source = [members()[0]]
    copied = replace(item, members=source)
    source.append(members()[1])
    assert len(copied.members) == 1


@pytest.mark.parametrize("bad", ["", "has space", "/path", True, 0, -1])
def test_identifiers_and_versions_reject_invalid_forms(bad):
    if isinstance(bad, str):
        with pytest.raises(ValueError):
            ref(record_id=bad)
    else:
        with pytest.raises(ValueError):
            replace(envelope(EmpiricalRecordType.SOURCE_CUSTODY), record_version=bad)


def test_envelope_statuses_supersession_conflict_and_synthetic_marker_are_independent():
    item = aggregate_record()
    assert item.envelope.activation is ActivationState.INACTIVE
    assert item.envelope.supersedes is not None
    assert item.envelope.evidence_class is EvidenceClass.EXPLORATORY_HYPOTHESIS
    assert item.envelope.synthetic_fixture is True
    assert literal_record().envelope.conflicts[0].members[0] != literal_record().envelope.conflicts[0].members[1]


def test_powder_component_and_equipment_identity_boundaries():
    item = configuration_record()
    assert item.powder.reference.schema_id == "modern_powley.m02.v1"
    assert item.powder.lot.missing_state is MissingState.UNKNOWN
    assert (item.bullet.kind, item.case.kind, item.primer.kind) == (ComponentKind.BULLET, ComponentKind.CASE, ComponentKind.PRIMER)
    assert {entry.kind for entry in item.equipment} == {EquipmentKind.FIREARM, EquipmentKind.BARREL, EquipmentKind.CHAMBER, EquipmentKind.THROAT_OR_FREEBORE}
    with pytest.raises(ValueError, match="M02 schema"):
        replace(item.powder, reference=ref(ReferenceRole.PARENT, "powder_identity", "SYN-ELE-P", "other.v1"))
    with pytest.raises(ValueError, match="manufacturer"):
        replace(item.bullet, manufacturer=missing(), product_designation=present("bare product"))


def test_charge_requires_positive_mass_without_replacing_source_text():
    item = configuration_record()
    assert item.charge.value.quantity.unit is Unit.GRAIN
    assert item.charge.value.source_value_text == "1.000"
    with pytest.raises(ValueError, match="dimension mass"):
        replace(item, charge=QuantityOrMissing(value=replace(item.charge.value, quantity=Quantity(1, Unit.INCH)), missing=None))
    with pytest.raises(ValueError, match="greater than zero"):
        replace(item, charge=QuantityOrMissing(value=replace(item.charge.value, quantity=Quantity(0, Unit.GRAIN)), missing=None))


def test_pressure_semantics_do_not_collapse_origin_location_unit_or_modeled_state():
    measured = pressure()
    modeled = pressure(origin=PressureOrigin.MODELED)
    crusher = replace(measured, origin=PressureOrigin.CRUSHER)
    cup = replace(crusher, unit=PressureUnit.CUP, source_unit_label="CUP", reported_value=replace(crusher.reported_value, source_unit_label="CUP"))
    assert len({measured, modeled, crusher, cup}) == 4
    with pytest.raises(ValueError, match="must agree"):
        replace(measured, origin=PressureOrigin.MODELED)
    with pytest.raises(ValueError, match="controlled pressure unit"):
        replace(measured, unit=PressureUnit.CUP)
    assert cup.unit is PressureUnit.CUP and measured.unit is PressureUnit.PSI


def test_velocity_distance_correction_and_barrel_context_remain_explicit():
    raw = velocity()
    corrected = velocity(correction=VelocityCorrectionState.CORRECTED)
    extrapolated = velocity(correction=VelocityCorrectionState.MUZZLE_EXTRAPOLATED)
    assert len({raw, corrected, extrapolated}) == 3
    assert raw.measurement_distance.value.quantity.unit is Unit.CENTIMETRE
    assert raw.barrel.reference.record_id == "SYN-ELE-BARREL"
    with pytest.raises(ValueError, match="requires an exact method"):
        replace(raw, correction_state=VelocityCorrectionState.CORRECTED)
    with pytest.raises(ValueError, match="controlled velocity unit"):
        replace(raw, unit=VelocityUnit.FOOT_PER_SECOND)


def test_pressure_velocity_and_sampling_values_reject_negative_or_zero_where_required():
    with pytest.raises(ValueError, match="pressure observation cannot be negative"):
        replace(pressure(), reported_value=reported(ReportedValueKind.PRESSURE, "-0.1", "psi"))
    with pytest.raises(ValueError, match="velocity observation cannot be negative"):
        replace(velocity(), reported_value=reported(ReportedValueKind.VELOCITY, "-0.1", "m/s"))
    item = trace_record()
    with pytest.raises(ValueError, match="sampling rate must be greater than zero"):
        replace(item, sampling_rate=reported(ReportedValueKind.SAMPLING_RATE, "0", "Hz"))


def test_cross_record_reference_roles_are_explicit_and_noninterchangeable():
    item = trace_record()
    with pytest.raises(ValueError, match="exact Phase 1 shot"):
        replace(item, shot_reference=ref(ReferenceRole.TRACE, "shot_observation", "SYN-ELE-SHOT-1"))
    load = configuration_record()
    with pytest.raises(ValueError, match="geometry references require parent"):
        replace(load, geometry_references=(ref(ReferenceRole.SOURCE, "geometry", "SYN-ELE-GEOMETRY"),))
    prior = aggregate_record().envelope.supersedes
    with pytest.raises(ValueError, match="exact prior Phase 1"):
        replace(aggregate_record().envelope, supersedes=replace(prior, schema_id="synthetic.schema.v1"))
    with pytest.raises(TypeError, match="sampling rate"):
        replace(item, sampling_rate=1)
    with pytest.raises(TypeError, match="aggregate value"):
        replace(aggregate_record(), value="1.0")


def test_shot_exclusion_and_duplicate_underlying_test_remain_present():
    item = shot_record()
    assert item.exclusion.state is ExclusionState.EXCLUDED
    assert item.exclusion.reason.value == "synthetic deliberate exclusion"
    assert item.underlying_test_reference.reference.role is ReferenceRole.UNDERLYING_TEST
    assert item.pressure_observations and item.velocity_observations


def test_shot_requires_present_or_semantically_missing_pressure_and_velocity():
    item = shot_record()
    with pytest.raises(ValueError, match="pressure"):
        replace(item, pressure_observations=(), pressure_missing=None)
    missing_pressure = replace(item, pressure_observations=(), pressure_missing=missing_value())
    assert missing_pressure.pressure_missing.state is MissingState.NOT_MEASURED
    with pytest.raises(ValueError, match="velocity"):
        replace(item, velocity_missing=missing_value())


def test_ordered_series_rejects_duplicate_ambiguous_or_out_of_order_members():
    item = series_record()
    assert [entry.position for entry in item.members] == [1, 2]
    with pytest.raises(ValueError, match="ascending"):
        replace(item, members=tuple(reversed(item.members)))
    with pytest.raises(ValueError, match="references"):
        replace(item, members=(item.members[0], replace(item.members[1], reference=item.members[0].reference)))


@pytest.mark.parametrize("state", list(TraceArtifactState))
def test_trace_states_preserve_metadata_without_samples_or_processing(state):
    item = trace_record(state)
    assert item.artifact_state is state
    assert not hasattr(item, "samples")
    assert item.excluded_windows[0].reason == "structural test"


def test_trace_hash_and_external_processing_conditionals_are_strict():
    item = trace_record()
    with pytest.raises(ValueError, match="SHA-256"):
        replace(item.artifact, sha256=present("BAD"))
    with pytest.raises(ValueError, match="requires an external method"):
        replace(item, processing_method=None)
    raw = trace_record(TraceArtifactState.RAW)
    with pytest.raises(ValueError, match="requires an external method"):
        replace(raw, processing_method=ref(ReferenceRole.METHOD, "method", "SYN-ELE-M"))


def test_chronograph_and_aggregate_preserve_members_without_calculating():
    chrono = chronograph_record()
    aggregate = aggregate_record()
    assert [item.position for item in chrono.members] == [1, 2]
    assert aggregate.calculation_origin is AggregateOrigin.EXTERNALLY_CALCULATED
    assert aggregate.member_references and aggregate.exclusions
    with pytest.raises(ValueError, match="exact method"):
        replace(aggregate, calculation_method=None)


def test_precision_uncertainty_and_exact_decimal_text_are_separate():
    value = reported(ReportedValueKind.VELOCITY, decimal="0001.2300", unit="m/s")
    assert value.decimal_text == "0001.2300"
    assert value.precision.kind is PrecisionKind.DECIMAL_PLACES
    assert value.uncertainty.kind is EvidenceUncertaintyKind.UNKNOWN
    for bad in ("NaN", "Infinity", "-Infinity", "not-number", ""):
        with pytest.raises(ValueError):
            replace(value, decimal_text=bad)


def test_none_zero_empty_and_nan_do_not_impersonate_semantic_missingness():
    with pytest.raises(ValueError, match="exactly one"):
        QuantityOrMissing(value=None, missing=None)
    with pytest.raises(ValueError):
        MissingValue(state=MissingState.UNKNOWN, explanation="")
    with pytest.raises(ValueError):
        ReportedValue(kind=ReportedValueKind.PRESSURE, decimal_text=str(math.nan), source_unit_label="psi", source_wording="synthetic", precision=precision(), uncertainty=evidence_uncertainty())
