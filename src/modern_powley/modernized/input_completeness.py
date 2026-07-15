"""Structured M03 completeness diagnostics with no input inference."""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from typing import Any, Mapping

from .input_requirements import (
    M03_SCHEMA_ID,
    InputBundle,
    InputCandidate,
    InputRequirement,
    RequirementKind,
    RequirementSet,
)
from .missing_values import MissingState
from .provenance import EvidenceClass, ModelMaturity, Provenance, ValueOrigin
from .units import Dimension


class CompletenessStatus(str, Enum):
    """Literal outcome for one declared input requirement."""

    SATISFIED = "satisfied"
    MISSING = "missing"
    EXPLICITLY_UNAVAILABLE = "explicitly_unavailable"
    WRONG_RECORD_TYPE = "wrong_record_type"
    WRONG_QUANTITY_DIMENSION = "wrong_quantity_dimension"
    INVALID_VALUE_DOMAIN = "invalid_value_domain"
    WRONG_CONTROLLED_CATEGORY = "wrong_controlled_category"
    MUTUALLY_INCONSISTENT = "mutually_inconsistent"
    CONFLICTING_SUPPLIED_VALUES = "conflicting_supplied_values"
    UNSUPPORTED_ALTERNATIVE = "unsupported_alternative"
    CONDITIONAL_CONTEXT_MISSING = "conditional_context_missing"
    NOT_APPLICABLE = "not_applicable"
    INDETERMINATE = "indeterminate"


