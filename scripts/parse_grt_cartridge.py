"""
Script to parse GRT .grtload XML files and extract cartridge data for calculations.
Extracts effective volume, bullet info (mass, dia, length), propellant mass, groove dia, case vol, barrel length, etc.
"""

import xml.etree.ElementTree as ET
import pandas as pd
import os
import glob

# Unit conversion constants
CM3_TO_GR_H2O = 15.432
MM_TO_INCH = 1 / 25.4
G_TO_GR = 1 / 0.0648  # Approximately 15.432

# Mapping of GRT fields to desired columns
CARTRIDGE_MAPPING = {
    # Caliber
    'casevol': 'case_vol',
    'Aeff': 'eff_case_vol',  # Assuming effective area as effective volume proxy
    'Dz': 'groove_dia',
    'oal': 'oal',
    'caselen': 'case_length',
    # Gun
    'xe': 'barrel_length',
    # Projectile
    'mp': 'bullet_mass',
    'Dbul': 'bullet_dia',
    'glen': 'bullet_length',
    # Propellant
    'mc': 'propellant_mass',
}

# Fields that need unit conversion
UNIT_CONVERSIONS = {
    'case_vol': CM3_TO_GR_H2O,  # cm³ to gr H₂O
    'groove_dia': MM_TO_INCH,  # mm to inches
    'oal': MM_TO_INCH,  # mm to inches
    'case_length': MM_TO_INCH,  # mm to inches
    'barrel_length': MM_TO_INCH,  # mm to inches
    'bullet_mass': G_TO_GR,  # g to gr
    'bullet_dia': MM_TO_INCH,  # mm to inches
    'bullet_length': MM_TO_INCH,  # mm to inches
    'propellant_mass': G_TO_GR,  # g to gr
}

def parse_grt_cartridge(file_path):
    """Parse a single GRT XML file and extract cartridge data."""
    tree = ET.parse(file_path)
    root = tree.getroot()

    data = {}

    # Extract cartridge name from title or caliber
    title = root.find('.//title')
    if title is not None and title.text:
        data['cartridge_name'] = title.text.replace('%20', ' ').replace('%2C', ',')
    else:
        caliber_name = root.find('.//caliber/input[@name="CaliberName"]')
        if caliber_name is not None:
            data['cartridge_name'] = caliber_name.get('value', '').replace('%20', ' ')

    # Parse caliber inputs
    caliber = root.find('.//caliber')
    if caliber is not None:
        for inp in caliber:
            name = inp.get('name')
            value = inp.get('value')
            if name in CARTRIDGE_MAPPING and value:
                try:
                    data[CARTRIDGE_MAPPING[name]] = float(value)
                except ValueError:
                    data[CARTRIDGE_MAPPING[name]] = value

    # Parse gun inputs
    gun = root.find('.//gun')
    if gun is not None:
        for inp in gun:
            name = inp.get('name')
            value = inp.get('value')
            if name in CARTRIDGE_MAPPING and value:
                try:
                    data[CARTRIDGE_MAPPING[name]] = float(value)
                except ValueError:
                    data[CARTRIDGE_MAPPING[name]] = value

    # Parse projectile inputs
    projectile = root.find('.//projectile')
    if projectile is not None:
        for inp in projectile:
            name = inp.get('name')
            value = inp.get('value')
            if name in CARTRIDGE_MAPPING and value:
                try:
                    data[CARTRIDGE_MAPPING[name]] = float(value)
                except ValueError:
                    data[CARTRIDGE_MAPPING[name]] = value

    # Parse propellant inputs
    propellant = root.find('.//propellant')
    if propellant is not None:
        for inp in propellant:
            name = inp.get('name')
            value = inp.get('value')
            if name in CARTRIDGE_MAPPING and value:
                try:
                    data[CARTRIDGE_MAPPING[name]] = float(value)
                except ValueError:
                    data[CARTRIDGE_MAPPING[name]] = value

    # Apply unit conversions
    for field, factor in UNIT_CONVERSIONS.items():
        if field in data:
            data[field] *= factor

    return data

def main(grt_dir, output_csv):
    grt_files = glob.glob(os.path.join(grt_dir, '*.grtload'))
    all_data = []

    for file in grt_files:
        data = parse_grt_cartridge(file)
        if data:
            all_data.append(data)

    if all_data:
        df = pd.DataFrame(all_data)
        df.to_csv(output_csv, index=False)
        print(f"Extracted cartridge data from {len(all_data)} files to {output_csv}")
    else:
        print("No cartridge data extracted.")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    grt_dir = os.path.join(script_dir, '..', 'data', 'GRT_Files')
    output_csv = os.path.join(script_dir, '..', 'data', 'cartridge_data_from_grt.csv')
    main(grt_dir, output_csv)