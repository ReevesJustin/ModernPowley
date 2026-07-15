# M01: Canonical Inputs And Geometry

## Status

M01 is implemented and reviewed. Its promoted API is
`modern_powley.modernized`; the acceptance mapping is in
`../reviews/M01_completion_review.md`. M02 is the next active phase.

M01 establishes physical quantity identity, units, provenance, validation, and
geometry before powder screening or prediction. It must interoperate with the
verified historical scalar reference through explicit adapters without changing
`src/modern_powley/original/`.

## Design Constraints

- Modern records are not historical inputs merely because units are compatible.
- Each observed or supplied value carries provenance, evidence class, source or
  measurement identity, uncertainty when known, and missingness explicitly.
- Measured and estimated quantities use different fields and types.
- Derived values identify their method and input records.
- Mixed-unit arithmetic occurs only after boundary conversion.
- Non-finite, dimensionally incompatible, and physically invalid inputs fail.

## Canonical Internal Unit Policy

The modernized layer normalizes M01 calculations to SI quantities:

| Dimension | Canonical internal unit |
|---|---|
| length | metre (`m`) |
| area | square metre (`m2`) |
| volume | cubic metre (`m3`) |
| mass | kilogram (`kg`) |
| temperature | kelvin (`K`) |

Source-faithful inch-pound values remain accepted at adapters and retained in
source records. Historical functions continue to receive their explicit grains,
inches, cubic inches, and water-grain conventions; adapters own those conversions.
No bare scalar may cross the modernized calculation boundary without a declared
unit.

Calculations use at least IEEE 754 binary64 precision and do not round intermediate
values for presentation. Source precision and measurement uncertainty are stored
separately. Serialization uses explicit unit identifiers and enough significant
digits to round-trip the stored numeric value; display rounding is not persisted
as a replacement for the calculation value.

Conversion ownership belongs to a single tested unit module. Conversion
constants must identify their authority and convention, including water density
or temperature when converting water mass to volume. The historical manual's
`253 gr water/in3` remains a source-specific convention and is not silently used
as a universal modern conversion.

## Common Provenance Fields

Each supplied dimensional value includes:

- value and unit;
- evidence class;
- source, publication, dataset row, or measurement identifier;
- measured, published, transcribed, inferred, fitted, calibrated, assumed, or
  derived origin;
- conditions and method where applicable;
- uncertainty, resolution, confidence, or an explicit unknown state;
- timestamp/version and notes;
- applicability domain.

Derived records additionally include method identity, model maturity, input
record identifiers, and assumptions.

## Cartridge And Chamber Inputs

Define the following concepts separately:

- **Cartridge identity:** normalized designation plus source-specific aliases;
  identity is not inferred from dimensions alone.
- **Case length:** axial case length with source/measurement conditions.
- **Gross fired-case water capacity:** water mass or converted volume at the
  documented fill boundary, case condition, primer state, water condition, and
  measurement uncertainty.
- **Measured seating-specific usable powder-space capacity:** capacity behind
  the intended seated projectile, with projectile identity, seating state,
  measurement procedure, and uncertainty. This is authoritative when supplied.
- **Geometrically estimated usable powder space:** a separate derived quantity
  with shape assumptions, primer-pocket treatment, and adequacy status.
- **Primer-pocket treatment:** included, excluded, filled, sealed, or unknown;
  never silently assumed.
- **Measurement conditions:** case sizing/firing state, fill boundary, water
  temperature or density convention, scale resolution, repeats, and operator.
- **Capacity uncertainty:** numeric distribution/bound where available, otherwise
  explicit unknown; it is not zero by omission.

Gross capacity cannot populate usable capacity without an explicit measurement
or geometric method record.

## Projectile Inputs

- projectile identity and manufacturer/lot where available;
- projectile mass;
- diameter with convention and measurement/source;
- total length;
- seating depth;
- cartridge overall length;
- cylindrical shank intrusion length and diameter where represented;
- boat-tail axial length or height;
- boat-tail base diameter;
- geometric adequacy flag describing whether the chosen shank/tail model
  represents the seated portion;
- optional ogive information only when a later phase demonstrates a need.

Seating depth may be supplied directly or derived from explicit dimensions by a
named method. Direct and derived values remain distinguishable. Boat-tail
correction cannot be applied when tail geometry or seated relationship is
unknown.

## Firearm Inputs

- groove diameter and bore diameter as separate optional quantities;
- explicit diameter convention used for each derived bore area;
- barrel length with its reference points;
- projectile travel from initial bullet-base position to muzzle;
- optional throat/freebore only when measured or sourced and required by a
  later phase;
- applicable pressure-standard identity and edition, without treating the
  identity itself as a pressure limit.

Projectile travel must not be computed by subtracting COAL or a fixed nominal
length from barrel length. Any geometric derivation must identify the chamber,
case, seating, and reference-point assumptions.

