# Algebraic Propellant Selection: A Modern Empirical Framework

This project develops a simple algebraic transfer function for propellant selection and load optimization in rifle cartridges. Leveraging empirical data from verified high-performance loads, it predicts suitable commercially available propellants, optimal charge weights, and key performance metrics. The system flags mismatches where no commercial powder achieves desired criteria (load density ≥95%, near-complete burnout, safe peak pressures ~55,000–60,000 PSI).

Building on Homer Powley's 1960s slide-rule tool, it updates for modern temperature-stable powders (Vihtavuori, Alliant, Hodgdon, IMR), high-density loads, and precise PSI targets. Core calculations involve expansion ratio, sectional density, and mass ratios to select propellants and predict charges.

## Documentation

- [Introduction](docs/Introduction.md) - Full overview, hypothesis, assumptions, and calculations
- [Equations](docs/Equations.md) - Detailed formulas, propellant table, and derivations
- [Current Findings](docs/Current_Findings.md) - Validation results and discussion
- [History](docs/History.md) - Account of the Powley Computer development
- [Dynamic Vivacity](docs/Dynamic_Vivacity.md) - Explanation of burn rate adjustments