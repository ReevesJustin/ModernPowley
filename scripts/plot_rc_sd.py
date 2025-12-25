"""
Script to generate banded propellant selection graph: RC vs SD with color-coded bands.
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

# Ensure plots dir exists
os.makedirs(plots_dir, exist_ok=True)

# Load data
df = pd.read_csv(csv_path)

# Calculate RC and SD
df['bore_area'] = np.pi * (df['groove_dia']/2)**2
df['bore_cap_per_inch'] = df['bore_area'] * 252.3  # gr H2O/inch
df['RC'] = df['eff_case_vol'] / df['bore_cap_per_inch']
df['SD'] = (df['bullet_mass'] / 7000) / (df['groove_dia'] ** 2)  # Sectional density

# Ba_eff dict
ba_eff_dict = {
    'RL16': 0.651,
    'N135': 0.65,
    'H4350': 0.45,
    'N110': 0.75,
    'IMR4064': 0.62,
    'N555': 0.586,
    'N160': 0.55,
    'N570': 0.475
}
df['Ba_eff'] = df['propellant_name'].replace(ba_eff_dict)

# Plot RC vs SD with banded regions
plt.figure(figsize=(8, 6))

# Define ranges
rc_min, rc_max = 1.0, 6.0
sd_min, sd_max = 0.150, 0.350

# Create x array for smooth bands
x_array = np.linspace(rc_min, rc_max, 100)

# Slope for diagonal bands
slope = (sd_max - sd_min) / (rc_max - rc_min)  # 0.04

# Boundaries for 3 bands, equally spaced in SD at RC=1
sd_vals = np.linspace(sd_min, sd_max, 4)  # 0.15, 0.2167, 0.2833, 0.35
boundary1 = sd_vals[2] - slope * (x_array - rc_min)  # upper for medium
boundary2 = sd_vals[1] - slope * (x_array - rc_min)  # lower for medium, upper for fast

# Add banded regions, rainbow colors: red (slow), yellow (medium), blue (fast)
plt.fill_between(x_array, boundary1, sd_max, color='red', alpha=0.5, label='Slow: Ba_eff < 0.55')
plt.fill_between(x_array, boundary2, boundary1, color='yellow', alpha=0.5, label='Medium: 0.55 ≤ Ba_eff ≤ 0.70')
plt.fill_between(x_array, sd_min, boundary2, color='blue', alpha=0.5, label='Fast: Ba_eff > 0.70')

# Overlay data points, color-coded by propellant
unique_props = df['propellant_name'].unique()
colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']
for i, prop in enumerate(unique_props):
    sub = df[df['propellant_name'] == prop]
    plt.scatter(sub['RC'], sub['SD'], color=colors[i % len(colors)], s=100, edgecolor='k', label=prop)

plt.title('Relative Capacity vs Sectional Density with Propellant Bands')
plt.xlabel('Relative Capacity')
plt.ylabel('SD')
plt.xlim(rc_min, rc_max)
plt.ylim(sd_min, sd_max)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'rc_sd_banded.png'), dpi=300)
plt.close()

print(f"Plot saved to {plots_dir}/rc_sd_banded.png")