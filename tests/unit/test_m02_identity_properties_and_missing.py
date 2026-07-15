import pytest

from modern_powley.modernized import (
    ApplicabilityDomain,
    DimensionalPropertyValue,
    EvidenceClass,
    IdentityQualifier,
    MissingPropertyObservation,
    MissingState,
    ModelMaturity,
    ObservationContext,
    ObservationTransformation,
    PhysicalValue,
    PowderIdentity,
    PowderIdentityRelationship,
    PowderPropertyObservation,
    PowderRelationshipKind,
    PropertyDefinition,
    PropertyId,
    PropertyValueKind,
    Provenance,
    Quantity,
    SourceLocator,
    SourceScalarPropertyValue,
    TranscriptionStatus,
    Uncertainty,
    Unit,
    ValueOrigin,
    standard_property_definition,
)


def synthetic_provenance(source_id="SYNTHETIC-M02-SOURCE"):
    return Provenance(
        EvidenceClass.EXPLORATORY_HYPOTHESIS,
        ValueOrigin.ASSUMED,
        source_id,
        ModelMaturity.RETAINED_CANDIDATE,
    )


def missing(state=MissingState.NOT_SUPPLIED_BY_SOURCE, explanation="synthetic fixture intentionally omits this qualifier"):
    return IdentityQualifier.missing(state, explanation)


def synthetic_identity(record_id="SYNTHETIC-M02-POWDER-A", lot="SYNTHETIC-LOT-A"):
    return PowderIdentity(
        record_id,
        "Synthetic Test Organization",
        "Synthetic Powder A",
        "SYNTHETIC POWDER A",
        "SYN-A",
        IdentityQualifier.present("synthetic fixture family"),
        IdentityQualifier.present("synthetic canister-status fixture"),
        IdentityQualifier.present(lot),
        missing(),
        missing(),
        IdentityQualifier.present("synthetic test market"),
        synthetic_provenance(),
    )


def context():
    return ObservationContext(
        missing(), missing(), missing(), missing(),
        IdentityQualifier.present("synthetic fixture era"),
    )


def physical(record_id, value, unit, uncertainty=None):
    return PhysicalValue(
        record_id,
        Quantity(value, unit),
        synthetic_provenance(),
        uncertainty or Uncertainty.unknown(),
    )


def bulk_observation(record_id="SYNTHETIC-M02-OBS-A", value=0.80, unit=Unit.GRAM_PER_CUBIC_CENTIMETRE):
    return PowderPropertyObservation(
        record_id,
        "SYNTHETIC-M02-POWDER-A",
        standard_property_definition(PropertyId.BULK_DENSITY),
        DimensionalPropertyValue(physical(f"{record_id}-VALUE", value, unit), "loose-poured synthetic fixture convention", "synthetic reported value"),
        synthetic_provenance(),
        SourceLocator("SYNTHETIC-M02-SOURCE", "synthetic fixture row", TranscriptionStatus.NOT_APPLICABLE),
        ObservationTransformation.ASSERTED,
        "Synthetic test value; not a real powder fact",
        missing(MissingState.NOT_MEASURED, "synthetic value has no measurement uncertainty"),
        context(),
        ApplicabilityDomain.unspecified("synthetic fixture defines no applicability domain"),
        (),
        ("synthetic only",),
    )


def test_identity_qualifiers_are_present_or_semantically_missing():
    assert IdentityQualifier.present("LOT-X").value == "LOT-X"
    assert missing(MissingState.WITHHELD_OR_PROPRIETARY).missing_state is MissingState.WITHHELD_OR_PROPRIETARY
    with pytest.raises(ValueError, match="exactly one"):
        IdentityQualifier("LOT-X", MissingState.UNKNOWN, "ambiguous")
    with pytest.raises(ValueError, match="explanation"):
        IdentityQualifier.missing(MissingState.UNKNOWN, "")


def test_powder_identity_does_not_merge_names_lots_or_organizations():
    left = synthetic_identity()
    different_lot = synthetic_identity("SYNTHETIC-M02-POWDER-B", "SYNTHETIC-LOT-B")
    different_org = PowderIdentity(
        "SYNTHETIC-M02-POWDER-C", "Another Synthetic Organization",
        left.published_designation, left.normalized_display_designation,
        left.source_specific_designation, left.product_family, left.product_class, left.lot_or_batch,
        left.manufacturing_date_or_era, left.formulation_or_revision,
        left.country_or_market, synthetic_provenance(),
    )
    assert left != different_lot
    assert left != different_org
    assert len({left.record_id, different_lot.record_id, different_org.record_id}) == 3


