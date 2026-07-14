"""Reproduce descriptive statistics for the committed prediction artifact."""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    rows = list(csv.DictReader((ROOT / "data/Predictions.csv").open(newline="", encoding="utf-8")))
    errors = [float(row["Difference (gr)"]) for row in rows]
    actual = [float(row["Actual Charge (gr)"]) for row in rows]
    predicted = [float(row["Predicted Charge (gr)"]) for row in rows]
    n = len(rows)
    mean_actual = sum(actual) / n
    sse = sum((a - p) ** 2 for a, p in zip(actual, predicted))
    sst = sum((a - mean_actual) ** 2 for a in actual)
    result = {
        "classification": "in-sample artifact reproduction; not validation",
        "n": n,
        "mae_grains": sum(abs(error) for error in errors) / n,
        "rmse_grains": (sum(error**2 for error in errors) / n) ** 0.5,
        "max_absolute_error_grains": max(abs(error) for error in errors),
        "mean_signed_error_grains": sum(errors) / n,
        "r_squared_prediction_form": 1 - sse / sst,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
