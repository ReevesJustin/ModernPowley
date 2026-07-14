# Audit Completion Report

Date: 2026-07-14
Branch: `main`
Preserved commit: `6485b3d2f4c9fb48e2349f548ba7c79c8821947d`
Preservation tag: `pre_audit_agent_derived_prototype`

## Delivered

- full 24-finding repository audit with severity, evidence, units, impact, test and disposition;
- complete pre-audit file inventory with hashes;
- source, equation, constant, data-field, GRT-mapping and legacy-artifact ledgers;
- six-part history separated by attribution;
- source-backed original arithmetic and explicit missing-source failures;
- separate Davis transcription and unresolved Howell/Miller placeholders;
- opt-in experimental namespace for `Ba_target`, `Ba_eff` and charge regression;
- repaired GRT parser with raw unit-bearing destination fields;
- disabled legacy selector, analysis, generator, plot and notebook workflows;
- corrected current-facing documentation;
- unit, reference, regression-reproduction, provenance, parser and artifact tests.

## Verification

```text
uv sync --locked
locked environment synchronized successfully

uv run pytest -q
36 passed in 0.03s

uv run python -m compileall -q src scripts tests
success

uv lock --check
success

CSV structural validation: success
JSON structural validation: success
Local Markdown link validation: success
git diff --check: success
Checkpoint tag dereference: exact match
```

Regression artifact reproduction over 10 rows:

```text
MAE:        1.0460839220 gr
RMSE:       1.3505634115 gr
Max |err|:  2.8916517475 gr
Mean error: -0.9237984375 gr
R2:         0.9942624233
```

These are in-sample descriptive values, not validation.

## Worktree Summary

- 21 existing files modified;
- 58 files added;
- 1 legacy environment file removed after migration to uv;
- no historical data or plot artifact deleted;
- no git history rewritten;
- no commit created by the audit.

## Explicitly Unverified

The repository does **not** yet contain an exact complete original-Powley
calculator. Exact original powder-scale boundaries, velocity equation and
pressure equation remain unavailable. Davis pages, Howell's 1997 source,
Miller's 1999 source, authoritative GRT parameter semantics, row-level load
provenance, 21 cited powder artifacts, burnout evidence and the original
regression fit procedure remain missing. Those paths fail or stay excluded; no
substitute equation or value was invented.

See `modern_powley_full_repository_audit.md` for the detailed unresolved-question
and sources-needed lists.
