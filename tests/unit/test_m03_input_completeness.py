import pytest

from modern_powley.modernized import (
    CompletenessStatus,
    EvidenceClass,
    InputBundle,
    InputCandidate,
    InputCandidateKind,
    MissingState,
    ModelMaturity,
    Provenance,
    Quantity,
    Unit,
    ValueOrigin,
    evaluate_input_completeness,
    production_requirement_sets,
)


def provenance():
    return Provenance(
        EvidenceClass.EXPLORATORY_HYPOTHESIS,
        ValueOrigin.ASSUMED,
        "SYNTHETIC-M03-SOURCE",
        ModelMaturity.RETAINED_CANDIDATE,
    )


def candidate(name, value, unit, kind=InputCandidateKind.PHYSICAL_VALUE):
    return InputCandidate(
        f"SYNTHETIC-M03-CANDIDATE-{name}", name, kind,
        f"SYNTHETIC-M03-RECORD-{name}", provenance(), Quantity(value, unit),
    )


def category(name, value):
    return InputCandidate(
        f"SYNTHETIC-M03-CANDIDATE-{name}", name,
        InputCandidateKind.CONTROLLED_CATEGORY,
        f"SYNTHETIC-M03-RECORD-{name}", provenance(), category=value,
    )


def bundle(*items):
    return InputBundle("SYNTHETIC-M03-BUNDLE", tuple(items), provenance(), "synthetic diagnostic fixture")


def requirement_set(name):
    return next(item for item in production_requirement_sets() if item.requirement_set_id == name)


def statuses(result):
    return {item.requirement_id: item.status for item in result.diagnostics}


def test_completeness_is_relative_to_named_versioned_existing_operation():
    sets = production_requirement_sets()
    assert sets
    assert all(item.version == 1 and item.operation_already_exists for item in sets)
    assert all(item.requirement_set_id not in {"pressure", "velocity", "powder_screening", "solver"} for item in sets)


def test_circle_area_reports_satisfied_missing_wrong_dimension_and_invalid_value():
    required = requirement_set("circle_area")
    complete = evaluate_input_completeness(required, bundle(candidate("diameter", 7.62, Unit.MILLIMETRE)), record_id="SYNTHETIC-M03-EVAL-1")
    missing = evaluate_input_completeness(required, bundle(), record_id="SYNTHETIC-M03-EVAL-2")
    wrong = evaluate_input_completeness(required, bundle(candidate("diameter", 2, Unit.GRAM)), record_id="SYNTHETIC-M03-EVAL-3")
    invalid = evaluate_input_completeness(required, bundle(candidate("diameter", 0, Unit.MILLIMETRE)), record_id="SYNTHETIC-M03-EVAL-4")
    assert complete.all_declared_conditions_satisfied
    assert statuses(missing)["diameter"] is CompletenessStatus.MISSING
    assert statuses(wrong)["diameter"] is CompletenessStatus.WRONG_QUANTITY_DIMENSION
    assert statuses(invalid)["diameter"] is CompletenessStatus.INVALID_VALUE_DOMAIN


def test_explicit_missing_state_remains_distinct_from_absence_and_zero():
    required = requirement_set("circle_area")
    unavailable = InputCandidate(
        "SYNTHETIC-M03-MISSING", "diameter", InputCandidateKind.PHYSICAL_VALUE,
        "SYNTHETIC-M03-MISSING-RECORD", provenance(),
        missing_state=MissingState.NOT_MEASURED, explanation="synthetic fixture not measured",
    )
    result = evaluate_input_completeness(required, bundle(unavailable), record_id="SYNTHETIC-M03-EVAL-MISSING")
    diagnostic = result.diagnostics[0]
    assert diagnostic.status is CompletenessStatus.EXPLICITLY_UNAVAILABLE
    assert diagnostic.missing_state is MissingState.NOT_MEASURED


