# ModernPowley Roadmap

This roadmap follows the completed provenance audit. Correct attribution and
explicit failure take priority over producing a numerical result.

## Current Status

- `scalar_arithmetic_core`: source-backed, tested, isolated, and reproducible
  relative to retained original-Powley evidence.
- `complete_historical_method`: `not_ready_to_freeze` because required physical
  graphical scales and reading procedures are unavailable.
- `select_powder`, `estimate_velocity`, and `estimate_pressure` must continue to
  raise `MissingProvenanceError` until the required primary evidence passes an
  implementation-readiness audit.

This is a provenance-completeness determination, not a judgment of predictive
accuracy and not a loading recommendation.

## Phase 0: Completed Audit And Sanitation

- Preserve the pre-audit prototype at `pre_audit_agent_derived_prototype`.
- Standardize the environment on `uv` and add repository agent guidance.
- Inventory files, equations, constants, fields, generated artifacts, and
  source hashes.
- Separate `original/`, `later/`, and `experimental/` namespaces.
- Reconstruct and test the source-backed original scalar arithmetic core.
- Audit the original manual, physical-computer photographs, archived emulator,
  and retained Davis derivatives.
- Quarantine unsupported `Ba_target`, `Ba_eff`, charge regression, GRT-derived
  mappings, selectors, plots, and prototype outputs.
- Sanitize current public notebook and repository-local artifacts.

## Phase 1: Blocked Original-Powley Reconstruction

The following are historical requirements, not active implementation tasks:

- Arrow 2 powder selection is blocked by missing scale geometry, powder
  boundaries, dividing lines, tie behavior, and revision identity.
- Original velocity is blocked by the missing Expansion Ratio-Velocity surface,
  numerical domain, interpolation, edge behavior, precision, and rounding rules.
- The 1961 muzzle-pressure operation is blocked by its missing surface and
  reading rules.
- The separate Powley psi Calculator remains a later unresolved artifact and
  must not be merged with the numbered 1961 manual.

No formula, table, fit, or fallback may be added to close these gaps without new
retained primary evidence.

## Phase 2: Evidence Acquisition

Follow
`docs/provenance/original_powley_evidence_acquisition.md` for capture, intake,
authentication, digitization, uncertainty, reconciliation, and authorization
gates. Priority artifacts are:

1. A relevant 1961 Powley Computer with complete, flat captures of both faces
   and every movable element.
2. Complete Arrow 2 and reverse Expansion Ratio-Velocity markings.
3. Any 1961 muzzle-pressure face, table, worksheet, or companion instructions.
4. Original instructions and tables for the separate later Powley psi
   Calculator.

Possessing a photograph does not by itself authorize implementation.

## Phase 3: Later-Method Maintenance

- Keep Davis equations and Table 4 under `later/davis.py`; retain current
  derivative confidence and primary-image verification gaps.
- Keep archived-emulator behavior under `later/emulator.py` as a secondary
  implementation witness.
- Keep Howell and Miller unavailable until their cited publications are
  retained, classified, transcribed, and independently audited.
- Correct cross-references when evidence changes, without promoting any later
  method into `original/`.

Later methods may be maintained or versioned on their own evidence. They cannot
complete an original-Powley source gap.

## Phase 4: Quarantined Experimental Or Modern Work

Only a separately authorized experimental phase may consider:

- sourced or measured powder bulk density;
- newer single-base relative-quickness hypotheses;
- a separately identified double-base empirical branch;
- regression research, plotting, ranking, packaging, or interfaces.

Such work must remain under `experimental/`, require explicit opt-in, preserve
units and provenance, and avoid powder or charge recommendations. Legacy charge
prediction, `Ba_eff` ranking, GRT-parameter harvesting, selectors, spreadsheets,
notebooks, Streamlit/Gradio concepts, and plots remain quarantined audit history,
not current deliverables.

## Prohibited Until New Evidence Is Retained

- Filling Arrow 2 boundaries from Davis, the emulator, burn-rate charts, or
  expected powder choices.
- Reconstructing the velocity surface from the seven retained observations.
- Substituting Davis or emulator pressure arithmetic for either Powley pressure
  artifact.
- Treating gross case capacity or a generic seating-intrusion estimate as the
  original measured powder-space input.
- Fitting, smoothing, calibrating, or extrapolating missing historical values.
- Building a load selector, charge predictor, recommended-powder workflow, or
  user interface around unresolved or experimental behavior.
- Declaring the complete historical method frozen before the evidence and
  implementation acceptance gates pass.
