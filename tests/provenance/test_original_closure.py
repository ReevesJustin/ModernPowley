import ast
import csv
from pathlib import Path

import pytest

from modern_powley.later.emulator import powder_index, select_powder_band, velocity_fps
from modern_powley.original.charge import charge_from_measured_powder_space
from modern_powley.original.geometry import (
    mass_ratio,
    projectile_travel_inches,
    total_expansion_ratio_from_dimensions,
)


REPORT = Path("docs/audits/original_powley_reconstruction_closure.md")
UNRESOLVED_ORIGINAL_IDS = {"EQ-022", "EQ-023", "EQ-047"}
ORIGINAL_CONSTANTS = {
    "CONST-001": ("7000", "src/modern_powley/original/units.py"),
    "CONST-002": ("253", "src/modern_powley/original/units.py"),
    "CONST-003": ("0.80", "src/modern_powley/original/charge.py"),
    "CONST-004": ("0.86", "src/modern_powley/original/charge.py"),
}


def test_closure_report_records_partial_reconstruction_and_required_gaps():
    text = REPORT.read_text(encoding="utf-8")
    classifications = {
        "CLOSED_SOURCE_BACKED_RECONSTRUCTION",
        "FUNCTIONALLY_COMPLETE_WITH_DOCUMENTED_AMBIGUITIES",
        "PARTIAL_RECONSTRUCTION",
        "INSUFFICIENT_PRIMARY_SOURCE_EVIDENCE",
    }
    declared = {
        value
        for value in classifications
        if f"Final reconstruction classification: `{value}`" in text
    }
    assert declared == {"PARTIAL_RECONSTRUCTION"}
    for required in (
        "Arrow 2",
        "Expansion Ratio-Velocity",
        "MissingProvenanceError",
        "SRC-POWLEY-1961-MANUAL",
        "data/reference/original_powley_powder_scale.csv",
    ):
        assert required in text


def test_all_unresolved_original_outputs_are_ledgered_as_explicit_failures():
    rows = {
        row["equation_id"]: row
        for row in csv.DictReader(
            Path("docs/provenance/equation_ledger.csv").open(newline="", encoding="utf-8")
        )
    }
    for equation_id in UNRESOLVED_ORIGINAL_IDS:
        row = rows[equation_id]
        assert row["attribution_class"] == "original_powley"
        assert row["equation_text"] == "unresolved"
        assert row["verification_status"] == "unresolved"
        assert "fails explicitly" in row["disposition"]
        implementation = Path(row["implemented_in"])
        tree = ast.parse(implementation.read_text(encoding="utf-8"), filename=str(implementation))
        assert any(
            isinstance(node, ast.Raise)
            and isinstance(node.exc, ast.Call)
            and isinstance(node.exc.func, ast.Name)
            and node.exc.func.id == "MissingProvenanceError"
            for node in ast.walk(tree)
        )


def test_original_numeric_constants_have_primary_source_traceability():
    rows = {
        row["constant_id"]: row
        for row in csv.DictReader(
            Path("docs/provenance/constant_ledger.csv").open(newline="", encoding="utf-8")
        )
    }
    for constant_id, (value, location) in ORIGINAL_CONSTANTS.items():
        row = rows[constant_id]
        assert row["value"] == value
        assert row["location"] == location
        assert row["attribution_class"] == "original_powley"
        assert row["source_id"] == "SRC-POWLEY-1961-MANUAL"
        assert row["verification_status"] == "verified_visual_scan"


def test_manual_example_arithmetic_and_emulator_divergence_remain_explicit():
    charge = charge_from_measured_powder_space(51.5, "IMR 4064")
    ratio = mass_ratio(44.3, 150)
    travel = projectile_travel_inches(21 + 5 / 16, 1 + 1 / 16)
    expansion = total_expansion_ratio_from_dimensions(51.5, 0.300, 0.308, travel)

    assert charge == pytest.approx(44.29)
    assert ratio == pytest.approx(0.29533333333333334)
    assert travel == pytest.approx(22.375)
    assert expansion == pytest.approx(8.97835551807793)

    index = powder_index(0.227, 0.295)
    emulator_velocity = velocity_fps(44.3, 150, 9.0)
    assert index == pytest.approx(117.32947502008706)
    assert select_powder_band(index).designation == "4320;4895;4064"
    assert emulator_velocity == pytest.approx(2696.7921204662666)
    assert emulator_velocity - 2730 == pytest.approx(-33.207879533733376)


def test_additional_manual_examples_reproduce_only_source_backed_initial_charge():
    assert charge_from_measured_powder_space(61.5, "IMR 4350") == pytest.approx(52.89)
    assert charge_from_measured_powder_space(79, "IMR 5010") == pytest.approx(67.94)
    assert charge_from_measured_powder_space(95, "IMR 5010") == pytest.approx(81.70)
