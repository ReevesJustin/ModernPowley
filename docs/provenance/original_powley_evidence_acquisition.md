# Original Powley Evidence Acquisition Specification

## Purpose And Boundary

This document specifies evidence needed to reconsider the unavailable original
Powley operations. It is acquisition guidance, not a historical Powley rule.
Possession of a photograph or transcription does not authorize implementation.

Current status remains:

- `scalar_arithmetic_core`: source-backed, tested, isolated, and reproducible
  relative to retained evidence.
- `complete_historical_method`: `not_ready_to_freeze`.

`select_powder`, `estimate_velocity`, and `estimate_pressure` must continue to
raise `MissingProvenanceError` until the applicable gates below pass.

## Required Physical Artifacts

Acquire or locate, where possible:

1. The relevant 1961 Powley Computer revision, with revision markings and
   provenance sufficient to distinguish it from later devices.
2. Flat images of both faces of the computer.
3. Every slider, cursor, arrow, movable strip, window, index mark, and overlay,
   including markings normally hidden during one alignment.
4. The complete Arrow 2 powder-selection face.
5. The complete reverse Expansion Ratio-Velocity face.
6. Any 1961 muzzle-pressure face, table, worksheet, instruction, or companion
   material referenced by the numbered manual.
7. Instructions, tables, and all faces for the separate Powley psi Calculator.
   Treat that calculator as a later artifact unless retained evidence establishes
   a different date and relationship.

Contemporary advertisements, correspondence, replacement instructions, and
dated revision sheets are useful when they identify which markings belong to
the 1961, 1965, 1985, or another revision.

## Imaging Requirements

These are capture recommendations, not claims about historical operation:

- Position the camera perpendicular to each surface and minimize perspective
  distortion.
- Use even, diffuse lighting that avoids glare, shadow, and washed-out ticks.
- Include a ruler or dimensional scale in the plane of the artifact.
- Include a color reference when available.
- Capture enough resolution to distinguish the smallest visible ticks, line
  intersections, labels, and cursor edges.
- Preserve lossless or minimally compressed originals before cropping,
  rectification, contrast adjustment, or annotation.
- Capture separate full-face overviews and overlapping detail images.
- Photograph multiple slider and cursor settings so no fixed or movable marking
  remains occluded.
- Capture front, reverse, edges, revision marks, and detached movable elements.
- Preserve camera metadata, original filenames, timestamps, orientation, and
  any available capture notes.
- Never replace the original capture with a destructively enhanced derivative.
  Store derived crops or rectifications separately with transformation records.

No mandatory DPI or numeric uncertainty threshold is asserted. Suitability
depends on whether the smallest relevant feature and its relationship to other
features can be independently resolved.

## Required Reconstruction Information

### Arrow 2

Evidence must establish:

- direction of every scale;
- sectional-density axis and complete graduations;
- charge-to-bullet-ratio axis and complete graduations;
- powder and letter label positions;
- boundary geometry and dividing lines;
- Arrow 2 index geometry and reading direction;
- tie and exact-boundary behavior;
- off-scale A/G and lettered F/D/B procedures;
- behavior when more than one powder position is plausible;
- relationship between the relevant 1961 scale and later revisions.

Worked examples alone cannot determine the full boundary surface.

### Expansion Ratio-Velocity

Evidence must establish:

- both axes and their units;
- every curve, grid line, cell, label, and numerical tick;
- the complete numerical domain;
- whether scales are linear, logarithmic, reciprocal, segmented, or another
  explicitly evidenced form;
- interpolation behavior within the domain;
- edge, exact-node, and off-scale behavior;
- printed or reasonably readable precision;
- rounding and reporting behavior;
- any dependence on powder selection or another prior reading.

The seven retained velocity observations are constraints, not a recoverable
surface and not permission to fit one.

### Pressure

For each pressure artifact, evidence must separately establish:

