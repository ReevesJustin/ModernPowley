import csv
import hashlib
from pathlib import Path


PHASE1 = Path(
    "docs/modernization/workstreams/empirical_load_evidence_records_phase_1.md"
)
DECISIONS = Path(
    "docs/modernization/decisions/"
    "empirical_load_evidence_records_phase_1_authorization.md"
)
REVIEW = Path(
    "docs/modernization/reviews/"
    "empirical_load_evidence_records_phase_1_authorization_review.md"
)
COMPLETION = Path(
    "docs/modernization/reviews/"
    "empirical_load_evidence_records_phase_1_completion_review.md"
)
PARENT = Path(
    "docs/modernization/workstreams/empirical_load_evidence_and_validation.md"
)


def _source_rows():
    with Path("reference/source_ledger.csv").open(
        newline="", encoding="utf-8"
    ) as handle:
        return {row["source_id"]: row for row in csv.DictReader(handle)}


def _words(text):
    return " ".join(text.split())


def test_phase1_is_accepted_while_parent_remains_planned():
    phase = PHASE1.read_text(encoding="utf-8")
    parent = PARENT.read_text(encoding="utf-8")
    assert "## Status\n\n`accepted`" in phase
    assert "## Status\n\n`planned`" in parent
    assert "parent empirical-load evidence and validation workstream remains `planned`" in _words(phase)
    assert "entered `in_progress` before source implementation" in phase
    assert "No next\nphase is authorized" in phase
    assert "This review authorizes no implementation in this commit" in REVIEW.read_text(
        encoding="utf-8"
    )


def test_phase1_authorizes_exactly_eight_distinct_record_families():
    text = PHASE1.read_text(encoding="utf-8")
    prose = _words(text)
    for heading in (
        "Source Artifact And Custody Metadata",
        "Literal Source-Declared Load Statement",
        "Physical Load Configuration",
        "Shot Observation",
        "Load Series Or Ladder",
        "Pressure-Trace Metadata",
        "Chronograph Series",
        "Aggregate Or Published Summary",
    ):
        assert f"### {heading}" in text
    assert "A shot is not a load configuration" in prose
    assert "It does not calculate order, discover members, interpolate" in prose
    assert "It never replaces or mutates its members" in prose


def test_phase1_keeps_intake_cohorts_splits_m05_and_m06_deferred():
    text = _words(PHASE1.read_text(encoding="utf-8"))
    for phrase in (
        "dataset cohorts, dataset splits",
        "scientific source download",
        "M05 source adapters",
        "charge-region construction or derivation",
        "pressure-trace sample arrays",
        "M06 implementation",
        "No cohort or split record is part of Phase 1",
    ):
        assert phrase in text
    assert "`high_performance` is prohibited as an intrinsic raw-observation" in text


def test_identity_pressure_velocity_trace_and_missingness_boundaries_are_explicit():
    text = _words(PHASE1.read_text(encoding="utf-8"))
    for phrase in (
        "Powder identity remains owned by M02",
        "scoped load-context component identity assertions",
        "CUP-to-PSI conversion",
        "modeled pressure as measurement",
        "raw versus corrected versus muzzle-extrapolated",
        "metadata and immutable artifact references only",
        "Duplicate publications of one underlying test share exact lineage",
        "Printed precision is never silently converted",
        "unit conversion never reconciles evidence",
    ):
        assert phrase in text


def test_strict_schema_and_narrow_module_qualified_architecture_is_implemented():
    text = PHASE1.read_text(encoding="utf-8")
    assert "`modern_powley.empirical_load_evidence.v1`" in text
    assert "reject duplicate JSON object\n  keys" in text
    assert "Canonical byte serialization is not promised" in text
    assert "not exported from\n`modern_powley.modernized.__init__`" in text

    modernized = Path("src/modern_powley/modernized")
    assert {path.name for path in modernized.glob("*empirical_load*")} == {
        "empirical_load_records.py",
        "empirical_load_serialization.py",
    }
    import modern_powley.modernized as package

    assert "EMPIRICAL_LOAD_EVIDENCE_SCHEMA_ID" not in package.__all__
    assert not hasattr(package, "EMPIRICAL_LOAD_EVIDENCE_SCHEMA_ID")


