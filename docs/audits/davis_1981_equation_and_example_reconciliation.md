# Davis 1981 Equation And Example Reconciliation

Date: 2026-07-14

## Scope

This audit reconciles the repository's normalized Davis transcription, equation
and constant ledgers, `src/modern_powley/later/davis.py`, and retained worked
examples. It is not a visual reconciliation with the 1981 NRA book: physical
pages 138-144 are still unavailable in the repository.

No equation is moved into `src/modern_powley/original/`. Original Arrow 2,
graphical velocity, and psi Calculator operations remain partially recovered.
No Table 4 cell or confidence classification changes in this pass.

## Evidence Hierarchy

1. `SRC-DAVIS-1981` is the underlying later primary publication, but no local
   primary page images are retained.
2. `SRC-DAVIS-1981-DERIVATIVE-REPRINT` is a verified secondary derivative, not
   an NRA facsimile.
3. `SRC-DAVIS-1981-RAW-OCR` is intentionally uncorrected `ocr_only` navigation
   evidence. It cannot establish equation glyphs or table cells.
4. `SRC-DAVIS-1981-TRANSCRIPTION` is the normalized repository derivative.
5. `SRC-DAVIS-1981-TABLE4` is a medium-confidence normalized candidate table,
   pending retained-primary visual verification.

The available derivatives agree on the normalized scalar relations below.
Agreement between derivatives is corroboration, not primary visual verification.

## Equation Mapping

`p.N` below means the printed page marker in raw OCR, not a visually verified
page citation. “Reprint section” identifies text visible in the secondary PDF.

