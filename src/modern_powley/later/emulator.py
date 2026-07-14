"""Exact arithmetic transcribed from the archived kwk.us emulator.

This module reproduces SRC-KWK-EMULATOR. It is not the original Powley method.
"""

from dataclasses import dataclass
from math import floor, isfinite, sqrt

SOURCE_ID = "SRC-KWK-EMULATOR"


def _positive(value: float, name: str) -> float:
    result = float(value)
    if not isfinite(result) or result <= 0:
        raise ValueError(f"{name} must be finite and greater than zero")
    return result


def sectional_density(bullet_weight_grains: float, bullet_diameter_inches: float) -> float:
    return _positive(bullet_weight_grains, "bullet_weight_grains") / 7000.0 / _positive(
        bullet_diameter_inches, "bullet_diameter_inches"
    ) ** 2


def estimated_spitzer_bullet_length_inches(sectional_density_value: float) -> float:
    return 0.20 + 3.67 * _positive(sectional_density_value, "sectional_density")


def estimated_round_nose_bullet_length_inches(sectional_density_value: float) -> float:
    return 0.08 + 3.67 * _positive(sectional_density_value, "sectional_density")


def seating_depth_inches(case_length_inches: float, bullet_length_inches: float, cartridge_length_inches: float) -> float:
    depth = (
        _positive(case_length_inches, "case_length_inches")
        + _positive(bullet_length_inches, "bullet_length_inches")
        - _positive(cartridge_length_inches, "cartridge_length_inches")
    )
    if depth < 0:
        raise ValueError("emulator seating depth is negative")
    return depth


def bullet_travel_inches(barrel_length_inches: float, case_length_inches: float, seating_depth: float) -> float:
    depth = float(seating_depth)
    if not isfinite(depth) or depth < 0:
        raise ValueError("seating_depth must be finite and nonnegative")
    travel = (
        _positive(barrel_length_inches, "barrel_length_inches")
        - _positive(case_length_inches, "case_length_inches")
        + depth
    )
    if not isfinite(travel) or travel <= 0:
        raise ValueError("emulator bullet travel must be positive")
    return travel


def approximate_bore_area_square_inches(bullet_diameter_inches: float) -> float:
    return 0.773 * _positive(bullet_diameter_inches, "bullet_diameter_inches") ** 2


def total_expansion_ratio_from_geometry(
    net_capacity_water_grains: float,
    bullet_diameter_inches: float,
    travel_inches: float,
) -> float:
    net_volume_cubic_inches = _positive(net_capacity_water_grains, "net_capacity_water_grains") / 252.4
    bore_volume_cubic_inches = approximate_bore_area_square_inches(bullet_diameter_inches) * _positive(
        travel_inches, "travel_inches"
    )
    return (bore_volume_cubic_inches + net_volume_cubic_inches) / net_volume_cubic_inches


def net_capacity_from_gross(
    gross_capacity_water_grains: float,
    seating_depth_inches: float,
    bullet_diameter_inches: float,
) -> float:
    gross = _positive(gross_capacity_water_grains, "gross_capacity_water_grains")
    depth = float(seating_depth_inches)
    if not isfinite(depth) or depth < 0:
        raise ValueError("seating_depth_inches must be finite and nonnegative")
    net = gross - 198.0 * depth * _positive(bullet_diameter_inches, "bullet_diameter_inches") ** 2
    if net <= 0:
        raise ValueError("emulator geometry leaves no volume under the bullet")
    return net


def powder_index(sectional_density_value: float, mass_ratio_value: float) -> float:
    return 20.0 + 12.0 / (
        _positive(sectional_density_value, "sectional_density") * sqrt(_positive(mass_ratio_value, "mass_ratio"))
    )


@dataclass(frozen=True)
class PowderBand:
    lower: float | None
    lower_inclusive: bool
    upper: float | None
    upper_inclusive: bool
    designation: str
    instruction: str

    def includes(self, value: float) -> bool:
        lower_ok = self.lower is None or value > self.lower or (self.lower_inclusive and value == self.lower)
        upper_ok = self.upper is None or value < self.upper or (self.upper_inclusive and value == self.upper)
        return lower_ok and upper_ok


POWDER_BANDS = (
    PowderBand(None, False, 81.0, False, "", "Much slower than 4831"),
    PowderBand(81.0, True, 91.0, True, "", "Slower than 4831"),
    PowderBand(91.0, False, 110.0, True, "4831;4350", ""),
    PowderBand(110.0, False, 125.0, True, "4320;4895;4064", ""),
    PowderBand(125.0, False, 145.0, True, "3031", ""),
    PowderBand(145.0, False, 165.0, True, "4198", ""),
    PowderBand(165.0, False, 180.0, True, "4227", ""),
    PowderBand(180.0, False, None, False, "", "Faster than 4227"),
)


