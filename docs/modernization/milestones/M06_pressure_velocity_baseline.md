# M06: Pressure And Velocity Baseline

## Status

`planned` — draft canonical specification, not authorized. Nothing in this
document authorizes an implementation, a record schema, a serializer, a
promoted pressure or velocity method, or any change to the accepted M01-M05
foundation or the accepted empirical-load Phase 1 contract. It becomes the
scope authority for M06 only if the maintainer separately authorizes it,
following the same draft-review-decide-authorize sequence used for M05 and
Phase 1 (`AGENTS.md`, "Modernization milestone governance"). The roadmap's
existing "Future Phase Concept M06" sketch
(`docs/modernization/modern_powley_roadmap.md`) is a planning recommendation,
not this specification, and is superseded as the scope authority once (if)
this document is authorized; it remains a historical planning record.

## Purpose

M01-M05 built inputs, geometry, powder-property evidence, diagnostics,
decision records, and charge-region records without computing a pressure or
velocity value anywhere in `modernized/`. Empirical-load Phase 1 built
immutable evidence-record containers, also without computing anything. No
milestone has yet given the modernized program a capability to produce a
pressure or velocity number at all — accepted or otherwise.

M06 proposes that capability, narrowly: **the software capability to
construct a fully attributed, immutable, structurally validated pressure
and/or velocity baseline record from one explicitly declared, versioned
method plus an explicit load configuration.** M06 does not itself supply,
validate, or promote any specific method. Whether a real method's *output* is
scientifically trustworthy is a separate question this specification
deliberately does not answer — see "Software Correctness Versus
Scientific Validity" below.

## Why This Scope, Not A Working Prediction

Three facts in the current codebase and evidence base directly shape this
proposal, and are the reason it is scoped to architecture rather than to any
actual prediction:

1. **No original-Powley pressure or velocity equation is reconstructed.**
   `src/modern_powley/original/pressure.py` and `velocity.py` are explicit
   `MissingProvenanceError` stubs — the 1961 manual's muzzle-pressure and
   velocity graphical scales are not source-complete
   (`complete_historical_method: evidence_limited` in `TODO.md`). The only
   working original arithmetic
   (`src/modern_powley/modernized/adapters/original.py`) covers sectional
   density, mass ratio, effective bore diameter, projectile travel, barrel
   volume and expansion ratios, and charge weight for eight named IMR
   powders — none of it pressure or velocity.
2. **No alternative method is promoted.** Davis's equations, the archived
   emulator, GRT-derived behavior, and any regression remain quarantined
   (`TODO.md`, "Quarantined And Later Work") — evaluable as candidates in
   their own evidence class, but none is automatically part of the
   modernized method, and none has been.
3. **No measured-validation dataset exists.** The empirical-load evidence and
   validation workstream remains `planned`; its accepted Phase 1 admits only
   immutable record containers with conspicuously fictional fixtures — no
   scientific source, cohort, or split. Exactly one real, informally supplied
   measurement is currently known to this repository at all — a DEVA test
   protocol supplied as a plain-text transcription (see
   `docs/modernization/reviews/`, DEVA provenance review) — which is a single
   uncustodied anchor point, not a dataset, and is not formally admitted
   anywhere.

Given this, a specification that tried to promote a working, evidence-backed
pressure/velocity *prediction* would either have to fabricate evidentiary
support that does not exist, or stall indefinitely on data this repository
does not have and cannot manufacture. Neither is acceptable. This
specification instead separates two questions that the roadmap's earlier
concept sketch left bundled together: whether the **software** correctly
executes a declared computation (answerable now, with synthetic fixtures,
exactly as M01-M05 and Phase 1 did), and whether any particular **method's
output** is scientifically valid (not answerable now, and gated below).

## Relationship To M01-M05 And Phase 1

- Reuses M01 `Quantity`, `Unit`, `Dimension`, and provenance primitives
  wherever their existing semantics are exact. M01 currently defines no
  pressure, velocity, or time dimension (confirmed in
  `src/modern_powley/modernized/units.py`); M06 does not amend M01 to add
  them (see "Decisions Requiring Authorization").
- Reuses the empirical-load Phase 1 pattern for representing a
  not-yet-M01-native quantity: a source- or method-preserving reported-value
  union with explicit unit label, quantity definition, and uncertainty/
  precision references, rather than inventing a second, incompatible
  pattern. M06's baseline value is a *computed* counterpart to Phase 1's
  *reported* value — architecturally parallel, not the same type.
- References M02 powder-property records, M03 diagnostics, and M04 decision
  records as optional, exact, non-duplicating inputs where a declared method
  needs them, using the same `ExactReferenceRole`-style pattern M05 already
  established (`src/modern_powley/modernized/charge_regions.py`).
- References M05 charge-region records as an optional input only; M06 does
  not require a bounded charge region to exist, and does not compute one.
