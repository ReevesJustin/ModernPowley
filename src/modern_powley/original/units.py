"""Units explicitly used by the 1961 Powley instruction manual."""

from math import isfinite

GRAINS_PER_POUND = 7000.0
WATER_GRAINS_PER_CUBIC_INCH_POWLEY = 253.0
SOURCE_ID = "SRC-POWLEY-1961-MANUAL"


def _positive(value: float, name: str) -> float:
    value = float(value)
    if not isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be finite and greater than zero")
    return value


def cubic_inches_to_water_grains(volume_cubic_inches: float) -> float:
    """Convert using Powley's stated 253 grains of water per cubic inch."""
    return _positive(volume_cubic_inches, "volume_cubic_inches") * WATER_GRAINS_PER_CUBIC_INCH_POWLEY
