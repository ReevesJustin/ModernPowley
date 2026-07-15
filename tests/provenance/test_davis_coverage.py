import ast
import csv
from pathlib import Path


DAVIS_EQUATIONS = {
    "seating_depth_inches": "EQ-061",
    "flat_base_displacement_water_grains": "EQ-062",
    "boat_tail_correction_water_grains": "EQ-063",
    "loaded_powder_space_capacity_water_grains": "EQ-064",
    "bullet_travel_inches": "EQ-066",
    "powder_chamber_volume_cubic_inches": "EQ-067",
    "effective_bore_volume_cubic_inches": "EQ-068",
    "expansion_ratio": "EQ-069",
    "initial_charge_weight_grains": "EQ-070",
    "mass_ratio": "EQ-072",
    "sectional_density": "EQ-073",
    "powder_selection_index": "EQ-012",
    "velocity_fraction_m": "EQ-074",
    "velocity_fraction_n": "EQ-075",
    "effective_moving_weight_grains": "EQ-076",
    "muzzle_velocity_fps": "EQ-077",
    "pressure_terms": "EQ-078",
    "historical_crusher_pressure": "EQ-081",
    "lookup_table4_f2": "EQ-084",
    "loading_density_pressure_scale": "EQ-082",
    "charge_for_target_loading_density": "EQ-083",
}


def test_every_davis_equation_function_has_primary_or_interpretive_ledger_coverage():
    rows = list(csv.DictReader(Path("docs/provenance/equation_ledger.csv").open(newline="", encoding="utf-8")))
    by_id = {row["equation_id"]: row for row in rows}
    module = Path("src/modern_powley/later/davis.py")
    tree = ast.parse(module.read_text(encoding="utf-8"), filename=str(module))
    functions = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
    assert set(DAVIS_EQUATIONS) <= functions
    for function_name, equation_id in DAVIS_EQUATIONS.items():
        row = by_id[equation_id]
        assert row["implemented_in"] == str(module), function_name
        assert row["source_id"], function_name
        assert row["test_reference"] not in {"", "none"}, function_name
        assert row["attribution_class"] in {"davis", "unknown"}, function_name


def test_original_namespace_does_not_import_davis_module_or_table():
    for path in Path("src/modern_powley/original").glob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "later.davis" not in text
        assert "davis_1981_table4" not in text


def test_table4_correction_ledger_keeps_every_row_pending_visual_review():
    rows = list(
        csv.DictReader(
            Path("reference/davis_1981/table4_correction_ledger.csv").open(
                newline="", encoding="utf-8"
            )
        )
    )
    assert len(rows) == 34
    assert {row["cells_reviewed"] for row in rows} == {"9"}
    assert {row["damaged_ocr_available"] for row in rows} == {"yes"}
    assert {row["resolution_basis"] for row in rows} == {
        "user-supplied normalized transcription; raw OCR unusable for cells"
    }
    assert {row["visual_verification"] for row in rows} == {"pending"}
    assert {row["confidence"] for row in rows} == {"medium"}


def test_davis_sources_distinguish_primary_authority_from_local_derivatives():
    rows = list(
        csv.DictReader(Path("reference/source_ledger.csv").open(newline="", encoding="utf-8"))
    )
    sources = {row["source_id"]: row for row in rows}
    publication = sources["SRC-DAVIS-1981"]
    transcription = sources["SRC-DAVIS-1981-TRANSCRIPTION"]
    table = sources["SRC-DAVIS-1981-TABLE4"]

    assert publication["source_type"] == "later primary publication"
    assert publication["primary_or_secondary"] == "primary"
    assert publication["artifact_hash"] == ""
    assert "access-restricted" in publication["access_status"]
    assert publication["verification_status"] == "user_reviewed_access_restricted_primary"

    assert transcription["primary_or_secondary"] == "secondary derivative"
    assert transcription["verification_status"] == "normalized_user_transcription"
    assert "SRC-DAVIS-1981" in transcription["notes"]

    assert table["primary_or_secondary"] == "secondary derivative"
    assert table["verification_status"] == "pending_retained_primary_visual_verification"
    assert table["confidence"] == "medium"
    assert "SRC-DAVIS-1981" in table["notes"]


def test_table4_runtime_rows_are_pending_normalized_derivatives():
    rows = list(
        csv.DictReader(
            Path("data/reference/davis_1981_table4.csv").open(newline="", encoding="utf-8")
        )
    )
    assert len(rows) == 34
    assert {row["source_id"] for row in rows} == {"SRC-DAVIS-1981-TABLE4"}
    assert {row["authority_source_id"] for row in rows} == {"SRC-DAVIS-1981"}
    assert {row["source_classification"] for row in rows} == {
        "normalized_historical_transcription"
    }
    assert {row["verification_status"] for row in rows} == {
        "pending_retained_primary_visual_verification"
    }
    assert {row["confidence"] for row in rows} == {"medium"}
    assert sum(len([key for key in row if key.startswith("mass_ratio_")]) for row in rows) == 306
