# M06 Pivot And Screening-Tool Direction Handoff

## Repository State

- Branch: `main`.
- Final commit: `81f77ff32236e0942e16f49b520b2ccd62dc71b2` (this checkpoint's
  parent; `origin/main` synchronized at closure).
- Worktree: clean at closure. `just check` passes (486 tests, ruff clean,
  `uv lock --check` clean).
- Historical tag `pre_audit_agent_derived_prototype` unchanged.
- No code was written this session. Every change is documentation, a script
  fix, and one CI workflow line. `original/`, `later/`, and all M01-M05
  `modernized/` source files are byte-identical to session start.

## What Changed This Session, In Order

1. Drafted an unauthorized empirical-load "Phase 2" source-admission
   requirements proposal, then revised it after review (three-axis source
   classification, multi-valued relationship assertions, corrected a
   reversed replication-credit rule, corrected an over-attribution of a
   reviewer recommendation to "maintainer-stated"). Status: `planned`,
   **paused per explicit maintainer instruction** — do not expand further
   without a concrete need.
2. Found and fixed a real defect in `scripts/generate_audit_inventory.py`:
   it silently overwrote a hand-maintained ledger (dropped 315 rows to
   ~126 under an incompatible 7-column schema) and a hand-maintained
   manifest field. Added a refusal guard (byte-for-byte for the two CSVs,
   field-for-field excluding an explicit volatile-key allowlist for the
   manifest), fixed a CI shallow-checkout gap that made the new regression
   test fail on GitHub, and fixed a second real gap a reviewer found
   (manifest built after the CSVs were written, risking a partial write on
   any mid-build failure). This is `docs/provenance/generate_audit_inventory_ownership.md`;
   the fix is real and accepted, not a draft.
3. Supplied and provenance-reviewed a real DEVA test-protocol transcription
   (`docs/modernization/reviews/deva_14981_protocol_provenance_note.md`,
   decision `source_intake_not_ready`). Corrected twice after review: wrong
   order reference/date in the first pass (14.981 / February 2020, not
   "14.98 T" / 1990-03-06), then "one observation" (it's seven, one
   configuration), an unsupported "one lot" claim, and "synthetic-adjacent"
   language (real data is never described that way). The client's name and
   address are redacted throughout — **not a resolved question**; that is
   the maintainer's to decide if this report is ever pursued further.
