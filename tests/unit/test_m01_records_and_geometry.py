from math import pi

import pytest

from modern_powley.modernized.geometry import (
    WaterConversionConvention,
    barrel_swept_volume,
    barrel_volume_ratio,
    boat_tail_seated_displacement,
    charge_to_bullet_mass_ratio,
    charge_to_estimated_usable_water_capacity_mass_ratio,
    charge_to_gross_water_capacity_mass_ratio,
    charge_to_measured_usable_water_capacity_mass_ratio,
    circle_area,
    compare_usable_powder_spaces,
    conical_frustum_volume,
    derive_seating_depth,
    estimate_geometric_usable_powder_space,
    flat_base_seated_displacement,
    sectional_density_mass_over_diameter_squared,
    total_expanded_volume,
    total_expansion_ratio,
    water_mass_to_volume,
    water_mass_to_volume_by_convention,
    water_volume_to_mass,
)
from modern_powley.modernized.provenance import EvidenceClass, ModelMaturity, Provenance, ValueOrigin
from modern_powley.modernized.records import (
    CapacityFillBoundary,
    CartridgeIdentity,
    CaseCondition,
    DiameterConvention,
    FirearmRecord,
    GeometryAdequacy,
    GrossCaseCapacity,
    MeasuredUsablePowderSpace,
    MeasurementConditions,
    PhysicalValue,
    PrimerPocketTreatment,
    PrimerPocketVolume,
    ProjectileRecord,
    ProjectileTravel,
    SeatingDepth,
    SeatingDepthKind,
)
from modern_powley.modernized.serialization import dumps_record, loads_record
from modern_powley.modernized.uncertainty import Uncertainty
from modern_powley.modernized.units import Quantity, Unit


def provenance(source_id="MEAS-M01-001"):
    return Provenance(EvidenceClass.USER_MEASUREMENT, ValueOrigin.MEASURED, source_id, ModelMaturity.RETAINED_CANDIDATE)


def pv(record_id, value, unit, source_id="MEAS-M01-001"):
    return PhysicalValue(record_id, Quantity(value, unit), provenance(source_id), Uncertainty.unknown())


def gross_conditions(treatment=PrimerPocketTreatment.INCLUDED):
    return MeasurementConditions(CaseCondition.FIRED_UNSIZED, treatment, CapacityFillBoundary.CASE_MOUTH, "water condition explicitly unknown")


def historical_usable_conditions():
    return MeasurementConditions(CaseCondition.OTHER, PrimerPocketTreatment.EXCLUDED, CapacityFillBoundary.BOTTOM_OF_FLASH_HOLE, "water condition not printed", case_condition_detail="unprimed empty case assembled with intended seated projectile")


def flat_projectile(depth_cm=1.0, adequacy=GeometryAdequacy.ADEQUATE_FOR_DECLARED_MODEL):
    seating_value = pv("PV-SEATING", depth_cm, Unit.CENTIMETRE)
    seating = SeatingDepth(seating_value, SeatingDepthKind.DIRECT, "projectile base to case-mouth plane")
    return ProjectileRecord("PROJECTILE-1", "test flat-base", pv("PV-BULLET-MASS", 180, Unit.GRAIN), pv("PV-BULLET-DIA", 0.5, Unit.CENTIMETRE), adequacy, seating_depth=seating, cylindrical_shank_diameter=pv("PV-SHANK", 0.5, Unit.CENTIMETRE))


def gross_capacity(volume_cm3=2.0, treatment=PrimerPocketTreatment.INCLUDED):
    return GrossCaseCapacity("GROSS-1", "CARTRIDGE-1", pv("PV-GROSS-MASS", 30, Unit.GRAIN), gross_conditions(treatment), pv("PV-GROSS-VOL", volume_cm3, Unit.CUBIC_CENTIMETRE), "CONV-SUPPLIED-DENSITY")


def measured_capacity(volume_cm3=1.7):
    return MeasuredUsablePowderSpace("MEASURED-1", "CARTRIDGE-1", "PROJECTILE-1", "intended projectile seated to recorded depth", "PROC-POWLEY-SEATED-FLASH-HOLE", pv("PV-MEASURED-MASS", 25, Unit.GRAIN), historical_usable_conditions(), pv("PV-MEASURED-VOL", volume_cm3, Unit.CUBIC_CENTIMETRE), "CONV-SUPPLIED-DENSITY")


