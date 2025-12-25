"""
Script to parse GRT .grtload XML files and extract propellant parameters to CSV.
Extracts Ba, a0, z1, z2, bulk_density, Qex, k, etc. from the caliberfile vars.
"""

import xml.etree.ElementTree as ET
import pandas as pd
import os
import glob

# Mapping of GRT var names to desired columns (Powley calculations)
PARAM_MAPPING = {
    # Propellant params
    'f': 'Ba',  # Vivacity
    'c_b_': 'a0',  # Ba(phi) coefficient 0
    'c_Z': 'z1',  # Lower burn-up limit
    'c_F': 'z2',  # Upper burn-up limit
    'c_Q': 'bulk_density',  # Bulk density
    'c_u_': 'Qex',  # Energy
    'c_alpha': 'k',  # Adiabatic index
    # Caliber params
    'c_L3': 'case_length',  # Case length (mm)
    'c_Pmax': 'p_max',  # Max pressure
    'Dz': 'groove_dia',  # Groove diameter (mm)
    'Aeff': 'eff_area',  # Effective area (mm2)
    'casevol': 'case_vol',  # Case volume (cm3)
    # Add more
}

def parse_grt_file(file_path):
    """Parse a single GRT XML file and extract params for Powley calculations."""
    tree = ET.parse(file_path)
    root = tree.getroot()

    data = {}

    # Parse caliber inputs
    caliber = root.find('.//caliber')
    if caliber is not None:
        for inp in caliber:
            name = inp.get('name')
            value = inp.get('value')
            unit = inp.get('unit')
            if name and value:
                key = f"{name}"
                try:
                    data[key] = float(value)
                except ValueError:
                    data[key] = value
                data[f"{name}_unit"] = unit if unit else ""

    # Find caliberfile vars (propellant model)
    caliberfile = root.find('.//caliberfile')
    if caliberfile is not None:
        for var in caliberfile:
            name = var.get('name')
            value = var.get('value')
            if name in PARAM_MAPPING and value:
                try:
                    data[PARAM_MAPPING[name]] = float(value)
                except ValueError:
                    data[PARAM_MAPPING[name]] = value

    # Propellant inputs
    propellant = root.find('.//propellant')
    if propellant is not None:
        for inp in propellant:
            name = inp.get('name')
            value = inp.get('value')
            if name and value:
                try:
                    data[name] = float(value)
                except ValueError:
                    data[name] = value
        # Combined name
        manu = data.get('mname')
        pname = data.get('pname')
        if manu and pname:
            data['propellant'] = f"{manu} {pname}"

    # Bullet from title or inputs (approximate)
    title = root.find('.//title')
    if title is not None and title.text:
        title_text = title.text
        # Parse title: "6.5%20Creedmoor%20Hornady%2C%20ELD-M%2026331%2C%200.264%2C%20140.00%20grain%20Alliant%20Reloder%2016"
        parts = title_text.split('%2C%20')
        if len(parts) >= 3:
            dia_str = parts[2]
            weight_str = parts[3].split('%20')[0] if len(parts) > 3 else '140.00'
            try:
                data['bullet_dia'] = float(dia_str)
                data['bullet_weight'] = float(weight_str)
            except ValueError:
                pass

    return data

def main(grt_dir, output_csv):
    grt_files = glob.glob(os.path.join(grt_dir, '*.grtload'))
    all_data = []

    for file in grt_files:
        data = parse_grt_file(file)
        if data:
            all_data.append(data)

    if all_data:
        df = pd.DataFrame(all_data)
        df.to_csv(output_csv, index=False)
        print(f"Extracted data from {len(all_data)} files to {output_csv}")
    else:
        print("No data extracted.")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    grt_dir = os.path.join(script_dir, '..', 'data', 'GRT_Files')
    output_csv = os.path.join(script_dir, '..', 'data', 'propellant_params.csv')
    main(grt_dir, output_csv)