from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from  src.cart.domain import CartCreate, CartItemCreate
from src.cart.repository import CartRepository

from typing import List

from src.cart.model import Cart, CartItem

from src.user.domain import UserDto

import json

from src.db.dependencies import get_cart_repository, get_current_user

router = APIRouter(prefix="/cart", tags=["cart"])

@router.post("/create", response_model=None)
def create_cart(
    cart: CartCreate,
    current_user: UserDto = Depends(get_current_user),
    repository: CartRepository = Depends(get_cart_repository),
):
    
    created_cart = repository.add(current_user.id, cart)
    return created_cart


@router.post("/cart/items", response_model=None)
def add_item_to_cart(
    items: list[CartItemCreate],
    current_user: UserDto = Depends(get_current_user),
    repository: CartRepository = Depends(get_cart_repository),
):
    cart: Cart = repository.get(current_user.id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    for item in items:
        cart.items.append(CartItem(**item.model_dump()))
        cart.total_items += item.quantity
    
    repository.update(cart)
    
    return cart

@router.get("/", response_model=None)
def get_cart(
    current_user: UserDto = Depends(get_current_user),
    repository: CartRepository = Depends(get_cart_repository),
):
    cart = repository.get(current_user.id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart

@router.get("/{cart_id}/products", response_model=None)
def get_products_from_cart(
    current_user: UserDto = Depends(get_current_user),
    repository: CartRepository = Depends(get_cart_repository),
):
    items:list[CartItem] = repository.get_items(current_user.id)    
    if not items:
        raise HTTPException(status_code=404, detail="No product in cart")
    return items





# @router.put("/{cart_id}", response_model=None)
# def update_cart(
#     cart_id: int,
#     cart: CartCreate,
#     repository: CartRepository = Depends(get_cart_repository),
# ):
#     existing_cart = repository.get(cart_id)
#     if not existing_cart:
#         raise HTTPException(status_code=404, detail="Cart not found")
    
#     updated_cart = repository.update(cart)
#     return updated_cart


# @router.delete("/{cart_id}")
# def delete_cart(
#     cart_id: int,
#     repository: CartRepository = Depends(get_cart_repository),
# ):
#     cart = repository.get(cart_id)
#     if not cart:
#         raise HTTPException(status_code=404, detail="Cart not found")
    
#     repository.delete(cart)