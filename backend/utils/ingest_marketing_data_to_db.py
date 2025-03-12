import sqlite3
from config import settings as config_settings
import pandas as pd

def seed_db():
    df = pd.read_csv(config_settings.TELECOM_DATA_SOURCE_PATH)
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    conn = sqlite3.connect(config_settings.TELECOM_DB_NAME)
    df.to_sql("df", conn, if_exists="replace", index=False)
    conn.close()

