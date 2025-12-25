"""
Script to generate RC vs Bullet Weight plot with viridis colormap and annotations.
Uses dynamic Ba_eff from propellant_params.csv.
Saves to plots/rc_bulletweight.png
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Paths
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', 'data')
plots_dir = os.path.join(script_dir, '..', 'plots')
csv_path = os.path.join(data_dir, 'CartridgeData.csv')
propellant_path = os.path.join(data_dir, 'propellant_params.csv')

# Ensure plots dir exists
os.makedirs(plots_dir, exist_ok=True)

# Load data
try:
    df = pd.read_csv(csv_path)
    df_prop = pd.read_csv(propellant_path)
except FileNotFoundError as e:
    print(f"Error loading CSV: {e}")
    exit(1)

# Clean propellant names
df_prop['pname_clean'] = df_prop['pname'].str.replace('%20', ' ').str.strip()

# Mapping to match CartridgeData propellant_name
prop_mapping = {
    'Reloder 16': 'RL16',
    # Add more mappings as propellant_params.csv grows
}
df_prop['propellant_name'] = df_prop['pname_clean'].replace(prop_mapping)

# Merge
df = df.merge(df_prop[['propellant_name', 'Ba_eff']], on='propellant_name', how='left')

# Check for missing Ba_eff
missing_ba = df['Ba_eff'].isna().sum() > 0
if missing_ba:
    print("Warning: Some propellants missing Ba_eff, filling with mean")
    df['Ba_eff'] = df['Ba_eff'].fillna(df['Ba_eff'].mean())

# Calculate RC
if not all(col in df.columns for col in ['groove_dia', 'eff_case_vol', 'bullet_mass']):
    print("Error: Missing required columns")
    exit(1)

df['bore_area'] = np.pi * (df['groove_dia']/2)**2
df['bore_cap_per_inch'] = df['bore_area'] * 252.3
df['RC'] = df['eff_case_vol'] / df['bore_cap_per_inch']

# Plot RC vs Bullet Weight with viridis colormap
plt.figure(figsize=(10, 8))

# Scatter with viridis
sc = plt.scatter(df['RC'], df['bullet_mass'], c=df['Ba_eff'], cmap='viridis', s=100, edgecolor='k', alpha=0.8)
plt.colorbar(sc, label='Ballistic Efficiency (Ba_eff)')

# Annotations: label with propellant
for idx in df.index:
    plt.annotate(df.loc[idx, 'propellant_name'], (df.loc[idx, 'RC'], df.loc[idx, 'bullet_mass']), textcoords="offset points", xytext=(5,5), ha='left', fontsize=8)

plt.title('Relative Capacity vs Bullet Weight')
plt.xlabel('Relative Capacity (RC)')
plt.ylabel('Bullet Weight (gr)')
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'rc_bulletweight.png'), dpi=300)
plt.close()

print(f"Plot saved to {plots_dir}/rc_bulletweight.png")