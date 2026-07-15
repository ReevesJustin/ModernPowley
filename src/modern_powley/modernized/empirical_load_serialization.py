"""Strict JSON serialization for empirical-load evidence Phase 1 records."""

from __future__ import annotations

import json
from collections.abc import Mapping
from numbers import Real
from typing import Any

from .empirical_load_records import (
    EMPIRICAL_LOAD_EVIDENCE_SCHEMA_ID,
    ActivationState,
    AggregateOrigin,
    AggregateStatistic,
    AggregateSummaryRecord,
    ArtifactReference,
    ArtifactRetentionState,
    ChronographSeriesRecord,
    ComponentKind,
    ConflictGroup,
    EmpiricalLoadEvidenceRecord,
    EmpiricalRecordType,
    EquipmentIdentity,
    EquipmentKind,
    EvidenceUncertainty,
    EvidenceUncertaintyKind,
    ExactRecordReference,
    ExcludedWindow,
    Exclusion,
    ExclusionState,
    LineageLink,
    LiteralLoadStatementRecord,
    LoadSeriesRecord,
    MissingValue,
    ObservationLevel,
    OrderedMember,
    PhysicalLoadConfigurationRecord,
    PhysicalQuantityEvidence,
    PowderIdentityReference,
    PrecisionKind,
    PressureAcquisitionState,
    PressureLocation,
    PressureObservation,
    PressureOrigin,
    PressureQuantity,
    PressureTraceMetadataRecord,
    PressureUnit,
    QuantityOrMissing,
    RECORD_CLASS_BY_TYPE,
    RecordEnvelope,
    ReferenceOrMissing,
    ReferenceRole,
    ReportedPrecision,
    ReportedValue,
    ReportedValueKind,
    ReviewContext,
    ReviewState,
    ScopedComponentIdentity,
    ShotObservationRecord,
    SourceCustodyRecord,
    SourceDeclarationState,
    TraceArtifactState,
    VelocityCorrectionState,
    VelocityObservation,
    VelocityQuantity,
    VelocityUnit,
)
from .missing_values import IdentityQualifier, MissingState
from .property_observations import SourceLocator, TranscriptionStatus
from .provenance import EvidenceClass, ModelMaturity
from .uncertainty import Uncertainty, UncertaintyKind
from .units import Quantity, Unit


_TOP_FIELDS = {"schema", "schema_version", "record_type", "envelope", "payload"}


