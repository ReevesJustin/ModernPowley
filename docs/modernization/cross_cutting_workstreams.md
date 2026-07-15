# Modernization Cross-Cutting Workstreams

Status: `planning_direction`

These workstreams guide future specifications. They authorize no implementation,
dependency, data intake, model, plot, parser, or interface.

## Powder Evidence And Data Foundation

Extend M02 eventually toward a neutral immutable versioned evidence store for
manufacturer, laboratory, user, other primary, and public observations. Preserve
source artifacts/hashes; powder/product/lot/revision; conditioning, temperature,
humidity; bulk-density method; apparatus/sample; uncertainty/variability;
domain; conflicts; activation/supersession; and source-relative burn-rate
ordinals. Ordinals are reference observations, never universal orderings.
Never borrow, impute, silently average, or canonically rank properties. No intake
is authorized now.

## Validation Foundation Before M06

The canonical planned specification is
[`workstreams/empirical_load_evidence_and_validation.md`](workstreams/empirical_load_evidence_and_validation.md).
It authorizes no implementation or intake.

Formal validation remains M09, but its record contracts and split policy must
begin before M06. Distinguish source-example reproduction, regression
reproduction, calibration, in-sample fit, interpolation evaluation,
cross-cartridge evaluation, held-out validation, and external replication.

Future records retain geometry; component/lot and charge identities; conditions;
barrel/chamber; instrument/calibration; pressure quantity/standard; raw
chronograph observations and pressure traces; sampling/timing/filtering;
exclusions; dataset version; calibration/evaluation split; metrics/residuals;
and failures. In-sample reproduction is never out-of-sample validation. This is
pre-M06 infrastructure, not M06 implementation.

## M06-M08 Modeling Sequence

M06 admits one documented pressure/velocity baseline at a time; M07 addresses
burn progression/burnout; M08 addresses muzzle pressure and secondary analytical
objectives. Each requires its own specification, equation/assumption ledger,
dimensional audit, source/domain, implementation, source examples, sensitivity,
failure inventory, calibration status, independent validation, and review.
Shared physical literature with QuickLOAD/GRT does not establish common
provenance. Empirical corrections remain separate from physical cores. Empirical
load data may constrain/validate only with exact component, lot, firearm,
pressure, velocity, condition, and measurement semantics.

## Uncertainty Workstream

1. Preserve source uncertainty and bounded inputs.
2. Add interval arithmetic only through a separately specified/validated task.
3. Add Monte Carlo only with documented distributions, dependence, sampling,
   and validation.

Keep measurement uncertainty, source rounding, lot and condition variability,
source disagreement, parameter uncertainty, model-form uncertainty, and
prediction uncertainty distinct. An uncertainty interval is not a charge region;
never invent a distribution to enable Monte Carlo.

## Diagnostics And Visualization

Future M03/M04 extensions may diagnose charge-region readiness, fill/expansion
evaluation, model-input/applicability, uncertainty readiness, validation-data
admissibility, and cross-source compatibility. Plots consume accepted records
and diagnostics rather than reimplement decisions. Candidate views include
expansion, region segments, domain boundaries, sensitivity, residuals, and
calibration/validation comparisons. Matplotlib is a reproducible static baseline;
Plotly is a later interactive candidate. Generated plots require input/code/
configuration manifests and hashes. No plotting is authorized now.

## Tooling Direction

Later bounded evaluation may consider Ruff, incremental strict mypy, and one
primary dataframe engine. Polars is a candidate for immutable typed pipelines;
pandas is a candidate where scientific interoperability dominates. Do not adopt
both reflexively. Evaluate style/type burden, CI/runtime, null/dtype semantics,
serialization/plot compatibility, dataset size, and adapters. No dependency or
lockfile change is authorized now.

## Future Web Interface And GRT Intake

The long-term goal includes a web interface that can upload GRT project files as
external evidence. A future adapter must preserve original bytes/hash; record
parser/schema versions; extract without guessing; retain unknown fields; map via
explicit adapter records; distinguish GRT/user/ModernPowley values; report
missing/conflicting/version-dependent/unsupported fields; require explicit
transformations; and never import model behavior merely because a field exists.
The first UI focuses on inspection, provenance, mapping, diagnostics, and
visualization. No web code, upload, parser, or adapter is authorized now.

## Provenance And Hypothesis Logging

Future empirical fits, corrections, variants, and experimental interpretations
require a versioned hypothesis record: ID, claim, motivation, evidence,
assumptions, expected observations, falsification criteria, domain, competing
explanations, calibration/held-out data, results, failures, promotion requirements,
status, and supersession. A fit never silently becomes physical law or a
production model.
