"""W. C. Davis Jr.'s 1981 simplified interior-ballistics formulation.

These functions preserve Davis's printed constants and inch/grain conventions.
They are later historical operations, not an original-Powley implementation and
not loading recommendations.
"""

import csv
from dataclasses import dataclass
from functools import lru_cache
from math import isfinite, sqrt
from pathlib import Path

from modern_powley.provenance.validation import MissingProvenanceError

SOURCE_ID = "SRC-DAVIS-1981"
WATER_GRAINS_PER_CUBIC_INCH = 252.4

DAVIS_RELATIVE_QUICKNESS = {
    "IMR 4227": 180,
    "IMR 4198": 160,
    "IMR 3031": 135,
    "IMR 4064": 120,
    "IMR 4895": 115,
    "IMR 4320": 110,
    "IMR 4350": 100,
    "IMR 4831": 95,
}
TABLE4_PATH = Path(__file__).resolve().parents[3] / "data/reference/davis_1981_table4.csv"


def _finite(value: float, name: str) -> float:
    result = float(value)
    if not isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def _positive(value: float, name: str) -> float:
    result = _finite(value, name)
    if result <= 0:
        raise ValueError(f"{name} must be positive")
    return result


def _nonnegative(value: float, name: str) -> float:
    result = _finite(value, name)
    if result < 0:
        raise ValueError(f"{name} must be nonnegative")
    return result


def seating_depth_inches(
    case_length_inches: float,
    bullet_length_inches: float,
    cartridge_oal_inches: float,
) -> float:
    """Davis S = C + B - L."""
    case_length = _positive(case_length_inches, "case_length_inches")
    bullet_length = _positive(bullet_length_inches, "bullet_length_inches")
    cartridge_oal = _positive(cartridge_oal_inches, "cartridge_oal_inches")
    return _positive(case_length + bullet_length - cartridge_oal, "seating_depth_inches")


def flat_base_displacement_water_grains(
    seating_depth_inches_value: float,
    bullet_diameter_inches: float,
) -> float:
    """Davis P = 198 S D^2, retaining the printed coefficient 198."""
    seating_depth = _positive(seating_depth_inches_value, "seating_depth_inches")
    diameter = _positive(bullet_diameter_inches, "bullet_diameter_inches")
    return 198.0 * seating_depth * diameter**2


def boat_tail_correction_water_grains(
    boat_tail_height_inches: float,
    bullet_diameter_inches: float,
    boat_tail_small_diameter_inches: float,
    seating_depth_inches_value: float,
) -> float:
    """Davis K = 66 H (2 D^2 - D J - J^2)."""
    height = _positive(boat_tail_height_inches, "boat_tail_height_inches")
    diameter = _positive(bullet_diameter_inches, "bullet_diameter_inches")
    tail_diameter = _positive(boat_tail_small_diameter_inches, "boat_tail_small_diameter_inches")
    seating_depth = _positive(seating_depth_inches_value, "seating_depth_inches")
    if height > seating_depth:
        raise ValueError("boat_tail_height_inches must not exceed seating_depth_inches")
    if tail_diameter > diameter:
        raise ValueError("boat_tail_small_diameter_inches must not exceed bullet_diameter_inches")
    return 66.0 * height * (2.0 * diameter**2 - diameter * tail_diameter - tail_diameter**2)


def loaded_powder_space_capacity_water_grains(
    gross_case_capacity_water_grains: float,
    flat_base_displacement_water_grains_value: float,
    boat_tail_correction_water_grains_value: float = 0.0,
) -> float:
    """Davis W = F - P for flat bases, or W = F - P + K for boat tails."""
    gross_capacity = _positive(gross_case_capacity_water_grains, "gross_case_capacity_water_grains")
    displacement = _nonnegative(
        flat_base_displacement_water_grains_value,
        "flat_base_displacement_water_grains",
    )
    correction = _nonnegative(
        boat_tail_correction_water_grains_value,
        "boat_tail_correction_water_grains",
    )
    return _positive(gross_capacity - displacement + correction, "loaded_powder_space_capacity_water_grains")


def bullet_travel_inches(
    barrel_length_from_bolt_face_inches: float,
    seating_depth_inches_value: float,
    case_length_inches: float,
) -> float:
    """Davis T = E + S - C, preserving the printed sequence."""
    barrel_length = _positive(
        barrel_length_from_bolt_face_inches,
        "barrel_length_from_bolt_face_inches",
    )
    seating_depth = _positive(seating_depth_inches_value, "seating_depth_inches")
    case_length = _positive(case_length_inches, "case_length_inches")
    return _positive(barrel_length + seating_depth - case_length, "bullet_travel_inches")


