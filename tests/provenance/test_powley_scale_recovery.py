import ast
import csv
from pathlib import Path

import pytest

from modern_powley.original.powder_index import select_powder
from modern_powley.original.pressure import estimate_pressure
from modern_powley.original.velocity import estimate_velocity
from modern_powley.provenance.validation import MissingProvenanceError


REPORT = Path("docs/audits/original_powley_scale_recovery.md")
OBSERVATIONS = Path("data/reference/original_powley_velocity_observations.csv")


def _source_rows() -> dict[str, dict[str, str]]:
    with Path("reference/source_ledger.csv").open(newline="", encoding="utf-8") as handle:
        return {row["source_id"]: row for row in csv.DictReader(handle)}


def test_recovery_report_declares_partial_readiness_only():
    text = REPORT.read_text(encoding="utf-8")
    assert "`ARROW2_PARTIALLY_RECOVERED`" in text
    assert "`VELOCITY_PARTIALLY_RECOVERED`" in text
    assert "`PRESSURE_PARTIALLY_RECOVERED`" in text
    assert "ARROW2_SOURCE_COMPLETE" not in text
    assert "VELOCITY_SOURCE_COMPLETE" not in text
    assert "PRESSURE_SOURCE_COMPLETE" not in text
    assert "MissingProvenanceError" in text


def test_scale_sources_distinguish_revisions_and_derivatives():
    rows = _source_rows()
    high_quality_photo = rows["SRC-POWLEY-SLIDE-PHOTO-HQ"]
    observations = rows["SRC-POWLEY-VELOCITY-OBSERVATIONS"]
    hutton_powley = rows["SRC-HUTTON-POWLEY-1963-WEB"]

    assert high_quality_photo["primary_or_secondary"] == "primary artifact"
    assert high_quality_photo["confidence"] == "medium"
    assert "1985" in high_quality_photo["notes"]
    assert "does not establish identity with 1961" in high_quality_photo["notes"]
    assert observations["primary_or_secondary"] == "secondary derivative"
    assert "not a scale surface" in observations["notes"]
    assert hutton_powley["primary_or_secondary"] == "secondary derivative"
    assert hutton_powley["verification_status"] == "verified_secondary"
    assert hutton_powley["artifact_hash"] == ""


def test_velocity_observations_are_exactly_the_printed_constraints():
    with OBSERVATIONS.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 7
    assert [row["observation_id"] for row in rows] == [
        f"POWLEY-VEL-{index:03d}" for index in range(1, 8)
    ]
    assert {
        (row["mass_ratio"], row["total_expansion_ratio"], row["velocity_fps"])
        for row in rows
    } == {
        ("0.28", "4.0", "2200"),
        ("0.28", "12.0", "2770"),
        ("0.30", "9.0", "2730"),
        ("0.31", "7.5", "2680"),
        ("0.51", "5.1", "3080"),
        ("", "5.0", "3220"),
        ("1.45", "4.5", "4480"),
    }
    assert {row["source_id"] for row in rows} == {"SRC-POWLEY-1961-MANUAL"}
    assert {row["implementation_status"] for row in rows} == {
        "non_executable_observation"
    }


@pytest.mark.parametrize("operation", [select_powder, estimate_velocity, estimate_pressure])
def test_recovered_evidence_does_not_enable_original_operations(operation):
    with pytest.raises(MissingProvenanceError):
        operation()


def test_original_namespace_does_not_import_recovery_data_or_later_code():
    for path in Path("src/modern_powley/original").glob("*.py"):
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
        imported = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.append(node.module)
        assert not any("modern_powley.later" in name for name in imported)
        assert not any("modern_powley.experimental" in name for name in imported)
        assert "original_powley_velocity_observations.csv" not in source


def test_davis_derivative_warnings_are_preserved_without_original_promotion():
    text = Path("docs/history/03_davis_transcription.md").read_text(encoding="utf-8")
    assert "42.530520632" in text
    assert "42.377625032" in text
    assert "35.4 gr" in text
    assert "36.44475752752 gr" in text
    assert "supplies no evidence for the original graphical computer" in text
