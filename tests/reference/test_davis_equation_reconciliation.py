from decimal import Decimal, getcontext

import pytest

from modern_powley.later import davis


getcontext().prec = 40
D = Decimal


def _independent_30_06() -> dict[str, Decimal]:
    case_length = D("2.484")
    full_capacity = D("69")
    bullet_length = D("1.220")
    tail_height = D("0.150")
    tail_diameter = D("0.200")
    bullet_diameter = D("0.308")
    bullet_weight = D("180")
    overall_length = D("3.30")
    barrel_length = D("24")

    seating = case_length + bullet_length - overall_length
    displacement = D("198") * seating * bullet_diameter**2
    tail_correction = D("66") * tail_height * (
        D("2") * bullet_diameter**2
        - bullet_diameter * tail_diameter
        - tail_diameter**2
    )
    capacity = full_capacity - displacement + tail_correction
    travel = barrel_length + seating - case_length
    chamber_volume = capacity / D("252.4")
    bore_volume = D("0.773") * travel * bullet_diameter**2
    expansion = (bore_volume + chamber_volume) / chamber_volume
    charge = D("0.86") * capacity
    mass_ratio = charge / bullet_weight
    sectional_density = bullet_weight / (D("7000") * bullet_diameter**2)
    powder_index = D("20") + D("12") / (sectional_density * mass_ratio.sqrt())
    m_value = D("1") / expansion.sqrt().sqrt()
    n_value = D("1") - m_value
    moving_weight = bullet_weight + charge / D("3")
    velocity = D("8000") * (charge * n_value / moving_weight).sqrt()
    return {
        "S": seating,
        "P": displacement,
        "K": tail_correction,
        "W": capacity,
        "T": travel,
        "U": chamber_volume,
        "Q": bore_volume,
        "R": expansion,
        "I": charge,
        "A": mass_ratio,
        "Z": sectional_density,
        "X": powder_index,
        "M": m_value,
        "N": n_value,
        "Y": moving_weight,
        "V": velocity,
    }


def _independent_22_250_capacity() -> dict[str, Decimal]:
    full_capacity = D("44.6")
    diameter = D("0.224")
    flat_seating = D("1.911") + D("0.708") - D("2.415")
    flat_displacement = D("198") * flat_seating * diameter**2
    boat_seating = D("1.911") + D("0.720") - D("2.415")
    boat_displacement = D("198") * boat_seating * diameter**2
    correction = D("66") * D("0.081") * (
        D("2") * diameter**2 - diameter * D("0.202") - D("0.202")**2
    )
    return {
        "flat_S": flat_seating,
        "flat_P": flat_displacement,
        "flat_W": full_capacity - flat_displacement,
        "boat_S": boat_seating,
        "boat_P": boat_displacement,
        "boat_K": correction,
        "boat_W": full_capacity - boat_displacement + correction,
    }


def test_independent_30_06_full_precision_chain_matches_implementation():
    expected = _independent_30_06()
    seating = davis.seating_depth_inches(2.484, 1.220, 3.30)
    displacement = davis.flat_base_displacement_water_grains(seating, 0.308)
    correction = davis.boat_tail_correction_water_grains(0.150, 0.308, 0.200, seating)
    capacity = davis.loaded_powder_space_capacity_water_grains(69, displacement, correction)
    travel = davis.bullet_travel_inches(24, seating, 2.484)
    chamber = davis.powder_chamber_volume_cubic_inches(capacity)
    bore = davis.effective_bore_volume_cubic_inches(travel, 0.308)
    expansion = davis.expansion_ratio(bore, chamber)
    charge = davis.initial_charge_weight_grains(capacity, "IMR 4350")
    ratio = davis.mass_ratio(charge, 180)
    sd = davis.sectional_density(180, 0.308)
    index = davis.powder_selection_index(sd, ratio)
    m_value = davis.velocity_fraction_m(expansion)
    n_value = davis.velocity_fraction_n(m_value)
    moving = davis.effective_moving_weight_grains(180, charge)
    velocity = davis.muzzle_velocity_fps(charge, n_value, moving)

    actual = (seating, displacement, correction, capacity, travel, chamber, bore,
              expansion, charge, ratio, sd, index, m_value, n_value, moving, velocity)
    for key, value in zip(expected, actual, strict=True):
        assert value == pytest.approx(float(expected[key]), rel=1e-13)

    assert float(expected["V"]) == pytest.approx(2619.409657819862)


