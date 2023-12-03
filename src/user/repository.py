from src.db.repository import AbstractRepository
from src.db.sql import SQLManager
from src.utils.logger import conf_logger as logger
from src.db.models import User
from src.auth.domain import Signup


class UserRepository(AbstractRepository):
    instance = None

    def __init__(self, db_manager: SQLManager) -> None:
        super().__init__()
        self.db = db_manager
        self.logger = logger("UserRepository")

    def __new__(cls, *args, **kwargs):
        """Singleton pattern"""
        if cls.instance is None:
            cls.instance = super(UserRepository, cls).__new__(cls)
        return cls.instance

    def add(
        self,
        user_data: Signup,
    ) -> User:
        user = User(**user_data.model_dump())
        self.db.session.add(user)
        self.db.session.commit()

        return user

    def get(self, user_id: int | None = None, email: str | None = None) -> User | None:
        if user_id:
            return self.db.session.query(User).filter(User.id == user_id).first()
        elif email:
            return self.db.session.query(User).filter(User.email == email).first()
        else:
            raise ValueError("user_id or email must be provided")

    def update(self, user: User):
        self.db.session.add(user)
        self.db.session.commit()

    def delete(self, user_id: int | None = None, email: str | None = None):
        if user_id:
            self.db.session.query(User).filter(User.id == user_id).delete()
        elif email:
            self.db.session.query(User).filter(User.email == email).delete()
        else:
            raise ValueError("user_id or email must be provided")
        self.db.session.commit()

    def get_all(self) -> list[User]:
        return self.db.session.query(User).all()
