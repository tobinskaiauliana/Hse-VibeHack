import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    huggingface_api_token: str = os.getenv("HUGGINGFACE_API_TOKEN")
    model_name: str = os.getenv("MODEL_NAME", "microsoft/DialoGPT-medium")
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    llm_timeout: int = int(os.getenv("LLM_TIMEOUT", 60))

    class Config:
        env_file = ".env"

settings = Settings()
