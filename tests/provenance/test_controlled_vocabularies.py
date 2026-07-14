import csv
from pathlib import Path

from modern_powley.provenance.source_types import AttributionClass, ProvenanceStatus


LEDGERS = (
    Path("reference/source_ledger.csv"),
    Path("docs/provenance/equation_ledger.csv"),
    Path("docs/provenance/constant_ledger.csv"),
    Path("docs/provenance/data_field_ledger.csv"),
    Path("docs/provenance/grt_field_mapping.csv"),
)


def test_provenance_ledgers_use_controlled_statuses_and_attributions():
    statuses = {item.value for item in ProvenanceStatus}
    attributions = {item.value for item in AttributionClass}
    for path in LEDGERS:
        rows = list(csv.DictReader(path.open(newline="", encoding="utf-8")))
        assert rows and "verification_status" in rows[0], path
        assert {row["verification_status"] for row in rows} <= statuses, path
        if "attribution_class" in rows[0]:
            assert {row["attribution_class"] for row in rows} <= attributions, path
        if "confidence" in rows[0]:
            assert {row["confidence"] for row in rows} <= {"low", "medium", "high"}, path


def test_manual_page_map_covers_every_numbered_page():
    text = Path("docs/history/original_manual_page_map.md").read_text(encoding="utf-8")
    for page in range(3, 13):
        assert f"| {page} |" in text
