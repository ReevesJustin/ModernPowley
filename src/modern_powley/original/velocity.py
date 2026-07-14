"""The original velocity scale is documented but no verified equation is available."""

from modern_powley.provenance.validation import MissingProvenanceError


def estimate_velocity(*_args: object, **_kwargs: object) -> None:
    raise MissingProvenanceError("Original Powley velocity equation/scale is not yet source-complete")
