# Empirical Load Evidence And Validation Decisions

Status: `planned_decisions`

These specification-level decisions authorize no implementation, source intake,
dataset, M05 method, or M06 work.

## Decisions

| Question | Alternatives | Evidence | Decision | Rationale and consequences | Remaining uncertainty |
|---|---|---|---|---|---|
| Canonical location | milestone; review only; workstream | cross-cutting roadmap spans M02/M05/M09 and pre-M06 | use `docs/modernization/workstreams/` | a cross-cutting scope is not falsely treated as an authorized numbered milestone | future workstream governance template |
| Record-family separation | one generic row; distinct types | source statements shots traces and summaries have incompatible semantics | distinct source/load/shot/series/trace/chronograph/aggregate/cohort/split records | prevents raw evidence from masquerading as summary or model input | exact future class/module layout |
| Layer separation | overwrite normalized values; immutable layers | charter and artifact policy require lineage | retain artifact -> literal/raw -> normalized -> summary -> cohort -> split -> model -> M05 | every transformation has exact method/input references; unit conversion does not reconcile evidence | storage/custody implementation |
| Shot/load/series identity | flatten; nested exact references | replicate/exclusion and changed-variable semantics | shots reference configurations; series reference ordered configurations; summaries reference members | failures remain visible and ladders imply no continuity | representation of repeated acquisition channels |
| Cohort representation | dynamic query; copied table; versioned selection record | M02/M04 prohibit discovery/preference | immutable exact-member cohort with versioned inclusion/exclusion rules and bias notes | reproducible membership; no automatic database selection | frozen-cohort storage format |
| Split vocabulary | train/test only; proposed eight roles | cross-cutting policy and model-boundary requirements | adopt `source_example_reproduction`, `regression_reproduction`, `calibration`, `in_sample_evaluation`, `interpolation_evaluation`, `cross_cartridge_evaluation`, `held_out_validation`, `external_replication` | exact evaluation claim is visible | nested-validation structure |
| Calibration separation | reuse cases silently; disclose; forbid all reuse | evidence classes require row-level role | calibration cases cannot be held-out for the same result; indirect use is disclosed | prevents inflated validation claims | policy for model-family-wide prior knowledge |
| Pressure identity | normalize by unit; controlled quantity/method context | M05 and historical audits show crusher/piezo/strain/model distinctions | retain quantity location method standard edition instrument calibration filtering units and wording separately | no CUP-to-PSI or cross-standard inference | future controlled pressure vocabulary |
| Velocity context | compare numeric values; retain acquisition context | barrel distance correction and aggregation materially differ | retain instrument distance correction/extrapolation atmosphere barrel shot/aggregate precision and uncertainty | incompatible configurations cannot silently compare | future correction-method registry |
| Component and lot identity | commercial name; optional exact identity; inferred aliases | M02 identity policy | preserve product/revision/lot for powder bullet case primer and explicit unknowns | no shared-name equivalence or cross-lot substitution | sources often omit lots |
| Missingness | null/zero; M02 semantic states | accepted M02 contract | reuse compatible semantic missingness and add only separately governed load-specific distinctions | omission never becomes generic applicability | exact future tagged union |
| Conflicts and duplicates | prefer newest; average; retain groups/lineage | M02 conflict policy | retain all conflict members; duplicate publications reference one underlying test | no winner inflation or duplicate replicate count | detecting common underlying tests may remain indeterminate |
| High-performance label | raw field; M04 criterion/cohort; prohibit forever | classification is operation-relative and risks leakage | no intrinsic raw field; later M04 criterion/outcome plus versioned cohort only | no safety optimality recommendation or cross-domain implication | whether any future use is scientifically valuable |
| M02 relationship | duplicate powder fields; exact references | M02 owns powder identity/properties/domains | load records reference exact powder identity/lot and property observations | no preferred property or universal burn order | separate powder-intake workstream specification recommended |
| M04 relationship | criterion pass as evidence; audit/classification only | M04 non-implications | M04 may audit admissibility or define operation-relative cohorts but cannot replace measurements | policy remains separate from science | future admissibility criterion sets require authorization |
| M05 relationship | evidence creates region; exact dependency only | accepted M05 is records-only | future regions reference exact evidence/diagnostics and separately admitted method | evidence storage does not authorize derivation | minimum references are method-specific |
| Hypothesis relationship | fit without hypothesis; versioned hypothesis | AGENTS and cross-cutting policy | every fit/correction/model variant references a versioned hypothesis and split records | falsification and failures precede promotion | hypothesis schema is future work |
| Proposed serialization | assign final ID now; defer ID; reuse M02 | no implementation is authorized | defer final schema ID; require future strict tagged/versioned records with exact nullability and lineage | avoids implying an API while preserving strictness requirements | schema partitioning and migration policy |
| First implementation increment | ingest data; implement adapter; records only | no admitted data or method and M06 depends on contracts | recommend immutable evidence records plus strict serialization and synthetic fixtures only | separates semantic review from scientific admission | requires explicit user authorization |

## Explicitly Deferred Decisions

- final schema identifier and module layout;
- exact controlled vocabularies for pressure quantities, instruments, exclusions,
  and load-specific missing states;
- source licensing terms for any particular publisher or dataset;
- storage for large raw pressure traces;
- replicate sufficiency, error metrics, or acceptance thresholds;
- nested-validation and grouping strategy;
- any M05 adapter, point/interval method, intersection, fit, or fill conversion;
- any scientific dataset or M06 model.

Deferral produces an explicit planning boundary, not permission to choose an
implementation default.