def _object(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise TypeError(f"{name} must be an object")
    return value


def _keys(data: Mapping[str, Any], fields: set[str], name: str) -> None:
    if set(data) != fields:
        raise ValueError(f"malformed {name} fields")


def _string(value: Any, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    return value


def _optional_string(value: Any, name: str) -> str | None:
    return None if value is None else _string(value, name)


def _integer(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    return value


def _boolean(value: Any, name: str) -> bool:
    if not isinstance(value, bool):
        raise TypeError(f"{name} must be a Boolean")
    return value


def _list(value: Any, name: str) -> list[Any]:
    if not isinstance(value, list):
        raise TypeError(f"{name} must be a list")
    return value


def _strings(value: Any, name: str) -> tuple[str, ...]:
    return tuple(_string(item, name) for item in _list(value, name))


def _enum(value: Any, enum_type: type, name: str):
    return enum_type(_string(value, name))


def _quantity_to_dict(value: Quantity) -> dict[str, object]:
    return {"value": value.value, "unit": value.unit.value}


def _quantity(value: Any) -> Quantity:
    data = _object(value, "quantity")
    _keys(data, {"value", "unit"}, "quantity")
    number = data["value"]
    if isinstance(number, bool) or not isinstance(number, Real):
        raise TypeError("quantity value must be a number")
    return Quantity(number, Unit(_string(data["unit"], "quantity unit")))


def _uncertainty_to_dict(value: Uncertainty) -> dict[str, object]:
    return value.to_dict()


def _uncertainty(value: Any) -> Uncertainty:
    data = _object(value, "uncertainty")
    kind = _enum(data.get("kind"), UncertaintyKind, "uncertainty kind")
    if kind is UncertaintyKind.UNKNOWN:
        _keys(data, {"kind", "justification"}, "unknown uncertainty")
        return Uncertainty(kind, justification=_string(data["justification"], "uncertainty justification"))
    if kind in {UncertaintyKind.INSTRUMENT_RESOLUTION, UncertaintyKind.SYMMETRIC_ABSOLUTE}:
        _keys(data, {"kind", "justification", "magnitude"}, "magnitude uncertainty")
        return Uncertainty(kind, magnitude=_quantity(data["magnitude"]), justification=_string(data["justification"], "uncertainty justification"))
    _keys(data, {"kind", "justification", "lower", "upper"}, "bounded uncertainty")
    return Uncertainty(kind, lower=_quantity(data["lower"]), upper=_quantity(data["upper"]), justification=_string(data["justification"], "uncertainty justification"))


def _qualifier_to_dict(value: IdentityQualifier) -> dict[str, object]:
    return value.to_dict()


def _qualifier(value: Any) -> IdentityQualifier:
    data = _object(value, "identity qualifier")
    _keys(data, {"value", "missing_state", "explanation"}, "identity qualifier")
    present = data["value"]
    missing = data["missing_state"]
    if present is not None:
        present = _string(present, "identity value")
    if missing is not None:
        missing = _enum(missing, MissingState, "missing state")
    return IdentityQualifier(present, missing, _string(data["explanation"], "identity explanation"))


def _locator_to_dict(value: SourceLocator) -> dict[str, object]:
    return value.to_dict()


def _locator(value: Any) -> SourceLocator:
    data = _object(value, "source locator")
    _keys(data, {"source_id", "locator", "transcription_status"}, "source locator")
    return SourceLocator(
        _string(data["source_id"], "source locator source_id"),
        _string(data["locator"], "source locator"),
        _enum(data["transcription_status"], TranscriptionStatus, "transcription status"),
    )


def _reference_to_dict(value: ExactRecordReference) -> dict[str, object]:
    return {
        "schema_id": value.schema_id,
        "record_type": value.record_type,
        "record_id": value.record_id,
        "version": value.version,
        "role": value.role.value,
    }


def _reference(value: Any) -> ExactRecordReference:
    data = _object(value, "exact reference")
    _keys(data, {"schema_id", "record_type", "record_id", "version", "role"}, "exact reference")
    version = data["version"]
    return ExactRecordReference(
        schema_id=_string(data["schema_id"], "reference schema_id"),
        record_type=_string(data["record_type"], "reference record_type"),
        record_id=_string(data["record_id"], "reference record_id"),
        version=None if version is None else _integer(version, "reference version"),
        role=_enum(data["role"], ReferenceRole, "reference role"),
    )


def _references(value: Any, name: str) -> tuple[ExactRecordReference, ...]:
    return tuple(_reference(item) for item in _list(value, name))


def _missing_to_dict(value: MissingValue) -> dict[str, object]:
    return {
        "state": value.state.value,
        "explanation": value.explanation,
        "source_references": [_reference_to_dict(item) for item in value.source_references],
    }


def _missing(value: Any) -> MissingValue:
    data = _object(value, "missing value")
    _keys(data, {"state", "explanation", "source_references"}, "missing value")
    return MissingValue(
        state=_enum(data["state"], MissingState, "missing state"),
        explanation=_string(data["explanation"], "missing explanation"),
        source_references=_references(data["source_references"], "missing references"),
    )


def _reference_or_missing_to_dict(value: ReferenceOrMissing) -> dict[str, object]:
    if value.reference is not None:
        return {"kind": "reference", "reference": _reference_to_dict(value.reference)}
    return {"kind": "missing", "missing": _missing_to_dict(value.missing)}


def _reference_or_missing(value: Any) -> ReferenceOrMissing:
    data = _object(value, "reference-or-missing")
    kind = _string(data.get("kind"), "reference-or-missing kind")
    if kind == "reference":
        _keys(data, {"kind", "reference"}, "reference-or-missing reference")
        return ReferenceOrMissing(reference=_reference(data["reference"]), missing=None)
    if kind == "missing":
        _keys(data, {"kind", "missing"}, "reference-or-missing missing")
        return ReferenceOrMissing(reference=None, missing=_missing(data["missing"]))
    raise ValueError(f"unsupported reference-or-missing kind: {kind!r}")


def _precision_to_dict(value: ReportedPrecision) -> dict[str, object]:
    return {"kind": value.kind.value, "statement": value.statement, "digits": value.digits}


def _precision(value: Any) -> ReportedPrecision:
    data = _object(value, "reported precision")
    _keys(data, {"kind", "statement", "digits"}, "reported precision")
    digits = data["digits"]
    return ReportedPrecision(
        kind=_enum(data["kind"], PrecisionKind, "precision kind"),
        statement=_string(data["statement"], "precision statement"),
        digits=None if digits is None else _integer(digits, "precision digits"),
    )


def _evidence_uncertainty_to_dict(value: EvidenceUncertainty) -> dict[str, object]:
    return {
        "kind": value.kind.value,
        "description": value.description,
        "reference": None if value.reference is None else _reference_to_dict(value.reference),
    }


def _evidence_uncertainty(value: Any) -> EvidenceUncertainty:
    data = _object(value, "evidence uncertainty")
    _keys(data, {"kind", "description", "reference"}, "evidence uncertainty")
    reference = data["reference"]
    return EvidenceUncertainty(
        kind=_enum(data["kind"], EvidenceUncertaintyKind, "evidence uncertainty kind"),
        description=_string(data["description"], "evidence uncertainty description"),
        reference=None if reference is None else _reference(reference),
    )


def _reported_value_to_dict(value: ReportedValue) -> dict[str, object]:
    return {
        "kind": value.kind.value,
        "decimal_text": value.decimal_text,
        "source_unit_label": value.source_unit_label,
        "source_wording": value.source_wording,
        "precision": _precision_to_dict(value.precision),
        "uncertainty": _evidence_uncertainty_to_dict(value.uncertainty),
        "source_defined_kind": value.source_defined_kind,
    }


def _reported_value(value: Any) -> ReportedValue:
    data = _object(value, "reported value")
    _keys(data, {"kind", "decimal_text", "source_unit_label", "source_wording", "precision", "uncertainty", "source_defined_kind"}, "reported value")
    return ReportedValue(
        kind=_enum(data["kind"], ReportedValueKind, "reported value kind"),
        decimal_text=_string(data["decimal_text"], "reported decimal text"),
        source_unit_label=_string(data["source_unit_label"], "reported unit label"),
        source_wording=_string(data["source_wording"], "reported source wording"),
        precision=_precision(data["precision"]),
        uncertainty=_evidence_uncertainty(data["uncertainty"]),
        source_defined_kind=_optional_string(data["source_defined_kind"], "source-defined kind"),
    )


def _physical_quantity_to_dict(value: PhysicalQuantityEvidence) -> dict[str, object]:
    return {
        "quantity": _quantity_to_dict(value.quantity),
        "source_value_text": value.source_value_text,
        "precision": _precision_to_dict(value.precision),
        "uncertainty": _uncertainty_to_dict(value.uncertainty),
    }


def _physical_quantity(value: Any) -> PhysicalQuantityEvidence:
    data = _object(value, "physical quantity evidence")
    _keys(data, {"quantity", "source_value_text", "precision", "uncertainty"}, "physical quantity evidence")
    return PhysicalQuantityEvidence(
        quantity=_quantity(data["quantity"]),
        source_value_text=_string(data["source_value_text"], "source value text"),
        precision=_precision(data["precision"]),
        uncertainty=_uncertainty(data["uncertainty"]),
    )


def _quantity_or_missing_to_dict(value: QuantityOrMissing) -> dict[str, object]:
    if value.value is not None:
        return {"kind": "value", "value": _physical_quantity_to_dict(value.value)}
    return {"kind": "missing", "missing": _missing_to_dict(value.missing)}


def _quantity_or_missing(value: Any) -> QuantityOrMissing:
    data = _object(value, "quantity-or-missing")
    kind = _string(data.get("kind"), "quantity-or-missing kind")
    if kind == "value":
        _keys(data, {"kind", "value"}, "quantity-or-missing value")
        return QuantityOrMissing(value=_physical_quantity(data["value"]), missing=None)
    if kind == "missing":
        _keys(data, {"kind", "missing"}, "quantity-or-missing missing")
        return QuantityOrMissing(value=None, missing=_missing(data["missing"]))
    raise ValueError(f"unsupported quantity-or-missing kind: {kind!r}")


def _review_to_dict(value: ReviewContext) -> dict[str, object]:
    return {
        "created_by": value.created_by,
        "created_at": value.created_at,
        "state": value.state.value,
        "reviewed_by": _qualifier_to_dict(value.reviewed_by),
        "reviewed_at": _qualifier_to_dict(value.reviewed_at),
        "notes": value.notes,
    }


def _review(value: Any) -> ReviewContext:
    data = _object(value, "review context")
    _keys(data, {"created_by", "created_at", "state", "reviewed_by", "reviewed_at", "notes"}, "review context")
    return ReviewContext(
        created_by=_string(data["created_by"], "created_by"),
        created_at=_string(data["created_at"], "created_at"),
        state=_enum(data["state"], ReviewState, "review state"),
        reviewed_by=_qualifier(data["reviewed_by"]),
        reviewed_at=_qualifier(data["reviewed_at"]),
        notes=_string(data["notes"], "review notes"),
    )


def _lineage_to_dict(value: LineageLink) -> dict[str, object]:
    return {"role": value.role.value, "reference": _reference_to_dict(value.reference), "statement": value.statement}


def _lineage(value: Any) -> LineageLink:
    data = _object(value, "lineage link")
    _keys(data, {"role", "reference", "statement"}, "lineage link")
    return LineageLink(
        role=_enum(data["role"], ReferenceRole, "lineage role"),
        reference=_reference(data["reference"]),
        statement=_string(data["statement"], "lineage statement"),
    )


def _conflict_to_dict(value: ConflictGroup) -> dict[str, object]:
    return {"conflict_id": value.conflict_id, "subject": value.subject, "members": [_reference_to_dict(item) for item in value.members], "explanation": value.explanation}


def _conflict(value: Any) -> ConflictGroup:
    data = _object(value, "conflict group")
    _keys(data, {"conflict_id", "subject", "members", "explanation"}, "conflict group")
    return ConflictGroup(
        conflict_id=_string(data["conflict_id"], "conflict_id"),
        subject=_string(data["subject"], "conflict subject"),
        members=_references(data["members"], "conflict members"),
        explanation=_string(data["explanation"], "conflict explanation"),
    )


def _exclusion_to_dict(value: Exclusion) -> dict[str, object]:
    return {"state": value.state.value, "reason": _qualifier_to_dict(value.reason), "authority": _qualifier_to_dict(value.authority), "review_context": value.review_context}


def _exclusion(value: Any) -> Exclusion:
    data = _object(value, "exclusion")
    _keys(data, {"state", "reason", "authority", "review_context"}, "exclusion")
    return Exclusion(
        state=_enum(data["state"], ExclusionState, "exclusion state"),
        reason=_qualifier(data["reason"]),
        authority=_qualifier(data["authority"]),
        review_context=_string(data["review_context"], "exclusion review context"),
    )


def _envelope_to_dict(value: RecordEnvelope) -> dict[str, object]:
    return {
        "record_type": value.record_type.value,
        "record_id": value.record_id,
        "record_version": value.record_version,
        "activation": value.activation.value,
        "evidence_class": value.evidence_class.value,
        "model_maturity": value.model_maturity.value,
        "review": _review_to_dict(value.review),
        "source_references": [_reference_to_dict(item) for item in value.source_references],
        "parent_references": [_reference_to_dict(item) for item in value.parent_references],
        "lineage": [_lineage_to_dict(item) for item in value.lineage],
        "conflicts": [_conflict_to_dict(item) for item in value.conflicts],
        "supersedes": None if value.supersedes is None else _reference_to_dict(value.supersedes),
        "synthetic_fixture": value.synthetic_fixture,
    }


def _envelope(value: Any) -> RecordEnvelope:
    data = _object(value, "record envelope")
    _keys(data, {"record_type", "record_id", "record_version", "activation", "evidence_class", "model_maturity", "review", "source_references", "parent_references", "lineage", "conflicts", "supersedes", "synthetic_fixture"}, "record envelope")
    supersedes = data["supersedes"]
    return RecordEnvelope(
        record_type=_enum(data["record_type"], EmpiricalRecordType, "envelope record type"),
        record_id=_string(data["record_id"], "record_id"),
        record_version=_integer(data["record_version"], "record_version"),
        activation=_enum(data["activation"], ActivationState, "activation"),
        evidence_class=_enum(data["evidence_class"], EvidenceClass, "evidence class"),
        model_maturity=_enum(data["model_maturity"], ModelMaturity, "model maturity"),
        review=_review(data["review"]),
        source_references=_references(data["source_references"], "source references"),
        parent_references=_references(data["parent_references"], "parent references"),
        lineage=tuple(_lineage(item) for item in _list(data["lineage"], "lineage")),
        conflicts=tuple(_conflict(item) for item in _list(data["conflicts"], "conflicts")),
        supersedes=None if supersedes is None else _reference(supersedes),
        synthetic_fixture=_boolean(data["synthetic_fixture"], "synthetic_fixture"),
    )


def _component_to_dict(value: ScopedComponentIdentity) -> dict[str, object]:
    return {"component_id": value.component_id, "kind": value.kind.value, "manufacturer": _qualifier_to_dict(value.manufacturer), "product_designation": _qualifier_to_dict(value.product_designation), "revision": _qualifier_to_dict(value.revision), "lot": _qualifier_to_dict(value.lot), "source_wording": value.source_wording, "source_references": [_reference_to_dict(item) for item in value.source_references]}


def _component(value: Any) -> ScopedComponentIdentity:
    data = _object(value, "component identity")
    _keys(data, {"component_id", "kind", "manufacturer", "product_designation", "revision", "lot", "source_wording", "source_references"}, "component identity")
    return ScopedComponentIdentity(
        component_id=_string(data["component_id"], "component_id"),
        kind=_enum(data["kind"], ComponentKind, "component kind"),
        manufacturer=_qualifier(data["manufacturer"]),
        product_designation=_qualifier(data["product_designation"]),
        revision=_qualifier(data["revision"]),
        lot=_qualifier(data["lot"]),
        source_wording=_string(data["source_wording"], "component source wording"),
        source_references=_references(data["source_references"], "component source references"),
    )


def _powder_to_dict(value: PowderIdentityReference) -> dict[str, object]:
    return {"reference": _reference_to_dict(value.reference), "lot": _qualifier_to_dict(value.lot)}


def _powder(value: Any) -> PowderIdentityReference:
    data = _object(value, "powder reference")
    _keys(data, {"reference", "lot"}, "powder reference")
    return PowderIdentityReference(reference=_reference(data["reference"]), lot=_qualifier(data["lot"]))


def _equipment_to_dict(value: EquipmentIdentity) -> dict[str, object]:
    return {"equipment_id": value.equipment_id, "kind": value.kind.value, "organization": _qualifier_to_dict(value.organization), "designation": _qualifier_to_dict(value.designation), "revision": _qualifier_to_dict(value.revision), "source_wording": value.source_wording}


def _equipment(value: Any) -> EquipmentIdentity:
    data = _object(value, "equipment identity")
    _keys(data, {"equipment_id", "kind", "organization", "designation", "revision", "source_wording"}, "equipment identity")
    return EquipmentIdentity(
        equipment_id=_string(data["equipment_id"], "equipment_id"),
        kind=_enum(data["kind"], EquipmentKind, "equipment kind"),
        organization=_qualifier(data["organization"]),
        designation=_qualifier(data["designation"]),
        revision=_qualifier(data["revision"]),
        source_wording=_string(data["source_wording"], "equipment source wording"),
    )


def _pressure_to_dict(value: PressureObservation) -> dict[str, object]:
    return {"reported_value": _reported_value_to_dict(value.reported_value), "quantity": value.quantity.value, "origin": value.origin.value, "location": value.location.value, "acquisition_state": value.acquisition_state.value, "unit": value.unit.value, "source_unit_label": value.source_unit_label, "standard": _reference_or_missing_to_dict(value.standard), "instrument": _reference_or_missing_to_dict(value.instrument), "sensor": _reference_or_missing_to_dict(value.sensor), "calibration": _reference_or_missing_to_dict(value.calibration), "filtering_state": _qualifier_to_dict(value.filtering_state), "peak_definition": _qualifier_to_dict(value.peak_definition), "observation_level": value.observation_level.value}


def _pressure(value: Any) -> PressureObservation:
    data = _object(value, "pressure observation")
    _keys(data, {"reported_value", "quantity", "origin", "location", "acquisition_state", "unit", "source_unit_label", "standard", "instrument", "sensor", "calibration", "filtering_state", "peak_definition", "observation_level"}, "pressure observation")
    return PressureObservation(
        reported_value=_reported_value(data["reported_value"]),
        quantity=_enum(data["quantity"], PressureQuantity, "pressure quantity"),
        origin=_enum(data["origin"], PressureOrigin, "pressure origin"),
        location=_enum(data["location"], PressureLocation, "pressure location"),
        acquisition_state=_enum(data["acquisition_state"], PressureAcquisitionState, "pressure acquisition state"),
        unit=_enum(data["unit"], PressureUnit, "pressure unit"),
        source_unit_label=_string(data["source_unit_label"], "pressure source unit label"),
        standard=_reference_or_missing(data["standard"]), instrument=_reference_or_missing(data["instrument"]),
        sensor=_reference_or_missing(data["sensor"]), calibration=_reference_or_missing(data["calibration"]),
        filtering_state=_qualifier(data["filtering_state"]), peak_definition=_qualifier(data["peak_definition"]),
        observation_level=_enum(data["observation_level"], ObservationLevel, "observation level"),
    )


def _velocity_to_dict(value: VelocityObservation) -> dict[str, object]:
    return {"reported_value": _reported_value_to_dict(value.reported_value), "quantity": value.quantity.value, "correction_state": value.correction_state.value, "unit": value.unit.value, "source_unit_label": value.source_unit_label, "measurement_distance": _quantity_or_missing_to_dict(value.measurement_distance), "correction_method": _reference_or_missing_to_dict(value.correction_method), "atmospheric_context": _qualifier_to_dict(value.atmospheric_context), "instrument": _reference_or_missing_to_dict(value.instrument), "firearm": _reference_or_missing_to_dict(value.firearm), "barrel": _reference_or_missing_to_dict(value.barrel), "observation_level": value.observation_level.value}


def _velocity(value: Any) -> VelocityObservation:
    data = _object(value, "velocity observation")
    _keys(data, {"reported_value", "quantity", "correction_state", "unit", "source_unit_label", "measurement_distance", "correction_method", "atmospheric_context", "instrument", "firearm", "barrel", "observation_level"}, "velocity observation")
    return VelocityObservation(
        reported_value=_reported_value(data["reported_value"]), quantity=_enum(data["quantity"], VelocityQuantity, "velocity quantity"),
        correction_state=_enum(data["correction_state"], VelocityCorrectionState, "velocity correction state"),
        unit=_enum(data["unit"], VelocityUnit, "velocity unit"), source_unit_label=_string(data["source_unit_label"], "velocity source unit label"),
        measurement_distance=_quantity_or_missing(data["measurement_distance"]), correction_method=_reference_or_missing(data["correction_method"]),
        atmospheric_context=_qualifier(data["atmospheric_context"]), instrument=_reference_or_missing(data["instrument"]),
        firearm=_reference_or_missing(data["firearm"]), barrel=_reference_or_missing(data["barrel"]),
        observation_level=_enum(data["observation_level"], ObservationLevel, "observation level"),
    )


def _artifact_to_dict(value: ArtifactReference) -> dict[str, object]:
    return {"artifact_id": value.artifact_id, "retention_state": value.retention_state.value, "sha256": _qualifier_to_dict(value.sha256), "media_type": value.media_type, "custody_reference": _reference_to_dict(value.custody_reference), "custody_limitation": value.custody_limitation}


def _artifact(value: Any) -> ArtifactReference:
    data = _object(value, "artifact reference")
    _keys(data, {"artifact_id", "retention_state", "sha256", "media_type", "custody_reference", "custody_limitation"}, "artifact reference")
    return ArtifactReference(artifact_id=_string(data["artifact_id"], "artifact_id"), retention_state=_enum(data["retention_state"], ArtifactRetentionState, "artifact retention state"), sha256=_qualifier(data["sha256"]), media_type=_string(data["media_type"], "media type"), custody_reference=_reference(data["custody_reference"]), custody_limitation=_string(data["custody_limitation"], "custody limitation"))


def _window_to_dict(value: ExcludedWindow) -> dict[str, object]:
    return {"window_id": value.window_id, "source_wording": value.source_wording, "reason": value.reason}


def _window(value: Any) -> ExcludedWindow:
    data = _object(value, "excluded window")
    _keys(data, {"window_id", "source_wording", "reason"}, "excluded window")
    return ExcludedWindow(window_id=_string(data["window_id"], "window_id"), source_wording=_string(data["source_wording"], "window source wording"), reason=_string(data["reason"], "window reason"))


def _member_to_dict(value: OrderedMember) -> dict[str, object]:
    return {"position": value.position, "reference": _reference_to_dict(value.reference), "source_role": value.source_role}


def _member(value: Any) -> OrderedMember:
    data = _object(value, "ordered member")
    _keys(data, {"position", "reference", "source_role"}, "ordered member")
    return OrderedMember(position=_integer(data["position"], "member position"), reference=_reference(data["reference"]), source_role=_string(data["source_role"], "member source role"))


def _aggregate_value_to_dict(value: Any) -> dict[str, object]:
    if isinstance(value, PressureObservation):
        return {"kind": "pressure", "value": _pressure_to_dict(value)}
    if isinstance(value, VelocityObservation):
        return {"kind": "velocity", "value": _velocity_to_dict(value)}
    if isinstance(value, ReportedValue):
        return {"kind": "reported", "value": _reported_value_to_dict(value)}
    raise TypeError("unsupported aggregate value")


def _aggregate_value(value: Any):
    data = _object(value, "aggregate value")
    _keys(data, {"kind", "value"}, "aggregate value")
    kind = _string(data["kind"], "aggregate value kind")
    if kind == "pressure":
        return _pressure(data["value"])
    if kind == "velocity":
        return _velocity(data["value"])
    if kind == "reported":
        return _reported_value(data["value"])
    raise ValueError(f"unsupported aggregate value kind: {kind!r}")


def _payload_to_dict(record: EmpiricalLoadEvidenceRecord) -> dict[str, object]:
    if isinstance(record, SourceCustodyRecord):
        return {"source_title": record.source_title, "originating_organization": _qualifier_to_dict(record.originating_organization), "edition_or_revision": _qualifier_to_dict(record.edition_or_revision), "locator": _locator_to_dict(record.locator), "acquisition_context": record.acquisition_context, "retention_context": record.retention_context, "artifacts": [_artifact_to_dict(item) for item in record.artifacts], "custody_lineage": [_reference_to_dict(item) for item in record.custody_lineage]}
    if isinstance(record, LiteralLoadStatementRecord):
        return {"source_reference": _reference_to_dict(record.source_reference), "locator": _locator_to_dict(record.locator), "exact_source_wording": record.exact_source_wording, "source_declared_component_wording": list(record.source_declared_component_wording), "declared_values": [_reported_value_to_dict(item) for item in record.declared_values], "qualifications": list(record.qualifications), "conditions": list(record.conditions), "declaration_state": record.declaration_state.value, "unresolved_wording": _qualifier_to_dict(record.unresolved_wording), "normalized_record_references": [_reference_to_dict(item) for item in record.normalized_record_references]}
    if isinstance(record, PhysicalLoadConfigurationRecord):
        return {"cartridge_designation": _qualifier_to_dict(record.cartridge_designation), "powder": _powder_to_dict(record.powder), "bullet": _component_to_dict(record.bullet), "case": _component_to_dict(record.case), "primer": _component_to_dict(record.primer), "charge": _quantity_or_missing_to_dict(record.charge), "geometry_references": [_reference_to_dict(item) for item in record.geometry_references], "equipment": [_equipment_to_dict(item) for item in record.equipment], "preparation": list(record.preparation), "conditions": list(record.conditions), "exclusion": _exclusion_to_dict(record.exclusion)}
    if isinstance(record, ShotObservationRecord):
        return {"load_configuration_reference": _reference_to_dict(record.load_configuration_reference), "acquisition_sequence": record.acquisition_sequence, "acquisition_timestamp": _qualifier_to_dict(record.acquisition_timestamp), "apparatus_references": [_reference_to_dict(item) for item in record.apparatus_references], "conditions": list(record.conditions), "pressure_observations": [_pressure_to_dict(item) for item in record.pressure_observations], "pressure_missing": None if record.pressure_missing is None else _missing_to_dict(record.pressure_missing), "velocity_observations": [_velocity_to_dict(item) for item in record.velocity_observations], "velocity_missing": None if record.velocity_missing is None else _missing_to_dict(record.velocity_missing), "trace_references": [_reference_to_dict(item) for item in record.trace_references], "exclusion": _exclusion_to_dict(record.exclusion), "underlying_test_reference": _reference_or_missing_to_dict(record.underlying_test_reference)}
    if isinstance(record, LoadSeriesRecord):
        return {"members": [_member_to_dict(item) for item in record.members], "purpose": record.purpose, "ordering_variable": _qualifier_to_dict(record.ordering_variable), "changed_variables": list(record.changed_variables), "controlled_variables": list(record.controlled_variables), "stopping_rule": _qualifier_to_dict(record.stopping_rule), "missing_members": [_missing_to_dict(item) for item in record.missing_members]}
    if isinstance(record, PressureTraceMetadataRecord):
        sampling = {"kind": "reported", "value": _reported_value_to_dict(record.sampling_rate)} if isinstance(record.sampling_rate, ReportedValue) else {"kind": "missing", "value": _missing_to_dict(record.sampling_rate)}
        return {"artifact": _artifact_to_dict(record.artifact), "shot_reference": _reference_to_dict(record.shot_reference), "instrument": _reference_or_missing_to_dict(record.instrument), "sensor": _reference_or_missing_to_dict(record.sensor), "channel": _reference_or_missing_to_dict(record.channel), "sampling_rate": sampling, "time_base": _qualifier_to_dict(record.time_base), "trigger_metadata": _qualifier_to_dict(record.trigger_metadata), "alignment_metadata": _qualifier_to_dict(record.alignment_metadata), "pressure_quantity": record.pressure_quantity.value, "pressure_location": record.pressure_location.value, "calibration": _reference_or_missing_to_dict(record.calibration), "artifact_state": record.artifact_state.value, "processing_method": None if record.processing_method is None else _reference_to_dict(record.processing_method), "excluded_windows": [_window_to_dict(item) for item in record.excluded_windows]}
    if isinstance(record, ChronographSeriesRecord):
        return {"members": [_member_to_dict(item) for item in record.members], "instrument": _reference_or_missing_to_dict(record.instrument), "setup": record.setup, "measurement_distance": _quantity_or_missing_to_dict(record.measurement_distance), "correction_state": record.correction_state.value, "correction_method": None if record.correction_method is None else _reference_to_dict(record.correction_method), "atmospheric_context": _qualifier_to_dict(record.atmospheric_context), "firearm": _reference_or_missing_to_dict(record.firearm), "barrel": _reference_or_missing_to_dict(record.barrel), "missing_measurements": [_missing_to_dict(item) for item in record.missing_measurements], "precision": _precision_to_dict(record.precision), "uncertainty": _evidence_uncertainty_to_dict(record.uncertainty)}
    if isinstance(record, AggregateSummaryRecord):
        return {"statistic": record.statistic.value, "statistic_definition": record.statistic_definition, "calculation_origin": record.calculation_origin.value, "calculation_method": None if record.calculation_method is None else _reference_to_dict(record.calculation_method), "value": _aggregate_value_to_dict(record.value), "member_references": [_reference_to_dict(item) for item in record.member_references], "membership_missing": None if record.membership_missing is None else _missing_to_dict(record.membership_missing), "exclusions": [_reference_to_dict(item) for item in record.exclusions], "source_wording": record.source_wording, "precision": _precision_to_dict(record.precision), "uncertainty": _evidence_uncertainty_to_dict(record.uncertainty)}
    raise TypeError("unsupported empirical-load evidence record")


def empirical_load_record_to_dict(record: EmpiricalLoadEvidenceRecord) -> dict[str, object]:
    """Convert one Phase 1 record to its strict tagged serialization object."""

    expected = RECORD_CLASS_BY_TYPE.get(record.envelope.record_type)
    if expected is None or not isinstance(record, expected):
        raise TypeError("record class and envelope discriminator do not match")
    return {"schema": EMPIRICAL_LOAD_EVIDENCE_SCHEMA_ID, "schema_version": 1, "record_type": record.envelope.record_type.value, "envelope": _envelope_to_dict(record.envelope), "payload": _payload_to_dict(record)}


def _parse_payload(record_type: EmpiricalRecordType, envelope: RecordEnvelope, value: Any) -> EmpiricalLoadEvidenceRecord:
    data = _object(value, f"{record_type.value} payload")
    if record_type is EmpiricalRecordType.SOURCE_CUSTODY:
        _keys(data, {"source_title", "originating_organization", "edition_or_revision", "locator", "acquisition_context", "retention_context", "artifacts", "custody_lineage"}, "source custody payload")
        return SourceCustodyRecord(envelope=envelope, source_title=_string(data["source_title"], "source title"), originating_organization=_qualifier(data["originating_organization"]), edition_or_revision=_qualifier(data["edition_or_revision"]), locator=_locator(data["locator"]), acquisition_context=_string(data["acquisition_context"], "acquisition context"), retention_context=_string(data["retention_context"], "retention context"), artifacts=tuple(_artifact(item) for item in _list(data["artifacts"], "artifacts")), custody_lineage=_references(data["custody_lineage"], "custody lineage"))
    if record_type is EmpiricalRecordType.LITERAL_LOAD_STATEMENT:
        _keys(data, {"source_reference", "locator", "exact_source_wording", "source_declared_component_wording", "declared_values", "qualifications", "conditions", "declaration_state", "unresolved_wording", "normalized_record_references"}, "literal statement payload")
        return LiteralLoadStatementRecord(envelope=envelope, source_reference=_reference(data["source_reference"]), locator=_locator(data["locator"]), exact_source_wording=_string(data["exact_source_wording"], "exact source wording"), source_declared_component_wording=_strings(data["source_declared_component_wording"], "component wording"), declared_values=tuple(_reported_value(item) for item in _list(data["declared_values"], "declared values")), qualifications=_strings(data["qualifications"], "qualifications"), conditions=_strings(data["conditions"], "conditions"), declaration_state=_enum(data["declaration_state"], SourceDeclarationState, "declaration state"), unresolved_wording=_qualifier(data["unresolved_wording"]), normalized_record_references=_references(data["normalized_record_references"], "normalized references"))
    if record_type is EmpiricalRecordType.PHYSICAL_LOAD_CONFIGURATION:
        _keys(data, {"cartridge_designation", "powder", "bullet", "case", "primer", "charge", "geometry_references", "equipment", "preparation", "conditions", "exclusion"}, "load configuration payload")
        return PhysicalLoadConfigurationRecord(envelope=envelope, cartridge_designation=_qualifier(data["cartridge_designation"]), powder=_powder(data["powder"]), bullet=_component(data["bullet"]), case=_component(data["case"]), primer=_component(data["primer"]), charge=_quantity_or_missing(data["charge"]), geometry_references=_references(data["geometry_references"], "geometry references"), equipment=tuple(_equipment(item) for item in _list(data["equipment"], "equipment")), preparation=_strings(data["preparation"], "preparation"), conditions=_strings(data["conditions"], "conditions"), exclusion=_exclusion(data["exclusion"]))
    if record_type is EmpiricalRecordType.SHOT_OBSERVATION:
        _keys(data, {"load_configuration_reference", "acquisition_sequence", "acquisition_timestamp", "apparatus_references", "conditions", "pressure_observations", "pressure_missing", "velocity_observations", "velocity_missing", "trace_references", "exclusion", "underlying_test_reference"}, "shot payload")
        pressure_missing, velocity_missing = data["pressure_missing"], data["velocity_missing"]
        return ShotObservationRecord(envelope=envelope, load_configuration_reference=_reference(data["load_configuration_reference"]), acquisition_sequence=_integer(data["acquisition_sequence"], "acquisition sequence"), acquisition_timestamp=_qualifier(data["acquisition_timestamp"]), apparatus_references=_references(data["apparatus_references"], "apparatus references"), conditions=_strings(data["conditions"], "conditions"), pressure_observations=tuple(_pressure(item) for item in _list(data["pressure_observations"], "pressure observations")), pressure_missing=None if pressure_missing is None else _missing(pressure_missing), velocity_observations=tuple(_velocity(item) for item in _list(data["velocity_observations"], "velocity observations")), velocity_missing=None if velocity_missing is None else _missing(velocity_missing), trace_references=_references(data["trace_references"], "trace references"), exclusion=_exclusion(data["exclusion"]), underlying_test_reference=_reference_or_missing(data["underlying_test_reference"]))
    if record_type is EmpiricalRecordType.LOAD_SERIES:
        _keys(data, {"members", "purpose", "ordering_variable", "changed_variables", "controlled_variables", "stopping_rule", "missing_members"}, "load series payload")
        return LoadSeriesRecord(envelope=envelope, members=tuple(_member(item) for item in _list(data["members"], "members")), purpose=_string(data["purpose"], "series purpose"), ordering_variable=_qualifier(data["ordering_variable"]), changed_variables=_strings(data["changed_variables"], "changed variables"), controlled_variables=_strings(data["controlled_variables"], "controlled variables"), stopping_rule=_qualifier(data["stopping_rule"]), missing_members=tuple(_missing(item) for item in _list(data["missing_members"], "missing members")))
    if record_type is EmpiricalRecordType.PRESSURE_TRACE_METADATA:
        _keys(data, {"artifact", "shot_reference", "instrument", "sensor", "channel", "sampling_rate", "time_base", "trigger_metadata", "alignment_metadata", "pressure_quantity", "pressure_location", "calibration", "artifact_state", "processing_method", "excluded_windows"}, "pressure trace payload")
        sampling = _object(data["sampling_rate"], "sampling rate")
        _keys(sampling, {"kind", "value"}, "sampling rate")
        sampling_kind = _string(sampling["kind"], "sampling rate kind")
        if sampling_kind == "reported": sampling_value = _reported_value(sampling["value"])
        elif sampling_kind == "missing": sampling_value = _missing(sampling["value"])
        else: raise ValueError(f"unsupported sampling rate kind: {sampling_kind!r}")
        method = data["processing_method"]
        return PressureTraceMetadataRecord(envelope=envelope, artifact=_artifact(data["artifact"]), shot_reference=_reference(data["shot_reference"]), instrument=_reference_or_missing(data["instrument"]), sensor=_reference_or_missing(data["sensor"]), channel=_reference_or_missing(data["channel"]), sampling_rate=sampling_value, time_base=_qualifier(data["time_base"]), trigger_metadata=_qualifier(data["trigger_metadata"]), alignment_metadata=_qualifier(data["alignment_metadata"]), pressure_quantity=_enum(data["pressure_quantity"], PressureQuantity, "pressure quantity"), pressure_location=_enum(data["pressure_location"], PressureLocation, "pressure location"), calibration=_reference_or_missing(data["calibration"]), artifact_state=_enum(data["artifact_state"], TraceArtifactState, "trace artifact state"), processing_method=None if method is None else _reference(method), excluded_windows=tuple(_window(item) for item in _list(data["excluded_windows"], "excluded windows")))
    if record_type is EmpiricalRecordType.CHRONOGRAPH_SERIES:
        _keys(data, {"members", "instrument", "setup", "measurement_distance", "correction_state", "correction_method", "atmospheric_context", "firearm", "barrel", "missing_measurements", "precision", "uncertainty"}, "chronograph payload")
        method = data["correction_method"]
        return ChronographSeriesRecord(envelope=envelope, members=tuple(_member(item) for item in _list(data["members"], "members")), instrument=_reference_or_missing(data["instrument"]), setup=_string(data["setup"], "chronograph setup"), measurement_distance=_quantity_or_missing(data["measurement_distance"]), correction_state=_enum(data["correction_state"], VelocityCorrectionState, "velocity correction state"), correction_method=None if method is None else _reference(method), atmospheric_context=_qualifier(data["atmospheric_context"]), firearm=_reference_or_missing(data["firearm"]), barrel=_reference_or_missing(data["barrel"]), missing_measurements=tuple(_missing(item) for item in _list(data["missing_measurements"], "missing measurements")), precision=_precision(data["precision"]), uncertainty=_evidence_uncertainty(data["uncertainty"]))
    _keys(data, {"statistic", "statistic_definition", "calculation_origin", "calculation_method", "value", "member_references", "membership_missing", "exclusions", "source_wording", "precision", "uncertainty"}, "aggregate payload")
    method, membership = data["calculation_method"], data["membership_missing"]
    return AggregateSummaryRecord(envelope=envelope, statistic=_enum(data["statistic"], AggregateStatistic, "aggregate statistic"), statistic_definition=_string(data["statistic_definition"], "statistic definition"), calculation_origin=_enum(data["calculation_origin"], AggregateOrigin, "aggregate origin"), calculation_method=None if method is None else _reference(method), value=_aggregate_value(data["value"]), member_references=_references(data["member_references"], "aggregate members"), membership_missing=None if membership is None else _missing(membership), exclusions=_references(data["exclusions"], "aggregate exclusions"), source_wording=_string(data["source_wording"], "aggregate source wording"), precision=_precision(data["precision"]), uncertainty=_evidence_uncertainty(data["uncertainty"]))


def empirical_load_record_from_dict(value: Mapping[str, Any]) -> EmpiricalLoadEvidenceRecord:
    """Parse one strict Phase 1 serialization object without coercion."""

    data = _object(value, "empirical-load record")
    _keys(data, _TOP_FIELDS, "empirical-load record")
    if data["schema"] != EMPIRICAL_LOAD_EVIDENCE_SCHEMA_ID:
        raise ValueError(f"unsupported schema: {data['schema']!r}")
    if _integer(data["schema_version"], "schema_version") != 1:
        raise ValueError(f"unsupported schema version: {data['schema_version']!r}")
    record_type = _enum(data["record_type"], EmpiricalRecordType, "record type")
    envelope = _envelope(data["envelope"])
    if envelope.record_type is not record_type:
        raise ValueError("top-level and envelope record discriminators differ")
    return _parse_payload(record_type, envelope, data["payload"])


def dumps_empirical_load_record(record: EmpiricalLoadEvidenceRecord, *, indent: int | None = 2) -> str:
    """Encode deterministic repository JSON while rejecting non-finite values."""

    if indent is not None and (isinstance(indent, bool) or not isinstance(indent, int) or indent < 0):
        raise ValueError("indent must be a non-negative integer or None")
    return json.dumps(empirical_load_record_to_dict(record), allow_nan=False, indent=indent, sort_keys=True)


def loads_empirical_load_record(payload: str) -> EmpiricalLoadEvidenceRecord:
    """Decode strict JSON, rejecting duplicate keys and non-finite constants."""

    if not isinstance(payload, str):
        raise TypeError("empirical-load JSON payload must be a string")

    def reject_constant(value: str) -> None:
        raise ValueError(f"non-finite JSON number is prohibited: {value}")

    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON object key: {key}")
            result[key] = value
        return result

    try:
        data = json.loads(payload, parse_constant=reject_constant, object_pairs_hook=reject_duplicates)
    except (json.JSONDecodeError, TypeError) as error:
        raise ValueError("invalid empirical-load JSON") from error
    return empirical_load_record_from_dict(data)
