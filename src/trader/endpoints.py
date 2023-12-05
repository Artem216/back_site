from fastapi import APIRouter, Depends, status
from src.db import schemas
from src.db.dependencies import (
    get_current_user,
    get_instrument_repository,
    get_user_repository,
)
from src.trader.repository import InstrumentRepository
from src.user.domain import UserDto
from src.user.repository import UserRepository

router = APIRouter(prefix="/trader", tags=["trader"])


@router.post(
    "/add_user_instrument",
    response_model=schemas.InstrumentCreate,
    status_code=status.HTTP_200_OK,
)
async def add_instrument_to_user(
    instrument_data: schemas.InstrumentBase,
    current_user: UserDto = Depends(get_current_user),
    instrument_repository: InstrumentRepository = Depends(get_instrument_repository),
) -> schemas.Instrument:
    instrument = instrument_repository.add_user_instrument(current_user.id, instrument_data)
    return instrument


@router.get(
    "/instrument_all",
    response_model=list[schemas.InstrumentCreate],
    status_code=status.HTTP_200_OK,
)
async def get_all_instruments(
    # current_user: UserDto = Depends(get_current_user),
    instrument_repository: InstrumentRepository = Depends(get_instrument_repository),
) -> list[schemas.Instrument]:
    return instrument_repository.get_all()


@router.get(
    "/user_instruments",
    response_model=list[schemas.InstrumentCreate],
    status_code=status.HTTP_200_OK,
)
async def get_user_instruments(
    current_user: UserDto = Depends(get_current_user),
    instrument_repository: InstrumentRepository = Depends(get_instrument_repository),
) -> list[schemas.Instrument]:
    return instrument_repository.get_user_instruments(current_user.id)

