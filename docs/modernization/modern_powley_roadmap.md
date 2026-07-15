# Modernized Powley Roadmap

## Program Status

`modernized_powley: authorized_for_development` proceeds independently of the
`complete_historical_method: evidence_limited` status. Historical scale recovery
is dormant evidence work, not a prerequisite for this roadmap. Every phase may
end in a negative conclusion; later phases do not begin until dependencies and
promotion gates pass.

Evidence and maturity terms are defined in
`evidence_and_model_classes.md`. Model separation and promotion are governed by
`model_boundaries.md`.

## M00: Program Authorization And Boundaries

- **Objective:** Establish purpose, safety boundary, evidence classes,
  architecture, phases, and promotion rules.
- **Prerequisites:** Completed historical reconstruction audit.
- **Allowed evidence:** All classes for classification; no numerical admission.
- **Required inputs:** Audit conclusions, repository architecture, provenance
  vocabulary, and user-defined modernization objectives.
- **Expected outputs:** Charter, evidence policy, model boundaries, roadmap, and
  M01 specification.
- **Exclusions:** Numerical implementation, namespace creation, model promotion,
  ranking, and recommendations.
- **Tests:** Documentation status, boundary, blocker, and file-presence tests.
- **Validation gates:** Entry points agree; historical failures remain explicit;
  no source, data, or numerical behavior changes.
- **Promotion criteria:** Documentation reviewed, tests pass, commit retained.
- **Stopping conditions:** Conflicting historical or safety boundary.
- **Artifacts:** This documentation set and its provenance tests.

## M01: Canonical Input, Unit, And Geometry Layer

**Status: implemented and reviewed.** See
`reviews/M01_completion_review.md`. M02 is the next active phase.

- **Objective:** Define typed, provenance-aware physical inputs and geometry
  without powder ranking or ballistics prediction.
- **Prerequisites:** M00; detailed specification in
  `phases/M01_canonical_inputs_and_geometry.md`.
- **Allowed evidence:** All evidence classes for input provenance; equations
  require declared evidence and maturity. Original arithmetic remains unchanged.
- **Required inputs:** Cartridge, capacity, projectile, firearm, measurement,
  uncertainty, provenance, and unit records.
- **Expected outputs:** Validated canonical records, explicit conversions, and
  separately named derived geometry.
- **Exclusions:** Powder selection, charge, pressure, velocity, burn, muzzle
  pressure, ranking, recommendation, and user interface.
- **Tests:** Unit round trips, dimensional invariants, capacity separation,
  invalid inputs, edge geometry, serialization, and architecture boundaries.
- **Validation gates:** Every field has units/provenance; measured capacity is
  never overwritten; no mixed-unit arithmetic; original scalar compatibility is
  demonstrated without changing `original/`.
- **Promotion criteria:** Independent review of schema, units, equations, tests,
  and migration policy; bounded M01 API approved.
- **Stopping conditions:** Ambiguous quantity semantics, uncontrolled conversion,
  or geometry that cannot report assumptions and uncertainty.
- **Artifacts:** Schema/design record, test fixtures, conversion ledger entries,
  implementation decision, and known-edge-case list.

## M02: Powder-Property Evidence Model

**Status: implemented and reviewed.** See
`reviews/M02_completion_review.md`. M03 is the next active phase.

- **Objective:** Define how identity, bulk density, energy, thermodynamic
  properties, burn behavior, lot/condition, missingness, and provenance are stored.
- **Prerequisites:** Promoted M01 records and unit policy.
- **Allowed evidence:** `other_published_primary`, `manufacturer_published`,
  `independent_laboratory_measurement`, and `user_measurement`; reverse-engineered,
  fitted, or calibrated values remain visibly experimental.
- **Required inputs:** Powder identity/lot, property value, units, conditions,
  source, uncertainty, method, and applicability domain.
- **Expected outputs:** Property schema and completeness report; no universal
  burn-rate ordering.
- **Exclusions:** Mean imputation, borrowed powder values, rankings, charge or
  pressure calculations, and automatic use of GRT fields.
- **Tests:** Identity uniqueness, unit validation, missing-value behavior,
  provenance requirements, condition handling, and serialization.
- **Validation gates:** Every property is traceable and semantically defined;
  modeled and measured values are distinct.
- **Promotion criteria:** Representative sources ingest without semantic loss;
  unknowns fail explicitly.
- **Stopping conditions:** Required semantics or units cannot be established.
- **Artifacts:** Source records, property dictionary, fixtures, and intake audit.

## M03: Transparent Geometric Screening

- **Objective:** Compute capacity/fill geometry, loading-density measures,
  expansion ratios, sectional density, mass ratio, and domain checks.
- **Prerequisites:** Promoted M01; M02 only for powder bulk-volume fields.
- **Allowed evidence:** Source-backed geometry, measured inputs, published unit
  conversions, and explicitly derived quantities.
- **Required inputs:** M01 geometry plus charge mass and, when used, sourced bulk
  density from M02.
