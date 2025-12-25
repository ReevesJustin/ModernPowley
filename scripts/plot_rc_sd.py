"""
Script to generate RC vs SD plot with Ba_eff bands.
Saves to plots/rc_sd_ba_eff.png
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
df['SD'] = df['bullet_mass']  # Powley SD scale approx

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

# Plot
plt.figure(figsize=(8, 6))
scatter = plt.scatter(df['RC'], df['SD'], c=df['Ba_eff'], cmap='viridis', s=100, edgecolor='k')
plt.colorbar(scatter, label='Ba_eff')
plt.title('Relative Capacity vs Sectional Density with Ba_eff Color Coding')
plt.xlabel('Relative Capacity (RC)')
plt.ylabel('Sectional Density (SD, grains)')

# Add band annotations
plt.text(0.05, 0.95, 'Slow: Ba_eff < 0.55', transform=plt.gca().transAxes, fontsize=10, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral"))
plt.text(0.05, 0.85, 'Medium: 0.55 ≤ Ba_eff ≤ 0.70', transform=plt.gca().transAxes, fontsize=10, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
plt.text(0.05, 0.75, 'Fast: Ba_eff > 0.70', transform=plt.gca().transAxes, fontsize=10, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen"))

plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'rc_sd_ba_eff.png'))
plt.close()

print(f"Plot saved to {plots_dir}/rc_sd_ba_eff.png")