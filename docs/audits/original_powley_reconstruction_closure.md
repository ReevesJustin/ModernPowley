# Original Powley Reconstruction Closure

Date: 2026-07-14

## Executive Finding

The repository cannot execute the complete original Powley method from documented
inputs through final powder selection and velocity output. It can reproduce the
source-backed input treatment, charge arithmetic, sectional density, mass ratio,
projectile travel, bore-volume arithmetic, and total expansion ratio. The retained
1961 manual directs the user to physical Arrow 2 and Expansion Ratio-Velocity
scales but does not reproduce their complete numeric geometry, tables, or a
generating equation. The later 1985 device photograph is not adequate for an exact
transcription. Original powder selection and velocity therefore remain unavailable.

The numbered 1961 instructions describe a working-pressure design range and print
isolated muzzle-pressure readings, not a complete chamber-pressure calculation.
The unnumbered pressure-calculator insert and the photographed later pressure
device lack sufficient primary instructions and scale data for implementation.
Pressure remains unavailable rather than being supplied from Davis, Howell,
Miller, or the archived emulator.

**Final reconstruction classification: `PARTIAL_RECONSTRUCTION`.**

## Scope And Source Hierarchy

This closure audit covers only `src/modern_powley/original/` and the original
inputs, intermediate values, and outputs described by `SRC-POWLEY-1961-MANUAL`.
The controlling source is the visually inspected PDF at
`reference/powley_manual/powleysmanuals1.pdf`, manual pp. 3-12 (PDF scan pages
4-9). Its OCR derivative is a navigation aid. `SRC-POWLEY-SLIDE-PHOTO` is a
photograph of a later 1985 revision and provides label-level corroboration only.
The archived emulator is secondary implementation evidence and never closes a
gap in the printed original method.

Davis, Howell, Miller, GRT, QuickLOAD, Kolbe, regressions, and ModernPowley
experiments are excluded. Implementation mechanics are limited to validation,
unit conversion, and direct arithmetic needed to express primary-source rules.

## Reconstruction Matrix

Status values in this table describe the current repository, not the historical
existence of the physical calculator.

