import pytest

from modern_powley.original.charge import charge_from_measured_powder_space, loading_density
from modern_powley.original.units import cubic_inches_to_water_grains


def test_powley_water_conversion():
    assert cubic_inches_to_water_grains(1) == 253


def test_original_loading_density_rules():
    assert loading_density("IMR 4198") == 0.80
    assert loading_density("IMR-4227") == 0.80
    assert loading_density("IMR 4064") == 0.86


def test_non_imr_does_not_borrow_imr_density():
    with pytest.raises(ValueError):
        loading_density("H4350")
    with pytest.raises(ValueError):
        loading_density("IMR 7977")


def test_charge_requires_net_powder_space_input():
    assert charge_from_measured_powder_space(51.5, "IMR 4064") == pytest.approx(44.29)
