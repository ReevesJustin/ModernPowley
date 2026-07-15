"""Immutable provenance-aware M01 physical records."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from .provenance import Provenance
from .uncertainty import Uncertainty
from .units import Dimension, Quantity, require_dimension, require_positive

SCHEMA_ID = "modern_powley.m01.v1"


class CaseCondition(str, Enum):
    """Controlled physical state of a case during capacity measurement."""
    FIRED_UNSIZED = "fired_unsized"
    FIRED_RESIZED = "fired_resized"
    NEW_UNFIRED = "new_unfired"
    OTHER = "other"
    UNKNOWN = "unknown"


class PrimerPocketTreatment(str, Enum):
    """Declared inclusion or treatment of primer-pocket volume."""
    INCLUDED = "included"
    EXCLUDED = "excluded"
    FILLED = "filled"
    SEALED = "sealed"
    UNKNOWN = "unknown"


class CapacityFillBoundary(str, Enum):
    """Boundary to which a water-capacity measurement is filled."""
    CASE_MOUTH = "case_mouth"
    BOTTOM_OF_FLASH_HOLE = "bottom_of_flash_hole"
    SEATED_PROJECTILE_BOUNDARY = "seated_projectile_boundary"
    OTHER = "other"
    UNKNOWN = "unknown"


class GeometryAdequacy(str, Enum):
    """Applicability of the declared simplified projectile geometry."""
    ADEQUATE_FOR_DECLARED_MODEL = "adequate_for_declared_model"
    PARTIAL = "partial"
    OUTSIDE_MODEL = "outside_model"
    UNKNOWN = "unknown"


class DiameterConvention(str, Enum):
    """Physical diameter identity selected for an area calculation."""
    BORE = "bore"
    GROOVE = "groove"
    PROJECTILE = "projectile"
    EXPLICIT_EFFECTIVE = "explicitly_supplied_effective_diameter"


class SeatingDepthKind(str, Enum):
    """Whether seating depth was supplied directly or derived."""
    DIRECT = "direct"
    DERIVED = "derived"


class UncertaintyTreatment(str, Enum):
    """Treatment applied to uncertainty in a supplied or derived value."""
    SUPPLIED = "supplied"
    UNRESOLVED = "unresolved"
    CONSERVATIVE_BOUND = "conservative_bound"
    PROPAGATED = "propagated"


def _nonblank(value: str, name: str) -> str:
    value = str(value).strip()
    if not value:
        raise ValueError(f"{name} is required")
    return value


def _enum(value: Any, enum_type: type[Enum]) -> Enum:
    return value if isinstance(value, enum_type) else enum_type(value)


def _detail_required(value: Enum, detail: str, name: str) -> None:
    if value.value == "other" and not detail.strip():
        raise ValueError(f"{name} detail is required for OTHER")


def _strict(data: Mapping[str, Any], required: set[str], optional: set[str] = set()) -> None:
    if not required <= set(data) or set(data) - required - optional:
        raise ValueError(f"malformed fields; required={sorted(required)} optional={sorted(optional)}")


def _record_header(record_type: str, record_id: str) -> dict[str, object]:
    return {"schema": SCHEMA_ID, "record_type": record_type, "record_id": record_id}


def _validate_header(data: Mapping[str, Any], record_type: str, fields: set[str]) -> None:
    _strict(data, {"schema", "record_type", "record_id"} | fields)
    if data["schema"] != SCHEMA_ID:
        raise ValueError(f"unsupported schema: {data['schema']!r}")
    if data["record_type"] != record_type:
        raise ValueError(f"expected record_type {record_type}")


@dataclass(frozen=True, slots=True)
class PhysicalValue:
    """A dimensional quantity with provenance and explicit uncertainty."""
    record_id: str
    quantity: Quantity
    provenance: Provenance
    uncertainty: Uncertainty
    uncertainty_treatment: UncertaintyTreatment = UncertaintyTreatment.SUPPLIED
    notes: str = ""

    def __post_init__(self) -> None:
        _nonblank(self.record_id, "physical value record_id")
        self.uncertainty.validate_for(self.quantity)
        object.__setattr__(
            self,
            "uncertainty_treatment",
            _enum(self.uncertainty_treatment, UncertaintyTreatment),
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "record_id": self.record_id,
            "quantity": self.quantity.to_dict(),
            "provenance": self.provenance.to_dict(),
            "uncertainty": self.uncertainty.to_dict(),
            "uncertainty_treatment": self.uncertainty_treatment.value,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> PhysicalValue:
        required = {"record_id", "quantity", "provenance", "uncertainty", "uncertainty_treatment", "notes"}
        _strict(data, required)
        return cls(
            str(data["record_id"]),
            Quantity.from_dict(data["quantity"]),
            Provenance.from_dict(data["provenance"]),
            Uncertainty.from_dict(data["uncertainty"]),
            UncertaintyTreatment(str(data["uncertainty_treatment"])),
            str(data["notes"]),
        )


@dataclass(frozen=True, slots=True)
class MeasurementConditions:
    """Controlled conditions for a water-capacity record."""
    case_condition: CaseCondition
    primer_pocket_treatment: PrimerPocketTreatment
    fill_boundary: CapacityFillBoundary
    water_condition: str
    case_condition_detail: str = ""
    fill_boundary_detail: str = ""
    water_temperature: PhysicalValue | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "case_condition", _enum(self.case_condition, CaseCondition))
        object.__setattr__(
            self,
            "primer_pocket_treatment",
            _enum(self.primer_pocket_treatment, PrimerPocketTreatment),
        )
        object.__setattr__(self, "fill_boundary", _enum(self.fill_boundary, CapacityFillBoundary))
        _detail_required(self.case_condition, self.case_condition_detail, "case condition")
        _detail_required(self.fill_boundary, self.fill_boundary_detail, "fill boundary")
        _nonblank(self.water_condition, "water_condition")
        if self.water_temperature is not None:
            require_dimension(
                self.water_temperature.quantity,
                Dimension.TEMPERATURE,
                "water_temperature",
            )

    def to_dict(self) -> dict[str, object]:
        return {
            "case_condition": self.case_condition.value,
            "primer_pocket_treatment": self.primer_pocket_treatment.value,
            "fill_boundary": self.fill_boundary.value,
            "water_condition": self.water_condition,
            "case_condition_detail": self.case_condition_detail,
            "fill_boundary_detail": self.fill_boundary_detail,
            "water_temperature": None if self.water_temperature is None else self.water_temperature.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> MeasurementConditions:
        required = {
            "case_condition", "primer_pocket_treatment", "fill_boundary", "water_condition",
            "case_condition_detail", "fill_boundary_detail", "water_temperature",
        }
        _strict(data, required)
        temperature = data["water_temperature"]
        return cls(
            CaseCondition(str(data["case_condition"])),
            PrimerPocketTreatment(str(data["primer_pocket_treatment"])),
            CapacityFillBoundary(str(data["fill_boundary"])),
            str(data["water_condition"]),
            str(data["case_condition_detail"]),
            str(data["fill_boundary_detail"]),
            None if temperature is None else PhysicalValue.from_dict(temperature),
        )


@dataclass(frozen=True, slots=True)
class CartridgeIdentity:
    """Stable cartridge identity with optional sourced case length."""

    record_id: str
    designation: str
    provenance: Provenance
    aliases: tuple[str, ...] = ()
    case_length: PhysicalValue | None = None

    def __post_init__(self) -> None:
        _nonblank(self.record_id, "cartridge record_id")
        _nonblank(self.designation, "cartridge designation")
        if self.case_length is not None:
            require_positive(self.case_length.quantity, Dimension.LENGTH, "case length")

    def to_dict(self) -> dict[str, object]:
        return _record_header("cartridge_identity", self.record_id) | {
            "designation": self.designation,
            "aliases": list(self.aliases),
            "provenance": self.provenance.to_dict(),
            "case_length": None if self.case_length is None else self.case_length.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> CartridgeIdentity:
        _validate_header(data, "cartridge_identity", {"designation", "aliases", "provenance", "case_length"})
        aliases = data["aliases"]
        if not isinstance(aliases, list) or not all(isinstance(item, str) for item in aliases):
            raise ValueError("aliases must be a string list")
        return cls(
            str(data["record_id"]),
            str(data["designation"]),
            Provenance.from_dict(data["provenance"]),
            tuple(aliases),
            None if data["case_length"] is None else PhysicalValue.from_dict(data["case_length"]),
        )


@dataclass(frozen=True, slots=True)
class GrossCaseCapacity:
    """Gross fired-case water capacity at declared measurement conditions."""
    record_id: str
    cartridge_id: str
    water_mass: PhysicalValue
    conditions: MeasurementConditions
    water_volume: PhysicalValue | None = None
    conversion_convention_id: str | None = None

    def __post_init__(self) -> None:
        _nonblank(self.record_id, "gross capacity record_id")
        _nonblank(self.cartridge_id, "cartridge_id")
        require_positive(self.water_mass.quantity, Dimension.MASS, "gross water mass")
        if self.water_volume is not None:
            require_positive(self.water_volume.quantity, Dimension.VOLUME, "gross water volume")
            _nonblank(self.conversion_convention_id or "", "conversion_convention_id")
        elif self.conversion_convention_id is not None:
            raise ValueError("conversion convention requires a converted water volume")

    def to_dict(self) -> dict[str, object]:
        return _record_header("gross_case_capacity", self.record_id) | {
            "cartridge_id": self.cartridge_id,
            "water_mass": self.water_mass.to_dict(),
            "water_volume": None if self.water_volume is None else self.water_volume.to_dict(),
            "conversion_convention_id": self.conversion_convention_id,
            "conditions": self.conditions.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> GrossCaseCapacity:
        fields = {"cartridge_id", "water_mass", "water_volume", "conversion_convention_id", "conditions"}
        _validate_header(data, "gross_case_capacity", fields)
        return cls(
            str(data["record_id"]), str(data["cartridge_id"]),
            PhysicalValue.from_dict(data["water_mass"]), MeasurementConditions.from_dict(data["conditions"]),
            None if data["water_volume"] is None else PhysicalValue.from_dict(data["water_volume"]),
            None if data["conversion_convention_id"] is None else str(data["conversion_convention_id"]),
        )


@dataclass(frozen=True, slots=True)
class MeasuredUsablePowderSpace:
    """Measured seating-specific water capacity behind a projectile."""
    record_id: str
    cartridge_id: str
    seated_projectile_id: str
    seating_state: str
    procedure_id: str
    water_mass: PhysicalValue
    conditions: MeasurementConditions
    water_volume: PhysicalValue | None = None
    conversion_convention_id: str | None = None

    def __post_init__(self) -> None:
        for value, name in ((self.record_id, "measured capacity record_id"), (self.cartridge_id, "cartridge_id"), (self.seated_projectile_id, "seated_projectile_id"), (self.seating_state, "seating_state"), (self.procedure_id, "procedure_id")):
            _nonblank(value, name)
        require_positive(self.water_mass.quantity, Dimension.MASS, "usable-space water mass")
        if self.water_volume is not None:
            require_positive(self.water_volume.quantity, Dimension.VOLUME, "usable-space water volume")
            _nonblank(self.conversion_convention_id or "", "conversion_convention_id")
        elif self.conversion_convention_id is not None:
            raise ValueError("conversion convention requires a converted water volume")

    def to_dict(self) -> dict[str, object]:
        return _record_header("measured_usable_powder_space", self.record_id) | {
            "cartridge_id": self.cartridge_id,
            "seated_projectile_id": self.seated_projectile_id,
            "seating_state": self.seating_state,
            "procedure_id": self.procedure_id,
            "water_mass": self.water_mass.to_dict(),
            "water_volume": None if self.water_volume is None else self.water_volume.to_dict(),
            "conversion_convention_id": self.conversion_convention_id,
            "conditions": self.conditions.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> MeasuredUsablePowderSpace:
        fields = {"cartridge_id", "seated_projectile_id", "seating_state", "procedure_id", "water_mass", "water_volume", "conversion_convention_id", "conditions"}
        _validate_header(data, "measured_usable_powder_space", fields)
        return cls(
            str(data["record_id"]), str(data["cartridge_id"]), str(data["seated_projectile_id"]),
            str(data["seating_state"]), str(data["procedure_id"]), PhysicalValue.from_dict(data["water_mass"]),
            MeasurementConditions.from_dict(data["conditions"]),
            None if data["water_volume"] is None else PhysicalValue.from_dict(data["water_volume"]),
            None if data["conversion_convention_id"] is None else str(data["conversion_convention_id"]),
        )


@dataclass(frozen=True, slots=True)
class PrimerPocketVolume:
    """Explicitly measured or sourced primer-pocket volume."""
    record_id: str
    cartridge_id: str
    volume: PhysicalValue
    treatment_basis: PrimerPocketTreatment

    def __post_init__(self) -> None:
        _nonblank(self.record_id, "primer-pocket record_id")
        _nonblank(self.cartridge_id, "cartridge_id")
        require_positive(self.volume.quantity, Dimension.VOLUME, "primer-pocket volume")
        object.__setattr__(self, "treatment_basis", _enum(self.treatment_basis, PrimerPocketTreatment))
        if self.treatment_basis is PrimerPocketTreatment.UNKNOWN:
            raise ValueError("primer-pocket volume requires a known treatment basis")

    def to_dict(self) -> dict[str, object]:
        return _record_header("primer_pocket_volume", self.record_id) | {
            "cartridge_id": self.cartridge_id,
            "volume": self.volume.to_dict(),
            "treatment_basis": self.treatment_basis.value,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> PrimerPocketVolume:
        _validate_header(data, "primer_pocket_volume", {"cartridge_id", "volume", "treatment_basis"})
        return cls(str(data["record_id"]), str(data["cartridge_id"]), PhysicalValue.from_dict(data["volume"]), PrimerPocketTreatment(str(data["treatment_basis"])))


@dataclass(frozen=True, slots=True)
class SeatingDepth:
    """Direct or explicitly derived projectile seating depth."""
    value: PhysicalValue
    kind: SeatingDepthKind
    reference_convention: str
    method_id: str | None = None
    input_record_ids: tuple[str, ...] = ()
    assumptions: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        require_positive(self.value.quantity, Dimension.LENGTH, "seating depth")
        object.__setattr__(self, "kind", _enum(self.kind, SeatingDepthKind))
        _nonblank(self.reference_convention, "seating-depth reference convention")
        if self.kind is SeatingDepthKind.DERIVED:
            if not self.method_id or len(self.input_record_ids) != 3:
                raise ValueError("derived seating depth requires method and three input records")
        elif self.method_id is not None or self.input_record_ids:
            raise ValueError("direct seating depth cannot carry derivation inputs")

    def to_dict(self) -> dict[str, object]:
        return {"value": self.value.to_dict(), "kind": self.kind.value, "reference_convention": self.reference_convention, "method_id": self.method_id, "input_record_ids": list(self.input_record_ids), "assumptions": list(self.assumptions)}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> SeatingDepth:
        fields = {"value", "kind", "reference_convention", "method_id", "input_record_ids", "assumptions"}
        _strict(data, fields)
        if not isinstance(data["input_record_ids"], list) or not isinstance(data["assumptions"], list):
            raise ValueError("seating derivation lists are malformed")
        return cls(PhysicalValue.from_dict(data["value"]), SeatingDepthKind(str(data["kind"])), str(data["reference_convention"]), None if data["method_id"] is None else str(data["method_id"]), tuple(data["input_record_ids"]), tuple(data["assumptions"]))


@dataclass(frozen=True, slots=True)
class ProjectileRecord:
    """Projectile identity and the simplified geometry used by M01."""
    record_id: str
    identity: str
    mass: PhysicalValue
    diameter: PhysicalValue
    geometry_adequacy: GeometryAdequacy
    total_length: PhysicalValue | None = None
    seating_depth: SeatingDepth | None = None
    cartridge_overall_length: PhysicalValue | None = None
    cylindrical_shank_diameter: PhysicalValue | None = None
    boat_tail_length: PhysicalValue | None = None
    boat_tail_base_diameter: PhysicalValue | None = None
    manufacturer: str = ""
    lot: str = ""

    def __post_init__(self) -> None:
        _nonblank(self.record_id, "projectile record_id")
        _nonblank(self.identity, "projectile identity")
        require_positive(self.mass.quantity, Dimension.MASS, "projectile mass")
        require_positive(self.diameter.quantity, Dimension.LENGTH, "projectile diameter")
        object.__setattr__(self, "geometry_adequacy", _enum(self.geometry_adequacy, GeometryAdequacy))
        for value, name in ((self.total_length, "projectile total length"), (self.cartridge_overall_length, "COAL"), (self.cylindrical_shank_diameter, "shank diameter"), (self.boat_tail_length, "boat-tail length"), (self.boat_tail_base_diameter, "boat-tail base diameter")):
            if value is not None:
                require_positive(value.quantity, Dimension.LENGTH, name)
        if (self.boat_tail_length is None) != (self.boat_tail_base_diameter is None):
            raise ValueError("boat-tail length and base diameter must be supplied together")
        if self.boat_tail_base_diameter is not None:
            shank = self.cylindrical_shank_diameter or self.diameter
            if self.boat_tail_base_diameter.quantity.si_value > shank.quantity.si_value:
                raise ValueError("boat-tail base diameter cannot exceed shank diameter")

    def to_dict(self) -> dict[str, object]:
        value = lambda item: None if item is None else item.to_dict()
        return _record_header("projectile", self.record_id) | {
            "identity": self.identity, "manufacturer": self.manufacturer, "lot": self.lot,
            "mass": self.mass.to_dict(), "diameter": self.diameter.to_dict(),
            "geometry_adequacy": self.geometry_adequacy.value, "total_length": value(self.total_length),
            "seating_depth": None if self.seating_depth is None else self.seating_depth.to_dict(),
            "cartridge_overall_length": value(self.cartridge_overall_length),
            "cylindrical_shank_diameter": value(self.cylindrical_shank_diameter),
            "boat_tail_length": value(self.boat_tail_length), "boat_tail_base_diameter": value(self.boat_tail_base_diameter),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> ProjectileRecord:
        fields = {"identity", "manufacturer", "lot", "mass", "diameter", "geometry_adequacy", "total_length", "seating_depth", "cartridge_overall_length", "cylindrical_shank_diameter", "boat_tail_length", "boat_tail_base_diameter"}
        _validate_header(data, "projectile", fields)
        pv = lambda key: None if data[key] is None else PhysicalValue.from_dict(data[key])
        return cls(str(data["record_id"]), str(data["identity"]), PhysicalValue.from_dict(data["mass"]), PhysicalValue.from_dict(data["diameter"]), GeometryAdequacy(str(data["geometry_adequacy"])), pv("total_length"), None if data["seating_depth"] is None else SeatingDepth.from_dict(data["seating_depth"]), pv("cartridge_overall_length"), pv("cylindrical_shank_diameter"), pv("boat_tail_length"), pv("boat_tail_base_diameter"), str(data["manufacturer"]), str(data["lot"]))


@dataclass(frozen=True, slots=True)
class ProjectileTravel:
    """Projectile-base travel between explicit initial and final references."""
    value: PhysicalValue
    initial_reference: str
    final_reference: str

    def __post_init__(self) -> None:
        require_positive(self.value.quantity, Dimension.LENGTH, "projectile travel")
        _nonblank(self.initial_reference, "travel initial_reference")
        _nonblank(self.final_reference, "travel final_reference")

    def to_dict(self) -> dict[str, object]:
        return {"value": self.value.to_dict(), "initial_reference": self.initial_reference, "final_reference": self.final_reference}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> ProjectileTravel:
        _strict(data, {"value", "initial_reference", "final_reference"})
        return cls(PhysicalValue.from_dict(data["value"]), str(data["initial_reference"]), str(data["final_reference"]))


@dataclass(frozen=True, slots=True)
class FirearmRecord:
    """Barrel dimensions, reference points, and pressure-standard metadata."""

    record_id: str
    identity: str
    barrel_length: PhysicalValue
    barrel_length_reference: str
    bore_diameter: PhysicalValue | None = None
    groove_diameter: PhysicalValue | None = None
    effective_diameter: PhysicalValue | None = None
    projectile_travel: ProjectileTravel | None = None
    pressure_standard_identity: str = ""
    pressure_standard_edition: str = ""
    freebore_length: PhysicalValue | None = None
    freebore_reference: str = ""

    def __post_init__(self) -> None:
        _nonblank(self.record_id, "firearm record_id")
        _nonblank(self.identity, "firearm identity")
        require_positive(self.barrel_length.quantity, Dimension.LENGTH, "barrel length")
        _nonblank(self.barrel_length_reference, "barrel_length_reference")
        for value, name in ((self.bore_diameter, "bore diameter"), (self.groove_diameter, "groove diameter"), (self.effective_diameter, "effective diameter")):
            if value is not None:
                require_positive(value.quantity, Dimension.LENGTH, name)
        if self.freebore_length is not None:
            require_positive(self.freebore_length.quantity, Dimension.LENGTH, "freebore length")
            _nonblank(self.freebore_reference, "freebore_reference")
        elif self.freebore_reference:
            raise ValueError("freebore reference requires an explicit freebore length")
        if bool(self.pressure_standard_identity) != bool(self.pressure_standard_edition):
            raise ValueError("pressure-standard identity and edition must be supplied together")

    def diameter_for(self, convention: DiameterConvention) -> PhysicalValue:
        """Return the explicitly requested barrel diameter; never average."""
        convention = DiameterConvention(convention)
        value = {DiameterConvention.BORE: self.bore_diameter, DiameterConvention.GROOVE: self.groove_diameter, DiameterConvention.EXPLICIT_EFFECTIVE: self.effective_diameter}.get(convention)
        if convention is DiameterConvention.PROJECTILE:
            raise ValueError("projectile diameter must come from a ProjectileRecord")
        if value is None:
            raise ValueError(f"{convention.value} is unavailable")
        return value

    def to_dict(self) -> dict[str, object]:
        value = lambda item: None if item is None else item.to_dict()
        return _record_header("firearm", self.record_id) | {
            "identity": self.identity, "barrel_length": self.barrel_length.to_dict(),
            "barrel_length_reference": self.barrel_length_reference, "bore_diameter": value(self.bore_diameter),
            "groove_diameter": value(self.groove_diameter), "effective_diameter": value(self.effective_diameter),
            "projectile_travel": None if self.projectile_travel is None else self.projectile_travel.to_dict(),
            "pressure_standard_identity": self.pressure_standard_identity,
            "pressure_standard_edition": self.pressure_standard_edition,
            "freebore_length": value(self.freebore_length),
            "freebore_reference": self.freebore_reference,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> FirearmRecord:
        fields = {"identity", "barrel_length", "barrel_length_reference", "bore_diameter", "groove_diameter", "effective_diameter", "projectile_travel", "pressure_standard_identity", "pressure_standard_edition", "freebore_length", "freebore_reference"}
        _validate_header(data, "firearm", fields)
        pv = lambda key: None if data[key] is None else PhysicalValue.from_dict(data[key])
        return cls(
            record_id=str(data["record_id"]),
            identity=str(data["identity"]),
            barrel_length=PhysicalValue.from_dict(data["barrel_length"]),
            barrel_length_reference=str(data["barrel_length_reference"]),
            bore_diameter=pv("bore_diameter"),
            groove_diameter=pv("groove_diameter"),
            effective_diameter=pv("effective_diameter"),
            projectile_travel=None if data["projectile_travel"] is None else ProjectileTravel.from_dict(data["projectile_travel"]),
            pressure_standard_identity=str(data["pressure_standard_identity"]),
            pressure_standard_edition=str(data["pressure_standard_edition"]),
            freebore_length=pv("freebore_length"),
            freebore_reference=str(data["freebore_reference"]),
        )


@dataclass(frozen=True, slots=True)
class EstimatedUsablePowderSpace:
    """Derived geometric usable volume, distinct from measured capacity."""
    record_id: str
    cartridge_id: str
    gross_capacity_record_id: str
    projectile_geometry_record_id: str
    usable_volume: PhysicalValue
    displacement_method_id: str
    primer_pocket_treatment: PrimerPocketTreatment
    geometry_adequacy: GeometryAdequacy
    assumptions: tuple[str, ...]
    input_record_ids: tuple[str, ...]
    primer_pocket_correction_record_id: str | None = None
    equivalent_water_mass: PhysicalValue | None = None

    def __post_init__(self) -> None:
        for value, name in ((self.record_id, "estimated capacity record_id"), (self.cartridge_id, "cartridge_id"), (self.gross_capacity_record_id, "gross_capacity_record_id"), (self.projectile_geometry_record_id, "projectile_geometry_record_id"), (self.displacement_method_id, "displacement_method_id")):
            _nonblank(value, name)
        require_positive(self.usable_volume.quantity, Dimension.VOLUME, "estimated usable volume")
        object.__setattr__(self, "primer_pocket_treatment", _enum(self.primer_pocket_treatment, PrimerPocketTreatment))
        object.__setattr__(self, "geometry_adequacy", _enum(self.geometry_adequacy, GeometryAdequacy))
        if self.geometry_adequacy is GeometryAdequacy.OUTSIDE_MODEL:
            raise ValueError("outside-model geometry cannot produce a usable-space estimate")
        if not self.assumptions or not self.input_record_ids:
            raise ValueError("estimated capacity requires assumptions and input identities")
        if self.equivalent_water_mass is not None:
            require_positive(self.equivalent_water_mass.quantity, Dimension.MASS, "equivalent water mass")

    def to_dict(self) -> dict[str, object]:
        return _record_header("estimated_usable_powder_space", self.record_id) | {
            "cartridge_id": self.cartridge_id, "gross_capacity_record_id": self.gross_capacity_record_id,
            "projectile_geometry_record_id": self.projectile_geometry_record_id,
            "usable_volume": self.usable_volume.to_dict(), "displacement_method_id": self.displacement_method_id,
            "primer_pocket_treatment": self.primer_pocket_treatment.value,
            "primer_pocket_correction_record_id": self.primer_pocket_correction_record_id,
            "geometry_adequacy": self.geometry_adequacy.value, "assumptions": list(self.assumptions),
            "input_record_ids": list(self.input_record_ids),
            "equivalent_water_mass": None if self.equivalent_water_mass is None else self.equivalent_water_mass.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> EstimatedUsablePowderSpace:
        fields = {"cartridge_id", "gross_capacity_record_id", "projectile_geometry_record_id", "usable_volume", "displacement_method_id", "primer_pocket_treatment", "primer_pocket_correction_record_id", "geometry_adequacy", "assumptions", "input_record_ids", "equivalent_water_mass"}
        _validate_header(data, "estimated_usable_powder_space", fields)
        if not isinstance(data["assumptions"], list) or not isinstance(data["input_record_ids"], list):
            raise ValueError("estimated capacity lists are malformed")
        return cls(str(data["record_id"]), str(data["cartridge_id"]), str(data["gross_capacity_record_id"]), str(data["projectile_geometry_record_id"]), PhysicalValue.from_dict(data["usable_volume"]), str(data["displacement_method_id"]), PrimerPocketTreatment(str(data["primer_pocket_treatment"])), GeometryAdequacy(str(data["geometry_adequacy"])), tuple(data["assumptions"]), tuple(data["input_record_ids"]), None if data["primer_pocket_correction_record_id"] is None else str(data["primer_pocket_correction_record_id"]), None if data["equivalent_water_mass"] is None else PhysicalValue.from_dict(data["equivalent_water_mass"]))


@dataclass(frozen=True, slots=True)
class CapacityComparison:
    """Diagnostic estimated-minus-measured comparison retaining both IDs."""
    record_id: str
    measured_record_id: str
    estimated_record_id: str
    signed_volume_difference: PhysicalValue

    def __post_init__(self) -> None:
        for value, name in ((self.record_id, "comparison record_id"), (self.measured_record_id, "measured_record_id"), (self.estimated_record_id, "estimated_record_id")):
            _nonblank(value, name)
        require_dimension(self.signed_volume_difference.quantity, Dimension.VOLUME, "capacity difference")

    def to_dict(self) -> dict[str, object]:
        return _record_header("capacity_comparison", self.record_id) | {"measured_record_id": self.measured_record_id, "estimated_record_id": self.estimated_record_id, "signed_volume_difference": self.signed_volume_difference.to_dict()}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> CapacityComparison:
        _validate_header(data, "capacity_comparison", {"measured_record_id", "estimated_record_id", "signed_volume_difference"})
        return cls(str(data["record_id"]), str(data["measured_record_id"]), str(data["estimated_record_id"]), PhysicalValue.from_dict(data["signed_volume_difference"]))
