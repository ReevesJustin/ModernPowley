import pytest

from modern_powley.original.charge import charge_from_measured_powder_space
from modern_powley.original.geometry import projectile_travel_inches


def test_manual_308_worked_example_reproduces_available_arithmetic():
    # 1961 manual p. 9: 51.5 gr H2O gives 44.3 gr; cleaning-rod
    # measurements 21-5/16 + 1-1/16 give about 22.4 inches travel.
    assert charge_from_measured_powder_space(51.5, "IMR 4064") == pytest.approx(44.3, abs=0.05)
    assert projectile_travel_inches(21 + 5 / 16, 1 + 1 / 16) == pytest.approx(22.4, abs=0.05)
