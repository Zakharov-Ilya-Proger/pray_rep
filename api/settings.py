from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from os import getenv
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):

    REDIS: str = getenv("REDIS")
    WORKERS: int = getenv("WORKERS")
    QUEUE_KEY: str = getenv("QUEUE_KEY")
    PORT: int = getenv("PORT")
    API_PASS: str = getenv("API_PASS")
    model_config = ConfigDict(extra="allow")

    class Config:
        env_file = ".env"

settings = Settings()