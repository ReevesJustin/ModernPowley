import csv
import hashlib
import json
from pathlib import Path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_legacy_artifact_registry_hashes_match_files():
    manifest = Path("docs/provenance/legacy_artifact_manifest.csv")
    for row in csv.DictReader(manifest.open(newline="", encoding="utf-8")):
        assert row["output_hash"].startswith("sha256:")
        assert digest(Path(row["output_path"])) == row["output_hash"].removeprefix("sha256:")


def test_inventory_manifest_output_hashes_match():
    manifest = json.loads(Path("docs/audits/inventory_generation_manifest.json").read_text())
    for output in manifest["outputs"]:
        assert digest(Path(output["path"])) == output["sha256"]


def test_local_artifact_hashes_match_source_ledger():
    sources = {
        row["source_id"]: row
        for row in csv.DictReader(Path("reference/source_ledger.csv").open(newline="", encoding="utf-8"))
    }
    assert digest(Path("data/GRT_Files/65CM_140ELDM_RL16_44F.grtload")) == sources[
        "SRC-GRT-LOAD-001"
    ]["artifact_hash"].removeprefix("sha256:")
    assert digest(Path("image/classiccardboard_3.jpg")) == sources["SRC-POWLEY-SLIDE-PHOTO"][
        "artifact_hash"
    ].removeprefix("sha256:")
    assert digest(Path("reference/powley_scales/ssusa_powley_computers_1985.jpg")) == sources[
        "SRC-POWLEY-SLIDE-PHOTO-HQ"
    ]["artifact_hash"].removeprefix("sha256:")
    assert digest(Path("data/reference/original_powley_velocity_observations.csv")) == sources[
        "SRC-POWLEY-VELOCITY-OBSERVATIONS"
    ]["artifact_hash"].removeprefix("sha256:")
    assert digest(Path("reference/powley_manual/powleysmanuals1.md")) == sources[
        "SRC-POWLEY-1961-MANUAL-TRANSCRIPTION"
    ]["artifact_hash"].removeprefix("sha256:")
    assert digest(Path("reference/powley_manual/powleysmanuals1.pdf")) == sources[
        "SRC-POWLEY-1961-MANUAL"
    ]["artifact_hash"].removeprefix("sha256:")
    assert digest(Path("reference/online_emulator/kwk_powley_20240228.html")) == sources[
        "SRC-KWK-EMULATOR"
    ]["artifact_hash"].removeprefix("sha256:")
    assert digest(Path("reference/davis_1981/davis_equation_transcription.md")) == sources[
        "SRC-DAVIS-1981-TRANSCRIPTION"
    ]["artifact_hash"].removeprefix("sha256:")
    assert digest(Path("data/reference/davis_1981_table4.csv")) == sources[
        "SRC-DAVIS-1981-TABLE4"
    ]["artifact_hash"].removeprefix("sha256:")
    assert digest(Path("reference/davis_1981/table4_correction_ledger.csv")) == sources[
        "SRC-DAVIS-1981-TABLE4-CORRECTIONS"
    ]["artifact_hash"].removeprefix("sha256:")
