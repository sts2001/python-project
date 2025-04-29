import argon2
import jwt
from fastapi.security import OAuth2PasswordBearer

from app.core.config import (OAUTH2_REF,
                             SECRET_KEY,
                             ALGO)

hasher = argon2.PasswordHasher()
o_auth2 = OAuth2PasswordBearer(tokenUrl=OAUTH2_REF)


def hash_password(password):
    return hasher.hash(password)


def is_it_correct_password(password_hash, password):
    try:
        return hasher.verify(password_hash, password)
    except argon2.exceptions.VerifyMismatchError:
        return False


def get_access_token(data):
    try:
        token = jwt.encode(data, SECRET_KEY, algorithm=ALGO)
        return token
    except jwt.PyJWTError:
        return None


def decode_token(token):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGO])
        user_id: str = data.get("user_id")
        return user_id
    except jwt.PyJWTError:
        return None
