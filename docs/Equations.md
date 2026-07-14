# Audited Equation Guide

The machine-readable authority is `docs/provenance/equation_ledger.csv`. The
prototype equation narrative is preserved at tag
`pre_audit_agent_derived_prototype`.

## Original Powley, Directly Sourced

```text
SD = (Wb / 7000) / d^2
MR = Wc / Wb
Wc = 0.80 * V0    for IMR 4198 and IMR 4227
Wc = 0.86 * V0    for the other listed IMR powders
```

`V0` is water weight filling the net powder space behind the seated bullet.
Powley's historical volume conversion is `253 gr H2O/in3`. Projectile travel is
from the initial bullet-base position to the muzzle.

```text
barrel_volume_ratio = Vb / V0
total_expansion_ratio = (V0 + Vb) / V0
```

The exact original powder-scale equation/boundaries, velocity equation, and
pressure equation remain unresolved and are not implemented by inference.

## Later Davis Transcription

An accessible secondary transcription attributes this equation to Davis:

```text
Q = 20 + 12 / (SD * sqrt(MR))
```

It is not labeled original Powley. Table boundaries, overlap handling, source
confidence, and the reported physical-scale variant are documented in
`docs/history/03_davis_transcription.md`.

## Quarantined Experiments

```text
Ba_eff = Ba * [a0 + (1-a0) * z2/2]
Ba_target = clamp(0.85 - 0.05*RC, 0.45, 0.90)
Wc = 0.71 * V0^1.02 * Ltravel^0.06
```

These are respectively a ModernPowley hypothesis, an agent-generated assumption,
and an empirical regression with missing fitting provenance. They require
explicit opt-in and must not be called Powley equations. `Ba_eff` is not ballistic
efficiency.
