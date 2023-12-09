import uuid
from decimal import Decimal
from typing import Sequence

from sqlalchemy import and_, select

from src.db import schemas
from src.db.models import Bot, Deal, DealType, Instrument, User
from src.db.sql import SQLManager
from src.utils.logger import conf_logger


class InstrumentDAL:
    """Data access layer for instruments"""

    instance = None

    def __init__(self, db_manager: SQLManager) -> None:
        super().__init__()
        self.db = db_manager
        self.logger = conf_logger("InsturmentDAL", "D")

    def __new__(cls, *args, **kwargs):
        """Singleton pattern"""
        if cls.instance is None:
            cls.instance = super(InstrumentDAL, cls).__new__(cls)
        return cls.instance

    def add(
        self,
        instrument_data: schemas.Instrument,
    ) -> Instrument:
        instrument = Instrument(code=instrument_data.code, title=instrument_data.title)
        self.db.session.add(instrument)
        self.db.session.commit()

        return instrument

    def get(self, instrument: schemas.InstrumentBase) -> Instrument | None:
        return self.db.session.get(Instrument, instrument.code)

    def update(self, user: User):
        self.db.session.add(user)
        self.db.session.commit()

    def delete(self, code: str):
        instrument = self.db.session.get(Instrument, code)
        if instrument:
            self.db.session.delete(instrument)
            self.db.session.commit()

    def get_all(self) -> Sequence[Instrument]:
        return self.db.session.scalars(select(Instrument)).all()

    # def add_user_instrument(
    #     self, user_id: uuid.UUID, instrument_data: schemas.InstrumentBase
    # ) -> schemas.Instrument:
    #     instrument = self.get(instrument_data)
    #     if not instrument:
    #         instrument = Instrument(**instrument_data.model_dump())
    #     stmt = select(User).where(User.id == user_id)
    #     user = self.db.session.scalars(stmt).one()
    #     user.instruments.append(instrument)
    #     self.db.session.merge(user)
    #     self.db.session.commit()
    #     return instrument

    # def get_user_instruments(self, user_id: uuid.UUID) -> list[schemas.Instrument]:
    #     stmt = (
    #         select(Instrument)
    #         .join(Instrument.deals)
    #         .where(Deal.user_id == user_id)
    #         .distinct()
    #     )
    #     instruments = self.db.session.scalars(stmt).all()
    #     return [
    #         schemas.Instrument(
    #             code=instrument.code,
    #             title=instrument.title,
    #             group=instrument.group,
    #         )
    #         for instrument in instruments
    #     ]


class DealDAL:
    """Data access layer for deals"""

    instance = None

    def __init__(self, db_manager: SQLManager) -> None:
        super().__init__()
        self.db = db_manager
        self.logger = conf_logger("DealDAL")

    def __new__(cls, *args, **kwargs):
        """Singleton pattern"""
        if cls.instance is None:
            cls.instance = super(DealDAL, cls).__new__(cls)
        return cls.instance

    def add(
        self,
        instrument_code: str,
        price: Decimal,
        quantity: int,
        deal_type: DealType,
        user_id: uuid.UUID,
    ) -> Deal:
        deal = Deal(
            instrument_code=instrument_code,
            price=price,
            quantity=quantity,
            deal_type=deal_type,
            user_id=user_id,
        )
        self.db.session.add(deal)
        self.db.session.commit()

        return deal

    def get_user_deals(self, user_id: str) -> list[Deal] | None:
        user = self.db.session.get(User, user_id)
        if user:
            return user.deals

    def get_user_deals_by_instrument(
        self, user_id: uuid.UUID, deals_request: schemas.UserDealsRequest
    ) -> Sequence[Deal]:
        stmt = select(Deal).where(
            and_(
                Deal.instrument_code == deals_request.instrument_code,
                Deal.user_id == user_id,
            )
        )
        return self.db.session.scalars(stmt).all()

class BotDAL:
    """Data access layer for bots"""

    instance = None

    def __init__(self, db_manager: SQLManager) -> None:
        super().__init__()
        self.db = db_manager
        self.logger = conf_logger("BotDAL", "D")

    def __new__(cls, *args, **kwargs):
        """Singleton pattern"""
        if cls.instance is None:
            cls.instance = super(BotDAL, cls).__new__(cls)
        return cls.instance

    def add(
        self,
        user_id: uuid.UUID,
        code: schemas.InstrumentBase,
    ) -> Bot:
        bot = Bot(user_id=user_id, instrument_code=code.code)
        self.db.session.add(bot)
        # TODO: check is bot exist
        self.db.session.commit()

        return bot

    def get(
        self,
        user_id: uuid.UUID,
        code: schemas.InstrumentBase,
    ) -> Bot | None:
        bot = self.db.session.get(Bot, (user_id, code.code))
        if bot:
            return bot

    def get_bot_status(
        self, user_id: uuid.UUID, instrument: schemas.InstrumentBase
    ) -> schemas.Bot | None:
        bot = self.db.session.get(Bot, (user_id, instrument.code))
        if bot:
            return bot

    def bot_toggle_status(
        self, user_id: uuid.UUID, instrument: schemas.InstrumentBase
    ) -> schemas.Bot | None:
        bot = self.db.session.get(Bot, (user_id, instrument.code))
        if bot:
            bot.status = not bot.status
            self.db.session.merge(bot)
            self.db.session.commit()
            return bot

    def get_all_user_bots(self, user_id: uuid.UUID) -> Sequence[Bot]:
        return self.db.session.scalars(select(Bot).where(Bot.user_id == user_id)).all()



