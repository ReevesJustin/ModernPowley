# Historical Reconstruction Pass

Date: 2026-07-14

## Checkpoint

The prior audit/environment work was committed without rewriting history:

```text
d89523c250ddf489cabeaf5a5061dfa2f2689180
chore: standardize environment and agent guidance
```

## Evidence Acquired and Verified

- `reference/powley_manual/powleysmanuals1.pdf`, SHA-256
  `119bc2c3cf4b798e7bf4ee1cb59b69a1643673875ad6556ee573912e1973ed66`.
  All nine scan pages were visually inspected.
- `reference/online_emulator/kwk_powley_20240228.html`, SHA-256
  `0162ee7722dfd4bf586120590e7a7fcd4d72c908e9d17b6f335822dcac990e03`.
  The inline JavaScript was audited independently of the manual.

Both downloaded artifacts match the hashes already recorded in the checkpoint
source ledger. The OCR remains a navigation aid with `ocr_only` status.

## Original Operations Now Verified

Visual inspection supports the following manual operations:

- `SD = (Wb/7000)/d^2`, manual p. 9, scan p. 7;
- `MR = Wc/Wb`, manual p. 9, scan p. 7;
- loading density `Wc/V0`, manual p. 3, scan p. 4;
- `Wc=0.80*V0` for 4198/4227 and `Wc=0.86*V0` for other listed IMR powders;
- `1 in3 water = 253 gr`, manual p. 9, scan p. 7;
- effective diameter `(bore+groove)/2` when a caliber is absent from the slide;
- projectile travel from seated bullet base to muzzle;
- total expansion ratio `(V0+Vb)/V0`;
- the supported arithmetic of the manual's .308 worked example.

The original namespace contains only these operations and explicit provenance
failures. Gross fired-case capacity subtraction was removed from `original/`;
that algorithm belongs to the archived emulator transcription.

## Independently Reproduced Emulator Operations

The separate `modern_powley.later.emulator` module reproduces the archived
geometry, bullet-length estimates, Davis-labeled quickness expression, load
density switch, exact powder branches, velocity, Miller-labeled `F2`,
Howell-labeled CUP expression, claimed CUP-to-PSI expression, inverse CUP
operation, energy, efficiency, and positive-output rounding. These are all
`online_emulator` / `emulator_derived`, never `original_powley`.

For the manual .308 inputs, the emulator quickness is about 117.33 and its group
contains 4064, but its velocity is about 2697 ft/s versus the manual's graphical
2730 ft/s reading. This does not establish equivalence.

## Intentionally Unavailable Original Operations

- exact measurement fixture/procedure for seating-depth-specific water capacity;
- original powder-selection equation or Arrow 2 numeric scale;
- exact original powder lookup boundaries;
- original Expansion Ratio-Velocity tables or generating equation;
- original peak/chamber pressure equation and precise historical pressure unit;
- complete muzzle-pressure interpolation rule;
- lettered powder procedures as executable algorithms, because the initiating
  physical scale position is unavailable.

`original.select_powder`, `original.estimate_velocity`, and
`original.estimate_pressure` continue to raise `MissingProvenanceError`.

## Sources Required Next

1. Flat, high-resolution scans of both sides and every scale of the 1961
   calculator, plus revision identification.
2. William C. Davis Jr., *Handloading* (1981), reported pp. 138-145, including
   Tables 3 and 4 and surrounding definitions.
3. Ken Howell's July 1997 *Varmint Hunter* article, complete title and pages.
4. Don Miller's July 1999 publication, including derivation and valid ranges.
5. Primary documentation for any later pressure sheet included as scan pages
   1-2, including its date and relationship to the 1961 calculator.
6. A primary description of the original water-capacity measurement fixture.

## Reproducible Verification

```bash
uv sync --locked --offline
uv lock --check
uv run pytest -q
uv run python -m compileall -q src tests scripts
git diff --check
```
