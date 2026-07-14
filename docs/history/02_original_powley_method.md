# Original Powley Method

This chapter reports only what visual inspection of the 1961 manual scan supports. An item
marked **unresolved** is not implemented by inference.

## Inputs and Measurement

| Input | Definition | Unit | Source |
|---|---|---|---|
| `net_capacity_water_grains` | water filling powder space for the seated load | gr H2O | manual pp. 3, 8-9 |
| `bullet_weight_grains` | bullet weight | gr | manual p. 9 |
| `bullet_diameter_inches` | diameter used for sectional density | in | manual p. 9 |
| `projectile_travel_inches` | initial bullet-base position to muzzle | in | manual p. 9 |
| `effective_bore_diameter_inches` | average bore/groove diameter when scale absent | in | manual p. 9 |

The manual asks the user to measure barrel length and water capacity, states that
capacity changes with seating depth and case brand, and recommends averaging
several readings (pp. 8-9). Visual inspection confirms that loading density uses
the water weight that fills the **powder space**. It does not instruct the user
to enter fired-case overflow capacity and does not print a complete weighing or
fixture procedure. Whether the water space was measured with a seated bullet or
by another equivalent fixture remains unresolved. Gross capacity minus a
cylindrical shank estimate is the archived emulator's method, not a verified
original-manual operation, and has been removed from `original/`.

## Confirmed Equations

```text
SD = (Wb / 7000) / d^2
MR = Wc / Wb
Wc = 0.80 * V0    for IMR 4198 and IMR 4227
Wc = 0.86 * V0    for the other listed IMR powders
deff = (dbore + dgroove) / 2
ER = (V0 + Vb) / V0
```

`V0` is numerically the water weight filling the available powder space, not
gross fired-case capacity. These historical density rules are not modern loading
recommendations.

Canonical expansion names are:

```text
barrel_volume_ratio = Vb / V0
total_expansion_ratio = (V0 + Vb) / V0
```

The repository uses the manual's `1 in3 = 253 gr H2O` convention only in the
original namespace.

## Powder Selection

The computer selects from IMR powder-number scales. The accessible manual and
perspective photograph do not support exact numeric transcription of every
boundary. The exact original equation and lookup boundaries are **unresolved**.
Calling the Davis equation original would be an attribution error.
`original.select_powder` raises `MissingProvenanceError`.

## Velocity and Pressure

The manual supplies scales and worked values but not a verified algebraic
equation in the accessible pages. Original velocity and pressure functions fail
explicitly. Davis, Howell and Miller variants are not inserted here.

## Published Worked Example

Manual p. 9 gives a .308 Winchester example. The complete audited calculation
is in `docs/history/original_powley_worked_example.md`.

| Quantity | Printed value |
|---|---:|
| water capacity/powder space | 51.5 gr H2O |
| bullet | 150 gr |
| charge | 44.3 gr |
| mass ratio | 0.295 |
| sectional density | 0.227 |
| selected powder | 4064 |
| nominal barrel | 24 in |
| muzzle-to-tip distance | 21 5/16 in |
| bullet length | 1 1/16 in |
| effective bullet travel | 22 3/8 in (manual rounds 22.4) |
| expansion ratio | 9.0 |
| predicted velocity | 2730 ft/s |

`51.5 * 0.86 = 44.29` reproduces the printed charge. SD cannot be independently
reproduced without the exact diameter Powley used; “.30 caliber” is insufficient.
Powder, ER and velocity are slide-rule observations, not reconstructed equations.

## Assumptions and Limits

The manual is built around listed single-base IMR powders, nearly full powder
space, and what it calls a good working pressure. Historical caution language
does not establish modern safety or applicability. No load recommendation is
derived from this baseline.

The manual also prints local percentage rules for small charge changes and
special procedures for lettered powder positions. They are recorded as
`EQ-057` through `EQ-059` but not implemented: the text limits their context,
and the letter procedures depend on an unavailable original scale position.