| Relation | Normalized form | Candidate evidence location | Normalized transcription | Implementation | Inputs -> output and units | Lookup dependency | Evidence / confidence | Result |
|---|---|---|---|---|---|---|---|---|
| seating depth | `S=C+B-L` | OCR p.140; reprint “Alternate method” | equation list | `seating_depth_inches` | in, in, in -> in | none | derivative agreement; medium | no defect |
| flat-base displacement | `P=198*S*D^2` | OCR p.140; reprint “Powder space” | equation list | `flat_base_displacement_water_grains` | in and in -> gr water | none | superscript normalized from derivative PDF; medium | no defect |
| boat-tail correction | `K=66*H*(2*D^2-D*J-J^2)` | OCR p.140 damaged; reprint equation | equation list | `boat_tail_correction_water_grains` | three lengths in -> gr water | none | derivative PDF supports normalized typography; medium | no defect |
| flat-base capacity | `W=F-P` | OCR p.140; reprint equation | equation list | `loaded_powder_space_capacity_water_grains` | gr water -> gr water | none | derivative agreement; medium | no defect |
| boat-tail capacity | `W=F-P+K` | OCR p.140; reprint equation | equation list | same function with explicit correction | gr water -> gr water | none | derivative agreement; medium | no defect |
| direct capacity fixture | filled assembled weight minus empty assembled weight | OCR p.139; reprint “Powder space” | prose only | no function; measured input | weights in gr -> gr water capacity | physical measurement | readable OCR and reprint; medium | source-backed procedure, appropriately not modeled |
| bullet travel | `T=E+S-C` | OCR p.140; reprint “Bullet travel” | equation list | `bullet_travel_inches` | in -> in | none | derivative agreement; medium | no defect |
| chamber volume | `U=W/252.4` | OCR p.140; reprint “Expansion ratio” | equation list | `powder_chamber_volume_cubic_inches` | gr water -> in3 | none | derivative agreement; medium | no defect |
| effective bore volume | `Q=0.773*T*D^2` | OCR p.140; reprint “Expansion ratio” | equation list | `effective_bore_volume_cubic_inches` | in and in -> in3 | none | derivative agreement; medium | no defect |
| expansion ratio | `R=(Q+U)/U` | OCR p.140; reprint “Expansion ratio” | equation list | `expansion_ratio` | in3 / in3 -> dimensionless | none | derivative agreement; medium | no defect |
| loading density | `LD=I/W` | OCR pp.141-142 context; reprint “Load Density” | equation list | no dedicated function; explicit input to scaling helpers | gr powder / gr water -> historical ratio | none | derivative agreement; medium | source-backed relation, not separately implemented |
| initial charge | `I=0.80*W` or `0.86*W` | OCR pp.141-142; reprint “Estimating the powder charge” | equation list | `initial_charge_weight_grains` | gr water -> gr powder | powder class/procedure | derivative agreement; medium | explicit powder API avoids inventing circular iteration |
| mass ratio | `A=I/G` | OCR p.142; reprint “Powder-selection Index” | equation list | `mass_ratio` | gr/gr -> dimensionless | none | derivative agreement; medium | no defect |
| sectional density | `Z=G/(7000*D^2)` | OCR p.142 damaged; reprint equation | equation list | `sectional_density` | gr and in -> lb/in2 convention | none | derivative PDF supports normalized superscript; medium | no defect |
| powder index | `X=20+12/(Z*sqrt(A))` | OCR p.142 radical absent; reprint equation | equation list | `powder_selection_index` | historical SD and ratio -> arbitrary index | none | derivative PDF supports normalized form; medium | no defect; Davis empirical relation, not Miller |
| Table 3 class | tabulated `X` intervals | OCR p.142; reprint Table 3 | history section | `matching_transcribed_bands` | index -> zero or more secondary bands | Table 3 | verified secondary; medium | stale `4427` note corrected to `4227`; endpoints unresolved |
| velocity fraction | `M=R^(-1/4)` | OCR p.142 damaged; reprint velocity section | equation list | `velocity_fraction_m` | dimensionless -> dimensionless | none | derivative PDF supports fourth root; medium | no defect |
| velocity fraction | `N=1-M` | OCR p.142; reprint velocity section | equation list | `velocity_fraction_n` | dimensionless -> dimensionless | none | derivative agreement; medium | no defect |
| moving weight | `Y=G+I/3` | OCR p.142; reprint velocity section | equation list | `effective_moving_weight_grains` | gr -> gr | none | derivative agreement; medium | no defect |
| muzzle velocity | `V=8000*sqrt(I*N/Y)` | OCR p.142 damaged; reprint velocity section | equation list | `muzzle_velocity_fps` | gr/gr under dimensioned coefficient -> ft/s | none | derivative PDF supports normalized form; medium | formula correct; `0<=N<1` enforced, with `N=0` producing zero velocity |
| pressure factor | `F2=f(A,R)` | OCR Table 4 severely damaged; reprint table legible | separate candidate CSV | `load_table4`, `lookup_table4_f2` | ratios -> dimensionless factor | Table 4 | pending primary visual verification; medium | values frozen; bounded lookup only |
| pressure term | `K1=0.0142*I*F2*V^2` | OCR p.144; reprint pressure section | equation list | `pressure_terms` | mixed -> pressure-times-capacity intermediate | Table 4 `F2` | derivative agreement; medium | no defect |
| pressure term | `K2=0.53*(G/I)+0.26` | OCR p.144; reprint pressure section | equation list | `pressure_terms` | dimensionless -> dimensionless | none | derivative agreement; medium | no defect |
| pressure term | `K3=W*(R-1)` | OCR p.144; reprint pressure section | equation list | `pressure_terms` | gr water -> gr water | none | derivative agreement; medium | no defect |
| pressure | `P=K1*K2/K3` | OCR p.144; reprint pressure section | equation list | `historical_crusher_pressure` | intermediates -> printed psi by copper crusher | explicit `F2` | derivative agreement; medium | no defect; not piezoelectric psi |
| LD pressure scaling | `P2=P1*(LD2/LD1)^2` | derivative reprint “Load Density”; normalized prior report | equation list | `loading_density_pressure_scale` | crusher pressure -> crusher pressure | none | secondary derivative; medium | approximate historical rule only |
| target-LD charge | `I2=W2*LDtarget` | derivative reprint “Load Density” | equation list | `charge_for_target_loading_density` | gr water -> gr powder | none | secondary derivative; medium | no defect |

Private `_finite`, `_positive`, `_nonnegative`, and `_bracket` functions are
implementation mechanics. They are not represented as Davis equations.

## Unit And Symbol Analysis

- Davis reuses `P` for flat-base displaced water and later for pressure. Python
  avoids the collision through descriptive names.
- `F` is gross water capacity to the mouth; `W` is net powder-chamber capacity
  beneath the seated bullet. They are not interchangeable.
- `S`, `B`, `C`, `D`, `E`, `H`, `J`, `L`, and `T` are inches. No feet conversion
  occurs in geometry.
- `E` is barrel length from bolt face; `T=E+S-C` is bullet-base travel to the
  muzzle. It is not barrel length minus cartridge overall length by itself.
- `D` is bullet diameter. Davis uses it in the approximate effective-bore
  relation; the method does not accept separate land and groove diameters.
- `252.4` carries `gr water/in3` at approximately 70 F. It converts `W` to `U`.
- `198` carries the effective conversion needed for `S*D^2` in cubic inches to
  grains of displaced water; numerically it approximates `252.4*pi/4`.
- `66` is likewise dimensioned for the boat-tail cubic geometry in inches to
  grains of water.
- `0.773` is the dimensionless effective-area coefficient multiplying `T*D^2`
  to obtain cubic inches; Davis describes an approximate rifling-land reduction.
