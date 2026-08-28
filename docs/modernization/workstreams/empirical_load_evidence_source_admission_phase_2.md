# Empirical Load Evidence Phase 2: Source Admission Requirements

## Status

`planned` — proposed draft only. This document is not authorized. It records a
documentation-only proposal for review. Nothing here authorizes an
implementation, a record schema, a serializer, a source selection, a
custody/licensing decision, or any change to the accepted Phase 1
specification, API, or `modern_powley.empirical_load_evidence.v1` schema. It
becomes a scope authority only if the maintainer separately authorizes it,
following the same draft-review-authorize sequence used for M05 and Phase 1.

**Revision note:** the original draft's flat source-classification field and
`independent_observation` relationship tag were exercised against the
checkpoint's named candidate example in
[`empirical_load_source_admission_deva14981_candidate_review.md`](../reviews/empirical_load_source_admission_deva14981_candidate_review.md)
and found to conflate independent concepts. The "Provenance" and "Duplicate
And Related-Observation Identifiability" sections below reflect that
revision. Status remains `planned`; the revision does not authorize anything
that was not already proposed.

## Purpose

Phase 1 defines how evidence is *represented* once it exists as a record:
immutable source/custody metadata, literal statements, normalized
configurations, shots, series, trace metadata, chronograph series, and
aggregates. It does not define when a source or observation is *eligible* to
become one of those records in the first place, nor how two admitted records
describing the same underlying test remain distinguishable from independent
evidence. This proposal drafts that eligibility layer, generically, before any
specific candidate source is selected.

This is deliberately source-agnostic. The July 2026 checkpoint
([`2026-07-15_empirical_evidence_phase_1_handoff.md`](../../checkpoints/2026-07-15_empirical_evidence_phase_1_handoff.md))
recommends a separate "Empirical Evidence Source Intake Authorization Review"
that considers exactly one named candidate package. That review is source
selection and custody/licensing authorization — item (1) in the checkpoint's
"Required Separation of Future Work." This proposal is upstream of that: it
asks what any candidate source, once selected, would have to satisfy for its
records to be admitted at all. It does not select, evaluate, or presuppose a
candidate, including the DEVA 14981 package the checkpoint names as a
possible-but-unselected example.

## Stale-Wording Check

Before drafting, the current milestone acceptance records were re-read against
the July checkpoint: `AGENTS.md`, `README.md`, `TODO.md`,
`docs/modernization/milestones/M05_charge_region_records.md`,
`docs/modernization/workstreams/empirical_load_evidence_records_phase_1.md`,
`docs/modernization/reviews/empirical_load_evidence_records_phase_1_completion_review.md`,
and the checkpoint itself. All state M05 `accepted` (records/serialization
only), Phase 1 `accepted` (records/serialization only, fictional fixtures),
and the parent workstream `planned`, consistently. No stale status wording was
found; none is corrected by this document.

## Relationship To Existing Documents

- Builds on the accepted Phase 1 common envelope, missingness/conflict/
  exclusion/duplication section, and component/measurement identity sections
  without modifying them.
- Formalizes, as explicit admission gates, the "Future Data-Intake Gates" and
  "Source Artifact And Licensing Requirements" sections already sketched in
  the parent
  [`empirical_load_evidence_and_validation.md`](empirical_load_evidence_and_validation.md)
  workstream document (`planned`).
- Does not replace, narrow, or broaden the checkpoint's named next work unit
  (source-specific authorization review); it proposes to precede it with a
  source-agnostic rubric that any candidate review could then apply.
- Is exercised, as a checklist only, against the checkpoint's named candidate
  example in the separate, documentation-only
  [`empirical_load_source_admission_deva14981_candidate_review.md`](../reviews/empirical_load_source_admission_deva14981_candidate_review.md).
  That review records how one example satisfies, fails, or exposes gaps in
  the requirements below; it does not select a source, decide custody or
  licensing, or admit any record, and this document remains the sole
  authority for the reusable requirements themselves.

## Explicit Exclusions

