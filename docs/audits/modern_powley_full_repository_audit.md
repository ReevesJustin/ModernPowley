# ModernPowley Full Repository Audit

Status: active audit, evidence cutoff 2026-07-14
Preserved state: tag `pre_audit_agent_derived_prototype`, commit `6485b3d2f4c9fb48e2349f548ba7c79c8821947d`

## Scope and Rules

This audit treats the tagged repository as an agent-derived prototype, not an
authority. A statement is source-backed only when its ledger entry identifies a
traceable artifact and location. Simulator values are modeled, regressions are
fitted, and missing scientific values remain missing. Nothing in this repository
is a loading recommendation.

Severity is P0 (invalidates core conclusions), P1 (material output/claim effect),
P2 (scientific/documentation quality), or P3 (software/maintenance). Categories
are the controlled categories requested in the audit brief.

## Findings

### MP-AUD-001 - Area mapped to volume

- **Severity/category:** P0 / dimensional error, incorrect implementation
- **File/symbol:** `scripts/parse_grt_cartridge.py:17-45`, `CARTRIDGE_MAPPING`
- **Current behavior:** maps XML `Aeff=34.645092 mm2` to `eff_case_vol` and applies no conversion.
- **Why questionable/evidence:** the source XML describes `Aeff` as `effektive area`, unit `mm2`; area cannot populate a water-mass volume.
- **Source status/units:** direct local GRT artifact, `SRC-GRT-LOAD-001`; mm2 -> incorrectly unlabeled destination.
- **Downstream impact:** parsed effective capacity, RC, ER, charge regression, ranking, and plots can be dimensionally invalid.
- **Correction/test/disposition:** exclude `Aeff` from volume mappings; `tests/provenance/test_grt_mapping.py`; legacy defect preserved at the checkpoint, canonical mapping excludes it.

### MP-AUD-002 - Gross capacity substituted for net powder space

- **Severity/category:** P0 / incorrect implementation
- **File/symbol:** `scripts/propellant_selector.py:42-43`; notebook demo
- **Current behavior:** `eff_case_vol = case_vol`.
- **Why questionable/evidence:** Powley 1961 pp. 3, 8-9 defines loading density against water filling the powder space, notes seating depth changes capacity, and asks for the case capacity applicable to the seated load.
- **Source status/units:** original manual, water grains; input dataset provenance remains unknown.
- **Downstream impact:** charge, RC, ER, regression and ranking.
- **Correction/test/disposition:** require measured net capacity or explicit gross-minus-intrusion derivation; `test_net_capacity_subtracts_intrusion_and_rejects_gross_alias`; canonical implementation complete, legacy CLI pending retirement.

### MP-AUD-003 - Bullet weight used as sectional density

- **Severity/category:** P0 / incorrect equation
- **File/symbol:** `scripts/propellant_selector.py:49-62`; notebook `SD_calc`
- **Current behavior:** `SD = bullet_mass` and unscaled nearest-neighbor distance.
- **Why questionable/evidence:** manual p. 9 gives `SD = W_gr / (7000*d_in^2)`; 180 gr/.308 example is about 0.271, not 180.
- **Source status/units:** directly sourced inch-pound convention; current value is grains, not SD.
- **Downstream impact:** chart coordinate, neighbor selection, and every suggestion.
- **Correction/test/disposition:** canonical `sectional_density`; unit tests added; user-facing selector must not run legacy ranking.

### MP-AUD-004 - Unsupported `Ba` target drives suggestions

- **Severity/category:** P0 / unsupported assumption, unsafe inference
- **File/symbol:** `scripts/propellant_selector.py:81-88`
- **Current behavior:** clamps `0.85 - 0.05*RC` to `[0.45, 0.90]` and ranks powders by distance.
- **Why questionable/evidence:** no source, fitting code, dataset, residuals, uncertainty, or calibration limits exist; git history first adds it as prototype code.
- **Source status/units:** agent-generated assumption; scalar semantics unresolved.
- **Downstream impact:** all powder suggestions.
- **Correction/test/disposition:** quarantined as `experimental.ba_target` with explicit opt-in; remove ranking from normal CLI.

