"""Strict versioned JSON serialization for M03 diagnostic records."""

from __future__ import annotations

import json
from typing import Any, Mapping, TypeAlias

from .domain_diagnostics import ApplicabilityEvaluation, DomainQueryContext
from .input_completeness import CompletenessEvaluation
from .input_requirements import M03_SCHEMA_ID, InputBundle, RequirementSet

M03Record: TypeAlias = RequirementSet | InputBundle | CompletenessEvaluation | DomainQueryContext | ApplicabilityEvaluation

_RECORD_TYPES = {
    "requirement_set": RequirementSet,
    "input_bundle": InputBundle,
    "completeness_evaluation": CompletenessEvaluation,
    "domain_query_context": DomainQueryContext,
    "applicability_evaluation": ApplicabilityEvaluation,
}


def m03_record_to_dict(record: M03Record) -> dict[str, object]:
    """Serialize one supported M03 record to a tagged dictionary."""

    return record.to_dict()


def m03_record_from_dict(data: Mapping[str, Any]) -> M03Record:
    """Parse one strict `modern_powley.m03.v1` tagged dictionary."""

    if not isinstance(data, Mapping):
        raise ValueError("M03 record must be an object")
    if "schema" not in data:
        raise ValueError("M03 record is missing schema")
    if data["schema"] != M03_SCHEMA_ID:
        raise ValueError(f"unsupported schema: {data['schema']!r}")
    if "record_type" not in data:
        raise ValueError("M03 record is missing record_type")
    try:
        record_type = _RECORD_TYPES[str(data["record_type"])]
    except KeyError as error:
        raise ValueError(f"unsupported record_type: {data['record_type']!r}") from error
    return record_type.from_dict(data)


def dumps_m03_record(record: M03Record, *, indent: int | None = 2) -> str:
    """Encode deterministic M03 JSON while rejecting NaN and infinity."""

    return json.dumps(m03_record_to_dict(record), allow_nan=False, indent=indent, sort_keys=True)


def loads_m03_record(payload: str) -> M03Record:
    """Decode strict M03 JSON without accepting non-finite constants."""

    def reject_constant(value: str) -> None:
        raise ValueError(f"non-finite JSON number is prohibited: {value}")

    try:
        data = json.loads(payload, parse_constant=reject_constant)
    except (json.JSONDecodeError, TypeError) as error:
        raise ValueError("invalid M03 JSON") from error
    return m03_record_from_dict(data)
