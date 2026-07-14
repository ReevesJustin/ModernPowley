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
    assert {row["damaged_ocr_available"] for row in rows} == {"no"}
    assert {row["visual_verification"] for row in rows} == {"pending"}
    assert {row["confidence"] for row in rows} == {"medium"}
