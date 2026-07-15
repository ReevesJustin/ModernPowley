# Empirical Load Evidence Records Phase 1 Authorization Decisions

## Status

`accepted_authorization_decisions`

These decisions refine only the separately authorized records-and-serialization
Phase 1. They authorize no implementation in this commit, source intake,
production data, cohort/split, M05 method, or M06 work.

## Decisions

| Question | Alternatives considered | Evidence | Decision | Rationale and consequences | Remaining uncertainty |
|---|---|---|---|---|---|
| Canonical scope identity | numbered milestone; parent workstream; bounded workstream phase | parent spans M02/M05/M09 and remains planned; M06 has different scientific scope | use `empirical_load_evidence_records_phase_1` under `docs/modernization/workstreams/` | gives the implementation a durable scope authority without inventing a historical milestone or authorizing the parent | future phases need their own specifications |
| Parent status | authorize entire workstream; authorize only Phase 1 | planning review recommends records first | keep parent `planned`; Phase 1 alone is `authorized` | cohort/split, intake, M05 method, and M06 remain deferred | no Phase 2 is defined |
| Common envelope | family-specific ad hoc fields; one independent envelope | M01-M05 require exact identity/version/provenance/lifecycle | require schema/type, ID/version, independent activation/evidence/maturity/review/supersession, exact lineage/conflicts, and synthetic marker | prevents lifecycle and evidence concepts collapsing | exact enum names remain implementation decisions |
| Record families | generic observation row; distinct source/load/shot/series/trace/chronograph/aggregate types | planned workstream and scientific semantics differ by layer | authorize eight distinct families | a shot cannot masquerade as a configuration/summary and aggregate never replaces members | some sources will lack sufficient identity for normalized records |
| Powder identity | commercial string; embedded copy; exact M02 reference | M02 owns powder identity and lot separation | exact M02 identity reference plus load-context lot qualifier; no embedded property observations | avoids duplicate powder truth and alias inference | future powder intake remains separately governed |
| Bullet/case/primer identity | require nonexistent catalog; commercial string; scoped assertion | no accepted general component store exists | authorize scoped component identity assertions with kind, manufacturer, product, revision, lot, provenance, and semantic missingness | preserves exact reported identity without claiming catalog authority | later component store migration requires explicit review |
| Firearm and apparatus | prose only; catalog records; scoped exact assertions | M01 owns geometry but not a complete equipment store | use exact scoped identities and M01 references where exact; unknowns remain tagged | configuration cannot disappear behind a firearm name | canonical apparatus store deferred |
| Pressure values | extend M01 units; bare number/unit; source-preserving reported value | M01 deliberately lacks pressure; pressure methods are non-equivalent | do not change M01; authorize a non-arithmetic reported-value union with quantity/method/location/standard/unit/source semantics | preserves CUP, piezo, strain, crusher, and modeled distinctions without conversion | exact controlled vocabulary requires implementation review |
| Velocity and acquisition values | extend M01 speculatively; bare floats; source-preserving values | M01 lacks velocity/time; acquisition context is material | same source-preserving no-arithmetic boundary; reuse M01 only where exact | prevents silent correction/normalization | exact velocity and time unit labels remain controlled implementation choices |
| Trace scope | embed arrays; metadata plus references; prohibit traces | planning authorizes custody/lineage before processing | metadata and immutable raw/processed artifact references only | no sample storage or signal processing; raw bytes stay immutable | artifact storage/intake is not authorized |
| Missingness | nulls/defaults; new broad taxonomy; reuse M02 | M02 already distinguishes required semantic states | reuse M02 where exact; new load states require explicit decision and tests | missing cannot become generic applicability | exact load-specific additions, if any, remain deferred to implementation decision |
| Conflicts and duplicate publications | select/average; retain groups; count publications | M02 conflict policy and replicate integrity | retain all conflict members; duplicate underlying tests share lineage and do not count as independent replicates | no automatic winner or inflated replication | common origin may remain indeterminate |
| Exclusions | delete invalid shots; inactive lifecycle; independent status | validation requires failure visibility | independent observation/exclusion status and reason; always serialize excluded records | activation does not erase acquisition validity context | controlled reason vocabulary remains an implementation decision |
| Precision versus uncertainty | infer tolerance from digits; separate fields | M01 uncertainty and planning policy | source wording/precision/rounding remain distinct from uncertainty | printed digits do not acquire statistical meaning | source may not disclose its rounding method |
| Units | normalize and replace; retain source plus optional derived conversion | M01 source-unit policy | retain source values/units; any normalized value is separate with exact method/lineage; no Phase 1 conversion | unit conversion cannot reconcile evidence | future conversion authorization may be needed for new dimensions |
| Serialization schema | reuse M02/M05; defer identifier; dedicated family | record semantics differ and Phase 1 is now bounded | use `modern_powley.empirical_load_evidence.v1`; strict tagged records, no migration/aliases/coercion/unknown fields | M01-M05 serializers remain unchanged | future versions need explicit migrations |
| JSON determinism | canonical bytes; unordered output; deterministic repository encoder | standard JSON has multiple equivalent byte forms | require sorted deterministic member output per encoder/configuration, exact data round trip, and duplicate-key rejection; do not promise canonical cross-encoder bytes | makes tests reproducible without a false cryptographic serialization claim | canonical byte format could be separately specified later |
| Public API | package-root exports; module-qualified; private only | user requests narrowest surface and M01-M05 root is stable | keep Phase 1 module-qualified initially; no package-root exports | limits accidental commitment and keeps M05 independent | export review may follow demonstrated accepted use |
| Synthetic fixtures | adapt existing rows; realistic examples; fictional markers | evidence boundary prohibits promotion and actionable data | fictional `SYN-ELE-*` identities, explicit synthetic marker, non-actionable values, tests-only location | exercises structure without creating evidence or guidance | exact fixture values chosen during implementation review |
| Cohorts and splits | include now; retain vocabulary only; remove policy | parent workstream owns future validation contracts | no cohort/split classes or serialization in Phase 1; eight roles remain documentation only | Phase 1 cannot assign calibration or validation membership | separate authorization required |
| Non-implications | general disclaimer; explicit list | parsing can be mistaken for validation/readiness | specification enumerates source, measurement, equivalence, replication, safety, recommendation, M05, and M06 non-implications | structural success has deliberately narrow meaning | none within Phase 1 |

## Authorization Consequence

A later task may move the Phase 1 specification to `in_progress`, create a
design and implementation decision record, then implement only the records,
strict serializer, synthetic fixtures, tests, documentation, and completion
evidence in the specification. No implementation starts in this authorization
commit. Any source intake, cohort/split, trace samples/processing, package-root
export, M05 dependency/adapter/derivation, model, or M06 work requires a new
traceable specification or amendment.
