"""Named M03 requirement sets and explicit input candidates."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from .missing_values import MissingState
from .provenance import EvidenceClass, ModelMaturity, Provenance, ValueOrigin
from .units import Dimension, Quantity

M03_SCHEMA_ID = "modern_powley.m03.v1"


class RequirementKind(str, Enum):
    """Whether an input is always, optionally, or conditionally inspected."""

    REQUIRED = "required"
    OPTIONAL = "optional"
    CONDITIONAL = "conditional"


class InputCandidateKind(str, Enum):
    """Semantic record kinds kept distinct during completeness evaluation."""

    PHYSICAL_VALUE = "physical_value"
    GROSS_CASE_CAPACITY = "gross_case_capacity"
    MEASURED_USABLE_CAPACITY = "measured_usable_capacity"
    ESTIMATED_USABLE_CAPACITY = "estimated_usable_capacity"
    PRIMER_POCKET_CAPACITY = "primer_pocket_capacity"
    CONTROLLED_CATEGORY = "controlled_category"
    EXPLICIT_IDENTIFIER = "explicit_identifier"


def _required_text(value: str, name: str) -> str:
    value = str(value).strip()
    if not value:
        raise ValueError(f"{name} is required")
    return value


def _strict(data: Mapping[str, Any], fields: set[str]) -> None:
    if set(data) != fields:
        raise ValueError(f"expected fields {sorted(fields)}, got {sorted(data)}")


@dataclass(frozen=True, slots=True)
class InputRequirement:
    """One explicit input condition in a named operation requirement set."""

    requirement_id: str
    semantic_input_id: str
    kind: RequirementKind
    description: str
    accepted_candidate_kinds: tuple[InputCandidateKind, ...]
    expected_dimension: Dimension | None = None
    allowed_categories: tuple[str, ...] = ()
    conditional_branch_id: str | None = None
    require_positive_quantity: bool = False
    allow_multiple: bool = False

    def __post_init__(self) -> None:
        _required_text(self.requirement_id, "requirement_id")
        _required_text(self.semantic_input_id, "semantic_input_id")
        _required_text(self.description, "requirement description")
        object.__setattr__(self, "kind", RequirementKind(self.kind))
        kinds = tuple(InputCandidateKind(item) for item in self.accepted_candidate_kinds)
        if not kinds or len(kinds) != len(set(kinds)):
            raise ValueError("accepted candidate kinds must be nonempty and unique")
        object.__setattr__(self, "accepted_candidate_kinds", kinds)
        if self.expected_dimension is not None:
            object.__setattr__(self, "expected_dimension", Dimension(self.expected_dimension))
        if any(not item.strip() for item in self.allowed_categories):
            raise ValueError("allowed categories must be nonblank")
        if self.kind is RequirementKind.CONDITIONAL:
            _required_text(self.conditional_branch_id or "", "conditional_branch_id")
        elif self.conditional_branch_id is not None:
            raise ValueError("only conditional requirements may identify a branch")
        if self.allowed_categories and InputCandidateKind.CONTROLLED_CATEGORY not in kinds:
            raise ValueError("allowed categories require the controlled-category candidate kind")

    def to_dict(self) -> dict[str, object]:
        return {
            "requirement_id": self.requirement_id,
            "semantic_input_id": self.semantic_input_id,
            "kind": self.kind.value,
            "description": self.description,
            "accepted_candidate_kinds": [item.value for item in self.accepted_candidate_kinds],
            "expected_dimension": None if self.expected_dimension is None else self.expected_dimension.value,
            "allowed_categories": list(self.allowed_categories),
            "conditional_branch_id": self.conditional_branch_id,
            "require_positive_quantity": self.require_positive_quantity,
            "allow_multiple": self.allow_multiple,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> InputRequirement:
        fields = {"requirement_id", "semantic_input_id", "kind", "description", "accepted_candidate_kinds", "expected_dimension", "allowed_categories", "conditional_branch_id", "require_positive_quantity", "allow_multiple"}
        _strict(data, fields)
        kinds, categories = data["accepted_candidate_kinds"], data["allowed_categories"]
        if not isinstance(kinds, list) or not isinstance(categories, list):
            raise TypeError("requirement candidate kinds and categories must be lists")
        if not all(isinstance(item, str) for item in kinds + categories):
            raise TypeError("requirement candidate kinds and categories must contain strings")
        if not isinstance(data["require_positive_quantity"], bool) or not isinstance(data["allow_multiple"], bool):
            raise TypeError("requirement Boolean fields are malformed")
        dimension = data["expected_dimension"]
        branch = data["conditional_branch_id"]
        return cls(
            str(data["requirement_id"]), str(data["semantic_input_id"]),
            RequirementKind(str(data["kind"])), str(data["description"]),
            tuple(InputCandidateKind(item) for item in kinds),
            None if dimension is None else Dimension(str(dimension)), tuple(categories),
            None if branch is None else str(branch), data["require_positive_quantity"],
            data["allow_multiple"],
        )


@dataclass(frozen=True, slots=True)
class ConditionalBranch:
    """One explicit branch selected by a literal controlled-category value."""

    branch_id: str
    selector_value: str
    description: str

    def __post_init__(self) -> None:
        _required_text(self.branch_id, "branch_id")
        _required_text(self.selector_value, "selector_value")
        _required_text(self.description, "branch description")

    def to_dict(self) -> dict[str, object]:
        return {"branch_id": self.branch_id, "selector_value": self.selector_value, "description": self.description}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> ConditionalBranch:
        _strict(data, {"branch_id", "selector_value", "description"})
        return cls(str(data["branch_id"]), str(data["selector_value"]), str(data["description"]))


@dataclass(frozen=True, slots=True)
class RequirementSet:
    """Immutable versioned requirements for one already implemented M01 operation."""

    record_id: str
    requirement_set_id: str
    version: int
    operation_id: str
    operation_name: str
    description: str
    requirements: tuple[InputRequirement, ...]
    branch_selector_input_id: str | None
    branches: tuple[ConditionalBranch, ...]
    provenance: Provenance
    model_maturity: ModelMaturity
    operation_already_exists: bool = True

    def __post_init__(self) -> None:
        for value, name in ((self.record_id, "record_id"), (self.requirement_set_id, "requirement_set_id"), (self.operation_id, "operation_id"), (self.operation_name, "operation_name"), (self.description, "description")):
            _required_text(value, name)
        if self.version <= 0:
            raise ValueError("requirement-set version must be positive")
        if not self.requirements:
            raise ValueError("requirement set must contain requirements")
        object.__setattr__(self, "model_maturity", ModelMaturity(self.model_maturity))
        if self.provenance.model_maturity is not self.model_maturity:
            raise ValueError("requirement-set maturity must match its provenance")
        ids = [item.requirement_id for item in self.requirements]
        if len(ids) != len(set(ids)):
            raise ValueError("requirement IDs must be unique")
        branch_ids = [item.branch_id for item in self.branches]
        selector_values = [item.selector_value for item in self.branches]
        if len(branch_ids) != len(set(branch_ids)) or len(selector_values) != len(set(selector_values)):
            raise ValueError("branch IDs and selector values must be unique")
        conditional_ids = {item.conditional_branch_id for item in self.requirements if item.kind is RequirementKind.CONDITIONAL}
        if self.branches:
            _required_text(self.branch_selector_input_id or "", "branch_selector_input_id")
            if conditional_ids - set(branch_ids):
                raise ValueError("conditional requirement references an undeclared branch")
        elif self.branch_selector_input_id is not None or conditional_ids:
            raise ValueError("branch selector and conditional requirements require declared branches")
        if not self.operation_already_exists:
            raise ValueError("production requirement sets may describe only existing operations")

    def to_dict(self) -> dict[str, object]:
        return {
            "schema": M03_SCHEMA_ID, "record_type": "requirement_set", "record_id": self.record_id,
            "requirement_set_id": self.requirement_set_id, "version": self.version,
            "operation_id": self.operation_id, "operation_name": self.operation_name,
            "description": self.description,
            "requirements": [item.to_dict() for item in self.requirements],
            "branch_selector_input_id": self.branch_selector_input_id,
            "branches": [item.to_dict() for item in self.branches],
            "provenance": self.provenance.to_dict(), "model_maturity": self.model_maturity.value,
            "operation_already_exists": self.operation_already_exists,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> RequirementSet:
        fields = {"schema", "record_type", "record_id", "requirement_set_id", "version", "operation_id", "operation_name", "description", "requirements", "branch_selector_input_id", "branches", "provenance", "model_maturity", "operation_already_exists"}
        _strict(data, fields)
        if data["schema"] != M03_SCHEMA_ID or data["record_type"] != "requirement_set":
            raise ValueError("invalid M03 requirement-set header")
        requirements, branches = data["requirements"], data["branches"]
        if not isinstance(requirements, list) or not isinstance(branches, list):
            raise TypeError("requirements and branches must be lists")
        if isinstance(data["version"], bool) or not isinstance(data["version"], int):
            raise TypeError("requirement-set version must be an integer")
        if not isinstance(data["operation_already_exists"], bool):
            raise TypeError("operation_already_exists must be Boolean")
        selector = data["branch_selector_input_id"]
        return cls(
            str(data["record_id"]), str(data["requirement_set_id"]), data["version"],
            str(data["operation_id"]), str(data["operation_name"]), str(data["description"]),
            tuple(InputRequirement.from_dict(item) for item in requirements),
            None if selector is None else str(selector),
            tuple(ConditionalBranch.from_dict(item) for item in branches),
            Provenance.from_dict(data["provenance"]), ModelMaturity(str(data["model_maturity"])),
            data["operation_already_exists"],
        )


@dataclass(frozen=True, slots=True)
class InputCandidate:
    """One explicitly supplied candidate; no value is inferred from its identity."""

    candidate_id: str
    semantic_input_id: str
    candidate_kind: InputCandidateKind
    source_record_id: str
    provenance: Provenance
    quantity: Quantity | None = None
    category: str | None = None
    missing_state: MissingState | None = None
    explanation: str = ""

    def __post_init__(self) -> None:
        for value, name in ((self.candidate_id, "candidate_id"), (self.semantic_input_id, "semantic_input_id"), (self.source_record_id, "source_record_id")):
            _required_text(value, name)
        object.__setattr__(self, "candidate_kind", InputCandidateKind(self.candidate_kind))
        if self.missing_state is not None:
            object.__setattr__(self, "missing_state", MissingState(self.missing_state))
        present = sum(value is not None for value in (self.quantity, self.category, self.missing_state))
        if present != 1:
            raise ValueError("input candidate requires exactly one of quantity, category, or missing_state")
        if self.quantity is not None and self.candidate_kind in {InputCandidateKind.CONTROLLED_CATEGORY, InputCandidateKind.EXPLICIT_IDENTIFIER}:
            raise ValueError("categorical and identifier candidates cannot contain quantities")
        if self.category is not None:
            _required_text(self.category, "candidate category")
            if self.candidate_kind not in {InputCandidateKind.CONTROLLED_CATEGORY, InputCandidateKind.EXPLICIT_IDENTIFIER}:
                raise ValueError("only categorical and identifier candidates contain category text")
        if self.missing_state is not None and not self.explanation.strip():
            raise ValueError("explicitly missing input requires an explanation")

    def to_dict(self) -> dict[str, object]:
        return {
            "candidate_id": self.candidate_id, "semantic_input_id": self.semantic_input_id,
            "candidate_kind": self.candidate_kind.value, "source_record_id": self.source_record_id,
            "provenance": self.provenance.to_dict(),
            "quantity": None if self.quantity is None else self.quantity.to_dict(),
            "category": self.category,
            "missing_state": None if self.missing_state is None else self.missing_state.value,
            "explanation": self.explanation,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> InputCandidate:
        fields = {"candidate_id", "semantic_input_id", "candidate_kind", "source_record_id", "provenance", "quantity", "category", "missing_state", "explanation"}
        _strict(data, fields)
        return cls(
            str(data["candidate_id"]), str(data["semantic_input_id"]),
            InputCandidateKind(str(data["candidate_kind"])), str(data["source_record_id"]),
            Provenance.from_dict(data["provenance"]),
            None if data["quantity"] is None else Quantity.from_dict(data["quantity"]),
            None if data["category"] is None else str(data["category"]),
            None if data["missing_state"] is None else MissingState(str(data["missing_state"])),
            str(data["explanation"]),
        )


@dataclass(frozen=True, slots=True)
class InputBundle:
    """Immutable candidates supplied for one completeness evaluation."""

    record_id: str
    candidates: tuple[InputCandidate, ...]
    provenance: Provenance
    notes: str = ""

    def __post_init__(self) -> None:
        _required_text(self.record_id, "input-bundle record_id")
        ids = [item.candidate_id for item in self.candidates]
        if len(ids) != len(set(ids)):
            raise ValueError("input candidate IDs must be unique")

    def to_dict(self) -> dict[str, object]:
        return {"schema": M03_SCHEMA_ID, "record_type": "input_bundle", "record_id": self.record_id, "candidates": [item.to_dict() for item in self.candidates], "provenance": self.provenance.to_dict(), "notes": self.notes}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> InputBundle:
        _strict(data, {"schema", "record_type", "record_id", "candidates", "provenance", "notes"})
        if data["schema"] != M03_SCHEMA_ID or data["record_type"] != "input_bundle":
            raise ValueError("invalid M03 input-bundle header")
        candidates = data["candidates"]
        if not isinstance(candidates, list):
            raise TypeError("input candidates must be a list")
        return cls(str(data["record_id"]), tuple(InputCandidate.from_dict(item) for item in candidates), Provenance.from_dict(data["provenance"]), str(data["notes"]))


def m03_design_provenance() -> Provenance:
    """Return the declared project-design authority for production M03 sets."""

    return Provenance(EvidenceClass.DERIVED_QUANTITY, ValueOrigin.ASSUMED, "SRC-M03-DESIGN", ModelMaturity.PROMOTED_MODERN, notes="M03 diagnostic design authority; not physical evidence")


def _req(requirement_id: str, semantic_input_id: str, dimension: Dimension, *, kind: RequirementKind = RequirementKind.REQUIRED, branch: str | None = None, candidate_kinds: tuple[InputCandidateKind, ...] = (InputCandidateKind.PHYSICAL_VALUE,)) -> InputRequirement:
    return InputRequirement(requirement_id, semantic_input_id, kind, f"Explicit {semantic_input_id} required by the existing M01 operation", candidate_kinds, dimension, (), branch, True)


def production_requirement_sets() -> tuple[RequirementSet, ...]:
    """Return only requirement sets for existing M01 geometry and ratio operations."""

    provenance = m03_design_provenance()
    promoted = ModelMaturity.PROMOTED_MODERN
    simple = (
        RequirementSet("M03-RS-CIRCLE-AREA-V1", "circle_area", 1, "M01-GEO-CIRCLE-AREA", "Circle area", "Explicit diameter for the existing M01 circle-area operation.", (_req("diameter", "diameter", Dimension.LENGTH),), None, (), provenance, promoted),
        RequirementSet("M03-RS-CYLINDER-VOLUME-V1", "cylinder_volume", 1, "M01-GEO-CYLINDER-VOLUME", "Cylinder volume", "Explicit diameter and axial length for the existing M01 cylinder-volume operation.", (_req("diameter", "diameter", Dimension.LENGTH), _req("axial_length", "axial_length", Dimension.LENGTH)), None, (), provenance, promoted),
        RequirementSet("M03-RS-FRUSTUM-VOLUME-V1", "conical_frustum_volume", 1, "M01-GEO-FRUSTUM-VOLUME", "Conical-frustum volume", "Explicit end diameters and axial length for the existing M01 frustum operation.", (_req("large_diameter", "large_diameter", Dimension.LENGTH), _req("small_diameter", "small_diameter", Dimension.LENGTH), _req("axial_length", "axial_length", Dimension.LENGTH)), None, (), provenance, promoted),
        RequirementSet("M03-RS-BARREL-SWEPT-VOLUME-V1", "barrel_swept_volume", 1, "M01-GEO-BARREL-SWEPT-VOLUME", "Barrel swept volume", "Explicit bore area and projectile travel for the existing M01 barrel-volume operation.", (_req("bore_area", "bore_area", Dimension.AREA), _req("projectile_travel", "projectile_travel", Dimension.LENGTH)), None, (), provenance, promoted),
        RequirementSet("M03-RS-BARREL-VOLUME-RATIO-V1", "barrel_volume_ratio", 1, "M01-GEO-BARREL-VOLUME-RATIO", "Barrel volume ratio", "Explicit powder-space and swept volumes for Vb/V0.", (_req("powder_space_volume", "powder_space_volume", Dimension.VOLUME), _req("barrel_swept_volume", "barrel_swept_volume", Dimension.VOLUME)), None, (), provenance, promoted),
        RequirementSet("M03-RS-TOTAL-EXPANSION-RATIO-V1", "total_expansion_ratio", 1, "M01-GEO-TOTAL-EXPANSION-RATIO", "Total expansion ratio", "Explicit powder-space and swept volumes for (V0+Vb)/V0.", (_req("powder_space_volume", "powder_space_volume", Dimension.VOLUME), _req("barrel_swept_volume", "barrel_swept_volume", Dimension.VOLUME)), None, (), provenance, promoted),
        RequirementSet("M03-RS-CAPACITY-COMPARISON-V1", "capacity_comparison", 1, "M01-GEO-CAPACITY-COMPARISON", "Measured/estimated capacity comparison", "Distinct measured and estimated usable-capacity records for the existing diagnostic comparison.", (_req("measured_usable_capacity", "measured_usable_capacity", Dimension.VOLUME, candidate_kinds=(InputCandidateKind.MEASURED_USABLE_CAPACITY,)), _req("estimated_usable_capacity", "estimated_usable_capacity", Dimension.VOLUME, candidate_kinds=(InputCandidateKind.ESTIMATED_USABLE_CAPACITY,))), None, (), provenance, promoted),
        RequirementSet(
            "M03-RS-USABLE-SPACE-ESTIMATE-V1", "geometric_usable_powder_space", 1,
            "M01-GEO-USABLE-SPACE-ESTIMATE", "Geometric usable-space estimate inputs",
            "Explicit gross capacity, displacement, primer-pocket bases, and any mathematically required correction for the existing M01 estimate.",
            (
                _req("gross_case_capacity", "gross_case_capacity", Dimension.VOLUME, candidate_kinds=(InputCandidateKind.GROSS_CASE_CAPACITY,)),
                _req("projectile_displacement", "projectile_displacement", Dimension.VOLUME),
                InputRequirement("gross_primer_pocket_treatment", "gross_primer_pocket_treatment", RequirementKind.REQUIRED, "Explicit primer-pocket basis of gross capacity", (InputCandidateKind.CONTROLLED_CATEGORY,), None, ("included", "excluded", "filled", "sealed", "unknown")),
                InputRequirement("target_primer_pocket_treatment", "target_primer_pocket_treatment", RequirementKind.REQUIRED, "Explicit primer-pocket basis requested for usable space", (InputCandidateKind.CONTROLLED_CATEGORY,), None, ("included", "excluded", "filled", "sealed", "unknown")),
                InputRequirement("primer_pocket_correction", "primer_pocket_correction", RequirementKind.OPTIONAL, "Explicit primer-pocket volume when the declared bases differ", (InputCandidateKind.PRIMER_POCKET_CAPACITY,), Dimension.VOLUME, (), None, True),
            ), None, (), provenance, promoted,
        ),
    )
    branch_selector = InputRequirement("base_geometry", "base_geometry", RequirementKind.REQUIRED, "Explicit projectile-base geometry branch", (InputCandidateKind.CONTROLLED_CATEGORY,), None, ("flat_base", "partial_boat_tail", "full_boat_tail"))
    displacement = RequirementSet(
        "M03-RS-SEATED-DISPLACEMENT-V1", "seated_projectile_displacement", 1,
        "M01-GEO-SEATED-DISPLACEMENT", "Seated projectile displacement",
        "Explicit flat-base, partial-boat-tail, or full-boat-tail branch inputs for existing M01 displacement operations.",
        (
            branch_selector,
            _req("flat_shank_diameter", "shank_diameter", Dimension.LENGTH, kind=RequirementKind.CONDITIONAL, branch="flat_base"),
            _req("flat_intrusion", "seated_intrusion", Dimension.LENGTH, kind=RequirementKind.CONDITIONAL, branch="flat_base"),
            _req("partial_shank_diameter", "shank_diameter", Dimension.LENGTH, kind=RequirementKind.CONDITIONAL, branch="partial_boat_tail"),
            _req("partial_tail_base_diameter", "boat_tail_base_diameter", Dimension.LENGTH, kind=RequirementKind.CONDITIONAL, branch="partial_boat_tail"),
            _req("partial_tail_length", "boat_tail_axial_length", Dimension.LENGTH, kind=RequirementKind.CONDITIONAL, branch="partial_boat_tail"),
            _req("partial_intrusion", "seated_intrusion", Dimension.LENGTH, kind=RequirementKind.CONDITIONAL, branch="partial_boat_tail"),
            _req("full_shank_diameter", "shank_diameter", Dimension.LENGTH, kind=RequirementKind.CONDITIONAL, branch="full_boat_tail"),
            _req("full_tail_base_diameter", "boat_tail_base_diameter", Dimension.LENGTH, kind=RequirementKind.CONDITIONAL, branch="full_boat_tail"),
            _req("full_tail_length", "boat_tail_axial_length", Dimension.LENGTH, kind=RequirementKind.CONDITIONAL, branch="full_boat_tail"),
            _req("full_intrusion", "seated_intrusion", Dimension.LENGTH, kind=RequirementKind.CONDITIONAL, branch="full_boat_tail"),
        ),
        "base_geometry",
        (
            ConditionalBranch("flat_base", "flat_base", "Existing flat-base cylinder displacement."),
            ConditionalBranch("partial_boat_tail", "partial_boat_tail", "Existing partial-frustum boat-tail displacement."),
            ConditionalBranch("full_boat_tail", "full_boat_tail", "Existing full-frustum plus shank displacement."),
        ), provenance, promoted,
    )
    return simple + (displacement,)
