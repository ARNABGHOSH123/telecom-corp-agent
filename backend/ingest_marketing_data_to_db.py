import sqlite3
import pandas as pd

df = pd.read_csv("data/telecom.csv")

df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')

conn = sqlite3.connect("telecom_marketing_data.db")

df.to_sql("df", conn, if_exists="replace", index=False)

conn.close()
