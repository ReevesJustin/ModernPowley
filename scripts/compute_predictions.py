"""
Automation script to compute charge predictions from CartridgeData.csv and output to Predictions.csv.
"""

import pandas as pd
import os

# Paths
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', 'data')
input_csv = os.path.join(data_dir, 'CartridgeData.csv')
output_csv = os.path.join(data_dir, 'Predictions.csv')

# Load data
df = pd.read_csv(input_csv)

# Compute predicted charge using the formula: charge_mass ≈ 0.71 * (eff_case_vol)^1.02 * (eff_barrel_length)^0.06
df['Predicted Charge (gr)'] = 0.71 * (df['eff_case_vol'] ** 1.02) * (df['eff_barrel_length'] ** 0.06)

# Prepare output: Cartridge, Eff Case Vol (gr H2O), Eff Barrel Length (in), Predicted Charge (gr), Actual Charge (gr), Difference (gr)
output_df = df[['cartridge', 'eff_case_vol', 'eff_barrel_length', 'Predicted Charge (gr)', 'propellant_mass']].copy()
output_df.rename(columns={
    'cartridge': 'Cartridge',
    'eff_case_vol': 'Eff Case Vol (gr H2O)',
    'eff_barrel_length': 'Eff Barrel Length (in)',
    'propellant_mass': 'Actual Charge (gr)'
}, inplace=True)
output_df['Difference (gr)'] = output_df['Actual Charge (gr)'] - output_df['Predicted Charge (gr)']

# Save to CSV
output_df.to_csv(output_csv, index=False)
print(f"Predictions computed and saved to {output_csv}")