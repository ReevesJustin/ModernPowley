from dataclasses import replace

import pytest

from modern_powley.modernized import (
    ApplicabilityDomain,
    ApplicabilitySummary,
    BoundKind,
    CategoricalDomainConstraint,
    DomainBound,
    DomainDiagnosticStatus,
    DomainQueryContext,
    DomainQueryKind,
    DomainQueryValue,
    DomainStatus,
    MissingState,
    NumericDomainConstraint,
    QueryInterval,
    Quantity,
    SourceScalarDomainBound,
    SourceScalarDomainConstraint,
    SourceScalarDomainValue,
    Unit,
    diagnose_observation_applicability,
)
from tests.unit.test_m02_domains_and_conflicts import physical
from tests.unit.test_m02_identity_properties_and_missing import bulk_observation, synthetic_provenance


def domain():
    return ApplicabilityDomain(
        DomainStatus.DECLARED,
        (
            NumericDomainConstraint(
                "temperature", "synthetic test temperature",
                DomainBound(BoundKind.INCLUSIVE, physical("SYNTHETIC-M03-T-LOW", 10, Unit.DEGREE_CELSIUS)),
                DomainBound(BoundKind.EXCLUSIVE, physical("SYNTHETIC-M03-T-HIGH", 30, Unit.DEGREE_CELSIUS)),
            ),
        ),
        (CategoricalDomainConstraint("apparatus", "synthetic apparatus identifier", ("VESSEL-A",)),),
        "synthetic declared domain",
        (
            SourceScalarDomainConstraint(
                "source_index", "synthetic source index", "index-unit", "index-convention",
                SourceScalarDomainBound(BoundKind.EXCLUSIVE, 1),
                SourceScalarDomainBound(BoundKind.INCLUSIVE, 3),
            ),
        ),
    )


def observation(custom_domain=None):
    return replace(bulk_observation("SYNTHETIC-M03-OBS"), applicability_domain=custom_domain or domain())


def query(*values, property_id="bulk_density", observation_id="SYNTHETIC-M03-OBS"):
    return DomainQueryContext("SYNTHETIC-M03-QUERY", observation_id, property_id, tuple(values), synthetic_provenance())


def point(variable, definition, value, unit):
    return DomainQueryValue(variable, definition, DomainQueryKind.NUMERIC_POINT, numeric_point=Quantity(value, unit))


def category(variable, definition, value, kind=DomainQueryKind.CATEGORICAL):
    return DomainQueryValue(variable, definition, kind, category_or_identifier=value)


def source(value, unit="index-unit", convention="index-convention"):
    return DomainQueryValue("source_index", "synthetic source index", DomainQueryKind.SOURCE_SCALAR_POINT, source_scalar_point=SourceScalarDomainValue(value, unit, convention))


def full_query(temperature=20, temperature_unit=Unit.DEGREE_CELSIUS, apparatus="VESSEL-A", source_value=2):
    return query(point("temperature", "synthetic test temperature", temperature, temperature_unit), category("apparatus", "synthetic apparatus identifier", apparatus, DomainQueryKind.IDENTIFIER), source(source_value))


def diagnostic(result, constraint_id):
    return next(item for item in result.diagnostics if item.constraint_id == constraint_id)


def test_all_declared_constraints_satisfied_is_literal_not_suitability():
    result = diagnose_observation_applicability(observation(), full_query(), record_id="SYNTHETIC-M03-APP-1")
    assert result.summary is ApplicabilitySummary.ALL_DECLARED_CONSTRAINTS_SATISFIED
    assert all(item.status is DomainDiagnosticStatus.INSIDE_DECLARED_DOMAIN for item in result.diagnostics)
    assert not hasattr(result, "suitable")
    assert not hasattr(result, "eligible")


@pytest.mark.parametrize(
    ("value", "expected", "reason"),
    [
        (10, DomainDiagnosticStatus.INSIDE_DECLARED_DOMAIN, "satisfies"),
        (30, DomainDiagnosticStatus.OUTSIDE_DECLARED_DOMAIN, "exclusive upper"),
        (9, DomainDiagnosticStatus.OUTSIDE_DECLARED_DOMAIN, "below"),
        (31, DomainDiagnosticStatus.OUTSIDE_DECLARED_DOMAIN, "above"),
    ],
)
def test_numeric_endpoint_inclusion_and_rejection_reasons(value, expected, reason):
    result = diagnose_observation_applicability(observation(), full_query(temperature=value), record_id=f"SYNTHETIC-M03-APP-T-{value}")
    item = diagnostic(result, "temperature")
    assert item.status is expected
    assert reason in item.rejection_reason.lower()
    assert item.query.numeric_point.value == value
    assert item.declared_constraint.lower.kind is BoundKind.INCLUSIVE
    assert item.declared_constraint.upper.kind is BoundKind.EXCLUSIVE


