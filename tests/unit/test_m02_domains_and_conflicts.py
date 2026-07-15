from dataclasses import replace

import pytest

from modern_powley.modernized import (
    ApplicabilityDomain,
    BoundKind,
    CategoricalDomainConstraint,
    DomainBound,
    DomainComparison,
    DomainMembershipStatus,
    DomainStatus,
    IdentityComparison,
    NumericComparison,
    NumericDomainConstraint,
    Uncertainty,
    UncertaintyKind,
    Quantity,
    PropertyDefinition,
    PropertyId,
    PropertyValueKind,
    SourceScalarPropertyValue,
    UnitComparison,
    SourceScalarDomainBound,
    SourceScalarDomainConstraint,
    SourceScalarDomainValue,
    Unit,
    compare_property_observations,
    test_domain_membership as literal_domain_membership,
)
from tests.unit.test_m02_identity_properties_and_missing import (
    bulk_observation,
    physical,
    synthetic_identity,
)


def declared_domain(lower_kind=BoundKind.INCLUSIVE, upper_kind=BoundKind.EXCLUSIVE):
    return ApplicabilityDomain(
        DomainStatus.DECLARED,
        (
            NumericDomainConstraint(
                "test_temperature", "synthetic source test temperature",
                DomainBound(lower_kind, physical("SYNTHETIC-T-LOW", 15, Unit.DEGREE_CELSIUS)),
                DomainBound(upper_kind, physical("SYNTHETIC-T-HIGH", 25, Unit.DEGREE_CELSIUS)),
            ),
        ),
        (CategoricalDomainConstraint("apparatus", "synthetic apparatus identity", ("VESSEL-A",)),),
        "synthetic declared domain",
    )


def test_unspecified_domain_is_not_unrestricted():
    result = literal_domain_membership(
        ApplicabilityDomain.unspecified("source states no domain"),
        numeric_values={}, categorical_values={},
    )
    assert result.status is DomainMembershipStatus.INDETERMINATE_UNSPECIFIED_DOMAIN


def test_domain_boundaries_are_literal_and_inclusive_or_exclusive():
    domain = declared_domain()
    at_lower = literal_domain_membership(domain, numeric_values={"test_temperature": Quantity(15, Unit.DEGREE_CELSIUS)}, categorical_values={"apparatus": "VESSEL-A"})
    at_upper = literal_domain_membership(domain, numeric_values={"test_temperature": Quantity(25, Unit.DEGREE_CELSIUS)}, categorical_values={"apparatus": "VESSEL-A"})
    interior = literal_domain_membership(domain, numeric_values={"test_temperature": Quantity(20, Unit.DEGREE_CELSIUS)}, categorical_values={"apparatus": "VESSEL-A"})
    assert at_lower.status is DomainMembershipStatus.WITHIN_DECLARED_DOMAIN
    assert at_upper.status is DomainMembershipStatus.OUTSIDE_DECLARED_DOMAIN
    assert interior.status is DomainMembershipStatus.WITHIN_DECLARED_DOMAIN


def test_domain_missing_dimension_and_category_fail_descriptively():
    domain = declared_domain()
    missing = literal_domain_membership(domain, numeric_values={}, categorical_values={})
    incompatible = literal_domain_membership(domain, numeric_values={"test_temperature": Quantity(20, Unit.MILLIMETRE)}, categorical_values={"apparatus": "VESSEL-A"})
    category = literal_domain_membership(domain, numeric_values={"test_temperature": Quantity(20, Unit.DEGREE_CELSIUS)}, categorical_values={"apparatus": "VESSEL-B"})
    assert missing.status is DomainMembershipStatus.INDETERMINATE_MISSING_INPUT
    assert incompatible.status is DomainMembershipStatus.INCOMPATIBLE_DIMENSION
    assert category.status is DomainMembershipStatus.OUTSIDE_DECLARED_DOMAIN


def test_open_closed_bounded_and_unbounded_endpoints_are_representable():
    lower_unbounded = NumericDomainConstraint(
        "temperature", "upper-only source domain",
        DomainBound(BoundKind.UNBOUNDED, None),
        DomainBound(BoundKind.INCLUSIVE, physical("UPPER", 30, Unit.DEGREE_CELSIUS)),
    )
    assert lower_unbounded.lower.value is None
    with pytest.raises(ValueError, match="both ends"):
        NumericDomainConstraint("x", "no restriction", DomainBound(BoundKind.UNBOUNDED, None), DomainBound(BoundKind.UNBOUNDED, None))


