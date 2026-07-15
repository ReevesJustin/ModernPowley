"""Provenance-aware M02 powder-property and missing-value observations."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from .missing_values import IdentityQualifier, MissingState
from .powder_identity import M02_SCHEMA_ID, _strict_record
from .powder_properties import (
    CategoricalPropertyValue,
    DimensionalPropertyValue,
    IntervalPropertyValue,
    OrdinalPropertyValue,
    PropertyDefinition,
    PropertyValue,
    PropertyValueKind,
    SourceScalarPropertyValue,
    TabularReferencePropertyValue,
    TextualPropertyValue,
    property_value_from_dict,
)
from .property_domains import ApplicabilityDomain
from .provenance import Provenance
from .provenance import ValueOrigin
from .units import Dimension


class TranscriptionStatus(str, Enum):
    """Relationship between an observation and its source representation."""

    DIRECT_SOURCE_RECORD = "direct_source_record"
    VISUALLY_VERIFIED_TRANSCRIPTION = "visually_verified_transcription"
    NORMALIZED_TRANSCRIPTION = "normalized_transcription"
    OCR_UNVERIFIED = "ocr_unverified"
    USER_MEDIATED_PRIMARY_REVIEW = "user_mediated_primary_review"
    NOT_APPLICABLE = "not_applicable"


class ObservationTransformation(str, Enum):
    """Operation used to obtain the stored observation value."""

    DIRECT_REPORTED = "direct_reported"
    TRANSCRIBED = "transcribed"
    UNIT_CONVERTED = "unit_converted"
    ALGEBRAICALLY_DERIVED = "algebraically_derived"
    INFERRED = "inferred"
    FITTED = "fitted"
    ASSERTED = "asserted"


@dataclass(frozen=True, slots=True)
class SourceLocator:
    """Source ID, precise locator, and transcription status."""

    source_id: str
    locator: str
    transcription_status: TranscriptionStatus

    def __post_init__(self) -> None:
        object.__setattr__(self, "transcription_status", TranscriptionStatus(self.transcription_status))
        if not self.source_id.strip() or not self.locator.strip():
            raise ValueError("source ID and locator are required")

    def to_dict(self) -> dict[str, object]:
        return {"source_id": self.source_id, "locator": self.locator, "transcription_status": self.transcription_status.value}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> SourceLocator:
        if set(data) != {"source_id", "locator", "transcription_status"}:
            raise ValueError("malformed source locator fields")
        return cls(str(data["source_id"]), str(data["locator"]), TranscriptionStatus(str(data["transcription_status"])))


@dataclass(frozen=True, slots=True)
class ObservationContext:
    """Explicit known-or-missing method, apparatus, condition, and date fields."""

    test_method: IdentityQualifier
    test_apparatus: IdentityQualifier
    environmental_conditions: IdentityQualifier
    powder_conditioning: IdentityQualifier
    measurement_date_or_publication_era: IdentityQualifier

    def to_dict(self) -> dict[str, object]:
        return {
            "test_method": self.test_method.to_dict(),
            "test_apparatus": self.test_apparatus.to_dict(),
            "environmental_conditions": self.environmental_conditions.to_dict(),
            "powder_conditioning": self.powder_conditioning.to_dict(),
            "measurement_date_or_publication_era": self.measurement_date_or_publication_era.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> ObservationContext:
        fields = {"test_method", "test_apparatus", "environmental_conditions", "powder_conditioning", "measurement_date_or_publication_era"}
        if set(data) != fields:
            raise ValueError("malformed observation context fields")
        return cls(*(IdentityQualifier.from_dict(data[field]) for field in ("test_method", "test_apparatus", "environmental_conditions", "powder_conditioning", "measurement_date_or_publication_era")))


_KIND_TO_CLASS = {
    PropertyValueKind.DIMENSIONAL: DimensionalPropertyValue,
    PropertyValueKind.CATEGORICAL: CategoricalPropertyValue,
    PropertyValueKind.ORDINAL: OrdinalPropertyValue,
    PropertyValueKind.TEXTUAL: TextualPropertyValue,
    PropertyValueKind.INTERVAL: IntervalPropertyValue,
    PropertyValueKind.TABULAR_REFERENCE: TabularReferencePropertyValue,
    PropertyValueKind.SOURCE_SPECIFIC: SourceScalarPropertyValue,
}


@dataclass(frozen=True, slots=True)
class PowderPropertyObservation:
    """One source-bounded property observation for one powder identity."""

    record_id: str
    powder_identity_id: str
    property_definition: PropertyDefinition
    value: PropertyValue
    provenance: Provenance
    source_locator: SourceLocator
    transformation: ObservationTransformation
    reported_wording: str
    uncertainty_qualification: IdentityQualifier
    context: ObservationContext
    applicability_domain: ApplicabilityDomain
    dependency_record_ids: tuple[str, ...]
    qualifications: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "transformation", ObservationTransformation(self.transformation))
        if not self.record_id.strip() or not self.powder_identity_id.strip() or not self.reported_wording.strip():
            raise ValueError("observation identity, powder identity, and source wording are required")
        expected_class = _KIND_TO_CLASS[self.property_definition.value_kind]
        if not isinstance(self.value, expected_class):
            raise ValueError(f"property {self.property_definition.property_id.value} requires {self.property_definition.value_kind.value} value")
        if isinstance(self.value, DimensionalPropertyValue):
            expected = self.property_definition.expected_dimension
            if expected is None:
                raise ValueError("dimensional property requires expected_dimension")
            if self.value.physical_value.quantity.dimension is not expected:
                raise ValueError("property value dimension does not match property definition")
            if self.property_definition.convention_required and not self.value.convention.strip():
                raise ValueError("property definition requires an explicit convention")
        if isinstance(self.value, IntervalPropertyValue):
            expected = self.property_definition.expected_dimension
            if expected is not None and self.value.lower.quantity.dimension is not expected:
                raise ValueError("property interval dimension does not match definition")
        if self.provenance.source_id != self.source_locator.source_id:
            raise ValueError("observation provenance and source locator must identify the same source")
        if self.transformation in {
            ObservationTransformation.UNIT_CONVERTED,
            ObservationTransformation.ALGEBRAICALLY_DERIVED,
            ObservationTransformation.INFERRED,
            ObservationTransformation.FITTED,
        } and not self.dependency_record_ids:
            raise ValueError("transformed observation requires dependency record IDs")
        expected_origins = {
            ObservationTransformation.TRANSCRIBED: ValueOrigin.TRANSCRIBED,
            ObservationTransformation.UNIT_CONVERTED: ValueOrigin.DERIVED,
            ObservationTransformation.ALGEBRAICALLY_DERIVED: ValueOrigin.DERIVED,
            ObservationTransformation.INFERRED: ValueOrigin.INFERRED,
            ObservationTransformation.FITTED: ValueOrigin.FITTED,
        }
        expected_origin = expected_origins.get(self.transformation)
        if expected_origin is not None and self.provenance.origin is not expected_origin:
            raise ValueError("observation transformation and provenance origin disagree")
        if self.provenance.origin is ValueOrigin.DERIVED and tuple(self.provenance.input_record_ids) != self.dependency_record_ids:
            raise ValueError("derived provenance inputs must equal observation dependency IDs")
        if any(not item.strip() for item in self.dependency_record_ids + self.qualifications):
            raise ValueError("observation dependencies and qualifications must be nonblank")

    def to_dict(self) -> dict[str, object]:
        return {
            "schema": M02_SCHEMA_ID,
            "record_type": "powder_property_observation",
            "record_id": self.record_id,
            "powder_identity_id": self.powder_identity_id,
            "property_definition": self.property_definition.to_dict(),
            "value": self.value.to_dict(),
            "provenance": self.provenance.to_dict(),
            "source_locator": self.source_locator.to_dict(),
            "transformation": self.transformation.value,
            "reported_wording": self.reported_wording,
            "uncertainty_qualification": self.uncertainty_qualification.to_dict(),
            "context": self.context.to_dict(),
            "applicability_domain": self.applicability_domain.to_dict(),
            "dependency_record_ids": list(self.dependency_record_ids),
            "qualifications": list(self.qualifications),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> PowderPropertyObservation:
        fields = {"powder_identity_id", "property_definition", "value", "provenance", "source_locator", "transformation", "reported_wording", "uncertainty_qualification", "context", "applicability_domain", "dependency_record_ids", "qualifications"}
        _strict_record(data, "powder_property_observation", fields)
        dependencies = data["dependency_record_ids"]
        qualifications = data["qualifications"]
        if not isinstance(dependencies, list) or not all(isinstance(item, str) for item in dependencies) or not isinstance(qualifications, list) or not all(isinstance(item, str) for item in qualifications):
            raise TypeError("observation dependency and qualification lists are malformed")
        return cls(
            str(data["record_id"]), str(data["powder_identity_id"]),
            PropertyDefinition.from_dict(data["property_definition"]),
            property_value_from_dict(data["value"]), Provenance.from_dict(data["provenance"]),
            SourceLocator.from_dict(data["source_locator"]),
            ObservationTransformation(str(data["transformation"])), str(data["reported_wording"]),
            IdentityQualifier.from_dict(data["uncertainty_qualification"]),
            ObservationContext.from_dict(data["context"]), ApplicabilityDomain.from_dict(data["applicability_domain"]),
            tuple(dependencies), tuple(qualifications),
        )


@dataclass(frozen=True, slots=True)
class MissingPropertyObservation:
    """Semantic assertion that one property value is unavailable."""

    record_id: str
    powder_identity_id: str
    property_definition: PropertyDefinition
    missing_state: MissingState
    provenance: Provenance
    source_locator: SourceLocator
    explanation: str
    review_context: str
    resolvable_by_later_review: bool
    related_record_ids: tuple[str, ...]
    applicability_domain: ApplicabilityDomain

    def __post_init__(self) -> None:
        object.__setattr__(self, "missing_state", MissingState(self.missing_state))
        if not self.record_id.strip() or not self.powder_identity_id.strip() or not self.explanation.strip() or not self.review_context.strip():
            raise ValueError("missing observation identity, powder identity, explanation, and review context are required")
        if self.provenance.source_id != self.source_locator.source_id:
            raise ValueError("missing assertion provenance and locator must identify the same source")
        if self.missing_state is MissingState.CONFLICTING_EVIDENCE and not self.related_record_ids:
            raise ValueError("conflicting-evidence missing state requires related records")
        if any(not item.strip() for item in self.related_record_ids):
            raise ValueError("related record IDs must be nonblank")

    def to_dict(self) -> dict[str, object]:
        return {
            "schema": M02_SCHEMA_ID,
            "record_type": "missing_property_observation",
            "record_id": self.record_id,
            "powder_identity_id": self.powder_identity_id,
            "property_definition": self.property_definition.to_dict(),
            "missing_state": self.missing_state.value,
            "provenance": self.provenance.to_dict(),
            "source_locator": self.source_locator.to_dict(),
            "explanation": self.explanation,
            "review_context": self.review_context,
            "resolvable_by_later_review": self.resolvable_by_later_review,
            "related_record_ids": list(self.related_record_ids),
            "applicability_domain": self.applicability_domain.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> MissingPropertyObservation:
        fields = {"powder_identity_id", "property_definition", "missing_state", "provenance", "source_locator", "explanation", "review_context", "resolvable_by_later_review", "related_record_ids", "applicability_domain"}
        _strict_record(data, "missing_property_observation", fields)
        related = data["related_record_ids"]
        if not isinstance(related, list) or not all(isinstance(item, str) for item in related) or not isinstance(data["resolvable_by_later_review"], bool):
            raise TypeError("missing-observation related records or resolvability are malformed")
        return cls(
            str(data["record_id"]), str(data["powder_identity_id"]),
            PropertyDefinition.from_dict(data["property_definition"]), MissingState(str(data["missing_state"])),
            Provenance.from_dict(data["provenance"]), SourceLocator.from_dict(data["source_locator"]),
            str(data["explanation"]), str(data["review_context"]), data["resolvable_by_later_review"],
            tuple(related), ApplicabilityDomain.from_dict(data["applicability_domain"]),
        )
