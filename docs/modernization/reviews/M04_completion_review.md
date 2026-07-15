# M04 Completion Review

Status: `implemented_and_reviewed`

M04 is an immutable criterion-definition and decision-record contract. It does
not contain a production criterion set, discover observations, search a powder
collection, resolve evidence conflicts, screen or rank powders, predict
ballistics, or establish suitability, safety, approval, or recommendation.

## Implementation Map

| Area | Implementation | Principal tests |
|---|---|---|
| Criterion and set definitions | `modernized/screening_criteria.py` | `test_m04_screening_records.py` |
| Exact evidence and context | `modernized/screening_contexts.py` | unit and serialization tests |
| Outcome and manual assertion records | `modernized/screening_outcomes.py` | unit and serialization tests |
| Narrow literal evaluation and set summary | `modernized/criterion_evaluation.py` | endpoint, interval, role and summary tests |
| Strict M04 serialization | `modernized/m04_serialization.py` | `test_m04_serialization_and_policy.py` |
| Provenance definitions | `SRC-M04-DESIGN`, `EQ-113`, `EQ-114`, M04 data fields | `test_m04_coverage.py` |
| Durable milestone governance | canonical M01-M04 specifications, roadmap, `AGENTS.md` | `test_milestone_governance.py` |

## Acceptance Gates

| Gate | Result | Evidence or limitation |
|---|---|---|
| 1. Starting-state integrity | pass | Clean synchronized `bf388c8`; preservation tag unchanged. |
| 2. Definition integrity | pass | Frozen versioned definitions/sets; controlled roles/statuses/forms; no callbacks or expression language. |
| 3. Explicit input integrity | pass | Exact evidence IDs in context; missing references produce structured failure; no discovery, aliases, fallback, or preference. |
| 4. Outcome integrity | pass | Controlled outcomes retain exact values, threshold, comparison, reason, versions, method and provenance. |
| 5. Criterion-set integrity | pass | Roles remain distinct; order is display-only; no weights/scores; advisory failures do not alter mandatory summary. |
| 6. Version integrity | pass | Exact criterion/set/context versions; mismatch and duplicate outcomes remain explicit; no migration. |
| 7. Missing and conflict integrity | pass | M02 missing states and all conflicting IDs retained; no numerical comparison, winner, averaging, or silent pass. |
| 8. M03 reuse integrity | pass | Exact M03 diagnostic status references; no M03 domain or completeness comparison is duplicated. |
| 9. Dimensional and boundary integrity | pass | M01 quantities, exact definitions, inclusive/exclusive endpoints, literal interval containment; partial overlap indeterminate. |
| 10. No discovery or selection | pass | Public API/AST tests; package has no catalog, query, alias, preference, or record-selection API. |
| 11. No ranking or scoring | pass | No weights, scores, tie breakers, percentages, or candidate comparison; counts are descriptive only. |
| 12. Serialization integrity | pass | Strict `modern_powley.m04.v1`; embedded evidence/thresholds reparse strictly; prior schema identifiers unchanged. |
| 13. Architecture isolation | pass | M04 imports only modernized M01-M03 contracts; `original/` has no modernized import and no numerical change. |
| 14. No ballistic or recommendation leakage | pass | Scope/API tests show no charge, pressure, velocity, burn, solver, calibration, safety, suitability, or recommendation behavior. |
| 15. Evidence restraint | pass | No production powder/criterion data; tests use conspicuous synthetic records; no quarantined source promoted. |
| 16. Documentation and ledger completeness | pass | Design, decisions, review, README/TODO/usage/roadmap, source/equation/field ledgers and source-ledger artifact inventory updated. |
| 17. Validation | pass | `uv sync --locked --offline`; lock check; 317 full tests; 86 focused tests; compile; diff; CSV/JSON/notebook/Markdown links; hashes; imports; architecture; vocabulary and roadmap checks passed. |
| 18. Durable milestone governance | pass | Four canonical specifications, complete required sections, roadmap chain, agent rules, source hashes and governance tests are present. |

## Literal Outcome Boundary

A pass records only that the exact evidence supplied in the context satisfied
the exact declaration and version. `all_mandatory_recorded_passes` records only
that each active mandatory criterion has an exact pass. An advisory failure does
not affect that summary. A set with no active mandatory criteria is not granted a
vacuous positive summary. Manual assertions are visibly separate and cannot
override inactive, superseded, mismatched, or absent definitions.

## Milestone Specification Reconstruction

The canonical M01-M03 specifications were reconstructed from their accepted
session authorization, phase documents, binding decisions, implementation,
principal tests, ledger entries, and completion reviews. They retain the gates
and evidence boundaries that were active at completion:

- M01 remains units, records, geometry and explicit historical adapters only.
- M02 remains neutral powder evidence records with no real powder database or
  property-selection semantics.
- M03 remains operation-relative completeness and literal domain diagnostics,
  not solver preparation or powder screening.

The principal implementation refinements were documented rather than silently
normalized: M01 used conservative record-specific serializers; M02 retained
unsupported dimensional-looking values as literal source scalars; M03 admitted
conservative interval containment with partial overlap indeterminate. None
removed or broadened an accepted gate.

M04 was specified with status `in_progress` before this completion review and
before any acceptance status. Its new Gate 18 requires the durable governance
contract to pass before acceptance.

## Governance And Future Workflow

The roadmap now links each M01-M04 specification, phase design, decision record,
completion review, ledgers, and principal tests. `AGENTS.md` requires future
agents to read the specification, treat decisions as binding refinements, keep
reviews evidentiary, use traceable amendments, and commit an authorized
specification before implementing M05 or later.

M05 remains a future phase concept and recommendation only. It has no canonical
authorized specification and no implementation permission.

## Intentionally Unavailable

M04 does not determine whether a threshold is scientifically correct, find an
observation, choose among conflicting records, screen a powder catalog, declare
powder/cartridge suitability or safety, rank candidates, calculate a charge, or
predict pressure, velocity, combustion, burnout, or muzzle pressure.

## Decision

All 18 gates pass. M04 is accepted as the declarative criterion and auditable
outcome record layer. M04 was specified before it was marked accepted; the
specification was written and tested before this
acceptance status; no gate was changed to fit the implementation. M05 remains
recommended for a separate specification-planning task and is not authorized.