### MP-AUD-005 - Unsupported `Ba_eff` presented as ballistic efficiency

- **Severity/category:** P0 / unsupported assumption, naming ambiguity
- **File/symbol:** `scripts/compute_ba_eff.py:16-20`; `docs/Equations.md:1-31`
- **Current behavior:** computes `Ba*[a0+(1-a0)*z2/2]`, labels it effective vivacity and elsewhere ballistic efficiency.
- **Why questionable/evidence:** no GRT burn-law source or justification for interval, uniform weighting, or use as a cartridge ranking parameter is committed. It is not an energy-efficiency ratio.
- **Source status/units:** GRT inputs plus ModernPowley hypothesis; `Ba` unit metadata is blank in the local XML.
- **Downstream impact:** ranking, chart colors/bands, conclusions.
- **Correction/test/disposition:** quarantined as `experimental.ba_eff`, opt-in required, never called ballistic efficiency.

### MP-AUD-006 - Progressivity explanation contradicts its own equation

- **Severity/category:** P1 / documentation mismatch
- **File/symbol:** `docs/Equations.md:10-12`
- **Current behavior:** says `a0>1` makes the displayed linear factor increase with burn progress.
- **Why questionable/evidence:** `a0+(1-a0)*phi` decreases from `a0` toward 1 when `a0>1`.
- **Source status/units:** equation source unresolved; algebra directly contradicts prose.
- **Downstream impact:** interpretation of powder behavior.
- **Correction/test/disposition:** legacy page marked unaudited; do not assert direction until GRT semantics are sourced.

### MP-AUD-007 - Ambiguous expansion ratio

- **Severity/category:** P1 / naming ambiguity
- **File/symbol:** `data/ExpansionRatio.csv:1`; `scripts/calculate_charge.py:18-21`
- **Current behavior:** both `Vb/V0` and `1+Vb/V0` are called expansion ratio.
- **Why questionable/evidence:** values differ by one and are not interchangeable.
- **Source status/units:** derived dimensionless quantities.
- **Downstream impact:** comparisons, documentation, regressions.
- **Correction/test/disposition:** canonical names `barrel_volume_ratio` and `total_expansion_ratio`; unit tests added; old CSV retained as stale historical artifact.

### MP-AUD-008 - Invalid effective barrel length

- **Severity/category:** P0 / incorrect implementation
- **File/symbol:** `scripts/propellant_selector.py:44`; notebook demo
- **Current behavior:** subtracts a fixed 2.5 inches; docs alternatively subtract COAL.
- **Why questionable/evidence:** original manual p. 9 defines effective length as bullet travel and demonstrates a cleaning-rod measurement to the initial bullet base.
- **Source status/units:** direct original manual, inches.
- **Downstream impact:** regression, bore volume, ER, velocity reasoning.
- **Correction/test/disposition:** canonical projectile-travel input/helper added; no COAL or fixed subtraction.

### MP-AUD-009 - Charge regression provenance absent

- **Severity/category:** P0 / provenance gap, empirical regression
- **File/symbol:** `scripts/compute_predictions.py:17-18`
- **Current behavior:** applies `0.71*V0^1.02*L^0.06` without fitting code.
- **Why questionable/evidence:** coefficients, row selection, duplicates, fit method and uncertainty cannot be reproduced from committed material.
- **Source status/units:** empirical regression of unknown origin; dimensionally dependent on chosen units.
- **Downstream impact:** predicted charge and accuracy claims.
- **Correction/test/disposition:** quarantined with opt-in; committed values reproduction-tested, refit prohibited until provenance exists.

### MP-AUD-010 - Validation claims use training/selected rows

- **Severity/category:** P0 / validation overclaim
- **File/symbol:** `docs/Current_Findings.md:3-8,35-38`
- **Current behavior:** claims 9 verified loads, `R2>0.998`, typical error below 1 gr and full range within +/-1.3 gr.
- **Why questionable/evidence:** CSV has 10 rows, including duplicate cartridge names. Recalculation gives in-sample MAE 1.0461 gr, RMSE 1.3506 gr, max 2.8917 gr, mean error -0.9238 gr, prediction-form R2 0.99426. No holdout or external validation exists.
- **Source status/units:** fitted/unknown observations; grains.
- **Downstream impact:** central project conclusion.
- **Correction/test/disposition:** claims withdrawn in audited docs; metrics reported only as in-sample artifact reproduction.

