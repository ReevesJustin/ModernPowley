# Audited Introduction

ModernPowley now has two purposes:

1. reconstruct source-backed portions of Homer Powley's historical method;
2. preserve later prototype experiments without presenting them as historical,
   validated, measured, or suitable for loading decisions.

The complete agent-derived prototype is preserved at tag
`pre_audit_agent_derived_prototype`. Its equations and claims are not authority.

## Scientific Boundaries

- Original Powley means an exact claim traceable to the 1961 manual or another
  identified primary artifact.
- Davis, Howell and Miller material is kept in separate attribution namespaces.
- GRT values are model parameters or simulator values, not measurements.
- A fit evaluated on its fitting/selected rows is in-sample reproduction, not
  validation.
- Missing fields remain missing and are excluded from calculations.
- Commercial burn-rate charts are rough ordinal references, not universal
  cartridge behavior.
- Burnout requires explicit burn fraction, distance/time, definition and source;
  muzzle pressure alone does not establish it.

## Current Capability

The `scalar_arithmetic_core` computes sectional density, mass ratio, historical
loading-density arithmetic, projectile travel, and separately named expansion
ratios. It is source-backed, tested, isolated, and reproducible relative to
retained evidence. The `complete_historical_method` is `not_ready_to_freeze`:
original Arrow 2 powder selection, Expansion Ratio-Velocity execution, and 1961
muzzle-pressure execution are unavailable and raise `MissingProvenanceError`.
The later Powley psi Calculator is a separate unresolved artifact.

ModernPowley `Ba_target`, `Ba_eff`, and charge-regression formulas are quarantined
experiments requiring explicit opt-in. Opt-in reproduces a hypothesis; it does
not validate it.

See [the history index](History.md), [equations](Equations.md), and
[full audit](audits/modern_powley_full_repository_audit.md).
