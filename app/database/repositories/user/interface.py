from abc import ABC, abstractmethod
from typing import Optional

from app.metrics.entities.user import User


class IUserRepository(ABC):
    @abstractmethod
    def create_user(self, email: str, password_hash: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_user_by_email(self, user: str) -> User:
        pass
