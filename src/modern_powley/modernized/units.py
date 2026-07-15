"""Explicit M01 dimensional quantities and SI conversions."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import isfinite
from numbers import Real
from typing import Any, Mapping


class Dimension(str, Enum):
    """Dimensions supported by M01 public quantities."""
    LENGTH = "length"
    AREA = "area"
    VOLUME = "volume"
    MASS = "mass"
    MASS_PER_AREA = "mass_per_area"
    TEMPERATURE = "temperature"
    MASS_DENSITY = "mass_density"
    RATIO = "ratio"


class Unit(str, Enum):
    """Source and canonical units admitted by M01."""
    METRE = "m"
    CENTIMETRE = "cm"
    MILLIMETRE = "mm"
    INCH = "in"
    SQUARE_METRE = "m2"
    SQUARE_CENTIMETRE = "cm2"
    SQUARE_MILLIMETRE = "mm2"
    SQUARE_INCH = "in2"
    CUBIC_METRE = "m3"
    CUBIC_CENTIMETRE = "cm3"
    CUBIC_MILLIMETRE = "mm3"
    CUBIC_INCH = "in3"
    KILOGRAM = "kg"
    GRAM = "g"
    GRAIN = "grain"
    POUND = "lb"
    KILOGRAM_PER_SQUARE_METRE = "kg/m2"
    KELVIN = "K"
    DEGREE_CELSIUS = "degC"
    KILOGRAM_PER_CUBIC_METRE = "kg/m3"
    GRAM_PER_CUBIC_CENTIMETRE = "g/cm3"
    ONE = "1"


INCH_TO_METRE_EXACT = 0.0254
POUND_TO_KILOGRAM_EXACT = 0.45359237
GRAIN_TO_KILOGRAM_EXACT = POUND_TO_KILOGRAM_EXACT / 7000.0

_UNIT_DIMENSION = {
    Unit.METRE: Dimension.LENGTH,
    Unit.CENTIMETRE: Dimension.LENGTH,
    Unit.MILLIMETRE: Dimension.LENGTH,
    Unit.INCH: Dimension.LENGTH,
    Unit.SQUARE_METRE: Dimension.AREA,
    Unit.SQUARE_CENTIMETRE: Dimension.AREA,
    Unit.SQUARE_MILLIMETRE: Dimension.AREA,
    Unit.SQUARE_INCH: Dimension.AREA,
    Unit.CUBIC_METRE: Dimension.VOLUME,
    Unit.CUBIC_CENTIMETRE: Dimension.VOLUME,
    Unit.CUBIC_MILLIMETRE: Dimension.VOLUME,
    Unit.CUBIC_INCH: Dimension.VOLUME,
    Unit.KILOGRAM: Dimension.MASS,
    Unit.GRAM: Dimension.MASS,
    Unit.GRAIN: Dimension.MASS,
    Unit.POUND: Dimension.MASS,
    Unit.KILOGRAM_PER_SQUARE_METRE: Dimension.MASS_PER_AREA,
    Unit.KELVIN: Dimension.TEMPERATURE,
    Unit.DEGREE_CELSIUS: Dimension.TEMPERATURE,
    Unit.KILOGRAM_PER_CUBIC_METRE: Dimension.MASS_DENSITY,
    Unit.GRAM_PER_CUBIC_CENTIMETRE: Dimension.MASS_DENSITY,
    Unit.ONE: Dimension.RATIO,
}

_TO_SI_FACTOR = {
    Unit.METRE: 1.0,
    Unit.CENTIMETRE: 0.01,
    Unit.MILLIMETRE: 0.001,
    Unit.INCH: INCH_TO_METRE_EXACT,
    Unit.SQUARE_METRE: 1.0,
    Unit.SQUARE_CENTIMETRE: 0.01**2,
    Unit.SQUARE_MILLIMETRE: 0.001**2,
    Unit.SQUARE_INCH: INCH_TO_METRE_EXACT**2,
    Unit.CUBIC_METRE: 1.0,
    Unit.CUBIC_CENTIMETRE: 0.01**3,
    Unit.CUBIC_MILLIMETRE: 0.001**3,
    Unit.CUBIC_INCH: INCH_TO_METRE_EXACT**3,
    Unit.KILOGRAM: 1.0,
    Unit.GRAM: 0.001,
    Unit.GRAIN: GRAIN_TO_KILOGRAM_EXACT,
    Unit.POUND: POUND_TO_KILOGRAM_EXACT,
    Unit.KILOGRAM_PER_SQUARE_METRE: 1.0,
    Unit.KELVIN: 1.0,
    Unit.DEGREE_CELSIUS: 1.0,
    Unit.KILOGRAM_PER_CUBIC_METRE: 1.0,
    Unit.GRAM_PER_CUBIC_CENTIMETRE: 1000.0,
    Unit.ONE: 1.0,
}


def _strict_keys(data: Mapping[str, Any], required: set[str]) -> None:
    if set(data) != required:
        raise ValueError(f"expected fields {sorted(required)}, got {sorted(data)}")


@dataclass(frozen=True, slots=True)
class Quantity:
    """A supplied value/unit pair with a computed canonical SI value."""

    value: float
    unit: Unit

    def __post_init__(self) -> None:
        if isinstance(self.value, bool) or not isinstance(self.value, Real):
            raise TypeError("quantity value must be a real JSON-compatible number")
        value = float(self.value)
        if not isfinite(value):
            raise ValueError("quantity value must be finite")
        object.__setattr__(self, "value", value)
        if not isinstance(self.unit, Unit):
            object.__setattr__(self, "unit", Unit(self.unit))

    @property
    def dimension(self) -> Dimension:
        return _UNIT_DIMENSION[self.unit]

    @property
    def si_value(self) -> float:
        if self.unit is Unit.DEGREE_CELSIUS:
            return self.value + 273.15
        return self.value * _TO_SI_FACTOR[self.unit]

    def to(self, unit: Unit) -> Quantity:
        target = Unit(unit)
        if _UNIT_DIMENSION[target] is not self.dimension:
            raise ValueError(f"cannot convert {self.dimension.value} to {_UNIT_DIMENSION[target].value}")
        if target is Unit.DEGREE_CELSIUS:
            value = self.si_value - 273.15
        else:
            value = self.si_value / _TO_SI_FACTOR[target]
        return Quantity(value, target)

    def to_dict(self) -> dict[str, object]:
        return {"value": self.value, "unit": self.unit.value}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Quantity:
        _strict_keys(data, {"value", "unit"})
        return cls(data["value"], Unit(str(data["unit"])))


def require_dimension(quantity: Quantity, dimension: Dimension, name: str) -> Quantity:
    if quantity.dimension is not dimension:
        raise ValueError(f"{name} must have dimension {dimension.value}")
    return quantity


def require_positive(quantity: Quantity, dimension: Dimension, name: str) -> Quantity:
    require_dimension(quantity, dimension, name)
    if quantity.si_value <= 0:
        raise ValueError(f"{name} must be greater than zero")
    return quantity


def require_nonnegative(quantity: Quantity, dimension: Dimension, name: str) -> Quantity:
    require_dimension(quantity, dimension, name)
    if quantity.si_value < 0:
        raise ValueError(f"{name} must be non-negative")
    return quantity
