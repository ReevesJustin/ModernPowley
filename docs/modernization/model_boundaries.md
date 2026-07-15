# Modernized Model Boundaries

## Boundary Principle

The repository may preserve several methods that compute similarly named
quantities. Shared names or similar results do not make those methods identical.

> Numerical similarity, worked-example agreement, or successful regression reproduction does not establish historical provenance.

Every calculation must retain its method identity through inputs, outputs,
tests, storage, and documentation.

## Model Areas

### Recovered Original Equations

`src/modern_powley/original/` contains only retained, source-backed arithmetic
and explicit failures. It is governed by the evidence-only maintenance policy.
Its scalar core is a verified reference, not a complete executable calculator.

### Unavailable Original Operations

Arrow 2 powder selection, the Expansion Ratio-Velocity surface, and the 1961
muzzle-pressure surface remain unavailable. Their public historical functions
must raise `MissingProvenanceError`. Neither modern development nor agreement
with printed examples changes that status.

### Later Published Methods

Davis, Howell, Miller, the later Powley psi Calculator, and other later
Powley-associated material belong under `later/` when sufficiently sourced.
They retain their own authorship, date, equations, units, and domains. They may
be modernization candidates but cannot be relabeled original.

### Archived Emulator Behavior

The archived emulator is a secondary implementation witness. Exact reproduction
belongs under `later/emulator.py`; reverse engineering from it is classified
`reverse_engineered`. Emulator agreement does not verify a physical scale.

### GRT And jRT Behavior

GRT-derived fields and jRT-recovered behavior are modeled or reverse-engineered
unless an authoritative source establishes otherwise. Field names alone do not
establish semantics. Area cannot populate volume, and missing powder properties
cannot be imputed or borrowed.

### Modern Published Substitutions

Modern engineering equations may enter the modernized program when retained,
transcribed, dimensionally audited, independently implemented, and validated
for their claimed decision role. They must use a new method identity and cannot
silently replace a historical operation.

### Empirical Calibration

Fits and calibrated parameters retain dataset, split, objective, residual,
uncertainty, and version provenance. In-sample reproduction is not validation.
A calibrated value is model-specific and cannot be presented as a universal
propellant property without supporting evidence.

### Exploratory Hypotheses

Unsourced proposals remain in `experimental/` with explicit opt-in. They cannot
drive promoted screening, rejection, ranking, or public output.

### External Powder-Property Data

Future property datasets must preserve manufacturer/product/lot identity,
measurement or model origin, units, conditions, access date, missingness, and
uncertainty. Commercial relative burn-rate position is a rough ordinal field,
not a universal physical quickness parameter.

## Required Numerical Declaration

Every future numerical implementation must declare:

- method identity;
- evidence class;
- model maturity;
- source and artifact identifiers;
- input and output units;
- mathematical and physical domain;
- interpolation policy;
- extrapolation policy;
- validation status and metrics;
- uncertainty status;
- calibration/evaluation role;
- whether it may participate in screening, rejection, ranking, or reporting.

Missing declarations require explicit failure. No silent fallback may switch to
another model family.

## Promotion Workflow

1. Retain the candidate source or evidence.
2. Record source identity and hash where applicable.
3. Transcribe equations, variables, units, tables, and domains.
4. Perform a dimensional audit.
5. Implement independently in an experimental location.
6. Reconcile against source examples.
7. Test mathematical invariants and limiting cases.
8. Assess parameter sensitivity and domain edges.
9. Validate against measured cases where applicable.
10. Separate calibration cases from evaluation cases.
11. Characterize uncertainty and known failure modes.
12. Document a promotion, rejection, or revision decision.
13. Move or reimplement accepted behavior in the future modernized namespace.
14. Preserve the experimental predecessor and decision history.

Promotion is scoped to a method, version, domain, and permitted decision role.
It is not a blanket endorsement of the model family.

## Historical Evidence-Only Changes

Changes to `original/` may integrate newly retained primary evidence, correct a
demonstrated transcription or implementation error, improve provenance, add
tests/documentation, or perform non-behavioral maintenance. Modern substitutions,
later equations, inferred boundaries, fitted tables, emulator/GRT behavior, and
silent changes to units, constants, domains, or rounding remain prohibited.
