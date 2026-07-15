# M05 Charge Region Records Design

Status: `implemented_and_reviewed`

This design was created while M05 was `in_progress`, before source
implementation, and remains the accepted implementation design.

## Modules And Public API

`charge_regions.py` owns enums, exact references, metadata, endpoints, segments,
and the top-level record. `m05_serialization.py` owns strict tagged dict/JSON
encoding. `modernized.__init__` exports only these public contracts and four
serialization entry points.

## Record Map

`ChargeRegionRecord` -> identity/version, state/basis/method, segments, role-
separated M01/M02/M03/M04/external references, provenance/source locator,
applicability/conditions/source wording/precision, uncertainty/dependency,
conflicts/qualifications/lineage, pressure contexts, lifecycle, and canonical
non-implication declaration.

## State Matrix

| State | Segments | Basis/method | Conflict refs | Explanation |
|---|---|---|---|---|
| bounded | one or more | required | prohibited | optional |
| empty | none | required | prohibited | required |
| unavailable | none | prohibited | prohibited | required |
| indeterminate | none | both absent or both present | prohibited | required |
| conflicting | none | prohibited | at least two unique | required |

Basis is caller-declared provenance and performs no operation. Empty requires a
basis/method because it represents a definite externally supplied analytical
result; unavailable does not.

## Segment Rules

Endpoints reuse M01 mass `Quantity`, retain source units/text/precision, and are
finite positive. Equal bounds require both included. Records require caller
ascending order; identical lower bounds, interior overlap, and a shared boundary
included by both segments fail. Touching segments are valid when at least one
side excludes the boundary. No sorting, merge, normalization, or arithmetic.

## References And Provenance

`ExactRecordReference` includes a controlled role, schema/type/record identity,
optional positive version, evidence class, and maturity. Role-specific record
fields prevent M04 audit references from becoming scientific inputs. Provenance
and `SourceLocator` are reused without ranking or resolution.

## Metadata

Reported precision is text separate from uncertainty. Uncertainty is a tagged
declaration, never a numeric propagation operation. Dependency is a four-value
status plus exact references. Pressure context is textual source metadata only,
with no M01 pressure quantity. Activation and exact prior region/version
supersession are independent.

## Serialization

`modern_powley.m05.v1` has one top-level `charge_region_record`. Every nested
object has exact keys and strict JSON types. JSON rejects duplicate object keys,
NaN/infinity, aliases, versions, unknown fields/types, and coercion. Output sorts
keys and preserves list order and supplied units.

## Tests And Exclusions

Synthetic `SYN-M05-*` fixtures cover immutability, states, units, point/touching/
disjoint segments, invalid bounds/order/overlap, references, lifecycle,
metadata, strict payloads, exports, architecture, and prior schemas. No real
data, region creation/transformation, estimator, intersection, uncertainty
propagation, pressure/velocity/burn behavior, plotting, GRT, web, or M06 code.
