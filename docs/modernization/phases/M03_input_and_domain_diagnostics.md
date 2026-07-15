# M03: Input Completeness And Literal Domain Diagnostics

## Status And Scope

Status: `implemented_and_reviewed`

M03 is a diagnostic layer over explicit M01 inputs and M02 applicability
domains. It reports whether the declared conditions for one named existing M01
operation are satisfied and explains literal domain comparisons. It does not
execute geometry, prepare a solver, screen powders, select observations, or
establish physical correctness, suitability, or safety.

## Requirement Sets

Every production requirement set is immutable, named, versioned, attributed to
`SRC-M03-DESIGN`, and bound to an existing M01 operation. Sets cover:

- circle area;
- cylinder and conical-frustum volume;
- flat, partial-boat-tail, and full-boat-tail seated displacement;
- barrel swept volume;
- measured-versus-estimated capacity comparison;
- geometric usable-space estimate inputs and primer-pocket basis correction;
- barrel volume ratio and total expansion ratio.

No set describes powder screening, charge, pressure, velocity, burn,
optimization, safety, ranking, or solver execution.

## Completeness Meaning

`all_declared_conditions_satisfied` means only that every required or active
conditional requirement in that exact set was satisfied by explicit candidates.
Detailed diagnostics are always retained. Inputs are never calculated, inferred,
selected, averaged, or defaulted. Gross, measured usable, estimated usable, and
primer-pocket capacities use non-substitutable record kinds.

Flat-base, partial-boat-tail, and full-boat-tail branches require an explicit
controlled branch input. Partial/full intrusion relationships and tail-base versus
shank diameter are checked literally against the existing M01 shape domain. No
projectile shape is detected or approximated.

## Literal Applicability

M03 compares one specific query with one specific M02 observation. Each declared
numeric, categorical, or literal source-scalar constraint produces a separate
diagnostic retaining the query and declared constraint.

- Compatible M01 units may be converted to canonical SI for comparison.
- Source scalars require exact reported units and conventions.
- Categories and identifiers use literal matching and the existing case policy.
- Inclusive and exclusive endpoints remain distinct.
- A query interval is inside only when fully contained and outside only when
  disjoint; partial overlap is indeterminate.
- An unspecified domain produces `no_declared_domain_supplied`, never a pass.
- Missing, explicitly unavailable, incompatible-unit, and definition-mismatch
  results remain distinct.

`all_declared_constraints_satisfied` means only that the supplied query did not
violate the literal constraints declared for that observation. It is not a
powder suitability, validity, eligibility, or safety classification.

## Serialization

Records use strict `modern_powley.m03.v1` JSON-compatible serialization. The
schema covers requirement sets, input bundles, completeness evaluations, domain
query contexts, and applicability evaluations. Unknown fields, malformed tagged
values, unsupported schema versions, non-finite numbers, and malformed units or
bounds fail explicitly. M01 and M02 schema semantics are unchanged.

## Exclusions

M03 contains no production powder data, screening, matching, ranking, source
preference, automatic conflict resolution, interpolation, extrapolation,
geometry approximation, capacity fallback, pressure, velocity, burn model,
charge determination, optimization, calibration, solver, or recommendation.
