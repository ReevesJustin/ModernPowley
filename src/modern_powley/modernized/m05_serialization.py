"""Strict `modern_powley.m05.v1` serialization."""

from __future__ import annotations

import json
from collections.abc import Mapping
from numbers import Real
from typing import Any

from .charge_regions import (
    M05_SCHEMA_ID, ActivationStatus, ChargeMassEndpoint, ChargeMassSegment,
    ChargeRegionRecord, DependencyStatus, EndpointInclusion, ExactRecordReference,
    ExactReferenceRole, LifecycleMetadata, MethodReference, NonImplicationDeclaration,
    PressureEvidenceContext, RegionBasis, RegionState, UncertaintyDeclaration,
    UncertaintyDeclarationKind, VersionedRegionReference,
)
from .property_observations import SourceLocator, TranscriptionStatus
from .provenance import EvidenceClass, ModelMaturity, Provenance, ValueOrigin
from .units import Quantity, Unit


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
    if value is None:
        return None
    return _string(value, name)


def _integer(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    return value


def _list(value: Any, name: str) -> list[Any]:
    if not isinstance(value, list):
        raise TypeError(f"{name} must be a list")
    return value


def _string_tuple(value: Any, name: str) -> tuple[str, ...]:
    return tuple(_string(item, name) for item in _list(value, name))


def _quantity(value: Any) -> Quantity:
    data = _object(value, "quantity")
    _keys(data, {"value", "unit"}, "quantity")
    number = data["value"]
    if isinstance(number, bool) or not isinstance(number, Real):
        raise TypeError("quantity value must be a number")
    return Quantity(number, Unit(_string(data["unit"], "quantity unit")))


def _reference(value: Any) -> ExactRecordReference:
    data = _object(value, "exact reference")
    _keys(data, {"role", "schema_id", "record_type", "record_id", "version", "evidence_class", "model_maturity"}, "exact reference")
    version = data["version"]
    return ExactRecordReference(
        ExactReferenceRole(_string(data["role"], "reference role")),
        _string(data["schema_id"], "reference schema_id"),
        _string(data["record_type"], "reference record_type"),
        _string(data["record_id"], "reference record_id"),
        None if version is None else _integer(version, "reference version"),
        EvidenceClass(_string(data["evidence_class"], "reference evidence_class")),
        ModelMaturity(_string(data["model_maturity"], "reference model_maturity")),
    )


def _references(value: Any, name: str) -> tuple[ExactRecordReference, ...]:
    return tuple(_reference(item) for item in _list(value, name))


def _provenance(value: Any) -> Provenance:
    data = _object(value, "provenance")
    _keys(data, {"evidence_class", "origin", "source_id", "model_maturity", "method_id", "input_record_ids", "notes"}, "provenance")
    return Provenance(
        EvidenceClass(_string(data["evidence_class"], "provenance evidence_class")),
        ValueOrigin(_string(data["origin"], "provenance origin")),
        _string(data["source_id"], "provenance source_id"),
        ModelMaturity(_string(data["model_maturity"], "provenance model_maturity")),
        _optional_string(data["method_id"], "provenance method_id"),
        _string_tuple(data["input_record_ids"], "provenance input_record_ids"),
        _string(data["notes"], "provenance notes"),
    )


def _locator(value: Any) -> SourceLocator:
    data = _object(value, "source locator")
    _keys(data, {"source_id", "locator", "transcription_status"}, "source locator")
    return SourceLocator(_string(data["source_id"], "locator source_id"), _string(data["locator"], "locator"), TranscriptionStatus(_string(data["transcription_status"], "transcription status")))


def _method(value: Any) -> MethodReference:
    data = _object(value, "method")
    _keys(data, {"method_id", "version", "authority_reference", "model_maturity", "status"}, "method")
    return MethodReference(_string(data["method_id"], "method_id"), _integer(data["version"], "method version"), _reference(data["authority_reference"]), ModelMaturity(_string(data["model_maturity"], "method maturity")), _string(data["status"], "method status"))


def _endpoint(value: Any) -> ChargeMassEndpoint:
    data = _object(value, "endpoint")
    _keys(data, {"quantity", "inclusion", "source_reported_value", "reported_precision", "source_references", "qualifications"}, "endpoint")
    return ChargeMassEndpoint(_quantity(data["quantity"]), EndpointInclusion(_string(data["inclusion"], "endpoint inclusion")), _optional_string(data["source_reported_value"], "source reported value"), _optional_string(data["reported_precision"], "reported precision"), _references(data["source_references"], "endpoint source references"), _string_tuple(data["qualifications"], "endpoint qualifications"))


def _segment(value: Any) -> ChargeMassSegment:
    data = _object(value, "segment")
    _keys(data, {"lower", "upper"}, "segment")
    return ChargeMassSegment(_endpoint(data["lower"]), _endpoint(data["upper"]))


def _uncertainty(value: Any) -> UncertaintyDeclaration:
    data = _object(value, "uncertainty")
    _keys(data, {"kind", "description", "references"}, "uncertainty")
    return UncertaintyDeclaration(UncertaintyDeclarationKind(_string(data["kind"], "uncertainty kind")), _string(data["description"], "uncertainty description"), _references(data["references"], "uncertainty references"))


def _pressure(value: Any) -> PressureEvidenceContext:
    data = _object(value, "pressure context")
    _keys(data, {"evidence_reference", "pressure_quantity_identity", "measurement_method", "standard_or_protocol", "instrument_type", "source_unit_label", "conditions", "source_locator", "source_limitations"}, "pressure context")
    return PressureEvidenceContext(_reference(data["evidence_reference"]), _string(data["pressure_quantity_identity"], "pressure quantity"), _string(data["measurement_method"], "measurement method"), _string(data["standard_or_protocol"], "standard/protocol"), _string(data["instrument_type"], "instrument type"), _string(data["source_unit_label"], "source unit label"), _string_tuple(data["conditions"], "pressure conditions"), _locator(data["source_locator"]), _string_tuple(data["source_limitations"], "pressure limitations"))


def _lifecycle(value: Any) -> LifecycleMetadata:
    data = _object(value, "lifecycle")
    _keys(data, {"activation", "supersedes"}, "lifecycle")
    supersedes_data = data["supersedes"]
    supersedes = None
    if supersedes_data is not None:
        item = _object(supersedes_data, "supersedes")
        _keys(item, {"region_id", "version"}, "supersedes")
        supersedes = VersionedRegionReference(_string(item["region_id"], "superseded region_id"), _integer(item["version"], "superseded version"))
    return LifecycleMetadata(ActivationStatus(_string(data["activation"], "activation")), supersedes)


_RECORD_FIELDS = {
    "schema", "record_type", "record_id", "region_id", "version", "state", "basis", "method", "segments",
    "m01_input_references", "m02_evidence_references", "m03_diagnostic_references", "m04_audit_references",
    "applicability_references", "provenance", "source_locator", "source_wording", "reported_precision", "conditions",
    "uncertainty", "dependency_status", "dependency_references", "conflict_references", "qualifications",
    "derivation_lineage", "pressure_contexts", "lifecycle", "explanation", "non_implication",
}


def m05_record_to_dict(record: ChargeRegionRecord) -> dict[str, object]:
    """Serialize one M05 record without transforming it."""
    if not isinstance(record, ChargeRegionRecord):
        raise TypeError("unsupported M05 record type")
    return record.to_dict()


def m05_record_from_dict(value: Mapping[str, Any]) -> ChargeRegionRecord:
    """Parse one strict M05 record without coercion or migration."""
    data = _object(value, "M05 record")
    _keys(data, _RECORD_FIELDS, "M05 record")
    if data["schema"] != M05_SCHEMA_ID:
        raise ValueError(f"unsupported schema: {data['schema']!r}")
    if data["record_type"] != "charge_region_record":
        raise ValueError(f"unsupported record_type: {data['record_type']!r}")
    basis_value, method_value = data["basis"], data["method"]
    return ChargeRegionRecord(
        _string(data["record_id"], "record_id"), _string(data["region_id"], "region_id"), _integer(data["version"], "version"),
        RegionState(_string(data["state"], "state")), None if basis_value is None else RegionBasis(_string(basis_value, "basis")),
        None if method_value is None else _method(method_value), tuple(_segment(item) for item in _list(data["segments"], "segments")),
        _references(data["m01_input_references"], "M01 references"), _references(data["m02_evidence_references"], "M02 references"),
        _references(data["m03_diagnostic_references"], "M03 references"), _references(data["m04_audit_references"], "M04 references"),
        _references(data["applicability_references"], "applicability references"), _provenance(data["provenance"]), _locator(data["source_locator"]),
        _string(data["source_wording"], "source_wording"), _optional_string(data["reported_precision"], "reported_precision"),
        _string_tuple(data["conditions"], "conditions"), _uncertainty(data["uncertainty"]),
        DependencyStatus(_string(data["dependency_status"], "dependency_status")), _references(data["dependency_references"], "dependency references"),
        _references(data["conflict_references"], "conflict references"), _string_tuple(data["qualifications"], "qualifications"),
        _references(data["derivation_lineage"], "derivation lineage"), tuple(_pressure(item) for item in _list(data["pressure_contexts"], "pressure contexts")),
        _lifecycle(data["lifecycle"]), _optional_string(data["explanation"], "explanation"),
        NonImplicationDeclaration(_string(data["non_implication"], "non_implication")),
    )


def dumps_m05_record(record: ChargeRegionRecord, *, indent: int | None = 2) -> str:
    """Encode deterministic strict M05 JSON."""
    if indent is not None and (isinstance(indent, bool) or not isinstance(indent, int) or indent < 0):
        raise ValueError("indent must be a non-negative integer or None")
    return json.dumps(m05_record_to_dict(record), allow_nan=False, indent=indent, sort_keys=True)


def loads_m05_record(payload: str) -> ChargeRegionRecord:
    """Decode strict M05 JSON, rejecting duplicate keys and non-finite values."""
    if not isinstance(payload, str):
        raise TypeError("M05 JSON payload must be a string")

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
        raise ValueError("invalid M05 JSON") from error
    return m05_record_from_dict(data)
