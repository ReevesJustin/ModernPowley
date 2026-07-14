"""Original slide-scale powder selection is not yet numerically reconstructed."""

from modern_powley.provenance.validation import MissingProvenanceError


def select_powder(*_args: object, **_kwargs: object) -> None:
    raise MissingProvenanceError(
        "The 1961 manual does not print the slide-scale equation or exact interval boundaries"
    )
