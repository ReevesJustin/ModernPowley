import pytest

from modern_powley.original.powder_index import select_powder
from modern_powley.original.pressure import estimate_pressure
from modern_powley.original.velocity import estimate_velocity
from modern_powley.later.howell import pressure_correction
from modern_powley.later.miller import pressure_ratio
from modern_powley.provenance.validation import MissingProvenanceError


@pytest.mark.parametrize(
    "operation", [select_powder, estimate_velocity, estimate_pressure, pressure_correction, pressure_ratio]
)
def test_unresolved_original_operations_fail_explicitly(operation):
    with pytest.raises(MissingProvenanceError):
        operation()