- `7000 gr/lb` converts bullet grains to pounds before division by `D^2`, giving
  the historical `lb/in2` sectional-density convention.
- `8000` is a dimensioned historical velocity coefficient producing `ft/s` from
  the dimensionless square-root mass ratio.
- `0.0142` is not universal or dimensionless. It embeds the inch/grain/ft/s and
  historical crusher-pressure convention so that division by `K3` produces the
  printed pressure quantity.
- `A`, `LD`, `M`, `N`, `R`, `F2`, and `K2` are dimensionless numerical ratios or
  factors. Powder-grains/water-grains loading density is a historical numerical
  convention, not a unitless material-density identity outside this method.
- Davis prints pressure as `psi (copper crusher)`. Repository output is therefore
  named historical crusher pressure and is semantically CUP/crusher pressure,
  not modern piezoelectric PSI.

## Independent Worked Calculations

All independent results below were calculated with Python `Decimal` at 40-digit
precision in `tests/reference/test_davis_equation_reconciliation.py`. The
independent formulas do not call `later.davis`; implementation results are then
compared separately.

### `.30-06` Geometry And Velocity

Inputs: `C=2.484`, `F=69`, `B=1.220`, `H=.150`, `J=.200`, `D=.308`,
`G=180`, `L=3.30`, `E=24`.

| Value | Source printed | Independent full precision | Implementation | Absolute difference | Relative difference | Classification |
|---|---:|---:|---:|---:|---:|---|
| `S` | .404 | .404 | .404 | 0 | 0% | agreement |
| `P` | 7.59 | 7.588361088 | 7.588361088 | -0.001638912 | -0.021593% | source rounding |
| `K` | .87 | .872467200 | .872467200 | +0.002467200 | +0.283586% | source rounding |
| `W` | 62.3 | 62.284106112 | 62.284106112 | -0.015893888 | -0.025512% | source rounding |
| `T` | 21.9 | 21.920 | 21.920 | +0.020 | +0.091324% | source rounding |
| `U` | .247 | .2467674568621236 | same | -0.0002325431 | -0.094147% | source rounding |
| `Q` | 1.606 | 1.607390794240 | same | +0.00139079424 | +0.086600% | source rounding |
| `R` | 7.50 | 7.513787574259022 | same | +0.01378757426 | +0.183834% | source rounding |
| `I` | 53.6 | 53.56433125632 | same | -0.03566874368 | -0.066546% | source rounding |
| `A` | .298 | .2975796180906667 | same | -0.0004203819 | -0.141068% | source rounding |
| `Z` | .271 | .2710647423077850 | same | +0.0000647423 | +0.023890% | source rounding |
| `X` | 101 | 101.1533819107877 | same | +0.1533819108 | +0.151863% | source rounding |
| `M` | .604 | .6039976818671506 | same | -0.0000023181 | -0.000384% | source rounding |
| `N` | .396 | .3960023181328494 | same | +0.0000023181 | +0.000585% | source rounding |
| `Y` | 197.9 | 197.85477708544 | same | -0.04522291456 | -0.022851% | source rounding |
| `V` | 2620 ft/s | 2619.409657819862 | same | -0.5903421801 ft/s | -0.022532% | source rounding |

Relative differences are below 0.3% for every printed intermediate. The
implementation agrees with the independent full-precision chain to floating
point precision.

### `.30-06` Pressure

The pressure example deliberately uses printed rounded inputs `I=53.6`,
`F2=1.74`, `V=2620`, `G=180`, `W=62.3`, and `R=7.5`.

| Value | Source printed | Independent | Implementation | Absolute difference | Relative difference |
|---|---:|---:|---:|---:|---:|
| `K1` | 9,090,854 | 9,090,859.902720 | same | +5.902720 | +0.000065% |
| `K2` | 2.040 | 2.039850746269 | same | -0.0001492537 | -0.007316% |
| `K3` | 405 | 404.950 | same | -0.050 | -0.012346% |
| pressure | 45,790 crusher psi | 45,793.301288523 | same | +3.301289 | +0.007210% |

This is source rounding, not an implementation defect. If the full-precision
geometry/velocity chain and the repository's explicitly inferred bilinear Table
4 interpretation are used instead, `F2=1.742999553043` and pressure is
`45,762.314842476`. That is an implementation-analysis result, not a replacement
for Davis's printed rounded example.

### Secondary `.22-250` Geometry

The derivative flat-base calculations agree exactly:

```text
S=.204
P=2.026708992 gr water
W=42.573291008 gr water
```

The boat-tail chain also agrees through:

```text
S=.216
P=2.145927168 gr water
K=.076447800 gr water
W=42.530520632 gr water
```

The derivative then changes `W` to `42.377625032` without explanation. The
difference is `-0.152895600 gr water` (`-0.359496%`). Continuing from the computed
`42.530520632` gives:

```text
U=.168504439904913 in3
R=6.155761412828331
I=36.57624774352 gr
V=3566.636371708978 ft/s
```

Continuing from the derivative's substituted `42.377625032` reproduces its
downstream values, including `R=6.17436305069916`, `I=36.44475752752`, and
`V=3563.715167834366`. Classification: **derivative-source inconsistency**.
It is not attributed to the NRA publication.

The derivative also describes the charge as `35.4 gr` in narrative while using
`36.44475752752 gr` in equations, an absolute difference of `1.04475752752 gr`
or `2.951292%` relative to the narrative value. Classification: **derivative-source
inconsistency**.

### Secondary Loading-Density Example

For `57.5 gr` in capacities `65.3` and `62.0 gr water`:

```text
LD1=.8805513016845329
LD2=.9274193548387097
P2=55,464.22996878252 historical crusher units
I2=54.59418070444104 gr at the original numerical LD
```

These match the derivative's displayed arithmetic and the implementation within
the shown decimal precision (absolute and relative differences effectively zero).
Classification: **no equation defect; secondary example only**.

### Secondary `.22-250` Pressure

Using the derivative's literal inconsistent inputs and its stated `F2=1.432`
reproduces:

```text
K1=9,981,563.086983394
K2=1.059840689788878
K3=219.2772171419648
P=48,244.25831905143 crusher psi
```

The derivative prints `48,244.2583190515`; the independent absolute difference
is about `-0.00000000007`, with a relative difference below `2e-13%`.

The current candidate table with explicit bilinear interpolation at the
derivative coordinates gives `F2=1.432508973776197`, not `1.432` (absolute
`+0.000508974`, relative `+0.035543%`). Normal rounding
to three decimals would give `1.433`; the derivative does not document enough
precision to resolve its procedure. Classification: **derivative-source
rounding/interpolation ambiguity**, pending primary evidence. No Table 4 cell or
interpolation rule was changed.

## Implementation Audit

- Operator precedence and printed constants agree with the normalized forms.
- Public scientific inputs reject non-finite and nonpositive values where
  appropriate. Geometry rejects a boat-tail height exceeding seating depth and
  a tail diameter exceeding bullet diameter.
- `velocity_fraction_m` enforces `R>1`; `velocity_fraction_n` enforces `0<M<1`.
  `muzzle_velocity_fps` accepts the mathematically valid boundary `N=0` and
  rejects negative, non-finite, or `N>=1` inputs.
- Table 4 validates its exact 34-by-9 schema, coordinate grids, metadata, and
  finite positive values. It checks monotonic consistency but never repairs,
  smooths, or replaces a cell.
- Exact table nodes return the stored values. Interpolation is linear along `A`
  and then `R`; the result is bilinear. `R` interpolation is supported by the
  worked example, while `A` interpolation remains an explicit repository
  interpretation.
- Inputs outside `0.20<=A<=1.00` or `5.0<=R<=13.0` raise `ValueError`; there is
  no extrapolation.
- `historical_crusher_pressure` requires explicit `F2`; it does not silently
  invoke the medium-confidence table.
- Original modules import neither Davis code nor its data.

## Discrepancy Classification And Corrections

| Finding | Classification | Correction |
|---|---|---|
| runtime Table 3 text claimed a secondary `4427` transcription | documentation defect | changed label to `IMR-4227`, as visible in the retained secondary PDF; endpoint uncertainty retained |
| `muzzle_velocity_fps` accepted `N>=1` and rejected the valid `N=0` boundary | implementation defect | enforce `0<=N<1`; zero produces zero velocity |
| Table 3 lookup lacked equation-ledger mapping | provenance gap | added `EQ-090` using the derivative PDF as verified secondary evidence |
| `.30-06` printed/full-precision differences | source rounding | documented; no constants changed |
| `.22-250 W` discontinuity | derivative-source inconsistency | documented; implementation continues the stated formula and does not adopt substituted value |
| `.22-250 35.4/36.444...` conflict | derivative-source inconsistency | documented; not attributed to primary NRA pages |
| `.22-250 F2 1.432` versus bilinear 1.432509 | derivative-source rounding/interpolation ambiguity | documented; no Table 4 change |
| exact powder-selection typography and all Table 4 cells | unresolved pending primary evidence | no promotion or data change |

## Stopping Boundary

The normalized scalar equations are mutually consistent across the retained
derivatives and implementation, subject to unresolved primary typography. This
does not recover or verify original Powley graphical scales. Completion of a
primary Davis reconciliation still requires retained, legible images of NRA
pages 138-144, including every Table 3 and Table 4 cell, heading, footnote,
superscript, radical, and decimal point.
