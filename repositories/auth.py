import os

import jwt
import datetime
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITM = "HS256"
EXPIRATION_TIME = timedelta(minutes=30)


def create_jwt(data: dict):
    created_at = datetime.datetime.now(datetime.UTC)
    expiration = created_at + EXPIRATION_TIME
    data.update({"exp": expiration})
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITM)
    return token, created_at


def veryfy_jwt(token: str):
    try:
        decode_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITM])
        return decode_data
    except jwt.PyJWTError:
        return None
