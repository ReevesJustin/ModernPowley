import csv
import hashlib
from pathlib import Path


ROOT = Path("reference/davis_1981")
OCR = ROOT / "davis_1981_pages_138_144_raw_ocr.txt"
REPRINT = ROOT / "derivative_partial_reprint.pdf"
MANIFEST = ROOT / "SHA256SUMS.txt"
REPORT = Path("docs/audits/davis_1981_evidence_intake.md")


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sources() -> dict[str, dict[str, str]]:
    with Path("reference/source_ledger.csv").open(newline="", encoding="utf-8") as handle:
        return {row["source_id"]: row for row in csv.DictReader(handle)}


def test_intake_manifest_matches_all_supplied_package_files():
    entries = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        digest, name = line.split(maxsplit=1)
        entries[name] = digest

    assert entries == {
        "README.txt": "f149ef602b6fdb9a4d2bd6dd1240a3e8e24bdc33fc7e60a06157afe4edde9754",
        "davis_1981_pages_138_144_raw_ocr.txt": (
            "ef8c4335e58259d6b22084e7ece946330f96aa4d873da61c9f67616dce591511"
        ),
        "derivative_partial_reprint.pdf": (
            "578227dd703820f4703b5384dfcb404302685741e0343dc2c4d6bff3960f6bc4"
        ),
    }
    for name, expected in entries.items():
        assert _digest(ROOT / name) == expected


def test_raw_ocr_is_ledgered_as_uncorrected_noncanonical_derivative():
    row = _sources()["SRC-DAVIS-1981-RAW-OCR"]
    assert row["source_type"] == "user-supplied raw OCR derivative"
    assert row["primary_or_secondary"] == "secondary derivative"
    assert row["verification_status"] == "ocr_only"
    assert row["confidence"] == "low"
    assert "Intentionally uncorrected" in row["notes"]
    assert "noncanonical" in row["notes"]

    text = OCR.read_text(encoding="utf-8")
    for page in range(138, 145):
        assert f"PAGE {page}" in text
    assert "TABLE 4 RAW OCR" in text
    assert "has not been visually reconciled" in text


def test_partial_reprint_is_secondary_and_not_primary_error_evidence():
    row = _sources()["SRC-DAVIS-1981-DERIVATIVE-REPRINT"]
    assert row["source_type"] == "derivative partial reprint"
    assert row["primary_or_secondary"] == "secondary derivative"
    assert row["verification_status"] == "verified_secondary"
    assert "Not a facsimile" in row["notes"]
    assert "derivative inconsistencies" in row["notes"]
    assert "not established primary-publication errors" in row["notes"]
    assert REPRINT.read_bytes().startswith(b"%PDF-1.4")


def test_intake_does_not_promote_table4_or_equation_typography():
    sources = _sources()
    table = sources["SRC-DAVIS-1981-TABLE4"]
    transcription = sources["SRC-DAVIS-1981-TRANSCRIPTION"]
    assert table["verification_status"] == "pending_retained_primary_visual_verification"
    assert table["confidence"] == "medium"
    assert transcription["verification_status"] == "normalized_user_transcription"
    assert transcription["confidence"] == "medium"

    report = REPORT.read_text(encoding="utf-8")
    normalized_report = " ".join(report.split())
    assert "cannot verify equation typography" in normalized_report
    assert "not errors attributable to Davis's primary publication" in normalized_report
    assert "Primary visual reconciliation remains blocked" in normalized_report


def test_original_namespace_and_davis_runtime_are_not_changed_by_intake():
    report = REPORT.read_text(encoding="utf-8")
    assert "No scientific implementation changed" in report
    for path in Path("src/modern_powley/original").glob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "SRC-DAVIS-1981-RAW-OCR" not in text
        assert "derivative_partial_reprint" not in text
    davis = Path("src/modern_powley/later/davis.py").read_text(encoding="utf-8")
    assert "pending_retained_primary_visual_verification" in davis
    assert "SRC-DAVIS-1981-RAW-OCR" not in davis