def test_controlled_other_requires_detail_and_historical_fixture_is_representable():
    with pytest.raises(ValueError, match="detail"):
        MeasurementConditions(CaseCondition.OTHER, PrimerPocketTreatment.EXCLUDED, CapacityFillBoundary.BOTTOM_OF_FLASH_HOLE, "unknown")
    record = measured_capacity()
    assert record.conditions.primer_pocket_treatment is PrimerPocketTreatment.EXCLUDED
    assert record.conditions.fill_boundary is CapacityFillBoundary.BOTTOM_OF_FLASH_HOLE
    assert "unprimed empty case" in record.conditions.case_condition_detail


def test_circle_cylinder_frustum_and_sectional_density_invariants():
    diameter = pv("D", 10, Unit.MILLIMETRE)
    length = pv("L", 20, Unit.MILLIMETRE)
    area = circle_area(diameter, DiameterConvention.PROJECTILE, result_id="AREA")
    cylinder = flat_base_seated_displacement(diameter, length, result_id="CYL")
    frustum = conical_frustum_volume(length, diameter, diameter, result_id="FRUSTUM")
    assert area.quantity.si_value == pytest.approx(pi * 0.005**2)
    assert cylinder.quantity.si_value == pytest.approx(area.quantity.si_value * 0.02)
    assert frustum.quantity.si_value == pytest.approx(cylinder.quantity.si_value)
    sd = sectional_density_mass_over_diameter_squared(pv("M", 10, Unit.GRAM), diameter, result_id="SD")
    assert sd.quantity.unit is Unit.KILOGRAM_PER_SQUARE_METRE
    assert sd.quantity.si_value == pytest.approx(100.0)


def test_partial_full_and_extended_boat_tail_displacement():
    shank = pv("D", 10, Unit.MILLIMETRE)
    base = pv("d", 6, Unit.MILLIMETRE)
    height = pv("H", 8, Unit.MILLIMETRE)
    partial = boat_tail_seated_displacement(shank, base, height, pv("I1", 4, Unit.MILLIMETRE), result_id="PARTIAL")
    expected_top = 0.006 + (0.010 - 0.006) * 0.5
    expected_partial = pi * 0.004 * (0.006**2 + 0.006 * expected_top + expected_top**2) / 12
    assert partial.quantity.si_value == pytest.approx(expected_partial)
    full = boat_tail_seated_displacement(shank, base, height, pv("I2", 8, Unit.MILLIMETRE), result_id="FULL")
    extended = boat_tail_seated_displacement(shank, base, height, pv("I3", 12, Unit.MILLIMETRE), result_id="EXTENDED")
    assert extended.quantity.si_value == pytest.approx(full.quantity.si_value + pi * 0.005**2 * 0.004)
    cylinder = boat_tail_seated_displacement(shank, shank, height, pv("I4", 12, Unit.MILLIMETRE), result_id="EQUAL")
    assert cylinder.quantity.si_value == pytest.approx(pi * 0.005**2 * 0.012)


def test_invalid_geometry_and_outside_model_are_rejected():
    with pytest.raises(ValueError):
        flat_base_seated_displacement(pv("D", 10, Unit.MILLIMETRE), pv("I", 0, Unit.MILLIMETRE), result_id="BAD")
    with pytest.raises(ValueError, match="cannot exceed"):
        boat_tail_seated_displacement(pv("D", 10, Unit.MILLIMETRE), pv("d", 11, Unit.MILLIMETRE), pv("H", 2, Unit.MILLIMETRE), pv("I", 1, Unit.MILLIMETRE), result_id="BAD")
    with pytest.raises(ValueError, match="outside"):
        estimate_geometric_usable_powder_space(gross_capacity(), flat_projectile(adequacy=GeometryAdequacy.OUTSIDE_MODEL), PrimerPocketTreatment.INCLUDED, result_id="EST", assumptions=("test",))


def test_geometric_estimate_requires_explicit_primer_basis_and_correction():
    gross = gross_capacity()
    projectile = flat_projectile()
    with pytest.raises(ValueError, match="primer-pocket volume"):
        estimate_geometric_usable_powder_space(gross, projectile, PrimerPocketTreatment.EXCLUDED, result_id="EST", assumptions=("cylindrical shank",))
    pocket = PrimerPocketVolume("POCKET-1", "CARTRIDGE-1", pv("PV-POCKET", 0.1, Unit.CUBIC_CENTIMETRE), PrimerPocketTreatment.INCLUDED)
    estimate = estimate_geometric_usable_powder_space(gross, projectile, PrimerPocketTreatment.EXCLUDED, result_id="EST", primer_pocket_volume=pocket, assumptions=("cylindrical shank",))
    displacement = pi * (0.005 / 2) ** 2 * 0.01
    assert estimate.usable_volume.quantity.si_value == pytest.approx(2e-6 - 0.1e-6 - displacement)
    assert estimate.primer_pocket_correction_record_id == "POCKET-1"
    assert estimate.gross_capacity_record_id == gross.record_id


