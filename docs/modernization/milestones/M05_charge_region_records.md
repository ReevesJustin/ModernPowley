# M05: Charge Region Records

## Status

`authorized`

M05 is authorized only for the immutable records, structural validation, and
strict serialization increment defined here. This authorization commit does not
implement or accept M05. It admits no production method or dataset and
authorizes no numerical creation or transformation of a region.

## Purpose

Define a versioned record contract for one or more explicitly supplied bounded
analytical charge-region segments and non-numeric region states. A record is not
a recommended, preferred, starting, or maximum charge; safe region; loading
instruction; suitability statement; pressure/velocity prediction; proof that
every interior point is valid; or proof that any point was tested.

## Starting Repository State Or Predecessor

Authorization predecessor: planned M05 at
`14ae7bcf3fea70494ac61dc2aa08e0b3bf9a3a94`, following accepted M04. This
authorization pass changes documentation and governance only. Implementation
must occur in a later commit.

## Scope

The implementation may define controlled enums/identifiers, charge-mass
segments, endpoint inclusion, multiple disjoint segments, explicit region
states, exact references, method/basis identity, provenance/applicability,
conflict and lifecycle metadata, uncertainty/dependency status,
non-implications, and strict `modern_powley.m05.v1` serialization. Synthetic
fixtures may exercise the contract.

The basis vocabulary is provenance semantics:

- `source_declared_interval`;
- `measurement_supported_interval`;
- `geometry_or_fill_constraint`;
- `property_uncertainty_constraint`;
- `intersection_of_explicit_constraints`;
- `experimental_estimate`.

The region-state vocabulary is exclusively `bounded`, `empty`, `unavailable`,
`indeterminate`, and `conflicting`. Basis and state are not interchangeable.
`duplicate` is validation failure, not state. `superseded` is lifecycle metadata,
separate from state and activation.

## Explicitly Permitted Behavior

- Store immutable, versioned records and explicitly supplied finite charge-mass
  segments.
- Require caller-supplied canonical ascending segment order.
- Reject out-of-order, overlapping, and exact duplicate segments.
- Preserve disjoint gaps and explicit endpoint inclusion.
- Represent a point segment only with equal bounds and both endpoints included.
- Validate consistency between segments and the declared region state.
- Retain source text/value, normalized quantity, reported precision,
  uncertainty, dependency, evidence, maturity, domain, conditions, conflicts,
  activation, supersession, qualifications, and exact lineage.
- Serialize externally supplied basis declarations, including an intersection
  basis, without calculating the basis result.
- Retain exact pressure-evidence references as non-computational context.
- Strictly serialize and deserialize `modern_powley.m05.v1`.

## Explicitly Prohibited Behavior

Charge-region derivation; intersection, union, interval arithmetic, segment
normalization, sorting/reordering, merge, gap fill, expansion/contraction,
midpoint/point selection, automatic rounding, unit guessing, source discovery,
catalog lookup, source preference, evidence ranking, conflict resolution,
averaging, fallback, aliases, capacity substitution, fill-to-charge conversion,
loading-density arithmetic, uncertainty propagation, Monte Carlo,
pressure-to-charge calculation, any pressure/velocity/burn/burnout/muzzle
prediction, powder suitability/ranking, loading instructions, safe-region claims,
production powder/cartridge/load records or dataset ingestion, promotion of GRT,
jRT, QuickLOAD, emulator, regression, later, or experimental behavior, M06, web,
plotting, or interface implementation.

No retained value, interval, criterion outcome, pressure observation, or bounded
region may be described as safe merely because it is bounded.

## Required Data And Record Models

The implementation must provide immutable concepts for region ID/version;
method/basis ID/version; charge-mass segment and endpoint rules; region state;
exact M01/M02 input and M03 diagnostic references; optional M04 audit references;
source/locator; evidence/maturity; domain/conditions; exact source wording and
reported precision; uncertainty kind/status; declarative dependency status;
conflict members; qualifications/non-implications; derivation lineage supplied
by the caller; and independent activation/supersession metadata.

