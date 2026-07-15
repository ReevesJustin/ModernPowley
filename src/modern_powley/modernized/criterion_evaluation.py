"""Narrow literal M04 evaluation and descriptive set aggregation."""

from __future__ import annotations

from .property_domains import BoundKind
from .property_observations import SourceLocator
from .provenance import Provenance
from .screening_contexts import (
    ConflictDeclaration,
    EvaluationContext,
    EvidenceReference,
    EvidenceReferenceKind,
    EvidenceValueKind,
)
from .screening_criteria import (
    CriterionDefinition,
    CriterionForm,
    CriterionRole,
    CriterionSetDefinition,
    CriterionStatus,
    FiniteSetThreshold,
    LiteralThreshold,
    MissingStateSetThreshold,
    NumericBoundThreshold,
    NumericIntervalThreshold,
)
from .screening_outcomes import (
    CriterionEvaluationRecord,
    CriterionOutcomeStatus,
    CriterionSetOutcomeRecord,
    CriterionSetSummary,
    EvaluationMethod,
    ManualAssertionDetails,
    OutcomeCounts,
)


_INACTIVE_STATUSES = {
    CriterionStatus.INACTIVE,
    CriterionStatus.WITHDRAWN,
    CriterionStatus.HISTORICAL,
    CriterionStatus.EXPERIMENTAL,
    CriterionStatus.EVIDENCE_LIMITED,
    CriterionStatus.UNAVAILABLE,
}


def _result(
    criterion: CriterionDefinition,
    criterion_set: CriterionSetDefinition,
    context: EvaluationContext,
    references: tuple[EvidenceReference, ...],
    *,
    record_id: str,
    status: CriterionOutcomeStatus,
    comparison: str,
    reason: str,
    provenance: Provenance,
    source_locator: SourceLocator,
    manual: ManualAssertionDetails | None = None,
) -> CriterionEvaluationRecord:
    observations = tuple(
        item.source_record_id
        for item in references
        if item.reference_kind in {
            EvidenceReferenceKind.M02_OBSERVATION,
            EvidenceReferenceKind.M02_MISSING_OBSERVATION,
            EvidenceReferenceKind.M02_CONFLICT,
        }
    )
    diagnostics = tuple(
        item.source_record_id
        for item in references
        if item.reference_kind in {
            EvidenceReferenceKind.M03_COMPLETENESS_DIAGNOSTIC,
            EvidenceReferenceKind.M03_DOMAIN_DIAGNOSTIC,
        }
    )
    conflicts = tuple(
        related
        for item in references
        if item.conflict_declaration in {
            ConflictDeclaration.CONFLICT_PRESENT,
            ConflictDeclaration.UNRESOLVED,
        }
        for related in item.related_record_ids
    )
    return CriterionEvaluationRecord(
        record_id=record_id,
        criterion_id=criterion.criterion_id,
        criterion_version=criterion.version,
        criterion_set_id=criterion_set.criterion_set_id,
        criterion_set_version=criterion_set.version,
        evaluation_context_id=context.record_id,
        referenced_evidence_ids=tuple(item.reference_id for item in references),
        referenced_observation_ids=observations,
        referenced_diagnostic_ids=diagnostics,
        supplied_values=tuple(item.to_dict() for item in references),
        comparison_performed=comparison,
        retained_threshold=None if criterion.threshold is None else criterion.threshold.to_dict(),
        result=status,
        reason=reason,
        provenance=provenance,
        source_locator=source_locator,
        evaluation_method=(
            EvaluationMethod.MANUAL_ASSERTION if manual is not None else EvaluationMethod.MECHANICAL_LITERAL
        ),
        manual_assertion=manual,
        dependency_record_ids=(criterion.record_id, criterion_set.record_id, context.record_id),
        conflicting_record_ids=conflicts,
        qualifications=criterion.known_limitations,
        review_context="M04 literal criterion evaluation",
    )


def _inside_point(value: float, interval: NumericIntervalThreshold) -> bool:
    lower, upper = interval.lower.quantity.si_value, interval.upper.quantity.si_value
    lower_ok = value > lower or (
        value == lower and interval.lower.boundary is BoundKind.INCLUSIVE
    )
    upper_ok = value < upper or (
        value == upper and interval.upper.boundary is BoundKind.INCLUSIVE
    )
    return lower_ok and upper_ok


