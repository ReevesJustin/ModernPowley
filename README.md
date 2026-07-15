# ModernPowley: Historical Reference And Modernization Program

> [!CAUTION]
> Current powder rankings are not validated. The prototype `Ba_target` and
> `Ba_eff` ranking logic are experimental, and some equations, field mappings,
> and historical attributions were introduced without adequate provenance.
> Current and preserved prototype outputs must not be treated as load
> recommendations or as evidence of pressure, velocity, or burnout performance.

This repository preserves an evidence-based reconstruction of the Powley
Computer, later published methods, and quarantined prototype experiments. The
historical audit is complete relative to retained evidence. A separately
governed modernized-Powley development program is now authorized; it does not
claim to recover missing historical scales. The agent-derived prototype remains
preserved at tag `pre_audit_agent_derived_prototype` (commit
`08e4ee05b5b10ec8b5f30986bd7e5bd945cc6dc8`). History was not rewritten.

Repository status has three independent scopes:

- `scalar_arithmetic_core: verified_reference` - source-backed, tested,
  isolated, and reproducible relative to retained original-Powley evidence.
- `complete_historical_method: evidence_limited` - incomplete because required
  graphical scales and reading procedures are unavailable.
- `modernized_powley: authorized_for_development` - a provenance-separated
  engineering research track governed by documented phase and promotion gates.

There is no supported load-selection, powder-recommendation, pressure-prediction,
velocity-prediction, or burnout-prediction workflow.

The repository uses `uv` exclusively for Python versions, dependency locking,
environment synchronization, and command execution. `pyproject.toml`,
`.python-version`, and `uv.lock` are the authoritative environment files.

## Audit Status

Visual inspection of the committed 1961 manual scan directly supports:

- net powder-space water capacity as the capacity input;
- inch-pound sectional density;
- charge-to-bullet mass ratio;
- historical 0.80/0.86 IMR loading-density arithmetic;
- bullet travel as effective barrel length;
- distinct barrel-volume and total-expansion ratios;
- one printed .308 Winchester worked example.

The archived emulator's exact powder bands and equations are reproduced only in
a separate `later.emulator` module. Exact original powder-scale boundaries, the
Expansion Ratio-Velocity surface, and the 1961 muzzle-pressure surface remain
source-incomplete. The later Powley psi Calculator is a separate unresolved
artifact. Those original operations fail
with `MissingProvenanceError`; they are not guessed from later transcriptions.
The `original/` namespace is maintained under an evidence-only policy. Missing
historical behavior cannot be supplied from the modernized track.

W. C. Davis Jr.'s later 1981 formulation is reconstructed separately in
`later.davis`, including a bounded transcription of his Table 4 pressure factor.
The Davis publication is a later primary source available through
access-restricted page viewing. The user reviewed those pages and supplied the
recovered material. The committed equation transcription and Table 4 CSV are
normalized secondary derivatives. Because the primary page images are not
retained, the complete Table 4 remains medium-confidence and pending
independently reproducible visual verification. Worked-example coordinates and
secondary transcriptions are cross-checks, not verification of all 306 cells.
This does not change the unavailable status of original-Powley powder
selection, velocity, or pressure operations.

The following are quarantined and unvalidated:

- `Ba_target = clamp(0.85 - 0.05*RC, 0.45, 0.90)`;
- `Ba_eff = Ba * [a0 + (1-a0)*z2/2]`;
- `Wc = 0.71 * V0^1.02 * Ltravel^0.06`.

They live under `src/modern_powley/experimental/` and require the explicit
keyword `allow_unvalidated=True`. `Ba_eff` is not ballistic efficiency.

## Repository Guide

