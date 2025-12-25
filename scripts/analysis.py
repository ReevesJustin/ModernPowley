import pandas as pd
import numpy as np
import os

# Load CSVs
cartridge_df = pd.read_csv('../data/CartridgeData.csv')
expansion_df = pd.read_csv('../data/ExpansionRatio.csv')
predictions_df = pd.read_csv('../data/Predictions.csv')

print("=== Statistical Insights ===")
print("CartridgeData numerical columns summary:")
numerical_cols = cartridge_df.select_dtypes(include=[np.number]).columns
print(cartridge_df[numerical_cols].describe())

print("\nExpansionRatio summary:")
print(expansion_df.describe())

print("\nPredictions summary:")
print(predictions_df.describe())

print("\n=== Validation of Predictions ===")
mae = np.mean(np.abs(predictions_df['Difference (gr)']))
rmse = np.sqrt(np.mean(predictions_df['Difference (gr)']**2))
print(f"Mean Absolute Error (MAE): {mae:.2f} gr")
print(f"Root Mean Square Error (RMSE): {rmse:.2f} gr")
print(f"Average Difference: {predictions_df['Difference (gr)'].mean():.2f} gr")

print("\n=== Trends and Anomalies ===")
# Trend: muzzle_vel vs barrel_length
corr = cartridge_df['muzzle_vel'].corr(cartridge_df['barrel_length'])
print(f"Correlation between muzzle velocity and barrel length: {corr:.2f}")

# Anomalies: outliers in muzzle_vel
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