### MP-AUD-011 - Measured and modeled data are conflated

- **Severity/category:** P0 / data-quality issue, provenance gap
- **File/symbol:** `data/CartridgeData.csv`; `docs/Current_Findings.md:11-13`
- **Current behavior:** calls rows empirical/verified while pressure fields are named estimated and GRT is described as a data source.
- **Why questionable/evidence:** no row-level source, instrument, publication, manual page, user measurement record, or simulator run manifest exists.
- **Source status/units:** unknown per field except the one local GRT load.
- **Downstream impact:** all fit and validation claims.
- **Correction/test/disposition:** all fields enumerated in data-field ledger; unknown values excluded from independent-validation claims.

### MP-AUD-012 - Burnout claims lack burnout fields

- **Severity/category:** P0 / unsupported assumption, unsafe inference
- **File/symbol:** README and `docs/Introduction.md`, `docs/Current_Findings.md`
- **Current behavior:** asserts complete or near-complete burn and infers it from muzzle pressure/selected loads.
- **Why questionable/evidence:** no `burn_fraction_at_muzzle`, burnout distance/time/definition/source fields exist.
- **Source status/units:** absent.
- **Downstream impact:** claimed optimality and powder ranking.
- **Correction/test/disposition:** audited docs prohibit burnout conclusions; legacy pages marked unaudited.

### MP-AUD-013 - Silent mean imputation

- **Severity/category:** P1 / data-quality issue
- **File/symbol:** `scripts/plot_rc_sd.py:43-46`; `plot_rc_bulletweight.py:43-47`
- **Current behavior:** missing `Ba_eff` is replaced by the available mean.
- **Why questionable/evidence:** substitutes another powder's unsupported property and makes missing points appear known.
- **Source status/units:** missing becomes fabricated scalar.
- **Downstream impact:** plot colors, contours, conclusions.
- **Correction/test/disposition:** forbidden in canonical package and tested; legacy artifacts labeled stale.

### MP-AUD-014 - GRT propellant parser maps unrelated caliber variables

- **Severity/category:** P1 / unresolved source semantics
- **File/symbol:** `scripts/parse_grt_prop.py:11-26`
- **Current behavior:** maps caliberfile `f`, `c_b_`, `c_Z`, `c_F`, `c_Q`, `c_u_`, `c_alpha` to propellant fields despite the XML containing explicit propellant inputs.
- **Why questionable/evidence:** variable names alone do not establish semantics; several values disagree strongly with explicit propellant values (for example `f=0.38` versus `Ba=0.468557`).
- **Source status/units:** unresolved GRT internals.
- **Downstream impact:** generated powder table if explicit inputs are absent/overwritten.
- **Correction/test/disposition:** mapping ledger marks these excluded; only explicit XML input metadata may be transcribed.

### MP-AUD-015 - Relative burn-rate claims overgeneralize

- **Severity/category:** P1 / unsafe inference
- **File/symbol:** `docs/Equations.md:100-124`; ranking narrative
- **Current behavior:** sorts a heterogeneous table by one modeled parameter as faster-to-slower.
- **Why questionable/evidence:** commercial chart order, closed-bomb vivacity, shape parameters, and cartridge response are different quantities. The local table itself lacks source artifacts for 21 of 22 entries.
- **Source status/units:** mostly absent; not universal ordering.
- **Downstream impact:** substitutions and rankings.
- **Correction/test/disposition:** audited history includes explicit chart caveat and IMR 4895/4064 example; no deterministic chart mapping.

### MP-AUD-016 - Historical variants collapsed

