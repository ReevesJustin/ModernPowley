# M01 Completion Review

Status: `implemented_and_reviewed`

M01 establishes canonical physical records and deterministic geometry. It does
not select powders, estimate charges, predict pressure or velocity, model burn
progress, rank candidates, or provide loading recommendations.

## Implemented Boundary

| Area | Implementation | Primary tests |
|---|---|---|
| Dimensions and conversions | `src/modern_powley/modernized/units.py` | `tests/unit/test_m01_units_and_uncertainty.py` |
| Evidence and maturity | `src/modern_powley/modernized/provenance.py` | `tests/provenance/test_m01_provenance_and_serialization.py` |
| Bounded uncertainty | `src/modern_powley/modernized/uncertainty.py` | `tests/unit/test_m01_units_and_uncertainty.py` |
| Physical records and conditions | `src/modern_powley/modernized/records.py` | `tests/unit/test_m01_records_and_geometry.py` |
| Euclidean geometry and ratios | `src/modern_powley/modernized/geometry.py` | `tests/unit/test_m01_records_and_geometry.py` |
| Versioned serialization | `src/modern_powley/modernized/serialization.py` | `tests/provenance/test_m01_provenance_and_serialization.py` |
| Historical scalar compatibility | `src/modern_powley/modernized/adapters/original.py` | `tests/reference/test_m01_original_adapters.py` |
| Namespace and scope boundary | `tests/provenance/test_architecture.py` | same |

## Acceptance Gates

| Gate | Evidence | Result | Remaining limitation |
|---|---|---|---|
| Every dimensional field has units and provenance | `Quantity`, `PhysicalValue`, controlled provenance tests, data-field ledger | pass | Composite records carry uncertainty per dimensional value; no dimensionless aggregate bound is invented. |
| Measured and estimated capacities cannot be confused | Distinct frozen record types, comparison API, serialization dispatch tests | pass | A later phase must select a capacity record explicitly. |
| Dimensional invariants and invalid inputs | Unit and geometry tests | pass | M01 supports only its declared shape domain. |
| Unit conversions round-trip | Exact-definition and binary64 tolerance tests | pass | Only M01-required units are exposed. |
| Water conversion is explicit | Supplied-density and named Powley-convention tests | pass | M01 supplies no default water density. |
| Original scalars consume compatible adapters unchanged | Original adapter reference tests and unchanged `original/` tree | pass | Missing historical graphical operations remain unavailable. |
| Geometry edges and outside-model states | Partial/full boat-tail, limiting, invalid, and adequacy tests | pass | Ogives and complex seated shapes remain outside model. |
| No modern behavior enters `original/` | Import-direction architecture test | pass | Adapter dependency is one-way only. |
| No ballistics prediction, screening, ranking, or interface | Public API and vocabulary architecture tests | pass | These capabilities require later phase authorization. |
| Schema, implementation, tests, and decisions reviewed | `modern_powley.m01.v1`, decision record, ledger-coverage test, this review | pass | Future schema changes require explicit migrations. |

## Provenance And Units

Exact customary-to-SI conversions are registered under `SRC-NIST-SP811` and
`CONST-042` through `CONST-045`. Direct geometry is project-derived and uses
stable `M01-*` method identities in the equation ledger. The Powley
`253 gr H2O/in3` convention remains `EQ-105`, an explicit source-specific choice
rather than a modern default.

## Intentionally Unavailable

M01 has no powder-property model, physical powder fill fraction, powder
selection, charge or charge-region estimator, pressure or velocity predictor,
burn-progress or burnout model, muzzle-pressure estimator, calibration,
regression, ranking score, CLI, notebook, or application interface. No
primer-pocket geometry is inferred. No probability distribution or statistical
uncertainty propagation is implemented.

## Decision

All independently supportable M01 acceptance gates pass. M01 is promoted as the
canonical modernized input and geometry layer. M02 subsequently implemented the
neutral powder-property evidence contract without changing M01 quantity
identities or introducing prediction behavior.
