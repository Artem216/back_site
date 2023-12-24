from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship

from ..db.models import Base


class Cart(Base):
    __tablename__ = 'carts'

    id: Mapped[int] = mapped_column(Integer, primary_key= True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=True)
    total_items: Mapped[int] = mapped_column(Integer, default=0)
    total_price: Mapped[float] = mapped_column(Float, default=0)

    user = relationship("User", back_populates="cart")
    items = relationship("CartItem", back_populates="cart")

class CartItem(Base):
    __tablename__ = 'cart_items'

    id: Mapped[int] = mapped_column(Integer, primary_key= True)
    cart_id: Mapped[int] = mapped_column(Integer, ForeignKey('carts.id'))
    product_id: Mapped[int] = mapped_column(Integer, default=0)
    quantity: Mapped[int] = mapped_column(Integer, default=0)
    price: Mapped[float] = mapped_column(Float, default=0)

    cart = relationship("Cart", back_populates="items")
