"""
Analysis script for cartridge data.
Loads data from CSVs, performs statistical analysis, validation, and suggests visualizations.
"""

import pandas as pd
import numpy as np
import os

# Get script directory for robust path handling
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load CSVs
cartridge_df = pd.read_csv(os.path.join(script_dir, '..', 'data', 'CartridgeData.csv'))
expansion_df = pd.read_csv(os.path.join(script_dir, '..', 'data', 'ExpansionRatio.csv'))
predictions_df = pd.read_csv(os.path.join(script_dir, '..', 'data', 'Predictions.csv'))

print("=== Statistical Insights ===")
# Summarize numerical columns in cartridge data
print("CartridgeData numerical columns summary:")
numerical_cols = cartridge_df.select_dtypes(include=[np.number]).columns
print(cartridge_df[numerical_cols].describe())

# Summarize expansion ratios
print("\nExpansionRatio summary:")
print(expansion_df.describe())

# Summarize predictions
print("\nPredictions summary:")
print(predictions_df.describe())

print("\n=== Validation of Predictions ===")
# Calculate prediction errors
mae = np.mean(np.abs(predictions_df['Difference (gr)']))
rmse = np.sqrt(np.mean(predictions_df['Difference (gr)']**2))
print(f"Mean Absolute Error (MAE): {mae:.2f} gr")
print(f"Root Mean Square Error (RMSE): {rmse:.2f} gr")
print(f"Average Difference: {predictions_df['Difference (gr)'].mean():.2f} gr")

print("\n=== Trends and Anomalies ===")
# Analyze correlation between muzzle velocity and barrel length
corr = cartridge_df['muzzle_vel'].corr(cartridge_df['barrel_length'])
print(f"Correlation between muzzle velocity and barrel length: {corr:.2f}")

# Detect outliers in muzzle velocity using IQR method
q1 = cartridge_df['muzzle_vel'].quantile(0.25)
q3 = cartridge_df['muzzle_vel'].quantile(0.75)
iqr = q3 - q1
outliers = cartridge_df[(cartridge_df['muzzle_vel'] < q1 - 1.5*iqr) | (cartridge_df['muzzle_vel'] > q3 + 1.5*iqr)]
print(f"Outliers in muzzle velocity: {len(outliers)} found")
if not outliers.empty:
    print(outliers[['cartridge', 'muzzle_vel']])

print("\n=== Suggested Visualizations ===")
print("1. Scatter plot: Muzzle Velocity vs Barrel Length (linear trend expected)")
print("2. Bar plot: Expansion Ratio by Cartridge")
print("3. Histogram: Distribution of Propellant Mass")
print("4. Line plot: Predicted vs Actual Charge with error bars")
print("Use matplotlib in plots/ directory: import matplotlib.pyplot as plt; plt.savefig('plots/filename.png')")