import csv
import hashlib
from pathlib import Path


def rows(path, key):
    with Path(path).open(newline="", encoding="utf-8") as handle:
        return {row[key]: row for row in csv.DictReader(handle)}


def test_m02_design_hash_and_equation_coverage_are_current():
    sources = rows("reference/source_ledger.csv", "source_id")
    source = sources["SRC-M02-DESIGN"]
    path = Path(source["url_or_local_path"])
    assert source["artifact_hash"] == f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"
    assert source["attribution_class"] == "modernized_powley"
    equations = rows("docs/provenance/equation_ledger.csv", "equation_id")
    for equation_id in ("EQ-108", "EQ-109"):
        assert equations[equation_id]["source_id"] == "SRC-M02-DESIGN"
        assert equations[equation_id]["implemented_in"].startswith("src/modern_powley/modernized/")
        assert equations[equation_id]["test_reference"].startswith("tests/")


def test_m02_schema_field_ledger_covers_identity_missing_domain_and_conflict():
    with Path("docs/provenance/data_field_ledger.csv").open(newline="", encoding="utf-8") as handle:
        fields = {row["field"] for row in csv.DictReader(handle) if row["data_asset"] == "modern_powley.m02.v1"}
    assert {
        "schema", "record_type", "record_id",
        "powder_identity.responsible_organization",
        "powder_identity.lot_or_batch",
        "powder_identity.product_class",
        "powder_identity_relationship.relationship",
        "property_definition.property_id",
        "property_definition.definition",
        "observation.value",
        "observation.source_locator",
        "missing_property_observation.missing_state",
        "applicability_domain.status",
        "applicability_domain.numeric_constraints",
        "applicability_domain.source_scalar_constraints",
        "conflict_comparison.numeric_comparison",
    } <= fields


def test_m02_completion_review_maps_all_fourteen_gates_and_scope_boundary():
    text = Path("docs/modernization/reviews/M02_completion_review.md").read_text(encoding="utf-8")
    for number in range(1, 15):
        assert f"| {number}." in text
    assert "Synthetic `SYNTHETIC-M02-*` fixtures only" in text
    assert "no production powder facts instantiated" in text
    assert "M03 is the next bounded phase" in text


def test_m02_design_explicitly_prohibits_preference_and_interpolation():
    text = Path("docs/modernization/decisions/M02_implementation_decisions.md").read_text(encoding="utf-8")
    assert "Source preference | Prohibited" in text
    assert "Interpolation/extrapolation | Prohibited" in text
    assert "Instantiate no real powder facts in M02" in text
