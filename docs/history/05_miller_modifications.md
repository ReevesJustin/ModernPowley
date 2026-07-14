# Miller Modifications

The tagged prototype says Don Miller published a simplification in July 1999,
corrected Davis typographical errors and replaced a pressure-ratio table with an
equation. No title, artifact, derivation, coefficients, valid range or validation
data are committed.

Classification: **Miller modification, unresolved**. No Miller equation is
implemented, and no unspecified Miller relationship supports a pressure estimate.

The archived emulator labels its `F2` expression as Miller's approximation of a
Davis table. The repository reproduces that code only under
`modern_powley.later.emulator`; the missing Miller publication prevents an
independent Miller implementation.
