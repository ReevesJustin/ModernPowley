"""
Propellant Selection Tool: CLI for propellant selection and charge prediction.
Dynamically loads propellant data, ranks by Ba_eff closeness to ideal, looks up closest cartridge,
provides text-based chart position, includes error handling, and optional summary file output.
"""

import pandas as pd
import numpy as np
import os

def main():
    try:
        # Load data
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(script_dir, '..', 'data')
        cartridge_df = pd.read_csv(os.path.join(data_dir, 'CartridgeData.csv'))
        propellant_df = pd.read_csv(os.path.join(data_dir, 'propellant_params.csv'))

        # Process propellant data
        propellant_df['pname'] = propellant_df['pname'].str.replace('%20', ' ')
        propellant_dict = propellant_df.set_index('pname')['Ba_eff'].to_dict()

        print("Propellant Selection Tool")
        print("Enter cartridge details:")

        cartridge = input("Cartridge name: ")
        groove_dia = float(input("Groove diameter (in): "))
        case_vol = float(input("Case volume (gr H2O): "))
        barrel_length = float(input("Barrel length (in): "))
        bullet_mass = float(input("Bullet mass (gr): "))

        # Assume eff_case_vol ≈ case_vol
        eff_case_vol = case_vol
        eff_barrel_length = barrel_length - 2.5  # rough cartridge OAL approx

        # Predict charge
        predicted_charge = 0.71 * (eff_case_vol ** 1.02) * (eff_barrel_length ** 0.06)

        # Calculate RC, SD
        bore_area = np.pi * (groove_dia/2)**2
        bore_cap_per_inch = bore_area * 253
        RC = eff_case_vol / bore_cap_per_inch
        SD = bullet_mass

        print(f"\nPredicted charge: {predicted_charge:.2f} gr")
        print(f"Relative Capacity (RC): {RC:.2f}")
        print(f"Sectional Density (SD): {SD}")

        # Find closest cartridge
        cartridge_df['RC_calc'] = cartridge_df['eff_case_vol'] / (np.pi * (cartridge_df['groove_dia']/2)**2 * 253)
        cartridge_df['SD_calc'] = cartridge_df['bullet_mass']
        distances = np.sqrt((cartridge_df['RC_calc'] - RC)**2 + (cartridge_df['SD_calc'] - SD)**2)
        closest_idx = distances.idxmin()
        closest_cartridge = cartridge_df.loc[closest_idx, 'cartridge']
        print(f"Closest cartridge: {closest_cartridge}")

        # Text-based chart position (simple RC vs SD grid)
        rc_min, rc_max = 0, 6
        sd_min, sd_max = 50, 200
        rc_scaled = int((RC - rc_min) / (rc_max - rc_min) * 20)
        sd_scaled = int((SD - sd_min) / (sd_max - sd_min) * 10)
        chart = [[' ' for _ in range(21)] for _ in range(11)]
        if 0 <= rc_scaled < 21 and 0 <= sd_scaled < 11:
            chart[10 - sd_scaled][rc_scaled] = '*'
        print("\nText-based RC vs SD chart (RC 0-6, SD 50-200):")
        print("SD ↑")
        for i, row in enumerate(chart):
            print(f"{sd_max - i*15:3d} {' '.join(row)}")
        print("RC →  0 1 2 3 4 5 6")

        # Ideal Ba_eff interpolation (rough linear fit from data)
        ideal_ba_eff = max(0.45, min(0.9, -0.05 * RC + 0.85))
        print(f"Ideal Ba_eff: {ideal_ba_eff:.3f}")

        # Rank propellants by closeness to ideal
        rankings = sorted(propellant_dict.items(), key=lambda x: abs(x[1] - ideal_ba_eff))
        top_suggestions = [name for name, _ in rankings[:5]]
        print(f"Top suggested propellants: {', '.join(top_suggestions)}")

        # Optional summary file
        save = input("Save summary to file? (y/n): ").lower().strip()
        if save == 'y':
            summary = f"Cartridge: {cartridge}\nGroove Dia: {groove_dia}\nCase Vol: {case_vol}\nBarrel Length: {barrel_length}\nBullet Mass: {bullet_mass}\nPredicted Charge: {predicted_charge:.2f}\nRC: {RC:.2f}\nSD: {SD}\nClosest Cartridge: {closest_cartridge}\nIdeal Ba_eff: {ideal_ba_eff:.3f}\nTop Propellants: {', '.join(top_suggestions)}\n"
            with open(os.path.join(data_dir, 'summary.txt'), 'w') as f:
                f.write(summary)
            print("Summary saved to data/summary.txt")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()