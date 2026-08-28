# DEVA Protocol 14.981: Provenance Note

## Status

`documentation_only` — decision state `source_intake_not_ready`. This is a
proportionate provenance note on one report, not the checkpoint's full
"Empirical Evidence Source Intake Authorization Review," and not an
implementation of anything. It supersedes-by-extension, not by edit, the
earlier one-line-description walkthrough in
[`empirical_load_source_admission_deva14981_candidate_review.md`](empirical_load_source_admission_deva14981_candidate_review.md),
which is preserved unchanged as a record of what was knowable before any
transcription of this report existed.

**Correction (this revision):** an earlier version of this note, filed under
the name `deva_1990_protocol_provenance_note.md`, read the order reference as
"14.98 T" and the date as 1990-03-06, from the originally supplied plain-text
transcription. The maintainer subsequently reported inspecting an actual scan
of the report (available to the maintainer in conversation; not retained by
this repository) and found both wrong: the reference appears to read
**14.981** — matching the checkpoint's "DEVA 14981" label essentially
exactly, resolving what the earlier version flagged as an unconfirmed
discrepancy — and the date appears to be **February 2020**, not 1990. This
note adopts the maintainer's corrected reading; neither figure has been
independently verified by anyone else against the scan. The file was renamed
accordingly.

## What Was Supplied

Initially, a plain-text translated transcription pasted into conversation by
the maintainer. The maintainer has since indicated a scan of the report
exists and was inspected directly (see "Correction" above), but that scan
itself has not been shared into this conversation or retained by the
repository — nothing beyond the transcribed text and the maintainer's two
corrections above is available here.

Reported content: a DEVA (German Testing and Inspection Institute for
Hunting and Sporting Weapons) gas-pressure/velocity test protocol, order
reference 14.981, protocol No. 1. Reported configuration: .30-06
Springfield, PPU case, CCI 200 primer, 49.00 gr Vihtavuori N140, ~180 gr
bullet (product ID noted by the source as uncertain), 81.00 mm COAL, 600 mm
barrel, production/batch number blank (not reported by the source — this is
one test configuration and session, not confirmed to be one manufacturing
lot). **Seven individual shot observations** (velocity + gas pressure) are
reported, plus source-reported mean, standard deviation, and CIP-style
upper-confidence-limit statistics computed across those seven. No
pressure-time trace, case capacity, chamber/freebore geometry, or test
temperature is included.

The client named on the protocol is a private individual, redacted
throughout this note (shown as **[client — redacted]**) because they are not
DEVA or a business, this repository's remote is public, and no publication
permission has been established. This redaction is the reviewer's
conservative default pending the maintainer's decision, not a resolved
question.

## Provenance And Completeness

- **Artifact:** no bytes are retained by this repository — only a rendered
  translation exists in this conversation, plus the maintainer's unverified
  (by this repository) report of two corrected fields from a scan the
  maintainer has but has not shared or retained here. No hash, scan file, or
  original-language document is held.
- **Classification (Phase 2 draft's three axes):** `artifact_form` = table
  transcription (of the text; the scan itself, if ever supplied, would be a
  different artifact form); `derivation_history` = `secondary_transcription`
  for the text (translated/re-keyed, not an instrument export or retained
  original) — the scan's own derivation history is unknown, since it has not
  been examined by this repository; `evidentiary_role` = not assignable
  without the retained original.
- **Custody/licensing:** unestablished — no statement of ownership,
  redistribution rights, or DEVA/client permission accompanies either the
  transcription or the scan.
- **Measurement semantics:** pressure is piezoelectric (Kistler transducer
  type 6215, charge amplifier TR 2519), source-declared, not modeled;
  velocity is instrumental (light screens, 1.0 m base), correction/
  muzzle-extrapolation status not stated. Both are reported per-shot (all
  seven) and as an aggregate.
- **Source vs. added interpretation:** the metric measurements and CIP-style
  statistics are source-declared; the ft/s and psi conversions and the
  "below the acceptance limit" reading in the originally supplied text are
  the transcriber's own gloss, not DEVA wording, and must not be conflated
  with the source values if this is ever cited.

## Decision

`source_intake_not_ready` — no retained artifact/hash, no established
custody or licensing, an unresolved privacy question, and unverified
corrected identity/date fields pending independent confirmation. This blocks
admission as a Phase 1 evidence record; it does not block anything else. Per
the maintainer's direction, this report — one test configuration with seven
individual shot observations — is **supporting evidence with explicitly
limited applicability**, not a blocker to M06 or any other design work. It
is real, measured data, not a fixture, and must never be described as
synthetic or synthetic-adjacent regardless of how limited its use; if ever
referenced by M06 or elsewhere, it is one real anchor comparison, never
validation.

## Not Authorized Here

No Phase 1 record, hash, or ledger entry is created from this transcription
or the reported scan. No custody, licensing, or redaction decision is
resolved — those remain the maintainer's to make if this report is ever
pursued further.