- **Expected outputs:** Named geometry and fill metrics with assumptions,
  uncertainty, and rejection reasons.
- **Exclusions:** Powder suitability, pressure, velocity, burn, and optimality.
- **Tests:** Dimensional identities, measured/estimated capacity branches,
  extrema, invalid geometry, and uncertainty propagation.
- **Validation gates:** No ambiguous `case_volume` or `expansion_ratio`; every
  rejection is attributable to a stated geometric/domain rule.
- **Promotion criteria:** Independent fixtures and boundary tests pass.
- **Stopping conditions:** Geometry uncertainty makes a screen indeterminate.
- **Artifacts:** Equation records, fixtures, decision logs, and domain report.

## M04: Candidate Powder Screening

- **Objective:** Develop transparent inclusion and exclusion rules without
  claiming validated optimal ranking.
- **Prerequisites:** Promoted M02 and M03.
- **Allowed evidence:** Published/manufacturer/measured property evidence;
  experimental candidates only in separately labeled comparisons.
- **Required inputs:** Candidate identity/properties, geometric metrics, source
  domains, and explicit screening thresholds.
- **Expected outputs:** Included, excluded, or indeterminate status with reasons
  and evidence references.
- **Exclusions:** Recommended powder, recommended charge, hidden aggregate score,
  pressure/velocity claims, and commercial burn-chart determinism.
- **Tests:** Rule isolation, missing properties, conflicting evidence, threshold
  boundaries, deterministic ordering, and indeterminate handling.
- **Validation gates:** Every decision is explainable; absence never becomes a
  default value.
- **Promotion criteria:** Rules survive source/domain review and representative
  negative cases.
- **Stopping conditions:** Screening depends on unavailable or unvalidated data.
- **Artifacts:** Rule catalog, candidate reports, rejected-method record.

## M05: Charge-Region Estimation

- **Objective:** Estimate bounded regions for further analysis, never a
  recommended charge.
- **Prerequisites:** Promoted M04; explicit fill and property uncertainties.
- **Allowed evidence:** Published primary, manufacturer, and measured relations;
  fits/calibrations only as experimental candidates with held-out plans.
- **Required inputs:** Candidate, geometry, fill bounds, property uncertainty,
  source domain, and pressure-standard identity.
- **Expected outputs:** Bounded analysis region, outside-domain status, and
  uncertainty contributors.
- **Exclusions:** Loading instruction, point recommendation, implicit safety
  assurance, and use of the quarantined charge regression without promotion.
- **Tests:** Bound ordering, monotonic/invariant checks where sourced, missing
  inputs, domain edges, and no point recommendation.
- **Validation gates:** Bounds have traceable causes and cannot exceed source
  applicability silently.
- **Promotion criteria:** Independent source reconciliation and conservative
  measured evaluation plan approved.
- **Stopping conditions:** A defensible bound cannot be established.
- **Artifacts:** Method audit, region fixtures, sensitivity report.

## M06: Pressure And Velocity Baseline

- **Objective:** Introduce one documented baseline model at a time for explicitly
  named pressure quantities and projectile velocity.
- **Prerequisites:** Promoted M05 and a defined measured-validation dataset.
- **Allowed evidence:** Published primary methods and independent measurements;
  reverse-engineered/simulator/fitted methods remain experimental.
- **Required inputs:** Complete model inputs, boundary/initial conditions,
  pressure semantics, standards, and uncertainty.
- **Expected outputs:** Named pressure and velocity estimates, domain, errors,
  and failure status.
- **Exclusions:** CUP-to-PSI conversion without authority, model-family fallback,
  high-fidelity claims, and ranking before validation.
- **Tests:** Equations, dimensions, source examples, invariants, limits, pressure
  naming, domain rejection, and deterministic solver behavior.
- **Validation gates:** Predeclared error metrics on independent cases; failures
  retained; calibration and evaluation separated.
- **Promotion criteria:** A bounded model/version/domain passes measured review.
- **Stopping conditions:** Pressure semantics or validation data are inadequate.
- **Artifacts:** Model record, datasets/splits, metrics, residuals, failures.

## M07: Burn Progression And Burnout Location

- **Objective:** Add burn fraction, burnout time, and burnout travel with an
  explicit pressure-path and combustion-model basis.
- **Prerequisites:** Promoted M06 pressure-time/travel foundation and M02 burn
  properties with authoritative semantics.
- **Allowed evidence:** Published combustion models and measured instrumented
  data; simulator behavior only as reverse-engineered comparison.
- **Required inputs:** Burn law/properties, geometry, pressure path, temperature,
  ignition assumptions, and uncertainty.
- **Expected outputs:** Burn fraction versus time/travel, burnout definition,
  time, travel, and before-muzzle status.
- **Exclusions:** Inferring burnout from muzzle pressure; unsupported complete
  burn claims; silent GRT parameter mapping.
