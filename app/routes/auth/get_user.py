from typing import Optional

from fastapi import Header, HTTPException, status, Request

from app.exceptions import AuthenticationFailedError
from app.routes.auth.jwt_token_handler import decode_jwt_token
from app.metrics.entities.user import User
from app.settings import AppSettings

PUBLIC_URLS = [
    "/auth/login",
    "/auth/register",
]


def get_current_user(request: Request, authorization: str = Header(None)) -> Optional[User]:
    if request.url.path in PUBLIC_URLS or AppSettings().auth_enabled is False:
        return

    if not authorization:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    try:
        decoded_user = decode_jwt_token(authorization)
    except AuthenticationFailedError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    return User(id=decoded_user["id"], email=decoded_user["email"])
