import os
from dotenv import load_dotenv

# This looks for a .env file on your computer
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "default-dev-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False