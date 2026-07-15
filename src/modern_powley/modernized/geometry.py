"""Transparent Euclidean geometry and explicit M01 ratios."""

from __future__ import annotations

from enum import Enum
from math import pi

from .provenance import derived_provenance
from .records import (
    CapacityComparison,
    CapacityFillBoundary,
    DiameterConvention,
    EstimatedUsablePowderSpace,
    GeometryAdequacy,
    GrossCaseCapacity,
    MeasuredUsablePowderSpace,
    PhysicalValue,
    PrimerPocketTreatment,
    PrimerPocketVolume,
    ProjectileRecord,
    SeatingDepth,
    SeatingDepthKind,
    UncertaintyTreatment,
)
from .uncertainty import Uncertainty
from .units import Dimension, Quantity, Unit, require_dimension, require_positive

METHOD_CIRCLE_AREA = "M01-GEO-CIRCLE-AREA"
METHOD_CYLINDER_VOLUME = "M01-GEO-CYLINDER-VOLUME"
METHOD_FRUSTUM_VOLUME = "M01-GEO-FRUSTUM-VOLUME"
METHOD_FLAT_BASE_DISPLACEMENT = "M01-GEO-FLAT-BASE-DISPLACEMENT"
METHOD_BOAT_TAIL_DISPLACEMENT = "M01-GEO-BOAT-TAIL-DISPLACEMENT"
METHOD_BARREL_SWEPT_VOLUME = "M01-GEO-BARREL-SWEPT-VOLUME"
METHOD_TOTAL_EXPANDED_VOLUME = "M01-GEO-TOTAL-EXPANDED-VOLUME"
METHOD_BARREL_VOLUME_RATIO = "M01-GEO-BARREL-VOLUME-RATIO"
METHOD_TOTAL_EXPANSION_RATIO = "M01-GEO-TOTAL-EXPANSION-RATIO"
METHOD_SECTIONAL_DENSITY = "M01-GEO-SECTIONAL-DENSITY-MASS-DIAMETER2"
METHOD_CHARGE_BULLET_RATIO = "M01-RATIO-CHARGE-BULLET"
METHOD_CHARGE_GROSS_WATER_RATIO = "M01-RATIO-CHARGE-GROSS-WATER"
METHOD_CHARGE_MEASURED_WATER_RATIO = "M01-RATIO-CHARGE-MEASURED-WATER"
METHOD_CHARGE_ESTIMATED_WATER_RATIO = "M01-RATIO-CHARGE-ESTIMATED-WATER"
METHOD_SEATING_DEPTH = "M01-GEO-SEATING-DEPTH-CASE-BULLET-COAL"
METHOD_USABLE_SPACE_ESTIMATE = "M01-GEO-USABLE-SPACE-ESTIMATE"
METHOD_CAPACITY_COMPARISON = "M01-GEO-CAPACITY-COMPARISON"
METHOD_WATER_SUPPLIED_DENSITY = "M01-CONV-WATER-SUPPLIED-DENSITY"
METHOD_WATER_POWLEY_253 = "M01-CONV-WATER-POWLEY-253"


class WaterConversionConvention(str, Enum):
    """Named source-specific water mass/volume conventions."""
    POWLEY_253_GRAIN_PER_CUBIC_INCH = "powley_253_grain_per_cubic_inch"


def _derived(record_id: str, quantity: Quantity, method_id: str, inputs: tuple[str, ...], notes: str = "") -> PhysicalValue:
    return PhysicalValue(
        record_id=record_id,
        quantity=quantity,
        provenance=derived_provenance(method_id, inputs),
        uncertainty=Uncertainty.unknown(),
        uncertainty_treatment=UncertaintyTreatment.UNRESOLVED,
        notes=notes,
    )


def circle_area(diameter: PhysicalValue, convention: DiameterConvention, *, result_id: str) -> PhysicalValue:
    """Return circle area for a diameter whose convention is explicit."""
    require_positive(diameter.quantity, Dimension.LENGTH, "diameter")
    convention = DiameterConvention(convention)
    area = pi * (diameter.quantity.si_value / 2.0) ** 2
    return _derived(result_id, Quantity(area, Unit.SQUARE_METRE), METHOD_CIRCLE_AREA, (diameter.record_id,), f"diameter_convention={convention.value}")


