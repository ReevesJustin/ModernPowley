# M01: Canonical Inputs and Geometry

## Status

`accepted`

This canonical specification was backfilled during M04 from the accepted M01
authorization, phase design, decision record, implementation, tests, ledgers,
and completion review. It records the scope that governed M01; it does not
retroactively broaden that scope.

## Purpose

Establish immutable, provenance-aware dimensional inputs, canonical SI
normalization, explicit uncertainty, strict v1 serialization, transparent
Euclidean geometry, and explicit adapters to source-backed original scalar
functions. M01 is a geometry and data-contract layer, not ballistics analysis.

## Starting Repository State Or Predecessor

Predecessor: M00 program authorization at commit `be7c27f`. Accepted M01 was
completed at commit `5b5aaf9`.

## Scope

Typed length, area, volume, mass, temperature, and ratio quantities; evidence,
origin, maturity, uncertainty, measurement vocabularies; cartridge, projectile,
capacity, and firearm records; direct geometry; water mass/volume conversions;
strict `modern_powley.m01.v1`; and explicit historical scalar adapters.

## Explicitly Permitted Behavior

- Exact standard-unit conversion through explicit units and canonical SI.
- Circle, cylinder, frustum, projectile-intrusion, barrel-volume, capacity,
  sectional-density, mass-ratio, and explicitly named expansion calculations.
- Direct seating-depth derivation only from compatible explicit reference data.
- Explicit comparison of measured and estimated usable space without selection.
- Historical scalar calls through the dedicated adapter with named conventions.

## Explicitly Prohibited Behavior

Powder data or selection; charge estimation; pressure, velocity, burn, burnout,
or muzzle-pressure prediction; ranking; regression; calibration; hidden units;
implicit water density; implicit diameter choice; capacity fallback; interfaces;
and loading recommendations. No modern behavior may enter `original/`.

## Required Data And Record Models

`Quantity`, `PhysicalValue`, tagged `Uncertainty`, `Provenance`, controlled
measurement enums, distinct gross/measured/estimated/primer-pocket capacity
records, projectile and firearm records, derived geometry records, and stable
record identities. Measured and estimated capacities are non-interchangeable.

## Evidence And Provenance Boundaries

Every supplied scientific value declares evidence class, origin, source, and
uncertainty. Exact conversions use `SRC-NIST-SP811`; direct Euclidean methods use
`SRC-M01-DESIGN`. The source-specific Powley 253 gr H2O/in3 convention is
available only by explicit selection and is not a universal water density.

## Namespace And Dependency Boundaries

M01 lives in `modernized/`. `original/` cannot import `modernized/`.
`modernized/adapters/original.py` is the only allowed modern-to-original adapter
path. No later, experimental, emulator, GRT, or legacy code is promoted.

## Serialization Requirements

Strict `modern_powley.m01.v1`; schema and record type required; explicit quantity
value/unit; unknown fields, unsupported versions, malformed unions, incompatible
units, NaN, and infinity rejected; deterministic JSON; no implicit migration.

## Required Repository Deliverables

M01 modules, adapters, tests, phase design, decision record, ledgers, completion
review, and entry-point status updates. No production data artifact was required.

## Required Policy Decisions

Standard-library immutable types; canonical SI; explicit source units; strict
JSON v1; bounded uncertainty; controlled measurement states; no inferred primer
pocket; distinct measured/estimated capacity; explicit water convention;
`barrel_volume_ratio` versus `total_expansion_ratio`; and no bare
`loading_density` or `expansion_ratio` field.

## Acceptance Gates

1. Starting commit, clean tree, synchronized remote, and preservation tag.
2. Dimensional types and exact supported conversions.
3. Provenance and explicit uncertainty for supplied values.
4. Strict serialization and migration refusal.
5. Capacity identities cannot substitute or overwrite one another.
6. Primer-pocket ambiguity fails when material.
7. Geometry invariants and boat-tail edge cases pass.
8. Explicit firearm diameters and projectile-travel reference points.
9. No implicit water-density or diameter convention.
10. Historical adapters reproduce unchanged original scalar results.
11. Architecture isolation and no M02-or-later behavior.
12. Documentation, ledgers, full tests, compile, and diff checks pass.

## Required Validation Commands

`uv sync --locked --offline`; `uv lock --check`; `uv run pytest -q`; focused M01
unit/provenance/architecture/reference tests; `uv run python -m compileall -q src
tests scripts`; `git diff --check`; CSV, JSON, notebook, Markdown-link, source-hash,
package-import, and circular-dependency validators.

## Scope-Control Review Checklist

Confirm no `original/` arithmetic or source value changed; no implicit capacity,
water, or diameter choice; no ambiguous expansion/loading-density field; no
prediction, recommendation, later, or experimental behavior; all public values
carry units; serialization round trips; and every completion gate has a test.

## Completion-Report Requirements

Report state, files, design/API, units, provenance, uncertainty, serialization,
measurement vocabularies, capacity and geometry behavior, adapters, ledgers,
tests, gate matrix, validation, exclusions, commit/push, final state, and next
bounded phase.

## Commit And Release Expectations

Accepted implementation commit: `5b5aaf9` (`feat: implement M01 canonical inputs
and geometry`). No amendment, history rewrite, or preservation-tag movement.

## Known Limitations

No powder-property semantics or production data; no statistical uncertainty
propagation; no inferred primer-pocket geometry; and no ballistic prediction.

## Authorized Next-Milestone Boundary

M02 was authorized only to define neutral powder identity/property evidence,
missingness, domains, conflicts, and serialization. M01 acceptance did not
authorize screening or ballistics behavior.

## Accepted Decisions And Completion Evidence

Binding refinements are in
[`M01_implementation_decisions.md`](../decisions/M01_implementation_decisions.md).
Evidence is in [`M01_completion_review.md`](../reviews/M01_completion_review.md),
`tests/unit/test_m01_*`, `tests/provenance/test_m01_*`, and ledger entries
`EQ-100` through `EQ-107`.

## Historical Discrepancies Or Refinements

No accepted gate was removed. The implementation used explicit record-specific
serializers and conservative uncertainty labels, refining file organization but
not broadening the authorized behavior.
