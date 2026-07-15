"""Strict versioned JSON serialization for M04 decision records."""

from __future__ import annotations

import json
from typing import Any, Mapping, TypeAlias

from .screening_contexts import EvaluationContext
from .screening_criteria import CriterionDefinition, CriterionSetDefinition, M04_SCHEMA_ID
from .screening_outcomes import CriterionEvaluationRecord, CriterionSetOutcomeRecord


M04Record: TypeAlias = (
    CriterionDefinition
    | CriterionSetDefinition
    | EvaluationContext
    | CriterionEvaluationRecord
    | CriterionSetOutcomeRecord
)

_RECORD_TYPES = {
    "criterion_definition": CriterionDefinition,
    "criterion_set_definition": CriterionSetDefinition,
    "evaluation_context": EvaluationContext,
    "criterion_evaluation": CriterionEvaluationRecord,
    "criterion_set_outcome": CriterionSetOutcomeRecord,
}


def m04_record_to_dict(record: M04Record) -> dict[str, object]:
    """Serialize one supported M04 record to a tagged dictionary."""

    return record.to_dict()


def m04_record_from_dict(data: Mapping[str, Any]) -> M04Record:
    """Parse one strict `modern_powley.m04.v1` tagged dictionary."""

    if not isinstance(data, Mapping):
        raise ValueError("M04 record must be an object")
    if "schema" not in data:
        raise ValueError("M04 record is missing schema")
    if data["schema"] != M04_SCHEMA_ID:
        raise ValueError(f"unsupported schema: {data['schema']!r}")
    if "record_type" not in data:
        raise ValueError("M04 record is missing record_type")
    try:
        record_type = _RECORD_TYPES[str(data["record_type"])]
    except KeyError as error:
        raise ValueError(f"unsupported record_type: {data['record_type']!r}") from error
    return record_type.from_dict(data)


def dumps_m04_record(record: M04Record, *, indent: int | None = 2) -> str:
    """Encode deterministic M04 JSON while rejecting NaN and infinity."""

    return json.dumps(m04_record_to_dict(record), allow_nan=False, indent=indent, sort_keys=True)


def loads_m04_record(payload: str) -> M04Record:
    """Decode strict M04 JSON without accepting non-finite constants."""

    def reject_constant(value: str) -> None:
        raise ValueError(f"non-finite JSON number is prohibited: {value}")

    try:
        data = json.loads(payload, parse_constant=reject_constant)
    except (json.JSONDecodeError, TypeError) as error:
        raise ValueError("invalid M04 JSON") from error
    return m04_record_from_dict(data)
