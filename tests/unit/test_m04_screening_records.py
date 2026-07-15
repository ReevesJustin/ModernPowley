from dataclasses import FrozenInstanceError, replace

import pytest

from modern_powley.modernized import (
    BoundKind,
    ConflictDeclaration,
    CriterionDefinition,
    CriterionForm,
    CriterionOutcomeStatus,
    CriterionReference,
    CriterionRole,
    CriterionSetDefinition,
    CriterionSetSummary,
    CriterionStatus,
    EvaluationContext,
    EvaluationMethod,
    EvidenceClass,
    EvidenceReference,
    EvidenceReferenceKind,
    EvidenceValueKind,
    FiniteSetThreshold,
    IdentityQualifier,
    LiteralThreshold,
    ManualAssertionDetails,
    ManualReviewStatus,
    MissingState,
    MissingStateSetThreshold,
    ModelMaturity,
    NumericBoundThreshold,
    NumericIntervalThreshold,
    Provenance,
    Quantity,
    QueryInterval,
    SourceLocator,
    TranscriptionStatus,
    Unit,
    ValueOrigin,
    evaluate_criterion,
    record_manual_assertion,
    summarize_criterion_set,
)


def provenance():
    return Provenance(
        EvidenceClass.EXPLORATORY_HYPOTHESIS,
        ValueOrigin.ASSUMED,
        "SYNTHETIC-M04-SOURCE",
        ModelMaturity.IMPLEMENTED_EXPERIMENTAL,
        notes="synthetic M04 test policy only",
    )


def locator():
    return SourceLocator(
        "SYNTHETIC-M04-SOURCE",
        "synthetic M04 fixture",
        TranscriptionStatus.NOT_APPLICABLE,
    )


def literal_reference(
    value="SYNTHETIC-CATEGORY-A",
    *,
    reference_id="SYNTHETIC-M04-EVIDENCE",
    definition_id="SYNTHETIC_PROPERTY",
    kind=EvidenceValueKind.CATEGORY,
):
    return EvidenceReference(
        reference_id,
        EvidenceReferenceKind.CONTROLLED_CATEGORY,
        "SYNTHETIC-M04-SOURCE-RECORD",
        definition_id,
        kind,
        provenance(),
        locator(),
        literal_value=value,
    )


def numeric_reference(value, unit=Unit.MILLIMETRE, *, reference_id="SYNTHETIC-M04-EVIDENCE"):
    return EvidenceReference(
        reference_id,
        EvidenceReferenceKind.M01_QUANTITY,
        "SYNTHETIC-M04-QUANTITY-RECORD",
        "SYNTHETIC_LENGTH",
        EvidenceValueKind.NUMERIC_POINT,
        provenance(),
        locator(),
        quantity=Quantity(value, unit),
    )


def interval_reference(lower, lower_kind, upper, upper_kind):
    return EvidenceReference(
        "SYNTHETIC-M04-EVIDENCE",
        EvidenceReferenceKind.M02_OBSERVATION,
        "SYNTHETIC-M04-INTERVAL-RECORD",
        "SYNTHETIC_LENGTH",
        EvidenceValueKind.NUMERIC_INTERVAL,
        provenance(),
        locator(),
        interval=QueryInterval(
            Quantity(lower, Unit.MILLIMETRE), lower_kind,
            Quantity(upper, Unit.MILLIMETRE), upper_kind,
        ),
    )


def criterion(
    form=CriterionForm.EXACT_CATEGORICAL_EQUALITY,
    threshold=None,
    *,
    role=CriterionRole.MANDATORY,
    status=CriterionStatus.ACTIVE,
    evidence_ids=("SYNTHETIC-M04-EVIDENCE",),
    definition_id="SYNTHETIC_PROPERTY",
    criterion_id="SYNTHETIC_CRITERION_001",
    version=1,
):
    if threshold is None and form is CriterionForm.EXACT_CATEGORICAL_EQUALITY:
        threshold = LiteralThreshold("SYNTHETIC-CATEGORY-A", "synthetic category", "literal")
    return CriterionDefinition(
        "SYNTHETIC-M04-CRITERION-RECORD",
        criterion_id,
        version,
        "Synthetic criterion",
        "Synthetic criterion used only to test the M04 record contract.",
        "Exercise literal M04 behavior without powder or load guidance.",
        role,
        status,
        form,
        definition_id,
        evidence_ids,
        threshold,
        (),
        provenance(),
        locator(),
        "SYNTHETIC-M04-AUTHORITY",
        "Synthetic contract verification.",
        ("Not a physical screening policy.",),
        "synthetic test era",
    )