def test_alias_relationship_is_directional_and_provenance_backed():
    relation = PowderIdentityRelationship(
        "SYNTHETIC-M02-REL-1", "SYNTHETIC-M02-POWDER-A",
        PowderRelationshipKind.DESCRIBED_AS_SIMILAR_TO,
        "SYNTHETIC-M02-POWDER-B", "synthetically described as similar",
        "synthetic fixture relation", synthetic_provenance(),
    )
    assert relation.subject_powder_id != relation.object_powder_id
    assert relation.relationship is PowderRelationshipKind.DESCRIBED_AS_SIMILAR_TO
    assert not hasattr(relation, "is_equivalent")


def test_property_vocabulary_keeps_similar_terms_distinct():
    assert PropertyId.HEAT_OF_EXPLOSION != PropertyId.FORCE
    assert PropertyId.FORCE != PropertyId.IMPETUS
    assert PropertyId.VIVACITY_REPORTED != PropertyId.BURN_RATE_COEFFICIENT_REPORTED
    assert PropertyId.MANUFACTURER_RELATIVE_BURN_RATE_POSITION != PropertyId.VIVACITY_REPORTED
    bulk = standard_property_definition(PropertyId.BULK_DENSITY)
    assert bulk.expected_dimension.value == "mass_density"
    with pytest.raises(ValueError, match="source-specific"):
        standard_property_definition(PropertyId.SOURCE_SPECIFIC_COEFFICIENT)


def test_source_specific_definition_and_value_retain_literal_semantics():
    definition = PropertyDefinition(
        PropertyId.SOURCE_SPECIFIC_COEFFICIENT,
        "Synthetic coefficient C",
        "Coefficient C exactly as defined by synthetic source method X",
        PropertyValueKind.SOURCE_SPECIFIC,
        None,
        True,
        "SYNTHETIC-METHOD-X:C",
    )
    value = SourceScalarPropertyValue(0.0, "synthetic-unit-X", "synthetic method X", definition.definition, "printed zero")
    assert value.value == 0.0
    assert value.reported_unit == "synthetic-unit-X"


def test_observation_enforces_property_dimension_and_source_identity():
    observation = bulk_observation()
    assert observation.value.physical_value.quantity.unit is Unit.GRAM_PER_CUBIC_CENTIMETRE
    assert observation.value.physical_value.quantity.si_value == pytest.approx(800.0)
    bad_value = DimensionalPropertyValue(physical("BAD-TEMP", 20, Unit.DEGREE_CELSIUS), "synthetic", "synthetic")
    with pytest.raises(ValueError, match="dimension"):
        PowderPropertyObservation(
            "SYNTHETIC-M02-BAD", observation.powder_identity_id,
            observation.property_definition, bad_value, observation.provenance,
            observation.source_locator, observation.transformation,
            observation.reported_wording, observation.uncertainty_qualification,
            observation.context, observation.applicability_domain, (), (),
        )


def test_transformation_and_provenance_origin_cannot_contradict():
    observation = bulk_observation()
    with pytest.raises(ValueError, match="origin disagree"):
        PowderPropertyObservation(
            "SYNTHETIC-M02-BAD-TRANSFORM", observation.powder_identity_id,
            observation.property_definition, observation.value,
            observation.provenance, observation.source_locator,
            ObservationTransformation.TRANSCRIBED, observation.reported_wording,
            observation.uncertainty_qualification, observation.context,
            observation.applicability_domain, (), (),
        )


@pytest.mark.parametrize("state", list(MissingState))
def test_every_missing_state_is_explicit_and_zero_is_not_missing(state):
    observation = bulk_observation()
    related = (observation.record_id,) if state is MissingState.CONFLICTING_EVIDENCE else ()
    missing_observation = MissingPropertyObservation(
        f"SYNTHETIC-MISSING-{state.value}", observation.powder_identity_id,
        observation.property_definition, state, observation.provenance,
        observation.source_locator, "synthetic missing-state fixture",
        "M02 unit test", True, related,
        ApplicabilityDomain.unspecified("source domain unavailable because value is missing"),
    )
    assert missing_observation.missing_state is state
    assert not hasattr(missing_observation, "value")
    assert SourceScalarPropertyValue(0, "unit-X", "convention-X", "definition-X", "reported 0").value == 0


def test_conflicting_missing_state_requires_related_records():
    observation = bulk_observation()
    with pytest.raises(ValueError, match="related"):
        MissingPropertyObservation(
            "SYNTHETIC-MISSING-CONFLICT", observation.powder_identity_id,
            observation.property_definition, MissingState.CONFLICTING_EVIDENCE,
            observation.provenance, observation.source_locator, "conflict",
            "test", True, (), ApplicabilityDomain.unspecified("unknown domain"),
        )
