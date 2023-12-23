from src.db.repository import AbstractRepository

from src.db.sql import SQLManager
from src.utils.logger import get_logger

from src.order.model import Order, OrderDetails
from src.order.domains import OrderCreate

from datetime import datetime

from src.cart.model import CartItem

import json

class OrderRepository(AbstractRepository):
    instance = None


    def __init__(self, db_manager: SQLManager) -> None:
        super().__init__()
        self.db = db_manager
        self.logger = get_logger("OrderRepository")


    def __new__(cls, *args, **kwargs):
        """Singleton pattern"""
        if cls.instance is None:
            cls.instance = super(OrderRepository, cls).__new__(cls)
        return cls.instance
    
    def add(
            self,
            user_id: int,
            items: list[CartItem],
    ) -> int:
        
        order_db: Order = Order(user_id= user_id, date= datetime.now())
        for item in items:
            order_db.details.append(OrderDetails(
                order_id= order_db.id,
                product_id= item.product_id,
                quantity= item.quantity
            ))
        self.db.session.add(order_db)
        self.db.session.commit()

        return 0
    
    def get(self, order_id: int | None = None) -> Order | None:
        if order_id:
            return (
                self.db.session.query(Order)
                .filter(Order.id == order_id)
                .first()
            )
        else:
            raise ValueError("order_id must be provided")

    def update(self, order: Order):
        self.db.session.add(Order)
        self.db.session.commit()


    def delete(self, order_id: int | None = None):
        if order_id:
            self.db.session.query(Order).filter(
                Order.id == order_id
            ).delete()
        else:
            raise ValueError("order_id must be provided")
        self.db.session.commit()


    def get_all(self, user_id: int) -> list[Order]:
        return self.db.session.query(Order).filter(Order.user_id == user_id).all()
    
    def get_order_details(self, order_id: int) -> list[OrderDetails]:
        return self.db.session.query(OrderDetails).filter(OrderDetails.order_id == order_id).all()
