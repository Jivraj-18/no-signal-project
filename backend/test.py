# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pandas",
# ]
# ///

import pandas as pd



import sqlite3

# Load CSV
df = pd.read_csv('unzipped_raw_data/analytics_data/DataCoSupplyChainDataset.csv', encoding='Windows-1252')  # Change encoding if needed

# Connect or create SQLite DB
conn = sqlite3.connect('my_database.db')

# Save to a table named 'my_table'
df.to_sql('supply_data', conn, if_exists='replace', index=False)

# Close DB connection
conn.close()
