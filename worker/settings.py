from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from os import getenv

load_dotenv()

class Settings(BaseSettings):
    REDIS_URL = getenv("REDIS_URL", "redis://localh:6379/0")

    QUEUE_KEY = getenv("QUEUE_KEY", "stt:queue")
    PROCESSING_KEY = getenv("PROCESSING_KEY", "stt:processing")
    DLQ_KEY = getenv("DLQ_KEY", "stt:dlq")

    BLOCK_SEC = int(getenv("BLOCK_SEC", "5"))
    MAX_ATTEMPTS = int(getenv("MAX_ATTEMPTS", "5"))
    ATTEMPTS_HASH = getenv("ATTEMPTS_HASH", "stt:attempts")

    REQUEUE_ON_START = getenv("REQUEUE_ON_START", "1") == "1"
    MODEL_PATH: str = getenv("MODEL_PATH")
    SAMPLE_RATE: int = getenv("SAMPLE_RATE", 16000)

    class Config:
        env_file = ".env"

settings = Settings()
    