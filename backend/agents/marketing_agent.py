from llama_index.llms.openai import OpenAI
from langchain_community.tools import Tool
from llama_index.experimental.query_engine import PandasQueryEngine
import pandas as pd
from config import settings

df = pd.read_csv("data/telecom.csv")
llama_llm = OpenAI(temperature=0,api_key=settings.OPENAI_API_KEY)
query_engine = PandasQueryEngine(df=df, llm=llama_llm, verbose=True)

def fetch_pandas_output(query):
    response = query_engine.query(query)
    return f"User Query: {query}\n\nPandas Output:\n{str(response)}"

marketing_agent = Tool(
    name="MarketingTool",
    func=fetch_pandas_output,  # Direct function call
    description=(
        "A data analysis tool for performing operations on marketing-related DataFrames. "
        "Use this tool to query and analyze data, such as finding correlations (e.g., 'correlation between total ad spend and sales'), "
        "aggregating metrics, filtering data, and generating statistical insights. "
        "Provide clear and structured queries related to marketing performance metrics."
    ),
)
