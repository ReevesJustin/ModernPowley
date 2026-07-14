"""Quarantined unvalidated vivacity average; not ballistic efficiency."""

from ._guard import require_opt_in

PROVENANCE_CLASS = "ModernPowley experimental hypothesis"


def effective_vivacity_hypothesis(
    ba: float, a0: float, z2: float, *, allow_unvalidated: bool = False
) -> float:
    require_opt_in(allow_unvalidated)
    return float(ba) * (float(a0) + (1.0 - float(a0)) * (float(z2) / 2.0))