def select_powder_band(index: float) -> PowderBand:
    value = _positive(index, "index")
    matches = [band for band in POWDER_BANDS if band.includes(value)]
    if len(matches) != 1:
        raise RuntimeError("archived emulator powder bands are not a total non-overlapping partition")
    return matches[0]


@dataclass(frozen=True)
class LoadResult:
    charge_weight_grains: float
    mass_ratio: float
    powder_index: float
    powder_band: PowderBand


def load_from_net_capacity(
    net_capacity_water_grains: float,
    bullet_weight_grains: float,
    bullet_diameter_inches: float,
) -> LoadResult:
    net = _positive(net_capacity_water_grains, "net_capacity_water_grains")
    bullet = _positive(bullet_weight_grains, "bullet_weight_grains")
    sd = sectional_density(bullet, bullet_diameter_inches)
    charge = 0.86 * net
    ratio = charge / bullet
    index = powder_index(sd, ratio)
    if index > 145.0:
        charge = 0.80 * net
        ratio = charge / bullet
    return LoadResult(charge, ratio, index, select_powder_band(index))


def javascript_round_to_increment(value: float, increment: float) -> float:
    number = _positive(value, "value")
    step = _positive(increment, "increment")
    return floor(number / step + 0.5) * step


def velocity_fps(
    charge_weight_grains: float,
    bullet_weight_grains: float,
    total_expansion_ratio: float,
) -> float:
    charge = _positive(charge_weight_grains, "charge_weight_grains")
    bullet = _positive(bullet_weight_grains, "bullet_weight_grains")
    ratio = _positive(total_expansion_ratio, "total_expansion_ratio")
    if ratio <= 1:
        raise ValueError("total_expansion_ratio must be greater than one")
    return 8000.0 * sqrt(charge * (1.0 - ratio ** (-0.25)) / (bullet + charge / 3.0))


def miller_f2(mass_ratio_value: float, total_expansion_ratio: float) -> float:
    mass_ratio = _positive(mass_ratio_value, "mass_ratio")
    ratio = _positive(total_expansion_ratio, "total_expansion_ratio")
    return 0.024075 * (9.3 - mass_ratio) * (1.071 + ratio - 0.009736 * ratio**2)


def pressure_cup(
    velocity_fps_value: float,
    loading_density: float,
    total_expansion_ratio: float,
    mass_ratio_value: float,
) -> float:
    velocity = _positive(velocity_fps_value, "velocity_fps")
    density = _positive(loading_density, "loading_density")
    ratio = _positive(total_expansion_ratio, "total_expansion_ratio")
    mass_ratio = _positive(mass_ratio_value, "mass_ratio")
    if ratio <= 1:
        raise ValueError("total_expansion_ratio must be greater than one")
    k2 = 0.53 / mass_ratio + 0.26
    return 134.7 * (velocity / 100.0) ** 2 * density / (ratio - 1.0) * k2 * miller_f2(mass_ratio, ratio)


def cup_to_claimed_psi(cup: float) -> float:
    value = _positive(cup, "cup")
    return value * (1.0 + value**2.2 / 1.2e11)


def velocity_for_target_cup(
    target_cup: float,
    total_expansion_ratio: float,
    mass_ratio_value: float,
) -> float:
    cup = _positive(target_cup, "target_cup")
    ratio = _positive(total_expansion_ratio, "total_expansion_ratio")
    mass_ratio = _positive(mass_ratio_value, "mass_ratio")
    if ratio <= 1:
        raise ValueError("total_expansion_ratio must be greater than one")
    k2 = 0.53 / mass_ratio + 0.26
    return 100.0 * sqrt(cup / k2 / miller_f2(mass_ratio, ratio) * (ratio - 1.0) / 0.86 / 134.7)


def kinetic_energy_foot_pounds(bullet_weight_grains: float, velocity_fps_value: float) -> float:
    bullet = _positive(bullet_weight_grains, "bullet_weight_grains")
    velocity = _positive(velocity_fps_value, "velocity_fps")
    return 0.5 * bullet / 7000.0 / 32.2 * velocity**2


def efficiency_percent(
    bullet_weight_grains: float,
    velocity_fps_value: float,
    charge_weight_grains: float,
) -> float:
    energy = kinetic_energy_foot_pounds(bullet_weight_grains, velocity_fps_value)
    return 100.0 * energy / (_positive(charge_weight_grains, "charge_weight_grains") * 185.0)