This proposal, and any future authorized Phase 2 built from it, does not
cover:

- selecting, naming, or evaluating any specific candidate source package,
  including DEVA 14981;
- custody, ownership, or licensing decisions for any specific artifact;
- source-specific adapters, parsers, or transcription implementation;
- literal record admission of any real observation;
- dataset cohorts, dataset splits, or validation-role assignment;
- calibration, fitting, regression, interpolation, or extrapolation;
- numerical derivation, M05 adapters, or M05 integration;
- any M06 implementation of any kind;
- any change to Phase 1's accepted API, record families, or schema ID.

## Source-Admission Requirements (Proposed)

These restate Phase 1's existing envelope and semantics as admission gates —
conditions a candidate record must satisfy before it may be admitted as a
Phase 1 record — rather than new fields. Where a genuinely new field is
proposed, it is marked **[new]** and listed again under "Decisions Requiring
Authorization."

### Provenance

A record is admissible only if it carries, explicitly and not by omission:

- exact artifact identity and source/owner/publisher identity;
- edition/date and acquisition path/date;
- ownership/license/access status, including "unknown" as an explicit tag
  rather than a blank field;
- SHA-256 when bytes are retained, or an explicit custody-limitation
  statement when they are not;
- three independent classification axes **[new: none of these are currently
  controlled fields in Phase 1's custody record]**, replacing an earlier
  single-field draft that conflated them (a single "export" or
  "transcription" label cannot say whether the artifact is a primary
  instrument export or a secondary copy of someone else's table — these are
  different questions):
  - `artifact_form` — what kind of artifact this is, independent of its
    history or role: `original_document`, `scanned_reproduction`,
    `data_export`, `photograph`, `table_excerpt`,
    `oral_or_unrecorded_statement`, or `unknown`.
  - `derivation_history` — how many removes this artifact is from the
    originating measurement or publication event: `primary_source` (the
    originating document or dataset itself — for example, an instrument's
    own data export), `secondary_transcription` (a copy or retype of another
    source — for example, a `data_export` that re-keys someone else's
    published table), `derived_export` (machine-exported from another
    retained artifact), or `unknown`.
  - `evidentiary_role` — the role this artifact plays relative to one
    specific claim it documents: `sole_known_source`,
    `corroborating_source` (with an explicit target reference to what it
    corroborates), `disputed_source` (member of an explicit conflict group),
    or `unknown`. Because one artifact can be the sole source for one printed
    statement and merely corroborate another, evidentiary role is recorded
    per source-declared load statement, not once per artifact-custody
    record.

A record with any of these fields silently absent — not tagged, simply
missing — is not admissible.

### Measurement Context

A load observation is admissible only if its configuration, instrument, and
protocol context are each either an exact reference or an explicit semantic
missing-state, per Phase 1's existing component/apparatus/measurement identity
sections: configuration (charge, powder/bullet/case/primer, cartridge/firearm/
geometry references), instrument/sensor/channel/calibration, standard/protocol
and edition, environment/conditioning, and pressure/velocity origin
classification (crusher/piezoelectric/strain/modeled/unresolved;
raw/corrected/muzzle-extrapolated). This restates Phase 1's existing
requirements as a gate; it adds no new field.

### Missing Information

Reuse Phase 1's and M02's existing semantic-missingness taxonomy. A field is
either "required-explicit" (must carry a literal value or one of the
controlled missing tags) or it is out of scope for admission at this layer.
Admission fails, rather than defaults, when a required-explicit field carries
no tag at all. This proposal does not add new missingness states; it proposes
using the existing ones as an admission precondition rather than only a
storage capability.

### Conflicts

Restates Phase 1's existing no-averaging, no-winner-selection policy as an
admission gate: a record describing a subject already covered by a
conflicting statement is admissible only as a member of an explicit conflict
group. Admission never resolves a conflict.

### Exclusion Reasons

Every excluded candidate record must cite one reason from a proposed closed
vocabulary **[new]**:

- `insufficient_provenance`
- `unresolved_measurement_method`
- `illegible_or_unresolved_transcription`
- `licensing_or_custody_restriction`
- `duplicate_of_admitted_record`
- `below_required_field_completeness`
- `unresolved_other` (requires accompanying free-text rationale)

This vocabulary is a draft starting point, not a decision. It is smaller than
the existing decision vocabulary the checkpoint proposed for the *review's*
outcome (`source_intake_authorized`, `source_intake_blocked_on_custody`,
etc.) — that vocabulary classifies a whole candidate source; this one
classifies one excluded record within an admitted or under-review source.

## Duplicate And Related-Observation Identifiability

Phase 1 already states that "duplicate publications of one underlying test
share exact lineage and a duplicate-underlying-test relationship; they do not
become independent replicates," and that uncertain common origin stays
explicit. This proposal drafts the vocabulary that statement implies but does
not itself define.

An earlier version of this draft required exactly one relationship tag per
record, including `independent_observation` for "no known relationship."
Reviewing that design against the checkpoint's named candidate example (see
the linked candidate review) found it overclaiming: two distinct records or
publications do not establish statistical independence merely because no
relationship has been noticed yet, a record can legitimately relate to more
than one other record at once (it can both duplicate one publication and
corroborate an unrelated claim in another), and an asserted relationship
without a named target is not a checkable claim. The design below replaces
the single required tag.

