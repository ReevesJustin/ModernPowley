"""Regression coverage for the generate_audit_inventory.py overwrite guard.

docs/provenance/data_field_ledger.csv and docs/audits/pre_audit_file_inventory.csv
were hand-extended beyond what scripts/generate_audit_inventory.py's own
checkpoint-era logic reproduces (eight-column maintained ledger schema versus
the script's seven-column output; see the module docstring). Running the
script unguarded silently overwrote that maintained content. These tests
prove the guard refuses before writing anything, using the real committed
files -- the divergence they exercise is the repository's actual current
state, not a synthetic fixture.

`test_main_refuses_and_leaves_all_protected_outputs_byte_identical` needs the
fixed pre-audit checkpoint commit reachable via `git show`/`git ls-tree`; a
shallow clone (CI's default `actions/checkout` behavior, or a contributor's
`git clone --depth 1`) does not have it. That is an environment gap, not a
guard failure, so the test skips with an explicit reason rather than either
failing on an unrelated `CalledProcessError` or -- worse -- appearing to pass
for the wrong reason. Every other test in this file is a pure logic test
against `tmp_path` fixtures and does not depend on repository history at all.
"""

import json
import subprocess
from pathlib import Path

import pytest

import scripts.generate_audit_inventory as generate_audit_inventory_module
from scripts.generate_audit_inventory import (
    COMMIT,
    FIELD_LEDGER_PATH,
    INVENTORY_PATH,
    MANIFEST_PATH,
    build_manifest,
    csv_overwrite_conflict,
    main,
    manifest_overwrite_conflict,
)

PROTECTED_PATHS = [INVENTORY_PATH, FIELD_LEDGER_PATH, MANIFEST_PATH]


def _checkpoint_commit_available() -> bool:
    try:
        subprocess.run(
            ["git", "cat-file", "-e", f"{COMMIT}^{{commit}}"],
            check=True,
            capture_output=True,
        )
        return True
    except subprocess.CalledProcessError:
        return False


requires_checkpoint_history = pytest.mark.skipif(
    not _checkpoint_commit_available(),
    reason=(
        f"pre-audit checkpoint commit {COMMIT} is not reachable in this "
        "clone (shallow checkout?); this is an environment gap, not a "
        "guard failure -- see the module docstring"
    ),
)


@requires_checkpoint_history
def test_main_refuses_and_leaves_all_protected_outputs_byte_identical():
    before = {path: path.read_bytes() for path in PROTECTED_PATHS}

    with pytest.raises(SystemExit):
        main()

    after = {path: path.read_bytes() for path in PROTECTED_PATHS}
    for path in PROTECTED_PATHS:
        assert after[path] == before[path], f"{path} changed despite refusal"


@requires_checkpoint_history
def test_main_writes_nothing_if_building_a_later_candidate_fails(monkeypatch):
    """A failure while building the manifest must not leave the two CSVs
    already written -- main() must build every candidate before writing any
    of them."""
    before = {path: path.read_bytes() for path in PROTECTED_PATHS}

    def _boom(*_args, **_kwargs):
        raise RuntimeError("injected manifest-construction failure")

    monkeypatch.setattr(generate_audit_inventory_module, "build_manifest", _boom)

    with pytest.raises(RuntimeError, match="injected manifest-construction failure"):
        main()

    after = {path: path.read_bytes() for path in PROTECTED_PATHS}
    for path in PROTECTED_PATHS:
        assert after[path] == before[path], f"{path} was written before the failure"


def test_field_ledger_conflict_is_the_hand_maintained_eight_column_schema():
    message = csv_overwrite_conflict(
        FIELD_LEDGER_PATH, b"data_asset,field\nonly,two-columns\n"
    )
    assert message is not None
    assert "hand-maintained" in message


def test_manifest_conflict_names_the_dropped_post_generation_updates_field():
    candidate = {"checkpoint_commit": "irrelevant-for-this-check"}
    message = manifest_overwrite_conflict(MANIFEST_PATH, candidate)
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


def test_manifest_overwrite_conflict_is_none_for_matching_schema_only_manifest(
    tmp_path: Path,
):
    target = tmp_path / "does_not_exist.json"
    candidate = {"checkpoint_commit": "abc", "timestamp": "candidate-time"}
    assert manifest_overwrite_conflict(target, candidate) is None

    target.write_text(json.dumps({"checkpoint_commit": "abc", "timestamp": "existing-time"}))
    assert manifest_overwrite_conflict(target, candidate) is None

    target.write_text(json.dumps({"checkpoint_commit": "abc", "extra_hand_field": "kept"}))
    message = manifest_overwrite_conflict(target, candidate)
    assert message is not None
    assert "extra_hand_field" in message


def test_manifest_overwrite_conflict_catches_a_changed_known_top_level_value(
    tmp_path: Path,
):
    """A prior gap: the guard only checked for *unknown* top-level keys and
    would silently accept a changed value on a *known* key."""
    target = tmp_path / "manifest.json"
    target.write_text(json.dumps({"checkpoint_commit": "original-commit", "timestamp": "t1"}))

    candidate = {"checkpoint_commit": "different-commit", "timestamp": "t2"}
    message = manifest_overwrite_conflict(target, candidate)
    assert message is not None
    assert "field(s) ['checkpoint_commit']" in message


def test_manifest_overwrite_conflict_catches_changed_nested_content(tmp_path: Path):
    """A prior gap: nested structures (for example `outputs`, a list of
    dicts) were never compared, only top-level key presence."""
    target = tmp_path / "manifest.json"
    existing_outputs = [{"path": "a.csv", "sha256": "aaa"}]
    target.write_text(json.dumps({"outputs": existing_outputs, "timestamp": "t1"}))

    candidate = {"outputs": [{"path": "a.csv", "sha256": "different-hash"}], "timestamp": "t2"}
    message = manifest_overwrite_conflict(target, candidate)
    assert message is not None
    assert "outputs" in message


def test_manifest_overwrite_conflict_treats_only_timestamp_as_volatile(tmp_path: Path):
    target = tmp_path / "manifest.json"
    target.write_text(
        json.dumps({"checkpoint_commit": "same", "environment": {"python": "3.14.0"}, "timestamp": "t1"})
    )

    # Every field matches except the volatile timestamp: no conflict.
    matching_candidate = {
        "checkpoint_commit": "same",
        "environment": {"python": "3.14.0"},
        "timestamp": "t2",
    }
    assert manifest_overwrite_conflict(target, matching_candidate) is None

    # A non-volatile field also differs: conflict, and timestamp is not
    # blamed for it.
    diverging_candidate = {
        "checkpoint_commit": "same",
        "environment": {"python": "3.13.0"},
        "timestamp": "t2",
    }
    message = manifest_overwrite_conflict(target, diverging_candidate)
    assert message is not None
    assert "environment" in message


def test_manifest_overwrite_conflict_refuses_on_invalid_json(tmp_path: Path):
    target = tmp_path / "broken.json"
    target.write_text("not json")
    candidate = {"checkpoint_commit": "irrelevant-for-this-check"}
    message = manifest_overwrite_conflict(target, candidate)
    assert message is not None
    assert "not valid JSON" in message


def test_build_manifest_does_not_touch_disk(tmp_path: Path, monkeypatch):
    """build_manifest() must derive everything from its in-memory arguments
    (plus the script's own file and repository-independent facts) so it can
    run before any output file exists on disk."""
    monkeypatch.chdir(tmp_path)
    manifest = build_manifest(b"fake-inventory-bytes", b"fake-ledger-bytes")
    assert manifest["outputs"][0]["sha256"]
    assert manifest["outputs"][1]["sha256"]
