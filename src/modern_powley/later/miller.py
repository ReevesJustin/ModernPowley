"""Miller modification placeholder: source artifact is not available."""

from modern_powley.provenance.validation import MissingProvenanceError


def pressure_ratio(*_args: object, **_kwargs: object) -> None:
    raise MissingProvenanceError("Miller July 1999 source and exact modification are unavailable")
