import ast
from dataclasses import replace
import json
from pathlib import Path

import pytest

from modern_powley.modernized.empirical_load_records import (
    EMPIRICAL_LOAD_EVIDENCE_SCHEMA_ID,
    ActivationState,
    AggregateSummaryRecord,
    EmpiricalRecordType,
    EvidenceUncertaintyKind,
    ExclusionState,
    MissingValue,
    PrecisionKind,
    RecordEnvelope,
    ReferenceRole,
    ReportedValueKind,
    ReviewState,
    TraceArtifactState,
    VelocityCorrectionState,
)
from modern_powley.modernized.empirical_load_serialization import (
    dumps_empirical_load_record,
    empirical_load_record_from_dict,
    empirical_load_record_to_dict,
    loads_empirical_load_record,
)
from modern_powley.modernized.missing_values import MissingState
from tests.unit.test_empirical_load_evidence_records import (
    aggregate_record,
    all_records,
    chronograph_record,
    envelope,
    literal_record,
    missing_value,
    pressure,
    ref,
    reported,
    shot_record,
    source_record,
    trace_record,
    velocity,
)


@pytest.mark.parametrize("record", all_records(), ids=lambda item: item.envelope.record_type.value)
def test_all_eight_record_families_round_trip_exactly(record):
    data = empirical_load_record_to_dict(record)
    assert data["schema"] == EMPIRICAL_LOAD_EVIDENCE_SCHEMA_ID
    assert data["schema_version"] == 1
    assert data["record_type"] == record.envelope.record_type.value
    assert empirical_load_record_from_dict(data) == record
    assert loads_empirical_load_record(dumps_empirical_load_record(record)) == record
    assert loads_empirical_load_record(dumps_empirical_load_record(record, indent=None)) == record


def test_repository_json_output_is_deterministic_but_precision_remains_text():
    item = literal_record()
    first = dumps_empirical_load_record(item)
    assert first == dumps_empirical_load_record(item)
    data = json.loads(first)
    declared = data["payload"]["declared_values"][0]
    assert declared["decimal_text"] == "0.1234"
    assert isinstance(declared["decimal_text"], str)
    assert declared["precision"]["digits"] == 4


@pytest.mark.parametrize("state", list(MissingState))
def test_every_m02_missing_state_survives_round_trip(state):
    item = shot_record(
        pressure_observations=(),
        pressure_missing=MissingValue(state=state, explanation="synthetic missing state"),
    )
    decoded = loads_empirical_load_record(dumps_empirical_load_record(item))
    assert decoded.pressure_missing.state is state


def test_conflicts_exclusion_supersession_inactivity_and_lineage_survive():
    literal = loads_empirical_load_record(dumps_empirical_load_record(literal_record()))
    shot = loads_empirical_load_record(dumps_empirical_load_record(shot_record()))
    aggregate = loads_empirical_load_record(dumps_empirical_load_record(aggregate_record()))
    assert len(literal.envelope.conflicts[0].members) == 2
    assert literal.envelope.lineage[0].role is ReferenceRole.DUPLICATE_PUBLICATION_OF
    assert shot.exclusion.state is ExclusionState.EXCLUDED
    assert aggregate.envelope.activation is ActivationState.INACTIVE
    assert aggregate.envelope.supersedes.record_id == "SYN-ELE-AGGREGATE-PRIOR"


@pytest.mark.parametrize("state", list(TraceArtifactState))
def test_trace_artifact_states_round_trip_without_sample_field(state):
    data = empirical_load_record_to_dict(trace_record(state))
    assert "samples" not in data["payload"]
    assert empirical_load_record_from_dict(data).artifact_state is state


@pytest.mark.parametrize("state", list(VelocityCorrectionState))
def test_velocity_correction_states_round_trip_without_correction(state):
    item = aggregate_record(value=velocity(level=velocity().observation_level.AGGREGATE, correction=state))
    decoded = loads_empirical_load_record(dumps_empirical_load_record(item))
    assert decoded.value.correction_state is state


