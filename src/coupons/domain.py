from pydantic import BaseModel
from typing import List

from datetime import datetime

class CouponCreate(BaseModel):
    code: str
    discount: int
    expiration_date: datetime 
    