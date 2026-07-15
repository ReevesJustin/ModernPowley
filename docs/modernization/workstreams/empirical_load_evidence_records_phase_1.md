# Empirical Load Evidence Records Phase 1

## Status

`authorized`

This is a bounded implementation authorization for immutable evidence records,
strict serialization, and conspicuously synthetic structural fixtures only. The
parent empirical-load evidence and validation workstream remains `planned`.
Phase 1 is not implemented or accepted by this authorization review.
Nothing in this specification authorizes scientific source intake, a production
dataset, an M05 adapter or derivation, dataset cohorts or splits, or M06.

## Purpose

Authorize the smallest evidence-preserving record contract needed to retain what
a source, test configuration, instrument, or shot explicitly reports. Phase 1
separates custody, literal statements, normalized configurations, observations,
series, trace metadata, chronograph series, and aggregates without assigning
scientific validity or computational meaning to them.

The canonical identifier is `empirical_load_evidence_records_phase_1`. It is a
cross-cutting workstream phase rather than a numbered scientific milestone:
these records may later support M02 evidence intake, M05 adapters, and M09
validation infrastructure, but they are not M06 and do not authorize any of
those later operations.

## Authority And Relationship To Other Documents

This specification is the scope authority for a later Phase 1 implementation.
The parent
[`empirical_load_evidence_and_validation.md`](empirical_load_evidence_and_validation.md)
remains the planned cross-cutting policy. The accepted M01-M05 specifications
and APIs remain unchanged.

The binding authorization decisions are in
[`empirical_load_evidence_records_phase_1_authorization.md`](../decisions/empirical_load_evidence_records_phase_1_authorization.md).
The authorization evidence is in
[`empirical_load_evidence_records_phase_1_authorization_review.md`](../reviews/empirical_load_evidence_records_phase_1_authorization_review.md).
That review is not an implementation completion review.

## Authorized Scope

A later, separate implementation task may add only:

1. immutable source-artifact and custody metadata records;
2. literal source-declared load-statement records;
3. normalized physical load-configuration records;
4. individual shot-observation records;
5. ordered load-series or ladder records;
6. pressure-trace metadata and immutable artifact references, without samples;
7. chronograph-series records;
8. published or externally supplied aggregate records;
9. exact component, apparatus, instrument, environmental, provenance,
   missingness, conflict, exclusion, and lineage structures needed by those
   records;
10. strict, versioned serialization and deserialization;
11. conspicuously synthetic structural fixtures; and
12. unit, validation, architecture, provenance, serialization, and governance
    tests for the authorized structures.

No authorized record constructor calculates a scientific result. An aggregate
record stores a literal source aggregate or an externally supplied calculated
aggregate with exact member and method references; Phase 1 does not calculate
the aggregate.

## Explicitly Deferred And Prohibited

Phase 1 does not authorize:

- dataset cohorts, dataset splits, cohort selection, role assignment, training,
  calibration, validation, holdout assignment, or nested-validation mechanics;
- scientific source download, retention, transcription, intake, production
  datasets, or published-data parsers/importers;
- pressure-trace sample arrays, signal filtering, baseline correction,
  resampling, feature extraction, peak detection, or pressure interpretation;
- M05 source adapters, measurement-supported point/interval adapters,
  charge-region construction or derivation, interval arithmetic/intersection,
  geometry-to-charge or fill-to-charge conversion;
- empirical fits, regressions, interpolation, extrapolation, uncertainty
  propagation, model variants, or source reconciliation;
- discovery, catalogs, queries, automatic record selection, alias inference,
  preference, averaging, ranking, screening, optimization, or recommendations;
- pressure, velocity, burn, burnout, muzzle-pressure, suitability, or safety
  prediction;
- production powders, components, load records, traces, chronograph records, or
  fixtures derived from existing repository artifacts;
- a database, dataframe layer, new dependency, plot, notebook, parser, web/API
  service, user interface, M06 implementation, or broader workstream
  authorization.

The future eight-role validation vocabulary remains planning policy only. No
cohort or split record is part of Phase 1.

## Common Record Envelope

