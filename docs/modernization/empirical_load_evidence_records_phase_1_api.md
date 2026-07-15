# Empirical Load Evidence Records Phase 1 API

Status: `accepted`

## Boundary

Phase 1 is a module-qualified immutable record and strict serialization contract.
It retains caller-supplied evidence without source intake, scientific
reconciliation, calculation, catalog discovery, persistence, or model behavior.
Successful construction or parsing establishes structure only, not source
accuracy, measurement validity, pressure equivalence, component
interchangeability, reproducibility, safety, suitability, recommendation, M05
derivation readiness, or M06 readiness.

## Modules And Schema

- `modern_powley.modernized.empirical_load_records` defines the records.
- `modern_powley.modernized.empirical_load_serialization` defines serialization.
- The schema ID is exactly `modern_powley.empirical_load_evidence.v1`; the
  separately emitted schema version is integer `1`.
- Phase 1 names are intentionally absent from
  `modern_powley.modernized.__init__`; callers import the two modules directly.

The serializer entry points are `empirical_load_record_to_dict`,
`empirical_load_record_from_dict`, `dumps_empirical_load_record`, and
`loads_empirical_load_record`.

## Record Families

The exact discriminators are `source_custody`, `literal_load_statement`,
`physical_load_configuration`, `shot_observation`, `load_series`,
`pressure_trace_metadata`, `chronograph_series`, and `aggregate_summary`.
Each discriminator maps to one distinct frozen, slotted dataclass. The envelope
discriminator must agree with the class.

Every record composes a `RecordEnvelope`. Activation (`active`, `inactive`),
M01 evidence class, M01 model maturity, review state, conflicts, synthetic
status, and exact supersession are independent. Exact references contain schema,
record type, ID, optional exact version, and a controlled role. IDs match
`[A-Za-z][A-Za-z0-9._:-]{0,127}`. Versions are positive integers and booleans
are rejected.

## Controlled Vocabularies

Phase 1 controls activation, review, reference role, exclusion, component and
equipment kind, source-declaration state, reported precision, evidence
uncertainty, reported-value kind, pressure quantity/origin/location/acquisition
state/unit, observation level, velocity quantity/correction state/unit, artifact
retention and trace state, and aggregate statistic/origin. Enum member values in
the source module are the wire values; unrestricted status strings are not
accepted.

The trace states are `raw`, `processed_externally`,
`derivative_transcription_or_export`, and `unresolved`. Processed and derivative
metadata require an exact external method reference. No processing occurs.

## Nullability And Missingness

Scientific missingness uses M02 `MissingState` in explicit tagged records.
`ReferenceOrMissing` and `QuantityOrMissing` require exactly one branch.
`None` is reserved for structural inapplicability explicitly encoded by the
type: optional supersession, optional exclusion source wording, optional exact
reference version where a non-versioned external identity is permitted,
conditional correction/processing methods, and mutually exclusive tagged-union
branches. Empty text, zero, non-finite numbers, and omitted fields never stand
for scientific missingness.

No Phase 1-specific missing state was added. All accepted M02 missing states
round trip without remapping.

## Identity And Lineage

Powder uses an exact `modern_powley.m02.v1` powder-identity reference plus
explicit manufacturer, designation, revision, and lot qualifiers. Phase 1 does
not duplicate powder properties. Bullet, case, and primer records are scoped
load-context assertions, not general component property records. A later
component store can be referenced by new exact lineage without changing or
overwriting the historical scoped assertion.

Firearm, barrel, chamber, throat/freebore, laboratory, operator, instrument,
sensor, channel, calibration, standard/protocol, and other apparatus identities
remain distinct equipment kinds. Duplicate publications can share one
`underlying_test` lineage reference; publication count therefore does not create
replicate identity. Conflict groups retain every exact member and contain no
preferred member. Exclusion retains state, reason, authority, review context,
source wording, and lineage; exclusion never deletes a record.

## Values, Precision, And Uncertainty

M01 `Quantity` is reused only for dimensions M01 represents exactly, such as
charge mass and distance. `PhysicalQuantityEvidence` preserves that quantity,
the literal source value text, source unit text, and explicit derivation
references. Conversion never replaces source text.

Pressure, velocity, sampling-rate, and source-specific values use
`ReportedValue`: a strictly parsed finite decimal string, controlled kind,
source unit label, exact wording, reported precision, and evidence uncertainty.
This prevents binary-float formatting from changing printed decimals. Printed
precision (`exact_as_reported`, `decimal_places`, `significant_digits`,
`rounded`, `unknown`) remains separate from M01 scalar measurement uncertainty,
model-form uncertainty, external uncertainty references, and unknown/not-
reported/not-applicable uncertainty states.

## Pressure And Velocity

Pressure preserves quantity, origin (`crusher`, `piezoelectric_transducer`,
`strain_derived`, `modeled`, `unresolved`), location, source-specific unit label,
standard, instrument, sensor, calibration, acquisition/processing state, peak
definition, observation level, wording, precision, and uncertainty. Modeled
origin requires modeled quantity and non-modeled origins reject modeled
quantity. CUP, PSI, bar, and MPa are labels within this evidence contract, not
conversion authority. No pressure conversion or safety API exists.

Velocity preserves individual versus aggregate quantity, instrument/setup,
measurement distance, raw/corrected/muzzle-extrapolated state, exact correction
method when required, atmospheric context, firearm/barrel, source unit, wording,
precision, and uncertainty. Phase 1 performs no correction, averaging, or
cross-configuration comparison.

## Trace Boundary

`PressureTraceMetadataRecord` stores an artifact ID, strict lowercase SHA-256,
custody reference, shot reference, apparatus metadata, sampling-rate evidence,
time base, trigger/alignment, pressure identity/location, calibration, external
processing reference, and excluded-window descriptions. It has no sample-array
field and performs no filesystem I/O, hashing of bytes, filtering, alignment,
resampling, correction, feature extraction, or interpretation.

## Serialization

The wire object has exactly `schema`, `schema_version`, `record_type`,
`envelope`, and `payload`. Every nested object has an exact field set. The
decoder rejects unknown/missing fields, aliases, unknown enums/discriminators,
future or legacy schemas, type coercion, booleans as integers, non-finite JSON,
invalid units, malformed tagged unions, and duplicate JSON keys. It does not
migrate or default scientific values.

Repository JSON is deterministic through sorted keys and fixed encoder options;
general RFC canonical JSON or cross-implementation byte canonicality is not
claimed. Immutable tuple order, source wording, printed decimal text, conflicts,
exclusions, inactive state, and supersession survive exact round trips.

## Synthetic Fixtures

Fixtures exist only in `tests/unit/test_empirical_load_evidence_records.py` and
dependent tests. IDs use `SYN-ELE-*`; organizations, components, cartridges,
apparatus, methods, and values are fictional and marked `synthetic_fixture=True`.
They are structural examples without evidence authority and are not load
instructions. No repository legacy row, manufacturer/laboratory/user data,
Powley or Davis example, GRT/QuickLOAD artifact, emulator output, or regression
row is used.
