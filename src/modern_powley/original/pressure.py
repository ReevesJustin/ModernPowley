"""The 1961 manual's muzzle-pressure reading is not numerically reconstructed.

The separate later Powley psi Calculator is a different historical instrument
and is not represented by this placeholder.
"""

from modern_powley.provenance.validation import MissingProvenanceError


def estimate_pressure(*_args: object, **_kwargs: object) -> None:
    raise MissingProvenanceError(
        "The 1961 manual muzzle-pressure scale and interpolation rules are not source-complete"
    )
