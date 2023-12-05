from __future__ import annotations

import enum
import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class DealType(enum.Enum):
    model_config = ConfigDict(from_attributes=True)

    buy = "buy"
    sell = "sell"


class InstrumentBase(BaseModel):
    code: str = Field(..., min_length=1, max_length=50)


class InstrumentCreate(InstrumentBase):
    title: str = Field(..., min_length=1, max_length=256)
    group: str = Field(..., min_length=1, max_length=50)


class Instrument(InstrumentBase):
    model_config = ConfigDict(from_attributes=True)

    deals: list[Deal] = []
    users: list[User] = []


class DealBase(BaseModel):
    price: Decimal = Field(ge=0.01, decimal_places=2)
    quantity: int = Field(ge=1)
    deal_type: DealType
    user: User
    instrument: Instrument


class Deal(DealBase):
    id: int
    datetime: datetime


class UserBase(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=256)


class UserSignup(UserBase):
    first_name: str = Field(..., min_length=2, max_length=30)
    last_name: str = Field(..., min_length=2, max_length=30)


class UserLogin(UserBase):
    ...


class User(UserSignup):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    deals: list[Deal]
    instruments: list[Instrument]
