"""
Script to calculate charge predictions, expansion ratios, etc.
Loads CartridgeData.csv, computes ER, predicts charge_mass.
"""

import pandas as pd
import numpy as np
import os

# Paths
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', 'data')
csv_path = os.path.join(data_dir, 'CartridgeData.csv')

# Load data
df = pd.read_csv(csv_path)

# Compute ER
df['bore_area'] = np.pi * (df['groove_dia']/2)**2
bore_volume = df['bore_area'] * df['eff_barrel_length'] * 253  # approx gr H2O
df['ER'] = 1 + bore_volume / df['eff_case_vol']

# Predict charge_mass
df['predicted_charge'] = 0.71 * (df['eff_case_vol'] ** 1.02) * (df['eff_barrel_length'] ** 0.06)

# Print summary
print("Calculated Metrics:")
print(df[['cartridge', 'ER', 'predicted_charge']].to_string())

# Save extended data
output_path = os.path.join(data_dir, 'calculated_metrics.csv')
df.to_csv(output_path, index=False)
print(f"Full data saved to {output_path}")