Every top-level Phase 1 record must preserve these independent concepts:

- the schema family and exact schema version;
- an exact record-type discriminator;
- stable `record_id` and positive integer `record_version` (booleans rejected);
- activation/lifecycle state independent of evidence class and maturity;
- evidence class and model maturity where applicable, without ranking;
- creation context and explicit review context;
- exact parent, source, and custody references;
- ordered immutable lineage references with declared roles;
- supersession as an optional exact record-ID/version reference, independent of
  activation;
- conflict-group references where applicable;
- an explicit `synthetic_fixture` marker that cannot confer evidence authority.

Activation, maturity, evidence class, review state, synthetic status, and
supersession must never be collapsed or inferred from one another. A record
cannot supersede its own exact identity/version. Exact reference roles are
controlled; references are stored, not discovered, loaded, resolved, or
verified by the record layer.

## Authorized Record Families

### Source Artifact And Custody Metadata

Identifies one retained or externally referenced artifact and its custody facts:
artifact identity, source identity, edition/date, locator, media type, SHA-256
when bytes are retained, ownership/license/access status, acquisition and
custody context, and immutable predecessor/derivative references. It is not a
scientific observation, transcription, load configuration, or assertion that
the source is accurate. Phase 1 stores metadata only and ingests no artifact.

### Literal Source-Declared Load Statement

Preserves exact source wording and supplied values for a single printed or
explicitly supplied statement, including literal terms such as `starting` or
`maximum`, exact edition/table/page/row, source precision, component/apparatus
context, and references to any reported pressure or velocity. It is not a
ModernPowley recommendation, safe limit, normalized physical observation,
tested continuous interval, or M05 charge region.

### Physical Load Configuration

Identifies one assembled test configuration: exact charge quantity when
reported; powder, bullet, case, primer, cartridge, firearm, barrel, chamber, and
throat/freebore identities; dimensions; conditioning; environment; apparatus;
and source context. It is not a shot, series, result, summary, model input
approval, component interchangeability assertion, or validated load.

### Shot Observation

Identifies one acquisition event with its exact configuration reference, shot
and acquisition sequence, timestamp when known, pressure/velocity reported
values or exact missingness, trace/channel references, exclusion status and
reason, and qualifications. A shot is not a load configuration, series,
summary, trace artifact, model result, or charge region. Failed and excluded
shots remain records.

### Load Series Or Ladder

Stores caller-supplied ordered references to exact configurations and/or shots,
the source-declared ordering, changed and controlled variables, replicate
structure, stopping-rule wording, and explicit missing members. It does not
calculate order, discover members, interpolate, establish continuity, or define
a charge region.

### Pressure-Trace Metadata

References an immutable raw or processed artifact and records trace identity,
SHA-256, custody/source, exact shot, instrument/sensor/channel, sampling-rate
wording/value, time-base identity, trigger/alignment metadata, source unit,
pressure quantity, calibration, excluded windows, raw/processed state, and an
exact processing-method/version reference for processed artifacts. It contains
no trace samples and performs no signal processing or interpretation.

### Chronograph Series

Stores ordered exact shot references plus chronograph instrument/setup,
measurement distance, correction state, correction-method/version where
applicable, atmospheric-correction status, exclusions, and source context. It
does not calculate statistics, normalize velocities, or replace its shots.

### Aggregate Or Published Summary

Preserves a source-reported or externally calculated statistic, exact member or
population references where known, source-reported sample count, exclusions,
precision, uncertainty status, and calculation method/version or explicit
unknown method. It never replaces or mutates its members and never masquerades
as raw observations.

## Component And Configuration Identity

### Powder

Powder identity remains owned by M02. A Phase 1 record uses an exact M02 powder
identity reference and separately preserves the lot qualifier applicable to the
load when known. It does not embed M02 property observations, borrow a property,
resolve aliases, infer product/lot equivalence, or use a commercial display
name as the identity.

### Bullet, Case, And Primer

