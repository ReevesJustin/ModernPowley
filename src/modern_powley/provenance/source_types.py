from enum import Enum


class AttributionClass(str, Enum):
    ORIGINAL_POWLEY = "Original Powley, directly sourced"
    DAVIS = "Later Davis transcription or extension"
    HOWELL = "Howell correction"
    MILLER = "Miller modification"
    GRT = "GRT-derived parameter or behavior"
    EXPERIMENTAL = "ModernPowley experimental hypothesis"
    REGRESSION = "Empirical regression"
    DERIVED = "Derived quantity"
    AGENT_ASSUMPTION = "Agent-generated assumption"
    UNKNOWN = "Unknown or unresolved"
