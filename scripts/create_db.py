"""
Script to create/update SQLite database from CSV cartridge data.
Usage: python create_db.py [--csv CSV_PATH] [--db DB_PATH]
"""

import sqlite3
import pandas as pd
import os
import logging
import argparse
import sys

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define default paths (relative to script location)
def get_default_paths():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, '..', 'data', 'CartridgeData.csv')
    db_path = os.path.join(script_dir, '..', 'data', 'cartridge_db.sqlite')
    return csv_path, db_path

def validate_csv(df, expected_columns):
    """Validate DataFrame has required columns and basic data integrity."""
    missing_cols = set(expected_columns) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    # Check for NaNs in critical columns
    critical_cols = ['cartridge', 'bullet_mass', 'propellant_mass', 'muzzle_vel']
    for col in critical_cols:
        if col in df.columns and df[col].isnull().any():
            logger.warning(f"NaN values found in column '{col}'. Rows: {df[df[col].isnull()].index.tolist()}")

    logger.info(f"Validation passed. Shape: {df.shape}")

def create_table(conn):
    """Create the loads table if it doesn't exist."""
    conn.execute('''
    CREATE TABLE IF NOT EXISTS loads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cartridge TEXT,
        groove_dia REAL,
        case_vol REAL,
        case_length REAL,
        cartridge_oal REAL,
        barrel_length REAL,
        eff_case_vol REAL,
        bullet_manu TEXT,
        bullet_mass REAL,
        bullet_length REAL,
        propellant_manu TEXT,
        propellant_name TEXT,
        bulk_density REAL,
        propellant_Qex REAL,
        propellant_mass REAL,
        load_ratio REAL,
        eff_barrel_length REAL,
        muzzle_vel REAL,
        est_pmax REAL,
        est_muzzle_pressure REAL
    )
    ''')
    logger.info("Table 'loads' created or already exists.")

def main(csv_path, db_path):
    # Check if CSV exists
    if not os.path.exists(csv_path):
        logger.error(f"CSV file '{csv_path}' not found.")
        sys.exit(1)

    try:
        logger.info("Loading CSV...")
        df = pd.read_csv(csv_path)
    except Exception as e:
        logger.error(f"Error reading CSV: {e}")
        sys.exit(1)

    # Strip spaces from column names
    df.columns = df.columns.str.strip()

    # Expected columns
    expected_columns = [
        'cartridge', 'groove_dia', 'case_vol', 'case_length', 'cartridge_oal',
        'barrel_length', 'eff_case_vol', 'bullet_manu', 'bullet_mass', 'bullet_length',
        'propellant_manu', 'propellant_name', 'bulk_density', 'propellant_Qex',
        'propellant_mass', 'load_ratio', 'eff_barrel_length', 'muzzle_vel',
        'est_pmax', 'est_muzzle_pressure'
    ]

    try:
        validate_csv(df, expected_columns)
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        sys.exit(1)

    logger.info(f"CSV loaded with shape: {df.shape}")
    logger.info(f"Columns: {df.columns.tolist()}")

    # Connect to DB and create table
    try:
        with sqlite3.connect(db_path) as conn:
            create_table(conn)
            # Import data
            df.to_sql('loads', conn, if_exists='replace', index=False)
            logger.info(f"Database '{db_path}' updated successfully with {len(df)} rows.")
    except Exception as e:
        logger.error(f"Database error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create/update cartridge database from CSV.")
    parser.add_argument('--csv', type=str, help="Path to CSV file")
    parser.add_argument('--db', type=str, help="Path to SQLite database")
    args = parser.parse_args()

    csv_path = args.csv if args.csv else get_default_paths()[0]
    db_path = args.db if args.db else get_default_paths()[1]

    main(csv_path, db_path)