# M04: Screening Decision Records

## Status

`accepted`

This specification is the scope authority for M04. It existed with status
`in_progress` before M04 was marked accepted. All gates below, including Gate
18, passed without changing their predeclared meaning.

## Purpose

Define immutable declarative criteria, criterion sets, evaluation contexts,
criterion outcomes, and descriptive set outcomes that retain an exact audit
chain. M04 records decisions over explicitly supplied evidence; it is not a
general powder-screening engine.

## Starting Repository State Or Predecessor

Predecessor: accepted M03 at `bf388c870ca04e15eaf74f237c1ae9438169c026`,
clean synchronized `main`, with preservation tag `08e4ee0` unchanged.

## Scope

Versioned definitions and roles/statuses; controlled literal forms; exact M01,
M02 and M03 evidence references; explicit manual assertions; narrow mechanical
literal evaluation; descriptive active-mandatory aggregation; strict
`modern_powley.m04.v1`; documentation, governance, tests, and ledgers.

## Explicitly Permitted Behavior

- Declare precise presence, missing-state, M03-status, category, identifier,
  bound, interval-containment, no-conflict, and manual-assertion criteria.
- Evaluate a criterion only against exact caller-supplied reference IDs.
- Retain passes, failures, unavailable, conflicting, incompatible,
  indeterminate, inactive, superseded, and unevaluated outcomes with reasons.
- Summarize whether exact active mandatory criteria have recorded passes,
  failures, indeterminate states, or missing evaluations.

## Explicitly Prohibited Behavior

Callbacks or expression languages; record discovery; alias resolution; fallback;
source preference; conflict resolution; production powder catalog or criterion
set; scores, weights, rankings, tie breaks, pass-percentage selection; safety,
suitability, approval, recommendation, solver readiness; charge, pressure,
velocity, burn, or muzzle prediction; interpolation, extrapolation, calibration,
regression, or optimization.

## Required Data And Record Models

Controlled criterion role/status/form; literal/finite/missing/bound/interval
thresholds; exact criterion references; criterion-set definition; tagged exact
evidence reference; evaluation context; manual assertion detail; criterion
evaluation; descriptive counts; criterion-set outcome.

## Evidence And Provenance Boundaries

Every definition and result retains project/source authority, evidence class,
maturity, locator, versions, dependencies and qualifications. M03 diagnostics
are referenced exactly, never recomputed. No real powder records or quarantined
sources are populated; tests use conspicuous `SYNTHETIC-M04-*` records.

## Namespace And Dependency Boundaries

M04 remains in `modernized/` and depends only on promoted M01-M03 contracts.
No import from `later/`, `experimental/`, emulator, GRT, jRT, QuickLOAD, or
legacy code. `original/` cannot import `modernized/` and cannot change.

## Serialization Requirements

Strict `modern_powley.m04.v1`; required schema/record type and exact criterion/set
versions; explicit unions/statuses/method/source/evidence/conflict; unknown fields,
record types, future versions, malformed units/intervals/unions, NaN and infinity
rejected; no implicit migration; M01-M03 behavior unchanged.

## Required Repository Deliverables

M04 definition, context, outcome, evaluator and serializer modules; unit,
serialization, architecture, scope and governance tests; design document;
decision record; completion review; source/equation/field ledgers; README, TODO,
usage and roadmap updates; canonical M01-M04 specifications.

## Required Policy Decisions

Definition/outcome and criterion/set separation; roles/statuses/versioning;
supported forms; narrow evaluation boundary; manual versus mechanical results;
exact references and no discovery; conflict/missing treatment; M03 reuse;
boundary/interval/definition rules; meanings and non-implications of passes;
no scores/production sets; synthetic policy; schema compatibility; namespace;
and safety/suitability/recommendation prohibitions.

## Acceptance Gates

1. Starting-state integrity.
2. Immutable versioned definitions/sets; controlled roles/statuses; no expressions.
3. Exact supplied inputs; no discovery, aliases, fallback, or inference.
4. Controlled outcomes with exact pass/failure/indeterminate evidence.
5. Mandatory/advisory/informational separation; no weights; positive meaning bounded.
6. Exact versions; mismatch and supersession explicit; no migration.
7. M02 missing/conflict states retained; no winner or silent pass.
8. Exact M03 diagnostics reused; no duplicated domain/completeness logic.
9. M01 dimensional thresholds; exact endpoints and interval containment.
10. No collection discovery, selection, aliases, defaults, or resolution.
11. No scores, weights, rankings, ties, or pass-percentage selection.
12. Strict M04 serialization; M01-M03 unchanged.
13. Architecture isolation and unchanged original behavior.
14. No ballistics, solver, calibration, safety, suitability, or recommendation leakage.
15. No production database/source promotion; synthetic tests only.
16. Design, decisions, review, ledgers, inventory, entry points complete.
17. Full validation suite passes.
18. Durable milestone governance: canonical M01-M04 specifications contain all
    required sections; accepted historical scopes remain intact; roadmap links
    specifications, decisions, reviews, ledgers and tests; AGENTS requires
    specification-first future work and traceable amendments; tests enforce the
    contract; M04 is not accepted before these conditions pass.

## Required Validation Commands

`uv sync --locked --offline`; `uv lock --check`; `uv run pytest -q`; focused M04
unit/provenance/serialization/architecture/governance tests; `uv run python -m
compileall -q src tests scripts`; `git diff --check`; CSV, JSON, notebook,
Markdown-link, artifact-hash, controlled-vocabulary, package-import, circular
dependency, serialization-compatibility, roadmap and status validators.

## Scope-Control Review Checklist

No original or prior-schema change; no real powder/criterion population; no
collection search, selection, alias/conflict resolution, default/preference,
score/weight/ranking, suitability/safety/approval language, duplicated M03 logic,
unspecified-domain pass, interpolation/extrapolation/tolerance/probability,
missing inference, source promotion, ballistics prediction, or recommendation.

## Completion-Report Requirements

Report state, files, definition/role/form/set/context/outcome models, manual versus
mechanical policy, exact references, missing/conflict/boundary behavior, schema,
evidence restraint, unavailable behavior, all 18 gates, exact validation, commit/
push/final state, unresolved issues, and M05 recommendation. Also report the four
specifications, M01-M03 reconstruction and discrepancies, roadmap links, AGENTS
changes, governance tests/statuses, M04 specification-before-acceptance, and that
M05 is recommended but not authorized.

## Commit And Release Expectations

After every gate passes, mark this specification `accepted`, commit as
`feat: implement M04 screening decision records`, push normally, verify clean
synchronization, and preserve the historical tag. No amend, squash, or force push.

## Known Limitations

M04 cannot establish threshold correctness, discover evidence, screen a catalog,
determine powder suitability/safety, rank candidates, or predict ballistics. A
manual assertion remains an assertion. A positive set summary has only its
literal recorded-mandatory meaning.

## Authorized Next-Milestone Boundary

No M05 work is authorized by this specification. The completion review may
recommend a bounded M05 planning topic, but M05 requires its own canonical
specification, review, planning commit, and explicit `authorized` status before
implementation.

## Implementation Decisions And Completion Evidence

Binding refinements are recorded in
[`M04_implementation_decisions.md`](../decisions/M04_implementation_decisions.md).
Completion evidence will be recorded separately in
[`M04_completion_review.md`](../reviews/M04_completion_review.md), tests, and
ledger entries; this specification is not replaced by those records.
