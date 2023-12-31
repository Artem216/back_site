from fastapi import Depends, HTTPException, status
from src.auth.jwt import decode_jwt, oauth2_scheme
from src.db.sql import SQLManager
from src.user.domain import UserDto
from src.user.repository import UserRepository
from src.order.repository import OrderRepository
from src.cart.repository import CartRepository
from src.coupons.repository import CouponRepository 
# from src.utils.logger import conf_logger

# logger = conf_logger(__name__)


async def get_db() -> SQLManager:
    """Get the database connection"""
    return SQLManager()


async def get_user_repository(db: SQLManager = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

async def get_order_repository(db: SQLManager = Depends(get_db)) -> OrderRepository:
    return OrderRepository(db)


async def get_cart_repository(db: SQLManager = Depends(get_db)) -> CartRepository:
    return CartRepository(db)

async def get_coupon_repository(db: SQLManager = Depends(get_db)) -> CartRepository:
    return CouponRepository(db)


async def get_current_user(
    access_token: str | None = Depends(oauth2_scheme),
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserDto | None:
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated (current_user)",
        )
    user_id = decode_jwt(access_token)
    print(user_repository.get(user_id=user_id).role)
    return UserDto.model_validate(user_repository.get(user_id=user_id))