"""Descriptive M02 comparison that never resolves or selects observations."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from .powder_identity import M02_SCHEMA_ID, PowderIdentity, _strict_record
from .powder_properties import (
    DimensionalPropertyValue,
    IntervalPropertyValue,
    SourceScalarPropertyValue,
)
from .property_domains import DomainStatus
from .property_observations import PowderPropertyObservation
from .provenance import EvidenceClass, ModelMaturity, Provenance, ValueOrigin
from .uncertainty import UncertaintyKind


class IdentityComparison(str, Enum):
    """Literal identity-record and lot relationship between observations."""

    SAME_IDENTITY_RECORD = "same_identity_record"
    DIFFERENT_IDENTITY_RECORD = "different_identity_record"
    DIFFERENT_KNOWN_LOTS = "different_known_lots"
    INSUFFICIENT_IDENTITY_DETAIL = "insufficient_identity_detail"


class DefinitionComparison(str, Enum):
    """Whether property definitions are identical or merely similarly named."""

    SAME_DEFINITION = "same_definition"
    DIFFERENT_DEFINITION = "different_definition"


class UnitComparison(str, Enum):
    """Literal unit comparability without conversion outside M01."""

    M01_CONVERTIBLE = "m01_convertible"
    SAME_SOURCE_UNIT_AND_DEFINITION = "same_source_unit_and_definition"
    NONCONVERTIBLE = "nonconvertible"
    NOT_NUMERIC = "not_numeric"


class NumericComparison(str, Enum):
    """Descriptive numeric relationship with no preferred value."""

    EQUAL_REPORTED_VALUES = "equal_reported_values"
    AGREE_WITHIN_DECLARED_UNCERTAINTY = "agree_within_declared_uncertainty"
    OVERLAPPING_REPORTED_INTERVALS = "overlapping_reported_intervals"
    NUMERICALLY_DIFFERENT = "numerically_different"
    INSUFFICIENT_FOR_NUMERIC_COMPARISON = "insufficient_for_numeric_comparison"


class DomainComparison(str, Enum):
    """Literal relationship between retained domain records."""

    SAME_DECLARED_DOMAIN = "same_declared_domain"
    DIFFERENT_DECLARED_DOMAINS = "different_declared_domains"
    ONE_OR_BOTH_UNSPECIFIED = "one_or_both_unspecified"


@dataclass(frozen=True, slots=True)
class ConflictComparison:
    """Neutral comparison retaining both observation IDs and no winner."""

    record_id: str
    left_observation_id: str
    right_observation_id: str
    identity_comparison: IdentityComparison
    definition_comparison: DefinitionComparison
    unit_comparison: UnitComparison
    numeric_comparison: NumericComparison
    domain_comparison: DomainComparison
    provenance: Provenance
    reasons: tuple[str, ...]

    def __post_init__(self) -> None:
        for field, enum_type in (
            ("identity_comparison", IdentityComparison),
            ("definition_comparison", DefinitionComparison),
            ("unit_comparison", UnitComparison),
            ("numeric_comparison", NumericComparison),
            ("domain_comparison", DomainComparison),
        ):
            object.__setattr__(self, field, enum_type(getattr(self, field)))
        if not self.record_id.strip() or not self.left_observation_id.strip() or not self.right_observation_id.strip():
            raise ValueError("comparison and observation identities are required")
        if self.left_observation_id == self.right_observation_id:
            raise ValueError("conflict comparison requires two distinct observations")
        if not self.reasons:
            raise ValueError("comparison requires descriptive reasons")

    def to_dict(self) -> dict[str, object]:
        return {
            "schema": M02_SCHEMA_ID,
            "record_type": "conflict_comparison",
            "record_id": self.record_id,
            "left_observation_id": self.left_observation_id,
            "right_observation_id": self.right_observation_id,
            "identity_comparison": self.identity_comparison.value,
            "definition_comparison": self.definition_comparison.value,
            "unit_comparison": self.unit_comparison.value,
            "numeric_comparison": self.numeric_comparison.value,
            "domain_comparison": self.domain_comparison.value,
            "provenance": self.provenance.to_dict(),
            "reasons": list(self.reasons),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> ConflictComparison:
        fields = {"left_observation_id", "right_observation_id", "identity_comparison", "definition_comparison", "unit_comparison", "numeric_comparison", "domain_comparison", "provenance", "reasons"}
        _strict_record(data, "conflict_comparison", fields)
        reasons = data["reasons"]
        if not isinstance(reasons, list) or not all(isinstance(item, str) for item in reasons):
            raise TypeError("comparison reasons must be a string list")
        return cls(str(data["record_id"]), str(data["left_observation_id"]), str(data["right_observation_id"]), IdentityComparison(str(data["identity_comparison"])), DefinitionComparison(str(data["definition_comparison"])), UnitComparison(str(data["unit_comparison"])), NumericComparison(str(data["numeric_comparison"])), DomainComparison(str(data["domain_comparison"])), Provenance.from_dict(data["provenance"]), tuple(reasons))


def _identity_comparison(left: PowderPropertyObservation, right: PowderPropertyObservation, left_identity: PowderIdentity | None, right_identity: PowderIdentity | None) -> IdentityComparison:
    if left.powder_identity_id == right.powder_identity_id:
        return IdentityComparison.SAME_IDENTITY_RECORD
    if left_identity is None or right_identity is None:
        return IdentityComparison.INSUFFICIENT_IDENTITY_DETAIL
    if left_identity.record_id != left.powder_identity_id or right_identity.record_id != right.powder_identity_id:
        raise ValueError("identity records must match their observations")
    left_lot = left_identity.lot_or_batch.value
    right_lot = right_identity.lot_or_batch.value
    if left_lot is not None and right_lot is not None and left_lot != right_lot:
        return IdentityComparison.DIFFERENT_KNOWN_LOTS
    return IdentityComparison.DIFFERENT_IDENTITY_RECORD


def _uncertainty_interval(value: DimensionalPropertyValue) -> tuple[float, float] | None:
    physical = value.physical_value
    uncertainty = physical.uncertainty
    center = physical.quantity.si_value
    if uncertainty.kind is UncertaintyKind.SYMMETRIC_ABSOLUTE and uncertainty.magnitude is not None:
        magnitude = uncertainty.magnitude.si_value
        return center - magnitude, center + magnitude
    if uncertainty.kind is UncertaintyKind.BOUNDED_INTERVAL and uncertainty.lower is not None and uncertainty.upper is not None:
        return uncertainty.lower.si_value, uncertainty.upper.si_value
    return None


def _numeric_comparison(left: PowderPropertyObservation, right: PowderPropertyObservation) -> tuple[UnitComparison, NumericComparison, str]:
    lv = left.value
    rv = right.value
    if isinstance(lv, DimensionalPropertyValue) and isinstance(rv, DimensionalPropertyValue):
        if lv.physical_value.quantity.dimension is not rv.physical_value.quantity.dimension:
            return UnitComparison.NONCONVERTIBLE, NumericComparison.INSUFFICIENT_FOR_NUMERIC_COMPARISON, "M01 dimensions differ"
        left_value = lv.physical_value.quantity.si_value
        right_value = rv.physical_value.quantity.si_value
        if left_value == right_value:
            return UnitComparison.M01_CONVERTIBLE, NumericComparison.EQUAL_REPORTED_VALUES, "canonical M01 values are equal"
        left_interval = _uncertainty_interval(lv)
        right_interval = _uncertainty_interval(rv)
        if left_interval is not None and right_interval is not None and max(left_interval[0], right_interval[0]) <= min(left_interval[1], right_interval[1]):
            return UnitComparison.M01_CONVERTIBLE, NumericComparison.AGREE_WITHIN_DECLARED_UNCERTAINTY, "declared uncertainty intervals overlap"
        return UnitComparison.M01_CONVERTIBLE, NumericComparison.NUMERICALLY_DIFFERENT, "canonical M01 values differ"
    if isinstance(lv, SourceScalarPropertyValue) and isinstance(rv, SourceScalarPropertyValue):
        same_definition = (lv.reported_unit, lv.convention, lv.definition) == (rv.reported_unit, rv.convention, rv.definition)
        if not same_definition:
            return UnitComparison.NONCONVERTIBLE, NumericComparison.INSUFFICIENT_FOR_NUMERIC_COMPARISON, "source scalar unit, convention, or definition differs"
        relation = NumericComparison.EQUAL_REPORTED_VALUES if lv.value == rv.value else NumericComparison.NUMERICALLY_DIFFERENT
        return UnitComparison.SAME_SOURCE_UNIT_AND_DEFINITION, relation, "source scalars compared without unit conversion"
    if isinstance(lv, IntervalPropertyValue) and isinstance(rv, IntervalPropertyValue):
        if lv.lower.quantity.dimension is not rv.lower.quantity.dimension:
            return UnitComparison.NONCONVERTIBLE, NumericComparison.INSUFFICIENT_FOR_NUMERIC_COMPARISON, "interval dimensions differ"
        overlap = max(lv.lower.quantity.si_value, rv.lower.quantity.si_value) <= min(lv.upper.quantity.si_value, rv.upper.quantity.si_value)
        relation = NumericComparison.OVERLAPPING_REPORTED_INTERVALS if overlap else NumericComparison.NUMERICALLY_DIFFERENT
        return UnitComparison.M01_CONVERTIBLE, relation, "reported interval overlap checked literally"
    return UnitComparison.NOT_NUMERIC, NumericComparison.INSUFFICIENT_FOR_NUMERIC_COMPARISON, "one or both values are nonnumeric or use different tagged representations"


def compare_property_observations(left: PowderPropertyObservation, right: PowderPropertyObservation, *, result_id: str, left_identity: PowderIdentity | None = None, right_identity: PowderIdentity | None = None) -> ConflictComparison:
    """Describe two retained observations without choosing or resolving either."""

    definition = DefinitionComparison.SAME_DEFINITION if left.property_definition == right.property_definition else DefinitionComparison.DIFFERENT_DEFINITION
    units, numeric, numeric_reason = _numeric_comparison(left, right)
    if definition is DefinitionComparison.DIFFERENT_DEFINITION:
        numeric = NumericComparison.INSUFFICIENT_FOR_NUMERIC_COMPARISON
    if left.applicability_domain.status is DomainStatus.UNSPECIFIED or right.applicability_domain.status is DomainStatus.UNSPECIFIED:
        domain = DomainComparison.ONE_OR_BOTH_UNSPECIFIED
    elif left.applicability_domain == right.applicability_domain:
        domain = DomainComparison.SAME_DECLARED_DOMAIN
    else:
        domain = DomainComparison.DIFFERENT_DECLARED_DOMAINS
    reasons = (
        f"identity={_identity_comparison(left, right, left_identity, right_identity).value}",
        f"definition={definition.value}",
        numeric_reason,
        f"domain={domain.value}",
        "no preferred or selected observation is produced",
    )
    provenance = Provenance(
        EvidenceClass.DERIVED_QUANTITY,
        ValueOrigin.DERIVED,
        "SRC-M02-DESIGN",
        ModelMaturity.PROMOTED_MODERN,
        "M02-COMPARE-PROPERTY-OBSERVATIONS",
        (left.record_id, right.record_id),
    )
    return ConflictComparison(result_id, left.record_id, right.record_id, _identity_comparison(left, right, left_identity, right_identity), definition, units, numeric, domain, provenance, reasons)
