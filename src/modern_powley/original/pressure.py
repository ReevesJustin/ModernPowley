"""The original pressure calculator is not reconstructed from an inferred formula."""

from modern_powley.provenance.validation import MissingProvenanceError


def estimate_pressure(*_args: object, **_kwargs: object) -> None:
    raise MissingProvenanceError("Original Powley pressure equation/scale is not yet source-complete")
