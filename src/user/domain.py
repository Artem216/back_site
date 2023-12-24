import uuid
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from enum import Enum

from typing import Optional

class UserRole(str, Enum):
    admin = "admin"
    person = "person"



class UserDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    role: UserRole 
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
