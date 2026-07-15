"""Exact M04 evidence references and immutable evaluation contexts."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from .domain_diagnostics import DomainConstraintDiagnostic, QueryInterval
from .input_completeness import CompletenessDiagnostic
from .missing_values import IdentityQualifier, MissingState
from .property_observations import SourceLocator
from .provenance import Provenance
from .screening_criteria import M04_SCHEMA_ID, _strict, _text
from .units import Quantity


class EvidenceReferenceKind(str, Enum):
    """Exact retained-record kind; no collection lookup is implied."""

    M01_QUANTITY = "m01_quantity"
    M02_OBSERVATION = "m02_observation"
    M02_MISSING_OBSERVATION = "m02_missing_observation"
    M02_CONFLICT = "m02_conflict"
    M03_COMPLETENESS_DIAGNOSTIC = "m03_completeness_diagnostic"
    M03_DOMAIN_DIAGNOSTIC = "m03_domain_diagnostic"
    CONTROLLED_CATEGORY = "controlled_category"
    EXPLICIT_IDENTIFIER = "explicit_identifier"


class EvidenceValueKind(str, Enum):
    """Tagged literal value retained by an evidence reference."""

    PRESENCE = "presence"
    NUMERIC_POINT = "numeric_point"
    NUMERIC_INTERVAL = "numeric_interval"
    CATEGORY = "category"
    IDENTIFIER = "identifier"
    MISSING_STATE = "missing_state"
    DIAGNOSTIC_CLASSIFICATION = "diagnostic_classification"
    CONFLICT_DECLARATION = "conflict_declaration"


class ConflictDeclaration(str, Enum):
    """Descriptive conflict state with no automatic resolution."""

    NO_RECORDED_CONFLICT = "no_recorded_conflict"
    CONFLICT_PRESENT = "conflict_present"
    UNRESOLVED = "unresolved"


@dataclass(frozen=True, slots=True)
class EvidenceReference:
    """One exact supplied record and one explicitly tagged literal value."""

    reference_id: str
    reference_kind: EvidenceReferenceKind
    source_record_id: str
    definition_id: str
    value_kind: EvidenceValueKind
    provenance: Provenance
    source_locator: SourceLocator
    quantity: Quantity | None = None
    interval: QueryInterval | None = None
    literal_value: str | None = None
    missing_state: MissingState | None = None
    conflict_declaration: ConflictDeclaration | None = None
    related_record_ids: tuple[str, ...] = ()
    notes: str = ""

    def __post_init__(self) -> None:
        for value, name in (
            (self.reference_id, "reference_id"),
            (self.source_record_id, "source_record_id"),
            (self.definition_id, "definition_id"),
        ):
            _text(value, name)
        object.__setattr__(self, "reference_kind", EvidenceReferenceKind(self.reference_kind))
        object.__setattr__(self, "value_kind", EvidenceValueKind(self.value_kind))
        if self.missing_state is not None:
            object.__setattr__(self, "missing_state", MissingState(self.missing_state))
        if self.conflict_declaration is not None:
            object.__setattr__(
                self, "conflict_declaration", ConflictDeclaration(self.conflict_declaration)
            )
        if self.provenance.source_id != self.source_locator.source_id:
            raise ValueError("evidence provenance and source locator must match")
        payloads = (
            self.quantity,
            self.interval,
            self.literal_value,
            self.missing_state,
            self.conflict_declaration,
        )
        expected_counts = {
            EvidenceValueKind.PRESENCE: 0,
            EvidenceValueKind.NUMERIC_POINT: 1,
            EvidenceValueKind.NUMERIC_INTERVAL: 1,
            EvidenceValueKind.CATEGORY: 1,
            EvidenceValueKind.IDENTIFIER: 1,
            EvidenceValueKind.MISSING_STATE: 1,
            EvidenceValueKind.DIAGNOSTIC_CLASSIFICATION: 1,
            EvidenceValueKind.CONFLICT_DECLARATION: 1,
        }
        if sum(item is not None for item in payloads) != expected_counts[self.value_kind]:
            raise ValueError("evidence value kind and tagged payload disagree")
        expected_payload = {
            EvidenceValueKind.NUMERIC_POINT: self.quantity,
            EvidenceValueKind.NUMERIC_INTERVAL: self.interval,
            EvidenceValueKind.CATEGORY: self.literal_value,
            EvidenceValueKind.IDENTIFIER: self.literal_value,
            EvidenceValueKind.MISSING_STATE: self.missing_state,
            EvidenceValueKind.DIAGNOSTIC_CLASSIFICATION: self.literal_value,
            EvidenceValueKind.CONFLICT_DECLARATION: self.conflict_declaration,
        }.get(self.value_kind)
        if self.value_kind is not EvidenceValueKind.PRESENCE and expected_payload is None:
            raise ValueError("evidence value kind does not match its tagged payload")
        if self.literal_value is not None:
            _text(self.literal_value, "literal_value")
        if any(not item.strip() for item in self.related_record_ids):
            raise ValueError("related record IDs must be nonblank")
        if self.conflict_declaration in {
            ConflictDeclaration.CONFLICT_PRESENT,
            ConflictDeclaration.UNRESOLVED,
        } and not self.related_record_ids:
            raise ValueError("conflict declarations require related record IDs")
        required_value_kinds = {
            EvidenceReferenceKind.M01_QUANTITY: {EvidenceValueKind.NUMERIC_POINT},
            EvidenceReferenceKind.M02_MISSING_OBSERVATION: {EvidenceValueKind.MISSING_STATE},
            EvidenceReferenceKind.M02_CONFLICT: {EvidenceValueKind.CONFLICT_DECLARATION},
            EvidenceReferenceKind.M03_COMPLETENESS_DIAGNOSTIC: {EvidenceValueKind.DIAGNOSTIC_CLASSIFICATION},
            EvidenceReferenceKind.M03_DOMAIN_DIAGNOSTIC: {EvidenceValueKind.DIAGNOSTIC_CLASSIFICATION},
            EvidenceReferenceKind.CONTROLLED_CATEGORY: {EvidenceValueKind.CATEGORY},
            EvidenceReferenceKind.EXPLICIT_IDENTIFIER: {EvidenceValueKind.IDENTIFIER},
        }
        if self.reference_kind in required_value_kinds and self.value_kind not in required_value_kinds[self.reference_kind]:
            raise ValueError("evidence reference kind and value kind disagree")

    @classmethod
    def from_completeness_diagnostic(
        cls,
        *,
        reference_id: str,
        evaluation_record_id: str,
        diagnostic: CompletenessDiagnostic,
        provenance: Provenance,
        source_locator: SourceLocator,
    ) -> EvidenceReference:
        """Retain an exact M03 completeness diagnostic without re-evaluating it."""

        return cls(
            reference_id,
            EvidenceReferenceKind.M03_COMPLETENESS_DIAGNOSTIC,
            evaluation_record_id,
            f"m03.completeness.{diagnostic.requirement_id}",
            EvidenceValueKind.DIAGNOSTIC_CLASSIFICATION,
            provenance,
            source_locator,
            literal_value=diagnostic.status.value,
            related_record_ids=diagnostic.supplied_record_ids,
            notes=f"{diagnostic.comparison_performed} {diagnostic.rejection_reason}",
        )

    @classmethod
    def from_domain_diagnostic(
        cls,
        *,
        reference_id: str,
        evaluation_record_id: str,
        diagnostic: DomainConstraintDiagnostic,
        provenance: Provenance,
        source_locator: SourceLocator,
    ) -> EvidenceReference:
        """Retain an exact M03 domain diagnostic without reinterpreting it."""

        return cls(
            reference_id,
            EvidenceReferenceKind.M03_DOMAIN_DIAGNOSTIC,
            evaluation_record_id,
            f"m03.domain.{diagnostic.constraint_id}",
            EvidenceValueKind.DIAGNOSTIC_CLASSIFICATION,
            provenance,
            source_locator,
            literal_value=diagnostic.status.value,
            notes=diagnostic.explanation,
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "reference_id": self.reference_id,
            "reference_kind": self.reference_kind.value,
            "source_record_id": self.source_record_id,
            "definition_id": self.definition_id,
            "value_kind": self.value_kind.value,
            "provenance": self.provenance.to_dict(),
            "source_locator": self.source_locator.to_dict(),
            "quantity": None if self.quantity is None else self.quantity.to_dict(),
            "interval": None if self.interval is None else self.interval.to_dict(),
            "literal_value": self.literal_value,
            "missing_state": None if self.missing_state is None else self.missing_state.value,
            "conflict_declaration": (
                None if self.conflict_declaration is None else self.conflict_declaration.value
            ),
            "related_record_ids": list(self.related_record_ids),
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> EvidenceReference:
        fields = {
            "reference_id", "reference_kind", "source_record_id", "definition_id",
            "value_kind", "provenance", "source_locator", "quantity", "interval",
            "literal_value", "missing_state", "conflict_declaration",
            "related_record_ids", "notes",
        }
        _strict(data, fields)
        related = data["related_record_ids"]
        if not isinstance(related, list) or not all(isinstance(item, str) for item in related):
            raise TypeError("related_record_ids must be a string list")
        return cls(
            str(data["reference_id"]),
            EvidenceReferenceKind(str(data["reference_kind"])),
            str(data["source_record_id"]),
            str(data["definition_id"]),
            EvidenceValueKind(str(data["value_kind"])),
            Provenance.from_dict(data["provenance"]),
            SourceLocator.from_dict(data["source_locator"]),
            None if data["quantity"] is None else Quantity.from_dict(data["quantity"]),
            None if data["interval"] is None else QueryInterval.from_dict(data["interval"]),
            None if data["literal_value"] is None else str(data["literal_value"]),
            None if data["missing_state"] is None else MissingState(str(data["missing_state"])),
            None if data["conflict_declaration"] is None else ConflictDeclaration(str(data["conflict_declaration"])),
            tuple(related),
            str(data["notes"]),
        )


@dataclass(frozen=True, slots=True)
class EvaluationContext:
    """Exact records supplied for one criterion-set evaluation."""

    record_id: str
    criterion_set_id: str
    criterion_set_version: int
    subject_identity: IdentityQualifier
    powder_identity: IdentityQualifier
    powder_lot: IdentityQualifier
    cartridge_or_geometry_identity: IdentityQualifier
    evidence_references: tuple[EvidenceReference, ...]
    evaluation_date: str
    evaluator: str
    software_version: str
    repository_commit: str
    schema_versions: tuple[str, ...]
    evidence_boundary: str
    stated_purpose: str
    explicit_exclusions: tuple[str, ...]
    provenance: Provenance

    def __post_init__(self) -> None:
        for value, name in (
            (self.record_id, "record_id"),
            (self.criterion_set_id, "criterion_set_id"),
            (self.evaluation_date, "evaluation_date"),
            (self.evaluator, "evaluator"),
            (self.software_version, "software_version"),
            (self.repository_commit, "repository_commit"),
            (self.evidence_boundary, "evidence_boundary"),
            (self.stated_purpose, "stated_purpose"),
        ):
            _text(value, name)
        if isinstance(self.criterion_set_version, bool) or not isinstance(self.criterion_set_version, int) or self.criterion_set_version <= 0:
            raise ValueError("criterion-set version must be positive")
        ids = [item.reference_id for item in self.evidence_references]
        if len(ids) != len(set(ids)):
            raise ValueError("evidence reference IDs must be unique")
        if not self.schema_versions or any(not item.strip() for item in self.schema_versions) or len(self.schema_versions) != len(set(self.schema_versions)):
            raise ValueError("evaluation context requires explicit schema versions")
        if any(not item.strip() for item in self.explicit_exclusions):
            raise ValueError("evaluation exclusions must be nonblank")

    def to_dict(self) -> dict[str, object]:
        return {
            "schema": M04_SCHEMA_ID,
            "record_type": "evaluation_context",
            "record_id": self.record_id,
            "criterion_set_id": self.criterion_set_id,
            "criterion_set_version": self.criterion_set_version,
            "subject_identity": self.subject_identity.to_dict(),
            "powder_identity": self.powder_identity.to_dict(),
            "powder_lot": self.powder_lot.to_dict(),
            "cartridge_or_geometry_identity": self.cartridge_or_geometry_identity.to_dict(),
            "evidence_references": [item.to_dict() for item in self.evidence_references],
            "evaluation_date": self.evaluation_date,
            "evaluator": self.evaluator,
            "software_version": self.software_version,
            "repository_commit": self.repository_commit,
            "schema_versions": list(self.schema_versions),
            "evidence_boundary": self.evidence_boundary,
            "stated_purpose": self.stated_purpose,
            "explicit_exclusions": list(self.explicit_exclusions),
            "provenance": self.provenance.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> EvaluationContext:
        fields = {
            "schema", "record_type", "record_id", "criterion_set_id",
            "criterion_set_version", "subject_identity", "powder_identity", "powder_lot",
            "cartridge_or_geometry_identity", "evidence_references", "evaluation_date",
            "evaluator", "software_version", "repository_commit", "schema_versions",
            "evidence_boundary", "stated_purpose", "explicit_exclusions", "provenance",
        }
        _strict(data, fields)
        if data["schema"] != M04_SCHEMA_ID or data["record_type"] != "evaluation_context":
            raise ValueError("invalid M04 evaluation-context header")
        references, schemas, exclusions = (
            data["evidence_references"], data["schema_versions"], data["explicit_exclusions"]
        )
        if not isinstance(references, list):
            raise TypeError("evidence_references must be a list")
        if any(not isinstance(value, list) or not all(isinstance(item, str) for item in value) for value in (schemas, exclusions)):
            raise TypeError("context schema and exclusion fields must be string lists")
        version = data["criterion_set_version"]
        if isinstance(version, bool) or not isinstance(version, int):
            raise TypeError("criterion-set version must be an integer")
        return cls(
            str(data["record_id"]), str(data["criterion_set_id"]), version,
            IdentityQualifier.from_dict(data["subject_identity"]),
            IdentityQualifier.from_dict(data["powder_identity"]),
            IdentityQualifier.from_dict(data["powder_lot"]),
            IdentityQualifier.from_dict(data["cartridge_or_geometry_identity"]),
            tuple(EvidenceReference.from_dict(item) for item in references),
            str(data["evaluation_date"]), str(data["evaluator"]),
            str(data["software_version"]), str(data["repository_commit"]), tuple(schemas),
            str(data["evidence_boundary"]), str(data["stated_purpose"]), tuple(exclusions),
            Provenance.from_dict(data["provenance"]),
        )
