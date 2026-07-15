import ast
import json
from pathlib import Path

import pytest

import modern_powley.modernized as modernized
from modern_powley.modernized import (
    CriterionForm,
    CriterionOutcomeStatus,
    CriterionSetSummary,
    EvaluationContext,
    M04_SCHEMA_ID,
    OutcomeCounts,
    CriterionSetOutcomeRecord,
    dumps_m04_record,
    evaluate_criterion,
    loads_m04_record,
    m04_record_from_dict,
)
from tests.unit.test_m04_screening_records import (
    context,
    criterion,
    criterion_set,
    literal_reference,
    locator,
    provenance,
)


def records():
    item = criterion()
    set_definition = criterion_set(item)
    evaluation_context = context(literal_reference())
    outcome = evaluate_criterion(
        item, set_definition, evaluation_context,
        record_id="SYNTHETIC-M04-SERIAL-OUTCOME",
        provenance=provenance(), source_locator=locator(),
    )
    summary = CriterionSetOutcomeRecord(
        "SYNTHETIC-M04-SERIAL-SUMMARY",
        set_definition.criterion_set_id,
        set_definition.version,
        evaluation_context.record_id,
        (outcome.record_id,),
        CriterionSetSummary.ALL_MANDATORY_RECORDED_PASSES,
        OutcomeCounts(1, 0, 0, 0, 0),
        "Every synthetic mandatory criterion has an exact recorded pass.",
        set_definition.non_implication_statement,
        provenance(),
    )
    return item, set_definition, evaluation_context, outcome, summary


@pytest.mark.parametrize("record", records())
def test_m04_v1_records_round_trip_strictly(record):
    payload = dumps_m04_record(record)
    decoded = loads_m04_record(payload)
    assert decoded == record
    parsed = json.loads(payload)
    assert parsed["schema"] == "modern_powley.m04.v1"
    assert dumps_m04_record(decoded) == payload


def test_unsupported_schema_record_type_unknown_fields_and_nonfinite_fail():
    payload = records()[0].to_dict()
    with pytest.raises(ValueError, match="unsupported schema"):
        m04_record_from_dict({**payload, "schema": "modern_powley.m04.v2"})
    with pytest.raises(ValueError, match="unsupported record_type"):
        m04_record_from_dict({**payload, "record_type": "powder_catalog"})
    with pytest.raises(ValueError, match="expected fields"):
        m04_record_from_dict({**payload, "unexpected": "not ignored"})
    with pytest.raises(ValueError, match="non-finite"):
        loads_m04_record('{"schema":"modern_powley.m04.v1","record_type":"criterion_definition","value":NaN}')


def test_malformed_threshold_embedded_evidence_and_versions_fail():
    item, _, _, outcome, _ = records()
    malformed_threshold = item.to_dict()
    malformed_threshold["threshold"] = {**malformed_threshold["threshold"], "extra": True}
    with pytest.raises(ValueError, match="expected fields"):
        m04_record_from_dict(malformed_threshold)
    malformed_evidence = outcome.to_dict()
    malformed_evidence["supplied_values"][0]["extra"] = True
    with pytest.raises(ValueError, match="expected fields"):
        m04_record_from_dict(malformed_evidence)
    bad_version = item.to_dict()
    bad_version["version"] = True
    with pytest.raises(TypeError, match="integer"):
        m04_record_from_dict(bad_version)


def test_m01_m02_and_m03_schema_identifiers_are_unchanged():
    assert modernized.SCHEMA_ID == "modern_powley.m01.v1"
    assert modernized.M02_SCHEMA_ID == "modern_powley.m02.v1"
    assert modernized.M03_SCHEMA_ID == "modern_powley.m03.v1"
    assert M04_SCHEMA_ID == "modern_powley.m04.v1"


def test_no_prohibited_discovery_ranking_solver_or_prediction_public_api():
    prohibited = {
        "find_observation", "select_observation", "preferred_observation", "best_record",
        "latest_record", "resolve_conflict", "choose_powder", "screen_powders",
        "eligible_powders", "suitable_powders", "rank_powders", "recommended_powders",
        "score_candidate", "solver_ready", "load_ready", "estimate_pressure",
        "estimate_velocity", "predict_burn", "recommend_charge",
    }
    assert prohibited.isdisjoint(modernized.__all__)
    assert not hasattr(modernized.CriterionDefinition, "weight")
    assert not hasattr(modernized.CriterionDefinition, "score")
    assert not hasattr(modernized.CriterionSetDefinition, "weights")


def imported_modules(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module)
    return imports


def test_m04_import_boundary_and_original_reverse_boundary():
    root = Path("src/modern_powley")
    m04_files = (
        "screening_criteria.py", "screening_contexts.py", "screening_outcomes.py",
        "criterion_evaluation.py", "m04_serialization.py",
    )
    forbidden = ("later", "experimental", "emulator", "grt", "jrt", "quickload", "legacy")
    for name in m04_files:
        imports = imported_modules(root / "modernized" / name)
        assert not any(any(token in module.casefold() for token in forbidden) for module in imports)
    for path in (root / "original").glob("*.py"):
        assert "modernized" not in path.read_text(encoding="utf-8")


def test_no_production_criterion_set_or_powder_database_is_added():
    root = Path("src/modern_powley/modernized")
    text = "\n".join(path.read_text(encoding="utf-8") for path in root.glob("*.py"))
    assert "production_criterion_sets" not in text
    assert "powder_catalog" not in text
    assert "criterion_weight" not in text
    assert "pass_percentage" not in text
    assert "SYNTHETIC_POWDER_ALPHA" not in text


def test_manual_form_cannot_be_mechanically_recorded_as_pass():
    item = criterion(CriterionForm.EXPLICIT_MANUAL_ASSERTION, None)
    result = evaluate_criterion(
        item, criterion_set(item), context(literal_reference()),
        record_id="SYNTHETIC-M04-MANUAL-REFUSED",
        provenance=provenance(), source_locator=locator(),
    )
    assert result.result is CriterionOutcomeStatus.UNSUPPORTED_COMPARISON
    assert result.manual_assertion is None
    assert isinstance(context(literal_reference()), EvaluationContext)
