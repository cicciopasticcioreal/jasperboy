from dataclasses import dataclass
import logging
from typing import List

import pandas as pd

from .data import DataFetcher
from .strategy import SimpleMovingAverageStrategy, TradeSignal

logging.basicConfig(level=logging.INFO)

@dataclass
class Position:
    symbol: str
    side: str
    amount: float
    entry_price: float
    take_profit: float
    stop_loss: float

class Trader:
    def __init__(self, exchange_id: str = "binance"):
        self.fetcher = DataFetcher(exchange_id)
        self.strategy = SimpleMovingAverageStrategy()
        self.positions: List[Position] = []

    def select_pairs(self) -> List[str]:
        markets = self.fetcher.list_markets()
        return [m for m in markets if m.endswith('/USDT')][:5]

    def check_signal(self, symbol: str) -> TradeSignal:
        df = self.fetcher.fetch_ohlcv(symbol)
        return self.strategy.generate(df, symbol)

    def open_position(self, signal: TradeSignal, amount: float = 0.01):
        ticker = self.fetcher.exchange.fetch_ticker(signal.symbol)
        price = ticker['last']
        tp = price * 1.02  # 2% take profit
        sl = price * 0.98  # 2% stop loss
        pos = Position(signal.symbol, signal.action, amount, price, tp, sl)
        logging.info(f"Opened {pos.side} position on {pos.symbol} at {price}")
        self.positions.append(pos)

    def run(self):
        for symbol in self.select_pairs():
            signal = self.check_signal(symbol)
            if signal.action in ('buy', 'sell'):
                self.open_position(signal)
