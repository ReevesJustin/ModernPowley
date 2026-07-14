# Online Emulator Implementation

`SRC-KWK-EMULATOR` is the archived 2024-02-28 snapshot of Karl W.
Kleimenhagen's `kwk.us/powley.html`, SHA-256
`0162ee7722dfd4bf586120590e7a7fcd4d72c908e9d17b6f335822dcac990e03`.
This is exact emulator behavior, not original Powley and not a substitute for
Davis, Howell, or Miller publications.

## Geometry (JavaScript lines 184-232)

```text
SD = (G/7000) / D^2
seating_depth = case_length + bullet_length - cartridge_length
intrusion_water_grains = 198 * seating_depth * D^2
net_capacity_water_grains = gross_capacity - intrusion_water_grains
net_capacity_in3 = net_capacity_water_grains / 252.4
approx_bore_area_in2 = 0.773 * D^2
bullet_travel = barrel_length - case_length + seating_depth
ER = (bore_volume + net_capacity_in3) / net_capacity_in3
```

These are emulator approximations, not equations labeled original Powley here.

## Load Computer (lines 241-283)

The emulator starts with `charge=0.86*net_capacity`, computes
`Q=20+12/(SD*sqrt(MR))`, and changes charge to `0.80*net_capacity` when
`Q>145`. It does not recompute `Q` after that change, though it recomputes MR.

```text
M = 1 / ER^(1/4)
N = 1 - M
Y = bullet_weight + charge/3
velocity = 8000 * sqrt(charge*N/Y)
```

Lookup uses ordered branches `<81`, `<=91`, `<=110`, `<=125`, `<=145`,
`<=165`, `<=180`, then `>180`; the emulator has no endpoint overlap. This is
distinct from ambiguous natural-language “x to y” Table 3 ranges.

## Pressure Computer (lines 289-340)

The code labels this as Miller's approximation of Davis's `F2` table:

```text
F2 = 0.024075 * (9.3-MR) * (1.071+ER-0.009736*ER^2)
K2 = 0.53/MR + 0.26
CUP = 134.7*(velocity/100)^2*loading_density/(ER-1)*K2*F2
```

Its comment says `134.7` is “per Howell” and Davis has `142`. Those attributions
remain secondary until the source pages are obtained. The emulator labels the
result CUP and applies a separate rough CUP-to-PSI function. None of these
equations is exposed as original or validated in the audited package.
