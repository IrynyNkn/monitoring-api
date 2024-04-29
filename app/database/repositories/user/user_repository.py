from typing import Optional

from sqlalchemy.orm import Session

from app.database.repositories.user.interface import IUserRepository
from app.metrics.entities.user import User as UserEntity
from app.database.tables import User as UserTable


class UserRepository(IUserRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_user(self, email: str, password_hash: str) -> UserEntity:
        db_entity = UserTable(email=email, password_hash=password_hash)

        self.session.add(db_entity)
        self.session.commit()

        return UserEntity(id=str(db_entity.id), email=db_entity.email, password_hash=db_entity.password_hash)

    def get_user_by_email(self, email: str) -> Optional[UserEntity]:
        entity = self.session.query(UserTable).filter(UserTable.email == email).first()

        if not entity:
            return None

        return UserEntity(id=str(entity.id), email=entity.email, password_hash=entity.password_hash)
