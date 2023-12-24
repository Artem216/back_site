from pydantic import BaseModel
from typing import List


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int
    price: float


class CartCreate(BaseModel):
    total_items: int
    total_price: float
    items: List[CartItemCreate]