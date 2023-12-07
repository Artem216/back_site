from fastapi import APIRouter, Depends, status
from src.db import schemas
from src.db.dependencies import (
    get_current_user,
    get_deal_dal,
    get_instrument_dal,
    get_user_repository,
)
from src.db.models import Deal
from src.trader.repository import DealDAL, InstrumentDAL
from src.user.domain import UserDto
from src.user.repository import UserRepository
from src.utils.logger import conf_logger

logger = conf_logger(__name__, "D")

router = APIRouter(prefix="/trader", tags=["trader"])


@router.post(
    "/add_user_instrument",
    response_model=schemas.Instrument,
    status_code=status.HTTP_200_OK,
)
async def add_instrument_to_user(
    instrument_data: schemas.InstrumentBase,
    current_user: UserDto = Depends(get_current_user),
    instrument_repository: InstrumentDAL = Depends(get_instrument_dal),
) -> schemas.Instrument:
    instrument = instrument_repository.add_user_instrument(
        current_user.id, instrument_data
    )
    return instrument


@router.get(
    "/instrument_all",
    response_model=list[schemas.Instrument],
    status_code=status.HTTP_200_OK,
)
async def get_all_instruments(
    instrument_repository: InstrumentDAL = Depends(get_instrument_dal),
) -> list[schemas.Instrument]:
    return instrument_repository.get_all()


@router.get(
    "/user_instruments",
    response_model=list[schemas.Instrument],
    status_code=status.HTTP_200_OK,
)
async def get_user_instruments(
    current_user: UserDto = Depends(get_current_user),
    instrument_dal: InstrumentDAL = Depends(get_instrument_dal),
) -> list[schemas.Instrument]:
    return instrument_dal.get_user_instruments(current_user.id)


@router.post(
    "/user_deals_by_instrument",
    response_model=list[schemas.Deal],
    status_code=status.HTTP_200_OK,
)
async def get_user_deals_by_instrument(
    deal_request: schemas.UserDealsRequest,
    current_user: UserDto = Depends(get_current_user),
    deal_dal: DealDAL = Depends(get_deal_dal),
) -> list[schemas.Deal]:
    return deal_dal.get_user_deals_by_instrument(current_user.id, deal_request)

