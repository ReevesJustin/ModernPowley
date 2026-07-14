# Archived Emulator Equation Audit

## Artifact

- Source: `SRC-KWK-EMULATOR`
- Archive URL: `https://web.archive.org/web/20240228100250id_/http://kwk.us/powley.html`
- Local artifact: `reference/online_emulator/kwk_powley_20240228.html`
- SHA-256: `0162ee7722dfd4bf586120590e7a7fcd4d72c908e9d17b6f335822dcac990e03`
- Language: HTML with inline ECMAScript; 1 file, 2003-2006 copyright comment
- Verification: retrieved bytes match the previously recorded hash

## Implemented Chain

| lines | behavior | units | provenance status | deviation/issue |
|---:|---|---|---|---|
| 184-232 | SD, two bullet-length estimates, seating depth, cylindrical intrusion, net capacity, approximate bore area, relative capacity, travel, ER | gr, in, in2 | emulator_derived | Uses gross fired-case overflow capacity plus geometric subtraction, unlike the manual's requested seating-depth-specific water capacity input. |
| 246-257 | `I=.86W`, `MR=I/G`, `Q=20+12/(SD*sqrt(MR))`; switch to `.80W` if `Q>145` | gr, ratio | emulator_derived | Code labels variables “per Davis”; `Q` is not recomputed after charge/MR change. |
| 259-264 | `V=8000*sqrt(I*(1-ER^-0.25)/(G+I/3))` | ft/s | emulator_derived | Matches the expanded later Davis transcription; it is not printed in the 1961 manual. |
| 266-283 | ordered powder branches | quickness index | emulator_derived | Exact nonoverlapping code boundaries; grouped outputs differ from a single slide position. |
| 289-295 | Miller-labeled approximation of Davis F2 table | dimensionless | emulator_derived | Davis Table 4 is now transcribed separately; Miller publication remains absent and the accuracy comment is author assertion only. |
| 297-300 | rough CUP-to-claimed-PSI expression | CUP to claimed psi | emulator_derived | Scientific source absent; repository does not treat it as a general conversion. |
| 302-340 | `K2`, Howell-labeled `134.7`, CUP, energy, efficiency | mixed | emulator_derived | The Davis pressure chain is transcribed separately; Howell and Miller primary publications remain absent. |
| 344-365 | inverse velocity for requested CUP with fixed 0.86 loading density | ft/s | emulator_derived | Emulator operation only; not a manual equation. |

## Powder Branches and Rounding

The branch order is `<81`, `<=91`, `<=110`, `<=125`, `<=145`, `<=165`,
`<=180`, and otherwise. Therefore 91 belongs to “Slower than 4831,” while the
next representable value belongs to `4831, 4350`. Outputs use JavaScript
`Math.round`: charge to 0.1 grain, quickness and velocity to integers, CUP to
the nearest 100, and claimed PSI to the nearest 1000. The Python transcription
exposes raw arithmetic; tests cover branch boundaries and raw values.

## Validation and Deviations

Input scanning rejects blank, nonnumeric, and nonpositive inputs, although its
message says values “must be >= 0.” It flags pressure extrapolation outside ER
5-13 or MR 0.2-1.0. The page warns that both computers can underestimate
pressure. These are emulator statements, not validation.

For the manual .308 example the emulator grouped band contains 4064, but its
velocity is approximately 2697 ft/s versus the manual slide reading 2730 ft/s.
This difference and one grouped-band match do not establish equivalence. No original powder-scale,
velocity-table, or pressure-scale differential suite is possible without the
physical calculator scales or authoritative tabulations.