- **Tests:** Conservation/invariants, fraction bounds, time/travel monotonicity,
  muzzle boundary, source examples, and outside-domain behavior.
- **Validation gates:** Burn outputs have measured or defensibly published
  validation and explicit definition.
- **Promotion criteria:** Error metrics and sensitivity are acceptable for the
  stated screening role.
- **Stopping conditions:** Required burn semantics or measured evidence absent.
- **Artifacts:** Burn-model audit, validation fixtures, failure cases.

## M08: Muzzle Pressure And Selection Objectives

- **Objective:** Add muzzle pressure and secondary discriminators after primary
  pressure and burn constraints are available.
- **Prerequisites:** Promoted M06 and M07.
- **Allowed evidence:** Promoted model outputs and applicable measured data.
- **Required inputs:** Pressure/travel solution, muzzle position, burn state,
  uncertainties, and user-defined objective thresholds.
- **Expected outputs:** Muzzle pressure, objective-specific comparisons, and
  transparent component reasons.
- **Exclusions:** A single unexplained score, recommendation, or claims that low
  muzzle pressure proves complete burn.
- **Tests:** Quantity identity, objective independence, threshold behavior,
  uncertainty ties, and missing-output handling.
- **Validation gates:** Muzzle pressure and burn status validated separately;
  objectives cannot override pressure rejection.
- **Promotion criteria:** Secondary criteria improve an explicitly measured
  decision task without hiding uncertainty.
- **Stopping conditions:** Primary models are not sufficiently valid.
- **Artifacts:** Objective definitions, comparison reports, validation record.

## M09: Measured Validation And Calibration

- **Objective:** Evaluate cartridge families, bullet weights, pressure data,
  velocity ladders, and holdout cases under a predeclared protocol.
- **Prerequisites:** Candidate outputs from M05-M08 and retained measurement data.
- **Allowed evidence:** Independent laboratory and carefully qualified user or
  manufacturer measurements; calibration sources separately labeled.
- **Required inputs:** Row-level provenance, instruments, conditions, splits,
  duplicates, uncertainty, and model versions.
- **Expected outputs:** MAE, RMSE, bias, maximum error, coverage, residuals,
  family/condition breakdowns, and known failures.
- **Exclusions:** In-sample validation claims, undisclosed row selection, and
  tuning on holdout cases.
- **Tests:** Dataset integrity, split leakage, reproducible metrics, uncertainty,
  and version binding.
- **Validation gates:** Holdout/external performance and failure analysis satisfy
  predeclared claim-specific criteria.
- **Promotion criteria:** Review accepts or narrows each model's domain.
- **Stopping conditions:** Insufficient independent data or unacceptable errors.
- **Artifacts:** Dataset manifests, splits, metrics, residual plots, decisions.

## M10: Uncertainty And Decision Policy

- **Objective:** Establish rejection thresholds, confidence classes,
  outside-domain behavior, and model-comparison policy.
- **Prerequisites:** M09 measured results and sensitivity analyses.
- **Allowed evidence:** Promoted results and retained uncertainty sources.
- **Required inputs:** Input, parameter, model-form, calibration, and measurement
  uncertainties plus decision objectives.
- **Expected outputs:** Confidence/applicability class, decision trace, rejection
  threshold, indeterminate state, and comparison policy.
- **Exclusions:** Hidden uncertainty, false precision, and score-only decisions.
- **Tests:** Uncertainty propagation, threshold crossings, ties, model conflicts,
  missing uncertainty, and conservative outside-domain handling.
- **Validation gates:** Decisions are reproducible and uncertainty-aware; unsafe
  ambiguity cannot become acceptance.
- **Promotion criteria:** Independent review approves the bounded decision role.
- **Stopping conditions:** Uncertainty cannot be characterized sufficiently.
- **Artifacts:** Decision-policy version, sensitivity report, test vectors.

## M11: User Workflow

- **Objective:** Expose only promoted numerical layers through an auditable CLI
  or application workflow.
- **Prerequisites:** Applicable M01-M10 gates passed and decision policy promoted.
- **Allowed evidence:** Promoted modern methods only; historical/later outputs
  may appear solely as separately labeled comparisons.
- **Required inputs:** Versioned schema, method selection, provenance, user data,
  and applicable standards.
- **Expected outputs:** Reproducible analytical report with reasons, uncertainty,
  outside-domain state, and method versions.
- **Exclusions:** Loading recommendations, concealed defaults, unsupported
  combinations, and direct revival of the legacy selector/notebook.
- **Tests:** End-to-end provenance, accessibility, invalid inputs, deterministic
  reports, method isolation, and no recommendation language.
- **Validation gates:** Every exposed output is promoted for that role and all
  caveats are machine-visible.
- **Promotion criteria:** Product review confirms no capability exceeds numerical
  validation.
- **Stopping conditions:** Any dependency lacks promotion or safe failure.
- **Artifacts:** Interface specification, report schema, end-to-end fixtures,
  release decision.