## Derived Quantities

M01 may eventually provide only transparent geometry and dimensionless ratios:

- bore area, with diameter convention and formula identity;
- sectional density, with explicit mass/area convention;
- charge-to-bullet mass ratio when an externally supplied charge is present;
- gross loading density with an unambiguous denominator;
- usable-space loading density with measured or estimated denominator identity;
- barrel swept volume;
- barrel volume ratio `Vb/V0`;
- total expansion ratio `(V0+Vb)/V0`;
- total expanded volume;
- seating displacement;
- boat-tail displacement correction;
- water-mass/volume conversion with named convention.

The term `expansion_ratio` alone is prohibited in a canonical field. Charge mass
may be accepted only to calculate ratios for an externally defined case; M01
does not predict or recommend it.

## Measured Versus Estimated Usable Space

Measured seating-specific usable powder space is authoritative when supplied.
A geometric estimate must:

- remain separately named and serialized;
- state its geometry and primer-pocket assumptions;
- state whether the seated projectile shape is adequately represented;
- report input and method uncertainty;
- never overwrite, replace, average with, or silently override a measurement;
- never be called the historical Powley measurement unless that historical
  water-displacement procedure was actually followed and documented.

When both exist, comparison is diagnostic. Selection of a value for a later
calculation must be explicit and retained in the decision trace.

## Validation And Boundary Rules

- Reject missing required values, non-finite values, and non-positive physical
  dimensions or masses.
- Reject negative derived volume and projectile travel.
- Reject seating/tail combinations that violate the declared geometric model.
- Do not assume bullet diameter equals groove diameter or bore diameter.
- Do not assume gross capacity measurement conditions.
- Do not assign zero uncertainty when uncertainty is unknown.
- Reject unitless serialization for dimensional values.
- Default extrapolation policy is not applicable: geometry either satisfies the
  declared shape model or reports outside-model.

## Serialization Expectations

The implementation design must choose a stable, versioned record schema. Each
dimensional field serializes value and unit; provenance and uncertainty remain
machine-readable. Derived records serialize method/version and input identities.
CSV export, if later required, uses unit-suffixed columns plus companion
provenance rather than ambiguous names. JSON uses explicit quantity objects or
an equally unambiguous schema. No serialization format is implemented in this
documentation phase.

## Compatibility With Historical Reference

Compatibility tests must show that appropriately sourced, converted inputs can
be passed to the existing original scalar functions and reproduce current
results. The adapter may convert units and names but may not:

- modify `original/` behavior;
- supply missing historical powder, velocity, or pressure operations;
- reinterpret a modern estimate as measured historical capacity;
- import modern modules into `original/`.

## M01 Exclusions

M01 does not include:

- powder selection or burn-rate ranking;
- charge prediction or charge-region estimation;
- pressure or velocity prediction;
- burnout or muzzle-pressure prediction;
- `Ba`, `Ba_target`, or `Ba_eff`;
- GRT powder behavior;
- regression, fitting, or calibration;
- a CLI, notebook, spreadsheet, or application interface;
- loading recommendations.

## Required Tests

- unit conversion round trips and cross-unit equivalence;
- dimensional invariants for area, volume, ratios, and displacement;
- non-finite, missing, negative, and zero input rejection;
- measured/estimated capacity identity and precedence behavior;
- flat-base and boat-tail geometry edge cases;
- projectile-travel reference points;
- diameter-convention separation;
- uncertainty and provenance retention;
- serialization round trip once a schema is selected;
- compatibility with source-backed original scalar fixtures;
- architecture prohibition on modern imports into `original/`;
- absence of powder or ballistics prediction behavior.

## Acceptance Gates

M01 is complete only when:

1. Every field has an explicit unit and provenance category.
2. Measured and estimated capacities cannot be confused by API, type, field,
   serialization, or default selection.
3. Dimensional invariants and invalid-input tests pass.
4. Unit conversions round-trip within documented binary64 tolerances.
5. Water conversion conventions are named and source-specific.
6. Source-backed original scalar calculations consume compatible adapter inputs
   without any behavior change in `original/`.
7. Geometry edge cases and outside-model states are tested.
8. No modern geometry behavior enters or is imported by `original/`.
9. No numerical ballistics prediction, powder screening, ranking, or interface
   is introduced.
10. Schema, implementation, tests, and decision record receive explicit review.

## Implemented Decisions

M01 uses frozen, slotted standard-library dataclasses and controlled enums. It
serializes strict tagged JSON-compatible records under
`modern_powley.m01.v1`; unsupported versions fail and future migrations must be
explicit. Scalar uncertainty is an explicit tagged union. Primer-pocket state
is declared, and a correction requires an explicitly measured or sourced
volume. No primer-pocket geometry is inferred. Full rationale is retained in
`../decisions/M01_implementation_decisions.md`.
