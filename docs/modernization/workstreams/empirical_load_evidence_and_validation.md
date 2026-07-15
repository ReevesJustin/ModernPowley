# Empirical Load Evidence And Validation Workstream

## Status

`planned`

This repository-authored specification authorizes no source implementation,
serialization schema, scientific-data intake, model, region derivation, or M06
work for the workstream as a whole. The separately bounded
[`Empirical Load Evidence Records Phase 1`](empirical_load_evidence_records_phase_1.md)
is `authorized` for a later immutable-record and strict-serialization
implementation with synthetic fixtures only. That authorization does not change
this parent status or authorize cohorts, splits, intake, M05 methods, or M06.

## Purpose

Define the evidence identities, measurement semantics, immutable lineage, and
dataset-split rules required before empirical evidence can support an M05 method
or an M06 pressure/velocity model. The contract must preserve what a source or
instrument actually reports without turning it into loading advice.

## Relationship To Existing Milestones

- M01 owns quantities, units, geometry, capacity identities, uncertainty, and
  provenance primitives.
- M02 owns powder identity/property observations, semantic missingness,
  conflicts, and applicability domains. Load evidence references those records;
  it does not duplicate powder properties or infer cross-lot equivalence.
- M03 owns operation-relative completeness and literal domain diagnostics.
- M04 owns versioned criteria and auditable outcomes. Any later
  `high-performance` classification belongs in M04 plus a cohort selection, not
  in raw evidence.
- M05 owns accepted records and strict serialization only. Load evidence may
  eventually be referenced by M05, but it does not itself create a region.
- M09 retains formal model-validation responsibility. This workstream supplies
  the dataset, cohort, split, and measurement contracts that must exist before
  M06 begins.

The M02 powder-evidence foundation should eventually receive its own bounded
intake specification. This workstream defines only its reference boundary and
does not authorize that broader powder store.

## Scope

Plan distinct records for source statements, physical load observations, shots,
series, pressure traces, chronograph series, aggregates, cohorts, and dataset
splits. Define identities, missing/conflict states, raw/normalized/derived
layers, licensing and source custody, validation roles, and future admission
gates.

## Explicit Exclusions

No source download, transcription, ingestion, database, dataframe, production
fixture, charge-region adapter, interval construction, fit, regression,
interpolation, extrapolation, uncertainty propagation, pressure conversion,
pressure/velocity/burn prediction, suitability decision, safety conclusion,
recommendation, M06 implementation, plot, parser, or interface is authorized.
No legacy CSV, GRT file, emulator output, Davis derivative, or prototype result
is promoted by this specification.

## Evidence Classes

Future records use the existing evidence classes without quality ranking:
`manufacturer_published`, `independent_laboratory_measurement`,
`user_measurement`, `other_published_primary`, `secondary_transcription`,
`reverse_engineered`, `empirical_fit`, `calibrated_parameter`, and
`derived_quantity` where applicable. Original and later Powley-associated
evidence retains its historical classification. Artifact presence is not
admission. Manufacturer data is not automatically independent laboratory data;
simulator output is not measurement; a normalized transcription is not primary
evidence.

## Proposed Record Families

### Source-Declared Load Statement

Preserve exact source wording, edition, table/page/row, component and apparatus
context, supplied units, reported precision, and any printed single value,
lower/upper value, interval, pressure, or velocity. Terms such as `starting` and
`maximum` remain literal source terminology. They do not become a universally
suitable start, a safe maximum, a ModernPowley interval, or evidence that every
interior point was tested.

### Individual Physical Load Observation

Represent one explicit test configuration and result: charge; powder, bullet,
case, and primer product/lot identities; cartridge dimensions; firearm, barrel,
chamber, throat/freebore; environment/conditioning; instrument/calibration;
pressure quantity/standard; velocity location/method; raw observation
references; uncertainty/precision; and exclusion/qualification state. Unknown
identities remain explicit unknowns.

### Shot-Level Observation

One shot retains shot ID, series/load reference, sequence, acquisition time when
available, raw velocity, raw pressure/trace reference, instrument channel,
valid/excluded state, and exclusion reason. A shot is not a configuration,
series, summary, or fitted value. Failed and excluded shots remain retained.

### Load Series Or Ladder

Represent a versioned ordered set of exact configuration references, declared
experimental design, changed and controlled variables, replicate structure,
stopping rules, missing members, and source-defined order. It does not imply
continuity or interpolation between members and is not a charge region.

### Pressure Trace

