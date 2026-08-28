# M06: Pressure And Velocity Baseline

## Status

`planned` — draft canonical specification, not authorized. Nothing in this
document authorizes an implementation, a record schema, a serializer, a
promoted pressure or velocity method, or any change to the accepted M01-M05
foundation, the accepted empirical-load Phase 1 contract, or `later/davis.py`.
It becomes the scope authority for M06 only if the maintainer separately
authorizes it. The roadmap's existing "Future Phase Concept M06" sketch
(`docs/modernization/modern_powley_roadmap.md`) is a planning recommendation,
not this specification.

**Revision note:** an earlier version of this draft proposed a generic,
method-agnostic `DeclaredMethod`/`BaselineRecord` architecture with no
promoted method, reasoning that no pressure/velocity equation was available
because the original-Powley scales are evidence-limited. Reviewer feedback
correctly identified this as substituting infrastructure for the milestone's
actual goal: the modernized program does not depend on completing the
historical reconstruction, and a real, already-reconciled candidate method
was sitting unexamined in `src/modern_powley/later/davis.py`. This revision
leads with that candidate instead.

## Purpose

No milestone through M05 computes a pressure or velocity value anywhere in
`modernized/`. M06 is where that capability should first appear. The
question this draft resolves first, before any implementation detail, is
*how*.

## Scope Decision — Resolve This Before Anything Else Below

**Finding:** `src/modern_powley/later/davis.py` already implements Davis's
complete 1981 velocity and pressure chain — `muzzle_velocity_fps` (EQ-077)
and `historical_crusher_pressure` (EQ-081), plus every geometry/charge input
they need. `docs/audits/davis_1981_equation_and_example_reconciliation.md`
independently re-derived Davis's printed `.30-06` worked example at 40-digit
precision and found the implementation agrees with Davis's own arithmetic to
within source-rounding error (largest relative difference 0.18% across
fifteen intermediate values; the final printed velocity and pressure agree to
0.023% and 0.007% respectively). This is attribution class `davis` (repo-wide
class 2, "Later Davis transcription or extension") — never original
Powley — and is already independent of the evidence-limited original-Powley
reconstruction, exactly as the project's own modernization principle says
later work should be. No new equation, transcription, or evidence intake is
needed to use it.

**Option A (this draft recommends this option):** M06's first deliverable is
a `modernized/adapters/davis.py` module, mirroring the existing
`modernized/adapters/original.py` pattern exactly, that wraps Davis's already
-reconciled velocity and pressure functions behind M01 `Quantity`-aware,
explicitly attributed entry points and produces an immutable, attributed
baseline record. This delivers an actual, working, evidence-grounded
pressure-and-velocity computation the first time — not a hypothetical
plugin surface waiting for a method that may never arrive.

**Option B (deferred, not recommended now):** the earlier generic
`DeclaredMethod`/`BaselineRecord` architecture, decoupled from any specific
method. Kept only as a possible later increment if a second real method
someday needs the same plumbing (a recovered original-Powley scale, or a new
empirical fit that has cleared its own hypothesis-record and promotion
process). Building it now, before a second method exists to design it
against, risks exactly the wrong kind of speculative machinery — it is not
built out further in this draft.

This draft is written around Option A. Everything below is provisional on
the maintainer confirming Option A over Option B (see decision 1).

## Relationship To M01-M05 And `later/davis.py`

- Reuses M01 `Quantity`, `Unit`, `Dimension`, and provenance primitives
  wherever exact. M01 has no pressure/velocity/time dimension; M06 does not
  amend M01 to add them (see decision 5).
- Does not modify `src/modern_powley/later/davis.py` — no equation,
  constant, or Table 4 value changes. M06 wraps it exactly as
  `modernized/adapters/original.py` wraps `original/`, without executing
  research into whether Davis's equations are correct (already independently
  reconciled) or reopening that reconciliation.
- Carries Davis's existing dual attribution forward unchanged: the
  repo-wide attribution class is `davis` (equation ledger), and the
  `modernized/` `EvidenceClass` enum's closest existing value is
  `OTHER_PUBLISHED_PRIMARY` — Davis's EQ-077/EQ-081 ledger rows already carry
  `verification_status: user_reviewed_access_restricted_primary` and the
  exact disposition notes ("printed by Davis and attributed by Davis to
  Powley; no original-source verification" and "not modern piezoelectric
  PSI; explicit F2 required") that any M06 record must preserve, not
  paraphrase away.
- References M02/M03/M04/M05 records as optional, non-duplicating inputs
  only where Davis's own inputs need them (for example, an M05 charge-region
  record is never required).

