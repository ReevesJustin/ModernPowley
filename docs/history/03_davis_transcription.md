# Davis Transcription

William C. Davis Jr.'s 1981 *Handloading* is referenced by the old repository,
but the pages are absent. A web transcription attributes this index to Davis:

```text
Q = 20 + 12 / (SD * sqrt(MR))
```

It is implemented only in `modern_powley.later.davis`, at medium confidence.
The transcription says the physical slide scale is closer to:

```text
Q = 19 + 12 / (SD * MR^0.6)
```

It does not know when or by whom the change was made. The latter is unresolved.

## Transcribed Table 3

| Index text | Powder text |
|---|---|
| less than 81 | much slower than IMR-4831; no suitable IMR canister powder |
| 81 to 91 | slower than IMR-4831/4350; transcription specifies a reduction |
| 91 to 110 | similar to IMR-4831 and IMR-4350 |
| 110 to 125 | similar to IMR-4064, IMR-4895 and IMR-4320 |
| 125 to 145 | similar to IMR-3031 |
| 145 to 165 | similar to IMR-4198 |
| 165 to 180 | similar to “IMR-4427” in the transcription |
| more than 180 | faster than “IMR-4427” |

Adjacent ranges overlap if “to” is inclusive. The implementation returns all
matches at an endpoint. `4427` is retained as a transcription issue rather than
silently corrected without the Davis page. No Davis velocity, pressure or Table
4 equation is implemented until the pages are acquired.
