# Algebraic Propellant Selection: A Modern Empirical Framework

## Introduction

The objective of this framework is to develop a simple algebraic transfer function for propellant selection and load optimization in rifle cartridges. By leveraging empirical data from verified high-performance loads, the system predicts suitable commercially available propellants, optimal charge weights, and key performance metrics. It flags mismatches where no commercial powder achieves the desired criteria: load density ≥95%, near-complete burnout at or before muzzle exit (low muzzle pressure, minimal blast), and safe peak pressures (~55,000–60,000 PSI in modern actions).

This approach draws direct inspiration from the **Powley Computer for Handloaders** (developed circa 1960 by Homer Powley at Frankford Arsenal, with contributions from Bob Forker, Bob Hutton, and later refinements by William C. Davis, Ken Howell, and Don Miller). The Powley Computer was a set of semi-empirical slide-rule tools (Load Computer for charge/velocity prediction and Pressure Computer for peak pressure estimates in CUP) designed to estimate safe, efficient loads primarily for IMR/single-base powders in modern bottleneck rifle cartridges. It assumed near-full cases (~86% density, adjustable), complete instantaneous burn, no friction/heat losses, and a conservative target pressure (~44,000 CUP, equivalent to ~50,000–52,000 PSI). While innovative for its era—using expansion ratio, sectional density, and mass ratio to select powder "quickness" and predict performance—it has limitations (e.g., underestimates modern pressures, inaccurate for non-IMR powders or extremes, optimistic velocities). Modern tools like QuickLOAD refine its math but share similar empirical challenges. Here, we update the Powley concept with contemporary high-density loads (>95%), diverse temperature-stable powders (Vihtavuori, Alliant, Hodgdon, etc.), effective barrel adjustments, and refined balance criteria.

---

## Hypothesis

Optimal loads exhibit consistent algebraic relationships driven by the *expansion ratio* (bore volume / effective case volume) and *dwell time* (effective barrel length). Propellant burn rate must match this ratio to achieve complete consumption near the muzzle while maintaining high load density for consistency and efficiency. When these align:

- Charge mass scales nearly linearly with effective case volume.
- A derived "balance index" (e.g., modified correlation number) remains near-constant (~0.10–0.11).
- No single commercial powder may perfectly fit extreme wildcats, allowing early identification of gaps.

This mirrors Powley's empirical finding that pressure scales roughly with velocity squared (~2% pressure rise per 1% velocity increase) and that quickness selection via sectional density and mass ratio yields balanced loads.

---

## Assumptions

- **High load density:** ≥95–100% (often compressed) for positioning consistency and low ES/SD (higher than Powley's ~86% baseline).
- **Near-complete burnout:** Inferred from moderate muzzle pressure (~10,000–16,000 PSI) and flat velocity curves (extending Powley's instantaneous burn ideal).
- **Target peak pressure:** ~55,000–60,000 PSI (Piezo; modern strong actions—higher than Powley's conservative ~44,000 CUP target).
- **Propellants:** Modern commercial options (Vihtavuori N1xx/N5xx, Alliant RL-series, Hodgdon H/V series, IMR Enduron/4000-series, etc.); accounts for in-cartridge behavior diverging from closed-bomb tests.
- **Bullet alignment:** Preference for heavy-for-caliber VLD/hybrid designs (long bearing surface, ~4.8–5.7 calibers).
- **Standard primers and jacketed bullets:** no major friction/heat losses (calibrated empirically, as in Powley).

---

## Core Calculations and Steps

### Inputs:
- `Case capacity` (gr H₂O, full to mouth)
- `Case length` (in)
- `Cartridge OAL` (in)
- `Bullet length` (in)
- `Bullet weight` (gr)
- `Bullet diameter/groove diameter` (in)
- `Barrel length` (in)

### Derived Parameters (Building on Powley Expansions):
- **Seating depth (in):** `Cartridge OAL – (case length + reasonable neck engagement)`
- **Effective case volume/net capacity (gr H₂O):** Full case capacity minus volume displaced by seated bullet portion (approximate using bullet geometry; boat-tails add less displacement—similar to Powley's "volume under bullet").
- **Effective barrel length (in):** `Barrel length – (cartridge OAL – ~0.5–1 in chamber/throat allowance)` (refines Powley's nominal barrel use).
- **Bore volume (gr H₂O):** `π × (groove_dia/2)² × effective_barrel_length × ~253` (conversion factor in³ to gr H₂O).
- **Expansion ratio (ER or X):** `1 + (bore volume / effective case volume)`. Optimal range ~5.5–9.0 for precision loads (higher ER needs faster powder; lower needs slower—core to Powley's quickness selection).
- **Sectional density (SD):** `Bullet weight (lb) / (diameter²) = bullet_mass_gr / (7000 × diameter²)`; used in Powley/Davis quickness equations.
- **Powder-to-bullet mass ratio (k or MR):** `Propellant_mass / bullet_mass` (~0.28–0.38 in optima; central to Miller's pressure ratio refinements).

### Propellant Selection and Charge Prediction (Modern Updates to Powley):
- **Initial charge estimate:** `Effective volume × density factor` (e.g., ~0.86–1.0+ for modern compressed loads vs. Powley's 0.86 baseline).
- **Use empirical fit:** `Charge mass (gr) ≈ constant × (eff_case_vol)^{~1.0–1.02} × (eff_barrel_length)^{~0.06}` (near-linear, extending Powley's volume-based scaling).
- **Quickness/burn rate matching:** Via expansion ratio and SD/MR (e.g., adapted Davis/Miller: `quickness ≈ 19–20 + 12 / (SD × MR^{0.5–0.6})`); map to modern powders).
- Flag if `predicted charge / (eff_case_vol × bulk_density_g/cm³)` < 0.95 (poor fill) or ER mismatch suggests post-muzzle burnout (higher muzzle blast).

### Velocity and Pressure Estimates (Refinements to Powley/Miller):
- **Velocity:** Approximate adiabatic expansion, tuned empirically (e.g., `V ≈ sqrt(2 × energy_from_charge × efficiency / bullet_mass)`; ~3000–4000 ft-lb chemical energy per gr powder, varying by type—Powley used similar thermodynamic conversion).
- **Pressure:** Empirical proxy from charge, velocity², and ER (`pressure ∝ velocity²`; use Miller's peak/average ratio with mass/expansion adjustments; convert CUP to modern PSI equivalents, accounting for ~10–20% underestimate in crusher method).

---

This framework enables rapid screening of wildcats or custom loads, highlighting when commercial propellants fall short—guiding further refinement in tools like GRT/QuickLOAD. It preserves the Powley Computer's elegant simplicity while addressing its limitations (e.g., higher densities, broader powders, true PSI targets). 

**Future expansion:** Database of characterized propellants (bulk density, Qex, in-cartridge burn proxy) for automated matching.