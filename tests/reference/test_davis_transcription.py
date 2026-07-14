import pytest

from modern_powley.later.davis import (
    DAVIS_RELATIVE_QUICKNESS,
    boat_tail_correction_water_grains,
    bullet_travel_inches,
    effective_bore_volume_cubic_inches,
    effective_moving_weight_grains,
    expansion_ratio,
    flat_base_displacement_water_grains,
    historical_crusher_pressure,
    initial_charge_weight_grains,
    loaded_powder_space_capacity_water_grains,
    load_table4,
    lookup_table4_f2,
    mass_ratio,
    matching_transcribed_bands,
    muzzle_velocity_fps,
    powder_chamber_volume_cubic_inches,
    powder_selection_index,
    pressure_terms,
    seating_depth_inches,
    sectional_density,
    velocity_fraction_m,
    velocity_fraction_n,
)


def test_davis_relative_quickness_table_is_transcribed_as_arbitrary_values():
    assert DAVIS_RELATIVE_QUICKNESS == {
        "IMR 4227": 180,
        "IMR 4198": 160,
        "IMR 3031": 135,
        "IMR 4064": 120,
        "IMR 4895": 115,
        "IMR 4320": 110,
        "IMR 4350": 100,
        "IMR 4831": 95,
    }


def test_davis_30_06_worked_example_reproduces_published_rounding_sequence():
    seating_depth = seating_depth_inches(2.484, 1.220, 3.30)
    flat_displacement = flat_base_displacement_water_grains(seating_depth, 0.308)
    boat_tail_correction = boat_tail_correction_water_grains(0.150, 0.308, 0.200, seating_depth)
    capacity = loaded_powder_space_capacity_water_grains(69, flat_displacement, boat_tail_correction)
    travel = bullet_travel_inches(24, seating_depth, 2.484)
    chamber_volume = powder_chamber_volume_cubic_inches(capacity)
    bore_volume = effective_bore_volume_cubic_inches(travel, 0.308)
    ratio = expansion_ratio(bore_volume, chamber_volume)
    charge = initial_charge_weight_grains(capacity, "IMR 4350")
    charge_to_bullet_ratio = mass_ratio(charge, 180)
    sd = sectional_density(180, 0.308)
    index = powder_selection_index(sd, charge_to_bullet_ratio)
    m_value = velocity_fraction_m(ratio)
    n_value = velocity_fraction_n(m_value)
    moving_weight = effective_moving_weight_grains(180, charge)
    velocity = muzzle_velocity_fps(charge, n_value, moving_weight)

    assert seating_depth == pytest.approx(0.404, abs=0.0005)
    assert flat_displacement == pytest.approx(7.59, abs=0.02)
    assert boat_tail_correction == pytest.approx(0.87, abs=0.02)
    assert capacity == pytest.approx(62.3, abs=0.1)
    assert travel == pytest.approx(21.9, abs=0.05)
    assert chamber_volume == pytest.approx(0.247, abs=0.001)
    assert bore_volume == pytest.approx(1.606, abs=0.003)
    assert ratio == pytest.approx(7.50, abs=0.03)
    assert charge == pytest.approx(53.6, abs=0.1)
    assert charge_to_bullet_ratio == pytest.approx(0.298, abs=0.001)
    assert sd == pytest.approx(0.271, abs=0.001)
    assert index == pytest.approx(101, abs=1)
    assert m_value == pytest.approx(0.604, abs=0.002)
    assert n_value == pytest.approx(0.396, abs=0.002)
    assert moving_weight == pytest.approx(197.9, abs=0.1)
    assert velocity == pytest.approx(2620, abs=10)


def test_davis_pressure_example_uses_published_rounded_inputs():
    assert lookup_table4_f2(0.30, 7.5) == pytest.approx(1.74)
    terms = pressure_terms(
        charge_weight_grains=53.6,
        table4_f2=1.74,
        muzzle_velocity_fps=2620,
        bullet_weight_grains=180,
        loaded_capacity_water_grains=62.3,
        expansion_ratio_value=7.50,
    )
    pressure = historical_crusher_pressure(
        charge_weight_grains=53.6,
        muzzle_velocity_fps=2620,
        bullet_weight_grains=180,
        loaded_capacity_water_grains=62.3,
        expansion_ratio_value=7.50,
        table4_f2=1.74,
    )

    assert terms.k1 == pytest.approx(9_090_854, rel=0.002)
    assert terms.k2 == pytest.approx(2.040, abs=0.002)
    assert terms.k3 == pytest.approx(405, abs=1)
    assert pressure == pytest.approx(45_790, rel=0.01)


def test_davis_table4_shape_and_monotonic_invariants():
    table = load_table4()
    assert table.mass_ratios == pytest.approx((0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00))
    assert len(table.rows) == 34
    assert all(len(row.f2_values) == 9 for row in table.rows)
    assert all(value > 0 for row in table.rows for value in row.f2_values)
    for column_index in range(9):
        column = [row.f2_values[column_index] for row in table.rows]
        assert column == sorted(column)
    for row in table.rows:
        assert list(row.f2_values) == sorted(row.f2_values, reverse=True)


def test_transcribed_table3_endpoints_remain_explicitly_overlapping():
    assert len(matching_transcribed_bands(81)) == 1
    assert len(matching_transcribed_bands(91)) == 2
    assert len(matching_transcribed_bands(110)) == 2
    assert len(matching_transcribed_bands(180)) == 1
    assert len(matching_transcribed_bands(180.01)) == 1
