from datetime import datetime, timedelta

import jwt

from app.exceptions import AuthenticationFailedError
from app.settings import AppSettings


def decode_jwt_token(token: str) -> str:
    split_token = token.split()

    if len(split_token) != 2:
        raise AuthenticationFailedError("Invalid token format!")
    if split_token[0].lower() != "token":
        raise AuthenticationFailedError("Invalid token format! Token must begin with 'Token'")

    token_to_decode = split_token[1]

    try:
        decoded_token = jwt.decode(token_to_decode, algorithms="HS256", key=AppSettings().secret_key)
    except jwt.DecodeError:
        raise AuthenticationFailedError("Invalid symbols passed in auth token")
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailedError("Authentication token expired")

    if datetime.utcnow() > datetime.fromtimestamp(decoded_token["exp"]):
        raise AuthenticationFailedError("Authentication token expired")

    return decoded_token["email"]


def create_jwt_token(email: str) -> str:
    settings = AppSettings()

    token_duration = timedelta(minutes=settings.token_life_minutes)
    token_expiration_time = datetime.utcnow() + token_duration

    to_encode = {"email": email, "exp": token_expiration_time, "sub": "access"}

    encoded_token = jwt.encode(to_encode, algorithm="HS256", key=settings.secret_key)

    return encoded_token