def criterion_set(*criteria, status=CriterionStatus.ACTIVE):
    if not criteria:
        criteria = (criterion(),)
    return CriterionSetDefinition(
        "SYNTHETIC-M04-SET-RECORD",
        "SYNTHETIC-M04-SET",
        1,
        "Synthetic criterion set",
        "Test literal decision records only.",
        "No powder, cartridge, load, or recommendation semantics.",
        tuple(
            CriterionReference(item.criterion_id, item.version, item.role, index)
            for index, item in enumerate(criteria)
        ),
        status,
        provenance(),
        locator(),
        "SYNTHETIC-M04-AUTHORITY",
        "synthetic test era",
        ("No production criteria.",),
        "A positive summary does not establish safety, suitability, recommendation, or physical correctness.",
    )


def context(*references, criterion_set_id="SYNTHETIC-M04-SET", version=1):
    return EvaluationContext(
        "SYNTHETIC-M04-CONTEXT",
        criterion_set_id,
        version,
        IdentityQualifier.present("SYNTHETIC-SUBJECT"),
        IdentityQualifier.present("SYNTHETIC_POWDER_ALPHA"),
        IdentityQualifier.missing(MissingState.NOT_SUPPLIED_BY_SOURCE, "synthetic lot omitted"),
        IdentityQualifier.missing(MissingState.NOT_APPLICABLE, "no cartridge is represented"),
        tuple(references),
        "2099-01-01",
        "SYNTHETIC-M04-EVALUATOR",
        "synthetic",
        "0" * 40,
        ("modern_powley.m01.v1", "modern_powley.m02.v1", "modern_powley.m03.v1", "modern_powley.m04.v1"),
        "synthetic records only",
        "Test M04 literal audit records.",
        ("No safety, suitability, prediction, or recommendation conclusion.",),
        provenance(),
    )


def evaluate(item, reference, set_definition=None):
    set_definition = set_definition or criterion_set(item)
    return evaluate_criterion(
        item,
        set_definition,
        context(reference),
        record_id=f"SYNTHETIC-M04-OUTCOME-{item.criterion_id}",
        provenance=provenance(),
        source_locator=locator(),
    )


def bound(value, boundary=BoundKind.INCLUSIVE):
    return NumericBoundThreshold(
        Quantity(value, Unit.MILLIMETRE), boundary, "synthetic length", "literal SI conversion",
        provenance(), "synthetic boundary test",
    )


def interval(lower=1, upper=3, lower_kind=BoundKind.INCLUSIVE, upper_kind=BoundKind.INCLUSIVE):
    return NumericIntervalThreshold(bound(lower, lower_kind), bound(upper, upper_kind))


def test_definitions_are_immutable_versioned_and_nonexecutable():
    item = criterion()
    with pytest.raises(FrozenInstanceError):
        item.version = 2
    assert not hasattr(item, "callback")
    assert not hasattr(item, "expression")
    with pytest.raises(ValueError, match="version"):
        replace(item, version=0)
    with pytest.raises(ValueError, match="inclusion"):
        criterion(CriterionForm.NUMERIC_ABOVE, bound(1, BoundKind.INCLUSIVE), definition_id="SYNTHETIC_LENGTH")


def test_role_status_and_supersession_are_explicit():
    with pytest.raises(ValueError, match="role and activation"):
        criterion(role=CriterionRole.HISTORICAL_RECORD, status=CriterionStatus.ACTIVE)
    inactive = criterion(role=CriterionRole.EXPLICITLY_INACTIVE, status=CriterionStatus.INACTIVE)
    result = evaluate(inactive, literal_reference())
    assert result.result is CriterionOutcomeStatus.INACTIVE_CRITERION
    superseded = replace(criterion(), status=CriterionStatus.SUPERSEDED, supersedes_criterion_id="SYNTHETIC-OLD", supersedes_version=1)
    assert evaluate(superseded, literal_reference()).result is CriterionOutcomeStatus.SUPERSEDED_CRITERION


