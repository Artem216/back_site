from __future__ import annotations

import enum
import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from src.db.models import DealType


class InstrumentBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    code: str = Field(..., min_length=1, max_length=50)


class Instrument(InstrumentBase):
    title: str = Field(..., min_length=1, max_length=256)
    group: str = Field(..., min_length=1, max_length=50)


class DealBase(BaseModel):
    price: Decimal = Field(ge=0.01, decimal_places=2)
    quantity: int = Field(ge=1)
    deal_type: DealType
    user: uuid.UUID
    instrument: str
    balance: Decimal


class Deal(DealBase):
    id: int
    datetime: datetime


class UserDealsRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    instrument_code: str


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


class Bot(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    instrument_code: str
    status: bool