def _interval_relation(reference: EvidenceReference, threshold: NumericIntervalThreshold) -> str:
    query = reference.interval
    assert query is not None
    ql, qu = query.lower.si_value, query.upper.si_value
    tl, tu = threshold.lower.quantity.si_value, threshold.upper.quantity.si_value
    below = qu < tl or (
        qu == tl
        and (query.upper_kind is BoundKind.EXCLUSIVE or threshold.lower.boundary is BoundKind.EXCLUSIVE)
    )
    above = ql > tu or (
        ql == tu
        and (query.lower_kind is BoundKind.EXCLUSIVE or threshold.upper.boundary is BoundKind.EXCLUSIVE)
    )
    if below or above:
        return "disjoint"
    lower_inside = ql > tl or (
        ql == tl
        and not (
            query.lower_kind is BoundKind.INCLUSIVE
            and threshold.lower.boundary is BoundKind.EXCLUSIVE
        )
    )
    upper_inside = qu < tu or (
        qu == tu
        and not (
            query.upper_kind is BoundKind.INCLUSIVE
            and threshold.upper.boundary is BoundKind.EXCLUSIVE
        )
    )
    return "contained" if lower_inside and upper_inside else "partial_overlap"


def evaluate_criterion(
    criterion: CriterionDefinition,
    criterion_set: CriterionSetDefinition,
    context: EvaluationContext,
    *,
    record_id: str,
    provenance: Provenance,
    source_locator: SourceLocator,
) -> CriterionEvaluationRecord:
    """Apply one controlled literal form to exact caller-supplied references."""

    if (context.criterion_set_id, context.criterion_set_version) != (
        criterion_set.criterion_set_id,
        criterion_set.version,
    ):
        return _result(
            criterion, criterion_set, context, (), record_id=record_id,
            status=CriterionOutcomeStatus.INVALID_CRITERION,
            comparison="Compared exact criterion-set identity and version.",
            reason="Evaluation context references a different criterion-set identity or version.",
            provenance=provenance, source_locator=source_locator,
        )
    if criterion_set.status is not CriterionStatus.ACTIVE:
        return _result(
            criterion, criterion_set, context, (), record_id=record_id,
            status=CriterionOutcomeStatus.INACTIVE_CRITERION,
            comparison="Inspected criterion-set activation status.",
            reason="Criterion set is not active.", provenance=provenance,
            source_locator=source_locator,
        )
    set_reference = next(
        (
            item for item in criterion_set.criteria
            if (item.criterion_id, item.criterion_version) == (criterion.criterion_id, criterion.version)
        ),
        None,
    )
    if set_reference is None or set_reference.role is not criterion.role:
        return _result(
            criterion, criterion_set, context, (), record_id=record_id,
            status=CriterionOutcomeStatus.INVALID_CRITERION,
            comparison="Compared exact criterion identity, version, and role with the set declaration.",
            reason="Criterion is absent from the set or its declared role differs.",
            provenance=provenance, source_locator=source_locator,
        )
    by_id = {item.reference_id: item for item in context.evidence_references}
    references = tuple(
        by_id[item] for item in criterion.required_evidence_ids if item in by_id
    )
    if criterion.status is CriterionStatus.SUPERSEDED:
        return _result(
            criterion, criterion_set, context, references, record_id=record_id,
            status=CriterionOutcomeStatus.SUPERSEDED_CRITERION,
            comparison="Inspected criterion activation status.",
            reason="Superseded criterion definitions are retained but not evaluated as active.",
            provenance=provenance, source_locator=source_locator,
        )
    if criterion.status in _INACTIVE_STATUSES or criterion.role in {
        CriterionRole.EXPLICITLY_INACTIVE,
        CriterionRole.HISTORICAL_RECORD,
        CriterionRole.EXPERIMENTAL_RECORD,
        CriterionRole.UNAVAILABLE_AT_CURRENT_MATURITY,
    }:
        status = (
            CriterionOutcomeStatus.EXPLICITLY_UNAVAILABLE
            if criterion.status is CriterionStatus.UNAVAILABLE
            else CriterionOutcomeStatus.INACTIVE_CRITERION
        )
        return _result(
            criterion, criterion_set, context, references, record_id=record_id,
            status=status, comparison="Inspected criterion activation status.",
            reason="Criterion is not active modernization policy.",
            provenance=provenance, source_locator=source_locator,
        )
    if len(references) != len(criterion.required_evidence_ids):
        return _result(
            criterion, criterion_set, context, references, record_id=record_id,
            status=CriterionOutcomeStatus.INPUT_MISSING,
            comparison="Matched exact required evidence reference IDs.",
            reason="One or more exact evidence references were not supplied.",
            provenance=provenance, source_locator=source_locator,
        )
    if criterion.form is not CriterionForm.PROHIBITED_MISSING_STATE_ABSENT and any(
        item.missing_state is not None for item in references
    ):
        return _result(
            criterion, criterion_set, context, references, record_id=record_id,
            status=CriterionOutcomeStatus.EXPLICITLY_UNAVAILABLE,
            comparison="Inspected retained M02 missing-state classifications.",
            reason="A required evidence record is explicitly unavailable; no numerical comparison was made.",
            provenance=provenance, source_locator=source_locator,
        )
    if criterion.form is not CriterionForm.NO_RECORDED_CONFLICT and any(
        item.conflict_declaration in {ConflictDeclaration.CONFLICT_PRESENT, ConflictDeclaration.UNRESOLVED}
        for item in references
    ):
        return _result(
            criterion, criterion_set, context, references, record_id=record_id,
            status=CriterionOutcomeStatus.CONFLICTING_EVIDENCE,
            comparison="Inspected explicit conflict declarations without selecting a record.",
            reason="Supplied evidence retains an unresolved conflict.",
            provenance=provenance, source_locator=source_locator,
        )
    if any(item.definition_id != criterion.reference_definition_id for item in references):
        return _result(
            criterion, criterion_set, context, references, record_id=record_id,
            status=CriterionOutcomeStatus.DEFINITION_MISMATCH,
            comparison="Compared evidence and criterion definition identifiers literally.",
            reason="At least one supplied evidence definition differs from the criterion definition.",
            provenance=provenance, source_locator=source_locator,
        )
    if criterion.form is CriterionForm.EXPLICIT_MANUAL_ASSERTION:
        return _result(
            criterion, criterion_set, context, references, record_id=record_id,
            status=CriterionOutcomeStatus.UNSUPPORTED_COMPARISON,
            comparison="Refused to infer a manual assertion mechanically.",
            reason="Use record_manual_assertion with explicit responsible-party details.",
            provenance=provenance, source_locator=source_locator,
        )

    reference = references[0]
    passed = False
    failed = False
    comparison = "Applied the exact controlled criterion form."
    reason = ""
    if criterion.form is CriterionForm.REQUIRED_REFERENCE_PRESENT:
        passed = True
        reason = "Every exact required evidence reference was supplied."
    elif criterion.form is CriterionForm.PROHIBITED_MISSING_STATE_ABSENT:
        assert isinstance(criterion.threshold, MissingStateSetThreshold)
        passed = all(item.missing_state not in criterion.threshold.states for item in references)
        failed = not passed
        reason = "No prohibited missing state is present." if passed else "A prohibited missing state is present."
    elif criterion.form in {
        CriterionForm.REQUIRED_M03_DIAGNOSTIC_CLASSIFICATION,
        CriterionForm.EXACT_CATEGORICAL_EQUALITY,
        CriterionForm.EXACT_IDENTIFIER_EQUALITY,
        CriterionForm.NO_RECORDED_CONFLICT,
    }:
        assert isinstance(criterion.threshold, LiteralThreshold)
        actual = (
            reference.conflict_declaration.value
            if reference.conflict_declaration is not None
            else reference.literal_value
        )
        passed, failed = actual == criterion.threshold.value, actual != criterion.threshold.value
        comparison = "Compared the supplied literal and declared literal for exact equality."
        reason = "Exact literal equality was satisfied." if passed else "Exact literal equality was not satisfied."
    elif criterion.form is CriterionForm.CATEGORY_IN_FINITE_SET:
        assert isinstance(criterion.threshold, FiniteSetThreshold)
        passed = reference.literal_value in criterion.threshold.values
        failed = not passed
        comparison = "Compared the supplied category with the declared finite set literally."
        reason = "Category is in the declared finite set." if passed else "Category is not in the declared finite set."
    elif criterion.form in {
        CriterionForm.NUMERIC_AT_OR_ABOVE, CriterionForm.NUMERIC_ABOVE,
        CriterionForm.NUMERIC_AT_OR_BELOW, CriterionForm.NUMERIC_BELOW,
    }:
        assert isinstance(criterion.threshold, NumericBoundThreshold)
        if reference.quantity is None:
            return _result(
                criterion, criterion_set, context, references, record_id=record_id,
                status=CriterionOutcomeStatus.INPUT_INCOMPATIBLE,
                comparison="Required a numeric-point evidence payload.",
                reason="Supplied evidence is not a numeric point.", provenance=provenance,
                source_locator=source_locator,
            )
        if reference.quantity.dimension is not criterion.threshold.quantity.dimension:
            return _result(
                criterion, criterion_set, context, references, record_id=record_id,
                status=CriterionOutcomeStatus.INPUT_INCOMPATIBLE,
                comparison="Compared M01 quantity dimensions.",
                reason="Supplied quantity and threshold dimensions are incompatible.",
                provenance=provenance, source_locator=source_locator,
            )
        value, bound = reference.quantity.si_value, criterion.threshold.quantity.si_value
        passed = {
            CriterionForm.NUMERIC_AT_OR_ABOVE: value >= bound,
            CriterionForm.NUMERIC_ABOVE: value > bound,
            CriterionForm.NUMERIC_AT_OR_BELOW: value <= bound,
            CriterionForm.NUMERIC_BELOW: value < bound,
        }[criterion.form]
        failed = not passed
        comparison = "Converted compatible M01 quantities to SI and applied the declared endpoint rule."
        reason = "Numeric bound was satisfied." if passed else "Numeric bound was not satisfied."
    elif criterion.form is CriterionForm.NUMERIC_POINT_INSIDE_INTERVAL:
        assert isinstance(criterion.threshold, NumericIntervalThreshold)
        if reference.quantity is None:
            return _result(
                criterion, criterion_set, context, references, record_id=record_id,
                status=CriterionOutcomeStatus.INPUT_INCOMPATIBLE,
                comparison="Required a numeric-point evidence payload.",
                reason="Supplied evidence is not a numeric point.", provenance=provenance,
                source_locator=source_locator,
            )
        if reference.quantity.dimension is not criterion.threshold.lower.quantity.dimension:
            return _result(
                criterion, criterion_set, context, references, record_id=record_id,
                status=CriterionOutcomeStatus.INPUT_INCOMPATIBLE,
                comparison="Compared M01 quantity dimensions.",
                reason="Supplied quantity and interval dimensions are incompatible.",
                provenance=provenance, source_locator=source_locator,
            )
        passed = _inside_point(reference.quantity.si_value, criterion.threshold)
        failed = not passed
        comparison = "Converted compatible quantities to SI and applied both declared interval endpoints."
        reason = "Point is inside the declared interval." if passed else "Point is outside the declared interval."
    elif criterion.form is CriterionForm.NUMERIC_INTERVAL_FULLY_CONTAINED:
        assert isinstance(criterion.threshold, NumericIntervalThreshold)
        if reference.interval is None:
            return _result(
                criterion, criterion_set, context, references, record_id=record_id,
                status=CriterionOutcomeStatus.INPUT_INCOMPATIBLE,
                comparison="Required a numeric-interval evidence payload.",
                reason="Supplied evidence is not a numeric interval.", provenance=provenance,
                source_locator=source_locator,
            )
        if reference.interval.lower.dimension is not criterion.threshold.lower.quantity.dimension:
            return _result(
                criterion, criterion_set, context, references, record_id=record_id,
                status=CriterionOutcomeStatus.INPUT_INCOMPATIBLE,
                comparison="Compared M01 interval dimensions.",
                reason="Supplied interval and criterion interval dimensions are incompatible.",
                provenance=provenance, source_locator=source_locator,
            )
        relation = _interval_relation(reference, criterion.threshold)
        if relation == "partial_overlap":
            return _result(
                criterion, criterion_set, context, references, record_id=record_id,
                status=CriterionOutcomeStatus.INDETERMINATE,
                comparison="Compared full interval containment without selecting a midpoint.",
                reason="Intervals partially overlap; the supplied interval is not fully contained.",
                provenance=provenance, source_locator=source_locator,
            )
        passed, failed = relation == "contained", relation == "disjoint"
        comparison = "Compared full interval containment with exact endpoint inclusion."
        reason = "Supplied interval is fully contained." if passed else "Supplied interval is disjoint from the criterion interval."
    else:
        return _result(
            criterion, criterion_set, context, references, record_id=record_id,
            status=CriterionOutcomeStatus.UNSUPPORTED_COMPARISON,
            comparison="Inspected the controlled criterion form.",
            reason="Criterion form has no admitted literal evaluator.", provenance=provenance,
            source_locator=source_locator,
        )
    return _result(
        criterion, criterion_set, context, references, record_id=record_id,
        status=CriterionOutcomeStatus.PASSED if passed else CriterionOutcomeStatus.FAILED,
        comparison=comparison, reason=reason, provenance=provenance, source_locator=source_locator,
    )