Retain the immutable raw artifact/hash, sampling rate, time base,
trigger/alignment, sensor/channel, calibration, units, pressure quantity,
protocol/standard, conditions, and excluded samples/windows. Filtering,
baseline correction, feature extraction, and processing software/version belong
to separately versioned processed artifacts. Raw bytes are never overwritten.

### Chronograph Series

Retain individual shot observations before summaries, including instrument,
setup, measurement distance, correction state, conditions, and exclusions. A
summary references exact members and declares statistic, sample count,
exclusions, rounding, uncertainty method, and instrument/setup.

### Aggregate Or Published Summary

Represent reported means, extreme spreads, standard deviations, peak pressures,
or other aggregates separately from raw observations. Preserve statistic
identity, member/population references when available, reported sample size and
precision, calculation method, and explicit unknown-method state.

### Dataset Cohort

A cohort is an immutable versioned selection record with exact members,
inclusion/exclusion criteria and versions, purpose, timestamp/version, known
missing populations, selection bias, activation/supersession, and frozen state.
It is never an implicit query, catalog discovery, or dynamic preference rule.

### Dataset Split

A split is a versioned assignment of exact cohort members to controlled roles
for one exact model/method evaluation. Proposed canonical roles are:

- `source_example_reproduction`;
- `regression_reproduction`;
- `calibration`;
- `in_sample_evaluation`;
- `interpolation_evaluation`;
- `cross_cartridge_evaluation`;
- `held_out_validation`;
- `external_replication`.

Conflicting roles for the same evaluation fail unless a separately documented
nested-validation design supplies outer/inner split identities and prevents
information leakage.

## Identity And Versioning

Every record needs stable record ID, semantic version, activation, independent
supersession, exact source and parent references, evidence class, maturity,
creation/review context, and immutable lineage. Preserve, when known:

- powder manufacturer/product/revision/lot;
- bullet manufacturer/product/revision/lot;
- case manufacturer/product/lot;
- primer manufacturer/product/lot;
- cartridge designation and exact loaded dimensions;
- firearm, receiver, barrel, barrel length, bore/groove, chamber, and
  throat/freebore identities;
- instrument, sensor/channel, calibration, laboratory, operator, and test date;
- source edition/table/page/row and environmental/conditioning context.

Unknown is not generic, unrestricted, or interchangeable. Shared commercial
names do not establish product, formulation, or lot equivalence.

## Source Artifact And Licensing Requirements

Before production intake, retain lawful source bytes where permitted, SHA-256,
source/owner/publisher, edition/date, acquisition path/date, license or
reproduction permission, access restrictions, and exact locator. When bytes
cannot be retained, record that limitation and prohibit unsupported primary
claims. Raw imports remain immutable; corrections use a transcription/correction
ledger. A secondary transcription cannot silently replace controlling evidence.

## Measurement Semantics

### Pressure

Preserve quantity identity; measurement location; crusher/transducer/strain/
modeled origin; CUP or source unit; piezoelectric PSI; bar/MPa units;
standard/protocol and edition; instrument/sensor; calibration; filtering;
reported-peak definition; conditions; wording; and uncertainty. Unit identity
does not establish measurement-method equivalence. CUP-to-PSI conversion,
cross-standard substitution, and safety inference are prohibited.

### Velocity

Preserve instrument type, measurement distance, raw/corrected status,
muzzle-extrapolated versus directly measured identity, atmospheric correction,
barrel/configuration, shot versus aggregate status, precision, and uncertainty.
Materially different configurations are not silently compared.

### Trace And Replicate Semantics

Shot identity, replicate identity, sequence, invalid/excluded status, and reason
are first-class. A trace remains linked to its shot and acquisition channel.
Summaries never replace members; missing or excluded observations remain visible.

## Missingness And Conflict

Use M02-compatible semantic missing states for unknown lot/firearm, absent
pressure method/sample count/raw observations/calibration/conditions, illegible
or unresolved transcription, withheld data, and unsupported evidence. Rounded
source values remain reported precision, not uncertainty.

Conflicting transcriptions, editions, pressure labels, or observations coexist
in explicit conflict groups. Duplicate publication of one underlying test is
recorded as lineage, not treated as an independent replicate. No averaging,
winner selection, recency preference, or source-class preference is allowed.

## Raw, Normalized, And Derived Layers

1. Retained source artifact.
2. Literal source transcription or imported raw data.
3. Normalized observation record.
4. Derived summary.
5. Dataset cohort.
6. Dataset split.
7. Model result.
8. M05 charge-region record.

Every layer after the first references exact inputs and method/version.
Normalization preserves wording and scientific semantics. Unit conversion is a
derived transformation, not evidence reconciliation. Model output is not
measurement; an M05 record is not a recommendation.

