"""
Prototype tool: Simple CLI for propellant selection and charge prediction.
Takes user inputs and outputs predictions.
"""

import pandas as pd
import numpy as np
import os

# Load data for reference
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', 'data')
cartridge_df = pd.read_csv(os.path.join(data_dir, 'CartridgeData.csv'))

print("Propellant Selection Tool")
print("Enter cartridge details:")

cartridge = input("Cartridge name: ")
groove_dia = float(input("Groove diameter (in): "))
case_vol = float(input("Case volume (gr H2O): "))
barrel_length = float(input("Barrel length (in): "))
bullet_mass = float(input("Bullet mass (gr): "))

# Assume eff_case_vol ≈ case_vol - adjustment, but for simplicity, use case_vol
eff_case_vol = case_vol
eff_barrel_length = barrel_length - 2.5  # rough cartridge OAL approx

# Predict charge
predicted_charge = 0.71 * (eff_case_vol ** 1.02) * (eff_barrel_length ** 0.06)

# Calculate RC, SD
bore_area = np.pi * (groove_dia/2)**2
bore_cap_per_inch = bore_area * 252.3
RC = eff_case_vol / bore_cap_per_inch
SD = bullet_mass

print(f"\nPredicted charge: {predicted_charge:.2f} gr")
print(f"Relative Capacity (RC): {RC:.2f}")
print(f"Sectional Density (SD): {SD}")

# Suggest propellant based on RC and Ba_eff
# From the dict
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

# Simple suggestion: if RC high, fast powder, etc.
if RC > 3:
    suggested = [k for k, v in ba_eff_dict.items() if v > 0.65]
elif RC > 2:
    suggested = [k for k, v in ba_eff_dict.items() if 0.55 <= v <= 0.7]
else:
    suggested = [k for k, v in ba_eff_dict.items() if v < 0.55]

print(f"Suggested propellants: {', '.join(suggested)}")