| Historical element | Repository symbol or field | Definition and unit | Domain | Controlling location and evidence class | Code; test | Status |
|---|---|---|---|---|---|---|
| Case Capacity / powder space | `net_capacity_water_grains` | water weight filling the space available behind the seated bullet; gr H2O | finite, positive; seating-depth and case specific | manual pp. 3, 8-9; original primary | function input; `tests/unit/test_units_and_charge.py` | implemented and verified |
| Capacity measurement procedure | same | grooved intended bullet vents water while seated to intended depth; capacity obtained by weight difference | finite positive measured result | manual pp. 8-9 plus 1963 Hutton-Powley publisher republication; original primary content in derivative representation | documented in `docs/history/02_original_powley_method.md` | source-backed procedure at medium confidence; original issue facsimile still needed |
| Gross-to-net conversion | none | no original equation established | not applicable | no supporting original passage | explicitly absent; `EQ-006`, `EQ-007` | unresolved |
| Bullet diameter | `bullet_diameter_inches` | diameter used in SD; in | finite, positive | manual p. 9; original primary | `original.geometry.sectional_density`; unit tests | implemented and verified |
| Bullet weight | `bullet_weight_grains` | projectile weight; gr | finite, positive | manual p. 9; original primary | SD and MR inputs; unit/reference tests | implemented and verified |
| Sectional Density | `sectional_density` | `(Wb/7000)/d^2`; lb/in2 numerical convention | finite positive inputs | manual p. 9; original primary; `EQ-001` | `original/geometry.py`; `tests/unit/test_geometry.py` | implemented and verified |
| Charge weight | `charge_weight_grains` | powder mass; gr | finite, positive | manual pp. 3, 9-11; original primary | `original/charge.py`; unit/reference tests | implemented and verified |
| Density of loading | `loading_density` | powder grains / water grains filling powder space; ratio | 0.80 for IMR 4198/4227; 0.86 for other evidenced IMR powders | manual p. 3; original primary; `EQ-003`, `EQ-004` | `original/charge.py`; `tests/unit/test_units_and_charge.py` | implemented and verified |
| Initial charge | `charge_from_measured_powder_space` | `Wc=LD*V0`; gr | finite positive net capacity; evidenced IMR set only | manual p. 3 and p. 9; original primary | `original/charge.py`; unit/reference tests | implemented and verified |
| Charge-to-bullet ratio | `mass_ratio` | `Wc/Wb`; dimensionless | finite positive inputs | manual pp. 4-5, 9; original primary; `EQ-002` | `original/geometry.py`; unit/reference tests | implemented and verified |
| Barrel/travel input | `projectile_travel_inches` | initial seated bullet-base position to muzzle; in | finite positive component measurements | manual p. 9; original primary; `EQ-008` | `original/geometry.py`; reference test | implemented and verified |
| Seating-depth treatment | capacity and travel measurement | seating changes powder space; bullet-base position defines travel | no printed geometric conversion | manual pp. 8-9; original primary | documented only | source-backed but not a general calculation |
| Effective bore diameter | `effective_bore_diameter_inches` | `(dbore+dgroove)/2`; in | finite positive diameters | manual p. 9 special condition; original primary; `EQ-044` | `original/geometry.py`; unit test | implemented and verified |
| Bore area | implementation intermediate | `pi*(deff/2)^2`; in2 | finite positive effective diameter | manual pp. 5, 9; original primary; `EQ-031` | `original/geometry.py`; unit test | implemented and verified |
| Water-volume conversion | `WATER_GRAINS_PER_CUBIC_INCH_POWLEY` | `1 in3 = 253 gr H2O` | finite positive volume | manual p. 9; original primary; `EQ-005` | `original/units.py`; unit test | implemented and verified |
| Bore capacity | `barrel_volume_water_grains` | swept circular bore volume over travel, expressed as gr-water equivalent | finite positive diameter and travel | manual pp. 5, 9; original primary; `EQ-009` | `original/geometry.py`; unit test | implemented and verified |
| Barrel-volume ratio | `barrel_volume_ratio` | `Vb/V0`; dimensionless implementation name | finite positive volumes | derived component of manual p. 5 definition; `EQ-010` | `original/geometry.py`; unit test | implementation-only arithmetic |
| Expansion Ratio | `total_expansion_ratio` | `(V0+Vb)/V0`; dimensionless | finite positive volumes; historical text discusses roughly 4-12 | manual p. 5; original primary; `EQ-011` | `original/geometry.py`; unit/reference tests | implemented and verified |
| Powder-selection alignment | `select_powder` | align charge/bullet ratio and SD, then read Arrow 2 | initiating inputs positive; exact scale domain absent | manual pp. 4, 9-10; original primary; physical scale absent; `EQ-047` | explicit failure; provenance test | unresolved |
| Powder classification/bands | none in `original/` | powder number or letter from physical scale | exact boundaries absent | manual pp. 3-5, 9-10; photo corroboration only | emulator table exists only under `later/` | unresolved |
| Lettered powder corrections | none | F/D/B instructions include a 5% charge change after a scale reading | depends on unavailable Arrow 2 location | manual p. 10; original primary; `EQ-058`, `EQ-059` | documented only | source-backed but not executable |
| Small charge-change rule | none | local percent velocity/pressure heuristic | source restricts to small changes | manual p. 11; original primary; `EQ-057` | documented only | source-backed but intentionally not implemented |
| Expansion Ratio-Velocity lookup | `estimate_velocity` | read velocity at ER and MR | complete axes, cells, interpolation, and boundaries absent | manual pp. 5, 8-12; original primary references missing tables; `EQ-022` | explicit failure; provenance test | unresolved |
| Muzzle velocity output | none | graphical/table reading; ft/s | same missing lookup | manual pp. 5, 9-12; worked example gives one point | no executable result | unresolved |
| Working/max pressure | none | copper-crusher pressure discussed with printed `psi` wording | described operating region, not an output algorithm | manual pp. 4, 8; original primary | documented only | out of scope for the numbered load-computer calculation |
| Muzzle pressure | `estimate_pressure` (unavailable) | isolated estimates labeled psi | complete scale/interpolation absent | manual p. 6; original primary; `EQ-023` | explicit failure; provenance test | unresolved |
| Later Powley psi Calculator | none | separate pressure device/insert; historical crusher semantics unresolved | instructions, axes, and revision relation incomplete | unnumbered scan insert and 1985 photo | no implementation | unresolved and not silently treated as 1961 method |
| Rounding | call-site comparison tolerances | physical scale readings and printed decimal rounding | scale resolution not specified globally | manual examples, especially p. 9 | reference tests use source-justified tolerances | ambiguous beyond printed examples |

The manual's comment that an expansion ratio below about 4 is not a proper
condition for the computer is a historical applicability statement. It is not
enforced as a universal geometry-domain rejection because the retained source
does not supply complete boundary behavior for every operation.

## Bidirectional Traceability

### Source To Code