4. Drafted an M06 (pressure/velocity baseline) specification, revised twice
   after review. First draft wrongly defaulted to generic, method-agnostic
   "architecture with no promoted method" — corrected: the actual first
   available capability is wrapping `later/davis.py`'s already-reconciled
   velocity/pressure chain (EQ-077/EQ-081) through a `modernized/adapters/
   davis.py`-style adapter, mirroring the existing `adapters/original.py`
   pattern. Second revision fixed three more factual errors (overclaimed
   "validated domain" for Table 4's lookup bounds, cited 0.18% instead of
   the actual 0.284% maximum reconciliation discrepancy, "never a sample"
   was wrong for DEVA's seven shots) and added missing pressure-method
   (crusher vs. piezoelectric) and propellant-scope (Davis has no evidence
   for Vihtavuori N140) cautions. **Status: `planned`, not authorized.
   Decision 1 (confirm Option A over Option B) is explicitly still open.**
5. **The maintainer then reframed the product objective directly, and this
   is the load-bearing finding of the session — read this before doing
   anything else with M06 or M04:** the intended product is a simple
   propellant candidate-screening tool (not a GRT/QuickLOAD replacement).
   Screening criteria: adequate case fill, and probable burnout (the
   breech-face distance where propellant is fully converted to gas — a
   core original-Powley operational-window concept, not a refinement).
   Historical reconstruction, record architecture, and the Davis adapter
   are *supporting* work, not the product objective themselves.

## The Key Technical Finding (Verify This Is Still True Before Building Anything)

Investigating the screening-tool direction found that almost everything
needed for the *first two* screening criteria already exists, accepted, and
tested in M01/M04 — this was not known or drafted for before this session,
and no milestone document currently states it:

- **Expansion ratio** is already computable end-to-end:
  `original_total_expansion_ratio` in `modernized/adapters/original.py`
  wraps verified original-Powley geometry (`original/geometry.py`). Nothing
  new needed for the computation.
- **Case fill ratio** is already implemented, accepted, tested, and
  exported: `charge_to_measured_usable_water_capacity_mass_ratio`,
  `charge_to_gross_water_capacity_mass_ratio`, and
  `charge_to_estimated_usable_water_capacity_mass_ratio` in
  `modernized/geometry.py` (tested at
  `tests/unit/test_m01_records_and_geometry.py:209`, exported from
  `modernized/__init__.py`). This is exactly the "empty case volume in gr
  H2O minus bullet-displaced volume" ratio the maintainer described as
  trivial — it was already built, just never surfaced as a screening
  output. **An M01 amendment was proposed for this and is unnecessary —
  do not draft one; the function already exists.**
- **M04's criterion vocabulary already supports the needed bound types**:
  `CriterionForm.NUMERIC_POINT_INSIDE_INTERVAL`,
  `NUMERIC_AT_OR_ABOVE`/`NUMERIC_AT_OR_BELOW` in
  `modernized/screening_criteria.py`. No new M04 record types needed either.
- **Real, scan-verified primary-source evidence exists for the burnout
  criterion's bound**, personally checked against
  `reference/powley_manual/powleysmanuals1.pdf` page 6 (manual page 6,
  "BORE CAPACITY" section) this session, not just the OCR transcription:
  > "all the powders selected by the computer will have completely burned
  > by the time the gas expansion has reached a value of 2, or at most, 4."

  And manual page 7 ("SPECIAL CONDITIONS"), a related but distinct
  practicality floor, also verified against the scan:
  > "If the Expansion Ratio of your gun comes to a value less than 4.0,
  > your gun will not perform properly with loads selected by your
  > computer... the remedy is usually another gun."

  **Important caveat, not yet resolved:** the burnout sentence is scoped to
  "powders selected by the computer" — i.e., it is Powley's own reassurance
  about his full selection procedure (which includes the evidence-limited
  Arrow 2 pressure-band selection), not necessarily a standalone bound
  usable for an arbitrary candidate propellant that hasn't gone through
  that selection. Whether/how this generalizes into a reusable screening
  bound is unresolved and needs its own careful treatment, not an assumed
  yes.
- Powley's own 0.80/0.86 loading-density convention
  (`original/charge.py:loading_density`) is the existing evidence anchor
  for a fill-ratio band, for the powders it's sourced for.

## What Was Proposed But Not Done

The session ended mid-turn on this exact point. The last concrete proposal,
**not yet built, not yet agreed to in final form**: a worked
example/test wiring the existing pipeline — M01 geometry records to the two
existing ratio functions above, into real M04 criterion instances using the
verified ER 2-4/≥4 and 0.80/0.86 bounds, evaluated for one example load — so
the maintainer can see exactly what it produces before deciding whether it
becomes a permanent fixture, a new test, a new small module, or something
else. **This is the concrete next step**, but it needs the maintainer's
go-ahead on:

1. Whether to proceed with that worked example now.
2. How to resolve the "powders selected by the computer" scoping caveat on
   the burnout bound before treating it as a general screening criterion.
3. Where any real, non-test criterion definitions should live (a new
   module? which evidence-ledger entries do they need?), since M04's
   "no production criteria" framing until now has always meant literally
   none exist yet.

## Explicit Repository Status Summary

| Item | Status | Notes |
|---|---|---|
| Empirical-load Phase 2 draft | `planned`, paused | Do not expand without concrete need. |
| DEVA 14981 provenance note | `documentation_only`, decision `source_intake_not_ready` | Client PII redacted, not resolved. |
| `generate_audit_inventory.py` guard | Implemented, accepted | Real fix, not a draft. |
| M06 (Davis adapter) draft | `planned`, not authorized | Decision 1 (Option A vs. B) still open; may now be secondary to the screening-tool direction below. |
| Screening-tool direction (fill ratio + burnout via M04) | **Not yet drafted as a specification anywhere** | This session's actual conclusion; the technical finding above is the starting point for whoever picks this up. |

## Future-Session Start Instructions

Read this checkpoint fully before touching M04, M06, or any screening work.
Verify the file/line references above still match (a future session may
have changed them). Do not re-derive the expansion-ratio/fill-ratio finding
from scratch — it is already confirmed here. Do not draft an M01 amendment
for fill ratio. Confirm with the maintainer before writing the worked
example described above, since the burnout-bound scoping caveat is
unresolved and the maintainer may want to resolve it before any code is
written. Auto-memory for this project (outside the repository) also has
entries reflecting this session's corrections and findings; consult it if
available.
