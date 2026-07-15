import csv
import hashlib
from pathlib import Path

from modern_powley.modernized import SCHEMA_ID


def _rows(path: str, key: str) -> dict[str, dict[str, str]]:
    with Path(path).open(newline="", encoding="utf-8") as handle:
        return {row[key]: row for row in csv.DictReader(handle)}


def test_m01_design_artifact_hash_and_classification_are_current():
    sources = _rows("reference/source_ledger.csv", "source_id")
    row = sources["SRC-M01-DESIGN"]
    digest = hashlib.sha256(
        Path(row["url_or_local_path"]).read_bytes()
    ).hexdigest()
    assert row["artifact_hash"] == f"sha256:{digest}"
    assert row["attribution_class"] == "modernized_powley"
    assert row["notes"].startswith("Repository-authored design authority")


def test_all_promoted_m01_geometry_relations_are_ledgered_and_tested():
    equations = _rows("docs/provenance/equation_ledger.csv", "equation_id")
    for number in range(92, 108):
        row = equations[f"EQ-{number:03d}"]
        assert row["implemented_in"].startswith("src/modern_powley/modernized/")
        assert row["test_reference"].startswith("tests/")
        assert row["disposition"]
    assert equations["EQ-105"]["attribution_class"] == "original_powley"
    assert "explicit" in equations["EQ-105"]["disposition"]


def test_m01_constants_and_schema_fields_have_ledger_coverage():
    constants = _rows("docs/provenance/constant_ledger.csv", "constant_id")
    for number in range(42, 46):
        row = constants[f"CONST-{number:03d}"]
        assert row["attribution_class"] == "modernized_powley"
        assert row["verification_status"] == "verified_primary"

    with Path("docs/provenance/data_field_ledger.csv").open(
        newline="", encoding="utf-8"
    ) as handle:
        fields = [row for row in csv.DictReader(handle) if row["data_asset"] == SCHEMA_ID]
    names = {row["field"] for row in fields}
    assert {
        "schema",
        "record_type",
        "record_id",
        "quantity.value",
        "quantity.unit",
        "provenance.evidence_class",
        "uncertainty.kind",
        "gross_case_capacity.water_mass",
        "measured_usable_powder_space.water_mass",
        "estimated_usable_powder_space.usable_volume",
        "barrel_volume_ratio",
        "total_expansion_ratio",
    } <= names


def test_m01_completion_review_maps_every_acceptance_gate():
    text = Path("docs/modernization/reviews/M01_completion_review.md").read_text(
        encoding="utf-8"
    )
    for phrase in (
        "Every dimensional field has units and provenance",
        "Measured and estimated capacities cannot be confused",
        "Unit conversions round-trip",
        "Water conversion is explicit",
        "No modern behavior enters `original/`",
        "No ballistics prediction, screening, ranking, or interface",
    ):
        assert phrase in text
    assert "M02 is the next phase" in text
