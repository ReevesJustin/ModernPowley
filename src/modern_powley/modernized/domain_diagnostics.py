"""Literal per-constraint M03 diagnostics for M02 applicability domains."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping, TypeAlias

from .input_requirements import M03_SCHEMA_ID
from .missing_values import MissingState
from .property_domains import (
    ApplicabilityDomain,
    BoundKind,
    CategoricalDomainConstraint,
    DomainStatus,
    NumericDomainConstraint,
    SourceScalarDomainConstraint,
    SourceScalarDomainValue,
)
from .property_observations import PowderPropertyObservation
from .provenance import EvidenceClass, ModelMaturity, Provenance, ValueOrigin
from .units import Quantity


class DomainQueryKind(str, Enum):
    """Literal query representations admitted by M03 diagnostics."""

    NUMERIC_POINT = "numeric_point"
    NUMERIC_INTERVAL = "numeric_interval"
    CATEGORICAL = "categorical"
    IDENTIFIER = "identifier"
    SOURCE_SCALAR_POINT = "source_scalar_point"
    EXPLICITLY_UNAVAILABLE = "explicitly_unavailable"


@dataclass(frozen=True, slots=True)
class QueryInterval:
    """A finite numeric query interval with explicit endpoint inclusion."""

    lower: Quantity
    lower_kind: BoundKind
    upper: Quantity
    upper_kind: BoundKind

    def __post_init__(self) -> None:
        object.__setattr__(self, "lower_kind", BoundKind(self.lower_kind))
        object.__setattr__(self, "upper_kind", BoundKind(self.upper_kind))
        if BoundKind.UNBOUNDED in {self.lower_kind, self.upper_kind}:
            raise ValueError("M03 query intervals must have finite bounded endpoints")
        if self.lower.dimension is not self.upper.dimension:
            raise ValueError("query interval endpoints must have compatible dimensions")
        if self.lower.si_value > self.upper.si_value:
            raise ValueError("query interval endpoints must be ordered")
        if self.lower.si_value == self.upper.si_value and BoundKind.EXCLUSIVE in {self.lower_kind, self.upper_kind}:
            raise ValueError("zero-width query interval must include both endpoints")

    def to_dict(self) -> dict[str, object]:
        return {"lower": self.lower.to_dict(), "lower_kind": self.lower_kind.value, "upper": self.upper.to_dict(), "upper_kind": self.upper_kind.value}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> QueryInterval:
        if set(data) != {"lower", "lower_kind", "upper", "upper_kind"}:
            raise ValueError("malformed query interval fields")
        return cls(Quantity.from_dict(data["lower"]), BoundKind(str(data["lower_kind"])), Quantity.from_dict(data["upper"]), BoundKind(str(data["upper_kind"])))


@dataclass(frozen=True, slots=True)
class DomainQueryValue:
    """One explicit query value or semantic missing state for a domain variable."""

    variable_id: str
    definition: str
    kind: DomainQueryKind
    numeric_point: Quantity | None = None
    numeric_interval: QueryInterval | None = None
    category_or_identifier: str | None = None
    source_scalar_point: SourceScalarDomainValue | None = None
    missing_state: MissingState | None = None
    explanation: str = ""

    def __post_init__(self) -> None:
        if not self.variable_id.strip() or not self.definition.strip():
            raise ValueError("domain query variable identity and definition are required")
        object.__setattr__(self, "kind", DomainQueryKind(self.kind))
        if self.missing_state is not None:
            object.__setattr__(self, "missing_state", MissingState(self.missing_state))
        values = (self.numeric_point, self.numeric_interval, self.category_or_identifier, self.source_scalar_point, self.missing_state)
        if sum(value is not None for value in values) != 1:
            raise ValueError("domain query requires exactly one tagged value")
        expected = {
            DomainQueryKind.NUMERIC_POINT: self.numeric_point,
            DomainQueryKind.NUMERIC_INTERVAL: self.numeric_interval,
            DomainQueryKind.CATEGORICAL: self.category_or_identifier,
            DomainQueryKind.IDENTIFIER: self.category_or_identifier,
            DomainQueryKind.SOURCE_SCALAR_POINT: self.source_scalar_point,
            DomainQueryKind.EXPLICITLY_UNAVAILABLE: self.missing_state,
        }[self.kind]
        if expected is None:
            raise ValueError("domain query kind does not match its tagged value")
        if self.category_or_identifier is not None and not self.category_or_identifier.strip():
            raise ValueError("query category or identifier must be nonblank")
        if self.kind is DomainQueryKind.EXPLICITLY_UNAVAILABLE and not self.explanation.strip():
            raise ValueError("explicitly unavailable query requires explanation")

    def to_dict(self) -> dict[str, object]:
        scalar = None
        if self.source_scalar_point is not None:
            scalar = {"value": self.source_scalar_point.value, "reported_unit": self.source_scalar_point.reported_unit, "convention": self.source_scalar_point.convention}
        return {
            "variable_id": self.variable_id, "definition": self.definition, "kind": self.kind.value,
            "numeric_point": None if self.numeric_point is None else self.numeric_point.to_dict(),
            "numeric_interval": None if self.numeric_interval is None else self.numeric_interval.to_dict(),
            "category_or_identifier": self.category_or_identifier, "source_scalar_point": scalar,
            "missing_state": None if self.missing_state is None else self.missing_state.value,
            "explanation": self.explanation,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> DomainQueryValue:
        fields = {"variable_id", "definition", "kind", "numeric_point", "numeric_interval", "category_or_identifier", "source_scalar_point", "missing_state", "explanation"}
        if set(data) != fields:
            raise ValueError("malformed domain query fields")
        scalar = data["source_scalar_point"]
        if scalar is not None:
            if not isinstance(scalar, Mapping) or set(scalar) != {"value", "reported_unit", "convention"}:
                raise ValueError("malformed source-scalar query")
            scalar = SourceScalarDomainValue(scalar["value"], str(scalar["reported_unit"]), str(scalar["convention"]))
        return cls(
            str(data["variable_id"]), str(data["definition"]), DomainQueryKind(str(data["kind"])),
            None if data["numeric_point"] is None else Quantity.from_dict(data["numeric_point"]),
            None if data["numeric_interval"] is None else QueryInterval.from_dict(data["numeric_interval"]),
            None if data["category_or_identifier"] is None else str(data["category_or_identifier"]),
            scalar, None if data["missing_state"] is None else MissingState(str(data["missing_state"])),
            str(data["explanation"]),
        )


@dataclass(frozen=True, slots=True)
class DomainQueryContext:
    """Query values supplied for one specific observation and property definition."""

    record_id: str
    observation_id: str
    property_definition_id: str
    values: tuple[DomainQueryValue, ...]
    provenance: Provenance

    def __post_init__(self) -> None:
        if not self.record_id.strip() or not self.observation_id.strip() or not self.property_definition_id.strip():
            raise ValueError("domain query context identities are required")
        ids = [item.variable_id for item in self.values]
        if len(ids) != len(set(ids)):
            raise ValueError("domain query variable IDs must be unique")

    def to_dict(self) -> dict[str, object]:
        return {"schema": M03_SCHEMA_ID, "record_type": "domain_query_context", "record_id": self.record_id, "observation_id": self.observation_id, "property_definition_id": self.property_definition_id, "values": [item.to_dict() for item in self.values], "provenance": self.provenance.to_dict()}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> DomainQueryContext:
        if set(data) != {"schema", "record_type", "record_id", "observation_id", "property_definition_id", "values", "provenance"} or data.get("schema") != M03_SCHEMA_ID or data.get("record_type") != "domain_query_context":
            raise ValueError("malformed M03 domain-query context")
        values = data["values"]
        if not isinstance(values, list):
            raise TypeError("domain query values must be a list")
        return cls(str(data["record_id"]), str(data["observation_id"]), str(data["property_definition_id"]), tuple(DomainQueryValue.from_dict(item) for item in values), Provenance.from_dict(data["provenance"]))


class ConstraintKind(str, Enum):
    """Declared constraint identity retained in a diagnostic."""

    PROPERTY_DEFINITION = "property_definition"
    NUMERIC = "numeric"
    CATEGORICAL = "categorical"
    SOURCE_SCALAR = "source_scalar"
    EXTRA_QUERY = "extra_query"
    DOMAIN = "domain"


class DomainDiagnosticStatus(str, Enum):
    """Literal result for one domain constraint or query precondition."""

    INSIDE_DECLARED_DOMAIN = "inside_declared_domain"
    OUTSIDE_DECLARED_DOMAIN = "outside_declared_domain"
    DOMAIN_UNSPECIFIED = "domain_unspecified"
    REQUIRED_QUERY_VALUE_MISSING = "required_query_value_missing"
    QUERY_VALUE_EXPLICITLY_UNAVAILABLE = "query_value_explicitly_unavailable"
    INCOMPATIBLE_UNITS = "incompatible_units"
    DEFINITION_MISMATCH = "definition_mismatch"
    CATEGORICAL_MISMATCH = "categorical_mismatch"
    IDENTIFIER_MISMATCH = "identifier_mismatch"
    PARTIALLY_COMPARABLE = "partially_comparable"
    INDETERMINATE = "indeterminate"
    CONSTRAINT_NOT_APPLICABLE = "constraint_not_applicable"


class ApplicabilitySummary(str, Enum):
    """Aggregate literal domain result without suitability semantics."""

    ALL_DECLARED_CONSTRAINTS_SATISFIED = "all_declared_constraints_satisfied"
    AT_LEAST_ONE_DECLARED_CONSTRAINT_REJECTED = "at_least_one_declared_constraint_rejected"
    NO_DECLARED_DOMAIN_SUPPLIED = "no_declared_domain_supplied"
    APPLICABILITY_INDETERMINATE = "applicability_indeterminate"


Constraint: TypeAlias = NumericDomainConstraint | CategoricalDomainConstraint | SourceScalarDomainConstraint


def _constraint_to_dict(value: Constraint | None) -> dict[str, object] | None:
    if value is None:
        return None
    kind = "numeric" if isinstance(value, NumericDomainConstraint) else "categorical" if isinstance(value, CategoricalDomainConstraint) else "source_scalar"
    return {"kind": kind, "value": value.to_dict()}


def _constraint_from_dict(data: Mapping[str, Any] | None) -> Constraint | None:
    if data is None:
        return None
    if set(data) != {"kind", "value"}:
        raise ValueError("malformed retained constraint")
    classes = {"numeric": NumericDomainConstraint, "categorical": CategoricalDomainConstraint, "source_scalar": SourceScalarDomainConstraint}
    try:
        return classes[str(data["kind"])].from_dict(data["value"])
    except KeyError as error:
        raise ValueError("unsupported retained constraint kind") from error


@dataclass(frozen=True, slots=True)
class DomainConstraintDiagnostic:
    """Explain one literal constraint comparison, including its exact operands."""

    observation_id: str
    constraint_id: str
    constraint_kind: ConstraintKind
    status: DomainDiagnosticStatus
    query: DomainQueryValue | None
    declared_constraint: Constraint | None
    comparison_performed: str
    rejection_reason: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "constraint_kind", ConstraintKind(self.constraint_kind))
        object.__setattr__(self, "status", DomainDiagnosticStatus(self.status))
        if not self.observation_id.strip() or not self.constraint_id.strip() or not self.comparison_performed.strip() or not self.rejection_reason.strip():
            raise ValueError("domain diagnostic identity and explanation are required")

    def to_dict(self) -> dict[str, object]:
        return {"observation_id": self.observation_id, "constraint_id": self.constraint_id, "constraint_kind": self.constraint_kind.value, "status": self.status.value, "query": None if self.query is None else self.query.to_dict(), "declared_constraint": _constraint_to_dict(self.declared_constraint), "comparison_performed": self.comparison_performed, "rejection_reason": self.rejection_reason}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> DomainConstraintDiagnostic:
        fields = {"observation_id", "constraint_id", "constraint_kind", "status", "query", "declared_constraint", "comparison_performed", "rejection_reason"}
        if set(data) != fields:
            raise ValueError("malformed domain diagnostic fields")
        return cls(str(data["observation_id"]), str(data["constraint_id"]), ConstraintKind(str(data["constraint_kind"])), DomainDiagnosticStatus(str(data["status"])), None if data["query"] is None else DomainQueryValue.from_dict(data["query"]), _constraint_from_dict(data["declared_constraint"]), str(data["comparison_performed"]), str(data["rejection_reason"]))


@dataclass(frozen=True, slots=True)
class ApplicabilityEvaluation:
    """Aggregate literal-domain result retaining every per-constraint diagnostic."""

    record_id: str
    observation_id: str
    query_context_id: str
    summary: ApplicabilitySummary
    diagnostics: tuple[DomainConstraintDiagnostic, ...]
    provenance: Provenance

    def __post_init__(self) -> None:
        object.__setattr__(self, "summary", ApplicabilitySummary(self.summary))
        if not self.record_id.strip() or not self.observation_id.strip() or not self.query_context_id.strip() or not self.diagnostics:
            raise ValueError("applicability evaluation identities and diagnostics are required")
        expected = _summarize_diagnostics(self.diagnostics)
        if self.summary is not expected:
            raise ValueError("applicability summary must exactly reflect retained diagnostics")

    def to_dict(self) -> dict[str, object]:
        return {"schema": M03_SCHEMA_ID, "record_type": "applicability_evaluation", "record_id": self.record_id, "observation_id": self.observation_id, "query_context_id": self.query_context_id, "summary": self.summary.value, "diagnostics": [item.to_dict() for item in self.diagnostics], "provenance": self.provenance.to_dict()}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> ApplicabilityEvaluation:
        fields = {"schema", "record_type", "record_id", "observation_id", "query_context_id", "summary", "diagnostics", "provenance"}
        if set(data) != fields or data.get("schema") != M03_SCHEMA_ID or data.get("record_type") != "applicability_evaluation":
            raise ValueError("malformed M03 applicability evaluation")
        diagnostics = data["diagnostics"]
        if not isinstance(diagnostics, list):
            raise TypeError("applicability diagnostics must be a list")
        return cls(str(data["record_id"]), str(data["observation_id"]), str(data["query_context_id"]), ApplicabilitySummary(str(data["summary"])), tuple(DomainConstraintDiagnostic.from_dict(item) for item in diagnostics), Provenance.from_dict(data["provenance"]))


def _query_for(context: DomainQueryContext, variable_id: str) -> DomainQueryValue | None:
    return next((item for item in context.values if item.variable_id == variable_id), None)


def _summarize_diagnostics(diagnostics: tuple[DomainConstraintDiagnostic, ...] | list[DomainConstraintDiagnostic]) -> ApplicabilitySummary:
    statuses = {item.status for item in diagnostics}
    if DomainDiagnosticStatus.DOMAIN_UNSPECIFIED in statuses:
        return ApplicabilitySummary.NO_DECLARED_DOMAIN_SUPPLIED
    rejected = {DomainDiagnosticStatus.OUTSIDE_DECLARED_DOMAIN, DomainDiagnosticStatus.CATEGORICAL_MISMATCH, DomainDiagnosticStatus.IDENTIFIER_MISMATCH}
    indeterminate = {DomainDiagnosticStatus.REQUIRED_QUERY_VALUE_MISSING, DomainDiagnosticStatus.QUERY_VALUE_EXPLICITLY_UNAVAILABLE, DomainDiagnosticStatus.INCOMPATIBLE_UNITS, DomainDiagnosticStatus.DEFINITION_MISMATCH, DomainDiagnosticStatus.PARTIALLY_COMPARABLE, DomainDiagnosticStatus.INDETERMINATE}
    if statuses & rejected:
        return ApplicabilitySummary.AT_LEAST_ONE_DECLARED_CONSTRAINT_REJECTED
    if statuses & indeterminate:
        return ApplicabilitySummary.APPLICABILITY_INDETERMINATE
    return ApplicabilitySummary.ALL_DECLARED_CONSTRAINTS_SATISFIED


def _missing_or_definition(observation_id: str, constraint: Constraint, query: DomainQueryValue | None, kind: ConstraintKind) -> DomainConstraintDiagnostic | None:
    if query is None:
        return DomainConstraintDiagnostic(observation_id, constraint.variable_id, kind, DomainDiagnosticStatus.REQUIRED_QUERY_VALUE_MISSING, None, constraint, "No comparison performed.", "Required literal query value was not supplied.")
    if query.kind is DomainQueryKind.EXPLICITLY_UNAVAILABLE:
        return DomainConstraintDiagnostic(observation_id, constraint.variable_id, kind, DomainDiagnosticStatus.QUERY_VALUE_EXPLICITLY_UNAVAILABLE, query, constraint, "No comparison performed.", f"Query is explicitly unavailable: {query.missing_state.value}.")
    if query.definition != constraint.definition:
        return DomainConstraintDiagnostic(observation_id, constraint.variable_id, kind, DomainDiagnosticStatus.DEFINITION_MISMATCH, query, constraint, "Compared query and declared variable definitions literally.", "Query definition differs from the declared domain definition.")
    return None


def _point_against_numeric(observation_id: str, constraint: NumericDomainConstraint, query: DomainQueryValue) -> DomainConstraintDiagnostic:
    if query.kind is not DomainQueryKind.NUMERIC_POINT or query.numeric_point is None:
        return DomainConstraintDiagnostic(observation_id, constraint.variable_id, ConstraintKind.NUMERIC, DomainDiagnosticStatus.DEFINITION_MISMATCH, query, constraint, "Compared query representation with numeric-point constraint.", "Query is not a numeric point or interval.")
    value = query.numeric_point
    if value.dimension is not constraint.dimension:
        return DomainConstraintDiagnostic(observation_id, constraint.variable_id, ConstraintKind.NUMERIC, DomainDiagnosticStatus.INCOMPATIBLE_UNITS, query, constraint, "Compared M01 quantity dimensions.", "Query unit is not dimensionally compatible with the domain boundary.")
    si = value.si_value
    if constraint.lower.value is not None:
        lower = constraint.lower.value.quantity.si_value
        if si < lower:
            return DomainConstraintDiagnostic(observation_id, constraint.variable_id, ConstraintKind.NUMERIC, DomainDiagnosticStatus.OUTSIDE_DECLARED_DOMAIN, query, constraint, "Converted compatible units to SI and compared the point with the lower boundary.", "Value is below the declared lower boundary.")
        if si == lower and constraint.lower.kind is BoundKind.EXCLUSIVE:
            return DomainConstraintDiagnostic(observation_id, constraint.variable_id, ConstraintKind.NUMERIC, DomainDiagnosticStatus.OUTSIDE_DECLARED_DOMAIN, query, constraint, "Converted compatible units to SI and compared equality with the exclusive lower boundary.", "Value equals the exclusive lower boundary.")
    if constraint.upper.value is not None:
        upper = constraint.upper.value.quantity.si_value
        if si > upper:
            return DomainConstraintDiagnostic(observation_id, constraint.variable_id, ConstraintKind.NUMERIC, DomainDiagnosticStatus.OUTSIDE_DECLARED_DOMAIN, query, constraint, "Converted compatible units to SI and compared the point with the upper boundary.", "Value is above the declared upper boundary.")
        if si == upper and constraint.upper.kind is BoundKind.EXCLUSIVE:
            return DomainConstraintDiagnostic(observation_id, constraint.variable_id, ConstraintKind.NUMERIC, DomainDiagnosticStatus.OUTSIDE_DECLARED_DOMAIN, query, constraint, "Converted compatible units to SI and compared equality with the exclusive upper boundary.", "Value equals the exclusive upper boundary.")
    return DomainConstraintDiagnostic(observation_id, constraint.variable_id, ConstraintKind.NUMERIC, DomainDiagnosticStatus.INSIDE_DECLARED_DOMAIN, query, constraint, "Converted compatible units to SI and applied exact endpoint inclusion.", "Point satisfies the literal declared numeric constraint.")


def _interval_against_numeric(observation_id: str, constraint: NumericDomainConstraint, query: DomainQueryValue) -> DomainConstraintDiagnostic:
    interval = query.numeric_interval
    assert interval is not None
    if interval.lower.dimension is not constraint.dimension:
        return DomainConstraintDiagnostic(observation_id, constraint.variable_id, ConstraintKind.NUMERIC, DomainDiagnosticStatus.INCOMPATIBLE_UNITS, query, constraint, "Compared M01 interval and boundary dimensions.", "Query interval unit is not dimensionally compatible with the domain boundary.")
    ql, qu = interval.lower.si_value, interval.upper.si_value
    lower = None if constraint.lower.value is None else constraint.lower.value.quantity.si_value
    upper = None if constraint.upper.value is None else constraint.upper.value.quantity.si_value
    below = lower is not None and (qu < lower or (qu == lower and (interval.upper_kind is BoundKind.EXCLUSIVE or constraint.lower.kind is BoundKind.EXCLUSIVE)))
    above = upper is not None and (ql > upper or (ql == upper and (interval.lower_kind is BoundKind.EXCLUSIVE or constraint.upper.kind is BoundKind.EXCLUSIVE)))
    if below or above:
        reason = "Query interval is wholly below the declared domain." if below else "Query interval is wholly above the declared domain."
        return DomainConstraintDiagnostic(observation_id, constraint.variable_id, ConstraintKind.NUMERIC, DomainDiagnosticStatus.OUTSIDE_DECLARED_DOMAIN, query, constraint, "Compared interval endpoints and inclusion for literal disjointness.", reason)
    lower_inside = lower is None or ql > lower or (ql == lower and not (interval.lower_kind is BoundKind.INCLUSIVE and constraint.lower.kind is BoundKind.EXCLUSIVE))
    upper_inside = upper is None or qu < upper or (qu == upper and not (interval.upper_kind is BoundKind.INCLUSIVE and constraint.upper.kind is BoundKind.EXCLUSIVE))
    if lower_inside and upper_inside:
        return DomainConstraintDiagnostic(observation_id, constraint.variable_id, ConstraintKind.NUMERIC, DomainDiagnosticStatus.INSIDE_DECLARED_DOMAIN, query, constraint, "Compared the full query interval with both declared endpoints.", "The full query interval is literally contained in the declared domain.")
    return DomainConstraintDiagnostic(observation_id, constraint.variable_id, ConstraintKind.NUMERIC, DomainDiagnosticStatus.PARTIALLY_COMPARABLE, query, constraint, "Compared interval containment without choosing a midpoint or distribution.", "Query interval partially overlaps but is not fully contained in the declared domain.")


def _evaluate_constraint(observation_id: str, constraint: Constraint, query: DomainQueryValue | None) -> DomainConstraintDiagnostic:
    kind = ConstraintKind.NUMERIC if isinstance(constraint, NumericDomainConstraint) else ConstraintKind.CATEGORICAL if isinstance(constraint, CategoricalDomainConstraint) else ConstraintKind.SOURCE_SCALAR
    preliminary = _missing_or_definition(observation_id, constraint, query, kind)
    if preliminary is not None:
        return preliminary
    assert query is not None
    if isinstance(constraint, NumericDomainConstraint):
        if query.kind is DomainQueryKind.NUMERIC_INTERVAL:
            return _interval_against_numeric(observation_id, constraint, query)
        return _point_against_numeric(observation_id, constraint, query)
    if isinstance(constraint, CategoricalDomainConstraint):
        if query.kind not in {DomainQueryKind.CATEGORICAL, DomainQueryKind.IDENTIFIER} or query.category_or_identifier is None:
            return DomainConstraintDiagnostic(observation_id, constraint.variable_id, kind, DomainDiagnosticStatus.DEFINITION_MISMATCH, query, constraint, "Compared query representation with categorical constraint.", "Query is not a categorical or identifier literal.")
        allowed = constraint.allowed_values if constraint.case_sensitive else tuple(item.casefold() for item in constraint.allowed_values)
        supplied = query.category_or_identifier if constraint.case_sensitive else query.category_or_identifier.casefold()
        if supplied not in allowed:
            status = DomainDiagnosticStatus.IDENTIFIER_MISMATCH if query.kind is DomainQueryKind.IDENTIFIER else DomainDiagnosticStatus.CATEGORICAL_MISMATCH
            return DomainConstraintDiagnostic(observation_id, constraint.variable_id, kind, status, query, constraint, "Compared the supplied literal with the declared allowed set.", "Identifier differs from every declared value." if status is DomainDiagnosticStatus.IDENTIFIER_MISMATCH else "Category is not in the declared set.")
        return DomainConstraintDiagnostic(observation_id, constraint.variable_id, kind, DomainDiagnosticStatus.INSIDE_DECLARED_DOMAIN, query, constraint, "Compared the supplied literal with the declared allowed set.", "Literal category or identifier satisfies the declared constraint.")
    if query.kind is not DomainQueryKind.SOURCE_SCALAR_POINT or query.source_scalar_point is None:
        return DomainConstraintDiagnostic(observation_id, constraint.variable_id, kind, DomainDiagnosticStatus.DEFINITION_MISMATCH, query, constraint, "Compared query representation with source-scalar constraint.", "Query is not a source-scalar point.")
    scalar = query.source_scalar_point
    if scalar.reported_unit != constraint.reported_unit:
        return DomainConstraintDiagnostic(observation_id, constraint.variable_id, kind, DomainDiagnosticStatus.INCOMPATIBLE_UNITS, query, constraint, "Compared source-unit strings literally; no conversion is defined.", "Source-scalar reported units differ.")
    if scalar.convention != constraint.convention:
        return DomainConstraintDiagnostic(observation_id, constraint.variable_id, kind, DomainDiagnosticStatus.DEFINITION_MISMATCH, query, constraint, "Compared source-scalar conventions literally.", "Source-scalar conventions differ.")
    value = scalar.value
    if constraint.lower.value is not None and (value < constraint.lower.value or (value == constraint.lower.value and constraint.lower.kind is BoundKind.EXCLUSIVE)):
        reason = "Value is below the source lower boundary." if value < constraint.lower.value else "Value equals the exclusive source lower boundary."
        return DomainConstraintDiagnostic(observation_id, constraint.variable_id, kind, DomainDiagnosticStatus.OUTSIDE_DECLARED_DOMAIN, query, constraint, "Compared the literal source scalar with the lower boundary.", reason)
    if constraint.upper.value is not None and (value > constraint.upper.value or (value == constraint.upper.value and constraint.upper.kind is BoundKind.EXCLUSIVE)):
        reason = "Value is above the source upper boundary." if value > constraint.upper.value else "Value equals the exclusive source upper boundary."
        return DomainConstraintDiagnostic(observation_id, constraint.variable_id, kind, DomainDiagnosticStatus.OUTSIDE_DECLARED_DOMAIN, query, constraint, "Compared the literal source scalar with the upper boundary.", reason)
    return DomainConstraintDiagnostic(observation_id, constraint.variable_id, kind, DomainDiagnosticStatus.INSIDE_DECLARED_DOMAIN, query, constraint, "Compared the source scalar using exact unit, convention, and endpoints.", "Source scalar satisfies the literal declared constraint.")


def diagnose_observation_applicability(observation: PowderPropertyObservation, context: DomainQueryContext, *, record_id: str) -> ApplicabilityEvaluation:
    """Compare one query literally with one observation's declared M02 domain."""

    diagnostics: list[DomainConstraintDiagnostic] = []
    if context.observation_id != observation.record_id:
        diagnostics.append(DomainConstraintDiagnostic(observation.record_id, "observation_id", ConstraintKind.PROPERTY_DEFINITION, DomainDiagnosticStatus.IDENTIFIER_MISMATCH, None, None, "Compared observation identifiers literally.", "Query context identifies a different observation."))
    if context.property_definition_id != observation.property_definition.property_id.value:
        diagnostics.append(DomainConstraintDiagnostic(observation.record_id, "property_definition_id", ConstraintKind.PROPERTY_DEFINITION, DomainDiagnosticStatus.DEFINITION_MISMATCH, None, None, "Compared property-definition identifiers literally.", "Query property definition differs from the observation definition."))
    domain = observation.applicability_domain
    if domain.status is DomainStatus.UNSPECIFIED:
        diagnostics.append(DomainConstraintDiagnostic(observation.record_id, "applicability_domain", ConstraintKind.DOMAIN, DomainDiagnosticStatus.DOMAIN_UNSPECIFIED, None, None, "No constraint comparison performed.", domain.explanation))
        summary = ApplicabilitySummary.NO_DECLARED_DOMAIN_SUPPLIED
    else:
        constraints: tuple[Constraint, ...] = domain.numeric_constraints + domain.categorical_constraints + domain.source_scalar_constraints
        diagnostics.extend(_evaluate_constraint(observation.record_id, item, _query_for(context, item.variable_id)) for item in constraints)
        declared_ids = {item.variable_id for item in constraints}
        for query in context.values:
            if query.variable_id not in declared_ids:
                diagnostics.append(DomainConstraintDiagnostic(observation.record_id, query.variable_id, ConstraintKind.EXTRA_QUERY, DomainDiagnosticStatus.CONSTRAINT_NOT_APPLICABLE, query, None, "No comparison performed because the observation declares no such constraint.", "Query variable is not constrained by this observation."))
        summary = _summarize_diagnostics(diagnostics)
    provenance = Provenance(EvidenceClass.DERIVED_QUANTITY, ValueOrigin.DERIVED, "SRC-M03-DESIGN", ModelMaturity.PROMOTED_MODERN, "M03-DIAG-LITERAL-DOMAIN", (observation.record_id, context.record_id), "Literal applicability only; no suitability or physical-validity claim.")
    return ApplicabilityEvaluation(record_id, observation.record_id, context.record_id, summary, tuple(diagnostics), provenance)