def record_manual_assertion(
    criterion: CriterionDefinition,
    criterion_set: CriterionSetDefinition,
    context: EvaluationContext,
    *,
    record_id: str,
    result: CriterionOutcomeStatus,
    reason: str,
    details: ManualAssertionDetails,
    provenance: Provenance,
    source_locator: SourceLocator,
) -> CriterionEvaluationRecord:
    """Retain a visible manual assertion without claiming mechanical evaluation."""

    if criterion.form is not CriterionForm.EXPLICIT_MANUAL_ASSERTION:
        raise ValueError("manual assertions require the explicit manual-assertion criterion form")
    if (context.criterion_set_id, context.criterion_set_version) != (
        criterion_set.criterion_set_id, criterion_set.version
    ) or criterion_set.status is not CriterionStatus.ACTIVE:
        raise ValueError("manual assertion requires the exact active criterion-set context")
    set_reference = next(
        (
            item for item in criterion_set.criteria
            if (item.criterion_id, item.criterion_version) == (criterion.criterion_id, criterion.version)
        ),
        None,
    )
    if set_reference is None or set_reference.role is not criterion.role or criterion.status is not CriterionStatus.ACTIVE:
        raise ValueError("manual assertion requires the exact active criterion definition")
    if result in {CriterionOutcomeStatus.INVALID_CRITERION, CriterionOutcomeStatus.SUPERSEDED_CRITERION}:
        raise ValueError("manual assertion cannot override criterion validity or supersession")
    by_id = {item.reference_id: item for item in context.evidence_references}
    references = tuple(by_id[item] for item in criterion.required_evidence_ids if item in by_id)
    if len(references) != len(criterion.required_evidence_ids):
        raise ValueError("manual assertion requires every exact evidence reference")
    if tuple(details.evidence_reference_ids) != tuple(criterion.required_evidence_ids):
        raise ValueError("manual assertion must identify the criterion's exact evidence references")
    return _result(
        criterion, criterion_set, context, references, record_id=record_id, status=result,
        comparison="Manual assertion recorded; no mechanical comparison performed.", reason=reason,
        provenance=provenance, source_locator=source_locator, manual=details,
    )


