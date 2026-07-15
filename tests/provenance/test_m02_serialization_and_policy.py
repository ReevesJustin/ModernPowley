import json

import pytest

from modern_powley.modernized import (
    ApplicabilityDomain,
    M02_SCHEMA_ID,
    MissingPropertyObservation,
    MissingState,
    PowderIdentityRelationship,
    PowderRelationshipKind,
    dumps_m02_record,
    dumps_record,
    loads_m02_record,
    loads_record,
    m02_record_from_dict,
    compare_property_observations,
)
from tests.unit.test_m02_identity_properties_and_missing import (
    bulk_observation,
    synthetic_identity,
    synthetic_provenance,
)


def records():
    identity = synthetic_identity()
    relationship = PowderIdentityRelationship(
        "SYNTHETIC-M02-REL", identity.record_id,
        PowderRelationshipKind.RELATED_TO, "SYNTHETIC-M02-POWDER-B",
        "synthetic relationship wording", "synthetic fixture locator",
        synthetic_provenance(),
    )
    observation = bulk_observation()
    missing = MissingPropertyObservation(
        "SYNTHETIC-M02-MISSING", identity.record_id,
        observation.property_definition, MissingState.NOT_PUBLISHED,
        observation.provenance, observation.source_locator,
        "synthetic source publishes no value", "M02 serialization test", True,
        (), ApplicabilityDomain.unspecified("source domain unavailable"),
    )
    comparison = compare_property_observations(
        observation, bulk_observation("SYNTHETIC-M02-OBS-B", 0.81),
        result_id="SYNTHETIC-M02-COMPARISON",
    )
    return identity, relationship, observation, missing, comparison


@pytest.mark.parametrize("record", records())
def test_m02_records_round_trip_strict_versioned_json(record):
    payload = dumps_m02_record(record)
    decoded = json.loads(payload)
    assert decoded["schema"] == M02_SCHEMA_ID
    assert loads_m02_record(payload) == record


def test_m02_rejects_missing_future_unknown_and_nonfinite_json():
    data = synthetic_identity().to_dict()
    for mutation, match in (
        ({key: value for key, value in data.items() if key != "schema"}, "missing schema"),
        (data | {"schema": "modern_powley.m02.v2"}, "unsupported schema"),
        (data | {"record_type": "future_record"}, "unsupported record_type"),
        (data | {"silently_ignored": "forbidden"}, "malformed"),
    ):
        with pytest.raises(ValueError, match=match):
            m02_record_from_dict(mutation)
    with pytest.raises(ValueError, match="non-finite"):
        loads_m02_record('{"schema":"modern_powley.m02.v1","record_type":"powder_identity","value":NaN}')


def test_m01_schema_round_trip_is_unchanged_and_not_accepted_as_m02():
    from modern_powley.modernized import CartridgeIdentity

    m01 = CartridgeIdentity("SYNTHETIC-M01-CARTRIDGE", "synthetic cartridge", synthetic_provenance())
    assert loads_record(dumps_record(m01)) == m01
    with pytest.raises(ValueError, match="unsupported schema"):
        loads_m02_record(dumps_record(m01))


def test_missing_record_has_no_numeric_sentinel_or_omitted_state():
    missing = records()[3]
    data = json.loads(dumps_m02_record(missing))
    assert data["missing_state"] == "not_published"
    assert "value" not in data
    with pytest.raises(ValueError, match="malformed"):
        m02_record_from_dict({key: value for key, value in data.items() if key != "missing_state"})
