# Original Powley Reconstruction Completion Audit

Date: 2026-07-14

## Executive Finding

The retained 1961 manual supports a coherent arithmetic subset: loading-density
charge estimates, charge-to-bullet ratio, sectional density, measured
bullet-base travel, effective bore diameter, swept bore capacity, and total
expansion ratio. Every executable scientific function in
`src/modern_powley/original/` maps to that evidence or to algebra needed to
express it, and the namespace contains no Davis, Howell, Miller, emulator,
simulation, regression, or experimental behavior.

The historical calculator is not functionally complete. The scan does not
contain the Arrow 2 scale geometry or the reverse Expansion Ratio-Velocity
surface. It also provides isolated muzzle-pressure readings without the complete
surface or interpolation rules. Consequently powder selection, velocity, and
muzzle pressure cannot execute. Their `MissingProvenanceError` failures are the
correct current behavior, but they prevent freezing the namespace as a complete
canonical historical Powley baseline.

**Freeze recommendation: `not_ready_to_freeze`.**

The two scopes are distinct:

- `scalar_arithmetic_core`: source-backed, tested, isolated, and reproducible
  relative to the retained evidence.
- `complete_historical_method`: `not_ready_to_freeze` because required physical
  graphical scales and their reading procedures are unavailable.

This is a provenance-completeness decision, not a judgment about predictive
accuracy and not a loading recommendation.

## Scope And Source Hierarchy

The controlling evidence is the visually inspected 1961 manual scan. The OCR is
only a navigation derivative. The 1985 computer photographs establish label
topology but neither exact coordinates nor identity with the 1961 revision. The
archived emulator is a later implementation witness and supplies no original
primary authority. Davis and other later methods are excluded.

| Evidence | Path or identifier | Classification | Relevant content | Hash / access result | Confidence and limitation |
|---|---|---|---|---|---|
| 1961 instruction manual | `reference/powley_manual/powleysmanuals1.pdf` | original primary scan | manual pp. 3-12; definitions, arithmetic, examples, scale instructions | `119bc2c3cf4b798e7bf4ee1cb59b69a1643673875ad6556ee573912e1973ed66`; matched ledger | high; physical calculator faces absent |
| Manual transcription | `reference/powley_manual/powleysmanuals1.md` | OCR secondary derivative | searchable text for all nine scan pages | `021e1896b199428874c20ecb2a5464894fa5a275f049e1ac05d6e5e9eaf7fa16`; matched ledger | low; merged pages and damaged glyphs |
| Compressed device photograph | `image/classiccardboard_3.jpg` | primary artifact of later device | 1985 computer and 1965 psi Calculator | `a20c32c606861535dc86b464fc71742a9316ac8f6e39c16e16f9177a258ee338`; matched ledger | medium; oblique and compressed |
| Higher-quality photograph | `reference/powley_scales/ssusa_powley_computers_1985.jpg` | primary artifact of later device | Arrow 2 labels and visible topology | `20ecd81b6f38331d3e2cef6696aa4b3c9f9dba061b68847dedaeb555e26178f0`; matched ledger | medium; reverse face absent and revision equivalence unproved |
| Velocity observations | `data/reference/original_powley_velocity_observations.csv` | normalized derivative of scan | seven printed graphical readings | `19a2d63824a00ecdf415c4bcc88fcda0c0a4440175de0a777bf18c467092730c`; matched ledger | high transcription confidence; not a surface |
| Hutton-Powley 1963 republication | `SRC-HUTTON-POWLEY-1963-WEB` | publisher secondary derivative | seated-bullet capacity fixture and incomplete pressure sequence | no local bytes or hash | medium; original article/table absent |
| Archived emulator | `reference/online_emulator/kwk_powley_20240228.html` | secondary implementation | later equations, lookup bands, rounding | `0162ee7722dfd4bf586120590e7a7fcd4d72c908e9d17b6f335822dcac990e03`; matched ledger | high for emulator behavior only |
| Emulator powder bands | `data/reference/original_powley_powder_scale.csv` | emulator-derived transcription | exact emulator branches | covered as `SRC-KWK-EMULATOR` | not original scale evidence despite legacy filename |

