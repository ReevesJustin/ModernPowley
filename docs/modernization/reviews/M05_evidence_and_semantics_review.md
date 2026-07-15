# M05 Evidence And Semantics Review

Review status: `completed_planning_snapshot`

This review records the evidence state at the planning commit. Its conclusion
that M05 was then `planned` is preserved for traceability; the later records-only
authorization changes the active milestone status without admitting a numerical
method or production evidence.

## Finding

A provenance-preserving charge-region record contract can be specified without
creating loading advice. The repository does not, however, retain an admitted
production method or dataset that can generate a defensible modern charge
region. M05 therefore remains `planned`; this review authorizes no numerical
implementation.

## Semantic Boundary

A charge-region record is a versioned bounded analytical object for later
evaluation. It is not a recommended charge, starting load, maximum load, safe
range, loading instruction, powder-suitability declaration, pressure or velocity
prediction, proof that every interior point is valid, or proof that any interior
point was tested.

These objects must remain distinct:

| Object | Meaning | Must not become |
|---|---|---|
| charge region | exact sourced/derived charge-mass segments plus lineage | recommendation or safe range |
| published load interval | values printed by one source under stated components/conditions | universal domain or inferred continuum |
| geometry/fill constraint | volume- or mass-ratio constraint with explicit property inputs | charge mass without powder-volume evidence |
| uncertainty interval | uncertainty attached to a measured or derived quantity | permissible charge interval |
| pressure limit/observation | named pressure quantity under a named method/standard | charge bound or safety proof |

## Evidence Inventory

| Family and repository locator | Class / maturity | Quantity semantics and units | Domain / pressure identity | Disposition and promotion requirement |
|---|---|---|---|---|
| Original Powley manual `SRC-POWLEY-1961-MANUAL`; `EQ-003`, `EQ-004`; `original/charge.py` | `original_powley_primary`; source-reconciled historical scalar | `Wc=0.86*V0` or `0.80*V0`; grains powder from grains water | limited printed IMR families and measured seating-specific powder space; not a pressure bound | historical/context only for M05; it yields an initial charge, not a region or safety interval. Admission would require an explicitly authorized historical-observation basis, never silent reuse as modern policy. |
| Original small-change and lettered procedures `EQ-057`, `EQ-058` | original primary; documented, unimplemented/evidence-limited | percent change heuristic and a 5% lettered procedure | manual excludes maximum loads; lettered procedure depends on missing scale | unavailable as an M05 method. Complete primary scale evidence, domains, and reading rules would be required even for historical execution. |
| Davis publication and derivatives `SRC-DAVIS-1981`, `SRC-DAVIS-1981-RAW-OCR`, `SRC-DAVIS-1981-DERIVATIVE-REPRINT`; `EQ-070`, `EQ-071`, `EQ-083` | later associated primary identity with local secondary derivatives; source reconciliation remains limited by absent primary page images | charge estimates and loading-density scaling in grains and dimensionless historical ratios | printed strong-rifle/IMR/non-compressed context; crusher-pressure semantics are separate | later-method context only. Primary visual verification, exact domains, method audit, and separate promotion would be required; no Davis value is admitted to M05 here. |
| Manufacturer-published charge/pressure data | `manufacturer_published`; no retained qualified dataset | potentially source-declared charge masses and named pressure/velocity observations | must retain exact components, lot/edition, test firearm, conditions, pressure quantity/method/standard | potentially admissible only after source intake, license/retention, field-level provenance, domain audit, and explicit authorization. Presence in a manual would not by itself prove every interior point tested or safe universally. |
| Independent laboratory measurements | `independent_laboratory_measurement`; none retained for M05 | measured charge points with instrumented outputs and uncertainties | apparatus, calibration, standard, protocol, components, conditions, replicates, and pressure identity required | potentially measurement-supported evidence after retained raw data/protocol and independent review; not currently available. |
| User measurements | `user_measurement`; no qualified M05 dataset | user-supplied physical observations | method, equipment, calibration, components, environmental conditions, uncertainty, and pressure identity required | may be retained as observations; not automatically a region, calibration authority, or final evaluation dataset. |
| M01 records and geometry `modern_powley.m01.v1`; `SRC-M01-DESIGN` | promoted modern foundation | explicit SI quantities, gross/measured/estimated capacity identities, geometry and uncertainty | record-specific conditions; no powder bulk-fill or charge estimator | admissible as exact inputs only. Capacity types cannot substitute. Geometry does not create a charge bound. |
| M02 observations `modern_powley.m02.v1`; `SRC-M02-DESIGN` | promoted neutral evidence contract | dimensional/categorical/source-specific observations, missingness, conflict, uncertainty and domains | literal declared domains; unspecified is not unrestricted | admissible as exact referenced evidence only. No production powder facts or automatic property selection exists. |
| M03 diagnostics `modern_powley.m03.v1`; `SRC-M03-DESIGN` | promoted diagnostic contract | requirement and literal-domain statuses | exact supplied requirement/domain context | admissible as exact diagnostic dependencies; a pass is not scientific validation or solver readiness. |
| M04 criteria/outcomes `modern_powley.m04.v1`; `SRC-M04-DESIGN` | accepted decision-record contract | declarative comparisons and recorded outcomes | exact criterion/set/context versions | audit dependency only. A pass cannot establish method validity, safety, suitability, or a region and cannot replace underlying M01/M02 evidence. |
| Charge regression `EQ-016`; `experimental/charge_regression.py`; legacy prediction artifacts | `empirical_fit` / experimental; fit provenance absent | predicted charge mass from net capacity and travel | training/evaluation population and applicability unresolved | experimental retention only. Requires source dataset, fit procedure, independent holdout plan, uncertainty/domain audit, and explicit promotion; prohibited as an M05 default. |
| Archived emulator `SRC-KWK-EMULATOR`; `later/emulator.py` | `reverse_engineered` / emulator-derived | reproduces archived charge, powder, velocity, pressure behavior | implementation-specific; not original authority | contextual comparison only; cannot fill M05 or original-source gaps. |
| GRT artifact `SRC-GRT-LOAD-001` and legacy GRT-derived CSVs | simulator/model artifact; unresolved field semantics | modeled inputs/outputs with heterogeneous or unknown units | one simulator load artifact, not laboratory measurement; pressure semantics require model docs | experimental/context only. Requires authoritative model semantics, retained dataset provenance, and separate promotion. |
| jRT and QuickLOAD references | no retained authoritative M05 source/data identified | proprietary or modeled behavior not established locally | unknown in retained evidence | unavailable. Artifact intake, rights, semantic mapping, and explicit reverse-engineered/model classification would be required. |
| Legacy CSVs and scripts under `data/` and `scripts/` | heterogeneous legacy/experimental artifacts | mixed fields; some source dependence and known defects | row provenance, domains, and validation status incomplete | audit retention only. They are not measurements and cannot populate M05 production records. |

