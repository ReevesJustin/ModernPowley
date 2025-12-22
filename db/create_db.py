import sqlite3
import pandas as pd
import os

# Define paths (adjust if needed)
csv_path = 'cartridge_db.csv'          # Make sure this file exists in the current folder
db_path = 'cartridge_db.sqlite'

# Check if CSV exists
if not os.path.exists(csv_path):
    print(f"Error: CSV file '{csv_path}' not found in the current directory.")
    print("Current working directory:", os.getcwd())
    print("Files in directory:", os.listdir('.'))
    exit()

print("Loading CSV...")
df = pd.read_csv(csv_path)

# Fix the column with space in header (common issue)
if 'bulk_densit y' in df.columns:
    df = df.rename(columns={'bulk_densit y': 'bulk_density'})
else:
    print("Note: 'bulk_densit y' column not found. Available columns:")
    print(df.columns.tolist())

print("CSV loaded with shape:", df.shape)
print("Columns after rename:", df.columns.tolist())

# Connect to SQLite database (creates it if it doesn't exist)
conn = sqlite3.connect(db_path)

# Create the table
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
    barrel_length2 REAL,
    muzzle_vel REAL,
    est_pmax REAL,
    est_muzzle_pressure REAL
)
''')

conn.commit()

# Import DataFrame to SQLite table
# Use if_exists='replace' to overwrite the table data (keeps the table structure)
# Or 'append' if you want to add rows without dropping existing data
df.to_sql('loads', conn, if_exists='replace', index=False)

conn.close()

print(f"Database '{db_path}' created/updated successfully with {len(df)} rows.")