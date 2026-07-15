# Original Powley Scale Recovery

Date: 2026-07-14

## Executive Finding

The retained primary manual and device photographs establish how Arrow 2 is
operated and preserve several graphical velocity readings, but they do not expose
the complete numeric geometry required to execute either operation. The clearest
photograph shows a 1985 revision at an oblique angle and only one slider setting.
The reverse face containing the Expansion Ratio-Velocity operation is not shown.
No scientific behavior was added to `src/modern_powley/original/`.

Classifications:

- `ARROW2_PARTIALLY_RECOVERED`
- `VELOCITY_PARTIALLY_RECOVERED`
- `PRESSURE_PARTIALLY_RECOVERED`

## Scope And Exclusions

This pass searched for primary scale geometry, tabulations, reading rules, and
worked-example constraints. The archived emulator and later Davis material were
used only to identify divergences and acquisition targets. Davis's algebraic
powder index, velocity equation, pressure equation, Table 3, and Table 4 remain
later material. They do not fill any original-source gap.

A newly reported derivative partial reprint of W. C. Davis Jr.'s 1981 article
corroborates the later method, including its direct water-displacement procedure,
geometry, powder index, velocity equation, pressure equation, and complete `F2`
table. No local bytes of that additional reprint were retained, so no artifact
hash is claimed. Its unexplained capacity change from `42.530520632` to
`42.377625032` and its use of `36.44475752752 gr` in an example labeled `35.4 gr`
are recorded as transcription/arithmetic warnings. Those findings require
comparison with the original NRA publication and do not change `original/`.

## Source Inventory

| Evidence | Artifact or URL | SHA-256 | Assessment |
|---|---|---|---|
| 1961 instruction manual scan | `reference/powley_manual/powleysmanuals1.pdf` | `119bc2c3cf4b798e7bf4ee1cb59b69a1643673875ad6556ee573912e1973ed66` | Controlling primary source; nine scan pages; physical scales absent. |
| Manual OCR | `reference/powley_manual/powleysmanuals1.md` | `021e1896b199428874c20ecb2a5464894fa5a275f049e1ac05d6e5e9eaf7fa16` | Navigation aid only. |
| Compressed device photograph | `image/classiccardboard_3.jpg` | `a20c32c606861535dc86b464fc71742a9316ac8f6e39c16e16f9177a258ee338` | Publisher-hosted quality-60 rendition; 1985 computer and 1965 pressure calculator. |
| Higher-quality device photograph | `reference/powley_scales/ssusa_powley_computers_1985.jpg` | `20ecd81b6f38331d3e2cef6696aa4b3c9f9dba061b68847dedaeb555e26178f0` | Same 1920x1080 publisher image without the quality query; best retained scale-face evidence. |
| Archived online emulator | `reference/online_emulator/kwk_powley_20240228.html` | `0162ee7722dfd4bf586120590e7a7fcd4d72c908e9d17b6f335822dcac990e03` | Secondary implementation; corroboration only. |
| 1963 Hutton-Powley article republication | Guns & Ammo publisher web page, source ledger `SRC-HUTTON-POWLEY-1963-WEB` | no local artifact | Publisher derivative of original coauthored content, not a facsimile. It supplies a capacity fixture and an incomplete pressure sequence. |
| Shooting Times 2011 article and small images | source ledger `SRC-SHOOTINGTIMES-2011` | not retained in this pass | Secondary history and a worked example; no reverse scale face. |

The existing manual page map remains the page-level inventory. PDF pages were
rendered at 400 dpi for inspection in temporary workspace. The source image
dimensions, not render DPI, limit recoverable detail; those temporary renders
were not committed.

## Image And Scan Quality

The manual's first two pages are later inserts. Numbered manual pages 3-12
describe operations and examples but do not reproduce the calculator faces or
the reverse velocity tables. Embedded raster resolution varies: the best pages
are about 1275 by 1746 pixels while several are substantially narrower. No edge
of a missing scale can be recovered by contrast or enlargement.

The higher-quality photograph is 1920 by 1080 pixels. The computer spans roughly
1220 pixels horizontally; the narrowest visible ticks are only about 5-7 pixels
apart and scale lines about 1-2 pixels thick. A visual center could therefore be
localized only to roughly 2-3 source pixels. Perspective, parallax, slider
position, partial occlusion, and the unproved relationship between the 1985 and
1961 revisions dominate that sampling error and cannot be converted into a
bounded historical scale-unit uncertainty.

Temporary inspection crops were generated from the higher-quality source with
FFmpeg (`crop=1450:500:180:0,scale=2900:1000` for Arrow 2 and
`crop=1000:650:740:380,scale=2000:1300` for pressure). Their hashes were
`80a4cb2bf40d30ed26ace1dfa035821cd24d0a9569cffca1e1a10e72c0573bf2` and
`53072d6515806b3962da6cdbf5b11631039887e6e20c68353e28687fce768b2d`.
They added no source resolution and were deliberately not committed.

## Arrow 2 Evidence

The photograph and manual agree on the operating sequence:

1. Set case capacity at `START` and read powder amount at Arrow 1.
2. Read the charge-to-bullet ratio at bullet weight.
3. Align bullet sectional density with that ratio.
4. Read a powder number at or to the right of Arrow 2.
5. If 4198 or 4227 is indicated, use the alternate loading-density index and
   recheck the ratio and powder.

