import uuid
from typing import Sequence

from sqlalchemy import and_, distinct, select
from src.db import schemas
from src.db.models import Deal, DealType, Instrument, User
from src.db.repository import AbstractRepository
from src.db.sql import SQLManager
from src.utils.logger import conf_logger as logger


class InstrumentDAL:
    """Data access layer for instruments"""

    instance = None

    def __init__(self, db_manager: SQLManager) -> None:
        super().__init__()
        self.db = db_manager
        self.logger = logger("InsturmentDAL", "D")

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

    def get_all(self) -> list[schemas.Instrument]:
        instruments = self.db.session.scalars(select(Instrument)).all()
        return [schemas.Instrument(
            code=instrument.code,
            title=instrument.title,
            group=instrument.group,
            ) for instrument in instruments]

    def add_user_instrument(
        self, user_id: uuid.UUID, instrument_data: schemas.InstrumentBase
    ) -> schemas.Instrument:
        instrument = self.get(instrument_data)
        if not instrument:
            instrument = Instrument(**instrument_data.model_dump())
        stmt = select(User).where(User.id == user_id)
        user = self.db.session.scalars(stmt).one()
        user.instruments.append(instrument)
        self.db.session.merge(user)
        self.db.session.commit()
        return instrument

    def get_user_instruments(self, user_id: uuid.UUID) -> list[schemas.Instrument]:
        stmt = select(Instrument).join(Instrument.deals).where(Deal.user_id == user_id).distinct()
        instruments = self.db.session.scalars(stmt).all()
        return [schemas.Instrument(
                code=instrument.code,
                title=instrument.title,
                group=instrument.group,
                ) for instrument in instruments]


class DealDAL:
    """Data access layer for deals"""

    instance = None

    def __init__(self, db_manager: SQLManager) -> None:
        super().__init__()
        self.db = db_manager
        self.logger = logger("DealDAL")

    def __new__(cls, *args, **kwargs):
        """Singleton pattern"""
        if cls.instance is None:
            cls.instance = super(DealDAL, cls).__new__(cls)
        return cls.instance

    def add(
        self,
        deal_data: schemas.DealBase,
    ) -> Deal:
        deal = Instrument(**deal_data.model_dump())
        self.db.session.add(deal)
        self.db.session.commit()

        return deal

    def get_user_deals(self, user_id: str) -> list[Deal] | None:
        user = self.db.session.get(User, user_id)
        if user:
            return user.deals

    def get_user_deals_by_instrument(
        self, user_id: uuid.UUID, deals_request: schemas.UserDealsRequest
    )  -> list[schemas.Deal]:
        self.logger.debug(f"{deals_request=}")
        stmt = select(Deal).where(
            and_(
                Deal.instrument_code == deals_request.instrument_code,
                Deal.user_id == user_id,
            )
        )
        deals = list(self.db.session.scalars(stmt).all())
        return [schemas.Deal(
            id=deal.id,
            price=deal.price,
            quantity=deal.quantity,
            deal_type=deal.deal_type,
            user=deal.user.id,
            instrument=deal.instrument_code,
            datetime=deal.date_time,
        ) for deal in deals]



