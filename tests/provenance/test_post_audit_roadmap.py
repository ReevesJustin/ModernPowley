from pathlib import Path


ROADMAP = Path("TODO.md")
ACQUISITION = Path("docs/provenance/original_powley_evidence_acquisition.md")
README = Path("README.md")


def test_roadmap_preserves_two_scope_status_and_blocked_operations():
    text = ROADMAP.read_text(encoding="utf-8")
    assert "`scalar_arithmetic_core`" in text
    assert "`complete_historical_method`: `not_ready_to_freeze`" in text
    assert "Arrow 2" in text
    assert "Expansion Ratio-Velocity" in text
    assert "1961 muzzle-pressure" in text
    assert "MissingProvenanceError" in text
    assert "Remaining Implementation Steps" not in text


def test_roadmap_does_not_offer_later_or_experimental_original_completion_paths():
    text = ROADMAP.read_text(encoding="utf-8")
    assert "complete an original-Powley source gap" in text
    assert "Filling Arrow 2 boundaries from Davis, the emulator" in text
    assert "Reconstructing the velocity surface from the seven retained observations" in text
    assert "Building a load selector, charge predictor, recommended-powder workflow" in text


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
    assert "`complete_historical_method` is `not_ready_to_freeze`" in text
    assert "Current and preserved prototype outputs must not be treated as load" in text
