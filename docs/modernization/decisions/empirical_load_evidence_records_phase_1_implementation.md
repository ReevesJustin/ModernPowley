# Empirical Load Evidence Records Phase 1 Implementation Decisions

## Status

`accepted`

## Decisions

| Question | Alternatives | Governing evidence | Decision | Consequence and limitation |
|---|---|---|---|---|
| module layout | one monolith; subpackage; two modules | authorized narrow module-qualified surface | records plus serialization modules | compact and acyclic; no root exports |
| record construction | positional; keyword-only | many semantically distinct fields | all new dataclasses are frozen/slotted/keyword-only | explicit call sites; tuples defend nested immutability |
| identifier grammar | unrestricted; UUID-only; restricted ASCII | exact stable IDs must support existing schema references | `[A-Za-z][A-Za-z0-9._:-]{0,127}` | rejects whitespace/path-like IDs without imposing UUIDs |
| record types | string; enum | controlled discriminator required | eight-value `EmpiricalRecordType` | class/envelope mismatch fails |
| lifecycle/review | combined status; independent enums | authorization forbids conflation | `ActivationState(active,inactive)` and `ReviewState(unreviewed,review_required,reviewed,qualified)` | exclusion and supersession remain separate |
| exclusion | boolean; deletion; enum record | excluded/invalid observations must remain | `ExclusionState(included,excluded,invalid,not_applicable)` plus reason/authority context | excluded/invalid require explanation and authority |
| missingness | new taxonomy; M02 reuse | M02 states cover authorized needs | reuse `MissingState`; add no new state | generic `MissingValue` and present-or-missing wrappers retain explanation/references |
| field nullability | optional scientific values; tagged unions | missing science cannot be omission | `None` only for inactive union arms, no supersession, or inapplicable method | all required facts are present or semantic missingness |
| exact decimals | float; Decimal object; exact lexical string | no binary loss and strict JSON | validate/store finite `decimal_text` string | no arithmetic or numeric coercion |
| precision | infer from value; free text only; controlled declaration | precision is not uncertainty | controlled precision kind plus exact statement and optional positive digits | no inferred tolerance |
| uncertainty | M01 everywhere; text only; two representations | M01 scalar semantics are not universal | M01 uncertainty only with M01 quantity; separate declarative uncertainty for reported values | no propagation or distributions |
| pressure vocabulary | unit-only; unrestricted strings; controlled dimensions | method/location/standard cannot collapse | controlled quantity, origin, location, acquisition, unit, and shot/aggregate context | standards/instrument identities remain exact references or missingness |
| controlled unit labels | trust any label; reconcile units; require literal agreement | CUP and PSI must not collapse | CUP/psi/bar/MPa and m/s/ft/s enums require their exact source labels; source-specific and unresolved labels remain literal | no conversion or equivalence is inferred |
| velocity vocabulary | generic speed; controlled acquisition/correction | distance/correction/context are material | controlled individual/mean/other identity and raw/corrected/muzzle-extrapolated states | no corrections or comparisons |
| component identity | catalog; bare name; scoped assertion | no component store exists | scoped bullet/case/primer assertions with manufacturer/product/revision/lot present-or-missing | future store links by new exact reference; original assertion is never overwritten |
| powder identity | copy M02; bare name; exact reference | M02 owns powder identity | exact `modern_powley.m02.v1/powder_identity` reference and lot qualifier | no property copying or alias resolution |
| trace states | raw/processed only; four states | external derivative and unresolved evidence differ | raw, processed externally, derivative transcription/export, unresolved | processed/derivative requires external method; no sample arrays |
| artifact hash | free text; filesystem verification; syntax validation | records do no I/O | retained artifacts require lowercase 64-hex SHA-256; external-not-retained uses semantic missingness | syntax only; no byte-verification claim |
| conflicts/duplicates | backrefs; winner; exact groups/lineage | all members retained, no replicate inflation | ordered unique exact member refs and explicit underlying-test lineage role | no automatic resolution or independence claim |
| exact dependency versions | allow unresolved version everywhere; require every external source to be versioned; role-specific exactness | exact M02/member/method/shot/configuration dependencies are required while external source identities may lack an internal version | exact scientific/audit dependencies require positive versions in their owning fields | unresolved external identities remain possible only where the enclosing field permits them |
| series ordering | list order only; position records | ambiguous/duplicate positions prohibited | positive, strictly ascending positions and unique exact members | caller order preserved; no sorting/interpolation |
| aggregate origin | calculate internally; store source/external | Phase 1 has no statistics API | source-reported or externally-calculated tag; latter requires method/version | aggregate value is stored, never computed |
| JSON | permissive stdlib; strict stdlib | M05 strict convention | exact keys/types, duplicate-key/nonfinite rejection, sorted output | no aliases/defaults/migrations; not canonical cross-encoder bytes |
| public surface | root exports; module-qualified | authorization chooses narrowest surface | no changes to `modernized.__init__` | callers import the two explicit modules |
| fixtures | realistic; legacy-derived; fictional | no production evidence allowed | tests-only `SYN-ELE-*` fixtures, explicit synthetic marker | no evidence authority or recognizable recipe |

## Deferred Decisions

Scientific source admission, artifact custody implementation, component-store
migration mechanics, cohorts/splits, adapters, calculations, models, and schema
migration remain outside Phase 1. A future component store may be referenced by
a new exact lineage/reference field in a later schema; it must not rewrite or
merge the serialized scoped assertion.
