# Data Status

The committed CSV files are preserved pre-audit artifacts. They are not a
homogeneous empirical dataset. Field-by-field classifications are in
`docs/provenance/data_field_ledger.csv`; generation status and hashes are in
`docs/provenance/legacy_artifact_manifest.csv`.

- GRT values are simulator/model inputs or outputs, not laboratory measurements.
- `CartridgeData.csv` has no row-level source record and cannot support independent
  validation claims.
- `cartridge_data_from_grt.csv` contains the historical `Aeff` area-to-volume
  defect and must not be used for calculations.
- `Predictions.csv` is an in-sample regression artifact with duplicate names and
  no stable source-row ID.
- Missing scientific values must remain missing. Mean imputation and values
  borrowed from other powders are prohibited.

No historical artifact is regenerated in place by the audited workflow.
