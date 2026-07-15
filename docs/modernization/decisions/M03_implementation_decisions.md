# M03 Implementation Decisions

## Scope

M03 adds structured input-completeness and literal applicability diagnostics. It
does not execute geometry, select records, screen powders, prepare a solver, or
make physical-validity or safety claims.

## Decisions

| Topic | Decision | Reason |
|---|---|---|
| Completeness | Always relative to an immutable named and versioned requirement set | There is no universal complete geometry or load. |
| Production sets | Only existing M01 circle, cylinder, frustum, seated-displacement, barrel-volume, capacity-comparison, and explicit ratio operations | Future powder and ballistic behavior is unavailable. |
| Inputs | Inspect explicit `InputCandidate` records only | No missing dimension, geometry, capacity, or category is inferred. |
| Requirement kinds | Required, optional, and branch-conditional | Absence and non-applicability remain distinct. |
| Alternatives | An explicit branch selector activates exactly one declared branch | Dimensional patterns never auto-detect projectile geometry. |
| Capacity | Gross, measured usable, estimated usable, and primer-pocket records have distinct candidate kinds | No fallback, substitution, preference, or averaging is allowed. |
| Multiple values | More than one candidate for a single-valued requirement is a conflict | Evidence and maturity never choose a winner. |
| Explicit missingness | M02 `MissingState` is retained in an explicit-unavailable diagnostic | Missingness never becomes zero, empty text, or a default. |
| Positive completeness | Every evaluated required or active conditional requirement was satisfied | This does not mean safe, suitable, physically correct, or ready for another model. |
| Domains | Evaluate each declared M02 constraint independently | Domains are never combined, inferred, interpolated, or extrapolated. |
| Unspecified domain | Produce `domain_unspecified` | Missing applicability information is not universal applicability. |
| Numeric points | Convert only through M01 units and compare with exact inclusive/exclusive endpoints | No hidden tolerance is admitted. |
| Numeric intervals | Inside only when fully contained; outside only when disjoint; partial overlap is `partially_comparable` | No midpoint, nominal value, or distribution is assumed. |
| Source scalars | Require exact reported unit and convention | M03 does not invent conversions for source-specific quantities. |
| Categories and identifiers | Exact literal matching, respecting the constraint's existing case policy | No alias, semantic-similarity, or fuzzy match. |
| Query definition | Must exactly equal the declared variable definition | Similar wording does not establish common meaning. |
| Conflicts | Diagnostics preserve every candidate identity | No automatic resolution exists. |
| Serialization | Strict `modern_powley.m03.v1`; no migration | M01 and M02 schemas remain unchanged; future migrations must be explicit. |
| Provenance | Requirement sets and derived evaluations use `SRC-M03-DESIGN` | Repository design authority is not historical or laboratory evidence. |
| Prohibited semantics | No solver-readiness, suitability, safety, selection, recommendation, interpolation, or extrapolation APIs | This increment is diagnostic only. |

## Rejected Alternatives

- A generic rules engine was rejected because it would obscure the small set of
  admitted operations and could be reused as an undeclared screening system.
- Passing arbitrary Python objects was rejected because record-kind and capacity
  identity would not serialize or audit reliably.
- Automatically choosing measured data, newer data, or higher-maturity data was
  rejected because completeness cannot resolve evidence conflicts.
- Treating a partially overlapping interval as inside was rejected because
  overlap is not containment.
- Treating absent domain metadata as unrestricted was rejected because it would
  convert missing evidence into authorization.
