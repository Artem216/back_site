from fastapi import APIRouter
from src.user.endpoints import router as user_router

from src.cart.endpoints import router as cart_router
from src.order.endpoints import router as order_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(cart_router)
api_router.include_router(order_router)
api_router.include_router(user_router)