- `docs/audits/modern_powley_full_repository_audit.md`: finding-by-finding audit.
- `docs/audits/original_powley_reconstruction_closure.md`: end-to-end original-method closure decision and traceability matrix.
- `docs/audits/original_powley_reconstruction_completion_audit.md`: freeze-readiness audit of every original operation, source gap, unit, and public function.
- `docs/provenance/original_powley_evidence_acquisition.md`: capture, intake, and acceptance requirements for missing physical evidence.
- [Modernization charter](docs/modernization/modern_powley_charter.md): purpose, safety boundary, and engineering principles.
- [Evidence and model classes](docs/modernization/evidence_and_model_classes.md): evidence and maturity classifications.
- [Model boundaries](docs/modernization/model_boundaries.md): historical, later, experimental, and future-modern separation.
- [Modernized roadmap](docs/modernization/modern_powley_roadmap.md): gated M00-M11 development sequence.
- [M01 specification](docs/modernization/phases/M01_canonical_inputs_and_geometry.md): implemented canonical inputs, units, provenance, serialization, and transparent geometry.
- [M01 completion review](docs/modernization/reviews/M01_completion_review.md): acceptance-gate mapping and remaining limits.
- [M02 specification](docs/modernization/phases/M02_powder_property_records.md): implemented neutral powder identity, property, missingness, domain, and conflict records.
- [M02 completion review](docs/modernization/reviews/M02_completion_review.md): evidence and no-behavior acceptance mapping.
- [M03 diagnostic specification](docs/modernization/phases/M03_input_and_domain_diagnostics.md): implemented operation-relative input completeness and literal M02 domain diagnostics.
- [M03 completion review](docs/modernization/reviews/M03_completion_review.md): diagnostic, boundary, architecture, and no-screening acceptance mapping.
- `TODO.md`: active roadmap, dormant historical acquisition work, and deferred phases.
- `docs/audits/original_powley_scale_recovery.md`: primary-source scale search, graphical evidence, and implementation-readiness decision.
- `docs/audits/davis_1981_evidence_intake.md`: derivative OCR/reprint intake and remaining primary-image verification boundary.
- `docs/audits/davis_1981_equation_and_example_reconciliation.md`: Davis scalar-equation, unit, implementation, and worked-example audit.
- `reference/source_ledger.csv`: source access and artifact hashes.
- `reference/powley_manual/powleysmanuals1.md`: searchable OCR-style manual transcription; verify against the scan.
- `reference/powley_manual/powleysmanuals1.pdf`: hash-verified primary scan.
- `docs/history/original_manual_page_map.md`: visual page-by-page source map.
- `docs/audits/archived_emulator_equation_audit.md`: independent emulator audit.
- `docs/provenance/equation_ledger.csv`: equation attribution and status.
- `docs/provenance/data_field_ledger.csv`: every committed CSV field.
- `docs/provenance/grt_field_mapping.csv`: audited XML mappings.
- `docs/history/`: separate Powley, Davis, Howell, Miller, and experimental histories.
- `src/modern_powley/original/`: only directly supported arithmetic and explicit failures.
- `src/modern_powley/later/`: later transcriptions, never labeled original.
- `src/modern_powley/experimental/`: opt-in prototype hypotheses.
- `src/modern_powley/modernized/`: promoted M01 inputs/geometry, M02 neutral powder-property evidence records, and M03 input/domain diagnostics; no powder screening, ranking, or ballistics prediction.
- `tests/`: unit, reference, regression-reproduction, and provenance tests.

Legacy CSVs, plots, scripts, and notebook outputs remain for auditability. They
are stale unless accompanied by a current generation manifest, and they do not
become measured data merely because they are committed.

## Reproducible Audit Commands

```bash
uv sync --locked
uv run pytest -q
uv run python scripts/audit_regression.py
uv run python scripts/generate_audit_inventory.py
uv lock --check
git diff --stat
```

The regression command reports in-sample artifact reproduction only. It is not
independent validation.

## Source and Data Policy

Every scientific value must retain units and one of the attribution classes in
the ledgers. GRT output is modeled data. Missing powder values remain missing;
they are never filled with a mean or borrowed from another powder. Commercial
relative burn-rate charts are rough ordinal references, not deterministic
internal-ballistics mappings.
