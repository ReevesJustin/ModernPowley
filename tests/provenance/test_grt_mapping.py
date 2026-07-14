from pathlib import Path
import xml.etree.ElementTree as ET


def test_aeff_is_area_and_not_effective_case_volume():
    root = ET.parse(Path("data/GRT_Files/65CM_140ELDM_RL16_44F.grtload")).getroot()
    field = root.find('.//caliber/input[@name="Aeff"]')
    assert field is not None
    assert field.get("unit") == "mm2"
    assert field.get("descr") == "effektive area"


def test_dimensional_defect_is_preserved_by_tag_and_repaired_in_worktree():
    legacy = Path("scripts/parse_grt_cartridge.py").read_text()
    canonical = "\n".join(path.read_text() for path in Path("src/modern_powley").rglob("*.py"))
    assert "'Aeff': 'effective_area_mm2'" in legacy
    assert "'Aeff': 'eff_case_vol'" not in legacy
    assert "Aeff" not in canonical
