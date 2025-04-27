import os

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
OAUTH2_TOKEN_URL = os.getenv("OAUTH2_TOKEN_URL")
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl=OAUTH2_TOKEN_URL)
ORIGINS = os.getenv("ORIGINS")
