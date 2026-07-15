import hashlib
from pathlib import Path


SPEC = Path("docs/modernization/milestones/M05_charge_region_records.md")
REVIEW = Path("docs/modernization/reviews/M05_evidence_and_semantics_review.md")
DECISIONS = Path("docs/modernization/decisions/M05_specification_decisions.md")
AUTHORIZATION = Path("docs/modernization/decisions/M05_records_only_authorization.md")
AUTHORIZATION_REVIEW = Path("docs/modernization/reviews/M05_records_only_authorization_review.md")
CROSS_CUTTING = Path("docs/modernization/cross_cutting_workstreams.md")
PHASE_DESIGN = Path("docs/modernization/phases/M05_charge_region_records.md")
IMPLEMENTATION_DECISIONS = Path("docs/modernization/decisions/M05_implementation_decisions.md")
COMPLETION_REVIEW = Path("docs/modernization/reviews/M05_completion_review.md")


def test_m05_is_accepted_only_as_records_and_serialization():
    spec = SPEC.read_text(encoding="utf-8")
    assert "## Status\n\n`accepted`" in spec
    assert "is now accepted only" in spec
    assert "immutable records, structural validation, and strict serialization" in spec
    assert REVIEW.is_file()
    assert DECISIONS.is_file()
    assert AUTHORIZATION.is_file()
    assert AUTHORIZATION_REVIEW.is_file()
    assert PHASE_DESIGN.is_file() and IMPLEMENTATION_DECISIONS.is_file() and COMPLETION_REVIEW.is_file()
    assert "entered `in_progress`" in spec


def test_m05_spec_contains_bounded_semantics_and_future_gates():
    spec = SPEC.read_text(encoding="utf-8").casefold()
    for phrase in (
        "multiple disjoint segments",
        "`empty`, `unavailable`",
        "uncertainty interval never becomes a bounded analytical charge region",
        "cup, piezoelectric psi",
        "recommended, preferred",
        "m04 references are optional audit dependencies",
        "no region derivation",
        "strict `modern_powley.m05.v1` serialization",
    ):
        assert phrase in spec


def test_entry_points_agree_m01_through_m05_are_accepted_and_m06_is_not():
    roadmap = Path("docs/modernization/modern_powley_roadmap.md").read_text(encoding="utf-8")
    todo = Path("TODO.md").read_text(encoding="utf-8")
    usage = Path("docs/Usage_Instructions.md").read_text(encoding="utf-8")
    assert "M04 is also accepted" in roadmap
    assert "Status: accepted for records and strict serialization only" in roadmap
    assert "M05 - Charge-region records:** accepted immutable" in todo
    assert "M05 is accepted only as an immutable records" in usage
    assert "M06-M08 remain future unauthorized" in roadmap


def test_m05_source_schema_and_exports_are_bounded():
    modernized_init = Path("src/modern_powley/modernized/__init__.py").read_text(encoding="utf-8")
    assert "m05_serialization" in modernized_init
    assert Path("src/modern_powley/modernized/charge_regions.py").is_file()
    assert Path("src/modern_powley/modernized/m05_serialization.py").is_file()


def test_authorization_resolves_record_policies_without_arithmetic_or_data():
    text = AUTHORIZATION.read_text(encoding="utf-8").casefold()
    for phrase in (
        "caller order is canonical ascending",
        "out-of-order, overlapping, and exact",
        "five region states",
        "no covariance",
        "no production derivation method",
        "implementation must be a later commit",
    ):
        assert phrase in text
    assert Path("src/modern_powley/modernized/m05_serialization.py").exists()


def test_cross_cutting_direction_is_non_authorizing_and_m06_remains_future():
    text = CROSS_CUTTING.read_text(encoding="utf-8")
    assert "authorize no implementation" in text
    assert "Validation Foundation Before M06" in text
    assert "No dependency or\nlockfile change is authorized" in text
    assert "No web code, upload, parser, or adapter is authorized" in text
    roadmap = Path("docs/modernization/modern_powley_roadmap.md").read_text(encoding="utf-8")
    for milestone in range(6, 12):
        assert f"Future Phase Concept M{milestone:02d}" in roadmap


def test_repository_does_not_claim_safe_charge_region_capability():
    entry_points = "\n".join(
        Path(path).read_text(encoding="utf-8")
        for path in ("README.md", "TODO.md", "docs/Usage_Instructions.md")
    ).casefold()
    assert "safe charge region" not in entry_points


def test_m05_design_artifacts_are_hash_ledgered():
    import csv

    with Path("reference/source_ledger.csv").open(newline="", encoding="utf-8") as handle:
        sources = {row["source_id"]: row for row in csv.DictReader(handle)}
    for source_id, path in (
        ("SRC-M05-SPEC", SPEC),
        ("SRC-M05-EVIDENCE-REVIEW", REVIEW),
        ("SRC-M05-SPEC-DECISIONS", DECISIONS),
        ("SRC-M05-RECORDS-AUTHORIZATION", AUTHORIZATION),
        ("SRC-M05-AUTHORIZATION-REVIEW", AUTHORIZATION_REVIEW),
        ("SRC-MODERNIZATION-CROSS-CUTTING", CROSS_CUTTING),
        ("SRC-M05-DESIGN", IMPLEMENTATION_DECISIONS),
        ("SRC-M05-PHASE-DESIGN", PHASE_DESIGN),
        ("SRC-M05-COMPLETION-REVIEW", COMPLETION_REVIEW),
    ):
        row = sources[source_id]
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        assert row["artifact_hash"] == f"sha256:{digest}"
        assert row["attribution_class"] == "modernized_powley"
        assert row["verification_status"] == "verified_primary"


def test_m05_schema_fields_are_ledgered_without_an_equation_or_constant():
    import csv

    with Path("docs/provenance/data_field_ledger.csv").open(newline="", encoding="utf-8") as handle:
        fields = {
            row["field"]
            for row in csv.DictReader(handle)
            if row["data_asset"] == "modern_powley.m05.v1"
        }
    assert {
        "schema", "record_type", "charge_region_record.state",
        "charge_region_record.basis", "charge_region_record.segments",
        "charge_region_record.references", "charge_region_record.non_implication",
    } <= fields

    for ledger in ("docs/provenance/equation_ledger.csv", "docs/provenance/constant_ledger.csv"):
        assert "M05" not in Path(ledger).read_text(encoding="utf-8")