def summarize_criterion_set(
    criterion_set: CriterionSetDefinition,
    definitions: tuple[CriterionDefinition, ...],
    context: EvaluationContext,
    evaluations: tuple[CriterionEvaluationRecord, ...],
    *,
    record_id: str,
    provenance: Provenance,
) -> CriterionSetOutcomeRecord:
    """Summarize exact recorded mandatory outcomes without weights or ranking."""

    summary = CriterionSetSummary.ALL_MANDATORY_RECORDED_PASSES
    reason = "Every active mandatory criterion has an exact recorded pass."
    definitions_by_key = {(item.criterion_id, item.version): item for item in definitions}
    evaluations_by_key = {(item.criterion_id, item.criterion_version): item for item in evaluations}
    duplicate_evaluation_keys = len(evaluations_by_key) != len(evaluations)
    version_error = (
        (context.criterion_set_id, context.criterion_set_version)
        != (criterion_set.criterion_set_id, criterion_set.version)
        or duplicate_evaluation_keys
        or any(
            (item.criterion_set_id, item.criterion_set_version)
            != (criterion_set.criterion_set_id, criterion_set.version)
            or item.evaluation_context_id != context.record_id
            for item in evaluations
        )
    )
    if version_error or any(
        (item.criterion_id, item.criterion_version) not in definitions_by_key
        for item in criterion_set.criteria
    ):
        summary = CriterionSetSummary.INCONSISTENT_CRITERION_VERSIONS
        reason = "Criterion, set, or context versions are inconsistent."
    elif criterion_set.status is not CriterionStatus.ACTIVE:
        summary = CriterionSetSummary.SET_INACTIVE_OR_INVALID
        reason = "Criterion set is not active."
    else:
        mandatory = tuple(
            item for item in criterion_set.criteria
            if item.role is CriterionRole.MANDATORY
            and definitions_by_key[(item.criterion_id, item.criterion_version)].status is CriterionStatus.ACTIVE
        )
        mandatory_outcomes = tuple(
            evaluations_by_key.get((item.criterion_id, item.criterion_version))
            for item in mandatory
        )
        if not mandatory:
            summary = CriterionSetSummary.MANDATORY_NOT_EVALUATED
            reason = "Criterion set declares no active mandatory criteria."
        elif any(item is None for item in mandatory_outcomes):
            summary = CriterionSetSummary.MANDATORY_NOT_EVALUATED
            reason = "At least one active mandatory criterion has no exact recorded outcome."
        else:
            statuses = {item.result for item in mandatory_outcomes if item is not None}
            if CriterionOutcomeStatus.FAILED in statuses:
                summary = CriterionSetSummary.MANDATORY_FAILURE_RECORDED
                reason = "At least one active mandatory criterion has a recorded failure."
            elif statuses - {CriterionOutcomeStatus.PASSED}:
                indeterminate = {
                    CriterionOutcomeStatus.INDETERMINATE,
                    CriterionOutcomeStatus.EXPLICITLY_UNAVAILABLE,
                    CriterionOutcomeStatus.CONFLICTING_EVIDENCE,
                    CriterionOutcomeStatus.INPUT_MISSING,
                    CriterionOutcomeStatus.INPUT_INCOMPATIBLE,
                    CriterionOutcomeStatus.DEFINITION_MISMATCH,
                    CriterionOutcomeStatus.OUTSIDE_DECLARED_DOMAIN,
                    CriterionOutcomeStatus.UNSUPPORTED_COMPARISON,
                }
                if statuses & indeterminate:
                    summary = CriterionSetSummary.MANDATORY_INDETERMINATE
                    reason = "No mandatory failure was recorded, but determination is incomplete."
                else:
                    summary = CriterionSetSummary.MANDATORY_NOT_EVALUATED
                    reason = "At least one mandatory criterion was not actively evaluated."

    all_statuses = [item.result for item in evaluations]
    counts = OutcomeCounts(
        passed=all_statuses.count(CriterionOutcomeStatus.PASSED),
        failed=all_statuses.count(CriterionOutcomeStatus.FAILED),
        indeterminate=sum(
            item in {
                CriterionOutcomeStatus.INDETERMINATE,
                CriterionOutcomeStatus.CONFLICTING_EVIDENCE,
                CriterionOutcomeStatus.EXPLICITLY_UNAVAILABLE,
            }
            for item in all_statuses
        ),
        unevaluated=sum(
            item in {CriterionOutcomeStatus.NOT_EVALUATED, CriterionOutcomeStatus.INACTIVE_CRITERION}
            for item in all_statuses
        ),
        other=0,
    )
    classified = counts.passed + counts.failed + counts.indeterminate + counts.unevaluated
    counts = OutcomeCounts(counts.passed, counts.failed, counts.indeterminate, counts.unevaluated, len(all_statuses) - classified)
    return CriterionSetOutcomeRecord(
        record_id, criterion_set.criterion_set_id, criterion_set.version, context.record_id,
        tuple(item.record_id for item in evaluations), summary, counts, reason,
        criterion_set.non_implication_statement, provenance,
    )