Until a separately governed component evidence store exists, Phase 1 may define
scoped load-context component identity assertions with a controlled component
kind and explicit manufacturer, product/designation, revision, and lot
qualifiers. Each qualifier is either a literal supplied value or semantic
missingness. The record must state its source/custody context and is not a
canonical product catalog entry. An unqualified commercial string cannot stand
alone as identity.

### Cartridge, Firearm, And Geometry

Cartridge designation and the exact loaded configuration remain separate.
Firearm/receiver, barrel, chamber, and throat/freebore identities are explicit
load-context assertions. M01 records are referenced where their semantics are
exact; nominal names do not replace measured geometry. Unknown revision, lot,
firearm, barrel, chamber, or throat information is not generic applicability or
interchangeability.

## Apparatus And Measurement Identity

Records must be capable of retaining explicit laboratory, operator, test date,
acquisition sequence, firearm/barrel configuration, instrument, sensor,
channel, calibration, standard/protocol and edition, environment, and
conditioning. Identity/version references are exact. Unknown apparatus,
calibration, condition, or edition uses semantic missingness; no default
instrument, protocol, atmosphere, or calibration is allowed.

## Reported Scientific Values

M01 `Quantity` is reused only for dimensions and units it actually supports.
Phase 1 must not modify M01 units merely to make evidence storage convenient.
For pressure, velocity, sampling-rate, time, or source-specific units that M01
does not represent, Phase 1 may define a source-preserving reported-value union:
a finite JSON number or exact textual value, explicit source unit label,
controlled quantity definition, source wording, reported precision, and
uncertainty/missingness references. It performs no conversion and exposes no
arithmetic.

Source values and normalized M01 quantities, when both exist, are separate and
connected by an exact transformation/method reference. Normalization never
overwrites the literal value and unit conversion never reconciles evidence.

Non-finite numbers are rejected. Positivity/nonnegativity is specified per
field: charge mass, distances, sampling rates, and absolute barrel dimensions
must be positive when present; signed environmental or time-offset quantities
may be negative when their controlled definition permits it; zero is a value,
not missingness.

## Pressure Semantics

Pressure evidence preserves these dimensions independently:

- quantity identity and reported-peak definition;
- measurement location;
- origin: crusher, piezoelectric transducer, strain-derived, modeled, or
  unresolved;
- exact source unit label, including CUP or source-specific labels;
- PSI, bar, and MPa only as unit labels unless a separately authorized quantity
  conversion exists;
- standard/protocol and edition;
- instrument, sensor, channel, and calibration;
- acquisition, filtering, and processing state;
- source wording, printed precision, uncertainty, conditions, and whether the
  value belongs to a shot or aggregate.

Equal units do not establish equal quantity definitions, methods, locations, or
standards. CUP-to-PSI conversion, crusher/piezo equivalence, chamber-location or
cross-standard substitution, treatment of modeled pressure as measurement, and
safety inference are prohibited.

## Velocity Semantics

Velocity evidence preserves instrument/setup, measurement distance, raw versus
corrected versus muzzle-extrapolated status, correction method/version,
atmospheric correction, barrel/firearm configuration, shot versus aggregate
identity, source wording/precision, and uncertainty. Phase 1 performs no
correction or comparison and never silently normalizes materially different
configurations.

## Trace Boundary

Trace records store metadata and immutable artifact references only. A retained
artifact reference must include artifact ID and SHA-256; an external artifact
whose bytes are not retained must state that custody limitation and may not
claim a repository-verified hash. Raw and processed artifacts are distinct
immutable identities. Processing records reference exact input artifact and
method/version. Raw bytes are never overwritten.

Phase 1 prohibits embedded production arrays, filtering, baseline correction,
resampling, feature extraction, peak detection, and pressure interpretation.
Synthetic tests may exercise metadata and hash validation but not scientific
sample arrays.

## Missingness, Conflict, Exclusion, And Duplication

Reuse M02 `MissingState` and compatible tagged structures where semantics are
exact. New load-specific states require a documented implementation decision
and controlled tests; convenience is not sufficient. At minimum, absent,
unknown, not reported/not supplied, not applicable, illegible, withheld,
unresolved, unsupported, and not measured remain distinct through explicit
tagged values. Omitted keys, `null`, empty strings, zero, or NaN cannot erase
scientific missingness.

