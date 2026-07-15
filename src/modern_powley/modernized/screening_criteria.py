"""Immutable M04 declarative criterion and criterion-set definitions."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping, TypeAlias

from .missing_values import MissingState
from .property_domains import BoundKind
from .property_observations import SourceLocator
from .provenance import ModelMaturity, Provenance
from .units import Quantity

M04_SCHEMA_ID = "modern_powley.m04.v1"


class CriterionRole(str, Enum):
    """Declared policy role independent of criterion activation status."""

    MANDATORY = "mandatory"
    ADVISORY = "advisory"
    INFORMATIONAL = "informational"
    DIAGNOSTIC_ONLY = "diagnostic_only"
    EXPLICITLY_INACTIVE = "explicitly_inactive"
    HISTORICAL_RECORD = "historical_record"
    EXPERIMENTAL_RECORD = "experimental_record"
    UNAVAILABLE_AT_CURRENT_MATURITY = "unavailable_at_current_maturity"


class CriterionStatus(str, Enum):
    """Lifecycle state of one immutable criterion or set definition."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    SUPERSEDED = "superseded"
    WITHDRAWN = "withdrawn"
    HISTORICAL = "historical"
    EXPERIMENTAL = "experimental"
    EVIDENCE_LIMITED = "evidence_limited"
    UNAVAILABLE = "unavailable"


class CriterionForm(str, Enum):
    """Small controlled set of declarative comparisons admitted by M04."""

    REQUIRED_REFERENCE_PRESENT = "required_reference_present"
    PROHIBITED_MISSING_STATE_ABSENT = "prohibited_missing_state_absent"
    REQUIRED_M03_DIAGNOSTIC_CLASSIFICATION = "required_m03_diagnostic_classification"
    EXACT_CATEGORICAL_EQUALITY = "exact_categorical_equality"
    CATEGORY_IN_FINITE_SET = "category_in_finite_set"
    EXACT_IDENTIFIER_EQUALITY = "exact_identifier_equality"
    NUMERIC_AT_OR_ABOVE = "numeric_at_or_above"
    NUMERIC_ABOVE = "numeric_above"
    NUMERIC_AT_OR_BELOW = "numeric_at_or_below"
    NUMERIC_BELOW = "numeric_below"
    NUMERIC_POINT_INSIDE_INTERVAL = "numeric_point_inside_interval"
    NUMERIC_INTERVAL_FULLY_CONTAINED = "numeric_interval_fully_contained"
    NO_RECORDED_CONFLICT = "no_recorded_conflict"
    EXPLICIT_MANUAL_ASSERTION = "explicit_manual_assertion"


class ThresholdKind(str, Enum):
    """Tagged threshold representations for controlled criterion forms."""

    LITERAL = "literal"
    FINITE_SET = "finite_set"
    MISSING_STATE_SET = "missing_state_set"
    NUMERIC_BOUND = "numeric_bound"
    NUMERIC_INTERVAL = "numeric_interval"


def _text(value: str, name: str) -> str:
    value = str(value).strip()
    if not value:
        raise ValueError(f"{name} is required")
    return value


def _strict(data: Mapping[str, Any], fields: set[str]) -> None:
    if set(data) != fields:
        raise ValueError(f"expected fields {sorted(fields)}, got {sorted(data)}")


@dataclass(frozen=True, slots=True)
class LiteralThreshold:
    """Exact category, identifier, diagnostic status, or conflict declaration."""

    value: str
    definition: str
    convention: str

    def __post_init__(self) -> None:
        _text(self.value, "literal threshold value")
        _text(self.definition, "literal threshold definition")
        _text(self.convention, "literal threshold convention")

    def to_dict(self) -> dict[str, object]:
        return {"kind": ThresholdKind.LITERAL.value, "value": self.value, "definition": self.definition, "convention": self.convention}


