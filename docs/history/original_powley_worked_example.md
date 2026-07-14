# Original Powley Worked Example

## Source

The most complete example is the .308 Winchester example on manual page 9,
visually verified on PDF scan page 7 of `SRC-POWLEY-1961-MANUAL`.

## Reconstruction

| step | printed or normalized input | calculation/source | result | status |
|---:|---|---|---:|---|
| 1 | powder-space water capacity | printed calculator input | 51.5 gr H2O | verified_visual_scan |
| 2 | standard listed IMR loading density | manual p. 3 | 0.86 | verified_visual_scan |
| 3 | charge | `51.5 * 0.86` | 44.29 gr; printed 44.3 | verified_visual_scan |
| 4 | bullet weight | printed | 150 gr | verified_visual_scan |
| 5 | charge/bullet ratio | `44.3 / 150` | 0.2953; printed 0.295 | verified_visual_scan |
| 6 | sectional density | printed table reading | 0.227 | verified_visual_scan |
| 7 | powder selection | original slide reading | IMR 4064 | verified_visual_scan, algorithm unresolved |
| 8 | muzzle-to-seated-tip distance | cleaning rod | 21 5/16 in | verified_visual_scan |
| 9 | bullet length | printed | 1 1/16 in | verified_visual_scan |
| 10 | projectile travel | sum of steps 8 and 9 | 22 3/8 in; manual rounds 22.4 | verified_visual_scan |
| 11 | effective diameter | manual special-condition convention with nominal .300 bore/.308 groove | 0.304 in | derived input choice |
| 12 | total expansion ratio | `1 + pi*(0.304/2)^2*22.375*253/51.5` | 8.963; printed scale reading 9.0 | verified_visual_scan definition |
| 13 | velocity | original Expansion Ratio-Velocity Table reading at MR 0.30, ER 9.0 | 2730 ft/s | verified_visual_scan, algorithm unresolved |

The manual does not state the exact diameter behind its printed SD table value,
so SD is not reverse-engineered. The nominal bore/groove values in step 11 are
used only to check the printed expansion ratio within slide-reading resolution.

## Emulator Comparison

The archived emulator gives `Q=20+12/(0.227*sqrt(0.295))=117.35`, selecting
its grouped `4320, 4895, 4064` band rather than the manual's single 4064 slide
reading. Its velocity equation gives about 2697 ft/s, approximately 33 ft/s
below the manual reading. This is a differential observation, not evidence that the
emulator equation was printed in or exactly reproduces the original calculator.
