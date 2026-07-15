# M02: Powder Property Records

## Status

M02 is implemented and reviewed. It defines evidence-preserving records only.
It does not assign powder suitability, compute powder behavior, or provide a
property value to a solver. M03 is the next active phase.

## Purpose

M02 records what a source says about a specifically identified powder or lot.
It preserves identity, terminology, source wording, conditions, domains,
uncertainty, missingness, and disagreement without merging or choosing records.

## Public Contract

- Powder identities retain manufacturer, source designation, display
  designation, family, lot/formulation/era qualifiers, and source provenance.
- Alias and relationship assertions are directional, separately sourced records.
- Property definitions use controlled identifiers and declare their value kind,
  meaning, dimensional expectation, and convention requirements.
- Numeric observations use M01 `PhysicalValue` when M01 recognizes the unit.
  Other reported numbers remain source scalars with literal units and no
  canonical conversion.
- Missing-property assertions use controlled semantic states; zero is a value.
- Applicability domains are either explicitly `unspecified` or declared through
  literal numeric bounds and categorical restrictions.
- Domain membership is a literal boundary check only. It does not interpolate,
  extrapolate, select, or rank.
- Multiple observations coexist. Comparison reports identity, definition, unit,
  domain, and numeric relationships without preference or resolution.
- Top-level serialization uses strict `modern_powley.m02.v1` records. Embedded
  M01 values retain their exact M01 quantity, provenance, and uncertainty shape.

## Property Vocabulary

The controlled vocabulary is representational, not computational. It keeps
bulk density, gravimetric density, heat of explosion, force, impetus, covolume,
specific-heat ratio, grain geometry, closed-bomb results, vivacity, burn-rate
coefficients, relative chart positions, composition categories, moisture,
temperature, publication indices, and source-specific coefficients distinct.
Supporting a category does not authorize any retained source or prototype value.

## Missingness

Supported states distinguish source omission, unpublished and unmeasured data,
inapplicability, unknown meaning, unresolved or illegible transcription,
conflict, outside-domain use, withholding, incomplete intake, unsupported
evidence, and intentional maturity limits. A missing assertion retains source,
locator, explanation, review context, resolvability, and related record IDs.

## Domains

Numeric bounds carry explicit inclusive, exclusive, or unbounded semantics and
M01 units. Categorical restrictions are literal allowed-value sets. An
unspecified domain is not unrestricted applicability. M02 never combines
domains from separate observations.

## Exclusions

M02 has no production powder database, alias inference, source preference,
automatic completion, screening, ranking, charge calculation, pressure or
velocity prediction, combustion law, energy calculation, interpolation,
extrapolation, regression, optimization, safety classification, recommendation,
CLI, notebook, or application interface.

## Acceptance Gates

M02 is complete only when identity, property-definition, provenance,
missingness, domain, conflict, serialization, dimensional, architecture,
evidence-restraint, documentation, and full-validation gates in the M02
completion review pass.
