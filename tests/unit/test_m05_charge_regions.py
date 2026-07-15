from dataclasses import FrozenInstanceError, replace
import math

import pytest

from modern_powley.modernized import (
    ActivationStatus, ChargeMassEndpoint, ChargeMassSegment, ChargeRegionRecord,
    DependencyStatus, EndpointInclusion, EvidenceClass, ExactRecordReference,
    ExactReferenceRole, LifecycleMetadata, MethodReference, ModelMaturity,
    NonImplicationDeclaration, Provenance, RegionBasis, RegionState, SourceLocator,
    PressureEvidenceContext,
    TranscriptionStatus, UncertaintyDeclaration, UncertaintyDeclarationKind,
    Unit, Quantity, ValueOrigin, VersionedRegionReference,
)


def ref(role=ExactReferenceRole.EXTERNAL_LINEAGE, record_id="SYN-M05-REF-1", version=1):
    return ExactRecordReference(role, "synthetic.schema.v1", "synthetic_record", record_id, version, EvidenceClass.OTHER_PUBLISHED_PRIMARY, ModelMaturity.RETAINED_CANDIDATE)


def endpoint(value, unit=Unit.GRAIN, inclusion=EndpointInclusion.INCLUDED):
    return ChargeMassEndpoint(Quantity(value, unit), inclusion, f"SYN-{value}", "synthetic reported precision", (ref(record_id=f"SYN-END-{value}-{unit.value}"),), ("synthetic only",))


def segment(low=10, high=20, *, low_in=EndpointInclusion.INCLUDED, high_in=EndpointInclusion.INCLUDED, unit=Unit.GRAIN):
    return ChargeMassSegment(endpoint(low, unit, low_in), endpoint(high, unit, high_in))


def method():
    return MethodReference("METHOD-M05-SYNTHETIC", 1, ref(record_id="SYN-AUTHORITY"), ModelMaturity.RETAINED_CANDIDATE, "synthetic_not_admitted")


def record(**changes):
    values = dict(
        record_id="SYN-M05-RECORD-1", region_id="SYN-M05-REGION-1", version=1,
        state=RegionState.BOUNDED, basis=RegionBasis.SOURCE_DECLARED_INTERVAL,
        method=method(), segments=(segment(),),
        m01_input_references=(ref(ExactReferenceRole.M01_INPUT, "SYN-M01"),),
        m02_evidence_references=(ref(ExactReferenceRole.M02_EVIDENCE, "SYN-M02"),),
        m03_diagnostic_references=(ref(ExactReferenceRole.M03_DIAGNOSTIC, "SYN-M03"),),
        m04_audit_references=(ref(ExactReferenceRole.M04_AUDIT, "SYN-M04"),),
        applicability_references=(ref(record_id="SYN-DOMAIN"),),
        provenance=Provenance(EvidenceClass.OTHER_PUBLISHED_PRIMARY, ValueOrigin.OTHER_PUBLISHED, "SRC-M05-SYNTHETIC", ModelMaturity.RETAINED_CANDIDATE, notes="synthetic only"),
        source_locator=SourceLocator("SRC-M05-SYNTHETIC", "synthetic locator", TranscriptionStatus.NOT_APPLICABLE),
        source_wording="synthetic bounded analytical record", reported_precision="synthetic precision text",
        conditions=("synthetic condition",), uncertainty=UncertaintyDeclaration(UncertaintyDeclarationKind.UNKNOWN, "synthetic unknown uncertainty"),
        dependency_status=DependencyStatus.UNKNOWN, dependency_references=(), conflict_references=(),
        qualifications=("not load data",), derivation_lineage=(ref(record_id="SYN-LINEAGE"),),
        pressure_contexts=(), lifecycle=LifecycleMetadata(ActivationStatus.ACTIVE), explanation=None,
        non_implication=NonImplicationDeclaration.M05_CANONICAL,
    )
    values.update(changes)
    return ChargeRegionRecord(**values)


def test_records_are_frozen_and_valid_single_disjoint_point_and_mixed_units():
    item = record()
    with pytest.raises(FrozenInstanceError):
        item.version = 2
    disjoint = record(segments=(segment(10, 20), segment(21, 30)))
    assert len(disjoint.segments) == 2
    point = record(segments=(segment(15, 15),))
    assert point.segments[0].lower.quantity.value == 15
    mixed = record(segments=(segment(1, 2, unit=Unit.GRAM), segment(40, 50, unit=Unit.GRAIN)))
    assert mixed.segments[0].lower.quantity.unit is Unit.GRAM


def test_touching_segments_require_shared_value_not_included_twice():
    valid = record(segments=(segment(10, 20, high_in=EndpointInclusion.EXCLUDED), segment(20, 30)))
    assert len(valid.segments) == 2
    with pytest.raises(ValueError, match="shared boundary"):
        record(segments=(segment(10, 20), segment(20, 30)))


@pytest.mark.parametrize("state", [RegionState.EMPTY, RegionState.UNAVAILABLE, RegionState.INDETERMINATE, RegionState.CONFLICTING])
def test_all_nonbounded_states_are_explicit(state):
    common = dict(state=state, segments=(), explanation="synthetic explicit state")
    if state is RegionState.EMPTY:
        item = record(**common)
    elif state is RegionState.INDETERMINATE:
        item = record(**common, basis=None, method=None)
    elif state is RegionState.CONFLICTING:
        item = record(**common, basis=None, method=None, conflict_references=(ref(ExactReferenceRole.M05_REGION, "SYN-CONFLICT-1"), ref(ExactReferenceRole.M05_REGION, "SYN-CONFLICT-2")))
    else:
        item = record(**common, basis=None, method=None)
    assert item.state is state and not item.segments