### Relationship Assertions

A record carries zero or more explicit relationship assertions rather than
exactly one tag. Each assertion requires **[new]**:

- a relationship type from a proposed closed vocabulary:
  `duplicate_publication_of`, `derivative_transcription_of`, `corroborates`,
  `disputes` (mirrors the existing conflict-group concept), or
  `unresolved_relationship`;
- an explicit target: the exact record ID/version this assertion is about.
  `unresolved_relationship` still requires a target when one is suspected; if
  even the target is unknown, the assertion says so explicitly rather than
  omitting the target field;
- a rationale: required free text explaining the basis for the assertion —
  this is supporting justification, not a classification value, so it does
  not weaken the closed relationship-type vocabulary;
- reviewer identity and timestamp.

A record that carries a `duplicate_publication_of` or
`derivative_transcription_of` assertion is proposed to contribute no
additional replication credit of its own beyond its target — the asserting
record (the republication or transcription) does not count as a separate,
independent replicate of the same underlying observation. This does not
exclude the target record itself, and it does not decide either record's
actual cohort or split eligibility or count; that determination belongs
entirely to a later, separately authorized cohort/split specification. This
proposal only prevents an admitted duplicate or derivative copy from
silently inflating apparent sample size — consistent with Phase 1's existing
prohibition on inflated replication. An earlier version of this sentence was
ambiguous about which record ("target" vs. asserting record) the prohibition
applied to; this is the corrected reading.

### No Default To Independence

A record with zero relationship assertions means no relationship has been
identified by a reviewer. This is explicitly **not** a claim of statistical
independence, absence of common cause, or eligibility for replicate
counting — those determinations belong to a later, separately authorized
cohort/split specification, not to this admission layer. No tag equivalent to
the removed `independent_observation` is proposed; the absence of assertions
is itself the only way to express "none identified," and it must never be
read as a stronger claim than that.

This phase, as drafted, proposes only the assertion structure and the
requirement that every relationship be manually reviewed and recorded at
admission time. It does not propose automated duplicate detection, fuzzy
matching, or any algorithm; automated detection, if ever wanted, is a
separate, later, and currently unauthorized proposal.

## Proposed Acceptance Criteria For This Phase

These are gates a *future authorized and implemented* Phase 2 admission layer
would need to pass — not gates this draft itself claims to pass. This draft
does not implement anything, so none of these are evaluated here.

1. Admission requirements reference only accepted M01/M02/Phase 1 primitives;
   no new record schema, serializer, or schema ID is introduced by
   documentation alone.
2. Every requirement traces either to an existing Phase 1 field/family or to
   an item explicitly marked **[new]** and separately authorized.
