# M05: Charge Region Records

## Status

`planned`

This specification is the scope authority for a possible future M05 record
contract. It does not authorize implementation. The evidence and semantics
review found no admitted production method for deriving a real charge region.

## Purpose

Define how a future immutable, versioned record could preserve one or more
bounded charge-mass regions for further analysis without presenting a
recommended charge, starting load, maximum load, safe range, loading
instruction, powder-suitability decision, pressure prediction, or velocity
prediction.

A charge-region record would state only what bounds were declared or derived,
their exact basis and inputs, and the limitations of that basis. It would not
state that every point in a region is valid or tested.

## Starting Repository State Or Predecessor

Planning predecessor: accepted M04 at
`884c5bd7fe2bf4d9494f5c8fb06c65513f07bc72`, with M01-M04 contracts unchanged.
This planning pass creates no M05 source module, export, serializer, production
data, or numerical behavior.

## Scope

The future contract may represent explicitly sourced charge-mass segments,
non-numeric region states, exact derivation lineage, source domains, conditions,
uncertainty status, conflicts, activation, and supersession. It may preserve a
literal intersection only after that operation and its semantics receive
separate implementation authorization.

The proposed controlled basis vocabulary is:

- `source_declared_interval`;
- `measurement_supported_interval`;
- `geometry_or_fill_constraint`;
- `property_uncertainty_constraint`;
- `intersection_of_explicit_constraints`;
- `experimental_estimate`;
- `unavailable`;
- `indeterminate`;
- `conflicting`.

These labels describe provenance, not authority, safety, or permission to load.
`measurement_supported_interval` must identify the actual measured points and
must not imply that unmeasured interior points were tested.

## Explicitly Permitted Behavior

A separately authorized implementation may:

- retain finite, explicitly unit-tagged charge-mass bounds and endpoint rules;
- retain multiple disjoint segments without filling gaps;
- preserve exact source values separately from rounded display values;
- represent empty, unavailable, indeterminate, and conflicting region states;
- reference exact M01/M02 inputs and exact M03 diagnostics;
- reference M04 outcomes as audit dependencies without treating passes as
  scientific validation;
- retain pressure records as contextual evidence with exact pressure quantity,
  method, standard, units, conditions, and source limits;
- report derivation lineage and non-implications.

## Explicitly Prohibited Behavior

Real-component loading instructions; recommended, optimal, preferred, starting,
or maximum charge language; safety, pressure-tested, or validated claims beyond
the exact evidence; catalog discovery; powder selection; ranking or scoring;
point or midpoint recommendations; automatic rounding; hidden tolerances;
unsupported interpolation or extrapolation; probability claims without a
defined basis; default source preference; averaging conflicts; gross/net
capacity substitution; silent conversion among charge mass, fill fraction,
loading density, and volume; silent `0.80` or `0.86` factors; the quarantined
charge regression; pressure, velocity, burn, burnout, or muzzle-pressure
prediction; and loading-manual replacement behavior.

No region may be called safe, suitable, approved, recommended, or validated
merely because it is bounded or because an M04 criterion passed.

## Required Data And Record Models

A future implementation must define separate immutable concepts for:

- region identity and version;
- method or basis identity and version;
- charge-mass segment with lower/upper bound and endpoint inclusion;
- region state: bounded segments, empty, unavailable, indeterminate, or
  conflicting;
- exact input-record and diagnostic references;
- source identity and locator;
- evidence class and model maturity;
- applicability domain and measurement conditions;
- uncertainty status and qualifications;
- conflict members and unresolved reason;
- derivation lineage;
- activation and supersession as independent fields;
- explicit non-implication statements.

One record may contain multiple ordered, non-overlapping segments. Disjoint
segments must never be enveloped into a single continuous interval. A point
segment is permitted only when the source or method explicitly yields that
point; it remains an analytical record, not a point recommendation.

Determinate segment bounds must be finite, dimensionally compatible charge
masses, ordered, and physically positive. Open-ended or missing bounds must be
retained as source constraints or non-determinate region states rather than
silently converted into a bounded region. Empty intersections are explicit;
partial or unresolved intersections are indeterminate; conflicts retain all
members.

## Evidence And Provenance Boundaries

Every future record must retain its source, locator, exact inputs, units,
conditions, domain, evidence class, maturity, uncertainty status, method version,
qualifications, and lineage. A derived record is a `derived_quantity`; it retains
all material input evidence classes and must not claim stronger admission or
maturity than any material input permits. Evidence classes are not an automatic
preference ordering.

Original Powley and Davis arithmetic remain historical method records, not
modern safety bounds. Manufacturer data may support a source-declared interval
only after the exact publication, components, lot where available, pressure
quantity, standard, conditions, and domain are retained. Laboratory or user
measurements require method, apparatus, conditions, uncertainty, and actual
sample identities. Emulator, GRT, jRT, QuickLOAD, regressions, and legacy
artifacts remain contextual or experimental unless separately promoted.

An uncertainty interval is not a charge region. Unknown dependence or
correlation remains explicit. No uncertainty propagation arithmetic is
authorized by this specification.

## Namespace And Dependency Boundaries

Any future M05 code must remain under `modern_powley.modernized` and may depend
only on promoted M01-M04 contracts. M01 owns quantities, geometry, capacity
identities, provenance, and uncertainty. M02 owns neutral observations,
missingness, conflicts, conditions, and domains. M03 owns completeness and
literal applicability diagnostics. M04 owns criteria and recorded outcomes.

M05 must reference exact underlying M01/M02 evidence and exact relevant M03
diagnostics. An M04 outcome may be retained as an audit dependency but cannot
replace underlying evidence or establish a scientific region. M05 must not
import `later/`, `experimental/`, emulator, GRT, jRT, QuickLOAD, or legacy code.
`original/` must not depend on M05.

