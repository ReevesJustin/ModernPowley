# M02 Implementation Decisions

Status: accepted for bounded M02 implementation

## Decisions

| Topic | Decision | Rationale |
|---|---|---|
| Identity | Immutable `PowderIdentity` records; identity is record-based, not name-based | Similar spelling cannot establish product, lot, formulation, or era equivalence. |
| Optional identity qualifiers | Explicit present-or-missing `IdentityQualifier` union | Lot, era, formulation, country, and market omissions retain semantic missingness. |
| Aliases | Directional `PowderIdentityRelationship` with source wording and provenance | Identical, renamed, related, replacement, and similar assertions are not interchangeable. |
| Lots and formulations | Never merged; each distinction remains in its identity record | No current evidence authorizes interchangeability. |
| Property names | Controlled `PropertyId` plus immutable `PropertyDefinition` | Extensible without accepting unrestricted free-form property semantics. |
| Similar terminology | Heat, force, impetus, vivacity, burn coefficients, and relative position remain separate IDs | Shared units or correlated values do not establish common definitions. |
| Property values | Tagged dimensional, source-scalar, categorical, ordinal, textual, interval, or tabular-reference values | Preserves source form without speculative normalization. |
| Unit conversion | Use M01 `PhysicalValue` only for M01-supported units; otherwise retain literal unit and definition as a source scalar | Prevents invented dimensions and conversions. |
| Dimensionless values | Require an explicit convention where the definition demands it | Dimensionless is not definition-free. |
| Missingness | Controlled `MissingState` assertion record; never zero, NaN, empty text, or omitted key | Missing reasons affect later admissibility and review. |
| Domains | Explicit `UNSPECIFIED` or `DECLARED`; unspecified never means universal | Absence of source constraints cannot authorize unrestricted use. |
| Bounds | Each bound is unbounded, inclusive, or exclusive; units are checked literally | Boundary behavior remains deterministic without interpolation. |
| Domain membership | Literal comparison against one declared domain; missing inputs return an indeterminate result | No domain inference, union, intersection, interpolation, or extrapolation. |
| Conflicts | Retain all observations and emit descriptive `ConflictComparison` records | No averaging, source ordering, maturity ordering, or winner selection. |
| Value origin | Reuse M01 provenance and additionally record observation transformation | Direct, transcribed, converted, derived, inferred, fitted, and asserted states remain distinct. |
| Serialization | Strict `modern_powley.m02.v1`; no migration and no changes to M01 v1 | Future versions require explicit version-to-version migration. |
| Fixtures | Synthetic identities use an unmistakable `SYNTHETIC-M02-*` namespace | Tests cannot be mistaken for a production powder database or recommendation. |
| Real data intake | Instantiate no real powder facts in M02 | No individual powder-property artifact has been authorized for promoted M02 population. |
| Source preference | Prohibited | Evidence class and maturity describe records but never select one. |
| Interpolation/extrapolation | Prohibited | M02 is a record contract, not a property model. |
| Powder or ballistics behavior | Prohibited | Screening and numerical behavior belong to later gated phases. |

## Dependency Decision

M02 adds no dependency. It reuses M01 immutable quantities, uncertainty, and
provenance. M02 modules do not import `original/`, `later/`, `experimental/`,
the emulator, GRT, jRT, or legacy scripts.

## Known Limits

M02 does not define conversions for pressure, energy, force, covolume, or burn
coefficients. Such values can be retained losslessly as source scalars until a
future, separately reviewed unit extension establishes their dimensions and
authoritative conversions. Domain membership supports only literal M01
quantities and categorical restrictions.
