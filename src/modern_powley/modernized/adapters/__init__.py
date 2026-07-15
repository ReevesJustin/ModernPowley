"""Explicit adapters from M01 records to separately governed model families."""

from .original import (
    HistoricalScalarResult,
    original_barrel_volume,
    original_barrel_volume_ratio,
    original_charge_arithmetic,
    original_effective_bore_diameter,
    original_mass_ratio,
    original_projectile_travel,
    original_sectional_density,
    original_total_expansion_ratio,
)

__all__ = [
    "HistoricalScalarResult",
    "original_barrel_volume",
    "original_barrel_volume_ratio",
    "original_charge_arithmetic",
    "original_effective_bore_diameter",
    "original_mass_ratio",
    "original_projectile_travel",
    "original_sectional_density",
    "original_total_expansion_ratio",
]
