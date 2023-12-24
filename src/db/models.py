from __future__ import annotations

import enum
import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DECIMAL, UUID, Boolean, DateTime, Enum, ForeignKey, Integer, String, Sequence, create_engine
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.sql import expression, func

from ..user.domain import UserRole
from ..order.domains import OrderStatus

Base = declarative_base()



users_id_seq = Sequence('users_id_seq', start=1)

from random import randint

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(users_id_seq, primary_key=True, autoincrement= True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String)
    adress: Mapped[str] = mapped_column(String, default= "")
    role: Mapped[str] = mapped_column(Enum(UserRole), default=UserRole.admin)
    pay_method: Mapped[str] = mapped_column(String, default= "")

    orders = relationship(
        'Order',
        primaryjoin='User.id == Order.user_id',
        back_populates="user"
    )

    cart = relationship(
        "Cart",
        primaryjoin='User.id == Cart.user_id',
        back_populates="user"
    )

    coupon = relationship(
        "Coupon",
        back_populates="user"
    )


# class Coupon(Base):

#     __tablename__ = 'coupons'

#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     code: Mapped[str] = mapped_column(String)
#     discount: Mapped[int] = mapped_column(Integer)
#     expiration_date: Mapped[datetime] = mapped_column(DateTime)
#     is_used: Mapped[bool] = mapped_column(Boolean)
#     user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))

#     user = relationship('User', back_populates='coupons')