## Calibration And Validation Semantics

- **Source-example reproduction:** correspondence with a printed example only.
- **Regression reproduction:** correspondence with existing model/emulator
  output only; not physical validation.
- **Calibration:** observations influence parameters, coefficients, thresholds,
  rules, stopping decisions, or model structure.
- **In-sample evaluation:** observations were directly or indirectly available
  during fitting or selection.
- **Interpolation evaluation:** explicitly held-out observations inside declared
  represented domains; the holdout design is recorded.
- **Cross-cartridge evaluation:** transfer across distinct cartridge/geometry
  domains, with domain identities explicit.
- **Held-out validation:** observations excluded from fitting, rule/threshold
  selection, and stopping decisions.
- **External replication:** independently collected or retained data outside the
  model-development process.

Calibration agreement, source-example reproduction, and regression reproduction
must never be labeled independent validation. Dataset membership and indirect
information leakage are disclosed.

## High-Performance Terminology

`high_performance` is prohibited as an intrinsic raw-observation field. If later
needed, it is an operation-relative M04 criterion/outcome plus exact cohort
selection. The versioned definition must state performance quantities,
thresholds, exact pressure identity/constraints, cartridge/firearm domain,
components, data quality, measurement requirements, missing/conflict policy,
selection bias, and source-declared versus ModernPowley-derived origin.

Such a classification establishes no safety, recommendation, optimality,
suitability, cross-standard compliance, cross-lot/firearm applicability, or
instruction to reproduce a charge.

## Powder Evidence Relationship

Load observations reference exact M02 powder identity and lot plus applicable
property observations. Powder identity, a property observation, a load using the
powder, a source-relative burn-rate ordinal, a bulk-density observation, and a
derived fill quantity remain distinct. No universal order, equivalence class,
property borrowing, cross-lot substitution, averaging, or preferred value is
created.

## Provenance And Hypothesis Linkage

Every derived summary, cohort, split, fit, or model result references its exact
inputs and method/version. Empirical fits and model variants additionally
reference the versioned hypothesis record required by `AGENTS.md`, including
claim, assumptions, falsification, applicable domain, calibration/held-out data,
failures, and promotion requirements.

## Proposed Serialization Boundary

No schema identifier is assigned for the parent workstream while it is
`planned`. The separately authorized Phase 1 specification assigns
`modern_powley.empirical_load_evidence.v1` only to its eight bounded record
families; it does not cover cohorts or splits. Later workstream phases must
define their own compatible boundary through explicit authorization. Each
strict versioned family requires explicit record-type tags, exact nested fields
and nullability, no unknown-field dropping, no aliases or coercion, exact
units/references, source wording/precision, missing/conflict/lifecycle states,
raw hashes, and immutable lineage. Existing M01-M05 serializers remain
unchanged.

## Future Implementation Gates

1. Canonical record identities and controlled vocabularies reviewed.
2. M01/M02 reuse demonstrated without semantic duplication.
3. Raw/source, normalized, summary, cohort, and split types remain distinct.
4. Component/lot, instrument, pressure, velocity, and trace semantics pass
   structural tests.
5. Missingness/conflicts cannot disappear through defaults or omission.
6. Split-role conflicts and leakage metadata are explicit.
7. Strict serialization is separately specified and tested.
8. No scientific source or production data is bundled with schema code.
9. Architecture, provenance, documentation, and no-recommendation tests pass.
10. A completion review accepts records only before any data intake.

## Future Data-Intake Gates

1. Source ownership, license/access, edition, bytes/hash, and locators recorded.
2. Intake specification names the permitted evidence family and exact fields.
3. Literal transcription/raw import is retained separately from normalization.
4. Component, lot, firearm, instrument, conditions, missingness, and uncertainty
   are preserved without inference.
5. Corrections and conflicts remain auditable.
6. No source terminology becomes ModernPowley advice or safety policy.
7. Cohort/split creation occurs in a separate governed step.

## Known Blockers

No production load source is currently admitted. Legacy CSVs have unresolved
origins and stale generators; GRT is modeled input; the Davis primary pages and
row-level validation population are unavailable; no authoritative pressure
crosswalk exists; and no accepted replicate, trace, cohort, or split schema
exists. Licensing and retention rules must be resolved per future source.

## Authorized Next-Step Boundary

The bounded records-and-strict-serialization Phase 1 has completed a separate
authorization review and is the only authorized implementation step. This
parent document still does not authorize implementation of its broader scope,
any data intake, cohorts, splits, M05 derivation, or M06. Acceptance of Phase 1
will not authorize another phase. A recommendation never authorizes work.