The page map covers all numbered manual pages 3-12 and both later inserts. This
audit visually rechecked scan pages 4-9. A visible source inconsistency is now
explicit: manual p. 3 appears to print `4427`, while p. 4 prints the actual IMR
designation `4227`. The normalized implementation uses `4227`; this is supported
by the same primary scan and is not an OCR-only repair. Without stronger source
evidence, this is classified as an internal primary-source printing or
legibility inconsistency rather than definitively as a typographical error.

Repository records inspected for bidirectional traceability were
`reference/source_ledger.csv`, `docs/provenance/equation_ledger.csv`,
`docs/provenance/constant_ledger.csv`,
`docs/provenance/data_field_ledger.csv`, and
`docs/provenance/legacy_artifact_manifest.csv`. Legacy generated artifacts are
preserved for auditability but are not source evidence for `original/`.

## Reconstruction And Gap Matrix

“Implemented” means executable source-backed arithmetic, not that the complete
historical workflow is available.

| Historical element | Source location | Transcribed | Ledgered | Implemented | Tested | Confidence | Status | Blocker |
|---|---|---:|---:|---:|---:|---|---|---|
| Powder-space capacity definition | manual pp. 3, 8-9 | yes | fields and `EQ-006` disposition | input only | yes | high | complete as measured input | detailed fixture not printed in 1961 manual |
| Direct seated-bullet capacity fixture | Hutton-Powley 1963 web derivative | yes | source ledger | no; physical measurement | documentation test | medium | documented but unimplemented | original article facsimile absent |
| Generic gross-minus-intrusion capacity | no original support | yes as rejected history | `EQ-006`, `EQ-007` | intentionally absent | provenance test | high | outside retained original evidence | must not be inferred |
| Seating-depth equation | none in 1961 manual | no original equation | rejected by `EQ-006`, `EQ-007` | absent | namespace test | high | outside original scope | later Davis/emulator geometry only |
| Flat-base/boat-tail correction | none in 1961 manual | no | later Davis only | absent | namespace test | high | outside original scope | later evidence only |
| Loading density definition | manual p. 3 | yes | `EQ-003`, `EQ-004` | `loading_density` | yes | high | complete | limited to evidenced 1961 IMR set |
| Standard IMR charge | manual pp. 3, 9 | yes | `EQ-003` | `charge_from_measured_powder_space` | yes | high | complete | requires measured net capacity |
| 4198/4227 charge | manual p. 3 | yes | `EQ-004` | same function | yes | high | complete | p. 3 `4427` normalized from p. 4 `4227` |
| Charge-to-bullet ratio | manual pp. 4-5, 9 | yes | `EQ-002` | `mass_ratio` | yes | high | complete | none |
| Sectional density | manual p. 9 | yes | `EQ-001`; `CONST-001` | `sectional_density` | yes | high | complete | printed example diameter not specified exactly |
| Projectile travel | manual p. 9 | yes | `EQ-008` | `projectile_travel_inches` | yes | high | complete | cleaning-rod measurements required |
| Effective bore diameter | manual p. 9 | yes | `EQ-044` | `effective_bore_diameter_inches` | yes | high | complete special-condition rule | source does not impose modern land/groove validation |
| Bore area/capacity | manual pp. 5, 9 | yes | `EQ-009`, `EQ-031`; `CONST-002` | `barrel_volume_water_grains` | yes | medium-high | complete arithmetic representation | physical caliber slide values not retained |
| Barrel-volume ratio helper | algebraic component of manual p. 5 ER | yes | `EQ-010` | `barrel_volume_ratio` | yes | high | equivalent implementation detail | not a separately named historical output |
| Total expansion ratio | manual p. 5 | yes | `EQ-011` | `total_expansion_ratio`; dimensions helper | yes | high | complete | source applicability discussion is not a universal API bound |
| Arrow 1 charge reading | manual pp. 3, 9-10 | procedural | charge rules ledgered | arithmetic replacement only where density is known | examples | medium | partially implemented | exact physical scale and rounding absent |
| Arrow 2 powder selection | manual pp. 4, 9-10; later photo topology | yes | `EQ-047` | explicit failure | yes | high that evidence is missing | blocked by illegible/missing source | 1961 geometry and boundaries absent |
| Dividing-line rule | manual pp. 9-10 | yes | `EQ-059` | no | ledger/provenance | high | documented but unimplemented | requires unavailable Arrow 2 boundary |
| Lettered F/D/B procedures | manual p. 10 | yes | `EQ-058` | no | ledger/provenance | high | documented but unimplemented | initiating scale location unavailable |
| A/G off-scale procedures | manual pp. 10-11 | yes | procedural documentation | no | audit documentation | high | documented but unimplemented | no computable scale input |
| Small charge-change heuristic | manual p. 11 | yes | `EQ-057` | no | ledger/provenance | high | documented but unimplemented | contextual heuristic, not required baseline equation |
| Ballistic-efficiency definition | manual pp. 4-5 | yes | `EQ-060` | no | ledger/provenance | medium | documented but unimplemented | contextual output, not core calculator path |
| ER-V graphical readings | manual pp. 5, 9-12 | seven points | fields and observation CSV | explicit failure | yes | high for points | partially recovered | reverse table/scale face absent |
| Velocity interpolation/domain | referenced but not printed | no | `EQ-022` | explicit failure | yes | high that evidence is absent | blocked by missing source | axes, cells, rounding and boundaries absent |
| 1961 muzzle-pressure readings | manual p. 6 | prose values | `EQ-023` | explicit failure | yes | medium-high | partially recovered | numeric surface and interpolation absent |
| Good-working/maximum pressure discussion | manual pp. 4, 8 | yes | documentation | no output algorithm | audit documentation | high | descriptive only | no calculation is printed |
| Separate Powley psi Calculator | later insert, 1963 derivative, 1965 photo | partial | `EQ-091` | absent | provenance test | medium | outside numbered 1961 baseline; unresolved | source table, instructions, geometry and unit definition absent |
| Barrel-length change procedure | manual p. 12 | yes | ER and velocity dispositions | ER recomputation only | arithmetic tests | high | partially implemented | final rereading requires absent ER-V surface |
| .308 primary example | manual p. 9 | yes | equation/source ledgers | supported arithmetic only | reference tests | high | partially reproducible | powder and velocity remain graphical readings |
| D/B/A examples | manual pp. 10-11 | yes | `EQ-058` and observation data | initial charges only | reference tests | high | partially reproducible | lettered selection and velocity face absent |