def test_missing_explicitly_unavailable_and_incompatible_units_are_distinct():
    missing = diagnose_observation_applicability(observation(), query(category("apparatus", "synthetic apparatus identifier", "VESSEL-A"), source(2)), record_id="SYNTHETIC-M03-APP-MISSING")
    unavailable_value = DomainQueryValue("temperature", "synthetic test temperature", DomainQueryKind.EXPLICITLY_UNAVAILABLE, missing_state=MissingState.NOT_MEASURED, explanation="synthetic missing query")
    unavailable = diagnose_observation_applicability(observation(), query(unavailable_value, category("apparatus", "synthetic apparatus identifier", "VESSEL-A"), source(2)), record_id="SYNTHETIC-M03-APP-UNAVAILABLE")
    incompatible = diagnose_observation_applicability(observation(), full_query(temperature_unit=Unit.MILLIMETRE), record_id="SYNTHETIC-M03-APP-INCOMPATIBLE")
    assert diagnostic(missing, "temperature").status is DomainDiagnosticStatus.REQUIRED_QUERY_VALUE_MISSING
    assert diagnostic(unavailable, "temperature").status is DomainDiagnosticStatus.QUERY_VALUE_EXPLICITLY_UNAVAILABLE
    assert diagnostic(unavailable, "temperature").query.missing_state is MissingState.NOT_MEASURED
    assert diagnostic(incompatible, "temperature").status is DomainDiagnosticStatus.INCOMPATIBLE_UNITS
    assert unavailable.summary is ApplicabilitySummary.APPLICABILITY_INDETERMINATE


def test_unspecified_domain_does_not_pass_or_mean_unrestricted():
    unknown = observation(ApplicabilityDomain.unspecified("synthetic source supplied no domain"))
    result = diagnose_observation_applicability(unknown, query(), record_id="SYNTHETIC-M03-APP-UNSPECIFIED")
    assert result.summary is ApplicabilitySummary.NO_DECLARED_DOMAIN_SUPPLIED
    assert result.diagnostics[0].status is DomainDiagnosticStatus.DOMAIN_UNSPECIFIED


def test_categorical_identifier_definition_and_source_unit_mismatches_are_distinct():
    categorical = diagnose_observation_applicability(observation(), full_query(apparatus="VESSEL-B"), record_id="SYNTHETIC-M03-APP-CAT")
    wrong_definition = query(point("temperature", "different temperature definition", 20, Unit.DEGREE_CELSIUS), category("apparatus", "synthetic apparatus identifier", "VESSEL-A"), source(2))
    definition = diagnose_observation_applicability(observation(), wrong_definition, record_id="SYNTHETIC-M03-APP-DEF")
    source_unit = query(point("temperature", "synthetic test temperature", 20, Unit.DEGREE_CELSIUS), category("apparatus", "synthetic apparatus identifier", "VESSEL-A"), source(2, unit="other-unit"))
    incompatible = diagnose_observation_applicability(observation(), source_unit, record_id="SYNTHETIC-M03-APP-UNIT")
    assert diagnostic(categorical, "apparatus").status is DomainDiagnosticStatus.IDENTIFIER_MISMATCH
    assert diagnostic(definition, "temperature").status is DomainDiagnosticStatus.DEFINITION_MISMATCH
    assert diagnostic(incompatible, "source_index").status is DomainDiagnosticStatus.INCOMPATIBLE_UNITS


def test_interval_must_be_contained_disjoint_or_partial_without_midpoint():
    def interval(lower, lower_kind, upper, upper_kind):
        return DomainQueryValue(
            "temperature", "synthetic test temperature", DomainQueryKind.NUMERIC_INTERVAL,
            numeric_interval=QueryInterval(Quantity(lower, Unit.DEGREE_CELSIUS), lower_kind, Quantity(upper, Unit.DEGREE_CELSIUS), upper_kind),
        )
    tail = (category("apparatus", "synthetic apparatus identifier", "VESSEL-A"), source(2))
    inside = diagnose_observation_applicability(observation(), query(interval(10, BoundKind.INCLUSIVE, 29, BoundKind.INCLUSIVE), *tail), record_id="SYNTHETIC-M03-APP-INT-IN")
    partial = diagnose_observation_applicability(observation(), query(interval(5, BoundKind.INCLUSIVE, 15, BoundKind.INCLUSIVE), *tail), record_id="SYNTHETIC-M03-APP-INT-PART")
    outside = diagnose_observation_applicability(observation(), query(interval(30, BoundKind.INCLUSIVE, 35, BoundKind.INCLUSIVE), *tail), record_id="SYNTHETIC-M03-APP-INT-OUT")
    assert diagnostic(inside, "temperature").status is DomainDiagnosticStatus.INSIDE_DECLARED_DOMAIN
    assert diagnostic(partial, "temperature").status is DomainDiagnosticStatus.PARTIALLY_COMPARABLE
    assert partial.summary is ApplicabilitySummary.APPLICABILITY_INDETERMINATE
    assert diagnostic(outside, "temperature").status is DomainDiagnosticStatus.OUTSIDE_DECLARED_DOMAIN


def test_context_identity_and_property_definition_must_match_literally():
    result = diagnose_observation_applicability(observation(), full_query().__class__("SYNTHETIC-M03-Q2", "OTHER-OBS", "other_property", full_query().values, synthetic_provenance()), record_id="SYNTHETIC-M03-APP-ID")
    statuses = {item.status for item in result.diagnostics}
    assert DomainDiagnosticStatus.IDENTIFIER_MISMATCH in statuses
    assert DomainDiagnosticStatus.DEFINITION_MISMATCH in statuses


def test_query_interval_rejects_reversed_nonfinite_and_open_zero_width():
    with pytest.raises(ValueError, match="ordered"):
        QueryInterval(Quantity(2, Unit.MILLIMETRE), BoundKind.INCLUSIVE, Quantity(1, Unit.MILLIMETRE), BoundKind.INCLUSIVE)
    with pytest.raises(ValueError, match="zero-width"):
        QueryInterval(Quantity(1, Unit.MILLIMETRE), BoundKind.EXCLUSIVE, Quantity(1, Unit.MILLIMETRE), BoundKind.INCLUSIVE)
    with pytest.raises(ValueError, match="finite"):
        Quantity(float("nan"), Unit.MILLIMETRE)
