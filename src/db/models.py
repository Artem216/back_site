from __future__ import annotations

import enum
import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DECIMAL, UUID, Boolean, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.sql import expression, func

from ..user.domain import UserRole
from ..order.domains import OrderStatus

Base = declarative_base()



class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=uuid.uuid4)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String)
    adress: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(Enum(UserRole), default=UserRole.person)
    pay_method: Mapped[str] = mapped_column(String)

    orders = relationship(
        'Order',
        primaryjoin='User.id == Order.user_id',
        back_populates="user"
    )



class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    date: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(Enum(OrderStatus), default=OrderStatus.in_process)

    details = relationship(
        'OrderDetails',
        primaryjoin='Order.id == OrdersDetails.order_id',
        back_populates='orders'
    )
    

class OrderDetails(Base):
    __tablename__ = 'ordersDetails'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey('orders.id'))
    product_id: Mapped[int] = mapped_column(Integer)
    quantity: Mapped[int] = mapped_column(Integer)


class Coupon(Base):

    __tablename__ = 'coupons'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String)
    discount: Mapped[int] = mapped_column(Integer)
    expiration_date: Mapped[datetime] = mapped_column(DateTime)
    is_used: Mapped[bool] = mapped_column(Boolean)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='coupons')