# M02: Powder Property Records

## Status

`accepted`

This specification was backfilled during M04 from the accepted M02 prompt,
design, decisions, implementation, tests, ledgers, and completion review.

## Purpose

Represent powder identity, source-bounded property observations, semantic
missingness, literal applicability domains, and unresolved conflicts without
assigning computational meaning, preference, suitability, or authority.

## Starting Repository State Or Predecessor

Predecessor: accepted M01 at `5b5aaf9`. Accepted M02 was completed at
`1089aac`.

## Scope

Immutable powder identities and directional relationships; controlled property
definitions and tagged values; provenance-rich observations; semantic missing
records; explicit domains; descriptive comparisons; strict
`modern_powley.m02.v1` serialization.

## Explicitly Permitted Behavior

- Retain separate manufacturers, lots, formulations, eras, and source names.
- Represent dimensional, categorical, ordinal, textual, interval, tabular, and
  source-specific observations without collapsing definitions.
- Literal boundary/category domain membership and descriptive pair comparison.
- Preserve multiple contradictory observations and explicit missing reasons.

## Explicitly Prohibited Behavior

Alias inference; record merge or preference; automatic completion; production
powder database; interpolation/extrapolation; powder screening, ranking,
selection, charge, pressure, velocity, energy-release or burn calculations;
regression; optimization; safety classification; recommendation; or UI.

## Required Data And Record Models

Powder identity and directional relationship; property definition and tagged
value; source locator and observation context; property/missing observation;
numeric/categorical/source-scalar domain; conflict comparison; M01 quantities,
uncertainty, evidence, maturity, and provenance reused unchanged.

## Evidence And Provenance Boundaries

Schema capability does not authorize a value. No quarantined Davis, Howell,
Miller, emulator, GRT, jRT, regression, OCR, or prototype data was populated.
Tests use conspicuous `SYNTHETIC-M02-*` records. `SRC-M02-DESIGN` is project
design authority, not historical Powley evidence.

## Namespace And Dependency Boundaries

M02 is under `modernized/`, depends on M01 foundations, and imports neither
`later/` nor `experimental/`. `original/` remains independent and unchanged.

## Serialization Requirements

Strict `modern_powley.m02.v1`; stable tagged unions; explicit missing/domain/
conflict/source records; exact supplied units retained; unknown fields, future
versions, malformed values, NaN, and infinity fail; no implicit migration; M01
serialization unchanged.

## Required Repository Deliverables

Identity, property, domain, missing, observation, conflict and serialization
modules; focused tests; phase design; decision record; ledgers; completion
review; and bounded status documentation.

## Required Policy Decisions

Identity and aliases; lots/formulations; controlled and source-specific property
names; tagged dimensional/categorical values; missing taxonomy; unspecified
versus unrestricted domains; endpoint semantics; conflict preservation; M01
conversion boundary; transformation/origin mapping; synthetic fixtures; no real
facts by default; no automatic preference/interpolation/selection.

## Acceptance Gates

1. Starting-state integrity.
2. No silent identity, lot, formulation, or era merge.
3. Explicit property definition and convention.
4. Observation provenance, wording, units, and transformation retained.
5. Semantic missing states; zero is never a sentinel.
6. Explicit domains; unspecified is not universal.
7. Conflicts coexist without winner, averaging, or preference.
8. Strict M02 serialization; M01 unchanged.
9. M01 dimensional conversions only; source scalars remain literal.
10. Architecture isolation and unchanged original behavior.
11. No screening, prediction, ranking, interpolation, or solver leakage.
12. Evidence restraint and synthetic fixtures.
13. Complete design, decisions, ledgers, tests, and review.
14. Full repository validation.

## Required Validation Commands

`uv sync --locked --offline`; `uv lock --check`; `uv run pytest -q`; focused M02
unit/provenance/architecture/serialization tests; `uv run python -m compileall -q
src tests scripts`; `git diff --check`; CSV, JSON, notebook, Markdown-link,
artifact-hash, package-import, and circular-dependency checks.

## Scope-Control Review Checklist

No original change; no production facts; no inferred alias or merged lot; no
missing-as-zero; no unspecified-as-unrestricted; no automatic conflict result;
no hidden default, interpolation, extrapolation, screening, suitability, safety,
prediction, or recommendation.

## Completion-Report Requirements

Report state, files, record types, identity/property/missing/domain/conflict
policies, schema, quarantine review, unavailable behavior, gate matrix,
validation, commit/push, final state, unresolved items, and next bounded task.

## Commit And Release Expectations

Accepted implementation commit: `1089aac` (`feat: implement M02 powder property
records`). Preservation tag and prior schemas remain unchanged.

## Known Limitations

No authoritative populated powder records; no property truth or interchangeability
decision; source-specific dimensions may remain unconverted; no selection logic.

## Authorized Next-Milestone Boundary

M03 was authorized only for named M01 input-completeness diagnostics and literal
M02 domain-query diagnostics. M02 acceptance did not authorize screening.

## Accepted Decisions And Completion Evidence

See [`M02_implementation_decisions.md`](../decisions/M02_implementation_decisions.md),
[`M02_completion_review.md`](../reviews/M02_completion_review.md), `tests/unit/test_m02_*`,
`tests/provenance/test_m02_*`, and ledger entries `EQ-108` and `EQ-109`.

## Historical Discrepancies Or Refinements

The implementation retained unrecognized dimensional-looking reports as
source-specific scalars rather than speculatively expanding M01 units. This is a
conservative narrowing, not a removed gate.
