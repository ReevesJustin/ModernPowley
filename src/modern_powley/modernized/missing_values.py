"""Semantic missing-value states shared by M02 records."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping


class MissingState(str, Enum):
    """Why a value is unavailable; no state is represented by zero or NaN."""

    NOT_SUPPLIED_BY_SOURCE = "not_supplied_by_source"
    NOT_PUBLISHED = "not_published"
    NOT_MEASURED = "not_measured"
    NOT_APPLICABLE = "not_applicable"
    UNKNOWN = "unknown"
    UNRESOLVED_TRANSCRIPTION = "unresolved_transcription"
    ILLEGIBLE_IN_SOURCE = "illegible_in_source"
    CONFLICTING_EVIDENCE = "conflicting_evidence"
    OUTSIDE_SOURCE_DOMAIN = "outside_source_domain"
    WITHHELD_OR_PROPRIETARY = "withheld_or_proprietary"
    NOT_YET_ENTERED = "not_yet_entered"
    UNSUPPORTED_BY_ACCEPTED_EVIDENCE = "unsupported_by_accepted_evidence"
    INTENTIONALLY_UNAVAILABLE_AT_CURRENT_MATURITY = (
        "intentionally_unavailable_at_current_maturity"
    )


def _strict(data: Mapping[str, Any], fields: set[str]) -> None:
    if set(data) != fields:
        raise ValueError(f"expected fields {sorted(fields)}, got {sorted(data)}")


@dataclass(frozen=True, slots=True)
class IdentityQualifier:
    """A present identity qualifier or an explicit semantic missing state."""

    value: str | None
    missing_state: MissingState | None
    explanation: str

    def __post_init__(self) -> None:
        if self.missing_state is not None:
            object.__setattr__(self, "missing_state", MissingState(self.missing_state))
        has_value = self.value is not None
        has_missing = self.missing_state is not None
        if has_value == has_missing:
            raise ValueError("identity qualifier requires exactly one of value or missing_state")
        if has_value and not str(self.value).strip():
            raise ValueError("identity qualifier value must be nonblank")
        if has_missing and not self.explanation.strip():
            raise ValueError("missing identity qualifier requires explanation")

    @classmethod
    def present(cls, value: str, explanation: str = "") -> IdentityQualifier:
        """Create a qualifier whose literal value is known."""

        return cls(value, None, explanation)

    @classmethod
    def missing(cls, state: MissingState, explanation: str) -> IdentityQualifier:
        """Create a qualifier with a semantic missing state."""

        return cls(None, state, explanation)

    def to_dict(self) -> dict[str, object]:
        return {
            "value": self.value,
            "missing_state": None if self.missing_state is None else self.missing_state.value,
            "explanation": self.explanation,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> IdentityQualifier:
        """Parse a strict identity qualifier."""

        _strict(data, {"value", "missing_state", "explanation"})
        return cls(
            None if data["value"] is None else str(data["value"]),
            None if data["missing_state"] is None else MissingState(str(data["missing_state"])),
            str(data["explanation"]),
        )
