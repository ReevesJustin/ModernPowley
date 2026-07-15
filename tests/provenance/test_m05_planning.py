import hashlib
from pathlib import Path


SPEC = Path("docs/modernization/milestones/M05_charge_region_records.md")
REVIEW = Path("docs/modernization/reviews/M05_evidence_and_semantics_review.md")
DECISIONS = Path("docs/modernization/decisions/M05_specification_decisions.md")


def test_m05_planning_documents_exist_and_remain_planning_only():
    spec = SPEC.read_text(encoding="utf-8")
    assert "## Status\n\n`planned`" in spec
    assert "This planning milestone creates no schema implementation" in spec
    assert "Only evidence review, specification amendment, and a user authorization review" in spec
    assert REVIEW.is_file()
    assert DECISIONS.is_file()
    assert not Path("docs/modernization/reviews/M05_completion_review.md").exists()


def test_m05_spec_contains_bounded_semantics_and_future_gates():
    spec = SPEC.read_text(encoding="utf-8").casefold()
    for phrase in (
        "multiple disjoint segments",
        "empty intersections",
        "uncertainty interval is not a charge region",
        "cup/psi",
        "predeclared gates for a future implementation",
        "recommended charge",
        "m04 outcome",
    ):
        assert phrase in spec


def test_entry_points_agree_m04_is_accepted_and_m05_is_planned():
    roadmap = Path("docs/modernization/modern_powley_roadmap.md").read_text(encoding="utf-8")
    todo = Path("TODO.md").read_text(encoding="utf-8")
    usage = Path("docs/Usage_Instructions.md").read_text(encoding="utf-8")
    assert "M04 is also accepted" in roadmap
    assert "Status: planned; specification-only; implementation is not authorized" in roadmap
    assert "status `planned`; implementation is not authorized" in todo
    assert "M05 is specification-only and remains `planned`" in usage


def test_no_m05_source_schema_export_or_completion_claim_exists():
    package = Path("src/modern_powley")
    assert not any("m05" in path.name.casefold() for path in package.rglob("*"))
    modernized_init = Path("src/modern_powley/modernized/__init__.py").read_text(encoding="utf-8")
    assert "m05" not in modernized_init.casefold()
    assert "modern_powley.m05.v1" not in modernized_init


def test_m05_design_artifacts_are_hash_ledgered():
    import csv

    with Path("reference/source_ledger.csv").open(newline="", encoding="utf-8") as handle:
        sources = {row["source_id"]: row for row in csv.DictReader(handle)}
    for source_id, path in (
        ("SRC-M05-SPEC", SPEC),
        ("SRC-M05-EVIDENCE-REVIEW", REVIEW),
        ("SRC-M05-SPEC-DECISIONS", DECISIONS),
    ):
        row = sources[source_id]
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        assert row["artifact_hash"] == f"sha256:{digest}"
        assert row["attribution_class"] == "modernized_powley"
        assert row["verification_status"] == "verified_primary"
