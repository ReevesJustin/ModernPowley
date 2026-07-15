import csv
import hashlib
from pathlib import Path

from modern_powley.modernized import production_requirement_sets


def rows(path, key):
    with Path(path).open(newline="", encoding="utf-8") as handle:
        return {row[key]: row for row in csv.DictReader(handle)}


def test_m03_design_hash_and_method_coverage_are_current():
    sources = rows("reference/source_ledger.csv", "source_id")
    source = sources["SRC-M03-DESIGN"]
    path = Path(source["url_or_local_path"])
    assert source["artifact_hash"] == f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"
    equations = rows("docs/provenance/equation_ledger.csv", "equation_id")
    assert {"EQ-110", "EQ-111", "EQ-112"} <= equations.keys()
    assert all(equations[item]["source_id"] == "SRC-M03-DESIGN" for item in ("EQ-110", "EQ-111", "EQ-112"))


def test_m03_schema_fields_and_production_sets_are_ledgered_and_bounded():
    with Path("docs/provenance/data_field_ledger.csv").open(newline="", encoding="utf-8") as handle:
        fields = {row["field"] for row in csv.DictReader(handle) if row["data_asset"] == "modern_powley.m03.v1"}
    assert {"schema", "record_type", "requirement_set.requirements", "input_bundle.candidates", "completeness_evaluation.diagnostics", "domain_query_context.values", "applicability_evaluation.diagnostics"} <= fields
    sets = production_requirement_sets()
    assert sets and all(item.operation_already_exists for item in sets)
    prohibited = ("pressure", "velocity", "burn", "powder_screen", "solver", "safety", "rank")
    assert not [item.operation_id for item in sets if any(token in item.operation_id.casefold() for token in prohibited)]


def test_m03_status_documents_preserve_diagnostic_only_boundary():
    phase = Path("docs/modernization/phases/M03_input_and_domain_diagnostics.md").read_text(encoding="utf-8")
    review = Path("docs/modernization/reviews/M03_completion_review.md").read_text(encoding="utf-8")
    assert "implemented_and_reviewed" in phase and "implemented_and_reviewed" in review
    assert "execute geometry" in phase and "diagnostic layer" in phase
    assert "powder suitability" in phase and "safety classification" in phase
    assert "M04 remains" in review and "inclusion decision" in review
