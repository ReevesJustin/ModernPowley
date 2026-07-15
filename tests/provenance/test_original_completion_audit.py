import ast
import csv
from pathlib import Path


REPORT = Path("docs/audits/original_powley_reconstruction_completion_audit.md")
ORIGINAL = Path("src/modern_powley/original")


def test_completion_audit_declares_one_freeze_readiness_decision():
    text = REPORT.read_text(encoding="utf-8")
    decisions = {
        "ready_to_freeze",
        "ready_to_freeze_with_documented_source_gaps",
        "not_ready_to_freeze",
    }
    declared = {decision for decision in decisions if f"Freeze recommendation: `{decision}`" in text}
    assert declared == {"not_ready_to_freeze"}
    assert "`scalar_arithmetic_core`" in text
    assert "`complete_historical_method`: `not_ready_to_freeze`" in text


def test_completion_audit_covers_every_public_original_function():
    text = REPORT.read_text(encoding="utf-8")
    for module in ORIGINAL.glob("*.py"):
        tree = ast.parse(module.read_text(encoding="utf-8"), filename=str(module))
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
                assert f"`{node.name}`" in text


def test_separate_pressure_artifacts_have_separate_ledger_dispositions():
    rows = {
        row["equation_id"]: row
        for row in csv.DictReader(
            Path("docs/provenance/equation_ledger.csv").open(newline="", encoding="utf-8")
        )
    }
    assert rows["EQ-023"]["equation_name"] == "1961 manual muzzle-pressure reading"
    assert rows["EQ-023"]["implemented_in"] == "src/modern_powley/original/pressure.py"
    assert rows["EQ-091"]["equation_name"] == "separate Powley psi Calculator"
    assert rows["EQ-091"]["implemented_in"] == ""
    assert rows["EQ-091"]["verification_status"] == "unresolved"


def test_original_namespace_contains_no_later_scientific_markers():
    forbidden = {
        "252.4",
        "0.773",
        "8000",
        "0.0142",
        "table4",
        "davis",
        "howell",
        "miller",
        "ba_eff",
        "vivacity",
        "quickload",
        "burnforge",
    }
    combined = "\n".join(path.read_text(encoding="utf-8").lower() for path in ORIGINAL.glob("*.py"))
    assert not {marker for marker in forbidden if marker in combined}


def test_original_namespace_has_no_geometric_case_intrusion_or_boat_tail_api():
    public_names = set()
    for module in ORIGINAL.glob("*.py"):
        tree = ast.parse(module.read_text(encoding="utf-8"), filename=str(module))
        public_names.update(
            node.name
            for node in tree.body
            if isinstance(node, ast.FunctionDef) and not node.name.startswith("_")
        )
    assert not {
        "seating_depth_inches",
        "flat_base_displacement_water_grains",
        "boat_tail_correction_water_grains",
    } & public_names
