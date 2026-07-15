"""Controlled M02 powder-property definitions and tagged reported values."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import isfinite
from numbers import Real
from types import MappingProxyType
from typing import Any, Mapping, TypeAlias

from .records import PhysicalValue
from .units import Dimension, require_dimension


class PropertyId(str, Enum):
    """Neutral property identities; no member implies computational approval."""

    BULK_DENSITY = "bulk_density"
    GRAVIMETRIC_DENSITY = "gravimetric_density"
    HEAT_OF_EXPLOSION = "heat_of_explosion"
    FORCE = "force"
    IMPETUS = "impetus"
    COVOLUME = "covolume"
    SPECIFIC_HEAT_RATIO = "specific_heat_ratio"
    GRAIN_DIMENSION = "grain_dimension"
    GRAIN_FORM = "grain_form"
    PERFORATION_COUNT = "perforation_count"
    CLOSED_BOMB_REPORTED_VALUE = "closed_bomb_reported_value"
    VIVACITY_REPORTED = "vivacity_reported"
    BURN_RATE_COEFFICIENT_REPORTED = "burn_rate_coefficient_reported"
    MANUFACTURER_RELATIVE_BURN_RATE_POSITION = "manufacturer_relative_burn_rate_position"
    SOURCE_SPECIFIC_COEFFICIENT = "source_specific_coefficient"
    COMPOSITION_CATEGORY = "composition_category"
    MOISTURE_CONTENT = "moisture_content"
    TEST_TEMPERATURE = "test_temperature"
    PUBLICATION_SPECIFIC_INDEX = "publication_specific_index"


class PropertyValueKind(str, Enum):
    """Representational form expected for a property definition."""

    DIMENSIONAL = "dimensional"
    CATEGORICAL = "categorical"
    ORDINAL = "ordinal"
    TEXTUAL = "textual"
    INTERVAL = "interval"
    TABULAR_REFERENCE = "tabular_reference"
    SOURCE_SPECIFIC = "source_specific"


@dataclass(frozen=True, slots=True)
class PropertyDefinition:
    """Meaning, value kind, dimension, and convention for one property ID."""

    property_id: PropertyId
    display_name: str
    definition: str
    value_kind: PropertyValueKind
    expected_dimension: Dimension | None
    convention_required: bool
    source_specific_identity: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "property_id", PropertyId(self.property_id))
        object.__setattr__(self, "value_kind", PropertyValueKind(self.value_kind))
        if self.expected_dimension is not None:
            object.__setattr__(self, "expected_dimension", Dimension(self.expected_dimension))
        if not self.display_name.strip() or not self.definition.strip():
            raise ValueError("property display name and definition are required")
        source_specific = self.property_id in {
            PropertyId.SOURCE_SPECIFIC_COEFFICIENT,
            PropertyId.CLOSED_BOMB_REPORTED_VALUE,
            PropertyId.PUBLICATION_SPECIFIC_INDEX,
        }
        if source_specific and not (self.source_specific_identity or "").strip():
            raise ValueError("source-specific property requires source_specific_identity")
        if not source_specific and self.source_specific_identity is not None:
            raise ValueError("standard property cannot carry source_specific_identity")

    def to_dict(self) -> dict[str, object]:
        return {
            "property_id": self.property_id.value,
            "display_name": self.display_name,
            "definition": self.definition,
            "value_kind": self.value_kind.value,
            "expected_dimension": None if self.expected_dimension is None else self.expected_dimension.value,
            "convention_required": self.convention_required,
            "source_specific_identity": self.source_specific_identity,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> PropertyDefinition:
        fields = {"property_id", "display_name", "definition", "value_kind", "expected_dimension", "convention_required", "source_specific_identity"}
        if set(data) != fields:
            raise ValueError("malformed property definition fields")
        if not isinstance(data["convention_required"], bool):
            raise TypeError("convention_required must be boolean")
        return cls(
            PropertyId(str(data["property_id"])), str(data["display_name"]),
            str(data["definition"]), PropertyValueKind(str(data["value_kind"])),
            None if data["expected_dimension"] is None else Dimension(str(data["expected_dimension"])),
            data["convention_required"],
            None if data["source_specific_identity"] is None else str(data["source_specific_identity"]),
        )


_STANDARD_DEFINITIONS = MappingProxyType({
    PropertyId.BULK_DENSITY: PropertyDefinition(PropertyId.BULK_DENSITY, "Bulk density", "Reported bulk mass per occupied bulk volume under the source conditions", PropertyValueKind.DIMENSIONAL, Dimension.MASS_DENSITY, False),
    PropertyId.GRAVIMETRIC_DENSITY: PropertyDefinition(PropertyId.GRAVIMETRIC_DENSITY, "Gravimetric density", "Source-defined gravimetric density; not assumed equivalent to bulk density", PropertyValueKind.SOURCE_SPECIFIC, None, True),
    PropertyId.HEAT_OF_EXPLOSION: PropertyDefinition(PropertyId.HEAT_OF_EXPLOSION, "Heat of explosion", "Source-reported heat-of-explosion statement; not force, impetus, or effective energy", PropertyValueKind.SOURCE_SPECIFIC, None, True),
    PropertyId.FORCE: PropertyDefinition(PropertyId.FORCE, "Force", "Source-defined propellant force statement", PropertyValueKind.SOURCE_SPECIFIC, None, True),
    PropertyId.IMPETUS: PropertyDefinition(PropertyId.IMPETUS, "Impetus", "Source-defined impetus statement", PropertyValueKind.SOURCE_SPECIFIC, None, True),
    PropertyId.COVOLUME: PropertyDefinition(PropertyId.COVOLUME, "Covolume", "Source-defined covolume statement", PropertyValueKind.SOURCE_SPECIFIC, None, True),
    PropertyId.SPECIFIC_HEAT_RATIO: PropertyDefinition(PropertyId.SPECIFIC_HEAT_RATIO, "Specific-heat ratio", "Dimensionless ratio under a declared thermodynamic convention", PropertyValueKind.DIMENSIONAL, Dimension.RATIO, True),
    PropertyId.GRAIN_DIMENSION: PropertyDefinition(PropertyId.GRAIN_DIMENSION, "Grain dimension", "One explicitly named physical grain dimension", PropertyValueKind.DIMENSIONAL, Dimension.LENGTH, True),
    PropertyId.GRAIN_FORM: PropertyDefinition(PropertyId.GRAIN_FORM, "Grain form", "Source-reported categorical grain geometry", PropertyValueKind.CATEGORICAL, None, True),
    PropertyId.PERFORATION_COUNT: PropertyDefinition(PropertyId.PERFORATION_COUNT, "Perforation count", "Source-reported integer perforation count", PropertyValueKind.ORDINAL, None, True),
    PropertyId.VIVACITY_REPORTED: PropertyDefinition(PropertyId.VIVACITY_REPORTED, "Reported vivacity", "Vivacity exactly as defined by the named source method", PropertyValueKind.SOURCE_SPECIFIC, None, True),
    PropertyId.BURN_RATE_COEFFICIENT_REPORTED: PropertyDefinition(PropertyId.BURN_RATE_COEFFICIENT_REPORTED, "Reported burn-rate coefficient", "Coefficient exactly as defined by the named burn-law source", PropertyValueKind.SOURCE_SPECIFIC, None, True),
    PropertyId.MANUFACTURER_RELATIVE_BURN_RATE_POSITION: PropertyDefinition(PropertyId.MANUFACTURER_RELATIVE_BURN_RATE_POSITION, "Manufacturer relative-burn-rate position", "Ordinal chart position within one identified publication", PropertyValueKind.ORDINAL, None, True),
    PropertyId.COMPOSITION_CATEGORY: PropertyDefinition(PropertyId.COMPOSITION_CATEGORY, "Composition category", "Source-reported categorical composition statement", PropertyValueKind.CATEGORICAL, None, True),
    PropertyId.MOISTURE_CONTENT: PropertyDefinition(PropertyId.MOISTURE_CONTENT, "Moisture content", "Reported moisture quantity under a named convention", PropertyValueKind.DIMENSIONAL, Dimension.RATIO, True),
    PropertyId.TEST_TEMPERATURE: PropertyDefinition(PropertyId.TEST_TEMPERATURE, "Test temperature", "Temperature associated with the reported property", PropertyValueKind.DIMENSIONAL, Dimension.TEMPERATURE, False),
})


def standard_property_definition(property_id: PropertyId) -> PropertyDefinition:
    """Return a neutral built-in definition or fail for source-specific IDs."""

    try:
        return _STANDARD_DEFINITIONS[PropertyId(property_id)]
    except KeyError as error:
        raise ValueError("property requires an explicit source-specific definition") from error


def _real(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real) or not isfinite(float(value)):
        raise ValueError(f"{name} must be a finite real number")
    return float(value)


@dataclass(frozen=True, slots=True)
class DimensionalPropertyValue:
    """Reported M01 physical value retaining source units and uncertainty."""

    physical_value: PhysicalValue
    convention: str
    source_wording: str

    def __post_init__(self) -> None:
        if not self.source_wording.strip():
            raise ValueError("dimensional property source wording is required")

    def to_dict(self) -> dict[str, object]:
        return {"kind": "dimensional", "physical_value": self.physical_value.to_dict(), "convention": self.convention, "source_wording": self.source_wording}


@dataclass(frozen=True, slots=True)
class SourceScalarPropertyValue:
    """Finite source scalar whose unit/definition has no admitted conversion."""

    value: float
    reported_unit: str
    convention: str
    definition: str
    source_wording: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", _real(self.value, "source scalar"))
        for value, name in ((self.reported_unit, "reported unit"), (self.convention, "convention"), (self.definition, "definition"), (self.source_wording, "source wording")):
            if not value.strip():
                raise ValueError(f"{name} is required")

    def to_dict(self) -> dict[str, object]:
        return {"kind": "source_scalar", "value": self.value, "reported_unit": self.reported_unit, "convention": self.convention, "definition": self.definition, "source_wording": self.source_wording}


@dataclass(frozen=True, slots=True)
class CategoricalPropertyValue:
    """Literal categorical statement under an identified vocabulary."""

    value: str
    vocabulary_or_convention: str
    source_wording: str

    def __post_init__(self) -> None:
        if not self.value.strip() or not self.vocabulary_or_convention.strip() or not self.source_wording.strip():
            raise ValueError("categorical value, convention, and source wording are required")

    def to_dict(self) -> dict[str, object]:
        return {"kind": "categorical", "value": self.value, "vocabulary_or_convention": self.vocabulary_or_convention, "source_wording": self.source_wording}


@dataclass(frozen=True, slots=True)
class OrdinalPropertyValue:
    """Reported ordinal position on one named scale; not a physical ratio."""

    value: float
    scale_id: str
    direction_definition: str
    source_wording: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", _real(self.value, "ordinal value"))
        if not self.scale_id.strip() or not self.direction_definition.strip() or not self.source_wording.strip():
            raise ValueError("ordinal scale, direction, and source wording are required")

    def to_dict(self) -> dict[str, object]:
        return {"kind": "ordinal", "value": self.value, "scale_id": self.scale_id, "direction_definition": self.direction_definition, "source_wording": self.source_wording}


@dataclass(frozen=True, slots=True)
class TextualPropertyValue:
    """Literal source text that has not been normalized into another kind."""

    text: str

    def __post_init__(self) -> None:
        if not self.text.strip():
            raise ValueError("textual property value must be nonblank")

    def to_dict(self) -> dict[str, object]:
        return {"kind": "textual", "text": self.text}


@dataclass(frozen=True, slots=True)
class IntervalPropertyValue:
    """Reported dimensional interval with explicit endpoint inclusion."""

    lower: PhysicalValue
    upper: PhysicalValue
    lower_inclusive: bool
    upper_inclusive: bool
    convention: str
    source_wording: str

    def __post_init__(self) -> None:
        if not isinstance(self.lower_inclusive, bool) or not isinstance(self.upper_inclusive, bool):
            raise TypeError("property interval inclusion flags must be boolean")
        require_dimension(self.upper.quantity, self.lower.quantity.dimension, "interval upper")
        if self.lower.quantity.si_value > self.upper.quantity.si_value:
            raise ValueError("property interval bounds must be ordered")
        if not self.convention.strip() or not self.source_wording.strip():
            raise ValueError("interval convention and source wording are required")

    def to_dict(self) -> dict[str, object]:
        return {"kind": "interval", "lower": self.lower.to_dict(), "upper": self.upper.to_dict(), "lower_inclusive": self.lower_inclusive, "upper_inclusive": self.upper_inclusive, "convention": self.convention, "source_wording": self.source_wording}


@dataclass(frozen=True, slots=True)
class TabularReferencePropertyValue:
    """Reference to retained tabular evidence without interpreting its surface."""

    table_record_id: str
    source_locator: str
    description: str

    def __post_init__(self) -> None:
        if not self.table_record_id.strip() or not self.source_locator.strip() or not self.description.strip():
            raise ValueError("tabular reference identity, locator, and description are required")

    def to_dict(self) -> dict[str, object]:
        return {"kind": "tabular_reference", "table_record_id": self.table_record_id, "source_locator": self.source_locator, "description": self.description}


PropertyValue: TypeAlias = DimensionalPropertyValue | SourceScalarPropertyValue | CategoricalPropertyValue | OrdinalPropertyValue | TextualPropertyValue | IntervalPropertyValue | TabularReferencePropertyValue


def property_value_from_dict(data: Mapping[str, Any]) -> PropertyValue:
    """Parse a strict tagged property value."""

    if not isinstance(data, Mapping) or "kind" not in data:
        raise ValueError("property value requires kind")
    kind = data["kind"]
    expected: dict[str, set[str]] = {
        "dimensional": {"kind", "physical_value", "convention", "source_wording"},
        "source_scalar": {"kind", "value", "reported_unit", "convention", "definition", "source_wording"},
        "categorical": {"kind", "value", "vocabulary_or_convention", "source_wording"},
        "ordinal": {"kind", "value", "scale_id", "direction_definition", "source_wording"},
        "textual": {"kind", "text"},
        "interval": {"kind", "lower", "upper", "lower_inclusive", "upper_inclusive", "convention", "source_wording"},
        "tabular_reference": {"kind", "table_record_id", "source_locator", "description"},
    }
    if kind not in expected or set(data) != expected[kind]:
        raise ValueError("malformed property value fields")
    if kind == "dimensional":
        return DimensionalPropertyValue(PhysicalValue.from_dict(data["physical_value"]), str(data["convention"]), str(data["source_wording"]))
    if kind == "source_scalar":
        return SourceScalarPropertyValue(data["value"], str(data["reported_unit"]), str(data["convention"]), str(data["definition"]), str(data["source_wording"]))
    if kind == "categorical":
        return CategoricalPropertyValue(str(data["value"]), str(data["vocabulary_or_convention"]), str(data["source_wording"]))
    if kind == "ordinal":
        return OrdinalPropertyValue(data["value"], str(data["scale_id"]), str(data["direction_definition"]), str(data["source_wording"]))
    if kind == "textual":
        return TextualPropertyValue(str(data["text"]))
    if kind == "interval":
        for field in ("lower_inclusive", "upper_inclusive"):
            if not isinstance(data[field], bool):
                raise TypeError(f"{field} must be boolean")
        return IntervalPropertyValue(PhysicalValue.from_dict(data["lower"]), PhysicalValue.from_dict(data["upper"]), data["lower_inclusive"], data["upper_inclusive"], str(data["convention"]), str(data["source_wording"]))
    return TabularReferencePropertyValue(str(data["table_record_id"]), str(data["source_locator"]), str(data["description"]))
