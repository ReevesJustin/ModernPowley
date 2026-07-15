from math import pi

import pytest

from modern_powley.original.charge import (
    LOW_DENSITY_POWDERS,
    STANDARD_DENSITY_POWDERS,
    charge_from_measured_powder_space,
    loading_density,
)
from modern_powley.original.geometry import (
    barrel_volume_ratio,
    barrel_volume_water_grains,
    effective_bore_diameter_inches,
    mass_ratio,
    projectile_travel_inches,
    sectional_density,
    total_expansion_ratio,
    total_expansion_ratio_from_dimensions,
)
from modern_powley.original.units import cubic_inches_to_water_grains


def test_every_original_scalar_relation_matches_independent_arithmetic():
    effective_diameter = (0.300 + 0.308) / 2
    travel = (21 + 5 / 16) + (1 + 1 / 16)
    bore_capacity = pi * (effective_diameter / 2) ** 2 * travel * 253

    assert cubic_inches_to_water_grains(1.25) == pytest.approx(316.25)
    assert charge_from_measured_powder_space(51.5, "IMR 4064") == pytest.approx(51.5 * 0.86)
    assert sectional_density(180, 0.308) == pytest.approx((180 / 7000) / 0.308**2)
    assert mass_ratio(44.3, 150) == pytest.approx(44.3 / 150)
    assert effective_bore_diameter_inches(0.300, 0.308) == pytest.approx(effective_diameter)
    assert projectile_travel_inches(21 + 5 / 16, 1 + 1 / 16) == pytest.approx(travel)
    assert barrel_volume_water_grains(effective_diameter, travel) == pytest.approx(bore_capacity)
    assert barrel_volume_ratio(bore_capacity, 51.5) == pytest.approx(bore_capacity / 51.5)
    assert total_expansion_ratio(bore_capacity, 51.5) == pytest.approx(1 + bore_capacity / 51.5)
    assert total_expansion_ratio_from_dimensions(51.5, 0.300, 0.308, travel) == pytest.approx(
        1 + bore_capacity / 51.5
    )


def test_original_loading_density_domain_is_the_evidenced_1961_powder_set():
    assert LOW_DENSITY_POWDERS == {"IMR 4198", "IMR 4227"}
    assert STANDARD_DENSITY_POWDERS == {
        "IMR 5010",
        "IMR 4831",
        "IMR 4350",
        "IMR 4320",
        "IMR 4064",
        "IMR 3031",
    }
    for powder in LOW_DENSITY_POWDERS:
        assert loading_density(powder) == 0.80
    for powder in STANDARD_DENSITY_POWDERS:
        assert loading_density(powder) == 0.86
    assert charge_from_measured_powder_space(50, "IMR 4227") == 40


@pytest.mark.parametrize("bad_value", [0, -1, float("nan"), float("inf"), float("-inf")])
def test_original_scalar_functions_reject_invalid_required_numeric_inputs(bad_value):
    calls = (
        lambda: cubic_inches_to_water_grains(bad_value),
        lambda: charge_from_measured_powder_space(bad_value, "IMR 4064"),
        lambda: sectional_density(bad_value, 0.308),
        lambda: sectional_density(180, bad_value),
        lambda: mass_ratio(bad_value, 150),
        lambda: mass_ratio(44.3, bad_value),
        lambda: effective_bore_diameter_inches(bad_value, 0.308),
        lambda: effective_bore_diameter_inches(0.300, bad_value),
        lambda: projectile_travel_inches(bad_value, 1.0),
        lambda: projectile_travel_inches(21.0, bad_value),
        lambda: barrel_volume_water_grains(bad_value, 22.0),
        lambda: barrel_volume_water_grains(0.304, bad_value),
        lambda: barrel_volume_ratio(bad_value, 50),
        lambda: barrel_volume_ratio(400, bad_value),
        lambda: total_expansion_ratio(bad_value, 50),
        lambda: total_expansion_ratio(400, bad_value),
        lambda: total_expansion_ratio_from_dimensions(bad_value, 0.300, 0.308, 22.0),
        lambda: total_expansion_ratio_from_dimensions(51.5, bad_value, 0.308, 22.0),
        lambda: total_expansion_ratio_from_dimensions(51.5, 0.300, bad_value, 22.0),
        lambda: total_expansion_ratio_from_dimensions(51.5, 0.300, 0.308, bad_value),
    )
    for call in calls:
        with pytest.raises(ValueError):
            call()


def test_additional_manual_charge_examples_reconcile_without_scale_inference():
    assert 61.5 * 0.86 == pytest.approx(52.89)
    assert charge_from_measured_powder_space(61.5, "IMR 4350") == pytest.approx(52.89)
    assert 79 * 0.86 == pytest.approx(67.94)
    assert charge_from_measured_powder_space(79, "IMR 5010") == pytest.approx(67.94)
    assert 95 * 0.86 == pytest.approx(81.70)
    assert charge_from_measured_powder_space(95, "IMR 5010") == pytest.approx(81.70)
