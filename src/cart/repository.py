from src.db.sql import SQLManager
from src.cart.model import Cart, CartItem
from src.cart.domain import CartCreate

from src.db.repository import AbstractRepository


class CartRepository(AbstractRepository):
    def __init__(self, db_manager: SQLManager):
        self.db = db_manager

    def add(self,user_id: int, cart_data: CartCreate) -> Cart:
        cart_db = self.db.session.query(Cart).filter(Cart.user_id == user_id).first()
        if cart_db:
            return cart_db
        cart_db = Cart(**cart_data.model_dump(exclude="items"), user_id= user_id)
        for item in cart_data.items:
            cart_db.items.append(CartItem(**item.model_dump()))
        
        self.db.session.add(cart_db)
        self.db.session.commit()
        
        return cart_db

    def get(self, user_id: int) -> Cart:
        return self.db.session.query(Cart).filter(Cart.user_id == user_id).first()

    def delete(self, cart: Cart) -> None:
        self.db.session.delete(cart)
        self.db.session.commit()

    def update(self, cart: Cart) -> Cart:
        self.db.session.add(cart)
        self.db.session.commit()
        return cart

    def get_all(self, user_id: int) -> list[Cart]:
        return self.db.session.query(Cart).filter(Cart.user_id == user_id).all()
    
    def get_items(self, user_id: int) -> list[CartItem]:
        user_cart_db = self.db.session.query(Cart).filter(Cart.user_id == user_id).first()
        cart_id = user_cart_db.id
        return self.db.session.query(CartItem).filter(CartItem.cart_id == cart_id).all()