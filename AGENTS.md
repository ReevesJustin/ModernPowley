# ModernPowley Agent Guide

## Mission

ModernPowley preserves an evidence-based reconstruction of Homer Powley's
historical method and authorizes a separate, provenance-controlled modernized
development program. Correct attribution, model boundaries, and explicit
uncertainty take priority over producing a numerical result.

This repository does not provide loading recommendations. Do not introduce
charge advice, component substitutions, pressure assurances, burnout assurances,
or generic safety language that obscures a specific technical limitation.

## Environment: Use uv

`uv` is the only supported environment and dependency manager.

```bash
uv sync --locked
uv run pytest -q
uv run python scripts/audit_regression.py
uv run python scripts/generate_audit_inventory.py
uv lock --check
```

- Run Python tools through `uv run`; do not call project tooling with bare
  `python`, `python3`, `pip`, or an activated ad hoc virtual environment.
- Declare runtime dependencies in `[project].dependencies` and development tools
  in `[dependency-groups].dev` within `pyproject.toml`.
- After dependency changes, run `uv lock`, commit `uv.lock`, then verify with
  `uv sync --locked` and `uv lock --check`.
- Keep `.python-version` consistent with the supported range in `pyproject.toml`.
- Do not recreate `requirements.txt`; uv metadata and `uv.lock` are authoritative.

## Authority and Attribution

Every scientific equation, constant, field, mapping, historical statement, and
derived artifact must use one of the repository's attribution classes:

1. Original Powley, directly sourced
2. Later Davis transcription or extension
3. Howell correction
4. Miller modification
5. GRT-derived parameter or behavior
6. ModernPowley experimental hypothesis
7. Modernized Powley promoted method
8. Empirical regression
9. Derived quantity
10. Agent-generated assumption
11. Unknown or unresolved

Relevant evidence lives in:

- `reference/source_ledger.csv`
- `docs/provenance/equation_ledger.csv`
- `docs/provenance/constant_ledger.csv`
- `docs/provenance/data_field_ledger.csv`
- `docs/provenance/grt_field_mapping.csv`
- `docs/audits/modern_powley_full_repository_audit.md`

The searchable manual transcription is
`reference/powley_manual/powleysmanuals1.md`. It contains OCR errors and is a
navigation aid, not independent primary evidence. Verify substantive wording,
numbers, symbols, page locations, and table boundaries against the scanned
manual identified by `SRC-POWLEY-1961-MANUAL`. Do not silently repair ambiguous
OCR or promote it to a sourced equation.

## Model Boundaries

- `src/modern_powley/original/` may contain only directly sourced original
  arithmetic or explicit `MissingProvenanceError` failures.
- `src/modern_powley/original/` is under an evidence-only maintenance policy.
  Behavioral changes require newly retained primary evidence or correction of a
  demonstrated transcription or implementation error. Modern substitutions,
  fitted scale data, and later methods are prohibited there.
- `src/modern_powley/later/` keeps Davis, Howell, Miller, and emulator material
  separate from original Powley.
- `src/modern_powley/experimental/` contains unvalidated ModernPowley behavior.
  Experimental calculations must require `allow_unvalidated=True`.
- Promoted modernized behavior lives in `src/modern_powley/modernized/`, declares
  evidence and maturity classes, and must pass its phase gates. M01 units,
  geometry, serialization, and historical adapters; M02 neutral powder
  identity/property evidence records; and M03 operation-relative input and
  literal-domain diagnostics; and M04 declarative criterion and outcome records
  are authorized there. Positive M03 or M04 results are not solver readiness,
  suitability, safety, recommendation, or physical validation. Catalog
  screening, prediction, ranking, and later-phase behavior remain absent.
- `modernized/` may call verified historical scalars only through
  `modernized/adapters/original.py`. `original/` must never import
  `modernized/`.
- Never describe the Davis formula, the kwk emulator, `Ba_target`, `Ba_eff`, or
  the charge regression as an original Powley equation.
- Never call `Ba_eff` ballistic efficiency.
- Do not fill missing historical operations by inference. Fail explicitly and
  update the unresolved-source list.

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

## Tests and Changes

### Modernization milestone governance

- Read the applicable canonical specification under
  `docs/modernization/milestones/` before changing modernized code. The
  specification is the scope authority; accepted decision records are binding
  refinements, while completion reviews are evidence and never substitutes for
  specifications.
- Do not implement a milestone until its canonical specification exists and is
  explicitly `authorized`. Do not treat a recommendation in a completion review
  or roadmap as authorization.
- Do not broaden a milestone for implementation convenience. Propose a scope
  change explicitly before coding it.
- Preserve accepted milestone specifications as historical records. Never
  retroactively edit an acceptance gate merely to match an implementation.
- Record an approved specification change in a dated amendment or decision
  record that identifies changed sections, rationale, and whether scope is
  broadened, narrowed, or clarified. Update materially affected tests.
- For M05 and later: draft and review the specification against evidence and
  architecture, commit it in a planning commit, mark it `authorized`, then
  implement; record decisions separately; complete tests/ledgers/validation;
  create the completion review; and mark `accepted` only after all gates pass.

The controlled milestone statuses are `planned`, `authorized`, `in_progress`,
`implemented`, `accepted`, `superseded`, `blocked`, and `evidence_limited`.

Before changing model behavior, add or update the narrowest relevant test:

- `tests/unit/` for units, geometry, validation, and canonical arithmetic
- `tests/reference/` for source-backed worked examples and transcriptions
- `tests/provenance/` for source failures, mappings, hashes, and artifact policy
- `tests/regression/` for reproduction of quarantined committed behavior

Always run:

```bash
uv run pytest -q
uv run python -m compileall -q src scripts tests
uv lock --check
git diff --check
```

Also validate CSV column counts, JSON syntax, local documentation links, and
artifact hashes when touching ledgers, notebooks, or generated files.

## Documentation and Artifacts

- Put current-facing facts in `README.md` and `docs/`; preserve superseded claims
  through git history/checkpoint tags rather than leaving them implicitly active.
- Every generated artifact needs inputs and hashes, generating script and hash,
  repository commit, command, environment, timestamp, output hash, and status.
- Never manually edit a generated scientific output. Regenerate it or mark it
  stale with the missing manifest facts explicitly unknown.
- Report in-sample metrics as in-sample. Do not use `validated`, `confirmed`,
  `proven`, `empirical`, `calibrated`, or equivalent language without evidence
  matching that exact claim.

## Repository Hygiene

- The worktree may contain audit work in progress. Do not revert, overwrite, or
  reformat unrelated user changes.
- Preserve the checkpoint tag `pre_audit_agent_derived_prototype` and never
  rewrite history unless the user explicitly requests it.
- Use `rg`/`rg --files` for search and `apply_patch` for manual text edits.
- Keep changes scoped; do not revive disabled legacy selectors or generators.
- At completion, report changed files, uv commands run, tests, unresolved
  questions, sources still needed, and what remains unverified.