def test_synthetic_fixture_policy_does_not_promote_existing_artifacts():
    text = _words(PHASE1.read_text(encoding="utf-8"))
    assert "`synthetic_fixture: true`" in text
    assert "fictional `SYN-ELE-*`" in text
    for prohibited in (
        "Legacy CSV rows", "Powley or Davis examples", "manufacturer/DEVA data",
        "GRT or QuickLOAD files", "emulator output", "regression rows",
    ):
        assert prohibited in text


def test_authorization_review_contains_all_fifty_passing_gates():
    text = REVIEW.read_text(encoding="utf-8")
    assert "`authorized_for_phase_1_implementation`" in text
    for gate in range(1, 51):
        assert f"| {gate} " in text
    assert text.count("| pass |") == 50
    assert "not a completion review" in _words(text).casefold()


def test_completion_review_contains_all_ninety_seven_passing_gates():
    text = COMPLETION.read_text(encoding="utf-8")
    assert "`empirical_evidence_records_phase_1_accepted`" in text
    for gate in range(1, 98):
        assert f"| {gate} |" in text
    assert text.count("| PASS |") == 97
    assert "structural acceptance is not scientific validation" in text


def test_entry_points_agree_on_the_bounded_authorization():
    paths = (
        "README.md",
        "TODO.md",
        "docs/Usage_Instructions.md",
        "docs/modernization/modern_powley_roadmap.md",
        "docs/modernization/cross_cutting_workstreams.md",
        "AGENTS.md",
    )
    for path in paths:
        text = Path(path).read_text(encoding="utf-8")
        assert "Phase 1" in text
        assert "accepted" in text
        assert "planned" in text
    roadmap = Path(paths[3]).read_text(encoding="utf-8")
    assert "is `accepted` as an immutable-record" in roadmap
    assert "No scientific data" in roadmap
    assert "M06\nmodel is admitted" in roadmap


def test_phase1_artifacts_are_hash_ledgered_as_repository_artifacts():
    rows = _source_rows()
    for source_id, path in (
        ("SRC-EMPIRICAL-LOAD-PHASE1-SPEC", PHASE1),
        ("SRC-EMPIRICAL-LOAD-PHASE1-DECISIONS", DECISIONS),
        ("SRC-EMPIRICAL-LOAD-PHASE1-AUTH-REVIEW", REVIEW),
        ("SRC-EMPIRICAL-LOAD-PHASE1-DESIGN", Path("docs/modernization/phases/empirical_load_evidence_records_phase_1.md")),
        ("SRC-EMPIRICAL-LOAD-PHASE1-IMPLEMENTATION", Path("docs/modernization/decisions/empirical_load_evidence_records_phase_1_implementation.md")),
        ("SRC-EMPIRICAL-LOAD-PHASE1-API", Path("docs/modernization/empirical_load_evidence_records_phase_1_api.md")),
        ("SRC-EMPIRICAL-LOAD-PHASE1-COMPLETION", COMPLETION),
        ("SRC-EMPIRICAL-LOAD-WORKSTREAM", PARENT),
    ):
        row = rows[source_id]
        assert row["artifact_hash"] == (
            f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"
        )
        assert row["attribution_class"] == "modernized_powley"
        assert "repository" in row["source_type"]
        assert "not historical Powley evidence" in row["notes"]


def test_no_equation_or_constant_ledger_is_extended_and_existing_schemas_hold():
    for ledger in (
        "docs/provenance/equation_ledger.csv",
        "docs/provenance/constant_ledger.csv",
    ):
        text = Path(ledger).read_text(encoding="utf-8")
        assert "EMPIRICAL-LOAD-PHASE1" not in text

    import modern_powley.modernized as modernized

    assert modernized.SCHEMA_ID == "modern_powley.m01.v1"
    assert modernized.M02_SCHEMA_ID == "modern_powley.m02.v1"
    assert modernized.M03_SCHEMA_ID == "modern_powley.m03.v1"
    assert modernized.M04_SCHEMA_ID == "modern_powley.m04.v1"
    assert modernized.M05_SCHEMA_ID == "modern_powley.m05.v1"


def test_phase1_schema_fields_are_definition_ledgered_not_scientific_evidence():
    text = Path("docs/provenance/data_field_ledger.csv").read_text(encoding="utf-8")
    assert "EMPIRICAL-LOAD-PHASE1" in text
    assert "repository schema definition" in text
