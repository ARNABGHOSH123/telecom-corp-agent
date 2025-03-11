from openai import OpenAI
from llama_index.llms.openai import OpenAI as LlamaOpenAi
import sqlite3
from llama_index.experimental.query_engine import PandasQueryEngine
import pandas as pd
import re
from config import settings

DB_PATH = "telecom_marketing_data.db"
llm = OpenAI(api_key=settings.OPENAI_API_KEY)

llama_llm = LlamaOpenAi(temperature=0, api_key=settings.OPENAI_API_KEY)

df = pd.read_csv("data/telecom.csv")
query_engine = PandasQueryEngine(df=df, llm=llama_llm)


def fetch_pandas_output(query):
    response = query_engine.query(query)
    return str(response)


def get_sqlite_schema():
    """Extract column names from the SQLite database for LLM context."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(df);")
        columns = cursor.fetchall()

    column_info = ", ".join([f"{col[1]} ({col[2]})" for col in columns])
    return f"Table: df | Columns: {column_info}"


sqlite_schema = get_sqlite_schema()


def validate_sql(query):
    if not re.match(r"^\s*SELECT\s+", query, re.IGNORECASE):
        raise ValueError("Only SELECT queries are allowed!")
    return query


def execute_sql(query):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    conn.close()

    if rows:
        output = [column_names] + rows
        output_str = "\n".join([" | ".join(map(str, row)) for row in output])
    else:
        output = "No rows found"

    return output_str


def marketing_agent(query):

    prompt = f"""
    You are an expert SQL assistant working for SQLite Database. 
    - Always use df as the table name.
    - Whenever encountering a date range use > , >=, < or <= symbols instead of LIKE or BETWEEN.
    - Interpret relative date expressions like "last year," "previous month," or "next year" dynamically based on the current date.
    - Ensure compatibility with SQLite by using strftime() instead of unsupported functions like DATE_TRUNC and DATEADD.
    - Use **strftime('%Y-%m', date)** when filtering by year and month.
    - For filtering months from the previous year, compute the date dynamically using **DATE('now', '-1 year', 'start of year', '+X months')**, where X is the number of months after January.
    - Convert natural language date references into absolute values using standard SQL date functions.
    - Optimize queries for readability and efficiency, avoiding redundant conditions.

    The data comes from a sqlite db file with the following schema:

    {sqlite_schema}

    Generate a SQL query for:
    "{query}"

    Return ONLY the SQL query and nothing else.
    """

    response = llm.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
    )
    validated_sql_query = validate_sql(response.choices[0].message.content.strip())
    try:
        output_str = execute_sql(validated_sql_query)
    except Exception as e:
        output_str = fetch_pandas_output(query)

    return f"\nOutput: {output_str}"