@dataclass(frozen=True, slots=True)
class CompletenessDiagnostic:
    """One requirement outcome retaining all supplied candidate identities."""

    requirement_id: str
    semantic_input_id: str
    requirement_kind: RequirementKind
    status: CompletenessStatus
    supplied_candidate_ids: tuple[str, ...]
    supplied_record_ids: tuple[str, ...]
    expected_candidate_kinds: tuple[str, ...]
    actual_candidate_kinds: tuple[str, ...]
    expected_categories: tuple[str, ...]
    actual_categories: tuple[str, ...]
    expected_dimension: Dimension | None
    actual_dimensions: tuple[Dimension, ...]
    source_ids: tuple[str, ...]
    evidence_classes: tuple[EvidenceClass, ...]
    model_maturities: tuple[ModelMaturity, ...]
    missing_state: MissingState | None
    conditional_branch_id: str | None
    related_conflicting_fields: tuple[str, ...]
    explanation: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "requirement_kind", RequirementKind(self.requirement_kind))
        object.__setattr__(self, "status", CompletenessStatus(self.status))
        object.__setattr__(self, "evidence_classes", tuple(EvidenceClass(item) for item in self.evidence_classes))
        object.__setattr__(self, "model_maturities", tuple(ModelMaturity(item) for item in self.model_maturities))
        if self.expected_dimension is not None:
            object.__setattr__(self, "expected_dimension", Dimension(self.expected_dimension))
        object.__setattr__(self, "actual_dimensions", tuple(Dimension(item) for item in self.actual_dimensions))
        if self.missing_state is not None:
            object.__setattr__(self, "missing_state", MissingState(self.missing_state))
        if not self.requirement_id.strip() or not self.semantic_input_id.strip() or not self.explanation.strip():
            raise ValueError("diagnostic requirement identity and explanation are required")

    def to_dict(self) -> dict[str, object]:
        return {
            "requirement_id": self.requirement_id, "semantic_input_id": self.semantic_input_id,
            "requirement_kind": self.requirement_kind.value, "status": self.status.value,
            "supplied_candidate_ids": list(self.supplied_candidate_ids),
            "supplied_record_ids": list(self.supplied_record_ids),
            "expected_candidate_kinds": list(self.expected_candidate_kinds),
            "actual_candidate_kinds": list(self.actual_candidate_kinds),
            "expected_categories": list(self.expected_categories),
            "actual_categories": list(self.actual_categories),
            "expected_dimension": None if self.expected_dimension is None else self.expected_dimension.value,
            "actual_dimensions": [item.value for item in self.actual_dimensions],
            "source_ids": list(self.source_ids),
            "evidence_classes": [item.value for item in self.evidence_classes],
            "model_maturities": [item.value for item in self.model_maturities],
            "missing_state": None if self.missing_state is None else self.missing_state.value,
            "conditional_branch_id": self.conditional_branch_id,
            "related_conflicting_fields": list(self.related_conflicting_fields),
            "explanation": self.explanation,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> CompletenessDiagnostic:
        fields = {"requirement_id", "semantic_input_id", "requirement_kind", "status", "supplied_candidate_ids", "supplied_record_ids", "expected_candidate_kinds", "actual_candidate_kinds", "expected_categories", "actual_categories", "expected_dimension", "actual_dimensions", "source_ids", "evidence_classes", "model_maturities", "missing_state", "conditional_branch_id", "related_conflicting_fields", "explanation"}
        if set(data) != fields:
            raise ValueError("malformed completeness diagnostic fields")
        list_fields = ("supplied_candidate_ids", "supplied_record_ids", "expected_candidate_kinds", "actual_candidate_kinds", "expected_categories", "actual_categories", "actual_dimensions", "source_ids", "evidence_classes", "model_maturities", "related_conflicting_fields")
        if any(not isinstance(data[field], list) or not all(isinstance(item, str) for item in data[field]) for field in list_fields):
            raise TypeError("completeness diagnostic list fields are malformed")
        dimension, missing, branch = data["expected_dimension"], data["missing_state"], data["conditional_branch_id"]
        return cls(
            str(data["requirement_id"]), str(data["semantic_input_id"]),
            RequirementKind(str(data["requirement_kind"])), CompletenessStatus(str(data["status"])),
            tuple(data["supplied_candidate_ids"]), tuple(data["supplied_record_ids"]),
            tuple(data["expected_candidate_kinds"]), tuple(data["actual_candidate_kinds"]),
            tuple(data["expected_categories"]), tuple(data["actual_categories"]),
            None if dimension is None else Dimension(str(dimension)),
            tuple(Dimension(item) for item in data["actual_dimensions"]),
            tuple(data["source_ids"]), tuple(EvidenceClass(item) for item in data["evidence_classes"]),
            tuple(ModelMaturity(item) for item in data["model_maturities"]),
            None if missing is None else MissingState(str(missing)),
            None if branch is None else str(branch), tuple(data["related_conflicting_fields"]),
            str(data["explanation"]),
        )


@dataclass(frozen=True, slots=True)
class CompletenessEvaluation:
    """Full diagnostic result; its Boolean means only declared conditions passed."""

    record_id: str
    requirement_set_id: str
    requirement_set_version: int
    input_bundle_id: str
    selected_branch_id: str | None
    all_declared_conditions_satisfied: bool
    diagnostics: tuple[CompletenessDiagnostic, ...]
    provenance: Provenance

    def __post_init__(self) -> None:
        if not self.record_id.strip() or not self.requirement_set_id.strip() or not self.input_bundle_id.strip():
            raise ValueError("completeness evaluation identities are required")
        if self.requirement_set_version <= 0 or not self.diagnostics:
            raise ValueError("evaluation requires a positive set version and diagnostics")
        pass_statuses = {CompletenessStatus.SATISFIED, CompletenessStatus.NOT_APPLICABLE}
        expected = all(item.status in pass_statuses for item in self.diagnostics)
        if self.all_declared_conditions_satisfied is not expected:
            raise ValueError("completeness Boolean must exactly reflect retained diagnostics")

    def to_dict(self) -> dict[str, object]:
        return {
            "schema": M03_SCHEMA_ID, "record_type": "completeness_evaluation", "record_id": self.record_id,
            "requirement_set_id": self.requirement_set_id,
            "requirement_set_version": self.requirement_set_version,
            "input_bundle_id": self.input_bundle_id, "selected_branch_id": self.selected_branch_id,
            "all_declared_conditions_satisfied": self.all_declared_conditions_satisfied,
            "diagnostics": [item.to_dict() for item in self.diagnostics],
            "provenance": self.provenance.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> CompletenessEvaluation:
        fields = {"schema", "record_type", "record_id", "requirement_set_id", "requirement_set_version", "input_bundle_id", "selected_branch_id", "all_declared_conditions_satisfied", "diagnostics", "provenance"}
        if set(data) != fields or data.get("schema") != M03_SCHEMA_ID or data.get("record_type") != "completeness_evaluation":
            raise ValueError("malformed M03 completeness-evaluation record")
        diagnostics = data["diagnostics"]
        if not isinstance(diagnostics, list) or not isinstance(data["all_declared_conditions_satisfied"], bool):
            raise TypeError("completeness diagnostics or summary are malformed")
        version = data["requirement_set_version"]
        if isinstance(version, bool) or not isinstance(version, int):
            raise TypeError("requirement-set version must be an integer")
        branch = data["selected_branch_id"]
        return cls(
            str(data["record_id"]), str(data["requirement_set_id"]), version,
            str(data["input_bundle_id"]), None if branch is None else str(branch),
            data["all_declared_conditions_satisfied"],
            tuple(CompletenessDiagnostic.from_dict(item) for item in diagnostics),
            Provenance.from_dict(data["provenance"]),
        )


def _details(requirement: InputRequirement, candidates: tuple[InputCandidate, ...], status: CompletenessStatus, explanation: str, *, missing_state: MissingState | None = None) -> CompletenessDiagnostic:
    return CompletenessDiagnostic(
        requirement.requirement_id, requirement.semantic_input_id, requirement.kind, status,
        tuple(item.candidate_id for item in candidates), tuple(item.source_record_id for item in candidates),
        tuple(item.value for item in requirement.accepted_candidate_kinds),
        tuple(item.candidate_kind.value for item in candidates),
        requirement.allowed_categories, tuple(item.category for item in candidates if item.category is not None),
        requirement.expected_dimension, tuple(item.quantity.dimension for item in candidates if item.quantity is not None),
        tuple(item.provenance.source_id for item in candidates),
        tuple(item.provenance.evidence_class for item in candidates),
        tuple(item.provenance.model_maturity for item in candidates),
        missing_state, requirement.conditional_branch_id,
        tuple(item.semantic_input_id for item in candidates) if len(candidates) > 1 else (), explanation,
    )


def _active_branch(requirement_set: RequirementSet, bundle: InputBundle) -> tuple[str | None, CompletenessStatus | None, str]:
    if not requirement_set.branches:
        return None, None, "requirement set has no conditional branch"
    candidates = tuple(item for item in bundle.candidates if item.semantic_input_id == requirement_set.branch_selector_input_id)
    if not candidates:
        return None, CompletenessStatus.CONDITIONAL_CONTEXT_MISSING, "explicit branch selector is missing"
    if len(candidates) > 1:
        return None, CompletenessStatus.MUTUALLY_INCONSISTENT, "multiple explicit geometry branches were supplied"
    candidate = candidates[0]
    if candidate.missing_state is not None:
        return None, CompletenessStatus.CONDITIONAL_CONTEXT_MISSING, "geometry branch is explicitly unavailable"
    if candidate.category is None:
        return None, CompletenessStatus.WRONG_CONTROLLED_CATEGORY, "branch selector is not a controlled category"
    matches = [item.branch_id for item in requirement_set.branches if item.selector_value == candidate.category]
    if not matches:
        return None, CompletenessStatus.UNSUPPORTED_ALTERNATIVE, f"unsupported explicit geometry branch {candidate.category!r}"
    return matches[0], None, "explicit branch selected"


def evaluate_input_completeness(requirement_set: RequirementSet, bundle: InputBundle, *, record_id: str) -> CompletenessEvaluation:
    """Inspect explicit candidates against one requirement set without inference."""

    selected_branch, branch_error, branch_explanation = _active_branch(requirement_set, bundle)
    diagnostics: list[CompletenessDiagnostic] = []
    for requirement in requirement_set.requirements:
        candidates = tuple(item for item in bundle.candidates if item.semantic_input_id == requirement.semantic_input_id)
        if requirement.kind is RequirementKind.CONDITIONAL:
            if branch_error is not None:
                diagnostics.append(_details(requirement, candidates, CompletenessStatus.CONDITIONAL_CONTEXT_MISSING, branch_explanation))
                continue
            if requirement.conditional_branch_id != selected_branch:
                diagnostics.append(_details(requirement, candidates, CompletenessStatus.NOT_APPLICABLE, "requirement belongs to an inactive explicit branch"))
                continue
        if not candidates:
            status = CompletenessStatus.NOT_APPLICABLE if requirement.kind is RequirementKind.OPTIONAL else CompletenessStatus.MISSING
            diagnostics.append(_details(requirement, (), status, "optional input was not supplied" if status is CompletenessStatus.NOT_APPLICABLE else "required explicit input was not supplied"))
            continue
        if len(candidates) > 1 and not requirement.allow_multiple:
            status = CompletenessStatus.MUTUALLY_INCONSISTENT if requirement.semantic_input_id == requirement_set.branch_selector_input_id else CompletenessStatus.CONFLICTING_SUPPLIED_VALUES
            diagnostics.append(_details(requirement, candidates, status, "multiple supplied candidates cannot satisfy this single-valued requirement"))
            continue
        candidate = candidates[0]
        if candidate.missing_state is not None:
            diagnostics.append(_details(requirement, candidates, CompletenessStatus.EXPLICITLY_UNAVAILABLE, candidate.explanation, missing_state=candidate.missing_state))
            continue
        if candidate.candidate_kind not in requirement.accepted_candidate_kinds:
            diagnostics.append(_details(requirement, candidates, CompletenessStatus.WRONG_RECORD_TYPE, "supplied record kind cannot substitute for the required kind"))
            continue
        if requirement.expected_dimension is not None:
            if candidate.quantity is None or candidate.quantity.dimension is not requirement.expected_dimension:
                diagnostics.append(_details(requirement, candidates, CompletenessStatus.WRONG_QUANTITY_DIMENSION, "supplied quantity dimension does not match the declared requirement"))
                continue
            if requirement.require_positive_quantity and candidate.quantity.si_value <= 0:
                diagnostics.append(_details(requirement, candidates, CompletenessStatus.INVALID_VALUE_DOMAIN, "existing M01 operation requires a positive quantity"))
                continue
        if requirement.allowed_categories:
            if candidate.category not in requirement.allowed_categories:
                status = CompletenessStatus.UNSUPPORTED_ALTERNATIVE if requirement.semantic_input_id == requirement_set.branch_selector_input_id else CompletenessStatus.WRONG_CONTROLLED_CATEGORY
                diagnostics.append(_details(requirement, candidates, status, "literal controlled category is not admitted by this requirement"))
                continue
        diagnostics.append(_details(requirement, candidates, CompletenessStatus.SATISFIED, "explicit supplied input satisfies the declared requirement"))

    if requirement_set.requirement_set_id == "geometric_usable_powder_space":
        gross = tuple(item for item in bundle.candidates if item.semantic_input_id == "gross_primer_pocket_treatment")
        target = tuple(item for item in bundle.candidates if item.semantic_input_id == "target_primer_pocket_treatment")
        correction = tuple(item for item in bundle.candidates if item.semantic_input_id == "primer_pocket_correction")
        correction_index = next(index for index, item in enumerate(diagnostics) if item.requirement_id == "primer_pocket_correction")
        current = diagnostics[correction_index]
        if len(gross) == len(target) == 1 and gross[0].category is not None and target[0].category is not None:
            if "unknown" in {gross[0].category, target[0].category}:
                diagnostics[correction_index] = replace(current, status=CompletenessStatus.INDETERMINATE, explanation="primer-pocket basis is explicitly unknown, so correction applicability cannot be determined")
            elif gross[0].category != target[0].category and not correction:
                diagnostics[correction_index] = replace(current, status=CompletenessStatus.MISSING, explanation=f"primer-pocket basis mismatch ({gross[0].category} versus {target[0].category}) requires an explicit correction volume")
            elif gross[0].category == target[0].category and correction:
                diagnostics[correction_index] = replace(current, status=CompletenessStatus.MUTUALLY_INCONSISTENT, explanation="primer-pocket correction was supplied although declared source and target bases are identical")
            elif gross[0].category != target[0].category and current.status is CompletenessStatus.SATISFIED:
                diagnostics[correction_index] = replace(current, explanation=f"explicit correction accompanies primer-pocket basis mismatch ({gross[0].category} versus {target[0].category})")

    if requirement_set.requirement_set_id == "seated_projectile_displacement" and selected_branch in {"partial_boat_tail", "full_boat_tail"}:
        def one_quantity(name: str):
            values = tuple(item for item in bundle.candidates if item.semantic_input_id == name and item.quantity is not None)
            return values[0].quantity if len(values) == 1 else None

        intrusion = one_quantity("seated_intrusion")
        tail_length = one_quantity("boat_tail_axial_length")
        shank = one_quantity("shank_diameter")
        tail_base = one_quantity("boat_tail_base_diameter")
        if intrusion is not None and tail_length is not None and intrusion.dimension is tail_length.dimension:
            inconsistent = (selected_branch == "partial_boat_tail" and intrusion.si_value > tail_length.si_value) or (selected_branch == "full_boat_tail" and intrusion.si_value < tail_length.si_value)
            if inconsistent:
                requirement_id = "partial_intrusion" if selected_branch == "partial_boat_tail" else "full_intrusion"
                index = next(index for index, item in enumerate(diagnostics) if item.requirement_id == requirement_id)
                diagnostics[index] = replace(diagnostics[index], status=CompletenessStatus.MUTUALLY_INCONSISTENT, explanation="explicit intrusion and tail length contradict the selected partial/full boat-tail branch")
        if shank is not None and tail_base is not None and shank.dimension is tail_base.dimension and tail_base.si_value > shank.si_value:
            requirement_id = "partial_tail_base_diameter" if selected_branch == "partial_boat_tail" else "full_tail_base_diameter"
            index = next(index for index, item in enumerate(diagnostics) if item.requirement_id == requirement_id)
            diagnostics[index] = replace(diagnostics[index], status=CompletenessStatus.INVALID_VALUE_DOMAIN, explanation="existing M01 boat-tail geometry rejects a tail-base diameter larger than the shank diameter")
    passed = all(item.status in {CompletenessStatus.SATISFIED, CompletenessStatus.NOT_APPLICABLE} for item in diagnostics)
    provenance = Provenance(
        EvidenceClass.DERIVED_QUANTITY, ValueOrigin.DERIVED, "SRC-M03-DESIGN",
        ModelMaturity.PROMOTED_MODERN, "M03-DIAG-INPUT-COMPLETENESS",
        (requirement_set.record_id, bundle.record_id),
        "Diagnostic completeness only; no physical-validity or readiness claim.",
    )
    return CompletenessEvaluation(record_id, requirement_set.requirement_set_id, requirement_set.version, bundle.record_id, selected_branch, passed, tuple(diagnostics), provenance)
