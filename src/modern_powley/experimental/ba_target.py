"""Quarantined agent-generated target; not a Powley equation."""

from ._guard import require_opt_in

PROVENANCE_CLASS = "agent-generated assumption"


def ba_target(relative_capacity: float, *, allow_unvalidated: bool = False) -> float:
    require_opt_in(allow_unvalidated)
    return max(0.45, min(0.90, 0.85 - 0.05 * float(relative_capacity)))
