# Current Audited Findings

## Confirmed Defects

- GRT `Aeff` (`mm2`) was mapped to effective case volume.
- The selector used gross capacity as net powder-space capacity.
- The selector and notebook used bullet grains as sectional density.
- Effective barrel length used a fixed 2.5-inch subtraction or COAL subtraction
  instead of initial bullet-base-to-muzzle travel.
- Powder suggestions depended on unsupported `Ba_target` and `Ba_eff` equations.
- Missing powder scalars were silently mean-imputed in plots.
- Modeled/unknown data was described as empirical and verified.
- Burnout claims had no supporting burn-fraction or burnout fields.

## Regression Reproduction

All 10 committed prediction rows produce:

| Metric | Value |
|---|---:|
| MAE | 1.0460839220 gr |
| RMSE | 1.3505634115 gr |
| maximum absolute error | 2.8916517475 gr |
| mean signed error | -0.9237984375 gr |
| prediction-form R2 | 0.9942624233 |

These are in-sample artifact statistics, not validation. There is no committed
fit procedure, uncertainty estimate, holdout, cross-validation, or external
dataset. Duplicate cartridge names and missing prediction row IDs further limit
join reliability.

## Historical Reconstruction

The 1961 manual supports net powder-space capacity, sectional density, mass
ratio, historical loading-density arithmetic, projectile travel, expansion-ratio
meaning, and a worked example. It does not provide enough accessible information
to implement exact original powder boundaries, velocity, or pressure equations.

The full evidence and dispositions are in
`docs/audits/modern_powley_full_repository_audit.md`.