@pytest.mark.parametrize("state", list(ReviewState))
def test_review_states_round_trip_independently(state):
    reviewed = state in {ReviewState.REVIEWED, ReviewState.QUALIFIED}
    from tests.unit.test_empirical_load_evidence_records import review

    item = source_record(envelope=envelope(EmpiricalRecordType.SOURCE_CUSTODY, review=review(state)))
    decoded = loads_empirical_load_record(dumps_empirical_load_record(item))
    assert decoded.envelope.review.state is state
    assert (decoded.envelope.review.reviewed_by.value is not None) is reviewed


def test_unknown_top_level_schema_version_type_and_fields_fail():
    data = empirical_load_record_to_dict(source_record())
    changes = []
    for key, value in (
        ("schema", "modern_powley.empirical_load_evidence.v2"),
        ("schema_version", 2),
        ("record_type", "dataset_cohort"),
    ):
        changed = json.loads(json.dumps(data))
        changed[key] = value
        changes.append(changed)
    unknown = json.loads(json.dumps(data)); unknown["unknown"] = True; changes.append(unknown)
    missing = json.loads(json.dumps(data)); missing.pop("payload"); changes.append(missing)
    for changed in changes:
        with pytest.raises((ValueError, TypeError)):
            empirical_load_record_from_dict(changed)


def test_unknown_nested_fields_missing_fields_aliases_and_discriminator_mismatch_fail():
    data = empirical_load_record_to_dict(source_record())
    nested = json.loads(json.dumps(data)); nested["envelope"]["extra"] = 1
    payload = json.loads(json.dumps(data)); payload["payload"]["extra"] = 1
    missing = json.loads(json.dumps(data)); missing["envelope"].pop("record_version")
    alias = json.loads(json.dumps(data)); alias["envelope"]["version"] = alias["envelope"].pop("record_version")
    mismatch = json.loads(json.dumps(data)); mismatch["envelope"]["record_type"] = "shot_observation"
    for changed in (nested, payload, missing, alias, mismatch):
        with pytest.raises((ValueError, TypeError)):
            empirical_load_record_from_dict(changed)


def test_string_number_boolean_and_collection_coercions_fail():
    data = empirical_load_record_to_dict(source_record())
    mutations = []
    for path, value in (
        (("schema_version",), "1"),
        (("envelope", "record_version"), True),
        (("envelope", "synthetic_fixture"), 1),
        (("envelope", "record_id"), 123),
        (("payload", "artifacts"), {}),
        (("payload", "source_title"), 12),
    ):
        changed = json.loads(json.dumps(data))
        target = changed
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value
        mutations.append(changed)
    for changed in mutations:
        with pytest.raises((ValueError, TypeError)):
            empirical_load_record_from_dict(changed)


def test_nonfinite_json_and_duplicate_keys_fail():
    payload = dumps_empirical_load_record(source_record())
    with pytest.raises(ValueError, match="non-finite"):
        loads_empirical_load_record(payload.replace('"schema_version": 1', '"schema_version": NaN'))
    duplicate = payload.replace(
        '"schema_version": 1',
        '"schema_version": 1, "schema_version": 1',
        1,
    )
    with pytest.raises(ValueError, match="duplicate JSON object key"):
        loads_empirical_load_record(duplicate)


def test_strict_nested_units_decimals_enums_and_tagged_unions_fail():
    load = empirical_load_record_to_dict(all_records()[2])
    bad_unit = json.loads(json.dumps(load)); bad_unit["payload"]["charge"]["value"]["quantity"]["unit"] = "psi"
    bad_number = json.loads(json.dumps(load)); bad_number["payload"]["charge"]["value"]["quantity"]["value"] = "1"
    bad_decimal = json.loads(json.dumps(load)); bad_decimal["payload"]["charge"]["value"]["source_value_text"] = 1.0
    bad_tag = json.loads(json.dumps(load)); bad_tag["payload"]["charge"]["kind"] = "default"
    bad_enum = json.loads(json.dumps(load)); bad_enum["envelope"]["activation"] = "approved"
    for changed in (bad_unit, bad_number, bad_decimal, bad_tag, bad_enum):
        with pytest.raises((ValueError, TypeError)):
            empirical_load_record_from_dict(changed)


