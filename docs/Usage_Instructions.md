# Audited Usage

There is no supported powder-selection or load-recommendation workflow. Legacy
analysis, prediction, plotting and selector scripts are disabled because their
inputs or models failed provenance audit.

## Verify the Repository

```bash
uv sync --locked
uv run pytest -q
uv run python scripts/audit_regression.py
uv run python scripts/generate_audit_inventory.py
uv lock --check
```

## Source-Backed Arithmetic

Run Python through `uv`, with `src` on its module path (pytest config already
does this):

```python
from modern_powley.original.geometry import sectional_density

sd = sectional_density(bullet_weight_grains=180, bullet_diameter_inches=0.308)
```

Inputs must carry the units named by the function. The original arithmetic
requires seating-depth-specific measured powder-space water capacity. A derived
gross-minus-intrusion estimate is not an original-Powley measurement and cannot
be silently supplied as one. Missing values raise errors.

Original powder selection, velocity, and 1961 muzzle pressure intentionally
raise `MissingProvenanceError` until exact source material passes the documented
evidence and implementation-readiness gates. The later Powley psi Calculator is
a separate unresolved artifact.

The `original/` namespace is evidence-only: modern geometry, later equations,
and fitted behavior cannot be used as fallbacks. The separately authorized M01
API under `modern_powley.modernized` provides explicit units, records,
serialization, transparent Euclidean geometry, and one-way historical scalar
adapters. It provides no powder screening, charge estimation, pressure,
velocity, burnout, muzzle pressure, ranking, or recommendation workflow.

The M02 API records powder identities and source observations, including
semantic missingness, applicability domains, and unresolved conflicts. It does
not include a production powder database, choose among observations, or assign
computational meaning to source-specific coefficients.

## Experimental Reproduction

Experimental functions live under `modern_powley.experimental` and reject calls
unless `allow_unvalidated=True` is supplied. That flag is for audit reproduction
only. It does not turn the result into a recommendation, measurement, validation,
or safety claim.

## GRT Parsing

The repaired parser keeps `Aeff` as `effective_area_mm2` and does not create an
effective volume from it. Unverified internal `caliberfile` variable mappings are
excluded. Exact paths, units and confidence are in
`docs/provenance/grt_field_mapping.csv`.
