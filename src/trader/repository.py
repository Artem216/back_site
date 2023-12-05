from typing import Sequence
import uuid
from sqlalchemy import select
from src.auth.domain import Signup
from src.db.models import Instrument, User
from src.db.repository import AbstractRepository
from src.db.sql import SQLManager
from src.utils.logger import conf_logger as logger
from src.db import schemas


class InstrumentRepository(AbstractRepository):
    instance = None

    def __init__(self, db_manager: SQLManager) -> None:
        super().__init__()
        self.db = db_manager
        self.logger = logger("InsturmentRepository")

    def __new__(cls, *args, **kwargs):
        """Singleton pattern"""
        if cls.instance is None:
            cls.instance = super(InstrumentRepository, cls).__new__(cls)
        return cls.instance

    def add(
        self,
        instrument_data: schemas.InstrumentCreate,
    ) -> Instrument:
        # instrument = Instrument(**instrument_data.model_dump())
        instrument = Instrument(
                code= instrument_data.code,
                title= instrument_data.title
                )
        self.db.session.add(instrument)
        self.db.session.commit()

        return instrument

    def get(self, code: str) -> Instrument | None:
        return self.db.session.get(Instrument, code)

    def update(self, user: User):
        self.db.session.add(user)
        self.db.session.commit()

    def delete(self, code: str):
        instrument = self.db.session.get(Instrument, code)
        if instrument:
            self.db.session.delete(instrument)
            self.db.session.commit()

    def get_all(self) -> list[Instrument]:
        return list(self.db.session.scalars(select(Instrument)).all())

    def get_user_instruments(self, user_id: uuid.UUID) -> list:
        stmt = select(User).where(User.id == user_id)
        return self.db.session.scalars(stmt).one().instruments


class DealRepository(AbstractRepository):
    instance = None

    def __init__(self, db_manager: SQLManager) -> None:
        super().__init__()
        self.db = db_manager
        self.logger = logger("DealRepository")

    def __new__(cls, *args, **kwargs):
        """Singleton pattern"""
        if cls.instance is None:
            cls.instance = super(DealRepository, cls).__new__(cls)
        return cls.instance

    def add(
        self,
        instrument_data: schemas.InstrumentCreate,
    ) -> Instrument:
        instrument = Instrument(**instrument_data.model_dump())
        self.db.session.add(instrument)
        self.db.session.commit()

        return instrument

    def get(self, code: str) -> Instrument | None:
        return self.db.session.get(Instrument, code)

    def update(self, user: User):
        self.db.session.add(user)
        self.db.session.commit()

    def delete(self, code: str):
        instrument = self.db.session.get(Instrument, code)
        if instrument:
            self.db.session.delete(instrument)
            self.db.session.commit()

    # def get_user_deals(self, user_id: uuid.UUID) -> list[DealSchema]:
    #     stmt = select(User).where(User.id == user_id)
    #     deals = self.db.session.scalars(stmt).one().deals
    #     return [DealSchema.model_validate(deal) for deal in deals]
