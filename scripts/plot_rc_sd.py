"""
Script to generate improved RC vs SD plot with plasma colormap, contours, and labels.
Uses dynamic Ba_eff from propellant_params.csv.
Saves to plots/rc_sd_banded.png
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
if df['Ba_eff'].isna().any():
    print("Warning: Some propellants missing Ba_eff, filling with mean or default")
    df['Ba_eff'] = df['Ba_eff'].fillna(df['Ba_eff'].mean())

# Calculate RC and SD
if not all(col in df.columns for col in ['groove_dia', 'eff_case_vol', 'bullet_mass']):
    print("Error: Missing required columns in CartridgeData.csv")
    exit(1)

df['bore_area'] = np.pi * (df['groove_dia']/2)**2
df['bore_cap_per_inch'] = df['bore_area'] * 252.3  # gr H2O/inch
df['RC'] = df['eff_case_vol'] / df['bore_cap_per_inch']
df['SD'] = (df['bullet_mass'] / 7000) / (df['groove_dia'] ** 2)  # Sectional density

# Plot RC vs SD with plasma colormap
plt.figure(figsize=(10, 8))

# Define ranges
rc_min, rc_max = df['RC'].min() * 0.9, df['RC'].max() * 1.1
sd_min, sd_max = df['SD'].min() * 0.9, df['SD'].max() * 1.1

# Scatter with plasma colormap
sc = plt.scatter(df['RC'], df['SD'], c=df['Ba_eff'], cmap='plasma', s=100, edgecolor='k', alpha=0.8)
plt.colorbar(sc, label='Ballistic Efficiency (Ba_eff)')

# Add contours if enough points, using tricontour
if len(df) > 10:
    try:
        levels = np.linspace(df['Ba_eff'].min(), df['Ba_eff'].max(), 5)
        cs = plt.tricontour(df['RC'], df['SD'], df['Ba_eff'], levels=levels, colors='k', linewidths=0.5)
        plt.clabel(cs, inline=True, fontsize=8)
    except:
        pass  # Skip if contour fails

# Labels: annotate each point with cartridge
for idx in df.index:
    plt.annotate(df.loc[idx, 'cartridge'], (df.loc[idx, 'RC'], df.loc[idx, 'SD']), textcoords="offset points", xytext=(5,5), ha='left', fontsize=8)

plt.title('Relative Capacity vs Sectional Density')
plt.xlabel('Relative Capacity (RC)')
plt.ylabel('Sectional Density (SD)')
plt.xlim(rc_min, rc_max)
plt.ylim(sd_min, sd_max)

plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'rc_sd_banded.png'), dpi=300)
plt.close()

print(f"Plot saved to {plots_dir}/rc_sd_banded.png")