def cylinder_volume(diameter: PhysicalValue, length: PhysicalValue, *, result_id: str) -> PhysicalValue:
    """Return the Euclidean volume of a right circular cylinder."""
    require_positive(diameter.quantity, Dimension.LENGTH, "diameter")
    require_positive(length.quantity, Dimension.LENGTH, "length")
    volume = pi * (diameter.quantity.si_value / 2.0) ** 2 * length.quantity.si_value
    return _derived(result_id, Quantity(volume, Unit.CUBIC_METRE), METHOD_CYLINDER_VOLUME, (diameter.record_id, length.record_id))


def conical_frustum_volume(height: PhysicalValue, large_diameter: PhysicalValue, small_diameter: PhysicalValue, *, result_id: str) -> PhysicalValue:
    """Return a conical-frustum volume for ordered positive diameters."""
    require_positive(height.quantity, Dimension.LENGTH, "frustum height")
    require_positive(large_diameter.quantity, Dimension.LENGTH, "large diameter")
    require_positive(small_diameter.quantity, Dimension.LENGTH, "small diameter")
    large = large_diameter.quantity.si_value
    small = small_diameter.quantity.si_value
    if small > large:
        raise ValueError("small frustum diameter cannot exceed large diameter")
    volume = pi * height.quantity.si_value * (large**2 + large * small + small**2) / 12.0
    return _derived(result_id, Quantity(volume, Unit.CUBIC_METRE), METHOD_FRUSTUM_VOLUME, (height.record_id, large_diameter.record_id, small_diameter.record_id))


def flat_base_seated_displacement(shank_diameter: PhysicalValue, intrusion: PhysicalValue, *, result_id: str) -> PhysicalValue:
    """Return cylindrical displacement for a flat-base seated projectile."""
    value = cylinder_volume(shank_diameter, intrusion, result_id=result_id)
    return PhysicalValue(value.record_id, value.quantity, derived_provenance(METHOD_FLAT_BASE_DISPLACEMENT, (shank_diameter.record_id, intrusion.record_id)), value.uncertainty, value.uncertainty_treatment, "flat-base cylindrical model")


def boat_tail_seated_displacement(shank_diameter: PhysicalValue, base_diameter: PhysicalValue, tail_length: PhysicalValue, intrusion: PhysicalValue, *, result_id: str) -> PhysicalValue:
    """Return displacement for partial/full linear boat-tail intrusion."""
    for value, name in ((shank_diameter, "shank diameter"), (base_diameter, "boat-tail base diameter"), (tail_length, "boat-tail length"), (intrusion, "seated intrusion")):
        require_positive(value.quantity, Dimension.LENGTH, name)
    shank = shank_diameter.quantity.si_value
    base = base_diameter.quantity.si_value
    height = tail_length.quantity.si_value
    seated = intrusion.quantity.si_value
    if base > shank:
        raise ValueError("boat-tail base diameter cannot exceed shank diameter")
    if seated <= height:
        top = base + (shank - base) * seated / height
        volume = pi * seated * (base**2 + base * top + top**2) / 12.0
        domain = "partial boat-tail frustum"
    else:
        tail_volume = pi * height * (shank**2 + shank * base + base**2) / 12.0
        shank_volume = pi * (shank / 2.0) ** 2 * (seated - height)
        volume = tail_volume + shank_volume
        domain = "full boat-tail frustum plus cylindrical shank"
    return _derived(result_id, Quantity(volume, Unit.CUBIC_METRE), METHOD_BOAT_TAIL_DISPLACEMENT, (shank_diameter.record_id, base_diameter.record_id, tail_length.record_id, intrusion.record_id), domain)


def barrel_swept_volume(diameter: PhysicalValue, travel: PhysicalValue, convention: DiameterConvention, *, result_id: str) -> PhysicalValue:
    """Return bore area times explicitly referenced projectile travel."""
    area = circle_area(diameter, convention, result_id=f"{result_id}:area")
    require_positive(travel.quantity, Dimension.LENGTH, "projectile travel")
    volume = area.quantity.si_value * travel.quantity.si_value
    return _derived(result_id, Quantity(volume, Unit.CUBIC_METRE), METHOD_BARREL_SWEPT_VOLUME, (diameter.record_id, travel.record_id), f"diameter_convention={DiameterConvention(convention).value}")


