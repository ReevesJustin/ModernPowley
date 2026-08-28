# DEVA Test Protocol (1990-03-06): Provenance Note

## Status

`documentation_only` — decision state `source_intake_not_ready`. This is a
proportionate provenance note on one report, not the checkpoint's full
"Empirical Evidence Source Intake Authorization Review," and not an
implementation of anything. It supersedes-by-extension, not by edit, the
earlier one-line-description walkthrough in
[`empirical_load_source_admission_deva14981_candidate_review.md`](empirical_load_source_admission_deva14981_candidate_review.md),
which is preserved unchanged as a record of what was knowable before this
transcription was supplied.

## What Was Supplied

A plain-text translated transcription, pasted into conversation by the
repository's maintainer: a DEVA (German Testing and Inspection Institute for
Hunting and Sporting Weapons) gas-pressure/velocity test protocol, order
reference transcribed as "14.98 T" (plausibly the source of the checkpoint's
"DEVA 14981" label, via transcription/OCR drift — not confirmed), protocol
No. 1, dated 1990-03-06. Reported configuration: .30-06 Springfield, PPU
case, CCI 200 primer, 49.00 gr Vihtavuori N140, ~180 gr bullet (product ID
noted by the source as uncertain), 81.00 mm COAL, 600 mm barrel. Seven
individual shots (velocity + gas pressure) plus source-reported mean,
standard deviation, and CIP-style upper-confidence-limit statistics for
both. No pressure-time trace, case capacity, chamber/freebore geometry, or
test temperature is included.

The client named on the protocol is a private individual, redacted
throughout this note (shown as **[client — redacted]**) because they are not
DEVA or a business, this repository's remote is public, and no publication
permission has been established. This redaction is the reviewer's
conservative default pending the maintainer's decision, not a resolved
question.

## Provenance And Completeness

- **Artifact:** no bytes are retained — only a rendered translation exists in
  this conversation. No hash, scan, or original-language document is held by
  this repository.
- **Classification (Phase 2 draft's three axes):** `artifact_form` =
  table transcription; `derivation_history` = `secondary_transcription`
  (translated/re-keyed, not an instrument export or retained original);
  `evidentiary_role` = not assignable without the original.
- **Custody/licensing:** unestablished — no statement of ownership,
  redistribution rights, or DEVA/client permission accompanies the
  transcription.
- **Measurement semantics:** pressure is piezoelectric (Kistler transducer
  type 6215, charge amplifier TR 2519), source-declared, not modeled;
  velocity is instrumental (light screens, 1.0 m base), correction/
  muzzle-extrapolation status not stated. Both are per-shot and aggregate.
- **Source vs. added interpretation:** the metric measurements and CIP-style
  statistics are source-declared; the ft/s and psi conversions and the
  "below the acceptance limit" reading in the supplied text are the
  transcriber's own gloss, not DEVA wording, and must not be conflated with
  the source values if this is ever cited.

## Decision

`source_intake_not_ready` — no retained artifact/hash, no established
custody or licensing, an unresolved privacy question, and several
source-hedged fields (order number, bullet product). This blocks admission
as a Phase 1 evidence record; it does not block anything else. Per the
maintainer's direction, this single report is **supporting evidence with
explicitly limited applicability** — one configuration, one lot, one date —
not a blocker to M06 or any other design work. M06's draft specification
treats it as, at most, one possible future anchor test case (decision 5
there), never as validation.

## Not Authorized Here

No Phase 1 record, hash, or ledger entry is created from this transcription.
No custody, licensing, or redaction decision is resolved — those remain the
maintainer's to make if this report is ever pursued further.
