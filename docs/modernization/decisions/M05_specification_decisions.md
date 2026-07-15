# M05 Specification Decisions

Status: `superseded_in_part`

These planning decisions still explain the evidence review. Decision 9's
planning status was superseded by the explicit records-only authorization in
`M05_records_only_authorization.md`; no numerical method was authorized.

## Decision 1: Region Shape

- **Question:** Can one record represent only one contiguous interval?
- **Alternatives considered:** one interval; one envelope around all values;
  multiple explicit segments.
- **Evidence:** M02/M03 preserve literal domains and partial comparability; an
  envelope would erase an unsupported gap.
- **Decision:** A future contract must support multiple disjoint segments and
  must not fill gaps.
- **Rationale:** Preserving topology avoids asserting unobserved interior values.
- **Consequences:** Serialization and tests must retain ordered endpoint-tagged
  segments.
- **Remaining uncertainty:** Normalization of overlapping same-source segments.
- **Roadmap effect:** Clarifies, without broadening, the M05 record concept.

## Decision 2: Non-Numeric Region States

- **Question:** How should empty, missing, conflicting, or unresolved results be
  represented?
- **Alternatives considered:** `None`; empty interval; tagged states.
- **Evidence:** M02/M03 require semantic missingness, conflicts, and
  indeterminate results.
- **Decision:** Use explicit future states for empty, unavailable,
  indeterminate, and conflicting regions.
- **Rationale:** None of these states is numerically equivalent.
- **Consequences:** No state becomes zero or an omitted bound.
- **Remaining uncertainty:** Exact implementation enum names.
- **Roadmap effect:** Narrows interpretation and preserves existing semantics.

## Decision 3: Open-Ended And Physical Bounds

- **Question:** Should an open-ended source constraint be a determinate charge
  region?
- **Alternatives considered:** allow infinite bound; insert default; retain as
  context/non-determinate state.
- **Evidence:** M01 rejects non-finite quantities and M05 cannot invent limits.
- **Decision:** Determinate segments require finite positive charge masses.
  Open-ended or missing bounds remain source constraints or non-determinate
  region states.
- **Rationale:** Infinity/defaults would fabricate an actionable-looking range.
- **Consequences:** Zero, negative, NaN, infinity, and reversed determinate
  bounds fail; point segments remain possible when explicitly sourced.
- **Remaining uncertainty:** Whether a later generic constraint type should
  serialize open bounds outside the region record.
- **Roadmap effect:** Narrows the future numerical contract.

## Decision 4: Basis Vocabulary

- **Question:** Which region bases need semantic separation?
- **Alternatives considered:** one free-form basis; the candidate categories;
  no basis vocabulary.
- **Evidence:** The review found source intervals, measurements, geometry/fill,
  uncertainty, intersections, and experimental estimates have different
  authority and non-implications.
- **Decision:** Adopt the controlled candidate vocabulary in the specification,
  with non-numeric unavailable/indeterminate/conflicting states.
- **Rationale:** A free-form label would permit semantic collapse.
- **Consequences:** Each basis requires exact method identity, provenance, and
  qualifications; schema capability does not admit evidence.
- **Remaining uncertainty:** Exact minimum fields for each basis.
- **Roadmap effect:** Clarifies the planned contract.

## Decision 5: Evidence Strength And Intersections

- **Question:** Does an intersection inherit the strongest input evidence?
- **Alternatives considered:** strongest wins; weakest evidence-class label;
  preserve all inputs without an automatic evidence ordering.
- **Evidence:** Evidence classes describe provenance and are not a total quality
  ordering.
- **Decision:** A derived intersection is a derived quantity, retains every
  material evidence class/maturity, and cannot claim admission beyond every
  material input. No automatic winner or class collapse is permitted.
- **Rationale:** Arithmetic does not improve provenance.
- **Consequences:** Promotion remains an explicit review decision.
- **Remaining uncertainty:** A future structured dependence record.
- **Roadmap effect:** Narrows authority claims.

## Decision 6: Uncertainty Is Not Permission

- **Question:** May a quantity uncertainty interval become a charge region?
- **Alternatives considered:** copy it; propagate automatically; retain it as a
  separate referenced uncertainty.
- **Evidence:** M01 supports bounded uncertainty but no probability or
  propagation policy; uncertainty and permissible values have different
  semantics.
- **Decision:** Uncertainty remains separate and never automatically becomes a
  charge region. No propagation arithmetic is authorized.
- **Rationale:** Measurement/model uncertainty does not grant permission to use
  every value in its bounds.
- **Consequences:** Dependencies and unknown correlations must remain explicit.
- **Remaining uncertainty:** Future propagation method and validation evidence.
- **Roadmap effect:** Narrows M05.

## Decision 7: Pressure Is Context, Not A Charge Rule

- **Question:** Can a published pressure number directly establish an M05 bound?
- **Alternatives considered:** compare numerically; convert CUP/PSI; retain exact
  contextual pressure evidence only.
- **Evidence:** Historical and modern pressure quantities/methods are not
  interchangeable, and no pressure model is admitted in M05.
- **Decision:** Retain exact pressure quantity, instrument/method, standard,
  units, conditions, and source limits as context only. No conversion, safety
  inference, or pressure-to-charge calculation is permitted.
- **Rationale:** A number without measurement semantics is not a comparable
  limit.
- **Consequences:** Pressure-based derivation remains blocked.
- **Remaining uncertainty:** Future authoritative cross-standard methods, if any.
- **Roadmap effect:** Narrows M05 and preserves M06 separation.

## Decision 8: M01-M04 References

- **Question:** Should M05 consume M04 passes or underlying records?
- **Alternatives considered:** M04 pass only; underlying M01/M02 only; underlying
  evidence plus exact M03 diagnostics and optional M04 audit references.
- **Evidence:** M04 explicitly says passes do not establish physical validity,
  safety, or suitability.
- **Decision:** Require exact underlying M01/M02 references and applicable M03
  diagnostics. Permit M04 references only as audit dependencies.
- **Rationale:** Policy outcomes cannot substitute for scientific inputs.
- **Consequences:** No prior logic is duplicated or weakened.
- **Remaining uncertainty:** Minimum diagnostic set for each future method.
- **Roadmap effect:** Clarifies dependency direction.

## Decision 9: First Implementation Boundary (Superseded In Part)

- **Question:** Does this planning pass authorize a serializer or arithmetic?
- **Alternatives considered:** implement immediately; authorize records plus
  intersection; remain planned.
- **Evidence:** No admitted production method/dataset exists, and governance
  requires a separate explicit authorization.
- **Decision:** At this planning commit M05 remained `planned`. The later user
  authorization at `M05_records_only_authorization.md` now authorizes only the
  records/structural-validation/serialization boundary.
- **Rationale:** The data contract can be reviewed independently of a derivation
  method.
- **Consequences:** This decision record itself created no schema or code. The
  authorization amendment permits those record-contract artifacts only in a
  later implementation commit and continues to prohibit numerical derivation.
- **Remaining uncertainty:** Whether the user will authorize a records-only
  increment and which unresolved segment policies must be settled first.
- **Roadmap effect:** Narrows the next possible step; does not authorize it.
