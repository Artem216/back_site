from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from typing import List
from src.coupons.domain import CouponCreate
from src.coupons.repository import CouponRepository

from src.user.domain import UserDto

from src.user.domain import UserRole

from src.db.dependencies import get_coupon_repository, get_current_user

router = APIRouter(prefix="/coupons", tags=["coupons"])


@router.post("/create", response_model= None)
def create_coupon(
    coupon: CouponCreate,
    current_user: UserDto = Depends(get_current_user),
    repository: CouponRepository = Depends(get_coupon_repository),
):
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return repository.add(coupon, current_user.id)


@router.get("/", response_model= None)
def get_active_cupons(
    current_user: UserDto = Depends(get_current_user),
    repository: CouponRepository = Depends(get_coupon_repository)
):
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    return repository.get_active()