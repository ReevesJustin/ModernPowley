from enum import Enum


class AttributionClass(str, Enum):
    ORIGINAL_POWLEY = "original_powley"
    DAVIS = "davis"
    HOWELL = "howell"
    MILLER = "miller"
    ONLINE_EMULATOR = "online_emulator"
    GRT = "grt"
    EXPERIMENTAL = "modern_powley_experiment"
    MODERNIZED = "modernized_powley"
    DERIVED = "derived_quantity"
    UNKNOWN = "unknown"


class ProvenanceStatus(str, Enum):
    VERIFIED_PRIMARY = "verified_primary"
    VERIFIED_VISUAL_SCAN = "verified_visual_scan"
    VERIFIED_SECONDARY = "verified_secondary"
    EMULATOR_DERIVED = "emulator_derived"
    OCR_ONLY = "ocr_only"
    INFERRED = "inferred"
    EXPERIMENTAL = "experimental"
    CONTRADICTED = "contradicted"
    UNRESOLVED = "unresolved"
    USER_REVIEWED_ACCESS_RESTRICTED_PRIMARY = "user_reviewed_access_restricted_primary"
    NORMALIZED_USER_TRANSCRIPTION = "normalized_user_transcription"
    PENDING_RETAINED_PRIMARY_VISUAL_VERIFICATION = (
        "pending_retained_primary_visual_verification"
    )
