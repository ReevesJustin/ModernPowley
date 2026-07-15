# Davis 1981 Evidence Intake

Date: 2026-07-14

## Scope

This pass preserves two newly supplied derivative artifacts associated with Wm.
C. Davis Jr.'s “Some Simplified Interior Ballistics for Handloaders,” printed in
the 1981 NRA book *Handloading*. It does not reconcile either derivative against
the physical book because page images 138-144 are not retained.

The artifacts are:

- [raw OCR pages 138-144](../../reference/davis_1981/davis_1981_pages_138_144_raw_ocr.txt)
- [derivative partial reprint](../../reference/davis_1981/derivative_partial_reprint.pdf)
- [intake README](../../reference/davis_1981/README.txt)
- [SHA-256 manifest](../../reference/davis_1981/SHA256SUMS.txt)

## Artifact Classification

| Source ID | Artifact | Classification | Verification status | Confidence |
|---|---|---|---|---|
| `SRC-DAVIS-1981-RAW-OCR` | raw OCR text | user-supplied secondary derivative; intentionally uncorrected | `ocr_only` | low |
| `SRC-DAVIS-1981-DERIVATIVE-REPRINT` | partial reprint PDF | later secondary Davis evidence; not an NRA facsimile | `verified_secondary` | medium |

The physical NRA publication remains the underlying later primary authority.
Neither derivative is controlling evidence for `src/modern_powley/original/`.

## Raw OCR Assessment

The OCR contains explicit markers for printed pages 138 through 144 and
corroborates the article's overall sequence: scope and warnings, capacity inputs,
direct and calculated powder-space procedures, expansion geometry, relative
quickness, powder selection, velocity, worked example, and pressure discussion.

It is deliberately preserved without correction. Examples of material damage
include lost superscripts in sectional density and boat-tail expressions,
malformed radicals in the powder-index and velocity equations, missing decimal
points, column interleaving, and severe Table 4 row/cell loss. The Table 4 OCR
does not preserve a reliable nine-column by 34-row grid. It therefore cannot
verify equation typography, constants affected by damaged glyphs, Table 3
boundary typography, or any of the 306 Table 4 values.

The raw OCR does preserve readable prose warning that relative-quickness order
is not a deterministic cartridge-performance order. In particular, it appears
to state that IMR-4064 can allow higher charge weights and velocities at an
acceptable pressure than IMR-4895 or IMR-4320 in some actual firings. This is
recorded as OCR corroboration pending visual verification, not as a newly
verified quotation.

## Derivative Partial Reprint Assessment

The PDF identifies itself as a partial explanatory reprint and is not a
facsimile of the NRA pages. It is later secondary evidence. Its `.22-250`
arithmetic contains internal discontinuities:

- loaded capacity is first calculated as `42.530520632 gr water` but later
  calculations use `42.377625032 gr water` without an explanation;
- narrative examples state `35.4 gr`, while the displayed pressure arithmetic
  uses `I=36.44475752752 gr`.

These are classified only as inconsistencies within the derivative artifact.
Without the physical NRA page images, they are not errors attributable to
Davis's primary publication.

## Existing Normalized Data

The normalized equation transcription and candidate Table 4 CSV remain
secondary derivatives. Their existing statuses are unchanged:

- equation typography: normalized user transcription, not visually verified;
- Table 4: `pending_retained_primary_visual_verification`, medium confidence;
- Table 4 interpolation along `A`: implementation interpretation;
- complete per-cell audit: not performed.

The independent `.30-06` calculation remains corroboration only. Unrounded
repository arithmetic produces approximately `2619.410 ft/s` and `45,762.315`
historical crusher-pressure units. Davis's printed rounded sequence produces
approximately `45,793.301`, consistent with the transcribed `45,790`. Agreement
does not verify damaged glyphs or the remaining Table 4 cells.

## Implementation Readiness

No scientific implementation changed. `src/modern_powley/later/davis.py` retains
its bounded medium-confidence Table 4 metadata and existing arithmetic.
`src/modern_powley/original/` is unchanged; original Arrow 2, graphical velocity,
and psi Calculator operations remain partially recovered and continue to fail
explicitly where provenance is missing.

Primary visual reconciliation remains blocked until legible retained images or a
facsimile of NRA *Handloading* pages 138-144 are available. Those images must
show page edges, equation typography, table headings, footnotes, and every Table
4 cell.