@dataclass(frozen=True, slots=True)
class FiniteSetThreshold:
    """Finite literal category set with no similarity or alias semantics."""

    values: tuple[str, ...]
    definition: str
    convention: str

    def __post_init__(self) -> None:
        if not self.values or any(not item.strip() for item in self.values) or len(self.values) != len(set(self.values)):
            raise ValueError("finite-set threshold values must be nonblank and unique")
        _text(self.definition, "finite-set definition")
        _text(self.convention, "finite-set convention")

    def to_dict(self) -> dict[str, object]:
        return {"kind": ThresholdKind.FINITE_SET.value, "values": list(self.values), "definition": self.definition, "convention": self.convention}


@dataclass(frozen=True, slots=True)
class MissingStateSetThreshold:
    """Explicit M02 missing states prohibited by one criterion."""

    states: tuple[MissingState, ...]
    rationale: str

    def __post_init__(self) -> None:
        states = tuple(MissingState(item) for item in self.states)
        if not states or len(states) != len(set(states)):
            raise ValueError("missing-state threshold must be nonempty and unique")
        object.__setattr__(self, "states", states)
        _text(self.rationale, "missing-state rationale")

    def to_dict(self) -> dict[str, object]:
        return {"kind": ThresholdKind.MISSING_STATE_SET.value, "states": [item.value for item in self.states], "rationale": self.rationale}


@dataclass(frozen=True, slots=True)
class NumericBoundThreshold:
    """One dimensional bound retaining supplied unit, definition, and authority."""

    quantity: Quantity
    boundary: BoundKind
    definition: str
    convention: str
    provenance: Provenance
    rationale: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "boundary", BoundKind(self.boundary))
        if self.boundary is BoundKind.UNBOUNDED:
            raise ValueError("criterion numeric bound must be inclusive or exclusive")
        _text(self.definition, "numeric-bound definition")
        _text(self.convention, "numeric-bound convention")
        _text(self.rationale, "numeric-bound rationale")

    def to_dict(self) -> dict[str, object]:
        return {"kind": ThresholdKind.NUMERIC_BOUND.value, "quantity": self.quantity.to_dict(), "boundary": self.boundary.value, "definition": self.definition, "convention": self.convention, "provenance": self.provenance.to_dict(), "rationale": self.rationale}


@dataclass(frozen=True, slots=True)
class NumericIntervalThreshold:
    """Finite dimensional interval with explicit endpoint inclusion."""

    lower: NumericBoundThreshold
    upper: NumericBoundThreshold

    def __post_init__(self) -> None:
        if self.lower.quantity.dimension is not self.upper.quantity.dimension:
            raise ValueError("criterion interval bounds must have compatible dimensions")
        if (self.lower.definition, self.lower.convention) != (self.upper.definition, self.upper.convention):
            raise ValueError("criterion interval definitions and conventions must match")
        if self.lower.quantity.si_value > self.upper.quantity.si_value:
            raise ValueError("criterion interval bounds must be ordered")
        if self.lower.quantity.si_value == self.upper.quantity.si_value and BoundKind.EXCLUSIVE in {self.lower.boundary, self.upper.boundary}:
            raise ValueError("zero-width criterion interval must include both endpoints")

    def to_dict(self) -> dict[str, object]:
        return {"kind": ThresholdKind.NUMERIC_INTERVAL.value, "lower": self.lower.to_dict(), "upper": self.upper.to_dict()}


CriterionThreshold: TypeAlias = LiteralThreshold | FiniteSetThreshold | MissingStateSetThreshold | NumericBoundThreshold | NumericIntervalThreshold