def test_exact_category_set_identifier_and_presence_forms():
    equal = evaluate(criterion(), literal_reference())
    unequal = evaluate(criterion(), literal_reference("SYNTHETIC-CATEGORY-B"))
    finite = criterion(
        CriterionForm.CATEGORY_IN_FINITE_SET,
        FiniteSetThreshold(("SYNTHETIC-CATEGORY-A", "SYNTHETIC-CATEGORY-B"), "synthetic category", "literal"),
    )
    present = criterion(CriterionForm.REQUIRED_REFERENCE_PRESENT, None)
    assert equal.result is CriterionOutcomeStatus.PASSED
    assert unequal.result is CriterionOutcomeStatus.FAILED
    assert evaluate(finite, literal_reference("SYNTHETIC-CATEGORY-B")).result is CriterionOutcomeStatus.PASSED
    assert evaluate(present, literal_reference()).result is CriterionOutcomeStatus.PASSED


@pytest.mark.parametrize(
    ("form", "boundary", "value", "expected"),
    [
        (CriterionForm.NUMERIC_AT_OR_ABOVE, BoundKind.INCLUSIVE, 2, CriterionOutcomeStatus.PASSED),
        (CriterionForm.NUMERIC_ABOVE, BoundKind.EXCLUSIVE, 2, CriterionOutcomeStatus.FAILED),
        (CriterionForm.NUMERIC_AT_OR_BELOW, BoundKind.INCLUSIVE, 2, CriterionOutcomeStatus.PASSED),
        (CriterionForm.NUMERIC_BELOW, BoundKind.EXCLUSIVE, 2, CriterionOutcomeStatus.FAILED),
    ],
)
def test_numeric_endpoint_semantics(form, boundary, value, expected):
    item = criterion(form, bound(2, boundary), definition_id="SYNTHETIC_LENGTH")
    assert evaluate(item, numeric_reference(value)).result is expected


def test_numeric_units_convert_but_dimensions_and_definitions_do_not_collapse():
    item = criterion(CriterionForm.NUMERIC_AT_OR_ABOVE, bound(25.4), definition_id="SYNTHETIC_LENGTH")
    assert evaluate(item, numeric_reference(1, Unit.INCH)).result is CriterionOutcomeStatus.PASSED
    wrong_dimension = numeric_reference(1, Unit.GRAM)
    assert evaluate(item, wrong_dimension).result is CriterionOutcomeStatus.INPUT_INCOMPATIBLE
    wrong_definition = numeric_reference(30)
    wrong_definition = replace(wrong_definition, definition_id="OTHER_LENGTH_DEFINITION")
    assert evaluate(item, wrong_definition).result is CriterionOutcomeStatus.DEFINITION_MISMATCH


def test_point_and_interval_boundary_behavior_has_no_tolerance():
    point_item = criterion(
        CriterionForm.NUMERIC_POINT_INSIDE_INTERVAL,
        interval(1, 3, BoundKind.EXCLUSIVE, BoundKind.INCLUSIVE),
        definition_id="SYNTHETIC_LENGTH",
    )
    assert evaluate(point_item, numeric_reference(1)).result is CriterionOutcomeStatus.FAILED
    assert evaluate(point_item, numeric_reference(3)).result is CriterionOutcomeStatus.PASSED
    interval_item = criterion(
        CriterionForm.NUMERIC_INTERVAL_FULLY_CONTAINED,
        interval(),
        definition_id="SYNTHETIC_LENGTH",
    )
    contained = evaluate(interval_item, interval_reference(1, BoundKind.INCLUSIVE, 3, BoundKind.INCLUSIVE))
    partial = evaluate(interval_item, interval_reference(0, BoundKind.INCLUSIVE, 2, BoundKind.INCLUSIVE))
    disjoint = evaluate(interval_item, interval_reference(4, BoundKind.INCLUSIVE, 5, BoundKind.INCLUSIVE))
    assert contained.result is CriterionOutcomeStatus.PASSED
    assert partial.result is CriterionOutcomeStatus.INDETERMINATE
    assert disjoint.result is CriterionOutcomeStatus.FAILED


