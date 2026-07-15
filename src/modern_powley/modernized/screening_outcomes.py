"""Immutable M04 criterion and criterion-set outcome records."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from .property_observations import SourceLocator
from .provenance import EvidenceClass, ModelMaturity, Provenance
from .screening_criteria import M04_SCHEMA_ID, _strict, _text


class EvaluationMethod(str, Enum):
    """How the retained outcome was obtained."""

    MECHANICAL_LITERAL = "mechanical_literal"
    MANUAL_ASSERTION = "manual_assertion"


class CriterionOutcomeStatus(str, Enum):
    """Controlled outcome without suitability or safety semantics."""

    PASSED = "passed"
    FAILED = "failed"
    INDETERMINATE = "indeterminate"
    NOT_EVALUATED = "not_evaluated"
    EXPLICITLY_UNAVAILABLE = "explicitly_unavailable"
    CONFLICTING_EVIDENCE = "conflicting_evidence"
    INVALID_CRITERION = "invalid_criterion"
    INPUT_MISSING = "input_missing"
    INPUT_INCOMPATIBLE = "input_incompatible"
    DEFINITION_MISMATCH = "definition_mismatch"
    OUTSIDE_DECLARED_DOMAIN = "outside_declared_domain"
    UNSUPPORTED_COMPARISON = "unsupported_comparison"
    SUPERSEDED_CRITERION = "superseded_criterion"
    INACTIVE_CRITERION = "inactive_criterion"


class ManualReviewStatus(str, Enum):
    """Review state of an explicitly manual assertion."""

    UNREVIEWED = "unreviewed"
    REVIEWED = "reviewed"
    INDEPENDENTLY_REVIEWED = "independently_reviewed"


@dataclass(frozen=True, slots=True)
class ManualAssertionDetails:
    """Responsible party and evidence for a visibly manual result."""

    responsible_party: str
    assertion_date: str
    rationale: str
    evidence_reference_ids: tuple[str, ...]
    review_status: ManualReviewStatus
    evidence_class: EvidenceClass
    model_maturity: ModelMaturity
    independently_verified: bool
    qualifications: tuple[str, ...]

    def __post_init__(self) -> None:
        for value, name in (
            (self.responsible_party, "responsible_party"),
            (self.assertion_date, "assertion_date"),
            (self.rationale, "rationale"),
        ):
            _text(value, name)
        object.__setattr__(self, "review_status", ManualReviewStatus(self.review_status))
        object.__setattr__(self, "evidence_class", EvidenceClass(self.evidence_class))
        object.__setattr__(self, "model_maturity", ModelMaturity(self.model_maturity))
        if not self.evidence_reference_ids or any(not item.strip() for item in self.evidence_reference_ids):
            raise ValueError("manual assertion requires evidence reference IDs")
        if any(not item.strip() for item in self.qualifications):
            raise ValueError("manual assertion qualifications must be nonblank")
        if self.independently_verified and self.review_status is not ManualReviewStatus.INDEPENDENTLY_REVIEWED:
            raise ValueError("independent verification requires independently reviewed status")

    def to_dict(self) -> dict[str, object]:
        return {
            "responsible_party": self.responsible_party,
            "assertion_date": self.assertion_date,
            "rationale": self.rationale,
            "evidence_reference_ids": list(self.evidence_reference_ids),
            "review_status": self.review_status.value,
            "evidence_class": self.evidence_class.value,
            "model_maturity": self.model_maturity.value,
            "independently_verified": self.independently_verified,
            "qualifications": list(self.qualifications),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> ManualAssertionDetails:
        fields = {
            "responsible_party", "assertion_date", "rationale", "evidence_reference_ids",
            "review_status", "evidence_class", "model_maturity", "independently_verified",
            "qualifications",
        }
        _strict(data, fields)
        references, qualifications = data["evidence_reference_ids"], data["qualifications"]
        if any(not isinstance(value, list) or not all(isinstance(item, str) for item in value) for value in (references, qualifications)):
            raise TypeError("manual assertion reference and qualification fields are malformed")
        if not isinstance(data["independently_verified"], bool):
            raise TypeError("independently_verified must be Boolean")
        return cls(
            str(data["responsible_party"]), str(data["assertion_date"]),
            str(data["rationale"]), tuple(references),
            ManualReviewStatus(str(data["review_status"])),
            EvidenceClass(str(data["evidence_class"])),
            ModelMaturity(str(data["model_maturity"])),
            data["independently_verified"], tuple(qualifications),
        )


@dataclass(frozen=True, slots=True)
class CriterionEvaluationRecord:
    """One exact criterion-version outcome retaining its complete audit chain."""

    record_id: str
    criterion_id: str
    criterion_version: int
    criterion_set_id: str
    criterion_set_version: int
    evaluation_context_id: str
    referenced_evidence_ids: tuple[str, ...]
    referenced_observation_ids: tuple[str, ...]
    referenced_diagnostic_ids: tuple[str, ...]
    supplied_values: tuple[dict[str, object], ...]
    comparison_performed: str
    retained_threshold: dict[str, object] | None
    result: CriterionOutcomeStatus
    reason: str
    provenance: Provenance
    source_locator: SourceLocator
    evaluation_method: EvaluationMethod
    manual_assertion: ManualAssertionDetails | None
    dependency_record_ids: tuple[str, ...]
    conflicting_record_ids: tuple[str, ...]
    qualifications: tuple[str, ...]
    review_context: str

    def __post_init__(self) -> None:
        from .screening_contexts import EvidenceReference
        from .screening_criteria import threshold_from_dict

        for value, name in (
            (self.record_id, "record_id"), (self.criterion_id, "criterion_id"),
            (self.criterion_set_id, "criterion_set_id"),
            (self.evaluation_context_id, "evaluation_context_id"),
            (self.comparison_performed, "comparison_performed"),
            (self.reason, "reason"), (self.review_context, "review_context"),
        ):
            _text(value, name)
        if any(isinstance(value, bool) or not isinstance(value, int) for value in (self.criterion_version, self.criterion_set_version)) or self.criterion_version <= 0 or self.criterion_set_version <= 0:
            raise ValueError("criterion and set versions must be positive")
        object.__setattr__(self, "result", CriterionOutcomeStatus(self.result))
        object.__setattr__(self, "evaluation_method", EvaluationMethod(self.evaluation_method))
        if self.provenance.source_id != self.source_locator.source_id:
            raise ValueError("outcome provenance and source locator must match")
        if self.evaluation_method is EvaluationMethod.MANUAL_ASSERTION:
            if self.manual_assertion is None:
                raise ValueError("manual outcome requires manual assertion details")
        elif self.manual_assertion is not None:
            raise ValueError("mechanical outcome cannot carry manual assertion details")
        if self.result is CriterionOutcomeStatus.CONFLICTING_EVIDENCE and not self.conflicting_record_ids:
            raise ValueError("conflicting outcome requires conflicting record IDs")
        lists = (
            self.referenced_evidence_ids, self.referenced_observation_ids,
            self.referenced_diagnostic_ids, self.dependency_record_ids,
            self.conflicting_record_ids, self.qualifications,
        )
        if any(any(not item.strip() for item in values) for values in lists):
            raise ValueError("outcome reference and qualification IDs must be nonblank")
        if any(not isinstance(value, dict) for value in self.supplied_values):
            raise TypeError("supplied values must be serialized dictionaries")
        parsed_references = tuple(EvidenceReference.from_dict(value) for value in self.supplied_values)
        object.__setattr__(self, "supplied_values", tuple(value.to_dict() for value in parsed_references))
        if tuple(value.reference_id for value in parsed_references) != self.referenced_evidence_ids:
            raise ValueError("referenced evidence IDs must exactly match retained supplied values")
        expected_observations = tuple(
            value.source_record_id for value in parsed_references
            if value.reference_kind.value.startswith("m02_")
        )
        expected_diagnostics = tuple(
            value.source_record_id for value in parsed_references
            if value.reference_kind.value.startswith("m03_")
        )
        if expected_observations != self.referenced_observation_ids or expected_diagnostics != self.referenced_diagnostic_ids:
            raise ValueError("observation and diagnostic IDs must match retained supplied values")
        if self.manual_assertion is not None and tuple(self.manual_assertion.evidence_reference_ids) != self.referenced_evidence_ids:
            raise ValueError("manual assertion evidence IDs must match retained supplied values")
        if self.retained_threshold is not None:
            object.__setattr__(
                self, "retained_threshold", threshold_from_dict(self.retained_threshold).to_dict()
            )

    def to_dict(self) -> dict[str, object]:
        return {
            "schema": M04_SCHEMA_ID,
            "record_type": "criterion_evaluation",
            "record_id": self.record_id,
            "criterion_id": self.criterion_id,
            "criterion_version": self.criterion_version,
            "criterion_set_id": self.criterion_set_id,
            "criterion_set_version": self.criterion_set_version,
            "evaluation_context_id": self.evaluation_context_id,
            "referenced_evidence_ids": list(self.referenced_evidence_ids),
            "referenced_observation_ids": list(self.referenced_observation_ids),
            "referenced_diagnostic_ids": list(self.referenced_diagnostic_ids),
            "supplied_values": [dict(item) for item in self.supplied_values],
            "comparison_performed": self.comparison_performed,
            "retained_threshold": self.retained_threshold,
            "result": self.result.value,
            "reason": self.reason,
            "provenance": self.provenance.to_dict(),
            "source_locator": self.source_locator.to_dict(),
            "evaluation_method": self.evaluation_method.value,
            "manual_assertion": None if self.manual_assertion is None else self.manual_assertion.to_dict(),
            "dependency_record_ids": list(self.dependency_record_ids),
            "conflicting_record_ids": list(self.conflicting_record_ids),
            "qualifications": list(self.qualifications),
            "review_context": self.review_context,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> CriterionEvaluationRecord:
        from .screening_contexts import EvidenceReference
        from .screening_criteria import threshold_from_dict

        fields = {
            "schema", "record_type", "record_id", "criterion_id", "criterion_version",
            "criterion_set_id", "criterion_set_version", "evaluation_context_id",
            "referenced_evidence_ids", "referenced_observation_ids",
            "referenced_diagnostic_ids", "supplied_values", "comparison_performed",
            "retained_threshold", "result", "reason", "provenance", "source_locator",
            "evaluation_method", "manual_assertion", "dependency_record_ids",
            "conflicting_record_ids", "qualifications", "review_context",
        }
        _strict(data, fields)
        if data["schema"] != M04_SCHEMA_ID or data["record_type"] != "criterion_evaluation":
            raise ValueError("invalid M04 criterion-evaluation header")
        list_fields = (
            "referenced_evidence_ids", "referenced_observation_ids",
            "referenced_diagnostic_ids", "dependency_record_ids",
            "conflicting_record_ids", "qualifications",
        )
        if any(not isinstance(data[field], list) or not all(isinstance(item, str) for item in data[field]) for field in list_fields):
            raise TypeError("criterion outcome reference lists are malformed")
        supplied = data["supplied_values"]
        if not isinstance(supplied, list) or not all(isinstance(item, dict) for item in supplied):
            raise TypeError("supplied_values must be an object list")
        for field in ("criterion_version", "criterion_set_version"):
            if isinstance(data[field], bool) or not isinstance(data[field], int):
                raise TypeError(f"{field} must be an integer")
        threshold = data["retained_threshold"]
        if threshold is not None and not isinstance(threshold, dict):
            raise TypeError("retained_threshold must be an object or null")
        parsed_values = tuple(EvidenceReference.from_dict(item).to_dict() for item in supplied)
        parsed_threshold = None if threshold is None else threshold_from_dict(threshold).to_dict()
        return cls(
            str(data["record_id"]), str(data["criterion_id"]), data["criterion_version"],
            str(data["criterion_set_id"]), data["criterion_set_version"],
            str(data["evaluation_context_id"]), tuple(data["referenced_evidence_ids"]),
            tuple(data["referenced_observation_ids"]), tuple(data["referenced_diagnostic_ids"]),
            parsed_values, str(data["comparison_performed"]),
            parsed_threshold, CriterionOutcomeStatus(str(data["result"])),
            str(data["reason"]), Provenance.from_dict(data["provenance"]),
            SourceLocator.from_dict(data["source_locator"]), EvaluationMethod(str(data["evaluation_method"])),
            None if data["manual_assertion"] is None else ManualAssertionDetails.from_dict(data["manual_assertion"]),
            tuple(data["dependency_record_ids"]), tuple(data["conflicting_record_ids"]),
            tuple(data["qualifications"]), str(data["review_context"]),
        )


class CriterionSetSummary(str, Enum):
    """Mechanical summary of retained mandatory outcomes only."""

    ALL_MANDATORY_RECORDED_PASSES = "all_mandatory_recorded_passes"
    MANDATORY_FAILURE_RECORDED = "mandatory_failure_recorded"
    MANDATORY_INDETERMINATE = "mandatory_indeterminate"
    MANDATORY_NOT_EVALUATED = "mandatory_not_evaluated"
    SET_INACTIVE_OR_INVALID = "set_inactive_or_invalid"
    INCONSISTENT_CRITERION_VERSIONS = "inconsistent_criterion_versions"


@dataclass(frozen=True, slots=True)
class OutcomeCounts:
    """Descriptive counts that must not be used to compare candidates."""

    passed: int
    failed: int
    indeterminate: int
    unevaluated: int
    other: int

    def __post_init__(self) -> None:
        if any(isinstance(value, bool) or not isinstance(value, int) or value < 0 for value in (self.passed, self.failed, self.indeterminate, self.unevaluated, self.other)):
            raise ValueError("outcome counts must be non-negative integers")

    def to_dict(self) -> dict[str, int]:
        return {name: getattr(self, name) for name in ("passed", "failed", "indeterminate", "unevaluated", "other")}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> OutcomeCounts:
        fields = {"passed", "failed", "indeterminate", "unevaluated", "other"}
        _strict(data, fields)
        if any(isinstance(data[field], bool) or not isinstance(data[field], int) for field in fields):
            raise TypeError("outcome counts must be integers")
        return cls(*(data[name] for name in ("passed", "failed", "indeterminate", "unevaluated", "other")))


@dataclass(frozen=True, slots=True)
class CriterionSetOutcomeRecord:
    """Descriptive set summary without ranking, suitability, or safety semantics."""

    record_id: str
    criterion_set_id: str
    criterion_set_version: int
    evaluation_context_id: str
    criterion_evaluation_ids: tuple[str, ...]
    summary: CriterionSetSummary
    counts: OutcomeCounts
    reason: str
    non_implication_statement: str
    provenance: Provenance

    def __post_init__(self) -> None:
        for value, name in (
            (self.record_id, "record_id"), (self.criterion_set_id, "criterion_set_id"),
            (self.evaluation_context_id, "evaluation_context_id"), (self.reason, "reason"),
            (self.non_implication_statement, "non_implication_statement"),
        ):
            _text(value, name)
        if isinstance(self.criterion_set_version, bool) or not isinstance(self.criterion_set_version, int) or self.criterion_set_version <= 0:
            raise ValueError("set outcome requires a positive criterion-set version")
        object.__setattr__(self, "summary", CriterionSetSummary(self.summary))
        if len(self.criterion_evaluation_ids) != len(set(self.criterion_evaluation_ids)):
            raise ValueError("criterion evaluation IDs must be unique")
        if sum(self.counts.to_dict().values()) != len(self.criterion_evaluation_ids):
            raise ValueError("descriptive counts must equal retained criterion evaluations")
        if "does not establish" not in self.non_implication_statement.casefold():
            raise ValueError("set outcome must state what a positive summary does not establish")

    def to_dict(self) -> dict[str, object]:
        return {
            "schema": M04_SCHEMA_ID, "record_type": "criterion_set_outcome",
            "record_id": self.record_id, "criterion_set_id": self.criterion_set_id,
            "criterion_set_version": self.criterion_set_version,
            "evaluation_context_id": self.evaluation_context_id,
            "criterion_evaluation_ids": list(self.criterion_evaluation_ids),
            "summary": self.summary.value, "counts": self.counts.to_dict(),
            "reason": self.reason, "non_implication_statement": self.non_implication_statement,
            "provenance": self.provenance.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> CriterionSetOutcomeRecord:
        fields = {
            "schema", "record_type", "record_id", "criterion_set_id",
            "criterion_set_version", "evaluation_context_id", "criterion_evaluation_ids",
            "summary", "counts", "reason", "non_implication_statement", "provenance",
        }
        _strict(data, fields)
        if data["schema"] != M04_SCHEMA_ID or data["record_type"] != "criterion_set_outcome":
            raise ValueError("invalid M04 criterion-set-outcome header")
        ids = data["criterion_evaluation_ids"]
        if not isinstance(ids, list) or not all(isinstance(item, str) for item in ids):
            raise TypeError("criterion_evaluation_ids must be a string list")
        version = data["criterion_set_version"]
        if isinstance(version, bool) or not isinstance(version, int):
            raise TypeError("criterion-set version must be an integer")
        return cls(
            str(data["record_id"]), str(data["criterion_set_id"]), version,
            str(data["evaluation_context_id"]), tuple(ids),
            CriterionSetSummary(str(data["summary"])), OutcomeCounts.from_dict(data["counts"]),
            str(data["reason"]), str(data["non_implication_statement"]),
            Provenance.from_dict(data["provenance"]),
        )
