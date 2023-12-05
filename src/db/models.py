from __future__ import annotations

import enum
import uuid
from decimal import Decimal

from sqlalchemy import UUID, Boolean, Column, DateTime, Enum, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.sql import expression

Base = declarative_base()


class DealType(enum.Enum):
    buy = "buy"
    sell = "sell"


association_user_instrument = Table(
    "associated_user_instruments",
    Base.metadata,
    Column("id", ForeignKey("users.id"), primary_key=True),
    Column("code", ForeignKey("instruments.code"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String)
    deals: Mapped[list[Deal]] = relationship(
        back_populates="user",
        cascade="all, delete",
    )
    instruments: Mapped[list[Instrument]] = relationship(
        secondary=association_user_instrument, back_populates="users"
    )


class Instrument(Base):
    __tablename__ = "instruments"

    code: Mapped[str] = mapped_column(String(30), primary_key=True)
    title: Mapped[str] = mapped_column(String)
    group: Mapped[str] = mapped_column(String(30))
    has_model: Mapped[bool] = mapped_column(Boolean, server_default=expression.false())
    deals: Mapped[list[Deal]] = relationship(
        back_populates="instrument",
        cascade="all, delete",
    )

    users: Mapped[list[User]] = relationship(
        secondary=association_user_instrument, back_populates="instruments"
    )

    def __repr__(self) -> str:
        return f"Instrument(code={self.code}, title={self.title})"


class Deal(Base):
    __tablename__ = "deals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    price: Mapped[Decimal]
    quantity: Mapped[int]
    deal_type: Mapped[DealType] = mapped_column(Enum(DealType))
    datetime: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now(),
    )
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship(back_populates="deals")
    instrument_code: Mapped[str] = mapped_column(ForeignKey("instruments.code"))
    instrument: Mapped[Instrument] = relationship(back_populates="deals")