- **Severity/category:** P1 / historical attribution error
- **File/symbol:** `docs/History.md:28-34`, `docs/Equations.md:77-80`
- **Current behavior:** presents `20+12/(SD*sqrt(MR))` and `19+12/(SD*MR^0.6)` as interchangeable approximations.
- **Why questionable/evidence:** the later Davis primary-source transcription prints the first; a secondary web transcription reports the physical slide scale approximates the second; exact change author/date is unknown.
- **Source status/units:** Davis formulation recovered as later primary publication; original scale image remains inadequate for exact numeric reconstruction.
- **Downstream impact:** false original attribution.
- **Correction/test/disposition:** Davis formula is isolated under `later.davis`; original lookup fails explicitly.

### MP-AUD-017 - Lookup endpoints unresolved

- **Severity/category:** P1 / provenance gap
- **File/symbol:** Davis Table 3 web transcription; no current implementation
- **Current behavior:** documentation gives examples but no exact bands.
- **Why questionable/evidence:** transcription phrases adjacent ranges as inclusive (`81 to 91`, `91 to 110`), creating overlaps; it also prints `4427`, likely but not safely assumed to mean `4227`.
- **Source status/units:** secondary transcription only; index dimension follows Davis convention.
- **Downstream impact:** boundary powder classifications.
- **Correction/test/disposition:** overlaps and raw typo retained in `later.davis`; a complete primary Table 3 page image is still needed.

### MP-AUD-018 - Unit constants are inconsistent

- **Severity/category:** P2 / documentation mismatch
- **File/symbol:** scripts use 252.3 and 253; parser uses 15.432 and approximate `1/0.0648`.
- **Current behavior:** conversions vary by script without source/temperature convention.
- **Why questionable/evidence:** original manual states 253 gr water/in3; modern physical conversion depends on water-density convention.
- **Source status/units:** 253 is original-manual convention; others unresolved.
- **Downstream impact:** small systematic differences and nonreproducible artifacts.
- **Correction/test/disposition:** original namespace uses named 253 constant only; modern conversions require separately sourced unit policy.

### MP-AUD-019 - “Efficiency proxy” is mislabeled

- **Severity/category:** P1 / naming ambiguity
- **File/symbol:** `scripts/calculate_metrics.py:17-22`
- **Current behavior:** calls velocity/peak-pressure ratio an efficiency proxy.
- **Why questionable/evidence:** fps/psi is dimensional and is not thermodynamic or ballistic efficiency.
- **Source status/units:** derived arbitrary ratio.
- **Downstream impact:** interpretation and plots.
- **Correction/test/disposition:** ledger classifies agent-generated derived metric; exclude from scientific claims.

### MP-AUD-020 - Generated artifacts have no manifests

- **Severity/category:** P2 / stale artifact
- **File/symbol:** all committed CSV/PNG outputs and notebook outputs
- **Current behavior:** scripts overwrite artifacts without input/script/environment hashes.
- **Why questionable/evidence:** `Predictions.csv` header already differs from its generator; notebook duplicates generation logic.
- **Source status/units:** generation state unknown.
- **Downstream impact:** cannot know which code produced figures/tables.
- **Correction/test/disposition:** historical artifacts retained and classified stale; new audit inventory has a manifest; per-artifact regeneration remains blocked where inputs lack provenance.

### MP-AUD-021 - Broad exception handling hides invalid output paths

- **Severity/category:** P3 / incorrect implementation
- **File/symbol:** selector catches all exceptions; plotting contour uses bare `except`
- **Current behavior:** emits generic messages or silently skips failures.
- **Why questionable/evidence:** provenance and validation failures are not distinguishable.
- **Source status/units:** software issue.
- **Downstream impact:** false appearance of successful processing.
- **Correction/test/disposition:** canonical functions raise typed/explicit errors; legacy scripts pending thin wrappers.

### MP-AUD-022 - Source table in Equations is not backed by committed data

- **Severity/category:** P0 / provenance gap
- **File/symbol:** `docs/Equations.md:100-124`
- **Current behavior:** claims 22 calibrated powder models while committed `propellant_params.csv` contains only one row.
- **Why questionable/evidence:** 21 rows have no local GRT files, extraction record, or hashes.
- **Source status/units:** unknown/absent.
- **Downstream impact:** central powder-band conclusion cannot be reproduced.
- **Correction/test/disposition:** table remains only in clearly labeled legacy document; sources still needed.

