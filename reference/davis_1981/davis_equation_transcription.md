# Davis 1981 Equation Transcription

## Source Status

This is a source-facing transcription of equations and worked values supplied
from visual review of W. C. Davis Jr., "Some Simplified Interior Ballistics for
Handloaders," *Handloading* (NRA, 1981), approximately pp. 138-144. The Internet
Archive item `handloading00will` is access-restricted. No page image was
available to store in this pass, so this file is not a facsimile substitute.
It is a normalized secondary derivative of user-mediated primary-page review;
its underlying authority is `SRC-DAVIS-1981`, and its status is not direct
retained-artifact verification.

## Printed Symbols

| Symbol | Davis meaning | Unit |
|---|---|---|
| A | charge weight divided by bullet weight | dimensionless |
| B | bullet length | in |
| C | case length | in |
| D | bullet diameter | in |
| E | barrel length from bolt face | in |
| F | gross fired-case water capacity | gr water |
| G | bullet weight | gr |
| H | boat-tail axial height | in |
| I | powder charge weight | gr |
| J | small-end boat-tail diameter | in |
| K | boat-tail displacement correction | gr water |
| L | cartridge overall length | in |
| LD | loading density, I/W | dimensionless |
| M | one divided by the fourth root of R | dimensionless |
| N | 1-M | dimensionless |
| P | seated flat-base displacement; later also pressure | gr water; crusher pressure |
| Q | effective bore volume | in3 |
| R | expansion ratio | dimensionless |
| S | seating depth | in |
| T | bullet travel | in |
| U | loaded powder-chamber volume | in3 |
| V | muzzle velocity | ft/s |
| W | loaded powder-chamber water capacity | gr water |
| X | empirical powder-selection index | arbitrary index |
| Y | effective moving-weight term | gr |
| Z | sectional density | lb/in2 convention |

## Transcribed Equations

```text
S = C + B - L
P = 198 S D^2
K = 66 H (2 D^2 - D J - J^2)
W = F - P
W = F - P + K
T = E + S - C
U = W / 252.4
Q = 0.773 T D^2
R = (Q + U) / U
I = 0.80 W or 0.86 W under Davis's powder-specific procedure
LD = I / W
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
pressure = K1 K2 / K3
P2 = P1 (LD2/LD1)^2
I2 = W2 LDtarget
```

## OCR Corrections Supplied With Visual Rationale

| damaged text | normalized text | basis |
|---|---|---|
| `D=` | `D^2` | exponent damaged in OCR; dimensional equation and image review |
| `VA` | `sqrt(A)` | radical damaged in OCR and image review |
| `M = 1/VR` | `M = 1/R^(1/4)` | fourth-root sign damaged in OCR and worked value |
| `Y = G + 1/3` | `Y = G + I/3` | missing `I`; dimensions and worked value |
| `A = 1/G` | `A = I/G` | capital `I` read as numeral one; definition and worked value |
| `K = 87` | `K = 0.87` | decimal lost; worked example and geometry |
| damaged velocity radical | `V = 8000 sqrt(I N / Y)` | image review and worked value |
| boat-tail expression ending damaged | final term is `-J^2` | image review, frustum geometry, and worked value |

The actual damaged OCR artifact was not supplied or downloadable in this pass.
These correction records preserve the reported damaged strings but cannot hash
or reproduce the complete OCR file.

## Worked .30-06 Values

```text
C=2.484, F=69, B=1.220, H=0.150, J=0.200,
D=0.308, G=180, L=3.30, E=24

S=0.404, P=7.59, K=0.87, W=62.3, T=21.9,
U=0.247, Q=1.606, R=7.50, I=53.6, A=0.298,
Z=0.271, X approximately 101, M approximately 0.604,
N approximately 0.396, Y approximately 197.9,
V approximately 2620 ft/s

F2=1.74, K1 approximately 9,090,854, K2 approximately 2.040,
K3 approximately 405, pressure approximately 45,790 crusher-gage psi
```

Publication rounding is retained; these displayed values are not exact binary
floating-point targets.