Conflict groups retain all exact member references, conflict subject, source
context, and unresolved status. They do not average, rank, prefer newer/highest-
class evidence, or select a winner. Duplicate publications of one underlying
test share exact lineage and a duplicate-underlying-test relationship; they do
not become independent replicates. When common origin is uncertain, that
uncertainty is explicit rather than assumed either way.

Observation/exclusion status is independent of activation and missingness.
Invalid, failed, or excluded shots/samples remain serialized with an explicit
reason and responsible source/reviewer context. Exclusion does not delete or
mutate the observation.

## Precision And Uncertainty

Source wording, source-reported numeric/text value, printed digits, rounding or
precision statement, measurement uncertainty, instrument resolution, and
model-form uncertainty are distinct fields or tagged records. Printed precision
is never silently converted to a statistical tolerance or uncertainty. Unknown
uncertainty remains explicit. Phase 1 calculates or propagates no uncertainty.

## Strict Serialization Boundary

The authorized implementation must use a dedicated schema family identifier:

`modern_powley.empirical_load_evidence.v1`

It must not reuse or broaden an M01-M05 serializer. Every supported top-level
record uses the common schema ID and an exact record discriminator. Parsers and
constructors must:

- reject missing or incompatible schema versions and unknown record types;
- reject unknown fields at every nested level and reject duplicate JSON object
  keys;
- reject aliases, silently renamed fields, implicit migration, and field
  dropping;
- reject wrong JSON types, including booleans as integers, and perform no
  string/number coercion;
- reject invalid/non-finite numbers and dimensionally incompatible M01
  quantities;
- use explicit tagged unions for semantic missingness, conflicts, reported
  values, artifact state, and exclusions;
- preserve source wording, source precision, units, record order where it is
  semantic, exact references, lineage, lifecycle, inactivity, supersession,
  exclusions, and conflicts;
- perform no implicit unit conversion or scientific defaulting;
- emit deterministic JSON member ordering and stable compact/indented forms;
- provide exact record-to-dictionary and dictionary-to-record round trips.

Canonical byte serialization is not promised. JSON whitespace, Unicode escape
choices, and encoder-version behavior can differ without changing the record.
Tests require deterministic output from the repository-provided encoder for a
fixed configuration, not a cross-implementation cryptographic byte format.

No migration exists for v1. Any future migration must be an explicit,
version-to-version operation authorized separately.

## Synthetic Fixture Policy

All implementation fixtures must:

- carry `synthetic_fixture: true` and no evidence authority;
- use unmistakably fictional `SYN-ELE-*` source, cartridge, powder, component,
  laboratory, instrument, and record identities;
- avoid commercial names, recognizable combinations, realistic published load
  rows, and values presented as loading instructions;
- live only under tests or a clearly marked synthetic fixture path, never a
  production/scientific data directory or scientific ledger;
- cover all authorized families plus missing, conflict, excluded, superseded,
  duplicate-lineage, and strict round-trip/rejection cases.

Legacy CSV rows, Powley or Davis examples, manufacturer/DEVA data, GRT or
QuickLOAD files, emulator output, and regression rows are prohibited as Phase 1
fixtures.

## Namespace And Dependency Boundary

The future implementation stays in `src/modern_powley/modernized/`, preferably
as narrowly named module-qualified records and serialization modules. Phase 1
objects initially remain module-qualified and are not exported from
`modern_powley.modernized.__init__`; a later export review may widen the public
surface after accepted usage demonstrates need.

The implementation may depend on accepted M01/M02 primitives only when semantic
equivalence is exact. It may reference, but not execute or duplicate, M03/M04/
M05 records. M05 must not depend on Phase 1 during this increment. No import is
permitted from `original/`, `later/`, `experimental/`, legacy scripts, GRT,
QuickLOAD, emulator, plotting, or web code. Those namespaces must not import
Phase 1. Existing M01-M05 APIs and serializers remain unchanged.

