from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Centralized configuration for API keys and environment variables
class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")

# Create a global settings instance
settings = Settings()
