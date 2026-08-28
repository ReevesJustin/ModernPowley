"""Regression coverage for the generate_audit_inventory.py overwrite guard.

docs/provenance/data_field_ledger.csv and docs/audits/pre_audit_file_inventory.csv
were hand-extended beyond what scripts/generate_audit_inventory.py's own
checkpoint-era logic reproduces (eight-column maintained ledger schema versus
the script's seven-column output; see the module docstring). Running the
script unguarded silently overwrote that maintained content. These tests
prove the guard refuses before writing anything, using the real committed
files -- the divergence they exercise is the repository's actual current
state, not a synthetic fixture.
"""

import json
from pathlib import Path

import pytest

from scripts.generate_audit_inventory import (
    FIELD_LEDGER_PATH,
    INVENTORY_PATH,
    MANIFEST_PATH,
    csv_overwrite_conflict,
    main,
    manifest_overwrite_conflict,
)

PROTECTED_PATHS = [INVENTORY_PATH, FIELD_LEDGER_PATH, MANIFEST_PATH]


def test_main_refuses_and_leaves_all_protected_outputs_byte_identical():
    before = {path: path.read_bytes() for path in PROTECTED_PATHS}

    with pytest.raises(SystemExit):
        main()

    after = {path: path.read_bytes() for path in PROTECTED_PATHS}
    for path in PROTECTED_PATHS:
        assert after[path] == before[path], f"{path} changed despite refusal"


def test_field_ledger_conflict_is_the_hand_maintained_eight_column_schema():
    message = csv_overwrite_conflict(
        FIELD_LEDGER_PATH, b"data_asset,field\nonly,two-columns\n"
    )
    assert message is not None
    assert "hand-maintained" in message


def test_manifest_conflict_names_the_dropped_post_generation_updates_field():
    message = manifest_overwrite_conflict(MANIFEST_PATH)
    assert message is not None
    assert "post_generation_updates" in message


def test_manifest_committed_json_actually_carries_the_extra_field():
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    assert "post_generation_updates" in manifest


def test_csv_overwrite_conflict_is_none_for_matching_or_absent_content(tmp_path: Path):
    target = tmp_path / "does_not_exist.csv"
    assert csv_overwrite_conflict(target, b"anything") is None

    target.write_bytes(b"same-bytes")
    assert csv_overwrite_conflict(target, b"same-bytes") is None
    assert csv_overwrite_conflict(target, b"different-bytes") is not None


def test_manifest_overwrite_conflict_is_none_for_schema_only_manifest(tmp_path: Path):
    target = tmp_path / "does_not_exist.json"
    assert manifest_overwrite_conflict(target) is None

    target.write_text(json.dumps({"checkpoint_commit": "abc", "timestamp": "t"}))
    assert manifest_overwrite_conflict(target) is None

    target.write_text(json.dumps({"checkpoint_commit": "abc", "extra_hand_field": "kept"}))
    message = manifest_overwrite_conflict(target)
    assert message is not None
    assert "extra_hand_field" in message


def test_manifest_overwrite_conflict_refuses_on_invalid_json(tmp_path: Path):
    target = tmp_path / "broken.json"
    target.write_text("not json")
    message = manifest_overwrite_conflict(target)
    assert message is not None
    assert "not valid JSON" in message
