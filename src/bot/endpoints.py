from fastapi import APIRouter, Depends, HTTPException, status
from src.bot.repository import BotDAL
from src.db import schemas
from src.db.dependencies import get_bot_dal, get_current_user
from src.user.domain import UserDto
from src.utils.logger import conf_logger

logger = conf_logger(__name__, "D")


router = APIRouter(prefix="/bot", tags=["bot"])


@router.post(
    "/add_bot",
    response_model=schemas.Instrument,
    status_code=status.HTTP_200_OK,
)
async def add_bot(
    instrument_data: schemas.InstrumentBase,
    current_user: UserDto = Depends(get_current_user),
    bot_dal: BotDAL = Depends(get_bot_dal),
) -> schemas.Bot:
    bot = bot_dal.add(current_user.id, instrument_data)
    if bot:
        return bot
    else:
        raise HTTPException(status_code=404, detail="Bot not found")


@router.post(
    "/bot_status",
    response_model=schemas.Bot,
    status_code=status.HTTP_200_OK,
)
async def get_bot_status(
    instrument_data: schemas.InstrumentBase,
    current_user: UserDto = Depends(get_current_user),
    bot_dal: BotDAL = Depends(get_bot_dal),
) -> schemas.Bot:
    bot = bot_dal.get_bot_status(user_id=current_user.id, instrument=instrument_data)
    if bot:
        return bot
    else:
        raise HTTPException(status_code=404, detail="Bot not found")

@router.post(
    "/bot_toggle_status",
    response_model=schemas.Bot,
    status_code=status.HTTP_200_OK,
)
async def bot_toggle_status(
    instrument_data: schemas.InstrumentBase,
    current_user: UserDto = Depends(get_current_user),
    bot_dal: BotDAL = Depends(get_bot_dal),
) -> schemas.Bot:
    bot = bot_dal.bot_toggle_status(user_id=current_user.id, instrument=instrument_data)
    if bot:
        return bot
    else:
        raise HTTPException(status_code=404, detail="Bot not found")

