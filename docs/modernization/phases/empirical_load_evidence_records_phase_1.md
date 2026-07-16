# Empirical Load Evidence Records Phase 1 Design

## Status

`accepted`

## Scope Boundary

Implement the eight authorized immutable record families and strict
`modern_powley.empirical_load_evidence.v1` serialization only. No scientific
intake, production data, cohort/split, adapter, calculation, model, M05
derivation, or M06 behavior is part of this design.

## Module Map

| Module | Responsibility |
|---|---|
| `modernized.empirical_load_records` | Controlled vocabularies, immutable supporting structures, eight records, and deterministic structural validation |
| `modernized.empirical_load_serialization` | Strict tagged dictionary and JSON conversion for Phase 1 records only |

The API remains module-qualified. `modernized.__init__` is unchanged. Neither
module imports `original`, `later`, `experimental`, M03, M04, or M05.

## Reused Ownership

| Primitive | Owner | Phase 1 use |
|---|---|---|
| `Quantity`, `Dimension`, `Unit` | M01 | mass, length, temperature, and other already-supported dimensional values only |
| `Uncertainty` | M01 | scalar uncertainty attached to an M01 quantity only |
| `EvidenceClass`, `ModelMaturity` | M01 | independent envelope classification without ranking |
| `MissingState`, `IdentityQualifier` | M02 | semantic missingness and present-or-missing text identities |
| `SourceLocator` | M02 | exact source and transcription locator |
| `PowderIdentity` schema identity | M02 | exact powder-record reference; no embedded powder properties |

Pressure, velocity, time, and sampling-rate values do not extend M01. They use
an exact decimal-text record, controlled quantity/unit semantics, source
wording, printed precision, and a non-computational uncertainty declaration.

## Common Envelope

Every top-level record composes `RecordEnvelope`: record type; ID/version;
activation; evidence; maturity; creation/review context; source and parent
references; ordered lineage; conflict groups; exact supersession; and synthetic
marker. Activation, review, evidence, maturity, supersession, exclusion, and
synthetic status are independent. Exact references use a documented restricted
ASCII grammar and positive integer versions.

## Record Field Map

| Record | Required semantic content | Conditional content |
|---|---|---|
| source custody | source title, locator, custody statement, artifact references | retained artifact requires SHA-256; external artifact requires explicit missing hash |
| literal statement | exact wording, source reference/locator, component wording, declared values, precision/qualifications | ambiguity is explicit present text or M02 missingness |
| load configuration | cartridge identity, M02 powder reference, scoped bullet/case/primer, charge, equipment/configuration, conditions | normalized charge is M01 mass or semantic missingness |
| shot | exact configuration reference, sequence, apparatus, conditions, pressure/velocity values, trace references, exclusion | excluded/invalid requires reason and authority |
| series/ladder | strictly ordered positioned member references, purpose, declared variables/stopping rule | missing members are explicit missing assertions |
| pressure trace | artifact, shot, apparatus/channel, sampling/time/trigger, pressure context, trace state | externally processed/derived states require method/version; raw forbids it |
| chronograph series | ordered shot references, setup, distance, correction state, environment, uncertainty | corrected/extrapolated states require external method/version |
| aggregate | statistic, calculation origin, value, membership, exclusions, wording/precision | external calculation requires method/version; unknown membership requires semantic missingness |

`None` is permitted only for structurally inapplicable alternatives: no
superseded predecessor; no external method for a raw artifact; and inactive
tagged-union arms. Required scientific facts use a present-or-missing tagged
record, never `None`.

## Controlled Semantics

Pressure keeps quantity, origin/method, location, acquisition state, unit label,
standard/edition, instrument/sensor/calibration, peak definition, context,
precision, and uncertainty separate. Modeled origin requires modeled
acquisition; no conversion or equivalence API exists.

Velocity keeps individual/aggregate quantity identity, acquisition distance,
raw/corrected/muzzle-extrapolated state, external correction method, atmosphere,
instrument/setup, firearm/barrel, unit, precision, and uncertainty separate.

Trace states are `raw`, `processed_externally`,
`derivative_transcription_or_export`, and `unresolved`. No sample field exists.

## Immutability And Ordering

All records use frozen slotted dataclasses and tuples. Constructors defensively
convert accepted sequences to tuples. Ordered members must be in strictly
ascending caller-supplied positions with unique references. Conflict members
are ordered, exact, and unique; no resolution is produced.

## Serialization

The serializer uses exact field sets at every level, explicit tagged unions,
strict JSON types, duplicate-key rejection, `allow_nan=False`, and sorted keys.
Exact decimal text is serialized as a string by definition and validated as a
finite decimal lexical form; it is never coerced from a JSON number. M01
quantities retain their supplied unit. No aliases, migration, defaults, or
cross-schema dispatch exist. Determinism is repository-encoder determinism, not
general canonical JSON bytes.

## Synthetic Fixtures And Tests

Fixtures live only within the test tree; the shared builders are in
`tests/unit/test_empirical_load_evidence_records.py`. They use `SYN-ELE-*`
identifiers, fictional organizations/components/apparatus, explicit
`synthetic_fixture=True`, and non-actionable structural values. Tests cover all records, immutability,
conditionals, pressure/velocity separation, missingness, conflicts, exclusions,
duplicate lineage, trace metadata, strict round trips/failures, no root exports,
dependency boundaries, and absence of prohibited APIs/data.

## Explicit Non-Implications

Structural success does not establish source accuracy, measurement validity,
pressure equivalence, component interchangeability, replication, safety,
suitability, recommendation, M05 derivation readiness, or M06 readiness.
