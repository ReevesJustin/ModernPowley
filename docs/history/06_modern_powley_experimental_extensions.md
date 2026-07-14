# ModernPowley Experimental Extensions

None of these equations is original Powley, Davis, Howell or Miller.

```text
Ba_eff = Ba * [a0 + (1-a0) * z2/2]
Ba_target = clamp(0.85 - 0.05*RC, 0.45, 0.90)
Wc = 0.71 * V0^1.02 * Ltravel^0.06
```

- `Ba_eff`: **ModernPowley experimental hypothesis**. GRT field definitions,
  units, averaging interval, weighting and cross-cartridge usefulness are not
  sourced. It is not ballistic efficiency.
- `Ba_target`: **agent-generated assumption**. No fit or source exists.
- charge equation: **empirical regression with missing fit provenance**. It is
  unit-dependent, in-sample only and has no independent validation.

All are quarantined under `modern_powley.experimental` and require
`allow_unvalidated=True`. Opt-in reproduces prototype behavior; it does not
validate it or make it loading guidance.

## Relative Burn-Rate Caution

Commercial charts are rough ordinal references, not universal physical order.
Chart position, closed-bomb vivacity, initial vivacity, progressivity, modeled
cartridge response and measured pressure/velocity are different quantities. IMR
4895 can be listed faster than IMR 4064 while a model orders their response
differently in a cartridge/pressure regime. That need not be contradictory. No
chart is used as a deterministic internal-ballistics mapping here.
