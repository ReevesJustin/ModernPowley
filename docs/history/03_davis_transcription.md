# Davis 1981 Reconstruction

W. C. Davis Jr., "Some Simplified Interior Ballistics for Handloaders," in
*Handloading* (National Rifle Association of America, 1981), approximately
pp. 138-144, is a later primary publication. It is not direct original-Powley
evidence. The source volume is access-restricted at the Internet Archive.

The equation transcription supplied for this audit came from visual review of
the primary page images. This pass confirmed the volume metadata but could not
independently recapture the restricted pages. Exact page allocation and every
Table 4 cell therefore remain medium confidence pending a retained page image.

## Classification

- Davis's geometry, charge, powder-index, velocity, pressure, and loading-density
  equations are implemented in `modern_powley.later.davis`.
- `X = 20 + 12/(Z sqrt(A))` is classified
  `davis_empirical_powder_selection`, not original Powley.
- Davis calls the velocity expression "Powley's equation for muzzle velocity."
  That is a Davis attribution, not independent original-source verification.
- Pressure output is named `historical_crusher_pressure`. Davis's printed
  crusher-gage `psi` terminology must not be read as modern piezoelectric PSI.
- Project algebraic reductions are documented but do not replace Davis's
  printed `K1`, `K2`, and `K3` implementation sequence.

## Implemented Printed Equations

```text
S = C + B - L
P = 198 S D^2
K = 66 H (2 D^2 - D J - J^2)
W = F - P                  flat base
W = F - P + K              boat tail
T = E + S - C
U = W / 252.4
Q = 0.773 T D^2
R = (Q + U) / U
I = 0.80 W                 IMR 4198 and IMR 4227
I = 0.86 W                 other evidenced table powders
A = I / G
Z = G / (7000 D^2)
X = 20 + 12 / (Z sqrt(A))
M = 1 / R^(1/4)
N = 1 - M
Y = G + I/3
V = 8000 sqrt(I N / Y)
K1 = 0.0142 I F2 V^2
K2 = 0.53 (G/I) + 0.26
K3 = W (R - 1)
historical crusher pressure = K1 K2 / K3
P2 = P1 (LD2/LD1)^2       approximate pressure scaling
I2 = W2 LDtarget
```

The `0.80`/`0.86` function requires an explicit powder designation. It does not
invent an iteration to resolve the dependency between initial charge and powder
selection.

## Table 4

The normalized 34-by-9 table is
`data/reference/davis_1981_table4.csv`. Its rows are expansion ratio `R`, its
columns are mass ratio `A`, and its values are `F2`. Every lookup is bounded to
`0.20 <= A <= 1.00` and `5.0 <= R <= 13.0`; extrapolation is rejected.

Davis's worked example establishes linear interpolation in `R`:

```text
F2(7.4, 0.30) = 1.72
F2(7.6, 0.30) = 1.76
F2(7.5, 0.30) = 1.74
```

Linear interpolation in `A`, and bilinear interpolation when both coordinates
fall between grid points, are explicit historical implementation
interpretations. They are not presented as separately printed Davis equations.
The correction ledger records pending visual verification by row.

## Table 3

The older web transcription of Table 3 remains secondary evidence. Its adjacent
"x to y" bands have unresolved endpoint overlap, so the API returns all matching
bands at an endpoint. The new primary-source report did not include a complete
visual Table 3 capture; it is not silently upgraded.

## Derived Algebra

The following are project-derived equivalences:

```text
T = E + B - L
R = 1 + Q/U
I [0.53(G/I) + 0.26] = 0.53 G + 0.26 I
W(R - 1) = 252.4 Q
```

They are useful checks, not additional Davis quotations.

## Historical Limits

Davis describes the powder index as empirical, roughly corresponding to an
arbitrary Du Pont relative-quickness scale, and intended around 45,000-50,000
crusher units. His reported caliber-level error summaries are historical claims,
not a recoverable row-level validation dataset. No modern validation or loading
recommendation follows from this reconstruction.

## Still Unresolved

- the primary page image and damaged OCR are not stored locally;
- exact printed page numbers for individual equations and tables;
- complete primary Table 1, Table 2, and Table 3 captures and footnotes;
- the exact printed rule for interpolation along mass ratio `A`;
- the procedural resolution of the 0.80/0.86 powder-selection dependency;
- individual records behind Davis's summarized comparison percentages.
