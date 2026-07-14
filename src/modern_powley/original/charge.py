"""Charge arithmetic printed in the 1961 instruction manual."""

from .units import _positive

SOURCE_ID = "SRC-POWLEY-1961-MANUAL"
LOW_DENSITY_POWDERS = frozenset({"IMR 4198", "IMR 4227"})
STANDARD_DENSITY_POWDERS = frozenset(
    {"IMR 5010", "IMR 4831", "IMR 4350", "IMR 4320", "IMR 4064", "IMR 3031"}
)


def loading_density(powder_name: str) -> float:
    normalized = " ".join(str(powder_name).upper().replace("-", " ").split())
    if normalized in LOW_DENSITY_POWDERS:
        return 0.80
    if normalized in STANDARD_DENSITY_POWDERS:
        return 0.86
    raise ValueError("the 1961 loading-density rule is sourced only for the listed IMR powders")


def charge_from_measured_powder_space(net_capacity_water_grains: float, powder_name: str) -> float:
    return _positive(net_capacity_water_grains, "net_capacity_water_grains") * loading_density(powder_name)