def test_source_scalar_domain_requires_literal_unit_and_convention_match():
    domain = ApplicabilityDomain(
        DomainStatus.DECLARED, (), (), "synthetic source-scalar pressure domain",
        (
            SourceScalarDomainConstraint(
                "reported_pressure", "synthetic source pressure label",
                "source-pressure-unit", "synthetic apparatus convention",
                SourceScalarDomainBound(BoundKind.INCLUSIVE, 10),
                SourceScalarDomainBound(BoundKind.INCLUSIVE, 20),
            ),
        ),
    )
    inside = literal_domain_membership(
        domain, numeric_values={}, categorical_values={},
        source_scalar_values={"reported_pressure": SourceScalarDomainValue(15, "source-pressure-unit", "synthetic apparatus convention")},
    )
    incompatible = literal_domain_membership(
        domain, numeric_values={}, categorical_values={},
        source_scalar_values={"reported_pressure": SourceScalarDomainValue(15, "other-unit", "synthetic apparatus convention")},
    )
    assert inside.status is DomainMembershipStatus.WITHIN_DECLARED_DOMAIN
    assert incompatible.status is DomainMembershipStatus.INCOMPATIBLE_DIMENSION


def test_conflicting_observations_coexist_without_resolution():
    left = bulk_observation("SYNTHETIC-M02-OBS-A", 0.80, Unit.GRAM_PER_CUBIC_CENTIMETRE)
    right = bulk_observation("SYNTHETIC-M02-OBS-B", 810, Unit.KILOGRAM_PER_CUBIC_METRE)
    comparison = compare_property_observations(
        left, right, result_id="SYNTHETIC-M02-COMPARE-1",
        left_identity=synthetic_identity(),
        right_identity=synthetic_identity("SYNTHETIC-M02-POWDER-A", "SYNTHETIC-LOT-A"),
    )
    assert left.record_id != right.record_id
    assert comparison.numeric_comparison is NumericComparison.NUMERICALLY_DIFFERENT
    assert comparison.domain_comparison is DomainComparison.ONE_OR_BOTH_UNSPECIFIED
    assert comparison.identity_comparison is IdentityComparison.SAME_IDENTITY_RECORD
    assert not hasattr(comparison, "preferred_record")
    assert not hasattr(comparison, "selected_value")


def test_known_lot_difference_is_reported_not_resolved():
    left = bulk_observation("SYNTHETIC-M02-OBS-A")
    right = bulk_observation("SYNTHETIC-M02-OBS-B")
    right = type(right)(
        right.record_id, "SYNTHETIC-M02-POWDER-B", right.property_definition,
        right.value, right.provenance, right.source_locator, right.transformation,
        right.reported_wording, right.uncertainty_qualification, right.context,
        right.applicability_domain, right.dependency_record_ids, right.qualifications,
    )
    comparison = compare_property_observations(
        left, right, result_id="SYNTHETIC-M02-COMPARE-LOTS",
        left_identity=synthetic_identity(),
        right_identity=synthetic_identity("SYNTHETIC-M02-POWDER-B", "SYNTHETIC-LOT-B"),
    )
    assert comparison.identity_comparison is IdentityComparison.DIFFERENT_KNOWN_LOTS
    assert "no preferred" in comparison.reasons[-1]


def test_declared_symmetric_uncertainty_can_be_described_as_overlapping():
    left = bulk_observation("SYNTHETIC-M02-OBS-U1", 0.800)
    right = bulk_observation("SYNTHETIC-M02-OBS-U2", 0.805)
    left_value = replace(
        left.value,
        physical_value=replace(
            left.value.physical_value,
            uncertainty=Uncertainty(
                UncertaintyKind.SYMMETRIC_ABSOLUTE,
                magnitude=Quantity(0.01, Unit.GRAM_PER_CUBIC_CENTIMETRE),
            ),
        ),
    )
    right_value = replace(
        right.value,
        physical_value=replace(
            right.value.physical_value,
            uncertainty=Uncertainty(
                UncertaintyKind.SYMMETRIC_ABSOLUTE,
                magnitude=Quantity(0.01, Unit.GRAM_PER_CUBIC_CENTIMETRE),
            ),
        ),
    )
    left = replace(left, value=left_value)
    right = replace(right, value=right_value)
    comparison = compare_property_observations(left, right, result_id="SYNTHETIC-M02-COMPARE-U")
    assert comparison.numeric_comparison is NumericComparison.AGREE_WITHIN_DECLARED_UNCERTAINTY


def test_source_scalar_definition_or_unit_difference_remains_nonconvertible():
    left = bulk_observation("SYNTHETIC-M02-SOURCE-SCALAR-1")
    right = bulk_observation("SYNTHETIC-M02-SOURCE-SCALAR-2")
    definition = PropertyDefinition(
        PropertyId.SOURCE_SPECIFIC_COEFFICIENT, "Synthetic C",
        "Synthetic source-specific coefficient C", PropertyValueKind.SOURCE_SPECIFIC,
        None, True, "SYNTHETIC-METHOD:C",
    )
    left = replace(left, property_definition=definition, value=SourceScalarPropertyValue(1, "unit-A", "method-C", definition.definition, "synthetic 1"))
    right = replace(right, property_definition=definition, value=SourceScalarPropertyValue(1, "unit-B", "method-C", definition.definition, "synthetic 1"))
    comparison = compare_property_observations(left, right, result_id="SYNTHETIC-M02-SOURCE-COMPARE")
    assert comparison.unit_comparison is UnitComparison.NONCONVERTIBLE
    assert comparison.numeric_comparison is NumericComparison.INSUFFICIENT_FOR_NUMERIC_COMPARISON
