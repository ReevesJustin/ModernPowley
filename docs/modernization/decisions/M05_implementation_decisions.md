# M05 Implementation Decisions

Status: `accepted`

M05 entered `in_progress` in the working tree before either source module was
created. These decisions implement only the accepted records-only authorization.

## Decisions

Each row records question; alternatives; governing authority; decision;
rationale; consequence; and remaining limitation.

| Question | Alternatives | Authority | Decision | Rationale / consequence | Remaining limitation |
|---|---|---|---|---|---|
| Module layout | one file; many files; two files | M05 scope | `charge_regions.py` plus `m05_serialization.py` | smallest separation of model and I/O | no repository/database layer |
| Reused types | duplicate; reuse M01-M02 | boundary | reuse `Quantity`, `Provenance`, `EvidenceClass`, `ModelMaturity`, `SourceLocator` | preserves accepted semantics | references are not verified |
| Exact references | strings; typed role | authorization | role/schema/type/id/version/evidence/maturity record | M04 can be audit-only | external identity truth is caller responsibility |
| Empty basis | optional; required | state policy | basis and method required | empty is a definite externally supplied result | repository cannot calculate emptiness |
| Indeterminate basis | prohibited; optional pair | semantic distinction | basis/method both absent or both present | preserves known attempted basis without partial identity | no inference |
| Conflict refs | arbitrary; unique two-plus | authorization | exact unique refs, at least two, `M05_REGION` role | preserves all members without winner | no resolution |
| Shared boundary | any touch; both included fails | segment policy | permit touch unless both include same value | preserves disjoint topology | no normalization |
| Precision | numeric tolerance; text | authorization | optional exact reported-precision text | never becomes uncertainty | no machine rounding semantics |
| Uncertainty | M01 scalar only; tagged declaration | authorization | measurement/model-form/unknown/not-applicable/external declaration | avoids false numeric semantics | no propagation |
| Pressure units | add M01 units; source label | pressure policy | required textual quantity/method/instrument/unit plus source metadata | no pressure arithmetic | labels are not normalized |
| Activation | criterion status; new enum | lifecycle policy | `active`/`inactive` | independent of supersession | no lifecycle automation |
| Supersession | partial strings; exact pair | lifecycle policy | exact prior region ID and positive version | rejects partial/self reference | no record lookup |
| Non-implication | arbitrary prose; controlled | contract | required singleton enum rendering canonical statement | cannot omit clauses | callers may add qualifications only |
| JSON types | coercion; strict | serialization authority | explicit type checks, bool rejected as int, no `str/int/float` coercion | malformed input fails | prior serializers unchanged |
| Duplicate JSON keys | last wins; reject | strictness | reject using `object_pairs_hook` | no silent overwrite | applies only to M05 loader |
| Public exports | all helpers; contract only | public boundary | enums/records/schema/four serializers only | no prohibited helpers | structural validation occurs in constructors |

No decision admits a method, real data, calculation, or future milestone.
