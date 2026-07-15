import json
from dataclasses import replace

import pytest

from modern_powley.modernized import (
    ApplicabilityDomain, BoundKind, CategoricalDomainConstraint, DomainBound,
    DomainQueryContext, DomainQueryKind, DomainQueryValue, DomainStatus,
    InputBundle, InputCandidate, InputCandidateKind, NumericDomainConstraint,
    Quantity, Unit, diagnose_observation_applicability, dumps_m03_record,
    evaluate_input_completeness, loads_m03_record, m03_record_from_dict,
    production_requirement_sets,
)
from tests.unit.test_m02_identity_properties_and_missing import bulk_observation, physical, synthetic_provenance


def circle_inputs():
    return InputBundle(
        "SYNTHETIC-M03-SERIAL-BUNDLE",
        (InputCandidate("SYNTHETIC-M03-DIAMETER", "diameter", InputCandidateKind.PHYSICAL_VALUE, "SYNTHETIC-M03-DIAMETER-RECORD", synthetic_provenance(), Quantity(7.62, Unit.MILLIMETRE)),),
        synthetic_provenance(), "synthetic serialization fixture",
    )


def declared_observation():
    domain = ApplicabilityDomain(
        DomainStatus.DECLARED,
        (NumericDomainConstraint("temperature", "synthetic temperature", DomainBound(BoundKind.INCLUSIVE, physical("SYNTHETIC-M03-LOW", 10, Unit.DEGREE_CELSIUS)), DomainBound(BoundKind.INCLUSIVE, physical("SYNTHETIC-M03-HIGH", 30, Unit.DEGREE_CELSIUS))),),
        (CategoricalDomainConstraint("apparatus", "synthetic apparatus", ("VESSEL-A",)),),
        "synthetic declared domain",
    )
    return replace(bulk_observation("SYNTHETIC-M03-SERIAL-OBS"), applicability_domain=domain)


def query_context():
    return DomainQueryContext(
        "SYNTHETIC-M03-SERIAL-QUERY", "SYNTHETIC-M03-SERIAL-OBS", "bulk_density",
        (
            DomainQueryValue("temperature", "synthetic temperature", DomainQueryKind.NUMERIC_POINT, numeric_point=Quantity(20, Unit.DEGREE_CELSIUS)),
            DomainQueryValue("apparatus", "synthetic apparatus", DomainQueryKind.CATEGORICAL, category_or_identifier="VESSEL-A"),
        ), synthetic_provenance(),
    )


def records():
    requirement_set = next(item for item in production_requirement_sets() if item.requirement_set_id == "circle_area")
    bundle = circle_inputs()
    completeness = evaluate_input_completeness(requirement_set, bundle, record_id="SYNTHETIC-M03-SERIAL-COMPLETE")
    query = query_context()
    applicability = diagnose_observation_applicability(declared_observation(), query, record_id="SYNTHETIC-M03-SERIAL-APP")
    return requirement_set, bundle, completeness, query, applicability


@pytest.mark.parametrize("index", range(5))
def test_every_m03_record_type_round_trips_strictly(index):
    record = records()[index]
    payload = dumps_m03_record(record)
    assert json.loads(payload)["schema"] == "modern_powley.m03.v1"
    assert loads_m03_record(payload) == record


@pytest.mark.parametrize("schema", ["modern_powley.m03.v2", "modern_powley.m02.v1", ""])
def test_unsupported_schema_versions_fail(schema):
    data = records()[0].to_dict()
    data["schema"] = schema
    with pytest.raises(ValueError, match="unsupported|invalid"):
        m03_record_from_dict(data)


def test_unknown_top_level_and_nested_fields_fail():
    top = records()[1].to_dict()
    top["silent"] = "not allowed"
    with pytest.raises(ValueError, match="expected"):
        m03_record_from_dict(top)
    nested = records()[0].to_dict()
    nested["requirements"][0]["silent"] = "not allowed"
    with pytest.raises(ValueError, match="expected"):
        m03_record_from_dict(nested)


@pytest.mark.parametrize("payload", ["{}", '{"schema":"modern_powley.m03.v1"}', '{"schema":"modern_powley.m03.v1","record_type":"future"}', '{"schema":"modern_powley.m03.v1","record_type":"input_bundle","value":NaN}'])
def test_missing_malformed_unknown_and_nonfinite_payloads_fail(payload):
    with pytest.raises(ValueError):
        loads_m03_record(payload)


def test_m01_and_m02_schema_identifiers_remain_distinct_and_unchanged():
    from modern_powley.modernized import M02_SCHEMA_ID, M03_SCHEMA_ID, SCHEMA_ID

    assert SCHEMA_ID == "modern_powley.m01.v1"
    assert M02_SCHEMA_ID == "modern_powley.m02.v1"
    assert M03_SCHEMA_ID == "modern_powley.m03.v1"


def test_positive_summary_cannot_disagree_with_diagnostics():
    complete = records()[2]
    with pytest.raises(ValueError, match="Boolean"):
        replace(complete, all_declared_conditions_satisfied=False)
    applicability = records()[4]
    from modern_powley.modernized import ApplicabilitySummary
    with pytest.raises(ValueError, match="summary"):
        replace(applicability, summary=ApplicabilitySummary.APPLICABILITY_INDETERMINATE)
