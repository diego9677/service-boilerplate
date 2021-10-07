import os
from pathlib import Path
from pydantic import BaseSettings
from dotenv import load_dotenv

"""
    This file is for the general configuration of the app in fastapi
"""

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')


class Settings(BaseSettings):
    HOST: str = '0.0.0.0'
    PORT: int = 8000
    DEBUG: bool = os.environ.get('DEBUG')
    DB_URL: str = os.environ.get('DB_URL')  # change url of the database in .env file
    SECRET_KEY: str = os.environ.get('SECRET_KEY')


settings = Settings()