def test_record_class_and_envelope_discriminator_must_match():
    item = source_record()
    with pytest.raises(ValueError, match="source_custody"):
        replace(item, envelope=replace(item.envelope, record_type=EmpiricalRecordType.LITERAL_LOAD_STATEMENT))


def test_schema_does_not_accept_m05_or_legacy_unversioned_records():
    with pytest.raises(ValueError):
        empirical_load_record_from_dict({"schema": "modern_powley.m05.v1"})
    with pytest.raises(ValueError):
        empirical_load_record_from_dict({"record_type": "source_custody"})


def test_phase1_is_module_qualified_and_package_root_exports_are_unchanged():
    import modern_powley.modernized as modernized

    phase_names = {
        "EMPIRICAL_LOAD_EVIDENCE_SCHEMA_ID",
        "SourceCustodyRecord",
        "LiteralLoadStatementRecord",
        "PhysicalLoadConfigurationRecord",
        "ShotObservationRecord",
        "LoadSeriesRecord",
        "PressureTraceMetadataRecord",
        "ChronographSeriesRecord",
        "AggregateSummaryRecord",
        "dumps_empirical_load_record",
        "loads_empirical_load_record",
    }
    assert phase_names.isdisjoint(modernized.__all__)
    assert all(not hasattr(modernized, name) for name in phase_names)


def test_phase1_modules_have_no_prohibited_behavior_or_dependencies():
    modules = (
        Path("src/modern_powley/modernized/empirical_load_records.py"),
        Path("src/modern_powley/modernized/empirical_load_serialization.py"),
    )
    prohibited_definitions = {
        "cohort", "split", "ingest", "parse_source", "adapt", "derive",
        "intersect", "fit", "regress", "predict", "rank", "recommend",
        "select", "calculate", "average", "filter", "resample", "plot",
        "upload", "safe", "suitable",
    }
    forbidden_import_parts = {
        "original", "later", "experimental", "charge_regions", "m05_serialization",
        "pandas", "polars", "sqlalchemy", "requests", "matplotlib", "plotly",
    }
    for path in modules:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        public = {
            node.name.casefold()
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
            and not node.name.startswith("_")
        }
        assert not {
            name for name in public
            if any(token in name for token in prohibited_definitions)
        }, path
        imported = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imported.append(node.module or "")
        assert not [
            name for name in imported
            if forbidden_import_parts.intersection(name.casefold().split("."))
        ], path


def test_no_trace_samples_cohort_split_model_or_production_collection_exists():
    records_text = Path("src/modern_powley/modernized/empirical_load_records.py").read_text(encoding="utf-8")
    for class_name in (
        "DatasetCohort", "DatasetSplit", "CalibrationAssignment",
        "ValidationAssignment", "PressureTraceSamples", "ModelFit",
    ):
        assert f"class {class_name}" not in records_text
    assert not list(Path("data").rglob("*empirical_load*"))
    assert not list(Path("reference").rglob("*empirical_load*"))


def test_all_controlled_value_kinds_precision_and_uncertainty_enums_are_serializable():
    for kind in ReportedValueKind:
        source_kind = "synthetic custom kind" if kind is ReportedValueKind.OTHER_SOURCE_DEFINED else None
        item = reported(kind, source_defined_kind=source_kind)
        assert item.kind is kind
    assert set(PrecisionKind)
    assert set(EvidenceUncertaintyKind)


def test_external_aggregate_preserves_members_and_does_not_calculate():
    item = aggregate_record()
    decoded = empirical_load_record_from_dict(empirical_load_record_to_dict(item))
    assert isinstance(decoded, AggregateSummaryRecord)
    assert decoded.member_references == item.member_references
    assert not hasattr(decoded, "calculate")
