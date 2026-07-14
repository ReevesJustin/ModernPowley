import csv
from collections import defaultdict, deque
from pathlib import Path

import pytest

from modern_powley.experimental.charge_regression import predicted_charge


def test_committed_predictions_reproduce_quarantined_equation():
    inputs = defaultdict(deque)
    for row in csv.DictReader(Path("data/CartridgeData.csv").open()):
        inputs[row["cartridge"]].append(row)
    outputs = list(csv.DictReader(Path("data/Predictions.csv").open()))
    for output in outputs:
        # The committed artifact predates the generator's current title-case
        # rename. Preserve and audit that stale schema while checking values.
        cartridge = output.get("Cartridge") or output["cartridge"]
        row = inputs[cartridge].popleft()
        reproduced = predicted_charge(
            float(row["eff_case_vol"]),
            float(row["eff_barrel_length"]),
            allow_unvalidated=True,
        )
        assert reproduced == pytest.approx(float(output["Predicted Charge (gr)"]), abs=1e-12)
