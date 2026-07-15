"""Bounded scalar uncertainty for M01 quantities."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from .units import Quantity, require_dimension, require_nonnegative


class UncertaintyKind(str, Enum):
    """Supported bounded scalar uncertainty representations."""
    UNKNOWN = "unknown"
    INSTRUMENT_RESOLUTION = "instrument_resolution"
    SYMMETRIC_ABSOLUTE = "symmetric_absolute"
    BOUNDED_INTERVAL = "bounded_interval"


@dataclass(frozen=True, slots=True)
class Uncertainty:
    """Explicit scalar uncertainty; unknown is distinct from zero."""
    kind: UncertaintyKind
    magnitude: Quantity | None = None
    lower: Quantity | None = None
    upper: Quantity | None = None
    justification: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.kind, UncertaintyKind):
            object.__setattr__(self, "kind", UncertaintyKind(self.kind))
        if self.kind is UncertaintyKind.UNKNOWN:
            if any(value is not None for value in (self.magnitude, self.lower, self.upper)):
                raise ValueError("unknown uncertainty cannot contain bounds")
        elif self.kind in {UncertaintyKind.INSTRUMENT_RESOLUTION, UncertaintyKind.SYMMETRIC_ABSOLUTE}:
            if self.magnitude is None or self.lower is not None or self.upper is not None:
                raise ValueError("resolution and symmetric uncertainty require only magnitude")
            require_nonnegative(self.magnitude, self.magnitude.dimension, "uncertainty magnitude")
            if self.magnitude.si_value == 0 and not self.justification.strip():
                raise ValueError("zero uncertainty requires justification")
        elif self.kind is UncertaintyKind.BOUNDED_INTERVAL:
            if self.magnitude is not None or self.lower is None or self.upper is None:
                raise ValueError("bounded uncertainty requires lower and upper")
            require_dimension(self.upper, self.lower.dimension, "upper uncertainty bound")
            if self.lower.si_value > self.upper.si_value:
                raise ValueError("uncertainty bounds must be ordered")

    @classmethod
    def unknown(cls) -> Uncertainty:
        return cls(UncertaintyKind.UNKNOWN)

    def validate_for(self, quantity: Quantity) -> None:
        for value in (self.magnitude, self.lower, self.upper):
            if value is not None:
                require_dimension(value, quantity.dimension, "uncertainty")

    def to_dict(self) -> dict[str, object]:
        data: dict[str, object] = {"kind": self.kind.value, "justification": self.justification}
        if self.magnitude is not None:
            data["magnitude"] = self.magnitude.to_dict()
        if self.lower is not None:
            data["lower"] = self.lower.to_dict()
        if self.upper is not None:
            data["upper"] = self.upper.to_dict()
        return data

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Uncertainty:
        allowed = {"kind", "justification", "magnitude", "lower", "upper"}
        if not {"kind", "justification"} <= set(data) or set(data) - allowed:
            raise ValueError("malformed uncertainty fields")
        parse = lambda key: None if key not in data else Quantity.from_dict(data[key])
        return cls(
            UncertaintyKind(str(data["kind"])),
            magnitude=parse("magnitude"),
            lower=parse("lower"),
            upper=parse("upper"),
            justification=str(data["justification"]),
        )
