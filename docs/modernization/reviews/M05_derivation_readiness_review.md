# M05 Derivation Readiness Review

Status: `planning_review`

## Decision

No M05 derivation family is admitted or authorized. The accepted M05 contract
continues to store caller-supplied records only. Empirical-load evidence records,
source intake, validation cohorts/splits, and method-specific authorization must
precede production derivation.

## Evidence Reviewed

| Evidence/model family | Repository locator | Classification and maturity | Current use |
|---|---|---|---|
| Original Powley loading-density arithmetic | `original/charge.py`; `EQ-003/004`; 1961 manual | `original_powley_primary`; verified historical scalar | historical context only; measured net powder space and historical powder classes required |
| Davis charge/pressure relations | `later/davis.py`; Davis audits; `EQ-072/073` and later entries | later associated source; primary pages not retained; normalized derivatives medium confidence | later historical reproduction only |
| Manufacturer load statements | no admitted local artifact/dataset | `manufacturer_published`; absent | unavailable pending lawful source intake |
| Independent laboratory measurements | none retained | `independent_laboratory_measurement`; absent | unavailable |
| User measurements | legacy values lack sufficient identities/methods | at best unresolved `user_measurement` candidates | context only; not admitted |
| M01 geometry/capacity | accepted M01 records | `derived_quantity`/declared inputs; promoted record layer | exact future inputs only; no charge inference |
| M02 powder evidence | accepted neutral schema; no production powder database | record capability only | exact future references; no property selection |
| M03 diagnostics | accepted literal diagnostics | derived diagnostic | method-specific prerequisites only |
| M04 outcomes | accepted audit records | policy/audit evidence | optional audit dependency; never scientific validation |
| Quarantined charge regression | `experimental/charge_regression.py`; `CONST-016/018` | `empirical_fit`; implemented experimental; fit provenance incomplete | regression reproduction only |
| Emulator/GRT/jRT/QuickLOAD/legacy artifacts | source ledger; artifact manifest; data audit | reverse-engineered/modeled/stale/unresolved | contextual or experimental only; no promotion |

Artifact presence establishes neither authority nor admissibility. No new
scientific evidence was retained for this review.

## Candidate A: Source-Declared Interval Adapter

This is primarily a source-normalization adapter when it copies an exact printed
interval without mathematical transformation; unit conversion or endpoint
normalization is a derived operation and must be separately identified.

Potential future admission requires lawful retained source bytes or a documented
retention limitation, edition/table/page/row, exact wording and supplied units,
components/lots when printed, firearm/apparatus, endpoint inclusion, reported
precision, conditions, and explicit missing states. Printed `starting` and
`maximum` remain source terms without endorsement. Missing inclusion makes a
bounded result indeterminate rather than guessed. A printed interval does not
prove every interior point was tested.

This is the least semantically ambitious production M05 candidate, but only
after the empirical evidence record contract and a separately authorized source
intake. It is not authorized now.

## Candidate B: Measurement-Supported Region

Exact measured load points can support explicit M05 point segments when their
component/lot, firearm, conditions, instrument/calibration, pressure quantity,
shot/replicate, exclusion, and uncertainty records are adequate. They do not by
themselves support continuity between charges. Initially, only exact observed
points are potentially defensible; no minimum replicate count is invented here.
Any future minimum must be method- and claim-specific and predeclared.

Failed/excluded shots remain visible. A pressure limit is contextual unless an
authorized method defines the exact comparison and standard. Sparse points,
mixed lots/configurations, missing raw observations, or unlike pressure methods
prevent interval claims. A convex envelope would overstate evidence. No
measurement-supported method is authorized.

## Candidate C: Empirical Cohort Envelope Or Fit

A future fit would require versioned features and units, training population,
cohort/split identity, duplicate lineage, selection-bias analysis, calibration
and holdout strategy, domain, residuals/error metrics, model-form uncertainty,
outlier policy, extrapolation rejection, and pressure-standard compatibility.
Selecting a `high-performance` cohort using the target quantities risks target
leakage and must be explicitly analyzed.

The existing charge regression can be reproduced only as quarantined in-sample
behavior: its source population, fit procedure, units, selection, and independent
validation are incomplete. It cannot be promoted. No fit is authorized.

## Candidate D: Geometry Or Fill Constraint

Any future mass constraint must distinguish gross case capacity from measured
seating-specific usable powder space and geometric estimates. It needs exact M02
powder bulk-density observations for the product/lot/conditions plus measurement
method, settling/packing procedure, uncertainty, and compressed-load semantics.
M02 currently provides record capability but no admitted production evidence.

A fill constraint does not establish pressure, burn behavior, suitability, or
safety. No fill-to-charge conversion is authorized.

## Candidate E: Historical Powley Arithmetic

The historical `0.80` and `0.86` factors apply to measured net powder space and
the limited evidenced 1961 powder classes. They produce an initial historical
charge value, not a modern region, safe value, or recommendation. Their domain
does not cover modern products/lots by name similarity.

A future adapter could preserve an explicit historical result separately, using
the original adapter boundary and canonical non-implications. It is historical
context only and is not admitted as a modern production M05 method.

## Candidate F: Davis Relations

Davis is later, never original Powley. The primary NRA pages are not retained;
equations/Table 4 are normalized derivatives with unresolved primary visual
reconciliation, interpolation interpretation, historical crusher-pressure
semantics, and missing row-level validation data. Loading-density and charge
relations retain their historical domain and powder dependency.

