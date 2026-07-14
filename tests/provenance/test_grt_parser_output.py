from pathlib import Path

from scripts.parse_grt_cartridge import parse_grt_cartridge
from scripts.parse_grt_prop import parse_grt_file

GRT_LOAD = Path("data/GRT_Files/65CM_140ELDM_RL16_44F.grtload")


def test_repaired_cartridge_parser_keeps_area_dimensionality():
    result = parse_grt_cartridge(GRT_LOAD)
    assert result["effective_area_mm2"] == 34.645092
    assert result["case_volume_cm3"] == 3.405544569646086
    assert result["groove_diameter_mm"] == 6.7056
    assert result["bullet_mass_g"] == 9.07184739996557
    assert result["propellant_mass_g"] == 2.721554219989671
    assert "eff_case_vol" not in result
    assert "case_vol" not in result


def test_propellant_parser_uses_explicit_inputs_not_caliberfile_name_guesses():
    result = parse_grt_file(GRT_LOAD)
    assert result["Ba"] == 0.468557
    assert result["a0"] == 1.7895
    assert result["z1"] == 0.4777
    assert result["z2"] == 0.8033
    assert result["Qex"] == 3860.0
    assert result["k"] == 1.2360609
    assert result["pcd"] == 903.0
    assert "bulk_density" not in result
