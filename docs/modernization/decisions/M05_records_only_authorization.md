# M05 Records-Only Authorization

Status: `accepted_authorization`

## User Authorization

The user explicitly authorized changing M05 from `planned` to `authorized` for
a later records-only implementation. This decision is a dated scope amendment
to the canonical specification. It clarifies and narrows the roadmap concept;
it does not authorize implementation in this commit.

## Exact Authorized Scope

The later increment may implement immutable identifiers/enums, charge-mass
segments, explicit endpoints, multiple disjoint segments, five region states,
exact record/evidence/diagnostic references, method/basis, provenance/domain,
conflict, activation/supersession, uncertainty/dependency metadata,
non-implications, strict `modern_powley.m05.v1`, and synthetic tests.

## Explicit Exclusions

No arithmetic creates or transforms a region: no intersection, union, interval
operations, sorting, merge, normalization, gap fill, midpoint/point selection,
rounding, unit guessing, discovery, preference, ranking, conflict resolution,
fallback, alias inference, capacity substitution, fill/loading-density
conversion, uncertainty propagation/Monte Carlo, pressure calculation,
prediction, suitability, recommendation, production data, external simulator or
later-method promotion, M06, plotting, tooling dependency, GRT intake, or web UI.

## Segment Policies

Caller order is canonical ascending. Out-of-order, overlapping, and exact
duplicate segments fail. Gaps remain. A point has equal finite positive bounds
with both endpoints included. No automatic ordering or normalization occurs.

## Basis And State Vocabulary

Basis describes provenance: source-declared, measurement-supported,
geometry/fill, property-uncertainty, externally intersected, or experimental.
State describes the record result: `bounded`, `empty`, `unavailable`,
`indeterminate`, or `conflicting`. Unavailable/indeterminate/conflicting are not
bases. Duplicate is invalid input; superseded and active/inactive are lifecycle
metadata independent of state.

## Open-Ended Constraints

Open, missing, NaN, infinite, non-positive, or otherwise unbounded statements
cannot be determinate bounded records. They remain referenced qualifications or
produce an unavailable/indeterminate state. No general open-constraint schema is
authorized.

## Source Rounding And Uncertainty

Source text/value, normalized quantity, reported precision/rounding,
measurement uncertainty, model-form uncertainty, and unknown uncertainty remain
distinct. Rounding is not tolerance; uncertainty is not a charge region; no
uncertainty arithmetic exists.

## Dependency And Correlation

Only declarative `not_applicable`, `unknown`, `explicitly_declared`, and
`externally_referenced` dependency status is authorized. No covariance,
correlation, joint distribution, sampling, or propagation is calculated.

## Evidence And Maturity

Records retain every material evidence/maturity reference without ranking or
winner selection. Authority cannot exceed material inputs; promotion is an
explicit review. Schema capability admits no source, method, or data.

## M01-M04 Dependencies

Use exact M01/M02 references and relevant exact M03 diagnostics. M04 references
are optional audit dependencies only. M04 passes cannot establish a region,
safety, suitability, or scientific validity. No earlier logic is duplicated.

## Pressure Context

Exact references may retain quantity, method, protocol/standard, instrument,
units, conditions, locator, and limitations. CUP, piezoelectric PSI,
strain-derived, crusher, and modeled pressure remain distinct. No pressure value
creates a bound.

## No-Method And No-Data Admission

No production derivation method, evidence family, powder/cartridge/load record,
manufacturer/laboratory dataset, simulator behavior, regression, later method,
or experimental hypothesis is admitted.

## Consequences And Amendment Triggers

Implementation must be a later commit and may contain only the authorized
contract. Any arithmetic, normalization, real data, evidence admission,
recommendation semantics, new external dependency, plotting/UI, or M06 behavior
requires a dated specification amendment and separate user authorization.
