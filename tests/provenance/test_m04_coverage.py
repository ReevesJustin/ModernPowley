import csv
import hashlib
from pathlib import Path


def rows(path, key):
    with Path(path).open(newline="", encoding="utf-8") as handle:
        return {row[key]: row for row in csv.DictReader(handle)}


def test_m04_design_hash_and_logical_derivations_are_ledgered():
    sources = rows("reference/source_ledger.csv", "source_id")
    source = sources["SRC-M04-DESIGN"]
    path = Path(source["url_or_local_path"])
    assert source["artifact_hash"] == f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"
    equations = rows("docs/provenance/equation_ledger.csv", "equation_id")
    assert {"EQ-113", "EQ-114"} <= equations.keys()
    assert equations["EQ-113"]["implemented_in"].endswith("criterion_evaluation.py")
    assert equations["EQ-114"]["source_id"] == "SRC-M04-DESIGN"


def test_m04_schema_fields_are_ledgered_without_container_equations():
    with Path("docs/provenance/data_field_ledger.csv").open(newline="", encoding="utf-8") as handle:
        fields = {
            row["field"] for row in csv.DictReader(handle)
            if row["data_asset"] == "modern_powley.m04.v1"
        }
    assert {
        "schema", "record_type", "criterion_definition",
        "criterion_set_definition.criteria", "evaluation_context.evidence_references",
        "criterion_evaluation.result", "criterion_evaluation.evaluation_method",
        "criterion_evaluation.supplied_values", "criterion_set_outcome.summary",
        "criterion_set_outcome.counts",
    } <= fields


def test_m04_documents_preserve_record_only_boundary_and_non_implications():
    phase = Path("docs/modernization/phases/M04_screening_decision_records.md").read_text(encoding="utf-8")
    spec = Path("docs/modernization/milestones/M04_screening_decision_records.md").read_text(encoding="utf-8")
    decisions = Path("docs/modernization/decisions/M04_implementation_decisions.md").read_text(encoding="utf-8")
    assert "not a\ngeneral powder-screening engine" in spec
    assert "No production criterion definitions" in phase
    assert "establishes physical correctness" in phase
    assert "Scores and ranking" in decisions and "Prohibited" in decisions
    assert "18. Durable milestone governance" in spec
