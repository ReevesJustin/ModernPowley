# Agent reference — units, geometry, and data rules

Routed from `AGENTS.md`. Read this before touching parsers, geometry, or
data-provenance code. Not needed for documentation-only or governance work.

## Units and Geometry

- Preserve source units at every parser boundary and encode units in field names
  where practical, such as `effective_area_mm2` and `case_volume_cm3`.
- Do not map area to volume or gross fired-case capacity to net powder space.
- Net powder-space capacity is distinct from gross capacity. Any geometric
  intrusion estimate must be labeled derived and state its shape assumptions.
- Use `barrel_volume_ratio = Vb/V0` and
  `total_expansion_ratio = (V0+Vb)/V0`; never call both simply expansion ratio.
- Projectile travel is initial bullet-base position to muzzle. Do not subtract
  COAL or a fixed nominal length from barrel length.
- Reject missing, non-finite, non-positive, or dimensionally incompatible inputs.

## Data and Simulator Rules

- GRT and QuickLOAD values are modeled data, not laboratory measurements.
- Do not infer GRT semantics from a field name. Require XML unit/description plus
  authoritative model documentation for calculations.
- Keep measured, manufacturer-published, manual-published, user-measured,
  simulated, geometry-derived, regression-predicted, manually entered,
  agent-generated, and unknown values distinguishable.
- Never mean-impute a missing powder parameter, borrow another powder's value, or
  collapse unknown scientific values to an average.
- Relative burn-rate charts are rough ordinal references, never deterministic
  internal-ballistics mappings or universal powder orderings.
- Burnout claims require explicit burn fraction/distance/time, definition, and
  source fields. Muzzle pressure does not establish burnout.
