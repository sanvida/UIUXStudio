import os
from pathlib import Path
from dotenv import load_dotenv
import urllib
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_TITLE: str = "AI-powered Personal Assistant Application"
    PROJECT_VERSION: str = "0.0.1"
   
    DB_SERVER: str = os.getenv("DB_SERVER")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_USERNAME: str = os.getenv("DB_USERNAME")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")

    DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@localhost/{DB_NAME}"

    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60


settings = Settings()
