from sqlalchemy import DECIMAL, UUID, Boolean, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.sql import expression, func
from datetime import datetime


from ..db.models import Base




class Coupon(Base):

    __tablename__ = 'coupons'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String)
    discount: Mapped[int] = mapped_column(Integer)
    expiration_date: Mapped[datetime] = mapped_column(DateTime)
    is_used: Mapped[bool] = mapped_column(Boolean, default=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='coupon')