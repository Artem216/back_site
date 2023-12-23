from pydantic import BaseModel
from typing import List


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int


class CartCreate(BaseModel):
    total_items: int
    items: List[CartItemCreate]