def powder_chamber_volume_cubic_inches(loaded_capacity_water_grains: float) -> float:
    """Davis U = W / 252.4."""
    capacity = _positive(loaded_capacity_water_grains, "loaded_capacity_water_grains")
    return capacity / WATER_GRAINS_PER_CUBIC_INCH


def effective_bore_volume_cubic_inches(
    bullet_travel_inches_value: float,
    bullet_diameter_inches: float,
) -> float:
    """Davis Q = 0.773 T D^2, including his approximate land-area reduction."""
    travel = _positive(bullet_travel_inches_value, "bullet_travel_inches")
    diameter = _positive(bullet_diameter_inches, "bullet_diameter_inches")
    return 0.773 * travel * diameter**2


def expansion_ratio(
    effective_bore_volume_cubic_inches_value: float,
    powder_chamber_volume_cubic_inches_value: float,
) -> float:
    """Davis R = (Q + U) / U."""
    bore_volume = _positive(
        effective_bore_volume_cubic_inches_value,
        "effective_bore_volume_cubic_inches",
    )
    chamber_volume = _positive(
        powder_chamber_volume_cubic_inches_value,
        "powder_chamber_volume_cubic_inches",
    )
    return (bore_volume + chamber_volume) / chamber_volume


def initial_charge_weight_grains(
    loaded_capacity_water_grains: float,
    powder_designation: str,
) -> float:
    """Davis I = LD W using 0.80 for 4198/4227 and 0.86 for listed peers."""
    capacity = _positive(loaded_capacity_water_grains, "loaded_capacity_water_grains")
    if powder_designation not in DAVIS_RELATIVE_QUICKNESS:
        raise ValueError("powder_designation must be one of the evidenced Davis IMR powders")
    loading_density = 0.80 if powder_designation in {"IMR 4198", "IMR 4227"} else 0.86
    return loading_density * capacity


def mass_ratio(charge_weight_grains: float, bullet_weight_grains: float) -> float:
    """Davis A = I / G."""
    charge = _positive(charge_weight_grains, "charge_weight_grains")
    bullet = _positive(bullet_weight_grains, "bullet_weight_grains")
    return charge / bullet


def sectional_density(bullet_weight_grains: float, bullet_diameter_inches: float) -> float:
    """Davis Z = G / (7000 D^2)."""
    bullet = _positive(bullet_weight_grains, "bullet_weight_grains")
    diameter = _positive(bullet_diameter_inches, "bullet_diameter_inches")
    return bullet / (7000.0 * diameter**2)


def powder_selection_index(sectional_density_value: float, mass_ratio_value: float) -> float:
    """Davis empirical powder-selection index X = 20 + 12/(Z sqrt(A))."""
    sd = _positive(sectional_density_value, "sectional_density")
    ratio = _positive(mass_ratio_value, "mass_ratio")
    return 20.0 + 12.0 / (sd * sqrt(ratio))


def velocity_fraction_m(expansion_ratio_value: float) -> float:
    """Davis M = 1 / R^(1/4)."""
    ratio = _positive(expansion_ratio_value, "expansion_ratio")
    if ratio <= 1.0:
        raise ValueError("expansion_ratio must be greater than 1")
    return 1.0 / ratio**0.25


def velocity_fraction_n(velocity_fraction_m_value: float) -> float:
    """Davis N = 1 - M."""
    m_value = _positive(velocity_fraction_m_value, "velocity_fraction_m")
    if m_value >= 1.0:
        raise ValueError("velocity_fraction_m must be less than 1")
    return 1.0 - m_value


def effective_moving_weight_grains(
    bullet_weight_grains: float,
    charge_weight_grains: float,
) -> float:
    """Davis Y = G + I/3."""
    bullet = _positive(bullet_weight_grains, "bullet_weight_grains")
    charge = _positive(charge_weight_grains, "charge_weight_grains")
    return bullet + charge / 3.0


def muzzle_velocity_fps(
    charge_weight_grains: float,
    velocity_fraction_n_value: float,
    effective_moving_weight_grains_value: float,
) -> float:
    """Davis-printed, Davis-attributed Powley equation V = 8000 sqrt(I N / Y)."""
    charge = _positive(charge_weight_grains, "charge_weight_grains")
    n_value = _positive(velocity_fraction_n_value, "velocity_fraction_n")
    moving_weight = _positive(
        effective_moving_weight_grains_value,
        "effective_moving_weight_grains",
    )
    return 8000.0 * sqrt(charge * n_value / moving_weight)