## Serialization Requirements

A future implementation may propose `modern_powley.m05.v1` only after explicit
authorization. The serializer must be strict and versioned, reject unknown
fields/types/versions and non-finite numbers, preserve explicit tagged unions,
units, endpoint semantics, disjoint segments, missing/conflict states, exact
references, and source wording, and perform no implicit migration or field
dropping. M01-M04 serialization semantics must remain unchanged.

This planning milestone creates no schema implementation and no package export.

## Required Repository Deliverables

A future authorized implementation would require: bounded-region records;
controlled basis and state vocabularies; strict serializer; synthetic fixtures;
unit, endpoint, disjoint-region, missing/conflict, provenance, architecture, and
serialization tests; design document; implementation decision record; ledger
entries for actual admitted definitions; documentation; and a completion review.
No production powder or load dataset is required or authorized merely to test
the record contract.

## Required Policy Decisions

Before implementation authorization, resolve or reaffirm:

1. whether the first increment is records-only or admits literal intersection;
2. exact segment normalization without merging gaps;
3. handling of overlapping segments from the same declared source;
4. whether open-ended source constraints are only contextual records;
5. exact meanings and permitted uses of every basis category;
6. dependency/correlation representation without propagation arithmetic;
7. representation of source rounding versus measurement uncertainty;
8. activation and supersession behavior without deletion;
9. minimum provenance for manufacturer and measured evidence;
10. pressure-quantity and pressure-standard metadata requirements;
11. whether any real evidence is admitted for production M05 records;
12. explicit prohibition on automatic discovery, preference, fallback, and
    conflict resolution.

## Acceptance Gates

Predeclared gates for a future implementation are:

1. A separately reviewed planning commit changes status to `authorized` before
   source implementation begins.
2. M01-M04 APIs and schemas remain unchanged.
3. Region, source load interval, fill constraint, uncertainty interval, and
   pressure limit are distinct record concepts.
4. Every record retains method/version, exact inputs, provenance, units, domain,
   conditions, uncertainty, qualifications, conflicts, and lineage.
5. Bounds are finite compatible charge masses with explicit endpoints; invalid,
   negative, zero, reversed, NaN, and infinite determinate bounds fail.
6. Point, empty, open-ended, missing, unavailable, indeterminate, conflicting,
   duplicate, and superseded cases are explicit.
7. Multiple disjoint segments are preserved; no gap is filled or midpoint
   selected.
8. An uncertainty interval never automatically becomes a charge region and no
   undisclosed propagation occurs.
9. Pressure quantity, method, standard, and units remain explicit; no CUP/PSI
   conversion or safety inference exists.
10. Exact M01/M02 evidence and M03 diagnostics are referenced; M04 passes never
    substitute for scientific evidence.
11. No discovery, source preference, alias inference, averaging, substitution,
    fallback, interpolation, extrapolation, rounding, or recommendation exists.
12. No powder selection, charge calculation, pressure/velocity/burn prediction,
    ranking, scoring, solver, safety, or suitability behavior exists.
13. Strict future serialization round trips and prior schemas remain unchanged.
14. No quarantined data or method is promoted; any real record has explicit
    authorization and provenance.
15. Architecture, documentation, ledgers, tests, scope review, full validation,
    and completion review pass before status can become `accepted`.

## Required Validation Commands

Future implementation validation must include `uv sync --locked --offline`,
`uv lock --check`, `uv run pytest -q`, focused M05 tests, `uv run python -m
compileall -q src tests scripts`, `git diff --check`, and repository CSV, JSON,
notebook, Markdown-link, artifact-hash, controlled-vocabulary, package-import,
circular-boundary, milestone-governance, and roadmap/status checks.

## Scope-Control Review Checklist

Confirm no original/prior-schema change; no real load instruction; no production
method or data without authorization; no charge recommendation, point/midpoint
selection, automatic rounding, source discovery/preference, conflict resolution,
capacity substitution, implicit factor, hidden default/tolerance, interpolation,
extrapolation, probability claim, safety/suitability implication, ballistics
prediction, quarantined-source promotion, or loading-manual replacement.

## Completion-Report Requirements

Report initial/final state; authorization commit; files and public API; region,
basis, segment, state, uncertainty, pressure, provenance, conflict, activation,
and supersession semantics; exact M01-M04 dependencies; admitted evidence;
unavailable behavior; every gate; exact validation; scope review; commit/push;
remaining limitations; and the next bounded recommendation. A recommendation
must not authorize M06.

## Commit And Release Expectations

This planning specification is committed separately as documentation and remains
`planned`. A future user authorization must change it to `authorized` in a
reviewed planning commit before implementation. Implementation must use a later
bounded commit, never amend this planning commit, and preserve historical tags.

## Known Limitations

No retained production evidence currently establishes a modern charge-region
method. No manufacturer load dataset or qualified independent measurement set is
retained. M02 contains no production powder database. Geometry/fill constraints
cannot become charge mass without explicitly sourced powder-volume semantics.
No uncertainty propagation or dependency model is authorized. Cross-standard
pressure comparison remains unresolved.

## Authorized Next-Milestone Boundary

Only evidence review, specification amendment, and a user authorization review
are permitted next. Numerical implementation, serializer creation, package
exports, real region construction, and M06 work remain unauthorized. A review
recommendation is not authorization.

## Implementation Decisions And Completion Evidence

Specification-level decisions are recorded in
[`M05_specification_decisions.md`](../decisions/M05_specification_decisions.md).
The planning evidence review is
[`M05_evidence_and_semantics_review.md`](../reviews/M05_evidence_and_semantics_review.md).
There is no M05 implementation decision record or completion review because M05
is not authorized or implemented.
