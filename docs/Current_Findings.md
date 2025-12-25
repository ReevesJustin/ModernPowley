# Current Findings: Validation and Refinement of the Algebraic Propellant Selection Framework

## Executive Summary
Analysis of 9 verified high-performance loads combined with 22 calibrated GRT propellant models confirms that a modernized Powley-style algebraic framework can reliably predict both optimal charge weight and propellant selection.
Charge mass prediction remains highly accurate (R² > 0.998, typical error < 1 grain) using the near-linear relationship with effective case volume and weak dependence on effective barrel length (per empirical fit, but rooted in expansion ratio ER = 1 + (bore vol / case vol) and P-V conservation via ideal gas law PV=nRT). Note: Effective barrel length is critical. Barrel length is partially responsible for selecting a propellant that is consumed before projectile muzzle exit. This is a built-in bias, in that the existing example loads were selected to fit this criterion.
Incorporation of dynamic burn rate index Ba_eff (averaged over φ=0 to z2, accounting for progressive burning a0>1; physics: r=Ba P^n, with Arrhenius k=A e^{-Ea/RT} for kinetics) from calibrated geometric burn models significantly improves propellant ranking over raw Ba or closed-bomb charts.
The original optimal propellants in the dataset fall within tight, well-populated bands on a Relative Capacity vs. Sectional Density plot, with multiple commercial alternatives available for most loads.
Gaps exist only at the extreme fast end (> Benchmark) and extreme slow end (< N570), correctly flagging cases where no ideal commercial powder exists. Note: Faster propellant models are available (e.g., VV N130, N133), but they have not yet been incorporated.
## Methods

### Data Sources
* 9 empirical optimal loads (high load density ≥ 97%, complete burnout, modern precision/ELR cartridges).
* 22 GRT-derived propellant models providing Ba, a0 (dynamic vivacity coefficient), z1/z2, bulk density, Qex, and k.

![Propellant Mass Histogram](https://github.com/ReevesJustin/ModernPowley/blob/main/plots/propellant_mass_hist.png)

### Key Calculations

Effective vivacity
`Ba_eff = Ba × [a0 + (1 – a0) × (z2 / 2)]`
(linear average of dynamic vivacity over useful burn fraction)
Relative Capacity (RC)
`RC ≈ effective case volume (gr H₂O) / bore capacity per inch (gr H₂O/in)`
Higher RC favors faster propellants.
Plot coordinates
* X-axis: Relative Capacity
* Y-axis: Approximate Powley SD scale (bullet weight in grains)

![Expansion Ratios](https://github.com/ReevesJustin/ModernPowley/blob/main/plots/expansion_ratios.png)

![Velocity vs Barrel Length](https://github.com/ReevesJustin/ModernPowley/blob/main/plots/velocity_vs_barrel.png)

## Results

### Charge Weight Prediction
The previously derived equation
`charge_mass ≈ 0.71 × (eff_case_vol)1.02 × (eff_barrel_length)0.06`
continues to predict actual charges within ±1.3 grains across the full range (17–88 gr), including the large-volume 300 Norma Magnum.

![Predicted vs Actual Charges](https://github.com/ReevesJustin/ModernPowley/blob/main/plots/predicted_vs_actual.png)

### Propellant Selection Accuracy
When original loads are plotted on an RC vs. SD graph and overlaid with Ba_eff-ranked bands:

![RC vs SD Plot](https://github.com/ReevesJustin/ModernPowley/blob/main/plots/rc_sd_modern.png)

![RC vs Bullet Weight Plot](https://github.com/ReevesJustin/ModernPowley/blob/main/plots/rc_bulletweight_modern.png)

* All 8 precision/ELR loads (excluding .300 Blackout outlier) cluster in the medium-slow band (Ba_eff 0.55–0.70).
* Actual propellants used (RL16, N555, IMR4064, N135, estimated N160, N570) fall centrally within their respective bands.
* Multiple alternatives exist within ±0.08 Ba_eff for every load, indicating robust commercial coverage in the precision cartridge space.
* The H4350 load in the 6mm GT remains the only clear mismatch (too slow for its RC), consistent with field observations requiring ≥25" barrel for optimality. Note: H4350 is seldom an optimal propellant for many applications due to its bulk density and dynamic vivacity. It is often too dense to allow optimal case fill under maximum peak pressure.
* Note on .300 Blackout: This load is an outlier because the propellant (N110), case volume, and projectile mass prevented a higher charge weight. While the end result is optimal with burn fraction φ ≈ 1 (complete consumption per mass/energy conservation) before the muzzle, it suggests the use of a heavier projectile would be prudent to improve ballistic efficiency, as maximum peak pressure is below the target window.

### Dynamic Vivacity Impact
Progressive-burning modern powders (high a0) show significant effective acceleration:

* RL16: base Ba 0.468 → Ba_eff 0.651
* N570: base Ba 0.295 → Ba_eff 0.475
* N555: base Ba 0.447 → Ba_eff 0.586

This adjustment correctly places extruded powders with apparent low temperature sensitivity in their observed performance sweet spot despite lower nominal Ba. Note: There is no such thing as truly temperature-stable extruded powders—only propellants that exhibit apparent low temperature sensitivity under specific internal ballistic and external temperature conditions.

## Discussion
The framework successfully replicates and extends the original Powley Computer’s functionality (empiricism flagged; alternative: direct Ba from Vieille's law):

* Charge prediction exceeds Powley accuracy due to modern high-density calibration.
* Propellant selection via Ba_eff bands is more reliable than closed-bomb rankings or raw vivacity.
* The system naturally identifies commercial gaps at the extremes, enabling informed wildcat design decisions.

## Current Limitations

* Relative Capacity calculation remains approximate for heavily seated heavy-for-caliber boat-tail bullets (displaced volume reduction).
* Extreme fast powders (pistol/shotgun territory) not yet modeled.
* Very slow surplus/extreme powders (US869, WC860 variants) untested.

## Conclusions and Recommendations

* The algebraic framework shows promise for further evaluation and is ready for practical use in screening conventional and mild wildcat cartridges.
* Propellant selection should use effective vivacity (Ba_eff) rather than base Ba for ranking.
* For new designs falling outside Ba_eff 0.45–0.90, expect either under-burn (too slow) or excessive muzzle blast/pressure (too fast).

## Next Steps

* Expand database with RL26, N560, H4831SC, and any available ultra-slow models.
* Refine Relative Capacity calculation to explicitly account for bullet seating displacement. Currently, effective case capacity is entered as an input instead of calculated.
* Develop simple spreadsheet implementation of the full selector (inputs → RC/SD point → recommended propellants + charge estimate).

This modern empirical framework preserves the elegant simplicity of the original Powley Computer while delivering substantially higher accuracy for contemporary high-performance reloading.