Davis behavior remains under `later/`. It is evidence-limited for any modern M05
role and is not promoted.

## Candidate G: Literal Intersection

Future intersection would need exact inclusive/exclusive endpoint rules,
preservation of disjoint results, explicit empty versus conflicting semantics,
constraint dependency/correlation metadata, source-domain checks, and retention
of every input authority/maturity without automatic ranking. Intersection cannot
make weak or dependent inputs more authoritative.

It should be method-specific until shared semantics and evidence propagation are
proven; a generic interval engine would invite unsupported reuse. Intersection
remains blocked and unauthorized.

## Method-Admissibility Matrix

| ID | Purpose / exact input | Output basis | Evidence / maturity / authority | Domain and assumptions | Required diagnostics / criteria / uncertainty / validation | Failure modes and non-implications | Disposition / missing evidence / authorization sequence |
|---|---|---|---|---|---|---|---|
| `M05-CAND-A` | Copy one exact retained source statement | `source_declared_interval` or nondeterminate state | source class retained; candidate until source intake; exact publisher/edition | only printed components apparatus conditions and endpoints; no inferred inclusion | M03 transcription/domain completeness; M04 wording/non-implication audit; precision separate from uncertainty; source comparison | missing/ambiguous endpoint edition/lot; no safety recommendation interior testing or universality | `potentially_admissible_after_source_intake`; evidence-record schema -> source intake -> adapter specification/amendment -> tests/review |
| `M05-CAND-B` | Represent exact measured points | initially point segments under `measurement_supported_interval` | laboratory/user measurement; retained candidate until validation contract | exact component lot firearm instrument conditions; no continuity | shot/load/replicate completeness; exclusions/conflicts; method-specific M04 audit; measurement uncertainty; independent replication where claimed | sparse/mixed/failed/unknown methods; no interval continuity safety or suitability | `potentially_admissible_after_validation_contract`; evidence records -> admitted dataset -> point-adapter specification -> validation/review |
| `M05-CAND-C` | Estimate bounds from a frozen cohort | `experimental_estimate` | `empirical_fit`; experimental only; hypothesis authority | declared training population/features/domain; no extrapolation | cohort/split leakage diagnostics; fit criteria; model-form uncertainty; held-out/external metrics | selection bias overfit duplicate leakage incompatible pressure outliers; no advice | `experimental_only`; contracts -> hypothesis -> experimental reproduction -> held-out validation -> separate promotion review |
| `M05-CAND-D` | Preserve an externally established fill/mass constraint | `geometry_or_fill_constraint` | M01 derived geometry plus admitted M02 measured properties; currently evidence-limited | exact usable-space basis powder lot bulk-density method packing/condition | capacity identity/domain diagnostics; explicit method criteria; input uncertainty retained; physical measurements | gross/net substitution packing compression lot variance; no pressure/suitability meaning | `evidence_limited`; powder intake + measurement method + method specification + validation |
| `M05-CAND-E` | Adapt explicit historical Powley initial-charge output | likely separately identified historical-context record | original primary scalar; verified historical reference only | 1961 powders historical factors measured net space | original adapter compatibility; M04 historical/non-implication audit; source rounding; source examples only | modern substitution domain error; not a region safety value or recommendation | `historical_context_only`; any adapter requires specification amendment and explicit authorization |
| `M05-CAND-F` | Adapt later Davis charge relation | separately identified later-method context | later Davis; source reconciliation incomplete; historical crusher context | printed historical domain and powder/pressure semantics | Davis completeness/domain diagnostics; later-method audit; unresolved uncertainty; primary reconciliation and measured validation | damaged/derivative source Table 4 interpolation crusher pressure; no modern safety | `evidence_limited`; retain primary pages -> reconcile -> candidate specification -> independent validation -> review |
| `M05-CAND-G` | Intersect already admitted constraints | `intersection_of_explicit_constraints` | derived quantity; no current method authority | only explicit compatible independent/dependent inputs with defined endpoint semantics | domain/dependency diagnostics; method-version criteria; no hidden uncertainty; invariant tests and validation against expected set algebra | empty/conflict conflation disjoint loss dependence authority inflation; no safety or preference | `blocked`; admit input methods -> specify dependency/authority rules -> authorize method-specific operation -> tests/review |

## Pressure And Validation Boundary

CUP, crusher pressure, piezoelectric PSI, strain-derived estimates, modeled
pressure, and measurement locations remain distinct. Equal units do not create
equivalence. No pressure value establishes a charge bound without an admitted
method, and remaining below a published value does not establish safety.

Source-example and regression reproduction test implementation correspondence.
Calibration and in-sample evaluation cannot be relabeled held-out validation.
External replication requires independently collected or retained evidence not
controlled by the development process.

## Recommended Bounded Next Step

Prepare a user authorization review for implementation of immutable empirical-
load evidence records and strict serialization only, with synthetic fixtures and
no scientific intake. Do not combine that schema work with M05 adapters,
datasets, cohorts, fits, intersection, or M06.

## Remaining Blockers

- no authorized empirical-load record/schema implementation;
- no admitted/lawfully retained manufacturer or laboratory dataset;
- no shot/trace/replicate/cohort/split contract;
- unresolved legacy CSV provenance and stale generators;
- absent pressure equivalence/cross-standard authority;
- incomplete Davis primary reconciliation and validation population;
- no admitted M02 production powder properties;
- no method-specific uncertainty or validation gates for a region claim.