@pytest.mark.parametrize("value", [0, -1, math.nan, math.inf, -math.inf])
def test_invalid_endpoint_values_fail(value):
    with pytest.raises((ValueError, TypeError)):
        endpoint(value)


def test_nonmass_reversed_and_excluded_point_fail():
    with pytest.raises(ValueError, match="dimension mass"):
        ChargeMassEndpoint(Quantity(1, Unit.INCH), EndpointInclusion.INCLUDED)
    with pytest.raises(ValueError, match="lower bound"):
        segment(20, 10)
    with pytest.raises(ValueError, match="point segment"):
        segment(10, 10, high_in=EndpointInclusion.EXCLUDED)


def test_order_overlap_and_duplicate_segments_fail_without_reordering():
    with pytest.raises(ValueError, match="ascending"):
        record(segments=(segment(20, 30), segment(10, 15)))
    with pytest.raises(ValueError, match="overlap"):
        record(segments=(segment(10, 20), segment(15, 25)))
    with pytest.raises(ValueError, match="ascending"):
        one = segment(10, 20)
        record(segments=(one, one))


def test_state_consistency_and_conflict_uniqueness_fail():
    with pytest.raises(ValueError, match="bounded"):
        record(segments=())
    with pytest.raises(ValueError, match="unavailable"):
        record(state=RegionState.UNAVAILABLE, segments=(), explanation="x")
    conflict = ref(ExactReferenceRole.M05_REGION, "SYN-C")
    with pytest.raises(ValueError, match="two conflicts"):
        record(state=RegionState.CONFLICTING, basis=None, method=None, segments=(), explanation="x", conflict_references=(conflict,))
    with pytest.raises(ValueError, match="unique"):
        record(state=RegionState.CONFLICTING, basis=None, method=None, segments=(), explanation="x", conflict_references=(conflict, conflict))


def test_reference_roles_dependency_uncertainty_and_lifecycle_are_structural():
    with pytest.raises(ValueError, match="wrong exact-reference role"):
        record(m01_input_references=(ref(ExactReferenceRole.M04_AUDIT),))
    with pytest.raises(ValueError, match="method authority"):
        MethodReference("SYN-M", 1, ref(ExactReferenceRole.M04_AUDIT), ModelMaturity.RETAINED_CANDIDATE, "x")
    external = ref(record_id="SYN-UNCERTAINTY")
    uncertainty = UncertaintyDeclaration(UncertaintyDeclarationKind.EXTERNALLY_REFERENCED, "external synthetic uncertainty", (external,))
    item = record(uncertainty=uncertainty, dependency_status=DependencyStatus.EXTERNALLY_REFERENCED, dependency_references=(ref(record_id="SYN-DEPENDENCY"),), lifecycle=LifecycleMetadata(ActivationStatus.INACTIVE, VersionedRegionReference("SYN-M05-REGION-0", 1)))
    assert item.lifecycle.activation is ActivationStatus.INACTIVE and item.lifecycle.supersedes is not None
    with pytest.raises(ValueError, match="supersede itself"):
        record(lifecycle=LifecycleMetadata(ActivationStatus.ACTIVE, VersionedRegionReference("SYN-M05-REGION-1", 1)))


@pytest.mark.parametrize("version", [0, -1, True])
def test_versions_reject_nonpositive_and_boolean(version):
    with pytest.raises(ValueError, match="positive integer"):
        replace(record(), version=version)


def test_non_implication_is_canonical_and_complete():
    text = NonImplicationDeclaration.M05_CANONICAL.statement
    for phrase in ("recommended", "starting", "maximum", "safe range", "loading instruction", "powder suitability", "pressure safety", "velocity prediction", "physical correctness", "every interior point"):
        assert phrase in text


@pytest.mark.parametrize("basis", list(RegionBasis))
def test_every_basis_is_a_noncomputational_round_trip_value(basis):
    assert record(basis=basis).basis is basis


@pytest.mark.parametrize("status", list(DependencyStatus))
def test_dependency_statuses_are_declarative(status):
    references = (ref(record_id="SYN-DEP"),) if status is DependencyStatus.EXTERNALLY_REFERENCED else ()
    assert record(dependency_status=status, dependency_references=references).dependency_status is status


def test_pressure_context_preserves_text_only_metadata():
    pressure = PressureEvidenceContext(
        ref(ExactReferenceRole.M02_EVIDENCE, "SYN-PRESSURE-EVIDENCE"),
        "synthetic pressure quantity", "synthetic method", "synthetic protocol",
        "synthetic instrument", "synthetic source unit label", ("synthetic condition",),
        SourceLocator("SRC-M05-SYNTHETIC", "synthetic pressure locator", TranscriptionStatus.NOT_APPLICABLE),
        ("not a pressure value",),
    )
    item = record(pressure_contexts=(pressure,))
    assert item.pressure_contexts[0].source_unit_label == "synthetic source unit label"