@dataclass(frozen=True)
class PressureTerms:
    """Davis's printed K1, K2, and K3 pressure intermediates."""

    k1: float
    k2: float
    k3: float


@dataclass(frozen=True)
class Table4Row:
    """One expansion-ratio row from Davis Table 4."""

    expansion_ratio: float
    f2_values: tuple[float, ...]


@dataclass(frozen=True)
class Table4:
    """Normalized Davis Table 4 with mass-ratio columns and expansion-ratio rows."""

    mass_ratios: tuple[float, ...]
    rows: tuple[Table4Row, ...]


@lru_cache(maxsize=1)
def load_table4() -> Table4:
    """Load and validate the source-backed Table 4 transcription."""
    mass_ratios = (0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00)
    value_columns = tuple(f"mass_ratio_{value:.2f}".replace(".", "_") for value in mass_ratios)
    with TABLE4_PATH.open(newline="", encoding="utf-8") as handle:
        source_rows = list(csv.DictReader(handle))
    if len(source_rows) != 34:
        raise ValueError("Davis Table 4 must contain exactly 34 expansion-ratio rows")

    rows = []
    for source_row in source_rows:
        if source_row["table_id"] != "Davis Table 4" or source_row["source_id"] != SOURCE_ID:
            raise ValueError("Davis Table 4 source metadata is inconsistent")
        if (
            source_row["source_location"] != "Table 4"
            or source_row["source_classification"] != "later_primary_publication"
            or source_row["verification_status"] != "verified_primary"
            or source_row["confidence"] != "medium"
        ):
            raise ValueError("Davis Table 4 provenance metadata is inconsistent")
        values = tuple(_positive(source_row[column], column) for column in value_columns)
        if len(values) != 9:
            raise ValueError("each Davis Table 4 row must contain exactly nine F2 values")
        if any(left < right for left, right in zip(values, values[1:])):
            raise ValueError("Davis Table 4 F2 must be nonincreasing with mass ratio")
        rows.append(Table4Row(_positive(source_row["expansion_ratio"], "expansion_ratio"), values))

    expansion_ratios = [row.expansion_ratio for row in rows]
    if expansion_ratios != sorted(expansion_ratios) or len(set(expansion_ratios)) != len(expansion_ratios):
        raise ValueError("Davis Table 4 expansion-ratio rows must be strictly increasing")
    for column_index in range(len(mass_ratios)):
        column = [row.f2_values[column_index] for row in rows]
        if any(lower > upper for lower, upper in zip(column, column[1:])):
            raise ValueError("Davis Table 4 F2 must be nondecreasing with expansion ratio")
    return Table4(mass_ratios=mass_ratios, rows=tuple(rows))


def _bracket(value: float, grid: tuple[float, ...], name: str) -> tuple[int, int, float]:
    if value < grid[0] or value > grid[-1]:
        raise ValueError(f"{name} is outside Davis Table 4")
    for index, grid_value in enumerate(grid):
        if abs(value - grid_value) < 1e-12:
            return index, index, 0.0
        if value < grid_value:
            lower_index = index - 1
            fraction = (value - grid[lower_index]) / (grid_value - grid[lower_index])
            return lower_index, index, fraction
    return len(grid) - 1, len(grid) - 1, 0.0


def pressure_terms(
    charge_weight_grains: float,
    table4_f2: float,
    muzzle_velocity_fps: float,
    bullet_weight_grains: float,
    loaded_capacity_water_grains: float,
    expansion_ratio_value: float,
) -> PressureTerms:
    """Return Davis K1, K2, K3 without changing his printed representation."""
    charge = _positive(charge_weight_grains, "charge_weight_grains")
    f2 = _positive(table4_f2, "table4_f2")
    velocity = _positive(muzzle_velocity_fps, "muzzle_velocity_fps")
    bullet = _positive(bullet_weight_grains, "bullet_weight_grains")
    capacity = _positive(loaded_capacity_water_grains, "loaded_capacity_water_grains")
    ratio = _positive(expansion_ratio_value, "expansion_ratio")
    if ratio <= 1.0:
        raise ValueError("expansion_ratio must be greater than 1")
    return PressureTerms(
        k1=0.0142 * charge * f2 * velocity**2,
        k2=0.53 * (bullet / charge) + 0.26,
        k3=capacity * (ratio - 1.0),
    )


