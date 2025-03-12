from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    TELECOM_DB_NAME: str = os.getenv("TELECOM_DB_NAME")
    TELECOM_DATA_SOURCE_PATH: str = os.getenv("TELECOM_DATA_SOURCE_PATH")
    ERROR_CODE_DATA_SOURCE_PATH: str = os.getenv("ERROR_CODE_DATA_SOURCE_PATH")
    VECTORE_DATASTORE_PATH: str = os.getenv("VECTORE_DATASTORE_PATH")

settings = Settings()
