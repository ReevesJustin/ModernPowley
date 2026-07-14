"""Original slide-scale powder selection is not yet numerically reconstructed."""

from modern_powley.provenance.validation import MissingProvenanceError


def select_powder(*_args: object, **_kwargs: object) -> None:
    raise MissingProvenanceError(
        "Exact 1961 slide-scale interval boundaries are not available in the committed sources"
    )