| Primary-source item | Ledger | Implementation or disposition | Test |
|---|---|---|---|
| SD arithmetic, p. 9 | `EQ-001` | `original.geometry.sectional_density` | `tests/unit/test_geometry.py` |
| charge/bullet ratio, pp. 4-5, 9 | `EQ-002` | `original.geometry.mass_ratio` | `tests/unit/test_geometry.py` |
| 0.86 and 0.80 loading rules, p. 3 | `EQ-003`, `EQ-004` | `original.charge` | unit and `.308` reference tests |
| 253 gr H2O/in3, p. 9 | `EQ-005` | `original.units` | `tests/unit/test_units_and_charge.py` |
| bullet-base travel, p. 9 | `EQ-008` | `original.geometry.projectile_travel_inches` | `.308` reference test |
| bore capacity and circular area, pp. 5, 9 | `EQ-009`, `EQ-031` | `original.geometry.barrel_volume_water_grains` | geometry unit tests |
| barrel/total volume relationship, p. 5 | `EQ-010`, `EQ-011` | distinct ratio functions | geometry unit/reference tests |
| average bore/groove special condition, p. 9 | `EQ-044` | `original.geometry.effective_bore_diameter_inches` | geometry unit test |
| Arrow 2 powder selection, pp. 4, 9-10 | `EQ-047` | `MissingProvenanceError` | missing-source and coverage tests |
| ER-V table reading, pp. 5, 8-12 | `EQ-022` | `MissingProvenanceError` | missing-source and coverage tests |
| incomplete pressure material, pp. 4, 6, 8 and insert | `EQ-023` | `MissingProvenanceError` | missing-source and coverage tests |
| contextual charge rules, pp. 10-11 | `EQ-057`-`EQ-059` | documented, not executable without scale context | ledger vocabulary/coverage review |

### Code To Source

Every public function under `src/modern_powley/original/` is enumerated in
`tests/provenance/test_original_coverage.py`. Its ledger mapping is checked for
an implementation path, source identifier, and test. Private `_positive` input
validators are implementation mechanics. `units.py` contains only the printed
7000 grains/lb convention embedded in SD and the printed 253 gr-water/in3
conversion. No scientific table is embedded in `original/`.

`tests/provenance/test_architecture.py` parses all original modules and rejects
imports from `later`, `experimental`, or GRT-specific modules. The original
fixtures depend only on literal primary worked-example inputs, not regression or
simulator data.

## Unit And Dimensional Findings

| Relation | Dimensional audit |
|---|---|
| `SD=(Wb/7000)/d^2` | grains divide by 7000 gr/lb, then by in2, producing the historical lb/in2 numerical convention. |
| `MR=Wc/Wb` | powder grains / bullet grains; dimensionless. Orientation is explicit. |
| `Wc=LD*V0` | powder-grain result uses the historical numerical ratio between powder grains and gr-water capacity; `LD` is not a material-density SI value. |
| `deff=(dbore+dgroove)/2` | inches remain inches. |
| `Vb=pi*(deff/2)^2*L*253` | in2 times in gives in3; multiplication by 253 gr-water/in3 gives gr-water. |
| `ER=(V0+Vb)/V0` | both volumes are represented in gr-water equivalents; ratio is dimensionless. |

No original code converts historical crusher readings to piezoelectric PSI or
generic CUP. The pressure output remains unavailable, which prevents a false
unit conversion from being hidden in a fitted constant.

## Tables, Scales, And Interpolation

No complete original numeric table is retained. Consequently there is no
source-backed original interpolation function, no defensible extrapolation
policy, and no original table whose corners or interior cells can be tested.
Exact Arrow 2 and ER-V input boundaries are rejected at the API level by making
the operations unavailable, rather than accepting an apparently plausible
domain.

`data/reference/original_powley_powder_scale.csv` is explicitly
`online_emulator` data. Davis Table 4 is later material. Neither is imported by
`original/`. Monotonicity and boundary tests for those later artifacts do not
verify an original physical scale.

## Worked-Example Reproduction

The controlling example is manual p. 9, `.308 Winchester`, 150 gr bullet,
51.5 gr-water seated powder space, 24 in nominal barrel. Printed scale readings
are retained as observations even when their algorithms are unavailable.