- Does not depend on the empirical-load workstream reaching cohorts or
  splits. M06's own correctness tests use synthetic fixtures, matching every
  prior milestone; only *evaluating* a real method's *accuracy* would need
  that infrastructure (see "Evidence Gaps" below), and no such evaluation is
  authorized by this document.

## Authorized Scope

A later, separately authorized implementation task may add only:

1. a `DeclaredMethod` identity structure: name, version, evidence class
   (reusing the repository's existing eleven attribution classes),
   maturity, applicable domain, exact required-input specification, and
   exact source/provenance references — describing a method, not executing
   research into which methods are correct;
2. a computed pressure-and/or-velocity reported-value structure, following
   the Phase 1 source-preserving pattern, extended with an explicit
   `computed_by_method` reference in place of (never in addition to, for the
   same field) a source-statement reference;
3. an immutable `BaselineRecord` that binds one `DeclaredMethod` invocation
   to its exact input record references (M01 geometry/inputs, optionally
   M02/M03/M04/M05 records), its computed value(s), an explicit domain/
   applicability statement, and the common envelope (identity, versioning,
   activation, evidence class, maturity, creation/review context, lineage,
   supersession) M01-M05 already require;
4. a narrow, explicit calling contract: given a `DeclaredMethod` (supplied
   by the caller as a plain callable plus its identity metadata, not
   selected or ranked by M06) and valid inputs, M06 constructs a
   `BaselineRecord` deterministically or raises an explicit, typed failure;
   M06 itself contains no pressure or velocity arithmetic and picks no
   method;
5. explicit failure/rejection behavior for out-of-domain inputs, missing
   required inputs, and dimensionally invalid outputs;
6. unit, architecture, provenance, and governance tests using conspicuously
   synthetic declared methods and fixtures (no real pressure/velocity
   equation is exercised as more than an interchangeable test double); and
7. documentation stating exactly this boundary.

No authorized behavior selects, ranks, validates, or recommends a method. A
`BaselineRecord`'s existence means only that some declared method produced
some value for some inputs — nothing about whether that value is close to
anything real.

## Explicit Exclusions

M06, as scoped here, does not authorize:

- an original-Powley, Davis, or any other named pressure/velocity equation's
  *admission* as a working method — that is a separate, later evidentiary
  and promotion decision per method, not a byproduct of this architecture;
- any claim, test assertion, or documentation statement that a
  `BaselineRecord`'s value is accurate, validated, safe, or recommended;
- CUP-to-PSI or any other cross-standard pressure conversion;
- model-family fallback, ensembling, or averaging across methods;
- ranking or comparing methods against each other;
- burn progression, burnout location, or muzzle-pressure/objective work
  (M07, M08);
- formal measured validation, error metrics, or holdout evaluation (M09) —
  M06 defines the record a future M09 evaluation would reference, but does
  not perform that evaluation;
- dataset cohorts, splits, or any empirical-load workstream phase beyond the
  accepted Phase 1 record containers;
- amending M01, M02, M03, M04, or M05's accepted specifications, APIs, or
  serializers;
- a database, dataframe, plotting, notebook, web/API, or CLI surface (M11).

## Software Correctness Versus Scientific Validity

This distinction is the spine of the specification and must be kept
explicit in every test, docstring, and future completion review:

**Software correctness** means: given a `DeclaredMethod` (including a
synthetic, fictional one used only in tests) and a fully specified set of
inputs, M06's architecture (a) calls the method with correctly unit-converted
arguments, (b) rejects out-of-domain or incomplete inputs before calling it,
(c) constructs a `BaselineRecord` whose fields, references, units, and
attribution exactly and deterministically reflect the call that was made,
(d) never silently substitutes a default, another method, or a cached value,
and (e) is fully verifiable today with synthetic fixtures, independent of
whether any real pressure/velocity equation exists yet. This is ordinary
software testing and requires no new evidence.

**Scientific validity** means: a specific method's output, for real inputs,
is close enough to a real measured pressure or velocity to be useful or
trustworthy for some stated purpose. This is not established by software
correctness, by an in-sample or source-example reproduction, by regression
reproduction against another unvalidated tool, or by any number of
`BaselineRecord`s existing. It requires the versioned hypothesis record
`AGENTS.md` already requires for empirical fits and model variants
(claim, assumptions, falsification, domain, calibration/held-out data,
failures, promotion requirements), and, for any claim beyond source-example
reproduction, the dataset/cohort/split and formal evaluation infrastructure
this specification explicitly does not build (M09's role, per the
empirical-load workstream). A `BaselineRecord` under this specification
carries no maturity value that means "scientifically validated"; the
existing `ModelMaturity`/`EvidenceClass` vocabulary is reused exactly, not
reinterpreted to imply more than it already means elsewhere in the
repository.

A future completion review for this specification must be able to state
plainly: "the architecture is tested and correct; no method admitted through
it has been scientifically validated" — and that must remain true regardless
of how many synthetic or even real `DeclaredMethod`s are later registered
against it, until a separate, explicit promotion gate (not part of this
specification) says otherwise for one specific method.

## Evidence Gaps: What They Block

Per the maintainer's explicit direction, gaps are classified by what they
block, not treated uniformly as blocking everything:

| Gap | Blocks drafting this spec? | Blocks implementing the M06 architecture? | Blocks admitting any real method? | Blocks M09 evaluation of a method? | Blocks promoting a method? |
|---|---|---|---|---|---|
| No original-Powley pressure/velocity equation exists | No | No | Yes, for that method specifically | N/A until admitted | Yes |
| Davis/GRT/emulator/regression remain quarantined | No | No | Yes, until independently evidence-reviewed and promoted under its own class | N/A until admitted | Yes |
| M01 has no pressure/velocity/time dimension | No (M06 uses its own reported-value structure, per Phase 1's precedent) | No | No | No | No |
| Empirical-load workstream has no cohort/split infrastructure | No | No | No (a method can be admitted with a narrow, explicit domain and no dataset, same as any M01-M05 record can exist without production data) | Yes | Yes |
| Only one informally supplied real observation (DEVA) exists, uncustodied | No | No | No, on its own — it is supporting evidence for one narrow domain point, not sufficient alone to admit a general method | Yes, for anything beyond a single anchor comparison | Yes |
| No versioned hypothesis record exists for any candidate method | No | No | Yes | Yes | Yes |

Nothing in this table blocks authorizing and implementing the architecture
itself. Everything in the "admitting/evaluating/promoting a method" columns
remains blocked, per method, until its own evidence is in hand — this
specification does not and cannot resolve that per-method work in advance.

## Non-Implications

Constructing a `BaselineRecord`, passing M06's tests, or this specification
being authorized establishes none of the following:

- that any pressure or velocity value is accurate, safe, or recommended;
- that a declared method is scientifically valid, calibrated, or superior to
  another;
- suitability, a starting or maximum charge, or any loading instruction;
- solver readiness, M07/M08/M09 readiness, or M11 readiness;
- that the original-Powley, Davis, or any other named method is admitted —
  admission of any specific method is a separate, later, per-method decision
  requiring its own evidence review and, where it is a fit or model variant,
  the versioned hypothesis record `AGENTS.md` requires.

## Required Future Implementation Deliverables

1. A design document and separate implementation decision record, following
   the same pattern as `docs/modernization/phases/` and
   `docs/modernization/decisions/` for M01-M05.
2. The smallest coherent module set inside `modernized/` (for example
   `modernized/baseline.py` or a `modernized/baseline/` package — exact
   naming is an implementation decision).
3. Tests using only synthetic, fictional `DeclaredMethod`s and fixtures,
   covering: correct unit handling, domain rejection, deterministic record
   construction, reference/lineage integrity, and architecture boundaries
   (no import from `original/`, `later/`, `experimental/`, or legacy
   scripts; no amendment to M01-M05 files).
4. A completion review mapping every gate below before status may become
   `accepted`, explicitly stating the software-correctness/scientific-
   validity distinction as fact, not aspiration.

## Decisions Requiring Authorization

This draft resolves none of the following:

1. **Overall scope acceptance** — is "architecture and record contract, no
   promoted method" the right first M06 increment, or does the maintainer
   want a narrower or broader first cut (for example, deferring even the
   `DeclaredMethod` contract until a real candidate method exists to design
   it against)?
2. **Pressure/velocity representation** — reuse and extend the Phase 1
   source-preserving reported-value pattern (as proposed), or amend M01 to
   add native pressure/velocity/time dimensions? The latter would require a
   separate M01 amendment process since M01 is `accepted`.
3. **Method-calling contract shape** — is a caller-supplied plain callable
   plus identity metadata (as proposed) the right interface, or should M06
   define a registry/protocol class instead? A registry raises the question
   of whether M06 would then be "selecting" methods, which this draft
   deliberately avoids.
4. **Serialization** — does M06 need its own strict schema (e.g.
   `modern_powley.m06.v1`), matching M02-M05's pattern, in this first
   increment, or should it start as an in-memory-only record type (no
   serializer) until real usage demonstrates the need, similar to how Phase
   1 stayed module-qualified before any export review?
5. **Relationship to the DEVA anchor point** — should the DEVA provenance
   review's single observation be usable, once the maintainer resolves its
   own open custody/privacy questions, as one synthetic-adjacent but
   real-world test case for the architecture (clearly labeled as one
   anchor, not validation), or should M06's tests remain entirely fictional
   until a real dataset exists? This draft defaults to entirely fictional
   fixtures, consistent with every prior milestone.
6. **Naming** — `M06_pressure_velocity_baseline.md` versus a more precise
   name reflecting the narrower "architecture only" scope (for example,
   distinguishing this from a hypothetical later "M06 Phase 2: promoted
   method").

No implementation, schema, or authorization follows from this document. The
next step is the maintainer's review of the six decisions above, resulting
in either an authorization decision record (mirroring
`docs/modernization/decisions/M05_records_only_authorization.md`) or a
determination that this draft should be revised.
