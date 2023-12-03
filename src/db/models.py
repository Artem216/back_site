import uuid

from sqlalchemy import UUID, String
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String)