def total_expanded_volume(usable_powder_space_volume: PhysicalValue, barrel_volume: PhysicalValue, *, result_id: str) -> PhysicalValue:
    """Return usable powder-space volume plus barrel swept volume."""
    require_positive(usable_powder_space_volume.quantity, Dimension.VOLUME, "usable powder-space volume")
    require_positive(barrel_volume.quantity, Dimension.VOLUME, "barrel volume")
    return _derived(result_id, Quantity(usable_powder_space_volume.quantity.si_value + barrel_volume.quantity.si_value, Unit.CUBIC_METRE), METHOD_TOTAL_EXPANDED_VOLUME, (usable_powder_space_volume.record_id, barrel_volume.record_id))


def barrel_volume_ratio(barrel_volume: PhysicalValue, usable_powder_space_volume: PhysicalValue, *, result_id: str) -> PhysicalValue:
    """Return explicitly named Vb/V0."""
    require_positive(barrel_volume.quantity, Dimension.VOLUME, "barrel volume")
    require_positive(usable_powder_space_volume.quantity, Dimension.VOLUME, "usable powder-space volume")
    return _derived(result_id, Quantity(barrel_volume.quantity.si_value / usable_powder_space_volume.quantity.si_value, Unit.ONE), METHOD_BARREL_VOLUME_RATIO, (barrel_volume.record_id, usable_powder_space_volume.record_id))


def total_expansion_ratio(barrel_volume: PhysicalValue, usable_powder_space_volume: PhysicalValue, *, result_id: str) -> PhysicalValue:
    """Return explicitly named (V0+Vb)/V0."""
    ratio = 1.0 + barrel_volume_ratio(barrel_volume, usable_powder_space_volume, result_id=f"{result_id}:barrel_ratio").quantity.si_value
    return _derived(result_id, Quantity(ratio, Unit.ONE), METHOD_TOTAL_EXPANSION_RATIO, (barrel_volume.record_id, usable_powder_space_volume.record_id))


def sectional_density_mass_over_diameter_squared(projectile_mass: PhysicalValue, projectile_diameter: PhysicalValue, *, result_id: str) -> PhysicalValue:
    """Return mass divided by projectile diameter squared in kg/m2."""
    require_positive(projectile_mass.quantity, Dimension.MASS, "projectile mass")
    require_positive(projectile_diameter.quantity, Dimension.LENGTH, "projectile diameter")
    value = projectile_mass.quantity.si_value / projectile_diameter.quantity.si_value**2
    return _derived(result_id, Quantity(value, Unit.KILOGRAM_PER_SQUARE_METRE), METHOD_SECTIONAL_DENSITY, (projectile_mass.record_id, projectile_diameter.record_id), "mass divided by diameter squared")


def _mass_ratio(numerator: PhysicalValue, denominator: PhysicalValue, result_id: str, method_id: str) -> PhysicalValue:
    require_positive(numerator.quantity, Dimension.MASS, "mass numerator")
    require_positive(denominator.quantity, Dimension.MASS, "mass denominator")
    return _derived(result_id, Quantity(numerator.quantity.si_value / denominator.quantity.si_value, Unit.ONE), method_id, (numerator.record_id, denominator.record_id))


def charge_to_bullet_mass_ratio(charge_mass: PhysicalValue, bullet_mass: PhysicalValue, *, result_id: str) -> PhysicalValue:
    """Return external charge mass divided by bullet mass."""
    return _mass_ratio(charge_mass, bullet_mass, result_id, METHOD_CHARGE_BULLET_RATIO)


def charge_to_gross_water_capacity_mass_ratio(charge_mass: PhysicalValue, capacity: GrossCaseCapacity, *, result_id: str) -> PhysicalValue:
    """Return charge mass divided by gross water-capacity mass."""
    return _mass_ratio(charge_mass, capacity.water_mass, result_id, METHOD_CHARGE_GROSS_WATER_RATIO)


def charge_to_measured_usable_water_capacity_mass_ratio(charge_mass: PhysicalValue, capacity: MeasuredUsablePowderSpace, *, result_id: str) -> PhysicalValue:
    """Return charge mass divided by measured usable water mass."""
    return _mass_ratio(charge_mass, capacity.water_mass, result_id, METHOD_CHARGE_MEASURED_WATER_RATIO)


