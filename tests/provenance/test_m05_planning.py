import hashlib
from pathlib import Path


SPEC = Path("docs/modernization/milestones/M05_charge_region_records.md")
REVIEW = Path("docs/modernization/reviews/M05_evidence_and_semantics_review.md")
DECISIONS = Path("docs/modernization/decisions/M05_specification_decisions.md")
AUTHORIZATION = Path("docs/modernization/decisions/M05_records_only_authorization.md")
AUTHORIZATION_REVIEW = Path("docs/modernization/reviews/M05_records_only_authorization_review.md")
CROSS_CUTTING = Path("docs/modernization/cross_cutting_workstreams.md")


def test_m05_is_authorized_only_for_later_records_implementation():
    spec = SPEC.read_text(encoding="utf-8")
    assert "## Status\n\n`authorized`" in spec
    assert "authorized only for the immutable records" in spec
    assert "This authorization commit creates no serializer or export" in spec
    assert REVIEW.is_file()
    assert DECISIONS.is_file()
    assert AUTHORIZATION.is_file()
    assert AUTHORIZATION_REVIEW.is_file()
    assert not Path("docs/modernization/reviews/M05_completion_review.md").exists()


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


def test_entry_points_agree_m04_is_accepted_and_m05_is_records_only_authorized():
    roadmap = Path("docs/modernization/modern_powley_roadmap.md").read_text(encoding="utf-8")
    todo = Path("TODO.md").read_text(encoding="utf-8")
    usage = Path("docs/Usage_Instructions.md").read_text(encoding="utf-8")
    assert "M04 is also accepted" in roadmap
    assert "Status: authorized for records and strict serialization only" in roadmap
    assert "status `authorized` for a later immutable" in todo
    assert "M05 is `authorized` only for a later records-and-strict-serialization increment" in usage


def test_no_m05_source_schema_export_or_completion_claim_exists():
    package = Path("src/modern_powley")
    assert not any("m05" in path.name.casefold() for path in package.rglob("*"))
    modernized_init = Path("src/modern_powley/modernized/__init__.py").read_text(encoding="utf-8")
    assert "m05" not in modernized_init.casefold()
    assert "modern_powley.m05.v1" not in modernized_init


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
    assert not Path("src/modern_powley/modernized/m05_serialization.py").exists()


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
    ):
        row = sources[source_id]
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        assert row["artifact_hash"] == f"sha256:{digest}"
        assert row["attribution_class"] == "modernized_powley"
        assert row["verification_status"] == "verified_primary"
