import sqlite3
import os
from config import settings as config_settings
import pandas as pd

def is_db_empty(db_path):
    if not os.path.exists(db_path):
        return True
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()
    
    return len(tables) == 0

def seed_db():
    db_path = config_settings.TELECOM_DB_NAME
    if is_db_empty(db_path):
        df = pd.read_csv(config_settings.TELECOM_DATA_SOURCE_PATH)
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        conn = sqlite3.connect(db_path)
        df.to_sql("df", conn, if_exists="replace", index=False)
        conn.close()
        print("Database seeded successfully.")
    else:
        print("Database already exists and is not empty. Seeding skipped.")