def charge_to_estimated_usable_water_capacity_mass_ratio(charge_mass: PhysicalValue, capacity: EstimatedUsablePowderSpace, *, result_id: str) -> PhysicalValue:
    """Return charge mass divided by an explicit estimated water equivalent."""
    if capacity.equivalent_water_mass is None:
        raise ValueError("estimated usable capacity has no explicitly converted equivalent water mass")
    return _mass_ratio(charge_mass, capacity.equivalent_water_mass, result_id, METHOD_CHARGE_ESTIMATED_WATER_RATIO)


def derive_seating_depth(case_length: PhysicalValue, bullet_length: PhysicalValue, cartridge_overall_length: PhysicalValue, *, reference_conventions: tuple[str, str, str], result_id: str) -> SeatingDepth:
    """Derive case length plus bullet length minus COAL with matched datums."""
    for value, name in ((case_length, "case length"), (bullet_length, "bullet length"), (cartridge_overall_length, "COAL")):
        require_positive(value.quantity, Dimension.LENGTH, name)
    if len(set(reference_conventions)) != 1 or not reference_conventions[0].strip():
        raise ValueError("case, projectile, and COAL reference conventions must match explicitly")
    depth = case_length.quantity.si_value + bullet_length.quantity.si_value - cartridge_overall_length.quantity.si_value
    if depth <= 0:
        raise ValueError("derived seating depth must be greater than zero")
    value = _derived(result_id, Quantity(depth, Unit.METRE), METHOD_SEATING_DEPTH, (case_length.record_id, bullet_length.record_id, cartridge_overall_length.record_id), "S=case length+projectile length-COAL; compatible axial references explicitly asserted")
    return SeatingDepth(value, SeatingDepthKind.DERIVED, reference_conventions[0], METHOD_SEATING_DEPTH, (case_length.record_id, bullet_length.record_id, cartridge_overall_length.record_id), ("nominal dimensions are not inferred",))


def water_mass_to_volume(mass: PhysicalValue, density: PhysicalValue, *, result_id: str) -> PhysicalValue:
    """Convert water mass to volume using caller-supplied density."""
    require_positive(mass.quantity, Dimension.MASS, "water mass")
    require_positive(density.quantity, Dimension.MASS_DENSITY, "water density")
    return _derived(result_id, Quantity(mass.quantity.si_value / density.quantity.si_value, Unit.CUBIC_METRE), METHOD_WATER_SUPPLIED_DENSITY, (mass.record_id, density.record_id), "caller-supplied water density")


def water_volume_to_mass(volume: PhysicalValue, density: PhysicalValue, *, result_id: str) -> PhysicalValue:
    """Convert water volume to mass using caller-supplied density."""
    require_positive(volume.quantity, Dimension.VOLUME, "water volume")
    require_positive(density.quantity, Dimension.MASS_DENSITY, "water density")
    return _derived(result_id, Quantity(volume.quantity.si_value * density.quantity.si_value, Unit.KILOGRAM), METHOD_WATER_SUPPLIED_DENSITY, (volume.record_id, density.record_id), "caller-supplied water density")


def water_mass_to_volume_by_convention(mass: PhysicalValue, convention: WaterConversionConvention, *, result_id: str) -> PhysicalValue:
    """Convert water mass with an explicitly selected source convention."""
    require_positive(mass.quantity, Dimension.MASS, "water mass")
    convention = WaterConversionConvention(convention)
    grains = mass.quantity.to(Unit.GRAIN).value
    cubic_inches = grains / 253.0
    return _derived(result_id, Quantity(cubic_inches, Unit.CUBIC_INCH).to(Unit.CUBIC_METRE), METHOD_WATER_POWLEY_253, (mass.record_id,), f"explicit source convention={convention.value}")


def water_volume_to_mass_by_convention(volume: PhysicalValue, convention: WaterConversionConvention, *, result_id: str) -> PhysicalValue:
    """Convert water volume with an explicitly selected source convention."""
    require_positive(volume.quantity, Dimension.VOLUME, "water volume")
    convention = WaterConversionConvention(convention)
    cubic_inches = volume.quantity.to(Unit.CUBIC_INCH).value
    return _derived(result_id, Quantity(cubic_inches * 253.0, Unit.GRAIN).to(Unit.KILOGRAM), METHOD_WATER_POWLEY_253, (volume.record_id,), f"explicit source convention={convention.value}")