## Source-To-Code Traceability

The executable source-backed relations map as follows:

| Source rule | Ledger | Implementation | Test |
|---|---|---|---|
| `SD=(Wb/7000)/d^2` | `EQ-001`, `CONST-001` | `sectional_density` | `tests/unit/test_geometry.py`; completion reconciliation |
| `MR=Wc/Wb` | `EQ-002` | `mass_ratio` | same |
| `Wc=0.86*V0` | `EQ-003`, `CONST-004` | `loading_density`; `charge_from_measured_powder_space` | charge and reference tests |
| `Wc=0.80*V0` | `EQ-004`, `CONST-003` | same | charge and completion tests |
| `1 in3=253 gr H2O` | `EQ-005`, `CONST-002` | `cubic_inches_to_water_grains` | unit and completion tests |
| bullet-base travel | `EQ-008` | `projectile_travel_inches` | primary example and completion tests |
| circular bore capacity | `EQ-009`, `EQ-031` | `barrel_volume_water_grains` | geometry and completion tests |
| `deff=(dbore+dgroove)/2` | `EQ-044` | `effective_bore_diameter_inches` | geometry and completion tests |
| `ER=(V0+Vb)/V0` | `EQ-010`, `EQ-011` | both ratio helpers | geometry and completion tests |
| Arrow 2 | `EQ-047` | `select_powder` raises | missing-source tests |
| ER-V operation | `EQ-022` | `estimate_velocity` raises | missing-source tests |
| 1961 muzzle pressure | `EQ-023` | `estimate_pressure` raises | missing-source tests |

The source-backed `EQ-057` through `EQ-060` relations are documented rather
than executed. They either depend on an unavailable scale location or are
contextual heuristics/definitions outside the minimum input-to-powder-and-
velocity path.

## Code-To-Source Review

Every public function under `src/modern_powley/original/` is reviewed here.