- exact artifact title, date, revision, and relationship to other devices;
- whether the represented quantity is muzzle, chamber, peak, average, breech,
  crusher-gage, or another pressure;
- printed units and measurement convention;
- every input and its unit;
- the complete scale, table, worksheet, or surface;
- interpolation, exact-boundary, edge, and off-scale behavior;
- rounding and readable precision;
- relationship to the numbered 1961 manual;
- relationship, if any, to the separate later Powley psi Calculator.

Do not convert historical crusher terminology to modern piezoelectric PSI
without an explicit, authoritative source.

## Intake And Provenance Procedure

For every newly acquired artifact:

1. Preserve the original bytes without normalization or enhancement.
2. Record source, owner or custodian, acquisition date, revision identity,
   chain of custody where known, and reproduction permission.
3. Calculate and record SHA-256 for the original bytes.
4. Add the artifact beneath `reference/` in a descriptive source directory;
   keep temporary working renders out of the evidence path.
5. Add or update `reference/source_ledger.csv` with access, classification,
   location, hash, claims, confidence, and limitations.
6. Create a page/image map covering every face, view, movable element, crop,
   occlusion, and unreadable region.
7. Preserve raw OCR or manual transcription separately from normalized
   transcription and correction records.
8. Quantify visual uncertainty where the image supports it; otherwise state why
   uncertainty cannot be bounded.
9. Reconcile the new evidence against every retained worked example and record
   agreements, contradictions, and revision differences.
10. Update equation, constant, field, and source ledgers before implementation.
11. Perform an explicit implementation-readiness audit before changing
    `src/modern_powley/original/`.
12. Preserve contradictions and literal readings; never silently normalize a
    disputed label, boundary, constant, or unit.

Derived images or digitized data require a manifest identifying source and
generated hashes, transformation commands, tool/environment, repository commit,
timestamp, output status, and uncertainty notes.

## Acceptance Gates

Each gate is independent. Passing an earlier gate does not imply a later one.

### Gate 1: Evidence Retained

- Original bytes are committed under `reference/`.
- SHA-256 and acquisition metadata are recorded.
- Reproduction permission and access limitations are explicit.

### Gate 2: Evidence Authenticated And Classified

- Artifact identity, date/revision, source type, and primary/secondary status
  are supported or explicitly unresolved.
- Relationship to the 1961 computer and later devices is recorded.

### Gate 3: Scale Digitized

- All required fixed and movable geometry is visible.
- Raw coordinates or cells, coordinate system, transformations, source hashes,
  and uncertainty are retained.
- Digitization does not repair or invent missing regions.

### Gate 4: Reconstruction Independently Checked

- A second review can reproduce the transcription or digitization from retained
  evidence.
- Disagreements and unreadable features remain recorded.

### Gate 5: Interpolation Rules Established

- Primary evidence or defensible verified geometry establishes exact-node,
  interior, boundary, tie, rounding, and off-scale behavior.
- Extrapolation remains prohibited unless explicitly sourced.

### Gate 6: Worked Examples Reconciled

- Every applicable primary example is independently recalculated or reread.
- Source, independent, and candidate implementation results are compared with
  precision and uncertainty appropriate to the artifact.

### Gate 7: Implementation Authorized

- Source, equation, constant, field, and artifact ledgers are current.
- An implementation-readiness audit identifies the complete supported domain.
- Tests exist for source points, boundaries, invalid inputs, missing evidence,
  architecture separation, and artifact hashes.
- Review explicitly authorizes a bounded change to `original/`.

### Gate 8: Historical Baseline Freeze Reconsidered

- Powder selection and velocity are complete across the evidenced domain.
- Pressure is assessed separately for the 1961 muzzle-pressure operation and
  the later psi Calculator.
- Remaining ambiguities are documented and do not require inferred scientific
  behavior.
- A new freeze-readiness audit chooses and justifies the repository status.

A photograph, OCR transcript, secondary equation, matching example, or
emulator-compatible approximation alone cannot pass these gates.
