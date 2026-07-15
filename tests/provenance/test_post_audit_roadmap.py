from pathlib import Path


ROADMAP = Path("TODO.md")
ACQUISITION = Path("docs/provenance/original_powley_evidence_acquisition.md")
README = Path("README.md")
CHARTER = Path("docs/modernization/modern_powley_charter.md")
CLASSES = Path("docs/modernization/evidence_and_model_classes.md")
BOUNDARIES = Path("docs/modernization/model_boundaries.md")
MODERN_ROADMAP = Path("docs/modernization/modern_powley_roadmap.md")
M01 = Path("docs/modernization/phases/M01_canonical_inputs_and_geometry.md")


def test_roadmap_preserves_three_statuses_and_blocked_operations():
    text = ROADMAP.read_text(encoding="utf-8")
    assert "`scalar_arithmetic_core: verified_reference`" in text
    assert "`complete_historical_method: evidence_limited`" in text
    assert "`modernized_powley: authorized_for_development`" in text
    assert "Arrow 2" in text
    assert "Expansion Ratio-Velocity" in text
    assert "1961 muzzle-pressure" in text
    assert "MissingProvenanceError" in text
    assert "Remaining Implementation Steps" not in text


def test_roadmap_separates_historical_and_modern_development_paths():
    text = ROADMAP.read_text(encoding="utf-8")
    assert "evidence-only change policy" in text
    assert "must not be reconstructed from Davis, the emulator, GRT" in text
    assert "Modernized development is authorized outside `original/`" in text
    assert "M01" in text and "next active implementation" in text
    assert "none may enter\n`original/`" in text


def test_evidence_acquisition_document_contains_independent_acceptance_gates():
    text = ACQUISITION.read_text(encoding="utf-8")
    required_gates = (
        "Gate 1: Evidence Retained",
        "Gate 2: Evidence Authenticated And Classified",
        "Gate 3: Scale Digitized",
        "Gate 4: Reconstruction Independently Checked",
        "Gate 5: Interpolation Rules Established",
        "Gate 6: Worked Examples Reconciled",
        "Gate 7: Implementation Authorized",
        "Gate 8: Historical Baseline Freeze Reconsidered",
    )
    for gate in required_gates:
        assert gate in text
    assert "Possession of a photograph or transcription does not authorize implementation" in text
    assert "Preserve the original bytes" in text
    assert "Calculate and record SHA-256" in text


def test_readme_does_not_present_a_current_loading_or_prediction_workflow():
    text = README.read_text(encoding="utf-8")
    assert "There is no supported load-selection" in text
    assert "`complete_historical_method: evidence_limited`" in text
    assert "`modernized_powley: authorized_for_development`" in text
    assert "evidence-only policy" in text
    assert "Current and preserved prototype outputs must not be treated as load" in text


def test_modernization_governance_documents_exist_and_separate_provenance():
    for path in (CHARTER, CLASSES, BOUNDARIES, MODERN_ROADMAP, M01):
        assert path.is_file()
    charter = CHARTER.read_text(encoding="utf-8")
    boundaries = BOUNDARIES.read_text(encoding="utf-8")
    assert "not:" in charter
    assert "a reconstruction of unavailable physical scales" in charter
    assert "outside `original/`" in charter
    assert "does not establish historical provenance" in boundaries
    assert "MissingProvenanceError" in boundaries


def test_m01_is_geometry_only_and_has_promotion_gates():
    text = M01.read_text(encoding="utf-8")
    assert "next active implementation phase" in text
    assert "Canonical Internal Unit Policy" in text
    assert "Measured seating-specific usable powder space is authoritative" in text
    assert "M01 Exclusions" in text
    assert "powder selection or burn-rate ranking" in text
    assert "Acceptance Gates" in text
    assert "No numerical ballistics prediction" in text


def test_no_current_candidate_is_promoted_by_modernization_policy():
    text = CLASSES.read_text(encoding="utf-8")
    assert "No current `Ba_target`, `Ba_eff`, charge regression" in text
    assert "is classified\n`promoted_modern`" in text