No convenience constructor may erase missingness, provenance, identity, or
source wording. No catalog, data discovery, repository/query, ranking,
recommendation, prediction, dataframe, database, or network API is authorized.
No dependency change is authorized.

## Evidence And Safety Non-Implications

Successful construction, parsing, serialization, structural validation, or
diagnostic completeness establishes none of the following:

- source accuracy or measurement validity;
- pressure-method, location, quantity, unit, or standard equivalence;
- component, product, formulation, lot, firearm, or barrel interchangeability;
- reproducibility, adequate replication, or physical validation;
- suitability, safe pressure, a starting charge, or a maximum charge;
- continuity or validity between tested points;
- recommendation, optimality, M05 derivation readiness, or M06 readiness.

`high_performance` is prohibited as an intrinsic raw-observation or load-
configuration field. Any later classification remains an operation-relative,
versioned M04/cohort decision and is outside Phase 1.

## Required Future Implementation Deliverables

1. A Phase 1 design document and separate implementation decision record.
2. The smallest coherent immutable module set inside `modernized/`.
3. Strict `modern_powley.empirical_load_evidence.v1` serialization.
4. Tests for every family, semantic missingness, conflicts, exclusions,
   duplicate lineage, identity/versioning, exact references, strict JSON, and
   architecture boundaries.
5. Conspicuously synthetic fixtures only.
6. Data-field/source-artifact governance updates required by repository policy,
   with no scientific source or data entries.
7. Entry-point documentation that describes records only.
8. A completion review mapping every implementation gate before the Phase 1
   status may become `accepted`.

## Required Implementation Decisions

The later implementation decision record must resolve without broadening scope:

1. exact module/file map and module-qualified public names;
2. exact record discriminators and field/tag vocabularies;
3. exact common-envelope activation, review, supersession, conflict, and
   synthetic-marker types;
4. exact-reference roles and uniqueness rules;
5. M01 quantity/provenance/uncertainty reuse versus Phase 1 wrappers;
6. M02 missingness and powder-identity reuse;
7. scoped bullet/case/primer and firearm/apparatus identity structures;
8. pressure/velocity reported-value and quantity-definition vocabularies;
9. raw/processed trace artifact status and SHA-256 validation;
10. exclusion and duplicate-underlying-test relationship vocabularies;
11. aggregate source-reported versus externally calculated tags;
12. deterministic JSON formatting and duplicate-key rejection;
13. strict nullability and collection-order/uniqueness rules;
14. synthetic fixture identity/value policy in executable tests; and
15. package-root non-export enforcement.

Any inability to support a semantic distinction must yield an explicit missing,
unsupported, or unavailable representation. It must not be filled with a
default.

## Implementation Acceptance Gates

A later implementation may mark Phase 1 `accepted` only when all gates pass:

1. The authorized specification and decisions were read before source edits.
2. Parent workstream remains `planned`; M01-M05 remain accepted and unchanged.
3. Source changes remain solely within the authorized modernized Phase 1
   modules and do not broaden package-root exports.
4. All eight record families are immutable, versioned, and non-interchangeable.
5. Every record carries the complete common envelope with independent lifecycle,
   evidence, maturity, review, supersession, lineage, and synthetic semantics.
6. Powder identity references M02; component revisions/lots and unknown states
   cannot collapse into names or generic applicability.
7. Apparatus, configuration, instrument, sensor/channel, calibration, protocol,
   environment, and acquisition contexts retain exact identities or missingness.
8. Pressure identity/method/location/standard/origin remain distinct; no
   conversion, equivalence, or safety inference exists.
9. Velocity acquisition/correction/distance/configuration remains explicit; no
   correction or comparison exists.
10. Trace records contain metadata/artifact references only and preserve raw
    versus processed lineage; no samples or processing algorithms exist.
11. Shot, load, series, trace, chronograph, and aggregate types cannot substitute
    for one another; series ordering implies no continuity.
12. Missingness cannot become null/default/zero; conflicts retain all members;
    excluded records survive; duplicate publications do not inflate replicates.
13. Source precision remains separate from uncertainty; unit conversion remains
    separate from evidence reconciliation.
