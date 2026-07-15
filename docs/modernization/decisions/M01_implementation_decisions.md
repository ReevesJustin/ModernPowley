# M01 Implementation Decisions

Status: accepted for M01 implementation

## Public File Map

- `modernized/units.py`: dimensions, units, immutable quantities, exact conversions.
- `modernized/uncertainty.py`: bounded scalar uncertainty tagged union.
- `modernized/provenance.py`: evidence, maturity, origin, and derivation metadata.
- `modernized/records.py`: controlled conditions and immutable physical records.
- `modernized/geometry.py`: direct Euclidean geometry and explicit ratios.
- `modernized/serialization.py`: strict `modern_powley.m01.v1` JSON dispatch.
- `modernized/adapters/original.py`: one-way calls to verified historical scalars.

## Decisions

| Topic | Decision | Rationale |
|---|---|---|
| Quantity mechanism | Frozen, slotted standard-library dataclasses plus enums and explicit conversion functions | Keeps dimensions visible without a dependency or mutable registry. |
| Dependencies | Add none | M01 does not require Pint, Pydantic, or another framework. |
| Canonical units | SI: m, m2, m3, kg, K, kg/m3, and dimensionless | One internal convention prevents mixed-unit arithmetic; supplied values and units remain retained. |
| Conversion authority | NIST exact inch, pound, and grain definitions; SI prefix identities | Replaces approximate legacy divisors. Area and volume factors are powers of the exact length definition. |
| Serialization | Strict tagged dictionaries and JSON using schema `modern_powley.m01.v1` | Unknown critical fields and unsupported versions fail; JSON rejects NaN/infinity. |
| Migration | No migration for v1; future versions require explicit version-to-version functions | Older data must never be silently reinterpreted. |
| Uncertainty | `unknown`, `instrument_resolution`, `symmetric_absolute`, or `bounded_interval` | Covers M01 measurement bounds without probability or covariance APIs. |
| Measurement vocabulary | Small controlled enums; `OTHER` requires detail and `UNKNOWN` remains explicit | Prevents free-form states while preserving real exceptions. |
| Primer pocket | Record declared treatment and optional explicit volume; infer no geometry | Primer identity cannot establish pocket dimensions. Mismatched bases require an explicit correction. |
| Modern namespace | Create `modernized/`; permit historical calls only in `adapters/original.py` | Makes the dependency direction auditable and prevents modern behavior entering `original/`. |
| Water conversion | Require supplied density or explicit named source convention | Powley's 253 gr/in3 remains historical and is never a modern default. |
| Sectional density | Name the modern function `sectional_density_mass_over_diameter_squared` | Avoids implying circle-area division and makes the convention explicit. |
| Loading terminology | Expose only denominator-specific charge-to-water-capacity mass ratios | M01 has no powder bulk density and therefore cannot compute volumetric fill. |
| Derived evidence | Add `derived_quantity` evidence and attribution values | Direct deterministic geometry is neither original evidence nor an exploratory hypothesis. |
| Composite-record uncertainty | Attach uncertainty to each dimensional `PhysicalValue`; do not invent one aggregate uncertainty for a multi-dimensional record | An aggregate bound has no coherent dimension. Top-level records retain their physical values, and every such value carries provenance and an explicit uncertainty tag. |

## Rejected Alternatives

- Third-party units/validation packages: unnecessary M01 dependency and hidden behavior.
- Bare SI floats at public boundaries: loses dimension and supplied-unit identity.
- Implicit room-temperature water density: conditions and uncertainty would be invented.
- One generic capacity class: would permit gross, measured usable, and estimated
  usable quantities to be exchanged accidentally.
- Generic `expansion_ratio`, `case_volume`, `effective_case_volume`, or
  `loading_density` fields: physically ambiguous.
- Reuse of Davis/emulator displacement coefficients: later-source behavior is
  unnecessary because direct Euclidean geometry is available.

## Known Limits

M01 performs no statistical uncertainty propagation. Derived results record
uncertainty as unresolved unless a function explicitly supplies a conservative
bound. Projectile geometry supports a flat base or one linear boat-tail frustum
plus cylindrical shank; more complex seated shapes report outside-model.