def test_missing_states_and_conflicts_are_retained_without_selection():
    missing_ref = EvidenceReference(
        "SYNTHETIC-M04-EVIDENCE", EvidenceReferenceKind.M02_MISSING_OBSERVATION,
        "SYNTHETIC-M04-MISSING-RECORD", "SYNTHETIC_PROPERTY",
        EvidenceValueKind.MISSING_STATE, provenance(), locator(),
        missing_state=MissingState.NOT_PUBLISHED,
    )
    required = criterion(CriterionForm.REQUIRED_REFERENCE_PRESENT, None)
    assert evaluate(required, missing_ref).result is CriterionOutcomeStatus.EXPLICITLY_UNAVAILABLE
    prohibited = criterion(
        CriterionForm.PROHIBITED_MISSING_STATE_ABSENT,
        MissingStateSetThreshold((MissingState.NOT_PUBLISHED,), "synthetic prohibition"),
    )
    assert evaluate(prohibited, missing_ref).result is CriterionOutcomeStatus.FAILED
    conflict = EvidenceReference(
        "SYNTHETIC-M04-EVIDENCE", EvidenceReferenceKind.M02_CONFLICT,
        "SYNTHETIC-M04-CONFLICT", "SYNTHETIC_PROPERTY",
        EvidenceValueKind.CONFLICT_DECLARATION, provenance(), locator(),
        conflict_declaration=ConflictDeclaration.CONFLICT_PRESENT,
        related_record_ids=("SYNTHETIC-M04-A", "SYNTHETIC-M04-B"),
    )
    outcome = evaluate(required, conflict)
    assert outcome.result is CriterionOutcomeStatus.CONFLICTING_EVIDENCE
    assert outcome.conflicting_record_ids == ("SYNTHETIC-M04-A", "SYNTHETIC-M04-B")


def test_exact_m03_diagnostic_classification_is_reused_not_recomputed():
    item = criterion(
        CriterionForm.REQUIRED_M03_DIAGNOSTIC_CLASSIFICATION,
        LiteralThreshold("inside_declared_domain", "M03 domain result", "exact status"),
        definition_id="m03.domain.SYNTHETIC-CONSTRAINT",
    )
    reference = EvidenceReference(
        "SYNTHETIC-M04-EVIDENCE", EvidenceReferenceKind.M03_DOMAIN_DIAGNOSTIC,
        "SYNTHETIC-M04-SOURCE-RECORD", "m03.domain.SYNTHETIC-CONSTRAINT",
        EvidenceValueKind.DIAGNOSTIC_CLASSIFICATION, provenance(), locator(),
        literal_value="domain_unspecified",
    )
    outcome = evaluate(item, reference)
    assert outcome.result is CriterionOutcomeStatus.FAILED
    assert outcome.referenced_diagnostic_ids == ("SYNTHETIC-M04-SOURCE-RECORD",)


def test_manual_assertion_is_visibly_distinct_from_mechanical_result():
    item = criterion(CriterionForm.EXPLICIT_MANUAL_ASSERTION, None)
    set_definition = criterion_set(item)
    evaluation_context = context(literal_reference())
    refused = evaluate_criterion(
        item, set_definition, evaluation_context, record_id="SYNTHETIC-M04-REFUSED",
        provenance=provenance(), source_locator=locator(),
    )
    assert refused.result is CriterionOutcomeStatus.UNSUPPORTED_COMPARISON
    details = ManualAssertionDetails(
        "SYNTHETIC-M04-REVIEWER", "2099-01-01", "Synthetic manual assertion test.",
        ("SYNTHETIC-M04-EVIDENCE",), ManualReviewStatus.UNREVIEWED,
        EvidenceClass.EXPLORATORY_HYPOTHESIS, ModelMaturity.IMPLEMENTED_EXPERIMENTAL,
        False, ("Not a physical conclusion.",),
    )
    recorded = record_manual_assertion(
        item, set_definition, evaluation_context, record_id="SYNTHETIC-M04-MANUAL",
        result=CriterionOutcomeStatus.INDETERMINATE, reason="Synthetic assertion remains indeterminate.",
        details=details, provenance=provenance(), source_locator=locator(),
    )
    assert recorded.evaluation_method is EvaluationMethod.MANUAL_ASSERTION
    assert recorded.manual_assertion is details
    with pytest.raises(ValueError, match="exact active criterion-set"):
        record_manual_assertion(
            item, set_definition, replace(evaluation_context, criterion_set_version=2),
            record_id="SYNTHETIC-M04-MANUAL-BAD", result=CriterionOutcomeStatus.PASSED,
            reason="Must fail before recording.", details=details,
            provenance=provenance(), source_locator=locator(),
        )