Dependency status is limited to `not_applicable`, `unknown`,
`explicitly_declared`, and `externally_referenced`. No covariance, correlation,
joint distribution, or propagated bound is calculated.

## Segment And Bound Policy

A bounded record contains one or more caller-ordered segments. Each determinate
bound is finite, dimensionally compatible charge mass and physically positive.
Lower must not exceed upper. Equal bounds form a point only when both endpoints
are inclusive. Canonical order is ascending; overlaps and exact duplicates fail.
The implementation performs no sorting, merging, normalization, or envelope.

Open-ended, missing-bound, infinite, NaN, negative, and zero statements are not
determinate bounded M05 regions. The first increment need not define a general
open-constraint schema; such evidence remains in exact references and
qualifications or yields `unavailable`/`indeterminate` when a bounded record is
requested.

## Evidence And Provenance Boundaries

Every record retains all material evidence and maturity references without an
automatic ranking or collapsed winner. An externally supplied/derived record
cannot claim stronger authority than its material inputs support; promotion is
an explicit review action, not weakest/strongest-wins arithmetic.

Schema capability admits no evidence. `measurement_supported_interval` retains
exact measured-point references and never implies unmeasured interior testing.
`property_uncertainty_constraint` never turns uncertainty into permission.
`intersection_of_explicit_constraints` can label an externally supplied record,
but this increment cannot calculate it. No real evidence family, production
method, powder record, load record, or dataset is admitted.

## Source Rounding And Uncertainty

Exact source wording/value, normalized machine quantity, source
rounding/reported precision, measurement uncertainty, model-form uncertainty,
and unknown uncertainty are distinct. Source rounding never becomes tolerance;
an uncertainty interval never becomes a bounded analytical charge region; and no
uncertainty arithmetic is authorized.

## Pressure Context

Pressure references preserve quantity identity, measurement method,
standard/protocol, instrument type, units, conditions, locator, and source
limitations. CUP, piezoelectric PSI, strain-derived pressure, crusher pressure,
and modeled pressure remain distinct. Pressure cannot establish a charge bound
without a separately admitted and authorized method.

## Namespace And Dependency Boundaries

M05 stays under `modern_powley.modernized`, depending only on promoted M01-M04
contracts. M01 owns quantities/units/geometry; M02 owns observations,
missingness/conflicts/domains; M03 owns completeness/applicability diagnostics;
M04 owns criteria/outcomes. M05 requires exact relevant M01/M02 references and
M03 diagnostics. M04 references are optional audit dependencies and cannot
establish a region, safety, or suitability. M05 duplicates none of their logic.
No imports from `later/`, `experimental/`, emulator, GRT, jRT, QuickLOAD, or
legacy code; `original/` cannot import M05.

## Serialization Requirements

Strict `modern_powley.m05.v1` serialization is authorized. It must reject
unknown fields/types/versions, malformed unions/units/endpoints, and non-finite
numbers; preserve explicit state/basis, caller order, gaps, references, source
semantics, lifecycle, uncertainty/dependency metadata, and non-implications; and
perform no implicit migration or field dropping. M01-M04 schemas remain
unchanged. This authorization commit creates no serializer or export.

## Required Repository Deliverables

Later implementation deliverables: M05 records/structural validators/serializer;
synthetic tests for ordering, overlap, duplicates, disjoint/point/non-numeric
states, provenance, lifecycle, strict payloads, architecture and prohibited APIs;
design and implementation decisions; appropriate definition/data-field ledger
entries; documentation; and `M05_completion_review.md`. No production data or
derivation method is required or permitted.

## Required Policy Decisions

The records-only policies are binding in
[`M05_records_only_authorization.md`](../decisions/M05_records_only_authorization.md).
Any change that adds arithmetic, normalization, production evidence/data,
recommendation semantics, or broader dependency behavior requires a dated
specification amendment and separate user authorization.