def test_30_06_rounded_pressure_sequence_is_recalculated_independently():
    charge = D("53.6")
    f2 = D("1.74")
    velocity = D("2620")
    bullet = D("180")
    capacity = D("62.3")
    expansion = D("7.5")
    k1 = D("0.0142") * charge * f2 * velocity**2
    k2 = D("0.53") * (bullet / charge) + D("0.26")
    k3 = capacity * (expansion - D("1"))
    pressure = k1 * k2 / k3

    terms = davis.pressure_terms(53.6, 1.74, 2620, 180, 62.3, 7.5)
    implementation = davis.historical_crusher_pressure(53.6, 2620, 180, 62.3, 7.5, 1.74)
    assert terms.k1 == pytest.approx(float(k1))
    assert terms.k2 == pytest.approx(float(k2))
    assert terms.k3 == pytest.approx(float(k3))
    assert implementation == pytest.approx(float(pressure))
    assert float(pressure) == pytest.approx(45_793.30128852253)


def test_derivative_22_250_capacity_discontinuity_is_not_adopted():
    expected = _independent_22_250_capacity()
    assert expected == {
        "flat_S": D("0.204"),
        "flat_P": D("2.026708992"),
        "flat_W": D("42.573291008"),
        "boat_S": D("0.216"),
        "boat_P": D("2.145927168"),
        "boat_K": D("0.076447800"),
        "boat_W": D("42.530520632"),
    }
    implementation = davis.loaded_powder_space_capacity_water_grains(
        44.6,
        davis.flat_base_displacement_water_grains(0.216, 0.224),
        davis.boat_tail_correction_water_grains(0.081, 0.224, 0.202, 0.216),
    )
    assert implementation == pytest.approx(float(expected["boat_W"]))
    assert expected["boat_W"] - D("42.377625032") == D("0.152895600")


def test_derivative_22_250_literal_pressure_chain_recalculates_but_remains_secondary():
    charge = D("36.44475752752")
    capacity = D("42.377625032")
    bullet = D("55")
    expansion = D("6.17436305069916")
    velocity = D("3670")
    f2 = D("1.432")
    k1 = D("0.0142") * charge * f2 * velocity**2
    k2 = D("0.53") * (bullet / charge) + D("0.26")
    k3 = capacity * (expansion - D("1"))
    pressure = k1 * k2 / k3

    implementation = davis.historical_crusher_pressure(
        float(charge), float(velocity), float(bullet), float(capacity),
        float(expansion), float(f2),
    )
    assert implementation == pytest.approx(float(pressure))
    assert float(pressure) == pytest.approx(48_244.25831905143)


def test_derivative_loading_density_example_recalculates_independently():
    commercial = D("57.5") / D("65.3")
    military = D("57.5") / D("62.0")
    scaled_pressure = D("50000") * (military / commercial) ** 2
    same_density_charge = commercial * D("62.0")
    assert davis.loading_density_pressure_scale(50_000, float(commercial), float(military)) == pytest.approx(
        float(scaled_pressure)
    )
    assert davis.charge_for_target_loading_density(62.0, float(commercial)) == pytest.approx(
        float(same_density_charge)
    )
    assert float(scaled_pressure) == pytest.approx(55_464.22996878252)
    assert float(same_density_charge) == pytest.approx(54.59418070444104)


def test_every_candidate_table4_node_is_recovered_exactly_without_extrapolation():
    table = davis.load_table4()
    for row in table.rows:
        for mass_ratio, expected in zip(table.mass_ratios, row.f2_values, strict=True):
            assert davis.lookup_table4_f2(mass_ratio, row.expansion_ratio) == expected


def test_candidate_table4_derivative_example_interpolation_is_not_promoted():
    interpolated = davis.lookup_table4_f2(36.4 / 55, 6.17436305069916)
    assert interpolated == pytest.approx(1.4325089737761965)
    assert interpolated != pytest.approx(1.432, abs=1e-6)
    assert davis.load_table4().verification_status == (
        "pending_retained_primary_visual_verification"
    )


def test_velocity_allows_zero_n_as_zero_velocity():
    assert davis.muzzle_velocity_fps(53.6, 0.0, 197.9) == 0.0


@pytest.mark.parametrize("n_value", [-0.01, float("-inf"), float("inf"), float("nan")])
def test_velocity_rejects_negative_or_nonfinite_n(n_value):
    with pytest.raises(ValueError):
        davis.muzzle_velocity_fps(53.6, n_value, 197.9)


@pytest.mark.parametrize("n_value", [1.0, 1.01])
def test_velocity_rejects_n_at_or_above_one(n_value):
    with pytest.raises(ValueError, match="velocity_fraction_n must be less than 1"):
        davis.muzzle_velocity_fps(53.6, n_value, 197.9)


def test_table3_secondary_label_uses_4227_without_claiming_endpoint_resolution():
    matches = davis.matching_transcribed_bands(170)
    assert len(matches) == 1
    assert matches[0].text == "similar to IMR-4227"
    assert len(davis.matching_transcribed_bands(165)) == 2
