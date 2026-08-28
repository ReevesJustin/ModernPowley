# `generate_audit_inventory.py` Output Ownership Conflict

## Status

`resolved_with_refusal_guard` — a maintenance fix, not a specification. This
record documents a defect and its bounded fix, not a milestone or workstream.

## Defect

`scripts/generate_audit_inventory.py` unconditionally overwrote three files
it does not fully own:

1. `docs/provenance/data_field_ledger.csv` — the script's own logic derives
   rows only from `data/*.csv` headers, using a seven-column schema
   (`data_asset, field, attribution_class, unit, source_id,
   verification_evidence, status`). The maintained, committed ledger has been
   hand-extended to an eight-column schema
   (`..., verification_status, disposition`) with 315 data rows covering
   M01-M05 and empirical-load Phase 1 fields the script has no logic to
   produce. Running the script replaced 315 hand-maintained rows with ~126
   script-derived rows under a different, incompatible column schema.
2. `docs/audits/pre_audit_file_inventory.csv` — the script's checkpoint-derived
   rows are content-identical to the committed file (same 40 rows, same
   hashes) but in a different order than the committed file currently uses.
   Byte comparison treats this as a conflict too; no row content is at risk,
   but the file cannot be silently regenerated either.
3. `docs/audits/inventory_generation_manifest.json` — the script's own output
   schema does not include a `post_generation_updates` key. The committed
   manifest carries one, narrating the manual ledger extensions above.
   Regenerating the manifest silently deleted that field.

Discovered 2026-08-27 while validating an unrelated documentation-only
change. The overwrite was caught before being committed and reverted; no
committed history was affected. A second, confirmed-by-inspection pass (not
executed) reached the same conclusions about the ledger schema and the
manifest field before this fix landed.

## Fix

`scripts/generate_audit_inventory.py` now builds every output in memory
first and, before writing anything, refuses if a target file already exists
with content the script would not reproduce exactly:

- `csv_overwrite_conflict()` does a byte-for-byte comparison for the two CSV
  outputs.
- `manifest_overwrite_conflict()` refuses if the existing manifest JSON
  carries any top-level key outside the script's own fixed schema
  (`MANIFEST_SCHEMA_KEYS`).

`main()` collects every conflict before writing any file and exits nonzero
via `sys.exit()` with all conflict messages if any check fails. No output is
written when any single check fails — the refusal is all-or-nothing and
occurs before any write.

This fix does not attempt to reconcile the script's generation logic with the
maintained eight-column ledger schema, merge rows, or regenerate the
authoritative ledger from the incomplete `data/*.csv`-only file list. That
reconciliation, if ever wanted, is a separate, larger task requiring its own
review of the current 315-row schema against this script's original scope.

`just audit` (`justfile`) invokes this script directly, so the guard applies
to that entry point without a `justfile` change. `just check` does not invoke
this script and was never affected.

## Regression Coverage

`tests/provenance/test_generate_audit_inventory_guard.py`:

- runs `main()` against the real repository's current (diverged) state and
  asserts it raises `SystemExit` and that all three protected files remain
  byte-identical before and after;
- confirms the ledger conflict and the manifest conflict are each detected
  and correctly attributed;
- unit-tests `csv_overwrite_conflict()` and `manifest_overwrite_conflict()`
  in isolation against synthetic `tmp_path` files for the match/mismatch and
  valid/invalid-JSON cases.

## Documentation Corrected

`README.md`'s "Reproducible Audit Commands" section and `CLAUDE.md`'s
environment command list no longer present `generate_audit_inventory.py` (or
`just audit`) as a routine, always-succeeding step; both now state that a
refusal is expected and point here.

## Remaining Limitation

The script's generation logic itself still only knows the original
checkpoint-era file list and the seven-column ledger schema. It cannot
currently regenerate either protected CSV even when a legitimate reason to
do so exists (for example, a genuinely new `data/*.csv` field). Extending its
logic to match the current maintained schema is unauthorized by this record
and requires a separate reviewed task.
