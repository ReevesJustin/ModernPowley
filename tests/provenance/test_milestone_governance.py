import re
from pathlib import Path


MILESTONE_DIR = Path("docs/modernization/milestones")
ROADMAP = Path("docs/modernization/modern_powley_roadmap.md")
AGENT_GUIDE = Path("AGENTS.md")

SPECS = {
    "M01": MILESTONE_DIR / "M01_canonical_inputs_and_geometry.md",
    "M02": MILESTONE_DIR / "M02_powder_property_records.md",
    "M03": MILESTONE_DIR / "M03_input_and_domain_diagnostics.md",
    "M04": MILESTONE_DIR / "M04_screening_decision_records.md",
    "M05": MILESTONE_DIR / "M05_charge_region_records.md",
}

REQUIRED_HEADINGS = {
    "Status",
    "Purpose",
    "Starting Repository State Or Predecessor",
    "Scope",
    "Explicitly Permitted Behavior",
    "Explicitly Prohibited Behavior",
    "Required Data And Record Models",
    "Evidence And Provenance Boundaries",
    "Namespace And Dependency Boundaries",
    "Serialization Requirements",
    "Required Repository Deliverables",
    "Required Policy Decisions",
    "Acceptance Gates",
    "Required Validation Commands",
    "Scope-Control Review Checklist",
    "Completion-Report Requirements",
    "Commit And Release Expectations",
    "Known Limitations",
    "Authorized Next-Milestone Boundary",
}

CONTROLLED_STATUSES = {
    "planned", "authorized", "in_progress", "implemented", "accepted",
    "superseded", "blocked", "evidence_limited",
}


def headings(text):
    return {line.removeprefix("## ").strip() for line in text.splitlines() if line.startswith("## ")}


def status(text):
    match = re.search(r"^## Status\n\n`([^`]+)`", text, re.MULTILINE)
    assert match, "milestone specification requires a controlled status"
    return match.group(1)


def test_m01_through_m05_have_canonical_complete_specs_and_controlled_statuses():
    for milestone, path in SPECS.items():
        assert path.is_file(), milestone
        text = path.read_text(encoding="utf-8")
        assert text.startswith(f"# {milestone}:")
        assert REQUIRED_HEADINGS <= headings(text)
        assert status(text) in CONTROLLED_STATUSES


def test_accepted_milestones_link_decisions_reviews_ledgers_and_principal_tests():
    roadmap = ROADMAP.read_text(encoding="utf-8")
    for milestone in ("M01", "M02", "M03", "M04"):
        assert f"milestones/{SPECS[milestone].name}" in roadmap
        assert f"decisions/{milestone}_implementation_decisions.md" in roadmap
        assert f"reviews/{milestone}_completion_review.md" in roadmap
        assert f"tests/unit/test_{milestone.casefold()}_" in roadmap
    assert "equation/data-field" in roadmap or "ledger entries" in roadmap


def test_completed_specs_preserve_scope_and_match_completion_evidence():
    required_boundaries = {
        "M01": ("no implicit water-density", "No powder-property semantics"),
        "M02": ("No silent identity", "No authoritative populated powder records"),
        "M03": ("No inference", "Diagnostics do not execute geometry"),
    }
    for milestone, phrases in required_boundaries.items():
        spec = SPECS[milestone].read_text(encoding="utf-8")
        review = Path(f"docs/modernization/reviews/{milestone}_completion_review.md").read_text(encoding="utf-8")
        assert status(spec) == "accepted"
        assert "implemented_and_reviewed" in review
        assert all(phrase.casefold() in spec.casefold() for phrase in phrases)
        assert Path(f"docs/modernization/decisions/{milestone}_implementation_decisions.md").is_file()


def test_m04_is_accepted_only_with_gate_18_and_completion_review():
    spec = SPECS["M04"].read_text(encoding="utf-8")
    review_path = Path("docs/modernization/reviews/M04_completion_review.md")
    assert "18. Durable milestone governance" in spec
    if status(spec) == "accepted":
        assert review_path.is_file()
        review = review_path.read_text(encoding="utf-8")
        assert "Gate 18" in review and "pass" in review
        assert "specified before" in review


def test_m05_is_records_only_authorized_and_later_phases_are_not_authorized():
    roadmap = ROADMAP.read_text(encoding="utf-8")
    assert status(SPECS["M05"].read_text(encoding="utf-8")) == "authorized"
    assert "authorized only for a later records-and-strict-serialization increment" in roadmap
    assert "no numerical method/data is admitted" in roadmap
    assert "recommendation never authorizes" in roadmap
    for milestone in range(6, 12):
        heading = f"Future Phase Concept M{milestone:02d}"
        assert heading in roadmap
    assert not Path("docs/modernization/reviews/M05_completion_review.md").exists()


def test_agent_guide_requires_specification_first_and_traceable_amendments():
    text = AGENT_GUIDE.read_text(encoding="utf-8")
    assert "Read the applicable canonical specification" in text
    assert "specification is the scope authority" in text
    assert "completion reviews are evidence" in text
    assert "Do not implement a milestone until its canonical specification exists" in text
    assert "Never\n  retroactively edit an acceptance gate" in text
    assert "dated amendment or decision" in text
    assert "For M05 and later" in text
    assert "recommendation in a completion review" in text
