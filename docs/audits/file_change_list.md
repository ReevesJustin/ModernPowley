# Audit and Environment File-Change List

Checkpoint: `pre_audit_agent_derived_prototype` ->
`6485b3d2f4c9fb48e2349f548ba7c79c8821947d`

## Modified Files (21)

- `.gitignore` - ignores the repository-local uv cache.
- `README.md` - audit warning, current capability, reproducible commands.
- `TODO.md` - records uv migration and disabled legacy scripts.
- `docs/Current_Findings.md` - replaces validation claims with audited findings.
- `docs/Equations.md` - source-backed and quarantined equation guide.
- `docs/History.md` - audited history index.
- `docs/Introduction.md` - provenance and scientific boundaries.
- `docs/Usage_Instructions.md` - audited verification/API use only.
- `jupyter/demo.ipynb` - legacy warning and immediate Run All stop.
- `scripts/analysis.py` - disables invalid validation workflow.
- `scripts/calculate_charge.py` - disables legacy charge regression generation.
- `scripts/calculate_metrics.py` - disables mislabeled metric generation.
- `scripts/compute_ba_eff.py` - disables unsupported in-place derivation.
- `scripts/compute_predictions.py` - disables legacy prediction generation.
- `scripts/create_db.py` - documents uv execution.
- `scripts/parse_grt_cartridge.py` - fixes area/volume defect; retains raw units.
- `scripts/parse_grt_prop.py` - removes variable-name semantic guesses.
- `scripts/plot_data.py` - disables stale plot generation.
- `scripts/plot_rc_bulletweight.py` - disables plot and removes efficiency label/imputation.
- `scripts/plot_rc_sd.py` - disables plot and removes efficiency label/imputation.
- `scripts/propellant_selector.py` - disables invalid powder suggestions.

## Added Audit and Provenance Files (21)

- `data/README.md`
- `plots/README.md`
- `reference/source_ledger.csv`
- `docs/audits/file_change_list.md`
- `docs/audits/audit_completion_report.md`
- `docs/audits/inventory_generation_manifest.json`
- `docs/audits/modern_powley_full_repository_audit.md`
- `docs/audits/pre_audit_file_inventory.csv`
- `docs/provenance/constant_ledger.csv`
- `docs/provenance/data_field_ledger.csv`
- `docs/provenance/equation_ledger.csv`
- `docs/provenance/grt_field_mapping.csv`
- `docs/provenance/legacy_artifact_manifest.csv`
- `docs/history/01_original_powley_sources.md`
- `docs/history/02_original_powley_method.md`
- `docs/history/03_davis_transcription.md`
- `docs/history/04_howell_corrections.md`
- `docs/history/05_miller_modifications.md`
- `docs/history/06_modern_powley_experimental_extensions.md`
- `docs/history/07_online_emulator_implementation.md`
- `pyproject.toml`

## Added Implementation and Audit Scripts (22)

- `scripts/audit_regression.py`
- `scripts/generate_audit_inventory.py`
- `src/modern_powley/__init__.py`
- `src/modern_powley/original/__init__.py`
- `src/modern_powley/original/charge.py`
- `src/modern_powley/original/geometry.py`
- `src/modern_powley/original/powder_index.py`
- `src/modern_powley/original/pressure.py`
- `src/modern_powley/original/units.py`
- `src/modern_powley/original/velocity.py`
- `src/modern_powley/later/__init__.py`
- `src/modern_powley/later/davis.py`
- `src/modern_powley/later/howell.py`
- `src/modern_powley/later/miller.py`
- `src/modern_powley/experimental/__init__.py`
- `src/modern_powley/experimental/_guard.py`
- `src/modern_powley/experimental/ba_eff.py`
- `src/modern_powley/experimental/ba_target.py`
- `src/modern_powley/experimental/charge_regression.py`
- `src/modern_powley/provenance/__init__.py`
- `src/modern_powley/provenance/source_types.py`
- `src/modern_powley/provenance/validation.py`

## Added Tests (11)

- `tests/unit/test_geometry.py`
- `tests/unit/test_units_and_charge.py`

## Added Environment and Source Files (4)

- `.python-version`
- `AGENTS.md`
- `reference/powley_manual/powleysmanuals1.md`
- `uv.lock`

## Removed Legacy Environment File (1)

- `requirements.txt` - dependencies moved to `pyproject.toml` and `uv.lock`.
- `tests/reference/test_powley_1961_example.py`
- `tests/reference/test_davis_transcription.py`
- `tests/regression/test_committed_regression.py`
- `tests/provenance/test_artifact_consistency.py`
- `tests/provenance/test_experimental_guards.py`
- `tests/provenance/test_grt_mapping.py`
- `tests/provenance/test_grt_parser_output.py`
- `tests/provenance/test_missing_sources.py`
- `tests/provenance/test_no_imputation.py`
