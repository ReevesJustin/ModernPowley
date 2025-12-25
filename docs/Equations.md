# Dynamic Vivacity Modification to GRT/QuickLOAD Models

In Gordon's Reloading Tool (and QuickLOAD), the base vivacity Ba is modified by a loading-density dependent function to produce dynamic vivacity Ba(φ):

### Ba(φ) = Ba × (a0 + (1 – a0) × φ)

where:<br>
φ = burned fraction (0 at start, 1 at complete burn).<br>
a0 = the coefficient from the .propellant file ("Ba(phi) coefficient 0").

For most modern powders:<br>
a0 >1 → dynamic vivacity increases as burn progresses (progressive burning).<br>
For a0 <1, it decreases (degressive).

This captures deterrent coating effects and grain geometry changes, making burn rate, pressure, and density dependent in a simple way.

The full rate equation is:
dφ/dt = Ba(φ) × p^(α)  (where α ≈ 1 for most, built into Ba units)
But for selection purposes, we use average or effective vivacity over the useful burn (φ = 0 to z2).
Integrating Dynamic Vivacity into the Framework
To create a more accurate "effective burn rate index" for Powley-style selection:<br>

Effective Ba_eff = Ba × average(a0 + (1 – a0) × φ) over φ = 0 to z2

Approximate average factor (linear assumption over burn):

avg_factor = a0 + (1 – a0) × (z2 / 2)

Ba_eff = Ba × avg_factor

Higher Ba_eff = effectively faster overall burn (accounts for progressive
powders appearing "slower" early but accelerating).

## List of Equations and Formulas Discussed in the Framework

Below is a comprehensive list of all equations and formulas referenced throughout the development of the Algebraic Propellant Selection Framework, including descriptions and variable definitions.

**Charge Mass Prediction Equation:**<br>
charge_mass ≈ 0.71 × (eff_case_vol)^1.02 × (eff_barrel_length)^0.06 <br>

Description: Empirical power-law fit to predict optimal propellant charge weight in grains for high-density, balanced loads.
    Variables:

charge_mass: Propellant charge weight (grains)

eff_case_vol: Effective case volume (grains of H₂O, after bullet seating displacement)

eff_barrel_length: Effective barrel length (inches; barrel length minus cartridge OAL)

**Expansion Ratio (ER or X) Equation:**<br>
ER = 1 + (bore volume / effective case volume)<br>

Description: Classic internal ballistics expansion ratio; determines required propellant burn rate (higher ER needs faster powder).

Variables:
bore volume: π × (groove_dia/2)2 × eff_barrel_length × ~253 (gr H₂O)
effective case volume: Same as eff_case_vol above

**Relative Capacity (RC) Equation:**<br>
RC ≈ effective case volume / (bore capacity per inch in gr H₂O)<br>
Description: Powley-style proxy for expansion characteristics; higher RC favors faster propellants. Equivalent to "inches of bore filled by case capacity."

Variables:
effective case volume: As above
bore capacity per inch: Cross-sectional bore area converted to gr H₂O per linear inch (~253 × π × (groove_dia/2)2)

**Effective Burn Rate Index (Ba_eff) Equation:**<br>
Ba_eff = Ba × [a0 + (1 – a0) × (z2 / 2)]<br>
Description: Averages dynamic Ba(φ) over useful burn; physics: burn rate r=Ba P^n, with Arrhenius for Ea activation energy in combustion kinetics.<br>
Variables:
Ba_eff: Effective/dynamic vivacity (higher = effectively faster burn)<br>
Ba: Base vivacity coefficient from GRT model<br>
a0: Dynamic vivacity coefficient (Ba(phi) coefficient 0; >1 for progressive powders)<br>
z2: Upper burn-up limit (fraction of grain consumed at effective end of burn)

**Powley Quickness Approximation (Historical Reference) Equation:** <br>
Quickness ≈ 19 to 20 + 12 / (SD × MR^{0.5–0.6})<br>Description: Empirical proxy for burn speed; quickness ≈ 19 to 20 + 12 / (SD × MR^{0.5–0.6}); not directly physics-based; alternative: use ER or Ba_eff for ranking, per P V^γ=const in gas dynamics.