## Acceptance Gates

1. This reviewed authorization commit precedes implementation.
2. M01-M04 APIs, behavior, and schemas remain unchanged.
3. Immutable versioned segment/region records retain every required identity,
   provenance, context, qualification, dependency, and non-implication.
4. Region, published load interval, fill constraint, uncertainty interval, and
   pressure limit remain distinct.
5. Finite positive compatible bounds and endpoint rules are enforced.
6. Caller ascending order is required; out-of-order, overlapping, and duplicate
   segments fail without sorting, merging, or normalization.
7. Disjoint gaps and explicit point semantics round trip exactly.
8. Five non-equivalent region states are explicit; supersession/activation are
   lifecycle metadata.
9. Source rounding, uncertainty kinds, and declarative dependency status remain
   distinct; no uncertainty arithmetic exists.
10. Pressure context remains non-computational and quantity-specific.
11. Exact M01/M02/M03 references are required where applicable; M04 is audit-only.
12. No region derivation, intersection, union, interval arithmetic, selection,
    discovery, preference, fallback, ranking, recommendation, or prediction.
13. No production method, evidence family, powder/load record, or dataset admitted.
14. Strict M05 serialization round trips and M01-M04 serializers remain unchanged.
15. Architecture, scope, provenance, documentation, ledgers, tests, and full
    validation pass before M05 becomes `accepted`.

## Required Validation Commands

`uv sync --locked --offline`; `uv lock --check`; `uv run pytest -q`; focused M05
record/serialization/provenance/architecture tests; `uv run python -m compileall
-q src tests scripts`; `git diff --check`; CSV, JSON, notebook, Markdown-link,
artifact-hash, controlled-vocabulary, package-import, circular-boundary,
milestone-governance, roadmap/status, and prior-schema checks.

## Scope-Control Review Checklist

No original/prior-schema change; production method/data; region arithmetic;
sort/merge/normalization; point/midpoint selection; automatic rounding;
discovery/preference/conflict resolution; capacity substitution; implicit factor;
hidden default/tolerance; uncertainty propagation/distribution; pressure
calculation; safety/suitability/recommendation; ballistics prediction; source
promotion; web/plot/UI behavior; or M06 implementation.

## Completion-Report Requirements

Report authorization predecessor; files/API/schema; segment/state/basis,
ordering, point/disjoint, open-bound, uncertainty/dependency, evidence/maturity,
M01-M04 and pressure policies; explicit unavailable behavior; every gate and
validation command; scope review; no production data/method; commit/push/final
state; limitations; and one bounded recommendation that does not authorize M06.

## Commit And Release Expectations

Implementation occurs in a later bounded commit. Mark M05 `accepted` only after
all gates and its completion review pass. Do not amend this authorization commit,
rewrite history, force-push, or alter the preservation tag.

## Known Limitations

No production charge-region method or qualified manufacturer/laboratory dataset
is admitted. No region is calculated. No uncertainty propagation/dependence
model or cross-standard pressure method exists. Open-ended constraints have no
general M05 schema. Records cannot establish safety, suitability, or advice.

## Authorized Next-Milestone Boundary

Only the records-only M05 implementation defined here is authorized next.
Numerical derivation, literal intersection, production data, M06, visualization,
tooling changes, GRT intake, and web interfaces remain unauthorized. A
recommendation never authorizes later work.

## Implementation Decisions And Completion Evidence

Planning evidence and decisions remain in
[`M05_evidence_and_semantics_review.md`](../reviews/M05_evidence_and_semantics_review.md)
and [`M05_specification_decisions.md`](../decisions/M05_specification_decisions.md).
The binding amendment and authorization evidence are
[`M05_records_only_authorization.md`](../decisions/M05_records_only_authorization.md)
and [`M05_records_only_authorization_review.md`](../reviews/M05_records_only_authorization_review.md).
No implementation decision record or `M05_completion_review.md` exists because
M05 is authorized but not implemented or accepted.
