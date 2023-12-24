from src.db.repository import AbstractRepository

from src.db.sql import SQLManager
from src.utils.logger import get_logger

from src.coupons.model import Coupon

from src.coupons.domain import CouponCreate

from datetime import datetime

class CouponRepository(AbstractRepository):

    instance = None


    def __init__(self,db_manager: SQLManager):
        super().__init__()
        self.db = db_manager
        self.logger = get_logger("OrderRepository")

    def __new__(cls, *args, **kwargs):
        """Singleton pattern"""
        if cls.instance is None:
            cls.instance = super(CouponRepository, cls).__new__(cls)
        return cls.instance

    def add(self, coupon: CouponCreate, user_id: int) -> Coupon:

        coupon_db = Coupon(**coupon.model_dump(), user_id= user_id)
        self.db.session.add(coupon_db)
        self.db.session.commit()
        return coupon

    def get(self, coupon_id: int) -> Coupon:
        return self.db.session.query(Coupon).filter_by(id=coupon_id).first()

    def delete(self, coupon: Coupon) -> None:
        self.db.session.delete(coupon)
        self.db.session.commit()

    def update(self, coupon: Coupon) -> Coupon:
        self.db.session.commit()
        return coupon

    def get_all(self, user_id: int) -> list[Coupon]:
        return self.db.session.query(Coupon).filter_by(user_id=user_id).all()   
    
    def get_active(self) -> Coupon:
        date_now = datetime.now()
        return self.db.session.query(Coupon).filter(Coupon.expiration_date > date_now).first()
    
    def appoint_coupon(self, coupon: Coupon, user_id: int) -> None:
        coupon_db: Coupon = Coupon(
            code= coupon.code,
            discount= coupon.discount,
            expiration_date= coupon.expiration_date,
            is_used= False,
            user_id= user_id
            )
        self.db.session.add(coupon_db)
        self.db.session.commit()