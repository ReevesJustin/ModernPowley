import json
from dataclasses import replace
from pathlib import Path

import pytest

from modern_powley.modernized import (
    M05_SCHEMA_ID, ActivationStatus, DependencyStatus, ExactReferenceRole,
    LifecycleMetadata, PressureEvidenceContext, RegionBasis, RegionState,
    SourceLocator, TranscriptionStatus, UncertaintyDeclaration,
    UncertaintyDeclarationKind, VersionedRegionReference,
    dumps_m05_record, loads_m05_record, m05_record_from_dict, m05_record_to_dict,
)
from tests.unit.test_m05_charge_regions import record, ref, segment


def test_strict_round_trip_preserves_units_order_metadata_and_is_deterministic():
    item = record(segments=(segment(10, 20), segment(21, 30)))
    data = m05_record_to_dict(item)
    assert data["schema"] == "modern_powley.m05.v1" == M05_SCHEMA_ID
    assert data["segments"][0]["lower"]["quantity"]["unit"] == "grain"
    assert m05_record_from_dict(data) == item
    assert loads_m05_record(dumps_m05_record(item)) == item
    assert loads_m05_record(dumps_m05_record(item, indent=None)) == item
    assert dumps_m05_record(item) == dumps_m05_record(item)


@pytest.mark.parametrize("state", list(RegionState))
def test_all_region_states_round_trip(state):
    if state is RegionState.BOUNDED:
        item = record()
    elif state is RegionState.EMPTY:
        item = record(state=state, segments=(), explanation="synthetic empty state")
    elif state is RegionState.CONFLICTING:
        item = record(
            state=state, basis=None, method=None, segments=(),
            explanation="synthetic conflicting state",
            conflict_references=(
                ref(ExactReferenceRole.M05_REGION, "SYN-CONFLICT-1"),
                ref(ExactReferenceRole.M05_REGION, "SYN-CONFLICT-2"),
            ),
        )
    else:
        item = record(state=state, basis=None, method=None, segments=(), explanation="synthetic state")
    assert loads_m05_record(dumps_m05_record(item)).state is state


@pytest.mark.parametrize("basis", list(RegionBasis))
def test_all_basis_values_round_trip_without_invoking_behavior(basis):
    item = record(basis=basis)
    assert loads_m05_record(dumps_m05_record(item)).basis is basis


@pytest.mark.parametrize("status", list(DependencyStatus))
def test_dependency_lifecycle_and_pressure_metadata_round_trip(status):
    dependency_references = (
        (ref(record_id="SYN-DEPENDENCY"),)
        if status is DependencyStatus.EXTERNALLY_REFERENCED else ()
    )
    pressure = PressureEvidenceContext(
        ref(ExactReferenceRole.M02_EVIDENCE, "SYN-PRESSURE"),
        "synthetic pressure identity", "synthetic method", "synthetic protocol",
        "synthetic instrument", "synthetic unit label", ("synthetic condition",),
        SourceLocator("SRC-M05-SYNTHETIC", "synthetic pressure locator", TranscriptionStatus.NOT_APPLICABLE),
        ("text context only",),
    )
    item = record(
        dependency_status=status,
        dependency_references=dependency_references,
        uncertainty=UncertaintyDeclaration(UncertaintyDeclarationKind.UNKNOWN, "synthetic unknown uncertainty"),
        pressure_contexts=(pressure,),
        lifecycle=LifecycleMetadata(
            ActivationStatus.INACTIVE,
            VersionedRegionReference("SYN-M05-PRIOR", 2),
        ),
    )
    decoded = loads_m05_record(dumps_m05_record(item))
    assert decoded == item
    assert decoded.pressure_contexts[0].source_unit_label == "synthetic unit label"
    assert decoded.lifecycle.activation is ActivationStatus.INACTIVE


def test_unknown_schema_type_field_missing_field_and_legacy_fail():
    data = m05_record_to_dict(record())
    for key, value in (("schema", "modern_powley.m05.v2"), ("record_type", "other")):
        changed = dict(data); changed[key] = value
        with pytest.raises(ValueError): m05_record_from_dict(changed)
    changed = dict(data); changed["unknown"] = 1
    with pytest.raises(ValueError): m05_record_from_dict(changed)
    changed = dict(data); changed.pop("state")
    with pytest.raises(ValueError): m05_record_from_dict(changed)
    changed = dict(data); changed["schema"] = "modern_powley.m04.v1"
    with pytest.raises(ValueError): m05_record_from_dict(changed)


def test_wrong_json_types_enums_units_lists_versions_and_nonfinite_fail():
    data = m05_record_to_dict(record())
    mutations = []
    for key, value in (("version", True), ("state", "safe"), ("basis", 3), ("segments", {})):
        changed = json.loads(json.dumps(data)); changed[key] = value; mutations.append(changed)
    bad_unit = json.loads(json.dumps(data)); bad_unit["segments"][0]["lower"]["quantity"]["unit"] = "psi"; mutations.append(bad_unit)
    bad_number = json.loads(json.dumps(data)); bad_number["segments"][0]["lower"]["quantity"]["value"] = "10"; mutations.append(bad_number)
    bad_nested = json.loads(json.dumps(data)); bad_nested["segments"][0]["lower"]["extra"] = 1; mutations.append(bad_nested)
    for changed in mutations:
        with pytest.raises((ValueError, TypeError)):
            m05_record_from_dict(changed)
    with pytest.raises(ValueError, match="non-finite"):
        loads_m05_record(dumps_m05_record(record()).replace("10.0", "NaN", 1))


def test_duplicate_json_keys_are_rejected():
    payload = dumps_m05_record(record())
    duplicate = payload.replace('"record_id": "SYN-M05-RECORD-1",', '"record_id": "SYN-M05-RECORD-1", "record_id": "OTHER",', 1)
    with pytest.raises(ValueError, match="duplicate JSON object key"):
        loads_m05_record(duplicate)


def test_partial_supersession_and_incomplete_nonimplication_fail():
    data = m05_record_to_dict(record())
    partial = json.loads(json.dumps(data)); partial["lifecycle"]["supersedes"] = {"region_id": "SYN-OLD"}
    with pytest.raises(ValueError): m05_record_from_dict(partial)
    incomplete = json.loads(json.dumps(data)); incomplete["non_implication"] = "not_recommended"
    with pytest.raises(ValueError): m05_record_from_dict(incomplete)


def test_no_m05_production_collection_or_prohibited_public_api():
    import modern_powley.modernized as modernized
    public = set(modernized.__all__)
    prohibited = {"estimate_charge_region", "derive_charge_region", "intersect_regions", "union_regions", "normalize_regions", "merge_regions", "rank_regions", "recommend_charge", "select_charge", "round_charge", "propagate_uncertainty", "simulate", "predict_pressure", "predict_velocity", "calculate_burn", "parse_grt", "plot_charge_region", "upload_grt"}
    assert prohibited.isdisjoint(public)
    assert not any("m05" in path.name.casefold() for path in Path("data").rglob("*"))


def test_m01_through_m04_schema_ids_remain_unchanged():
    import modern_powley.modernized as modernized
    assert modernized.SCHEMA_ID == "modern_powley.m01.v1"
    assert modernized.M02_SCHEMA_ID == "modern_powley.m02.v1"
    assert modernized.M03_SCHEMA_ID == "modern_powley.m03.v1"
    assert modernized.M04_SCHEMA_ID == "modern_powley.m04.v1"
