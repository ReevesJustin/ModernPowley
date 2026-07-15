import pytest

from modern_powley.modernized.adapters.original import (
    original_barrel_volume,
    original_barrel_volume_ratio,
    original_charge_arithmetic,
    original_effective_bore_diameter,
    original_mass_ratio,
    original_projectile_travel,
    original_sectional_density,
    original_total_expansion_ratio,
)
from modern_powley.modernized.provenance import EvidenceClass, ModelMaturity, Provenance, ValueOrigin
from modern_powley.modernized.records import (
    CapacityFillBoundary,
    CaseCondition,
    EstimatedUsablePowderSpace,
    FirearmRecord,
    GeometryAdequacy,
    MeasuredUsablePowderSpace,
    MeasurementConditions,
    PhysicalValue,
    PrimerPocketTreatment,
    ProjectileRecord,
)
from modern_powley.modernized.uncertainty import Uncertainty
from modern_powley.modernized.units import Quantity, Unit
from modern_powley.original.charge import charge_from_measured_powder_space
from modern_powley.original.geometry import sectional_density


def provenance():
    return Provenance(EvidenceClass.USER_MEASUREMENT, ValueOrigin.MEASURED, "MEAS-ADAPTER-001", ModelMaturity.RETAINED_CANDIDATE)


def pv(record_id, value, unit):
    return PhysicalValue(record_id, Quantity(value, unit), provenance(), Uncertainty.unknown())


def projectile():
    return ProjectileRecord("PROJECTILE-180", "180 grain .308 test projectile", pv("MASS-180", 180, Unit.GRAIN), pv("DIAMETER-308", 0.308, Unit.INCH), GeometryAdequacy.UNKNOWN)


def measured_capacity():
    conditions = MeasurementConditions(CaseCondition.OTHER, PrimerPocketTreatment.EXCLUDED, CapacityFillBoundary.BOTTOM_OF_FLASH_HOLE, "manual condition not printed", case_condition_detail="unprimed empty case with intended projectile seated")
    return MeasuredUsablePowderSpace("MEASURED-51.5", "CARTRIDGE-308", "PROJECTILE-150", "intended seating", "PROC-POWLEY-SEATED-FLASH-HOLE", pv("WATER-51.5", 51.5, Unit.GRAIN), conditions)


def test_m01_adapter_reproduces_original_scalar_outputs_without_behavior_changes():
    bullet = projectile()
    sd = original_sectional_density(bullet)
    assert sd.value == pytest.approx(sectional_density(180, 0.308))
    ratio = original_mass_ratio(pv("CHARGE-44.3", 44.3, Unit.GRAIN), ProjectileRecord("PROJECTILE-150", "150 grain .30", pv("MASS-150", 150, Unit.GRAIN), pv("DIA-30", 0.308, Unit.INCH), GeometryAdequacy.UNKNOWN))
    assert ratio.value == pytest.approx(44.3 / 150)
    assert original_charge_arithmetic(measured_capacity(), "IMR 4064").value == pytest.approx(charge_from_measured_powder_space(51.5, "IMR 4064"))


def test_historical_effective_diameter_travel_volume_and_ratios_chain_explicitly():
    firearm = FirearmRecord("FIREARM-308", "24 inch reference barrel", pv("BARREL-24", 24, Unit.INCH), "bolt face to muzzle", pv("BORE-300", 0.300, Unit.INCH), pv("GROOVE-308", 0.308, Unit.INCH))
    effective = original_effective_bore_diameter(firearm)
    travel = original_projectile_travel(pv("MUZZLE-TIP", 21 + 5 / 16, Unit.INCH), pv("BULLET-LENGTH", 1 + 1 / 16, Unit.INCH))
    barrel = original_barrel_volume(effective, travel)
    bvr = original_barrel_volume_ratio(barrel, measured_capacity())
    ter = original_total_expansion_ratio(barrel, measured_capacity())
    assert effective.value == pytest.approx(0.304)
    assert travel.value == pytest.approx(22.375)
    assert ter.value == pytest.approx(1 + bvr.value)
    assert ter.value == pytest.approx(9.0, abs=0.05)
    assert "253" in barrel.unit_or_convention


def test_historical_capacity_adapter_refuses_estimated_capacity():
    estimated = object.__new__(EstimatedUsablePowderSpace)
    with pytest.raises(TypeError, match="measured seating-specific"):
        original_charge_arithmetic(estimated, "IMR 4064")