3. No specific candidate source is named, evaluated, or presupposed.
4. No cohort, split, adapter, fit, derivation, or M06 behavior is described as
   authorized by this phase.
5. Exclusion-reason, source-classification-axis, and relationship-type
   vocabularies are closed, controlled lists with an
   `unresolved_other`/`unknown`/`unresolved_relationship` catch-all that
   itself requires rationale — never free-form classification. Rationale and
   target-reference fields on a relationship assertion are required
   supporting content, not classification values, and do not reopen the
   closed type vocabulary.
6. Missing-information and conflict handling remain consistent with Phase 1's
   and M02's existing non-averaging, no-default policy; no new missingness or
   conflict semantics are introduced without explicit decision.
7. A completion review confirms no evidence, artifact, or production data was
   admitted by this phase alone, matching Phase 1's completion-review
   pattern.

## Decisions Requiring Authorization

This draft resolves none of the following. It surfaces them because Phase 2
cannot be marked `authorized` until they are. **Maintainer-stated
preference, not yet a formal decision record:** keep this rubric
documentation-only until one actual source package receives its own
source-selection and custody review, do not introduce another serializer,
and do not amend accepted Phase 1 records yet — bearing on (1), (2)/(5), and
(6) below. This narrows what a future authorization decision record would
need to formalize; it does not itself authorize anything.

1. **Sequencing** — should this admission-requirements draft be authorized
   and resolved before the checkpoint's named "Source Intake Authorization
   Review" for a specific candidate, run in parallel with it, or folded into
   it as one combined review? The checkpoint named the source-specific review
   as the next recommended unit; this draft proposes a source-agnostic
   precursor instead.
2. **Source-classification axes** — are `artifact_form`, `derivation_history`,
   and `evidentiary_role` the right three axes, and are their proposed
   value lists correct and complete? Are these new required fields on Phase
   1's custody and load-statement records (which would require a Phase 1
   amendment, since Phase 1 is `accepted`), or Phase 2-only fields on a new
   wrapper/decision record that references Phase 1 records without modifying
   them?
3. **Exclusion-reason vocabulary** — is the seven-term list above correct and
   complete, or does it need revision before being treated as controlled?
4. **Relationship-type vocabulary** — is the five-term list
   (`duplicate_publication_of`, `derivative_transcription_of`,
   `corroborates`, `disputes`, `unresolved_relationship`) correct and
   complete? Should `corroborates` and `disputes` reuse Phase 1's existing
   conflict-group mechanism instead of a relationship assertion, to avoid two
   ways of expressing the same disagreement?
5. **Where relationship assertions and evidentiary role live** — same
   question as (2): a Phase 1 amendment, or a separate Phase 2 record type
   that references Phase 1 records? Evidentiary role is proposed per
   source-declared load statement rather than per artifact — does that
   granularity match how Phase 1's records are actually structured?
6. **Serialization** — does an authorized Phase 2 need its own strict schema
   (e.g., `modern_powley.empirical_load_admission.v1`), matching Phase 1's
   pattern, or should it remain pure governance/documentation (decision
   records only, no new serializer) until a real candidate source exists to
   exercise it against?
7. **Reviewer-identity requirement** — must every relationship or exclusion
   judgment carry a named human reviewer and timestamp, as drafted, or can
   some remain provisionally `unresolved_relationship` indefinitely without a
   reviewer of record?
8. **Scope of "admission"** — does this phase gate only whether a record may
   be *constructed* (structural admission, matching Phase 1's existing
   scope), or does the maintainer want it to also gate whether an admitted
   record may later enter a cohort (which the parent workstream currently
   assigns to a separate, later cohort-definition specification)?

No implementation, schema, or authorization follows from this document. The
next step is the maintainer's review of the eight decisions above, resulting
in either an authorization decision record (mirroring
[`empirical_load_evidence_records_phase_1_authorization.md`](../decisions/empirical_load_evidence_records_phase_1_authorization.md))
or a determination that this proposal should be revised, merged into the
source-specific review, or deferred.
