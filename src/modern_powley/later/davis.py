"""Davis transcription as quoted by the accessible secondary transcription."""

from dataclasses import dataclass
from math import sqrt

from modern_powley.original.units import _positive

SOURCE_ID = "SRC-DAVIS-1981-TRANSCRIPTION-UNVERIFIED"


def powder_selection_index(sectional_density_value: float, mass_ratio_value: float) -> float:
    sd = _positive(sectional_density_value, "sectional_density")
    mr = _positive(mass_ratio_value, "mass_ratio")
    return 20.0 + 12.0 / (sd * sqrt(mr))


@dataclass(frozen=True)
class TranscribedBand:
    lower: float | None
    upper: float | None
    text: str
    lower_inclusive: bool = True
    upper_inclusive: bool = True

    def includes(self, value: float) -> bool:
        lower_ok = self.lower is None or value > self.lower or (self.lower_inclusive and value == self.lower)
        upper_ok = self.upper is None or value < self.upper or (self.upper_inclusive and value == self.upper)
        return lower_ok and upper_ok


# Endpoint overlap is retained because the transcription says "x to y" for
# adjacent rows. Resolving inclusivity requires the Davis page image.
TRANSCRIBED_BANDS = (
    TranscribedBand(None, 81, 'much slower than IMR-4831; no suitable IMR canister powder', upper_inclusive=False),
    TranscribedBand(81, 91, 'slower than IMR-4831 and IMR-4350; transcription specifies a reduction'),
    TranscribedBand(91, 110, 'similar to IMR-4831 and IMR-4350'),
    TranscribedBand(110, 125, 'similar to IMR-4064, IMR-4895, and IMR-4320'),
    TranscribedBand(125, 145, 'similar to IMR-3031'),
    TranscribedBand(145, 165, 'similar to IMR-4198'),
    TranscribedBand(165, 180, 'similar to IMR-4227 (transcription contains 4427)'),
    TranscribedBand(180, None, 'faster than IMR-4227', lower_inclusive=False),
)


def matching_transcribed_bands(index: float) -> tuple[TranscribedBand, ...]:
    value = _positive(index, "index")
    return tuple(band for band in TRANSCRIBED_BANDS if band.includes(value))
