import bcrypt
from typing import Dict, Any

from app.database.repositories.user.user_repository import UserRepository
from app.exceptions import LoginFailedError
from app.routes.auth.jwt_token_handler import create_jwt_token
from app.routes.serializers import RegisterUserData, LoginUserData


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    def login(self, user_data: LoginUserData) -> Dict[str, Any]:
        user = self._user_repository.get_user_by_email(user_data.email)

        if not user:
            raise LoginFailedError()

        if not self._validate_password_hash(user_data.password, user.password_hash):
            raise LoginFailedError()

        token = create_jwt_token(user)
        return {
            "user": {
                "id": user.id,
               "email":  user.email
            },
            "token": token
        }

    def register(self, user_data: RegisterUserData) -> Dict[str, Any]:
        password_hash = self._hash_password(user_data.password)
        created_user = self._user_repository.create_user(user_data.email, password_hash)

        token = create_jwt_token(created_user)
        return {
            "user": {
                "id": created_user.id,
                "email": created_user.email
            },
            "token": token
        }

    def _hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()

        return bcrypt.hashpw(password.encode(), salt).decode()

    def _validate_password_hash(self, password: str, password_hash: str) -> bool:
        try:
            return bcrypt.checkpw(password.encode(), password_hash.encode())
        except ValueError:
            return False  # return False if the password hash is invalid