| Public function | Inputs / return | Validation and endpoint behavior | Provenance result |
|---|---|---|---|
| `cubic_inches_to_water_grains` | in3 -> gr water | float-coercible, finite, `>0`; zero rejected as a required physical input | source-backed conversion |
| `loading_density` | evidenced powder name -> historical ratio | normalizes case/hyphen/space; rejects powders outside retained 1961 set | source-backed decision rule; no modern substitution |
| `charge_from_measured_powder_space` | positive gr water plus powder -> gr powder | positive finite capacity; delegates powder-domain check | source-backed arithmetic |
| `sectional_density` | positive gr and in -> historical lb/in2 numeric convention | both finite and `>0` | source-backed arithmetic |
| `mass_ratio` | positive gr/gr -> ratio | both finite and `>0` | source-backed orientation |
| `effective_bore_diameter_inches` | bore/groove in -> in | both finite and `>0`; no unsupported ordering restriction | source-backed special-condition approximation |
| `projectile_travel_inches` | muzzle-to-tip plus bullet length -> in | both components finite and `>0` | source-backed measurement sequence |
| `barrel_volume_water_grains` | effective diameter and travel -> gr water | finite and `>0`; uses `pi` and printed 253 conversion | source-backed geometry |
| `barrel_volume_ratio` | two positive gr-water volumes -> ratio | finite and `>0`; no interpolation | algebraic implementation helper |
| `total_expansion_ratio` | two positive gr-water volumes -> ER | finite and `>0`; result necessarily `>1` | source-backed definition |
| `total_expansion_ratio_from_dimensions` | net capacity, bore/groove and travel -> ER | component validation; no hidden nominal barrel subtraction | source-backed composition |
| `select_powder` | unavailable | always raises `MissingProvenanceError` | correct unresolved disposition |
| `estimate_velocity` | unavailable | always raises `MissingProvenanceError` | correct unresolved disposition |
| `estimate_pressure` | unavailable 1961 muzzle-pressure surface | always raises `MissingProvenanceError` | correct unresolved disposition; separate psi Calculator excluded |

Private finite/positive validation and function composition are implementation
mechanics, not historical equations. Accepting float-coercible numeric inputs is
a repository API behavior. The positive restrictions enforce the mathematical
denominators and the physical meaning of required capacity, mass, diameter, and
travel inputs; they are not claimed as printed manual boundary rules.

## Unit And Dimensional Audit

| Quantity or constant | Classification | Dimensional finding |
|---|---|---|
| `7000 gr/lb` | unit conversion | converts bullet grains to pounds before division by diameter squared |
| `253 gr H2O/in3` | historical unit conversion | converts swept cubic inches to a water-grain volume equivalent; source precision retained |
| `0.80`, `0.86` | empirical historical numerical loading-density ratios | powder grains divided by water grains filling powder space; not modern bulk density |
| `pi/4` in bore area | dimensionless geometry | effective diameter squared produces in2 |
| powder-space capacity | measured gr water | seating-depth-specific net space, not gross overflow capacity |
| bullet/charge mass | grains | their ratio is dimensionless; sectional density alone converts bullet grains to pounds |
| bore and travel | inches | area times travel gives in3 before conversion to gr water |
| expansion ratio | dimensionless | numerator and denominator use the same gr-water volume representation |
| velocity | ft/s | only printed graphical observations are retained; no dimensioned equation constant exists in `original/` |
| pressure | historical printed `psi` wording | manual states copper-crusher measurement context; no conversion to piezoelectric PSI or generic CUP is implemented |

The original namespace contains none of the later Davis constants `252.4`,
`0.773`, `8000`, or `0.0142`.

## Independent Worked-Example Reconciliation

Independent arithmetic uses the printed formulas and Python/decimal arithmetic,
not calls to the original implementation. Implementation results are compared
afterward.

### Manual Page 9 `.308 Winchester`

| Quantity | Printed | Independent | Implementation | Absolute difference from print | Relative difference | Classification |
|---|---:|---:|---:|---:|---:|---|
| initial charge | 44.3 gr | `51.5*0.86=44.29` | 44.29 | -0.01 gr | -0.0226% | source rounding |
| mass ratio | 0.295 | `44.3/150=0.2953333333` | same | +0.0003333333 | +0.1130% | source rounding |
| travel | 22.4 in | `21 5/16 + 1 1/16=22.375` | 22.375 | -0.025 in | -0.1116% | source rounding |
| expansion ratio | 9.0 | `1+pi*(.304/2)^2*22.375*253/51.5=8.9783555181` | same | -0.0216444819 | -0.2405% | source/scale rounding and explicit nominal diameter check |
| powder | IMR 4064 | not independently computable | unavailable | not applicable | not applicable | unresolved source geometry |
| velocity | 2730 ft/s | not independently computable | unavailable | not applicable | not applicable | unresolved source surface |

