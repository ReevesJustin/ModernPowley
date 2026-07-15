"""Immutable M05 bounded analytical charge-region records."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from .property_observations import SourceLocator
from .provenance import EvidenceClass, ModelMaturity, Provenance
from .units import Dimension, Quantity, require_positive

M05_SCHEMA_ID = "modern_powley.m05.v1"


class RegionState(str, Enum):
    BOUNDED = "bounded"
    EMPTY = "empty"
    UNAVAILABLE = "unavailable"
    INDETERMINATE = "indeterminate"
    CONFLICTING = "conflicting"


class RegionBasis(str, Enum):
    SOURCE_DECLARED_INTERVAL = "source_declared_interval"
    MEASUREMENT_SUPPORTED_INTERVAL = "measurement_supported_interval"
    GEOMETRY_OR_FILL_CONSTRAINT = "geometry_or_fill_constraint"
    PROPERTY_UNCERTAINTY_CONSTRAINT = "property_uncertainty_constraint"
    INTERSECTION_OF_EXPLICIT_CONSTRAINTS = "intersection_of_explicit_constraints"
    EXPERIMENTAL_ESTIMATE = "experimental_estimate"


class DependencyStatus(str, Enum):
    NOT_APPLICABLE = "not_applicable"
    UNKNOWN = "unknown"
    EXPLICITLY_DECLARED = "explicitly_declared"
    EXTERNALLY_REFERENCED = "externally_referenced"


class ActivationStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class EndpointInclusion(str, Enum):
    INCLUDED = "included"
    EXCLUDED = "excluded"


class ExactReferenceRole(str, Enum):
    M01_INPUT = "m01_input"
    M02_EVIDENCE = "m02_evidence"
    M03_DIAGNOSTIC = "m03_diagnostic"
    M04_AUDIT = "m04_audit"
    M05_REGION = "m05_region"
    EXTERNAL_LINEAGE = "external_lineage"


class UncertaintyDeclarationKind(str, Enum):
    MEASUREMENT = "measurement_uncertainty"
    MODEL_FORM = "model_form_uncertainty"
    UNKNOWN = "unknown_uncertainty"
    NOT_APPLICABLE = "not_applicable"
    EXTERNALLY_REFERENCED = "externally_referenced"


class NonImplicationDeclaration(str, Enum):
    M05_CANONICAL = "m05_canonical_non_implication_v1"

    @property
    def statement(self) -> str:
        return (
            "This bounded analytical charge-region record does not establish a "
            "recommended, preferred, starting, or maximum charge; a safe range; "
            "a loading instruction; powder suitability; pressure safety; pressure "
            "or velocity prediction; physical correctness; validity of every "
            "interior point; or experimental testing of every interior point."
        )


def _required_text(value: str, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} is required")


def _optional_text(value: str | None, name: str) -> None:
    if value is not None:
        _required_text(value, name)


def _positive_version(value: int, name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{name} must be a positive integer")


def _unique(items: tuple[Any, ...], name: str) -> None:
    if len(items) != len(set(items)):
        raise ValueError(f"{name} must be unique")


@dataclass(frozen=True, slots=True)
class ExactRecordReference:
    """Caller-supplied exact identity; no lookup or resolution is performed."""

    role: ExactReferenceRole
    schema_id: str
    record_type: str
    record_id: str
    version: int | None
    evidence_class: EvidenceClass
    model_maturity: ModelMaturity

    def __post_init__(self) -> None:
        object.__setattr__(self, "role", ExactReferenceRole(self.role))
        object.__setattr__(self, "evidence_class", EvidenceClass(self.evidence_class))
        object.__setattr__(self, "model_maturity", ModelMaturity(self.model_maturity))
        for value, name in ((self.schema_id, "schema_id"), (self.record_type, "record_type"), (self.record_id, "record_id")):
            _required_text(value, name)
        if self.version is not None:
            _positive_version(self.version, "reference version")

    @property
    def identity(self) -> tuple[str, str, str, int | None]:
        return (self.schema_id, self.record_type, self.record_id, self.version)

    def to_dict(self) -> dict[str, object]:
        return {
            "role": self.role.value, "schema_id": self.schema_id,
            "record_type": self.record_type, "record_id": self.record_id,
            "version": self.version, "evidence_class": self.evidence_class.value,
            "model_maturity": self.model_maturity.value,
        }


@dataclass(frozen=True, slots=True)
class MethodReference:
    method_id: str
    version: int
    authority_reference: ExactRecordReference
    model_maturity: ModelMaturity
    status: str

    def __post_init__(self) -> None:
        _required_text(self.method_id, "method_id")
        _positive_version(self.version, "method version")
        object.__setattr__(self, "model_maturity", ModelMaturity(self.model_maturity))
        _required_text(self.status, "method status")
        if self.authority_reference.role is ExactReferenceRole.M04_AUDIT:
            raise ValueError("M04 audit reference cannot be method authority")

    def to_dict(self) -> dict[str, object]:
        return {"method_id": self.method_id, "version": self.version, "authority_reference": self.authority_reference.to_dict(), "model_maturity": self.model_maturity.value, "status": self.status}


@dataclass(frozen=True, slots=True)
class ChargeMassEndpoint:
    quantity: Quantity
    inclusion: EndpointInclusion
    source_reported_value: str | None = None
    reported_precision: str | None = None
    source_references: tuple[ExactRecordReference, ...] = ()
    qualifications: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        require_positive(self.quantity, Dimension.MASS, "charge-mass endpoint")
        object.__setattr__(self, "inclusion", EndpointInclusion(self.inclusion))
        _optional_text(self.source_reported_value, "source_reported_value")
        _optional_text(self.reported_precision, "reported_precision")
        if any(not isinstance(item, str) or not item.strip() for item in self.qualifications):
            raise ValueError("endpoint qualifications must be nonblank")
        _unique(tuple(item.identity for item in self.source_references), "endpoint source references")

    def to_dict(self) -> dict[str, object]:
        return {"quantity": self.quantity.to_dict(), "inclusion": self.inclusion.value, "source_reported_value": self.source_reported_value, "reported_precision": self.reported_precision, "source_references": [item.to_dict() for item in self.source_references], "qualifications": list(self.qualifications)}


@dataclass(frozen=True, slots=True)
class ChargeMassSegment:
    lower: ChargeMassEndpoint
    upper: ChargeMassEndpoint

    def __post_init__(self) -> None:
        if self.lower.quantity.si_value > self.upper.quantity.si_value:
            raise ValueError("segment lower bound exceeds upper bound")
        if self.lower.quantity.si_value == self.upper.quantity.si_value and (
            self.lower.inclusion is not EndpointInclusion.INCLUDED
            or self.upper.inclusion is not EndpointInclusion.INCLUDED
        ):
            raise ValueError("point segment must include both endpoints")

    def to_dict(self) -> dict[str, object]:
        return {"lower": self.lower.to_dict(), "upper": self.upper.to_dict()}


@dataclass(frozen=True, slots=True)
class UncertaintyDeclaration:
    kind: UncertaintyDeclarationKind
    description: str
    references: tuple[ExactRecordReference, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "kind", UncertaintyDeclarationKind(self.kind))
        _required_text(self.description, "uncertainty description")
        _unique(tuple(item.identity for item in self.references), "uncertainty references")
        if self.kind is UncertaintyDeclarationKind.EXTERNALLY_REFERENCED and not self.references:
            raise ValueError("externally referenced uncertainty requires references")
        if self.kind is not UncertaintyDeclarationKind.EXTERNALLY_REFERENCED and self.references:
            raise ValueError("only externally referenced uncertainty carries references")

    def to_dict(self) -> dict[str, object]:
        return {"kind": self.kind.value, "description": self.description, "references": [item.to_dict() for item in self.references]}


@dataclass(frozen=True, slots=True)
class PressureEvidenceContext:
    evidence_reference: ExactRecordReference
    pressure_quantity_identity: str
    measurement_method: str
    standard_or_protocol: str
    instrument_type: str
    source_unit_label: str
    conditions: tuple[str, ...]
    source_locator: SourceLocator
    source_limitations: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.evidence_reference.role is ExactReferenceRole.M04_AUDIT:
            raise ValueError("M04 audit reference cannot be pressure evidence")
        for value, name in ((self.pressure_quantity_identity, "pressure quantity"), (self.measurement_method, "measurement method"), (self.standard_or_protocol, "standard/protocol"), (self.instrument_type, "instrument type"), (self.source_unit_label, "source unit label")):
            _required_text(value, name)
        if any(not item.strip() for item in self.conditions + self.source_limitations):
            raise ValueError("pressure conditions and limitations must be nonblank")

    def to_dict(self) -> dict[str, object]:
        return {"evidence_reference": self.evidence_reference.to_dict(), "pressure_quantity_identity": self.pressure_quantity_identity, "measurement_method": self.measurement_method, "standard_or_protocol": self.standard_or_protocol, "instrument_type": self.instrument_type, "source_unit_label": self.source_unit_label, "conditions": list(self.conditions), "source_locator": self.source_locator.to_dict(), "source_limitations": list(self.source_limitations)}


@dataclass(frozen=True, slots=True)
class VersionedRegionReference:
    region_id: str
    version: int

    def __post_init__(self) -> None:
        _required_text(self.region_id, "superseded region_id")
        _positive_version(self.version, "superseded version")

    def to_dict(self) -> dict[str, object]:
        return {"region_id": self.region_id, "version": self.version}


@dataclass(frozen=True, slots=True)
class LifecycleMetadata:
    activation: ActivationStatus
    supersedes: VersionedRegionReference | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "activation", ActivationStatus(self.activation))

    def to_dict(self) -> dict[str, object]:
        return {"activation": self.activation.value, "supersedes": None if self.supersedes is None else self.supersedes.to_dict()}


@dataclass(frozen=True, slots=True)
class ChargeRegionRecord:
    record_id: str
    region_id: str
    version: int
    state: RegionState
    basis: RegionBasis | None
    method: MethodReference | None
    segments: tuple[ChargeMassSegment, ...]
    m01_input_references: tuple[ExactRecordReference, ...]
    m02_evidence_references: tuple[ExactRecordReference, ...]
    m03_diagnostic_references: tuple[ExactRecordReference, ...]
    m04_audit_references: tuple[ExactRecordReference, ...]
    applicability_references: tuple[ExactRecordReference, ...]
    provenance: Provenance
    source_locator: SourceLocator
    source_wording: str
    reported_precision: str | None
    conditions: tuple[str, ...]
    uncertainty: UncertaintyDeclaration
    dependency_status: DependencyStatus
    dependency_references: tuple[ExactRecordReference, ...]
    conflict_references: tuple[ExactRecordReference, ...]
    qualifications: tuple[str, ...]
    derivation_lineage: tuple[ExactRecordReference, ...]
    pressure_contexts: tuple[PressureEvidenceContext, ...]
    lifecycle: LifecycleMetadata
    explanation: str | None
    non_implication: NonImplicationDeclaration

    def __post_init__(self) -> None:
        _required_text(self.record_id, "record_id")
        _required_text(self.region_id, "region_id")
        _positive_version(self.version, "region version")
        object.__setattr__(self, "state", RegionState(self.state))
        if self.basis is not None:
            object.__setattr__(self, "basis", RegionBasis(self.basis))
        object.__setattr__(self, "dependency_status", DependencyStatus(self.dependency_status))
        object.__setattr__(self, "non_implication", NonImplicationDeclaration(self.non_implication))
        _optional_text(self.reported_precision, "reported_precision")
        _optional_text(self.explanation, "explanation")
        if self.provenance.source_id != self.source_locator.source_id:
            raise ValueError("record provenance and source locator must match")
        if any(not isinstance(item, str) or not item.strip() for item in self.conditions + self.qualifications):
            raise ValueError("conditions and qualifications must be nonblank")
        _required_text(self.source_wording, "source_wording")
        self._validate_reference_roles()
        self._validate_state()
        self._validate_segments()
        self._validate_dependencies()
        if self.lifecycle.supersedes == VersionedRegionReference(self.region_id, self.version):
            raise ValueError("region cannot supersede itself")

    def _validate_reference_roles(self) -> None:
        groups = (
            (self.m01_input_references, ExactReferenceRole.M01_INPUT, "M01 references"),
            (self.m02_evidence_references, ExactReferenceRole.M02_EVIDENCE, "M02 references"),
            (self.m03_diagnostic_references, ExactReferenceRole.M03_DIAGNOSTIC, "M03 references"),
            (self.m04_audit_references, ExactReferenceRole.M04_AUDIT, "M04 references"),
        )
        scientific_identities: list[tuple[str, str, str, int | None]] = []
        for references, role, name in groups:
            if any(item.role is not role for item in references):
                raise ValueError(f"{name} have wrong exact-reference role")
            _unique(tuple(item.identity for item in references), name)
            if role is not ExactReferenceRole.M04_AUDIT:
                scientific_identities.extend(item.identity for item in references)
        _unique(tuple(scientific_identities), "scientific input references")
        for references, name in ((self.applicability_references, "applicability references"), (self.derivation_lineage, "derivation lineage")):
            if any(item.role is ExactReferenceRole.M04_AUDIT for item in references):
                raise ValueError(f"{name} cannot contain M04 audit references")
            _unique(tuple(item.identity for item in references), name)

    def _validate_state(self) -> None:
        if self.state is RegionState.BOUNDED:
            if not self.segments or self.basis is None or self.method is None or self.conflict_references:
                raise ValueError("bounded region requires segments, basis, method, and no conflicts")
        elif self.state is RegionState.EMPTY:
            if self.segments or self.basis is None or self.method is None or self.conflict_references or self.explanation is None:
                raise ValueError("empty region requires basis, method, explanation, and no segments/conflicts")
        elif self.state is RegionState.UNAVAILABLE:
            if self.segments or self.basis is not None or self.method is not None or self.conflict_references or self.explanation is None:
                raise ValueError("unavailable region requires explanation and no analytical result fields")
        elif self.state is RegionState.INDETERMINATE:
            if self.segments or self.conflict_references or self.explanation is None or ((self.basis is None) != (self.method is None)):
                raise ValueError("indeterminate region requires explanation and a complete or absent basis/method pair")
        else:
            if self.segments or self.basis is not None or self.method is not None or self.explanation is None or len(self.conflict_references) < 2:
                raise ValueError("conflicting region requires explanation, two conflicts, and no analytical result fields")
            if any(item.role is not ExactReferenceRole.M05_REGION for item in self.conflict_references):
                raise ValueError("conflict references must identify exact M05 regions")
            _unique(tuple(item.identity for item in self.conflict_references), "conflict references")

    def _validate_segments(self) -> None:
        for previous, current in zip(self.segments, self.segments[1:]):
            if current.lower.quantity.si_value <= previous.lower.quantity.si_value:
                raise ValueError("segments must be in strict caller-supplied ascending order")
            if current.lower.quantity.si_value < previous.upper.quantity.si_value:
                raise ValueError("segments must not overlap")
            if current.lower.quantity.si_value == previous.upper.quantity.si_value and current.lower.inclusion is EndpointInclusion.INCLUDED and previous.upper.inclusion is EndpointInclusion.INCLUDED:
                raise ValueError("adjacent segments cannot both include a shared boundary")

    def _validate_dependencies(self) -> None:
        _unique(tuple(item.identity for item in self.dependency_references), "dependency references")
        if self.dependency_status is DependencyStatus.EXTERNALLY_REFERENCED and not self.dependency_references:
            raise ValueError("externally referenced dependency requires references")
        if self.dependency_status is not DependencyStatus.EXTERNALLY_REFERENCED and self.dependency_references:
            raise ValueError("only externally referenced dependency carries references")

    def to_dict(self) -> dict[str, object]:
        return {
            "schema": M05_SCHEMA_ID, "record_type": "charge_region_record",
            "record_id": self.record_id, "region_id": self.region_id, "version": self.version,
            "state": self.state.value, "basis": None if self.basis is None else self.basis.value,
            "method": None if self.method is None else self.method.to_dict(),
            "segments": [item.to_dict() for item in self.segments],
            "m01_input_references": [item.to_dict() for item in self.m01_input_references],
            "m02_evidence_references": [item.to_dict() for item in self.m02_evidence_references],
            "m03_diagnostic_references": [item.to_dict() for item in self.m03_diagnostic_references],
            "m04_audit_references": [item.to_dict() for item in self.m04_audit_references],
            "applicability_references": [item.to_dict() for item in self.applicability_references],
            "provenance": self.provenance.to_dict(), "source_locator": self.source_locator.to_dict(),
            "source_wording": self.source_wording, "reported_precision": self.reported_precision,
            "conditions": list(self.conditions), "uncertainty": self.uncertainty.to_dict(),
            "dependency_status": self.dependency_status.value,
            "dependency_references": [item.to_dict() for item in self.dependency_references],
            "conflict_references": [item.to_dict() for item in self.conflict_references],
            "qualifications": list(self.qualifications),
            "derivation_lineage": [item.to_dict() for item in self.derivation_lineage],
            "pressure_contexts": [item.to_dict() for item in self.pressure_contexts],
            "lifecycle": self.lifecycle.to_dict(), "explanation": self.explanation,
            "non_implication": self.non_implication.value,
        }
