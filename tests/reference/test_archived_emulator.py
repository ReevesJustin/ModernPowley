import csv
import math
from pathlib import Path

import pytest

from modern_powley.later.emulator import (
    POWDER_BANDS,
    approximate_bore_area_square_inches,
    bullet_travel_inches,
    cup_to_claimed_psi,
    efficiency_percent,
    estimated_round_nose_bullet_length_inches,
    estimated_spitzer_bullet_length_inches,
    javascript_round_to_increment,
    kinetic_energy_foot_pounds,
    load_from_net_capacity,
    miller_f2,
    net_capacity_from_gross,
    powder_index,
    pressure_cup,
    seating_depth_inches,
    select_powder_band,
    total_expansion_ratio_from_geometry,
    velocity_fps,
    velocity_for_target_cup,
)


def test_emulator_transcription_is_anchored_to_archived_source_literals():
    source = Path("reference/online_emulator/kwk_powley_20240228.html").read_text(encoding="ascii")
    required_literals = (
        "Z = ( G / 7000 ) / sqr( D )",
        "P = 198 * S * sqr( D )",
        "area = 0.773 * sqr( D )",
        "X = 20 + ( 12 / ( Z * Math.sqrt( A ) ) )",
        "V = 8000 * Math.sqrt( I * N / Y )",
        "return  0.024075 * ( 9.3 - A ) * ( 1.071 + R - 0.009736 * sqr( R ) )",
        "CUP = 134.7 * sqr( V / 100 )  *  LD / ( R - 1 )  * K2 * F2",
        "if ( X < 81 )",
        "else if ( X <= 180 )",
    )
    for literal in required_literals:
        assert literal in source


@pytest.mark.parametrize("transition", [81.0, 91.0, 110.0, 125.0, 145.0, 165.0, 180.0])
def test_emulator_boundaries_are_total_and_nonoverlapping(transition):
    for value in (math.nextafter(transition, -math.inf), transition, math.nextafter(transition, math.inf)):
        assert sum(band.includes(value) for band in POWDER_BANDS) == 1


def test_emulator_boundary_designations_match_javascript_branches():
    assert select_powder_band(91).instruction == "Slower than 4831"
    assert select_powder_band(math.nextafter(91, math.inf)).designation == "4831;4350"
    assert select_powder_band(110).designation == "4831;4350"
    assert select_powder_band(math.nextafter(110, math.inf)).designation == "4320;4895;4064"
    assert select_powder_band(180).designation == "4227"
    assert select_powder_band(math.nextafter(180, math.inf)).instruction == "Faster than 4227"


def test_committed_emulator_scale_matches_code():
    rows = list(
        csv.DictReader(
            Path("data/reference/original_powley_powder_scale.csv").open(newline="", encoding="utf-8")
        )
    )
    assert len(rows) == len(POWDER_BANDS)
    for row, band in zip(rows, POWDER_BANDS, strict=True):
        assert (float(row["lower_bound"]) if row["lower_bound"] else None) == band.lower
        assert (row["lower_inclusive"] == "true") == band.lower_inclusive
        assert (float(row["upper_bound"]) if row["upper_bound"] else None) == band.upper
        assert (row["upper_inclusive"] == "true") == band.upper_inclusive
        assert row["powder_designation"] == band.designation
        assert row["instruction"] == band.instruction
        assert row["attribution_class"] == "online_emulator"


def test_emulator_geometry_constant_is_not_promoted_to_original():
    assert net_capacity_from_gross(51.5, 0.5, 0.308) == pytest.approx(51.5 - 198 * 0.5 * 0.308**2)


def test_emulator_geometry_chain_matches_javascript_example_one():
    sd = 150 / 7000 / 0.308**2
    assert estimated_spitzer_bullet_length_inches(sd) == pytest.approx(0.20 + 3.67 * sd)
    assert estimated_round_nose_bullet_length_inches(sd) == pytest.approx(0.08 + 3.67 * sd)
    depth = seating_depth_inches(2.49, 1.07, 3.20)
    net = net_capacity_from_gross(69, depth, 0.308)
    travel = bullet_travel_inches(24, 2.49, depth)
    assert approximate_bore_area_square_inches(0.308) == pytest.approx(0.773 * 0.308**2)
    assert total_expansion_ratio_from_geometry(net, 0.308, travel) == pytest.approx(7.503734079023006)


def test_emulator_load_preserves_non_recomputed_index_behavior():
    result = load_from_net_capacity(20, 100, 0.308)
    assert result.powder_index > 145
    assert result.charge_weight_grains == 16
    assert result.mass_ratio == 0.16
    assert result.powder_index == powder_index(100 / 7000 / 0.308**2, 0.172)


def test_emulator_rounding_energy_and_pressure_inverse():
    assert javascript_round_to_increment(44.25, 0.1) == pytest.approx(44.3)
    energy = kinetic_energy_foot_pounds(150, 2730)
    assert efficiency_percent(150, 2730, 44.3) == pytest.approx(100 * energy / (44.3 * 185))
    cup = pressure_cup(2730, 0.86, 9.0, 0.295)
    assert velocity_for_target_cup(cup, 9.0, 0.295) == pytest.approx(2730)


def test_manual_worked_values_through_emulator_equations_are_only_a_comparison():
    index = powder_index(0.227, 0.295)
    assert select_powder_band(index).designation == "4320;4895;4064"
    assert velocity_fps(44.3, 150, 9.0) == pytest.approx(2696.7921204662666)


def test_emulator_pressure_chain_matches_archived_javascript_arithmetic():
    f2 = miller_f2(0.295, 9.0)
    cup = pressure_cup(2730, 0.86, 9.0, 0.295)
    assert f2 == pytest.approx(2.0123779201740004)
    assert cup == pytest.approx(44664.541138433924)
    assert cup_to_claimed_psi(cup) == pytest.approx(50984.292019723696)
