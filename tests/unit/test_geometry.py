import math

import pytest

from modern_powley.original.geometry import (
    barrel_volume_ratio,
    cylindrical_bullet_intrusion_water_grains,
    mass_ratio,
    net_case_capacity,
    projectile_travel_inches,
    sectional_density,
    total_expansion_ratio,
)


def test_sectional_density_inch_pound_convention():
    assert sectional_density(180, 0.308) == pytest.approx(0.2710647423)


def test_sectional_density_is_not_bullet_weight():
    assert sectional_density(135, 0.257) != 135


def test_mass_ratio_is_charge_over_bullet_weight():
    assert mass_ratio(59, 180) == pytest.approx(0.3277777778)


def test_net_capacity_subtracts_intrusion_and_rejects_gross_alias():
    assert net_case_capacity(52.0, 4.5) == 47.5
    with pytest.raises(ValueError):
        net_case_capacity(52.0, 52.0)


def test_cylindrical_intrusion_keeps_units_explicit():
    expected = math.pi * (0.264 / 2) ** 2 * 0.4 * 253.0
    assert cylindrical_bullet_intrusion_water_grains(0.264, 0.4) == pytest.approx(expected)


def test_expansion_ratios_have_distinct_names():
    assert barrel_volume_ratio(400, 50) == 8
    assert total_expansion_ratio(400, 50) == 9


def test_projectile_travel_uses_bullet_base_position():
    assert projectile_travel_inches(21 + 5 / 16, 1 + 1 / 16) == pytest.approx(22.375)


@pytest.mark.parametrize("value", [0, -1, float("nan"), float("inf")])
def test_invalid_required_inputs_fail(value):
    with pytest.raises(ValueError):
        sectional_density(180, value)
