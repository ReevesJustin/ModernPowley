"""Quarantined in-sample regression whose original fit procedure is absent."""

from ._guard import require_opt_in

PROVENANCE_CLASS = "empirical regression"


def predicted_charge(
    net_capacity_water_grains: float,
    projectile_travel_inches: float,
    *,
    allow_unvalidated: bool = False,
) -> float:
    require_opt_in(allow_unvalidated)
    return 0.71 * float(net_capacity_water_grains) ** 1.02 * float(projectile_travel_inches) ** 0.06
