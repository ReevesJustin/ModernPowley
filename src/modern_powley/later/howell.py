"""Howell correction placeholder: source artifact is not available."""

from modern_powley.provenance.validation import MissingProvenanceError


def pressure_correction(*_args: object, **_kwargs: object) -> None:
    raise MissingProvenanceError("Howell July 1997 source and exact correction are unavailable")
