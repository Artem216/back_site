from fastapi import APIRouter, status, Depends, HTTPException
from typing import List, Union, Optional
from .model import Order

from src.order.repository import OrderRepository
from src.order.domains import OrderCreate

from src.order.model import OrderDetails

from src.cart.repository import CartRepository
from src.cart.model import CartItem

from src.user.domain import UserDto

from src.db.dependencies import get_order_repository, get_current_user, get_cart_repository

router = APIRouter(prefix="/orders", tags=["order"])




@router.post("/create", response_model=int , status_code=status.HTTP_201_CREATED)
def create_order(
    repository: OrderRepository = Depends(get_order_repository),
    cart_repository: CartRepository = Depends(get_cart_repository),
    current_user: UserDto = Depends(get_current_user)) -> int:
    
    items: list[CartItem]  = cart_repository.get_items(current_user.id)
    if not items:
        raise HTTPException(status_code=404, detail="No Items in cart")
    
    add_order = repository.add(current_user.id ,items)
    cart = cart_repository.get(current_user.id)
    # print(f"{cart.id} {cart.total_items} {}" )
    cart_repository.delete(cart)

    return add_order

    
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
    repository: OrderRepository = Depends(get_order_repository),
    current_user: UserDto = Depends(get_current_user)
) -> list[OrderDetails]:
    order_details = repository.get_order_details(order_id=order_id)
    return order_details