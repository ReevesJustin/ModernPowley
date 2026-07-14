# Original Manual Page Map

Source: `SRC-POWLEY-1961-MANUAL`, local artifact
`reference/powley_manual/powleysmanuals1.pdf`. SHA-256 verification and visual
inspection were completed 2026-07-14. The scan has nine PDF pages; several scan
pages contain two numbered manual pages. The first two scan pages are later
supplements and are not part of the numbered 1961 instruction manual.

| manual_page | scan_page | section | content_type | equations | tables_or_scales | implemented_status | verification_status | notes |
|---|---:|---|---|---|---|---|---|---|
| later insert | 1 | Hutton Rifle Ranch Rifle Powder Selection | table | none | 16-position cross-brand burning-rate table | not implemented | verified_visual_scan | Later sheet mentions 1975 data; not evidence for the 1961 calculator scale. |
| later insert | 2 | Examples and Powley psi Calculator | examples/instructions | small-change percentage rules | .30-30, .25-06, and .270 examples | not implemented | verified_visual_scan | Separate later pressure sheet; not the numbered manual. |
| cover/contents | 3 | Powley Computer for Handloaders | contents | none | section/page index | not applicable | verified_visual_scan | Establishes manual pages 3-12. |
| 3 | 4 | Efficient Powder Selection | narrative/definitions | loading density 0.80 or 0.86 | no numeric calculator scale | charge arithmetic implemented | verified_visual_scan | Defines loading density as powder weight divided by water weight filling powder space. |
| 4 | 5 | IMR Powders | narrative/tables | none | cartridge/powder and bullet/powder examples; energy table | descriptive only | verified_visual_scan | Powder selection is a calculator reading, not a printed equation. |
| 5 | 5 | Ballistic Efficiency; Bore Capacity | definitions/examples | total expansion-ratio definition | expansion-ratio/velocity readings at ER 4 and 12 | geometry implemented | verified_visual_scan | Velocity values are graphical/table readings. |
| 6 | 6 | Muzzle Pressure; Primers; Other Powders | narrative/readings | none complete | isolated muzzle-pressure readings | not implemented | verified_visual_scan | No complete interpolation algorithm is printed. |
| 7 | 6 | Ideal Powder; Duplex Loads; Maximum Velocity | narrative | qualitative percentage relationships | none | not implemented | verified_visual_scan | Historical claims are not generalized into a model. |
| 8 | 7 | Good Working Pressure; Using Your Computer | limitations/measurement | none | Expansion Ratio-Velocity Tables referenced but absent | measurement documented | verified_visual_scan | Requires user measurements of barrel length and case water capacity and averaging several readings. |
| 9 | 7 | Typical Example; Special Conditions; Powder Numbers | worked example/instructions | SD arithmetic; 253 gr water/in3; 86% charge; MR orientation | .308 worked example; slide readings | supported arithmetic implemented | verified_visual_scan | Exact powder/velocity scales are not reproduced in the scan. |
| 10 | 8 | Lettered powder selections | procedural rules/examples | 5% charge changes for F, D, B | several worked readings | not implemented | verified_visual_scan | Rules depend on unavailable Arrow 2 scale positions. |
| 11 | 8 | Changing Powder Charges | procedural narrative | local percentage relationships | 5010 example | not implemented | verified_visual_scan | Manual limits rules to small changes and excludes maximum-load use. |
| 12 | 9 | Barrel Length and Velocity; Conclusion | procedure | recompute ER then reread table | absent Expansion Ratio-Velocity Tables | unresolved | verified_visual_scan | No explicit velocity equation. |

## OCR Issues

The Markdown transcription has a single marker before manual page 3 and merges
manual pages 3-12. Visual inspection corrected navigation, not source wording.
Known OCR risks include `41.M psi`, fractions, `4427`/`4227`, and lost page
boundaries. Numeric evidence in ledgers cites the scan page and manual page.