### MP-AUD-023 - Duplicate names and missing stable row key

- **Severity/category:** P1 / data-quality issue
- **File/symbol:** `data/CartridgeData.csv`, `data/Predictions.csv`
- **Current behavior:** two 6mm GT and two 6.5 Creedmoor rows share names; the prediction artifact omits source row `id`.
- **Why questionable/evidence:** name-keyed joins collapse distinct rows and can compare a prediction with the wrong observation.
- **Source status/units:** row identity unresolved; no unit.
- **Downstream impact:** joins, regression reproduction, plotting and error metrics.
- **Correction/test/disposition:** audit reproduction consumes duplicate rows in committed order; future generated data must retain immutable row IDs.

### MP-AUD-024 - Online emulator was not separately attributed

- **Severity/category:** P1 / historical attribution error
- **File/symbol:** tagged `docs/History.md`; previously absent implementation ledger
- **Current behavior:** described the kwk emulator as implementing “refined equations” without recording its exact code, formula variants, or boundary behavior.
- **Why questionable/evidence:** archived JavaScript uses Davis-labeled load arithmetic, a Miller-labeled `F2` approximation, a Howell-labeled coefficient, its own geometry approximations, and ordered non-overlapping lookup branches. These are not one original-Powley model.
- **Source status/units:** secondary implementation `SRC-KWK-EMULATOR`, SHA-256 `0162ee7722dfd4bf586120590e7a7fcd4d72c908e9d17b6f335822dcac990e03`; mixed historical inch-pound/CUP conventions.
- **Downstream impact:** false attribution of emulator behavior to Powley and incorrect assumptions about Table 3 endpoint overlap.
- **Correction/test/disposition:** exact code behavior is separately documented in `docs/history/07_online_emulator_implementation.md` and ledgered as later/secondary; it is not implemented as original or validated behavior.

## Regression Recalculation

Command: `uv run python scripts/audit_regression.py`.
Current direct reproduction over all ten committed rows:

| Metric | Value | Status |
|---|---:|---|
| n | 10 | includes duplicate cartridge names |
| MAE | 1.0460839220 gr | in-sample only |
| RMSE | 1.3505634115 gr | in-sample only |
| maximum absolute error | 2.8916517475 gr | in-sample only |
| mean signed error | -0.9237984375 gr | actual minus predicted |
| R2 | 0.9942624233 | prediction-form; not validation |

Coefficient uncertainty, residual diagnostics, train/test results,
cross-validation, and external validation are **unavailable** because the fit
procedure and independently sourced observations are absent.

## Unresolved Questions

1. What exact edition/page images of Davis 1981 establish every equation and Table 3 endpoint convention?
2. Which original physical-computer revision is represented by the local 1985 photograph, and how do its scale boundaries compare with the 1961 manual?
3. Where are Howell's July 1997 correction and Miller's July 1999 derivation?
4. What are GRT's authoritative definitions and units for `Ba`, `a0`, `z1`, and `z2`?
5. How was each `CartridgeData.csv` field obtained, and which values are measured versus simulated?
6. How were the regression coefficients fitted and which rows were included?
7. Where are the 21 missing propellant model artifacts cited by `docs/Equations.md`?
8. What evidence, if any, supports each burnout assertion?

## Sources Still Needed

- Davis, *Handloading* (1981), complete relevant pages including Tables 3 and 4.
- Howell, *Varmint Hunter*, July 1997, exact article/pages.
- Miller, July 1999 publication/code and derivation.
- Original Powley slide-rule scale scans at sufficient resolution for exact boundaries.
- Authoritative GRT format/model documentation or source code for propellant fields.
- Row-level load records, simulator exports, manuals, measurements, and selection criteria.
- Original regression notebook/script and environment.

## Current Disposition

Source-backed arithmetic is under `src/modern_powley/original`; Davis material is
separate under `later`; agent hypotheses and the regression are under
`experimental` and require explicit opt-in. Powder selection, velocity, and
pressure in the original namespace fail with `MissingProvenanceError` until exact
sources are available. This is intentional and is the only evidence-based
baseline currently possible.