def threshold_from_dict(data: Mapping[str, Any]) -> CriterionThreshold:
    """Parse one strict tagged criterion threshold."""

    if not isinstance(data, Mapping) or "kind" not in data:
        raise ValueError("criterion threshold requires kind")
    kind = ThresholdKind(str(data["kind"]))
    if kind is ThresholdKind.LITERAL:
        _strict(data, {"kind", "value", "definition", "convention"})
        return LiteralThreshold(str(data["value"]), str(data["definition"]), str(data["convention"]))
    if kind is ThresholdKind.FINITE_SET:
        _strict(data, {"kind", "values", "definition", "convention"})
        values = data["values"]
        if not isinstance(values, list) or not all(isinstance(item, str) for item in values):
            raise TypeError("finite-set values must be a string list")
        return FiniteSetThreshold(tuple(values), str(data["definition"]), str(data["convention"]))
    if kind is ThresholdKind.MISSING_STATE_SET:
        _strict(data, {"kind", "states", "rationale"})
        states = data["states"]
        if not isinstance(states, list) or not all(isinstance(item, str) for item in states):
            raise TypeError("missing states must be a string list")
        return MissingStateSetThreshold(tuple(MissingState(item) for item in states), str(data["rationale"]))
    if kind is ThresholdKind.NUMERIC_BOUND:
        _strict(data, {"kind", "quantity", "boundary", "definition", "convention", "provenance", "rationale"})
        return NumericBoundThreshold(Quantity.from_dict(data["quantity"]), BoundKind(str(data["boundary"])), str(data["definition"]), str(data["convention"]), Provenance.from_dict(data["provenance"]), str(data["rationale"]))
    _strict(data, {"kind", "lower", "upper"})
    lower, upper = threshold_from_dict(data["lower"]), threshold_from_dict(data["upper"])
    if not isinstance(lower, NumericBoundThreshold) or not isinstance(upper, NumericBoundThreshold):
        raise ValueError("criterion interval requires numeric bounds")
    return NumericIntervalThreshold(lower, upper)


_NO_THRESHOLD_FORMS = {CriterionForm.REQUIRED_REFERENCE_PRESENT, CriterionForm.EXPLICIT_MANUAL_ASSERTION}
_LITERAL_FORMS = {CriterionForm.REQUIRED_M03_DIAGNOSTIC_CLASSIFICATION, CriterionForm.EXACT_CATEGORICAL_EQUALITY, CriterionForm.EXACT_IDENTIFIER_EQUALITY, CriterionForm.NO_RECORDED_CONFLICT}
_BOUND_FORMS = {CriterionForm.NUMERIC_AT_OR_ABOVE, CriterionForm.NUMERIC_ABOVE, CriterionForm.NUMERIC_AT_OR_BELOW, CriterionForm.NUMERIC_BELOW}
_INTERVAL_FORMS = {CriterionForm.NUMERIC_POINT_INSIDE_INTERVAL, CriterionForm.NUMERIC_INTERVAL_FULLY_CONTAINED}


