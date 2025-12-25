"""
Script to generate data visualizations from cartridge data.
Saves plots to ../plots/ directory.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style
sns.set(style="whitegrid")

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
sns.scatterplot(data=df, x='barrel_length', y='muzzle_vel', hue='cartridge', s=100)
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
sns.barplot(data=er_df, x='Cartridge', y='Expansion Ratio (Barrel Vol / Eff Case Vol)')
plt.title('Expansion Ratios by Cartridge')
plt.xlabel('Cartridge')
plt.ylabel('Expansion Ratio')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'expansion_ratios.png'))
plt.close()

# Histogram: Propellant mass
plt.figure(figsize=(8, 6))
sns.histplot(data=df, x='propellant_mass', bins=10, kde=True)
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

print(f"Plots saved to {plots_dir}")