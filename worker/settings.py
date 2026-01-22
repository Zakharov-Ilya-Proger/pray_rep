from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from os import getenv

load_dotenv()

class Settings(BaseSettings):
    REDIS_URL: str = getenv("REDIS_URL", "redis://localh:6379/0")

    QUEUE_KEY: str = getenv("QUEUE_KEY", "stt:queue")
    PROCESSING_KEY: str = getenv("PROCESSING_KEY", "stt:processing")

    MODEL_PATH: str = getenv("MODEL_PATH")

    API_RECORD_PASS: str = getenv("API_RECORD_PASS", "0")
    API_RECORD_URL: str = getenv("API_RECORD_URL", "0")

    class Config:
        env_file = ".env"

settings = Settings()
    