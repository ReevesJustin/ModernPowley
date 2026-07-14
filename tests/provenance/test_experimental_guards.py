import pytest

from modern_powley.experimental.ba_eff import effective_vivacity_hypothesis
from modern_powley.experimental.ba_target import ba_target
from modern_powley.experimental.charge_regression import predicted_charge


@pytest.mark.parametrize(
    ("function", "args"),
    [(ba_target, (3.0,)), (effective_vivacity_hypothesis, (0.4, 1.5, 0.8)), (predicted_charge, (50, 22))],
)
def test_experiments_require_opt_in(function, args):
    with pytest.raises(RuntimeError, match="unvalidated"):
        function(*args)


def test_quarantined_equations_are_reproducible_only_after_opt_in():
    assert ba_target(3, allow_unvalidated=True) == pytest.approx(0.70)
    assert effective_vivacity_hypothesis(0.4, 1.5, 0.8, allow_unvalidated=True) == pytest.approx(0.52)
    assert predicted_charge(50, 22, allow_unvalidated=True) == pytest.approx(0.71 * 50**1.02 * 22**0.06)