## Authorized Scope

A later, separately authorized implementation task may add only:

1. `modernized/adapters/davis.py`: explicit one-way wrapper functions for
   Davis's existing geometry/charge chain and its two terminal outputs
   (`muzzle_velocity_fps`, `historical_crusher_pressure`), each requiring
   explicit M01 records as input (mirroring `original.py`'s
   `HistoricalScalarResult` pattern) and performing only unit conversion via
   `.to(Unit.X)` before calling the existing, already-reconciled `later.davis`
   functions unchanged;
2. an immutable `DavisBaselineRecord` (exact name is an implementation
   decision) carrying: the computed velocity (ft/s) and/or historical
   crusher pressure value, an explicit, un-droppable statement that this
   pressure is copper-crusher, not modern piezoelectric PSI, the Table 4 F2
   value used and its existing `pending_retained_primary_visual_verification`
   / medium-confidence status, the exact EQ-077/EQ-081 (and supporting
   EQ-061 through EQ-086) equation-ledger references, exact input record
   references, domain bounds actually enforced (`0.20<=A<=1.00`,
   `5.0<=R<=13.0`, no extrapolation — Davis's existing `ValueError` behavior
   is preserved, not loosened), and the common envelope (identity, version,
   activation, evidence class, maturity, creation/review context, lineage)
   M01-M05 already require;
3. explicit rejection, not extrapolation or silent substitution, for any
   input outside Davis's existing validated domain, matching
   `later/davis.py`'s current behavior;
4. tests that reproduce the existing independent `.30-06` worked-example
   agreement (`tests/reference/test_davis_equation_reconciliation.py`)
   through the new adapter, proving the adapter's unit handling and record
   construction, not re-deriving Davis's equations again;
5. documentation stating the exact attribution, confidence-disclosure, and
   non-piezoelectric-pressure requirements above.

No authorized behavior changes `later/davis.py`, claims Davis's method is
scientifically validated beyond source-example reproduction, or builds
Option B's generic method contract.

## Explicit Exclusions

- Any change to `later/davis.py` equations, constants, Table 4 values, or
  its existing domain/rejection behavior.
- Promotion of original-Powley pressure/velocity arithmetic — it remains an
  explicit `MissingProvenanceError` stub; this milestone does not depend on
  it and does not change it.
- CUP-to-PSI or any cross-standard pressure conversion.
- Any claim, test, or documentation statement that Davis's method (as
  distinct from the adapter's faithfulness to it) is scientifically
  accurate for real firearms beyond reproducing Davis's own printed
  examples.
- Using the DEVA report, or any other single real observation, as
  validation. See "Software Correctness Versus Scientific Validity."
- Option B's generic `DeclaredMethod` architecture, dataset cohorts/splits,
  M07/M08/M09 work, and any database/dataframe/plotting/web/CLI surface.
- Amending M01-M05's accepted specifications, APIs, or serializers.

## Software Correctness Versus Scientific Validity

**Software correctness**, for this milestone, means: the adapter converts
M01 quantities into exactly the inputs Davis's already-reconciled functions
expect, calls those functions unchanged, and constructs a record whose
fields, units, domain bounds, and attribution exactly reflect that call.
Because the functions being wrapped are fixed, known, and already
independently reconciled — not an arbitrary caller-supplied callable — this
is ordinary, fully testable software engineering today, using the existing
worked-example fixtures. It requires no new evidence.

**Scientific validity** means: Davis's 1981 method, for a real load, predicts
a pressure or velocity close enough to reality to be useful. The existing
reconciliation establishes only that the repository's Davis implementation
matches *Davis's own printed arithmetic* — a claim about implementation
fidelity, not about physical accuracy. Nothing in this repository currently
establishes the latter. The one informally supplied DEVA observation (see
`docs/modernization/reviews/deva_14981_protocol_provenance_note.md`) — one
configuration, seven shot observations, not a dataset — could at most serve
as one illustrative real-world comparison point for a Davis-computed
estimate on the same configuration, explicitly labeled as such; it is never
validation, never a sample, and never evidence of general accuracy. Formal
scientific validity requires the versioned hypothesis record `AGENTS.md`
requires for model variants and, for anything beyond source-example
reproduction, M09's dataset/cohort/split infrastructure, which this
specification does not build.

## Evidence Gaps: What They Block

