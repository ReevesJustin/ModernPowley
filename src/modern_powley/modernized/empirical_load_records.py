"""Immutable empirical-load evidence records with structural validation only."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from enum import Enum
import re
from typing import Any

from .missing_values import IdentityQualifier, MissingState
from .property_observations import SourceLocator
from .provenance import EvidenceClass, ModelMaturity
from .uncertainty import Uncertainty
from .units import Dimension, Quantity, require_dimension, require_positive


EMPIRICAL_LOAD_EVIDENCE_SCHEMA_ID = "modern_powley.empirical_load_evidence.v1"

_IDENTIFIER = re.compile(r"[A-Za-z][A-Za-z0-9._:-]{0,127}\Z")
_SHA256 = re.compile(r"[0-9a-f]{64}\Z")

_PRESSURE_UNIT_LABELS = {
    "CUP": "CUP",
    "psi": "psi",
    "bar": "bar",
    "MPa": "MPa",
}
_VELOCITY_UNIT_LABELS = {"m/s": "m/s", "ft/s": "ft/s"}


class EmpiricalRecordType(str, Enum):
    SOURCE_CUSTODY = "source_custody"
    LITERAL_LOAD_STATEMENT = "literal_load_statement"
    PHYSICAL_LOAD_CONFIGURATION = "physical_load_configuration"
    SHOT_OBSERVATION = "shot_observation"
    LOAD_SERIES = "load_series"
    PRESSURE_TRACE_METADATA = "pressure_trace_metadata"
    CHRONOGRAPH_SERIES = "chronograph_series"
    AGGREGATE_SUMMARY = "aggregate_summary"


class ActivationState(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class ReviewState(str, Enum):
    UNREVIEWED = "unreviewed"
    REVIEW_REQUIRED = "review_required"
    REVIEWED = "reviewed"
    QUALIFIED = "qualified"


class ReferenceRole(str, Enum):
    SOURCE = "source"
    PARENT = "parent"
    CUSTODY = "custody"
    NORMALIZED_FROM = "normalized_from"
    MEMBER = "member"
    CONFIGURATION = "configuration"
    SHOT = "shot"
    APPARATUS = "apparatus"
    TRACE = "trace"
    METHOD = "method"
    UNDERLYING_TEST = "underlying_test"
    DUPLICATE_PUBLICATION_OF = "duplicate_publication_of"
    PROCESSED_FROM = "processed_from"
    EXTERNAL = "external"


class ExclusionState(str, Enum):
    INCLUDED = "included"
    EXCLUDED = "excluded"
    INVALID = "invalid"
    NOT_APPLICABLE = "not_applicable"


class ComponentKind(str, Enum):
    BULLET = "bullet"
    CASE = "case"
    PRIMER = "primer"


class EquipmentKind(str, Enum):
    LABORATORY = "laboratory"
    OPERATOR = "operator"
    FIREARM = "firearm"
    RECEIVER = "receiver"
    BARREL = "barrel"
    CHAMBER = "chamber"
    THROAT_OR_FREEBORE = "throat_or_freebore"
    INSTRUMENT = "instrument"
    SENSOR = "sensor"
    CHANNEL = "channel"
    CALIBRATION = "calibration"
    STANDARD = "standard"


class SourceDeclarationState(str, Enum):
    LITERAL = "literal"
    AMBIGUOUS = "ambiguous"
    UNRESOLVED = "unresolved"


class PrecisionKind(str, Enum):
    EXACT_AS_REPORTED = "exact_as_reported"
    DECIMAL_PLACES = "decimal_places"
    SIGNIFICANT_DIGITS = "significant_digits"
    SOURCE_ROUNDED = "source_rounded"
    UNKNOWN = "unknown"


class EvidenceUncertaintyKind(str, Enum):
    MEASUREMENT = "measurement"
    INSTRUMENT_RESOLUTION = "instrument_resolution"
    MODEL_FORM = "model_form"
    UNKNOWN = "unknown"
    NOT_REPORTED = "not_reported"
    NOT_APPLICABLE = "not_applicable"
    EXTERNALLY_REFERENCED = "externally_referenced"


class ReportedValueKind(str, Enum):
    CHARGE_MASS = "charge_mass"
    PRESSURE = "pressure"
    VELOCITY = "velocity"
    SAMPLING_RATE = "sampling_rate"
    TIME = "time"
    TEMPERATURE = "temperature"
    OTHER_SOURCE_DEFINED = "other_source_defined"


class PressureQuantity(str, Enum):
    PEAK = "peak"
    MEAN = "mean"
    SOURCE_DECLARED_LIMIT = "source_declared_limit"
    OTHER = "other"
    UNRESOLVED = "unresolved"


class PressureOrigin(str, Enum):
    CRUSHER = "crusher"
    PIEZOELECTRIC_TRANSDUCER = "piezoelectric_transducer"
    STRAIN_DERIVED = "strain_derived"
    MODELED = "modeled"
    UNRESOLVED = "unresolved"


class PressureLocation(str, Enum):
    CHAMBER = "chamber"
    BREECH = "breech"
    CASE_MOUTH = "case_mouth"
    OTHER = "other"
    UNRESOLVED = "unresolved"


class PressureAcquisitionState(str, Enum):
    RAW_MEASUREMENT = "raw_measurement"
    PROCESSED_EXTERNALLY = "processed_externally"
    SOURCE_REPORTED_AGGREGATE = "source_reported_aggregate"
    MODELED = "modeled"
    UNRESOLVED = "unresolved"


class PressureUnit(str, Enum):
    CUP = "CUP"
    PSI = "psi"
    BAR = "bar"
    MEGAPASCAL = "MPa"
    SOURCE_SPECIFIC = "source_specific"
    UNRESOLVED = "unresolved"


class ObservationLevel(str, Enum):
    SHOT = "shot"
    AGGREGATE = "aggregate"


class VelocityQuantity(str, Enum):
    INDIVIDUAL_SHOT_SPEED = "individual_shot_speed"
    SOURCE_REPORTED_MEAN = "source_reported_mean"
    SOURCE_REPORTED_OTHER_AGGREGATE = "source_reported_other_aggregate"


class VelocityCorrectionState(str, Enum):
    RAW = "raw"
    CORRECTED = "corrected"
    MUZZLE_EXTRAPOLATED = "muzzle_extrapolated"
    UNRESOLVED = "unresolved"


class VelocityUnit(str, Enum):
    METRE_PER_SECOND = "m/s"
    FOOT_PER_SECOND = "ft/s"
    SOURCE_SPECIFIC = "source_specific"
    UNRESOLVED = "unresolved"


class ArtifactRetentionState(str, Enum):
    RETAINED = "retained"
    EXTERNAL_NOT_RETAINED = "external_not_retained"


class TraceArtifactState(str, Enum):
    RAW = "raw"
    PROCESSED_EXTERNALLY = "processed_externally"
    DERIVATIVE_TRANSCRIPTION_OR_EXPORT = "derivative_transcription_or_export"
    UNRESOLVED = "unresolved"


class AggregateStatistic(str, Enum):
    MEAN = "mean"
    STANDARD_DEVIATION = "standard_deviation"
    EXTREME_SPREAD = "extreme_spread"
    PEAK = "peak"
    COUNT = "count"
    OTHER = "other"


class AggregateOrigin(str, Enum):
    SOURCE_REPORTED = "source_reported"
    EXTERNALLY_CALCULATED = "externally_calculated"


def _enum(instance: Any, enum_type: type[Enum]) -> Enum:
    return instance if isinstance(instance, enum_type) else enum_type(instance)


def _required_text(value: str, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} is required")


def _identifier(value: str, name: str) -> None:
    if not isinstance(value, str) or _IDENTIFIER.fullmatch(value) is None:
        raise ValueError(f"{name} must match {_IDENTIFIER.pattern}")


def _positive_integer(value: int, name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{name} must be a positive integer")


def _nonnegative_integer(value: int, name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be a non-negative integer")


def _tuple(value: Any) -> tuple[Any, ...]:
    if isinstance(value, tuple):
        return value
    if isinstance(value, list):
        return tuple(value)
    raise TypeError("immutable collection fields require a tuple or list")


def _unique(values: tuple[Any, ...], name: str) -> None:
    if len(values) != len(set(values)):
        raise ValueError(f"{name} must be unique")


def _decimal_text(value: str) -> None:
    _required_text(value, "decimal_text")
    try:
        parsed = Decimal(value)
    except InvalidOperation as error:
        raise ValueError("decimal_text must be a valid decimal number") from error
    if not parsed.is_finite():
        raise ValueError("decimal_text must be finite")


@dataclass(frozen=True, slots=True, kw_only=True)
class ExactRecordReference:
    schema_id: str
    record_type: str
    record_id: str
    version: int | None
    role: ReferenceRole

    def __post_init__(self) -> None:
        _identifier(self.schema_id, "reference schema_id")
        _identifier(self.record_type, "reference record_type")
        _identifier(self.record_id, "reference record_id")
        if self.version is not None:
            _positive_integer(self.version, "reference version")
        object.__setattr__(self, "role", _enum(self.role, ReferenceRole))

    @property
    def identity(self) -> tuple[str, str, str, int | None]:
        return self.schema_id, self.record_type, self.record_id, self.version


@dataclass(frozen=True, slots=True, kw_only=True)
class MissingValue:
    state: MissingState
    explanation: str
    source_references: tuple[ExactRecordReference, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "state", _enum(self.state, MissingState))
        _required_text(self.explanation, "missing-value explanation")
        refs = _tuple(self.source_references)
        object.__setattr__(self, "source_references", refs)
        _unique(tuple(item.identity for item in refs), "missing-value references")


@dataclass(frozen=True, slots=True, kw_only=True)
class ReferenceOrMissing:
    reference: ExactRecordReference | None
    missing: MissingValue | None

    def __post_init__(self) -> None:
        if (self.reference is None) == (self.missing is None):
            raise ValueError("reference-or-missing requires exactly one tagged arm")


@dataclass(frozen=True, slots=True, kw_only=True)
class ReportedPrecision:
    kind: PrecisionKind
    statement: str
    digits: int | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "kind", _enum(self.kind, PrecisionKind))
        _required_text(self.statement, "precision statement")
        needs_digits = self.kind in {
            PrecisionKind.DECIMAL_PLACES,
            PrecisionKind.SIGNIFICANT_DIGITS,
        }
        if needs_digits:
            _positive_integer(self.digits, "precision digits")
        elif self.digits is not None:
            raise ValueError("precision digits apply only to decimal/significant-digit kinds")


@dataclass(frozen=True, slots=True, kw_only=True)
class EvidenceUncertainty:
    kind: EvidenceUncertaintyKind
    description: str
    reference: ExactRecordReference | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "kind", _enum(self.kind, EvidenceUncertaintyKind))
        _required_text(self.description, "uncertainty description")
        if self.kind is EvidenceUncertaintyKind.EXTERNALLY_REFERENCED:
            if self.reference is None:
                raise ValueError("externally referenced uncertainty requires a reference")
        elif self.reference is not None:
            raise ValueError("only externally referenced uncertainty carries a reference")


@dataclass(frozen=True, slots=True, kw_only=True)
class ReportedValue:
    kind: ReportedValueKind
    decimal_text: str
    source_unit_label: str
    source_wording: str
    precision: ReportedPrecision
    uncertainty: EvidenceUncertainty
    source_defined_kind: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "kind", _enum(self.kind, ReportedValueKind))
        _decimal_text(self.decimal_text)
        _required_text(self.source_unit_label, "source unit label")
        _required_text(self.source_wording, "source wording")
        if self.kind is ReportedValueKind.OTHER_SOURCE_DEFINED:
            _required_text(self.source_defined_kind, "source-defined value kind")
        elif self.source_defined_kind is not None:
            raise ValueError("source_defined_kind applies only to other_source_defined")


@dataclass(frozen=True, slots=True, kw_only=True)
class PhysicalQuantityEvidence:
    quantity: Quantity
    source_value_text: str
    precision: ReportedPrecision
    uncertainty: Uncertainty

    def __post_init__(self) -> None:
        _decimal_text(self.source_value_text)
        self.uncertainty.validate_for(self.quantity)


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantityOrMissing:
    value: PhysicalQuantityEvidence | None
    missing: MissingValue | None

    def __post_init__(self) -> None:
        if (self.value is None) == (self.missing is None):
            raise ValueError("quantity-or-missing requires exactly one tagged arm")


@dataclass(frozen=True, slots=True, kw_only=True)
class ReviewContext:
    created_by: str
    created_at: str
    state: ReviewState
    reviewed_by: IdentityQualifier
    reviewed_at: IdentityQualifier
    notes: str

    def __post_init__(self) -> None:
        _identifier(self.created_by, "created_by")
        _required_text(self.created_at, "created_at")
        object.__setattr__(self, "state", _enum(self.state, ReviewState))
        if self.state in {ReviewState.REVIEWED, ReviewState.QUALIFIED}:
            if self.reviewed_by.value is None or self.reviewed_at.value is None:
                raise ValueError("reviewed records require reviewer and review time")
        elif self.reviewed_by.value is not None or self.reviewed_at.value is not None:
            raise ValueError("unreviewed records cannot carry completed review identity")


@dataclass(frozen=True, slots=True, kw_only=True)
class LineageLink:
    role: ReferenceRole
    reference: ExactRecordReference
    statement: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "role", _enum(self.role, ReferenceRole))
        if self.reference.role is not self.role:
            raise ValueError("lineage role must match exact-reference role")
        _required_text(self.statement, "lineage statement")


@dataclass(frozen=True, slots=True, kw_only=True)
class ConflictGroup:
    conflict_id: str
    subject: str
    members: tuple[ExactRecordReference, ...]
    explanation: str

    def __post_init__(self) -> None:
        _identifier(self.conflict_id, "conflict_id")
        _required_text(self.subject, "conflict subject")
        _required_text(self.explanation, "conflict explanation")
        members = _tuple(self.members)
        object.__setattr__(self, "members", members)
        if len(members) < 2:
            raise ValueError("conflict group requires at least two members")
        _unique(tuple(item.identity for item in members), "conflict members")
        if any(item.version is None for item in members):
            raise ValueError("conflict members require exact record versions")


@dataclass(frozen=True, slots=True, kw_only=True)
class Exclusion:
    state: ExclusionState
    reason: IdentityQualifier
    authority: IdentityQualifier
    review_context: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "state", _enum(self.state, ExclusionState))
        _required_text(self.review_context, "exclusion review context")
        excluded = self.state in {ExclusionState.EXCLUDED, ExclusionState.INVALID}
        if excluded and (self.reason.value is None or self.authority.value is None):
            raise ValueError("excluded or invalid observations require reason and authority")
        if not excluded and (self.reason.value is not None or self.authority.value is not None):
            raise ValueError("included/not-applicable exclusion cannot carry exclusion facts")


@dataclass(frozen=True, slots=True, kw_only=True)
class RecordEnvelope:
    record_type: EmpiricalRecordType
    record_id: str
    record_version: int
    activation: ActivationState
    evidence_class: EvidenceClass
    model_maturity: ModelMaturity
    review: ReviewContext
    source_references: tuple[ExactRecordReference, ...]
    parent_references: tuple[ExactRecordReference, ...]
    lineage: tuple[LineageLink, ...]
    conflicts: tuple[ConflictGroup, ...]
    supersedes: ExactRecordReference | None
    synthetic_fixture: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "record_type", _enum(self.record_type, EmpiricalRecordType))
        object.__setattr__(self, "activation", _enum(self.activation, ActivationState))
        object.__setattr__(self, "evidence_class", _enum(self.evidence_class, EvidenceClass))
        object.__setattr__(self, "model_maturity", _enum(self.model_maturity, ModelMaturity))
        _identifier(self.record_id, "record_id")
        _positive_integer(self.record_version, "record_version")
        if not isinstance(self.synthetic_fixture, bool):
            raise TypeError("synthetic_fixture must be a Boolean")
        for field in ("source_references", "parent_references", "lineage", "conflicts"):
            object.__setattr__(self, field, _tuple(getattr(self, field)))
        _unique(tuple(item.identity for item in self.source_references), "source references")
        _unique(tuple(item.identity for item in self.parent_references), "parent references")
        _unique(tuple((item.role, item.reference.identity) for item in self.lineage), "lineage links")
        _unique(tuple(item.conflict_id for item in self.conflicts), "conflict groups")
        if any(item.role is not ReferenceRole.SOURCE for item in self.source_references):
            raise ValueError("source references require source role")
        if any(item.role is not ReferenceRole.PARENT for item in self.parent_references):
            raise ValueError("parent references require parent role")
        if self.supersedes is not None:
            if (
                self.supersedes.schema_id != EMPIRICAL_LOAD_EVIDENCE_SCHEMA_ID
                or self.supersedes.record_type != self.record_type.value
                or self.supersedes.version is None
                or self.supersedes.role is not ReferenceRole.PARENT
            ):
                raise ValueError("supersession requires an exact prior Phase 1 record version")
            if self.supersedes.identity == (
                EMPIRICAL_LOAD_EVIDENCE_SCHEMA_ID,
                self.record_type.value,
                self.record_id,
                self.record_version,
            ):
                raise ValueError("record cannot supersede itself")


@dataclass(frozen=True, slots=True, kw_only=True)
class ScopedComponentIdentity:
    component_id: str
    kind: ComponentKind
    manufacturer: IdentityQualifier
    product_designation: IdentityQualifier
    revision: IdentityQualifier
    lot: IdentityQualifier
    source_wording: str
    source_references: tuple[ExactRecordReference, ...]

    def __post_init__(self) -> None:
        _identifier(self.component_id, "component_id")
        object.__setattr__(self, "kind", _enum(self.kind, ComponentKind))
        _required_text(self.source_wording, "component source wording")
        refs = _tuple(self.source_references)
        object.__setattr__(self, "source_references", refs)
        _unique(tuple(item.identity for item in refs), "component source references")
        if self.manufacturer.value is None and self.product_designation.value is not None:
            raise ValueError("component product designation cannot stand without manufacturer identity")


@dataclass(frozen=True, slots=True, kw_only=True)
class PowderIdentityReference:
    reference: ExactRecordReference
    lot: IdentityQualifier

    def __post_init__(self) -> None:
        if self.reference.schema_id != "modern_powley.m02.v1":
            raise ValueError("powder identity must reference the M02 schema")
        if self.reference.record_type != "powder_identity":
            raise ValueError("powder reference must identify an M02 powder_identity record")
        if self.reference.role is not ReferenceRole.PARENT or self.reference.version is None:
            raise ValueError("powder identity requires exact parent reference and version")


@dataclass(frozen=True, slots=True, kw_only=True)
class EquipmentIdentity:
    equipment_id: str
    kind: EquipmentKind
    organization: IdentityQualifier
    designation: IdentityQualifier
    revision: IdentityQualifier
    source_wording: str

    def __post_init__(self) -> None:
        _identifier(self.equipment_id, "equipment_id")
        object.__setattr__(self, "kind", _enum(self.kind, EquipmentKind))
        _required_text(self.source_wording, "equipment source wording")


@dataclass(frozen=True, slots=True, kw_only=True)
class PressureObservation:
    reported_value: ReportedValue
    quantity: PressureQuantity
    origin: PressureOrigin
    location: PressureLocation
    acquisition_state: PressureAcquisitionState
    unit: PressureUnit
    source_unit_label: str
    standard: ReferenceOrMissing
    instrument: ReferenceOrMissing
    sensor: ReferenceOrMissing
    calibration: ReferenceOrMissing
    filtering_state: IdentityQualifier
    peak_definition: IdentityQualifier
    observation_level: ObservationLevel

    def __post_init__(self) -> None:
        for field, enum_type in (
            ("quantity", PressureQuantity), ("origin", PressureOrigin),
            ("location", PressureLocation), ("acquisition_state", PressureAcquisitionState),
            ("unit", PressureUnit), ("observation_level", ObservationLevel),
        ):
            object.__setattr__(self, field, _enum(getattr(self, field), enum_type))
        if self.reported_value.kind is not ReportedValueKind.PRESSURE:
            raise ValueError("pressure observation requires a pressure reported value")
        _required_text(self.source_unit_label, "pressure source unit label")
        if self.source_unit_label != self.reported_value.source_unit_label:
            raise ValueError("pressure unit label must match its reported value")
        expected_label = _PRESSURE_UNIT_LABELS.get(self.unit.value)
        if expected_label is not None and self.source_unit_label != expected_label:
            raise ValueError("controlled pressure unit and source unit label must agree")
        modeled = self.origin is PressureOrigin.MODELED
        if modeled != (self.acquisition_state is PressureAcquisitionState.MODELED):
            raise ValueError("modeled pressure origin and acquisition state must agree")
        if Decimal(self.reported_value.decimal_text) < 0:
            raise ValueError("pressure observation cannot be negative")
        for name in ("standard", "instrument", "sensor", "calibration"):
            item = getattr(self, name)
            if item.reference is not None and item.reference.role is not ReferenceRole.APPARATUS:
                raise ValueError(f"pressure {name} requires apparatus reference role")


@dataclass(frozen=True, slots=True, kw_only=True)
class VelocityObservation:
    reported_value: ReportedValue
    quantity: VelocityQuantity
    correction_state: VelocityCorrectionState
    unit: VelocityUnit
    source_unit_label: str
    measurement_distance: QuantityOrMissing
    correction_method: ReferenceOrMissing
    atmospheric_context: IdentityQualifier
    instrument: ReferenceOrMissing
    firearm: ReferenceOrMissing
    barrel: ReferenceOrMissing
    observation_level: ObservationLevel

    def __post_init__(self) -> None:
        for field, enum_type in (
            ("quantity", VelocityQuantity), ("correction_state", VelocityCorrectionState),
            ("unit", VelocityUnit), ("observation_level", ObservationLevel),
        ):
            object.__setattr__(self, field, _enum(getattr(self, field), enum_type))
        if self.reported_value.kind is not ReportedValueKind.VELOCITY:
            raise ValueError("velocity observation requires a velocity reported value")
        _required_text(self.source_unit_label, "velocity source unit label")
        if self.source_unit_label != self.reported_value.source_unit_label:
            raise ValueError("velocity unit label must match its reported value")
        expected_label = _VELOCITY_UNIT_LABELS.get(self.unit.value)
        if expected_label is not None and self.source_unit_label != expected_label:
            raise ValueError("controlled velocity unit and source unit label must agree")
        if Decimal(self.reported_value.decimal_text) < 0:
            raise ValueError("velocity observation cannot be negative")
        if self.measurement_distance.value is not None:
            require_positive(
                self.measurement_distance.value.quantity,
                Dimension.LENGTH,
                "velocity measurement distance",
            )
        needs_method = self.correction_state in {
            VelocityCorrectionState.CORRECTED,
            VelocityCorrectionState.MUZZLE_EXTRAPOLATED,
        }
        if needs_method != (self.correction_method.reference is not None):
            raise ValueError("corrected/extrapolated velocity requires an exact method reference")
        if self.correction_method.reference is not None and (
            self.correction_method.reference.role is not ReferenceRole.METHOD
            or self.correction_method.reference.version is None
        ):
            raise ValueError("velocity correction requires exact method reference and version")
        for name in ("instrument", "firearm", "barrel"):
            item = getattr(self, name)
            if item.reference is not None and item.reference.role is not ReferenceRole.APPARATUS:
                raise ValueError(f"velocity {name} requires apparatus reference role")


@dataclass(frozen=True, slots=True, kw_only=True)
class ArtifactReference:
    artifact_id: str
    retention_state: ArtifactRetentionState
    sha256: IdentityQualifier
    media_type: str
    custody_reference: ExactRecordReference
    custody_limitation: str

    def __post_init__(self) -> None:
        _identifier(self.artifact_id, "artifact_id")
        object.__setattr__(self, "retention_state", _enum(self.retention_state, ArtifactRetentionState))
        _required_text(self.media_type, "artifact media type")
        _required_text(self.custody_limitation, "artifact custody limitation")
        if self.custody_reference.role is not ReferenceRole.CUSTODY:
            raise ValueError("artifact custody reference requires custody role")
        if self.retention_state is ArtifactRetentionState.RETAINED:
            if self.sha256.value is None or _SHA256.fullmatch(self.sha256.value) is None:
                raise ValueError("retained artifact requires lowercase 64-hex SHA-256")
        elif self.sha256.missing_state is None:
            raise ValueError("external non-retained artifact requires semantic missing hash")


@dataclass(frozen=True, slots=True, kw_only=True)
class ExcludedWindow:
    window_id: str
    source_wording: str
    reason: str

    def __post_init__(self) -> None:
        _identifier(self.window_id, "window_id")
        _required_text(self.source_wording, "excluded-window source wording")
        _required_text(self.reason, "excluded-window reason")


@dataclass(frozen=True, slots=True, kw_only=True)
class OrderedMember:
    position: int
    reference: ExactRecordReference
    source_role: str

    def __post_init__(self) -> None:
        _positive_integer(self.position, "member position")
        _required_text(self.source_role, "member source role")
        if self.reference.role is not ReferenceRole.MEMBER or self.reference.version is None:
            raise ValueError("ordered-member reference requires exact member role and version")


def _validate_members(members: tuple[OrderedMember, ...], name: str) -> None:
    if not members:
        raise ValueError(f"{name} requires at least one member")
    if any(current.position <= previous.position for previous, current in zip(members, members[1:])):
        raise ValueError(f"{name} positions must be strictly ascending in caller order")
    _unique(tuple(item.position for item in members), f"{name} positions")
    _unique(tuple(item.reference.identity for item in members), f"{name} references")


def _validate_envelope(envelope: RecordEnvelope, expected: EmpiricalRecordType) -> None:
    if envelope.record_type is not expected:
        raise ValueError(f"record envelope must declare {expected.value}")


@dataclass(frozen=True, slots=True, kw_only=True)
class SourceCustodyRecord:
    envelope: RecordEnvelope
    source_title: str
    originating_organization: IdentityQualifier
    edition_or_revision: IdentityQualifier
    locator: SourceLocator
    acquisition_context: str
    retention_context: str
    artifacts: tuple[ArtifactReference, ...]
    custody_lineage: tuple[ExactRecordReference, ...]

    def __post_init__(self) -> None:
        _validate_envelope(self.envelope, EmpiricalRecordType.SOURCE_CUSTODY)
        for value, name in ((self.source_title, "source title"), (self.acquisition_context, "acquisition context"), (self.retention_context, "retention context")):
            _required_text(value, name)
        for field in ("artifacts", "custody_lineage"):
            object.__setattr__(self, field, _tuple(getattr(self, field)))
        _unique(tuple(item.artifact_id for item in self.artifacts), "source artifacts")
        _unique(tuple(item.identity for item in self.custody_lineage), "custody lineage")
        if any(item.role is not ReferenceRole.CUSTODY for item in self.custody_lineage):
            raise ValueError("custody lineage requires custody reference role")


@dataclass(frozen=True, slots=True, kw_only=True)
class LiteralLoadStatementRecord:
    envelope: RecordEnvelope
    source_reference: ExactRecordReference
    locator: SourceLocator
    exact_source_wording: str
    source_declared_component_wording: tuple[str, ...]
    declared_values: tuple[ReportedValue, ...]
    qualifications: tuple[str, ...]
    conditions: tuple[str, ...]
    declaration_state: SourceDeclarationState
    unresolved_wording: IdentityQualifier
    normalized_record_references: tuple[ExactRecordReference, ...]

    def __post_init__(self) -> None:
        _validate_envelope(self.envelope, EmpiricalRecordType.LITERAL_LOAD_STATEMENT)
        if self.source_reference.role is not ReferenceRole.SOURCE:
            raise ValueError("literal statement requires an exact source reference")
        _required_text(self.exact_source_wording, "exact source wording")
        object.__setattr__(self, "declaration_state", _enum(self.declaration_state, SourceDeclarationState))
        for field in ("source_declared_component_wording", "declared_values", "qualifications", "conditions", "normalized_record_references"):
            values = _tuple(getattr(self, field))
            object.__setattr__(self, field, values)
        if any(not isinstance(item, str) or not item.strip() for item in self.source_declared_component_wording + self.qualifications + self.conditions):
            raise ValueError("literal statement text collections must be nonblank")
        _unique(tuple(item.identity for item in self.normalized_record_references), "normalized record references")
        if any(item.role is not ReferenceRole.NORMALIZED_FROM for item in self.normalized_record_references):
            raise ValueError("normalized record references require normalized_from role")
        unresolved = self.declaration_state in {SourceDeclarationState.AMBIGUOUS, SourceDeclarationState.UNRESOLVED}
        if unresolved != (self.unresolved_wording.value is not None):
            raise ValueError("ambiguous/unresolved declaration requires explicit wording detail")


@dataclass(frozen=True, slots=True, kw_only=True)
class PhysicalLoadConfigurationRecord:
    envelope: RecordEnvelope
    cartridge_designation: IdentityQualifier
    powder: PowderIdentityReference
    bullet: ScopedComponentIdentity
    case: ScopedComponentIdentity
    primer: ScopedComponentIdentity
    charge: QuantityOrMissing
    geometry_references: tuple[ExactRecordReference, ...]
    equipment: tuple[EquipmentIdentity, ...]
    preparation: tuple[str, ...]
    conditions: tuple[str, ...]
    exclusion: Exclusion

    def __post_init__(self) -> None:
        _validate_envelope(self.envelope, EmpiricalRecordType.PHYSICAL_LOAD_CONFIGURATION)
        expected = (ComponentKind.BULLET, ComponentKind.CASE, ComponentKind.PRIMER)
        if (self.bullet.kind, self.case.kind, self.primer.kind) != expected:
            raise ValueError("bullet, case, and primer assertions must retain their scoped kinds")
        if self.charge.value is not None:
            require_positive(self.charge.value.quantity, Dimension.MASS, "charge mass")
        for field in ("geometry_references", "equipment", "preparation", "conditions"):
            object.__setattr__(self, field, _tuple(getattr(self, field)))
        _unique(tuple(item.identity for item in self.geometry_references), "geometry references")
        if any(item.role is not ReferenceRole.PARENT for item in self.geometry_references):
            raise ValueError("geometry references require parent role")
        _unique(tuple(item.equipment_id for item in self.equipment), "equipment identities")
        if any(not item.strip() for item in self.preparation + self.conditions):
            raise ValueError("preparation and conditions must be nonblank")


@dataclass(frozen=True, slots=True, kw_only=True)
class ShotObservationRecord:
    envelope: RecordEnvelope
    load_configuration_reference: ExactRecordReference
    acquisition_sequence: int
    acquisition_timestamp: IdentityQualifier
    apparatus_references: tuple[ExactRecordReference, ...]
    conditions: tuple[str, ...]
    pressure_observations: tuple[PressureObservation, ...]
    pressure_missing: MissingValue | None
    velocity_observations: tuple[VelocityObservation, ...]
    velocity_missing: MissingValue | None
    trace_references: tuple[ExactRecordReference, ...]
    exclusion: Exclusion
    underlying_test_reference: ReferenceOrMissing

    def __post_init__(self) -> None:
        _validate_envelope(self.envelope, EmpiricalRecordType.SHOT_OBSERVATION)
        if (
            self.load_configuration_reference.schema_id != EMPIRICAL_LOAD_EVIDENCE_SCHEMA_ID
            or self.load_configuration_reference.record_type
            != EmpiricalRecordType.PHYSICAL_LOAD_CONFIGURATION.value
            or self.load_configuration_reference.version is None
            or self.load_configuration_reference.role is not ReferenceRole.CONFIGURATION
        ):
            raise ValueError("shot requires exact Phase 1 load-configuration reference")
        _positive_integer(self.acquisition_sequence, "acquisition sequence")
        for field in ("apparatus_references", "conditions", "pressure_observations", "velocity_observations", "trace_references"):
            object.__setattr__(self, field, _tuple(getattr(self, field)))
        if bool(self.pressure_observations) == (self.pressure_missing is not None):
            raise ValueError("shot pressure requires observations or one missing assertion")
        if bool(self.velocity_observations) == (self.velocity_missing is not None):
            raise ValueError("shot velocity requires observations or one missing assertion")
        if any(item.observation_level is not ObservationLevel.SHOT for item in self.pressure_observations + self.velocity_observations):
            raise ValueError("shot observations require shot-level pressure and velocity")
        _unique(tuple(item.identity for item in self.apparatus_references), "shot apparatus references")
        _unique(tuple(item.identity for item in self.trace_references), "shot trace references")
        if any(item.role is not ReferenceRole.APPARATUS for item in self.apparatus_references):
            raise ValueError("shot apparatus references require apparatus role")
        if any(item.role is not ReferenceRole.TRACE for item in self.trace_references):
            raise ValueError("shot trace references require trace role")
        if any(item.version is None for item in self.trace_references):
            raise ValueError("shot trace references require exact versions")
        if (
            self.underlying_test_reference.reference is not None
            and self.underlying_test_reference.reference.role is not ReferenceRole.UNDERLYING_TEST
        ):
            raise ValueError("underlying test requires underlying_test reference role")
        if any(not item.strip() for item in self.conditions):
            raise ValueError("shot conditions must be nonblank")


@dataclass(frozen=True, slots=True, kw_only=True)
class LoadSeriesRecord:
    envelope: RecordEnvelope
    members: tuple[OrderedMember, ...]
    purpose: str
    ordering_variable: IdentityQualifier
    changed_variables: tuple[str, ...]
    controlled_variables: tuple[str, ...]
    stopping_rule: IdentityQualifier
    missing_members: tuple[MissingValue, ...]

    def __post_init__(self) -> None:
        _validate_envelope(self.envelope, EmpiricalRecordType.LOAD_SERIES)
        _required_text(self.purpose, "series purpose")
        for field in ("members", "changed_variables", "controlled_variables", "missing_members"):
            object.__setattr__(self, field, _tuple(getattr(self, field)))
        _validate_members(self.members, "load series")
        if any(not item.strip() for item in self.changed_variables + self.controlled_variables):
            raise ValueError("series variable descriptions must be nonblank")


@dataclass(frozen=True, slots=True, kw_only=True)
class PressureTraceMetadataRecord:
    envelope: RecordEnvelope
    artifact: ArtifactReference
    shot_reference: ExactRecordReference
    instrument: ReferenceOrMissing
    sensor: ReferenceOrMissing
    channel: ReferenceOrMissing
    sampling_rate: ReportedValue | MissingValue
    time_base: IdentityQualifier
    trigger_metadata: IdentityQualifier
    alignment_metadata: IdentityQualifier
    pressure_quantity: PressureQuantity
    pressure_location: PressureLocation
    calibration: ReferenceOrMissing
    artifact_state: TraceArtifactState
    processing_method: ExactRecordReference | None
    excluded_windows: tuple[ExcludedWindow, ...]

    def __post_init__(self) -> None:
        _validate_envelope(self.envelope, EmpiricalRecordType.PRESSURE_TRACE_METADATA)
        if (
            self.shot_reference.schema_id != EMPIRICAL_LOAD_EVIDENCE_SCHEMA_ID
            or self.shot_reference.role is not ReferenceRole.SHOT
            or self.shot_reference.record_type != EmpiricalRecordType.SHOT_OBSERVATION.value
            or self.shot_reference.version is None
        ):
            raise ValueError("trace shot reference requires exact Phase 1 shot role and version")
        object.__setattr__(self, "pressure_quantity", _enum(self.pressure_quantity, PressureQuantity))
        object.__setattr__(self, "pressure_location", _enum(self.pressure_location, PressureLocation))
        object.__setattr__(self, "artifact_state", _enum(self.artifact_state, TraceArtifactState))
        if not isinstance(self.sampling_rate, (ReportedValue, MissingValue)):
            raise TypeError("trace sampling rate requires reported value or semantic missingness")
        if isinstance(self.sampling_rate, ReportedValue) and self.sampling_rate.kind is not ReportedValueKind.SAMPLING_RATE:
            raise ValueError("trace sampling rate requires sampling_rate reported-value kind")
        if isinstance(self.sampling_rate, ReportedValue) and Decimal(self.sampling_rate.decimal_text) <= 0:
            raise ValueError("trace sampling rate must be greater than zero")
        processed = self.artifact_state in {
            TraceArtifactState.PROCESSED_EXTERNALLY,
            TraceArtifactState.DERIVATIVE_TRANSCRIPTION_OR_EXPORT,
        }
        if processed != (self.processing_method is not None):
            raise ValueError("processed/derivative trace metadata requires an external method")
        if self.processing_method is not None and (
            self.processing_method.role is not ReferenceRole.METHOD
            or self.processing_method.version is None
        ):
            raise ValueError("trace processing method requires exact method role and version")
        for name in ("instrument", "sensor", "channel", "calibration"):
            item = getattr(self, name)
            if item.reference is not None and item.reference.role is not ReferenceRole.APPARATUS:
                raise ValueError(f"trace {name} requires apparatus reference role")
        windows = _tuple(self.excluded_windows)
        object.__setattr__(self, "excluded_windows", windows)
        _unique(tuple(item.window_id for item in windows), "excluded trace windows")


@dataclass(frozen=True, slots=True, kw_only=True)
class ChronographSeriesRecord:
    envelope: RecordEnvelope
    members: tuple[OrderedMember, ...]
    instrument: ReferenceOrMissing
    setup: str
    measurement_distance: QuantityOrMissing
    correction_state: VelocityCorrectionState
    correction_method: ExactRecordReference | None
    atmospheric_context: IdentityQualifier
    firearm: ReferenceOrMissing
    barrel: ReferenceOrMissing
    missing_measurements: tuple[MissingValue, ...]
    precision: ReportedPrecision
    uncertainty: EvidenceUncertainty

    def __post_init__(self) -> None:
        _validate_envelope(self.envelope, EmpiricalRecordType.CHRONOGRAPH_SERIES)
        for field in ("members", "missing_measurements"):
            object.__setattr__(self, field, _tuple(getattr(self, field)))
        _validate_members(self.members, "chronograph series")
        _required_text(self.setup, "chronograph setup")
        if self.measurement_distance.value is not None:
            require_positive(self.measurement_distance.value.quantity, Dimension.LENGTH, "chronograph distance")
        object.__setattr__(self, "correction_state", _enum(self.correction_state, VelocityCorrectionState))
        corrected = self.correction_state in {VelocityCorrectionState.CORRECTED, VelocityCorrectionState.MUZZLE_EXTRAPOLATED}
        if corrected != (self.correction_method is not None):
            raise ValueError("corrected/extrapolated chronograph series requires method")
        if self.correction_method is not None and (
            self.correction_method.role is not ReferenceRole.METHOD
            or self.correction_method.version is None
        ):
            raise ValueError("chronograph correction method requires exact method role and version")
        for name in ("instrument", "firearm", "barrel"):
            item = getattr(self, name)
            if item.reference is not None and item.reference.role is not ReferenceRole.APPARATUS:
                raise ValueError(f"chronograph {name} requires apparatus reference role")


AggregateValue = ReportedValue | PressureObservation | VelocityObservation


@dataclass(frozen=True, slots=True, kw_only=True)
class AggregateSummaryRecord:
    envelope: RecordEnvelope
    statistic: AggregateStatistic
    statistic_definition: str
    calculation_origin: AggregateOrigin
    calculation_method: ExactRecordReference | None
    value: AggregateValue
    member_references: tuple[ExactRecordReference, ...]
    membership_missing: MissingValue | None
    exclusions: tuple[ExactRecordReference, ...]
    source_wording: str
    precision: ReportedPrecision
    uncertainty: EvidenceUncertainty

    def __post_init__(self) -> None:
        _validate_envelope(self.envelope, EmpiricalRecordType.AGGREGATE_SUMMARY)
        object.__setattr__(self, "statistic", _enum(self.statistic, AggregateStatistic))
        object.__setattr__(self, "calculation_origin", _enum(self.calculation_origin, AggregateOrigin))
        _required_text(self.statistic_definition, "statistic definition")
        _required_text(self.source_wording, "aggregate source wording")
        for field in ("member_references", "exclusions"):
            object.__setattr__(self, field, _tuple(getattr(self, field)))
        if bool(self.member_references) == (self.membership_missing is not None):
            raise ValueError("aggregate requires exact members or semantic missing membership")
        _unique(tuple(item.identity for item in self.member_references), "aggregate members")
        _unique(tuple(item.identity for item in self.exclusions), "aggregate exclusions")
        if any(
            item.role is not ReferenceRole.MEMBER or item.version is None
            for item in self.member_references + self.exclusions
        ):
            raise ValueError("aggregate members and exclusions require exact member role and version")
        external = self.calculation_origin is AggregateOrigin.EXTERNALLY_CALCULATED
        if external != (self.calculation_method is not None):
            raise ValueError("externally calculated aggregate requires exact method/version")
        if self.calculation_method is not None and (
            self.calculation_method.role is not ReferenceRole.METHOD
            or self.calculation_method.version is None
        ):
            raise ValueError("aggregate method requires exact method role and version")
        if not isinstance(self.value, (ReportedValue, PressureObservation, VelocityObservation)):
            raise TypeError("aggregate value must be an authorized reported-value type")
        if isinstance(self.value, (PressureObservation, VelocityObservation)) and self.value.observation_level is not ObservationLevel.AGGREGATE:
            raise ValueError("aggregate pressure/velocity values require aggregate level")


EmpiricalLoadEvidenceRecord = (
    SourceCustodyRecord
    | LiteralLoadStatementRecord
    | PhysicalLoadConfigurationRecord
    | ShotObservationRecord
    | LoadSeriesRecord
    | PressureTraceMetadataRecord
    | ChronographSeriesRecord
    | AggregateSummaryRecord
)


RECORD_CLASS_BY_TYPE = {
    EmpiricalRecordType.SOURCE_CUSTODY: SourceCustodyRecord,
    EmpiricalRecordType.LITERAL_LOAD_STATEMENT: LiteralLoadStatementRecord,
    EmpiricalRecordType.PHYSICAL_LOAD_CONFIGURATION: PhysicalLoadConfigurationRecord,
    EmpiricalRecordType.SHOT_OBSERVATION: ShotObservationRecord,
    EmpiricalRecordType.LOAD_SERIES: LoadSeriesRecord,
    EmpiricalRecordType.PRESSURE_TRACE_METADATA: PressureTraceMetadataRecord,
    EmpiricalRecordType.CHRONOGRAPH_SERIES: ChronographSeriesRecord,
    EmpiricalRecordType.AGGREGATE_SUMMARY: AggregateSummaryRecord,
}
