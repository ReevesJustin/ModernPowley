import json

import pytest

from modern_powley.modernized.provenance import EvidenceClass, ModelMaturity, Provenance, ValueOrigin
from modern_powley.modernized.records import CartridgeIdentity, SCHEMA_ID
from modern_powley.modernized.serialization import dumps_record, loads_record, record_from_dict


def provenance() -> Provenance:
    return Provenance(EvidenceClass.MANUFACTURER_PUBLISHED, ValueOrigin.MANUFACTURER_PUBLISHED, "SRC-MFR-EXAMPLE", ModelMaturity.RETAINED_CANDIDATE)


def test_all_documented_evidence_and_maturity_classes_are_machine_readable():
    assert {item.value for item in EvidenceClass} >= {
        "original_powley_primary", "later_powley_associated_primary", "other_published_primary",
        "manufacturer_published", "independent_laboratory_measurement", "user_measurement",
        "secondary_transcription", "reverse_engineered", "empirical_fit", "calibrated_parameter",
        "exploratory_hypothesis", "derived_quantity",
    }
    assert {item.value for item in ModelMaturity} == {
        "retained_candidate", "transcribed", "dimensionally_audited", "source_reconciled",
        "implemented_experimental", "measured_validated", "promoted_modern", "deprecated", "rejected",
    }


def test_supplied_and_derived_provenance_have_distinct_requirements():
    assert Provenance.from_dict(provenance().to_dict()) == provenance()
    with pytest.raises(ValueError, match="source_id"):
        Provenance(EvidenceClass.USER_MEASUREMENT, ValueOrigin.MEASURED, "", ModelMaturity.RETAINED_CANDIDATE)
    with pytest.raises(ValueError, match="method_id"):
        Provenance(EvidenceClass.DERIVED_QUANTITY, ValueOrigin.DERIVED, "SRC-M01-DESIGN", ModelMaturity.PROMOTED_MODERN)


def test_strict_versioned_json_round_trip():
    record = CartridgeIdentity("CARTRIDGE-308", ".308 Winchester", provenance(), ("7.62x51 family context only",))
    payload = dumps_record(record)
    decoded = json.loads(payload)
    assert decoded["schema"] == SCHEMA_ID
    assert decoded["record_type"] == "cartridge_identity"
    assert loads_record(payload) == record


def test_serialization_rejects_schema_record_and_unknown_field_errors():
    record = CartridgeIdentity("CARTRIDGE-308", ".308 Winchester", provenance())
    data = record.to_dict()
    for mutation, match in (
        ({key: value for key, value in data.items() if key != "schema"}, "missing schema"),
        (data | {"schema": "modern_powley.m01.v2"}, "unsupported schema"),
        (data | {"record_type": "unknown"}, "unsupported record_type"),
        (data | {"critical_new_field": 1}, "malformed fields"),
    ):
        with pytest.raises(ValueError, match=match):
            record_from_dict(mutation)


def test_json_rejects_nonfinite_numbers():
    with pytest.raises(ValueError, match="non-finite"):
        loads_record('{"schema":"modern_powley.m01.v1","record_type":"cartridge_identity","value":NaN}')