def test_set_summary_uses_active_mandatory_outcomes_only_without_scores():
    mandatory = criterion()
    advisory = criterion(
        criterion_id="SYNTHETIC_CRITERION_002", role=CriterionRole.ADVISORY,
        evidence_ids=("SYNTHETIC-M04-EVIDENCE-2",),
    )
    set_definition = criterion_set(mandatory, advisory)
    evaluation_context = context(
        literal_reference(),
        literal_reference("SYNTHETIC-CATEGORY-B", reference_id="SYNTHETIC-M04-EVIDENCE-2"),
    )
    mandatory_outcome = evaluate_criterion(
        mandatory, set_definition, evaluation_context, record_id="SYNTHETIC-M04-OUTCOME-1",
        provenance=provenance(), source_locator=locator(),
    )
    advisory_outcome = evaluate_criterion(
        advisory, set_definition, evaluation_context, record_id="SYNTHETIC-M04-OUTCOME-2",
        provenance=provenance(), source_locator=locator(),
    )
    summary = summarize_criterion_set(
        set_definition, (mandatory, advisory), evaluation_context,
        (mandatory_outcome, advisory_outcome), record_id="SYNTHETIC-M04-SUMMARY",
        provenance=provenance(),
    )
    assert advisory_outcome.result is CriterionOutcomeStatus.FAILED
    assert summary.summary is CriterionSetSummary.ALL_MANDATORY_RECORDED_PASSES
    assert summary.counts.passed == 1 and summary.counts.failed == 1
    assert not hasattr(summary, "score")
    assert not hasattr(summary, "weight")


def test_set_summary_distinguishes_failure_indeterminate_missing_and_version_error():
    item = criterion()
    set_definition = criterion_set(item)
    evaluation_context = context(literal_reference())
    passed = evaluate_criterion(
        item, set_definition, evaluation_context, record_id="SYNTHETIC-M04-PASS",
        provenance=provenance(), source_locator=locator(),
    )
    failed = replace(passed, record_id="SYNTHETIC-M04-FAIL", result=CriterionOutcomeStatus.FAILED)
    indeterminate = replace(passed, record_id="SYNTHETIC-M04-INDET", result=CriterionOutcomeStatus.INDETERMINATE)
    summarize = lambda outcomes, ctx=evaluation_context: summarize_criterion_set(
        set_definition, (item,), ctx, outcomes, record_id="SYNTHETIC-M04-SUMMARY-X", provenance=provenance()
    )
    assert summarize((failed,)).summary is CriterionSetSummary.MANDATORY_FAILURE_RECORDED
    assert summarize((indeterminate,)).summary is CriterionSetSummary.MANDATORY_INDETERMINATE
    assert summarize(()).summary is CriterionSetSummary.MANDATORY_NOT_EVALUATED
    assert summarize((passed,), replace(evaluation_context, criterion_set_version=2)).summary is CriterionSetSummary.INCONSISTENT_CRITERION_VERSIONS
    duplicate = replace(passed, record_id="SYNTHETIC-M04-DUPLICATE")
    assert summarize((passed, duplicate)).summary is CriterionSetSummary.INCONSISTENT_CRITERION_VERSIONS


def test_advisory_only_set_does_not_receive_vacuous_all_mandatory_pass():
    advisory = criterion(role=CriterionRole.ADVISORY)
    set_definition = criterion_set(advisory)
    evaluation_context = context(literal_reference())
    outcome = evaluate_criterion(
        advisory, set_definition, evaluation_context, record_id="SYNTHETIC-M04-ADVISORY",
        provenance=provenance(), source_locator=locator(),
    )
    summary = summarize_criterion_set(
        set_definition, (advisory,), evaluation_context, (outcome,),
        record_id="SYNTHETIC-M04-ADVISORY-SUMMARY", provenance=provenance(),
    )
    assert summary.summary is CriterionSetSummary.MANDATORY_NOT_EVALUATED
