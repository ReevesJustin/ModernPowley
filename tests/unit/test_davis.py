from math import pi

import pytest

from modern_powley.later.davis import (
    boat_tail_correction_water_grains,
    bullet_travel_inches,
    charge_for_target_loading_density,
    effective_bore_volume_cubic_inches,
    expansion_ratio,
    flat_base_displacement_water_grains,
    historical_crusher_pressure,
    initial_charge_weight_grains,
    loaded_powder_space_capacity_water_grains,
    loading_density_pressure_scale,
    lookup_table4_f2,
    mass_ratio,
    muzzle_velocity_fps,
    powder_chamber_volume_cubic_inches,
    powder_selection_index,
    seating_depth_inches,
    sectional_density,
    velocity_fraction_m,
    velocity_fraction_n,
)
from modern_powley.provenance.validation import MissingProvenanceError


def test_davis_geometry_coefficients_retain_printed_precision():
    depth = 0.5
    diameter = 0.3
    printed = flat_base_displacement_water_grains(depth, diameter)
    geometric_identity = 252.4 * pi / 4 * depth * diameter**2
    assert printed == pytest.approx(198 * depth * diameter**2)
    assert printed == pytest.approx(geometric_identity, rel=0.002)
    assert effective_bore_volume_cubic_inches(20, diameter) == pytest.approx(0.773 * 20 * diameter**2)


def test_davis_flat_base_and_boat_tail_capacity_branches():
    displacement = flat_base_displacement_water_grains(0.4, 0.308)
    flat_capacity = loaded_powder_space_capacity_water_grains(60, displacement)
    correction = boat_tail_correction_water_grains(0.15, 0.308, 0.2, 0.4)
    boat_tail_capacity = loaded_powder_space_capacity_water_grains(60, displacement, correction)
    assert boat_tail_capacity == pytest.approx(flat_capacity + correction)


def test_davis_travel_volume_expansion_and_velocity_equations_independently():
    travel = bullet_travel_inches(24, 0.4, 2.5)
    assert travel == pytest.approx(21.9)
    chamber = powder_chamber_volume_cubic_inches(62.3)
    bore = effective_bore_volume_cubic_inches(travel, 0.308)
    ratio = expansion_ratio(bore, chamber)
    assert ratio == pytest.approx((bore + chamber) / chamber)
    m_value = velocity_fraction_m(ratio)
    n_value = velocity_fraction_n(m_value)
    assert m_value == pytest.approx(1 / ratio**0.25)
    assert n_value == pytest.approx(1 - m_value)
    assert muzzle_velocity_fps(53.6, n_value, 180 + 53.6 / 3) > 0


def test_davis_charge_ratio_sectional_density_and_index_equations_independently():
    assert initial_charge_weight_grains(50, "IMR 4198") == pytest.approx(40)
    assert initial_charge_weight_grains(50, "IMR 4227") == pytest.approx(40)
    assert initial_charge_weight_grains(50, "IMR 4350") == pytest.approx(43)
    assert mass_ratio(50, 200) == pytest.approx(0.25)
    assert sectional_density(180, 0.308) == pytest.approx(180 / (7000 * 0.308**2))
    assert powder_selection_index(0.271, 0.298) == pytest.approx(20 + 12 / (0.271 * 0.298**0.5))


def test_davis_loading_density_adjustments_are_explicit_approximate_operations():
    assert loading_density_pressure_scale(52_000, 0.865, 0.909) == pytest.approx(57_425, rel=0.001)
    assert charge_for_target_loading_density(49.5, 0.865) == pytest.approx(42.8, abs=0.05)


def test_davis_table4_exact_and_published_r_axis_interpolation():
    assert lookup_table4_f2(0.30, 7.4) == pytest.approx(1.72)
    assert lookup_table4_f2(0.30, 7.6) == pytest.approx(1.76)
    assert lookup_table4_f2(0.30, 7.5) == pytest.approx(1.74)


def test_davis_table4_a_axis_and_bilinear_interpolation_are_bounded():
    assert lookup_table4_f2(0.25, 7.4) == pytest.approx(1.725)
    assert lookup_table4_f2(0.25, 7.5) == pytest.approx(1.745)
    for mass_ratio_value, expansion_ratio_value in (
        (0.19, 7.5),
        (1.01, 7.5),
        (0.30, 4.9),
        (0.30, 13.1),
    ):
        with pytest.raises(ValueError, match="outside Davis Table 4"):
            lookup_table4_f2(mass_ratio_value, expansion_ratio_value)


def test_davis_pressure_still_requires_an_explicit_f2_value():
    with pytest.raises(MissingProvenanceError):
        historical_crusher_pressure(53.6, 2620, 180, 62.3, 7.5)


@pytest.mark.parametrize(
    ("operation", "args"),
    [
        (seating_depth_inches, (2.0, 1.0, 3.1)),
        (flat_base_displacement_water_grains, (-0.1, 0.3)),
        (boat_tail_correction_water_grains, (0.5, 0.3, 0.2, 0.4)),
        (boat_tail_correction_water_grains, (0.1, 0.3, 0.31, 0.4)),
        (loaded_powder_space_capacity_water_grains, (0, 1)),
        (loaded_powder_space_capacity_water_grains, (5, 6)),
        (powder_chamber_volume_cubic_inches, (0,)),
        (mass_ratio, (1, 0)),
        (sectional_density, (1, 0)),
        (expansion_ratio, (1, 0)),
        (velocity_fraction_m, (1,)),
        (historical_crusher_pressure, (53.6, 2620, 180, 62.3, 1.0, 1.74)),
    ],
)
def test_davis_rejects_invalid_physical_inputs(operation, args):
    with pytest.raises(ValueError):
        operation(*args)


def test_davis_rejects_unlisted_powder_for_initial_density_rule():
    with pytest.raises(ValueError, match="evidenced Davis IMR powders"):
        initial_charge_weight_grains(50, "IMR 7828")
