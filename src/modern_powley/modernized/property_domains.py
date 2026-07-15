"""Literal M02 applicability domains with no interpolation or extrapolation."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import isfinite
from numbers import Real
from typing import Any, Mapping

from .records import PhysicalValue
from .units import Quantity, require_dimension


class DomainStatus(str, Enum):
    """Whether a source domain is declared or explicitly unspecified."""

    UNSPECIFIED = "unspecified"
    DECLARED = "declared"


class BoundKind(str, Enum):
    """Endpoint inclusion or absence for a numeric domain bound."""

    UNBOUNDED = "unbounded"
    INCLUSIVE = "inclusive"
    EXCLUSIVE = "exclusive"


@dataclass(frozen=True, slots=True)
class DomainBound:
    """One unbounded, inclusive, or exclusive domain endpoint."""

    kind: BoundKind
    value: PhysicalValue | None

    def __post_init__(self) -> None:
        object.__setattr__(self, "kind", BoundKind(self.kind))
        if (self.kind is BoundKind.UNBOUNDED) != (self.value is None):
            raise ValueError("unbounded domain endpoint has no value; bounded endpoint requires one")

    def to_dict(self) -> dict[str, object]:
        return {"kind": self.kind.value, "value": None if self.value is None else self.value.to_dict()}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> DomainBound:
        if set(data) != {"kind", "value"}:
            raise ValueError("malformed domain bound fields")
        return cls(BoundKind(str(data["kind"])), None if data["value"] is None else PhysicalValue.from_dict(data["value"]))


@dataclass(frozen=True, slots=True)
class NumericDomainConstraint:
    """One source-defined numeric range with literal boundary semantics."""

    variable_id: str
    definition: str
    lower: DomainBound
    upper: DomainBound

    def __post_init__(self) -> None:
        if not self.variable_id.strip() or not self.definition.strip():
            raise ValueError("domain variable identity and definition are required")
        if self.lower.value is None and self.upper.value is None:
            raise ValueError("numeric domain constraint cannot be unbounded at both ends")
        if self.lower.value is not None and self.upper.value is not None:
            require_dimension(self.upper.value.quantity, self.lower.value.quantity.dimension, "domain upper bound")
            if self.lower.value.quantity.si_value > self.upper.value.quantity.si_value:
                raise ValueError("domain bounds must be ordered")

    @property
    def dimension(self):
        """Return the declared bound dimension."""

        value = self.lower.value or self.upper.value
        assert value is not None
        return value.quantity.dimension

    def to_dict(self) -> dict[str, object]:
        return {"variable_id": self.variable_id, "definition": self.definition, "lower": self.lower.to_dict(), "upper": self.upper.to_dict()}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> NumericDomainConstraint:
        if set(data) != {"variable_id", "definition", "lower", "upper"}:
            raise ValueError("malformed numeric domain fields")
        return cls(str(data["variable_id"]), str(data["definition"]), DomainBound.from_dict(data["lower"]), DomainBound.from_dict(data["upper"]))


@dataclass(frozen=True, slots=True)
class SourceScalarDomainBound:
    """Endpoint for a source scalar whose unit has no admitted conversion."""

    kind: BoundKind
    value: float | None

    def __post_init__(self) -> None:
        object.__setattr__(self, "kind", BoundKind(self.kind))
        if (self.kind is BoundKind.UNBOUNDED) != (self.value is None):
            raise ValueError("unbounded source endpoint has no value; bounded endpoint requires one")
        if self.value is not None:
            if isinstance(self.value, bool) or not isinstance(self.value, Real) or not isfinite(float(self.value)):
                raise ValueError("source domain bound must be finite")
            object.__setattr__(self, "value", float(self.value))

    def to_dict(self) -> dict[str, object]:
        return {"kind": self.kind.value, "value": self.value}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> SourceScalarDomainBound:
        if set(data) != {"kind", "value"}:
            raise ValueError("malformed source domain bound fields")
        return cls(BoundKind(str(data["kind"])), data["value"])


@dataclass(frozen=True, slots=True)
class SourceScalarDomainConstraint:
    """Literal range in one source unit and convention without conversion."""

    variable_id: str
    definition: str
    reported_unit: str
    convention: str
    lower: SourceScalarDomainBound
    upper: SourceScalarDomainBound

    def __post_init__(self) -> None:
        if not all(value.strip() for value in (self.variable_id, self.definition, self.reported_unit, self.convention)):
            raise ValueError("source scalar domain identity, definition, unit, and convention are required")
        if self.lower.value is None and self.upper.value is None:
            raise ValueError("source scalar domain cannot be unbounded at both ends")
        if self.lower.value is not None and self.upper.value is not None and self.lower.value > self.upper.value:
            raise ValueError("source scalar domain bounds must be ordered")

    def to_dict(self) -> dict[str, object]:
        return {"variable_id": self.variable_id, "definition": self.definition, "reported_unit": self.reported_unit, "convention": self.convention, "lower": self.lower.to_dict(), "upper": self.upper.to_dict()}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> SourceScalarDomainConstraint:
        fields = {"variable_id", "definition", "reported_unit", "convention", "lower", "upper"}
        if set(data) != fields:
            raise ValueError("malformed source scalar domain fields")
        return cls(str(data["variable_id"]), str(data["definition"]), str(data["reported_unit"]), str(data["convention"]), SourceScalarDomainBound.from_dict(data["lower"]), SourceScalarDomainBound.from_dict(data["upper"]))


@dataclass(frozen=True, slots=True)
class SourceScalarDomainValue:
    """Query value in a literal source unit and convention."""

    value: float
    reported_unit: str
    convention: str

    def __post_init__(self) -> None:
        if isinstance(self.value, bool) or not isinstance(self.value, Real) or not isfinite(float(self.value)):
            raise ValueError("source scalar domain value must be finite")
        object.__setattr__(self, "value", float(self.value))
        if not self.reported_unit.strip() or not self.convention.strip():
            raise ValueError("source scalar domain value requires unit and convention")


@dataclass(frozen=True, slots=True)
class CategoricalDomainConstraint:
    """Literal allowed categories for one source-defined domain variable."""

    variable_id: str
    definition: str
    allowed_values: tuple[str, ...]
    case_sensitive: bool = True

    def __post_init__(self) -> None:
        if not self.variable_id.strip() or not self.definition.strip() or not self.allowed_values:
            raise ValueError("categorical domain identity, definition, and values are required")
        if any(not value.strip() for value in self.allowed_values) or len(set(self.allowed_values)) != len(self.allowed_values):
            raise ValueError("categorical domain values must be unique and nonblank")

    def to_dict(self) -> dict[str, object]:
        return {"variable_id": self.variable_id, "definition": self.definition, "allowed_values": list(self.allowed_values), "case_sensitive": self.case_sensitive}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> CategoricalDomainConstraint:
        if set(data) != {"variable_id", "definition", "allowed_values", "case_sensitive"}:
            raise ValueError("malformed categorical domain fields")
        values = data["allowed_values"]
        if not isinstance(values, list) or not all(isinstance(value, str) for value in values) or not isinstance(data["case_sensitive"], bool):
            raise TypeError("categorical domain values and case_sensitive are malformed")
        return cls(str(data["variable_id"]), str(data["definition"]), tuple(values), data["case_sensitive"])


@dataclass(frozen=True, slots=True)
class ApplicabilityDomain:
    """An explicitly unspecified or source-declared applicability domain."""

    status: DomainStatus
    numeric_constraints: tuple[NumericDomainConstraint, ...]
    categorical_constraints: tuple[CategoricalDomainConstraint, ...]
    explanation: str
    source_scalar_constraints: tuple[SourceScalarDomainConstraint, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "status", DomainStatus(self.status))
        if not self.explanation.strip():
            raise ValueError("domain explanation is required")
        if self.status is DomainStatus.UNSPECIFIED and (self.numeric_constraints or self.categorical_constraints or self.source_scalar_constraints):
            raise ValueError("unspecified domain cannot contain constraints")
        if self.status is DomainStatus.DECLARED and not (self.numeric_constraints or self.categorical_constraints or self.source_scalar_constraints):
            raise ValueError("declared domain requires at least one constraint")
        ids = [item.variable_id for item in self.numeric_constraints + self.categorical_constraints + self.source_scalar_constraints]
        if len(ids) != len(set(ids)):
            raise ValueError("domain variable IDs must be unique")

    @classmethod
    def unspecified(cls, explanation: str) -> ApplicabilityDomain:
        """Create a domain that is explicitly unknown, never universal."""

        return cls(DomainStatus.UNSPECIFIED, (), (), explanation, ())

    def to_dict(self) -> dict[str, object]:
        return {"status": self.status.value, "numeric_constraints": [item.to_dict() for item in self.numeric_constraints], "categorical_constraints": [item.to_dict() for item in self.categorical_constraints], "source_scalar_constraints": [item.to_dict() for item in self.source_scalar_constraints], "explanation": self.explanation}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> ApplicabilityDomain:
        if set(data) != {"status", "numeric_constraints", "categorical_constraints", "source_scalar_constraints", "explanation"}:
            raise ValueError("malformed applicability domain fields")
        numeric = data["numeric_constraints"]
        categorical = data["categorical_constraints"]
        source_scalar = data["source_scalar_constraints"]
        if not isinstance(numeric, list) or not isinstance(categorical, list) or not isinstance(source_scalar, list):
            raise TypeError("domain constraints must be lists")
        return cls(DomainStatus(str(data["status"])), tuple(NumericDomainConstraint.from_dict(item) for item in numeric), tuple(CategoricalDomainConstraint.from_dict(item) for item in categorical), str(data["explanation"]), tuple(SourceScalarDomainConstraint.from_dict(item) for item in source_scalar))


class DomainMembershipStatus(str, Enum):
    """Literal result of testing supplied values against one declared domain."""

    WITHIN_DECLARED_DOMAIN = "within_declared_domain"
    OUTSIDE_DECLARED_DOMAIN = "outside_declared_domain"
    INDETERMINATE_UNSPECIFIED_DOMAIN = "indeterminate_unspecified_domain"
    INDETERMINATE_MISSING_INPUT = "indeterminate_missing_input"
    INCOMPATIBLE_DIMENSION = "incompatible_dimension"


@dataclass(frozen=True, slots=True)
class DomainMembership:
    """Descriptive domain-membership result with no selection consequence."""

    status: DomainMembershipStatus
    reasons: tuple[str, ...]


def test_domain_membership(domain: ApplicabilityDomain, *, numeric_values: Mapping[str, Quantity], categorical_values: Mapping[str, str], source_scalar_values: Mapping[str, SourceScalarDomainValue] | None = None) -> DomainMembership:
    """Perform literal boundary checks only; never interpolate or extrapolate."""

    if domain.status is DomainStatus.UNSPECIFIED:
        return DomainMembership(DomainMembershipStatus.INDETERMINATE_UNSPECIFIED_DOMAIN, (domain.explanation,))
    source_scalar_values = {} if source_scalar_values is None else source_scalar_values
    missing = [item.variable_id for item in domain.numeric_constraints if item.variable_id not in numeric_values]
    missing += [item.variable_id for item in domain.categorical_constraints if item.variable_id not in categorical_values]
    missing += [item.variable_id for item in domain.source_scalar_constraints if item.variable_id not in source_scalar_values]
    if missing:
        return DomainMembership(DomainMembershipStatus.INDETERMINATE_MISSING_INPUT, tuple(f"missing {item}" for item in missing))
    reasons: list[str] = []
    for item in domain.numeric_constraints:
        value = numeric_values[item.variable_id]
        if value.dimension is not item.dimension:
            return DomainMembership(DomainMembershipStatus.INCOMPATIBLE_DIMENSION, (f"{item.variable_id} dimension mismatch",))
        si = value.si_value
        if item.lower.value is not None:
            bound = item.lower.value.quantity.si_value
            if si < bound or (si == bound and item.lower.kind is BoundKind.EXCLUSIVE):
                reasons.append(f"{item.variable_id} below lower boundary")
        if item.upper.value is not None:
            bound = item.upper.value.quantity.si_value
            if si > bound or (si == bound and item.upper.kind is BoundKind.EXCLUSIVE):
                reasons.append(f"{item.variable_id} above upper boundary")
    for item in domain.categorical_constraints:
        supplied = categorical_values[item.variable_id]
        allowed = item.allowed_values if item.case_sensitive else tuple(value.casefold() for value in item.allowed_values)
        candidate = supplied if item.case_sensitive else supplied.casefold()
        if candidate not in allowed:
            reasons.append(f"{item.variable_id} category outside declared set")
    for item in domain.source_scalar_constraints:
        supplied = source_scalar_values[item.variable_id]
        if (supplied.reported_unit, supplied.convention) != (item.reported_unit, item.convention):
            return DomainMembership(DomainMembershipStatus.INCOMPATIBLE_DIMENSION, (f"{item.variable_id} source unit or convention mismatch",))
        value = supplied.value
        if item.lower.value is not None and (value < item.lower.value or (value == item.lower.value and item.lower.kind is BoundKind.EXCLUSIVE)):
            reasons.append(f"{item.variable_id} below lower source boundary")
        if item.upper.value is not None and (value > item.upper.value or (value == item.upper.value and item.upper.kind is BoundKind.EXCLUSIVE)):
            reasons.append(f"{item.variable_id} above upper source boundary")
    if reasons:
        return DomainMembership(DomainMembershipStatus.OUTSIDE_DECLARED_DOMAIN, tuple(reasons))
    return DomainMembership(DomainMembershipStatus.WITHIN_DECLARED_DOMAIN, ("all supplied values satisfy literal declared constraints",))
