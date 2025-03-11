from langchain_openai.embeddings import OpenAIEmbeddings
from config import settings as config_settings

embeddings = OpenAIEmbeddings(
    api_key=config_settings.OPENAI_API_KEY
)