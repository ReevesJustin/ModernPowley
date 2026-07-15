"""M01 evidence, maturity, origin, and derivation metadata."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping


class EvidenceClass(str, Enum):
    """Controlled evidence identity for modernized records and methods."""
    ORIGINAL_POWLEY_PRIMARY = "original_powley_primary"
    LATER_POWLEY_ASSOCIATED_PRIMARY = "later_powley_associated_primary"
    OTHER_PUBLISHED_PRIMARY = "other_published_primary"
    MANUFACTURER_PUBLISHED = "manufacturer_published"
    INDEPENDENT_LABORATORY_MEASUREMENT = "independent_laboratory_measurement"
    USER_MEASUREMENT = "user_measurement"
    SECONDARY_TRANSCRIPTION = "secondary_transcription"
    REVERSE_ENGINEERED = "reverse_engineered"
    EMPIRICAL_FIT = "empirical_fit"
    CALIBRATED_PARAMETER = "calibrated_parameter"
    EXPLORATORY_HYPOTHESIS = "exploratory_hypothesis"
    DERIVED_QUANTITY = "derived_quantity"


class ModelMaturity(str, Enum):
    """Lifecycle state independent of evidence class or confidence."""
    RETAINED_CANDIDATE = "retained_candidate"
    TRANSCRIBED = "transcribed"
    DIMENSIONALLY_AUDITED = "dimensionally_audited"
    SOURCE_RECONCILED = "source_reconciled"
    IMPLEMENTED_EXPERIMENTAL = "implemented_experimental"
    MEASURED_VALIDATED = "measured_validated"
    PROMOTED_MODERN = "promoted_modern"
    DEPRECATED = "deprecated"
    REJECTED = "rejected"


class ValueOrigin(str, Enum):
    """How a supplied or derived value entered the repository."""
    MEASURED = "measured"
    MANUFACTURER_PUBLISHED = "manufacturer_published"
    OTHER_PUBLISHED = "other_published"
    TRANSCRIBED = "transcribed"
    INFERRED = "inferred"
    ASSUMED = "assumed"
    DERIVED = "derived"
    FITTED = "fitted"
    CALIBRATED = "calibrated"


@dataclass(frozen=True, slots=True)
class Provenance:
    """Immutable source, origin, maturity, and derivation metadata."""
    evidence_class: EvidenceClass
    origin: ValueOrigin
    source_id: str
    model_maturity: ModelMaturity
    method_id: str | None = None
    input_record_ids: tuple[str, ...] = ()
    notes: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "evidence_class", EvidenceClass(self.evidence_class))
        object.__setattr__(self, "origin", ValueOrigin(self.origin))
        object.__setattr__(self, "model_maturity", ModelMaturity(self.model_maturity))
        if not self.source_id.strip():
            raise ValueError("provenance source_id is required")
        if self.origin is ValueOrigin.DERIVED:
            if not self.method_id or not self.input_record_ids:
                raise ValueError("derived provenance requires method_id and input_record_ids")
        elif self.method_id is not None or self.input_record_ids:
            raise ValueError("supplied provenance cannot carry derived method inputs")

    def to_dict(self) -> dict[str, object]:
        return {
            "evidence_class": self.evidence_class.value,
            "origin": self.origin.value,
            "source_id": self.source_id,
            "model_maturity": self.model_maturity.value,
            "method_id": self.method_id,
            "input_record_ids": list(self.input_record_ids),
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Provenance:
        required = {"evidence_class", "origin", "source_id", "model_maturity", "method_id", "input_record_ids", "notes"}
        if set(data) != required:
            raise ValueError("malformed provenance fields")
        inputs = data["input_record_ids"]
        if not isinstance(inputs, list) or not all(isinstance(item, str) for item in inputs):
            raise ValueError("input_record_ids must be a string list")
        return cls(
            EvidenceClass(str(data["evidence_class"])),
            ValueOrigin(str(data["origin"])),
            str(data["source_id"]),
            ModelMaturity(str(data["model_maturity"])),
            None if data["method_id"] is None else str(data["method_id"]),
            tuple(inputs),
            str(data["notes"]),
        )


def derived_provenance(method_id: str, input_record_ids: tuple[str, ...]) -> Provenance:
    """Create promoted M01 provenance for a deterministic derived value."""
    return Provenance(
        evidence_class=EvidenceClass.DERIVED_QUANTITY,
        origin=ValueOrigin.DERIVED,
        source_id="SRC-M01-DESIGN",
        model_maturity=ModelMaturity.PROMOTED_MODERN,
        method_id=method_id,
        input_record_ids=input_record_ids,
    )
