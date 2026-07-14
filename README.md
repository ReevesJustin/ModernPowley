# ModernPowley: Repository Under Audit

> [!CAUTION]
> Current powder rankings are not validated. The historical `Ba` target and
> `Ba_eff` ranking logic are experimental, and some equations, field mappings,
> and historical attributions were introduced without adequate provenance.
> Current and preserved prototype outputs must not be treated as load
> recommendations or as evidence of pressure, velocity, or burnout performance.

This repository is an evidence-based reconstruction of the Powley Computer plus
a quarantined record of later ModernPowley experiments. The agent-derived
prototype is preserved at tag `pre_audit_agent_derived_prototype` (commit
`6485b3d2f4c9fb48e2349f548ba7c79c8821947d`). History was not rewritten.

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
original velocity equation, and the original pressure equation remain
source-incomplete. Those original operations fail
with `MissingProvenanceError`; they are not guessed from later transcriptions.

The following are quarantined and unvalidated:

- `Ba_target = clamp(0.85 - 0.05*RC, 0.45, 0.90)`;
- `Ba_eff = Ba * [a0 + (1-a0)*z2/2]`;
- `Wc = 0.71 * V0^1.02 * Ltravel^0.06`.

They live under `src/modern_powley/experimental/` and require the explicit
keyword `allow_unvalidated=True`. `Ba_eff` is not ballistic efficiency.

## Repository Guide

- `docs/audits/modern_powley_full_repository_audit.md`: finding-by-finding audit.
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
