import pytest

from modern_powley.original.geometry import (
    barrel_volume_ratio,
    effective_bore_diameter_inches,
    mass_ratio,
    projectile_travel_inches,
    sectional_density,
    total_expansion_ratio,
    total_expansion_ratio_from_dimensions,
)


def test_sectional_density_inch_pound_convention():
    assert sectional_density(180, 0.308) == pytest.approx(0.2710647423)


def test_sectional_density_is_not_bullet_weight():
    assert sectional_density(135, 0.257) != 135


def test_mass_ratio_is_charge_over_bullet_weight():
    assert mass_ratio(59, 180) == pytest.approx(0.3277777778)


def test_manual_effective_diameter_is_average_of_bore_and_groove():
    assert effective_bore_diameter_inches(0.300, 0.308) == pytest.approx(0.304)


def test_expansion_ratios_have_distinct_names():
    assert barrel_volume_ratio(400, 50) == 8
    assert total_expansion_ratio(400, 50) == 9


def test_projectile_travel_uses_bullet_base_position():
    assert projectile_travel_inches(21 + 5 / 16, 1 + 1 / 16) == pytest.approx(22.375)


def test_manual_308_dimensions_reproduce_printed_expansion_ratio():
    assert total_expansion_ratio_from_dimensions(51.5, 0.300, 0.308, 22.375) == pytest.approx(9.0, abs=0.05)


@pytest.mark.parametrize("value", [0, -1, float("nan"), float("inf")])
def test_invalid_required_inputs_fail(value):
    with pytest.raises(ValueError):
        sectional_density(180, value)
