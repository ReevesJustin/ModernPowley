"""
Script to generate data visualizations from cartridge data.
Saves plots to ../plots/ directory.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Set style
plt.style.use('default')

# Paths
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', 'data')
plots_dir = os.path.join(script_dir, '..', 'plots')
csv_path = os.path.join(data_dir, 'CartridgeData.csv')

# Ensure plots dir exists
os.makedirs(plots_dir, exist_ok=True)

# Load data
df = pd.read_csv(csv_path)

# Scatter plot: Muzzle velocity vs Barrel length
plt.figure(figsize=(8, 6))
for cart in df['cartridge'].unique():
    sub = df[df['cartridge'] == cart]
    plt.scatter(sub['barrel_length'], sub['muzzle_vel'], label=cart, s=100)
plt.title('Muzzle Velocity vs Barrel Length')
plt.xlabel('Barrel Length (in)')
plt.ylabel('Muzzle Velocity (fps)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'velocity_vs_barrel.png'))
plt.close()

# Bar chart: Expansion ratios (need to calculate or from another csv)
# ExpansionRatio.csv has ER
er_df = pd.read_csv(os.path.join(data_dir, 'ExpansionRatio.csv'))
plt.figure(figsize=(8, 6))
plt.bar(er_df['Cartridge'], er_df['Expansion Ratio (Barrel Vol / Eff Case Vol)'])
plt.title('Expansion Ratios by Cartridge')
plt.xlabel('Cartridge')
plt.ylabel('Expansion Ratio')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'expansion_ratios.png'))
plt.close()

# Histogram: Propellant mass
plt.figure(figsize=(8, 6))
plt.hist(df['propellant_mass'], bins=10, alpha=0.7)
plt.title('Distribution of Propellant Mass')
plt.xlabel('Propellant Mass (gr)')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'propellant_mass_hist.png'))
plt.close()

# Line plot: Predicted vs Actual charges (from Predictions.csv)
pred_df = pd.read_csv(os.path.join(data_dir, 'Predictions.csv'))
plt.figure(figsize=(8, 6))
for _, row in pred_df.iterrows():
    plt.plot([row['Predicted Charge (gr)'], row['Actual Charge (gr)']], [row['Cartridge'], row['Cartridge']], marker='o')
plt.title('Predicted vs Actual Charges')
plt.xlabel('Charge (gr)')
plt.ylabel('Cartridge')
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'predicted_vs_actual.png'))
plt.close()

# Calculate RC and SD
df['bore_area'] = np.pi * (df['groove_dia']/2)**2
df['bore_cap_per_inch'] = df['bore_area'] * 252.3  # gr H2O/inch
df['RC'] = df['eff_case_vol'] / df['bore_cap_per_inch']
df['SD'] = df['bullet_mass']  # approximate Powley SD scale

# Ba_eff dict based on calibrated models
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

# Plot RC vs SD, color-coded by Ba_eff
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

# Calculate R² for charge predictions
pred_df = pd.read_csv(os.path.join(data_dir, 'Predictions.csv'))
y_true = pred_df['Actual Charge (gr)']
y_pred = pred_df['Predicted Charge (gr)']
ss_res = np.sum((y_true - y_pred)**2)
ss_tot = np.sum((y_true - np.mean(y_true))**2)
r2_charge = 1 - (ss_res / ss_tot)
print(f"R² for charge predictions: {r2_charge:.4f}")

# Band clustering
slow = df[df['Ba_eff'] < 0.55]
medium = df[(df['Ba_eff'] >= 0.55) & (df['Ba_eff'] <= 0.70)]
fast = df[df['Ba_eff'] > 0.70]
print(f"Slow band (<0.55): {len(slow)} loads")
print(f"Medium band (0.55-0.70): {len(medium)} loads")
print(f"Fast band (>0.70): {len(fast)} loads")

print(f"Plots saved to {plots_dir}")