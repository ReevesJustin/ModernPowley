"""Geometry and input definitions used by the audited baseline.

Powley's manual calls for measured water capacity of the powder space. No
gross-capacity subtraction helper is exposed in this source-backed namespace.
"""

from math import pi

from .units import GRAINS_PER_POUND, _positive, cubic_inches_to_water_grains

SOURCE_ID = "SRC-POWLEY-1961-MANUAL"


def sectional_density(bullet_weight_grains: float, bullet_diameter_inches: float) -> float:
    weight = _positive(bullet_weight_grains, "bullet_weight_grains")
    diameter = _positive(bullet_diameter_inches, "bullet_diameter_inches")
    return (weight / GRAINS_PER_POUND) / diameter**2


def mass_ratio(charge_weight_grains: float, bullet_weight_grains: float) -> float:
    return _positive(charge_weight_grains, "charge_weight_grains") / _positive(
        bullet_weight_grains, "bullet_weight_grains"
    )


def effective_bore_diameter_inches(bore_diameter_inches: float, groove_diameter_inches: float) -> float:
    """Manual p. 9 convention when the caliber slide does not list a caliber."""
    bore = _positive(bore_diameter_inches, "bore_diameter_inches")
    groove = _positive(groove_diameter_inches, "groove_diameter_inches")
    return (bore + groove) / 2.0


def projectile_travel_inches(distance_from_muzzle_to_bullet_tip_inches: float, bullet_length_inches: float) -> float:
    """Reproduce the cleaning-rod method in the manual's worked example."""
    return _positive(distance_from_muzzle_to_bullet_tip_inches, "distance_from_muzzle_to_bullet_tip_inches") + _positive(
        bullet_length_inches, "bullet_length_inches"
    )


def barrel_volume_water_grains(effective_bore_diameter_inches: float, projectile_travel: float) -> float:
    diameter = _positive(effective_bore_diameter_inches, "effective_bore_diameter_inches")
    travel = _positive(projectile_travel, "projectile_travel")
    return cubic_inches_to_water_grains(pi * (diameter / 2.0) ** 2 * travel)


def barrel_volume_ratio(barrel_volume_water_grains_value: float, net_capacity_water_grains: float) -> float:
    return _positive(barrel_volume_water_grains_value, "barrel_volume_water_grains") / _positive(
        net_capacity_water_grains, "net_capacity_water_grains"
    )


def total_expansion_ratio(barrel_volume_water_grains_value: float, net_capacity_water_grains: float) -> float:
    return 1.0 + barrel_volume_ratio(barrel_volume_water_grains_value, net_capacity_water_grains)


def total_expansion_ratio_from_dimensions(
    net_capacity_water_grains: float,
    bore_diameter_inches: float,
    groove_diameter_inches: float,
    projectile_travel: float,
) -> float:
    diameter = effective_bore_diameter_inches(bore_diameter_inches, groove_diameter_inches)
    barrel_volume = barrel_volume_water_grains(diameter, projectile_travel)
    return total_expansion_ratio(barrel_volume, net_capacity_water_grains)
