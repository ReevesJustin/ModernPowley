"""Strict versioned JSON serialization for M02 powder-property records."""

from __future__ import annotations

import json
from typing import Any, Mapping, TypeAlias

from .powder_identity import M02_SCHEMA_ID, PowderIdentity, PowderIdentityRelationship
from .property_observations import MissingPropertyObservation, PowderPropertyObservation
from .property_conflicts import ConflictComparison

M02Record: TypeAlias = PowderIdentity | PowderIdentityRelationship | PowderPropertyObservation | MissingPropertyObservation | ConflictComparison

_RECORD_TYPES = {
    "powder_identity": PowderIdentity,
    "powder_identity_relationship": PowderIdentityRelationship,
    "powder_property_observation": PowderPropertyObservation,
    "missing_property_observation": MissingPropertyObservation,
    "conflict_comparison": ConflictComparison,
}


def m02_record_to_dict(record: M02Record) -> dict[str, object]:
    """Serialize one supported M02 record to a tagged dictionary."""

    return record.to_dict()


def m02_record_from_dict(data: Mapping[str, Any]) -> M02Record:
    """Parse a strict `modern_powley.m02.v1` tagged dictionary."""

    if not isinstance(data, Mapping):
        raise ValueError("M02 record must be an object")
    if "schema" not in data:
        raise ValueError("M02 record is missing schema")
    if data["schema"] != M02_SCHEMA_ID:
        raise ValueError(f"unsupported schema: {data['schema']!r}")
    if "record_type" not in data:
        raise ValueError("M02 record is missing record_type")
    try:
        record_type = _RECORD_TYPES[str(data["record_type"])]
    except KeyError as error:
        raise ValueError(f"unsupported record_type: {data['record_type']!r}") from error
    return record_type.from_dict(data)


def dumps_m02_record(record: M02Record, *, indent: int | None = 2) -> str:
    """Encode deterministic M02 JSON while rejecting NaN and infinity."""

    return json.dumps(m02_record_to_dict(record), allow_nan=False, indent=indent, sort_keys=True)


def loads_m02_record(payload: str) -> M02Record:
    """Decode strict M02 JSON without accepting non-finite constants."""

    def reject_constant(value: str) -> None:
        raise ValueError(f"non-finite JSON number is prohibited: {value}")

    try:
        data = json.loads(payload, parse_constant=reject_constant)
    except (json.JSONDecodeError, TypeError) as error:
        raise ValueError("invalid M02 JSON") from error
    return m02_record_from_dict(data)
