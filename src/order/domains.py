from enum import Enum
from pydantic import BaseModel, Field, ConfigDict

from datetime import datetime, timedelta

class OrderStatus(str, Enum):
    in_process = "В обработке"
    assembly = "Сборка"
    on_the_way = "В пути"
    received = "Получен"


class OrderDetails(BaseModel):    

    product_id: int = Field(...)
    quantity: int = Field(...)


class OrderDetailsCreate(BaseModel):
    # id: int = Field(...)
    
    product_id: int = Field(...)
    quantity: int = Field(...)


class OrderBase(BaseModel):
    # id: int = Field(...)
    date: datetime = Field(
        ..., example=datetime.now() + timedelta(days=1)
    )
    status: OrderStatus = Field(...)


class OrderCreate(OrderBase):
    details: list[OrderDetailsCreate] = Field(...)



