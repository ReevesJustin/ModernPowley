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

## Milestone Governance

For M01-M04 the durable chain is: canonical specification -> phase design ->
accepted implementation decisions -> tests and ledgers -> completion review.
The specification is the scope authority; a review is evidence, not a substitute.
M05 is accepted only for records, structural validation, and strict serialization;
no numerical method/data is admitted.
Future phase concepts M06-M11 remain unspecified, unauthorized concepts. Before
any planned milestone
becomes implementable, its specification must be reviewed in a planning commit
and explicitly marked `authorized`. A recommendation never authorizes the next
milestone. Amendments must be explicit and traceable; completed acceptance gates
are not rewritten to match implementation.

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
[`specification`](milestones/M01_canonical_inputs_and_geometry.md),
[`design`](phases/M01_canonical_inputs_and_geometry.md),
[`decisions`](decisions/M01_implementation_decisions.md), and
[`completion review`](reviews/M01_completion_review.md). Principal evidence:
`tests/unit/test_m01_*`, `tests/provenance/test_m01_*`, and equation/data-field
ledgers. M01 remains the promoted geometry foundation.

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
[`specification`](milestones/M02_powder_property_records.md),
[`design`](phases/M02_powder_property_records.md),
[`decisions`](decisions/M02_implementation_decisions.md), and
[`completion review`](reviews/M02_completion_review.md). Principal evidence:
`tests/unit/test_m02_*`, `tests/provenance/test_m02_*`, and equation/data-field
ledgers. M02 remains the promoted neutral evidence layer.

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

## M03: Input Completeness And Literal Domain Diagnostics

**Status: implemented and reviewed.** See
[`specification`](milestones/M03_input_and_domain_diagnostics.md),
[`design`](phases/M03_input_and_domain_diagnostics.md),
[`decisions`](decisions/M03_implementation_decisions.md), and
[`completion review`](reviews/M03_completion_review.md). Principal evidence:
`tests/unit/test_m03_*`, `tests/provenance/test_m03_*`, and equation/data-field
ledgers. M03 remains an accepted diagnostic layer; M04 is also accepted.

- **Objective:** Explain whether explicit inputs satisfy a named existing M01
  operation's requirements and whether one query literally satisfies one M02
  observation's declared domain.
- **Prerequisites:** Promoted M01 and M02 record contracts.
- **Allowed evidence:** Explicit M01/M02 records and repository-authored M03
  requirement definitions; no production powder facts are introduced.
- **Required inputs:** A named versioned requirement set and explicit candidate
  bundle, or one observation and an explicit domain-query context.
- **Expected outputs:** Per-requirement completeness diagnostics and
  per-constraint literal applicability diagnostics.
- **Exclusions:** Geometry execution, powder screening or suitability, source
  selection, solver preparation, interpolation, extrapolation, and prediction.
- **Tests:** Missingness, dimensions, capacity identity, branch conditions,
  conflicts, domain endpoints, intervals, categories, units, and serialization.
- **Validation gates:** No input inference or substitution; unspecified domains
  do not pass; every rejection identifies its exact requirement or constraint.
- **Promotion criteria:** Strict schema, architecture, traceability, and all
  diagnostic boundary tests pass.
- **Stopping conditions:** Required context is absent, explicitly unavailable,
  conflicting, unsupported, or only partially comparable.
- **Artifacts:** Requirement definitions, diagnostic records, decision log,
  ledgers, fixtures, and completion review.

## M04: Declarative Screening Criteria And Auditable Outcome Records

**Status: accepted and reviewed.** See
[`specification`](milestones/M04_screening_decision_records.md),
[`design`](phases/M04_screening_decision_records.md),
[`decisions`](decisions/M04_implementation_decisions.md), and the completion
review path `reviews/M04_completion_review.md`. Principal tests are
`tests/unit/test_m04_*`, `tests/provenance/test_m04_*`, and milestone-governance
tests; ledger entries use `SRC-M04-DESIGN`.

- **Objective:** Represent immutable criteria, exact supplied evidence,
  evaluation contexts, recorded outcomes, and descriptive mandatory summaries.
- **Prerequisites:** Promoted M01-M03 record contracts.
- **Allowed evidence:** Exact caller-supplied M01-M03 records; synthetic fixtures
  only in this increment.
- **Required inputs:** Versioned criterion and set definitions, exact evidence
  references, context identity, and explicit evaluation provenance.
- **Expected outputs:** Literal criterion outcomes and descriptive set summaries
  with full audit chains and bounded non-implication statements.
- **Exclusions:** Catalog search, observation discovery, production criteria,
  powder suitability, ranking, scoring, prediction, solver, or recommendation.