@dataclass(frozen=True, slots=True)
class CriterionDefinition:
    """Immutable, versioned, nonexecutable declaration of one criterion."""

    record_id: str
    criterion_id: str
    version: int
    name: str
    description: str
    purpose: str
    role: CriterionRole
    status: CriterionStatus
    form: CriterionForm
    reference_definition_id: str
    required_evidence_ids: tuple[str, ...]
    threshold: CriterionThreshold | None
    applicability_conditions: tuple[str, ...]
    provenance: Provenance
    source_locator: SourceLocator
    design_authority: str
    rationale: str
    known_limitations: tuple[str, ...]
    date_or_publication_context: str
    supersedes_criterion_id: str | None = None
    supersedes_version: int | None = None

    def __post_init__(self) -> None:
        for value, name in ((self.record_id, "record_id"), (self.criterion_id, "criterion_id"), (self.name, "name"), (self.description, "description"), (self.purpose, "purpose"), (self.reference_definition_id, "reference_definition_id"), (self.design_authority, "design_authority"), (self.rationale, "rationale"), (self.date_or_publication_context, "date_or_publication_context")):
            _text(value, name)
        if isinstance(self.version, bool) or not isinstance(self.version, int) or self.version <= 0 or not self.required_evidence_ids or any(not item.strip() for item in self.required_evidence_ids) or len(self.required_evidence_ids) != len(set(self.required_evidence_ids)):
            raise ValueError("criterion version and unique required evidence IDs are required")
        object.__setattr__(self, "role", CriterionRole(self.role))
        object.__setattr__(self, "status", CriterionStatus(self.status))
        object.__setattr__(self, "form", CriterionForm(self.form))
        if self.provenance.source_id != self.source_locator.source_id:
            raise ValueError("criterion provenance and source locator must match")
        if any(not item.strip() for item in self.applicability_conditions + self.known_limitations):
            raise ValueError("criterion conditions and limitations must be nonblank")
        if (self.supersedes_criterion_id is None) != (self.supersedes_version is None):
            raise ValueError("criterion supersession requires both identity and version")
        if self.supersedes_version is not None and self.supersedes_version <= 0:
            raise ValueError("superseded criterion version must be positive")
        if (self.supersedes_criterion_id, self.supersedes_version) == (self.criterion_id, self.version):
            raise ValueError("criterion cannot supersede its own exact version")
        expected = None
        if self.form in _LITERAL_FORMS:
            expected = LiteralThreshold
        elif self.form is CriterionForm.CATEGORY_IN_FINITE_SET:
            expected = FiniteSetThreshold
        elif self.form is CriterionForm.PROHIBITED_MISSING_STATE_ABSENT:
            expected = MissingStateSetThreshold
        elif self.form in _BOUND_FORMS:
            expected = NumericBoundThreshold
        elif self.form in _INTERVAL_FORMS:
            expected = NumericIntervalThreshold
        if self.form in _NO_THRESHOLD_FORMS:
            if self.threshold is not None:
                raise ValueError("criterion form does not accept a threshold")
        elif expected is None or not isinstance(self.threshold, expected):
            raise ValueError("criterion form and threshold representation disagree")
        multi_reference_forms = {
            CriterionForm.REQUIRED_REFERENCE_PRESENT,
            CriterionForm.PROHIBITED_MISSING_STATE_ABSENT,
            CriterionForm.EXPLICIT_MANUAL_ASSERTION,
        }
        if self.form not in multi_reference_forms and len(self.required_evidence_ids) != 1:
            raise ValueError("literal comparison form requires exactly one evidence reference")
        boundary_by_form = {
            CriterionForm.NUMERIC_AT_OR_ABOVE: BoundKind.INCLUSIVE,
            CriterionForm.NUMERIC_ABOVE: BoundKind.EXCLUSIVE,
            CriterionForm.NUMERIC_AT_OR_BELOW: BoundKind.INCLUSIVE,
            CriterionForm.NUMERIC_BELOW: BoundKind.EXCLUSIVE,
        }
        if self.form in boundary_by_form and isinstance(self.threshold, NumericBoundThreshold):
            if self.threshold.boundary is not boundary_by_form[self.form]:
                raise ValueError("criterion form and numeric-bound inclusion disagree")
        role_status = {
            CriterionRole.EXPLICITLY_INACTIVE: CriterionStatus.INACTIVE,
            CriterionRole.HISTORICAL_RECORD: CriterionStatus.HISTORICAL,
            CriterionRole.EXPERIMENTAL_RECORD: CriterionStatus.EXPERIMENTAL,
            CriterionRole.UNAVAILABLE_AT_CURRENT_MATURITY: CriterionStatus.UNAVAILABLE,
        }
        if self.role in role_status and self.status is not role_status[self.role]:
            raise ValueError("criterion role and activation status disagree")

    def to_dict(self) -> dict[str, object]:
        return {
            "schema": M04_SCHEMA_ID, "record_type": "criterion_definition", "record_id": self.record_id,
            "criterion_id": self.criterion_id, "version": self.version, "name": self.name,
            "description": self.description, "purpose": self.purpose, "role": self.role.value,
            "status": self.status.value, "form": self.form.value,
            "reference_definition_id": self.reference_definition_id,
            "required_evidence_ids": list(self.required_evidence_ids),
            "threshold": None if self.threshold is None else self.threshold.to_dict(),
            "applicability_conditions": list(self.applicability_conditions),
            "provenance": self.provenance.to_dict(), "source_locator": self.source_locator.to_dict(),
            "design_authority": self.design_authority, "rationale": self.rationale,
            "known_limitations": list(self.known_limitations),
            "date_or_publication_context": self.date_or_publication_context,
            "supersedes_criterion_id": self.supersedes_criterion_id,
            "supersedes_version": self.supersedes_version,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> CriterionDefinition:
        fields = {"schema", "record_type", "record_id", "criterion_id", "version", "name", "description", "purpose", "role", "status", "form", "reference_definition_id", "required_evidence_ids", "threshold", "applicability_conditions", "provenance", "source_locator", "design_authority", "rationale", "known_limitations", "date_or_publication_context", "supersedes_criterion_id", "supersedes_version"}
        _strict(data, fields)
        if data["schema"] != M04_SCHEMA_ID or data["record_type"] != "criterion_definition":
            raise ValueError("invalid M04 criterion-definition header")
        evidence, conditions, limitations = data["required_evidence_ids"], data["applicability_conditions"], data["known_limitations"]
        if any(not isinstance(value, list) or not all(isinstance(item, str) for item in value) for value in (evidence, conditions, limitations)):
            raise TypeError("criterion string-list fields are malformed")
        version = data["version"]
        if isinstance(version, bool) or not isinstance(version, int):
            raise TypeError("criterion version must be an integer")
        superseded_version = data["supersedes_version"]
        if superseded_version is not None and (isinstance(superseded_version, bool) or not isinstance(superseded_version, int)):
            raise TypeError("superseded version must be an integer")
        return cls(
            str(data["record_id"]), str(data["criterion_id"]), version, str(data["name"]),
            str(data["description"]), str(data["purpose"]), CriterionRole(str(data["role"])),
            CriterionStatus(str(data["status"])), CriterionForm(str(data["form"])),
            str(data["reference_definition_id"]), tuple(evidence),
            None if data["threshold"] is None else threshold_from_dict(data["threshold"]),
            tuple(conditions), Provenance.from_dict(data["provenance"]),
            SourceLocator.from_dict(data["source_locator"]), str(data["design_authority"]),
            str(data["rationale"]), tuple(limitations), str(data["date_or_publication_context"]),
            None if data["supersedes_criterion_id"] is None else str(data["supersedes_criterion_id"]),
            superseded_version,
        )


@dataclass(frozen=True, slots=True)
class CriterionReference:
    """Exact criterion identity/version and display-only order within one set."""

    criterion_id: str
    criterion_version: int
    role: CriterionRole
    display_order: int

    def __post_init__(self) -> None:
        _text(self.criterion_id, "criterion reference identity")
        if any(isinstance(value, bool) or not isinstance(value, int) for value in (self.criterion_version, self.display_order)) or self.criterion_version <= 0 or self.display_order < 0:
            raise ValueError("criterion reference version must be positive and display order non-negative")
        object.__setattr__(self, "role", CriterionRole(self.role))

    def to_dict(self) -> dict[str, object]:
        return {"criterion_id": self.criterion_id, "criterion_version": self.criterion_version, "role": self.role.value, "display_order": self.display_order}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> CriterionReference:
        _strict(data, {"criterion_id", "criterion_version", "role", "display_order"})
        if any(isinstance(data[field], bool) or not isinstance(data[field], int) for field in ("criterion_version", "display_order")):
            raise TypeError("criterion reference version and order must be integers")
        return cls(str(data["criterion_id"]), data["criterion_version"], CriterionRole(str(data["role"])), data["display_order"])


@dataclass(frozen=True, slots=True)
class CriterionSetDefinition:
    """Versioned narrow-purpose collection of criterion references without weights."""

    record_id: str
    criterion_set_id: str
    version: int
    name: str
    purpose: str
    scope: str
    criteria: tuple[CriterionReference, ...]
    status: CriterionStatus
    provenance: Provenance
    source_locator: SourceLocator
    design_authority: str
    effective_date_or_era: str
    known_exclusions: tuple[str, ...]
    non_implication_statement: str
    supersedes_set_id: str | None = None
    supersedes_version: int | None = None

    def __post_init__(self) -> None:
        for value, name in ((self.record_id, "record_id"), (self.criterion_set_id, "criterion_set_id"), (self.name, "name"), (self.purpose, "purpose"), (self.scope, "scope"), (self.design_authority, "design_authority"), (self.effective_date_or_era, "effective_date_or_era"), (self.non_implication_statement, "non_implication_statement")):
            _text(value, name)
        if isinstance(self.version, bool) or not isinstance(self.version, int) or self.version <= 0 or not self.criteria:
            raise ValueError("criterion set requires positive version and criterion references")
        object.__setattr__(self, "status", CriterionStatus(self.status))
        keys = [(item.criterion_id, item.criterion_version) for item in self.criteria]
        criterion_ids = [item.criterion_id for item in self.criteria]
        orders = [item.display_order for item in self.criteria]
        if len(keys) != len(set(keys)) or len(criterion_ids) != len(set(criterion_ids)) or len(orders) != len(set(orders)):
            raise ValueError("criterion identities, references, and display orders must be unique")
        if self.provenance.source_id != self.source_locator.source_id:
            raise ValueError("criterion-set provenance and source locator must match")
        if any(not item.strip() for item in self.known_exclusions):
            raise ValueError("criterion-set exclusions must be nonblank")
        if "does not establish" not in self.non_implication_statement.casefold():
            raise ValueError("criterion set must explicitly state what a pass does not establish")
        if (self.supersedes_set_id is None) != (self.supersedes_version is None):
            raise ValueError("set supersession requires identity and version")
        if self.supersedes_version is not None and self.supersedes_version <= 0:
            raise ValueError("superseded criterion-set version must be positive")
        if (self.supersedes_set_id, self.supersedes_version) == (self.criterion_set_id, self.version):
            raise ValueError("criterion set cannot supersede its own exact version")

    def to_dict(self) -> dict[str, object]:
        return {
            "schema": M04_SCHEMA_ID, "record_type": "criterion_set_definition", "record_id": self.record_id,
            "criterion_set_id": self.criterion_set_id, "version": self.version, "name": self.name,
            "purpose": self.purpose, "scope": self.scope,
            "criteria": [item.to_dict() for item in self.criteria], "status": self.status.value,
            "provenance": self.provenance.to_dict(), "source_locator": self.source_locator.to_dict(),
            "design_authority": self.design_authority, "effective_date_or_era": self.effective_date_or_era,
            "known_exclusions": list(self.known_exclusions),
            "non_implication_statement": self.non_implication_statement,
            "supersedes_set_id": self.supersedes_set_id, "supersedes_version": self.supersedes_version,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> CriterionSetDefinition:
        fields = {"schema", "record_type", "record_id", "criterion_set_id", "version", "name", "purpose", "scope", "criteria", "status", "provenance", "source_locator", "design_authority", "effective_date_or_era", "known_exclusions", "non_implication_statement", "supersedes_set_id", "supersedes_version"}
        _strict(data, fields)
        if data["schema"] != M04_SCHEMA_ID or data["record_type"] != "criterion_set_definition":
            raise ValueError("invalid M04 criterion-set header")
        criteria, exclusions = data["criteria"], data["known_exclusions"]
        if not isinstance(criteria, list) or not isinstance(exclusions, list) or not all(isinstance(item, str) for item in exclusions):
            raise TypeError("criterion references and exclusions are malformed")
        version = data["version"]
        if isinstance(version, bool) or not isinstance(version, int):
            raise TypeError("criterion-set version must be an integer")
        superseded = data["supersedes_version"]
        if superseded is not None and (isinstance(superseded, bool) or not isinstance(superseded, int)):
            raise TypeError("superseded set version must be an integer")
        return cls(
            str(data["record_id"]), str(data["criterion_set_id"]), version, str(data["name"]),
            str(data["purpose"]), str(data["scope"]), tuple(CriterionReference.from_dict(item) for item in criteria),
            CriterionStatus(str(data["status"])), Provenance.from_dict(data["provenance"]),
            SourceLocator.from_dict(data["source_locator"]), str(data["design_authority"]),
            str(data["effective_date_or_era"]), tuple(exclusions), str(data["non_implication_statement"]),
            None if data["supersedes_set_id"] is None else str(data["supersedes_set_id"]), superseded,
        )
