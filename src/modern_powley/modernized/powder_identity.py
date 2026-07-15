"""Explicit M02 powder identities and directional source assertions."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from .missing_values import IdentityQualifier
from .provenance import Provenance

M02_SCHEMA_ID = "modern_powley.m02.v1"


def _required(value: str, name: str) -> str:
    value = str(value).strip()
    if not value:
        raise ValueError(f"{name} is required")
    return value


def _strict_record(data: Mapping[str, Any], record_type: str, fields: set[str]) -> None:
    expected = {"schema", "record_type", "record_id"} | fields
    if set(data) != expected:
        raise ValueError(f"malformed {record_type} fields")
    if data["schema"] != M02_SCHEMA_ID:
        raise ValueError(f"unsupported schema: {data['schema']!r}")
    if data["record_type"] != record_type:
        raise ValueError(f"expected record_type {record_type}")


class PowderRelationshipKind(str, Enum):
    """Direction and strength of one source-backed powder-name assertion."""

    ASSERTED_IDENTICAL = "asserted_identical"
    RENAMED_TO = "renamed_to"
    RELATED_TO = "related_to"
    REPLACEMENT_FOR = "replacement_for"
    DESCRIBED_AS_SIMILAR_TO = "described_as_similar_to"


@dataclass(frozen=True, slots=True)
class PowderIdentity:
    """A powder identity scoped to its reported organization, lot, and era."""

    record_id: str
    responsible_organization: str
    published_designation: str
    normalized_display_designation: str
    source_specific_designation: str
    product_family: IdentityQualifier
    product_class: IdentityQualifier
    lot_or_batch: IdentityQualifier
    manufacturing_date_or_era: IdentityQualifier
    formulation_or_revision: IdentityQualifier
    country_or_market: IdentityQualifier
    provenance: Provenance

    def __post_init__(self) -> None:
        for value, name in (
            (self.record_id, "powder record_id"),
            (self.responsible_organization, "responsible organization"),
            (self.published_designation, "published designation"),
            (self.normalized_display_designation, "normalized display designation"),
            (self.source_specific_designation, "source-specific designation"),
        ):
            _required(value, name)

    def to_dict(self) -> dict[str, object]:
        return {
            "schema": M02_SCHEMA_ID,
            "record_type": "powder_identity",
            "record_id": self.record_id,
            "responsible_organization": self.responsible_organization,
            "published_designation": self.published_designation,
            "normalized_display_designation": self.normalized_display_designation,
            "source_specific_designation": self.source_specific_designation,
            "product_family": self.product_family.to_dict(),
            "product_class": self.product_class.to_dict(),
            "lot_or_batch": self.lot_or_batch.to_dict(),
            "manufacturing_date_or_era": self.manufacturing_date_or_era.to_dict(),
            "formulation_or_revision": self.formulation_or_revision.to_dict(),
            "country_or_market": self.country_or_market.to_dict(),
            "provenance": self.provenance.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> PowderIdentity:
        fields = {
            "responsible_organization", "published_designation",
            "normalized_display_designation", "source_specific_designation",
            "product_family", "product_class", "lot_or_batch", "manufacturing_date_or_era",
            "formulation_or_revision", "country_or_market", "provenance",
        }
        _strict_record(data, "powder_identity", fields)
        return cls(
            str(data["record_id"]), str(data["responsible_organization"]),
            str(data["published_designation"]), str(data["normalized_display_designation"]),
            str(data["source_specific_designation"]),
            IdentityQualifier.from_dict(data["product_family"]),
            IdentityQualifier.from_dict(data["product_class"]),
            IdentityQualifier.from_dict(data["lot_or_batch"]),
            IdentityQualifier.from_dict(data["manufacturing_date_or_era"]),
            IdentityQualifier.from_dict(data["formulation_or_revision"]),
            IdentityQualifier.from_dict(data["country_or_market"]),
            Provenance.from_dict(data["provenance"]),
        )


@dataclass(frozen=True, slots=True)
class PowderIdentityRelationship:
    """A directional, provenance-backed assertion between identity records."""

    record_id: str
    subject_powder_id: str
    relationship: PowderRelationshipKind
    object_powder_id: str
    source_wording: str
    source_locator: str
    provenance: Provenance

    def __post_init__(self) -> None:
        object.__setattr__(self, "relationship", PowderRelationshipKind(self.relationship))
        for value, name in (
            (self.record_id, "relationship record_id"),
            (self.subject_powder_id, "subject powder identity"),
            (self.object_powder_id, "object powder identity"),
            (self.source_wording, "source wording"),
            (self.source_locator, "source locator"),
        ):
            _required(value, name)
        if self.subject_powder_id == self.object_powder_id:
            raise ValueError("powder relationship requires two distinct identity records")

    def to_dict(self) -> dict[str, object]:
        return {
            "schema": M02_SCHEMA_ID,
            "record_type": "powder_identity_relationship",
            "record_id": self.record_id,
            "subject_powder_id": self.subject_powder_id,
            "relationship": self.relationship.value,
            "object_powder_id": self.object_powder_id,
            "source_wording": self.source_wording,
            "source_locator": self.source_locator,
            "provenance": self.provenance.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> PowderIdentityRelationship:
        fields = {
            "subject_powder_id", "relationship", "object_powder_id",
            "source_wording", "source_locator", "provenance",
        }
        _strict_record(data, "powder_identity_relationship", fields)
        return cls(
            str(data["record_id"]), str(data["subject_powder_id"]),
            PowderRelationshipKind(str(data["relationship"])),
            str(data["object_powder_id"]), str(data["source_wording"]),
            str(data["source_locator"]), Provenance.from_dict(data["provenance"]),
        )
