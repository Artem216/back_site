import math
import time
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Literal

import pandas as pd
import pandas_ta as ta
from moexalgo import Ticker

from src.bot.repository import BotDAL
from src.db.models import DealType
from src.db.sql import SQLManager
from src.trader.repository import DealDAL
from src.utils.logger import conf_logger

logger = conf_logger(__name__, "D")


class Bot:
    def __init__(self, user_id, instrument_code: str, status: bool, balance) -> None:
        self.user_id = user_id
        self.instrument_code = instrument_code
        self.status = status
        self.balance = balance
        self.candles: pd.DataFrame = pd.DataFrame()
        self.bot_dal = BotDAL(SQLManager())
        self.deal_dal = DealDAL(SQLManager())
        self.in_stock = 0

    def sell_request(self, price):
        logger.debug(
            "Sell request for instrument: %s, price: %s, quantity: %s",
            self.instrument_code,
            price,
            self.in_stock,
        )
        self._add_deal_to_db(
            price=price, quantity=self.in_stock, deal_type=DealType.sell
        )
        self.balance += price * self.in_stock
        self.in_stock = 0

    def buy_request(self, price, quantity):
        logger.debug(
            "Buy request for instrument: %s, price: %s, quantity: %s",
            self.instrument_code,
            price,
            quantity,
        )
        self._add_deal_to_db(price=price, quantity=quantity, deal_type=DealType.buy)
        self.balance -= price * quantity
        self.in_stock += quantity

    def _add_deal_to_db(self, price, quantity, deal_type):
        self.deal_dal.add(
            instrument_code=self.instrument_code,
            price=price,
            quantity=quantity,
            deal_type=deal_type,
            user_id=self.user_id,
        )

    def get_candles(self, period: str = "10m") -> pd.DataFrame:
        logger.debug("Getting candles for %s", self.instrument_code)
        now = datetime.now(timezone(timedelta(hours=3)))
        now = now.replace(minute=0, second=0, microsecond=0) - timedelta(hours=1)
        now = now.replace(tzinfo=None)
        start = now - timedelta(days=10)
        ticket = Ticker(self.instrument_code)
        data = pd.DataFrame(ticket.candles(date=start, till_date=now, period=period))
        data = data[-30:].reset_index(drop=True)
        return data  # pyright: ignore

    @staticmethod
    def indicator_rsi(data: pd.DataFrame, min_lvl=30, max_lvl=70, lenght=14) -> list[Literal[0, 1, 2]]:
        rsi = data.ta.rsi(length=lenght).to_list()
        for i in range(len(data)):
            if math.isnan(rsi[i]):
                rsi[i] = 0
            elif rsi[i] >= max_lvl:
                rsi[i] = 1
            elif rsi[i] <= min_lvl:
                rsi[i] = 2
            else:
                rsi[i] = 0
        return rsi

    @staticmethod
    def indicator_alligator(data: pd.DataFrame, lenght=[13, 8, 5], offset=[8, 5, 3]) -> list[Literal[0, 1, 2]]:
        jaw = data.ta.sma(length=lenght[0], offset=offset[0])
        teeth = data.ta.sma(length=lenght[1], offset=offset[1])
        lips = data.ta.sma(length=lenght[2], offset=offset[2])
        indicator = []
        for i in range(len(data)):
            if math.isnan(jaw[i]) or math.isnan(teeth[i]) or math.isnan(lips[i]):
                indicator.append(0)  # Нет достаточных данных для расчета
            elif lips[i] > teeth[i] and teeth[i] > jaw[i]:
                indicator.append(2)  # Покупка, аллигатор просыпается
            elif lips[i] < teeth[i] and teeth[i] < jaw[i]:
                indicator.append(1)  # Продажа, аллигатор засыпает
            else:
                indicator.append(0)  # Ничего, аллигатор спит
        return indicator

    @staticmethod
    def rebuild(array_data) -> list[Literal[0, 1, 2]]:
        repeat_val = array_data[0]
        for i in range(len(array_data) - 1):
            if repeat_val == 1:
                if repeat_val == array_data[i + 1]:
                    array_data[i + 1] = 0
                else:
                    repeat_val = array_data[i + 1]
            elif repeat_val == 2:
                array_data[i] = 0
                if repeat_val == array_data[i + 1]:
                    array_data[i + 1] = 0
                elif array_data[i + 1] != repeat_val:
                    array_data[i] = 2
                    repeat_val = array_data[i + 1]
            elif repeat_val == 0:
                repeat_val = array_data[i + 1]
        return array_data

    def make_prediction(self, data) -> tuple[Literal[1, 2, 3], Decimal]:
        logger.debug("Making prediction for %s", self.instrument_code)
        data["indicator_rsi"] = self.indicator_rsi(data)
        data["indicator_alligator"] = self.indicator_alligator(data)
        data["indicator_rsi"] = self.rebuild(data["indicator_rsi"].values)
        prediction = max(
            data["indicator_rsi"].iloc[-1], data["indicator_alligator"].iloc[-1]
        )
        deal_price = data["close"].iloc[-1]

        return prediction, deal_price




def run_bot():
    bot = Bot(user_id="332097ee-807e-4958-b053-1bbf8c35e846", instrument_code="SBER", status= True, balance = 10_000)
    candles = bot.get_candles()
    if not candles.equals(bot.candles):
        bot.candles = candles
        desision, price = bot.make_prediction(candles)
        if desision == 1 and bot.in_stock > 0:
            bot.sell_request(price)
        elif desision == 2:
            quantity = bot.balance // price
            if quantity > 0:
                bot.buy_request(price, quantity)