- **Tests:** Versions, roles, statuses, missing/conflict behavior, exact bounds,
  interval containment, manual/mechanical separation, schema, architecture, and
  durable milestone governance.
- **Validation gates:** All 18 gates in the canonical specification, including
  specification-first governance, passed before status became `accepted`.
- **Promotion criteria:** Strict record contract and literal evaluator reviewed;
  no screening engine or physical policy is promoted.
- **Stopping conditions:** Required exact evidence, definition, version, or
  comparison semantics are absent or conflicting.
- **Artifacts:** M04 records, tests, ledgers, specification, decisions, design,
  completion review, and governance contract.

## M05: Charge-Region Records

**Status: accepted for records and strict serialization only.** See
the canonical [`specification`](milestones/M05_charge_region_records.md),
planning [`evidence and semantics review`](reviews/M05_evidence_and_semantics_review.md),
[`specification decisions`](decisions/M05_specification_decisions.md),
[`authorization decision`](decisions/M05_records_only_authorization.md), and
[`authorization review`](reviews/M05_records_only_authorization_review.md).
See also the [`implementation design`](phases/M05_charge_region_records.md),
[`implementation decisions`](decisions/M05_implementation_decisions.md), and
[`completion review`](reviews/M05_completion_review.md).

- **Objective:** Define a provenance-preserving contract for bounded analytical
  regions for further analysis, never a recommended charge or safe range.
- **Prerequisites:** Accepted M04 and retained records-only authorization.
- **Allowed evidence:** Published primary, manufacturer, and measured relations;
  fits/calibrations remain experimental candidates. The accepted records layer
  admits no production method or data.
- **Required inputs:** Records require exact M01/M02 evidence,
  applicable M03 diagnostics, method/version, units, domain, conditions,
  uncertainty, conflict, and lineage. M04 references are audit dependencies only.
- **Expected outputs:** Immutable caller-supplied region records, structural
  validation, strict serialization, and synthetic tests only.
- **Exclusions:** Loading instruction, point recommendation, implicit safety
  assurance, all region derivation/intersection arithmetic, real region
  construction, production data, and the quarantined regression.
- **Tests:** Unit, serialization, architecture, provenance, and governance tests
  enforce the contract and no dependency/data changes.
- **Validation gates:** Canonical record/serialization gates and completion
  review pass without numerical region behavior.
- **Promotion criteria:** Records layer accepted; numerical work requires a new
  amendment and explicit authorization.
- **Stopping conditions:** No admitted method/data; unresolved pressure,
  dependency, or region semantics; or any recommendation/safety implication.
- **Artifacts:** Canonical specification, evidence review, specification
  decisions, authorization/completion reviews, tests, serializer, and ledgers.

## Cross-Cutting Governed Workstreams

[`cross_cutting_workstreams.md`](cross_cutting_workstreams.md) records future
powder evidence, validation infrastructure, uncertainty, diagnostics/plots,
tooling, hypothesis logging, and GRT-file web-interface direction. These are
planning directions, not implementation authorization. Validation record and
dataset-split foundations begin before M06; formal model validation remains M09.
M06-M08 remain future unauthorized model concepts, and a recommendation never
authorizes any workstream.

The canonical parent empirical-load specification remains `planned`:
[`empirical_load_evidence_and_validation.md`](workstreams/empirical_load_evidence_and_validation.md).
Its separately bounded
[`Empirical Load Evidence Records Phase 1`](workstreams/empirical_load_evidence_records_phase_1.md)
is `authorized` for a later immutable-record and strict-serialization
implementation using fictional fixtures only; see its
[`authorization decisions`](decisions/empirical_load_evidence_records_phase_1_authorization.md)
and [`authorization review`](reviews/empirical_load_evidence_records_phase_1_authorization_review.md).
It is not implemented or accepted and authorizes no cohort, split, source
intake, M05 adapter, or model. Candidate M05 method dispositions remain in
[`M05_derivation_readiness_review.md`](reviews/M05_derivation_readiness_review.md).
No scientific data, high-performance cohort, production M05 derivation, or M06
model is admitted. A recommendation never authorizes implementation.

## Future Phase Concept M06: Pressure And Velocity Baseline

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

## Future Phase Concept M07: Burn Progression And Burnout Location

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

## Future Phase Concept M08: Muzzle Pressure And Selection Objectives

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

## Future Phase Concept M09: Formal Measured Validation And Calibration

- **Objective:** Evaluate cartridge families, bullet weights, pressure data,
  velocity ladders, and holdout cases under a predeclared protocol.
- **Prerequisites:** Candidate outputs from M05-M08 and retained measurement
  data using validation contracts/split policy established before M06.
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

## Future Phase Concept M10: Uncertainty And Decision Policy

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

## Future Phase Concept M11: User Workflow

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
