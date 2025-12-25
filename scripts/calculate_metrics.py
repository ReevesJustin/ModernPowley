"""
Script to calculate derived metrics from cartridge data.
Outputs to console and optionally to CSV.
"""

import pandas as pd
import os

# Paths
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', 'data')
csv_path = os.path.join(data_dir, 'CartridgeData.csv')

# Load data
df = pd.read_csv(csv_path)

# Calculate metrics
# Efficiency proxy: velocity / pressure
df['efficiency_proxy'] = df['muzzle_vel'] / df['est_pmax']

# Mass ratio
df['mass_ratio'] = df['propellant_mass'] / df['bullet_mass']

# Expansion ratio (approximate from barrel_length, assuming groove_dia ~ bullet_dia)
# But since not in this csv, skip or use from other.

# Print summary
print("Derived Metrics:")
print(df[['cartridge', 'efficiency_proxy', 'mass_ratio']].to_string())

# Save to CSV
output_path = os.path.join(data_dir, 'derived_metrics.csv')
df.to_csv(output_path, index=False)
print(f"Full data with metrics saved to {output_path}")