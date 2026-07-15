# M04: Declarative Screening Criteria And Auditable Outcome Records

## Status And Scope

Status: `implemented_and_reviewed` after all acceptance gates pass.

M04 provides an immutable audit-trail contract for criteria and explicitly
supplied evidence. It does not discover observations, iterate a powder catalog,
screen candidates, rank outcomes, establish suitability or safety, or predict
ballistic behavior.

## Record Model

- `CriterionDefinition` separates role, activation status, controlled form,
  exact evidence IDs, threshold, authority, provenance, limitations and version.
- `CriterionSetDefinition` retains exact criterion versions and display order.
  It has no weights, scores, priorities, or selection semantics.
- `EvidenceReference` retains one exact source record and one tagged literal
  value, M02 missing state, M03 diagnostic status, or conflict declaration.
- `EvaluationContext` states exactly which evidence records, subject identities,
  schema versions, repository commit, purpose and exclusions were supplied.
- `CriterionEvaluationRecord` retains exact versions, values, comparison,
  threshold, result, reason, dependencies, conflicts, method and provenance.
- `CriterionSetOutcomeRecord` summarizes recorded active mandatory outcomes with
  descriptive counts and an explicit non-implication statement.

No production criterion definitions or criterion sets are instantiated by the
package. Test records use only conspicuous `SYNTHETIC-M04-*` identities.

## Controlled Forms

M04 admits exact reference presence, prohibited missing-state absence, exact M03
diagnostic classification, exact category or identifier equality, membership in
a finite literal set, four explicit one-sided numeric bounds, point-in-interval,
full interval containment, explicit no-conflict declaration, and visible manual
assertion. There is no callback, expression string, query language, or dynamic
rule execution.

Compatible M01 dimensions convert to SI for exact comparison. Endpoint inclusion
is explicit. A fully contained interval passes, a disjoint interval fails, and a
partial overlap is indeterminate. No tolerance, distribution, midpoint,
interpolation, extrapolation, or inferred threshold is used.

## Evidence And Diagnostic Reuse

The caller supplies exact reference IDs. M04 never searches, resolves aliases,
prefers a source, chooses among lots, averages observations, or fills missing
data. M03 completeness and domain diagnostics enter only through exact retained
diagnostic references and controlled status strings. M04 does not repeat M03
comparison logic and does not turn an unspecified domain into a pass.

## Outcome Meaning

A criterion pass means only that explicitly supplied evidence satisfied that
exact criterion version under the retained context. An
`all_mandatory_recorded_passes` summary means only that every active mandatory
criterion in that exact set version has a recorded pass. Neither result
establishes physical correctness, powder suitability, safety, approval,
recommendation, or solver readiness.

Manual assertions retain the responsible party, date, rationale, evidence,
review status, evidence class, maturity, verification state, and qualifications.
They cannot be produced by the mechanical evaluator and never masquerade as a
literal comparison.

## Serialization

Strict `modern_powley.m04.v1` covers criterion definitions, criterion-set
definitions, evaluation contexts, criterion evaluations, and criterion-set
outcomes. Unknown fields/types/versions and malformed embedded thresholds or
evidence fail. JSON encoding rejects NaN and infinity. M01-M03 schemas are
unchanged and no migration is implicit.

## Exclusions

M04 has no production powder records, production criteria, collection search,
record discovery, alias resolution, fallback, preference, conflict resolution,
weights, scores, ranking, tie breaking, pass-percentage selection, screening,
suitability, safety, recommendation, charge, pressure, velocity, combustion,
muzzle pressure, solver, calibration, regression, optimization, interpolation,
extrapolation, CLI, notebook, or application interface.

## Governance

The canonical scope authority is
[`M04_screening_decision_records.md`](../milestones/M04_screening_decision_records.md).
Implementation decisions and completion evidence remain separate. M01-M04 have
durable specifications; M05 is only a future recommendation until a separate
specification-first authorization commit exists.