The printed SD `0.227` is a table reading. The manual says “.30 caliber” but
does not print the exact bullet diameter used for that value, so the audit does
not reverse-engineer it.

### Lettered And Extreme Examples

| Manual location | Printed initial charge | Independent initial charge | Implementation | Difference | Remaining graphical dependency |
|---|---:|---:|---:|---:|---|
| p. 10 D example, `V0=61.5` | 52.9 gr | 52.89 | 52.89 | -0.01 gr (-0.0189%) | D selection, 5% procedure and 2680 ft/s reading |
| p. 10 B example, `V0=79` | 68.0 gr | 67.94 | 67.94 | -0.06 gr (-0.0882%) | B selection, 5% procedure and about 3080 ft/s reading |
| p. 11 A/5010 example, `V0=95` | 81.7 gr | 81.70 | 81.70 | exact | A selection and about 3220 ft/s reading |

These examples constrain the absent scales but do not reconstruct them. The
other velocity observations are likewise preserved as non-executable points.

## Printed Method Versus Emulator

For the p. 9 example, the emulator returns a grouped powder band containing
4064 and approximately `2696.792 ft/s`, while the manual reads one `IMR 4064`
position and `2730 ft/s`. The velocity difference is `-33.208 ft/s` (`-1.216%`).
The emulator uses the later Davis-form powder index and velocity relation plus
its own branches and rounding. Agreement near one observation is corroboration
only and is not imported into `original/`.

## Architecture And Contamination Findings

- AST architecture tests reject imports from `later`, `experimental`, and GRT
  modules.
- Original source files contain no Davis Table 3/Table 4 data, Davis constants,
  Howell/Miller arithmetic, simulator fields, regressions, vivacity, `Ba`, or
  modern powder mappings.
- Original tests use literal manual inputs. Emulator comparisons import the
  emulator explicitly and label its results separately.
- No gross-capacity-minus-geometric-intrusion helper exists in `original/`.
- The pressure placeholder now names only the unavailable 1961 muzzle-pressure
  surface. `EQ-091` separately records the later Powley psi Calculator gap.

No scientific implementation defect or later-material contamination was found.

## Freeze Readiness

For this repository, “freeze” would mean declaring the listed Python modules,
their source-backed data, ledgers, and reference fixtures the versioned
canonical executable representation of the historical calculator. A frozen
baseline could receive implementation-only maintenance without silently changing
historical outputs; new historical evidence would require a reviewed baseline
amendment and versioned provenance change.

The candidate baseline files are:

```text
src/modern_powley/original/*.py
reference/powley_manual/powleysmanuals1.pdf
reference/powley_manual/powleysmanuals1.md
data/reference/original_powley_velocity_observations.csv
docs/history/01_original_powley_sources.md
docs/history/02_original_powley_method.md
docs/history/original_manual_page_map.md
docs/history/original_powley_worked_example.md
docs/provenance/equation_ledger.csv
docs/provenance/constant_ledger.csv
docs/provenance/data_field_ledger.csv
tests/unit/test_geometry.py
tests/unit/test_units_and_charge.py
tests/reference/test_powley_1961_example.py
tests/reference/test_original_completion_reconciliation.py
tests/provenance/test_original_coverage.py
tests/provenance/test_original_completion_audit.py
```

They are complete only for the retained arithmetic subset. They are not complete
for the historical method's required powder and velocity outputs. Therefore the
namespace is isolated and internally auditable but **not ready to freeze as the
canonical complete baseline**.

Required evidence before reconsidering the decision:

1. Flat, calibrated images of both faces and every movable element of the
   relevant 1961 device revision.
2. Complete Arrow 2 boundaries, letter positions, direction, tie behavior, and
   revision identity.
3. The reverse Expansion Ratio-Velocity surface or primary numeric tables,
   including domains, interpolation and reading precision.
4. For 1961 muzzle-pressure execution, its complete surface and reading rules.
5. Separately, for the later psi Calculator, original instructions, missing
   table/worksheet, scale geometry, revision date, and pressure-unit definition.

Until items 1-3 are retained and audited, `select_powder` and
`estimate_velocity` must continue to fail. `estimate_pressure` must also fail
unless the 1961 muzzle-pressure surface is independently recovered. Future bulk
density, newer-powder quickness, or double-base hypotheses belong exclusively
under `experimental/` and cannot amend this historical baseline.
