"""
Script to batch process propellant CSV and add Ba_eff column.
"""

import pandas as pd
import os

# Paths
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', 'data')
csv_path = os.path.join(data_dir, 'propellant_params.csv')

# Load data
df = pd.read_csv(csv_path)

# Compute Ba_eff (effective vivacity): accounts for burn characteristics
df['Ba_eff'] = df['Ba'] * (df['a0'] + (1 - df['a0']) * (df['z2'] / 2))

# Save back
df.to_csv(csv_path, index=False)
print(f"Ba_eff added to {csv_path}")
print(df[['propellant', 'Ba', 'a0', 'z2', 'Ba_eff']].to_string())