| Gap | Blocks drafting this spec? | Blocks implementing the Davis adapter? | Blocks claiming source-example reproduction? | Blocks claiming real-world scientific validity? | Blocks M09 evaluation? |
|---|---|---|---|---|---|
| Table 4 is medium-confidence, pending primary visual verification | No | No — the adapter surfaces this status honestly rather than resolving it | No | Yes | Yes |
| No dataset/cohort/split infrastructure exists | No | No | No | Yes | Yes |
| Only one informally supplied real observation (DEVA), uncustodied, unadmitted | No | No | No | Yes, alone | Yes |
| Davis's method has no versioned hypothesis record | No | No | No | Yes | Yes |
| Original-Powley pressure/velocity scales remain evidence-limited | No | No — Option A does not depend on them | No | No — orthogonal to Davis | No |

Nothing here blocks drafting or implementing the adapter itself. Everything
about *scientific validity beyond reproducing Davis's own printed examples*
remains blocked, and this specification does not claim otherwise anywhere.

## Non-Implications

Constructing a `DavisBaselineRecord`, passing M06's tests, or this
specification being authorized establishes none of the following:

- that Davis's computed pressure or velocity is accurate, safe, or
  recommended for any real load;
- that historical crusher pressure is equivalent to, or convertible to,
  modern piezoelectric PSI;
- that Davis's Table 4 factor is fully verified against the primary NRA
  publication — it remains medium-confidence pending primary images;
- suitability, a starting or maximum charge, or any loading instruction;
- that original-Powley pressure/velocity arithmetic is now available —
  it is unchanged and still evidence-limited;
- M07/M08/M09/M11 readiness.

## Acceptance Gates

A later implementation may mark this milestone `accepted` only when all
gates pass:

1. `src/modern_powley/later/davis.py` is unmodified — no equation, constant,
   or Table 4 value changes; its existing domain-rejection behavior is
   unchanged.
2. `modernized/adapters/davis.py` accepts only explicit M01 records as
   input; no bare floats or ad hoc unit handling.
3. All unit conversion uses M01's `.to(Unit.X)`, not inline arithmetic.
4. Every produced record surfaces the Table 4 F2 medium-confidence /
   pending-primary-verification status and the copper-crusher (not modern
   PSI) statement; neither can be omitted, defaulted, or paraphrased away.
5. Domain bounds (`0.20<=A<=1.00`, `5.0<=R<=13.0`) are enforced exactly as
   `later/davis.py` already enforces them; no extrapolation is added.
6. Tests reproduce the existing independent `.30-06` worked-example
   agreement (source rounding only, no implementation defect) through the
   new adapter.
7. Every record cites EQ-077/EQ-081 (and its supporting EQ-061 through
   EQ-086 chain), the `davis` repo-wide attribution class, and the
   maintainer-selected `EvidenceClass` value (decision 2).
8. No test, docstring, or documentation claims validation, confirmation, or
   real-world accuracy beyond source-example reproduction.
9. No import from `original/`, `experimental/`, legacy scripts, or any
   M01-M05 file changes beyond what this specification authorizes.
10. `just check` passes; a completion review maps every gate above.

## Decisions Requiring Authorization

1. **Confirm Option A over Option B.** This draft recommends wrapping
   Davis's already-reconciled chain (Option A) as M06's actual first
   deliverable, instead of building a generic method-agnostic architecture
   with no promoted method (Option B, deferred). This is the decision every
   other item below depends on.
2. **`EvidenceClass` mapping.** Is `OTHER_PUBLISHED_PRIMARY` the right
   existing value for Davis-derived M06 records, or does the `EvidenceClass`
   enum need a more specific addition (the enum currently has no dedicated
   "later Davis" value, unlike the repo-wide ledger's `davis` class)?
3. **Table 4 confidence disclosure mechanism.** A typed status field, a
   required free-text disclaimer, or both?
4. **Supporting geometry outputs.** Does M06 expose only the final
   velocity/pressure, or also Davis's intermediate geometry values (seating
   depth, expansion ratio, etc.) as their own attributed records?
5. **Pressure/velocity representation.** Reuse and extend the empirical-load
   Phase 1 source-preserving reported-value pattern (as Option A implicitly
   assumes), or amend M01 to add native pressure/velocity dimensions? The
   latter needs its own M01 amendment process.
6. **Serialization.** A strict schema now (`modern_powley.m06.v1`,
   matching M02-M05), or in-memory-only until real usage demonstrates need?
7. **The DEVA anchor point.** May it ever be cited, once its own custody/
   privacy questions resolve, as one explicitly-labeled illustrative
   comparison alongside a Davis-computed estimate for the same
   configuration — never as validation?
8. **Option B's status.** Confirm it is deferred, not abandoned or silently
   forgotten, pending a second real method that would need shared plumbing.

No implementation, schema, or authorization follows from this document. The
next step is the maintainer's review of the eight decisions above.
