import csv
import hashlib
from pathlib import Path


WORKSTREAM = Path("docs/modernization/workstreams/empirical_load_evidence_and_validation.md")
REVIEW = Path("docs/modernization/reviews/M05_derivation_readiness_review.md")
DECISIONS = Path("docs/modernization/decisions/empirical_load_evidence_and_validation_decisions.md")
M05_SPEC = Path("docs/modernization/milestones/M05_charge_region_records.md")
M05_REVIEW = Path("docs/modernization/reviews/M05_completion_review.md")


def source_rows():
    with Path("reference/source_ledger.csv").open(newline="", encoding="utf-8") as handle:
        return {row["source_id"]: row for row in csv.DictReader(handle)}


def test_workstream_is_planned_and_non_authorizing():
    text = WORKSTREAM.read_text(encoding="utf-8")
    assert "## Status\n\n`planned`" in text
    assert "authorizes no source implementation" in text
    assert "parent workstream" in text
    assert "does not authorize implementation of its broader scope" in text
    assert "cohorts, splits, M05 derivation, or M06" in text


def test_distinct_record_families_and_layers_are_specified():
    text = WORKSTREAM.read_text(encoding="utf-8")
    for heading in (
        "Source-Declared Load Statement", "Individual Physical Load Observation",
        "Shot-Level Observation", "Load Series Or Ladder", "Pressure Trace",
        "Chronograph Series", "Aggregate Or Published Summary", "Dataset Cohort",
        "Dataset Split",
    ):
        assert f"### {heading}" in text
    for layer in (
        "Retained source artifact", "Literal source transcription or imported raw data",
        "Normalized observation record", "Derived summary", "Dataset cohort",
        "Dataset split", "Model result", "M05 charge-region record",
    ):
        assert layer in text


def test_validation_split_roles_are_controlled_and_nonconflated():
    text = WORKSTREAM.read_text(encoding="utf-8")
    roles = (
        "source_example_reproduction", "regression_reproduction", "calibration",
        "in_sample_evaluation", "interpolation_evaluation",
        "cross_cartridge_evaluation", "held_out_validation", "external_replication",
    )
    assert all(f"`{role}`" in text for role in roles)
    assert "Calibration agreement, source-example reproduction, and regression reproduction\nmust never be labeled independent validation" in text


def test_high_performance_is_not_raw_evidence_or_safety_semantics():
    text = WORKSTREAM.read_text(encoding="utf-8")
    assert "`high_performance` is prohibited as an intrinsic raw-observation field" in text
    assert "operation-relative M04 criterion/outcome" in text
    assert "establishes no safety, recommendation, optimality" in text


def test_derivation_review_admits_no_candidate_method():
    text = REVIEW.read_text(encoding="utf-8")
    assert "No M05 derivation family is admitted or authorized" in text
    for disposition in (
        "potentially_admissible_after_source_intake",
        "potentially_admissible_after_validation_contract",
        "experimental_only", "evidence_limited", "historical_context_only", "blocked",
    ):
        assert f"`{disposition}`" in text
    assert "No fit is authorized" in text
    assert "Intersection" in text
    assert "remains blocked and unauthorized" in text


def test_m05_status_and_final_release_gates_are_reconciled():
    assert "## Status\n\n`accepted`" in M05_SPEC.read_text(encoding="utf-8")
    review = M05_REVIEW.read_text(encoding="utf-8")
    assert "| 34 normal commit/push | pass |" in review
    assert "| 35 clean synchronization | pass |" in review
    assert "0c3020fcf8480b0f2a2df4016a56b397cf0f90fc" in review
    assert "pending final commit" not in review
    assert "pending push" not in review


def test_entry_points_agree_and_m06_remains_unauthorized():
    texts = {
        path: Path(path).read_text(encoding="utf-8")
        for path in (
            "README.md", "TODO.md", "docs/Usage_Instructions.md",
            "docs/modernization/modern_powley_roadmap.md",
        )
    }
    assert all("M05" in text for text in texts.values())
    assert all("planned" in text.casefold() for text in texts.values())
    assert "M06" in texts["docs/Usage_Instructions.md"]
    assert "remain unauthorized" in " ".join(
        texts["docs/Usage_Instructions.md"].split()
    )
    assert "M06-M08 remain future unauthorized" in texts["docs/modernization/modern_powley_roadmap.md"]


def test_planning_artifacts_are_hash_ledgered_as_repository_artifacts():
    sources = source_rows()
    for source_id, path in (
        ("SRC-EMPIRICAL-LOAD-WORKSTREAM", WORKSTREAM),
        ("SRC-M05-DERIVATION-READINESS", REVIEW),
        ("SRC-EMPIRICAL-LOAD-DECISIONS", DECISIONS),
        ("SRC-M05-COMPLETION-REVIEW", M05_REVIEW),
    ):
        row = sources[source_id]
        assert row["artifact_hash"] == f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"
        assert row["attribution_class"] == "modernized_powley"
        assert "repository" in row["source_type"]


def test_no_equation_constant_or_public_derivation_api_is_added():
    for ledger in ("docs/provenance/equation_ledger.csv", "docs/provenance/constant_ledger.csv"):
        text = Path(ledger).read_text(encoding="utf-8")
        assert "SRC-EMPIRICAL-LOAD" not in text
        assert "SRC-M05-DERIVATION-READINESS" not in text

    import modern_powley.modernized as modernized

    prohibited = {
        "derive_charge_region", "source_declared_interval_adapter",
        "measurement_supported_region", "intersect_charge_regions",
        "fit_charge_region", "ingest_load_evidence",
    }
    assert prohibited.isdisjoint(modernized.__all__)
    assert modernized.SCHEMA_ID == "modern_powley.m01.v1"
    assert modernized.M02_SCHEMA_ID == "modern_powley.m02.v1"
    assert modernized.M03_SCHEMA_ID == "modern_powley.m03.v1"
    assert modernized.M04_SCHEMA_ID == "modern_powley.m04.v1"
    assert modernized.M05_SCHEMA_ID == "modern_powley.m05.v1"
