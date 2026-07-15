# Modernized Powley Charter

## Status And Authority

This charter authorizes `modernized_powley: authorized_for_development` as a
separate engineering research program. It does not change these historical
statuses:

- `scalar_arithmetic_core: verified_reference`;
- `complete_historical_method: evidence_limited`.

The modernized program must remain provenance-separated from the evidence-only
historical namespace. Its authorization permits staged research; it does not
validate any existing prototype equation, ranking, or output.
All modernized numerical behavior must be implemented outside `original/`.

## Purpose

The intended system is a transparent engineering selection and rejection
framework inspired by the compact sequence of Powley's workflow. Its initial
question is whether a cartridge, projectile, propellant, and bounded charge
region merits further analysis or should be rejected with an explicit reason.

The modernized system is not:

- a reconstruction of unavailable physical scales;
- a claim of historical identity;
- a replacement for published loading data;
- initially a high-fidelity internal-ballistics solver;
- initially a user-facing load recommendation system.

Historical incompleteness does not block modernized development, and modernized
behavior cannot close a historical provenance gap.

## Primary Engineering Objectives

The program may eventually screen candidates in this priority order:

1. safe pressure margin;
2. approximately 95 to 100 percent useful case fill where practical;
3. complete burn before the muzzle;
4. preferred burnout at approximately 50 to 75 percent of projectile travel;
5. minimized muzzle pressure as a secondary discriminator;
6. temperature and uncertainty headroom;
7. transparent reasons for acceptance, rejection, and ranking.

These are user-defined modernization objectives. They are not attributed to
Homer Powley. Each objective remains inactive until its inputs, model, domain,
uncertainty, and validation gates are satisfied. In particular, complete burn
and burnout location require explicit burn fraction, time, and travel outputs;
muzzle pressure is not a substitute.

## Initial Product Boundary

The first promoted releases should be an analytical library and an auditable
command-line or test workflow. A spreadsheet, notebook, Streamlit application,
Gradio application, graphical selector, or public recommendation interface is
deferred until all numerical layers it exposes have passed promotion gates.

M01 is the next authorized implementation phase. It defines inputs, units,
provenance, and geometry only. It does not authorize ballistics prediction or a
new numerical package namespace by this documentation commit.

## Modeling Principles

Every modernized numerical method must provide:

- explicit units at every input, output, storage, and parser boundary;
- dimensional auditing of equations and dimensioned constants;
- source attribution for every equation, constant, table, and parameter;
- separation of measured, published, transcribed, inferred, fitted,
  calibrated, and assumed values;
- deterministic reproduction from versioned inputs and code;
- no hidden calibration or undisclosed parameter overrides;
- a stated mathematical and physical domain;
- bounded interpolation with a documented algorithm;
- an explicit extrapolation policy, with rejection as the default;
- uncertainty and applicability reporting;
- explicit failure outside supported domains;
- preservation and testing of known failures;
- no silent fallback between historical, later, empirical, simulator-derived,
  or other model families;
- no single unexplained aggregate ranking score.

Similar numerical output does not establish shared provenance. A model that
matches an example or another program remains classified by its own evidence.

## Physical Quantity Distinctions

The data model and APIs must keep these quantities distinct:

- gross case water capacity;
- measured seating-specific usable powder-space water capacity;
- geometrically estimated usable powder space;
- primer-pocket volume;
- powder bulk volume;
- solid propellant volume;
- initial free gas volume;
- chamber pressure;
- projectile-base or breech pressure;
- mean bore pressure;
- peak pressure;
- muzzle pressure;
- projectile velocity;
- gas velocity;
- burn fraction;
- burnout time;
- burnout travel.

No shared label such as `case_volume`, `pressure`, or `burnout` may collapse
these distinctions at an API or storage boundary.

## Architecture Boundary

- `original/` is an evidence-limited historical reconstruction under the
  evidence-only maintenance policy.
- `later/` contains Davis, Howell, Miller, emulator, and other separately
  attributed later methods.
- `experimental/` contains unvalidated hypotheses, fits, calibrations, and
  reverse-engineered candidates with explicit opt-in.
- A future modernized namespace may contain only behavior admitted through the
  phase and promotion gates. It is not created by this documentation pass.

No current prototype output or implementation is automatically promoted. A
candidate may be rejected even when it is reproducible.

## Evidence Policy

Every implementation must declare an evidence class from
`evidence_and_model_classes.md`, a model maturity class, source identity,
confidence or uncertainty status, and whether it may participate in screening,
rejection, ranking, calibration, or evaluation.

Calibration inputs and evaluation inputs must be disjoint or their overlap must
be disclosed. Simulator outputs are modeled results, not measurements.
Manufacturer-published values remain manufacturer-published. Missing values may
not be mean-imputed, borrowed from another propellant, or silently defaulted.

## Validation Philosophy

Promotion requires validation appropriate to the method, including:

- equation-level tests against independent calculations;
- dimensional and unit-conversion tests;
- reconciliation with published source examples;
- synthetic invariant and limiting-case tests;
- measured-load validation where the output claims physical prediction;
- holdout evaluation for fitted or calibrated parameters;
- explicit pressure, velocity, burn-location, and muzzle-pressure error metrics
  when those outputs are implemented;
- disclosure when tuning and evaluation use the same cases;
- retained fixtures for known failures and outside-domain cases.

Passing software tests establishes implementation consistency, not physical
validity. Promotion decisions must state which claim the evidence supports.

## Safety Boundary

ModernPowley is an analytical research framework. Outputs are not loading
instructions. Published load data and applicable pressure standards remain
authoritative. Unsupported inputs must fail or be marked outside-domain.
Uncertainty must not be hidden behind a ranking score, and the framework must
not convert an experimental estimate into a recommended charge.

## Governance

Each phase requires a bounded task, reviewable artifacts, tests, and a recorded
decision to continue, revise, stop, reject, or promote. Negative findings are
valid phase outcomes. Changes to historical behavior follow the separate
evidence-only policy and are never bundled with modernization promotion.