def test_capacity_types_cannot_substitute_or_acquire_precedence():
    required = requirement_set("capacity_comparison")
    measured = candidate("measured_usable_capacity", 3.0, Unit.CUBIC_CENTIMETRE, InputCandidateKind.MEASURED_USABLE_CAPACITY)
    estimated = candidate("estimated_usable_capacity", 3.1, Unit.CUBIC_CENTIMETRE, InputCandidateKind.ESTIMATED_USABLE_CAPACITY)
    complete = evaluate_input_completeness(required, bundle(measured, estimated), record_id="SYNTHETIC-M03-EVAL-CAP")
    substituted = candidate("measured_usable_capacity", 3.0, Unit.CUBIC_CENTIMETRE, InputCandidateKind.GROSS_CASE_CAPACITY)
    wrong = evaluate_input_completeness(required, bundle(substituted, estimated), record_id="SYNTHETIC-M03-EVAL-CAP-WRONG")
    assert complete.all_declared_conditions_satisfied
    assert statuses(wrong)["measured_usable_capacity"] is CompletenessStatus.WRONG_RECORD_TYPE
    assert not hasattr(complete, "effective_capacity")


def test_primer_pocket_basis_mismatch_requires_explicit_correction():
    required = requirement_set("geometric_usable_powder_space")
    inputs = (
        candidate("gross_case_capacity", 3.5, Unit.CUBIC_CENTIMETRE, InputCandidateKind.GROSS_CASE_CAPACITY),
        candidate("projectile_displacement", 0.5, Unit.CUBIC_CENTIMETRE),
        category("gross_primer_pocket_treatment", "included"),
        category("target_primer_pocket_treatment", "excluded"),
    )
    missing = evaluate_input_completeness(required, bundle(*inputs), record_id="SYNTHETIC-M03-EVAL-PRIMER-MISSING")
    correction = candidate("primer_pocket_correction", 0.1, Unit.CUBIC_CENTIMETRE, InputCandidateKind.PRIMER_POCKET_CAPACITY)
    corrected = evaluate_input_completeness(required, bundle(*inputs, correction), record_id="SYNTHETIC-M03-EVAL-PRIMER-CORRECTED")
    unknown_inputs = inputs[:-2] + (category("gross_primer_pocket_treatment", "unknown"), category("target_primer_pocket_treatment", "excluded"))
    unknown = evaluate_input_completeness(required, bundle(*unknown_inputs), record_id="SYNTHETIC-M03-EVAL-PRIMER-UNKNOWN")
    assert statuses(missing)["primer_pocket_correction"] is CompletenessStatus.MISSING
    assert "basis mismatch" in next(item.explanation for item in missing.diagnostics if item.requirement_id == "primer_pocket_correction")
    assert corrected.all_declared_conditions_satisfied
    assert statuses(unknown)["primer_pocket_correction"] is CompletenessStatus.INDETERMINATE


def test_unneeded_primer_pocket_correction_is_inconsistent_not_preferred():
    required = requirement_set("geometric_usable_powder_space")
    result = evaluate_input_completeness(
        required,
        bundle(
            candidate("gross_case_capacity", 3.5, Unit.CUBIC_CENTIMETRE, InputCandidateKind.GROSS_CASE_CAPACITY),
            candidate("projectile_displacement", 0.5, Unit.CUBIC_CENTIMETRE),
            category("gross_primer_pocket_treatment", "excluded"),
            category("target_primer_pocket_treatment", "excluded"),
            candidate("primer_pocket_correction", 0.1, Unit.CUBIC_CENTIMETRE, InputCandidateKind.PRIMER_POCKET_CAPACITY),
        ), record_id="SYNTHETIC-M03-EVAL-PRIMER-UNNEEDED",
    )
    assert statuses(result)["primer_pocket_correction"] is CompletenessStatus.MUTUALLY_INCONSISTENT


def test_multiple_candidates_are_preserved_as_conflict_without_selection():
    required = requirement_set("circle_area")
    first = candidate("diameter", 7.6, Unit.MILLIMETRE)
    second = InputCandidate(
        "SYNTHETIC-M03-CANDIDATE-DIAMETER-2", "diameter",
        InputCandidateKind.PHYSICAL_VALUE, "SYNTHETIC-M03-RECORD-DIAMETER-2",
        provenance(), Quantity(7.62, Unit.MILLIMETRE),
    )
    result = evaluate_input_completeness(required, bundle(first, second), record_id="SYNTHETIC-M03-EVAL-CONFLICT")
    diagnostic = result.diagnostics[0]
    assert diagnostic.status is CompletenessStatus.CONFLICTING_SUPPLIED_VALUES
    assert diagnostic.supplied_candidate_ids == (first.candidate_id, second.candidate_id)
    assert not hasattr(result, "preferred_input")


