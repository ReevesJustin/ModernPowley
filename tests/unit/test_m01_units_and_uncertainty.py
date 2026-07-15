import math

import pytest

from modern_powley.modernized.provenance import EvidenceClass, ModelMaturity, Provenance, ValueOrigin
from modern_powley.modernized.records import PhysicalValue, UncertaintyTreatment
from modern_powley.modernized.uncertainty import Uncertainty, UncertaintyKind
from modern_powley.modernized.units import (
    Dimension,
    GRAIN_TO_KILOGRAM_EXACT,
    INCH_TO_METRE_EXACT,
    POUND_TO_KILOGRAM_EXACT,
    Quantity,
    Unit,
)


def supplied_provenance() -> Provenance:
    return Provenance(EvidenceClass.USER_MEASUREMENT, ValueOrigin.MEASURED, "MEAS-UNIT-001", ModelMaturity.RETAINED_CANDIDATE)


def test_exact_customary_conversions_and_source_value_preservation():
    inch = Quantity(1.0, Unit.INCH)
    pound = Quantity(1.0, Unit.POUND)
    grain = Quantity(1.0, Unit.GRAIN)
    assert inch.value == 1.0 and inch.unit is Unit.INCH
    assert inch.si_value == INCH_TO_METRE_EXACT
    assert pound.si_value == POUND_TO_KILOGRAM_EXACT
    assert grain.si_value == GRAIN_TO_KILOGRAM_EXACT
    assert Quantity(1, Unit.SQUARE_INCH).si_value == INCH_TO_METRE_EXACT**2
    assert Quantity(1, Unit.CUBIC_INCH).si_value == INCH_TO_METRE_EXACT**3
    assert grain.to(Unit.GRAIN).value == pytest.approx(1.0)


@pytest.mark.parametrize(
    ("quantity", "target"),
    [
        (Quantity(12.3, Unit.CENTIMETRE), Unit.INCH),
        (Quantity(45.6, Unit.CUBIC_CENTIMETRE), Unit.CUBIC_INCH),
        (Quantity(180, Unit.GRAIN), Unit.GRAM),
        (Quantity(1.2, Unit.GRAM_PER_CUBIC_CENTIMETRE), Unit.KILOGRAM_PER_CUBIC_METRE),
    ],
)
def test_supported_conversions_round_trip(quantity, target):
    assert quantity.to(target).to(quantity.unit).value == pytest.approx(quantity.value, rel=1e-15)


def test_temperature_conversion_and_dimension_rejection():
    assert Quantity(0, Unit.DEGREE_CELSIUS).si_value == pytest.approx(273.15)
    assert Quantity(273.15, Unit.KELVIN).to(Unit.DEGREE_CELSIUS).value == pytest.approx(0)
    with pytest.raises(ValueError, match="cannot convert"):
        Quantity(1, Unit.INCH).to(Unit.GRAM)


@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf])
def test_nonfinite_quantities_are_rejected(value):
    with pytest.raises(ValueError, match="finite"):
        Quantity(value, Unit.METRE)


def test_uncertainty_kinds_validate_and_round_trip():
    resolution = Uncertainty(UncertaintyKind.INSTRUMENT_RESOLUTION, magnitude=Quantity(0.01, Unit.MILLIMETRE))
    symmetric = Uncertainty(UncertaintyKind.SYMMETRIC_ABSOLUTE, magnitude=Quantity(0.1, Unit.GRAIN))
    bounded = Uncertainty(UncertaintyKind.BOUNDED_INTERVAL, lower=Quantity(9.9, Unit.MILLIMETRE), upper=Quantity(10.1, Unit.MILLIMETRE))
    assert Uncertainty.from_dict(resolution.to_dict()) == resolution
    assert Uncertainty.from_dict(symmetric.to_dict()) == symmetric
    assert Uncertainty.from_dict(bounded.to_dict()) == bounded
    assert Uncertainty.unknown().kind is UncertaintyKind.UNKNOWN


def test_uncertainty_is_explicit_and_dimensionally_compatible():
    physical = PhysicalValue("PV-LENGTH", Quantity(1, Unit.INCH), supplied_provenance(), Uncertainty.unknown())
    assert physical.uncertainty.kind is UncertaintyKind.UNKNOWN
    assert physical.uncertainty_treatment is UncertaintyTreatment.SUPPLIED
    with pytest.raises(ValueError, match="dimension"):
        PhysicalValue("PV-BAD", Quantity(1, Unit.INCH), supplied_provenance(), Uncertainty(UncertaintyKind.SYMMETRIC_ABSOLUTE, magnitude=Quantity(1, Unit.GRAIN)))


def test_invalid_uncertainty_bounds_and_unjustified_zero_are_rejected():
    with pytest.raises(ValueError, match="ordered"):
        Uncertainty(UncertaintyKind.BOUNDED_INTERVAL, lower=Quantity(2, Unit.MILLIMETRE), upper=Quantity(1, Unit.MILLIMETRE))
    with pytest.raises(ValueError, match="justification"):
        Uncertainty(UncertaintyKind.INSTRUMENT_RESOLUTION, magnitude=Quantity(0, Unit.MILLIMETRE))
    explicit_zero = Uncertainty(UncertaintyKind.INSTRUMENT_RESOLUTION, magnitude=Quantity(0, Unit.MILLIMETRE), justification="exact digital source value")
    assert explicit_zero.magnitude.si_value == 0


def test_quantity_serialization_is_strict():
    assert Quantity.from_dict({"value": 1.0, "unit": "in"}) == Quantity(1.0, Unit.INCH)
    with pytest.raises(ValueError):
        Quantity.from_dict({"value": 1.0, "unit": "in", "ignored": 2})
    with pytest.raises(ValueError):
        Quantity.from_dict({"value": 1.0, "unit": "fps"})
    with pytest.raises(TypeError, match="real"):
        Quantity.from_dict({"value": "1.0", "unit": "in"})
    with pytest.raises(TypeError, match="real"):
        Quantity.from_dict({"value": True, "unit": "in"})
