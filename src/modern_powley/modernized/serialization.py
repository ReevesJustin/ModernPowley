"""Strict versioned JSON serialization for M01 top-level records."""

from __future__ import annotations

import json
from typing import Any, Mapping, TypeAlias

from .records import (
    CapacityComparison,
    CartridgeIdentity,
    EstimatedUsablePowderSpace,
    FirearmRecord,
    GrossCaseCapacity,
    MeasuredUsablePowderSpace,
    PrimerPocketVolume,
    ProjectileRecord,
    SCHEMA_ID,
)

M01Record: TypeAlias = CartridgeIdentity | GrossCaseCapacity | MeasuredUsablePowderSpace | PrimerPocketVolume | ProjectileRecord | FirearmRecord | EstimatedUsablePowderSpace | CapacityComparison

_RECORD_TYPES = {
    "cartridge_identity": CartridgeIdentity,
    "gross_case_capacity": GrossCaseCapacity,
    "measured_usable_powder_space": MeasuredUsablePowderSpace,
    "primer_pocket_volume": PrimerPocketVolume,
    "projectile": ProjectileRecord,
    "firearm": FirearmRecord,
    "estimated_usable_powder_space": EstimatedUsablePowderSpace,
    "capacity_comparison": CapacityComparison,
}


def record_to_dict(record: M01Record) -> dict[str, object]:
    """Serialize a supported M01 record to a strict tagged dictionary."""
    return record.to_dict()


def record_from_dict(data: Mapping[str, Any]) -> M01Record:
    """Parse a strict `modern_powley.m01.v1` tagged dictionary."""
    if not isinstance(data, Mapping):
        raise ValueError("M01 record must be an object")
    if "schema" not in data:
        raise ValueError("M01 record is missing schema")
    if data["schema"] != SCHEMA_ID:
        raise ValueError(f"unsupported schema: {data['schema']!r}")
    if "record_type" not in data:
        raise ValueError("M01 record is missing record_type")
    try:
        record_type = _RECORD_TYPES[str(data["record_type"])]
    except KeyError as error:
        raise ValueError(f"unsupported record_type: {data['record_type']!r}") from error
    return record_type.from_dict(data)


def dumps_record(record: M01Record, *, indent: int | None = 2) -> str:
    """Encode a record as deterministic JSON with non-finite values disabled."""
    return json.dumps(record_to_dict(record), allow_nan=False, indent=indent, sort_keys=True)


def loads_record(payload: str) -> M01Record:
    """Decode strict M01 JSON without accepting NaN or infinity."""
    def reject_constant(value: str) -> None:
        raise ValueError(f"non-finite JSON number is prohibited: {value}")

    try:
        data = json.loads(payload, parse_constant=reject_constant)
    except (json.JSONDecodeError, TypeError) as error:
        raise ValueError("invalid M01 JSON") from error
    return record_from_dict(data)
