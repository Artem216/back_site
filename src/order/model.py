from sqlalchemy import DECIMAL, UUID, Boolean, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.sql import expression, func
from datetime import datetime

import uuid

from ..db.models import Base

from ..user.domain import UserRole
from ..order.domains import OrderStatus

class OrderDetails(Base):
    __tablename__ = 'ordersDetails'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey('orders.id'))
    product_id: Mapped[int] = mapped_column(Integer)
    quantity: Mapped[int] = mapped_column(Integer)

    order = relationship(
        "Order", 
        back_populates= "details"
    )


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    date: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(Enum(OrderStatus), default=OrderStatus.in_process)

    details = relationship(
        'OrderDetails',
        primaryjoin='Order.id == OrderDetails.order_id',
        back_populates='order'
    )

    user = relationship(
        "User",
        back_populates="orders"
    )