| Quantity | Inputs | Printed expected | Repository result | Absolute difference | Relative difference | Comparison basis |
|---|---|---:|---:|---:|---:|---|
| charge | `51.5`, IMR 4064 | 44.3 gr | 44.29 gr | -0.01 gr | -0.0226% | exact arithmetic, printed to 0.1 gr |
| mass ratio | `44.3/150` | 0.295 | 0.295333 | +0.000333 | +0.113% | exact arithmetic, printed to 0.001 |
| projectile travel | `21 5/16 + 1 1/16` | 22 3/8 in; text 22.4 | 22.375 in | 0 from fraction | 0% | exact fraction; printed decimal rounds |
| total expansion ratio | `V0=51.5`, bore `.300`, groove `.308`, travel `22.375` | 9.0 | 8.97836 | -0.02164 | -0.240% | geometric reproduction; physical scale/printed rounding |
| sectional density | 150 gr; exact diameter not printed in example | 0.227 | not asserted | not applicable | not applicable | cannot independently reproduce without supplying an unstated diameter |
| powder | SD 0.227, MR 0.295 | IMR 4064 | unavailable | not applicable | not applicable | original Arrow 2 scale absent |
| velocity | ER 9.0, MR 0.30 | 2730 ft/s | unavailable | not applicable | not applicable | original ER-V table absent |

The repository does not force the expansion ratio to 9.0; the small difference
is consistent with a physical scale reading and printed rounding. It also does
not choose a diameter merely to force SD to 0.227.

Manual pp. 10-11 contain further examples, but none supplies an independently
executable powder-selection and velocity path. Their source-backed initial
charge arithmetic compares as follows:

| Manual example | Direct inputs | Printed initial charge | Repository result | Absolute difference | Remaining unavailable reading |
|---|---|---:|---:|---:|---|
| 180 gr `.30-06`, D position | 61.5 gr-water, ordinary-powder 0.86 rule | 52.9 gr | 52.89 gr | -0.01 gr | D position and 2680 ft/s ER-V reading |
| 140 gr `.264 Winchester`, B position | 79 gr-water, ordinary-powder 0.86 rule | 68.0 gr | 67.94 gr | -0.06 gr | B position and 3080 ft/s ER-V reading |
| 139 gr 6.5 mm wildcat, IMR 5010 | 95 gr-water, ordinary-powder 0.86 rule | 81.7 gr | 81.70 gr | 0 gr | about 3220 ft/s ER-V reading |

The later 5% additions in the D and B examples are recorded as contextual
manual rules but are not general APIs. The Hutton extreme-condition narrative
begins with a 107 gr physical-scale result and therefore cannot independently
test the initial selection. Its reported chronograph value is a historical
observation, not a source table and not a validation dataset.

## Printed Method Versus Archived Emulator

Using the manual's already-read SD 0.227, MR 0.295, charge 44.3 gr, bullet
150 gr, and ER 9.0 as emulator inputs gives:

| Output | Manual observation | Archived emulator | Absolute difference | Relative difference | Classification |
|---|---:|---:|---:|---:|---|
| quickness/powder result | IMR 4064 | index 117.329; group `4320;4895;4064` | not comparable as scalar | not applicable | emulator corroborates group membership only |
| velocity | 2730 ft/s | 2696.792 ft/s | -33.208 ft/s | -1.216% | emulator-only equation differs from printed scale reading |

The emulator uses `20+12/(SD*sqrt(MR))`, approximate geometry constants, later
Davis-form velocity arithmetic, Miller-labeled pressure-factor arithmetic, and
Howell-labeled pressure arithmetic. The original scale does not establish those
equations. Matching one powder within a grouped band and approaching one
velocity reading do not establish identity.

## Architecture Findings And Corrections

- No `original/` module imports `later/`, `experimental/`, GRT parsers, or their
  data.
- No original reference fixture uses regression or simulator output.
- Each executable original scientific function has an equation-ledger entry and
  test; unresolved output functions fail explicitly.
- The closure audit required no scientific code change. Adding a later formula
  would reduce, not improve, historical fidelity.
- README's stale commit value for `pre_audit_agent_derived_prototype` was
  corrected to the unchanged tag target; history and the tag were not changed.

## Remaining Evidence Gaps

1. Flat, calibrated, high-resolution images of every face, slider, cursor,
   arrow, index mark, and scale for the relevant 1961 device revision.
2. The complete original Expansion Ratio-Velocity numeric tables, or a primary
   derivation specifying their axes, values, interpolation, rounding, and domain.
3. A primary source defining exact Arrow 2 powder boundaries and lettered
   positions for the 1961 revision.
4. A facsimile of the March 1963 Hutton-Powley article to independently verify
   the recovered seating-depth-specific capacity fixture wording.
5. Dated primary instructions and complete scale data for the separate Powley
   psi Calculator, plus its relationship to the numbered 1961 manual.
6. A primary definition distinguishing any maximum/chamber crusher quantity
   from the manual's muzzle-pressure scale and specifying the printed pressure
   unit semantics.

Until items 1-3 are recovered, the original load-and-velocity path cannot close.
Item 5 is additionally required before a later Powley pressure device can be
implemented under an accurately revisioned historical namespace.