def historical_crusher_pressure(
    charge_weight_grains: float,
    muzzle_velocity_fps: float,
    bullet_weight_grains: float,
    loaded_capacity_water_grains: float,
    expansion_ratio_value: float,
    table4_f2: float | None = None,
) -> float:
    """Davis crusher-gage pressure, preserving his historical ``psi`` semantics."""
    if table4_f2 is None:
        raise MissingProvenanceError(
            "supply a source-backed Davis Table 4 F2 value explicitly"
        )
    terms = pressure_terms(
        charge_weight_grains,
        table4_f2,
        muzzle_velocity_fps,
        bullet_weight_grains,
        loaded_capacity_water_grains,
        expansion_ratio_value,
    )
    return terms.k1 * terms.k2 / terms.k3


def lookup_table4_f2(mass_ratio_value: float, expansion_ratio_value: float) -> float:
    """Lookup Table 4, interpolating without extrapolation.

    Linear interpolation on the R axis is shown by Davis's worked example.
    Linear A-axis and bilinear interpolation are explicit repository
    interpretations because the exact second-axis procedure is not recovered.
    """
    mass_ratio_number = _positive(mass_ratio_value, "mass_ratio")
    ratio = _positive(expansion_ratio_value, "expansion_ratio")
    table = load_table4()
    expansion_ratios = tuple(row.expansion_ratio for row in table.rows)
    a0, a1, a_fraction = _bracket(mass_ratio_number, table.mass_ratios, "mass_ratio")
    r0, r1, r_fraction = _bracket(ratio, expansion_ratios, "expansion_ratio")

    lower_at_a0 = table.rows[r0].f2_values[a0]
    lower_at_a1 = table.rows[r0].f2_values[a1]
    lower = lower_at_a0 + a_fraction * (lower_at_a1 - lower_at_a0)
    if r0 == r1:
        return lower
    upper_at_a0 = table.rows[r1].f2_values[a0]
    upper_at_a1 = table.rows[r1].f2_values[a1]
    upper = upper_at_a0 + a_fraction * (upper_at_a1 - upper_at_a0)
    return lower + r_fraction * (upper - lower)


def loading_density_pressure_scale(
    initial_historical_crusher_pressure: float,
    initial_loading_density: float,
    target_loading_density: float,
) -> float:
    """Davis approximate P2 = P1 (LD2/LD1)^2 rule."""
    pressure = _positive(
        initial_historical_crusher_pressure,
        "initial_historical_crusher_pressure",
    )
    initial_density = _positive(initial_loading_density, "initial_loading_density")
    target_density = _positive(target_loading_density, "target_loading_density")
    return pressure * (target_density / initial_density) ** 2


def charge_for_target_loading_density(
    loaded_capacity_water_grains: float,
    target_loading_density: float,
) -> float:
    """Davis I2 = W2 LD_target."""
    capacity = _positive(loaded_capacity_water_grains, "loaded_capacity_water_grains")
    density = _positive(target_loading_density, "target_loading_density")
    return capacity * density


@dataclass(frozen=True)
class TranscribedBand:
    """Endpoint-preserving secondary transcription of Davis Table 3."""

    lower: float | None
    upper: float | None
    text: str
    lower_inclusive: bool = True
    upper_inclusive: bool = True

    def includes(self, value: float) -> bool:
        lower_ok = self.lower is None or value > self.lower or (self.lower_inclusive and value == self.lower)
        upper_ok = self.upper is None or value < self.upper or (self.upper_inclusive and value == self.upper)
        return lower_ok and upper_ok


# Endpoint overlap is retained because the secondary transcription says "x to
# y" for adjacent rows. Resolving inclusivity requires the Davis page image.
TRANSCRIBED_BANDS = (
    TranscribedBand(None, 81, "much slower than IMR-4831; no suitable IMR canister powder", upper_inclusive=False),
    TranscribedBand(81, 91, "slower than IMR-4831 and IMR-4350; transcription specifies a reduction"),
    TranscribedBand(91, 110, "similar to IMR-4831 and IMR-4350"),
    TranscribedBand(110, 125, "similar to IMR-4064, IMR-4895, and IMR-4320"),
    TranscribedBand(125, 145, "similar to IMR-3031"),
    TranscribedBand(145, 165, "similar to IMR-4198"),
    TranscribedBand(165, 180, "similar to IMR-4227 (secondary transcription contains 4427)"),
    TranscribedBand(180, None, "faster than IMR-4227", lower_inclusive=False),
)


def matching_transcribed_bands(index: float) -> tuple[TranscribedBand, ...]:
    """Return every secondary Table 3 band matching an unresolved endpoint."""
    value = _positive(index, "index")
    return tuple(band for band in TRANSCRIBED_BANDS if band.includes(value))
