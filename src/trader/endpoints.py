from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, status
from src.db import schemas
from src.db.dependencies import (
    get_bot_dal,
    get_current_user,
    get_deal_dal,
    get_instrument_dal,
)
from src.db.models import DealType
from src.trader.repository import BotDAL, DealDAL, InstrumentDAL
from src.user.domain import UserDto
from src.utils.logger import conf_logger

logger = conf_logger(__name__, "D")

router = APIRouter(prefix="/trader", tags=["trader"])


@router.get(
    "/instrument_all",
    response_model=list[schemas.Instrument],
    status_code=status.HTTP_200_OK,
)
async def get_all_instruments(
    instrument_repository: InstrumentDAL = Depends(get_instrument_dal),
) -> list[schemas.Instrument]:
    instruments = instrument_repository.get_all()
    return [
        schemas.Instrument(
            code=instrument.code,
            title=instrument.title,
            group=instrument.group,
        )
        for instrument in instruments
    ]


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
    deals = deal_dal.get_user_deals_by_instrument(current_user.id, deal_request.instrument_code)
    return [
        schemas.Deal(
            id=deal.id,
            price=deal.price,
            quantity=deal.quantity,
            deal_type=deal.deal_type,
            user=deal.user.id,
            instrument=deal.instrument_code,
            datetime=deal.date_time,
            balance=deal.balance,
        )
        for deal in deals
    ]


@router.post(
    "/add_bot",
    response_model=schemas.Bot,
    status_code=status.HTTP_200_OK,
)
async def add_bot(
    bot_data: schemas.Bot,
    current_user: UserDto = Depends(get_current_user),
    bot_dal: BotDAL = Depends(get_bot_dal),
) -> schemas.Bot:
    bot = bot_dal.get(current_user.id, bot_data.instrument_code)
    if not bot:
        bot = bot_dal.add(current_user.id, bot_data )
        return schemas.Bot(instrument_code=bot.instrument_code, status=bot.status, start_balance=bot.start_balance)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Bot already exist"
        )


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
        return schemas.Bot(instrument_code=bot.instrument_code, status=bot.status, start_balance=bot.start_balance)
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
        return schemas.Bot(instrument_code=instrument_data.code, status=bot.status, start_balance=bot.start_balance)
    else:
        raise HTTPException(status_code=404, detail="Bot not found")


@router.get(
    "/get_all_user_bots",
    response_model=list[schemas.BotWithCurrentBalance],
    status_code=status.HTTP_200_OK,
)
async def get_user_bots(
    current_user: UserDto = Depends(get_current_user),
    bot_dal: BotDAL = Depends(get_bot_dal),
    deal_dal: DealDAL = Depends(get_deal_dal),
) -> list[schemas.BotWithCurrentBalance]:
    bots = bot_dal.get_all_user_bots(current_user.id)
    bot_result_list = []
    for bot in bots:
        bot_deals = deal_dal.get_user_deals_by_instrument(current_user.id, bot.instrument_code)
        if bot_deals:
            current_balance = bot_deals[-1].balance
        else:
            current_balance = bot.start_balance
        # deals_end_sum = bot.start_balance + sum([deal.price * deal.quantity for deal in bot_deals])
        current_balance = (
            bot.start_balance
            + sum(
                [
                    deal.price * deal.quantity
                    for deal in bot_deals
                    if deal.deal_type == DealType.sell
                ]
            )
            - sum(
                [
                    deal.price * deal.quantity
                    for deal in bot_deals
                    if deal.deal_type == DealType.buy
                ]
            )
        )

        bot_result_list.append(
            schemas.BotWithCurrentBalance(
                instrument_code=bot.instrument_code,
                status=bot.status,
                start_balance=bot.start_balance,
                current_balance=Decimal(current_balance),
            )
        )
    return bot_result_list



    # return [
    #     schemas.BotWithCurrentBalance(instrument_code=bot.instrument_code, status=bot.status, start_balance=bot.start_balance)
    #     for bot in bots
    # ]