Visible left-to-right labels on the photographed revision are approximately:

```text
A, 5010, B, C, 4831, 4350, D, 4320, 4064, E, 3031, F, 4198, 4227
```

The body carries the charge/bullet-ratio scale and Arrow 2; the slider carries
sectional density and powder labels. The photograph establishes topology and
direction, not exact boundaries. It shows only one alignment, is oblique, and
does not establish that the 1985 markings are identical to the 1961 device.
No polygons, breakpoints, or lookup bands are therefore published as original
machine data.

## Expansion Ratio-Velocity Evidence

Manual pages 5 and 8-12 call for turning to the Expansion Ratio-Velocity tables
and reading at expansion ratio and charge-to-bullet ratio. No retained image
shows that face, its axes, curves, table cells, interpolation instructions, or
boundaries. The seven printed observations are transcribed without interpolation
in `data/reference/original_powley_velocity_observations.csv`.

These points are constraints, not a surface. One observation lacks a printed
mass-ratio coordinate; another is explicitly rough. The manual's `2730 ft/s`
result is a graphical reading with printed precision, not an exact numeric
oracle. With the scale absent, digitization uncertainty cannot be quantified and
`estimate_velocity` remains unavailable.

## Worked-Example Constraints

| Source location | MR | ER | Printed velocity | Powder/position | Use |
|---|---:|---:|---:|---|---|
| manual p.5 | 0.28 | 4.0 | 2200 ft/s | not stated | isolated endpoint |
| manual p.5 | 0.28 | 12.0 | 2770 ft/s | not stated | isolated endpoint |
| manual p.9 | 0.30 table line | 9.0 | 2730 ft/s | IMR 4064 | controlling example |
| manual p.10 | 0.31 | 7.5 | 2680 ft/s | D position | contextual example |
| manual p.10 | 0.51 | 5.1 | about 3080 ft/s | B position | approximate example |
| manual p.10 | not printed | 5.0 | about 3220 ft/s | IMR 5010 | incomplete coordinate |
| manual p.11 | 1.45 | 4.5 | roughly 4480 ft/s | extreme context | rough reading |

The source-backed initial charges `44.29`, `52.89`, `67.94`, and `81.70 gr`
remain reproducible. The added observation file is explicitly non-executable and
is not imported by `original/`.

## Emulator Comparison

For the manual p.9 inputs, the emulator yields a grouped powder result containing
4064 and approximately `2696.792 ft/s`, versus the manual's single 4064 reading
and `2730 ft/s`. The velocity difference is `-33.208 ft/s` (`-1.216%`). The
emulator implements later Davis-form equations and cannot define the missing
physical geometry merely because one example is close.

## Pressure Calculator Evidence

The retained photograph shows a separate device marked 1965. Visible scales
include powder/capacity, expansion ratio, mass ratio, muzzle velocity, and a
pressure scale printed in thousands of `psi`. The oblique single-setting image
does not preserve its complete geometry or establish whether that historical
label corresponds to a specific crusher quantity. It is not part of the 1961
numbered manual.

The publisher republication of Hutton and Powley's March 1963 article describes
a sequence using loading density, squared velocity, mass ratio, expansion ratio,
and a missing table multiplier to move from an average-pressure expression to a
peak estimate. The original issue page and multiplier table are not retained.
That derivative evidence is insufficient for implementation and is not a basis
for converting crusher readings to modern piezoelectric PSI.

## Seating-Depth Capacity Evidence

The 1963 publisher republication describes grooving the intended bullet, filling
a sized/primed case with water, seating the bullet to the intended depth so water
vents through the groove, wiping the assembly, and obtaining powder-space water
capacity from the weight difference. The newly reported Davis derivative gives
a substantially similar later procedure and specifies a fired primer for sealing.
This closes the fixture-description gap at medium documentary confidence; it does
not establish a general original equation subtracting geometric intrusion from
gross overflow capacity.

## Missing-Source Acquisition List

1. A flat, calibrated, high-resolution scan or orthographic photograph of both
   faces and all moving elements of the relevant 1961/1962 Powley Computer.
   This would permit revision identification and Arrow 2 geometry recovery.
2. The reverse Expansion Ratio-Velocity face, including every curve/table line,
   tick, label, cursor edge, and instruction. A partial image is useful only if
   it overlaps known coordinates sufficiently to register with another image.
3. Original March 1963 *Guns & Ammo* pages for Hutton and Powley's “Pressure
   Estimation by Chronograph,” especially the referenced worksheet/table around
   printed page 57. Search by title, authors, magazine, month, and page.
4. Flat scans and dated instructions for the separate 1965 Powley psi Calculator,
   including its reverse and pressure-unit definition.
5. Contemporary advertisements or instruction editions that explicitly map the
   1961, 1962, and 1985 computer revisions and document changed scale markings.
6. Original NRA 1981 *Handloading* pages 138-144 to audit the supplied Davis
   derivative's unexplained capacity and charge discrepancies and all `F2` cells.

## Implementation Readiness

Arrow 2, velocity, and pressure fail the six readiness conditions: complete
primary geometry is absent; interpolation and boundary behavior are not
defensible; and uncertainty is dominated by unbounded revision/perspective
effects. `select_powder`, `estimate_velocity`, and `estimate_pressure` therefore
continue to raise `MissingProvenanceError`. The repository remains a
`PARTIAL_RECONSTRUCTION`.
