"""Explicit one-way adapters to verified original-Powley scalar functions."""

from __future__ import annotations

from dataclasses import dataclass

from modern_powley.original.charge import charge_from_measured_powder_space
from modern_powley.original.geometry import (
    barrel_volume_ratio,
    barrel_volume_water_grains,
    effective_bore_diameter_inches,
    mass_ratio,
    projectile_travel_inches,
    sectional_density,
    total_expansion_ratio,
)

from ..records import FirearmRecord, MeasuredUsablePowderSpace, PhysicalValue, ProjectileRecord
from ..units import Dimension, Unit, require_positive


@dataclass(frozen=True, slots=True)
class HistoricalScalarResult:
    """Historical scalar plus convention and modern source-record identities."""
    value: float
    unit_or_convention: str
    historical_method_id: str
    source_record_ids: tuple[str, ...]


def original_sectional_density(projectile: ProjectileRecord) -> HistoricalScalarResult:
    """Invoke original Powley sectional density with explicit unit conversion."""
    value = sectional_density(projectile.mass.quantity.to(Unit.GRAIN).value, projectile.diameter.quantity.to(Unit.INCH).value)
    return HistoricalScalarResult(value, "historical lb/in2 sectional-density convention", "EQ-001", (projectile.mass.record_id, projectile.diameter.record_id))


def original_mass_ratio(charge_mass: PhysicalValue, projectile: ProjectileRecord) -> HistoricalScalarResult:
    """Invoke original Powley charge-to-bullet mass ratio."""
    require_positive(charge_mass.quantity, Dimension.MASS, "charge mass")
    value = mass_ratio(charge_mass.quantity.to(Unit.GRAIN).value, projectile.mass.quantity.to(Unit.GRAIN).value)
    return HistoricalScalarResult(value, "dimensionless charge/bullet mass ratio", "EQ-002", (charge_mass.record_id, projectile.mass.record_id))


def original_effective_bore_diameter(firearm: FirearmRecord) -> HistoricalScalarResult:
    """Invoke the explicit historical bore/groove arithmetic mean."""
    if firearm.bore_diameter is None or firearm.groove_diameter is None:
        raise ValueError("historical effective diameter requires explicit bore and groove diameters")
    value = effective_bore_diameter_inches(firearm.bore_diameter.quantity.to(Unit.INCH).value, firearm.groove_diameter.quantity.to(Unit.INCH).value)
    return HistoricalScalarResult(value, "inch; original Powley bore/groove arithmetic mean", "EQ-044", (firearm.bore_diameter.record_id, firearm.groove_diameter.record_id))


def original_projectile_travel(distance_muzzle_to_bullet_tip: PhysicalValue, bullet_length: PhysicalValue) -> HistoricalScalarResult:
    """Invoke historical cleaning-rod projectile-travel arithmetic."""
    for value, name in ((distance_muzzle_to_bullet_tip, "muzzle-to-tip distance"), (bullet_length, "bullet length")):
        require_positive(value.quantity, Dimension.LENGTH, name)
    result = projectile_travel_inches(distance_muzzle_to_bullet_tip.quantity.to(Unit.INCH).value, bullet_length.quantity.to(Unit.INCH).value)
    return HistoricalScalarResult(result, "inch; original cleaning-rod reference points", "EQ-008", (distance_muzzle_to_bullet_tip.record_id, bullet_length.record_id))


def _historical_inches(value: PhysicalValue | HistoricalScalarResult, name: str) -> tuple[float, tuple[str, ...]]:
    if isinstance(value, PhysicalValue):
        require_positive(value.quantity, Dimension.LENGTH, name)
        return value.quantity.to(Unit.INCH).value, (value.record_id,)
    if isinstance(value, HistoricalScalarResult) and value.unit_or_convention.startswith("inch"):
        return value.value, value.source_record_ids
    raise TypeError(f"{name} must be a length record or historical inch result")


def original_barrel_volume(effective_diameter: PhysicalValue | HistoricalScalarResult, projectile_travel: PhysicalValue | HistoricalScalarResult) -> HistoricalScalarResult:
    """Invoke historical barrel-volume arithmetic and its 253 convention."""
    diameter_inches, diameter_ids = _historical_inches(effective_diameter, "effective diameter")
    travel_inches, travel_ids = _historical_inches(projectile_travel, "projectile travel")
    result = barrel_volume_water_grains(diameter_inches, travel_inches)
    return HistoricalScalarResult(result, "grain H2O using explicit Powley 253 gr/in3 convention", "EQ-009", diameter_ids + travel_ids)


def _measured_water_grains(capacity: MeasuredUsablePowderSpace) -> float:
    if not isinstance(capacity, MeasuredUsablePowderSpace):
        raise TypeError("historical capacity adapter requires measured seating-specific powder space")
    return capacity.water_mass.quantity.to(Unit.GRAIN).value


def original_barrel_volume_ratio(barrel_volume_water_grains_value: HistoricalScalarResult, measured_capacity: MeasuredUsablePowderSpace) -> HistoricalScalarResult:
    """Invoke historical Vb/V0 using measured seating-specific capacity."""
    result = barrel_volume_ratio(barrel_volume_water_grains_value.value, _measured_water_grains(measured_capacity))
    return HistoricalScalarResult(result, "dimensionless Vb/V0", "EQ-010", barrel_volume_water_grains_value.source_record_ids + (measured_capacity.record_id,))


def original_total_expansion_ratio(barrel_volume_water_grains_value: HistoricalScalarResult, measured_capacity: MeasuredUsablePowderSpace) -> HistoricalScalarResult:
    """Invoke historical (V0+Vb)/V0 using measured capacity."""
    result = total_expansion_ratio(barrel_volume_water_grains_value.value, _measured_water_grains(measured_capacity))
    return HistoricalScalarResult(result, "dimensionless (V0+Vb)/V0", "EQ-011", barrel_volume_water_grains_value.source_record_ids + (measured_capacity.record_id,))


def original_charge_arithmetic(measured_capacity: MeasuredUsablePowderSpace, powder_name: str) -> HistoricalScalarResult:
    """Invoke only the verified historical charge arithmetic."""
    result = charge_from_measured_powder_space(_measured_water_grains(measured_capacity), powder_name)
    return HistoricalScalarResult(result, "grain propellant; source-specific historical arithmetic only", "EQ-003/EQ-004", (measured_capacity.record_id,))
