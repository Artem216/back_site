from fastapi import APIRouter, status, Depends
from typing import List, Union, Optional
from .model import Order, OrderDetails

from src.order.repository import OrderRepository
from src.order.domains import OrderCreate


from src.user.domain import UserDto

from src.db.dependencies import get_order_repository, get_current_user

router = APIRouter(prefix="/orders", tags=["order"])




@router.post("/create", response_model=int , status_code=status.HTTP_201_CREATED)
def create_order(
    orders: list[OrderCreate],
    repository: OrderRepository = Depends(get_order_repository),
    current_user: UserDto = Depends(get_current_user)) -> int:
    
    return repository.add(current_user.id ,orders)

    
@router.get("/get_all_user_orders", response_model= None, status_code=status.HTTP_200_OK )
def get_all_orders(
    current_user: UserDto = Depends(get_current_user),
    repository: OrderRepository = Depends(get_order_repository),
) ->  Union[list[Order], int]:
    orders = repository.get_all(current_user.id)
    if orders == []:
        return 0
    return orders

@router.get("/order/{order_id}/details", response_model=None, status_code=status.HTTP_200_OK )
def get_order_details(
    order_id: int,
    repository: OrderRepository = Depends(get_order_repository)
) -> list[OrderDetails]:
    order = repository.get_order_details(order_id=order_id)
    return order.details