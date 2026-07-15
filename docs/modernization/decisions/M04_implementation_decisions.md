# M04 Implementation Decisions

## Scope

M04 records declarative criteria, explicit evidence supplied for their review,
criterion outcomes, and descriptive criterion-set summaries. It does not search
records, screen a catalog, select observations, rank candidates, or predict
ballistic behavior.

## Decisions

| Topic | Decision | Reason |
|---|---|---|
| Definition versus outcome | Immutable criterion definitions state a condition; separate evaluation records state what evidence and result were recorded | Policy and audit history must not be overwritten by a result. |
| Criterion versus set | Sets contain versioned criterion references and display order only | Ordering is not weighting or preference. |
| Roles | Mandatory, advisory, informational, diagnostic-only, inactive, historical, experimental, and unavailable | Nonmandatory or nonactive records cannot silently become mandatory policy. |
| Status | Active, inactive, superseded, withdrawn, historical, experimental, evidence-limited, or unavailable | Superseded and unavailable definitions remain retained and never imply pass. |
| Versions | Positive integers; sets reference exact criterion versions; supersession is an explicit identity | No implicit migration or substitution. |
| Forms | Presence, missing-state prohibition, required M03 classification, exact category/identifier, finite category membership, four one-sided numeric bounds, numeric point/interval containment, explicit no-conflict declaration, and manual assertion | These forms are literal and bounded; no expression language or rules engine is needed. |
| Mechanical evaluation | Implement narrow literal helpers only for the controlled forms | Exact evidence IDs are supplied by the caller; no discovery or inference occurs. |
| Manual assertions | Separate method with responsible party, date, rationale, review status, evidence references, verification state, and qualifications | A human assertion cannot masquerade as a mechanical comparison. |
| Evidence references | Immutable tagged records retain exact source record identity, definition, supplied value/status, provenance, and source locator | Similar names or higher evidence class never authorize substitution. |
| M03 reuse | Completeness and domain criteria consume exact M03 diagnostic references and their controlled status; M04 does not repeat domain or completeness logic | M03 remains the authority for those comparisons. |
| Missingness | Retain M02 `MissingState`; absent, unavailable, conflicting, and unevaluated remain distinct | Missing data never becomes zero, empty text, or a failed numeric comparison. |
| Conflicts | Require an explicit conflict declaration or preserve conflicting evidence IDs | No value is selected, averaged, preferred, or converted into a pass. |
| Numeric boundaries | M01 quantities only; exact SI conversion; explicit inclusive/exclusive endpoint | No tolerance, interpolation, extrapolation, or probability. |
| Intervals | Pass only on literal full containment; disjoint fails; partial overlap is indeterminate | No midpoint or nominal value is selected. |
| Definitions | Property/diagnostic definition identifiers and conventions must match literally | Numerical compatibility does not establish semantic equivalence. |
| Criterion pass | Explicit supplied evidence satisfied that exact criterion version | It does not establish safety, suitability, recommendation, or physical correctness. |
| Set positive summary | Every active mandatory criterion in that exact set version has a recorded pass | Advisory results and counts cannot influence the summary. |
| Scores and ranking | Prohibited | M04 is an audit trail, not an optimization or selection system. |
| Production sets | None in M04 | No accepted source-backed modernization screening policy has been authorized. |
| Fixtures | `SYNTHETIC-M04-*` identities only | Tests cannot be confused with a powder catalog or load guidance. |
| Serialization | Strict `modern_powley.m04.v1`; no migration | M01-M03 schemas remain unchanged; future migration must be explicit. |
| Namespace | M04 stays under `modernized/` and imports only promoted M01-M03 contracts | No historical, later, experimental, emulator, GRT, jRT, or legacy behavior enters M04. |

## Rejected Alternatives

- Callbacks, expression strings, dynamic imports, and a generic rule engine were
  rejected because they would make policy execution unauditable and unbounded.
- A powder collection or observation query API was rejected because the caller
  must supply exact evidence identities.
- Evidence-class, maturity, recency, and uncertainty preference were rejected
  because they would resolve conflicts without authorization.
- Weights, points, pass percentages, and composite scores were rejected because
  they would introduce ranking semantics.
- Treating an absent M03 domain as a pass was rejected because missing domain
  evidence is not universal applicability.