14. Strict schema/type/field/number/reference validation and deterministic
    repository encoder round trips pass; incompatible versions and duplicate
    JSON keys fail.
15. Inactive, superseded, excluded, conflicting, and synthetic records survive
    serialization exactly.
16. Fixtures are fictional, marked synthetic, non-actionable, and isolated from
    production/scientific data and ledgers.
17. No cohort/split, scientific intake, parser, production data, M05 adapter,
    derivation, interval operation, fit, prediction, recommendation, M06,
    plotting, web, database, dataframe, or new dependency is introduced.
18. M05 and existing M01-M05 serializers and public behavior remain unchanged.
19. Documentation, ledgers, architecture, provenance, controlled-vocabulary,
    no-public-API, and governance tests pass.
20. Full repository validation passes and a completion review maps every gate.
21. Normal commit/push succeeds; final branch is synchronized and clean; the
    historical checkpoint tag is unchanged.

## Required Validation Commands

At minimum, the implementation task must run:

```bash
uv sync --locked --offline
uv lock --check
uv run pytest -q
uv run python -m compileall -q src tests scripts
git diff --check
```

It must also run repository CSV, JSON/notebook, Markdown-link, source-hash,
artifact-inventory, controlled-vocabulary, import/circular-boundary,
architecture, milestone/workstream-governance, M01-M05 compatibility, strict
Phase 1 serialization, prohibited-API, and no-production-data checks. Dependency,
historical/later/experimental, plot, notebook, and scientific-data diffs must be
empty.

## Scope-Control Review Checklist

Before acceptance, inspect the complete diff and confirm:

- no production/scientific record, artifact, trace, charge, pressure, or
  velocity value was added;
- no legacy, Powley, Davis, manufacturer, laboratory, user, GRT, QuickLOAD,
  emulator, or regression value became a fixture;
- no cohort/split or validation assignment exists;
- no M05 adapter/derivation, interval operation, model, fit, or M06 behavior
  exists;
- no source discovery, alias resolution, preference, conflict resolution,
  averaging, query, ranking, safety, suitability, or recommendation exists;
- no pressure or velocity conversion/comparison and no trace processing exists;
- no missingness, excluded member, conflict member, or source wording can be
  silently dropped;
- no M01-M05 API/serializer or protected namespace changed;
- no dependency, plot, UI, parser, database, or dataframe layer was added; and
- parent workstream remains `planned` and Phase 1 acceptance claims records and
  serialization only.

## Completion-Report Requirements

The later report must give initial/final Git state and tag; status transition;
all files; module-qualified API; record/envelope/identity semantics; pressure,
velocity, trace, missingness, conflict, exclusion, duplicate, precision,
uncertainty, and serialization behavior; fixture policy; architecture and
prohibited behavior; every gate; every validation command/result; confirmation
of no production data/intake/cohort/split/M05 derivation/M06/dependency change;
commit/push; remaining limitations; and the exact next recommendation without
authorizing it.

## Commit And Release Expectations

Implementation must occur in a later task and commit, after an `in_progress`
transition and design/decision record. Use a bounded feature commit, push
normally, do not amend/rebase/force-push, keep the historical tag unchanged, and
mark `accepted` only after all gates and completion evidence pass.

## Known Limitations

- No scientific source, artifact, or production record is admitted.
- No complete component catalog or component evidence store exists.
- M01 does not currently represent pressure, velocity, time, or sampling-rate
  dimensions; Phase 1 preserves such source values without conversion.
- Exact controlled vocabularies and nullability are implementation decisions
  bounded by this specification.
- Source licensing/custody must be decided per future intake; this phase stores
  only the contract.
- Cohorts, splits, validation assignments, signal samples/processing, M05
  adapters/derivations, and M06 remain unavailable.

## Authorized Next-Step Boundary

The only authorized next task is a separate implementation of the immutable
Phase 1 records, strict serialization, synthetic fixtures, tests, documentation,
and completion evidence described here. It must not begin scientific intake,
cohorts, splits, M05 adapters or derivation, or M06. The parent workstream
remains `planned`; acceptance of Phase 1 will not authorize its next phase.