Provided for context/comparison.

Variables:
SD: Sectional density (bullet grains / caliber² × scaling factor)<br>
MR: Mass ratio (propellant charge / bullet weight)

**Sectional Density (SD) – Powley Scale**<br> 
Description: Approximate scaling to original Powley Y-axis (150–350 grains range).
Variables:
Often simplified as bullet weight in grains for trend analysis in this framework.


These equations form the core of the modernized framework:

Charge prediction (1)
Propellant matching via RC and Ba_eff (2–4)
Historical context (5)

All other references (e.g., velocity from adiabatic expansion, pressure ∝ velocity²) are qualitative or secondary and not formalized with specific constants in the current work.

Updated Table (Sorted by Vivacity Ba Descending: Faster → Slower)
| Propellant          | Ba (Vivacity) | Bulk Density (kg/m³) | Qex (kJ/kg) | k      | z1     | z2     | Notes / Calibrated For     |
|--------------------|---------------|----------------------|-------------|--------|--------|--------|----------------------------|
| Benchmark         | 0.688267      | 952                  | 3770        | 1.2398 | 0.4015 | 0.7984 | General/short-medium       |
| N140              | 0.657737      | 930                  | 3600        | 1.2306 | 0.4278 | 0.7901 | .223 75 ELDM               |
| Ramshot TAC       | 0.635197      | 1054                 | 3750        | 1.2602 | 0.4725 | 0.7564 | .223 data                  |
| IMR 4064          | 0.634434      | 871                  | 3790        | 1.2326 | 0.4094 | 0.8282 | .308 175 SMK               |
| IMR 3031          | 0.621245      | 875                  | 3790        | 1.2427 | 0.5047 | 0.8228 | .308 178                   |
| N135              | 0.613499      | 886                  | 3550        | 1.2499 | 0.5335 | 0.8388 | .223 75 ELDM               |
| AA 2495           | 0.605440      | 901                  | 3810        | 1.2502 | 0.3950 | 0.7000 | General                    |
| Varget            | 0.599450      | 914                  | 3950        | 1.2327 | 0.4431 | 0.7911 | Versatile medium           |
| N150              | 0.586051      | 890                  | 3790        | 1.2312 | 0.4697 | 0.8169 | "24"" 7-08"                |
| H4895             | 0.581043      | 918                  | 3850        | 1.2460 | 0.4695 | 0.8183 | General                    |
| N540              | 0.578052      | 955                  | 4000        | 1.2283 | 0.4882 | 0.8341 | General                    |
| IMR 4350          | 0.556900      | 930                  | 3650        | 1.2293 | 0.4762 | 0.7471 | General                    |
| Reloder TS 15.5   | 0.531264      | 890                  | 3900        | 1.2326 | 0.4868 | 0.7843 | .308 175 SMK               |
| Reloder 16        | 0.467522      | 903                  | 3860        | 1.2333 | 0.4777 | 0.8033 | 6.5 Creed                  |
| H4350             | 0.459287      | 944                  | 3900        | 1.2292 | 0.5175 | 0.8298 | 6.5 Creed 140 ELDM         |
| N555              | 0.447034      | 904                  | 3750        | 1.2261 | 0.5084 | 0.8311 | 6.5 Creed 140 ELDM         |
| H4831             | 0.439805      | 930                  | 3850        | 1.2383 | 0.5063 | 0.8091 | Classic magnum             |
| Reloder 22        | 0.412700      | 940                  | 3820        | 1.2321 | 0.5138 | 0.8327 | Magnum                     |
| H1000             | 0.370715      | 920                  | 3780        | 1.2395 | 0.6263 | 0.8544 | Extreme magnum             |
| Retumbo           | 0.346255      | 960                  | 3700        | 1.2562 | 0.6613 | 0.8577 | Magnum/extreme             |
| N565              | 0.321356      | 891                  | 4000        | 1.2393 | 0.5042 | 0.8211 | Large magnum               |
| N570              | 0.295283      | 930                  | 4000        | 1.2325 | 0.5059 | 0.7925 | Large magnum               |