def test_unknown_primer_basis_negative_volume_and_missing_conversion_fail():
    unknown = gross_capacity(treatment=PrimerPocketTreatment.UNKNOWN)
    with pytest.raises(ValueError, match="must be known"):
        estimate_geometric_usable_powder_space(unknown, flat_projectile(), PrimerPocketTreatment.EXCLUDED, result_id="EST", assumptions=("test",))
    mass_only = GrossCaseCapacity("GROSS-MASS", "CARTRIDGE-1", pv("MASS", 2, Unit.GRAIN), gross_conditions())
    with pytest.raises(ValueError, match="explicit water mass-to-volume"):
        estimate_geometric_usable_powder_space(mass_only, flat_projectile(), PrimerPocketTreatment.INCLUDED, result_id="EST", assumptions=("test",))
    with pytest.raises(ValueError, match="greater than zero"):
        estimate_geometric_usable_powder_space(gross_capacity(0.01), flat_projectile(1.0), PrimerPocketTreatment.INCLUDED, result_id="EST", assumptions=("test",))


def test_measured_and_estimated_capacities_coexist_without_averaging():
    estimated = estimate_geometric_usable_powder_space(gross_capacity(), flat_projectile(), PrimerPocketTreatment.INCLUDED, result_id="EST", assumptions=("cylindrical shank",))
    measured = measured_capacity()
    comparison = compare_usable_powder_spaces(measured, estimated, result_id="COMPARE")
    assert comparison.measured_record_id == measured.record_id
    assert comparison.estimated_record_id == estimated.record_id
    assert not hasattr(comparison, "effective_capacity")
    assert loads_record(dumps_record(estimated)) == estimated
    assert loads_record(dumps_record(measured)) == measured


def test_every_top_level_m01_record_round_trips_strict_json():
    gross = gross_capacity()
    projectile = flat_projectile()
    measured = measured_capacity()
    pocket = PrimerPocketVolume("POCKET-1", "CARTRIDGE-1", pv("PV-POCKET", 0.1, Unit.CUBIC_CENTIMETRE), PrimerPocketTreatment.INCLUDED)
    estimated = estimate_geometric_usable_powder_space(gross, projectile, PrimerPocketTreatment.INCLUDED, result_id="EST", assumptions=("cylindrical shank",))
    firearm = FirearmRecord("FIREARM-1", "test barrel", pv("BARREL", 24, Unit.INCH), "bolt face to muzzle")
    records = (
        CartridgeIdentity("CARTRIDGE-1", "test cartridge", provenance(), case_length=pv("CASE-LENGTH", 2, Unit.INCH)),
        gross,
        measured,
        pocket,
        projectile,
        estimated,
        firearm,
        compare_usable_powder_spaces(measured, estimated, result_id="COMPARE"),
    )
    for record in records:
        assert loads_record(dumps_record(record)) == record


def test_water_conversion_requires_supplied_density_or_named_convention():
    water_mass = pv("WATER-MASS", 1, Unit.GRAM)
    density = pv("WATER-DENSITY", 1, Unit.GRAM_PER_CUBIC_CENTIMETRE)
    volume = water_mass_to_volume(water_mass, density, result_id="WATER-VOLUME")
    assert volume.quantity.to(Unit.CUBIC_CENTIMETRE).value == pytest.approx(1)
    assert water_volume_to_mass(volume, density, result_id="WATER-MASS-2").quantity.to(Unit.GRAM).value == pytest.approx(1)
    powley = water_mass_to_volume_by_convention(pv("POWLEY-WATER", 253, Unit.GRAIN), WaterConversionConvention.POWLEY_253_GRAIN_PER_CUBIC_INCH, result_id="POWLEY-VOLUME")
    assert powley.quantity.to(Unit.CUBIC_INCH).value == pytest.approx(1)


