# import uuid
#
# from sqlalchemy import select
# from src.db import schemas
# from src.db.models import Bot
# from src.db.sql import SQLManager
# from src.utils.logger import conf_logger
#
#
# class BotDAL:
#     """Data access layer for bots"""
#
#     instance = None
#
#     def __init__(self, db_manager: SQLManager) -> None:
#         super().__init__()
#         self.db = db_manager
#         self.logger = conf_logger("BotDAL", "D")
#
#     def __new__(cls, *args, **kwargs):
#         """Singleton pattern"""
#         if cls.instance is None:
#             cls.instance = super(BotDAL, cls).__new__(cls)
#         return cls.instance
#
#     def add(
#         self,
#         user_id: uuid.UUID,
#         code: schemas.InstrumentBase,
#     ) -> Bot:
#         bot = Bot(user_id=user_id, instrument_code=code.code)
#         self.db.session.add(bot)
#         # TODO: check is bot exist
#         self.db.session.commit()
#
#         return bot
#
#     def get(
#         self,
#         user_id: uuid.UUID,
#         code: schemas.InstrumentBase,
#     ) -> Bot | None:
#         bot = self.db.session.get(Bot, (user_id, code.code))
#         if bot:
#             return bot
#
#     def get_bot_status(
#         self, user_id: uuid.UUID, instrument: schemas.InstrumentBase
#     ) -> schemas.Bot | None:
#         bot = self.db.session.get(Bot, (user_id, instrument.code))
#         if bot:
#             return bot
#
#     def bot_toggle_status(
#         self, user_id: uuid.UUID, instrument: schemas.InstrumentBase
#     ) -> schemas.Bot | None:
#         bot = self.db.session.get(Bot, (user_id, instrument.code))
#         if bot:
#             bot.status = not bot.status
#             self.db.session.merge(bot)
#             self.db.session.commit()
#             return bot
#
#     def get_all_active(self) -> list[schemas.Bot]:
#         bots = self.db.session.scalars(select(Bot).where(Bot.status == True)).all()
#         return [
#             schemas.Bot(instrument_code=bot.instrument_code, status=bot.status)
#             for bot in bots
#         ]
#
