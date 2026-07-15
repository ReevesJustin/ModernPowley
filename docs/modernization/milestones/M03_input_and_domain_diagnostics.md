# M03: Input and Domain Diagnostics

## Status

`accepted`

This specification was backfilled during M04 from the accepted M03 prompt,
design, decisions, implementation, tests, ledgers, and completion review.

## Purpose

Explain whether explicit inputs satisfy one named existing M01 operation and
whether one literal query satisfies one exact M02 observation domain. The layer
is diagnostic, not solver preparation or powder evaluation.

## Starting Repository State Or Predecessor

Predecessor: accepted M02 at `1089aac`. Accepted M03 was completed at
`bf388c8`.

## Scope

Immutable, versioned requirement sets for existing M01 operations; explicit
input bundles; per-requirement completeness diagnostics; explicit query records;
per-constraint domain diagnostics; aggregate diagnostic summaries; strict
`modern_powley.m03.v1` serialization.

## Explicitly Permitted Behavior

- Inspect exact supplied candidates without computing missing inputs.
- Distinguish presence, missingness, incompatibility, conflict, branch and
  indeterminate states for named requirements.
- Compare literal points/intervals/categories/identifiers with declared M02
  domain constraints and preserve exact rejection reasons.
- Convert compatible supplied M01 quantities only for literal comparison.

## Explicitly Prohibited Behavior

Universal completeness; future solver requirement sets; value inference;
capacity substitution/fallback; geometry approximation; source or record
selection; fuzzy/alias matching; interpolation/extrapolation; powder screening,
suitability, ranking, prediction, optimization, calibration, safety, or advice.

## Required Data And Record Models

Requirement kind, input candidate kind, conditional geometry branch, requirement
set, input bundle, completeness diagnostic/evaluation, domain query value/context,
constraint diagnostic, and applicability evaluation. Capacity types and M02
missing states remain non-substitutable.

## Evidence And Provenance Boundaries

Production sets describe only promoted M01 operations. No powder facts or
quarantined sources were introduced. `SRC-M03-DESIGN` is project design
authority. Tests use `SYNTHETIC-M03-*` inputs.

## Namespace And Dependency Boundaries

M03 is under `modernized/` and may depend on M01/M02 only. No imports from
`later/`, `experimental/`, emulator, GRT, jRT, or legacy code. `original/`
remains independent and numerically unchanged.

## Serialization Requirements

Strict `modern_powley.m03.v1`; explicit set versions, tagged candidates, missing
and indeterminate statuses, query/constraint operands; unknown fields, malformed
unions/units/bounds, future versions, NaN and infinity rejected; M01/M02 schemas
unchanged.

## Required Repository Deliverables

Requirement, completeness, domain-query/diagnostic and serialization modules;
production M01-operation sets; tests; phase design; decision record; ledgers;
completion review; status/usage updates.

## Required Policy Decisions

Named relative completeness; production operation list; required/optional/
conditional inputs; geometry branches; presence versus validity/applicability;
capacity non-substitution; multiple values; missing states; positive-summary
meaning; unspecified domain; exact endpoints; interval containment/overlap;
literal definitions/categories; serialization; no readiness/suitability language.

## Acceptance Gates

1. Starting-state integrity.
2. Named/versioned sets only for existing M01 operations.
3. No inference, fallback, hidden defaults, or conflict selection.
4. Structured per-requirement diagnostics retained with summaries.
5. Gross/measured/estimated/primer capacities remain distinct.
6. Explicit flat/partial/full geometry branches; unsupported stays unsupported.
7. Independent literal domain constraints and exact rejections.
8. Inclusive/exclusive and interval relations tested; non-finite fails.
9. Missing, unavailable, incompatible, unspecified and indeterminate distinct.
10. Conflicting candidates coexist without preference.
11. Strict M03 serialization; M01/M02 unchanged.
12. Architecture isolation and unchanged original behavior.
13. No screening, ranking, prediction, solver or interpolation leakage.
14. Evidence restraint and synthetic fixtures.
15. Documentation and ledgers complete.
16. Full validation passes.

## Required Validation Commands

`uv sync --locked --offline`; `uv lock --check`; `uv run pytest -q`; focused M03
unit/provenance/architecture/serialization tests; `uv run python -m compileall -q
src tests scripts`; `git diff --check`; CSV, JSON, notebook, Markdown-link,
artifact-hash, vocabulary, package-import, circular-boundary, and roadmap checks.

## Scope-Control Review Checklist

No original change or unavailable operation; no future solver set; no selected
powder property; no capacity substitution or geometry inference; no unspecified
domain pass; no suitability terminology, tolerance, interpolation, extrapolation,
uncertainty distribution, conflict resolution, hidden default, or source promotion.

## Completion-Report Requirements

Report state, files, requirement sets, diagnostic taxonomies, capacity/geometry
branches, domain and interval behavior, conflicts, schema, evidence restraint,
unavailable behavior, gate table, validation, commit/push, final state, issues,
and next bounded task.

## Commit And Release Expectations

Accepted implementation commit: `bf388c8` (`feat: implement M03 input and domain
diagnostics`). Prior schemas and preservation tag remain unchanged.

## Known Limitations

Diagnostics do not execute geometry, establish physical correctness, choose a
record, prepare a solver, or imply powder suitability or safety.

## Authorized Next-Milestone Boundary

M04 was authorized only for declarative criterion definitions and auditable
recorded outcomes over exact supplied M01-M03 evidence. No catalog screening,
ranking, prediction, or production criterion set was authorized.

## Accepted Decisions And Completion Evidence

See [`M03_implementation_decisions.md`](../decisions/M03_implementation_decisions.md),
[`M03_completion_review.md`](../reviews/M03_completion_review.md), `tests/unit/test_m03_*`,
`tests/provenance/test_m03_*`, and ledger entries `EQ-110` through `EQ-112`.

## Historical Discrepancies Or Refinements

M03 implemented interval comparisons conservatively: full containment passes,
disjointness rejects, and partial overlap is indeterminate. This was explicitly
permitted and did not broaden the diagnostic scope.