def _projectile_displacement(projectile: ProjectileRecord, result_id: str) -> PhysicalValue:
    if projectile.geometry_adequacy is GeometryAdequacy.OUTSIDE_MODEL:
        raise ValueError("projectile geometry is outside the M01 model")
    if projectile.seating_depth is None:
        raise ValueError("projectile seating depth is required")
    shank = projectile.cylindrical_shank_diameter or projectile.diameter
    if projectile.boat_tail_length is None:
        return flat_base_seated_displacement(shank, projectile.seating_depth.value, result_id=result_id)
    assert projectile.boat_tail_base_diameter is not None
    return boat_tail_seated_displacement(shank, projectile.boat_tail_base_diameter, projectile.boat_tail_length, projectile.seating_depth.value, result_id=result_id)


def estimate_geometric_usable_powder_space(gross_capacity: GrossCaseCapacity, projectile: ProjectileRecord, desired_primer_pocket_treatment: PrimerPocketTreatment, *, result_id: str, primer_pocket_volume: PrimerPocketVolume | None = None, assumptions: tuple[str, ...]) -> EstimatedUsablePowderSpace:
    """Estimate usable volume without replacing a measured capacity record."""
    if gross_capacity.water_volume is None:
        raise ValueError("gross capacity requires explicit water mass-to-volume conversion")
    if gross_capacity.conditions.fill_boundary is not CapacityFillBoundary.CASE_MOUTH:
        raise ValueError("geometric estimate requires a known case-mouth gross-capacity boundary")
    source_treatment = gross_capacity.conditions.primer_pocket_treatment
    desired = PrimerPocketTreatment(desired_primer_pocket_treatment)
    if PrimerPocketTreatment.UNKNOWN in {source_treatment, desired}:
        raise ValueError("primer-pocket treatment must be known")
    adjusted = gross_capacity.water_volume.quantity.si_value
    correction_id = None
    inputs = [gross_capacity.record_id, projectile.record_id, gross_capacity.water_volume.record_id]
    if source_treatment is not desired:
        if {source_treatment, desired} != {PrimerPocketTreatment.INCLUDED, PrimerPocketTreatment.EXCLUDED}:
            raise ValueError("primer-pocket treatment mismatch is not geometrically defined")
        if primer_pocket_volume is None:
            raise ValueError("explicit primer-pocket volume is required to change capacity basis")
        if primer_pocket_volume.cartridge_id != gross_capacity.cartridge_id:
            raise ValueError("primer-pocket correction must belong to the gross-capacity cartridge")
        correction = primer_pocket_volume.volume.quantity.si_value
        adjusted += correction if source_treatment is PrimerPocketTreatment.EXCLUDED else -correction
        correction_id = primer_pocket_volume.record_id
        inputs.append(primer_pocket_volume.record_id)
    displacement = _projectile_displacement(projectile, f"{result_id}:displacement")
    inputs.append(displacement.record_id)
    usable = adjusted - displacement.quantity.si_value
    if usable <= 0:
        raise ValueError("geometric usable powder-space volume must be greater than zero")
    value = _derived(result_id + ":volume", Quantity(usable, Unit.CUBIC_METRE), METHOD_USABLE_SPACE_ESTIMATE, tuple(inputs), "uncertainty unresolved; no measured value replaced")
    return EstimatedUsablePowderSpace(result_id, gross_capacity.cartridge_id, gross_capacity.record_id, projectile.record_id, value, displacement.provenance.method_id or "", desired, projectile.geometry_adequacy, assumptions, tuple(inputs), correction_id)


def compare_usable_powder_spaces(measured: MeasuredUsablePowderSpace, estimated: EstimatedUsablePowderSpace, *, result_id: str) -> CapacityComparison:
    """Compare measured and estimated records without averaging or selecting."""
    if measured.water_volume is None:
        raise ValueError("measured usable capacity requires explicit volume conversion for comparison")
    if measured.cartridge_id != estimated.cartridge_id:
        raise ValueError("capacity comparison requires the same cartridge identity")
    difference = estimated.usable_volume.quantity.si_value - measured.water_volume.quantity.si_value
    value = _derived(result_id + ":difference", Quantity(difference, Unit.CUBIC_METRE), METHOD_CAPACITY_COMPARISON, (measured.record_id, estimated.record_id), "estimated minus measured; records retained separately")
    return CapacityComparison(result_id, measured.record_id, estimated.record_id, value)