def test_explicit_ratios_and_barrel_geometry_have_no_ambiguous_names():
    charge = pv("CHARGE", 10, Unit.GRAIN)
    projectile = flat_projectile()
    gross = gross_capacity()
    measured = measured_capacity()
    estimated = estimate_geometric_usable_powder_space(gross, projectile, PrimerPocketTreatment.INCLUDED, result_id="EST", assumptions=("test",))
    equivalent = water_volume_to_mass(estimated.usable_volume, pv("DENSITY", 1, Unit.GRAM_PER_CUBIC_CENTIMETRE), result_id="EST-MASS")
    estimated = type(estimated)(estimated.record_id, estimated.cartridge_id, estimated.gross_capacity_record_id, estimated.projectile_geometry_record_id, estimated.usable_volume, estimated.displacement_method_id, estimated.primer_pocket_treatment, estimated.geometry_adequacy, estimated.assumptions, estimated.input_record_ids, estimated.primer_pocket_correction_record_id, equivalent)
    assert charge_to_bullet_mass_ratio(charge, projectile.mass, result_id="CB").quantity.si_value == pytest.approx(10 / 180)
    assert charge_to_gross_water_capacity_mass_ratio(charge, gross, result_id="CG").quantity.si_value == pytest.approx(10 / 30)
    assert charge_to_measured_usable_water_capacity_mass_ratio(charge, measured, result_id="CM").quantity.si_value == pytest.approx(10 / 25)
    assert charge_to_estimated_usable_water_capacity_mass_ratio(charge, estimated, result_id="CE").quantity.si_value > 0
    swept = barrel_swept_volume(pv("BORE", 10, Unit.MILLIMETRE), pv("TRAVEL", 500, Unit.MILLIMETRE), DiameterConvention.BORE, result_id="SWEPT")
    usable = measured.water_volume
    assert usable is not None
    assert barrel_volume_ratio(swept, usable, result_id="BVR").quantity.si_value == pytest.approx(swept.quantity.si_value / usable.quantity.si_value)
    assert total_expansion_ratio(swept, usable, result_id="TER").quantity.si_value == pytest.approx(1 + swept.quantity.si_value / usable.quantity.si_value)
    assert total_expanded_volume(usable, swept, result_id="TOTAL").quantity.si_value == pytest.approx(usable.quantity.si_value + swept.quantity.si_value)


def test_direct_and_derived_seating_depth_and_firearm_diameters_remain_distinct():
    derived = derive_seating_depth(pv("CASE-L", 2.0, Unit.INCH), pv("BULLET-L", 1.0, Unit.INCH), pv("COAL", 2.8, Unit.INCH), reference_conventions=("case head axial datum",) * 3, result_id="SEATING-DERIVED")
    assert derived.kind is SeatingDepthKind.DERIVED
    assert derived.value.quantity.to(Unit.INCH).value == pytest.approx(0.2)
    with pytest.raises(ValueError, match="must match"):
        derive_seating_depth(pv("C", 2, Unit.INCH), pv("B", 1, Unit.INCH), pv("O", 2.8, Unit.INCH), reference_conventions=("a", "b", "a"), result_id="BAD")
    firearm = FirearmRecord("FIREARM-1", "test barrel", pv("BARREL", 24, Unit.INCH), "bolt face to muzzle", pv("BORE", 0.300, Unit.INCH), pv("GROOVE", 0.308, Unit.INCH), projectile_travel=ProjectileTravel(pv("TRAVEL", 22.4, Unit.INCH), "seated bullet base", "muzzle"), pressure_standard_identity="SAAMI example metadata", pressure_standard_edition="2026 example")
    assert firearm.diameter_for(DiameterConvention.BORE).record_id == "BORE"
    assert firearm.diameter_for(DiameterConvention.GROOVE).record_id == "GROOVE"
    with pytest.raises(ValueError, match="projectile diameter"):
        firearm.diameter_for(DiameterConvention.PROJECTILE)
    assert not hasattr(firearm, "pressure")


def test_case_length_and_freebore_are_explicit_optional_metadata():
    cartridge = CartridgeIdentity(
        "CARTRIDGE-1", "test cartridge", provenance(),
        case_length=pv("CASE-LENGTH", 2.0, Unit.INCH),
    )
    assert cartridge.case_length.quantity.to(Unit.INCH).value == pytest.approx(2.0)
    firearm = FirearmRecord(
        "FIREARM-FREEBORE", "test barrel", pv("BARREL", 24, Unit.INCH),
        "bolt face to muzzle", freebore_length=pv("FREEBORE", 0.1, Unit.INCH),
        freebore_reference="case mouth datum to rifling origin",
    )
    assert loads_record(dumps_record(firearm)) == firearm
    with pytest.raises(ValueError, match="reference"):
        FirearmRecord(
            "FIREARM-BAD", "test barrel", pv("BARREL-2", 24, Unit.INCH),
            "bolt face to muzzle", freebore_reference="unsourced text only",
        )
