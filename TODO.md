# ModernPowley Roadmap

This roadmap follows the completed historical audit and authorizes a separately
governed modernized-Powley program. Historical reconstruction and modernization
have independent status and acceptance gates.

## Repository Status

- `scalar_arithmetic_core: verified_reference` - source-backed, tested,
  isolated, and reproducible relative to retained original-Powley evidence.
- `complete_historical_method: evidence_limited` - incomplete because required
  physical graphical scales and reading procedures are unavailable.
- `modernized_powley: authorized_for_development` - active, provenance-separated
  engineering development outside `original/`.

Historical `select_powder`, `estimate_velocity`, and `estimate_pressure` must
continue to raise `MissingProvenanceError`. This is a provenance boundary, not
a loading recommendation and not a prohibition on modernized development.

## Completed Historical Work

- Preserved the pre-audit prototype and sanitized the public repository.
- Standardized the environment on `uv` and established agent guidance.
- Created source, equation, constant, field, GRT-mapping, and artifact ledgers.
- Separated original, later, emulator, and experimental behavior.
- Implemented and tested the retained source-backed scalar arithmetic core.
- Reconciled original and Davis examples without conflating their provenance.
- Added provenance, namespace, artifact-hash, and reconciliation tests.
- Completed reconstruction closure, scale-recovery, and completion audits.
- Identified every unresolved historical graphical operation explicitly.

## Historical Evidence-Only Maintenance

`src/modern_powley/original/` is under an evidence-only change policy.

Permitted work:

- integrate newly retained original primary evidence;
- correct demonstrated transcription or implementation errors;
- improve provenance mappings, documentation, and tests;
- perform non-behavioral maintenance.

Prohibited work:

- insert modern substitutions or later equations for missing original scales;
- infer graphical boundaries or fit historical tables;
- present emulator or GRT behavior as original;
- silently change source units, constants, domains, or rounding rules.

## Dormant Historical Evidence Acquisition

These tasks resume only if additional evidence becomes available:

- recover Arrow 2 powder-selection geometry and reading rules;
- recover the Expansion Ratio-Velocity surface and interpolation rules;
- recover the 1961 muzzle-pressure surface and reading rules;
- classify and recover the separate later Powley psi Calculator.

Follow `docs/provenance/original_powley_evidence_acquisition.md`. Missing scales
must not be reconstructed from Davis, the emulator, GRT, regressions, modern
powder behavior, or sparse observations inside `original/`.

## Active Modernized-Powley Program

Modernized development is authorized outside `original/` and does not depend on
recovery of the missing historical scales. The controlling documents are:

- `docs/modernization/modern_powley_charter.md`;
- `docs/modernization/evidence_and_model_classes.md`;
- `docs/modernization/model_boundaries.md`;
- `docs/modernization/modern_powley_roadmap.md`.

Dependency order:

1. **M00 - Program authorization and boundaries:** completed by documentation.
2. **M01 - Canonical inputs, units, and geometry:** implemented and reviewed;
   see `docs/modernization/reviews/M01_completion_review.md`.
3. **M02 - Powder-property evidence model:** implemented and reviewed;
   contains records only and no production powder database.
4. **M03 - Input and literal-domain diagnostics:** first bounded increment
   implemented and reviewed; it does not screen powders or prepare a solver.
5. **M04 - Declarative screening criteria and auditable outcome records:**
   implemented and reviewed as a record/audit layer only; it contains no
   production criteria, catalog search, suitability decision, ranking, or
   ballistics prediction.
6. **M05 - Future bounded phase:** recommended for specification drafting only;
   it is not authorized. Its canonical specification must be reviewed and
   committed before any implementation.
7. **M06 - Pressure and velocity baseline.**
8. **M07 - Burn progression and burnout location.**
9. **M08 - Muzzle pressure and secondary selection objectives.**
10. **M09 - Measured validation and calibration.**
11. **M10 - Uncertainty and decision policy.**
12. **M11 - CLI or application workflow after numerical promotion gates pass.**

M01 establishes canonical inputs and geometry. M02 adds neutral identity,
property, missingness, domain, and conflict records without powder behavior.
M03 consumes those explicit records without imputing missing properties or
selecting powders. Its positive summaries mean only that declared requirements
or literal domain constraints were satisfied; they do not mean solver readiness,
physical validity, suitability, or safety.

M04 records exact criterion definitions, supplied evidence, literal outcomes,
and descriptive active-mandatory summaries. A pass does not establish physical
correctness, powder suitability, safety, approval, recommendation, or solver
readiness. Future milestones follow the specification-first workflow in
`AGENTS.md`; a recommendation does not authorize implementation.

## Quarantined And Later Work

The following may be evaluated as candidates in their correct evidence class,
but none is automatically part of the modernized method and none may enter
`original/`:

- Davis equations and Table 4;
- unresolved Howell and Miller methods;
- archived emulator behavior;
- GRT-derived fields and behavior;
- `Ba`, `Ba_target`, and `Ba_eff`;
- regression or fitted ranking models;
- modern powder databases;
- empirical pressure, velocity, or burn models.

Existing prototype outputs remain quarantined. Similar output, worked-example
agreement, or regression reproduction does not establish provenance or satisfy
a promotion gate.

## Deferred Product Work

Spreadsheets, notebooks, Streamlit, Gradio, graphical selectors, aggregate
rankings, and public recommendation interfaces remain deferred through M10.
Only promoted numerical layers may support M11. No current output is a loading
instruction or recommended charge.
