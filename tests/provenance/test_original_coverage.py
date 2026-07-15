import ast
import csv
from pathlib import Path


PUBLIC_EQUATIONS = {
    ("units.py", "cubic_inches_to_water_grains"): "EQ-005",
    ("charge.py", "loading_density"): "EQ-003",
    ("charge.py", "charge_from_measured_powder_space"): "EQ-003",
    ("geometry.py", "sectional_density"): "EQ-001",
    ("geometry.py", "mass_ratio"): "EQ-002",
    ("geometry.py", "effective_bore_diameter_inches"): "EQ-044",
    ("geometry.py", "projectile_travel_inches"): "EQ-008",
    ("geometry.py", "barrel_volume_water_grains"): "EQ-009",
    ("geometry.py", "barrel_volume_ratio"): "EQ-010",
    ("geometry.py", "total_expansion_ratio"): "EQ-011",
    ("geometry.py", "total_expansion_ratio_from_dimensions"): "EQ-011",
    ("powder_index.py", "select_powder"): "EQ-047",
    ("velocity.py", "estimate_velocity"): "EQ-022",
    ("pressure.py", "estimate_pressure"): "EQ-023",
}


def test_every_public_original_function_has_equation_and_test_coverage():
    rows = list(csv.DictReader(Path("docs/provenance/equation_ledger.csv").open(newline="", encoding="utf-8")))
    by_id = {row["equation_id"]: row for row in rows}
    observed = set()
    for module in Path("src/modern_powley/original").glob("*.py"):
        if module.name == "__init__.py":
            continue
        tree = ast.parse(module.read_text(encoding="utf-8"), filename=str(module))
        observed.update(
            (module.name, node.name)
            for node in tree.body
            if isinstance(node, ast.FunctionDef) and not node.name.startswith("_")
        )
    assert observed == set(PUBLIC_EQUATIONS)
    for symbol, equation_id in PUBLIC_EQUATIONS.items():
        row = by_id[equation_id]
        assert row["implemented_in"] == f"src/modern_powley/original/{symbol[0]}"
        assert row["source_id"]
        assert row["test_reference"] not in {"", "none"}


def test_unresolved_original_operations_have_no_fabricated_equation():
    rows = list(csv.DictReader(Path("docs/provenance/equation_ledger.csv").open(newline="", encoding="utf-8")))
    unresolved = {row["equation_name"]: row for row in rows if row["equation_id"] in {"EQ-022", "EQ-023"}}
    assert unresolved["original velocity"]["equation_text"] == "unresolved"
    assert unresolved["1961 manual muzzle-pressure reading"]["equation_text"] == "unresolved"
