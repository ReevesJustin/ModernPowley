"""
Script to parse GRT .grtload XML files and extract cartridge data for calculations.
Extracts effective volume, bullet info (mass, dia, length), propellant mass, groove dia, case vol, barrel length, etc.
"""

import xml.etree.ElementTree as ET
import os
import glob

# Mapping of GRT fields to desired columns
CARTRIDGE_MAPPING = {
    # Caliber
    'casevol': 'case_volume_cm3',
    'Aeff': 'effective_area_mm2',  # XML unit is mm2; never map area to volume
    'Dz': 'groove_diameter_mm',
    'oal': 'cartridge_oal_mm',
    'caselen': 'case_length_mm',
    # Gun
    'xe': 'barrel_length_mm',
    # Projectile
    'mp': 'bullet_mass_g',
    'Dbul': 'bullet_diameter_mm',
    'glen': 'bullet_length_mm',
    # Propellant
    'mc': 'propellant_mass_g',
}

# Preserve source units at the XML boundary. Any later conversion must be an
# explicit, separately tested transformation with both source and target units.
UNIT_CONVERSIONS = {}

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
    import pandas as pd

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
