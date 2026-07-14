import pytest

from modern_powley.original.charge import charge_from_measured_powder_space
from modern_powley.original.geometry import (
    mass_ratio,
    projectile_travel_inches,
    total_expansion_ratio_from_dimensions,
)


def test_manual_308_worked_example_reproduces_available_arithmetic():
    # 1961 manual p. 9: 51.5 gr H2O gives 44.3 gr; cleaning-rod
    # measurements 21-5/16 + 1-1/16 give about 22.4 inches travel.
    assert charge_from_measured_powder_space(51.5, "IMR 4064") == pytest.approx(44.3, abs=0.05)
    assert mass_ratio(44.3, 150) == pytest.approx(0.295, abs=0.0005)
    assert projectile_travel_inches(21 + 5 / 16, 1 + 1 / 16) == pytest.approx(22.4, abs=0.05)
    assert total_expansion_ratio_from_dimensions(51.5, 0.300, 0.308, 22 + 3 / 8) == pytest.approx(
        9.0, abs=0.05
    )