No candidate family is promoted by this review.

## Proposed Region Semantics

The future contract should support a tagged region state: one or more bounded
segments, empty, unavailable, indeterminate, or conflicting. Determinate
segments use finite positive charge-mass bounds, explicit units, and explicit
inclusive/exclusive endpoints. A point is a closed equal-bound segment and does
not become a recommendation.

Multiple disjoint segments are required. A containing envelope would assert
validity across an evidentiary gap, so it is prohibited. Exact duplicates may be
identified but not silently removed when their provenance differs. Supersession
and activation remain independent: a superseded record is retained, and an
inactive record is not deleted or automatically replaced.

An empty intersection records that explicit constraints share no value. An
indeterminate result records that missing bounds, unresolved domains, partial
comparability, dependency, or conflict prevents a literal conclusion. A
conflicting region retains every member and does not average or choose one.
Open-ended source statements and missing bounds remain source constraints or
non-determinate states; they are not silently made finite.

## Basis Review

The controlled basis categories proposed in the specification are justified as
descriptive distinctions, subject to later implementation review:

- `source_declared_interval`: exact interval printed by a retained source;
- `measurement_supported_interval`: explicitly defined from retained measured
  points, with coverage limitations retained;
- `geometry_or_fill_constraint`: a constraint whose physical quantity and
  conversion inputs remain explicit;
- `property_uncertainty_constraint`: a constraint derived from an explicitly
  identified property uncertainty, not a permission interval;
- `intersection_of_explicit_constraints`: lineage-preserving literal
  intersection, if separately authorized;
- `experimental_estimate`: visibly unpromoted method output;
- `unavailable`, `indeterminate`, and `conflicting`: non-numeric states.

No evidence-class hierarchy selects a basis. A derived intersection is a
derived quantity, retains all material inputs, and cannot claim admission or
maturity beyond what every material input supports.

## Uncertainty And Dependence

Measurement, geometry, capacity, bulk-density/lot variation, source rounding,
model-form uncertainty, and unknown uncertainty must remain separately
identified. A source-rounded endpoint is not automatically a measurement error
bound. M01 bounded uncertainty may be referenced, but no probability,
confidence, covariance, Monte Carlo, or propagation rule is admitted.

Dependence and correlation must be explicit when known and `unknown` otherwise.
An uncertainty interval cannot be copied into the region field or interpreted as
a permissible charge interval.

## Pressure Semantics

Any contextual pressure record must retain pressure quantity identity, method,
instrument (including crusher versus transducer), standard/protocol and edition,
units, conditions, source domain, and exact source limit or observation. CUP and
modern piezoelectric PSI are not interchangeable and no conversion is admitted.
Being below a published number does not establish safety, and this planning task
performs no pressure-to-charge calculation.

## M01-M04 Dependency Decision

A future M05 record must reference exact underlying M01/M02 evidence and exact
M03 diagnostics used to establish completeness or literal domain status. It may
also reference exact M04 outcomes to preserve an audit chain, but it cannot
consume an M04 pass as a substitute for scientific evidence. This avoids
duplicating prior contracts and prevents a recorded policy outcome from becoming
an unsupported physical claim.

## Unresolved Blockers

1. No production charge-region derivation method is admitted.
2. No retained manufacturer dataset or qualified laboratory dataset supports a
   real M05 record.
3. Converting a fill constraint to charge mass requires admitted, lot/condition-
   specific powder-volume semantics absent from current production data.
4. No uncertainty propagation or input-dependence model is authorized.
5. Cross-standard pressure interpretation and comparison remain unresolved.
6. Literal intersection behavior, segment normalization, and overlapping
   same-source segments require implementation-level decisions.
7. The first implementation increment should remain records-only unless a later
   authorization explicitly admits a narrowly sourced derivation.

## Recommendation

`ready_for_user_authorization_review`

This recommendation concerns a records-only M05 implementation boundary. It is
not authorization, does not admit a production derivation method, and does not
authorize numerical charge-region construction.
