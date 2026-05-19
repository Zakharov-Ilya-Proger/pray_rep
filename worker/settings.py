from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from os import getenv

load_dotenv()

class Settings(BaseSettings):
    REDIS: str = getenv("REDIS", "redis://localh:6379/0")

    QUEUE_KEY: str = getenv("QUEUE_KEY", "stt:queue")

    MODEL_PATH: str = getenv("MODEL_PATH")

    API_RECORD_PASS: str = getenv("API_RECORD_PASS", "0")
    API_RECORD_URL: str = getenv("API_RECORD_URL", "0")

    API_PHP_URL: str = getenv("API_PHP_URL", "0")
    API_PHP_PASS: str = getenv("API_PHP_PASS", "0")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
    