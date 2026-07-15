# Evidence And Model Classes

## Purpose

These controlled conceptual classes govern candidate intake and promotion for
the modernized program. They supplement, rather than replace, the repository's
historical attribution and provenance-status vocabularies. Adding them to
machine-readable ledgers is a future implementation task and requires a schema
review.

Every future numerical implementation must declare one evidence class and one
model maturity class. Multiple evidence records may support a method, but their
classes must remain individually visible.

## Evidence Classes

| Class | Qualifying evidence | Historical use | Modernized use | Provenance and uncertainty | Calibration | Final evaluation |
|---|---|---|---|---|---|---|
| `original_powley_primary` | Retained original Powley manual, device, article, table, or other authenticated primary bytes | May support `original/` within the evidenced domain | Yes | Artifact identity, hash, location, transcription, visual confidence, units, and contradictions required | Only if separately justified; do not alter historical claims | Yes when applicable and independent of calibration |
| `later_powley_associated_primary` | Retained primary Davis, Howell, Miller, later Powley, or associated publication | No substitution for missing original behavior; belongs in `later/` | Yes as a separately named candidate | Author, edition, pages, artifact hash/access, exact attribution, uncertainty, and historical relationship required | Permitted with disclosure | Permitted if not used for calibration and applicable |
| `other_published_primary` | Retained technical standard, paper, monograph, or first-party research publication | No | Yes | Stable citation, edition, page/equation/table, artifact access, units, domain, and reported uncertainty | Permitted within source domain | Permitted when independent and applicable |
| `manufacturer_published` | Current or archived manufacturer manual, specification, test report, or published dataset | No | Yes | Manufacturer, product/lot where available, edition/date, test conditions, units, and access record required | Permitted with source limitations | Permitted when not used for calibration; not automatically laboratory-independent |
| `independent_laboratory_measurement` | Instrumented measurements with independent laboratory identity and documented procedure | No | Yes; preferred physical validation evidence | Instrumentation, calibration, conditions, sample identity, uncertainty, raw/processed distinction, and custody required | Permitted with held-out cases | Yes; independence and holdout status required |
| `user_measurement` | User-observed dimensions, masses, capacities, velocities, or pressures with a recorded method | No unless it documents operation of retained primary evidence | Yes with bounded scope | Observer, date, instrument, resolution/calibration, conditions, repeated observations, and uncertainty required | Permitted cautiously and visibly | Only with stated limitations; not independent by default |
| `secondary_transcription` | OCR, normalized transcription, review, summary, or derivative without retained controlling primary bytes | Navigation/corroboration only unless independently verified | Candidate support only | Parent source, transformation, correction ledger, confidence, and unresolved glyphs required | Not alone | Not alone for physical validation |
| `reverse_engineered` | Behavior inferred from software, simulator output, device response, or black-box observations | Never original evidence | Experimental candidate only | Target/version/hash, inputs, observation method, coverage, ambiguity, and legal/access limitations required | Permitted only as disclosed reverse engineering | Not as independent physical validation |
| `empirical_fit` | Equation or parameters fitted to observations | Never original evidence | Experimental candidate until promoted | Dataset identities, selection, duplicates, preprocessing, objective, algorithm, residuals, uncertainty, and split required | Yes, by definition | Only on disjoint holdout or external data |
| `calibrated_parameter` | Parameter adjusted so a model agrees with designated calibration cases | Never original evidence | Model-specific candidate | Base model, parameter meaning/units, calibration cases, objective, bounds, covariance/sensitivity, and version required | Yes | Not on calibration cases; external or held-out cases required |
| `exploratory_hypothesis` | Agent/user proposal without sufficient source or validation | Never | Quarantined exploration only | Author/date, rationale, units, assumptions, expected falsification test, and known gaps required | Not for promoted behavior | No |

### Evidence Rules

- A secondary transcription cannot acquire primary status through agreement with
  a worked example.
- Manufacturer and simulator outputs are not independent laboratory measurements.
- Reverse-engineered behavior cannot establish authorship or historical identity.
- Calibration and evaluation cases must be labeled at row level.
- A value with unresolved units or semantics is excluded from numerical use.
- Evidence confidence and model maturity are separate dimensions.

## Model Maturity Classes

| Class | Meaning | Permitted use |
|---|---|---|
| `retained_candidate` | Source or proposal is retained and classified; transcription may be incomplete | Documentation and intake only |
| `transcribed` | Equations, variables, tables, units, and literal ambiguities are recorded | Audit and independent calculation only |
| `dimensionally_audited` | Unit behavior and dimensioned constants are explicit and internally consistent | Experimental implementation planning |
| `source_reconciled` | Independent calculation matches source examples within justified precision, with discrepancies classified | Experimental implementation permitted |
| `implemented_experimental` | Versioned implementation exists outside `original/` with guards, tests, and declared domain | Research reproduction only; no implied physical validity |
| `measured_validated` | Defined claims meet predeclared error metrics on independent measured cases | Candidate for modern promotion within validated domain |
| `promoted_modern` | A documented review admits the method to the future modernized namespace for stated decisions | Only the approved domain and decision uses |
| `deprecated` | Superseded behavior retained for reproducibility but excluded from new decisions | Historical reproduction only |
| `rejected` | Evidence, dimensions, validation, or applicability failed | Retain decision record; exclude from decisions |

No current `Ba_target`, `Ba_eff`, charge regression, GRT mapping, emulator
formula, Davis equation, or other quarantined behavior is classified
`promoted_modern` by this document.

## Required Declaration

Before numerical implementation, a candidate record must state:

- stable method identifier and human-readable name;
- evidence class and source identifier;
- model maturity;
- attribution class;
- equations, constants, units, and variable semantics;
- supported domain and excluded cases;
- interpolation and extrapolation policy;
- calibration/evaluation role;
- uncertainty and confidence treatment;
- permitted decision roles: geometry, screening, rejection, ranking,
  calibration, or reporting;
- implementation, test, and decision-record locations.