def test_explicit_flat_partial_and_full_geometry_branches_are_separate():
    required = requirement_set("seated_projectile_displacement")
    flat = evaluate_input_completeness(
        required,
        bundle(category("base_geometry", "flat_base"), candidate("shank_diameter", 7.62, Unit.MILLIMETRE), candidate("seated_intrusion", 5, Unit.MILLIMETRE)),
        record_id="SYNTHETIC-M03-EVAL-FLAT",
    )
    assert flat.selected_branch_id == "flat_base"
    assert flat.all_declared_conditions_satisfied
    assert statuses(flat)["partial_tail_length"] is CompletenessStatus.NOT_APPLICABLE

    partial = evaluate_input_completeness(
        required,
        bundle(
            category("base_geometry", "partial_boat_tail"),
            candidate("shank_diameter", 7.62, Unit.MILLIMETRE),
            candidate("boat_tail_base_diameter", 6.2, Unit.MILLIMETRE),
            candidate("boat_tail_axial_length", 4, Unit.MILLIMETRE),
            candidate("seated_intrusion", 2, Unit.MILLIMETRE),
        ), record_id="SYNTHETIC-M03-EVAL-PARTIAL",
    )
    assert partial.selected_branch_id == "partial_boat_tail"
    assert partial.all_declared_conditions_satisfied

    unsupported = evaluate_input_completeness(
        required, bundle(category("base_geometry", "complex_rebated_tail")),
        record_id="SYNTHETIC-M03-EVAL-UNSUPPORTED",
    )
    assert CompletenessStatus.UNSUPPORTED_ALTERNATIVE in statuses(unsupported).values()
    assert not unsupported.all_declared_conditions_satisfied


def test_missing_or_multiple_geometry_branch_is_explicitly_diagnostic():
    required = requirement_set("seated_projectile_displacement")
    missing = evaluate_input_completeness(required, bundle(), record_id="SYNTHETIC-M03-EVAL-NO-BRANCH")
    assert CompletenessStatus.CONDITIONAL_CONTEXT_MISSING in statuses(missing).values()
    multiple = evaluate_input_completeness(
        required,
        bundle(category("base_geometry", "flat_base"), InputCandidate("SYNTHETIC-M03-BRANCH-2", "base_geometry", InputCandidateKind.CONTROLLED_CATEGORY, "SYNTHETIC-M03-BRANCH-RECORD-2", provenance(), category="full_boat_tail")),
        record_id="SYNTHETIC-M03-EVAL-MULTI-BRANCH",
    )
    assert statuses(multiple)["base_geometry"] is CompletenessStatus.MUTUALLY_INCONSISTENT


def test_partial_full_branch_and_tail_diameter_inconsistencies_are_literal():
    required = requirement_set("seated_projectile_displacement")
    partial = evaluate_input_completeness(
        required,
        bundle(
            category("base_geometry", "partial_boat_tail"),
            candidate("shank_diameter", 7.62, Unit.MILLIMETRE),
            candidate("boat_tail_base_diameter", 8.0, Unit.MILLIMETRE),
            candidate("boat_tail_axial_length", 4, Unit.MILLIMETRE),
            candidate("seated_intrusion", 5, Unit.MILLIMETRE),
        ), record_id="SYNTHETIC-M03-EVAL-BRANCH-INCONSISTENT",
    )
    assert statuses(partial)["partial_intrusion"] is CompletenessStatus.MUTUALLY_INCONSISTENT
    assert statuses(partial)["partial_tail_base_diameter"] is CompletenessStatus.INVALID_VALUE_DOMAIN


@pytest.mark.parametrize("name", ["circle_area", "cylinder_volume", "conical_frustum_volume", "barrel_swept_volume", "barrel_volume_ratio", "total_expansion_ratio", "capacity_comparison", "geometric_usable_powder_space", "seated_projectile_displacement"])
def test_production_requirement_set_ids_are_stable_and_unique(name):
    assert requirement_set(name).record_id.startswith("M03-RS-")
