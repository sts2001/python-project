import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
OAUTH2_REF = os.getenv("OAUTH2_REF")
ORIGINS = os.getenv("ORIGINS")
DB_SCHEMA = os.getenv("DB_SCHEMA")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
ALGO = os.getenv("ALGO")
ACCESS_TOKEN_EXP = int(os.getenv("ACCESS_TOKEN_EXP"))
